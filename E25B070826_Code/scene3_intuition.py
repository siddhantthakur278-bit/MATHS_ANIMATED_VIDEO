"""Scene 3: Visual Intuition — ValueTracker unit-circle sweep and invariant lines."""

from manim import (
    always_redraw,
    ApplyMatrix,
    Arc,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    Flash,
    GrowArrow,
    LEFT,
    MathTex,
    NumberPlane,
    RIGHT,
    Text,
    Transform,
    UP,
    ValueTracker,
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
    PANEL_BG,
    PANEL_BORDER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TRANS_VEC_COLOR,
)
from helpers.visuals import make_axis_labels, make_card, make_eigen_lines, make_plane_vector, make_scene_header
from helpers.voice import get_speech_service


class Scene3Intuition(VoiceoverScene):
    """Discover invariant directions geometrically via a live angle-sweep diagram."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        self.set_speech_service(get_speech_service())

        header = make_scene_header("Visual Intuition: Zero Rotation", "Before Algebra")

        # Background grid to show initial transformation, plus static labeled axes for unit circle
        warped_grid = NumberPlane(
            x_range=(-10, 10, 1),
            y_range=(-8, 8, 1),
            x_length=20,
            y_length=16,
            background_line_style={"stroke_color": GRID_MAIN, "stroke_width": 1.1, "stroke_opacity": 0.45},
            faded_line_style={"stroke_color": GRID_FADED, "stroke_width": 0.6, "stroke_opacity": 0.25},
            axis_config={"stroke_color": AXIS_COLOR, "stroke_width": 1.6, "include_numbers": False},
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
        unit_circle = Circle(radius=1.0, color=ORD_VEC_COLOR, stroke_width=2.0, stroke_opacity=0.65)

        theta_tracker = ValueTracker(0.0)

        def get_v_vec(theta: float) -> np.ndarray:
            return np.array([np.cos(theta), np.sin(theta)])

        def get_av_vec(theta: float) -> np.ndarray:
            return MATRIX_A @ get_v_vec(theta)

        def get_angle_deg(theta: float) -> float:
            v = get_v_vec(theta)
            av = get_av_vec(theta)
            cos_a = np.clip(np.dot(v, av) / (np.linalg.norm(v) * np.linalg.norm(av)), -1.0, 1.0)
            return float(np.degrees(np.arccos(cos_a)))

        v_arrow = always_redraw(
            lambda: Arrow(
                plane.c2p(0, 0),
                plane.c2p(*get_v_vec(theta_tracker.get_value())),
                buff=0,
                color=ORD_VEC_COLOR,
                stroke_width=5.5,
                tip_length=0.22,
            )
        )
        av_arrow = always_redraw(
            lambda: Arrow(
                plane.c2p(0, 0),
                plane.c2p(*get_av_vec(theta_tracker.get_value())),
                buff=0,
                color=TRANS_VEC_COLOR,
                stroke_width=4.5,
                tip_length=0.22,
            )
        )

        def make_angle_sector():
            th = theta_tracker.get_value()
            v = get_v_vec(th)
            av = get_av_vec(th)
            a1 = float(np.arctan2(v[1], v[0]))
            a2 = float(np.arctan2(av[1], av[0]))
            diff = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
            if abs(diff) < 0.025:
                return VGroup()
            return Arc(
                radius=0.55,
                start_angle=a1,
                angle=diff,
                arc_center=plane.c2p(0, 0),
                color=ACCENT_GREEN if abs(np.degrees(diff)) < 3 else TRANS_VEC_COLOR,
                stroke_width=3.2,
            )

        angle_sector = always_redraw(make_angle_sector)

        v_dot_lbl = always_redraw(
            lambda: MathTex(r"\mathbf{v}", color=ORD_VEC_COLOR)
            .scale(0.95)
            .move_to(plane.c2p(*(1.32 * get_v_vec(theta_tracker.get_value()))))
        )
        av_dot_lbl = always_redraw(
            lambda: MathTex(r"A\mathbf{v}", color=TRANS_VEC_COLOR)
            .scale(0.95)
            .move_to(plane.c2p(*(get_av_vec(theta_tracker.get_value()) * 1.15 + np.array([0.25, 0.2]))))
        )

        # Live Telemetry HUD on top right
        def make_hud():
            th = theta_tracker.get_value()
            deg = np.degrees(th) % 360.0
            diff_deg = get_angle_deg(th)
            scale = float(np.linalg.norm(get_av_vec(th)))
            aligned = diff_deg < 1.8
            diff_color = ACCENT_GREEN if aligned else TRANS_VEC_COLOR
            lines = VGroup(
                Text(f"Input angle: {deg:5.1f} deg", font_size=19, color=ORD_VEC_COLOR),
                Text(
                    f"Angle(v, Av): {diff_deg:4.1f} deg" + ("  [HIT!]" if aligned else ""),
                    font_size=19,
                    color=diff_color,
                    weight="BOLD" if aligned else "NORMAL",
                ),
                Text(f"Scale ||Av||/||v||: {scale:4.2f}x", font_size=19, color=TEXT_PRIMARY),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            return make_card(lines, pad=0.16, stroke_color=ACCENT_GREEN if aligned else PANEL_BORDER).to_corner(UP + RIGHT, buff=0.32)

        hud = always_redraw(make_hud)

        cue_3a = (
            "Before touching any algebra, let us test every direction around the unit circle. "
            "Here, the rotating arrow is our input vector v, and the yellow arrow is its output A times v. "
            "Notice the angle readout between them. Almost everywhere, A knocks the output off the input's line. "
            "Watch what happens at forty-five degrees: the angle drops to zero, and both arrows align! "
            "Continue rotating: they separate again, until one hundred thirty-five degrees, where the angle hits zero a second time."
        )

        hit_markers = VGroup()
        with self.voiceover(text=cue_3a) as tracker:
            self.play(
                Create(warped_grid, run_time=0.9),
                FadeIn(plane),
                FadeIn(axis_labels),
                FadeIn(header[0]),
            )
            self.play(ApplyMatrix(MATRIX_A, warped_grid), run_time=1.8)
            self.play(
                Create(unit_circle),
                FadeIn(v_arrow),
                FadeIn(av_arrow),
                FadeIn(angle_sector),
                FadeIn(v_dot_lbl),
                FadeIn(av_dot_lbl),
                FadeIn(hud),
                run_time=1.0,
            )

            # Sweep 0 -> 45 deg
            self.play(theta_tracker.animate.set_value(np.pi / 4), run_time=3.0)
            dot_45 = Dot(plane.c2p(np.cos(np.pi / 4), np.sin(np.pi / 4)), color=EIG1_COLOR, radius=0.09)
            hit_markers.add(dot_45)
            self.add(dot_45)
            self.play(Flash(dot_45, color=EIG1_COLOR, flash_radius=0.45), run_time=0.8)
            self.wait(1.0)

            # Sweep 45 -> 135 deg
            self.play(theta_tracker.animate.set_value(3 * np.pi / 4), run_time=3.5)
            dot_135 = Dot(plane.c2p(np.cos(3 * np.pi / 4), np.sin(3 * np.pi / 4)), color=EIG2_COLOR, radius=0.09)
            hit_markers.add(dot_135)
            self.add(dot_135)
            self.play(Flash(dot_135, color=EIG2_COLOR, flash_radius=0.45), run_time=0.8)
            self.wait(0.8)

            # Complete sweep 135 -> 225 -> 315 -> 360 deg
            self.play(theta_tracker.animate.set_value(5 * np.pi / 4), run_time=1.8)
            dot_225 = Dot(plane.c2p(np.cos(5 * np.pi / 4), np.sin(5 * np.pi / 4)), color=EIG1_COLOR, radius=0.07)
            hit_markers.add(dot_225)
            self.add(dot_225)
            self.play(theta_tracker.animate.set_value(7 * np.pi / 4), run_time=1.8)
            dot_315 = Dot(plane.c2p(np.cos(7 * np.pi / 4), np.sin(7 * np.pi / 4)), color=EIG2_COLOR, radius=0.07)
            hit_markers.add(dot_315)
            self.add(dot_315)
            self.play(theta_tracker.animate.set_value(2 * np.pi), run_time=1.2)
            self.wait(max(0.4, tracker.duration - 17.6))

        # --- Cue 3B: Reveal the Two Invariant Lines and Scaling Factors ---
        eigen_lines = make_eigen_lines(plane)
        line1_lbl = MathTex(r"y = x \;\;(\lambda_1 = 3)", color=EIG1_COLOR).scale(0.95)
        line1_lbl_card = make_card(line1_lbl, pad=0.14, stroke_color=EIG1_COLOR)
        line1_lbl_card.move_to(plane.c2p(4.2, 1.8))

        line2_lbl = MathTex(r"y = -x \;\;(\lambda_2 = 1)", color=EIG2_COLOR).scale(0.95)
        line2_lbl_card = make_card(line2_lbl, pad=0.14, stroke_color=EIG2_COLOR)
        line2_lbl_card.move_to(plane.c2p(4.1, -1.65))

        # Test vectors on y=x and y=-x showing pure scaling (x3 and x1)
        v_yx_in = make_plane_vector(plane, (1, 1), color=EIG1_COLOR, stroke_width=5.5)
        v_yx_out = make_plane_vector(plane, (3, 3), color=EIG1_COLOR, stroke_width=5.5)
        v_ynx_in = make_plane_vector(plane, (1, -1), color=EIG2_COLOR, stroke_width=5.5)
        v_ynx_out = make_plane_vector(plane, (1, -1), color=EIG2_COLOR, stroke_width=5.5)

        badge_x3 = make_card(MathTex(r"(1,1) \mapsto 3(1,1) = (3,3)", color=EIG1_COLOR).scale(0.9), pad=0.14, stroke_color=EIG1_COLOR)
        badge_x3.to_corner(DOWN + LEFT, buff=0.4)
        badge_x1 = make_card(MathTex(r"(1,-1) \mapsto 1(1,-1) = (1,-1)", color=EIG2_COLOR).scale(0.9), pad=0.14, stroke_color=EIG2_COLOR)
        badge_x1.to_corner(DOWN + RIGHT, buff=0.4)

        cue_3b = (
            "Sweeping the full circle reveals two special invariant lines. "
            "Along the orange line y equals x, every vector stays on its own line and stretches to three times its length. "
            "Along the teal line y equals minus x, vectors stay on their line completely unchanged, scaled by one. "
            "Everything else gets pulled away from its line."
        )
        with self.voiceover(text=cue_3b) as tracker:
            self.play(
                FadeOut(VGroup(v_arrow, av_arrow, angle_sector, v_dot_lbl, av_dot_lbl, hud)),
                Create(eigen_lines),
                run_time=1.3,
            )
            self.play(
                GrowArrow(v_yx_in),
                FadeIn(line1_lbl_card),
                FadeIn(badge_x3, shift=UP * 0.15),
                run_time=1.1,
            )
            self.play(Transform(v_yx_in, v_yx_out), run_time=1.8)
            self.play(
                GrowArrow(v_ynx_in),
                FadeIn(line2_lbl_card),
                FadeIn(badge_x1, shift=UP * 0.15),
                run_time=1.1,
            )
            self.play(Flash(v_ynx_in.get_end(), color=EIG2_COLOR, flash_radius=0.35), run_time=1.0)
            self.wait(max(0.5, tracker.duration - 6.3))

        self.play(
            FadeOut(
                VGroup(
                    header[0],
                    warped_grid,
                    plane,
                    axis_labels,
                    unit_circle,
                    hit_markers,
                    eigen_lines,
                    line1_lbl_card,
                    line2_lbl_card,
                    v_yx_in,
                    v_ynx_in,
                    badge_x3,
                    badge_x1,
                )
            ),
            run_time=0.7,
        )
