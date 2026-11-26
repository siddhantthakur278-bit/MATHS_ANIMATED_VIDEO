"""Shared configuration, colors, matrix data, and typography for the M3 animation."""

import numpy as np

# Student & course metadata
COURSE_NAME = "Linear Algebra and Calculus (M3)"
PROJECT_TITLE = "Eigenvalues and Eigenvectors"
PROJECT_SUBTITLE = "Invariant Directions & Scaling Factors Under a Linear Transformation"
STUDENT_NAME = "SIDDHANT KUMAR THAKUR"
STUDENT_ID = "E25B070826"

LEARNING_OBJECTIVE = (
    "By the end of this video, the viewer will be able to explain what an "
    "eigenvector and eigenvalue are geometrically, and compute them for a 2x2 matrix."
)

# Worked example matrix A = [[2, 1], [1, 2]] (verified by verify_math.py)
MATRIX_A = np.array([[2, 1], [1, 2]], dtype=float)
MATRIX_A_INT = [[2, 1], [1, 2]]

LAMBDA_1 = 3
V1 = np.array([1, 1], dtype=float)

LAMBDA_2 = 1
V2 = np.array([1, -1], dtype=float)

DET_A = 3

# ── Black / charcoal / grey palette with vivid neon accents ─────────────────
BG_COLOR = "#080808"          # near-black background
PANEL_BG = "#111111"          # very dark charcoal card fill
PANEL_BORDER = "#3A3A3A"      # medium grey card border
GLOSS_HIGHLIGHT = "#FFFFFF"   # white gloss sheen (used at low opacity)

TEXT_PRIMARY = "#F0F0F0"      # near-white text
TEXT_MUTED = "#909090"        # mid-grey muted text

# Vivid neon accents — pop cleanly on a black background
EIG1_COLOR = "#FF8C42"        # Bright orange: v1 = (1,1), λ₁ = 3
EIG2_COLOR = "#00E5CC"        # Vivid teal: v2 = (1,-1), λ₂ = 1
ORD_VEC_COLOR = "#5BC0EB"     # Cyan-blue: ordinary input vectors
TRANS_VEC_COLOR = "#FFE033"   # Bright yellow: transformed vectors Av
SQUARE_COLOR = "#7DD3FC"      # Light sky-blue: unit square / parallelogram
GRID_MAIN = "#2A2A2A"         # dark grey main grid lines
GRID_FADED = "#181818"        # very dark faded grid lines
AXIS_COLOR = "#505050"        # charcoal grey axis lines
ACCENT_RED = "#FF5F7E"        # neon red
ACCENT_GREEN = "#39FF14"      # neon green

# Typography & scaling (keep MathTex >= 1.0 for crisp 1080p legibility)
TITLE_FONT_SIZE = 44
HEADING_FONT_SIZE = 34
BODY_FONT_SIZE = 24
SMALL_FONT_SIZE = 20
MATH_SCALE = 1.0
MATH_LARGE_SCALE = 1.15
