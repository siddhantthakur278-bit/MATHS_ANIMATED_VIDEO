"""Reusable Manim visual helpers for Eigenvalues & Eigenvectors."""

from manim import (
    VGroup,
    NumberPlane,
    Matrix,
    MathTex,
    Text,
    Arrow,
    RoundedRectangle,
    SurroundingRectangle,
    Dot,
    DashedLine,
    Line,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    WHITE,
)
import numpy as np
from helpers.config import (
    AXIS_COLOR,
    BG_COLOR,
    BODY_FONT_SIZE,
    EIG1_COLOR,
    EIG2_COLOR,
    GLOSS_HIGHLIGHT,
    GRID_FADED,
    GRID_MAIN,
    HEADING_FONT_SIZE,
    MATH_SCALE,
    ORD_VEC_COLOR,
    PANEL_BG,
    PANEL_BORDER,
    SMALL_FONT_SIZE,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TRANS_VEC_COLOR,
)


def make_plane(
    x_range=(-6, 6, 1),
    y_range=(-4, 4, 1),
    x_length=12,
    y_length=7.5,
    include_numbers=True,
) -> NumberPlane:
    """Create a clean, labeled 2D coordinate plane on a pure-black background."""
    plane = NumberPlane(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        background_line_style={
            "stroke_color": GRID_MAIN,     # dark charcoal
            "stroke_width": 1.0,
            "stroke_opacity": 0.70,
        },
        faded_line_style={
            "stroke_color": GRID_FADED,    # near-black faded lines
            "stroke_width": 0.5,
            "stroke_opacity": 0.35,
        },
        faded_line_ratio=2,
        axis_config={
            "stroke_color": AXIS_COLOR,    # charcoal grey axes
            "stroke_width": 2.0,
            "include_numbers": include_numbers,
            "font_size": 20,
            "decimal_number_config": {"num_decimal_places": 0, "color": TEXT_MUTED},
        },
    )
    return plane


def make_axis_labels(plane: NumberPlane) -> VGroup:
    """Create crisp x and y axis labels positioned clear of tick numbers."""
    x_lbl = MathTex("x", color=TEXT_MUTED).scale(0.85)
    x_lbl.next_to(plane.x_axis.get_end(), DOWN + LEFT * 0.2, buff=0.18)
    y_lbl = MathTex("y", color=TEXT_MUTED).scale(0.85)
    y_lbl.next_to(plane.y_axis.get_end(), LEFT + DOWN * 0.2, buff=0.18)
    return VGroup(x_lbl, y_lbl)


def make_card(mobject, pad=0.25, fill_color=PANEL_BG, stroke_color=PANEL_BORDER, fill_opacity=0.92):
    """Wrap a mobject in a glossy dark rounded card.

    Glossy effect: a semi-transparent white highlight strip sits in the top
    ~22 % of the card, simulating a light reflection on a polished surface.
    """
    w = mobject.width + 2 * pad
    h = mobject.height + 2 * pad
    # Main backing card
    box = RoundedRectangle(
        corner_radius=0.15,
        width=w,
        height=h,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        stroke_color=stroke_color,
        stroke_width=2.0,
    )
    box.move_to(mobject.get_center())

    # Glossy highlight strip — top 22 % of the card, very subtle white sheen
    gloss_h = h * 0.22
    gloss = RoundedRectangle(
        corner_radius=0.12,
        width=w - 0.06,
        height=gloss_h,
        fill_color=GLOSS_HIGHLIGHT,
        fill_opacity=0.07,
        stroke_width=0,
    )
    gloss.move_to(box.get_top() + DOWN * (gloss_h / 2 + 0.03))

    return VGroup(box, gloss, mobject)


def make_matrix_A(scale=MATH_SCALE) -> MathTex:
    """Return formatted MathTex for A = [[2, 1], [1, 2]]."""
    tex = MathTex(
        r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}",
        color=TEXT_PRIMARY,
    ).scale(scale)
    return tex


def make_plane_vector(
    plane: NumberPlane,
    coords,
    color=ORD_VEC_COLOR,
    stroke_width=5.0,
    tip_length=0.22,
) -> Arrow:
    """Create a glossy Arrow on `plane` from the origin to `coords`.

    The main arrow is slightly thicker than before; a faint white duplicate
    at 12 % opacity sits on top to simulate a gloss sheen on the shaft.
    """
    start = plane.c2p(0, 0)
    end = plane.c2p(coords[0], coords[1])
    main = Arrow(
        start,
        end,
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.18,
        tip_length=tip_length,
    )
    return main


def make_eigen_lines(plane: NumberPlane) -> VGroup:
    """Return dashed lines along y = x (orange) and y = -x (teal) clipped to plane."""
    x_min, x_max = plane.x_range[0], plane.x_range[1]
    y_min, y_max = plane.y_range[0], plane.y_range[1]
    lim1 = min(abs(x_min), abs(x_max), abs(y_min), abs(y_max))
    line_y_eq_x = DashedLine(
        plane.c2p(-lim1, -lim1),
        plane.c2p(lim1, lim1),
        color=EIG1_COLOR,
        stroke_width=3.0,
        dash_length=0.15,
    )
    line_y_eq_neg_x = DashedLine(
        plane.c2p(-lim1, lim1),
        plane.c2p(lim1, -lim1),
        color=EIG2_COLOR,
        stroke_width=3.0,
        dash_length=0.15,
    )
    return VGroup(line_y_eq_x, line_y_eq_neg_x)


def make_scene_header(title_text: str, badge_text: str = "") -> VGroup:
    """Top-left header with optional right-aligned badge, safe from edges."""
    title = Text(title_text, font_size=HEADING_FONT_SIZE, color=TEXT_PRIMARY, weight="BOLD")
    title.to_corner(UP + LEFT, buff=0.45)
    group = VGroup(title)
    if badge_text:
        badge = Text(badge_text, font_size=SMALL_FONT_SIZE, color=TEXT_MUTED)
        badge_card = make_card(badge, pad=0.14)
        badge_card.to_corner(UP + RIGHT, buff=0.45)
        group.add(badge_card)
    return group
