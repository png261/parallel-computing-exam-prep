import numpy as np
from manim import *
from scene_utils import (
    setup_bg, make_header, make_card, make_trap_banner, clear_stage, play_voiced,
    make_grid_box, make_bar_chart, make_code_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, BORDER_DIM, SANS, MONO,
)

OWN = [CYAN, AMBER, EMERALD, CORAL]


def T(s, size=16, color=TEXT_MAIN, font=SANS, weight=NORMAL):
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def P(x, y):
    return np.array([x, y, 0.0])


def arr(a, b, col=TEXT_MUTED, sw=2.5, tl=0.14):
    return Arrow(a, b, buff=0, color=col, stroke_width=sw, tip_length=tl,
                 max_tip_length_to_length_ratio=0.6)


def box(w, h, col, fill=PANEL_BG, op=0.95, sw=1.8, r=0.08):
    return RoundedRectangle(width=w, height=h, corner_radius=r, stroke_color=col,
                            stroke_width=sw, fill_color=fill, fill_opacity=op)


def labelbox(s, w, h, col, size=15, font=MONO, fill=PANEL_BG):
    b = box(w, h, col, fill)
    t = T(s, size, TEXT_MAIN, font)
    if t.width > w - 0.1:
        t.scale_to_fit_width(w - 0.1)
    t.move_to(b)
    return VGroup(b, t)


