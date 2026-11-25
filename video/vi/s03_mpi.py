from manim import *
import numpy as np
from scene_utils import play_module_drills
from scene_utils import (
    setup_bg, make_header, make_card, make_code_box, make_trap_banner,
    clear_stage, play_voiced, make_grid_box, make_bar_chart,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, BORDER_DIM, SANS, MONO
)

DARK = "#0D1117"
RANK_COLORS = [CYAN, EMERALD, AMBER, VIOLET]


def P(x, y):
    return np.array([x, y, 0.0])


def T(s, size=16, color=TEXT_MAIN, font=SANS, bold=False):
    return Text(s, font=font, font_size=size, color=color, weight=BOLD if bold else NORMAL)


def path(*pts):
    m = VMobject()
    m.set_points_as_corners([P(*p) if len(p) == 2 else np.array(p) for p in pts])
    return m


def rank_node(i, color=None, r=0.4, label=None):
    color = color or RANK_COLORS[i % 4]
    c = Circle(radius=r, color=color, stroke_width=2.5).set_fill(PANEL_BG, 1)
    t = T(label or f"rank {i}", 14, TEXT_MAIN, bold=True)
    if t.width > 2 * r - 0.1:
        t.scale_to_fit_width(2 * r - 0.1)
    t.move_to(c)
    return VGroup(c, t)


def pkt(label, color=AMBER, w=0.7, h=0.4, size=15):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.08, color=color, stroke_width=1.5).set_fill(color, 0.95)
    t = T(label, size, DARK, MONO, True)
    if t.width > w - 0.1:
        t.scale_to_fit_width(w - 0.1)
    t.move_to(r)
    return VGroup(r, t)


def box(label, color=CYAN, w=1.1, h=0.6, size=18):
    return make_grid_box(label, w=w, h=h, color=color, font_size=size)


def swap_text(mob, label, color=None):
    """Transform target for a make_grid_box with new label."""
    new = make_grid_box(label, w=mob[0].width, h=mob[0].height, color=color or mob[0].get_color(),
                        font_size=int(mob[1].font_size) if hasattr(mob[1], "font_size") else 16)
    new.move_to(mob)
    return new


class Ar(Arrow):
    def __init__(self, *a, **k):
        k.setdefault("tip_length", 0.2)
        super().__init__(*a, **k)


