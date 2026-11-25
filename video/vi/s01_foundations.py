from manim import *
import numpy as np
from scene_utils import play_module_drills
from scene_utils import (
    setup_bg, make_header, make_trap_banner, clear_stage,
    play_voiced, make_grid_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, BORDER_DIM, SANS, MONO
)

BGC = "#0D1117"


def T(s, size=18, color=TEXT_MAIN, mono=False, bold=False, maxw=None):
    t = Text(s, font=MONO if mono else SANS, font_size=size, color=color,
             weight=BOLD if bold else NORMAL)
    if maxw and t.width > maxw:
        t.scale_to_fit_width(maxw)
    return t


def P(x, y):
    return np.array([x, y, 0.0])


def bx(w, h, color=CYAN, fill=PANEL_BG, sw=2.0, fo=1.0, r=0.08):
    return RoundedRectangle(width=w, height=h, corner_radius=min(r, h / 2.5), color=color,
                            fill_color=fill, fill_opacity=fo, stroke_width=sw)


def lbox(s, w, h, color, size=14, mono=True, tc=TEXT_MAIN, fill=PANEL_BG):
    r = bx(w, h, color, fill)
    t = T(s, size, tc, mono, maxw=w - 0.1)
    t.move_to(r)
    return VGroup(r, t)


def poly(*pts):
    m = VMobject()
    m.set_points_as_corners([P(*p) if len(p) == 2 else np.array(p) for p in pts])
    return m


def arr(a, b, color, sw=3, tip=0.13):
    a = P(*a) if len(a) == 2 else a
    b = P(*b) if len(b) == 2 else b
    return Arrow(a, b, buff=0, color=color, stroke_width=sw, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45)


def panel(cx, cy, w, h, color=BORDER_DIM):
    return bx(w, h, color, fill=PANEL_BG, sw=1.5, fo=0.35, r=0.15).move_to(P(cx, cy))


def rect_at(x, y, w, h, color, fo=0.6, sw=1.5):
    return Rectangle(width=w, height=h, color=color, fill_color=color, fill_opacity=fo,
                     stroke_width=sw).move_to(P(x + w / 2, y))


def dot(color, r=0.08):
    return Dot(radius=r, color=color)


