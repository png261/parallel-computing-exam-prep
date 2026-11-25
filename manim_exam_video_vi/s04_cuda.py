from manim import *
from scene_utils import play_module_drills
from scene_utils import (
    setup_bg, make_header, clear_stage, make_bar_chart, play_voiced,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, BORDER_DIM, SANS, MONO
)


def T(s, size=18, color=TEXT_MAIN, weight=NORMAL, font=SANS, maxw=None):
    t = Text(s, font=font, font_size=size, color=color, weight=weight)
    if maxw and t.width > maxw:
        t.scale_to_fit_width(maxw)
    return t


def R(w, h, color=BORDER_DIM, fill=PANEL_BG, op=0.95, sw=2.0, r=0.08):
    return RoundedRectangle(width=w, height=h, corner_radius=min(r, w / 2 - 0.001, h / 2 - 0.001),
                            stroke_color=color, stroke_width=sw, fill_color=fill, fill_opacity=op)


def C(w, h, color, op=0.85, sw=1.2, stroke=None):
    return Rectangle(width=w, height=h, stroke_color=stroke or color, stroke_width=sw,
                     fill_color=color, fill_opacity=op)


def key(s, color=AMBER):
    return T(s, 20, color, BOLD, maxw=12.0).move_to(DOWN * 3.1)


