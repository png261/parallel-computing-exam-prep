import numpy as np
from manim import *
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
    else:            # algorithms: tree
        pts = [_P(0, 0.4), _P(-0.5, 0), _P(0.5, 0), _P(-0.75, -0.4), _P(-0.25, -0.4), _P(0.5, -0.4)]
        for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]:
            g.add(Line(pts[a], pts[b], color=TEXT_MUTED, stroke_width=2))
        for p in pts:
            g.add(Dot(p, radius=0.09, color=col))
    return g


class Scene06Summary(Scene):
    def construct(self):
        setup_bg(self)
        hdr = make_header("Tổng kết: một trang để nhớ", "65 phút", AMBER)

        mods = [("Nền tảng", CYAN), ("Bộ nhớ chung", EMERALD), ("MPI", AMBER), ("CUDA", VIOLET), ("Thuật toán", CORAL)]
        tiles = []
        for i, (nm, col) in enumerate(mods):
            fr = RoundedRectangle(width=2.3, height=1.55, corner_radius=0.12, stroke_color=col, stroke_width=1.8,
                                  fill_color=PANEL_BG, fill_opacity=0.9)
            ic = _icon(i, col).move_to(fr.get_center() + UP * 0.2)
            lb = _T(nm, 16, col, weight=BOLD).move_to(fr.get_bottom() + UP * 0.25)
            tiles.append(VGroup(fr, ic, lb).move_to(_P((i - 2) * 2.5, 1.8)))

        F = [
            ("1", "Amdahl: S = 1 / (P/N + 1 − P)", CYAN, 0),
            ("2", "E = S/p = Ts / (p·Tp)", CYAN, 0),
            ("3", "MPI: t(n) = α + n/β", AMBER, 2),
            ("4", "idx = blockIdx.x·B + threadIdx.x", VIOLET, 3),
            ("5", "SAXPY BW = 3·n·4 B / t", VIOLET, 3),
            ("6", "Euler: v[A] − v[C] + 1", CORAL, 4),
        ]
        fcards = []
        for k, (num, txt, col, tidx) in enumerate(F):
            fr = RoundedRectangle(width=6.1, height=0.66, corner_radius=0.1, stroke_color=col, stroke_width=1.6,
                                  fill_color=PANEL_BG, fill_opacity=0.95)
            badge = _T(num, 18, col, MONO, BOLD).move_to(fr.get_left() + RIGHT * 0.3)
            t = _T(txt, 22, TEXT_MAIN, MONO)
            if t.width > 5.1:
                t.scale_to_fit_width(5.1)
            t.next_to(badge, RIGHT, buff=0.25)
            c = VGroup(fr, badge, t)
            c.move_to(_P(-3.3 if k % 2 == 0 else 3.3, 0.3 - (k // 2) * 0.8))
            fcards.append(c)

        # timeline
        sc = 12.2 / 65
        x0 = -6.1
        segs = [(40, "40′ trắc nghiệm", CYAN), (20, "20′ tự luận", AMBER), (5, "5′", CORAL)]
        bars = VGroup()
        xx = x0
        for m, nm, col in segs:
            w = m * sc
            r = Rectangle(width=w, height=0.5, stroke_color="#0D1117", stroke_width=2, fill_color=col, fill_opacity=0.85)
            r.move_to(_P(xx + w / 2, -2.35))
            t = _T(nm, 17, "#0D1117", weight=BOLD).move_to(r)
            if t.width > w - 0.1:
                t.scale_to_fit_width(w - 0.1)
            bars.add(VGroup(r, t))
            xx += w
        ticks = VGroup(*[VGroup(Line(_P(x0 + m * sc, -2.65), _P(x0 + m * sc, -2.77), color=TEXT_MUTED),
                                _T(str(m), 13, TEXT_MUTED, MONO).move_to(_P(x0 + m * sc, -2.98))) for m in (0, 40, 60, 65)])
        chk = _T("kiểm tra đơn vị & bẫy", 14, CORAL).move_to(_P(x0 + 62.5 * sc - 1.0, -3.3))
        marker = Triangle(color=TEXT_MAIN, fill_opacity=1).scale(0.12).rotate(PI).move_to(_P(x0, -1.98))

        def steps():
            yield ([FadeIn(hdr), LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tiles], lag_ratio=0.2)], 2.0)
            for k, c in enumerate(fcards):
                t = tiles[F[k][3]]
                yield ([FadeIn(c, shift=UP * 0.1), Indicate(t[0], color=F[k][2], scale_factor=1.06)], 1.3)
            yield ([FadeIn(ticks), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.5), FadeIn(marker)], 2.0)
            yield ([marker.animate.move_to(_P(x0 + 40 * sc, -1.98))], 1.2)
            yield ([marker.animate.move_to(_P(x0 + 60 * sc, -1.98))], 1.0)
            yield ([marker.animate.move_to(_P(x0 + 65 * sc, -1.98)), FadeIn(chk)], 1.0)
        play_voiced(self, "06_01", steps())
        clear_stage(self)