class Scene01Foundations(Scene):
    def construct(self):
        setup_bg(self)
        self.s01()
        self.s02()
        self.s03()
        self.s04()
        self.s05()
        self.s06()
        self.s14()
        self.s15()
        self.s16()
        self.s07()
        self.s17()
        self.s11()
        self.s18()
        self.s19()
        self.s20()
        self.s21()
        play_module_drills(self, "M1", "Ch 1, 2")

    # ------------------------------------------------------------ 01_01
    def s01(self):
        title = T("Tính toán song song & HPC", 42, CYAN, bold=True).move_to(P(0, 2.7))
        sub = T("Ôn thi chuyên sâu", 20, TEXT_MUTED).next_to(title, DOWN, buff=0.12)

        def chip(cx, color, icon, big, small, bigsize=38):
            b = bx(3.5, 2.5, color, sw=2).move_to(P(cx, 0.3))
            icon.move_to(P(cx, 1.05))
            bt = T(big, bigsize, color, bold=True, maxw=3.1).move_to(P(cx, 0.25))
            st = T(small, 18, TEXT_MAIN, maxw=3.1).move_to(P(cx, -0.5))
            return VGroup(b, icon, bt, st)

        # icon 1: question list
        ic1 = VGroup(*[VGroup(Square(0.16, color=AMBER, stroke_width=2),
                              Line(LEFT * 0.1, RIGHT * 0.4, color=TEXT_MUTED, stroke_width=2).shift(RIGHT * 0.38))
                       for _ in range(3)]).arrange(DOWN, buff=0.1)
        ic1.scale(0.9)
        # icon 2: clock
        ic2 = VGroup(Circle(0.34, color=CYAN, stroke_width=3),
                     Line(ORIGIN, UP * 0.24, color=CYAN, stroke_width=3),
                     Line(ORIGIN, RIGHT * 0.17, color=CYAN, stroke_width=3))
        # icon 3: calculator
        keys = VGroup(*[Square(0.12, color=EMERALD, fill_opacity=0.8, stroke_width=0) for _ in range(6)]
                      ).arrange_in_grid(rows=2, cols=3, buff=0.08)
        scr = Rectangle(width=0.5, height=0.14, color=EMERALD, stroke_width=2)
        ic3 = VGroup(scr, keys).arrange(DOWN, buff=0.08)
        ic3 = VGroup(bx(0.7, 0.8, EMERALD, sw=2, r=0.06).move_to(ic3), ic3)

        c1 = chip(-4.1, AMBER, ic1, "40–60", "câu trắc nghiệm + 1–2 tự luận")
        c2 = chip(0, CYAN, ic2, "60–70", "phút")
        c3 = chip(4.1, EMERALD, ic3, "Đóng sách", "chỉ máy tính bỏ túi", 30)

        names = ["Nền tảng", "Threads + OpenMP", "MPI", "CUDA", "Luyện đề"]
        cols = [CYAN, AMBER, EMERALD, VIOLET, TEXT_MAIN]
        xs = np.linspace(-4.6, 4.6, 5)
        line = Line(P(-5.6, -2.1), P(5.6, -2.1), color=BORDER_DIM, stroke_width=3)
        nodes = VGroup(); labs = VGroup()
        for i, (n, c, x) in enumerate(zip(names, cols, xs)):
            d = Circle(0.24, color=c, fill_color=PANEL_BG, fill_opacity=1, stroke_width=3).move_to(P(x, -2.1))
            num = T(str(i + 1), 16, c, bold=True).move_to(d)
            nodes.add(VGroup(d, num))
            labs.add(T(n, 18, TEXT_MAIN, maxw=2.1).move_to(P(x, -2.75)))
        token = Dot(radius=0.13, color=AMBER).move_to(P(xs[0], -2.1))

        steps = [
            ([FadeIn(title, shift=UP * 0.2), FadeIn(sub)], 1.2),
            ([FadeIn(c1, shift=UP * 0.2)], 2.2),
            ([FadeIn(c2, shift=UP * 0.2)], 2.2),
            ([FadeIn(c3, shift=UP * 0.2)], 2.2),
            ([Create(line), FadeIn(nodes), FadeIn(labs), FadeIn(token)], 1.5),
        ]
        for i in range(1, 5):
            steps.append(([token.animate.move_to(P(xs[i], -2.1)),
                           nodes[i][0].animate.set_fill(cols[i], opacity=0.35)], 1.3))
        play_voiced(self, "01_01", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_02
    def s02(self):
        hdr = make_header("Vì sao tăng tốc tuần tự dừng lại", "Chương 1", CYAN)
        cxs = [-4.4, 0.0, 4.4]
        pans = VGroup(*[panel(c, 0.0, 4.1, 4.8) for c in cxs])
        titles = VGroup(*[T(s, 22, col, bold=True).move_to(P(c, 2.05)) for s, col, c in
                          zip(["1. Tín hiệu", "2. Thu nhỏ", "3. Kinh tế"], [CYAN, VIOLET, CORAL], cxs)])

        # panel 1: chip + race
        cx = cxs[0]
        chip = VGroup(bx(1.3, 1.1, TEXT_MUTED, sw=2).move_to(P(cx, 1.05)),
                      VGroup(*[Square(0.2, color=TEXT_MUTED, stroke_width=1.5) for _ in range(9)]
                             ).arrange_in_grid(3, 3, buff=0.08).move_to(P(cx, 1.05)))
        y1, y2 = 0.0, -0.95
        l_light = Line(P(cx - 1.6, y1), P(cx + 1.6, y1), color=CYAN, stroke_width=2)
        l_cu = Line(P(cx - 1.6, y2), P(cx + 1.6, y2), color=AMBER, stroke_width=2)
        t_light = T("ánh sáng 30 cm/ns", 14, CYAN).next_to(l_light, UP, buff=0.08)
        t_cu = T("dây đồng 9 cm/ns", 14, AMBER).next_to(l_cu, UP, buff=0.08)
        d_light = dot(CYAN, 0.12).move_to(l_light.get_start())
        d_cu = dot(AMBER, 0.12).move_to(l_cu.get_start())
        t_note = T("chip phải nhỏ lại", 16, TEXT_MAIN).move_to(P(cx, -1.9))

        # panel 2: atoms
        cx2 = cxs[1]

        def tr(size, n):
            sq = Square(size, color=VIOLET, stroke_width=3, fill_color=BGC, fill_opacity=1)
            step = size / n
            atoms = VGroup(*[Dot(radius=0.06, color=VIOLET) for _ in range(n * n)]).arrange_in_grid(
                n, n, buff=step - 0.12)
            atoms.move_to(sq)
            return VGroup(sq, atoms).move_to(P(cx2, 0.5))
        s_a, s_b, s_c = tr(2.0, 6), tr(1.0, 3), tr(0.4, 1)
        t_a = T("transistor", 16, TEXT_MUTED).move_to(P(cx2, -1.0))
        t_q = T("vài nguyên tử!", 20, VIOLET, bold=True).move_to(P(cx2, -1.7))

        # panel 3: economics
        cx3 = cxs[2]
        big = Rectangle(width=1.2, height=2.3, color=CORAL, fill_color=CORAL, fill_opacity=0.6,
                        stroke_width=2).move_to(P(cx3 - 0.95, -0.15))
        bigt = T("$$$$", 20, TEXT_MAIN, mono=True, bold=True).move_to(big)
        bigl = T("1 CPU nhanh hơn", 13, CORAL, maxw=1.6).move_to(P(cx3 - 0.95, -1.5))
        smalls = VGroup(*[Rectangle(width=0.36, height=0.75, color=AMBER, fill_color=AMBER, fill_opacity=0.6,
                                    stroke_width=2).move_to(P(cx3 + 0.3 + 0.44 * i, -0.15 - 1.15 + 0.375))
                          for i in range(4)])
        smallt = T("$", 22, TEXT_MAIN, mono=True, bold=True).move_to(P(cx3 + 0.96, -0.2))
        smalll = T("nhiều CPU vừa", 13, AMBER, maxw=1.8).move_to(P(cx3 + 1.1, -1.5))
        warn = T("rẻ hơn mà nhanh bằng", 16, EMERALD, maxw=3.7).move_to(P(cx3, -2.0))

        steps = [
            ([FadeIn(hdr), FadeIn(pans), FadeIn(titles)], 1.0),
            ([FadeIn(chip), Create(l_light), Create(l_cu), FadeIn(t_light), FadeIn(t_cu),
              FadeIn(d_light), FadeIn(d_cu)], 1.5),
            ([AnimationGroup(d_light.animate(run_time=0.8, rate_func=linear).move_to(l_light.get_end()),
                             d_cu.animate(run_time=2.7, rate_func=linear).move_to(l_cu.get_end()))], 2.8),
            ([FadeIn(t_note)], 0.8),
            ([FadeIn(s_a)], 1.2),
            ([ReplacementTransform(s_a, s_b), FadeIn(t_a)], 1.8),
            ([ReplacementTransform(s_b, s_c), FadeIn(t_q)], 1.8),
            ([GrowFromEdge(big, DOWN), FadeIn(bigt), FadeIn(bigl)], 1.6),
            ([LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in smalls], lag_ratio=0.2), FadeIn(smallt), FadeIn(smalll)], 2.0),
            ([FadeIn(warn)], 1.0),
        ]
        play_voiced(self, "01_02", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_03
    def flynn_cell(self, kind, cx, cy, color, name, sub):
        pan = panel(cx, cy, 6.2, 2.75, color)
        title = T(name, 22, color, bold=True).move_to(P(cx - 2.75, cy + 1.05), aligned_edge=LEFT)
        subt = T(sub, 14, TEXT_MUTED).move_to(P(cx + 2.9, cy + 1.05), aligned_edge=RIGHT)
        xs = [0.0] if kind == "SISD" else [-1.6, 0.0, 1.6]
        cores = VGroup(*[lbox("CPU", 0.8, 0.6, color, 13) for _ in xs])
        for c, x in zip(cores, xs):
            c.move_to(P(cx + x, cy - 0.1))
        top, bot = cy + 0.2, cy - 0.4
        grp = VGroup(pan, title, subt, cores)
        idots, ddots, ianims, danims = [], [], [], []
        def add_i(x_from, y_from, x, ):
            pass
        if kind == "SISD":
            a = arr((cx, cy + 0.75), (cx, top), AMBER); b = arr((cx, cy - 1.15), (cx, bot), CYAN)
            grp.add(a, b)
            idots.append((dot(AMBER), poly((cx, cy + 0.75), (cx, top))))
            ddots.append((dot(CYAN), poly((cx, cy - 1.15), (cx, bot))))
        elif kind == "SIMD":
            bus = Line(P(cx - 2.1, cy + 0.65), P(cx + 1.6, cy + 0.65), color=AMBER, stroke_width=3)
            src = lbox("lệnh", 0.75, 0.36, AMBER, 12, mono=False).move_to(P(cx - 2.5, cy + 0.65))
            grp.add(bus, src)
            for x in xs:
                grp.add(arr((cx + x, cy + 0.65), (cx + x, top), AMBER),
                        arr((cx + x, cy - 1.15), (cx + x, bot), CYAN))
                idots.append((dot(AMBER), poly((cx - 2.1, cy + 0.65), (cx + x, cy + 0.65), (cx + x, top))))
                ddots.append((dot(CYAN), poly((cx + x, cy - 1.15), (cx + x, bot))))
        elif kind == "MISD":
            for x in xs:
                grp.add(arr((cx + x, cy + 0.75), (cx + x, top), AMBER))
                idots.append((dot(AMBER), poly((cx + x, cy + 0.75), (cx + x, top))))
            y = cy - 0.1
            seg = [(-2.8, -1.6 - 0.4), (-1.6 + 0.4, -0.4), (0.4, 1.6 - 0.4), (1.6 + 0.4, 2.8)]
            for a_, b_ in seg:
                grp.add(arr((cx + a_, y), (cx + b_, y), CYAN))
            ddots.append((dot(CYAN), poly((cx - 2.8, y), (cx + 2.8, y))))
        else:
            for x in xs:
                grp.add(arr((cx + x, cy + 0.75), (cx + x, top), AMBER),
                        arr((cx + x, cy - 1.15), (cx + x, bot), CYAN))
                idots.append((dot(AMBER), poly((cx + x, cy + 0.75), (cx + x, top))))
                ddots.append((dot(CYAN), poly((cx + x, cy - 1.15), (cx + x, bot))))
        allp = idots + ddots
        for d, p in allp:
            d.move_to(p.get_start())
        dots = VGroup(*[d for d, p in allp])
        def pulse():
            return [AnimationGroup(*[MoveAlongPath(d, p) for d, p in allp])]
        return grp, dots, pulse

    def s03(self):
        hdr = make_header("Phân loại Flynn (1966)", "Chương 1", CYAN)
        specs = [("SISD", -3.3, 1.15, TEXT_MUTED, "1 lệnh · 1 dữ liệu"),
                 ("SIMD", 3.3, 1.15, CYAN, "1 lệnh · nhiều dữ liệu"),
                 ("MISD", -3.3, -1.75, VIOLET, "nhiều lệnh · 1 dữ liệu"),
                 ("MIMD", 3.3, -1.75, EMERALD, "nhiều lệnh · nhiều dữ liệu")]
        leg = VGroup(Line(ORIGIN, RIGHT * 0.5, color=AMBER, stroke_width=4), T("luồng lệnh", 14, AMBER),
                     Line(ORIGIN, RIGHT * 0.5, color=CYAN, stroke_width=4), T("luồng dữ liệu", 14, CYAN)
                     ).arrange(RIGHT, buff=0.15).move_to(P(0, -3.4))
        steps = [([FadeIn(hdr), FadeIn(leg)], 0.8)]
        for k, cx, cy, col, sub in specs:
            g, dots, pulse = self.flynn_cell(k, cx, cy, col, k, sub)
            steps.append(([FadeIn(g), FadeIn(dots)], 1.2))
            steps.append((pulse(), 1.8))
            steps.append(([FadeOut(dots)], 0.3))
        play_voiced(self, "01_03", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_04
    def s04(self):
        hdr = make_header("Kiến trúc bộ nhớ", "Chương 1", AMBER)
        cxs = [-4.35, 0.0, 4.35]
        pans = VGroup(*[panel(c, 0.0, 4.1, 5.0) for c in cxs])
        cols = [CYAN, AMBER, EMERALD]
        titles = VGroup(*[T(s, 22, col, bold=True).move_to(P(c, 2.2)) for s, col, c in
                          zip(["UMA (SMP)", "CC-NUMA", "Phân tán"], cols, cxs)])
        subs = VGroup(*[T(s, 14, TEXT_MUTED).move_to(P(c, 1.88)) for s, c in
                        zip(["chục CPU", "trăm CPU", "nghìn CPU"], cxs)])

        def cpu(x, y, s=0.5, col=TEXT_MAIN, lab=""):
            return lbox(lab, s, s, col, 11)

        # UMA
        c = cxs[0]
        ucp = VGroup(*[cpu(c + x, 1.25, 0.6, CYAN, "CPU") for x in (-1.35, -0.45, 0.45, 1.35)])
        for g, x in zip(ucp, (-1.35, -0.45, 0.45, 1.35)):
            g.move_to(P(c + x, 1.25))
        bus = Line(P(c - 1.7, 0.3), P(c + 1.7, 0.3), color=AMBER, stroke_width=6)
        stubs = VGroup(*[Line(P(c + x, 0.95), P(c + x, 0.3), color=AMBER, stroke_width=2) for x in (-1.35, -0.45, 0.45, 1.35)])
        ram = lbox("RAM", 2.2, 0.6, CYAN, 15).move_to(P(c, -0.9))
        rs = Line(P(c, 0.3), P(c, -0.6), color=AMBER, stroke_width=2)
        bl = T("1 bus", 13, AMBER).move_to(P(c - 1.45, 0.08))
        ul = T("truy cập đều", 16, EMERALD).move_to(P(c, -1.8))
        uma = VGroup(ucp, bus, stubs, ram, rs, bl, ul)
        udots = [(dot(AMBER), poly((c + x, 0.95), (c + x, 0.3), (c, 0.3), (c, -0.6))) for x in (-1.35, -0.45, 0.45, 1.35)]
        for d, p in udots: d.move_to(p.get_start())

        # NUMA
        c = cxs[1]
        numa = VGroup()
        xa, xb = c - 1.1, c + 1.1
        for xc, nm in ((xa, "SMP 1"), (xb, "SMP 2")):
            numa.add(bx(1.5, 2.8, AMBER, sw=1.5, fo=0.0, r=0.1).move_to(P(xc, 0.2)))
            for dx in (-0.35, 0.35):
                numa.add(cpu(xc + dx, 1.15, 0.45, AMBER, "").move_to(P(xc + dx, 1.15)))
                numa.add(Line(P(xc + dx, 0.925), P(xc + dx, -0.25), color=TEXT_MUTED, stroke_width=2))
            numa.add(lbox("RAM", 1.2, 0.5, AMBER, 13).move_to(P(xc, -0.5)))
            numa.add(T(nm, 12, TEXT_MUTED).move_to(P(xc, -0.97)))
        link = Line(P(xa + 0.35, 0.3), P(xb - 0.35, 0.3), color=VIOLET, stroke_width=6)
        link_t = T("link", 12, VIOLET).move_to(P(c, 0.5))
        near = T("gần = nhanh", 15, EMERALD).move_to(P(c, -1.65))
        far = T("xa = chậm", 15, CORAL).move_to(P(c, -2.0))
        loc = (dot(EMERALD), poly((xa - 0.35, 0.925), (xa - 0.35, -0.25)))
        rem = (dot(CORAL), poly((xa + 0.35, 0.925), (xa + 0.35, 0.3), (xb - 0.35, 0.3), (xb - 0.35, -0.25)))
        for d, p in (loc, rem): d.move_to(p.get_start())

        # distributed
        c = cxs[2]
        dist = VGroup()
        nx = [c - 1.25, c, c + 1.25]
        for x in nx:
            dist.add(bx(1.1, 1.4, EMERALD, sw=1.5, fo=0.0, r=0.1).move_to(P(x, 0.85)))
            dist.add(cpu(x, 1.15, 0.4, EMERALD, "").move_to(P(x, 1.15)))
            dist.add(lbox("RAM", 0.85, 0.35, EMERALD, 11).move_to(P(x, 0.6)))
            dist.add(Line(P(x, 0.15), P(x, -0.5), color=EMERALD, stroke_width=2))
        net = Line(P(nx[0], -0.5), P(nx[2], -0.5), color=EMERALD, stroke_width=6)
        net_t = T("mạng", 13, EMERALD).move_to(P(c, -0.8))
        dl = T("RAM riêng + MPI", 16, TEXT_MAIN).move_to(P(c, -1.8))
        dist.add(net, net_t, dl)
        pk = (dot(AMBER, 0.11), poly((nx[0], 0.15), (nx[0], -0.5), (nx[2], -0.5), (nx[2], 0.15)))
        pk[0].move_to(pk[1].get_start())

        ban = make_trap_banner("Siêu máy tính thật: lai SMP + MPI")
        steps = [
            ([FadeIn(hdr), FadeIn(pans), FadeIn(titles), FadeIn(subs)], 1.0),
            ([FadeIn(uma), *[FadeIn(d) for d, p in udots]], 1.6),
            ([AnimationGroup(*[MoveAlongPath(d, p) for d, p in udots], lag_ratio=0.0)], 2.2),
            ([FadeOut(VGroup(*[d for d, p in udots]))], 0.3),
            ([FadeIn(numa), FadeIn(link), FadeIn(link_t), FadeIn(loc[0]), FadeIn(rem[0])], 1.6),
            ([MoveAlongPath(loc[0], loc[1]), FadeIn(near)], 0.8),
            ([MoveAlongPath(rem[0], rem[1]), FadeIn(far)], 2.6),
            ([FadeIn(dist), FadeIn(pk[0])], 1.6),
            ([MoveAlongPath(pk[0], pk[1])], 2.4),
            ([FadeIn(ban)], 1.0),
        ]
        play_voiced(self, "01_04", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_05
    def s05(self):
        hdr = make_header("Speedup quan sát & overhead", "Chương 1", EMERALD)
        sc, x0 = 0.045, -5.3
        ser = rect_at(x0, 2.0, 120 * sc, 0.5, CYAN, 0.55)
        ser_t = T("Ts = 120 s", 18, TEXT_MAIN, bold=True).move_to(ser)
        ser_l = T("1 CPU", 14, TEXT_MUTED).move_to(P(x0 - 0.45, 2.0))
        work, ovh = VGroup(), VGroup()
        for i in range(8):
            y = 1.0 - i * 0.29
            work.add(rect_at(x0, y, 15 * sc, 0.24, CYAN, 0.6, 1))
            ovh.add(rect_at(x0 + 15 * sc, y, 5 * sc, 0.24, CORAL, 0.9, 1))
        par_l = T("8 CPU", 14, TEXT_MUTED).move_to(P(x0 - 0.45, 0.0))
        tp_line = DashedLine(P(x0 + 20 * sc, 2.3), P(x0 + 20 * sc, -1.2), color=AMBER, stroke_width=2)
        tp_t = T("Tp = 20 s", 16, AMBER, bold=True).move_to(P(x0 + 20 * sc + 0.12, 1.45), aligned_edge=LEFT)
        ideal = T("lý tưởng: 120 / 8 = 15 s", 18, TEXT_MAIN, maxw=3.6).move_to(P(-3.4, -1.75))
        rx = 1.1
        r1 = T("S = Ts / Tp = 6×", 26, EMERALD, bold=True, maxw=3.4).move_to(P(rx, 2.0), aligned_edge=LEFT)
        cells = VGroup(*[Square(0.22, color=EMERALD, stroke_width=2, fill_opacity=0) for _ in range(8)]
                       ).arrange(RIGHT, buff=0.1).move_to(P(rx + 1.2, 1.35))
        r2 = T("lý tưởng: 8×", 26, AMBER, bold=True, maxw=3.2).move_to(P(rx, 0.3), aligned_edge=LEFT)
        r3 = T("overhead 5 s: khởi tạo · đồng bộ · truyền", 18, CORAL, bold=True, maxw=5.4).move_to(P(rx, -1.2), aligned_edge=LEFT)
        steps = [
            ([FadeIn(hdr)], 0.4),
            ([GrowFromEdge(ser, LEFT), FadeIn(ser_t), FadeIn(ser_l)], 2.0),
            ([LaggedStart(*[GrowFromEdge(w, LEFT) for w in work], lag_ratio=0.1), FadeIn(par_l)], 2.2),
            ([FadeIn(ovh), Create(tp_line), FadeIn(tp_t)], 1.6),
            ([FadeIn(r1)], 1.0),
            ([FadeIn(cells)], 0.8),
            ([LaggedStart(*[c.animate.set_fill(EMERALD, opacity=0.9) for c in cells[:6]], lag_ratio=0.3)], 2.2),
            ([FadeIn(r2), FadeIn(ideal)], 2.0),
            ([FadeIn(r3), Indicate(ovh, color=CORAL, scale_factor=1.15)], 2.4),
        ]
        play_voiced(self, "01_05", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_06
    def s06(self):
        hdr = make_header("Định luật Amdahl", "Chương 1", AMBER)
        x0, W = -4.9, 6.0
        lA = T("N = 1", 16, TEXT_MUTED).move_to(P(x0 - 0.7, 2.15))
        lB = T("N = 17", 16, TEXT_MUTED).move_to(P(x0 - 0.7, 1.25))
        sA = rect_at(x0, 2.15, 0.9, 0.55, CORAL, 0.7)
        pA = rect_at(x0 + 0.9, 2.15, 5.1, 0.55, CYAN, 0.55)
        slices = VGroup(*[Line(P(x0 + 0.9 + 5.1 * k / 17, 1.9), P(x0 + 0.9 + 5.1 * k / 17, 2.4), color=BGC, stroke_width=1.5)
                          for k in range(1, 17)])
        slices.set_z_index(1)
        tsA = T("0.15", 15, TEXT_MAIN, bold=True, maxw=0.8).move_to(sA)
        tpA = T("0.85", 18, TEXT_MAIN, bold=True).move_to(pA).set_z_index(5)
        sB = rect_at(x0, 1.25, 0.9, 0.55, CORAL, 0.7)
        pB = rect_at(x0 + 0.9, 1.25, 0.3, 0.55, CYAN, 0.55)
        tsB = T("0.15", 15, TEXT_MAIN, bold=True, maxw=0.8).move_to(sB)
        tpB = T("0.85 / 17 = 0.05", 16, CYAN).move_to(P(x0 + 1.35, 1.25), aligned_edge=LEFT)
        res = T("S = 1 / 0.20 = 5×", 30, EMERALD, bold=True, maxw=3.8).move_to(P(4.3, 1.95))
        # graph
        ax = Axes(x_range=[0, 64, 16], y_range=[0, 10, 2], x_length=8.6, y_length=2.3,
                  axis_config={"color": TEXT_MUTED, "stroke_width": 2, "include_ticks": True,
                               "tick_size": 0.05}).move_to(P(0.2, -1.75))
        xt = VGroup(*[T(str(v), 12, TEXT_MUTED).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (16, 32, 48, 64)])
        yt = VGroup(*[T(str(v), 12, TEXT_MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v in (2, 4, 6, 8, 10)])
        xl = T("N (số CPU)", 14, TEXT_MUTED).move_to(P(0.2, -3.28))
        yl = T("S", 14, TEXT_MUTED).next_to(ax.y_axis.get_end(), UP, buff=0.05)
        f = lambda p: (lambda n: 1.0 / (p / n + (1 - p)))
        c85 = ax.plot(f(0.85), x_range=[1, 64], color=EMERALD, stroke_width=4)
        c90 = ax.plot(f(0.90), x_range=[1, 64], color=CYAN, stroke_width=3)
        a85 = DashedLine(ax.c2p(0, 6.67), ax.c2p(64, 6.67), color=EMERALD, stroke_width=1.5)
        a90 = DashedLine(ax.c2p(0, 10), ax.c2p(64, 10), color=CYAN, stroke_width=1.5)
        t85 = T("P = 0.85 → 6.67×", 14, EMERALD).next_to(ax.c2p(64, 6.67), UP, buff=0.05).shift(LEFT * 1.2)
        t90 = T("P = 0.90 → 10×", 14, CYAN).next_to(ax.c2p(64, 10), DOWN, buff=0.05).shift(LEFT * 1.0)
        pt = dot(AMBER, 0.11).move_to(ax.c2p(17, 5.0))
        hl = DashedLine(ax.c2p(0, 5), ax.c2p(17, 5), color=AMBER, stroke_width=2)
        vl = DashedLine(ax.c2p(17, 0), ax.c2p(17, 5), color=AMBER, stroke_width=2)
        t5 = T("5×", 16, AMBER, bold=True).next_to(pt, DOWN, buff=0.12).shift(RIGHT * 0.15)
        steps = [
            ([FadeIn(hdr), FadeIn(lA), GrowFromEdge(sA, LEFT), GrowFromEdge(pA, LEFT), FadeIn(tsA), FadeIn(tpA)], 2.0),
            ([Create(slices)], 1.2),
            ([FadeIn(lB), TransformFromCopy(sA, sB), TransformFromCopy(pA, pB), FadeIn(tsB)], 2.4),
            ([FadeIn(tpB)], 1.4),
            ([FadeIn(res, shift=UP * 0.1)], 1.6),
            ([Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl)], 1.5),
            ([Create(c85)], 2.4),
            ([FadeIn(pt), Create(hl), Create(vl), FadeIn(t5)], 1.6),
            ([Create(a85), FadeIn(t85)], 1.2),
            ([Create(c90), Create(a90), FadeIn(t90)], 1.8),
        ]
        play_voiced(self, "01_06", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_07
    def s07(self):
        hdr = make_header("Mô hình PRAM", "Chương 2", VIOLET)
        cxs = [-4.4, 0.0, 4.4]
        names = [("EREW", "đọc riêng · ghi riêng", CYAN), ("CREW", "đọc chung · ghi riêng", AMBER),
                 ("CRCW", "đọc chung · ghi chung", EMERALD)]
        pans = VGroup(*[panel(c, 0.2, 4.1, 4.7) for c in cxs])
        heads = VGroup()
        procs, cells = [], []
        for c, (n, s, col) in zip(cxs, names):
            heads.add(T(n, 24, col, bold=True).move_to(P(c, 2.1)), T(s, 13, TEXT_MUTED).move_to(P(c, 1.78)))
            procs.append([VGroup(Circle(0.25, color=col, fill_color=PANEL_BG, fill_opacity=1, stroke_width=2.5),
                                 T(f"P{i + 1}", 13, TEXT_MAIN)).move_to(P(c + x, 1.0))
                          for i, x in enumerate((-1.2, 0, 1.2))])
            for p in procs[-1]:
                p[1].move_to(p[0])
            cells.append([VGroup(bx(0.6, 0.6, col, sw=2), T(str(v), 16, TEXT_MAIN, mono=True)).move_to(P(c + x, -0.5))
                          for v, x in zip((7, 3, 5), (-1.2, 0, 1.2))])
            for g in cells[-1]:
                g[1].move_to(g[0])
        base = VGroup(pans, heads, *[VGroup(*p) for p in procs], *[VGroup(*cl) for cl in cells])

        def rd(c, pi, ci, col=CYAN):
            return arr((c + (-1.2, 0, 1.2)[ci], -0.2), (c + (-1.2, 0, 1.2)[pi], 0.75), col)

        def wr(c, pi, ci, col=AMBER):
            return arr((c + (-1.2, 0, 1.2)[pi], 0.75), (c + (-1.2, 0, 1.2)[ci], -0.2), col)

        def stt(c, ok, txt):
            return VGroup(T("✓" if ok else "✗", 26, EMERALD if ok else CORAL, bold=True),
                          T(txt, 15, EMERALD if ok else CORAL)).arrange(RIGHT, buff=0.12).move_to(P(c, -1.55))

        # EREW
        e1 = VGroup(*[rd(cxs[0], i, i) for i in range(3)]); e1s = stt(cxs[0], True, "mỗi CPU một ô")
        e2 = VGroup(rd(cxs[0], 0, 1, CORAL), rd(cxs[0], 1, 1, CORAL)); e2s = stt(cxs[0], False, "cùng ô: cấm")
        # CREW
        r1 = VGroup(*[rd(cxs[1], i, 1) for i in range(3)]); r1s = stt(cxs[1], True, "đọc chung: được")
        r2 = VGroup(wr(cxs[1], 0, 1, CORAL), wr(cxs[1], 1, 1, CORAL)); r2s = stt(cxs[1], False, "ghi chung: cấm")
        # CRCW
        w1 = VGroup(*[wr(cxs[2], i, 1) for i in range(3)]); w1s = stt(cxs[2], True, "ghi chung: được")
        rule = T("ưu tiên · bằng nhau · tùy ý", 14, EMERALD, maxw=3.8).move_to(P(cxs[2], -2.0))
        hier = T("EREW ⊂ CREW ⊂ CRCW", 28, AMBER, mono=True, bold=True, maxw=8).move_to(P(0, -3.05))
        steps = [
            ([FadeIn(hdr), FadeIn(base)], 1.4),
            ([Create(e1), FadeIn(e1s)], 2.0),
            ([FadeOut(e1), FadeOut(e1s), Create(e2), FadeIn(e2s)], 2.0),
            ([Create(r1), FadeIn(r1s)], 2.0),
            ([FadeOut(r1), FadeOut(r1s), Create(r2), FadeIn(r2s)], 2.0),
            ([Create(w1), FadeIn(w1s), FadeIn(rule)], 2.2),
            ([FadeIn(hier)], 1.5),
        ]
        play_voiced(self, "01_07", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_11 (new)
    def s11(self):
        hdr = make_header("Rút gọn dạng cây: tổng 8 số", "Chương 2", VIOLET)
        vals = [[3, 1, 4, 1, 5, 9, 2, 6]]
        for _ in range(3):
            v = vals[-1]
            vals.append([v[2 * i] + v[2 * i + 1] for i in range(len(v) // 2)])
        ys = [1.9, 0.6, -0.7, -2.0]
        xs0 = [(i - 3.5) * 1.4 for i in range(8)]
        xl = [xs0]
        for _ in range(3):
            p = xl[-1]
            xl.append([(p[2 * i] + p[2 * i + 1]) / 2 for i in range(len(p) // 2)])
        cols = [CYAN, EMERALD, EMERALD, AMBER]
        lv = [VGroup(*[make_grid_box(str(v), w=0.8, h=0.6, color=cols[k], font_size=20).move_to(P(x, ys[k]))
                       for v, x in zip(vals[k], xl[k])]) for k in range(4)]
        edges = []
        for k in range(1, 4):
            es = VGroup()
            for j in range(len(vals[k])):
                for q in (2 * j, 2 * j + 1):
                    es.add(Line(lv[k - 1][q].get_bottom(), lv[k][j].get_top(), color=TEXT_MUTED, stroke_width=2))
            edges.append(es)
        left = [T(f"bước {k}", 15, TEXT_MUTED).move_to(P(-6.0, ys[k])) for k in (1, 2, 3)]
        right = [T(f"{n} CPU", 15, TEXT_MUTED, mono=True).move_to(P(6.0, ys[k])) for k, n in zip((1, 2, 3), (4, 2, 1))]
        take = T("7 phép cộng → 3 bước = log₂ 8", 24, AMBER, bold=True, maxw=9).move_to(P(0, -3.1))
        steps = [([FadeIn(hdr), LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in lv[0]], lag_ratio=0.15)], 2.0)]
        for k in (1, 2, 3):
            steps.append(([Create(edges[k - 1]), FadeIn(left[k - 1]), FadeIn(right[k - 1])], 1.2))
            steps.append(([LaggedStart(*[FadeIn(b, scale=0.5) for b in lv[k]], lag_ratio=0.2)], 1.6))
            if k < 3:
                steps.append(([Indicate(lv[k], color=AMBER, scale_factor=1.15)], 1.2))
        steps.append(([Indicate(lv[3], color=AMBER, scale_factor=1.4), FadeIn(take)], 2.0))
        play_voiced(self, "01_11", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_14 (new)
    def s14(self):
        hdr = make_header("Thuật ngữ nền tảng", "Chương 1", CYAN)
        cxs = [-4.4, 0.0, 4.4]
        pans = VGroup(*[panel(c, 0.0, 4.1, 4.8) for c in cxs])
        titles = VGroup(*[T(s, 21, col, bold=True).move_to(P(c, 2.05)) for s, col, c in
                          zip(["von Neumann", "Granularity", "Đồng bộ"], [CYAN, AMBER, CORAL], cxs)])
        # von Neumann
        c = cxs[0]
        mem = lbox("RAM: lệnh + dữ liệu", 3.3, 0.7, CYAN, 14, mono=False).move_to(P(c, 1.1))
        cpu = lbox("CPU", 1.6, 0.6, CYAN, 16).move_to(P(c, -0.6))
        a_dn = arr((c - 0.5, 0.72), (c - 0.5, -0.27), AMBER)
        a_up = arr((c + 0.5, -0.27), (c + 0.5, 0.72), EMERALD)
        vn = T("lấy lệnh, chạy tuần tự", 15, TEXT_MAIN, maxw=3.7).move_to(P(c, -1.6))
        d_f = dot(AMBER, 0.1).move_to(P(c - 0.5, 0.72))
        # granularity
        c = cxs[1]

        def gran(y, nblk, wc, wm):
            g = VGroup()
            x = c - 1.6
            for _ in range(nblk):
                g.add(rect_at(x, y, wc, 0.4, CYAN, 0.6))
                x += wc
                g.add(rect_at(x, y, wm, 0.4, CORAL, 0.95))
                x += wm
            return g
        coarse = gran(0.95, 2, 1.4, 0.2)
        fine = gran(-0.3, 8, 0.25, 0.15)
        cl = T("thô: tính nhiều, truyền ít", 14, TEXT_MAIN, maxw=3.6).move_to(P(c, 1.5))
        fl = T("mịn: tính ít, truyền nhiều", 14, TEXT_MAIN, maxw=3.6).move_to(P(c, 0.25))
        leg = VGroup(rect_at(0, 0, 0.3, 0.2, CYAN, 0.6), T("tính", 13, CYAN),
                     rect_at(0, 0, 0.3, 0.2, CORAL, 0.95), T("truyền", 13, CORAL)
                     ).arrange(RIGHT, buff=0.12).move_to(P(c, -0.95))
        gcap = T("tỷ lệ tính / truyền", 15, AMBER, bold=True).move_to(P(c, -1.7))
        # sync
        c = cxs[2]
        bxp = c - 1.7
        lens = [1.0, 2.0, 2.9]
        ys = [1.05, 0.3, -0.45]
        tasks = [rect_at(bxp, y, l, 0.4, CORAL if False else CYAN, 0.6) for y, l in zip(ys, lens)]
        waits = [rect_at(bxp + l, y, 2.9 - l, 0.4, CORAL, 0.5) for y, l in zip(ys, lens)]
        barrier = DashedLine(P(bxp + 2.9, 1.4), P(bxp + 2.9, -0.85), color=AMBER, stroke_width=3)
        sy = T("nhanh phải chờ chậm", 15, CORAL, maxw=3.7).move_to(P(c, -1.3))
        mp = T("massively parallel: ~6 chữ số CPU", 14, VIOLET, maxw=3.7).move_to(P(c, -1.9))
        steps = [
            ([FadeIn(hdr), FadeIn(pans), FadeIn(titles)], 1.0),
            ([FadeIn(mem), FadeIn(cpu), FadeIn(a_dn), FadeIn(a_up), FadeIn(d_f)], 1.4),
            ([MoveAlongPath(d_f, Line(P(cxs[0] - 0.5, 0.72), P(cxs[0] - 0.5, -0.27))), FadeIn(vn)], 1.6),
            ([FadeIn(cl), LaggedStart(*[GrowFromEdge(r, LEFT) for r in coarse], lag_ratio=0.3)], 1.8),
            ([FadeIn(fl), LaggedStart(*[GrowFromEdge(r, LEFT) for r in fine], lag_ratio=0.05)], 1.8),
            ([FadeIn(leg), FadeIn(gcap)], 1.0),
            ([AnimationGroup(*[GrowFromEdge(t, LEFT, run_time=l / 2.9 * 2.0, rate_func=linear)
                               for t, l in zip(tasks, lens)])], 2.2),
            ([Create(barrier), *[FadeIn(w) for w in waits]], 1.4),
            ([FadeIn(sy)], 1.0),
            ([FadeIn(mp)], 1.2),
        ]
        play_voiced(self, "01_14", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_15 (new)
    def s15(self):
        hdr = make_header("Bốn mô hình lập trình song song", "Chương 2", AMBER)
        cxs = [-4.95, -1.65, 1.65, 4.95]
        cols = [CYAN, AMBER, EMERALD, VIOLET]
        pans = VGroup(*[panel(c, -0.15, 3.15, 4.7) for c in cxs])
        names = ["Shared memory", "Threads", "Message passing", "Data parallel"]
        subs = ["khóa / semaphore", "POSIX · OpenMP", "send ↔ recv · MPI", "cùng phép toán"]
        titles = VGroup(*[T(n, 17, col, bold=True, maxw=2.9).move_to(P(c, 1.85)) for n, col, c in zip(names, cols, cxs)])
        stl = VGroup(*[T(s, 13, TEXT_MUTED, maxw=2.9).move_to(P(c, 1.5)) for s, c in zip(subs, cxs)])
        # 1 shared memory
        c = cxs[0]
        tk = VGroup(*[VGroup(Circle(0.22, color=CYAN, fill_color=PANEL_BG, fill_opacity=1, stroke_width=2.5),
                             T("T" + str(i + 1), 12)).move_to(P(c + x, 0.7)) for i, x in enumerate((-0.9, 0, 0.9))])
        for g in tk:
            g[1].move_to(g[0])
        mem = lbox("địa chỉ chung", 2.5, 0.55, CYAN, 13, mono=False).move_to(P(c, -0.6))
        sm_a = VGroup(*[arr((c + x, 0.45), (c + x, -0.3), CYAN) for x in (-0.9, 0, 0.9)])
        sm_t = T("không cần gửi dữ liệu", 13, TEXT_MAIN, maxw=2.9).move_to(P(c, -1.35))
        sm_d = [dot(AMBER, 0.07).move_to(P(c + x, 0.45)) for x in (-0.9, 0, 0.9)]
        # 2 threads
        c = cxs[1]
        mainb = lbox("a.out", 1.3, 0.45, AMBER, 13).move_to(P(c, 0.9))
        ths = VGroup(*[lbox("luồng", 0.8, 0.4, AMBER, 11, mono=False).move_to(P(c + x, -0.1)) for x in (-0.95, 0, 0.95)])
        fl = VGroup(*[Line(mainb.get_bottom(), t_.get_top(), color=AMBER, stroke_width=2) for t_ in ths])
        gm = lbox("bộ nhớ chung", 2.7, 0.45, AMBER, 12, mono=False).move_to(P(c, -0.95))
        tl = VGroup(*[Line(t_.get_bottom(), P(t_.get_center()[0], -0.72), color=TEXT_MUTED, stroke_width=2) for t_ in ths])
        th_t = T("tạo luồng từ a.out", 13, TEXT_MAIN, maxw=2.9).move_to(P(c, -1.55))
        # 3 message passing
        c = cxs[2]
        n1 = VGroup(bx(1.1, 1.5, EMERALD, sw=2, fo=0.0), T("RAM", 12)).move_to(P(c - 0.85, 0.2))
        n2 = VGroup(bx(1.1, 1.5, EMERALD, sw=2, fo=0.0), T("RAM", 12)).move_to(P(c + 0.85, 0.2))
        for g in (n1, n2):
            g[1].move_to(g[0].get_center() + DOWN * 0.45)
        sm = arr((c - 0.85, 0.45), (c + 0.85, 0.45), AMBER)
        stx = T("send", 13, AMBER).move_to(P(c - 0.85, 0.75))
        rtx = T("recv", 13, EMERALD).move_to(P(c + 0.85, 0.75))
        mp_t = T("send phải có recv", 13, TEXT_MAIN, maxw=2.9).move_to(P(c, -1.1))
        mp_d = dot(AMBER, 0.09).move_to(P(c - 0.85, 0.45))
        # 4 data parallel
        c = cxs[3]
        vals = [1, 2, 3, 4, 5, 6]
        arrc = VGroup(*[make_grid_box(str(v), w=0.42, h=0.5, color=VIOLET, font_size=14).move_to(P(c - 1.05 + 0.42 * i + (0.12 if i > 2 else -0.12), 0.5))
                        for i, v in enumerate(vals)])
        newc = VGroup(*[make_grid_box(str(v + 4), w=0.42, h=0.5, color=VIOLET, font_size=14).move_to(arrc[i]) for i, v in enumerate(vals)])
        ch1 = T("tác vụ 1", 12, TEXT_MUTED).move_to(P(c - 0.55, -0.1))
        ch2 = T("tác vụ 2", 12, TEXT_MUTED).move_to(P(c + 0.55, -0.1))
        dp_t = T("mỗi phần: cộng 4", 13, TEXT_MAIN, maxw=2.9).move_to(P(c, -0.85))
        ban = T("không có mô hình tốt nhất", 20, CORAL, bold=True).move_to(P(0, -3.0))
        steps = [
            ([FadeIn(hdr), FadeIn(pans), FadeIn(titles), FadeIn(stl)], 1.2),
            ([FadeIn(tk), FadeIn(mem), Create(sm_a), *[FadeIn(d) for d in sm_d]], 1.4),
            ([AnimationGroup(*[MoveAlongPath(d, Line(P(cxs[0] + x, 0.45), P(cxs[0] + x, -0.3)))
                               for d, x in zip(sm_d, (-0.9, 0, 0.9))]), FadeIn(sm_t)], 1.6),
            ([FadeIn(mainb), Create(fl), FadeIn(ths)], 1.4),
            ([FadeIn(gm), Create(tl), FadeIn(th_t)], 1.4),
            ([FadeIn(n1), FadeIn(n2), FadeIn(stx), FadeIn(rtx), Create(sm), FadeIn(mp_d)], 1.4),
            ([MoveAlongPath(mp_d, Line(P(cxs[2] - 0.85, 0.45), P(cxs[2] + 0.85, 0.45))), FadeIn(mp_t)], 1.6),
            ([FadeIn(arrc), FadeIn(ch1), FadeIn(ch2)], 1.2),
            ([*[ReplacementTransform(a_, b_) for a_, b_ in zip(arrc, newc)], FadeIn(dp_t)], 1.8),
            ([FadeIn(ban)], 1.0),
        ]
        play_voiced(self, "01_15", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_16 (new)
    def s16(self):
        hdr = make_header("SPMD · MPMD · Hybrid", "Chương 2", VIOLET)
        cxs = [-4.4, 0.0, 4.4]
        cols = [CYAN, AMBER, EMERALD]
        pans = VGroup(*[panel(c, -0.15, 4.1, 4.7) for c in cxs])
        titles = VGroup(*[T(n, 22, col, bold=True).move_to(P(c, 1.95)) for n, col, c in zip(["SPMD", "MPMD", "Hybrid"], cols, cxs)])
        xs4 = (-1.35, -0.45, 0.45, 1.35)
        # SPMD
        c = cxs[0]
        prog = lbox("1 chương trình", 2.0, 0.5, CYAN, 13, mono=False).move_to(P(c, 1.15))
        t4 = VGroup(*[lbox("T" + str(i), 0.72, 0.5, CYAN, 13).move_to(P(c + x, 0.0)) for i, x in enumerate(xs4)])
        sa = VGroup(*[Line(P(c, 0.9), t_.get_top(), color=CYAN, stroke_width=2) for t_ in t4])
        dd = VGroup(*[lbox("d" + str(i), 0.6, 0.4, TEXT_MUTED, 12).move_to(P(c + x, -0.9)) for i, x in enumerate(xs4)])
        cap1 = T("dữ liệu riêng, rẽ nhánh theo pid", 13, TEXT_MAIN, maxw=3.8).move_to(P(c, -1.7))
        # MPMD
        c = cxs[1]
        pa = lbox("a.out", 1.2, 0.5, AMBER, 13).move_to(P(c - 0.9, 1.15))
        pb = lbox("b.out", 1.2, 0.5, CORAL, 13).move_to(P(c + 0.9, 1.15))
        tb = VGroup(*[lbox("T" + str(i), 0.72, 0.5, AMBER if i < 2 else CORAL, 13).move_to(P(c + x, 0.0)) for i, x in enumerate(xs4)])
        ma = VGroup(*[Line((pa if i < 2 else pb).get_bottom(), t_.get_top(), color=AMBER if i < 2 else CORAL, stroke_width=2) for i, t_ in enumerate(tb)])
        cap2 = T("nhiều file thực thi", 13, TEXT_MAIN, maxw=3.8).move_to(P(c, -1.7))
        # Hybrid
        c = cxs[2]
        nodes = VGroup()
        for x in (-0.95, 0.95):
            nodes.add(bx(1.5, 1.6, EMERALD, sw=2, fo=0.0).move_to(P(c + x, 0.45)))
            for dx in (-0.3, 0.3):
                for dy in (0.35, 0.85):
                    nodes.add(lbox("", 0.4, 0.35, EMERALD, 10).move_to(P(c + x + dx, dy)))
            nodes.add(T("OpenMP", 12, EMERALD).move_to(P(c + x, -0.1)))
        link = DashedLine(P(c - 0.2, 0.45), P(c + 0.2, 0.45), color=VIOLET, stroke_width=4)
        ml = T("MPI", 15, VIOLET, bold=True).move_to(P(c, 1.55))
        cap3 = T("MPI giữa nút + OpenMP trong nút", 13, TEXT_MAIN, maxw=3.8).move_to(P(c, -1.7))
        d1 = dot(AMBER, 0.09).move_to(P(c - 0.75, 0.45))
        steps = [
            ([FadeIn(hdr), FadeIn(pans), FadeIn(titles)], 1.0),
            ([FadeIn(prog), Create(sa), FadeIn(t4)], 1.4),
            ([FadeIn(dd), FadeIn(cap1)], 1.4),
            ([Indicate(t4[0], color=AMBER), Indicate(t4[2], color=AMBER)], 1.4),
            ([FadeIn(pa), FadeIn(pb), Create(ma), FadeIn(tb)], 1.6),
            ([FadeIn(cap2)], 1.0),
            ([FadeIn(nodes), FadeIn(ml)], 1.4),
            ([Create(link), FadeIn(d1)], 0.6),
            ([MoveAlongPath(d1, Line(P(cxs[2] - 0.75, 0.45), P(cxs[2] + 0.75, 0.45))), FadeIn(cap3)], 1.8),
        ]
        play_voiced(self, "01_16", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_17 (new)
    def s17(self):
        hdr = make_header("Ghi chung trên CRCW & Boolean AND", "Chương 2", EMERALD)
        cl, cr = -3.3, 3.3
        pl = panel(cl, -0.1, 6.2, 5.3)
        pr = panel(cr, -0.1, 6.2, 5.3)
        tl = T("Ba CPU cùng ghi: 3, 3, 7", 20, EMERALD, bold=True, maxw=5.6).move_to(P(cl, 2.15))
        tr_ = T("Boolean AND", 20, CYAN, bold=True).move_to(P(cr, 2.15))
        pxs = (-1.8, 0, 1.8)
        vv = ("3", "3", "7")
        procs = VGroup(*[VGroup(Circle(0.27, color=EMERALD, fill_color=PANEL_BG, fill_opacity=1, stroke_width=2.5),
                                T("P" + str(i + 1), 13)).move_to(P(cl + x, 1.1)) for i, x in enumerate(pxs)])
        for g in procs:
            g[1].move_to(g[0])
        vals = VGroup(*[T(v, 18, AMBER, mono=True, bold=True).move_to(P(cl + x, 0.55)) for v, x in zip(vv, pxs)])
        cell = bx(1.5, 0.7, EMERALD, sw=2.5).move_to(P(cl, -0.7))
        arrs = VGroup(*[arr((cl + x, 0.35), (cl + x * 0.25, -0.35), AMBER) for x in pxs])
        rules = [("Priority: P1 thắng", "3", CYAN), ("Equality: 3 ≠ 7, không ghi", "–", CORAL),
                 ("Arbitrary: chọn bất kỳ", "3 hoặc 7", AMBER), ("Combining: tổng", "13", EMERALD)]

        def rule_grp(name, res, col):
            return VGroup(T(name, 17, col, bold=True, maxw=5.6).move_to(P(cl, -1.55)),
                          T(res, 22, col, mono=True, bold=True, maxw=1.3).move_to(cell))
        rgs = [rule_grp(*r) for r in rules]
        # right: AND
        flags = [True, True, False, True, False, True]
        fx = [cr - 2.0 + 0.8 * i for i in range(6)]
        cells = VGroup(*[VGroup(bx(0.65, 0.55, EMERALD if f else CORAL, sw=2),
                                T("T" if f else "F", 16, EMERALD if f else CORAL, mono=True, bold=True)).move_to(P(x, 1.1))
                         for f, x in zip(flags, fx)])
        for g in cells:
            g[1].move_to(g[0])
        res = VGroup(bx(1.8, 0.7, CYAN, sw=2.5), T("KQ = TRUE", 15, EMERALD, mono=True, bold=True)).move_to(P(cr, -0.7))
        res[1].move_to(res[0])
        fres = VGroup(bx(1.8, 0.7, CORAL, sw=2.5), T("KQ = FALSE", 15, CORAL, mono=True, bold=True)).move_to(P(cr, -0.7))
        fres[1].move_to(fres[0])
        wa = VGroup(*[arr((fx[i], 0.8), (cr + (fx[i] - cr) * 0.3, -0.3), CORAL) for i, f in enumerate(flags) if not f])
        o1 = T("CRCW: O(1)", 22, EMERALD, mono=True, bold=True).move_to(P(cr, -1.6))
        o2 = T("EREW: O(log n)", 22, AMBER, mono=True, bold=True).move_to(P(cr, -2.2))
        steps = [
            ([FadeIn(hdr), FadeIn(pl), FadeIn(pr), FadeIn(tl), FadeIn(tr_)], 1.0),
            ([FadeIn(procs), FadeIn(vals), FadeIn(cell), Create(arrs)], 1.6),
            ([FadeIn(rgs[0])], 1.6),
            ([FadeOut(rgs[0]), FadeIn(rgs[1])], 1.6),
            ([FadeOut(rgs[1]), FadeIn(rgs[2])], 1.6),
            ([FadeOut(rgs[2]), FadeIn(rgs[3])], 1.6),
            ([FadeIn(cells), FadeIn(res)], 1.4),
            ([Create(wa)], 1.0),
            ([FadeOut(res), FadeIn(fres)], 1.0),
            ([FadeIn(o1)], 1.0),
            ([FadeIn(o2)], 1.2),
        ]
        play_voiced(self, "01_17", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_18 (new)
    def s18(self):
        hdr = make_header("Broadcast: nhân đôi trên EREW", "Chương 2", AMBER)
        xs = [-4.9 + 1.4 * i for i in range(8)]
        y = 0.4
        procs = VGroup(*[VGroup(Circle(0.3, color=TEXT_MUTED, fill_color=PANEL_BG, fill_opacity=1, stroke_width=2.5),
                                T("P" + str(i + 1), 14)).move_to(P(x, y)) for i, x in enumerate(xs)])
        for g in procs:
            g[1].move_to(g[0])
        xb = [T("x", 18, AMBER, mono=True, bold=True).next_to(g, DOWN, buff=0.12) for g in procs]
        hold = [[0], [0, 1], [0, 1, 2, 3], list(range(8))]
        lbls = ["bước 1: 1 CPU có x", "bước 2: 2 CPU", "bước 3: 4 CPU", "bước 4: 8 CPU"]
        lab = [T(s, 22, AMBER, bold=True).move_to(P(0, -1.6)) for s in lbls]
        naive = T("tuần tự: O(n)", 18, CORAL, mono=True).move_to(P(-4.4, 2.3))
        fast = T("nhân đôi: O(log n)", 18, EMERALD, mono=True, bold=True).move_to(P(4.2, 2.3))

        def arcs(src_dst):
            g = VGroup()
            for s_, d_ in src_dst:
                g.add(CurvedArrow(procs[s_].get_top() + UP * 0.02, procs[d_].get_top() + UP * 0.02, angle=-1.0,
                                  color=AMBER, stroke_width=3, tip_length=0.15))
            return g
        a2 = arcs([(0, 1)])
        a3 = arcs([(0, 2), (1, 3)])
        a4 = arcs([(0, 4), (1, 5), (2, 6), (3, 7)])
        take = T("n CPU = log₂ n vòng nhân đôi", 24, AMBER, bold=True).move_to(P(0, -2.6))
        steps = [
            ([FadeIn(hdr), FadeIn(procs), FadeIn(naive)], 1.4),
            ([procs[0][0].animate.set_color(AMBER), FadeIn(xb[0]), FadeIn(lab[0])], 1.6),
            ([Create(a2), procs[1][0].animate.set_color(AMBER), FadeIn(xb[1]), FadeOut(lab[0]), FadeIn(lab[1])], 1.8),
            ([FadeOut(a2), Create(a3), *[procs[i][0].animate.set_color(AMBER) for i in (2, 3)], *[FadeIn(xb[i]) for i in (2, 3)],
              FadeOut(lab[1]), FadeIn(lab[2])], 1.8),
            ([FadeOut(a3), Create(a4), *[procs[i][0].animate.set_color(AMBER) for i in range(4, 8)], *[FadeIn(xb[i]) for i in range(4, 8)],
              FadeOut(lab[2]), FadeIn(lab[3])], 2.0),
            ([FadeIn(fast), FadeIn(take)], 1.6),
        ]
        play_voiced(self, "01_18", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_19 (new)
    def s19(self):
        hdr = make_header("Pointer jumping: xếp hạng danh sách", "Chương 2", CYAN)
        n = 8
        xs = [-4.5 + 1.3 * i for i in range(n)]
        ny, ry = -0.2, -1.1
        nodes = VGroup(*[lbox(str(i + 1), 0.8, 0.55, CYAN, 16).move_to(P(x, ny)) for i, x in enumerate(xs)])
        rl = T("RANK", 14, TEXT_MUTED).move_to(P(-6.0, ry))
        nl = T("NEXT", 14, TEXT_MUTED).move_to(P(-6.0, 0.6))
        # states
        rank = [1] * n
        nxt = [i + 1 if i + 1 < n else -1 for i in range(n)]
        states = [(list(rank), list(nxt))]
        for _ in range(3):
            r2 = list(rank)
            n2 = list(nxt)
            for i in range(n):
                if nxt[i] != -1:
                    r2[i] = rank[i] + rank[nxt[i]]
                    n2[i] = nxt[nxt[i]]
            rank, nxt = r2, n2
            states.append((list(rank), list(nxt)))

        def rank_row(rk):
            return VGroup(*[T(str(v), 22, AMBER, mono=True, bold=True).move_to(P(xs[i], ry)) for i, v in enumerate(rk)])

        def arc_row(nx):
            g = VGroup()
            for i, j in enumerate(nx):
                if j != -1:
                    g.add(CurvedArrow(nodes[i].get_top() + UP * 0.02, nodes[j].get_top() + UP * 0.02, angle=-1.1,
                                      color=EMERALD, stroke_width=3, tip_length=0.14))
            return g
        rrows = [rank_row(s[0]) for s in states]
        arows = [arc_row(s[1]) for s in states]
        vong = [T("khởi tạo: RANK = 1, nhảy 1", 20, TEXT_MAIN, bold=True),
                T("vòng 1: nhảy 2", 20, EMERALD, bold=True), T("vòng 2: nhảy 4", 20, EMERALD, bold=True),
                T("vòng 3: xong, RANK = khoảng cách tới cuối", 20, AMBER, bold=True, maxw=9)]
        for v in vong:
            v.move_to(P(0, -2.2))
        rule = T("RANK[i] += RANK[NEXT[i]];  NEXT[i] = NEXT[NEXT[i]]", 16, TEXT_MUTED, mono=True, maxw=10).move_to(P(0, 2.3))
        take = T("O(log n) · EREW · O(n) CPU  (tuần tự: O(n))", 18, EMERALD, mono=True, bold=True, maxw=10).move_to(P(0, -3.0))
        steps = [
            ([FadeIn(hdr), FadeIn(nodes), FadeIn(rl), FadeIn(nl), FadeIn(rrows[0]), FadeIn(arows[0]), FadeIn(vong[0])], 1.6),
            ([FadeIn(rule)], 1.4),
        ]
        for k in (1, 2, 3):
            steps.append(([FadeOut(arows[k - 1]), FadeOut(rrows[k - 1]), FadeIn(arows[k]), FadeIn(rrows[k]),
                           FadeOut(vong[k - 1]), FadeIn(vong[k])], 2.0))
        steps.append(([FadeIn(take)], 1.4))
        play_voiced(self, "01_19", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_20 (new)
    def s20(self):
        hdr = make_header("Partitioning: trộn hai mảng đã sắp", "Chương 2", EMERALD)
        c1, c2 = -3.4, 0.6
        cols = [CYAN, AMBER]
        A = [[1, 4], [7, 9]]
        B = [[2, 3], [5, 8]]
        C = [[1, 2, 3, 4], [5, 7, 8, 9]]
        pans = VGroup(*[panel(c, -0.2, 3.6, 5.0) for c in (c1, c2)])
        lab = VGroup(*[T(s, 20, TEXT_MUTED, bold=True).move_to(P(-5.9, y)) for s, y in (("A", 1.5), ("B", 0.4), ("C", -1.3))])
        pt = VGroup(*[T("P" + str(i + 1), 18, col, bold=True).move_to(P(c, 2.0)) for i, (c, col) in enumerate(zip((c1, c2), cols))])

        def row(cx, vals, y, col, step=0.8):
            k = len(vals)
            return VGroup(*[make_grid_box(str(v), w=0.65, h=0.55, color=col, font_size=18).move_to(P(cx + (i - (k - 1) / 2) * step, y))
                            for i, v in enumerate(vals)])
        arA = [row(c, A[g], 1.5, cols[g]) for g, c in enumerate((c1, c2))]
        arB = [row(c, B[g], 0.4, cols[g]) for g, c in enumerate((c1, c2))]
        arC = [row(c, C[g], -1.3, cols[g]) for g, c in enumerate((c1, c2))]
        r1 = T("r = n / log n nhóm", 18, TEXT_MAIN, maxw=3.4).move_to(P(4.6, 1.8))
        r2 = T("mỗi P: tìm nhị phân j[i]", 16, CYAN, maxw=3.4).move_to(P(4.6, 0.8))
        r3 = T("rồi trộn NA[i] với NB[i]", 16, EMERALD, maxw=3.4).move_to(P(4.6, 0.1))
        r4 = T("mỗi bước O(log n)", 18, AMBER, bold=True, maxw=3.4).move_to(P(4.6, -0.9))
        r5 = T("tuần tự (3 con trỏ): O(n)", 16, CORAL, maxw=3.4).move_to(P(4.6, -1.8))
        steps = [
            ([FadeIn(hdr), FadeIn(pans), FadeIn(lab), FadeIn(pt)], 1.0),
            ([FadeIn(arA[0]), FadeIn(arA[1]), FadeIn(r1)], 1.8),
            ([FadeIn(arB[0]), FadeIn(arB[1]), FadeIn(r2)], 2.0),
            ([FadeIn(r3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in arC[0]], lag_ratio=0.2)], 2.2),
            ([LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in arC[1]], lag_ratio=0.2)], 2.0),
            ([FadeIn(r4)], 1.2),
            ([FadeIn(r5)], 1.2),
        ]
        play_voiced(self, "01_20", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_21 (new)
    def s21(self):
        hdr = make_header("Ký hiệu O, Ω, Θ & bảng kết quả", "Chương 2", AMBER)
        cl, cr = -3.4, 3.4
        pl = panel(cl, -0.1, 6.0, 5.3)
        pr = panel(cr, -0.1, 6.0, 5.3)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 12, 4], x_length=4.8, y_length=2.7,
                  axis_config={"color": TEXT_MUTED, "stroke_width": 2, "include_ticks": False}).move_to(P(cl, 0.45))
        Tn = ax.plot(lambda n: n + 0.6 * np.sin(1.5 * n), x_range=[0.3, 10], color=AMBER, stroke_width=4)
        up = ax.plot(lambda n: 1.5 * n, x_range=[0.3, 8], color=CORAL, stroke_width=2.5)
        lo = ax.plot(lambda n: 0.5 * n, x_range=[0.3, 10], color=CYAN, stroke_width=2.5)
        mline = DashedLine(ax.c2p(2, 0), ax.c2p(2, 12), color=TEXT_MUTED, stroke_width=1.5)
        mt = T("m", 14, TEXT_MUTED).next_to(ax.c2p(2, 0), DOWN, buff=0.08)
        tT = T("T(n)", 14, AMBER, bold=True).next_to(ax.c2p(10, 10.6), UP, buff=0.05).shift(LEFT * 0.3)
        tU = T("c₂·f(n)", 14, CORAL).next_to(ax.c2p(8, 12), RIGHT, buff=0.05)
        tL = T("c₁·f(n)", 14, CYAN).next_to(ax.c2p(10, 5), DOWN, buff=0.08).shift(LEFT * 0.4)
        chips = VGroup(T("O: chặn trên", 15, CORAL, bold=True), T("Ω: chặn dưới", 15, CYAN, bold=True),
                       T("Θ: cả hai", 15, AMBER, bold=True)).arrange(RIGHT, buff=0.35).move_to(P(cl, -2.0))
        note = T("thường quan tâm O(n)", 14, TEXT_MUTED).move_to(P(cl, -2.5))
        ttl = T("Kết quả cần nhớ", 18, EMERALD, bold=True).move_to(P(cr, 2.15))
        rows = [("cộng 2 vector", "O(1)", "EREW"), ("tổng n số", "O(log n)", "EREW"), ("Boolean AND", "O(1)", "CRCW"),
                ("broadcast", "O(log n)", "EREW"), ("xếp hạng DS", "O(log n)", "EREW"), ("trộn 2 mảng", "O(log n)", "chia nhóm")]
        trs = []
        for i, (nm, cx_, mc) in enumerate(rows):
            y = 1.5 - 0.72 * i
            trs.append(VGroup(T(nm, 17, TEXT_MAIN, maxw=2.2).move_to(P(cr - 2.9, y), aligned_edge=LEFT),
                              T(cx_, 18, AMBER, mono=True, bold=True).move_to(P(cr + 0.5, y)),
                              T(mc, 14, VIOLET, maxw=1.5).move_to(P(cr + 2.3, y))))
        steps = [
            ([FadeIn(hdr), FadeIn(pl), FadeIn(pr)], 1.0),
            ([Create(ax), Create(Tn), FadeIn(tT)], 2.0),
            ([Create(lo), FadeIn(tL), Create(up), FadeIn(tU), Create(mline), FadeIn(mt)], 2.4),
            ([FadeIn(chips), FadeIn(note)], 2.0),
            ([FadeIn(ttl)], 0.6),
        ]
        for r in trs:
            steps.append(([FadeIn(r, shift=LEFT * 0.15)], 1.0))
        play_voiced(self, "01_21", steps)
        clear_stage(self)
