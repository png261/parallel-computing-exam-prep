"""Playful helpers: a mascot ("Bé Core"), speech bubbles, XP HUD, level banners. Pure Manim shapes (no emoji/LaTeX)."""
from manim import *
from scene_utils import (
    PANEL_BG, BORDER_DIM, CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, SANS, MONO,
)


def make_mascot(mood: str = "happy", scale: float = 1.0, color=CYAN) -> VGroup:
    """A friendly CPU-chip character. mood: happy | think | wow | sad | cheer."""
    body = RoundedRectangle(width=1.5, height=1.4, corner_radius=0.22, fill_color=color, fill_opacity=0.95,
                            stroke_color=TEXT_MAIN, stroke_width=3)
    pins = VGroup()
    for i in range(3):
        for dx, dy, w, h in ((-0.86, 0.35 - 0.35 * i, 0.22, 0.08), (0.86, 0.35 - 0.35 * i, 0.22, 0.08)):
            pins.add(Rectangle(width=w, height=h, fill_color=TEXT_MUTED, fill_opacity=1, stroke_width=0).move_to(RIGHT * dx + UP * dy))
    for i in range(3):
        for dx, dy, w, h in ((-0.4 + 0.4 * i, 0.78, 0.08, 0.2), (-0.4 + 0.4 * i, -0.78, 0.08, 0.2)):
            pins.add(Rectangle(width=w, height=h, fill_color=TEXT_MUTED, fill_opacity=1, stroke_width=0).move_to(RIGHT * dx + UP * dy))
    def eye(x):
        white = Circle(radius=0.2, fill_color=WHITE, fill_opacity=1, stroke_color="#0D1117", stroke_width=2).move_to(RIGHT * x + UP * 0.2)
        pupil = Circle(radius=0.09, fill_color="#0D1117", fill_opacity=1, stroke_width=0).move_to(white.get_center() + DOWN * 0.02)
        return VGroup(white, pupil)
    eyes = VGroup(eye(-0.3), eye(0.3))
    if mood == "sad":
        mouth = Arc(radius=0.28, start_angle=PI * 0.15, angle=PI * 0.7, color="#0D1117", stroke_width=4).move_to(DOWN * 0.38)
        mouth.rotate(PI)
    elif mood == "think":
        mouth = Line(LEFT * 0.2, RIGHT * 0.2, color="#0D1117", stroke_width=4).move_to(DOWN * 0.35)
        eyes[1][1].shift(UP * 0.07 + RIGHT * 0.04)
    elif mood in ("wow", "cheer"):
        mouth = Ellipse(width=0.34, height=0.3, fill_color="#7F1D1D", fill_opacity=1, stroke_color="#0D1117", stroke_width=3).move_to(DOWN * 0.38)
    else:
        mouth = Arc(radius=0.3, start_angle=PI * 1.15, angle=PI * 0.7, color="#0D1117", stroke_width=4).move_to(DOWN * 0.28)
    cheeks = VGroup(*[Circle(radius=0.08, fill_color=CORAL, fill_opacity=0.55, stroke_width=0).move_to(RIGHT * x + DOWN * 0.18) for x in (-0.52, 0.52)])
    g = VGroup(pins, body, cheeks, eyes, mouth)
    if mood == "cheer":
        g.add(Star(n=5, outer_radius=0.17, inner_radius=0.07, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to(UP * 1.0 + RIGHT * 0.5))
    return g.scale(scale)


def make_bubble(text: str, width: float = 4.0, color=CYAN, font_size: int = 20) -> VGroup:
    t = Text(text, font=SANS, font_size=font_size, color=TEXT_MAIN)
    if t.width > width - 0.4:
        t.scale_to_fit_width(width - 0.4)
    box = RoundedRectangle(width=max(t.width + 0.5, 1.2), height=t.height + 0.45, corner_radius=0.2,
                           fill_color=PANEL_BG, fill_opacity=0.98, stroke_color=color, stroke_width=2.2)
    t.move_to(box.get_center())
    return VGroup(box, t)


def make_hud(xp: int, streak: int = 0, level: int = 1, accent=AMBER) -> VGroup:
    star = Star(n=5, outer_radius=0.16, inner_radius=0.07, fill_color=accent, fill_opacity=1, stroke_width=0)
    xp_t = Text(f"{xp} XP", font=MONO, font_size=18, weight=BOLD, color=accent)
    lv_t = Text(f"Màn {level}", font=SANS, font_size=16, color=TEXT_MUTED)
    items = [star, xp_t, lv_t]
    if streak >= 2:
        items.append(Text(f"chuỗi x{streak}", font=SANS, font_size=16, weight=BOLD, color=CORAL))
    g = VGroup(*items).arrange(RIGHT, buff=0.22)
    pill = RoundedRectangle(width=g.width + 0.4, height=g.height + 0.26, corner_radius=0.18,
                            fill_color=PANEL_BG, fill_opacity=0.95, stroke_color=accent, stroke_width=1.6)
    g.move_to(pill.get_center())
    return VGroup(pill, g)


def bounce(mob, h: float = 0.25, run_time: float = 0.5):
    """Little hop animation for the mascot."""
    return Succession(mob.animate(run_time=run_time / 2, rate_func=rush_from).shift(UP * h),
                      mob.animate(run_time=run_time / 2, rate_func=rush_into).shift(DOWN * h))


def level_banner(text: str, sub: str = "", color=AMBER) -> VGroup:
    t = Text(text, font=SANS, font_size=40, weight=BOLD, color=color)
    s = Text(sub, font=SANS, font_size=22, color=TEXT_MAIN) if sub else None
    g = VGroup(t, s) if s else VGroup(t)
    g.arrange(DOWN, buff=0.2)
    box = RoundedRectangle(width=max(g.width + 1.0, 5.0), height=g.height + 0.8, corner_radius=0.25,
                           fill_color="#161B22", fill_opacity=0.98, stroke_color=color, stroke_width=3)
    g.move_to(box.get_center())
    return VGroup(box, g)
