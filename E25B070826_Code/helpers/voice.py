"""Voiceover SpeechService using Kokoro ONNX (offline) with edge-tts / gTTS fallbacks."""

import asyncio
import os
import subprocess
from pathlib import Path
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService
from manim_voiceover.services.gtts import GTTSService

DEFAULT_KOKORO_DIR = (
    Path(__file__).resolve().parent.parent.parent / ".venv" / "kokoro_models"
)


class KokoroSpeechService(SpeechService):
    """Offline neural TTS SpeechService powered by kokoro-onnx."""

    def __init__(
        self,
        model_path: str | Path | None = None,
        voices_path: str | Path | None = None,
        voice: str = "am_michael",
        speed: float = 0.96,
        lang: str = "en-us",
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)
        from kokoro_onnx import Kokoro

        model_dir = DEFAULT_KOKORO_DIR
        self.model_path = Path(model_path) if model_path else model_dir / "kokoro-v1.0.onnx"
        self.voices_path = Path(voices_path) if voices_path else model_dir / "voices-v1.0.bin"
        if not self.model_path.exists() or not self.voices_path.exists():
            raise FileNotFoundError(
                f"Kokoro models not found at {self.model_path} / {self.voices_path}"
            )
        self.kokoro = Kokoro(str(self.model_path), str(self.voices_path))
        self.voice = voice
        self.speed = speed
        self.lang = lang

    def generate_from_text(
        self,
        text: str,
        cache_dir: str | Path | None = None,
        path: str | Path | None = None,
        **kwargs: object,
    ) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir
        Path(cache_dir).mkdir(parents=True, exist_ok=True)

        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "kokoro_onnx",
            "voice": self.voice,
            "speed": self.speed,
        }
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached

        if path is None:
            audio_name = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_name = os.fspath(path)

        out_mp3 = Path(cache_dir) / audio_name
        tmp_wav = out_mp3.with_suffix(".tmp.wav")

        import soundfile as sf

        samples, sample_rate = self.kokoro.create(
            input_text,
            voice=self.voice,
            speed=self.speed,
            lang=self.lang,
        )
        sf.write(str(tmp_wav), samples, sample_rate)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-i",
                str(tmp_wav),
                "-c:a",
                "libmp3lame",
                "-b:a",
                "192k",
                str(out_mp3),
            ],
            check=True,
        )
        tmp_wav.unlink(missing_ok=True)

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_name,
        }


class EdgeTTSSpeechService(SpeechService):
    """Fallback neural TTS using Microsoft edge-tts."""

    def __init__(self, voice: str = "en-US-AndrewMultilingualNeural", rate: str = "-4%", **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.voice = voice
        self.rate = rate

    def generate_from_text(
        self,
        text: str,
        cache_dir: str | Path | None = None,
        path: str | Path | None = None,
        **kwargs: object,
    ) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir
        Path(cache_dir).mkdir(parents=True, exist_ok=True)

        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "edge_tts",
            "voice": self.voice,
            "rate": self.rate,
        }
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached

        if path is None:
            audio_name = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_name = os.fspath(path)

        out_mp3 = Path(cache_dir) / audio_name

        async def _run() -> None:
            import edge_tts
            communicate = edge_tts.Communicate(input_text, self.voice, rate=self.rate)
            await communicate.save(str(out_mp3))

        asyncio.run(_run())

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_name,
        }


def get_speech_service() -> SpeechService:
    """Return Kokoro ONNX if available, falling back to edge-tts then gTTS."""
    try:
        return KokoroSpeechService(voice="am_michael", speed=0.96, lang="en-us")
    except Exception:
        pass
    try:
        import edge_tts  # noqa: F401
        return EdgeTTSSpeechService(voice="en-US-AndrewMultilingualNeural", rate="-4%")
    except Exception:
        return GTTSService(lang="en", tld="com")
