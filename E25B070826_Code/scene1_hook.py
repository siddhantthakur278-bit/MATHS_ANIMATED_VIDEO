"""Scene 1: Hook / Context — Opening frame and the mystery of invariant directions."""

from manim import (
    ApplyMatrix,
    Arrow,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GrowArrow,
    LaggedStart,
    LEFT,
    MathTex,
    NumberPlane,
    ORIGIN,
    RIGHT,
    RoundedRectangle,
    Text,
    Transform,
    UP,
    VGroup,
    Write,
)
from manim_voiceover import VoiceoverScene
import numpy as np

from helpers.config import (
    AXIS_COLOR,
    BG_COLOR,
    BODY_FONT_SIZE,
    COURSE_NAME,
    EIG1_COLOR,
    EIG2_COLOR,
    GRID_FADED,
    GRID_MAIN,
    MATRIX_A,
    ORD_VEC_COLOR,
    PANEL_BG,
    PANEL_BORDER,
    PROJECT_SUBTITLE,
    PROJECT_TITLE,
    SMALL_FONT_SIZE,
    STUDENT_ID,
    STUDENT_NAME,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TITLE_FONT_SIZE,
    TRANS_VEC_COLOR,
)
from helpers.visuals import make_axis_labels, make_card, make_matrix_A, make_plane_vector
from helpers.voice import get_speech_service