def seg_01_09(self):
    hdr = make_header("Bốn kỹ thuật phân rã", "Chương 7", VIOLET)
    cs = [(-3.3, 1.38), (3.3, 1.38), (-3.3, -1.5), (3.3, -1.5)]
    names = [("Đệ quy", CYAN), ("Dữ liệu", AMBER), ("Thăm dò", EMERALD), ("Suy đoán", CORAL)]
    frames = VGroup()
    for (cx, cy), (nm, col) in zip(cs, names):
        fr = RoundedRectangle(width=6.1, height=2.65, corner_radius=0.12, stroke_color=col,
                              stroke_width=1.6, fill_color=PANEL_BG, fill_opacity=0.6).move_to(P(cx, cy))
        tt = T(nm, 18, col, weight=BOLD).move_to(fr.get_top() + DOWN * 0.27)
        frames.add(VGroup(fr, tt))

    # ---- panel 1: recursive split of an array
    cx, cy = cs[0]
    def bar(x, y, w, col, op=0.5):
        return Rectangle(width=w, height=0.28, stroke_color=col, stroke_width=1.5,
                         fill_color=col, fill_opacity=op).move_to(P(x, y))
    root = bar(cx, cy + 0.4, 4.4, VIOLET)
    l1 = VGroup(bar(cx - 1.15, cy - 0.2, 2.1, VIOLET), bar(cx + 1.15, cy - 0.2, 2.1, VIOLET))
    l2 = VGroup(*[bar(cx + dx, cy - 0.8, 1.0, OWN[i]) for i, dx in enumerate([-1.7, -0.6, 0.6, 1.7])])
    c1 = VGroup(*[Line(root.get_bottom(), b.get_top(), color=TEXT_MUTED, stroke_width=1.5) for b in l1])
    c2 = VGroup(*[Line(l1[i // 2].get_bottom(), b.get_top(), color=TEXT_MUTED, stroke_width=1.5) for i, b in enumerate(l2)])
    p1_lbl = VGroup(*[T("P%d" % i, 13, OWN[i], MONO).next_to(l2[i], DOWN, buff=0.06) for i in range(4)])

    # ---- panel 2: matrix split by rows, owner computes
    cx, cy = cs[1]
    gc = P(cx - 1.0, cy - 0.2)
    cells = VGroup(*[Square(0.36, stroke_color=BORDER_DIM, stroke_width=1, fill_color=PANEL_BG, fill_opacity=1)
                     .move_to(gc + P((c - 1.5) * 0.38, -(r - 1.5) * 0.38)) for r in range(4) for c in range(4)])
    owners = VGroup(*[VGroup(arr(P(cx - 0.12, gc[1] - (r - 1.5) * 0.38), P(cx + 0.8, gc[1] - (r - 1.5) * 0.38), OWN[r], 2, 0.12),
                             T("P%d" % r, 15, OWN[r], MONO).move_to(P(cx + 1.15, gc[1] - (r - 1.5) * 0.38))) for r in range(4)])

    # ---- panel 3: 15-puzzle search tree
    cx, cy = cs[2]
    puz = VGroup(*[Square(0.3, stroke_color=TEXT_MUTED, stroke_width=1.2, fill_color=PANEL_BG if k != 8 else BG_DARK(),
                          fill_opacity=1).move_to(P(cx - 2.35 + (k % 3) * 0.32, cy - 0.2 - (k // 3) * 0.32 + 0.32))
                  for k in range(9)])
    for k, c in enumerate(puz):
        if k != 8:
            c.add(T(str(k + 1), 12, TEXT_MAIN, MONO).move_to(c))
    npos = {"r": P(cx - 1.0, cy - 0.2), "a": P(cx + 0.3, cy + 0.4), "b": P(cx + 0.3, cy - 0.2), "c": P(cx + 0.3, cy - 0.8),
            "a1": P(cx + 1.6, cy + 0.6), "a2": P(cx + 1.6, cy + 0.15), "c1": P(cx + 1.6, cy - 0.6), "c2": P(cx + 1.6, cy - 1.0)}
    ed = [("r", "a"), ("r", "b"), ("r", "c"), ("a", "a1"), ("a", "a2"), ("c", "c1"), ("c", "c2")]
    tedges = VGroup(*[Line(npos[a], npos[b], color=TEXT_MUTED, stroke_width=1.8) for a, b in ed])
    tnodes = {k: Circle(0.13, stroke_color=TEXT_MUTED, stroke_width=1.5, fill_color=PANEL_BG, fill_opacity=1).move_to(v)
              for k, v in npos.items()}
    tn = VGroup(*tnodes.values())
    cpu = [Dot(npos["r"], radius=0.09, color=OWN[i]) for i in range(3)]
    for d_ in cpu:
        d_.set_z_index(5)
    goal = Text("★", font=SANS, font_size=20, color=AMBER).move_to(npos["c2"]).shift(RIGHT * 0.3)

    # ---- panel 4: speculation
    cx, cy = cs[3]
    dia = Square(0.62, stroke_color=CORAL, stroke_width=1.8, fill_color=PANEL_BG, fill_opacity=1).rotate(PI / 4).move_to(P(cx - 2.1, cy - 0.2))
    q = T("?", 20, AMBER, weight=BOLD).move_to(dia)
    ba = labelbox("A", 1.3, 0.42, CYAN, 15, SANS).move_to(P(cx + 0.1, cy + 0.35))
    bb = labelbox("B", 1.3, 0.42, AMBER, 15, SANS).move_to(P(cx + 0.1, cy - 0.75))
    res = Circle(0.2, stroke_color=EMERALD, stroke_width=1.8, fill_color=PANEL_BG, fill_opacity=1).move_to(P(cx + 2.3, cy - 0.2))
    res_t = T("kq", 13, EMERALD, SANS).move_to(res)
    a_in = arr(dia.get_center() + P(0.3, 0.2), ba.get_left(), TEXT_MUTED, 2, 0.12)
    b_in = arr(dia.get_center() + P(0.3, -0.2), bb.get_left(), TEXT_MUTED, 2, 0.12)
    a_out = arr(ba.get_right(), res.get_center() + P(-0.16, 0.12), TEXT_MUTED, 2, 0.12)
    b_out = arr(bb.get_right(), res.get_center() + P(-0.16, -0.12), TEXT_MUTED, 2, 0.12)
    fa = Rectangle(width=1.2, height=0.12, stroke_width=0, fill_color=CYAN, fill_opacity=0.9)
    fb = Rectangle(width=1.2, height=0.12, stroke_width=0, fill_color=AMBER, fill_opacity=0.9)
    fa.move_to(ba.get_bottom() + DOWN * 0.1)
    fb.move_to(bb.get_bottom() + DOWN * 0.1)
    fa.save_state(); fb.save_state()
    fa.stretch_to_fit_width(0.01).align_to(ba.get_bottom() + LEFT * 0.6, LEFT)
    fb.stretch_to_fit_width(0.01).align_to(bb.get_bottom() + LEFT * 0.6, LEFT)
    cross = T("✗", 26, CORAL, weight=BOLD).move_to(bb.get_right() + RIGHT * 0.3)
    tick = T("✓", 22, EMERALD, weight=BOLD).move_to(dia)

    def steps():
        yield ([FadeIn(hdr), FadeIn(frames)], 1.2)
        yield ([FadeIn(root)], 0.8)
        yield ([Create(c1), TransformFromCopy(root, l1[0]), TransformFromCopy(root, l1[1])], 1.4)
        yield ([Create(c2), *[TransformFromCopy(l1[i // 2], b) for i, b in enumerate(l2)], FadeIn(p1_lbl)], 1.6)
        yield ([FadeIn(cells)], 0.9)
        yield ([LaggedStart(*[cells[r * 4 + c].animate.set_fill(OWN[r], opacity=0.7) for r in range(4) for c in range(4)], lag_ratio=0.08)], 1.6)
        yield ([FadeIn(owners)], 1.0)
        yield ([Indicate(cells[8:12], color=EMERALD, scale_factor=1.1)], 1.0)
        yield ([FadeIn(puz), FadeIn(tedges), FadeIn(tn)], 1.4)
        yield ([cpu[0].animate.move_to(npos["a"]), cpu[1].animate.move_to(npos["b"]), cpu[2].animate.move_to(npos["c"])], 1.2)
        yield ([cpu[0].animate.move_to(npos["a2"]), cpu[1].animate.set_opacity(0.0), cpu[2].animate.move_to(npos["c2"])], 1.4)
        yield ([tnodes["c2"].animate.set_fill(AMBER, opacity=1).set_stroke(AMBER), FadeIn(goal, scale=1.5), FadeOut(cpu[0])], 1.0)
        yield ([FadeIn(VGroup(dia, q)), FadeIn(VGroup(ba, bb)), FadeIn(VGroup(a_in, b_in, a_out, b_out, res, res_t))], 1.4)
        yield ([fa.animate.restore(), fb.animate.restore(), Indicate(q, color=AMBER)], 2.4)
        yield ([FadeOut(q), FadeIn(tick), bb.animate.set_opacity(0.3), fb.animate.set_fill(CORAL), FadeIn(cross)], 1.2)
    play_voiced(self, "01_09", steps())
    clear_stage(self)


def BG_DARK():
    return "#0D1117"


def seg_01_13(self):
    hdr = make_header("Ánh xạ tác vụ lên bộ xử lý", "Chương 7", EMERALD)
    n = 16
    pitch, cw = 0.57, 0.5
    x0 = -3.5
    rows = [("Khối", [i // 4 for i in range(n)]),
            ("Vòng", [i % 4 for i in range(n)]),
            ("Khối-vòng", [(i // 2) % 4 for i in range(n)]),
            ("Ngẫu nhiên", [3, 0, 2, 1, 1, 3, 0, 2, 2, 1, 3, 0, 0, 2, 1, 3])]
    ys = [1.8, 1.0, 0.2, -0.6]
    strips = []
    labels = VGroup()
    for (nm, own), y in zip(rows, ys):
        cells = VGroup(*[Square(cw, stroke_color=BORDER_DIM, stroke_width=1, fill_color=PANEL_BG, fill_opacity=1)
                         .move_to(P(x0 + k * pitch, y)) for k in range(n)])
        strips.append(cells)
        lb = T(nm, 16, TEXT_MAIN).move_to(P(-5.6, y), aligned_edge=LEFT)
        lb.align_to(P(-6.4, y), LEFT)
        labels.add(lb)
    legend = VGroup(*[VGroup(Square(0.24, stroke_width=0, fill_color=OWN[i], fill_opacity=0.9),
                             T("P%d" % i, 14, OWN[i], MONO)).arrange(RIGHT, buff=0.1) for i in range(4)]).arrange(RIGHT, buff=0.4)
    legend.move_to(P(0.0, -1.6))

    # load bars (task i costs i+1)
    cost = [i + 1 for i in range(n)]
    def loads(own):
        l = [0] * 4
        for c, o in zip(cost, own):
            l[o] += c
        return l
    def bars(own, cx, title):
        l = loads(own)
        g = VGroup()
        base_y = -2.0
        for i, v in enumerate(l):
            h = v / 60 * 2.8
            r = Rectangle(width=0.7, height=h, stroke_width=0, fill_color=OWN[i], fill_opacity=0.85)
            r.move_to(P(cx + (i - 1.5) * 0.9, base_y + h / 2))
            t = T(str(v), 15, OWN[i], MONO, BOLD).next_to(r, UP, buff=0.05)
            g.add(VGroup(r, t))
        axis = Line(P(cx - 2.1, base_y), P(cx + 2.1, base_y), color=TEXT_MUTED, stroke_width=2)
        ttl = T(title, 18, TEXT_MAIN, weight=BOLD).move_to(P(cx, 1.55))
        return VGroup(axis, g, ttl), g
    bl, bl_g = bars(rows[0][1], -3.2, "Khối")
    cy_, cy_g = bars(rows[1][1], 3.2, "Vòng")
    avg = DashedLine(P(-5.5, -2.0 + 34 / 60 * 2.8), P(5.5, -2.0 + 34 / 60 * 2.8), color=AMBER, stroke_width=2)
    avg_t = T("đều = 34", 14, AMBER, MONO).move_to(P(-5.2, -2.0 + 34 / 60 * 2.8 + 0.2))
    cost_t = T("tác vụ i tốn i đơn vị", 15, TEXT_MUTED).move_to(P(0, 2.3))
    trap = make_trap_banner("Số tác vụ bằng nhau ≠ tải cân bằng")

    # dynamic: master / workers
    master = labelbox("Master", 1.7, 0.8, VIOLET, 17, SANS).move_to(P(-3.6, -0.2))
    queue_x = [-5.7 + k * 0.62 for k in range(7)]
    qy = 1.7
    qlbl = T("hàng đợi", 14, TEXT_MUTED).move_to(P(-4.0, qy + 0.5))
    sizes = [3.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0]
    toks = []
    for k in range(7):
        tk = VGroup(Square(0.5, stroke_color=VIOLET, stroke_width=1.6, fill_color="#2A2350", fill_opacity=1),
                    T(str(k + 1), 15, TEXT_MAIN, MONO)).move_to(P(queue_x[k], qy))
        toks.append(tk)
    wy = [1.3, 0.0, -1.3]
    wk = [labelbox("W%d" % (i + 1), 1.8, 0.8, TEXT_MUTED, 17, SANS).move_to(P(2.6, wy[i])) for i in range(3)]
    wires = VGroup(*[Line(master.get_right(), wk[i].get_left(), color=BORDER_DIM, stroke_width=1.5) for i in range(3)])
    wcol = [CYAN, AMBER, EMERALD]
    held = [None, None, None]

    def assign(k, w):
        tk = toks[k]
        held[w] = k
        return [tk.animate.move_to(wk[w].get_center() + P(-0.9 - 0.35, 0)).scale(0.8),
                wk[w][0].animate.set_stroke(wcol[w], 3).set_fill("#10303a", 1)]

    def finish(w):
        tk = toks[held[w]]
        return [FadeOut(tk, scale=0.5), wk[w][0].animate.set_stroke(TEXT_MUTED, 1.8).set_fill(PANEL_BG, 0.95)]

    def req(w):
        a = CurvedArrow(wk[w].get_left() + P(0, 0.1), master.get_right() + P(0.05, 0.15 * (1 - w)), angle=-0.4,
                        color=wcol[w], stroke_width=3, tip_length=0.15)
        return a

    def steps():
        yield ([FadeIn(hdr), FadeIn(labels), FadeIn(legend)], 1.0)
        for s_, (nm, own) in zip(strips, rows):
            yield ([FadeIn(s_)], 0.3)
        for s_, (nm, own) in zip(strips, rows):
            yield ([LaggedStart(*[s_[k].animate.set_fill(OWN[own[k]], 0.75) for k in range(n)], lag_ratio=0.05)], 1.6)
        yield ([FadeOut(VGroup(*strips)), FadeOut(labels), FadeOut(legend)], 0.6)
        yield ([FadeIn(bl), FadeIn(cost_t)], 1.0)
        yield ([LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bl_g], lag_ratio=0.2), FadeIn(VGroup(*[b[1] for b in bl_g]))], 1.6)
        yield ([FadeIn(cy_)], 0.8)
        yield ([LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in cy_g], lag_ratio=0.2), FadeIn(VGroup(*[b[1] for b in cy_g])), Create(avg), FadeIn(avg_t)], 1.8)
        yield ([FadeIn(trap)], 0.8)
        yield ([FadeOut(VGroup(bl, cy_, avg, avg_t, cost_t, trap))], 0.6)
        # dynamic
        yield ([FadeIn(master), FadeIn(VGroup(*wk)), Create(wires), FadeIn(qlbl), FadeIn(VGroup(*toks))], 1.2)
        yield (assign(0, 0) + assign(1, 1) + assign(2, 2), 1.4)
        yield (finish(1) + finish(2) + [FadeIn(req(1)), FadeIn(req(2))], 0.8)
        yield (assign(3, 1) + assign(4, 2) + [FadeOut(m) for m in self.mobjects if isinstance(m, CurvedArrow)], 1.2)
        yield (finish(1) + [FadeIn(req(1))], 1.0)
        yield (assign(5, 1) + [FadeOut(m) for m in self.mobjects if isinstance(m, CurvedArrow)], 1.0)
        yield (finish(0) + finish(2) + [FadeIn(req(0))], 1.0)
        yield (assign(6, 0) + [FadeOut(m) for m in self.mobjects if isinstance(m, CurvedArrow)], 1.0)
    play_voiced(self, "01_13", steps())
    clear_stage(self)


def seg_01_10(self):
    hdr = make_header("Overhead và isoefficiency: cộng 64 số", "Chương 7", EMERALD)
    xs = [(i - 3.5) * 1.5 for i in range(8)]
    loc = [36, 100, 164, 228, 292, 356, 420, 484]
    tiles0, dots0, plabs = [], [], VGroup()
    for i in range(8):
        tl = box(1.1, 0.6, CYAN, op=0.95, r=0.06).move_to(P(xs[i], 1.5))
        dg = VGroup(*[Dot(radius=0.045, color=CYAN).move_to(P(xs[i] + (c - 1.5) * 0.17, 1.5 + (0.1 if r == 0 else -0.1)))
                      for r in range(2) for c in range(4)])
        tiles0.append(tl); dots0.append(dg)
        plabs.add(T("P%d" % i, 13, TEXT_MUTED, MONO).move_to(P(xs[i], 2.1)))
    nums = [T(str(v), 17, CYAN, MONO, BOLD).move_to(P(xs[i], 1.5)) for i, v in enumerate(loc)]
    # reduction tree
    lvl = [[(P(xs[i], 1.5), loc[i]) for i in range(8)]]
    ys_ = [1.5, 0.45, -0.6, -1.65]
    vals = loc[:]
    for L in range(1, 4):
        nxt = []
        prev = lvl[-1]
        nv = []
        for j in range(len(prev) // 2):
            p = (prev[2 * j][0] + prev[2 * j + 1][0]) / 2
            p[1] = ys_[L]
            nxt.append((p, prev[2 * j][1] + prev[2 * j + 1][1]))
        lvl.append(nxt)
    lvl_groups, lvl_arrows = [], []
    for L in range(1, 4):
        g = VGroup(); a = VGroup()
        for j, (p, v) in enumerate(lvl[L]):
            col = [AMBER, VIOLET, EMERALD][L - 1]
            tl = box(1.1, 0.55, col, r=0.06).move_to(p)
            tt = T(str(v), 17, col, MONO, BOLD).move_to(p)
            g.add(VGroup(tl, tt))
            for k in (0, 1):
                src = lvl[L - 1][2 * j + k][0]
                a.add(arr(src + DOWN * 0.3, p + P((-0.25 if k == 0 else 0.25), 0.3), col, 2.2, 0.12))
        lvl_groups.append(g); lvl_arrows.append(a)
    f1 = T("Tp = n/p + 2·log₂p = 8 + 6 = 14", 22, TEXT_MAIN, MONO).move_to(P(0, -2.75))
    lvl_lab = T("3 mức", 16, TEXT_MUTED).move_to(P(4.6, -1.0))

    # gantt
    u = 0.16
    def gantt(y, comp, comm, col_e, e_txt, tag):
        x_start = -5.8
        b1 = Rectangle(width=comp * u, height=0.5, stroke_width=0, fill_color=CYAN, fill_opacity=0.85).move_to(P(x_start + comp * u / 2, y))
        b2 = Rectangle(width=comm * u, height=0.5, stroke_width=0, fill_color=CORAL, fill_opacity=0.85).move_to(P(x_start + comp * u + comm * u / 2, y))
        tg = T(tag, 16, TEXT_MAIN, weight=BOLD).move_to(P(x_start, y + 0.5), aligned_edge=LEFT)
        tg.align_to(P(x_start, 0), LEFT)
        nt = T("%d" % comp, 14, BG_DARK(), MONO, BOLD).move_to(b1)
        et = T(e_txt, 24, col_e, MONO, BOLD)
        return VGroup(b1, b2, tg, nt), et
    gA, eA = gantt(1.3, 8, 6, CORAL, "E = 57%", "n = 64")
    eA.move_to(P(-5.8 + 14 * u + 1.2, 1.3))
    gB, eB = gantt(-0.1, 64, 6, EMERALD, "E = 91%", "n = 512")
    eB.move_to(P(4.3, -0.1 + 0.5))
    lg = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=CYAN, fill_opacity=0.9), T("tính", 14)).arrange(RIGHT, buff=0.1),
                VGroup(Square(0.2, stroke_width=0, fill_color=CORAL, fill_opacity=0.9), T("giao tiếp", 14)).arrange(RIGHT, buff=0.1)
                ).arrange(RIGHT, buff=0.4).move_to(P(4.4, 2.4))
    chart = make_bar_chart([57, 80, 91], ["n=64", "n=192", "n=512"], [CORAL, AMBER, EMERALD],
                           max_val=100, width=6.0, height=3.2, unit="%").move_to(P(0, -0.3))
    f2 = T("To = 2p·log p  →  n tăng như p·log p", 22, TEXT_MAIN, MONO).move_to(P(0, -2.9))
    f2.scale_to_fit_width(min(f2.width, 11))
    rowsGantt = VGroup(gA, eA, gB, eB, lg)

    def steps():
        yield ([FadeIn(hdr), FadeIn(plabs), FadeIn(VGroup(*tiles0)), FadeIn(VGroup(*dots0))], 1.4)
        yield ([ReplacementTransform(dots0[i], nums[i]) for i in range(8)], 1.5)
        for L in range(3):
            yield ([LaggedStart(*[Create(a) for a in lvl_arrows[L]], lag_ratio=0.1),
                    *([FadeIn(lvl_lab)] if L == 0 else [])], 1.0)
            yield ([FadeIn(lvl_groups[L], shift=DOWN * 0.15)], 1.0)
        yield ([FadeIn(f1)], 1.2)
        yield ([FadeOut(VGroup(plabs, *tiles0, *nums, *lvl_groups, *lvl_arrows, f1, lvl_lab))], 0.6)
        yield ([FadeIn(lg), FadeIn(gA[2]), GrowFromEdge(gA[0], LEFT), GrowFromEdge(gA[1], LEFT), FadeIn(gA[3])], 1.6)
        yield ([FadeIn(eA, scale=1.2)], 1.0)
        yield ([FadeIn(gB[2]), GrowFromEdge(gB[0], LEFT), GrowFromEdge(gB[1], LEFT), FadeIn(gB[3])], 2.0)
        yield ([FadeIn(eB, scale=1.2)], 1.0)
        yield ([FadeOut(rowsGantt)], 0.5)
        yield ([Create(chart[0]), Create(chart[1])], 0.6)
        yield ([LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart[2]], lag_ratio=0.5)], 2.2)
        yield ([FadeIn(f2)], 1.0)
    play_voiced(self, "01_10", steps())
    clear_stage(self)


def seg_05_06(self):
    hdr = make_header("Tổng tiền tố bằng pointer jumping", "Chương 10", CYAN)
    A = [3, 1, 4, 1, 5, 9, 2, 6]
    rowsv = [A]
    for d in (1, 2, 4):
        p = rowsv[-1]
        rowsv.append([p[i] + (p[i - d] if i >= d else 0) for i in range(8)])
    cols = [TEXT_MUTED, CYAN, AMBER, EMERALD]
    ys = [1.85, 0.5, -0.85, -2.2]
    pitch = 1.2
    xs = [-3.9 + i * pitch for i in range(8)]
    grid = []
    for r in range(4):
        row = VGroup(*[make_grid_box(str(v), w=0.95, h=0.58, color=cols[r], font_size=19).move_to(P(xs[i], ys[r]))
                       for i, v in enumerate(rowsv[r])])
        grid.append(row)
    idx = VGroup(*[T(str(i), 12, TEXT_MUTED, MONO).move_to(P(xs[i], 2.4)) for i in range(8)])
    labs = [T(s, 20, cols[r], MONO, BOLD).move_to(P(-5.8, ys[r])) for r, s in enumerate(["A", "d = 1", "d = 2", "d = 4"])]

    def step_arrows(r, d):
        g = VGroup()
        for i in range(8):
            a = grid[r][i]; b = grid[r + 1][i]
            g.add(Line(a.get_bottom(), b.get_top(), color=BORDER_DIM, stroke_width=1.5))
            if i >= d:
                src = grid[r][i - d]
                hot = (i == 7)
                g.add(arr(src.get_bottom() + DOWN * 0.02, b.get_top() + UP * 0.02, cols[r + 1] if not hot else TEXT_MAIN,
                          3.5 if hot else 2, 0.12))
        return g
    arrs = [step_arrows(r, d) for r, d in zip(range(3), (1, 2, 4))]
    f1 = T("3 bước = log₂8", 22, TEXT_MAIN, MONO).move_to(P(0, -3.05))

    def steps():
        yield ([FadeIn(hdr), FadeIn(idx), FadeIn(labs[0]), FadeIn(grid[0], lag_ratio=0.1)], 1.8)
        for r in range(3):
            yield ([FadeIn(labs[r + 1]), LaggedStart(*[Create(a) for a in arrs[r]], lag_ratio=0.04)], 2.0)
            yield ([FadeIn(grid[r + 1], lag_ratio=0.1)], 1.2)
            if r == 2:
                yield ([Indicate(grid[3][7], color=TEXT_MAIN, scale_factor=1.25)], 1.0)
        yield ([FadeIn(f1)], 0.8)
        yield ([Indicate(grid[3], color=EMERALD, scale_factor=1.08)], 1.2)
    play_voiced(self, "05_06", steps())
    clear_stage(self)


def seg_05_07(self):
    hdr = make_header("Euler tour trên cây nhị phân", "Chương 10", VIOLET)
    pos = {1: P(-3.2, 2.0), 2: P(-4.4, 1.0), 3: P(-2.0, 1.0), 4: P(-5.0, 0.0), 5: P(-3.8, 0.0), 6: P(-2.0, 0.0)}
    nodes = {}
    for k, p in pos.items():
        nodes[k] = VGroup(Circle(0.24, stroke_color=CYAN, stroke_width=2, fill_color=PANEL_BG, fill_opacity=1),
                          T(str(k), 17, TEXT_MAIN, MONO)).move_to(p).set_z_index(3)
    edges = VGroup(*[Line(pos[a], pos[b], color=TEXT_MUTED, stroke_width=2)
                     for a, b in [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]])
    seq = ["1A", "2A", "4A", "4B", "4C", "2B", "5A", "5B", "5C", "2C", "1B", "3A", "6A", "6B", "6C", "3B", "3C", "1C"]
    off = {"A": P(-0.33, 0.12), "B": P(0, -0.36), "C": P(0.33, 0.12)}
    pts = [pos[int(s[0])] + off[s[1]] for s in seq]
    cw = 1.05
    xs = [(i % 9 - 4) * 1.2 for i in range(18)]
    ysr = [-1.1 if i < 9 else -2.3 for i in range(18)]
    cells = VGroup(*[make_grid_box(s, w=cw, h=0.42, color=TEXT_MUTED, font_size=15).move_to(P(xs[i], ysr[i]))
                     for i, s in enumerate(seq)])
    def wts(letter):
        w = [1 if s.endswith(letter) else 0 for s in seq]
        suf = [sum(w[i:]) for i in range(18)]
        wt = VGroup(*[T(str(v), 13, AMBER if v else TEXT_MUTED, MONO).move_to(P(xs[i], ysr[i] - 0.4)) for i, v in enumerate(w)])
        sf = VGroup(*[T(str(v), 16, EMERALD, MONO, BOLD).move_to(P(xs[i], ysr[i] - 0.68)) for i, v in enumerate(suf)])
        return w, suf, wt, sf
    wA, sA, wtA, sfA = wts("A")
    wC, sC, wtC, sfC = wts("C")
    dot = Dot(pts[0], radius=0.1, color=CORAL).set_z_index(6)
    # result
    slots = [P(1.2 + i * 0.95, 1.15) for i in range(6)]
    res_lbl = T("duyệt tiền thứ tự", 16, TEXT_MUTED).move_to(P(3.5, 1.95))
    slot_sq = VGroup(*[Square(0.6, stroke_color=BORDER_DIM, stroke_width=1.5).move_to(p) for p in slots])
    order = sorted([i for i, s in enumerate(seq) if s.endswith("A")], key=lambda i: -sA[i])  # largest suffix first
    order = sorted([i for i, s in enumerate(seq) if s.endswith("A")], key=lambda i: -sA[i])
    f1 = T("vị trí = 7 − v[A]", 20, AMBER, MONO).move_to(P(3.5, 0.3))
    f2 = T("v[2A] − v[2C] + 1 = 6 − 4 + 1 = 3", 19, TEXT_MAIN, MONO).move_to(P(3.2, 1.6))
    f2.scale_to_fit_width(min(f2.width, 5.6))
    sub_lbl = T("kích thước cây con", 16, TEXT_MUTED).move_to(P(3.2, 2.1))

    def steps():
        yield ([FadeIn(hdr), FadeIn(edges), FadeIn(VGroup(*nodes.values()))], 1.2)
        yield ([FadeIn(cells, lag_ratio=0.05)], 1.2)
        yield ([FadeIn(dot)], 0.4)
        prev = pts[0]
        for i in range(18):
            ln = Line(prev, pts[i], color=CORAL, stroke_width=2, stroke_opacity=0.6)
            col = AMBER if seq[i].endswith("A") else (CYAN if seq[i].endswith("B") else VIOLET)
            anims = [dot.animate.move_to(pts[i]), cells[i][0].animate.set_fill(col, 0.35).set_stroke(col)]
            if i > 0:
                anims.append(Create(ln))
            yield (anims, 0.28)
            prev = pts[i]
        yield ([FadeOut(dot)], 0.3)
        yield ([FadeIn(wtA)], 1.0)
        yield ([LaggedStart(*[FadeIn(sfA[i], shift=LEFT * 0.1) for i in range(17, -1, -1)], lag_ratio=0.12)], 2.2)
        yield ([FadeIn(res_lbl), FadeIn(slot_sq), FadeIn(f1)], 0.8)
        anims = []
        res_toks = []
        for rank, i in enumerate(order):
            nd = int(seq[i][0])
            tok = VGroup(Circle(0.22, stroke_color=AMBER, stroke_width=2, fill_color=PANEL_BG, fill_opacity=1),
                         T(str(nd), 16, TEXT_MAIN, MONO)).move_to(slots[rank])
            anims.append(TransformFromCopy(cells[i], tok))
            res_toks.append(tok)
        yield ([LaggedStart(*anims, lag_ratio=0.35)], 3.0)
        yield ([FadeOut(VGroup(res_lbl, slot_sq, f1, *res_toks))], 0.6)
        yield ([Transform(wtA, wtC), Transform(sfA, sfC)], 1.4)
        rects = [SurroundingRectangle(VGroup(*cells[1:9]), color=AMBER, buff=0.04, stroke_width=3),
                 SurroundingRectangle(cells[9], color=AMBER, buff=0.04, stroke_width=3)]
        yield ([FadeIn(sub_lbl), *[Create(r) for r in rects],
                *[nodes[k][0].animate.set_stroke(AMBER, 4) for k in (2, 4, 5)]], 1.4)
        yield ([FadeIn(f2)], 1.2)
    play_voiced(self, "05_07", steps())
    clear_stage(self)


def seg_05_08(self):
    hdr = make_header("Bitonic sort: mạng sắp xếp 8 số", "Chương 10", AMBER)
    n = 8
    ysw = [1.95 - i * 0.5 for i in range(n)]
    cols_x = [-3.6 + 1.5 * c for c in range(6)]
    xl, xr = -5.2, 5.6
    wires = VGroup(*[Line(P(xl, y), P(xr, y), color=BORDER_DIM, stroke_width=1.5) for y in ysw])
    stages = []
    for k, j in [(2, 1), (4, 2), (4, 1), (8, 4), (8, 2), (8, 1)]:
        st = []
        for i in range(n):
            l = i ^ j
            if l > i:
                st.append((i, l, (i & k) == 0))
        stages.append(st)
    comp = []
    for c, st in enumerate(stages):
        g = VGroup()
        for i, l, asc in st:
            a, b = P(cols_x[c], ysw[i]), P(cols_x[c], ysw[l])
            if asc:
                ln = arr(a, b + UP * 0.02, TEXT_MUTED, 2.5, 0.13)
            else:
                ln = arr(b, a + DOWN * 0.02, TEXT_MUTED, 2.5, 0.13)
            g.add(ln)
        comp.append(g)
    clab = VGroup(*[T(str(c + 1), 14, TEXT_MUTED, MONO).move_to(P(cols_x[c], -2.15)) for c in range(6)])
    vals = [3, 7, 4, 8, 6, 2, 1, 5]
    toks = [VGroup(Circle(0.2, stroke_color=CYAN, stroke_width=2, fill_color=PANEL_BG, fill_opacity=1),
                   T(str(v), 17, TEXT_MAIN, MONO, BOLD)).move_to(P(-5.2, ysw[i])).set_z_index(4) for i, v in enumerate(vals)]
    # track which token is at which wire
    at = list(range(n))
    f1 = T("6 cột = 1 + 2 + 3 = k(k+1)/2,  n = 2ᵏ", 20, TEXT_MAIN, MONO).move_to(P(0, -2.85))
    f1.scale_to_fit_width(min(f1.width, 8.5))
    note4 = T("tách ở khoảng cách 4", 15, AMBER).move_to(P(cols_x[3], 2.5))
    lo = Text("nhỏ", font=SANS, font_size=14, color=CYAN).move_to(P(5.0, 1.0))
    hi = Text("lớn", font=SANS, font_size=14, color=AMBER).move_to(P(5.0, -0.7))

    def steps():
        yield ([FadeIn(hdr), Create(wires), FadeIn(clab)], 1.0)
        yield ([FadeIn(VGroup(*toks), lag_ratio=0.1)], 1.2)
        yield ([FadeIn(VGroup(*comp), lag_ratio=0.15)], 1.5)
        for c, st in enumerate(stages):
            yield ([toks[t].animate.move_to(P(cols_x[c], ysw[w])) for w, t in enumerate(at)], 0.7)
            anims = [comp[c].animate.set_color(AMBER)]
            if c == 3:
                anims.append(FadeIn(note4))
            for i, l, asc in st:
                a, b = at[i], at[l]
                va, vb = vals[a], vals[b]
                swap = (va > vb) if asc else (va < vb)
                if swap:
                    at[i], at[l] = b, a
                    anims += [toks[b].animate.move_to(P(cols_x[c], ysw[i])), toks[a].animate.move_to(P(cols_x[c], ysw[l]))]
                    pass
            yield (anims, 1.0)
            yield ([comp[c].animate.set_color(TEXT_MUTED)] + ([FadeOut(note4)] if c == 3 else []), 0.3)
            if c == 3:
                yield ([toks[at[w]][0].animate.set_stroke(CYAN if w < 4 else AMBER, 3) for w in range(8)], 0.8)
        yield ([toks[at[w]].animate.move_to(P(5.0, ysw[w])) for w in range(8)], 0.9)
        yield ([toks[at[w]][0].animate.set_stroke(EMERALD, 3) for w in range(8)], 0.6)
        yield ([FadeIn(f1)], 1.0)
    play_voiced(self, "05_08", steps())
    clear_stage(self)


def seg_05_09(self):
    hdr = make_header("Phương trình nhiệt: SPMD với MPI", "Chương 9", CYAN)
    s = 0.4
    N = 6
    temp = [[0.1] * N for _ in range(N)]
    for r in (2, 3):
        for c in (2, 3):
            temp[r][c] = 1.0
    def colr(v):
        return interpolate_color(ManimColor("#1E3A8A"), ManimColor(CORAL), min(1.0, v) ** 0.8)
    def diffuse(t):
        o = [[0.1] * N for _ in range(N)]
        for r in range(N):
            for c in range(N):
                up = t[r - 1][c] if r > 0 else 0.1
                dn = t[r + 1][c] if r < N - 1 else 0.1
                lf = t[r][c - 1] if c > 0 else 0.1
                rt = t[r][c + 1] if c < N - 1 else 0.1
                o[r][c] = t[r][c] + 0.24 * (up + dn + lf + rt - 4 * t[r][c])
        return o
    T1 = diffuse(temp)
    T2 = diffuse(T1)
    rc = (-5.0, 0.0)
    def cell_xy(r, c, cx, cy):
        return P(cx + (c - 2.5) * s, cy + (1.5 - (r % 2)) * s - s)  # within band: 2 rows centered at cy
    cells = [[None] * N for _ in range(N)]
    bands = []
    for b in range(3):
        g = VGroup()
        for rr in range(2):
            for c in range(N):
                r = 2 * b + rr
                sq = Square(s, stroke_color="#0D1117", stroke_width=1.2, fill_color=colr(temp[r][c]), fill_opacity=1)
                sq.move_to(P(rc[0] + (c - 2.5) * s, (2.5 - r) * s))
                cells[r][c] = sq
                g.add(sq)
        bands.append(g)
    root_grp = VGroup(*bands)
    root_lbl = T("root", 16, VIOLET, MONO, BOLD).move_to(P(rc[0], 1.55))
    bx = 0.0
    byt = [1.75, 0.0, -1.75]
    # ghosts (positions relative to band center)
    def ghost_row(yc):
        return VGroup(*[Square(s, stroke_color=TEXT_MUTED, stroke_width=1, fill_opacity=0).move_to(P(bx + (c - 2.5) * s, yc)) for c in range(N)])
    ghosts = {}
    ghosts[(1, "top")] = ghost_row(byt[1] + 0.6)
    ghosts[(1, "bot")] = ghost_row(byt[1] - 0.6)
    ghosts[(0, "bot")] = ghost_row(byt[0] - 0.6)
    ghosts[(2, "top")] = ghost_row(byt[2] + 0.6)
    allg = VGroup(*ghosts.values())
    cpu_lbl = VGroup(*[T("CPU %d" % i, 15, OWN[i], MONO, BOLD).move_to(P(1.95, byt[i])) for i in range(3)])
    outl = []
    ph = T("MPI_Scatter", 20, AMBER, MONO, BOLD).move_to(P(0, 2.55))
    sc_arrows = VGroup(*[arr(P(-3.7, 0.0), P(-1.45, byt[i]), AMBER, 2.5, 0.15) for i in range(3)])
    ga_x = 5.0
    ga_arrows = VGroup(*[arr(P(1.5, byt[i]), P(3.55, 0.8 - 0.8 * i), EMERALD, 2.5, 0.15) for i in range(3)])
    # stencil cross
    sc = P(-5.0, 0.0)
    sten = VGroup()
    for lab, dx, dy, col in [("c", 0, 0, AMBER), ("u", 0, 1, CYAN), ("d", 0, -1, CYAN), ("l", -1, 0, CYAN), ("r", 1, 0, CYAN)]:
        sq = Square(0.5, stroke_color=col, stroke_width=2.5, fill_color=PANEL_BG, fill_opacity=1).move_to(sc + P(dx * 0.55, dy * 0.55))
        sten.add(VGroup(sq, T(lab, 17, col, MONO, BOLD).move_to(sq)))
    formula = T("ΔC = D/Δx² · (u + d + l + r − 4c)", 21, TEXT_MAIN, MONO).move_to(P(0, -2.95))
    def halo_copies():
        cps, anims = [], []
        for b in range(2):
            low = [bands[b][N + c] for c in range(N)]       # bottom row of band b
            hi = [bands[b + 1][c] for c in range(N)]        # top row of band b+1
            for c in range(N):
                a = low[c].copy(); cps.append(a)
                anims.append(a.animate.move_to(ghosts[(b + 1, "top")][c].get_center()))
                bb = hi[c].copy(); cps.append(bb)
                anims.append(bb.animate.move_to(ghosts[(b, "bot")][c].get_center()))
        return cps, anims
    def recolor(Tn):
        return [cells[r][c].animate.set_fill(colr(Tn[r][c])) for r in range(N) for c in range(N)]
    box_note = {}
    def steps():
        yield ([FadeIn(hdr), FadeIn(root_grp), FadeIn(root_lbl)], 1.4)
        yield ([FadeIn(ph, shift=DOWN * 0.1), FadeIn(sc_arrows)], 1.0)
        yield ([bands[i].animate.move_to(P(bx, byt[i])) for i in range(3)] + [FadeOut(root_lbl)], 1.8)
        outl.extend(SurroundingRectangle(bands[i], buff=0.0, color=OWN[i], stroke_width=3) for i in range(3))
        yield ([FadeIn(cpu_lbl), *[Create(o) for o in outl], FadeOut(sc_arrows), FadeIn(allg)], 1.0)
        for t, Tn in enumerate((T1, T2)):
            ph2 = T("Trao đổi halo" if t == 0 else "Halo, lần hai", 20, AMBER, MONO, BOLD).move_to(P(0, 2.55))
            yield ([Transform(ph, ph2)], 0.5)
            cps, anims = halo_copies()
            self.add(*cps)
            yield (anims, 1.6)
            if t == 0:
                yield ([FadeIn(sten, shift=RIGHT * 0.2), FadeIn(formula)], 1.2)
            ph3 = T("Tính cục bộ", 20, EMERALD, MONO, BOLD).move_to(P(0, 2.55))
            yield ([Transform(ph, ph3)] + recolor(Tn), 1.6)
            yield ([FadeOut(VGroup(*cps))], 0.4)
        yield ([FadeOut(sten), FadeOut(cpu_lbl), FadeOut(allg), *[FadeOut(o) for o in outl], Transform(ph, T("MPI_Gather", 20, AMBER, MONO, BOLD).move_to(P(0, 2.55)))], 0.8)
        yield ([FadeIn(ga_arrows)], 0.6)
        yield ([bands[i].animate.move_to(P(ga_x, 0.8 - 0.8 * i)) for i in range(3)], 1.8)
        yield ([FadeOut(ga_arrows), FadeIn(T("root", 16, VIOLET, MONO, BOLD).move_to(P(ga_x, 1.55)))], 0.8)
    play_voiced(self, "05_09", steps())
    clear_stage(self)
