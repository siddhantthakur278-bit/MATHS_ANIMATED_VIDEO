"""Scene 5: Interpretation — Eigenbasis stretching & unit square -> parallelogram area."""

from manim import (
    ApplyMatrix,
    Arrow,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    Flash,
    GrowArrow,
    LEFT,
    MathTex,
    NumberPlane,
    Polygon,
    RIGHT,
    Text,
    Transform,
    UP,
    VGroup,
    Write,
)
from manim_voiceover import VoiceoverScene
import numpy as np

from helpers.config import (
    ACCENT_GREEN,
    AXIS_COLOR,
    BG_COLOR,
    EIG1_COLOR,
    EIG2_COLOR,
    GRID_FADED,
    GRID_MAIN,
    MATRIX_A,
    ORD_VEC_COLOR,
    PANEL_BORDER,
    SQUARE_COLOR,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TRANS_VEC_COLOR,
)
from helpers.visuals import make_axis_labels, make_card, make_eigen_lines, make_plane_vector, make_scene_header
from helpers.voice import get_speech_service


class Scene5Interpretation(VoiceoverScene):
    """Connect algebra back to geometry: eigen-stretching and determinant area scaling."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        self.set_speech_service(get_speech_service())

        header = make_scene_header("Geometric Interpretation", "Eigen-Stretch & Area")

        grid = NumberPlane(
            x_range=(-10, 10, 1),
            y_range=(-8, 8, 1),
            x_length=20,
            y_length=16,
            background_line_style={"stroke_color": GRID_MAIN, "stroke_width": 1.2, "stroke_opacity": 0.55},
            faded_line_style={"stroke_color": GRID_FADED, "stroke_width": 0.7, "stroke_opacity": 0.3},
            axis_config={"stroke_color": AXIS_COLOR, "stroke_width": 1.8, "include_numbers": False},
        )
        plane = NumberPlane(
            x_range=(-6, 6, 1),
            y_range=(-4, 4, 1),
            x_length=12,
            y_length=8,
            background_line_style={"stroke_opacity": 0},
            axis_config={
                "stroke_color": AXIS_COLOR,
                "stroke_width": 2.2,
                "include_numbers": True,
                "font_size": 20,
                "decimal_number_config": {"num_decimal_places": 0, "color": TEXT_MUTED},
            },
        )
        axis_labels = make_axis_labels(plane)
        eigen_lines = make_eigen_lines(plane)

        v1 = make_plane_vector(plane, (1, 1), color=EIG1_COLOR, stroke_width=5.5)
        v1_stretched = make_plane_vector(plane, (3, 3), color=EIG1_COLOR, stroke_width=5.5)
        v1_lbl = MathTex(r"\mathbf{v}_1 = (1,1)", color=EIG1_COLOR).scale(0.9).move_to(plane.c2p(1.9, 0.7))
        v1_out_lbl = MathTex(r"3\mathbf{v}_1 = (3,3)", color=EIG1_COLOR).scale(0.95).move_to(plane.c2p(4.2, 2.8))

        v2 = make_plane_vector(plane, (1, -1), color=EIG2_COLOR, stroke_width=5.5)
        v2_lbl = MathTex(r"\mathbf{v}_2 = (1,-1)", color=EIG2_COLOR).scale(0.9).move_to(plane.c2p(2.6, -0.85))

        stretch_card = make_card(
            VGroup(
                Text("Along eigen-directions:", font_size=21, color=TEXT_PRIMARY, weight="BOLD"),
                Text("Pure stretching (x3 and x1), NO rotation", font_size=20, color=TRANS_VEC_COLOR),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            pad=0.18,
            stroke_color=TRANS_VEC_COLOR,
        )
        stretch_card.to_corner(UP + LEFT, buff=0.45).shift(DOWN * 0.65)

        cue_5a = (
            "Putting the algebra back on our grid, the vector one, one lies right along the orange line y equals x, "
            "stretching by three. The vector one, minus one lies along the teal line y equals minus x, scaled by one. "
            "Along these eigen-directions, the transformation acts purely as stretching, with zero rotation."
        )
        with self.voiceover(text=cue_5a) as tracker:
            self.play(
                Create(grid, run_time=0.8),
                FadeIn(plane),
                FadeIn(axis_labels),
                FadeIn(header[0]),
                Create(eigen_lines),
            )
            self.play(
                GrowArrow(v1),
                FadeIn(v1_lbl),
                GrowArrow(v2),
                FadeIn(v2_lbl),
                run_time=1.4,
            )
            self.play(FadeIn(stretch_card, shift=RIGHT * 0.15), run_time=0.9)
            self.wait(0.8)
            self.play(
                Transform(v1, v1_stretched),
                Transform(v1_lbl, v1_out_lbl),
                Flash(plane.c2p(1, -1), color=EIG2_COLOR, flash_radius=0.35),
                run_time=2.0,
            )
            self.wait(max(0.5, tracker.duration - 5.9))

        # --- Cue 5B: Unit Square -> Parallelogram & Area Scaling ---
        unit_sq = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            color=SQUARE_COLOR,
            fill_color=SQUARE_COLOR,
            fill_opacity=0.35,
            stroke_width=2.8,
        )
        parallelogram = Polygon(
            plane.c2p(0, 0),
            plane.c2p(2, 1),
            plane.c2p(3, 3),
            plane.c2p(1, 2),
            color=SQUARE_COLOR,
            fill_color=SQUARE_COLOR,
            fill_opacity=0.35,
            stroke_width=3.0,
        )
        e1_arrow = make_plane_vector(plane, (1, 0), color=ORD_VEC_COLOR, stroke_width=4.0)
        e2_arrow = make_plane_vector(plane, (0, 1), color=ORD_VEC_COLOR, stroke_width=4.0)
        Ae1_arrow = make_plane_vector(plane, (2, 1), color=TRANS_VEC_COLOR, stroke_width=4.0)
        Ae2_arrow = make_plane_vector(plane, (1, 2), color=TRANS_VEC_COLOR, stroke_width=4.0)

        area_before = make_card(
            MathTex(r"\text{Unit Square Area} = 1", color=SQUARE_COLOR).scale(0.95),
            pad=0.16,
            stroke_color=SQUARE_COLOR,
        )
        area_before.to_corner(DOWN + LEFT, buff=0.45)

        area_after = make_card(
            VGroup(
                MathTex(r"\text{Parallelogram Area} = |\det(A)| = 3", color=ACCENT_GREEN).scale(0.95),
                MathTex(r"\det(A) = \lambda_1 \cdot \lambda_2 = 3 \times 1 = 3", color=TRANS_VEC_COLOR).scale(0.95),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            pad=0.18,
            stroke_color=ACCENT_GREEN,
        )
        area_after.to_corner(DOWN + RIGHT, buff=0.45)

        cue_5b = (
            "Now watch the unit square, which starts with area one. "
            "Under A, its basis edges one, zero and zero, one map to two, one and one, two, forming a parallelogram. "
            "Its area is the determinant of A, which equals three. "
            "Notice that three equals three times one, the product of our two eigenvalues!"
        )
        with self.voiceover(text=cue_5b) as tracker:
            self.play(
                Create(unit_sq),
                GrowArrow(e1_arrow),
                GrowArrow(e2_arrow),
                FadeIn(area_before, shift=UP * 0.15),
                run_time=1.4,
            )
            self.wait(1.0)
            self.play(
                ApplyMatrix(MATRIX_A, grid),
                Transform(unit_sq, parallelogram),
                Transform(e1_arrow, Ae1_arrow),
                Transform(e2_arrow, Ae2_arrow),
                run_time=2.6,
            )
            self.play(FadeIn(area_after, shift=UP * 0.2), run_time=1.2)
            self.wait(max(0.5, tracker.duration - 6.2))

        self.play(
            FadeOut(
                VGroup(
                    header[0],
                    grid,
                    plane,
                    axis_labels,
                    eigen_lines,
                    v1,
                    v1_lbl,
                    v2,
                    v2_lbl,
                    stretch_card,
                    unit_sq,
                    e1_arrow,
                    e2_arrow,
                    area_before,
                    area_after,
                )
            ),
            run_time=0.7,
        )
