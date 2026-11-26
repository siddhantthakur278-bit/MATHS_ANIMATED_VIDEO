"""Main entry point to render all 6 scenes and assemble E25B070826_Video.mp4."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCENES = [
    ("scene1_hook.py", "Scene1Hook"),
    ("scene2_concept.py", "Scene2Concept"),
    ("scene3_intuition.py", "Scene3Intuition"),
    ("scene4_example.py", "Scene4WorkedExample"),
    ("scene5_interpretation.py", "Scene5Interpretation"),
    ("scene6_summary.py", "Scene6SummaryCredits"),
]

QUALITY_FLAGS = {
    "l": ("-ql", "480p15"),
    "m": ("-qm", "720p30"),
    "h": ("-qh", "1080p30"),
}


def run_cmd(cmd: list[str], env: dict[str, str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, env=env, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render and concatenate M3 Eigenvalues video.")
    parser.add_argument("-q", "--quality", choices=["l", "m", "h"], default="h", help="Render quality (default: h = 1080p30)")
    parser.add_argument("--scene", type=int, choices=range(1, 7), help="Render only scene N (1-6) without final concat")
    parser.add_argument("--concat-only", action="store_true", help="Skip rendering and concatenate existing scene MP4s")
    args = parser.parse_args()

    code_dir = Path(__file__).resolve().parent
    repo_root = code_dir.parent
    manim_bin = Path(sys.executable).parent / "manim"
    q_flag, q_dir = QUALITY_FLAGS[args.quality]

    env = os.environ.copy()
    tinytex_bin = str(Path.home() / "Library" / "TinyTeX" / "bin" / "universal-darwin")
    env["PATH"] = f"{tinytex_bin}:{env.get('PATH', '')}"

    if not args.concat_only:
        targets = [SCENES[args.scene - 1]] if args.scene else SCENES
        for filename, cls_name in targets:
            run_cmd(
                [str(manim_bin), q_flag, "--fps", "30", str(code_dir / filename), cls_name],
                env=env,
            )

    if args.scene:
        return

    # Concatenate all 6 scene MP4s cleanly with ffmpeg
    scene_mp4s = []
    for filename, cls_name in SCENES:
        stem = Path(filename).stem
        mp4 = code_dir / "media" / "videos" / stem / q_dir / f"{cls_name}.mp4"
        if not mp4.exists():
            raise FileNotFoundError(f"Missing rendered scene MP4: {mp4}")
        scene_mp4s.append(mp4)

    concat_list = code_dir / "media" / "concat_list.txt"
    concat_list.parent.mkdir(parents=True, exist_ok=True)
    concat_list.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in scene_mp4s) + "\n",
        encoding="utf-8",
    )

    out_mp4 = repo_root / "E25B070826_Video.mp4"
    # Re-encode cleanly with libx264 (-crf 21, yuv420p) + AAC 192k so timestamps & audio streams are seamless
    run_cmd(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c:v",
            "libx264",
            "-crf",
            "21",
            "-preset",
            "medium",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(out_mp4),
        ],
        env=env,
    )
    print(f"\nAssembled final video: {out_mp4}")


if __name__ == "__main__":
    main()