class Scene1Hook(VoiceoverScene):
    """Opening title card + grid transformation hook."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        self.set_speech_service(get_speech_service())

        # --- Part 1A: Animated Opening Title Card ---
        course_lbl = Text(COURSE_NAME, font_size=SMALL_FONT_SIZE, color=EIG2_COLOR, weight="BOLD")
        title_lbl = Text(PROJECT_TITLE, font_size=52, color=TEXT_PRIMARY, weight="BOLD")
        subtitle_lbl = Text(PROJECT_SUBTITLE, font_size=24, color=TEXT_MUTED)

        # Mini animated diagram motif on title card: two invariant-direction arrows
        motif_origin = ORIGIN + DOWN * 0.45
        m_arrow1 = Arrow(motif_origin, motif_origin + np.array([1.1, 1.1, 0]), buff=0, color=EIG1_COLOR, stroke_width=5)
        m_arrow2 = Arrow(motif_origin, motif_origin + np.array([0.85, -0.85, 0]), buff=0, color=EIG2_COLOR, stroke_width=5)
        m_label = MathTex(r"A\mathbf{v} = \lambda\mathbf{v}", color=TRANS_VEC_COLOR).scale(1.15)
        m_label.next_to(VGroup(m_arrow1, m_arrow2), RIGHT, buff=0.6)
        motif = VGroup(m_arrow1, m_arrow2, m_label).move_to(ORIGIN + DOWN * 0.35)

        student_lbl = Text(
            f"Presented by: {STUDENT_NAME}   |   ID: {STUDENT_ID}",
            font_size=22,
            color=TEXT_PRIMARY,
        )

        title_stack = VGroup(course_lbl, title_lbl, subtitle_lbl).arrange(DOWN, buff=0.22)
        title_stack.to_edge(UP, buff=0.85)
        student_card = make_card(student_lbl, pad=0.2, stroke_color=EIG1_COLOR)
        student_card.to_edge(DOWN, buff=0.7)

        cue_1a = (
            "Welcome to this M3 Linear Algebra visual guide on eigenvalues and eigenvectors."
        )
        with self.voiceover(text=cue_1a):
            self.play(
                FadeIn(course_lbl, shift=DOWN * 0.2),
                Write(title_lbl, run_time=1.2),
                FadeIn(subtitle_lbl, shift=UP * 0.15),
            )
            self.play(
                GrowArrow(m_arrow1),
                GrowArrow(m_arrow2),
                Write(m_label),
                FadeIn(student_card, shift=UP * 0.2),
                run_time=1.4,
            )
            self.wait(0.6)

        # Smooth transition from Title Card to Coordinate Plane
        self.play(
            FadeOut(title_stack, shift=UP * 0.3),
            FadeOut(motif, scale=0.85),
            FadeOut(student_card, shift=DOWN * 0.3),
            run_time=0.7,
        )

        # --- Part 1B: Plane, Arrows, and Linear Transformation Hook ---
        # Oversized background grid (1:1 scene coords) + labeled primary axes
        grid = NumberPlane(
            x_range=(-10, 10, 1),
            y_range=(-8, 8, 1),
            x_length=20,
            y_length=16,
            background_line_style={
                "stroke_color": GRID_MAIN,
                "stroke_width": 1.3,
                "stroke_opacity": 0.7,
            },
            faded_line_style={
                "stroke_color": GRID_FADED,
                "stroke_width": 0.8,
                "stroke_opacity": 0.35,
            },
            faded_line_ratio=2,
            axis_config={"stroke_color": AXIS_COLOR, "stroke_width": 2.0, "include_numbers": False},
        )
        static_axes = NumberPlane(
            x_range=(-6, 6, 1),
            y_range=(-4, 4, 1),
            x_length=12,
            y_length=8,
            background_line_style={"stroke_opacity": 0},
            axis_config={
                "stroke_color": AXIS_COLOR,
                "stroke_width": 2.4,
                "include_numbers": True,
                "font_size": 20,
                "decimal_number_config": {"num_decimal_places": 0, "color": TEXT_MUTED},
            },
        )
        axis_labels = make_axis_labels(static_axes)

        # Sample vectors around the plane (ordinary + two hidden eigen-directions)
        sample_coords = [
            (1.6, 0.0),
            (1.1, 0.4),
            (0.0, 1.4),
            (-1.4, 1.4),   # along y = -x (eigen-direction)
            (-0.9, 1.5),
            (-1.3, -0.3),
            (-0.8, -0.8),  # along y = x (eigen-direction)
            (0.5, -1.2),
            (1.0, 1.0),    # along y = x (eigen-direction)
            (1.4, -1.4),   # along y = -x (eigen-direction)
        ]
        arrows = VGroup(*[make_plane_vector(static_axes, c, color=ORD_VEC_COLOR) for c in sample_coords])
        transformed_arrows = VGroup(
            *[
                make_plane_vector(static_axes, MATRIX_A @ np.array(c), color=TRANS_VEC_COLOR)
                for c in sample_coords
            ]
        )

        mat_card = make_card(make_matrix_A(scale=1.05), pad=0.22, stroke_color=ORD_VEC_COLOR)
        mat_card.to_corner(UP + LEFT, buff=0.4)

        question_txt = Text(
            "Is there any direction that survives without rotating?",
            font_size=26,
            color=TRANS_VEC_COLOR,
            weight="BOLD",
        )
        question_card = make_card(question_txt, pad=0.22, stroke_color=TRANS_VEC_COLOR)
        question_card.to_edge(DOWN, buff=0.4)

        cue_1b = (
            "Imagine the two-dimensional plane filled with vectors pointing in many directions. "
            "Now let us apply the matrix A, with entries two, one, one, two, to the entire plane. "
            "Watch closely as the grid warps. Almost every arrow tilts onto a completely new angle. "
            "That raises a natural question: is there any direction that survives the transformation without rotating?"
        )
        with self.voiceover(text=cue_1b) as tracker:
            self.play(
                Create(grid, run_time=1.0),
                FadeIn(static_axes),
                FadeIn(axis_labels),
                FadeIn(mat_card, shift=DOWN * 0.2),
            )
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=2.2)
            self.wait(0.8)
            # Apply the matrix transformation to both the grid and arrows cleanly
            self.play(
                ApplyMatrix(MATRIX_A, grid),
                *[Transform(a, ta) for a, ta in zip(arrows, transformed_arrows)],
                run_time=3.2,
            )
            self.wait(1.0)
            self.play(FadeIn(question_card, shift=UP * 0.2), run_time=0.9)
            remaining = max(0.5, tracker.duration - 9.1)
            self.wait(remaining)

        self.play(
            FadeOut(VGroup(grid, static_axes, axis_labels, arrows, mat_card, question_card)),
            run_time=0.7,
        )
