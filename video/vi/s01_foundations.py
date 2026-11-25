from manim import *
import numpy as np
from extras import seg_01_09, seg_01_13, seg_01_10
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
        self.s07()
        self.s11()
        self.s08()
        self.s12()
        seg_01_09(self)
        seg_01_13(self)
        seg_01_10(self)
        play_module_drills(self, "M1", "Ch 1, 2, 7")

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

        names = ["Nền tảng", "OpenMP", "MPI", "CUDA", "Thuật toán", "Luyện đề"]
        cols = [CYAN, AMBER, EMERALD, VIOLET, CORAL, TEXT_MAIN]
        xs = np.linspace(-5.0, 5.0, 6)
        line = Line(P(-5.6, -2.1), P(5.6, -2.1), color=BORDER_DIM, stroke_width=3)
        nodes = VGroup(); labs = VGroup()
        for i, (n, c, x) in enumerate(zip(names, cols, xs)):
            d = Circle(0.24, color=c, fill_color=PANEL_BG, fill_opacity=1, stroke_width=3).move_to(P(x, -2.1))
            num = T(str(i + 1), 16, c, bold=True).move_to(d)
            nodes.add(VGroup(d, num))
            labs.add(T(n, 18, TEXT_MAIN, maxw=1.7).move_to(P(x, -2.75)))
        token = Dot(radius=0.13, color=AMBER).move_to(P(xs[0], -2.1))

        steps = [
            ([FadeIn(title, shift=UP * 0.2), FadeIn(sub)], 1.2),
            ([FadeIn(c1, shift=UP * 0.2)], 2.2),
            ([FadeIn(c2, shift=UP * 0.2)], 2.2),
            ([FadeIn(c3, shift=UP * 0.2)], 2.2),
            ([Create(line), FadeIn(nodes), FadeIn(labs), FadeIn(token)], 1.5),
        ]
        for i in range(1, 6):
            steps.append(([token.animate.move_to(P(xs[i], -2.1)),
                           nodes[i][0].animate.set_fill(cols[i], opacity=0.35)], 1.3))
        play_voiced(self, "01_01", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_02
    def s02(self):
        hdr = make_header("Vì sao tăng tốc tuần tự dừng lại", "Chương 1 & 5", CYAN)
        cxs = [-4.4, 0.0, 4.4]
        pans = VGroup(*[panel(c, 0.0, 4.1, 4.8) for c in cxs])
        titles = VGroup(*[T(s, 22, col, bold=True).move_to(P(c, 2.05)) for s, col, c in
                          zip(["1. Tín hiệu", "2. Thu nhỏ", "3. Công suất"], [CYAN, VIOLET, CORAL], cxs)])

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

        # panel 3: power
        cx3 = cxs[2]
        ax = Axes(x_range=[0, 1.1, 0.5], y_range=[0, 1.3, 0.5], x_length=2.4, y_length=1.5,
                  axis_config={"color": TEXT_MUTED, "stroke_width": 2, "include_ticks": False}
                  ).move_to(P(cx3, -0.15))
        curve = ax.plot(lambda v: v * v, x_range=[0.05, 1.05], color=CORAL, stroke_width=4)
        tx = T("V", 14, TEXT_MUTED).next_to(ax.x_axis.get_end(), DOWN, buff=0.05)
        ty = T("P", 14, TEXT_MUTED).next_to(ax.y_axis.get_end(), LEFT, buff=0.05)
        mv = dot(AMBER, 0.1).move_to(ax.c2p(1.0, 1.0))
        flame = VGroup(
            Polygon(P(0, 0), P(0.28, 0.25), P(0.18, 0.6), P(0, 0.95), P(-0.2, 0.5), P(-0.28, 0.25),
                    color=CORAL, fill_color=CORAL, fill_opacity=0.95, stroke_width=0),
            Polygon(P(0, 0), P(0.14, 0.2), P(0, 0.5), P(-0.14, 0.2),
                    color=AMBER, fill_color=AMBER, fill_opacity=1, stroke_width=0))
        flame.move_to(P(cx3, 1.55), aligned_edge=DOWN).shift(UP * 0.0)
        flame_pt = flame.get_bottom()
        formula = T("P ~ f × V²", 24, AMBER, mono=True, bold=True).move_to(P(cx3, -1.35))
        warn = T("V quá thấp: 0 và 1 lẫn", 15, CORAL, maxw=3.7).move_to(P(cx3, -1.95))

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
            ([Create(ax), FadeIn(tx), FadeIn(ty), Create(curve), FadeIn(flame), FadeIn(formula)], 2.0),
            ([mv.animate.move_to(ax.c2p(0.5, 0.25)) if False else FadeIn(mv)], 0.4),
            ([MoveAlongPath(mv, ax.plot(lambda v: v * v, x_range=[1.0, 0.45]).reverse_points()
                            if False else Line(ax.c2p(1.0, 1.0), ax.c2p(0.5, 0.25))),
              flame.animate.scale(0.35, about_point=flame_pt)], 2.2),
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
        hdr = make_header("Thước đo hiệu năng: ví dụ số", "Ch. 1 & 7", EMERALD)
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
        cost = T("Chi phí = 8 × 20 = 160", 20, TEXT_MAIN, maxw=3.6).move_to(P(-3.4, -1.75))
        # right: metrics
        rx = 1.1
        r1 = T("S = 120 / 20 = 6×", 26, EMERALD, bold=True, maxw=3.2).move_to(P(rx, 2.0), aligned_edge=LEFT)
        cells = VGroup(*[Square(0.22, color=EMERALD, stroke_width=2, fill_opacity=0) for _ in range(8)]
                       ).arrange(RIGHT, buff=0.1).move_to(P(rx + 1.2, 1.35))
        r2 = T("E = 6 / 8 = 75%", 26, AMBER, bold=True, maxw=3.2).move_to(P(rx, 0.3), aligned_edge=LEFT)
        ring_bg = Circle(0.4, color=BORDER_DIM, stroke_width=6).move_to(P(5.6, 0.3))
        ring = Arc(radius=0.4, start_angle=PI / 2, angle=-1.5 * PI, color=AMBER, stroke_width=6,
                   arc_center=P(5.6, 0.3))
        r3 = T("Overhead = 160 − 120 = 40 s", 22, CORAL, bold=True, maxw=5.2).move_to(P(rx, -1.2), aligned_edge=LEFT)
        steps = [
            ([FadeIn(hdr)], 0.4),
            ([GrowFromEdge(ser, LEFT), FadeIn(ser_t), FadeIn(ser_l)], 2.0),
            ([LaggedStart(*[GrowFromEdge(w, LEFT) for w in work], lag_ratio=0.1), FadeIn(par_l)], 2.2),
            ([FadeIn(ovh), Create(tp_line), FadeIn(tp_t)], 1.6),
            ([FadeIn(r1)], 1.0),
            ([FadeIn(cells)], 0.8),
            ([LaggedStart(*[c.animate.set_fill(EMERALD, opacity=0.9) for c in cells[:6]], lag_ratio=0.3)], 2.2),
            ([FadeIn(r2), FadeIn(ring_bg), Create(ring)], 2.6),
            ([FadeIn(cost)], 1.2),
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

    # ------------------------------------------------------------ 01_08
    def s08(self):
        hdr = make_header("Đường găng trong DAG tác vụ", "Chương 7", CYAN)
        pos = {"A": (-4.8, 0.9), "B": (-2.0, 1.7), "C": (-2.0, 0.1), "D": (0.8, 1.7), "E": (0.8, 0.1), "F": (3.6, 0.9)}
        tm = {"A": 3, "B": 2, "C": 6, "D": 4, "E": 1, "F": 2}
        crit = ["A", "C", "E", "F"]
        nodes = {k: lbox(f"{k} ({tm[k]})", 1.3, 0.6, CYAN, 17, mono=True).move_to(P(*pos[k])) for k in pos}
        E = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "F"), ("E", "F")]
        ed = {}
        for a, b in E:
            ed[(a, b)] = Arrow(nodes[a].get_right(), nodes[b].get_left(), buff=0.06, color=TEXT_MUTED, stroke_width=3,
                               tip_length=0.15, max_tip_length_to_length_ratio=0.3)
        dag = VGroup(*nodes.values())
        path1 = poly(pos["A"], pos["B"], pos["D"], pos["F"])
        path2 = poly(pos["A"], pos["C"], pos["E"], pos["F"])
        d1 = dot(CYAN, 0.1).move_to(P(*pos["A"]))
        d2 = dot(CORAL, 0.1).move_to(P(*pos["A"]))
        n11 = T("ABDF = 11", 18, CYAN, bold=True).move_to(P(5.3, 1.7))
        n12 = T("ACEF = 12", 18, CORAL, bold=True).move_to(P(5.3, 0.1))
        formula = T("Đường găng = 3 + 6 + 1 + 2 = 12", 22, CORAL, bold=True, maxw=7).move_to(P(0, -0.85))
        # gantt
        gx, gs = -3.0, 0.5
        gl = [T("CPU 1", 14, TEXT_MUTED).move_to(P(gx - 0.5, -1.75)), T("CPU 2", 14, TEXT_MUTED).move_to(P(gx - 0.5, -2.45))]
        tasks = [("A", 0, 3, 0), ("C", 3, 9, 0), ("E", 9, 10, 0), ("F", 10, 12, 0), ("B", 3, 5, 1), ("D", 5, 9, 1)]
        gb = {}
        for k, s_, e_, r in tasks:
            col = CORAL if k in crit else CYAN
            y = -1.75 - 0.7 * r
            g = VGroup(rect_at(gx + s_ * gs, y, (e_ - s_) * gs, 0.5, col, 0.55), T(k, 15, TEXT_MAIN, bold=True))
            g[1].move_to(g[0]); gb[k] = g
        end = DashedLine(P(gx + 12 * gs, -1.35), P(gx + 12 * gs, -2.85), color=AMBER, stroke_width=2)
        endt = T("12", 16, AMBER, bold=True).move_to(P(gx + 12 * gs, -3.05))
        steps = [
            ([FadeIn(hdr), LaggedStart(*[FadeIn(n) for n in dag], lag_ratio=0.15)], 1.8),
            ([Create(e) for e in ed.values()], 1.4),
            ([FadeIn(d1), MoveAlongPath(d1, path1)], 2.2),
            ([FadeOut(d1)], 0.2),
            ([FadeIn(n11)], 0.8),
            ([FadeIn(d2), MoveAlongPath(d2, path2)], 2.4),
            ([FadeOut(d2)], 0.2),
            ([FadeIn(n12), *[ed[e].animate.set_color(CORAL) for e in [("A", "C"), ("C", "E"), ("E", "F")]],
              *[nodes[k][0].animate.set_stroke(CORAL, width=4) for k in crit]], 1.4),
            ([FadeIn(formula)], 1.4),
            ([FadeIn(VGroup(*gl))], 0.6),
            ([FadeIn(gb[k], shift=RIGHT * 0.1) for k in ("A", "C", "E", "F")], 2.4),
            ([FadeIn(gb[k], shift=RIGHT * 0.1) for k in ("B", "D")], 1.4),
            ([Create(end), FadeIn(endt)], 1.0),
        ]
        play_voiced(self, "01_08", steps)
        clear_stage(self)

    # ------------------------------------------------------------ 01_12 (new)
    def s12(self):
        hdr = make_header("Phụ thuộc vòng lặp & thăm dò", "Chương 7", EMERALD)
        xs = [-2.5 + i for i in range(6)]

        def row(y, code, col):
            c = T(code, 18, TEXT_MAIN, mono=True).move_to(P(-6.4, y), aligned_edge=LEFT)
            cl = VGroup(*[VGroup(bx(0.7, 0.55, col, sw=2), T(str(i), 14, TEXT_MUTED, mono=True)).move_to(P(x, y))
                          for i, x in enumerate(xs)])
            for g in cl:
                g[1].move_to(g[0])
            return c, cl
        c1, cl1 = row(1.9, "a[i] = a[i-1] + 1", CORAL)
        c2, cl2 = row(0.6, "b[i] = c[i] * 2", EMERALD)
        ar = VGroup(*[arr((xs[i] + 0.37, 1.9), (xs[i + 1] - 0.37, 1.9), CORAL, 3, 0.1) for i in range(5)])
        tg1 = T("tuần tự", 22, CORAL, bold=True).move_to(P(5.2, 1.9))
        tg2 = T("song song", 22, EMERALD, bold=True).move_to(P(5.2, 0.6))
        sep = Line(P(-6.4, -0.15), P(6.4, -0.15), color=BORDER_DIM, stroke_width=1.5)
        # tree
        root = bx(0.6, 0.45, VIOLET).move_to(P(-0.5, -0.8))
        lx = [-3.5, -1.5, 0.5, 2.5]
        leaves = VGroup(*[VGroup(bx(0.7, 0.5, VIOLET if i != 2 else AMBER, sw=2), T(str(i + 1), 14, TEXT_MAIN)).move_to(P(x, -2.35))
                          for i, x in enumerate(lx)])
        for g in leaves:
            g[1].move_to(g[0])
        tl = VGroup(*[Line(root.get_bottom(), g.get_top(), color=TEXT_MUTED, stroke_width=2) for g in leaves])
        star = T("★", 30, AMBER, bold=True).move_to(leaves[2].get_center() + DOWN * 0.55)
        tl_l = T("thăm dò", 18, VIOLET, bold=True).move_to(P(-5.6, -1.6))
        tl_r = T("tìm sớm: siêu tuyến tính", 15, AMBER, maxw=3.2).move_to(P(5.0, -1.6))
        sdots = [dot(AMBER, 0.09).move_to(root.get_bottom()) for _ in lx]
        steps = [
            ([FadeIn(hdr), FadeIn(c1), FadeIn(cl1), FadeIn(tg1)], 1.6),
            ([Succession(*[AnimationGroup(cl1[i][0].animate.set_fill(CORAL, opacity=0.6),
                                          *( [Create(ar[i - 1])] if i > 0 else [])) for i in range(6)])], 4.5),
            ([FadeIn(c2), FadeIn(cl2), FadeIn(tg2)], 1.4),
            ([*[g[0].animate.set_fill(EMERALD, opacity=0.6) for g in cl2]], 1.6),
            ([Create(sep), FadeIn(root), Create(tl), FadeIn(leaves), FadeIn(tl_l)], 1.8),
            ([FadeIn(VGroup(*sdots))], 0.3),
            ([MoveAlongPath(d, Line(root.get_bottom(), g.get_top())) for d, g in zip(sdots, leaves)], 1.8),
            ([FadeIn(star), Flash(leaves[2], color=AMBER), FadeIn(tl_r),
              *[g.animate.set_opacity(0.3) for i, g in enumerate(leaves) if i != 2]], 2.0),
        ]
        play_voiced(self, "01_12", steps)
        clear_stage(self)
