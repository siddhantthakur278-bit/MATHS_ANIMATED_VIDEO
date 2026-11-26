"""Scene 2: Concept Introduction — Linear maps, Av = lambda*v, notation, and objective."""

from manim import (
    Arc,
    Arrow,
    Create,
    DashedLine,
    DOWN,
    FadeIn,
    FadeOut,
    GrowArrow,
    LaggedStart,
    LEFT,
    Line,
    MathTex,
    NumberPlane,
    RIGHT,
    RoundedRectangle,
    SurroundingRectangle,
    Text,
    Transform,
    TransformMatchingTex,
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
    EIG1_COLOR,
    EIG2_COLOR,
    GRID_FADED,
    GRID_MAIN,
    LEARNING_OBJECTIVE,
    MATH_LARGE_SCALE,
    MATH_SCALE,
    ORD_VEC_COLOR,
    PANEL_BG,
    PANEL_BORDER,
    SMALL_FONT_SIZE,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TRANS_VEC_COLOR,
)
from helpers.visuals import make_card, make_scene_header
from helpers.voice import get_speech_service


class Scene2Concept(VoiceoverScene):
    """Formal definition, symbol key, geometric contrast diagram, and learning objective."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        self.set_speech_service(get_speech_service())

        header = make_scene_header("What Is an Eigenvector?", "Concept & Notation")
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.6)

        # --- Left Panel: Animated Geometric Contrast Diagram ---
        mini_plane = NumberPlane(
            x_range=(-3.5, 3.5, 1),
            y_range=(-3.5, 3.5, 1),
            x_length=5.2,
            y_length=4.6,
            background_line_style={"stroke_color": GRID_MAIN, "stroke_width": 1.1, "stroke_opacity": 0.65},
            faded_line_style={"stroke_color": GRID_FADED, "stroke_width": 0.6, "stroke_opacity": 0.3},
            axis_config={"stroke_color": AXIS_COLOR, "stroke_width": 1.8, "include_numbers": False},
        )
        mini_plane.move_to(LEFT * 3.6 + UP * 0.15)
        plane_frame = RoundedRectangle(
            corner_radius=0.18,
            width=5.6,
            height=5.0,
            stroke_color=PANEL_BORDER,
            stroke_width=1.6,
            fill_color=PANEL_BG,
            fill_opacity=0.45,
        ).move_to(mini_plane.get_center())

        # Ordinary vector v = (1.2, 0.0) -> Av = (2.4, 1.2)
        origin_pt = mini_plane.c2p(0, 0)
        v_ord = Arrow(origin_pt, mini_plane.c2p(1.4, 0.0), buff=0, color=ORD_VEC_COLOR, stroke_width=4.5)
        av_ord = Arrow(origin_pt, mini_plane.c2p(2.6, 1.3), buff=0, color=TRANS_VEC_COLOR, stroke_width=4.5)
        v_ord_lbl = MathTex(r"\mathbf{x}", color=ORD_VEC_COLOR).scale(0.95).next_to(v_ord.get_end(), DOWN, buff=0.12)
        av_ord_lbl = MathTex(r"A\mathbf{x}", color=TRANS_VEC_COLOR).scale(0.95).next_to(av_ord.get_end(), UP, buff=0.12)

        angle_arc = Arc(
            radius=0.85,
            start_angle=0.0,
            angle=np.arctan2(1.3, 2.6),
            arc_center=origin_pt,
            color=TRANS_VEC_COLOR,
            stroke_width=2.8,
        )
        rot_tag = Text("Rotated!", font_size=20, color=TRANS_VEC_COLOR).move_to(mini_plane.c2p(1.4, 1.95))

        # Eigenvector case along y = x: v = (1, 1) -> Av = (2.6, 2.6) scaled cleanly inside mini_plane
        span_line = DashedLine(
            mini_plane.c2p(-2.8, -2.8),
            mini_plane.c2p(2.8, 2.8),
            color=EIG1_COLOR,
            stroke_width=2.2,
            dash_length=0.14,
        )
        v_eig = Arrow(origin_pt, mini_plane.c2p(0.9, 0.9), buff=0, color=EIG1_COLOR, stroke_width=5)
        av_eig = Arrow(origin_pt, mini_plane.c2p(2.5, 2.5), buff=0, color=TRANS_VEC_COLOR, stroke_width=4.2)
        v_eig_lbl = MathTex(r"\mathbf{v}", color=EIG1_COLOR).scale(1.0).next_to(mini_plane.c2p(0.9, 0.9), DOWN + RIGHT * 0.2, buff=0.1)
        av_eig_lbl = MathTex(r"A\mathbf{v} = \lambda\mathbf{v}", color=TRANS_VEC_COLOR).scale(0.9).move_to(mini_plane.c2p(1.75, 2.95))
        stay_tag = Text("Same direction!", font_size=20, color=EIG1_COLOR).move_to(mini_plane.c2p(-1.65, 2.35))

        # --- Right Panel: Equations & Symbol Definitions ---
        eq_linear = MathTex(r"T(\mathbf{x}) = A\mathbf{x}", color=TEXT_PRIMARY).scale(MATH_LARGE_SCALE)
        eq_eigen = MathTex(
            r"A", r"\mathbf{v}", r"=", r"\lambda", r"\mathbf{v}", r",\quad", r"\mathbf{v} \neq \mathbf{0}",
            color=TEXT_PRIMARY,
        ).scale(MATH_LARGE_SCALE)
        eq_eigen[1].set_color(EIG1_COLOR)
        eq_eigen[3].set_color(TRANS_VEC_COLOR)
        eq_eigen[4].set_color(EIG1_COLOR)

        eq_linear.move_to(RIGHT * 3.1 + UP * 2.05)
        eq_eigen.move_to(RIGHT * 3.1 + UP * 1.1)
        eigen_box = SurroundingRectangle(eq_eigen, color=EIG1_COLOR, buff=0.18, corner_radius=0.1, stroke_width=1.8)

        # Symbol definitions (define ALL notation before first use)
        def_rows = VGroup(
            VGroup(MathTex("A", color=TEXT_PRIMARY).scale(1.0), Text(": 2x2 transformation matrix", font_size=21, color=TEXT_MUTED)).arrange(RIGHT, buff=0.18),
            VGroup(MathTex("I", color=EIG2_COLOR).scale(1.0), Text(": 2x2 identity matrix", font_size=21, color=TEXT_MUTED)).arrange(RIGHT, buff=0.18),
            VGroup(MathTex(r"\mathbf{v}", color=EIG1_COLOR).scale(1.0), Text(": nonzero eigenvector", font_size=21, color=TEXT_MUTED)).arrange(RIGHT, buff=0.18),
            VGroup(MathTex(r"\lambda", color=TRANS_VEC_COLOR).scale(1.0), Text(": scalar eigenvalue (scale factor)", font_size=21, color=TEXT_MUTED)).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        def_card = make_card(def_rows, pad=0.22, stroke_color=PANEL_BORDER)
        def_card.move_to(RIGHT * 3.1 + DOWN * 0.7)

        cue_2a = (
            "A matrix A defines a linear transformation T of x equals A times x, moving each vector to a new position "
            "while keeping grid lines parallel and evenly spaced. An eigenvector is a nonzero vector v whose direction "
            "never changes under A. Instead, A times v equals lambda times v, where the scalar lambda is the eigenvalue "
            "that measures how much v stretches or shrinks."
        )
        with self.voiceover(text=cue_2a) as tracker:
            self.play(
                FadeIn(plane_frame),
                Create(mini_plane, run_time=0.9),
                Write(eq_linear, run_time=0.9),
            )
            self.play(
                GrowArrow(v_ord),
                FadeIn(v_ord_lbl),
                run_time=0.8,
            )
            self.play(
                GrowArrow(av_ord),
                FadeIn(av_ord_lbl),
                Create(angle_arc),
                FadeIn(rot_tag),
                run_time=1.3,
            )
            self.wait(1.0)
            # Transition ordinary vector into eigenvector staying on its span line
            self.play(
                FadeOut(VGroup(v_ord, av_ord, v_ord_lbl, av_ord_lbl, angle_arc, rot_tag)),
                Create(span_line),
                Write(eq_eigen),
                Create(eigen_box),
                run_time=1.4,
            )
            self.play(
                GrowArrow(v_eig),
                FadeIn(v_eig_lbl),
                run_time=0.8,
            )
            self.play(
                GrowArrow(av_eig),
                FadeIn(av_eig_lbl),
                FadeIn(stay_tag),
                run_time=1.2,
            )
            self.wait(max(0.5, tracker.duration - 7.4))

        # --- Cue 2B: Notation badges & Learning Objective ---
        obj_prefix = Text("Learning Objective: ", font_size=21, color=EIG2_COLOR, weight="BOLD")
        obj_body = Text(LEARNING_OBJECTIVE, font_size=20, color=TEXT_PRIMARY)
        # Wrap learning objective cleanly in two lines if needed using MarkupText or two Text lines
        obj_line1 = Text(
            "Learning Objective: By the end of this video, the viewer will be able to explain what an",
            font_size=20,
            color=TEXT_PRIMARY,
        )
        obj_line2 = Text(
            "eigenvector and eigenvalue are geometrically, and compute them for a 2x2 matrix.",
            font_size=20,
            color=TEXT_PRIMARY,
        )
        obj_group = VGroup(obj_line1, obj_line2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        obj_card = make_card(obj_group, pad=0.2, fill_color="#0F2942", stroke_color=EIG2_COLOR)
        obj_card.to_edge(DOWN, buff=0.25)

        cue_2b = (
            "Here, A is our two-by-two matrix, I is the identity matrix, v is a nonzero vector, and lambda is a real number. "
            "By the end of this video, you will be able to explain eigenvectors and eigenvalues geometrically, "
            "and compute them for a two-by-two matrix."
        )
        with self.voiceover(text=cue_2b) as tracker:
            self.play(
                FadeIn(def_card[0]),
                LaggedStart(*[FadeIn(row, shift=LEFT * 0.15) for row in def_rows], lag_ratio=0.25),
                run_time=2.5,
            )
            self.wait(0.8)
            self.play(FadeIn(obj_card, shift=UP * 0.25), run_time=1.0)
            self.wait(max(0.5, tracker.duration - 4.3))

        self.play(
            FadeOut(
                VGroup(
                    header,
                    plane_frame,
                    mini_plane,
                    span_line,
                    v_eig,
                    av_eig,
                    v_eig_lbl,
                    av_eig_lbl,
                    stay_tag,
                    eq_linear,
                    eq_eigen,
                    eigen_box,
                    def_card,
                    obj_card,
                )
            ),
            run_time=0.7,
        )
