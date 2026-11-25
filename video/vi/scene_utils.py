import json
from pathlib import Path
from manim import *

TTS_DIR = Path(__file__).resolve().parent / "tts_wav"
_DURATIONS = None


def get_duration(seg_id: str) -> float:
    global _DURATIONS
    if _DURATIONS is None:
        meta = TTS_DIR / "durations.json"
        _DURATIONS = json.loads(meta.read_text()) if meta.exists() else {}
    return float(_DURATIONS.get(seg_id, 6.0))


def play_voiced(scene: Scene, seg_id: str, anim_steps: list[tuple]):
    """
    Play audio segment `seg_id` synced with a list of `(animations_list, run_time)` steps.
    Waits until audio finishes + 0.35s breathing pause.
    """
    wav = TTS_DIR / f"{seg_id}.wav"
    dur = get_duration(seg_id)
    if wav.exists():
        scene.add_sound(str(wav))
    elapsed = 0.0
    for anims, rt in anim_steps:
        if not isinstance(anims, (list, tuple)):
            anims = [anims]
        scene.play(*anims, run_time=rt)
        elapsed += rt
    rem = max(0.35, dur - elapsed + 0.35)
    scene.wait(rem)


def make_grid_box(label_str: str, w: float = 1.1, h: float = 0.65, color: str = "#38BDF8", font_size: int = 15) -> VGroup:
    rect = RoundedRectangle(
        width=w, height=h, corner_radius=0.08,
        color=color, fill_color=PANEL_BG, fill_opacity=0.95, stroke_width=1.8
    )
    txt = Text(label_str, font=MONO, font_size=font_size, color=TEXT_MAIN)
    if txt.width > w - 0.14:
        txt.scale_to_fit_width(w - 0.14)
    txt.move_to(rect.get_center())
    return VGroup(rect, txt)

# Palette (3B1B / Dark Modern Slate)
BG_COLOR = "#0D1117"
PANEL_BG = "#161B22"
BORDER_DIM = "#30363D"
CYAN = "#38BDF8"
AMBER = "#FBBF24"
EMERALD = "#34D399"
CORAL = "#F87171"
VIOLET = "#A78BFA"
TEXT_MAIN = "#F3F4F6"
TEXT_MUTED = "#9CA3AF"

SANS = "Helvetica Neue"
MONO = "Menlo"


def setup_bg(scene: Scene):
    scene.camera.background_color = BG_COLOR


def make_header(title_str: str, tag_str: str = "", accent=CYAN) -> VGroup:
    title = Text(title_str, font=SANS, font_size=30, weight=BOLD, color=TEXT_MAIN)
    title.to_edge(UP, buff=0.28).to_edge(LEFT, buff=0.55)
    if title.width > 9.5:
        title.scale_to_fit_width(9.5)

    group = VGroup(title)
    if tag_str:
        tag = Text(tag_str, font=MONO, font_size=16, color=accent)
        pill = SurroundingRectangle(
            tag, color=accent, fill_color=PANEL_BG, fill_opacity=0.9,
            buff=0.12, corner_radius=0.1, stroke_width=1.5
        )
        pill_grp = VGroup(pill, tag)
        pill_grp.to_edge(UP, buff=0.28).to_edge(RIGHT, buff=0.55)
        group.add(pill_grp)

    line = Line(
        LEFT * 6.55 + UP * 2.82,
        RIGHT * 6.55 + UP * 2.82,
        color=BORDER_DIM, stroke_width=1.5
    )
    group.add(line)
    return group


def make_card(title_str: str, lines: list[str], width: float = 5.8,
              accent=CYAN, title_size: int = 21, body_size: int = 17,
              code_body: bool = False) -> VGroup:
    t = Text(title_str, font=SANS, font_size=title_size, weight=BOLD, color=accent)
    body_items = VGroup()
    font_choice = MONO if code_body else SANS
    for ln in lines:
        if ln.strip() == "":
            item = Rectangle(width=0.02, height=0.06, stroke_opacity=0, fill_opacity=0)
        else:
            lead = len(ln) - len(ln.lstrip(" "))
            item = Text("\u00a0" * lead + ln.lstrip(" "), font=font_choice, font_size=body_size, color=TEXT_MAIN)
            if item.width > width - 0.55:
                item.scale_to_fit_width(width - 0.55)
        body_items.add(item)
    body_items.arrange(DOWN, aligned_edge=LEFT, buff=0.14)

    if t.width > width - 0.55:
        t.scale_to_fit_width(width - 0.55)

    content = VGroup(t, body_items).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    box_h = max(content.height + 0.45, 1.2)
    box = RoundedRectangle(
        width=width, height=box_h, corner_radius=0.14,
        fill_color=PANEL_BG, fill_opacity=0.95,
        stroke_color=accent, stroke_width=1.8
    )
    content.move_to(box.get_center()).align_to(box, LEFT).shift(RIGHT * 0.25)
    return VGroup(box, content)


