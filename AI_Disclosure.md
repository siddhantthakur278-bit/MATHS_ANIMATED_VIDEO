# AI Tools Disclosure

In accordance with academic integrity requirements for the Linear Algebra and Calculus (M3) Internal Assessment Project, this document discloses all AI tools used during the creation of this project.

## Tools Used & Scope of Assistance

1. **Google Antigravity (AI Coding & Engineering Assistant)**
   - Assisted with structuring the Python/Manim project (`E25B070826_Code/`), drafting modular scene classes, debugging LaTeX/rendering issues, and organizing documentation (`README.md`, `Storyboard.pdf`, `Viva_Prep.md`).
   - Assisted in refining the conversational flow and timing of `narration_script.md` to fit the 5-minute target duration.
   - All mathematical derivations and numerical results were independently verified using SymPy and NumPy (`verify_math.py`), and all visual frames and code were reviewed and understood by the student for viva defense.

2. **Text-to-Speech (TTS) & Voice Cloning Engine**
   - **F5-TTS-MLX (`lucasnewman/f5-tts-mlx`, offline Apple Silicon zero-shot voice cloning)** via `manim-voiceover`, conditioned on a 13.25-second voice sample recorded by the student (`SIDDHANT KUMAR THAKUR`), to synthesize narration for all 6 scenes from `narration_script.md` (with `Kokoro ONNX` configured as offline fallback).

## Authorship & Originality Statement

- All Manim animation scripts were written originally for this specific project (`A = [[2, 1], [1, 2]]`) and do not copy code from 3Blue1Brown or any external animation repository.
- No background music was used; audio consists solely of voice-over narration.
- References cited (such as 3Blue1Brown's *Essence of Linear Algebra* and Gilbert Strang's *Introduction to Linear Algebra*) are genuine, verified sources used strictly for conceptual inspiration and textbook grounding.
