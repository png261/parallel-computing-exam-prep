import numpy as np
from manim import *
from fun_utils import make_mascot, make_bubble, make_hud, bounce
from scene_utils import (
    setup_bg, make_header, clear_stage, play_voiced, make_grid_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, BORDER_DIM, SANS, MONO,
)


def _T(s, size=16, color=TEXT_MAIN, font=SANS, weight=NORMAL):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def _P(x, y):
    return np.array([x, y, 0.0])


def _icon(kind, col):
    g = VGroup()
    if kind == 0:   # architecture: cores + memory bus
        for i in range(4):
            g.add(Square(0.28, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.3).move_to(_P((i - 1.5) * 0.4, 0.2)))
        g.add(Line(_P(-0.8, -0.2), _P(0.8, -0.2), color=TEXT_MUTED, stroke_width=3))
        g.add(Rectangle(width=1.6, height=0.2, stroke_color=col, stroke_width=1.5, fill_opacity=0).move_to(_P(0, -0.38)))
    elif kind == 1:  # shared memory: threads over one memory
        for i in range(3):
            g.add(Line(_P((i - 1) * 0.5, 0.45), _P((i - 1) * 0.5, -0.1), color=col, stroke_width=3))
            g.add(Dot(_P((i - 1) * 0.5, 0.45), radius=0.07, color=col))
        g.add(Rectangle(width=1.6, height=0.28, stroke_color=col, stroke_width=1.8, fill_color=col, fill_opacity=0.25).move_to(_P(0, -0.3)))
    elif kind == 2:  # MPI: two ranks exchanging
        a = Square(0.5, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.3).move_to(_P(-0.7, 0))
        b = Square(0.5, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.3).move_to(_P(0.7, 0))
        g.add(a, b, Arrow(_P(-0.4, 0.1), _P(0.4, 0.1), buff=0, color=TEXT_MAIN, stroke_width=2.5, tip_length=0.12),
              Arrow(_P(0.4, -0.12), _P(-0.4, -0.12), buff=0, color=TEXT_MAIN, stroke_width=2.5, tip_length=0.12))
    elif kind == 3:  # CUDA grid
        for r in range(3):
            for c in range(4):
                g.add(Square(0.26, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.2 + 0.1 * ((r + c) % 3)).move_to(_P((c - 1.5) * 0.3, (1 - r) * 0.3)))
    return g


