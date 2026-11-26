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

# Consistent color palette (dark slate background with high-contrast accents)
BG_COLOR = "#0B1120"
PANEL_BG = "#111C33"
PANEL_BORDER = "#334155"

TEXT_PRIMARY = "#F8FAFC"
TEXT_MUTED = "#CBD5E1"

EIG1_COLOR = "#FB923C"      # Orange: v1 = (1, 1), lambda1 = 3
EIG2_COLOR = "#2DD4BF"      # Teal:   v2 = (1, -1), lambda2 = 1
ORD_VEC_COLOR = "#60A5FA"   # Blue-grey: ordinary input vectors v
TRANS_VEC_COLOR = "#FACC15" # Yellow: transformed output vectors Av
SQUARE_COLOR = "#38BDF8"    # Sky cyan: unit square / parallelogram
GRID_MAIN = "#334155"
GRID_FADED = "#1E293B"
AXIS_COLOR = "#94A3B8"
ACCENT_RED = "#F87171"
ACCENT_GREEN = "#4ADE80"

# Typography & scaling (keep MathTex >= 1.0 for crisp 1080p legibility)
TITLE_FONT_SIZE = 44
HEADING_FONT_SIZE = 34
BODY_FONT_SIZE = 24
SMALL_FONT_SIZE = 20
MATH_SCALE = 1.0
MATH_LARGE_SCALE = 1.15