def make_code_box(lines: list[str], width: float = 6.0, font_size: int = 16,
                  accent=VIOLET, title_str: str = "") -> VGroup:
    code_grp = VGroup(*[
        Rectangle(width=0.02, height=0.06, stroke_opacity=0, fill_opacity=0) if ln.strip() == ""
        else Text("\u00a0" * (len(ln) - len(ln.lstrip(" "))) + ln.lstrip(" "), font=MONO, font_size=font_size, color=TEXT_MAIN)
        for ln in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    if code_grp.width > width - 0.45:
        code_grp.scale_to_fit_width(width - 0.45)

    parts = VGroup()
    if title_str:
        hdr = Text(title_str, font=SANS, font_size=17, weight=BOLD, color=accent)
        parts.add(hdr, code_grp)
        parts.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    else:
        parts.add(code_grp)

    box = RoundedRectangle(
        width=width, height=parts.height + 0.4, corner_radius=0.12,
        fill_color="#090D13", fill_opacity=0.98,
        stroke_color=accent, stroke_width=1.6
    )
    parts.move_to(box.get_center()).align_to(box, LEFT).shift(RIGHT * 0.22)
    return VGroup(box, parts)


def make_trap_banner(msg: str) -> VGroup:
    label = Text(f"BẪY THI: {msg}", font=SANS, font_size=17, weight=BOLD, color=CORAL)
    if label.width > 12.2:
        label.scale_to_fit_width(12.2)
    box = RoundedRectangle(
        width=min(label.width + 0.6, 12.8), height=0.52, corner_radius=0.12,
        fill_color="#2A1215", fill_opacity=0.95,
        stroke_color=CORAL, stroke_width=1.6
    )
    label.move_to(box.get_center())
    grp = VGroup(box, label)
    grp.to_edge(DOWN, buff=0.25)
    return grp


def make_frac(num_str: str, den_str: str, font_size: int = 22, color=TEXT_MAIN) -> VGroup:
    num = Text(num_str, font=SANS, font_size=font_size, color=color)
    den = Text(den_str, font=SANS, font_size=font_size, color=color)
    w = max(num.width, den.width) + 0.2
    bar = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=2)
    grp = VGroup(num, bar, den).arrange(DOWN, buff=0.08)
    return grp


def clear_stage(scene: Scene, keep=None):
    keep_set = set(keep) if keep else set()
    to_remove = [m for m in scene.mobjects if m not in keep_set]
    if to_remove:
        scene.play(*[FadeOut(m, shift=DOWN * 0.1) for m in to_remove], run_time=0.4)


def make_bar_chart(values: list[float], labels: list[str], colors: list,
                   max_val: float, width: float = 5.2, height: float = 2.6,
                   unit: str = "s") -> VGroup:
    n = len(values)
    slot_w = width / n
    bar_w = slot_w * 0.56
    base = Line(LEFT * width / 2, RIGHT * width / 2, color=TEXT_MUTED, stroke_width=2)
    y_axis = Line(LEFT * width / 2, LEFT * width / 2 + UP * height, color=TEXT_MUTED, stroke_width=2)

    bars = VGroup()
    for i, (val, lbl, col) in enumerate(zip(values, labels, colors)):
        h = max((val / max_val) * (height - 0.35), 0.08)
        cx = -width / 2 + slot_w * (i + 0.5)
        rect = Rectangle(
            width=bar_w, height=h, color=col,
            fill_color=col, fill_opacity=0.85, stroke_width=1.5
        )
        rect.move_to(RIGHT * cx + UP * (h / 2))
        val_txt = Text(f"{val:g} {unit}", font=MONO, font_size=14, weight=BOLD, color=col)
        val_txt.next_to(rect, UP, buff=0.08)
        lbl_txt = Text(lbl, font=SANS, font_size=14, color=TEXT_MAIN)
        if lbl_txt.width > slot_w * 0.92:
            lbl_txt.scale_to_fit_width(slot_w * 0.92)
        lbl_txt.next_to(rect, DOWN, buff=0.14)
        bars.add(VGroup(rect, val_txt, lbl_txt))

    return VGroup(base, y_axis, bars)


import textwrap


def _wrap_lines(s: str, width: int) -> list[str]:
    return textwrap.wrap(s, width=width) or [""]


def play_drill(scene: Scene, key: str, item: dict, mod_label: str, num: int, total: int):
    """On-screen exam drill: question + 4 options -> 5 s countdown -> reveal answer + reason."""
    hdr = make_header(f"Bài luyện thi {num}/{total}: Tạm dừng & trả lời", mod_label, CORAL)
    q_card = make_card("Câu hỏi", _wrap_lines(item["q"], 92), width=12.4, accent=AMBER,
                       title_size=17, body_size=19).move_to(UP * 1.75)
    opts = VGroup()
    for i, o in enumerate(item["opts"]):
        box = RoundedRectangle(width=6.0, height=0.72, corner_radius=0.1, color=BORDER_DIM,
                               fill_color=PANEL_BG, fill_opacity=0.95, stroke_width=1.8)
        t = Text(f"{chr(65 + i)}.  {o}", font=SANS, font_size=17, color=TEXT_MAIN)
        if t.width > 5.6:
            t.scale_to_fit_width(5.6)
        t.move_to(box.get_center()).align_to(box, LEFT).shift(RIGHT * 0.22)
        opts.add(VGroup(box, t))
    opts.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.22))
    opts.next_to(q_card, DOWN, buff=0.3)

    play_voiced(scene, f"{key}_q", [
        ([FadeIn(hdr), FadeIn(q_card, shift=DOWN * 0.1)], 0.9),
        ([LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in opts], lag_ratio=0.25)], 1.4),
    ])

    # 5-second countdown
    ring = Circle(radius=0.42, color=AMBER, stroke_width=4).to_edge(DOWN, buff=0.45)
    num_t = Text("5", font=MONO, font_size=30, weight=BOLD, color=AMBER).move_to(ring)
    lbl = Text("Hãy tạm dừng video nếu bạn cần thêm thời gian", font=SANS, font_size=16,
               color=TEXT_MUTED).next_to(ring, RIGHT, buff=0.3)
    scene.play(FadeIn(ring), FadeIn(num_t), FadeIn(lbl), run_time=0.3)
    for k in range(4, -1, -1):
        new_t = Text(str(k), font=MONO, font_size=30, weight=BOLD,
                     color=CORAL if k <= 1 else AMBER).move_to(ring)
        scene.play(Transform(num_t, new_t), run_time=0.25)
        scene.wait(0.75)
    scene.play(FadeOut(ring), FadeOut(num_t), FadeOut(lbl), run_time=0.3)

    ans = item["ans"]
    reveal = []
    for i, o in enumerate(opts):
        if i == ans:
            reveal += [o[0].animate.set_stroke(EMERALD, width=4).set_fill("#0B3B2E", opacity=1.0)]
        else:
            reveal += [o.animate.set_opacity(0.3)]
    exp_card = make_card(f"Đáp án: {chr(65 + ans)}", _wrap_lines(item["say_a"], 105), width=12.4,
                         accent=EMERALD, title_size=17, body_size=15).to_edge(DOWN, buff=0.22)
    play_voiced(scene, f"{key}_a", [
        (reveal, 0.8),
        ([FadeIn(exp_card, shift=UP * 0.1)], 0.8),
    ])
    clear_stage(scene)


def play_module_drills(scene: Scene, mod: str, mod_label: str):
    try:
        from drill_data import DRILLS
    except ImportError:
        return
    items = DRILLS.get(mod, [])
    for i, item in enumerate(items):
        play_drill(scene, f"d{mod}_{i + 1}", item, mod_label, i + 1, len(items))
