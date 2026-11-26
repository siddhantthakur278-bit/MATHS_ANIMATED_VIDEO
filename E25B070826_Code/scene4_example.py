"""Scene 4: Worked Example — Full step-by-step algebra & geometric singularity check."""

from manim import (
    ApplyMatrix,
    Arrow,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    Flash,
    GrowArrow,
    LaggedStart,
    LEFT,
    MathTex,
    NumberPlane,
    ORIGIN,
    Polygon,
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
    ACCENT_GREEN,
    ACCENT_RED,
    AXIS_COLOR,
    BG_COLOR,
    EIG1_COLOR,
    EIG2_COLOR,
    GRID_FADED,
    GRID_MAIN,
    MATH_SCALE,
    ORD_VEC_COLOR,
    PANEL_BG,
    PANEL_BORDER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TRANS_VEC_COLOR,
)
from helpers.visuals import make_card, make_scene_header
from helpers.voice import get_speech_service


class Scene4WorkedExample(VoiceoverScene):
    """Step-by-step algebraic derivation for A = [[2, 1], [1, 2]] with singularity diagram."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        self.set_speech_service(get_speech_service())

        header = make_scene_header("Worked Example: Algebraic Solution", "A = [[2,1],[1,2]]")
        self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.6)

        # =====================================================================
        # PART 4A: Rearranging Av = lambda*v & WHY det(A - lambda*I) = 0
        # =====================================================================
        step1 = MathTex(r"A\mathbf{v}", r"=", r"\lambda", r"\mathbf{v}").scale(1.1)
        step2 = MathTex(r"A\mathbf{v}", r"=", r"\lambda I", r"\mathbf{v}").scale(1.1)
        step3 = MathTex(r"(A - \lambda I)\mathbf{v} = \mathbf{0}", r",\quad \mathbf{v} \neq \mathbf{0}").scale(1.05)

        step1.move_to(LEFT * 3.4 + UP * 1.9)
        step2.move_to(LEFT * 3.4 + UP * 0.9)
        step3.move_to(LEFT * 3.4 + DOWN * 0.15)
        step3_box = SurroundingRectangle(step3, color=TRANS_VEC_COLOR, buff=0.16, corner_radius=0.1, stroke_width=1.8)

        det_reason = VGroup(
            Text("Why det(A - lambda I) = 0 ?", font_size=23, color=TRANS_VEC_COLOR, weight="BOLD"),
            Text("If (A - lambda I) were invertible,", font_size=20, color=TEXT_MUTED),
            Text("only v = 0 solves (A - lambda I)v = 0.", font_size=20, color=TEXT_MUTED),
            Text("For v ≠ 0, matrix must be SINGULAR:", font_size=20, color=TEXT_PRIMARY),
            MathTex(r"\det(A - \lambda I) = 0", color=ACCENT_GREEN).scale(1.05),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        det_reason_card = make_card(det_reason, pad=0.22, stroke_color=PANEL_BORDER)
        det_reason_card.move_to(LEFT * 3.4 + DOWN * 1.95)

        # Right side: Animated Singularity Diagram (squishing 2D plane onto 1D line)
        sing_plane = NumberPlane(
            x_range=(-2.5, 2.5, 1),
            y_range=(-2.5, 2.5, 1),
            x_length=4.6,
            y_length=4.2,
            background_line_style={"stroke_color": GRID_MAIN, "stroke_width": 1.1, "stroke_opacity": 0.65},
            faded_line_style={"stroke_color": GRID_FADED, "stroke_width": 0.6, "stroke_opacity": 0.3},
            axis_config={"stroke_color": AXIS_COLOR, "stroke_width": 1.8, "include_numbers": False},
        )
        sing_plane.move_to(RIGHT * 3.2 + DOWN * 0.25)
        sing_frame = RoundedRectangle(
            corner_radius=0.18,
            width=5.2,
            height=5.0,
            stroke_color=ACCENT_GREEN,
            stroke_width=1.6,
            fill_color=PANEL_BG,
            fill_opacity=0.45,
        ).move_to(RIGHT * 3.2 + DOWN * 0.05)
        sing_title = Text("Singular Map: det = 0", font_size=22, color=ACCENT_GREEN, weight="BOLD")
        sing_title.next_to(sing_frame.get_top(), DOWN, buff=0.18)

        # Unit square & nonzero null-space vector (1, 1) inside sing_plane
        # Note: sing_plane center is at RIGHT*3.2 + DOWN*0.25, scale_x = 4.6/5 = 0.92, scale_y = 4.2/5 = 0.84
        sq_pts = [sing_plane.c2p(0, 0), sing_plane.c2p(1, 0), sing_plane.c2p(1, 1), sing_plane.c2p(0, 1)]
        sing_square = Polygon(*sq_pts, color=ORD_VEC_COLOR, fill_color=ORD_VEC_COLOR, fill_opacity=0.3, stroke_width=2.2)

        # Under singular matrix M = [[-1, 1], [1, -1]]:
        # (0,0)->(0,0), (1,0)->(-1,1), (1,1)->(0,0), (0,1)->(1,-1)
        squished_pts = [sing_plane.c2p(0, 0), sing_plane.c2p(-1, 1), sing_plane.c2p(0, 0), sing_plane.c2p(1, -1)]
        squished_line = Polygon(*squished_pts, color=ACCENT_GREEN, fill_color=ACCENT_GREEN, fill_opacity=0.35, stroke_width=3.5)

        null_vec = Arrow(sing_plane.c2p(0, 0), sing_plane.c2p(1, 1), buff=0, color=EIG1_COLOR, stroke_width=5)
        null_lbl = MathTex(r"\mathbf{v} \neq \mathbf{0}", color=EIG1_COLOR).scale(0.85).next_to(null_vec.get_end(), UP + RIGHT * 0.1, buff=0.08)
        zero_dot = Dot(sing_plane.c2p(0, 0), color=EIG1_COLOR, radius=0.1)
        collapse_lbl = Text("v collapses to 0!", font_size=20, color=EIG1_COLOR).next_to(sing_frame.get_bottom(), UP, buff=0.18)

        cue_4a = (
            "Now let us find those exact numbers algebraically for A equals two, one, one, two. "
            "Start from the definition: A v equals lambda v. Insert the identity matrix I so we can factor out v, "
            "giving A minus lambda I, all times v, equals zero. "
            "Why must the determinant of A minus lambda I equal zero? Because we need a nonzero vector v. "
            "If this matrix were invertible, the only solution would be v equals zero. "
            "Setting the determinant to zero makes the matrix singular, squishing space so a nonzero direction collapses to zero."
        )
        with self.voiceover(text=cue_4a) as tracker:
            self.play(Write(step1), run_time=1.0)
            self.wait(0.8)
            self.play(TransformMatchingTex(step1.copy(), step2), run_time=1.2)
            self.wait(0.6)
            self.play(Write(step3), Create(step3_box), run_time=1.3)
            self.play(
                FadeIn(sing_frame),
                Create(sing_plane),
                FadeIn(sing_title),
                Create(sing_square),
                GrowArrow(null_vec),
                FadeIn(null_lbl),
                run_time=1.6,
            )
            self.play(FadeIn(det_reason_card, shift=UP * 0.15), run_time=1.4)
            self.wait(1.0)
            # Squish the square and collapse null_vec to 0!
            self.play(
                Transform(sing_square, squished_line),
                Transform(null_vec, zero_dot),
                FadeOut(null_lbl),
                FadeIn(collapse_lbl),
                run_time=2.2,
            )
            self.play(Flash(zero_dot, color=EIG1_COLOR, flash_radius=0.4), run_time=0.8)
            self.wait(max(0.4, tracker.duration - 11.9))

        self.play(
            FadeOut(
                VGroup(
                    step1,
                    step2,
                    step3,
                    step3_box,
                    det_reason_card,
                    sing_frame,
                    sing_plane,
                    sing_title,
                    sing_square,
                    null_vec,
                    collapse_lbl,
                )
            ),
            run_time=0.6,
        )

        # =====================================================================
        # PART 4B: Characteristic Equation & Eigenvalues (One line at a time)
        # =====================================================================
        c1 = MathTex(
            r"A - \lambda I = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} - \lambda \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 2 - \lambda & 1 \\ 1 & 2 - \lambda \end{bmatrix}",
            color=TEXT_PRIMARY,
        ).scale(1.0)
        c2 = MathTex(
            r"\det(A - \lambda I) = (2 - \lambda)(2 - \lambda) - (1)(1) = 0",
            color=TEXT_PRIMARY,
        ).scale(1.0)
        c3 = MathTex(
            r"(2 - \lambda)^2 - 1 = 4 - 4\lambda + \lambda^2 - 1 = 0",
            color=TEXT_MUTED,
        ).scale(1.0)
        c4 = MathTex(r"\lambda^2 - 4\lambda + 3 = 0", color=TRANS_VEC_COLOR).scale(1.05)
        c5 = MathTex(r"(\lambda - 1)(\lambda - 3) = 0", color=TRANS_VEC_COLOR).scale(1.05)

        lam1_badge = make_card(MathTex(r"\lambda_1 = 3", color=EIG1_COLOR).scale(1.15), pad=0.2, stroke_color=EIG1_COLOR)
        lam2_badge = make_card(MathTex(r"\lambda_2 = 1", color=EIG2_COLOR).scale(1.15), pad=0.2, stroke_color=EIG2_COLOR)
        eigs_row = VGroup(lam1_badge, lam2_badge).arrange(RIGHT, buff=0.9)

        alg_stack = VGroup(c1, c2, c3, c4, c5, eigs_row).arrange(DOWN, buff=0.3)
        alg_stack.move_to(ORIGIN + DOWN * 0.25)

        cue_4b = (
            "Subtracting lambda along the diagonal gives two minus lambda, one, one, two minus lambda. "
            "Its determinant is two minus lambda squared, minus one. "
            "Expanding gives lambda squared minus four lambda plus three equals zero. "
            "Factoring into lambda minus one times lambda minus three equals zero yields two eigenvalues: "
            "lambda one equals three, and lambda two equals one."
        )
        with self.voiceover(text=cue_4b) as tracker:
            self.play(Write(c1), run_time=2.0)
            self.wait(0.8)
            self.play(Write(c2), run_time=1.8)
            self.wait(0.8)
            self.play(Write(c3), run_time=1.8)
            self.wait(0.6)
            self.play(Write(c4), run_time=1.4)
            self.wait(0.6)
            self.play(Write(c5), run_time=1.4)
            self.wait(0.6)
            self.play(FadeIn(eigs_row, shift=UP * 0.15), run_time=1.2)
            self.wait(max(0.4, tracker.duration - 13.0))

        self.play(FadeOut(alg_stack), run_time=0.6)

        # =====================================================================
        # PART 4C: Solve Each Null Space & Verify by Substitution
        # =====================================================================
        # Left column: lambda1 = 3 (orange)
        l_hdr = MathTex(r"\text{Case 1: } \lambda_1 = 3", color=EIG1_COLOR).scale(1.05)
        l_eq1 = MathTex(r"(A - 3I)\mathbf{v} = \mathbf{0}").scale(0.95)
        l_eq2 = MathTex(r"\begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}").scale(0.95)
        l_eq3 = MathTex(r"-x + y = 0 \implies y = x").scale(0.95)
        l_v = MathTex(r"\mathbf{v}_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}", color=EIG1_COLOR).scale(1.0)
        l_chk = MathTex(r"A\begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 3 \\ 3 \end{bmatrix} = 3\begin{bmatrix} 1 \\ 1 \end{bmatrix}", color=ACCENT_GREEN).scale(0.92)
        left_col = VGroup(l_hdr, l_eq1, l_eq2, l_eq3, l_v, l_chk).arrange(DOWN, buff=0.22)
        left_card = make_card(left_col, pad=0.25, stroke_color=EIG1_COLOR)
        left_card.move_to(LEFT * 3.35 + DOWN * 0.25)

        # Right column: lambda2 = 1 (teal)
        r_hdr = MathTex(r"\text{Case 2: } \lambda_2 = 1", color=EIG2_COLOR).scale(1.05)
        r_eq1 = MathTex(r"(A - 1I)\mathbf{v} = \mathbf{0}").scale(0.95)
        r_eq2 = MathTex(r"\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}").scale(0.95)
        r_eq3 = MathTex(r"x + y = 0 \implies y = -x").scale(0.95)
        r_v = MathTex(r"\mathbf{v}_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=EIG2_COLOR).scale(1.0)
        r_chk = MathTex(r"A\begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 1 \\ -1 \end{bmatrix} = 1\begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=ACCENT_GREEN).scale(0.92)
        right_col = VGroup(r_hdr, r_eq1, r_eq2, r_eq3, r_v, r_chk).arrange(DOWN, buff=0.22)
        right_card = make_card(right_col, pad=0.25, stroke_color=EIG2_COLOR)
        right_card.move_to(RIGHT * 3.35 + DOWN * 0.25)

        cue_4c = (
            "Let us solve for each eigenvector. "
            "For lambda one equals three, A minus three I has rows minus one, one and one, minus one. "
            "Both give minus x plus y equals zero, so y equals x, giving v one equals one, one. "
            "For lambda two equals one, A minus I has rows one, one and one, one, giving x plus y equals zero, "
            "so v two equals one, minus one. "
            "Substituting back confirms A times one, one equals three, three, and A times one, minus one equals one, minus one."
        )
        with self.voiceover(text=cue_4c) as tracker:
            self.play(FadeIn(left_card[0]), Write(l_hdr), run_time=0.9)
            self.play(Write(l_eq1), run_time=0.9)
            self.play(Write(l_eq2), run_time=1.4)
            self.play(Write(l_eq3), run_time=1.2)
            self.play(Write(l_v), run_time=1.0)
            self.wait(0.6)

            self.play(FadeIn(right_card[0]), Write(r_hdr), run_time=0.9)
            self.play(Write(r_eq1), run_time=0.9)
            self.play(Write(r_eq2), run_time=1.4)
            self.play(Write(r_eq3), run_time=1.2)
            self.play(Write(r_v), run_time=1.0)
            self.wait(0.6)

            # Verification by substitution
            self.play(Write(l_chk), Write(r_chk), run_time=1.8)
            self.wait(max(0.5, tracker.duration - 13.8))

        self.play(FadeOut(VGroup(header, left_card, right_card)), run_time=0.7)
