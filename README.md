# M3 Linear Algebra & Calculus — Eigenvalues & Eigenvectors

**Student:** SIDDHANT KUMAR THAKUR  
**Student ID:** E25B070826  
**Course:** Linear Algebra and Calculus (M3) — Internal Assessment Project (Option 1: Animation Video)

---

## Concept Summary

An **eigenvector** of a square matrix $A$ is a nonzero vector $\mathbf{v}$ whose direction remains invariant under the linear transformation $T(\mathbf{x}) = A\mathbf{x}$, changing only by a scalar factor $\lambda$ (the **eigenvalue**):

$$A\mathbf{v} = \lambda\mathbf{v}, \quad \mathbf{v} \neq \mathbf{0}$$

This animation develops geometric intuition before algebra, then solves the complete worked example:

$$A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$$

- **Characteristic equation:** $\det(A - \lambda I) = (2 - \lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = (\lambda - 1)(\lambda - 3) = 0$
- **Eigenvalues & Eigenvectors:**
  - $\lambda_1 = 3 \implies \mathbf{v}_1 = (1, 1)$ along $y = x$ (vectors stretch $\times 3$)
  - $\lambda_2 = 1 \implies \mathbf{v}_2 = (1, -1)$ along $y = -x$ (vectors remain unchanged $\times 1$)
- **Geometric Interpretation:** The unit square transforms into a parallelogram whose area scales by $\det(A) = 3 = \lambda_1 \cdot \lambda_2$.

---

## Repository File Index

| File / Folder | Description |
|---|---|
| `E25B070826_Video.mp4` | Final 1080p (1920x1080, 30 fps) narrated MP4 animation |
| `Storyboard.pdf` | 1-page 6-scene storyboard with timing, visuals, narration, and math plan |
| `narration_script.md` | Full voice-over script across all 6 scenes with word counts and pacing |
| `AI_Disclosure.md` | Honest disclosure of AI tools and TTS engine used |
| `Viva_Prep.md` | Code walkthrough, full math derivations, 15 viva Q&As, and design choices |
| `E25B070826_Code/verify_math.py` | SymPy & NumPy verification of every equation and vector in the video |
| `E25B070826_Code/main.py` | CLI runner to render all 6 scenes at 1080p and assemble `E25B070826_Video.mp4` |
| `E25B070826_Code/scene1_hook.py` – `scene6_summary.py` | Six modular Manim `VoiceoverScene` classes |
| `E25B070826_Code/helpers/` | Shared constants (`config.py`), visual builders (`visuals.py`), and TTS (`voice.py`) |
| `E25B070826_Code/requirements.txt` | Python package dependencies |

---

## How to Verify & Render Locally

### Prerequisites
- Python 3.12+
- `ffmpeg`, `cairo`, `pango`, `sox`
- A LaTeX installation providing `latex` and `dvisvgm` (e.g., TinyTeX or TeX Live)

### Setup & Run
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r E25B070826_Code/requirements.txt

# 1. Verify all math with SymPy & NumPy
python E25B070826_Code/verify_math.py

# 2. Render all 6 scenes at 1080p30 and assemble E25B070826_Video.mp4
python E25B070826_Code/main.py -q h
```

---

## Tools Used, Credits & AI Disclosure

- **Animation Engine:** Manim Community Edition (`manim`)
- **Voiceover & TTS:** `manim-voiceover` with **Kokoro ONNX** offline neural TTS (`am_michael`)
- **Math Verification:** `SymPy` and `NumPy`
- **Storyboard PDF:** `ReportLab`
- **Music:** None (voice-only narration for clarity)
- **References:**
  - 3Blue1Brown, *Essence of Linear Algebra*, Chapter 14: "Eigenvectors and eigenvalues" (visual inspiration only; all code written from scratch)
  - Gilbert Strang, *Introduction to Linear Algebra* (5th ed.), Chapter 6
  - M3 Linear Algebra & Calculus Course Lecture Notes
- **AI Disclosure:** See [AI_Disclosure.md](AI_Disclosure.md) for full details on Google Antigravity assistance and TTS voice synthesis.