class Scene04CUDA(Scene):
    def construct(self):
        setup_bg(self)
        self.s01()
        self.s02()
        self.s03()
        self.s04()
        self.s05()
        self.s06()
        self.s07()
        self.s08()
        self.s09()
        self.s10()
        self.s11()
        self.s12()
        self.s13()
        self.s14()
        self.s15()
        self.s16()
        self.s17()
        self.s18()
        self.s19()
        self.s20()
        self.s21()
        play_module_drills(self, "M4", "CUDA")

    # 04_01 CPU vs GPU
    def s01(self):
        hdr = make_header("CPU và GPU: độ trễ hay thông lượng", "RTX 4070", EMERALD)
        cp = R(5.8, 3.3, CYAN, r=0.15).move_to(LEFT * 3.25 + UP * 0.0)
        ct = T("CPU", 22, CYAN, BOLD).move_to(cp.get_top() + DOWN * 0.3)
        cores = VGroup(*[C(1.1, 1.2, CYAN, 0.7) for _ in range(4)]).arrange(RIGHT, buff=0.15)
        cores.move_to(cp.get_center() + UP * 0.35)
        cache = C(5.0, 0.7, VIOLET, 0.5).move_to(cp.get_center() + DOWN * 0.95)
        cache_t = T("Cache lớn", 16).move_to(cache)
        cpu = VGroup(cp, ct, cores, cache, cache_t)

        gp = R(5.8, 3.3, EMERALD, r=0.15).move_to(RIGHT * 3.25)
        gt = T("GPU", 22, EMERALD, BOLD).move_to(gp.get_top() + DOWN * 0.3)
        cells = VGroup(*[C(0.3, 0.3, EMERALD, 0.35) for _ in range(60)]).arrange_in_grid(rows=5, cols=12, buff=0.12)
        cells.move_to(gp.get_center() + DOWN * 0.15)
        gpu = VGroup(gp, gt, cells)

        l1 = T("Ít nhân, rất nhanh", 18, CYAN).move_to(LEFT * 3.25 + DOWN * 2.1)
        l2 = T("Nhiều nhân, cùng lúc", 18, EMERALD).move_to(RIGHT * 3.25 + DOWN * 2.1)
        k = key("RTX 4070: 46 SM · 5.888 nhân · 438 GB/s")

        tok = C(0.28, 0.28, AMBER, 1.0).move_to(cores[0].get_center())
        path = [cores[i].get_center() for i in range(4)]
        play_voiced(self, "04_01", [
            ([FadeIn(hdr), FadeIn(cpu)], 1.2),
            ([FadeIn(l1), FadeIn(tok)], 0.8),
            ([MoveAlongPath(tok, Line(path[0], path[3]), rate_func=linear)], 1.0),
            ([FadeOut(tok)], 0.3),
            ([FadeIn(gpu), FadeIn(l2)], 1.2),
            ([LaggedStart(*[c.animate.set_fill(AMBER, 0.95) for c in cells], lag_ratio=0.04)], 2.5),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_02 host / device flow
    def s02(self):
        hdr = make_header("Luồng host - device: copy vào, chạy, copy ra", "PCIe", CYAN)
        host = R(3.0, 2.6, CYAN, r=0.12).move_to(LEFT * 4.3 + UP * 0.2)
        dev = R(3.0, 2.6, EMERALD, r=0.12).move_to(RIGHT * 4.3 + UP * 0.2)
        ht = T("CPU + RAM", 18, CYAN, BOLD).move_to(host.get_top() + DOWN * 0.3)
        dt = T("GPU + VRAM", 18, EMERALD, BOLD).move_to(dev.get_top() + DOWN * 0.3)
        pipe = R(5.6, 0.55, BORDER_DIM, op=0.6).move_to(UP * 0.3)
        pl = T("PCIe", 16, TEXT_MUTED).next_to(pipe, DOWN, buff=0.15)
        hc = VGroup(*[C(0.5, 0.5, CYAN) for _ in range(4)]).arrange(RIGHT, buff=0.08).move_to(host.get_center() + UP * 0.1)
        hc.set_y(0.3)
        slots = VGroup(*[C(0.5, 0.5, BORDER_DIM, 0.15, stroke=BORDER_DIM) for _ in range(4)]).arrange(RIGHT, buff=0.08)
        slots.move_to(dev.get_center()).set_y(0.3)
        res = VGroup(*[C(0.5, 0.5, EMERALD, 0.15, stroke=BORDER_DIM) for _ in range(4)]).arrange(RIGHT, buff=0.08)
        res.move_to(host.get_center()).set_y(-0.55)
        launch = Arrow(LEFT * 2.8 + UP * 1.3, RIGHT * 2.8 + UP * 1.3, color=AMBER, buff=0, stroke_width=5)
        step1 = T("① Copy vào (H→D)", 22, CYAN, BOLD).move_to(DOWN * 2.2)
        step2 = T("② Chạy kernel", 22, AMBER, BOLD).move_to(DOWN * 2.2)
        step3 = T("③ Copy ra (D→H)", 22, EMERALD, BOLD).move_to(DOWN * 2.2)
        k = key("Dữ liệu qua PCIe hai lần")
        copies = [hc[i].copy() for i in range(4)]
        play_voiced(self, "04_02", [
            ([FadeIn(hdr), FadeIn(host), FadeIn(dev), FadeIn(ht), FadeIn(dt), FadeIn(pipe), FadeIn(pl),
              FadeIn(hc), FadeIn(slots), FadeIn(res)], 1.4),
            ([FadeIn(step1)], 0.4),
            ([LaggedStart(*[copies[i].animate.move_to(slots[i]) for i in range(4)], lag_ratio=0.3)], 2.4),
            ([ReplacementTransform(step1, step2), GrowArrow(launch)], 0.8),
            ([slots[i].animate.set_fill(EMERALD, 0.9).set_stroke(EMERALD) for i in range(4)] +
             [c.animate.set_fill(EMERALD, 0.9) for c in copies], 1.2),
            ([ReplacementTransform(step2, step3), FadeOut(launch)], 0.8),
            ([LaggedStart(*[copies[i].copy().animate.move_to(res[i]) for i in range(4)], lag_ratio=0.3)], 2.4),
            ([FadeIn(k)], 0.6),
        ])
        clear_stage(self)

    # 04_03 grid -> block -> thread + SAXPY n=1000
    def s03(self):
        hdr = make_header("Grid → block → thread: SAXPY n = 1000", "256 thread / block", VIOLET)
        top = T("số block = ⌈1000 / 256⌉ = 4", 24, AMBER, BOLD, MONO, maxw=8).move_to(UP * 2.4)
        grid = R(12.2, 2.3, VIOLET, op=0.3, r=0.12).move_to(UP * 0.8)
        gl = T("Grid", 16, VIOLET, BOLD).move_to(grid.get_corner(UL) + RIGHT * 0.45 + DOWN * 0.2)
        blocks = VGroup(); bars = VGroup(); fills = VGroup(); labs = VGroup()
        for b in range(4):
            x = -4.35 + 2.9 * b
            br = R(2.6, 1.7, EMERALD, r=0.1).move_to(RIGHT * x + UP * 0.65)
            bl = T("Block %d" % b, 16, EMERALD, BOLD).move_to(RIGHT * x + UP * 1.28)
            bar = Rectangle(width=2.0, height=0.8, stroke_color=TEXT_MUTED, stroke_width=1.5, fill_opacity=0)
            bar.move_to(RIGHT * x + UP * 0.3)
            frac = 1.0 if b < 3 else 232 / 256
            fl = Rectangle(width=2.0, height=0.8 * frac, stroke_width=0, fill_color=CYAN, fill_opacity=0.85)
            fl.align_to(bar, DOWN).align_to(bar, LEFT)
            blocks.add(br); labs.add(bl); bars.add(bar); fills.add(fl)
        nlab = T("256 thread", 15, TEXT_MAIN).move_to(bars[0])
        # worked strip
        idxs = list(range(996, 1004))
        strip = VGroup(*[VGroup(C(0.85, 0.6, EMERALD if i < 1000 else CORAL, 0.8 if i < 1000 else 0.5),
                                T(str(i), 16, TEXT_MAIN, BOLD, MONO)) for i in idxs])
        for g in strip:
            g[1].move_to(g[0])
        strip.arrange(RIGHT, buff=0.06).move_to(DOWN * 1.35)
        sl = T("i = 3 × 256 + t", 18, TEXT_MUTED, NORMAL, MONO).next_to(strip, LEFT, buff=0.3)
        ok = T("i < n: chạy ✓", 16, EMERALD, BOLD).next_to(strip[:4], DOWN, buff=0.2)
        no = T("bỏ qua ✗ (24 thread)", 16, CORAL, BOLD).next_to(strip[4:], DOWN, buff=0.2)
        zoom = Line(bars[3].get_bottom() + RIGHT * 0.9, strip.get_top() + RIGHT * 0.5, color=CORAL, stroke_width=1.5)
        play_voiced(self, "04_03", [
            ([FadeIn(hdr), FadeIn(grid), FadeIn(gl)], 1.0),
            ([LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.2), FadeIn(labs), FadeIn(bars), FadeIn(nlab)], 1.6),
            ([FadeIn(top)], 0.8),
            ([GrowFromEdge(fills[i], DOWN) for i in range(3)], 1.5),
            ([GrowFromEdge(fills[3], DOWN)], 1.0),
            ([FadeIn(strip), FadeIn(sl), Create(zoom)], 1.2),
            ([FadeIn(ok), FadeIn(no)], 1.0),
        ])
        clear_stage(self)

    # 04_04 2D index
    def s04(self):
        hdr = make_header("Chỉ số 2D: ảnh rộng 1920 pixel", "blockIdx · threadIdx", CYAN)
        bg = VGroup(*[C(0.6, 0.6, BORDER_DIM, 0.5, 1.5, stroke=TEXT_MUTED) for _ in range(24)]).arrange_in_grid(rows=4, cols=6, buff=0.04)
        bg.move_to(LEFT * 4.6 + UP * 0.5)
        bsel = bg[2 * 6 + 3]
        bl = T("blockIdx = (3, 2)", 17, VIOLET, BOLD, MONO).next_to(bg, DOWN, buff=0.2)
        tg = VGroup(*[C(0.18, 0.18, EMERALD, 0.3, 0.8, stroke=EMERALD) for _ in range(256)]).arrange_in_grid(rows=16, cols=16, buff=0.02)
        tg.move_to(LEFT * 0.4 + UP * 0.4)
        tsel = tg[5 * 16 + 4]
        tl = T("threadIdx = (4, 5)  ·  block 16×16", 15, EMERALD, BOLD, MONO, maxw=3.9).next_to(tg, DOWN, buff=0.2)
        arr = Arrow(LEFT * 2.75 + UP * 0.5, LEFT * 2.15 + UP * 0.5, color=TEXT_MUTED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.5)
        hl1 = SurroundingRectangle(bsel, color=AMBER, buff=0.0, stroke_width=4)
        hl2 = SurroundingRectangle(tsel, color=AMBER, buff=0.0, stroke_width=3)
        f1 = T("ix = 3×16 + 4 = 52", 20, CYAN, BOLD, MONO)
        f2 = T("iy = 2×16 + 5 = 37", 20, EMERALD, BOLD, MONO)
        f3 = T("idx = 37×1920 + 52", 20, TEXT_MAIN, BOLD, MONO)
        f4 = T("= 71092", 28, AMBER, BOLD, MONO)
        fs = VGroup(f1, f2, f3, f4).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        panel = R(4.7, 3.3, AMBER, r=0.12).move_to(RIGHT * 4.2 + UP * 0.4)
        fs.move_to(panel)
        play_voiced(self, "04_04", [
            ([FadeIn(hdr), FadeIn(bg)], 1.0),
            ([Create(hl1), FadeIn(bl)], 1.0),
            ([FadeIn(arr), FadeIn(tg), FadeIn(tl)], 1.2),
            ([Create(hl2), tsel.animate.set_fill(AMBER, 1)], 1.0),
            ([FadeIn(panel), FadeIn(f1)], 1.2),
            ([FadeIn(f2)], 1.2),
            ([FadeIn(f3)], 1.2),
            ([FadeIn(f4)], 1.0),
        ])
        clear_stage(self)

    # 04_05 warp lockstep + divergence
    def s05(self):
        hdr = make_header("Warp: 32 lane chạy cùng lệnh", "lockstep", AMBER)
        lanes = VGroup(*[C(0.33, 0.55, CYAN, 0.35, 1.2) for _ in range(32)]).arrange(RIGHT, buff=0.04).move_to(UP * 0.5)
        n0 = T("lane 0", 14, TEXT_MUTED).next_to(lanes[0], DOWN, buff=0.12).align_to(lanes, LEFT)
        n31 = T("lane 31", 14, TEXT_MUTED).next_to(lanes[31], DOWN, buff=0.12).align_to(lanes, RIGHT)
        ins1 = VGroup(R(4.0, 0.6, AMBER), T("y = a×x + y", 20, TEXT_MAIN, BOLD, MONO))
        ins1[1].move_to(ins1[0]); ins1.move_to(UP * 1.9)
        ins2 = VGroup(R(6.2, 0.6, AMBER), T("if (lane < 16) A  else  B", 20, TEXT_MAIN, BOLD, MONO))
        ins2[1].move_to(ins2[0]); ins2.move_to(UP * 1.9)
        grey = "#3A4048"
        left = lanes[:16]; right = lanes[16:]
        # timelines
        u = 2.8
        r1 = C(u, 0.4, EMERALD, 0.85).move_to(LEFT * 4.5 + RIGHT * u / 2 + DOWN * 1.5)
        r1.align_to(LEFT * 4.5, LEFT)
        r2a = C(u, 0.4, CYAN, 0.85); r2b = C(u, 0.4, VIOLET, 0.85)
        r2 = VGroup(r2a, r2b).arrange(RIGHT, buff=0).move_to(DOWN * 2.3).align_to(r1, LEFT)
        L1 = T("Không rẽ nhánh", 15, TEXT_MAIN).move_to(LEFT * 5.6 + DOWN * 1.5)
        L2 = T("Rẽ nhánh", 15, TEXT_MAIN).move_to(LEFT * 5.6 + DOWN * 2.3)
        for L in (L1, L2):
            L.align_to(LEFT * 6.5, LEFT)
        t1 = T("0,62 ms", 16, EMERALD, BOLD, MONO).next_to(r1, RIGHT, buff=0.2)
        t2 = T("1,23 ms  (×2)", 16, CORAL, BOLD, MONO).next_to(r2, RIGHT, buff=0.2)
        ta = T("A", 16, "#0D1117", BOLD).move_to(r2a); tb = T("B", 16, "#0D1117", BOLD).move_to(r2b)
        play_voiced(self, "04_05", [
            ([FadeIn(hdr), FadeIn(lanes), FadeIn(n0), FadeIn(n31)], 1.0),
            ([FadeIn(ins1)], 0.6),
            ([lanes.animate.set_fill(CYAN, 0.95)], 0.6),
            ([Indicate(lanes, color=AMBER, scale_factor=1.05)], 1.0),
            ([FadeIn(L1), GrowFromEdge(r1, LEFT), FadeIn(t1)], 1.0),
            ([ReplacementTransform(ins1, ins2), lanes.animate.set_fill(CYAN, 0.35)], 0.8),
            ([left.animate.set_fill(CYAN, 0.95), right.animate.set_fill(grey, 0.9).set_stroke(grey)], 1.2),
            ([FadeIn(L2), GrowFromEdge(r2a, LEFT), FadeIn(ta)], 0.8),
            ([left.animate.set_fill(grey, 0.9).set_stroke(grey), right.animate.set_fill(VIOLET, 0.95).set_stroke(VIOLET)], 1.2),
            ([GrowFromEdge(r2b, LEFT), FadeIn(tb), FadeIn(t2)], 0.8),
        ])
        clear_stage(self)

    # 04_06 latency hiding timeline
    def s06(self):
        hdr = make_header("Che độ trễ: chuyển warp", "400–800 chu kỳ", EMERALD)
        cols = [CYAN, AMBER, EMERALD, VIOLET]
        x0 = -5.5; u = 1.4; h = 0.45
        ys = [1.9, 1.2, 0.5, -0.2]
        smy = -1.25

        def seg(a, b, y, color, op=0.9, hh=h):
            return C((b - a) * u, hh, color, op).move_to(RIGHT * (x0 + (a + b) / 2 * u) + UP * y)
        names = [T("Warp %d" % i, 14, cols[i], BOLD).move_to(LEFT * 6.1 + UP * ys[i]) for i in range(4)]
        sml = T("SM", 16, TEXT_MAIN, BOLD).move_to(LEFT * 6.15 + UP * smy)
        for t in names:
            t.set_x(-6.0)
        rows = []
        for k in range(4):
            c1 = seg(k, k + 1, ys[k], cols[k])
            w = seg(k + 1, k + 4, ys[k], BORDER_DIM, 0.9)
            w.set_stroke(TEXT_MUTED, 1)
            c2 = seg(k + 4, k + 5, ys[k], cols[k])
            rows.append((c1, w, c2))
        wl = T("chờ DRAM", 14, TEXT_MUTED).move_to(rows[0][1])
        sm_pieces = []
        for t in range(8):
            sm_pieces.append(seg(t, t + 1, smy, cols[t % 4], 0.9, 0.55))
        idle = [seg(1, 4, smy, CORAL, 0.15, 0.55), seg(5, 8, smy, CORAL, 0.15, 0.55)]
        for d in idle:
            d.set_stroke(CORAL, 1.5)
        il = T("SM rảnh!", 16, CORAL, BOLD).move_to(idle[0])
        k = key("Luôn có warp sẵn sàng → SM luôn bận", EMERALD)
        play_voiced(self, "04_06", [
            ([FadeIn(hdr), FadeIn(names[0]), FadeIn(sml)], 0.8),
            ([FadeIn(rows[0][0]), FadeIn(rows[0][1]), FadeIn(rows[0][2]), FadeIn(wl)], 1.2),
            ([FadeIn(sm_pieces[0]), FadeIn(sm_pieces[4]), FadeIn(idle[0]), FadeIn(idle[1]), FadeIn(il)], 1.2),
            ([FadeIn(names[1]), FadeIn(names[2]), FadeIn(names[3])] +
             [FadeIn(m) for kk in (1, 2, 3) for m in rows[kk]], 1.5),
            ([FadeOut(idle[0]), FadeOut(idle[1]), FadeOut(il)] +
             [FadeIn(sm_pieces[i]) for i in (1, 2, 3, 5, 6, 7)], 1.5),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_07 memory pyramid
    def s07(self):
        hdr = make_header("Phân cấp bộ nhớ CUDA", "nhanh ↔ lớn", VIOLET)
        cx = -3.4; ytop = 1.9
        names = ["Register", "Shared 48 KB", "Global DRAM"]
        cols = [EMERALD, CYAN, CORAL]
        layers = VGroup(); texts = VGroup(); centers = []
        for j in range(3):
            yt = ytop - j * 1.0; yb = yt - 0.95
            wt = 0.8 + 1.467 * j; wb = 0.8 + 1.467 * (j + 0.95)
            p = Polygon([cx - wt / 2, yt, 0], [cx + wt / 2, yt, 0], [cx + wb / 2, yb, 0], [cx - wb / 2, yb, 0],
                        stroke_color=cols[j], stroke_width=2, fill_color=cols[j], fill_opacity=0.35)
            layers.add(p)
            texts.add(T(names[j], 16, TEXT_MAIN, BOLD, maxw=1.3 + j * 1.2).move_to(RIGHT * cx + UP * (yt - 0.475)))
            centers.append(RIGHT * cx + UP * (yt - 0.475))
        fast = T("nhanh", 15, EMERALD, BOLD).move_to(LEFT * 6.3 + UP * 2.2)
        slow = T("chậm", 15, CORAL, BOLD).move_to(LEFT * 6.3 + DOWN * 1.3)
        ar = Arrow(LEFT * 6.3 + DOWN * 1.0, LEFT * 6.3 + UP * 1.9, color=TEXT_MUTED, buff=0, stroke_width=3)
        chart = make_bar_chart([1, 5, 600], ["Register\n(thread)", "Shared\n(block)", "Global\n(grid)"],
                               [EMERALD, CYAN, CORAL], 700, width=5.0, height=2.9, unit="chu kỳ")
        chart.move_to(RIGHT * 3.4 + DOWN * 0.3)
        dot = Dot(centers[2] + RIGHT * 0.8, radius=0.13, color=AMBER)
        k = key("Tải một lần → dùng nhiều lần")
        play_voiced(self, "04_07", [
            ([FadeIn(hdr)], 0.5),
            ([LaggedStart(*[FadeIn(layers[i]) for i in (0, 1, 2)], lag_ratio=0.3), FadeIn(texts), FadeIn(ar), FadeIn(fast), FadeIn(slow)], 1.6),
            ([FadeIn(chart)], 1.6),
            ([FadeIn(dot)], 0.3),
            ([dot.animate.move_to(centers[1] + RIGHT * 0.8)], 1.0),
            ([dot.animate.move_to(centers[0] + RIGHT * 0.68)], 1.0),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_08 coalescing
    def s08(self):
        hdr = make_header("Truy cập liên tục vs bước nhảy", "coalescing", AMBER)
        pitch = 0.18
        mem = VGroup(*[C(0.16, 0.45, BORDER_DIM, 0.6, 0.8, stroke=TEXT_MUTED) for _ in range(64)]).arrange(RIGHT, buff=0.02)
        mem.move_to(UP * 0.2)
        lines = VGroup(*[SurroundingRectangle(mem[8 * i:8 * i + 8], color=TEXT_MUTED, buff=0.02, stroke_width=1.5) for i in range(8)])
        ml = T("bộ nhớ: 8 dòng × 8 từ", 15, TEXT_MUTED).next_to(mem, DOWN, buff=0.45)

        def lane_group(targets):
            g = VGroup(); a = VGroup()
            for k_, c in enumerate(targets):
                top = mem[c].get_top() + UP * 1.5 + RIGHT * 0
                d = Dot(mem[c].get_top() + UP * 1.5, radius=0.1, color=CYAN)
                g.add(d)
                a.add(Arrow(d.get_bottom(), mem[c].get_top(), buff=0.03, color=CYAN, stroke_width=2, tip_length=0.12))
            return g, a
        # contiguous: lanes spread over x
        cont_targets = list(range(8))
        lanes1 = VGroup(*[Dot(radius=0.1, color=CYAN).move_to(LEFT * 5.2 + RIGHT * 0.45 * i + UP * 1.7) for i in range(8)])
        lanes1.move_to(mem[3].get_center() + RIGHT * 0.09 + UP * 1.7)
        ar1 = VGroup(*[Arrow(lanes1[i].get_bottom(), mem[i].get_top(), buff=0.03, color=CYAN, stroke_width=2, tip_length=0.1) for i in range(8)])
        lanes2 = VGroup(*[Dot(mem[8 * i].get_top() + UP * 1.7, radius=0.1, color=CORAL) for i in range(8)])
        ar2 = VGroup(*[Arrow(lanes2[i].get_bottom(), mem[8 * i].get_top(), buff=0.03, color=CORAL, stroke_width=2, tip_length=0.1) for i in range(8)])
        hl1 = SurroundingRectangle(mem[0:8], color=EMERALD, buff=0.04, stroke_width=4)
        hl2 = VGroup(*[SurroundingRectangle(mem[8 * i:8 * i + 8], color=CORAL, buff=0.04, stroke_width=3) for i in range(8)])
        c1 = T("liên tục: 1 giao dịch", 24, EMERALD, BOLD).move_to(DOWN * 1.7)
        c2 = T("bước nhảy 8: 8 giao dịch", 24, CORAL, BOLD).move_to(DOWN * 1.7)
        wl = T("8 lane của warp", 15, TEXT_MUTED).next_to(lanes1, UP, buff=0.15)
        chart = make_bar_chart([447, 100], ["Liên tục", "Bước nhảy"], [EMERALD, CORAL], 480, width=5.0, height=2.8, unit="GB/s")
        chart.move_to(DOWN * 0.1)
        k = key("Băng thông: 447 → 100 GB/s")
        play_voiced(self, "04_08", [
            ([FadeIn(hdr), FadeIn(mem), FadeIn(lines), FadeIn(ml)], 1.0),
            ([FadeIn(lanes1), FadeIn(wl)], 0.8),
            ([LaggedStart(*[GrowArrow(a) for a in ar1], lag_ratio=0.1), Create(hl1)], 1.5),
            ([FadeIn(c1)], 1.2),
            ([FadeOut(lanes1), FadeOut(ar1), FadeOut(hl1), FadeOut(wl), ReplacementTransform(c1, c2)], 0.8),
            ([FadeIn(lanes2), LaggedStart(*[GrowArrow(a) for a in ar2], lag_ratio=0.1), FadeIn(hl2)], 2.0),
            ([FadeOut(lanes2), FadeOut(ar2), FadeOut(hl2), FadeOut(mem), FadeOut(lines), FadeOut(ml), FadeOut(c2)], 0.6),
            ([FadeIn(chart), FadeIn(k)], 1.5),
        ])
        clear_stage(self)

    # 04_09 pinned & unified memory
    def s09(self):
        hdr = make_header("Pinned và Unified Memory", "256 MiB", CYAN)
        c1 = make_bar_chart([21.3, 26.4], ["Thường", "Pinned"], [CYAN, EMERALD], 30, width=4.6, height=2.8, unit="GB/s")
        c1.move_to(LEFT * 3.3 + DOWN * 0.3)
        t1 = T("D→H: cudaMallocHost", 18, CYAN, BOLD).move_to(LEFT * 3.3 + UP * 1.9)
        c2 = make_bar_chart([27.5, 11.7, 1.23], ["Page fault", "Prefetch", "Trên GPU"], [CORAL, AMBER, EMERALD], 30, width=5.4, height=2.8, unit="ms")
        c2.move_to(RIGHT * 3.4 + DOWN * 0.3)
        t2 = T("Unified: cudaMallocManaged", 18, EMERALD, BOLD).move_to(RIGHT * 3.4 + UP * 1.9)
        k = key("Dữ liệu càng gần GPU, càng nhanh", EMERALD)
        play_voiced(self, "04_09", [
            ([FadeIn(hdr), FadeIn(t1)], 0.8),
            ([FadeIn(c1[0]), FadeIn(c1[1]), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in c1[2]], lag_ratio=0.5)], 2.0),
            ([FadeIn(t2)], 0.8),
            ([FadeIn(c2[0]), FadeIn(c2[1]), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in c2[2]], lag_ratio=0.5)], 3.0),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_10 async launch
    def s10(self):
        hdr = make_header("Gọi kernel là bất đồng bộ", "cudaDeviceSynchronize", AMBER)
        x0 = -5.5; u = 1.1
        cy = 1.0; gy = -0.4

        def seg(a, b, y, color, label="", op=0.85, ts=14, tc=None):
            r_ = C((b - a) * u, 0.6, color, op).move_to(RIGHT * (x0 + (a + b) / 2 * u) + UP * y)
            g = VGroup(r_)
            if label:
                g.add(T(label, ts, tc or "#0D1117", BOLD, maxw=(b - a) * u - 0.1).move_to(r_))
            return g
        lc = T("CPU", 18, CYAN, BOLD).move_to(LEFT * 6.2 + UP * cy)
        lg = T("GPU", 18, EMERALD, BOLD).move_to(LEFT * 6.2 + UP * gy)
        launch = seg(0, 0.9, cy, AMBER, "launch")
        work = seg(0.9, 3.5, cy, CYAN, "việc khác")
        wait = seg(3.5, 7, cy, BORDER_DIM, "chờ cudaDeviceSynchronize", 1.0, 14, TEXT_MAIN)
        wait[0].set_stroke(AMBER, 2)
        read = seg(7, 9, cy, CYAN, "đọc kết quả ✓")
        kern = seg(1.0, 7, gy, EMERALD, "kernel chạy")
        early = DashedLine(RIGHT * (x0 + 2.3 * u) + UP * (cy - 0.3), RIGHT * (x0 + 2.3 * u) + UP * (gy + 0.3), color=CORAL, stroke_width=3)
        early_t = T("✗ đọc sớm: sai!", 15, CORAL, BOLD).next_to(early, RIGHT, buff=0.12)
        k = key("<<<1, 2000>>> sai: tối đa 1024 thread / block", CORAL)
        tmark = Arrow(LEFT * 5.5 + DOWN * 1.1, RIGHT * 5.5 + DOWN * 1.1, color=TEXT_MUTED, buff=0, stroke_width=2)
        tl = T("thời gian", 14, TEXT_MUTED).next_to(tmark, DOWN, buff=0.08).align_to(tmark, RIGHT)
        play_voiced(self, "04_10", [
            ([FadeIn(hdr), FadeIn(lc), FadeIn(lg), FadeIn(tmark), FadeIn(tl)], 0.8),
            ([FadeIn(launch)], 0.6),
            ([GrowFromEdge(kern, LEFT), GrowFromEdge(work, LEFT)], 1.6),
            ([Create(early), FadeIn(early_t)], 1.0),
            ([FadeOut(early), FadeOut(early_t), GrowFromEdge(wait, LEFT)], 1.6),
            ([FadeIn(read)], 0.8),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_11 block independence
    def s11(self):
        hdr = make_header("Block độc lập, chỉ đồng bộ trong block", "__syncthreads", CORAL)
        box = R(5.6, 3.2, EMERALD, op=0.4, r=0.12).move_to(LEFT * 3.5 + UP * 0.1)
        bl = T("Block 0", 16, EMERALD, BOLD).move_to(box.get_corner(UL) + RIGHT * 0.7 + DOWN * 0.25)
        bar_x = -2.3
        bar = DashedLine(RIGHT * bar_x + UP * 1.2, RIGHT * bar_x + DOWN * 1.35, color=AMBER, stroke_width=4)
        bt = T("__syncthreads()", 15, AMBER, BOLD, MONO).move_to(RIGHT * bar_x + UP * 1.42)
        ys = [0.8, 0.25, -0.3, -0.85]
        sx = [-5.8, -5.3, -5.6, -5.0]
        dots = VGroup(*[Dot(RIGHT * sx[i] + UP * ys[i], radius=0.16, color=cols) for i, cols in enumerate([CYAN, AMBER, EMERALD, VIOLET])])
        okl = T("Cùng block: đợi nhau ✓", 17, EMERALD, BOLD).move_to(LEFT * 3.5 + DOWN * 1.95)
        sm = R(2.5, 1.7, BORDER_DIM, r=0.1).move_to(RIGHT * 5.0 + UP * 0.6)
        sml = T("SM (đầy)", 14, TEXT_MUTED).move_to(sm.get_top() + DOWN * 0.22)
        b1 = VGroup(R(2.0, 0.7, AMBER, r=0.08), T("Block 1", 16, AMBER, BOLD)); b1[1].move_to(b1[0]); b1.move_to(sm.get_center() + DOWN * 0.15)
        b0 = VGroup(R(1.8, 0.7, CORAL, op=0.2, r=0.08), T("Block 0", 16, CORAL, BOLD)); b0[1].move_to(b0[0]); b0.move_to(RIGHT * 1.9 + UP * 0.6)
        b0l = T("chờ chỗ trong SM", 14, TEXT_MUTED).next_to(b0, DOWN, buff=0.12)
        ar = Arrow(b1.get_left(), b0.get_right(), color=AMBER, buff=0.06, stroke_width=4)
        al = T("đợi cờ", 14, AMBER, BOLD).next_to(ar, UP, buff=0.08)
        dl = T("DEADLOCK", 28, CORAL, BOLD).move_to(RIGHT * 3.5 + DOWN * 0.7)
        nol = T("Khác block: không khóa ✗", 17, CORAL, BOLD).move_to(RIGHT * 3.5 + DOWN * 1.95)
        mv = [MoveAlongPath(dots[i], Line(dots[i].get_center(), RIGHT * (bar_x - 0.25) + UP * ys[i]), run_time=r_, rate_func=smooth)
              for i, r_ in enumerate([1.0, 1.6, 0.8, 2.0])]
        play_voiced(self, "04_11", [
            ([FadeIn(hdr), FadeIn(box), FadeIn(bl), FadeIn(dots)], 1.0),
            ([Create(bar), FadeIn(bt)], 0.8),
            (mv, 2.0),
            ([bar.animate.set_color(EMERALD)] + [d.animate.shift(RIGHT * 1.7) for d in dots], 1.2),
            ([FadeIn(okl)], 0.6),
            ([FadeIn(sm), FadeIn(sml), FadeIn(b1), FadeIn(b0), FadeIn(b0l)], 1.2),
            ([GrowArrow(ar), FadeIn(al)], 0.8),
            ([FadeIn(dl), FadeIn(nol)], 1.0),
        ])
        clear_stage(self)

    # 04_12 PCIe bottleneck
    def s12(self):
        hdr = make_header("Nút thắt PCIe của SAXPY", "n = 2²⁶ float", CORAL)
        x0 = -5.8; s = 0.24
        ys = [1.3, 0.2, -0.9]
        h = 0.5

        def bar(a, b, y, color):
            return C((b - a) * s, h, color, 0.9).move_to(RIGHT * (x0 + (a + b) / 2 * s) + UP * y)
        lab = [T("CPU tuần tự", 17, TEXT_MAIN, BOLD).move_to(RIGHT * x0 + UP * (ys[0] + 0.45)).align_to(LEFT * 5.8, LEFT),
               T("GPU: chỉ kernel", 17, TEXT_MAIN, BOLD).move_to(UP * (ys[1] + 0.45)).align_to(LEFT * 5.8, LEFT),
               T("GPU: cả quy trình", 17, TEXT_MAIN, BOLD).move_to(UP * (ys[2] + 0.45)).align_to(LEFT * 5.8, LEFT)]
        b_cpu = bar(0, 15.1, ys[0], CYAN)
        b_ker = bar(0, 1.84, ys[1], EMERALD)
        b_h2d = bar(0, 25.2, ys[2], CORAL)
        b_k2 = bar(25.2, 27.04, ys[2], EMERALD)
        b_d2h = bar(27.04, 40.24, ys[2], AMBER)
        n_cpu = T("15,1 ms", 18, CYAN, BOLD, MONO).next_to(b_cpu, RIGHT, buff=0.2)
        n_ker = T("1,84 ms  (nhanh 8×)", 18, EMERALD, BOLD, MONO).next_to(b_ker, RIGHT, buff=0.2)
        t_h2d = T("H→D 25,2", 15, "#0D1117", BOLD, MONO).move_to(b_h2d)
        t_d2h = T("D→H 13,2", 15, "#0D1117", BOLD, MONO, maxw=3.4).move_to(b_d2h)
        n_tot = T("≈ 40 ms", 18, CORAL, BOLD, MONO).next_to(b_d2h, RIGHT, buff=0.2)
        k = key("Kernel nhanh 8×, tổng thể chậm 2,7×", CORAL)
        play_voiced(self, "04_12", [
            ([FadeIn(hdr), FadeIn(lab[0])], 0.6),
            ([GrowFromEdge(b_cpu, LEFT), FadeIn(n_cpu)], 1.4),
            ([FadeIn(lab[1]), GrowFromEdge(b_ker, LEFT), FadeIn(n_ker)], 1.4),
            ([FadeIn(lab[2])], 0.4),
            ([GrowFromEdge(b_h2d, LEFT), FadeIn(t_h2d)], 1.8),
            ([FadeIn(b_k2)], 0.6),
            ([GrowFromEdge(b_d2h, LEFT), FadeIn(t_d2h), FadeIn(n_tot)], 1.4),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_13 bandwidth formula
    def s13(self):
        hdr = make_header("Băng thông hiệu dụng của SAXPY", "3 truy cập / phần tử", AMBER)
        xb = VGroup(R(1.5, 0.8, CYAN), T("x[i] = 2", 18, CYAN, BOLD, MONO)); xb[1].move_to(xb[0]); xb.move_to(LEFT * 5.2 + UP * 1.5)
        yb = VGroup(R(1.5, 0.8, VIOLET), T("y[i] = 1", 18, VIOLET, BOLD, MONO)); yb[1].move_to(yb[0]); yb.move_to(LEFT * 5.2 + UP * 0.2)
        kb = R(2.8, 1.6, AMBER, r=0.12).move_to(LEFT * 0.3 + UP * 0.85)
        kt1 = T("y = a×x + y", 20, AMBER, BOLD, MONO).move_to(kb.get_center() + UP * 0.35)
        kt2 = T("3×2 + 1 = 7", 20, TEXT_MAIN, BOLD, MONO).move_to(kb.get_center() + DOWN * 0.3)
        ob = VGroup(R(1.5, 0.8, EMERALD), T("y[i] = 7", 18, EMERALD, BOLD, MONO)); ob[1].move_to(ob[0]); ob.move_to(RIGHT * 4.9 + UP * 0.85)
        a1 = Arrow(xb.get_right(), kb.get_left() + UP * 0.35, color=CYAN, buff=0.1, stroke_width=4)
        a2 = Arrow(yb.get_right(), kb.get_left() + DOWN * 0.35, color=VIOLET, buff=0.1, stroke_width=4)
        a3 = Arrow(kb.get_right(), ob.get_left(), color=EMERALD, buff=0.1, stroke_width=4)
        l1 = T("đọc 4 B", 15, CYAN, BOLD).next_to(a1, UP, buff=0.05).shift(LEFT * 0.2)
        l2 = T("đọc 4 B", 15, VIOLET, BOLD).next_to(a2, DOWN, buff=0.05).shift(LEFT * 0.2)
        l3 = T("ghi 4 B", 15, EMERALD, BOLD).next_to(a3, UP, buff=0.05)
        tot = T("12 B mỗi phần tử", 18, TEXT_MAIN, BOLD).move_to(UP * 2.3)
        f = T("BW = 3 × 4 B × 2²⁶ ÷ 1,84 ms", 22, AMBER, BOLD, MONO, maxw=11).move_to(DOWN * 1.9)
        f2 = T("≈ 805 MB ÷ 1,84 ms ≈ 438 GB/s", 22, EMERALD, BOLD, MONO, maxw=11).move_to(DOWN * 2.7)
        toks = [Square(0.22, stroke_width=0, fill_color=c, fill_opacity=1) for c in (CYAN, VIOLET)]
        toks[0].move_to(xb.get_right()); toks[1].move_to(yb.get_right())
        otok = Square(0.22, stroke_width=0, fill_color=EMERALD, fill_opacity=1).move_to(kb.get_right())
        play_voiced(self, "04_13", [
            ([FadeIn(hdr), FadeIn(xb), FadeIn(yb), FadeIn(kb), FadeIn(kt1)], 1.2),
            ([GrowArrow(a1), GrowArrow(a2), FadeIn(l1), FadeIn(l2)], 1.0),
            ([FadeIn(toks[0]), FadeIn(toks[1])], 0.2),
            ([toks[0].animate.move_to(kb.get_left() + UP * 0.35), toks[1].animate.move_to(kb.get_left() + DOWN * 0.35)], 1.0),
            ([FadeOut(toks[0]), FadeOut(toks[1]), FadeIn(kt2)], 0.6),
            ([GrowArrow(a3), FadeIn(l3), FadeIn(ob), FadeIn(otok)], 1.0),
            ([otok.animate.move_to(ob.get_left())], 0.8),
            ([FadeIn(tot)], 0.6),
            ([FadeIn(f)], 1.2),
            ([FadeIn(f2)], 1.2),
        ])
        clear_stage(self)

    # 04_14 power wall
    def s14(self):
        hdr = make_header("Bức tường công suất của CPU", "công suất ~ f × V²", CORAL)
        form = T("P ~ f × V²", 32, AMBER, BOLD, MONO).move_to(LEFT * 3.4 + UP * 1.9)
        c1 = T("f × 1,25 và V × 0,9", 20, TEXT_MAIN, BOLD, MONO, maxw=5.6)
        c2 = T("1,25 × 0,9² = 1,25 × 0,81", 20, CYAN, BOLD, MONO, maxw=5.6)
        c3 = T("≈ 1,01: gần như không đổi", 20, EMERALD, BOLD, MONO, maxw=5.6)
        c4 = T("V hết đường giảm: f × 2 → P × 2", 20, CORAL, BOLD, MONO, maxw=5.6)
        cs = VGroup(c1, c2, c3, c4).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(LEFT * 3.4 + DOWN * 0.3)
        chart = make_bar_chart([1, 1.01, 2], ["Gốc", "f ×1,25\nV ×0,9", "f ×2\nV cố định"],
                               [CYAN, EMERALD, CORAL], 2.4, width=5.6, height=3.0, unit="×")
        chart.move_to(RIGHT * 3.4 + DOWN * 0.5)
        k = key("Hết đường tăng xung → thêm nhân", AMBER)
        play_voiced(self, "04_14", [
            ([FadeIn(hdr), FadeIn(form)], 1.0),
            ([FadeIn(c1)], 1.0),
            ([FadeIn(chart[0]), FadeIn(chart[1]), FadeIn(chart[2][0], shift=UP * 0.2)], 1.2),
            ([FadeIn(c2)], 1.2),
            ([FadeIn(c3), FadeIn(chart[2][1], shift=UP * 0.2)], 1.4),
            ([FadeIn(c4), FadeIn(chart[2][2], shift=UP * 0.2)], 1.6),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_15 function qualifiers
    def s15(self):
        hdr = make_header("__global__, __device__, __host__", "ai gọi · chạy ở đâu", VIOLET)
        host = R(4.8, 3.6, CYAN, op=0.35, r=0.14).move_to(LEFT * 3.6 + UP * 0.05)
        dev = R(5.6, 3.6, EMERALD, op=0.35, r=0.14).move_to(RIGHT * 3.4 + UP * 0.05)
        ht = T("CPU (host)", 17, CYAN, BOLD).move_to(host.get_top() + DOWN * 0.28)
        dt = T("GPU (device)", 17, EMERALD, BOLD).move_to(dev.get_top() + DOWN * 0.28)

        def box(txt, col, pos, w=2.1):
            b = VGroup(R(w, 0.62, col, r=0.08), T(txt, 16, TEXT_MAIN, BOLD, MONO, maxw=w - 0.2))
            b[1].move_to(b[0]); b.move_to(pos)
            return b
        main = box("main()", CYAN, LEFT * 4.8 + UP * 0.8)
        hfn = box("hàm host", CYAN, LEFT * 4.8 + DOWN * 0.8)
        ker = box("kernel", EMERALD, RIGHT * 2.0 + UP * 0.8)
        hlp = box("hàm phụ", EMERALD, RIGHT * 2.0 + DOWN * 0.8)
        a_g = Arrow(main.get_right(), ker.get_left(), color=AMBER, buff=0.08, stroke_width=5)
        l_g = T("__global__ · trả về void", 15, AMBER, BOLD, MONO, maxw=3.3).next_to(a_g, UP, buff=0.12)
        a_d = Arrow(ker.get_bottom(), hlp.get_top(), color=VIOLET, buff=0.08, stroke_width=4)
        l_d = T("__device__", 15, VIOLET, BOLD, MONO).next_to(a_d, RIGHT, buff=0.15)
        a_h = Arrow(main.get_bottom(), hfn.get_top(), color=CYAN, buff=0.08, stroke_width=4)
        l_h = T("__host__", 15, CYAN, BOLD, MONO).next_to(a_h, RIGHT, buff=0.15)
        k = key("__host__ __device__: dùng được ở cả hai phía", AMBER)
        play_voiced(self, "04_15", [
            ([FadeIn(hdr), FadeIn(host), FadeIn(dev), FadeIn(ht), FadeIn(dt)], 1.0),
            ([FadeIn(main), FadeIn(ker)], 0.8),
            ([GrowArrow(a_g), FadeIn(l_g)], 1.4),
            ([FadeIn(hlp), GrowArrow(a_d), FadeIn(l_d)], 1.4),
            ([FadeIn(hfn), GrowArrow(a_h), FadeIn(l_h)], 1.4),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_16 TH2 index patterns
    def s16(self):
        hdr = make_header("TH2: ba kernel ghi mảng 16 phần tử", "chỉ số luồng", CYAN)
        pal = [CYAN, AMBER, EMERALD, VIOLET]

        def row(vals, y, colvals=None):
            g = VGroup()
            for i, v in enumerate(vals):
                col = pal[(colvals if colvals else vals)[i] % 4]
                c = C(0.62, 0.5, col, 0.85)
                t = T(str(v), 17, "#0D1117", BOLD, MONO).move_to(c)
                g.add(VGroup(c, t))
            g.arrange(RIGHT, buff=0.04).move_to(RIGHT * 0.75 + UP * y)
            return g
        idx = VGroup(*[T(str(i), 14, TEXT_MUTED, NORMAL, MONO).move_to(RIGHT * (0.75 + 0.66 * (i - 7.5)) + UP * 1.55) for i in range(16)])
        li = T("idx", 15, TEXT_MUTED, BOLD, MONO).move_to(LEFT * 5.55 + UP * 1.55)
        head1 = T("kernel<<<4, 4>>>(a)", 22, AMBER, BOLD, MONO).move_to(UP * 2.25)
        head2 = T("kernel<<<2, 8>>>(a)", 22, AMBER, BOLD, MONO).move_to(UP * 2.25)
        r7 = row([7] * 16, 0.85, [3] * 16)
        r7.set_color(WHITE)
        r7 = row([7] * 16, 0.85, [i // 4 for i in range(16)])
        rb = row([i // 4 for i in range(16)], 0.1)
        rt = row([i % 4 for i in range(16)], -0.65)
        rb2 = row([i // 8 for i in range(16)], 0.1)
        rt2 = row([i % 8 for i in range(16)], -0.65)
        l7 = T("a = 7", 15, TEXT_MAIN, BOLD, MONO).move_to(LEFT * 5.55 + UP * 0.85)
        lb = T("blockIdx", 15, TEXT_MAIN, BOLD, MONO).move_to(LEFT * 5.55 + UP * 0.1)
        lt = T("threadIdx", 15, TEXT_MAIN, BOLD, MONO).move_to(LEFT * 5.55 + DOWN * 0.65)
        k1 = key("Mọi luồng chạy cùng mã; idx = blockIdx × blockDim + threadIdx", AMBER)
        k2 = key("Dự đoán trước khi chạy: 2 block × 8 luồng", EMERALD)
        play_voiced(self, "04_16", [
            ([FadeIn(hdr), FadeIn(head1), FadeIn(idx), FadeIn(li)], 1.0),
            ([FadeIn(l7), FadeIn(r7)], 1.2),
            ([FadeIn(lb), FadeIn(rb)], 1.6),
            ([FadeIn(lt), FadeIn(rt)], 1.6),
            ([FadeIn(k1)], 0.8),
            ([ReplacementTransform(head1, head2), FadeOut(k1)], 0.8),
            ([ReplacementTransform(rb, rb2)], 1.4),
            ([ReplacementTransform(rt, rt2), FadeIn(k2)], 1.4),
        ])
        clear_stage(self)

    # 04_17 residency limits
    def s17(self):
        hdr = make_header("Một SM chứa được mấy block?", "Fermi · 48 thanh ghi", AMBER)
        sc_ = 10.0 / 32768
        x0 = -5.0
        yr = 0.95
        reg = Rectangle(width=10.0, height=0.8, stroke_color=TEXT_MUTED, stroke_width=2, fill_opacity=0).move_to(RIGHT * 0.0 + UP * yr)
        lr = T("Thanh ghi: 32.768 mỗi SM", 17, CYAN, BOLD).move_to(LEFT * 3.4 + UP * (yr + 0.8))
        w = 12288 * sc_
        bl = []
        for i in range(3):
            fillc = CYAN if i < 2 else CORAL
            b = Rectangle(width=w, height=0.8, stroke_color=fillc, stroke_width=2,
                          fill_color=fillc, fill_opacity=0.7 if i < 2 else 0.15)
            b.move_to(RIGHT * (x0 + w * (i + 0.5)) + UP * yr)
            bl.append(b)
        t0 = T("block 0 · 12.288", 15, "#0D1117", BOLD, maxw=w - 0.2).move_to(bl[0])
        t1 = T("block 1 · 12.288", 15, "#0D1117", BOLD, maxw=w - 0.2).move_to(bl[1])
        t2 = T("block 2: 36.864 > 32.768 ✗", 15, CORAL, BOLD, maxw=3.4).next_to(bl[2], DOWN, buff=0.12)
        eq = T("48 × 256 = 12.288 / block", 18, TEXT_MAIN, BOLD, MONO, maxw=6).move_to(RIGHT * 3.2 + UP * (yr + 0.8))
        yt = -1.15
        thr = Rectangle(width=10.0, height=0.8, stroke_color=TEXT_MUTED, stroke_width=2, fill_opacity=0).move_to(UP * yt)
        slots = VGroup(*[C(10.0 / 6, 0.8, BORDER_DIM, 0.12, stroke=TEXT_MUTED, sw=1.2) for _ in range(6)]).arrange(RIGHT, buff=0).move_to(UP * yt)
        lt = T("Luồng: 1536 mỗi SM = 6 block × 256", 17, EMERALD, BOLD).move_to(LEFT * 2.6 + UP * (yt + 0.8))
        used = VGroup(slots[0].copy().set_fill(EMERALD, 0.8).set_stroke(EMERALD), slots[1].copy().set_fill(EMERALD, 0.8).set_stroke(EMERALD))
        ut = T("512 / 1536 dùng", 16, EMERALD, BOLD).next_to(thr, DOWN, buff=0.12).align_to(thr, LEFT)
        k = key("min(2, 6) = 2 block → nút thắt là thanh ghi", AMBER)
        play_voiced(self, "04_17", [
            ([FadeIn(hdr), FadeIn(reg), FadeIn(lr), FadeIn(thr), FadeIn(slots), FadeIn(lt)], 1.2),
            ([FadeIn(eq)], 1.2),
            ([FadeIn(bl[0]), FadeIn(t0), FadeIn(bl[1]), FadeIn(t1)], 1.6),
            ([FadeIn(bl[2]), FadeIn(t2)], 1.6),
            ([FadeIn(used), FadeIn(ut)], 1.6),
            ([FadeIn(k)], 0.8),
        ])
        clear_stage(self)

    # 04_18 block scalability
    def s18(self):
        hdr = make_header("Block độc lập: tự mở rộng theo số SM", "8 block × T", EMERALD)
        src = VGroup()
        for i in range(8):
            c = C(0.5, 0.42, AMBER, 0.9)
            t = T(str(i), 14, "#0D1117", BOLD, MONO).move_to(c)
            src.add(VGroup(c, t))
        src.arrange(RIGHT, buff=0.1).move_to(UP * 2.25)
        pl = R(5.4, 2.7, CYAN, op=0.25, r=0.12).move_to(LEFT * 3.2 + DOWN * 0.15)
        pr = R(5.4, 2.7, EMERALD, op=0.25, r=0.12).move_to(RIGHT * 3.2 + DOWN * 0.15)
        tl = T("GPU 2 SM", 17, CYAN, BOLD).next_to(pl, UP, buff=0.1)
        tr = T("GPU 4 SM", 17, EMERALD, BOLD).next_to(pr, UP, buff=0.1)

        def slot_at(cx0, ry, col):
            return RIGHT * (cx0 + 0.66 * col) + UP * ry
        slotsL = []; slotsR = []
        grpL = VGroup(); grpR = VGroup()
        for r_ in range(2):
            ry = 0.35 - 0.7 * r_
            grpL.add(T("SM%d" % r_, 14, TEXT_MUTED, BOLD, MONO).move_to(LEFT * 5.35 + UP * ry))
            for c_ in range(4):
                s = C(0.58, 0.45, BORDER_DIM, 0.15, stroke=TEXT_MUTED, sw=1.0).move_to(slot_at(-4.5, ry, c_))
                grpL.add(s); slotsL.append((r_, c_, s))
        for r_ in range(4):
            ry = 0.85 - 0.6 * r_
            grpR.add(T("SM%d" % r_, 14, TEXT_MUTED, BOLD, MONO).move_to(RIGHT * 1.05 + UP * ry))
            for c_ in range(2):
                s = C(0.58, 0.45, BORDER_DIM, 0.15, stroke=TEXT_MUTED, sw=1.0).move_to(slot_at(2.0, ry, c_))
                grpR.add(s); slotsR.append((r_, c_, s))
        tL = T("tổng: 4T", 22, CYAN, BOLD, MONO).move_to(LEFT * 3.2 + DOWN * 1.9)
        tR = T("tổng: 2T", 22, EMERALD, BOLD, MONO).move_to(RIGHT * 3.2 + DOWN * 1.9)
        # blocks go to slots: i -> row i%R, col i//R
        cl = [src[i].copy() for i in range(8)]
        cr = [src[i].copy() for i in range(8)]
        dl = [slotsL[(i % 2) * 4 + (i // 2)][2].get_center() for i in range(8)]
        dr = [slotsR[(i % 4) * 2 + (i // 4)][2].get_center() for i in range(8)]
        k1 = key("Không cần sửa mã: thêm SM là chạy nhanh hơn", EMERALD)
        k2 = key("2²⁶ phần tử: 262.144 block, 276 block/lượt → ≥ 950 lượt", AMBER)
        play_voiced(self, "04_18", [
            ([FadeIn(hdr), FadeIn(src)], 1.0),
            ([FadeIn(pl), FadeIn(tl), FadeIn(grpL)], 1.0),
            ([LaggedStart(*[cl[i].animate.move_to(dl[i]) for i in range(8)], lag_ratio=0.12)], 2.4),
            ([FadeIn(tL)], 0.6),
            ([FadeIn(pr), FadeIn(tr), FadeIn(grpR)], 1.0),
            ([LaggedStart(*[cr[i].animate.move_to(dr[i]) for i in range(8)], lag_ratio=0.12)], 2.4),
            ([FadeIn(tR), FadeIn(k1)], 0.8),
            ([ReplacementTransform(k1, k2)], 1.2),
        ])
        clear_stage(self)

    # 04_19 cudaMemcpy kinds and PCIe slot
    def s19(self):
        hdr = make_header("cudaMemcpy: ba chiều chép", "dst trước, src sau", CYAN)
        sig = T("cudaMemcpy(dst, src, bytes, kind)", 22, AMBER, BOLD, MONO, maxw=11).move_to(UP * 2.2)
        host = R(2.6, 1.8, CYAN, r=0.12).move_to(LEFT * 4.6 + UP * 0.2)
        da = R(2.4, 1.8, EMERALD, r=0.12).move_to(RIGHT * 0.8 + UP * 0.2)
        db = R(2.4, 1.8, VIOLET, r=0.12).move_to(RIGHT * 5.0 + UP * 0.2)
        nh = T("host\n(RAM)", 17, CYAN, BOLD).move_to(host)
        na_ = T("d_a\n(GPU)", 17, EMERALD, BOLD).move_to(da)
        nb = T("d_b\n(GPU)", 17, VIOLET, BOLD).move_to(db)
        a1 = Arrow(host.get_right() + UP * 0.45, da.get_left() + UP * 0.45, color=CYAN, buff=0.08, stroke_width=4)
        a2 = Arrow(da.get_left() + DOWN * 0.45, host.get_right() + DOWN * 0.45, color=AMBER, buff=0.08, stroke_width=4)
        a3 = Arrow(da.get_right(), db.get_left(), color=VIOLET, buff=0.08, stroke_width=4)
        l1 = T("HostToDevice", 14, CYAN, BOLD, MONO, maxw=2.3).next_to(a1, UP, buff=0.08)
        l2 = T("DeviceToHost", 14, AMBER, BOLD, MONO, maxw=2.3).next_to(a2, DOWN, buff=0.08)
        l3 = T("DeviceToDevice", 13, VIOLET, BOLD, MONO, maxw=1.7).next_to(a3, UP, buff=0.08)
        k1 = key("Chặn CPU cho đến khi chép xong mọi byte", CORAL)
        diag = VGroup(sig, host, da, db, nh, na_, nb, a1, a2, a3, l1, l2, l3)
        c1 = make_bar_chart([26.8, 0.8], ["PCIe x16", "PCIe x1"], [EMERALD, CORAL], 30, width=4.6, height=2.8, unit="GB/s")
        c1.move_to(LEFT * 3.3 + DOWN * 0.3)
        c2 = make_bar_chart([10, 336], ["PCIe x16", "PCIe x1"], [EMERALD, CORAL], 380, width=4.6, height=2.8, unit="ms")
        c2.move_to(RIGHT * 3.3 + DOWN * 0.3)
        t1 = T("tốc độ chép", 18, CYAN, BOLD).move_to(LEFT * 3.3 + UP * 1.9)
        t2 = T("chép 256 MiB", 18, AMBER, BOLD).move_to(RIGHT * 3.3 + UP * 1.9)
        k2 = key("Khe x1 chậm hơn khoảng 33 lần", CORAL)
        play_voiced(self, "04_19", [
            ([FadeIn(hdr), FadeIn(sig), FadeIn(host), FadeIn(da), FadeIn(db), FadeIn(nh), FadeIn(na_), FadeIn(nb)], 1.2),
            ([GrowArrow(a1), FadeIn(l1)], 1.0),
            ([GrowArrow(a2), FadeIn(l2)], 1.0),
            ([GrowArrow(a3), FadeIn(l3)], 1.0),
            ([FadeIn(k1)], 1.0),
            ([FadeOut(diag), FadeOut(k1)], 0.5),
            ([FadeIn(t1), FadeIn(c1[0]), FadeIn(c1[1]), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in c1[2]], lag_ratio=0.5)], 1.8),
            ([FadeIn(t2), FadeIn(c2[0]), FadeIn(c2[1]), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in c2[2]], lag_ratio=0.5), FadeIn(k2)], 2.0),
        ])
        clear_stage(self)

    # 04_20 optimization appendix
    def s20(self):
        hdr = make_header("Phụ lục tối ưu: mức tăng tốc", "RTX 4070", AMBER)
        vals = [36, 151, 14.9, 7.7, 8.9]
        labs = ["block_size\n1 → 92 block", "reduction\natomic → tốt nhất", "pi\nfloat vs double",
                "matmul\ncuBLAS vs OpenBLAS", "Jacobi 2D\nGPU vs MPI"]
        cols = [CYAN, EMERALD, VIOLET, AMBER, CORAL]
        chart = make_bar_chart(vals, labs, cols, 165, width=11.6, height=3.4, unit="×")
        chart.move_to(DOWN * 0.45)
        dets = ["12 → 433 GB/s", "88,9 → 0,59 ms", "58 → 3,9 ms", "2930 → 22.591 GFLOP/s", "1,021 → 0,115 s"]
        dt = [T(s, 22, cols[i], BOLD, MONO).move_to(UP * 2.3) for i, s in enumerate(dets)]
        steps = [([FadeIn(hdr), FadeIn(chart[0]), FadeIn(chart[1])], 1.0)]
        for i in range(5):
            a = [FadeIn(chart[2][i], shift=UP * 0.2)]
            if i == 0:
                a.append(FadeIn(dt[0]))
            else:
                a.append(ReplacementTransform(dt[i - 1], dt[i]))
            steps.append((a, 1.8))
        play_voiced(self, "04_20", steps)
        clear_stage(self)

    # 04_21 nvcc compilation
    def s21(self):
        hdr = make_header("Biên dịch bằng nvcc", "-arch chọn thế hệ GPU", VIOLET)

        def box(txt, col, pos, w, h=0.9, size=17):
            b = VGroup(R(w, h, col, r=0.1), T(txt, size, TEXT_MAIN, BOLD, MONO, maxw=w - 0.2))
            b[1].move_to(b[0]); b.move_to(pos)
            return b
        f = box("saxpy.cu", AMBER, LEFT * 5.5 + UP * 0.7, 2.0)
        n = box("nvcc", VIOLET, LEFT * 2.6 + UP * 0.7, 1.6)
        h = box("mã host → g++", CYAN, RIGHT * 0.5 + UP * 1.5, 3.4, 0.8, 16)
        g = box("kernel → mã GPU", EMERALD, RIGHT * 0.5 + DOWN * 0.1, 3.4, 0.8, 16)
        e = box("saxpy\nCPU + GPU", AMBER, RIGHT * 4.9 + UP * 0.7, 2.4, 1.1, 16)
        a1 = Arrow(f.get_right(), n.get_left(), color=TEXT_MUTED, buff=0.08, stroke_width=4)
        a2 = Arrow(n.get_right(), h.get_left(), color=CYAN, buff=0.08, stroke_width=4)
        a3 = Arrow(n.get_right(), g.get_left(), color=EMERALD, buff=0.08, stroke_width=4)
        a4 = Arrow(h.get_right(), e.get_left() + UP * 0.2, color=CYAN, buff=0.08, stroke_width=4)
        a5 = Arrow(g.get_right(), e.get_left() + DOWN * 0.2, color=EMERALD, buff=0.08, stroke_width=4)
        cmd = T("nvcc -O2 -arch=native saxpy.cu -o saxpy", 22, TEXT_MAIN, BOLD, MONO, maxw=11).move_to(DOWN * 1.5)
        p1 = VGroup(R(3.6, 0.6, EMERALD, r=0.1), T("sm_89 · RTX 4070", 16, EMERALD, BOLD, MONO)); p1[1].move_to(p1[0]); p1.move_to(LEFT * 2.3 + DOWN * 2.5)
        p2 = VGroup(R(3.6, 0.6, CYAN, r=0.1), T("sm_75 · RTX 2070", 16, CYAN, BOLD, MONO)); p2[1].move_to(p2[0]); p2.move_to(RIGHT * 2.3 + DOWN * 2.5)
        play_voiced(self, "04_21", [
            ([FadeIn(hdr), FadeIn(f)], 0.8),
            ([GrowArrow(a1), FadeIn(n)], 1.0),
            ([GrowArrow(a2), FadeIn(h), GrowArrow(a3), FadeIn(g)], 1.6),
            ([GrowArrow(a4), GrowArrow(a5), FadeIn(e)], 1.6),
            ([FadeIn(cmd)], 1.0),
            ([FadeIn(p1), FadeIn(p2)], 1.4),
        ])
        clear_stage(self)
