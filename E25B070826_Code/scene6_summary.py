"""Scene 6: Summary & Credits — 3 core takeaways, references, AI disclosure, student credits."""

from manim import (
    Arrow,
    Create,
    DashedLine,
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    LEFT,
    MathTex,
    Polygon,
    RIGHT,
    Text,
    UP,
    VGroup,
    Write,
)
from manim_voiceover import VoiceoverScene
import numpy as np

from helpers.config import (
    ACCENT_GREEN,
    BG_COLOR,
    COURSE_NAME,
    EIG1_COLOR,
    EIG2_COLOR,
    PANEL_BORDER,
    PROJECT_TITLE,
    SQUARE_COLOR,
    STUDENT_ID,
    STUDENT_NAME,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TRANS_VEC_COLOR,
)
from helpers.visuals import make_card, make_scene_header
from helpers.voice import get_speech_service


class Scene6SummaryCredits(VoiceoverScene):
    """3-point visual summary followed by academic credits and AI disclosure."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        self.set_speech_service(get_speech_service())

        header = make_scene_header("Summary: Key Takeaways", "Eigenvalues & Eigenvectors")

        # --- Mini diagrams for the 3 takeaway cards ---
        # Icon 1: Collinear eigen-arrows
        i1_line = DashedLine(LEFT * 0.55, RIGHT * 0.55, color=EIG1_COLOR, stroke_width=2)
        i1_a1 = Arrow(LEFT * 0.45, RIGHT * 0.05, buff=0, color=EIG1_COLOR, stroke_width=4, tip_length=0.14)
        i1_a2 = Arrow(LEFT * 0.45, RIGHT * 0.5, buff=0, color=TRANS_VEC_COLOR, stroke_width=3, tip_length=0.14).shift(DOWN * 0.16)
        icon1 = VGroup(i1_line, i1_a1, i1_a2)

        # Icon 2: Determinant badge
        icon2 = MathTex(r"\det(A-\lambda I)=0", color=EIG2_COLOR).scale(0.8)

        # Icon 3: Square -> Parallelogram
        sq = Polygon([0, 0, 0], [0.45, 0, 0], [0.45, 0.45, 0], [0, 0.45, 0], color=SQUARE_COLOR, fill_opacity=0.35, stroke_width=2)
        pg = Polygon([0.65, 0, 0], [1.25, 0.18, 0], [1.45, 0.63, 0], [0.85, 0.45, 0], color=ACCENT_GREEN, fill_opacity=0.35, stroke_width=2)
        icon3 = VGroup(sq, pg)

        def make_takeaway(num: str, title: str, body: str, icon, accent: str):
            num_txt = Text(num, font_size=26, color=accent, weight="BOLD")
            t_txt = Text(title, font_size=24, color=TEXT_PRIMARY, weight="BOLD")
            b_txt = Text(body, font_size=19, color=TEXT_MUTED)
            text_col = VGroup(VGroup(num_txt, t_txt).arrange(RIGHT, buff=0.16), b_txt).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            row = VGroup(icon, text_col).arrange(RIGHT, buff=0.35)
            return make_card(row, pad=0.22, stroke_color=accent)

        card1 = make_takeaway(
            "1.",
            "Geometric Meaning",
            "Eigenvectors keep their direction (Av = lambda v); eigenvalues measure scaling.",
            icon1,
            EIG1_COLOR,
        )
        card2 = make_takeaway(
            "2.",
            "Algebraic Recipe",
            "Solve det(A - lambda I) = 0 for eigenvalues, then (A - lambda I)v = 0 for eigenvectors.",
            icon2,
            EIG2_COLOR,
        )
        card3 = make_takeaway(
            "3.",
            "Determinant & Area Link",
            "det(A) = lambda1 * lambda2 = 3 gives the area scale factor (unit square -> parallelogram).",
            icon3,
            ACCENT_GREEN,
        )

        takeaways = VGroup(card1, card2, card3).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        takeaways.move_to(DOWN * 0.25)

        cue_6a = (
            "To summarize: first, eigenvectors keep their direction while eigenvalues measure their scaling. "
            "Second, solve determinant of A minus lambda I equals zero for eigenvalues, then solve the null space for eigenvectors. "
            "Third, the determinant equals the product of the eigenvalues and gives the area scale factor."
        )
        with self.voiceover(text=cue_6a) as tracker:
            self.play(FadeIn(header, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(card1, shift=UP * 0.2), run_time=1.3)
            self.wait(1.8)
            self.play(FadeIn(card2, shift=UP * 0.2), run_time=1.3)
            self.wait(2.2)
            self.play(FadeIn(card3, shift=UP * 0.2), run_time=1.3)
            self.wait(max(0.5, tracker.duration - 8.5))

        # --- Transition to Credits Frame ---
        self.play(FadeOut(VGroup(header, takeaways)), run_time=0.6)

        cred_title = Text(f"{PROJECT_TITLE} — Credits & References", font_size=34, color=TEXT_PRIMARY, weight="BOLD")
        cred_student = Text(
            f"Student: {STUDENT_NAME}   |   ID: {STUDENT_ID}   |   {COURSE_NAME}",
            font_size=22,
            color=EIG1_COLOR,
            weight="BOLD",
        )
        refs_block = VGroup(
            Text("References:", font_size=22, color=EIG2_COLOR, weight="BOLD"),
            Text("  - 3Blue1Brown, 'Essence of Linear Algebra' (Ch. 14: Eigenvectors & Eigenvalues) — visual inspiration", font_size=19, color=TEXT_MUTED),
            Text("  - Gilbert Strang, 'Introduction to Linear Algebra' (5th ed.) — Ch. 6", font_size=19, color=TEXT_MUTED),
            Text("  - M3 Linear Algebra & Calculus Course Lecture Notes", font_size=19, color=TEXT_MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        audio_block = VGroup(
            Text("Audio & Tools Disclosure:", font_size=22, color=TRANS_VEC_COLOR, weight="BOLD"),
            Text("  - Music: None (voice-only narration for clarity)", font_size=19, color=TEXT_MUTED),
            Text("  - AI Disclosure: Google Antigravity assisted with Manim scripting, narration pacing, and docs.", font_size=19, color=TEXT_MUTED),
            Text("  - TTS Engine: F5-TTS-MLX (zero-shot voice clone from student's own voice sample) via manim-voiceover.", font_size=18, color=TEXT_MUTED),
            Text("  - All math independently verified via SymPy & NumPy (verify_math.py).", font_size=19, color=TEXT_MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        credits_content = VGroup(cred_title, cred_student, refs_block, audio_block).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        credits_card = make_card(credits_content, pad=0.32, stroke_color=PANEL_BORDER)
        credits_card.move_to(0)

        cue_6b = (
            "Thank you for watching. Inspired by three-blue-one-brown and M3 Linear Algebra notes. "
            "Presented by Siddhant Kumar Thakur, Student ID E-two-five-B-zero-seven-zero-eight-two-six."
        )
        with self.voiceover(text=cue_6b) as tracker:
            self.play(FadeIn(credits_card, shift=UP * 0.2), run_time=1.2)
            self.wait(max(1.2, tracker.duration - 1.2))

        self.wait(1.0)
        self.play(FadeOut(credits_card), run_time=0.7)
