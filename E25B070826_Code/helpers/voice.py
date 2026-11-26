"""Voiceover SpeechService supporting F5-TTS-MLX voice cloning, Kokoro ONNX, edge-tts, and gTTS."""

import asyncio
import os
import re
import subprocess
from pathlib import Path
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService
from manim_voiceover.services.gtts import GTTSService

VENV_ROOT = Path(__file__).resolve().parent.parent.parent / ".venv"
DEFAULT_KOKORO_DIR = VENV_ROOT / "kokoro_models"
DEFAULT_F5_REF_WAV = VENV_ROOT / "f5_ref" / "siddhant_ref.wav"
DEFAULT_F5_REF_TEXT = (
    "Imagine the two-dimensional plane filled with vectors pointing in many directions. "
    "Almost every arrow tilts onto a new angle, except along special invariant lines."
)


class F5TTSSpeechService(SpeechService):
    """Offline zero-shot voice-cloning SpeechService powered by f5-tts-mlx."""

    def __init__(
        self,
        ref_audio_path: str | Path = DEFAULT_F5_REF_WAV,
        ref_text: str = DEFAULT_F5_REF_TEXT,
        model_name: str = "lucasnewman/f5-tts-mlx",
        speed: float = 0.98,
        steps: int = 8,
        cfg_strength: float = 2.0,
        seed: int = 42,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)
        self.ref_audio_path = Path(ref_audio_path)
        if not self.ref_audio_path.exists():
            raise FileNotFoundError(f"Reference voice sample not found: {self.ref_audio_path}")
        self.ref_text = ref_text
        self.model_name = model_name
        self.speed = speed
        self.steps = steps
        self.cfg_strength = cfg_strength
        self.seed = seed
        self._model = None
        self._ref_audio_mx = None

    def _ensure_loaded(self) -> None:
        if self._model is not None:
            return
        import mlx.core as mx
        import soundfile as sf
        from f5_tts_mlx.cfm import F5TTS
        from f5_tts_mlx.generate import SAMPLE_RATE, TARGET_RMS

        # Compatibility shim for mlx>=0.32 where mx.random.normal requires Python ints in shape
        if not getattr(mx.random.normal, "_int_shape_patched", False):
            _orig_normal = mx.random.normal

            def _safe_normal(shape=(), *args, **kwargs):
                if isinstance(shape, (tuple, list)):
                    shape = tuple(int(s.item()) if hasattr(s, "item") else int(s) for s in shape)
                return _orig_normal(shape, *args, **kwargs)

            _safe_normal._int_shape_patched = True
            mx.random.normal = _safe_normal

        audio, sr = sf.read(str(self.ref_audio_path))
        if sr != SAMPLE_RATE:
            raise ValueError(f"Reference audio must be {SAMPLE_RATE} Hz, got {sr} Hz")
        ref_mx = mx.array(audio)
        rms = mx.sqrt(mx.mean(mx.square(ref_mx)))
        if rms < TARGET_RMS:
            ref_mx = ref_mx * TARGET_RMS / rms

        self._ref_audio_mx = ref_mx
        self._model = F5TTS.from_pretrained(self.model_name)

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
            "service": "f5_tts_mlx",
            "ref": self.ref_audio_path.name,
            "speed": self.speed,
            "steps": self.steps,
            "seed": self.seed,
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

        self._ensure_loaded()
        import mlx.core as mx
        import numpy as np
        import soundfile as sf
        from f5_tts_mlx.generate import FRAMES_PER_SEC, SAMPLE_RATE, estimated_duration
        from f5_tts_mlx.utils import convert_char_to_pinyin

        spoken_text = re.sub(r"\bM3\b", "M three", input_text)
        sentences = [s.strip() for s in re.split(r"(?<=[.!?;:])\s+", spoken_text.strip()) if s.strip()]
        if not sentences:
            sentences = [spoken_text.strip()]

        chunks = []
        pause = mx.zeros((int(0.14 * SAMPLE_RATE),), dtype=mx.float32)
        for idx, sent in enumerate(sentences):
            if sent[-1] not in ".!?;:":
                sent += "."
            dur_frames = int(
                estimated_duration(self._ref_audio_mx, self.ref_text, sent, self.speed)
                * FRAMES_PER_SEC
            )
            pinyin = convert_char_to_pinyin([f"{self.ref_text} {sent}"])
            wave, _ = self._model.sample(
                mx.expand_dims(self._ref_audio_mx, axis=0),
                text=pinyin,
                duration=dur_frames,
                steps=self.steps,
                method="rk4",
                speed=self.speed,
                cfg_strength=self.cfg_strength,
                sway_sampling_coef=-1.0,
                seed=self.seed + idx,
            )
            wave = wave[self._ref_audio_mx.shape[0] :]
            mx.eval(wave)
            chunks.append(wave)
            if idx < len(sentences) - 1:
                chunks.append(pause)

        full_wave = mx.concatenate(chunks, axis=0)
        sf.write(str(tmp_wav), np.array(full_wave), SAMPLE_RATE)

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-i",
                str(tmp_wav),
                "-af",
                "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11",
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
    """Return cloned student voice (F5-TTS-MLX) if reference sample exists, else Kokoro/edge-tts/gTTS."""
    if DEFAULT_F5_REF_WAV.exists():
        try:
            return F5TTSSpeechService()
        except Exception:
            pass
    try:
        return KokoroSpeechService(voice="am_michael", speed=0.96, lang="en-us")
    except Exception:
        pass
    try:
        import edge_tts  # noqa: F401
        return EdgeTTSSpeechService(voice="en-US-AndrewMultilingualNeural", rate="-4%")
    except Exception:
        return GTTSService(lang="en", tld="com")