def _fit(t, w):
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def _trophy(scale=1.0):
    cup = Polygon(_P(-0.42, 0.45), _P(0.42, 0.45), _P(0.26, -0.12), _P(-0.26, -0.12),
                  stroke_color=TEXT_MAIN, stroke_width=2, fill_color=AMBER, fill_opacity=1)
    h1 = Arc(radius=0.2, start_angle=PI / 2, angle=PI, color=AMBER, stroke_width=4).move_to(_P(-0.5, 0.25))
    h2 = Arc(radius=0.2, start_angle=-PI / 2, angle=PI, color=AMBER, stroke_width=4).move_to(_P(0.5, 0.25))
    stem = Rectangle(width=0.12, height=0.3, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to(_P(0, -0.27))
    base = Rectangle(width=0.62, height=0.12, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to(_P(0, -0.48))
    st = Star(n=5, outer_radius=0.17, inner_radius=0.07, fill_color="#0D1117", fill_opacity=1, stroke_width=0).move_to(_P(0, 0.2))
    return VGroup(h1, h2, cup, stem, base, st).scale(scale)


def _badge(k, col, lit=False):
    c = Circle(radius=0.42, stroke_color=col if lit else BORDER_DIM, stroke_width=3,
               fill_color=col if lit else PANEL_BG, fill_opacity=0.9 if lit else 0.9)
    n = _T(str(k), 30, "#0D1117" if lit else TEXT_MUTED, weight=BOLD).move_to(c)
    return VGroup(c, n)


class Scene06Summary(Scene):
    def construct(self):
        setup_bg(self)
        hdr = make_header("Màn cuối: Chiến thắng!", "", AMBER)
        mods = [("Nền tảng", CYAN), ("Threads+OpenMP", EMERALD), ("MPI", AMBER), ("CUDA", VIOLET)]
        badges, names, lit = [], [], []
        for i, (nm, col) in enumerate(mods):
            x = -4.8 + i * 3.2
            b = _badge(i + 1, col).move_to(_P(x - 0.8, 1.9))
            ic = _icon(i, col).scale(0.7).move_to(_P(x + 0.35, 1.9))
            lb = _T("Màn %d" % (i + 1), 14, TEXT_MUTED).move_to(_P(x - 0.8, 1.27))
            nt = _fit(_T(nm, 13, col), 1.5).move_to(_P(x + 0.35, 1.38))
            badges.append(VGroup(b, ic, lb, nt))
            lit.append(_badge(i + 1, col, True).move_to(b))
        hud = make_hud(0, 0, 1).move_to(_P(5.2, 3.15))
        mascot = make_mascot("happy", 1.15).move_to(_P(-4.9, -0.6))
        trophy = _trophy(1.1).move_to(_P(-3.35, -0.55))
        deck_base = _P(2.6, -2.55)
        deck_lbl = _T("Bộ bài 6 lá", 18, AMBER, weight=BOLD).move_to(_P(2.6, -3.25))
        F = [
            ("1", "Amdahl: S = 1 / (P/N + S)", CYAN, 0),
            ("2", "Tối đa = 1 / (1 − P)", CYAN, 0),
            ("3", "static: n/p lần lặp/luồng", EMERALD, 1),
            ("4", "MPI: t(n) = α + n/β", AMBER, 2),
            ("5", "idx = blockIdx.x·B + threadIdx.x", VIOLET, 3),
            ("6", "nblocks = (n + 255) / 256", VIOLET, 3),
        ]
        cards = []
        for k, (num, txt, col, tidx) in enumerate(F):
            fr = RoundedRectangle(width=6.1, height=0.8, corner_radius=0.12, stroke_color=col, stroke_width=2.4,
                                  fill_color=PANEL_BG, fill_opacity=1)
            badge = _T(num, 22, col, MONO, BOLD).move_to(fr.get_left() + RIGHT * 0.35)
            t = _fit(_T(txt, 22, TEXT_MAIN, MONO), 5.0).next_to(badge, RIGHT, buff=0.25)
            cards.append(VGroup(fr, badge, t).move_to(_P(0.8, -0.3)))
        xp = [0]

        def hud_to(k, streak):
            return Transform(hud, make_hud(30 * k, streak, k).move_to(hud.get_center()))

        def steps():
            yield ([FadeIn(hdr), FadeIn(hud), LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in badges], lag_ratio=0.2)], 1.6)
            yield ([FadeIn(mascot, shift=UP * 0.3), FadeIn(trophy, shift=UP * 0.3), FadeIn(deck_lbl)], 0.8)
            seen = set()
            nxt = 0
            for k, c in enumerate(cards):
                col, tidx = F[k][2], F[k][3]
                yield ([FadeIn(c, shift=UP * 0.2), Indicate(badges[tidx][0], color=col, scale_factor=1.15)], 0.7)
                if tidx not in seen:
                    seen.add(tidx)
                    nxt += 1
                    yield ([Transform(badges[tidx][0], lit[tidx]), hud_to(nxt, nxt), bounce(mascot)], 0.6)
                tgt = deck_base + UP * 0.42 * k + RIGHT * 0.12 * (k % 2)
                yield ([c.animate.scale(0.52).move_to(tgt)], 0.6)
            cm = make_mascot("cheer", 1.15).move_to(mascot)
            yield ([Transform(mascot, cm), trophy.animate.shift(UP * 0.35), Flash(trophy, color=AMBER, flash_radius=0.9)], 0.8)
            yield ([bounce(mascot, 0.35, 0.6), Indicate(hud, color=AMBER, scale_factor=1.2)], 0.8)
            yield ([hud.animate.scale(1.0)], 0.2)
        play_voiced(self, "06_01", steps())
        clear_stage(self)

        # ------------------------------------------------------------------
        # 06_10  Mẹo nhớ: mỗi công thức một bức tranh
        # ------------------------------------------------------------------
        self.mnemonic()
        self.rapid_fire()
        self.race_track()

    # ---- mnemonic drawings -------------------------------------------------
    def _draw(self, k, col):
        g = VGroup()
        if k == 0:   # cổ chai
            g.add(Polygon(_P(-1.3, 0.5), _P(-0.3, 0.5), _P(0.1, 0.12), _P(1.3, 0.12), _P(1.3, -0.12), _P(0.1, -0.12),
                          _P(-0.3, -0.5), _P(-1.3, -0.5), stroke_color=col, stroke_width=3, fill_opacity=0))
            for i in range(3):
                for j in range(3):
                    g.add(Dot(_P(-1.1 + i * 0.28, -0.3 + j * 0.3), radius=0.07, color=col))
            g.add(Dot(_P(0.8, 0.0), radius=0.07, color=col), Dot(_P(1.1, 0.0), radius=0.07, color=col))
        elif k == 1:  # trần nhà
            pts = [_P(x, 0.4 - 0.85 * np.exp(-(x + 1.4) * 1.3) ) for x in np.linspace(-1.4, 1.4, 20)]
            cv = VMobject(color=col, stroke_width=4).set_points_smoothly(pts)
            g.add(Line(_P(-1.5, 0.5), _P(1.5, 0.5), color=CORAL, stroke_width=6))
            for x in np.linspace(-1.4, 1.4, 8):
                g.add(Line(_P(x, 0.5), _P(x + 0.1, 0.62), color=CORAL, stroke_width=3))
            g.add(Line(_P(-1.4, -0.5), _P(1.5, -0.5), color=TEXT_MUTED, stroke_width=2), cv)
        elif k == 2:  # chia bánh
            g.add(Circle(radius=0.5, stroke_color=TEXT_MAIN, stroke_width=2, fill_color=col, fill_opacity=0.35))
            for i in range(6):
                g.add(Line(ORIGIN, 0.5 * _P(np.cos(i * PI / 3), np.sin(i * PI / 3), ), color=TEXT_MAIN, stroke_width=2))
            g.add(Sector(radius=0.5, angle=PI / 3, fill_color=col, fill_opacity=0.95, stroke_width=0))
            for i in range(3):
                g.add(Circle(radius=0.14, stroke_color=col, stroke_width=2, fill_color=PANEL_BG, fill_opacity=1).move_to(_P(1.0 + i * 0.35, 0.0)))
                g.add(Dot(_P(0.96 + i * 0.35, 0.03), radius=0.02, color=TEXT_MAIN), Dot(_P(1.04 + i * 0.35, 0.03), radius=0.02, color=TEXT_MAIN))
            g.move_to(ORIGIN)
        elif k == 3:  # xe tải
            light = VGroup(Rectangle(width=0.3, height=0.7, stroke_color=TEXT_MUTED, fill_color=PANEL_BG, fill_opacity=1),
                           Circle(radius=0.1, fill_color=CORAL, fill_opacity=1, stroke_width=0).shift(UP * 0.18),
                           Circle(radius=0.1, fill_color=BORDER_DIM, fill_opacity=1, stroke_width=0).shift(DOWN * 0.18)).move_to(_P(-1.3, 0.05))
            al = _T("α", 20, CORAL, weight=BOLD).move_to(_P(-0.95, 0.45))
            cargo = Rectangle(width=1.1, height=0.6, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.35).move_to(_P(0.2, 0.0))
            cab = Rectangle(width=0.45, height=0.42, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.7).move_to(_P(1.0, -0.09))
            w1 = Circle(radius=0.12, fill_color=TEXT_MAIN, fill_opacity=1, stroke_width=0).move_to(_P(-0.15, -0.34))
            w2 = Circle(radius=0.12, fill_color=TEXT_MAIN, fill_opacity=1, stroke_width=0).move_to(_P(0.95, -0.34))
            nb = _T("n/β", 15, TEXT_MAIN, MONO).move_to(cargo)
            g.add(light, al, cargo, cab, w1, w2, nb)
        elif k == 4:  # số nhà
            for r in range(2):
                for c in range(4):
                    hs = Square(0.38, stroke_color=col, stroke_width=1.8, fill_color=PANEL_BG, fill_opacity=1)
                    rf = Triangle(stroke_color=col, stroke_width=1.8, fill_color=col, fill_opacity=0.4).scale(0.26).next_to(hs, UP, buff=0)
                    hh = VGroup(hs, rf).move_to(_P(-0.45 + c * 0.55, 0.35 - r * 0.7))
                    if r == 1 and c == 2:
                        hs.set_fill(AMBER, 0.9)
                    g.add(hh)
            g.add(_T("dãy", 13, TEXT_MUTED).move_to(_P(-1.25, 0.35)), _T("dãy", 13, TEXT_MUTED).move_to(_P(-1.25, -0.35)))
            g.add(Arrow(_P(1.6, -0.35), _P(0.9, -0.35), buff=0, color=AMBER, stroke_width=2.5, tip_length=0.12))
            g.scale(0.78).move_to(ORIGIN)
        else:        # xe buýt 256 chỗ
            def bus(cc, op):
                b = Rectangle(width=1.2, height=0.55, stroke_color=cc, stroke_width=2, fill_color=cc, fill_opacity=op)
                ws = VGroup(*[Square(0.16, stroke_width=0, fill_color=PANEL_BG, fill_opacity=1).move_to(b.get_center() + RIGHT * (i - 2) * 0.22 + UP * 0.05) for i in range(5)])
                wh = VGroup(*[Circle(radius=0.09, fill_color=TEXT_MAIN, fill_opacity=1, stroke_width=0).move_to(b.get_bottom() + RIGHT * s * 0.35) for s in (-1, 1)])
                return VGroup(b, ws, wh)
            b1 = bus(col, 0.6).move_to(_P(-0.9, 0.0))
            b2 = bus(CORAL, 0.15).move_to(_P(1.1, 0.0))
            p = VGroup(Circle(radius=0.11, fill_color=CORAL, fill_opacity=1, stroke_width=0),
                       _T("+1", 15, CORAL, weight=BOLD).next_to(ORIGIN, UP, buff=0.12)).move_to(_P(0.1, 0.0))
            g.add(b1, p, b2, _T("256", 14, TEXT_MAIN, MONO).move_to(b1.get_top() + UP * 0.17))
        return g

    def mnemonic(self):
        hdr = make_header("Mẹo nhớ: mỗi công thức một bức tranh", "6 lá bài", AMBER)
        items = [
            ("Amdahl = cổ chai", "S = 1 / (P/N + S)", CYAN),
            ("Giới hạn = trần nhà", "tối đa = 1 / (1 − P)", CYAN),
            ("static = chia bánh", "n/p lần lặp mỗi luồng", EMERALD),
            ("MPI = xe tải", "t(n) = α + n/β", AMBER),
            ("CUDA idx = số nhà", "blockIdx.x·B + threadIdx.x", VIOLET),
            ("nblocks = xe buýt", "(n + 255) / 256", VIOLET),
        ]
        panels, draws = [], []
        for k, (cap, fm, col) in enumerate(items):
            fr = RoundedRectangle(width=4.0, height=2.15, corner_radius=0.14, stroke_color=col, stroke_width=1.8,
                                  fill_color=PANEL_BG, fill_opacity=0.95)
            dr = self._draw(k, col)
            dr.move_to(fr.get_center() + UP * 0.35)
            c = _fit(_T(cap, 18, col, weight=BOLD), 3.7).move_to(fr.get_center() + DOWN * 0.58)
            m = _fit(_T(fm, 14, TEXT_MUTED, MONO), 3.7).move_to(fr.get_center() + DOWN * 0.88)
            cx = -4.15 + (k % 3) * 4.15
            cy = 1.45 if k < 3 else -0.95
            pan = VGroup(fr, c, m).move_to(_P(cx, cy))
            dr.move_to(pan[0].get_center() + UP * 0.35)
            panels.append(pan)
            draws.append(dr)
        mascot = make_mascot("wow", 0.42).move_to(_P(-5.6, -2.85))
        bub = make_bubble("Vẽ trong đầu, nhớ lâu hơn!", 4.2, AMBER, 18).next_to(mascot, RIGHT, buff=0.3)

        def steps():
            yield ([FadeIn(hdr), FadeIn(mascot), FadeIn(bub)], 0.8)
            for k in range(6):
                yield ([FadeIn(panels[k]), Create(draws[k]) if k in (1,) else FadeIn(draws[k], scale=0.8)], 0.7)
                yield ([Indicate(draws[k], color=items[k][2], scale_factor=1.12)], 0.6)
                if k == 5:
                    yield ([bounce(mascot)], 0.5)
        play_voiced(self, "06_10", steps())
        clear_stage(self)

    # ---- rapid fire ---------------------------------------------------------
    def rapid_fire(self):
        hdr = make_header("Vòng tốc độ: Đúng hay Sai?", "", CORAL)
        hud = make_hud(0, 0, 1).move_to(_P(5.2, 3.15))
        mascot = make_mascot("think", 0.9).move_to(_P(-5.0, -0.2))
        bub = make_bubble("Đoán thử!", 2.0, AMBER, 20).move_to(_P(-5.0, 1.3))
        Q = [
            ("Màn 1", "Thêm bộ xử lý mãi mãi,\nspeedup tăng mãi mãi?", False, "Sai: có trần 1 / (1 − P)", CYAN),
            ("Màn 2", "Race condition: dùng mutex hoặc\natomic để bảo vệ được?", True, "Đúng: mutex, atomic, critical", EMERALD),
            ("Màn 3", "MPI_Allreduce: chỉ rank 0\nnhận được tổng?", False, "Sai: mọi tiến trình đều nhận tổng", AMBER),
            ("Màn 4", "Kernel __global__ phải\ntrả về void?", True, "Đúng: __global__ trả về void", VIOLET),
            ("Màn 4", "hello<<<2, 4>>>() chạy\ntổng cộng 8 luồng?", True, "Đúng: 2 block x 4 luồng = 8", VIOLET),
        ]

        def build(q):
            tag, txt, ans, expl, col = q
            fr = RoundedRectangle(width=7.6, height=1.9, corner_radius=0.16, stroke_color=col, stroke_width=2.4,
                                  fill_color=PANEL_BG, fill_opacity=0.97)
            chip = _T(tag, 15, col, weight=BOLD).move_to(fr.get_corner(UL) + RIGHT * 0.55 + DOWN * 0.3)
            t = _fit(_T(txt, 26, TEXT_MAIN, weight=BOLD), 7.0).move_to(fr.get_center() + DOWN * 0.15)
            card = VGroup(fr, chip, t).move_to(_P(0.7, 1.05))
            bt, bf = [], []
            for lab, c in (("Đúng", EMERALD), ("Sai", CORAL)):
                r = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.14, stroke_color=c, stroke_width=2.4,
                                     fill_color=PANEL_BG, fill_opacity=1)
                bt.append(VGroup(r, _T(lab, 24, c, weight=BOLD).move_to(r)))
            bts = VGroup(*bt).arrange(RIGHT, buff=0.6).move_to(_P(0.7, -0.75))
            ex = _fit(_T(expl, 22, EMERALD if ans else CORAL, weight=BOLD), 7.4).move_to(_P(0.7, -1.95))
            return card, bts, ex, ans

        def steps():
            yield ([FadeIn(hdr), FadeIn(hud), FadeIn(mascot), FadeIn(bub)], 0.8)
            prev = None
            for n, q in enumerate(Q):
                card, bts, ex, ans = build(q)
                a = [FadeIn(card, shift=DOWN * 0.15), FadeIn(bts, shift=UP * 0.15),
                     Transform(mascot, make_mascot("think", 0.9).move_to(mascot))]
                if prev is not None:
                    a += [FadeOut(prev)]
                yield (a, 0.8)
                yield ([Wait(run_time=2.5)], 2.5)
                win = bts[0] if ans else bts[1]
                lose = bts[1] if ans else bts[0]
                yield ([win[0].animate.set_fill("#0B3B2E" if ans else "#3B1218", 1.0).set_stroke(width=5),
                        lose.animate.set_opacity(0.3), FadeIn(ex, shift=UP * 0.1),
                        Transform(mascot, make_mascot("cheer", 0.9).move_to(mascot)),
                        Transform(hud, make_hud(24 * (n + 1), n + 1, 1 + min(n, 3)).move_to(hud.get_center()))], 0.7)
                yield ([bounce(mascot, 0.3, 0.5)], 0.5)
                prev = VGroup(card, bts, ex)
        play_voiced(self, "06_11", steps())
        clear_stage(self)

    # ---- race track ---------------------------------------------------------
    def race_track(self):
        hdr = make_header("Ngày thi: đường đua 65 phút", "40 / 20 / 5", AMBER)
        sc = 12.2 / 65
        x0 = -6.1
        ty = 0.0
        segs = [(40, "40′ trắc nghiệm", CYAN), (20, "20′ tự luận", AMBER), (5, "5′", CORAL)]
        track = VGroup()
        xx = x0
        cents = []
        for m, nm, col in segs:
            w = m * sc
            r = Rectangle(width=w, height=1.1, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.28)
            r.move_to(_P(xx + w / 2, ty))
            tt = _fit(_T(nm, 18, col, weight=BOLD), w - 0.1).move_to(r.get_center() + DOWN * 0.0)
            tt.move_to(r.get_bottom() + UP * 0.18) if False else None
            track.add(VGroup(r, tt))
            cents.append(xx + w / 2)
            xx += w
        flags = VGroup()
        for m in (0, 40, 60, 65):
            x = x0 + m * sc
            flags.add(Line(_P(x, ty + 0.45), _P(x, ty + 0.95), color=TEXT_MAIN, stroke_width=2.5),
                      Polygon(_P(x, ty + 0.95), _P(x + 0.3, ty + 0.83), _P(x, ty + 0.71), fill_color=CORAL if m == 65 else AMBER,
                              fill_opacity=1, stroke_width=0))
        mascot = make_mascot("happy", 0.46).move_to(_P(x0 + 0.5, ty + 0.05))
        clock = _T("Còn 65′", 24, AMBER, MONO, BOLD).move_to(_P(4.9, 2.05))
        # predict bubble
        q = _T("?", 44, AMBER, weight=BOLD)
        qb = VGroup(RoundedRectangle(width=7.4, height=1.0, corner_radius=0.18, stroke_color=AMBER, stroke_width=2.4,
                                     fill_color=PANEL_BG, fill_opacity=0.98),
                    _T("Đoán thử: mỗi câu trắc nghiệm có bao nhiêu giây?", 20, TEXT_MAIN)).move_to(_P(-2.4, 1.95))
        qb[1].move_to(qb[0].get_center() + LEFT * 0.4)
        q.move_to(qb[0].get_right() + LEFT * 0.45)
        qb.add(q)
        ans = _fit(_T("khoảng 40 đến 60 giây/câu", 20, EMERALD, weight=BOLD), 5.2).move_to(qb[0].get_center())
        # tips
        tips = []
        specs = [("Đọc kỹ bẫy", "trước khi chọn đáp án", CYAN, 0), ("Máy tính", "Amdahl, α + n/β", AMBER, 1),
                 ("Kiểm tra đơn vị", "5′ cuối: đơn vị + bẫy code", CORAL, 2)]
        for k, (tt, sub, col, ci) in enumerate(specs):
            fr = RoundedRectangle(width=3.9, height=1.15, corner_radius=0.14, stroke_color=col, stroke_width=2,
                                  fill_color=PANEL_BG, fill_opacity=0.97)
            if k == 0:
                ic = VGroup(Circle(radius=0.2, stroke_color=col, stroke_width=3), Line(_P(0.14, -0.14), _P(0.34, -0.34), color=col, stroke_width=4))
            elif k == 1:
                ic = VGroup(Rectangle(width=0.5, height=0.65, stroke_color=col, stroke_width=2.5, fill_opacity=0),
                            Rectangle(width=0.38, height=0.14, stroke_width=0, fill_color=col, fill_opacity=0.8).shift(UP * 0.2),
                            *[Dot(_P(-0.12 + a * 0.12, -0.05 - b * 0.14), radius=0.03, color=col) for a in range(3) for b in range(2)])
            else:
                ic = VGroup(Rectangle(width=0.75, height=0.26, stroke_color=col, stroke_width=2.5, fill_opacity=0),
                            *[Line(_P(-0.3 + a * 0.15, 0.13), _P(-0.3 + a * 0.15, 0.0), color=col, stroke_width=2) for a in range(5)])
            ic.move_to(fr.get_left() + RIGHT * 0.65)
            t1 = _fit(_T(tt, 20, col, weight=BOLD), 2.6)
            t2 = _fit(_T(sub, 14, TEXT_MAIN), 2.6)
            tx = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(fr.get_center() + RIGHT * 0.5)
            card = VGroup(fr, ic, tx).move_to(_P(-4.25 + k * 4.25, -1.75))
            cn = Line(_P(cents[k], ty - 0.45), card.get_top(), color=col, stroke_width=2)
            tips.append(VGroup(cn, card))
        finish = VGroup(*[Square(0.14, stroke_width=0, fill_color=TEXT_MAIN if (a + b) % 2 else "#0D1117", fill_opacity=1)
                          .move_to(_P(x0 + 65 * sc + 0.0 - 0.07 + 0, ty + 0.35 - b * 0.14 - 0.0)) for a in range(1) for b in range(6)])

        def hop():
            return bounce(mascot, 0.15, 0.3)

        def steps():
            yield ([FadeIn(hdr), LaggedStart(*[GrowFromEdge(b, LEFT) for b in track], lag_ratio=0.4), FadeIn(flags), FadeIn(mascot), FadeIn(clock)], 1.6)
            yield ([FadeIn(qb, shift=DOWN * 0.15), Transform(mascot, make_mascot("think", 0.46).move_to(mascot))], 0.6)
            yield ([Wait(run_time=3)], 3.0)
            yield ([Transform(qb[1], ans.move_to(qb[0].get_center())), FadeOut(qb[2]), Transform(mascot, make_mascot("cheer", 0.46).move_to(mascot)), hop()], 0.6)
            yield ([FadeOut(qb), Transform(mascot, make_mascot("happy", 0.46).move_to(mascot))], 0.4)
            yield ([mascot.animate.move_to(_P(x0 + 40 * sc - 0.4, ty + 0.05)), Transform(clock, _T("Còn 25′", 24, AMBER, MONO, BOLD).move_to(clock)),
                    FadeIn(tips[0], shift=UP * 0.1)], 1.6)
            yield ([mascot.animate.move_to(_P(x0 + 60 * sc - 0.4, ty + 0.05)), Transform(clock, _T("Còn 5′", 24, CORAL, MONO, BOLD).move_to(clock)),
                    FadeIn(tips[1], shift=UP * 0.1)], 1.4)
            yield ([mascot.animate.move_to(_P(x0 + 65 * sc - 0.3, ty + 0.05)), Transform(clock, _T("Hết giờ", 24, EMERALD, MONO, BOLD).move_to(clock)),
                    FadeIn(tips[2], shift=UP * 0.1)], 1.2)
            yield ([Transform(mascot, make_mascot("cheer", 0.46).move_to(mascot)), hop()], 0.6)
        play_voiced(self, "06_12", steps())
        clear_stage(self)