class Scene03MPI(Scene):
    # ------------------------------------------------------------------ 03_01
    def seg01(self):
        hdr = make_header("Module 3: MPI – mỗi rank một bộ nhớ", "MPI_COMM_WORLD", CYAN)
        xs = [-4.8, -1.6, 1.6, 4.8]
        world = RoundedRectangle(width=12.6, height=4.3, corner_radius=0.2, color=CYAN, stroke_width=1.8)
        world.set_fill(PANEL_BG, 0.4).move_to(P(0, 0.2))
        wl = T("MPI_COMM_WORLD · size = 4", 15, CYAN, MONO).move_to(P(-3.9, 1.95))
        ranks = VGroup(*[rank_node(i).move_to(P(xs[i], 1.1)) for i in range(4)])
        vals = ["x = 42", "x = ?", "x = ?", "x = 7"]
        mems = VGroup(*[box(vals[i], RANK_COLORS[i], w=2.4, h=0.8, size=20).move_to(P(xs[i], -0.35)) for i in range(4)])
        walls = VGroup(*[DashedLine(P(x, 1.65), P(x, -0.85), color=CORAL, stroke_width=2) for x in (-3.2, 0, 3.2)])
        p1 = pkt("42", AMBER).move_to(P(-4.8, -0.8))
        p2 = pkt("7", EMERALD).move_to(P(4.8, -0.8))
        take = T("Chia sẻ dữ liệu = gửi thông điệp", 22, AMBER, bold=True).move_to(P(0, -2.65))
        play_voiced(self, "03_01", [
            ([FadeIn(hdr), FadeIn(world), FadeIn(wl)], 1.5),
            ([LaggedStart(*[FadeIn(r, scale=0.8) for r in ranks], lag_ratio=0.3)], 2.5),
            ([FadeIn(mems), Create(walls)], 3.0),
            ([FadeIn(p1), MoveAlongPath(p1, path((-4.8, -0.8), (-4.8, -1.3), (1.6, -1.3), (1.6, -0.8)))], 4.0),
            ([Transform(mems[2], swap_text(mems[2], "x = 42", AMBER)), FadeOut(p1)], 1.0),
            ([FadeIn(p2), MoveAlongPath(p2, path((4.8, -0.8), (4.8, -1.65), (-1.6, -1.65), (-1.6, -0.8)))], 4.0),
            ([Transform(mems[1], swap_text(mems[1], "x = 7", EMERALD)), FadeOut(p2)], 1.0),
            ([FadeIn(take, shift=UP * 0.1)], 1.5),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_02
    def seg02(self):
        hdr = make_header("Send / Recv phải khớp phong bì", "(source, tag, comm)", AMBER)
        r0 = rank_node(0, CYAN).move_to(P(-5.2, 0.9))
        r1 = rank_node(1, EMERALD).move_to(P(5.2, 0.9))
        c0 = box("Send(dest=1, tag=7)", CYAN, w=3.2, h=0.6, size=14).move_to(P(-4.9, -0.2))
        c1 = box("Recv(src=0, tag=7)", EMERALD, w=3.2, h=0.6, size=14).move_to(P(4.9, -0.2))

        def env():
            return pkt("src 0 · tag 7 · WORLD", AMBER, w=2.7, h=0.5, size=12)
        e1 = env().move_to(P(-3.2, 0.9))
        ok1 = T("✓", 46, EMERALD, bold=True).move_to(P(0, 1.9))
        c1_bad = box("Recv(src=0, tag=9)", CORAL, w=3.2, h=0.6, size=14).move_to(P(4.9, -0.2))
        e2 = env().move_to(P(-3.2, 0.9))
        bad = T("tag 7 ≠ 9  ✗", 24, CORAL, bold=True).move_to(P(0, 1.9))
        wait = T("(nằm chờ trong hàng đợi)", 14, TEXT_MUTED).move_to(P(1.6, 0.25))
        c1_any = box("Recv(src=0, ANY_TAG)", EMERALD, w=3.2, h=0.6, size=14).move_to(P(4.9, -0.2))
        ok2 = T("✓", 46, EMERALD, bold=True).move_to(P(0, 1.9))
        take = T("Khớp = source + tag + comm", 22, AMBER, bold=True).move_to(P(0, -2.3))
        play_voiced(self, "03_02", [
            ([FadeIn(hdr), FadeIn(r0), FadeIn(r1), FadeIn(c0), FadeIn(c1)], 2.5),
            ([FadeIn(e1), e1.animate.move_to(P(3.2, 0.9))], 3.5),
            ([FadeIn(ok1, scale=1.5), Indicate(c1, color=EMERALD)], 1.5),
            ([FadeOut(e1, scale=0.3, shift=RIGHT * 1.2), FadeOut(ok1)], 1.0),
            ([Transform(c1, c1_bad)], 1.2),
            ([FadeIn(e2), e2.animate.move_to(P(3.2, 0.9))], 3.5),
            ([FadeIn(bad, scale=1.3), Wiggle(e2), FadeIn(wait)], 2.5),
            ([Transform(c1, c1_any), FadeOut(bad), FadeOut(wait)], 1.5),
            ([FadeIn(ok2, scale=1.5), FadeOut(e2, shift=RIGHT * 1.2, scale=0.3)], 2.5),
            ([FadeIn(take, shift=UP * 0.1)], 1.5),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_03
    def seg03(self):
        hdr = make_header("count = phần tử & không vượt mặt", "Send / Recv", CYAN)
        r0 = rank_node(0, CYAN, r=0.45).move_to(P(-5.6, 1.5))
        r1 = rank_node(1, EMERALD, r=0.45).move_to(P(5.6, 1.5))
        src = VGroup(*[box(str(v), CYAN, w=0.75, h=0.65) for v in (5, 8, 2)]).arrange(RIGHT, buff=0.05).move_to(P(-3.3, 1.5))
        dst = VGroup(*[box("·", EMERALD, w=0.75, h=0.65) for _ in range(3)]).arrange(RIGHT, buff=0.05).move_to(P(3.3, 1.5))
        mv = src.copy()
        good = T("count = 3  ✓  (phần tử)", 20, EMERALD, bold=True).move_to(P(0, 2.2))
        bad = T("count = 12  ✗  (byte)", 20, CORAL, bold=True).move_to(P(0, 0.8))
        dst_f = VGroup(*[box(str(v), EMERALD, w=0.75, h=0.65) for v in (5, 8, 2)]).arrange(RIGHT, buff=0.05).move_to(P(3.3, 1.5))
        sep = DashedLine(P(-6.3, -0.15), P(6.3, -0.15), color=BORDER_DIM)
        q0 = rank_node(0, CYAN, r=0.45).move_to(P(-5.6, -1.3))
        q1 = rank_node(1, EMERALD, r=0.45).move_to(P(5.6, -1.3))
        pa = pkt("A", CYAN, w=0.6, h=0.5, size=20).move_to(P(-4.1, -1.3))
        pb = pkt("B", AMBER, w=0.6, h=0.5, size=20).move_to(P(-4.8, -1.3))
        slots = VGroup(*[RoundedRectangle(width=0.7, height=0.6, corner_radius=0.08, color=BORDER_DIM, stroke_width=1.5) for _ in range(2)])
        slots.arrange(RIGHT, buff=0.15).move_to(P(3.0, -1.3))  # B (x~2.65), A (x~3.5)
        take = T("Gửi A rồi B  →  nhận A rồi B", 22, AMBER, bold=True).move_to(P(0, -2.65))
        play_voiced(self, "03_03", [
            ([FadeIn(hdr), FadeIn(r0), FadeIn(r1), FadeIn(src), FadeIn(dst)], 2.5),
            ([FadeIn(good, shift=DOWN * 0.1)], 1.5),
            ([FadeIn(mv), mv.animate.move_to(P(3.3, 1.5))], 3.0),
            ([Transform(dst, dst_f), FadeOut(mv)], 1.0),
            ([FadeIn(bad, shift=UP * 0.1)], 2.0),
            ([Create(sep), FadeIn(q0), FadeIn(q1), FadeIn(slots)], 2.0),
            ([FadeIn(pa), FadeIn(pb)], 1.0),
            ([pa.animate.move_to(slots[1].get_center()), pb.animate.move_to(slots[0].get_center())], 4.0),
            ([FadeIn(take, shift=UP * 0.1)], 1.5),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_04
    def seg04(self):
        hdr = make_header("Chi phí thông điệp: α + n / β", "t(n) = α + n / β", AMBER)
        ox, oy, Lx, Ly = -5.5, -2.5, 6.8, 3.9
        k = 3.5 / 25.0
        xax = Ar(P(ox, oy), P(ox + Lx, oy), color=TEXT_MUTED, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.05)
        yax = Ar(P(ox, oy), P(ox, oy + Ly), color=TEXT_MUTED, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.05)
        xl = T("n (byte)", 14, TEXT_MUTED).move_to(P(ox + Lx + 0.5, oy - 0.3))
        yl = T("t (μs)", 14, TEXT_MUTED).move_to(P(ox + 0.1, oy + Ly + 0.15))
        tick = T("1 MiB", 14, TEXT_MUTED).move_to(P(ox + 6.0, oy - 0.3))
        tk = Line(P(ox + 6.0, oy - 0.08), P(ox + 6.0, oy + 0.08), color=TEXT_MUTED)
        a0, a1 = P(ox, oy + 0.3 * k), P(ox + 6.0, oy + 23.8 * k)
        line = Line(a0, a1, color=CYAN, stroke_width=4)
        dot = Dot(a0, color=AMBER, radius=0.1)
        alpha_l = T("α = 0,106 μs", 15, AMBER, bold=True).move_to(P(ox + 2.4, oy + 0.45))
        guide = DashedLine(a1, P(ox, a1[1]), color=TEXT_MUTED)
        end_l = T("23,8 μs", 16, EMERALD, bold=True).move_to(a1 + UP * 0.35 + LEFT * 0.2)
        # right panel: 1 MiB qua bộ nhớ chung và qua TCP loopback
        x0, s = 1.6, 0.075
        inp = T("thông điệp 1 MiB", 15, TEXT_MUTED).move_to(P(4.0, 2.2))

        def bar_row(y, a_us, tot_us, col):
            a = Rectangle(width=max(a_us * s, 0.06), height=0.5, color=AMBER, stroke_width=1).set_fill(AMBER, 0.9)
            b = Rectangle(width=(tot_us - a_us) * s, height=0.5, color=col, stroke_width=1).set_fill(col, 0.85)
            a.move_to(P(x0 + a.width / 2, y))
            b.next_to(a, RIGHT, buff=0)
            return VGroup(a, b)
        row1 = bar_row(1.4, 0.106, 23.8, CYAN)
        row2 = bar_row(0.2, 2.63, 59.9, CORAL)
        l1 = T("bộ nhớ chung: 23,8 μs", 15, CYAN, bold=True).move_to(P(4.0, 1.9))
        l2 = T("TCP loopback: 59,9 μs", 15, CORAL, bold=True).move_to(P(4.0, 0.7))
        la = T("α = 2,63", 14, AMBER, bold=True).move_to(P(x0 + 0.1, -0.35))
        tot = T("nhỏ: chịu α · lớn: chịu băng thông", 17, AMBER, bold=True).move_to(P(3.9, -1.5))
        play_voiced(self, "03_04", [
            ([FadeIn(hdr), Create(xax), Create(yax), FadeIn(xl), FadeIn(yl), FadeIn(tick), FadeIn(tk)], 2.5),
            ([FadeIn(dot), FadeIn(alpha_l)], 2.0),
            ([Create(line), MoveAlongPath(dot, line)], 4.0),
            ([Create(guide), FadeIn(end_l, shift=UP * 0.1), Indicate(dot)], 2.0),
            ([FadeIn(inp), FadeIn(row1), FadeIn(l1)], 2.5),
            ([FadeIn(row2), FadeIn(l2), FadeIn(la)], 3.0),
            ([FadeIn(tot, shift=UP * 0.1)], 2.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_05
    def seg05(self):
        hdr = make_header("α phụ thuộc kênh truyền – gộp tin nhỏ", "Ryzen 9900X", AMBER)
        chart = make_bar_chart([0.106, 0.274, 2.63], ["shm gần", "shm xa", "TCP"], [EMERALD, CYAN, CORAL],
                               max_val=2.63, width=5.0, height=3.2, unit="μs").move_to(P(-3.5, -0.4))
        x25 = T("×25", 34, DARK, bold=True).move_to(P(-1.83, 0.3))
        # right: aggregation
        x0, u = 1.0, 0.62
        top_t = T("8 tin nhỏ", 15, TEXT_MAIN).move_to(P(3.0, 1.9))
        small = VGroup(*[Rectangle(width=u - 0.05, height=0.5, color=AMBER, stroke_width=1).set_fill(AMBER, 0.9) for _ in range(8)])
        small.arrange(RIGHT, buff=0.05).move_to(P(x0 + 4 * u, 1.3)).align_to(P(x0, 0), LEFT)
        sl = T("8 × α = 21 μs", 16, AMBER, bold=True).move_to(P(3.2, 0.7))
        bot_t = T("1 tin lớn", 15, TEXT_MAIN).move_to(P(3.0, -0.2))
        big = Rectangle(width=u - 0.05, height=0.5, color=EMERALD, stroke_width=1).set_fill(EMERALD, 0.9)
        big.move_to(P(x0 + (u - 0.05) / 2, -0.8))
        bl = T("1 × α = 2,63 μs", 16, EMERALD, bold=True).move_to(P(3.2, -1.4))
        take = T("Ít tin, tin to", 24, AMBER, bold=True).move_to(P(3.2, -2.5))
        play_voiced(self, "03_05", [
            ([FadeIn(hdr)], 0.8),
            ([FadeIn(chart[0]), FadeIn(chart[1])] + [GrowFromEdge(b[0], DOWN) for b in chart[2]] + [FadeIn(b[1]) for b in chart[2]] + [FadeIn(b[2]) for b in chart[2]], 4.0),
            ([FadeIn(x25, scale=1.4)], 2.0),
            ([FadeIn(top_t), LaggedStart(*[GrowFromEdge(r, UP) for r in small], lag_ratio=0.2)], 4.0),
            ([FadeIn(sl)], 1.5),
            ([FadeIn(bot_t), GrowFromEdge(big, LEFT)], 2.0),
            ([FadeIn(bl)], 1.5),
            ([FadeIn(take, shift=UP * 0.1)], 1.5),
        ])
        clear_stage(self)

    # ---------------------------------------------------------- sequence helper
    def seq_frame(self, cx0=-3.0, cx1=3.0, bottom=-2.7):
        b0 = box("rank 0", CYAN, w=1.5, h=0.5, size=16).move_to(P(cx0, 2.3))
        b1 = box("rank 1", EMERALD, w=1.5, h=0.5, size=16).move_to(P(cx1, 2.3))
        l0 = DashedLine(P(cx0, 2.05), P(cx0, bottom), color=BORDER_DIM, stroke_width=2)
        l1 = DashedLine(P(cx1, 2.05), P(cx1, bottom), color=BORDER_DIM, stroke_width=2)
        tl = Ar(P(-6.4, 1.8), P(-6.4, -1.8), color=TEXT_MUTED, buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        tt = T("thời gian", 12, TEXT_MUTED).rotate(PI / 2).move_to(P(-6.15, 0))
        return VGroup(b0, b1, l0, l1, tl, tt)

    def badge(self, lines, color, pos, w=2.5):
        txts = VGroup(*[T(s, 15, TEXT_MAIN if i else color, bold=(i == 0)) for i, s in enumerate(lines)]).arrange(DOWN, buff=0.1)
        if txts.width > w - 0.3:
            txts.scale_to_fit_width(w - 0.3)
        rect = RoundedRectangle(width=w, height=txts.height + 0.3, corner_radius=0.1, color=color, stroke_width=1.6).set_fill(PANEL_BG, 0.95)
        g = VGroup(rect, txts)
        txts.move_to(rect)
        return g.move_to(pos)

    # ------------------------------------------------------------------ 03_06
    def seg06(self):
        hdr = make_header("Giao thức Eager: Send trả về ngay", "n ≤ 4096 B", EMERALD)
        cx0, cx1 = -2.6, 2.4
        fr = self.seq_frame(cx0, cx1)
        bd = self.badge(["EAGER", "n = 1000 int", "4000 B ≤ 4096 B"], EMERALD, P(-5.0, 1.0), w=2.4)
        sbar = Rectangle(width=0.3, height=0.7, color=AMBER, stroke_width=1).set_fill(AMBER, 0.9).move_to(P(cx0, 1.45))
        sl = T("Send", 15, AMBER, bold=True).move_to(P(cx0 + 0.6, 1.8))
        buf = RoundedRectangle(width=1.5, height=0.5, corner_radius=0.08, color=VIOLET, stroke_width=2).move_to(P(cx1 + 1.9, 0.8))
        bl = T("buffer", 14, VIOLET).move_to(buf)
        data = pkt("4000B", AMBER, w=0.95, h=0.38, size=13).move_to(P(cx0 + 0.2, 1.3))
        ret = T("return ✓", 16, EMERALD, bold=True).move_to(P(cx0 + 0.95, 0.6))
        calc = Rectangle(width=0.3, height=2.2, color=CYAN, stroke_width=1).set_fill(CYAN, 0.5).move_to(P(cx0, -1.0))
        cl = T("tính tiếp", 14, CYAN).move_to(P(cx0 - 1.0, -1.0))
        rbar = Rectangle(width=0.3, height=0.7, color=EMERALD, stroke_width=1).set_fill(EMERALD, 0.9).move_to(P(cx1, -1.2))
        rl = T("Recv", 15, EMERALD, bold=True).move_to(P(cx1 - 0.6, -1.2))
        out = pkt("4000B", AMBER, w=0.95, h=0.38, size=13).move_to(buf.get_center())
        take = T("Eager: sao chép vào buffer rồi return", 20, AMBER, bold=True).move_to(P(0.5, -3.15))
        play_voiced(self, "03_06", [
            ([FadeIn(hdr), FadeIn(fr), FadeIn(bd)], 2.0),
            ([GrowFromEdge(sbar, UP), FadeIn(sl), FadeIn(buf), FadeIn(bl)], 2.0),
            ([FadeIn(data), MoveAlongPath(data, path((cx0 + 0.2, 1.3), (cx1, 0.9), (cx1 + 1.9, 0.8)))], 3.5),
            ([FadeIn(ret, scale=1.3), GrowFromEdge(calc, UP), FadeIn(cl)], 3.0),
            ([GrowFromEdge(rbar, UP), FadeIn(rl)], 2.0),
            ([FadeIn(out), FadeOut(data), out.animate.move_to(P(cx1 + 0.4, -1.2))], 3.0),
            ([FadeIn(take, shift=UP * 0.1)], 1.5),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_07
    def seg07(self):
        hdr = make_header("Giao thức Rendezvous: Send bị chặn", "n > 4096 B", CORAL)
        cx0, cx1 = -2.6, 2.4
        fr = self.seq_frame(cx0, cx1)
        bd = self.badge(["RENDEZVOUS", "n = 1005 int", "4020 B + header"], CORAL, P(-5.0, 1.0), w=2.4)
        sblock = Rectangle(width=0.3, height=2.7, color=CORAL, stroke_width=1).set_fill(CORAL, 0.85).move_to(P(cx0, 0.15))
        sl = T("Send chặn", 15, CORAL, bold=True).move_to(P(cx0 + 0.95, 1.8))
        busy = Rectangle(width=0.3, height=2.0, color=TEXT_MUTED, stroke_width=1).set_fill(TEXT_MUTED, 0.5).move_to(P(cx1, 0.45))
        bl = T("đang tính", 14, TEXT_MUTED).move_to(P(cx1 + 0.95, 0.45))
        rts = Ar(P(cx0 + 0.2, 1.4), P(cx1 - 0.2, 1.1), color=AMBER, buff=0, stroke_width=3)
        rtl = T("gửi?", 15, AMBER, bold=True).move_to(P(0, 1.55))
        rbar = Rectangle(width=0.3, height=1.4, color=EMERALD, stroke_width=1).set_fill(EMERALD, 0.9).move_to(P(cx1, -1.3))
        rl = T("Recv", 15, EMERALD, bold=True).move_to(P(cx1 + 0.6, -1.75))
        cts = Ar(P(cx1 - 0.2, -0.75), P(cx0 + 0.2, -1.0), color=EMERALD, buff=0, stroke_width=3)
        ctl = T("sẵn sàng", 15, EMERALD, bold=True).move_to(P(0, -0.55))
        data = pkt("4020B", AMBER, w=0.95, h=0.38, size=13).move_to(P(cx0 + 0.2, -1.2))
        done = T("return ✓", 16, EMERALD, bold=True).move_to(P(cx0 - 0.95, -2.05))
        take = T("Send chặn đến khi Recv sẵn sàng", 20, AMBER, bold=True).move_to(P(0.5, -3.15))
        play_voiced(self, "03_07", [
            ([FadeIn(hdr), FadeIn(fr), FadeIn(bd)], 2.0),
            ([GrowArrow(rts), FadeIn(rtl)], 1.5),
            ([GrowFromEdge(sblock, UP), FadeIn(sl), GrowFromEdge(busy, UP), FadeIn(bl)], 5.0),
            ([GrowFromEdge(rbar, UP), FadeIn(rl), GrowArrow(cts), FadeIn(ctl)], 3.0),
            ([FadeIn(data), MoveAlongPath(data, path((cx0 + 0.2, -1.2), (cx1 - 0.2, -1.7)))], 3.0),
            ([FadeIn(done, scale=1.3), sblock.animate.set_fill(EMERALD, 0.85).set_stroke(EMERALD)], 2.0),
            ([FadeIn(take, shift=UP * 0.1)], 1.5),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_08
    def seg08(self):
        hdr = make_header("Hai rank cùng Send: deadlock", "Send; Recv", CORAL)
        div = DashedLine(P(0, 2.5), P(0, -2.2), color=BORDER_DIM)

        def panel(cx, title, tcol, big):
            t = T(title, 20, tcol, bold=True).move_to(P(cx, 2.1))
            a = rank_node(0, CYAN, r=0.45).move_to(P(cx - 2.3, 0.5))
            b = rank_node(1, EMERALD, r=0.45).move_to(P(cx + 2.3, 0.5))
            ca = box("Send; Recv", CYAN, w=1.7, h=0.5, size=14).move_to(P(cx - 2.3, -0.4))
            cb = box("Send; Recv", EMERALD, w=1.7, h=0.5, size=14).move_to(P(cx + 2.3, -0.4))
            w = 1.1 if big else 0.55
            m1 = pkt("", AMBER, w=w, h=0.4).move_to(P(cx - 1.7, 0.95))
            m2 = pkt("", AMBER, w=w, h=0.4).move_to(P(cx + 1.7, 0.2))
            return t, a, b, ca, cb, m1, m2
        tL, aL, bL, caL, cbL, m1L, m2L = panel(-3.3, "n = 1000 int  (Eager)", EMERALD, False)
        tR, aR, bR, caR, cbR, m1R, m2R = panel(3.3, "n = 2000 int  (Rendezvous)", CORAL, True)
        okL = T("✓ chạy bình thường", 20, EMERALD, bold=True).move_to(P(-3.3, -1.5))
        xr = T("✗", 40, CORAL, bold=True).move_to(P(3.3, 0.57))
        dl = T("DEADLOCK", 28, CORAL, bold=True).move_to(P(3.3, -1.5))
        take = T("Ngưỡng Eager ≈ 4096 B", 20, AMBER, bold=True).move_to(P(0, -2.75))
        play_voiced(self, "03_08", [
            ([FadeIn(hdr), Create(div)], 1.0),
            ([FadeIn(tL), FadeIn(aL), FadeIn(bL), FadeIn(caL), FadeIn(cbL),
              FadeIn(tR), FadeIn(aR), FadeIn(bR), FadeIn(caR), FadeIn(cbR)], 2.5),
            ([FadeIn(m1L), FadeIn(m2L), FadeIn(m1R), FadeIn(m2R)], 1.0),
            ([m1L.animate.move_to(P(-3.3 + 1.7, 0.95)), m2L.animate.move_to(P(-3.3 - 1.7, 0.2)),
              m1R.animate.move_to(P(3.3 - 0.6, 0.95)), m2R.animate.move_to(P(3.3 + 0.6, 0.2))], 3.5),
            ([FadeIn(okL, shift=UP * 0.1), FadeOut(m1L), FadeOut(m2L)], 1.5),
            ([FadeIn(xr, scale=1.5), FadeIn(dl, scale=1.3), Wiggle(m1R), Wiggle(m2R)], 3.0),
            ([FadeIn(take, shift=UP * 0.1)], 1.5),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_09
    def seg09(self):
        hdr = make_header("3 cách sửa deadlock", "an toàn", EMERALD)
        cxs = [-4.4, 0.0, 4.4]
        titles = ["① Sắp thứ tự", "② Sendrecv", "③ Isend + Irecv"]
        cols = [AMBER, CYAN, VIOLET]
        divs = VGroup(DashedLine(P(-2.2, 2.5), P(-2.2, -2.4), color=BORDER_DIM), DashedLine(P(2.2, 2.5), P(2.2, -2.4), color=BORDER_DIM))
        ts = VGroup(*[T(titles[i], 19, cols[i], bold=True).move_to(P(cxs[i], 2.15)) for i in range(3)])
        circ = VGroup()
        for cx in cxs:
            circ.add(rank_node(0, CYAN, r=0.4, label="0").move_to(P(cx - 1.4, 0.6)),
                     rank_node(1, EMERALD, r=0.4, label="1").move_to(P(cx + 1.4, 0.6)))
        sub = VGroup(
            T("rank 0: Send→Recv", 13, TEXT_MUTED, MONO).move_to(P(cxs[0], -0.35)),
            T("rank 1: Recv→Send", 13, TEXT_MUTED, MONO).move_to(P(cxs[0], -0.7)),
            T("gộp gửi + nhận", 14, TEXT_MUTED).move_to(P(cxs[1], -0.5)),
            T("khởi động cả hai", 14, TEXT_MUTED).move_to(P(cxs[2], -0.5)),
        )
        # panel 1: sequential
        a1 = pkt("1", AMBER, w=0.45).move_to(P(cxs[0] - 0.65, 1.0))
        a2 = pkt("2", AMBER, w=0.45).move_to(P(cxs[0] + 0.65, 0.2))
        # panel 2: simultaneous
        b1 = pkt("", CYAN, w=0.45).move_to(P(cxs[1] - 0.65, 1.0))
        b2 = pkt("", CYAN, w=0.45).move_to(P(cxs[1] + 0.65, 0.2))
        # panel 3
        c1 = pkt("", VIOLET, w=0.45).move_to(P(cxs[2] - 0.65, 1.0))
        c2 = pkt("", VIOLET, w=0.45).move_to(P(cxs[2] + 0.65, 0.2))
        wbar_bg = Rectangle(width=2.6, height=0.28, color=VIOLET, stroke_width=1.5).move_to(P(cxs[2], -1.3))
        wbar = Rectangle(width=2.6, height=0.28, color=VIOLET, stroke_width=0).set_fill(VIOLET, 0.8).move_to(P(cxs[2], -1.3))
        wl = T("Waitall", 14, VIOLET, bold=True).move_to(P(cxs[2], -1.75))
        warn = T("không đụng buffer trước Wait", 14, CORAL).move_to(P(cxs[2], -2.2))
        oks = VGroup(*[T("✓", 34, EMERALD, bold=True).move_to(P(cx, -1.4)) for cx in cxs[:2]])
        oks.add(T("✓", 34, EMERALD, bold=True).move_to(P(cxs[2] + 1.6, -1.3)))
        play_voiced(self, "03_09", [
            ([FadeIn(hdr), Create(divs), FadeIn(ts), FadeIn(circ)], 2.5),
            ([FadeIn(sub[0]), FadeIn(sub[1]), FadeIn(a1), a1.animate.move_to(P(cxs[0] + 0.65, 1.0))], 3.0),
            ([FadeIn(a2), a2.animate.move_to(P(cxs[0] - 0.65, 0.2))], 3.0),
            ([FadeIn(sub[2]), FadeIn(b1), FadeIn(b2), b1.animate.move_to(P(cxs[1] + 0.65, 1.0)), b2.animate.move_to(P(cxs[1] - 0.65, 0.2))], 3.0),
            ([FadeIn(sub[3]), FadeIn(c1), FadeIn(c2), c1.animate.move_to(P(cxs[2] + 0.65, 1.0)), c2.animate.move_to(P(cxs[2] - 0.65, 0.2))], 3.0),
            ([FadeIn(wbar_bg), FadeIn(wl), GrowFromEdge(wbar, LEFT)], 3.0),
            ([FadeIn(oks[0]), FadeIn(oks[1]), FadeIn(oks[2]), FadeIn(warn)], 2.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_10
    def seg10(self):
        hdr = make_header("MPI_Bcast: cây log₂ p bước", "p = 8", CYAN)
        xs = [-5.25 + 1.5 * i for i in range(8)]
        ny = -0.3
        nodes = [rank_node(i, CYAN, r=0.38, label=str(i)).move_to(P(xs[i], ny)) for i in range(8)]
        for n in nodes:
            n[0].set_fill(PANEL_BG, 1)
        tags = [T("42", 18, AMBER, MONO, True).move_to(P(xs[i], ny - 0.8)) for i in range(8)]
        f = T("log₂ 8 = 3 bước", 24, AMBER, bold=True).move_to(P(0, 2.2))
        steps = [[(0, 4)], [(0, 2), (4, 6)], [(0, 1), (2, 3), (4, 5), (6, 7)]]
        cols = [CORAL, EMERALD, CYAN]

        def arcs(step, col):
            g = VGroup()
            for a, b in step:
                ar = CurvedArrow(P(xs[a] + 0.1, ny + 0.4), P(xs[b] - 0.1, ny + 0.4), angle=-TAU / 4, color=col, stroke_width=3.5, tip_length=0.18)
                g.add(ar)
            return g
        arc_g = [arcs(s, c) for s, c in zip(steps, cols)]
        cnt = [T(f"có dữ liệu: {n}", 20, TEXT_MAIN, bold=True).move_to(P(0, -2.4)) for n in (1, 2, 4, 8)]
        recv = [[4], [2, 6], [1, 3, 5, 7]]
        anims = [([FadeIn(hdr), FadeIn(f)] + [FadeIn(n) for n in nodes], 2.5),
                 ([nodes[0][0].animate.set_fill(AMBER, 0.45), FadeIn(tags[0]), FadeIn(cnt[0])], 1.5)]
        for si in range(3):
            a = [Create(x) for x in arc_g[si]]
            a += [nodes[j][0].animate.set_fill(AMBER, 0.45) for j in recv[si]]
            a += [FadeIn(tags[j], scale=1.3) for j in recv[si]]
            a += [Transform(cnt[0], cnt[si + 1])]
            anims.append((a, 3.5))
        play_voiced(self, "03_10", anims)
        clear_stage(self)

    # ------------------------------------------------------------------ 03_11
    def seg11(self):
        hdr = make_header("Scatter → tính → Gather", "root = rank 0", EMERALD)
        xs = [-4.5, -1.5, 1.5, 4.5]
        root = rank_node(0, CYAN, r=0.42, label="root").move_to(P(-4.4, 1.7))
        arr = VGroup(*[box(str(v), CYAN, w=1.2, h=0.7, size=22) for v in (10, 20, 30, 40)]).arrange(RIGHT, buff=0.03).move_to(P(0, 1.7))
        ranks = VGroup(*[rank_node(i, r=0.42).move_to(P(xs[i], -2.1)) for i in range(4)])
        cells = VGroup(*[box("·", RANK_COLORS[i], w=1.2, h=0.7, size=22).move_to(P(xs[i], -0.8)) for i in range(4)])
        lab = [T(s, 22, AMBER, bold=True).move_to(P(4.3, 1.7)) for s in ("Scatter", "Tính: × 2", "Gather")]
        sc = [arr[i].copy() for i in range(4)]
        full = [box(str(v), RANK_COLORS[i], w=1.2, h=0.7, size=22).move_to(P(xs[i], -0.8)) for i, v in enumerate((10, 20, 30, 40))]
        dbl = [box(str(v), AMBER, w=1.2, h=0.7, size=22).move_to(P(xs[i], -0.8)) for i, v in enumerate((20, 40, 60, 80))]
        back = [d.copy() for d in dbl]
        root_dbl = VGroup(*[box(str(v), AMBER, w=1.2, h=0.7, size=22) for v in (20, 40, 60, 80)]).arrange(RIGHT, buff=0.03).move_to(P(0, 1.7))
        play_voiced(self, "03_11", [
            ([FadeIn(hdr), FadeIn(root), FadeIn(arr), FadeIn(ranks), FadeIn(cells)], 2.5),
            ([FadeIn(lab[0])], 1.0),
            ([sc[i].animate.move_to(P(xs[i], -0.8)) for i in range(4)], 4.0),
            ([Transform(lab[0], lab[1])] + [Transform(cells[i], dbl[i]) for i in range(4)] + [FadeOut(s) for s in sc], 3.5),
            ([Transform(lab[0], lab[2])], 1.0),
            ([FadeIn(back[i]) for i in range(4)] + [back[i].animate.move_to(arr[i].get_center()) for i in range(4)], 4.0),
            ([Transform(arr, root_dbl)] + [FadeOut(b) for b in back], 2.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_12
    def seg12(self):
        hdr = make_header("Reduce / Allreduce với SUM", "3 + 1 + 4 + 2", VIOLET)
        xs = [-4.5, -1.5, 1.5, 4.5]
        ranks = VGroup(*[rank_node(i, r=0.42).move_to(P(xs[i], -2.2)) for i in range(4)])
        vals = VGroup(*[box(str(v), RANK_COLORS[i], w=1.0, h=0.65, size=22).move_to(P(xs[i], -1.05)) for i, v in enumerate((3, 1, 4, 2))])
        m1 = box("3+1 = 4", AMBER, w=1.5, h=0.55, size=17).move_to(P(-3.0, 0.2))
        m2 = box("4+2 = 6", AMBER, w=1.5, h=0.55, size=17).move_to(P(3.0, 0.2))
        top = box("4+6 = 10", EMERALD, w=1.8, h=0.6, size=18).move_to(P(0, 1.7))

        def up(a, b):
            return Ar(a, b, color=TEXT_MUTED, buff=0.05, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)
        ups = [up(vals[0].get_top(), m1.get_bottom() + LEFT * 0.4), up(vals[1].get_top(), m1.get_bottom() + RIGHT * 0.4),
               up(vals[2].get_top(), m2.get_bottom() + LEFT * 0.4), up(vals[3].get_top(), m2.get_bottom() + RIGHT * 0.4)]
        ups2 = [up(m1.get_top(), top.get_bottom() + LEFT * 0.4), up(m2.get_top(), top.get_bottom() + RIGHT * 0.4)]
        lab = [T(s, 20, AMBER, bold=True).move_to(P(4.9, 1.7)) for s in ("Reduce (SUM)", "Allreduce (SUM)")]
        res0 = box("10", EMERALD, w=1.0, h=0.65, size=22).move_to(vals[0])
        top2 = box("10", EMERALD, w=1.2, h=0.6, size=22).move_to(P(0, 0.9))
        arr0 = Ar(top2.get_bottom() + LEFT * 0.3, vals[0].get_top(), color=EMERALD, buff=0.08, stroke_width=3)
        arrs = [Ar(top2.get_bottom(), vals[i].get_top(), color=EMERALD, buff=0.08, stroke_width=3) for i in (1, 2, 3)]
        play_voiced(self, "03_12", [
            ([FadeIn(hdr), FadeIn(ranks), FadeIn(vals)], 2.5),
            ([FadeIn(lab[0])] + [GrowArrow(a) for a in ups[:2]] + [FadeIn(m1, shift=UP * 0.2)], 3.0),
            ([GrowArrow(a) for a in ups[2:]] + [FadeIn(m2, shift=UP * 0.2)], 3.0),
            ([GrowArrow(a) for a in ups2] + [FadeIn(top, shift=UP * 0.2)], 3.0),
            ([FadeOut(VGroup(m1, m2, *ups, *ups2, top)), FadeIn(top2)], 1.5),
            ([GrowArrow(arr0), Transform(vals[0], res0)], 3.0),
            ([Transform(lab[0], lab[1])] + [GrowArrow(a) for a in arrs] +
             [Transform(vals[i], box("10", EMERALD, w=1.0, h=0.65, size=22).move_to(vals[i])) for i in (1, 2, 3)], 4.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_13
    def seg13(self):
        hdr = make_header("MPI_Scan: tổng tiền tố", "1,2,3,4 → 1,3,6,10", AMBER)
        xs = [-4.5, -1.5, 1.5, 4.5]
        ins = VGroup(*[box(str(v), RANK_COLORS[i], w=1.2, h=0.7, size=24).move_to(P(xs[i], 1.5)) for i, v in enumerate((1, 2, 3, 4))])
        outs = VGroup(*[box("·", BORDER_DIM, w=1.2, h=0.7, size=24).move_to(P(xs[i], -0.7)) for i in range(4)])
        ranks = VGroup(*[T(f"rank {i}", 15, RANK_COLORS[i], bold=True).move_to(P(xs[i], -2.2)) for i in range(4)])
        exprs = ["1", "1+2", "1+2+3", "1+2+3+4"]
        res = [1, 3, 6, 10]

        def hl(i):
            return RoundedRectangle(width=(xs[i] - xs[0]) + 1.5, height=1.0, corner_radius=0.1, color=EMERALD, stroke_width=3
                                    ).set_fill(EMERALD, 0.18).move_to(P((xs[0] + xs[i]) / 2, 1.5))
        h = hl(0)
        steps = [([FadeIn(hdr), FadeIn(ins), FadeIn(outs), FadeIn(ranks), Create(h)], 3.0)]
        elabs = []
        for i in range(4):
            ar = Ar(P(xs[i], 0.95), P(xs[i], -0.25), color=EMERALD, buff=0, stroke_width=3)
            el = T(exprs[i], 16, TEXT_MUTED, MONO).move_to(P(xs[i], -1.4))
            newout = box(str(res[i]), EMERALD, w=1.2, h=0.7, size=26).move_to(outs[i])
            a = [GrowArrow(ar), FadeIn(el), Transform(outs[i], newout)]
            if i > 0:
                a.append(Transform(h, hl(i)))
            steps.append((a, 2.8))
            elabs.append((ar, el))
        play_voiced(self, "03_13", steps)
        clear_stage(self)

    # ------------------------------------------------------------------ 03_14
    def seg14(self):
        hdr = make_header("MPI_Alltoall = chuyển vị", "hàng ↔ cột", CORAL)
        cw, ch = 1.2, 0.68
        cx = lambda c: -2.025 + 1.35 * c
        ry = lambda r: 1.5 - 1.0 * r
        letters = "ABCD"
        cells = [[box(f"{letters[r]}{c}", RANK_COLORS[r], w=cw, h=ch, size=22).move_to(P(cx(c), ry(r))) for c in range(4)] for r in range(4)]
        allc = VGroup(*[cells[r][c] for r in range(4) for c in range(4)])
        rl = VGroup(*[T(f"rank {r}", 16, RANK_COLORS[r], bold=True).move_to(P(-4.4, ry(r))) for r in range(4)])
        pointer = Ar(P(cx(1), ry(0) - 0.4), P(cx(0), ry(1) + 0.4), color=AMBER, buff=0, stroke_width=3)
        pointer2 = Ar(P(cx(1), ry(0) - 0.4), P(cx(0) + 0.5, ry(1) + 0.4), color=AMBER, buff=0, stroke_width=3)
        take = T("rank k nhận phần thứ k của mọi rank", 20, AMBER, bold=True).move_to(P(0, -2.65))
        moves = []
        for r in range(4):
            for c in range(4):
                if r != c:
                    moves.append(cells[r][c].animate.move_to(P(cx(r), ry(c))))
        play_voiced(self, "03_14", [
            ([FadeIn(hdr), FadeIn(rl), LaggedStart(*[FadeIn(c) for c in allc], lag_ratio=0.05)], 3.0),
            ([Indicate(cells[0][1], color=AMBER, scale_factor=1.3), Create(pointer2)], 3.0),
            ([FadeOut(pointer2)] + moves, 5.0),
            ([FadeIn(take, shift=UP * 0.1)], 2.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_15
    def seg15(self):
        hdr = make_header("Trao đổi halo (ghost cell)", "1D, 4 rank", VIOLET)
        bw = 0.5
        bx = lambda i: -5.525 + i * 2.85
        by = 0.55
        blocks, real, ghostL, ghostR = [], [], [], []
        for i in range(4):
            x = bx(i)
            gl = RoundedRectangle(width=bw, height=0.55, corner_radius=0.05, color=TEXT_MUTED, stroke_width=1.5).move_to(P(x + bw / 2, by))
            gr = RoundedRectangle(width=bw, height=0.55, corner_radius=0.05, color=TEXT_MUTED, stroke_width=1.5).move_to(P(x + 2.5 - bw / 2, by))
            gl = DashedVMobject(gl, num_dashes=14); gr = DashedVMobject(gr, num_dashes=14)
            rr = [box(str(3 * i + j + 1), RANK_COLORS[i], w=bw, h=0.55, size=15).move_to(P(x + bw * (j + 1.5), by)) for j in range(3)]
            real.append(rr)
            ghostL.append(gl); ghostR.append(gr)
            blocks.append(VGroup(gl, gr, *rr))
        grp = VGroup(*blocks)
        rl = VGroup(*[T(f"rank {i}", 15, RANK_COLORS[i], bold=True).move_to(P(bx(i) + 1.25, -1.5)) for i in range(4)])
        null_l = T("∅", 20, CORAL, bold=True).move_to(P(bx(0) + bw / 2, by))
        null_r = T("∅", 20, CORAL, bold=True).move_to(P(bx(3) + 2.5 - bw / 2, by))
        code = T("up = rank > 0 ? rank − 1 : MPI_PROC_NULL", 18, TEXT_MAIN, MONO).move_to(P(0, -2.6))
        steps = [([FadeIn(hdr), FadeIn(grp), FadeIn(rl)], 2.5), ([FadeIn(null_l), FadeIn(null_r)], 1.5)]
        # phase 1: send right (above)
        sendR = []
        copies = []
        for i in range(4):
            cp = real[i][2].copy()
            copies.append(cp)
        anims = []
        for i in range(3):
            tx, ty = bx(i + 1) + bw / 2, by
            sx = real[i][2].get_center()
            anims.append(MoveAlongPath(copies[i], path((sx[0], by), (sx[0], 1.3), (tx, 1.3), (tx, by))))
        sx3 = real[3][2].get_center()
        anims.append(MoveAlongPath(copies[3], path((sx3[0], by), (sx3[0], 1.3), (6.2, 1.3))))
        steps.append(([FadeIn(c) for c in copies], 0.8))
        steps.append((anims, 3.5))
        x1 = T("✗", 30, CORAL, bold=True).move_to(P(6.2, 1.3))
        steps.append(([FadeIn(x1, scale=1.4), FadeOut(copies[3])], 1.5))
        # phase 2: send left (below)
        copies2 = [real[i][0].copy() for i in range(4)]
        anims2 = []
        for i in range(1, 4):
            tx = bx(i - 1) + 2.5 - bw / 2
            sx = real[i][0].get_center()
            anims2.append(MoveAlongPath(copies2[i], path((sx[0], by), (sx[0], -0.55), (tx, -0.55), (tx, by))))
        sx0 = real[0][0].get_center()
        anims2.append(MoveAlongPath(copies2[0], path((sx0[0], by), (sx0[0], -0.55), (-6.2, -0.55))))
        x2 = T("✗", 30, CORAL, bold=True).move_to(P(-6.2, -0.55))
        steps.append(([FadeIn(c) for c in copies2], 0.8))
        steps.append((anims2, 3.5))
        steps.append(([FadeIn(x2, scale=1.4), FadeOut(copies2[0])], 1.5))
        steps.append(([FadeIn(code, shift=UP * 0.1)], 2.0))
        play_voiced(self, "03_15", steps)
        clear_stage(self)

    # ------------------------------------------------------------------ 03_16
    def seg16(self):
        hdr = make_header("Đo thời gian: Barrier → Wtime → MAX", "Ch. 4", CYAN)
        x0, u = -4.6, 1.15
        durs = [2.4, 3.1, 4.2, 2.8]
        ys = [1.5, 0.5, -0.5, -1.5]
        rl = VGroup(*[T(f"rank {i}", 15, RANK_COLORS[i], bold=True).move_to(P(-5.6, ys[i])) for i in range(4)])
        bar_line = DashedLine(P(x0, 2.3), P(x0, -2.2), color=AMBER, stroke_width=3)
        bar_lab = T("MPI_Barrier", 16, AMBER, MONO, True).move_to(P(x0 + 0.1, 2.5)).shift(RIGHT * 0.9)
        bars = VGroup(*[Rectangle(width=durs[i] * u, height=0.5, color=RANK_COLORS[i], stroke_width=1).set_fill(RANK_COLORS[i], 0.8)
                        .move_to(P(x0 + durs[i] * u / 2, ys[i])) for i in range(4)])
        nums = VGroup(*[T(f"{durs[i]:g} s".replace(".", ","), 16, TEXT_MAIN, MONO, True).move_to(P(x0 + durs[i] * u + 0.55, ys[i])) for i in range(4)])
        endl = DashedLine(P(x0 + 4.2 * u, 2.0), P(x0 + 4.2 * u, -2.0), color=CORAL, stroke_width=2)
        res = box("T = max = 4,2 s", EMERALD, w=2.9, h=0.7, size=18).move_to(P(4.6, 0.0))
        rlab = T("MPI_Reduce(MAX)", 15, EMERALD, MONO, True).move_to(P(4.6, 0.7))
        arrs = VGroup(*[Ar(nums[i].get_right() + RIGHT * 0.05, P(3.1, 0.22 * (1.5 - i)), color=EMERALD, buff=0.05, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
                        for i in range(4)])
        play_voiced(self, "03_16", [
            ([FadeIn(hdr), FadeIn(rl), Create(bar_line), FadeIn(bar_lab)], 3.0),
            ([GrowFromEdge(b, LEFT) for b in bars], 6.0),
            ([FadeIn(n) for n in nums], 2.0),
            ([FadeIn(rlab), LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2)], 3.0),
            ([FadeIn(res, scale=1.1), Create(endl), Indicate(bars[2], color=CORAL)], 3.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ gantt helper
    COSTS = [4, 1, 3, 1, 2, 1, 4, 1, 3, 1, 2, 1]
    COST_COL = {1: CYAN, 2: EMERALD, 3: AMBER, 4: CORAL}

    def gantt(self, assign, x0, ys, u, rh=0.28):
        """assign: list of (worker, start, cost). Returns (blocks list, rows, end_line, T)."""
        blocks = []
        for (w, s, c) in assign:
            col = self.COST_COL[c]
            r = Rectangle(width=c * u - 0.04, height=rh, color=DARK, stroke_width=1).set_fill(col, 0.9)
            r.move_to(P(x0 + (s + c / 2) * u, ys[w]))
            t = T(str(c), 12, DARK, MONO, True).move_to(r)
            blocks.append(VGroup(r, t))
        return blocks

    # ------------------------------------------------------------------ 03_17
    def seg17(self):
        hdr = make_header("Cân bằng tải: block vs cyclic", "12 công việc, 4 rank", AMBER)
        c = self.COSTS
        x0, u = -3.9, 0.7
        ys1 = [1.95, 1.55, 1.15, 0.75]
        ys2 = [-0.65, -1.05, -1.45, -1.85]
        # block
        t = [0] * 4
        blk = []
        for i, ci in enumerate(c):
            w = i // 3
            blk.append((w, t[w], ci)); t[w] += ci
        Tb = max(t)
        t = [0] * 4
        cyc = []
        for i, ci in enumerate(c):
            w = i % 4
            cyc.append((w, t[w], ci)); t[w] += ci
        Tc = max(t)
        B = self.gantt(blk, x0, ys1, u, rh=0.36)
        C = self.gantt(cyc, x0, ys2, u, rh=0.36)
        lab = lambda ys, col: VGroup(*[T(f"r{i}", 13, TEXT_MUTED, MONO).move_to(P(x0 - 0.35, ys[i])) for i in range(4)])
        l1, l2 = lab(ys1, 0), lab(ys2, 0)
        n1 = T("Block", 20, CYAN, bold=True).move_to(P(-5.6, 1.35))
        n2 = T("Cyclic", 20, CORAL, bold=True).move_to(P(-5.6, -1.25))
        for n in (n1, n2):
            n.scale_to_fit_width(1.0) if n.width > 1.0 else None
        e1 = DashedLine(P(x0 + Tb * u, 2.3), P(x0 + Tb * u, 0.45), color=AMBER, stroke_width=2.5)
        e2 = DashedLine(P(x0 + Tc * u, -0.3), P(x0 + Tc * u, -2.2), color=AMBER, stroke_width=2.5)
        t1 = T(f"T = {Tb}", 30, CYAN, bold=True).move_to(P(4.9, 1.35))
        t2 = T(f"T = {Tc}", 30, CORAL, bold=True).move_to(P(4.9, -1.25))
        sep = DashedLine(P(-6.3, 0.15), P(6.3, 0.15), color=BORDER_DIM)
        play_voiced(self, "03_17", [
            ([FadeIn(hdr), FadeIn(n1), FadeIn(l1), Create(sep)], 2.0),
            ([LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in B], lag_ratio=0.2)], 5.0),
            ([Create(e1), FadeIn(t1, scale=1.2)], 2.0),
            ([FadeIn(n2), FadeIn(l2)], 1.0),
            ([LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in C], lag_ratio=0.2)], 5.0),
            ([Create(e2), FadeIn(t2, scale=1.2)], 2.0),
            ([Indicate(VGroup(*[C[i] for i in range(12) if i % 4 in (0, 2)]), color=CORAL)], 3.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_18
    def seg18(self):
        hdr = make_header("Manager–Worker: chia tải động", "worker rảnh → nhận việc", EMERALD)
        c = self.COSTS
        x0, u = -3.3, 0.68
        ys = [0.8, 0.35, -0.1, -0.55]
        # greedy schedule
        free = [0] * 4
        sched = []
        for ci in c:
            w = free.index(min(free))
            sched.append((w, free[w], ci)); free[w] += ci
        Tm = max(free)
        G = self.gantt(sched, x0, ys, u, rh=0.38)
        mgr = rank_node(0, EMERALD, r=0.42, label="M").move_to(P(-5.5, 0.12))
        qs = VGroup(*[Rectangle(width=0.42, height=0.42, color=DARK, stroke_width=1).set_fill(self.COST_COL[ci], 0.9) for ci in c])
        qs.arrange(RIGHT, buff=0.04).move_to(P(-1.0, 2.0))
        rl = VGroup(*[T(f"w{i + 1}", 13, TEXT_MUTED, MONO).move_to(P(x0 - 0.35, ys[i])) for i in range(4)])
        endl = DashedLine(P(x0 + Tm * u, 1.2), P(x0 + Tm * u, -0.95), color=AMBER, stroke_width=2.5)
        tl = T(f"T = {Tm}", 24, EMERALD, bold=True).move_to(P(x0 + Tm * u + 0.2, 1.45))
        chart = make_bar_chart([9, 8, Tm], ["cyclic", "block", "mgr"], [CORAL, CYAN, EMERALD], max_val=9,
                               width=3.6, height=2.6, unit="").move_to(P(4.6, -0.6))
        disp = VGroup(*[Line(mgr[0].get_right(), P(x0 - 0.7, ys[i]), color=BORDER_DIM, stroke_width=1.5) for i in range(4)])
        lg = []
        for i, (w, s, ci) in enumerate(sched):
            lg.append(AnimationGroup(FadeOut(qs[i], shift=DOWN * 0.3), FadeIn(G[i], shift=RIGHT * 0.2)))
        play_voiced(self, "03_18", [
            ([FadeIn(hdr), FadeIn(mgr), FadeIn(qs), FadeIn(rl), FadeIn(disp)], 2.5),
            ([LaggedStart(*lg, lag_ratio=0.4)], 8.0),
            ([Create(endl), FadeIn(tl, scale=1.2)], 2.0),
            ([FadeIn(chart[0]), FadeIn(chart[1])] + [GrowFromEdge(b[0], DOWN) for b in chart[2]] +
             [FadeIn(b[1]) for b in chart[2]] + [FadeIn(b[2]) for b in chart[2]], 4.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_19
    def seg19(self):
        hdr = make_header("Hybrid: MPI giữa node + OpenMP trong node", "FUNNELED", VIOLET)
        cxs = [-3.4, 3.4]
        nodes = VGroup(*[RoundedRectangle(width=4.8, height=3.4, corner_radius=0.2, color=BORDER_DIM, stroke_width=2).set_fill(PANEL_BG, 0.6).move_to(P(cx, 0.1))
                         for cx in cxs])
        rk = [rank_node(i, RANK_COLORS[i], r=0.45).move_to(P(cxs[i], 1.1)) for i in range(2)]
        thr = []
        for i in range(2):
            row = []
            for j in range(4):
                d = Circle(radius=0.28, color=AMBER if j == 0 else CYAN, stroke_width=2).set_fill(AMBER if j == 0 else CYAN, 0.35)
                d.move_to(P(cxs[i] - 1.65 + 1.1 * j, -0.5))
                row.append(d)
            thr.append(row)
        links = VGroup(*[Line(rk[i][0].get_bottom(), thr[i][j].get_top(), color=TEXT_MUTED, stroke_width=1.5) for i in range(2) for j in range(4)])
        allthr = VGroup(*[d for r in thr for d in r])
        p = pkt("MPI", AMBER, w=0.8, h=0.4).move_to(rk[0][0].get_right() + RIGHT * 0.5)
        mainl = T("thread chính", 13, AMBER).move_to(P(cxs[0] - 1.65, -1.05))
        code = T("MPI_Init_thread(…, MPI_THREAD_FUNNELED)", 18, TEXT_MAIN, MONO).move_to(P(0, -2.4))
        pulses = [Indicate(d, color=AMBER, scale_factor=1.35) for r in thr for d in r[1:]]
        play_voiced(self, "03_19", [
            ([FadeIn(hdr), FadeIn(nodes)], 1.5),
            ([FadeIn(rk[0]), FadeIn(rk[1])], 1.5),
            ([FadeIn(allthr), Create(links), FadeIn(mainl)], 2.5),
            ([LaggedStart(*pulses, lag_ratio=0.1)], 4.0),
            ([FadeIn(p), p.animate.move_to(rk[1][0].get_left() + LEFT * 0.5)], 4.0),
            ([FadeOut(p), Indicate(thr[0][0], color=AMBER, scale_factor=1.5), Indicate(thr[1][0], color=AMBER, scale_factor=1.5)], 2.0),
            ([FadeIn(code, shift=UP * 0.1)], 2.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_20
    def seg20(self):
        hdr = make_header("Tính π: MPI_Bcast + MPI_Reduce", "n = 10^9", CYAN)
        xs = [-4.8, -1.6, 1.6, 4.8]
        ranks = VGroup(*[rank_node(i).move_to(P(xs[i], 2.15)) for i in range(4)])
        n0 = box("n = 10^9", AMBER, w=1.9, h=0.45, size=15).move_to(P(xs[0], 1.4))
        nb = VGroup(*[box("n", AMBER, w=0.9, h=0.45, size=15).move_to(P(xs[i], 1.4)) for i in range(1, 4)])
        bl = T("MPI_Bcast", 15, AMBER, MONO, True).move_to(P(0, 1.4))
        pk = [pkt("n", AMBER, w=0.5, h=0.34, size=13).move_to(P(xs[0] + 0.6, 1.4)) for _ in range(3)]
        cx = [-5.39 + 0.98 * i for i in range(12)]
        neutral = VGroup(*[box(str(i), TEXT_MUTED, w=0.82, h=0.5, size=15).move_to(P(cx[i], 0.5)) for i in range(12)])
        colored = VGroup(*[box(str(i), RANK_COLORS[i % 4], w=0.82, h=0.5, size=15).move_to(P(cx[i], 0.5)) for i in range(12)])
        loop = T("for (i = rank; i < n; i += size)", 15, TEXT_MAIN, MONO).move_to(P(0, -0.1))
        labs = ["f(0)+f(4)+f(8)", "f(1)+f(5)+f(9)", "f(2)+f(6)+f(10)", "f(3)+f(7)+f(11)"]
        parts = VGroup(*[box(labs[i], RANK_COLORS[i], w=2.8, h=0.5, size=14).move_to(P(xs[i], -0.85)) for i in range(4)])
        pibox = box("π ≈ 3,14159", EMERALD, w=2.5, h=0.6, size=18).move_to(P(-1.5, -2.2))
        arrs = VGroup(*[Ar(parts[i].get_bottom() + DOWN * 0.03, pibox.get_top() + RIGHT * (0.5 * (i - 1.5)), color=RANK_COLORS[i], buff=0.05,
                           stroke_width=2.5, max_tip_length_to_length_ratio=0.15) for i in range(4)])
        rl = T("MPI_Reduce(SUM, root = 0)", 15, EMERALD, MONO, True).move_to(P(-4.7, -2.2))
        sp1 = T("1 → 12 rank: 0,719 s → 0,065 s", 17, TEXT_MAIN).move_to(P(3.9, -2.35))
        sp2 = T("tăng tốc 11,1×", 24, EMERALD, bold=True).move_to(P(3.9, -2.9))
        play_voiced(self, "03_20", [
            ([FadeIn(hdr), FadeIn(ranks), FadeIn(n0)], 2.5),
            ([FadeIn(bl)] + [FadeIn(p) for p in pk] + [pk[i].animate.move_to(P(xs[i + 1], 1.4)) for i in range(3)], 3.0),
            ([FadeOut(p) for p in pk] + [FadeIn(nb)], 1.0),
            ([LaggedStart(*[FadeIn(c) for c in neutral], lag_ratio=0.1)], 2.0),
            ([ReplacementTransform(neutral[i], colored[i]) for i in range(12)] + [FadeIn(loop)], 2.5),
            ([Indicate(VGroup(colored[0], colored[4], colored[8]), color=CYAN, scale_factor=1.25)], 2.0),
            ([LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in parts], lag_ratio=0.3)], 3.0),
            ([FadeIn(rl), LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2)], 3.0),
            ([FadeIn(pibox, scale=1.1)], 1.5),
            ([FadeIn(sp1), FadeIn(sp2, scale=1.2)], 3.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_21
    def seg21(self):
        hdr = make_header("Nhân ma trận–vectơ: chia theo hàng", "n = 6000", AMBER)
        H, ay = 2.4, 0.9
        def stripe(cx, w, op=0.8):
            return VGroup(*[Rectangle(width=w, height=H / 4, color=DARK, stroke_width=1).set_fill(RANK_COLORS[i], op)
                            .move_to(P(cx, ay + H / 2 - H / 8 - i * H / 4)) for i in range(4)])
        bands = stripe(-5.0, 2.0)
        xp = stripe(-3.0, 0.4)
        yp = stripe(-1.8, 0.4)
        la = T("A (n × n)", 15, TEXT_MUTED).move_to(P(-5.0, ay + H / 2 + 0.3))
        lx = T("x", 15, TEXT_MUTED).move_to(P(-3.0, ay + H / 2 + 0.3))
        ly = T("y", 15, TEXT_MUTED).move_to(P(-1.8, ay + H / 2 + 0.3))
        t1 = T("×", 26, TEXT_MAIN).move_to(P(-3.75, ay))
        t2 = T("=", 26, TEXT_MAIN).move_to(P(-2.4, ay))
        ag = box("MPI_Allgather: x_part → x đầy đủ", VIOLET, w=5.0, h=0.5, size=14).move_to(P(-3.5, -0.9))
        aarrs = VGroup(Ar(P(-3.0, -0.35), P(-3.0, -0.62), color=VIOLET, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.5))
        loc = box("mỗi rank: n/p hàng cục bộ", CYAN, w=5.0, h=0.5, size=14).move_to(P(-3.5, -1.6))
        sz1 = T("A: 288 MB, đọc lại mỗi vòng từ RAM", 16, CORAL, bold=True).move_to(P(-3.5, -2.3))
        sz2 = T("x: chỉ 48 KB", 16, EMERALD, bold=True).move_to(P(-3.5, -2.8))
        chart = make_bar_chart([1.0, 1.83, 2.84, 3.59, 3.79], ["1", "2", "4", "8", "12"], [CYAN, CYAN, CYAN, CYAN, AMBER],
                               max_val=12, width=5.0, height=3.0, unit="×").move_to(P(3.6, -0.2))
        ct = T("tăng tốc theo số rank", 16, TEXT_MUTED).move_to(P(3.6, 1.7))
        ideal = T("lý tưởng: 12×", 16, CORAL, bold=True).move_to(P(3.6, 1.25))
        play_voiced(self, "03_21", [
            ([FadeIn(hdr), FadeIn(bands), FadeIn(xp), FadeIn(yp), FadeIn(la), FadeIn(lx), FadeIn(ly), FadeIn(t1), FadeIn(t2)], 3.0),
            ([FadeIn(ag), GrowArrow(aarrs[0]), Indicate(xp, color=WHITE, scale_factor=1.15)], 3.5),
            ([FadeIn(loc), Indicate(bands, color=WHITE, scale_factor=1.05)], 2.5),
            ([FadeIn(sz1), FadeIn(sz2)], 3.5),
            ([FadeIn(ct), FadeIn(chart[0]), FadeIn(chart[1])] + [GrowFromEdge(b[0], DOWN) for b in chart[2]] +
             [FadeIn(b[1]) for b in chart[2]] + [FadeIn(b[2]) for b in chart[2]], 4.5),
            ([FadeIn(ideal, scale=1.2), Indicate(chart[2][4][0], color=AMBER)], 2.5),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_22
    def seg22(self):
        hdr = make_header("Chạy trên nhiều máy: 5 điều kiện", "mã nguồn giữ nguyên", CYAN)
        cxs = [-3.7, 3.7]
        nodes = VGroup(*[RoundedRectangle(width=4.6, height=2.7, corner_radius=0.2, color=BORDER_DIM, stroke_width=2)
                         .set_fill(PANEL_BG, 0.6).move_to(P(c, 1.25)) for c in cxs])
        nl = VGroup(T("node1 (khởi động)", 16, CYAN, bold=True).move_to(P(cxs[0], 2.3)),
                    T("node2", 16, EMERALD, bold=True).move_to(P(cxs[1], 2.3)))
        mpis = VGroup(*[box("MPI 5.0.11", VIOLET, w=1.9, h=0.45, size=14).move_to(P(c - 1.05, 1.6)) for c in cxs])
        progs = VGroup(*[box("./hello", AMBER, w=1.5, h=0.45, size=14).move_to(P(c + 1.4, 1.6)) for c in cxs])
        procs = VGroup(box("mpirun", CYAN, w=1.9, h=0.45, size=14).move_to(P(cxs[0] - 1.05, 1.0)),
                       box("prted", EMERALD, w=1.9, h=0.45, size=14).move_to(P(cxs[1] - 1.05, 1.0)))
        hosts = VGroup(*[T(t, 13, TEXT_MUTED, MONO).move_to(P(c, 0.45)) for c, t in zip(cxs, ["192.168.1.11 node1", "192.168.1.12 node2"])])
        ssh = Ar(P(-1.35, 1.0), P(1.35, 1.0), color=AMBER, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        sshl = T("ssh", 15, AMBER, MONO, True).move_to(P(0, 1.35))
        fw = DashedLine(P(0, 2.4), P(0, 0.1), color=CORAL, stroke_width=2.5)
        fwl = T("tường lửa", 13, CORAL).move_to(P(0, -0.1))
        names = ["① cùng bản MPI", "② cùng đường dẫn", "③ SSH không mật khẩu", "④ tên máy phân giải", "⑤ tường lửa mở cổng"]
        cols = [VIOLET, AMBER, CYAN, TEXT_MUTED, CORAL]
        chips = VGroup(*[box(names[i], cols[i], w=2.35, h=0.5, size=13).move_to(P(-5.0 + 2.5 * i, -1.2)) for i in range(5)])
        cmd = T("$ ssh node2 which mpirun", 18, TEXT_MAIN, MONO).move_to(P(-2.6, -2.2))
        okk = T("→ /opt/openmpi/bin/mpirun  ✓", 16, EMERALD, MONO, True).move_to(P(2.9, -2.2))
        bad = T("không in gì → mpirun cũng hỏng (shell không tương tác)", 16, CORAL, bold=True).move_to(P(0, -2.85))
        play_voiced(self, "03_22", [
            ([FadeIn(hdr), FadeIn(nodes), FadeIn(nl), FadeIn(procs)], 3.0),
            ([FadeIn(chips[0]), FadeIn(mpis, scale=1.2)], 3.0),
            ([FadeIn(chips[1]), FadeIn(progs, scale=1.2)], 3.0),
            ([FadeIn(chips[2]), GrowArrow(ssh), FadeIn(sshl)], 3.0),
            ([FadeIn(chips[3]), FadeIn(hosts)], 2.5),
            ([FadeIn(chips[4]), Create(fw), FadeIn(fwl)], 3.0),
            ([FadeIn(cmd), FadeIn(okk)], 3.5),
            ([FadeIn(bad, shift=UP * 0.1)], 3.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_23
    def seg23(self):
        hdr = make_header("Hostfile, slots và --map-by", "bố trí rank", EMERALD)
        hf = make_code_box(["$ cat hosts.txt", "node1 slots=4", "node2 slots=4", "", "$ mpirun -np 8 \\", "    --hostfile hosts.txt ./hello"],
                           width=5.4, font_size=15, accent=EMERALD).move_to(P(-3.6, 0.9))
        dm = T("--map-by node --display map", 15, AMBER, MONO).move_to(P(-3.6, -1.0))
        sx = [2.3, 3.4, 4.5, 5.6]
        ys = [1.7, 0.6]
        slots = VGroup(*[Rectangle(width=1.0, height=0.7, color=BORDER_DIM, stroke_width=1.5).set_fill(PANEL_BG, 0.6).move_to(P(sx[j], ys[r]))
                         for r in range(2) for j in range(4)])
        nlab = VGroup(T("node1", 16, CYAN, bold=True).move_to(P(1.0, ys[0])), T("node2", 16, EMERALD, bold=True).move_to(P(1.0, ys[1])))
        mode1 = T("mặc định: lấp đầy node1 trước", 16, AMBER, bold=True).move_to(P(3.9, 2.45))
        mode2 = T("--map-by node: xen kẽ", 16, VIOLET, bold=True).move_to(P(3.9, 2.45))
        def pos_slot(i):
            return P(sx[i % 4], ys[i // 4])
        def pos_node(i):
            return P(sx[i // 2], ys[i % 2])
        rk = VGroup(*[rank_node(i, RANK_COLORS[i % 4], r=0.3, label=str(i)).move_to(pos_slot(i)) for i in range(8)])
        extra = VGroup(*[rank_node(8 + k, CORAL, r=0.3, label=str(8 + k)).move_to(P(sx[k], -0.55)) for k in range(4)])
        err = T("-np 12 > 8 slot → not enough slots", 17, CORAL, bold=True).move_to(P(3.9, -1.2))
        cap = T("rank trao đổi nhiều → nên ở cùng một nút", 19, AMBER, bold=True).move_to(P(0, -2.6))
        play_voiced(self, "03_23", [
            ([FadeIn(hdr), FadeIn(hf)], 3.0),
            ([FadeIn(slots), FadeIn(nlab), FadeIn(mode1)], 3.0),
            ([LaggedStart(*[FadeIn(r, scale=0.7) for r in rk], lag_ratio=0.25)], 5.0),
            ([FadeIn(dm), Transform(mode1, mode2)] + [rk[i].animate.move_to(pos_node(i)) for i in range(8)], 4.0),
            ([LaggedStart(*[FadeIn(e, scale=0.7) for e in extra], lag_ratio=0.2), FadeIn(err)], 4.0),
            ([FadeIn(cap, shift=UP * 0.1)], 3.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_24
    def seg24(self):
        hdr = make_header("Xử lý sự cố khi chạy nhiều máy", "từng lớp một", CORAL)
        syms = ["Host key verification failed", "Permission denied (publickey)", "prted: command not found", "treo ở thông điệp đầu tiên"]
        fixes = ["ssh node2 một lần, xác nhận khóa", "ssh-copy-id node2", "PATH đầu .bashrc, hoặc --prefix", "btl_tcp_if_include / mở cổng"]
        ys = [2.1, 1.4, 0.7, 0.0]
        rows = []
        for i in range(4):
            a = box(syms[i], CORAL, w=5.6, h=0.55, size=15).move_to(P(-3.3, ys[i]))
            ar = Ar(P(-0.35, ys[i]), P(0.35, ys[i]), color=TEXT_MUTED, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.5)
            b = box(fixes[i], EMERALD, w=5.6, h=0.55, size=15).move_to(P(3.3, ys[i]))
            rows.append(VGroup(a, ar, b))
        lad = T("gỡ lỗi từ đơn giản đến phức tạp", 18, AMBER, bold=True).move_to(P(0, -0.85))
        names = ["ssh hostname", "ssh which mpirun", "mpirun hostname", "hello MPI", "chương trình"]
        cols = [CYAN, CYAN, VIOLET, VIOLET, EMERALD]
        chips = VGroup(*[box(names[i], cols[i], w=2.2, h=0.55, size=14).move_to(P(-5.0 + 2.5 * i, -1.8)) for i in range(5)])
        links = VGroup(*[Ar(chips[i].get_right(), chips[i + 1].get_left(), color=TEXT_MUTED, buff=0.02, stroke_width=2,
                            max_tip_length_to_length_ratio=0.8) for i in range(4)])
        play_voiced(self, "03_24", [
            ([FadeIn(hdr), FadeIn(rows[0])], 4.0),
            ([FadeIn(rows[1])], 3.0),
            ([FadeIn(rows[2])], 4.5),
            ([FadeIn(rows[3])], 4.5),
            ([FadeIn(lad)], 1.5),
            ([LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in chips], lag_ratio=0.35), LaggedStart(*[GrowArrow(l) for l in links], lag_ratio=0.35)], 7.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_25
    def seg25(self):
        hdr = make_header("Chạy MPI trên cluster với Slurm", "sbatch + srun", VIOLET)
        code = make_code_box(["#!/bin/bash", "#SBATCH --nodes=2", "#SBATCH --ntasks-per-node=12", "#SBATCH --time=00:10:00",
                              "#SBATCH --output=jacobi_%j.txt", "", "srun ./jacobi sendrecv 4000 200"],
                             width=6.2, font_size=15, accent=VIOLET).move_to(P(-3.5, 0.7))
        calc = T("2 × 12 = 24 tiến trình MPI", 20, EMERALD, bold=True).move_to(P(-3.5, -1.5))
        hl = SurroundingRectangle(VGroup(code[1][0][1], code[1][0][2]), color=EMERALD, buff=0.06, stroke_width=2)
        s1 = box("sbatch job.sh → job 123", CYAN, w=4.6, h=0.55, size=15).move_to(P(3.7, 2.1))
        s2 = box("squeue -u $USER:  PD", AMBER, w=4.6, h=0.55, size=15).move_to(P(3.7, 1.2))
        s2r = box("squeue -u $USER:  R", EMERALD, w=4.6, h=0.55, size=15).move_to(P(3.7, 1.2))
        nodes = VGroup(*[RoundedRectangle(width=2.0, height=1.1, corner_radius=0.12, color=BORDER_DIM, stroke_width=2).set_fill(PANEL_BG, 0.6)
                         .move_to(P(2.65 + 2.1 * k, -0.15)) for k in range(2)])
        dots = VGroup(*[Circle(radius=0.09, color=RANK_COLORS[j % 4], stroke_width=1).set_fill(RANK_COLORS[j % 4], 0.9)
                        .move_to(P(2.65 + 2.1 * k - 0.75 + 0.3 * (j % 6), -0.15 + 0.2 - 0.4 * (j // 6))) for k in range(2) for j in range(12)])
        s3 = T("srun: 24 rank", 15, TEXT_MAIN, MONO, True).move_to(P(3.7, 0.55))
        out = box("jacobi_123.txt", EMERALD, w=3.2, h=0.55, size=15).move_to(P(3.7, -1.3))
        cap = T("Phòng máy: SSH + hostfile · Cluster: sbatch + srun", 17, AMBER, bold=True).move_to(P(0, -2.6))
        play_voiced(self, "03_25", [
            ([FadeIn(hdr), FadeIn(code)], 3.0),
            ([Create(hl), FadeIn(calc, scale=1.1)], 4.0),
            ([FadeIn(s1)], 3.0),
            ([FadeIn(s2)], 3.0),
            ([Transform(s2, s2r), FadeIn(s3), FadeIn(nodes)], 2.5),
            ([LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05)], 3.0),
            ([FadeIn(out, shift=UP * 0.1)], 3.0),
            ([FadeIn(cap)], 3.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_27
    def seg27(self):
        hdr = make_header("Lỗi thường gặp và quy trình", "danh sách kiểm tra", CORAL)
        bad = make_card("Sai hoặc treo", ["• cả hai cùng Send trước", "• tập thể chỉ vài rank gọi", "• lệch số phần tử / kiểu / tag",
                                          "• dùng lại buffer trước Wait", "• quên MPI_Finalize"], width=6.1, accent=CORAL, body_size=16).move_to(P(-3.2, 0.6))
        slow = make_card("Đúng nhưng chậm", ["• nhiều thông điệp nhỏ", "• chia tĩnh cho tải không đều", "• rank 0 làm hết nhập/xuất",
                                             "• băng thông RAM bão hòa", "• đo giờ không barrier"], width=6.1, accent=AMBER, body_size=16).move_to(P(3.2, 0.6))
        cap = T("Quy trình khuyến nghị", 18, EMERALD, bold=True).move_to(P(0, -1.55))
        names = ["bản tuần tự", "chia dữ liệu", "Sendrecv + tập thể", "rank lẻ + Ssend", "đo, tìm rank chậm"]
        chips = VGroup(*[box(names[i], EMERALD, w=2.3, h=0.55, size=14).move_to(P(-5.0 + 2.5 * i, -2.4)) for i in range(5)])
        links = VGroup(*[Ar(chips[i].get_right(), chips[i + 1].get_left(), color=TEXT_MUTED, buff=0.02, stroke_width=2,
                            max_tip_length_to_length_ratio=0.8) for i in range(4)])
        play_voiced(self, "03_27", [
            ([FadeIn(hdr), FadeIn(bad[0]), FadeIn(bad[1][0])], 2.0),
            ([LaggedStart(*[FadeIn(l) for l in bad[1][1]], lag_ratio=0.5)], 8.0),
            ([FadeIn(slow[0]), FadeIn(slow[1][0])], 1.0),
            ([LaggedStart(*[FadeIn(l) for l in slow[1][1]], lag_ratio=0.5)], 8.0),
            ([FadeIn(cap)], 1.0),
            ([LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in chips], lag_ratio=0.35), LaggedStart(*[GrowArrow(l) for l in links], lag_ratio=0.35)], 7.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_28
    def seg28(self):
        hdr = make_header("SPMD: một chương trình, nhiều rank", "mpirun -np 4", CYAN)
        code = make_code_box(["MPI_Init(&argc, &argv);", "MPI_Comm_rank(c, &rank);", "MPI_Comm_size(c, &size);",
                              "if (rank == 0) { ... }", "MPI_Finalize();"], width=5.8, font_size=15, accent=CYAN).move_to(P(-3.3, 0.5))
        lines = code[1][0]
        hl = SurroundingRectangle(lines[0], color=AMBER, buff=0.06, stroke_width=2)
        ys = [1.5, 0.5, -0.5, -1.5]
        ranks = VGroup(*[rank_node(i, r=0.4).move_to(P(1.2, ys[i])) for i in range(4)])
        def outs(order):
            return [box(f"rank {i} / 4", RANK_COLORS[i], w=2.1, h=0.5, size=14).move_to(P(3.6, ys[i])) for i in order]
        run1 = outs([1, 2, 3, 0])
        run2 = outs([2, 0, 3, 1])
        l1 = T("lần chạy 1", 15, AMBER, bold=True).move_to(P(5.2, 2.3))
        l2 = T("lần chạy 2", 15, VIOLET, bold=True).move_to(P(5.2, 2.3))
        cap = T("Thứ tự in thay đổi mỗi lần chạy", 22, AMBER, bold=True).move_to(P(0, -2.9))
        r1 = VGroup(*run1)
        r2 = VGroup(*run2)
        play_voiced(self, "03_28", [
            ([FadeIn(hdr), FadeIn(code), FadeIn(ranks)], 2.5),
            ([Create(hl)], 1.0),
            ([Transform(hl, SurroundingRectangle(lines[1], color=AMBER, buff=0.06, stroke_width=2))], 1.0),
            ([Transform(hl, SurroundingRectangle(lines[2], color=AMBER, buff=0.06, stroke_width=2))], 1.0),
            ([Transform(hl, SurroundingRectangle(lines[3], color=EMERALD, buff=0.06, stroke_width=2))], 1.5),
            ([Transform(hl, SurroundingRectangle(lines[4], color=CORAL, buff=0.06, stroke_width=2))], 1.0),
            ([FadeIn(l1)] + [FadeIn(o, shift=LEFT * 0.2) for o in run1[:1]], 1.0),
            ([FadeIn(run1[1])], 0.8), ([FadeIn(run1[2])], 0.8), ([FadeIn(run1[3])], 0.8),
            ([FadeOut(r1), Transform(l1, l2)], 1.0),
            ([FadeIn(run2[0])], 0.8), ([FadeIn(run2[1])], 0.8), ([FadeIn(run2[2])], 0.8), ([FadeIn(run2[3])], 0.8),
            ([FadeIn(cap, shift=UP * 0.1)], 1.5),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_29
    def seg29(self):
        hdr = make_header("Biên dịch và chạy MPI", "mpicxx · mpirun", EMERALD)
        c1 = box("mpicxx prog.cpp -o prog", CYAN, w=4.4, h=0.6, size=15).move_to(P(-3.6, 1.9))
        c2 = box("mpirun -np 4 ./prog", EMERALD, w=4.0, h=0.6, size=15).move_to(P(2.3, 1.9))
        arr = Ar(c1.get_right(), c2.get_left(), color=TEXT_MUTED, buff=0.1, stroke_width=2.5, max_tip_length_to_length_ratio=0.5)
        wrap = T("lớp bọc quanh g++", 14, TEXT_MUTED).move_to(P(-3.6, 1.35))
        procs = VGroup(*[rank_node(i, r=0.3, label=str(i)).move_to(P(5.2 + 0 * i, 1.9)) for i in range(1)])
        cores = VGroup(*[Rectangle(width=0.8, height=0.55, color=BORDER_DIM, stroke_width=1.5).set_fill(PANEL_BG, 0.8) for _ in range(12)])
        cores.arrange_in_grid(rows=2, cols=6, buff=0.12).move_to(P(-2.6, -0.3))
        cl = T("máy 12 lõi", 15, TEXT_MUTED).move_to(P(-2.6, 0.75))
        dots = VGroup(*[Dot(cores[i].get_center(), radius=0.12, color=EMERALD) for i in range(12)])
        ok = T("-np 12  ✓", 20, EMERALD, bold=True).move_to(P(3.3, 0.4))
        dots2 = VGroup(*[Dot(cores[i % 12].get_center() + RIGHT * (0.2 if i >= 12 else -0.2) * 0.5, radius=0.1, color=CORAL) for i in range(12, 24)])
        no = T("-np 24  ✗  bị từ chối", 20, CORAL, bold=True).move_to(P(3.3, -0.4))
        fix = box("--oversubscribe", AMBER, w=3.0, h=0.55, size=15).move_to(P(3.3, -1.2))
        hf = box("--hostfile hosts.txt", VIOLET, w=3.8, h=0.55, size=15).move_to(P(-2.6, -2.2))
        hfl = T("nhiều máy: mỗi dòng một nút + slot", 14, TEXT_MUTED).move_to(P(3.0, -2.2))
        play_voiced(self, "03_29", [
            ([FadeIn(hdr), FadeIn(c1), FadeIn(wrap)], 3.0),
            ([GrowArrow(arr), FadeIn(c2)], 2.0),
            ([FadeIn(cores), FadeIn(cl)], 2.0),
            ([LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.1), FadeIn(ok)], 3.0),
            ([LaggedStart(*[FadeIn(d, scale=0.5) for d in dots2], lag_ratio=0.1), FadeIn(no)], 3.0),
            ([FadeOut(dots2), FadeIn(fix)], 2.5),
            ([FadeIn(hf), FadeIn(hfl)], 3.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_30
    def seg30(self):
        hdr = make_header("MPI_Recv: vùng nhận và status", "count · ANY_SOURCE", AMBER)
        r0 = rank_node(0, CYAN, r=0.45).move_to(P(5.5, 0.9))
        def slots(n, col, filled):
            g = VGroup(*[box(str(v), col, w=0.7, h=0.6, size=16) for v in filled] +
                       [box("", BORDER_DIM, w=0.7, h=0.6, size=16) for _ in range(n - len(filled))]).arrange(RIGHT, buff=0.06)
            return g
        buf = slots(4, EMERALD, [3, 5]).move_to(P(1.8, 1.7))
        bl = T("vùng nhận: 4 phần tử", 15, TEXT_MUTED).move_to(P(1.8, 2.3))
        okm = T("thông điệp 2  ≤ 4  ✓", 20, EMERALD, bold=True).move_to(P(-3.3, 1.7))
        buf2 = slots(4, CORAL, [3, 5, 7, 9]).move_to(P(1.8, 0.5))
        extra = VGroup(box("1", CORAL, w=0.7, h=0.6, size=16), box("2", CORAL, w=0.7, h=0.6, size=16)).arrange(RIGHT, buff=0.06).next_to(buf2, RIGHT, buff=0.06)
        badm = T("thông điệp 6  >  4  ✗", 20, CORAL, bold=True).move_to(P(-3.3, 0.5))
        sep = DashedLine(P(-6.3, -0.4), P(6.3, -0.4), color=BORDER_DIM)
        ws = VGroup(*[rank_node(i, RANK_COLORS[i], r=0.3, label=str(i)).move_to(P(-5.6, -0.9 - 0.65 * (i - 1) + 0.0)) for i in (1, 2, 3)])
        vals = {1: 1, 2: 4, 3: 9}
        q0 = rank_node(0, CYAN, r=0.4).move_to(P(-1.0, -1.55))
        wl = T("ANY_SOURCE: ai tới trước nhận trước", 15, TEXT_MUTED).move_to(P(-1.0, -0.8))
        order = [3, 2, 1]
        rows = VGroup(*[box(f"from {w}: {vals[w]}", RANK_COLORS[w], w=2.4, h=0.5, size=14).move_to(P(2.6, -1.0 - 0.6 * j)) for j, w in enumerate(order)])
        tot = box("total = 14", AMBER, w=2.4, h=0.55, size=16).move_to(P(5.2, -1.6))
        pk = [pkt(str(vals[w]), RANK_COLORS[w], w=0.5, h=0.35, size=14).move_to(ws[w - 1].get_center() + RIGHT * 0.5) for w in order]
        play_voiced(self, "03_30", [
            ([FadeIn(hdr), FadeIn(r0), FadeIn(buf), FadeIn(bl)], 2.5),
            ([FadeIn(okm, shift=RIGHT * 0.1)], 2.0),
            ([FadeIn(buf2), FadeIn(extra)], 1.5),
            ([FadeIn(badm, shift=RIGHT * 0.1), Wiggle(extra)], 3.0),
            ([Create(sep), FadeIn(ws), FadeIn(q0), FadeIn(wl)], 3.0),
            ([FadeIn(pk[0]), pk[0].animate.move_to(q0.get_center() + LEFT * 0.5), FadeIn(rows[0])], 2.0),
            ([FadeIn(pk[1]), pk[1].animate.move_to(q0.get_center() + LEFT * 0.5), FadeIn(rows[1])], 2.0),
            ([FadeIn(pk[2]), pk[2].animate.move_to(q0.get_center() + LEFT * 0.5), FadeIn(rows[2])], 2.0),
            ([FadeIn(tot, scale=1.2)], 2.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_31
    def seg31(self):
        hdr = make_header("Tập thể: mọi rank phải gọi", "cùng thứ tự", CORAL)
        xs = [-4.5, -1.5, 1.5, 4.5]
        rk = VGroup(*[rank_node(i, r=0.4).move_to(P(xs[i], 1.6)) for i in range(4)])
        calls = VGroup(*[box("Reduce", EMERALD, w=1.7, h=0.5, size=15).move_to(P(xs[i], 0.6)) for i in range(4)])
        skip = box("bỏ qua", CORAL, w=1.7, h=0.5, size=15).move_to(P(xs[2], 0.6))
        hang = T("cả nhóm treo", 24, CORAL, bold=True).move_to(P(0, -0.4))
        chart = make_bar_chart([6.1, 8.6, 14.4], ["vòng lặp", "Reduce", "Allreduce"], [AMBER, EMERALD, CYAN],
                               max_val=14.4, width=5.0, height=2.8, unit="ms").move_to(P(-3.0, 0.4))
        ct = T("m = 10⁶ double, 12 rank", 15, TEXT_MUTED).move_to(P(-3.0, 2.25))
        note1 = T("1 nút: vòng lặp đôi khi nhanh hơn", 16, AMBER, bold=True).move_to(P(3.2, 1.0))
        note2 = T("tập thể: gọn, log p bước", 16, EMERALD, bold=True).move_to(P(3.2, 0.1))
        play_voiced(self, "03_31", [
            ([FadeIn(hdr), FadeIn(rk), FadeIn(calls)], 3.0),
            ([Transform(calls[2], skip)], 2.0),
            ([FadeIn(hang, scale=1.2), Wiggle(rk)], 3.0),
            ([FadeOut(VGroup(rk, calls, hang))], 1.0),
            ([FadeIn(ct), FadeIn(chart[0]), FadeIn(chart[1])] + [GrowFromEdge(b[0], DOWN) for b in chart[2]] + [FadeIn(b[1]) for b in chart[2]] + [FadeIn(b[2]) for b in chart[2]], 4.0),
            ([FadeIn(note1)], 3.0),
            ([FadeIn(note2)], 3.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_32
    def seg32(self):
        hdr = make_header("Giới hạn mở rộng trên một nút", "12 rank", AMBER)
        chart = make_bar_chart([11.1, 9.1, 3.8, 2.4], ["π", "Jacobi 1000", "matvec 6000", "Jacobi 4000"],
                               [EMERALD, CYAN, AMBER, CORAL], max_val=12, width=8.0, height=4.2, unit="×").move_to(P(-1.5, -0.55))
        why = VGroup(*[T(s, 14, TEXT_MUTED) for s in ["tính toán thuần", "vừa cache", "băng thông RAM", "băng thông RAM"]])
        slot = 8.0 / 4
        for i, w in enumerate(why):
            w.move_to(P(chart[2][i][0].get_x(), chart[0].get_center()[1] - 0.62))
        by = chart[0].get_center()[1] + 3.85
        ideal = DashedLine(P(chart[0].get_left()[0], by), P(chart[0].get_right()[0], by), color=TEXT_MUTED, stroke_width=2)
        il = T("lý tưởng = 12", 14, TEXT_MUTED).move_to(P(chart[0].get_right()[0] + 1.0, by))
        cap = T("Đo để biết giới hạn", 20, AMBER, bold=True).move_to(P(4.5, 0.0))
        play_voiced(self, "03_32", [
            ([FadeIn(hdr), FadeIn(chart[0]), FadeIn(chart[1]), Create(ideal), FadeIn(il)], 2.5),
            ([GrowFromEdge(chart[2][0][0], DOWN), FadeIn(chart[2][0][1]), FadeIn(chart[2][0][2]), FadeIn(why[0])], 3.0),
            ([GrowFromEdge(chart[2][1][0], DOWN), FadeIn(chart[2][1][1]), FadeIn(chart[2][1][2]), FadeIn(why[1])], 3.0),
            ([GrowFromEdge(chart[2][2][0], DOWN), FadeIn(chart[2][2][1]), FadeIn(chart[2][2][2]), FadeIn(why[2])], 3.0),
            ([GrowFromEdge(chart[2][3][0], DOWN), FadeIn(chart[2][3][1]), FadeIn(chart[2][3][2]), FadeIn(why[3])], 3.0),
            ([FadeIn(cap, shift=UP * 0.1)], 2.0),
        ])
        clear_stage(self)

    # ------------------------------------------------------------------ 03_33
    def seg33(self):
        hdr = make_header("MPI hay OpenMP?", "so sánh", VIOLET)
        h1 = T("OpenMP / luồng", 20, AMBER, bold=True).move_to(P(-0.9, 2.3))
        h2 = T("MPI", 20, VIOLET, bold=True).move_to(P(3.7, 2.3))
        rows = [("Bộ nhớ", "dùng chung", "riêng mỗi rank"), ("Quy mô", "một nút", "nhiều nút"),
                ("Trao đổi", "ngầm, qua biến", "thông điệp"), ("Lỗi điển hình", "race condition", "bế tắc"),
                ("Song song hóa", "từng vòng lặp", "chia dữ liệu")]
        grp = []
        for j, (a, b, c) in enumerate(rows):
            y = 1.5 - 0.8 * j
            la = T(a, 16, TEXT_MUTED, bold=True).move_to(P(-4.9, y))
            ba = box(b, AMBER, w=3.4, h=0.6, size=15).move_to(P(-0.9, y))
            bb = box(c, VIOLET, w=3.4, h=0.6, size=15).move_to(P(3.7, y))
            grp.append(VGroup(la, ba, bb))
        hyb = T("Lai: MPI giữa các nút + OpenMP trong nút", 20, EMERALD, bold=True).move_to(P(0, -2.75))
        play_voiced(self, "03_33", [
            ([FadeIn(hdr), FadeIn(h1), FadeIn(h2)], 1.5),
            ([FadeIn(grp[0])], 2.5), ([FadeIn(grp[1])], 2.5), ([FadeIn(grp[2])], 2.5),
            ([FadeIn(grp[3])], 3.0), ([FadeIn(grp[4])], 2.5),
            ([FadeIn(hyb, shift=UP * 0.1)], 2.5),
        ])
        clear_stage(self)


    # ------------------------------------------------------------------ main
    def construct(self):
        setup_bg(self)
        for f in (self.seg01, self.seg28, self.seg29, self.seg02, self.seg30, self.seg03, self.seg04, self.seg05, self.seg06, self.seg07,
                  self.seg08, self.seg09, self.seg10, self.seg11, self.seg12, self.seg13, self.seg14, self.seg31,
                  self.seg15, self.seg16, self.seg17, self.seg18, self.seg19, self.seg32,
                  self.seg20, self.seg21, self.seg22, self.seg23, self.seg24, self.seg25, self.seg33, self.seg27):
            f()
        play_module_drills(self, "M3", "MPI")
