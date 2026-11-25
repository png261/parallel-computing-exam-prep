from manim import *
from scene_utils import *
from scene_utils import play_module_drills
import heapq

TH = [CYAN, AMBER, EMERALD, VIOLET]
DARK = "#0D1117"
PINK = "#F472B6"
ORANGE = "#FB923C"
TEAL = "#2DD4BF"
EIGHT = [CYAN, AMBER, EMERALD, VIOLET, CORAL, PINK, ORANGE, TEAL]


def tx(s, size=20, color=TEXT_MAIN, font=None, bold=False, maxw=None):
    t = Text(s, font=font or SANS, font_size=size, color=color, weight=BOLD if bold else NORMAL)
    if maxw and t.width > maxw:
        t.scale_to_fit_width(maxw)
    return t


def mono(s, size=20, color=TEXT_MAIN, maxw=None, bold=False):
    return tx(s, size, color, MONO, bold, maxw)


def rbox(w, h, color=BORDER_DIM, fill=PANEL_BG, sw=2, r=0.1, op=0.95):
    return RoundedRectangle(width=w, height=h, corner_radius=r, stroke_color=color,
                            stroke_width=sw, fill_color=fill, fill_opacity=op)


def labeled(s, w, h, color, size=18, font=None, textcolor=TEXT_MAIN, bold=False):
    b = rbox(w, h, color)
    t = tx(s, size, textcolor, font, bold, maxw=w - 0.2)
    t.move_to(b)
    return VGroup(b, t)


def tok(s, color, w=0.55, h=0.42, size=20):
    b = rbox(w, h, color, fill=color, op=1, r=0.08, sw=1)
    t = mono(s, size, DARK, bold=True)
    t.move_to(b)
    return VGroup(b, t)


def AM(m, f):
    return ApplyFunction(f, m)


def fly(m, target, rt=0.8):
    return [([FadeIn(m, scale=0.8)], 0.25), ([AM(m, lambda _m: _m.move_to(target))], rt)]


class Scene02SharedMem(Scene):
    def setcap(self, s, color=TEXT_MAIN, size=22):
        new = tx(s, size, color, bold=True, maxw=12.2).move_to(DOWN * 3.05)
        if self.cap is None:
            a = FadeIn(new, shift=UP * 0.1)
        else:
            a = ReplacementTransform(self.cap, new)
        self.cap = new
        return a

    def construct(self):
        setup_bg(self)
        for fn in [self.seg_01, self.seg_02, self.seg_03, self.seg_09, self.seg_04, self.seg_05, self.seg_06, self.seg_10, self.seg_07, self.seg_11, self.seg_12, self.seg_16, self.seg_17, self.seg_18, self.seg_19, self.seg_20, self.seg_21, self.seg_22, self.seg_24, self.seg_25, self.seg_26, self.seg_27, self.seg_28, self.seg_29, self.seg_30, self.seg_31]:
            self.cap = None
            fn()
            clear_stage(self)
        play_module_drills(self, "M2", "C++ threads / OpenMP")

    # ------------------------------------------------------------ 02_01
    def seg_01(self):
        hdr = make_header("Ngăn xếp phần mềm luồng", "Linux", CYAN)
        cx = -1.9
        ys = [1.85, 0.65, -0.55, -1.75]
        a = labeled("std::jthread", 3.5, 0.85, CYAN, 20, MONO)
        b = labeled("OpenMP", 3.5, 0.85, AMBER, 20, MONO)
        VGroup(a, b).arrange(RIGHT, buff=0.2).move_to(RIGHT * cx + UP * ys[0])
        l2 = labeled("POSIX threads (glibc)", 7.2, 0.85, VIOLET, 20).move_to(RIGHT * cx + UP * ys[1])
        l3 = labeled("clone3 / futex", 7.2, 0.85, EMERALD, 20, MONO).move_to(RIGHT * cx + UP * ys[2])
        l4 = labeled("Nhân Linux", 7.2, 0.85, CORAL, 20).move_to(RIGHT * cx + UP * ys[3])
        arrows = VGroup(*[Arrow(UP * (ys[i] - 0.45) + RIGHT * cx, UP * (ys[i + 1] + 0.45) + RIGHT * cx,
                                buff=0, color=TEXT_MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.5)
                          for i in range(3)])
        cores = VGroup(*[rbox(1.1, 1.1, BORDER_DIM) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.2)
        cores.move_to(RIGHT * 4.5 + UP * 0.2)
        cl = tx("4 lõi CPU", 18, TEXT_MUTED).next_to(cores, DOWN, buff=0.15)
        karr = Arrow(l4.get_right(), cores.get_bottom() + DOWN * 0.1 + LEFT * 0.4, buff=0.1, color=TEXT_MUTED)
        karr = Arrow(l4.get_right(), cores.get_left() + DOWN * 0.3, buff=0.1, color=TEXT_MUTED, stroke_width=3)
        d1 = Dot(color=CYAN, radius=0.14).move_to(a.get_center())
        d2 = Dot(color=AMBER, radius=0.14).move_to(b.get_center())
        steps = [
            ([FadeIn(a), FadeIn(b)], 0.8),
            ([FadeIn(l2, shift=UP * 0.1), GrowArrow(arrows[0])], 0.7),
            ([FadeIn(l3, shift=UP * 0.1), GrowArrow(arrows[1])], 0.7),
            ([FadeIn(l4, shift=UP * 0.1), GrowArrow(arrows[2])], 0.7),
            ([FadeIn(cores), FadeIn(cl), GrowArrow(karr)], 0.8),
            ([FadeIn(d1), FadeIn(d2)], 0.3),
            ([AM(d1, lambda _m: _m.move_to(l2.get_center() + LEFT * 1.0)), AM(d2, lambda _m: _m.move_to(l2.get_center() + RIGHT * 1.0))], 1.0),
            ([AM(d1, lambda _m: _m.move_to(l3.get_center() + LEFT * 1.0)), AM(d2, lambda _m: _m.move_to(l3.get_center() + RIGHT * 1.0))], 1.0),
            ([AM(d1, lambda _m: _m.move_to(l4.get_center() + LEFT * 1.0)), AM(d2, lambda _m: _m.move_to(l4.get_center() + RIGHT * 1.0))], 1.0),
            ([AM(d1, lambda _m: _m.move_to(cores[0])), AM(d2, lambda _m: _m.move_to(cores[3]))], 1.0),
            ([AM(cores[0][0], lambda _m: _m.set_fill(CYAN, 0.6).set_stroke(CYAN)), AM(cores[3][0], lambda _m: _m.set_fill(AMBER, 0.6).set_stroke(AMBER)),
              self.setcap("Cả hai đều đi qua pthread", AMBER)], 0.8),
        ]
        steps.insert(0, ([FadeIn(hdr)], 0.5))
        play_voiced(self, "02_01", steps)

    # ------------------------------------------------------------ 02_02
    def seg_02(self):
        hdr = make_header("thread và jthread", "C++11 vs C++20", AMBER)
        rows = [1.05, -1.35]
        names = ["std::thread (C++11)", "std::jthread (C++20)"]
        lab = [tx(n, 22, c, MONO, True).move_to(LEFT * 6.4 + UP * (y + 0.75), aligned_edge=LEFT)
               for n, y, c in zip(names, rows, [CORAL, EMERALD])]
        mains = [Rectangle(width=6.0, height=0.34, fill_color=CYAN, fill_opacity=0.9, stroke_width=0)
                 .move_to(RIGHT * (-5.5 + 3.0) + UP * y) for y in rows]
        thr = [Rectangle(width=8.4, height=0.34, fill_color=AMBER, fill_opacity=0.9, stroke_width=0)
               .move_to(RIGHT * (-4.4 + 4.2) + UP * (y - 0.55)) for y in rows]
        ml = [tx("main", 16, DARK, bold=True).move_to(m) for m in mains]
        tl = [tx("luồng t", 16, DARK, bold=True).move_to(t) for t in thr]
        scope = [DashedLine(RIGHT * 0.5 + UP * (y + 0.5), RIGHT * 0.5 + UP * (y - 1.0), color=TEXT_MAIN, stroke_width=2.5)
                 for y in rows]
        sl = [tx("hết phạm vi }", 17, TEXT_MUTED).next_to(s, UP, buff=0.05).shift(RIGHT * 0.5) for s in scope]
        # row 1: crash
        cut = Rectangle(width=4.1, height=0.34, fill_color=CORAL, fill_opacity=0.9, stroke_width=0).move_to(
            RIGHT * (0.5 + 2.05) + UP * (rows[0] - 0.55))
        bang = tx("terminate()!", 24, CORAL, MONO, True).move_to(RIGHT * 3.3 + UP * (rows[0] + 0.2))
        xmark = VGroup(Line(UL * 0.25, DR * 0.25, color=CORAL, stroke_width=7), Line(UR * 0.25, DL * 0.25, color=CORAL, stroke_width=7)).move_to(RIGHT * 0.9 + UP * (rows[0] - 0.55))
        # row 2: join
        wait = Rectangle(width=4.0, height=0.34, fill_color=VIOLET, fill_opacity=0.9, stroke_width=0).move_to(
            RIGHT * (0.5 + 2.0) + UP * rows[1])
        wl = tx("tự động join", 16, DARK, bold=True).move_to(wait)
        check = tx("✓", 40, EMERALD, bold=True).move_to(RIGHT * 5.4 + UP * (rows[1] - 0.2))
        steps = [
            ([FadeIn(hdr)], 0.4),
            ([FadeIn(lab[0]), FadeIn(lab[1])], 0.6),
            ([GrowFromEdge(mains[0], LEFT), GrowFromEdge(mains[1], LEFT), FadeIn(ml[0]), FadeIn(ml[1])], 0.9),
            ([GrowFromEdge(thr[0], LEFT), GrowFromEdge(thr[1], LEFT), FadeIn(tl[0]), FadeIn(tl[1])], 1.0),
            ([Create(scope[0]), Create(scope[1]), FadeIn(sl[0]), FadeIn(sl[1])], 0.9),
            ([FadeIn(xmark, scale=2.0), AM(thr[0], lambda _m: _m.set_fill(CORAL)), FadeIn(bang)], 1.0),
            ([Indicate(xmark, color=CORAL), self.setcap("Quên join → chương trình crash", CORAL)], 0.8),
            ([GrowFromEdge(wait, LEFT), FadeIn(wl)], 1.2),
            ([FadeIn(check, scale=2.0), self.setcap("jthread: hàm hủy tự join", EMERALD)], 0.8),
        ]
        play_voiced(self, "02_02", steps)

    # ------------------------------------------------------------ 02_03
    def seg_03(self):
        hdr = make_header("Data race: mất một cập nhật", "counter++", CORAL)
        form = tx("counter++  =  đọc → cộng 1 → ghi", 22, AMBER, bold=True, maxw=11).move_to(UP * 2.2)
        cbox = rbox(2.6, 1.1, CYAN).move_to(UP * 0.1)
        cname = tx("counter", 18, TEXT_MUTED).next_to(cbox, UP, buff=0.1)
        cval = mono("5", 40, CYAN, bold=True).move_to(cbox)
        tbs = []
        regs = []
        for x, nm, col in [(-4.6, "Thread 1", AMBER), (4.6, "Thread 2", VIOLET)]:
            b = rbox(2.4, 1.9, col).move_to(RIGHT * x + UP * 0.1)
            t = tx(nm, 20, col, bold=True).move_to(b.get_top() + DOWN * 0.4)
            reg = mono("r = _", 26).move_to(b.get_center() + DOWN * 0.3)
            tbs.append(VGroup(b, t))
            regs.append(reg)
        rp = [r.get_center() for r in regs]
        t1 = tok("5", AMBER).move_to(cbox)
        t2 = tok("5", VIOLET).move_to(cbox)
        w1 = tok("6", AMBER).move_to(regs[0])
        w2 = tok("6", VIOLET).move_to(regs[1])
        r1 = mono("r = 5", 26, AMBER).move_to(rp[0])
        r2 = mono("r = 5", 26, VIOLET).move_to(rp[1])
        r1b = mono("r = 6", 26, AMBER).move_to(rp[0])
        r2b = mono("r = 6", 26, VIOLET).move_to(rp[1])
        cval6 = mono("6", 40, CYAN, bold=True).move_to(cbox)
        steps = [
            ([FadeIn(hdr)], 0.4),
            ([FadeIn(cbox), FadeIn(cname), FadeIn(cval), *[FadeIn(g) for g in tbs], *[FadeIn(r) for r in regs], FadeIn(form)], 1.0),
        ]
        steps += fly(t1, rp[0] + UP * 0.0, 0.8)
        steps += [([FadeOut(t1), ReplacementTransform(regs[0], r1), self.setcap("Thread 1 đọc 5", AMBER)], 0.4)]
        steps += fly(t2, rp[1], 0.8)
        steps += [([FadeOut(t2), ReplacementTransform(regs[1], r2), self.setcap("Thread 2 cũng đọc 5", VIOLET)], 0.4)]
        steps += [([ReplacementTransform(r1, r1b), ReplacementTransform(r2, r2b), self.setcap("Cả hai cùng tính ra 6")], 0.8)]
        w1.move_to(rp[0]); w2.move_to(rp[1])
        steps += [([FadeIn(w1)], 0.2), ([AM(w1, lambda _m: _m.move_to(cbox))], 0.7),
                  ([FadeOut(w1), ReplacementTransform(cval, cval6), self.setcap("Thread 1 ghi 6", AMBER)], 0.4)]
        steps += [([FadeIn(w2)], 0.2), ([AM(w2, lambda _m: _m.move_to(cbox))], 0.7),
                  ([FadeOut(w2), Indicate(cval6, color=CORAL, scale_factor=1.4), AM(cbox, lambda _m: _m.set_stroke(CORAL, 4)),
                    self.setcap("Thread 2 ghi 6 đè lên: đáng lẽ phải là 7!", CORAL)], 0.9)]
        play_voiced(self, "02_03", steps)

    # ------------------------------------------------------------ 02_09
    def seg_09(self):
        hdr = make_header("Sửa data race: chi phí", "4 luồng × 10 triệu", EMERALD)
        vol = labeled("volatile: mất 60–70%", 4.2, 0.7, CORAL, 20, bold=True).move_to(LEFT * 4.2 + UP * 1.6)
        chart = make_bar_chart([1.399, 0.210, 0.002], ["mutex", "atomic", "biến cục bộ"],
                               [CORAL, AMBER, EMERALD], 1.5, width=7.0, height=3.9, unit="s")
        chart.move_to(RIGHT * 2.0 + DOWN * 0.1)
        bars = chart[2]
        for g in bars:
            g[0].save_state()
        ico = VGroup(*[Dot(radius=0.13, color=TH[i]) for i in range(4)]).arrange(RIGHT, buff=0.2)
        tgt = rbox(1.4, 0.7, CYAN)
        lockrow = VGroup(ico, Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=TEXT_MUTED, stroke_width=3), tgt).arrange(RIGHT, buff=0.25)
        tcnt = mono("counter", 18, CYAN).move_to(tgt)
        lockrow.move_to(LEFT * 4.2 + DOWN * 0.3)
        tcnt.move_to(lockrow[2])
        mrg = tx("700×", 40, EMERALD, bold=True).move_to(LEFT * 4.2 + DOWN * 1.9)
        mrg2 = tx("nhanh hơn mutex", 20, TEXT_MUTED).next_to(mrg, DOWN, buff=0.1)
        steps = [
            ([FadeIn(hdr)], 0.4),
            ([FadeIn(vol)], 0.7),
            ([FadeIn(lockrow), FadeIn(tcnt)], 0.8),
            ([FadeIn(chart[0]), FadeIn(chart[1])], 0.5),
            ([FadeIn(bars[0], shift=UP * 0.3)], 1.0),
            ([FadeIn(bars[1], shift=UP * 0.3)], 1.0),
            ([FadeIn(bars[2], shift=UP * 0.3)], 1.0),
            ([FadeIn(mrg), FadeIn(mrg2), Indicate(bars[2][0], color=EMERALD)], 1.0),
        ]
        play_voiced(self, "02_09", steps)

    # ------------------------------------------------------------ 02_04
    def seg_04(self):
        hdr = make_header("atomic hay mutex?", "bất biến 2 biến", AMBER)
        inv = tx("bất biến:  sum = 2 × count", 24, AMBER, bold=True).move_to(UP * 2.4)
        cb = rbox(2.6, 1.2, CYAN).move_to(LEFT * 1.8 + UP * 0.2)
        sb = rbox(2.6, 1.2, EMERALD).move_to(RIGHT * 1.8 + UP * 0.2)
        cn = tx("count", 18, TEXT_MUTED).next_to(cb, UP, buff=0.08)
        sn = tx("sum", 18, TEXT_MUTED).next_to(sb, UP, buff=0.08)
        cv = mono("3", 38, CYAN, bold=True).move_to(cb)
        sv = mono("6", 38, EMERALD, bold=True).move_to(sb)
        wr = labeled("Writer", 1.8, 0.9, AMBER, 20, bold=True).move_to(LEFT * 5.3 + UP * 0.2)
        rd = labeled("Reader", 1.8, 0.9, VIOLET, 20, bold=True).move_to(RIGHT * 5.3 + UP * 0.2)
        wa1 = Arrow(wr.get_right(), cb.get_left(), buff=0.1, color=AMBER, stroke_width=4)
        wa2 = CurvedArrow(wr.get_top() + UP * 0.05, sb.get_top() + UP * 0.05, angle=-TAU / 10, color=AMBER, stroke_width=4)
        ra = DoubleArrow(rd.get_left(), sb.get_right(), buff=0.1, color=VIOLET, stroke_width=3)
        ra2 = CurvedArrow(rd.get_bottom() + DOWN * 0.05, cb.get_bottom() + DOWN * 0.05, angle=-TAU / 6, color=VIOLET, stroke_width=3)
        cv4 = mono("4", 38, CYAN, bold=True).move_to(cb)
        sv8 = mono("8", 38, EMERALD, bold=True).move_to(sb)
        seen = mono("thấy 4 và 6  →  6 ≠ 8", 22, CORAL, bold=True).move_to(DOWN * 1.9)
        lock = rbox(7.0, 1.9, AMBER, fill=DARK, sw=4, op=0.0).move_to(UP * 0.2)
        lk = tx("std::scoped_lock", 18, AMBER, MONO, True).next_to(lock, DOWN, buff=0.08)
        steps = [
            ([FadeIn(hdr)], 0.4),
            ([FadeIn(inv), FadeIn(cb), FadeIn(sb), FadeIn(cn), FadeIn(sn), FadeIn(cv), FadeIn(sv), FadeIn(wr), FadeIn(rd)], 1.0),
            ([GrowArrow(wa1)], 0.6),
            ([ReplacementTransform(cv, cv4)], 0.6),
            ([GrowArrow(ra), Create(ra2)], 0.8),
            ([FadeIn(seen, shift=UP * 0.1), AM(cb, lambda _m: _m.set_stroke(CORAL, 4)), AM(sb, lambda _m: _m.set_stroke(CORAL, 4))], 1.2),
            ([FadeOut(ra), FadeOut(ra2), FadeOut(seen), Create(wa2)], 0.7),
            ([ReplacementTransform(sv, sv8), AM(cb, lambda _m: _m.set_stroke(CYAN, 2)), AM(sb, lambda _m: _m.set_stroke(EMERALD, 2))], 0.7),
            ([FadeOut(wa1), FadeOut(wa2), FadeIn(lock), FadeIn(lk), self.setcap("mutex bảo vệ cả hai cùng lúc", AMBER)], 1.0),
            ([AM(lock, lambda _m: _m.set_stroke(EMERALD, 4)), AM(lk, lambda _m: _m.set_color(EMERALD))], 0.5),
        ]
        play_voiced(self, "02_04", steps)

    # ------------------------------------------------------------ 02_05
    def seg_05(self):
        hdr = make_header("False sharing", "alignas(64)", CORAL)
        step0 = 0.8
        cols = VGroup()
        for i in range(8):
            ol = Rectangle(width=step0, height=1.0, stroke_color=AMBER, stroke_width=1.5, fill_opacity=0)
            cell = rbox(0.66, 0.6, EIGHT[i], op=1.0, sw=2.5)
            cl = mono(f"c{i}", 16, TEXT_MAIN).move_to(cell)
            line = Line(UP * 0.0, DOWN * 0.9, color=BORDER_DIM, stroke_width=2).next_to(ol, DOWN, buff=0)
            core = rbox(0.7, 0.5, EIGHT[i], fill=PANEL_BG, sw=2).next_to(line, DOWN, buff=0)
            ct = mono(f"T{i}", 15, EIGHT[i], bold=True).move_to(core)
            g = VGroup(ol, VGroup(cell, cl), line, VGroup(core, ct))
            g.move_to(RIGHT * ((i - 3.5) * step0) + UP * 0.3)
            cols.add(g)
        big = RoundedRectangle(width=8 * step0 + 0.15, height=1.2, corner_radius=0.08, stroke_color=AMBER,
                               stroke_width=4, fill_opacity=0).move_to(UP * 0.3 + cols.get_center()[0] * RIGHT)
        big.set_y(cols[0][0].get_center()[1])
        bl = tx("1 cache line = 64 byte", 20, AMBER, bold=True).next_to(big, UP, buff=0.15)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(cols, lag_ratio=0.1), Create(big), FadeIn(bl)], 1.4)]
        for w in (0, 5, 2, 7):
            others = [cols[j][1][0] for j in range(8) if j != w]
            steps.append(([Indicate(cols[w][1], color=AMBER, scale_factor=1.3),
                           *[Indicate(o, color=CORAL, scale_factor=1.0) for o in others]], 0.9))
        steps.append(([self.setcap("8 luồng, 1 line: chậm 20× (0,719 s)", CORAL)], 0.6))
        pad_cap_label = tx("mỗi ô một line riêng", 20, EMERALD, bold=True).move_to(bl)
        moves = [AM(cols[i], lambda _m, i=i: _m.set_x((i - 3.5) * 1.5)) for i in range(8)]
        steps.append(([FadeOut(big), ReplacementTransform(bl, pad_cap_label), *moves], 1.4))
        steps.append(([FadeToColor(cols[i][0], EMERALD) for i in range(8)] +
                      [self.setcap("Padding 64 byte: hết bouncing", EMERALD)], 0.8))
        play_voiced(self, "02_05", steps)

    # ------------------------------------------------------------ 02_06
    def seg_06(self):
        hdr = make_header("OpenMP: fork–join & dữ liệu", "parallel", CYAN)
        m1 = Rectangle(width=2.8, height=0.3, fill_color=CYAN, fill_opacity=0.95, stroke_width=0).move_to(LEFT * 4.6 + UP * 0.2)
        m2 = Rectangle(width=2.8, height=0.3, fill_color=CYAN, fill_opacity=0.95, stroke_width=0).move_to(RIGHT * 4.6 + UP * 0.2)
        ys = [1.5, 0.7, -0.1, -0.9]
        lanes = [Rectangle(width=5.2, height=0.3, fill_color=TH[i], fill_opacity=0.95, stroke_width=0).move_to(UP * y) for i, y in enumerate(ys)]
        lt = [tx(f"T{i}", 16, DARK, bold=True).move_to(lanes[i].get_left() + RIGHT * 0.4) for i in range(4)]
        fk = tx("fork", 22, AMBER, bold=True).move_to(LEFT * 3.0 + DOWN * 1.8)
        jn = tx("join", 22, AMBER, bold=True).move_to(RIGHT * 3.0 + DOWN * 1.8)
        fl = VGroup(*[Line(LEFT * 3.2 + UP * 0.2, LEFT * 2.6 + UP * y, color=TEXT_MUTED, stroke_width=2) for y in ys])
        jl = VGroup(*[Line(RIGHT * 2.6 + UP * y, RIGHT * 3.2 + UP * 0.2, color=TEXT_MUTED, stroke_width=2) for y in ys])
        bar = DashedLine(RIGHT * 2.6 + UP * 2.0, RIGHT * 2.6 + DOWN * 1.4, color=AMBER, stroke_width=2.5)
        partA = Group(m1, m2, *lanes, *lt, fk, jn, fl, jl, bar)

        mode = tx("private(x)", 24, CYAN, MONO, True).move_to(UP * 2.2)
        xb = rbox(1.8, 1.4, TEXT_MUTED).move_to(LEFT * 5.0 + UP * 0.2)
        xn = tx("x ngoài", 18, TEXT_MUTED).move_to(xb.get_top() + DOWN * 0.3)
        xv = mono("10", 34, TEXT_MAIN, bold=True).move_to(xb.get_center() + DOWN * 0.2)
        tbs = []
        for i, cx in enumerate([-1.6, 0.6, 2.8, 5.0]):
            b_ = rbox(1.9, 1.7, TH[i]).move_to(RIGHT * cx + UP * 0.2)
            t_ = tx(f"T{i}", 20, TH[i], bold=True).move_to(b_.get_top() + DOWN * 0.3)
            tbs.append(VGroup(b_, t_))
        cur = [mono("?", 34, TEXT_MUTED, bold=True).move_to(tbs[i][0].get_center() + DOWN * 0.25) for i in range(4)]

        def sv(strs, cols):
            out = []
            for i in range(4):
                n = mono(strs[i], 34, cols[i], bold=True).move_to(tbs[i][0].get_center() + DOWN * 0.25)
                out.append(ReplacementTransform(cur[i], n))
                cur[i] = n
            return out

        def mk(m, col):
            return Transform(mode, tx(m, 24, col, MONO, True).move_to(UP * 2.2))
        x13 = mono("13", 34, EMERALD, bold=True).move_to(xv)
        arrow13 = Arrow(tbs[3][0].get_bottom() + DOWN * 0.0, xb.get_bottom() + DOWN * 0.0, buff=0.1, color=EMERALD, stroke_width=4)
        arrow13 = CurvedArrow(tbs[3][0].get_bottom() + DOWN * 0.05, xb.get_bottom() + DOWN * 0.05, angle=-TAU / 5, color=EMERALD, stroke_width=4)
        steps = [([FadeIn(hdr)], 0.4),
                 ([GrowFromEdge(m1, LEFT)], 0.7),
                 ([Create(fl), *[GrowFromEdge(l, LEFT) for l in lanes], *[FadeIn(t) for t in lt], FadeIn(fk)], 1.2),
                 ([Create(bar)], 0.5),
                 ([Create(jl), GrowFromEdge(m2, LEFT), FadeIn(jn)], 1.0),
                 ([FadeOut(partA)], 0.5),
                 ([FadeIn(mode), FadeIn(xb), FadeIn(xn), FadeIn(xv), *[FadeIn(t) for t in tbs], *[FadeIn(c) for c in cur]], 0.9),
                 ([Indicate(c, color=CORAL) for c in cur] + [self.setcap("private: bản sao rỗng, x ngoài vẫn 10", TEXT_MAIN)], 1.2),
                 ([mk("firstprivate(x)", AMBER)] + sv(["10"] * 4, [AMBER] * 4), 1.0),
                 (sv(["10", "11", "12", "13"], TH) + [self.setcap("firstprivate: mỗi bản sao bắt đầu từ 10", AMBER)], 1.2),
                 ([mk("lastprivate(x)", EMERALD), Indicate(xv, color=TEXT_MAIN)], 0.8),
                 ([Create(arrow13), ReplacementTransform(xv, x13), AM(tbs[3][0], lambda _m: _m.set_stroke(EMERALD, 4)),
                   self.setcap("lastprivate: vòng lặp cuối ghi về x = 13", EMERALD)], 1.2),
                 ]
        play_voiced(self, "02_06", steps)

    # ------------------------------------------------------------ 02_10
    def seg_10(self):
        hdr = make_header("reduction: tổng 1 đến 8", "reduction(+:sum)", EMERALD)
        cells = VGroup(*[tok(str(i + 1), TH[i // 2], 0.9, 0.6, 26) for i in range(8)]).arrange(RIGHT, buff=0.3).move_to(UP * 1.9)
        lcx = [(cells[2 * k].get_center()[0] + cells[2 * k + 1].get_center()[0]) / 2 for k in range(4)]
        part = []
        for k, v in enumerate([3, 7, 11, 15]):
            b = labeled(f"T{k}: {v}", 2.0, 0.7, TH[k], 24, MONO, bold=True).move_to(RIGHT * lcx[k] + UP * 0.5)
            part.append(b)
        arr1 = [VGroup(*[Arrow(cells[2 * k + j].get_bottom(), part[k].get_top() + RIGHT * (0.3 if j else -0.3), buff=0.08,
                               color=TH[k], stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for j in range(2)]) for k in range(4)]
        m1 = labeled("10", 1.3, 0.7, TEXT_MAIN, 26, MONO, bold=True).move_to(RIGHT * (lcx[0] + lcx[1]) / 2 + DOWN * 0.8)
        m2 = labeled("26", 1.3, 0.7, TEXT_MAIN, 26, MONO, bold=True).move_to(RIGHT * (lcx[2] + lcx[3]) / 2 + DOWN * 0.8)
        fin = labeled("sum = 36", 3.0, 0.9, EMERALD, 30, MONO, bold=True).move_to(DOWN * 2.1)
        a2 = [Arrow(part[0].get_bottom(), m1.get_top() + LEFT * 0.2, buff=0.08, color=TEXT_MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3),
              Arrow(part[1].get_bottom(), m1.get_top() + RIGHT * 0.2, buff=0.08, color=TEXT_MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3),
              Arrow(part[2].get_bottom(), m2.get_top() + LEFT * 0.2, buff=0.08, color=TEXT_MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3),
              Arrow(part[3].get_bottom(), m2.get_top() + RIGHT * 0.2, buff=0.08, color=TEXT_MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3)]
        a3 = [Arrow(m1.get_bottom(), fin.get_top() + LEFT * 0.5, buff=0.08, color=TEXT_MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3),
              Arrow(m2.get_bottom(), fin.get_top() + RIGHT * 0.5, buff=0.08, color=TEXT_MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3)]
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(cells, lag_ratio=0.15)], 1.4),
                 ([FadeIn(part[k]) for k in range(4)] + [Create(a) for a in arr1], 1.4),
                 ([self.setcap("Mỗi luồng cộng vào bản sao riêng", TEXT_MAIN)], 0.5),
                 ([FadeIn(m1), FadeIn(m2), *[Create(a) for a in a2]], 1.2),
                 ([FadeIn(fin, scale=1.2), *[Create(a) for a in a3]], 1.2),
                 ([self.setcap("Không khóa, tăng tốc 7,9× (critical: chậm 176×)", EMERALD)], 0.8)]
        play_voiced(self, "02_10", steps)

    # ------------------------------------------------------------ 02_07
    def seg_07(self):
        hdr = make_header("Lập lịch vòng lặp", "16 vòng, 4 luồng", AMBER)
        cw = 0.5
        x0 = -3.9
        ys = [1.85, 0.65, -0.55, -1.75]
        names = ["static", "static,1", "dynamic", "guided"]
        asg = [
            [i // 4 for i in range(16)],
            [i % 4 for i in range(16)],
            [0, 1, 2, 3, 2, 0, 1, 3, 1, 2, 0, 3, 0, 1, 3, 2],
            None,
        ]
        g = []
        for sz, t in zip([4, 3, 3, 2, 1, 1, 1, 1], [0, 1, 2, 3, 0, 1, 2, 3]):
            g += [t] * sz
        asg[3] = g
        rows = []
        labs = []
        for r in range(4):
            lb = tx(names[r], 20, TEXT_MAIN, MONO, True, maxw=2.3).move_to(LEFT * 6.4 + UP * ys[r], aligned_edge=LEFT)
            labs.append(lb)
            cs = VGroup()
            for i in range(16):
                c = tok(str(i + 1), TH[asg[r][i]], cw - 0.03, 0.5, 14)
                c.move_to(RIGHT * (x0 + cw * (i + 0.5)) + UP * ys[r])
                cs.add(c)
            rows.append(cs)
        leg = VGroup(*[VGroup(Square(0.22, fill_color=TH[i], fill_opacity=1, stroke_width=0), tx(f"T{i}", 18, TH[i], bold=True)).arrange(RIGHT, buff=0.12) for i in range(4)]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 5.6 + UP * 0.1)
        notes = [("khối liên tục", CYAN), ("xoay vòng: lệch tải số nguyên tố", CORAL), ("ai rảnh thì nhận", EMERALD), ("khối nhỏ dần", AMBER)]
        steps = [([FadeIn(hdr)], 0.4), ([FadeIn(leg)], 0.5)]
        caps = [("static: mỗi luồng một khối liên tục", CYAN),
                ("static,1: chia xoay vòng từng vòng lặp", AMBER),
                ("dynamic: luồng nào rảnh thì nhận tiếp", EMERALD),
                ("guided: khối to dần nhỏ lại", VIOLET)]
        for r in range(4):
            steps.append(([FadeIn(labs[r]), FadeIn(rows[r], lag_ratio=0.06), self.setcap(*caps[r])], 1.5))
        play_voiced(self, "02_07", steps)

    # ------------------------------------------------------------ 02_11
    def seg_11(self):
        hdr = make_header("Tải tăng dần: dynamic thắng", "chi phí vòng i = i", AMBER)
        u = 0.5
        x0 = -3.8
        costs = list(range(1, 9))
        sched1 = []
        free = [0, 0, 0, 0]
        for i, c in enumerate(costs):
            t = i // 2
            sched1.append((t, free[t], c, i + 1))
            free[t] += c
        mk1 = max(free)
        sched2 = []
        free = [0, 0, 0, 0]
        for i, c in enumerate(costs):
            t = free.index(min(free))
            sched2.append((t, free[t], c, i + 1))
            free[t] += c
        mk2 = max(free)

        def panel(sched, ytop):
            gr = VGroup()
            for (t, s, c, it) in sched:
                r = Rectangle(width=c * u - 0.03, height=0.38, fill_color=TH[t], fill_opacity=0.95, stroke_color=DARK, stroke_width=1)
                r.move_to(RIGHT * (x0 + u * s + c * u / 2) + UP * (ytop - 0.45 * t))
                lb = mono(str(it), 15, DARK, bold=True).move_to(r)
                gr.add(VGroup(r, lb))
            return gr
        p1 = panel(sched1, 1.55)
        p2 = panel(sched2, -0.8)
        l1 = tx("static", 22, CORAL, MONO, True).move_to(LEFT * 6.4 + UP * 0.9, aligned_edge=LEFT)
        l2 = tx("dynamic,1", 22, EMERALD, MONO, True, maxw=2.0).move_to(LEFT * 6.4 + DOWN * 1.45, aligned_edge=LEFT)
        f1 = DashedLine(RIGHT * (x0 + u * mk1) + UP * 1.9, RIGHT * (x0 + u * mk1) + DOWN * 0.1, color=CORAL, stroke_width=3)
        f2 = DashedLine(RIGHT * (x0 + u * mk2) + DOWN * 0.45, RIGHT * (x0 + u * mk2) + DOWN * 2.5, color=EMERALD, stroke_width=3)
        t1 = tx(f"xong lúc {mk1}", 22, CORAL, bold=True).next_to(f1, RIGHT, buff=0.1).shift(UP * 0.5)
        t2 = tx(f"xong lúc {mk2}", 22, EMERALD, bold=True).next_to(f2, RIGHT, buff=0.1).shift(UP * 0.5)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(l1), FadeIn(p1, lag_ratio=0.15)], 2.0),
                 ([Create(f1), FadeIn(t1), self.setcap("static: T3 gánh hết việc nặng", CORAL)], 1.0),
                 ([FadeIn(l2), FadeIn(p2, lag_ratio=0.15)], 2.0),
                 ([Create(f2), FadeIn(t2), self.setcap("dynamic: cân bằng, xong sớm hơn", EMERALD)], 1.0)]
        play_voiced(self, "02_11", steps)

    # ------------------------------------------------------------ 02_12
    def seg_12(self):
        hdr = make_header("OpenMP task: fib(4)", "task / taskwait", VIOLET)
        spec = {
            "f4": ((0, 1.9), None, CYAN, 3),
            "f3": ((-2.6, 0.8), "f4", CYAN, 2),
            "f2r": ((2.6, 0.8), "f4", AMBER, 1),
            "f2l": ((-4.0, -0.3), "f3", EMERALD, 1),
            "f1a": ((-1.4, -0.3), "f3", VIOLET, 1),
            "f1b": ((1.3, -0.3), "f2r", AMBER, 1),
            "f0b": ((3.9, -0.3), "f2r", CYAN, 0),
            "f1c": ((-5.0, -1.4), "f2l", EMERALD, 1),
            "f0c": ((-3.0, -1.4), "f2l", EMERALD, 0),
        }
        nodes = {}
        edges = {}
        for k, ((x, y), par, col, v) in spec.items():
            c = Circle(radius=0.38, stroke_color=col, stroke_width=3, fill_color=PANEL_BG, fill_opacity=1).move_to(RIGHT * x + UP * y)
            t = mono("f" + k[1], 20, col, bold=True).move_to(c)
            nodes[k] = VGroup(c, t)
        for k, ((x, y), par, col, v) in spec.items():
            if par:
                edges[k] = Line(nodes[par][0].get_center(), nodes[k][0].get_center(), color=BORDER_DIM, stroke_width=2.5, buff=0.38) if False else \
                    Line(nodes[par][0].get_bottom() * 0 + nodes[par][0].get_center(), nodes[k][0].get_center(), color=TEXT_MUTED, stroke_width=2.5, z_index=-1)
        order = [["f4"], ["f3", "f2r"], ["f2l", "f1a", "f1b", "f0b"], ["f1c", "f0c"]]
        steps = [([FadeIn(hdr)], 0.4)]
        for lv in order:
            an = []
            for k in lv:
                an.append(FadeIn(nodes[k], scale=0.6))
                if k in edges:
                    an.append(Create(edges[k]))
            steps.append((an, 0.9))
        steps.append(([self.setcap("Mỗi lời gọi sinh một task", VIOLET)], 0.5))
        # values bottom-up
        valorder = [["f1c", "f0c", "f1a", "f1b", "f0b"], ["f2l", "f2r"], ["f3"], ["f4"]]
        for lv in valorder:
            an = []
            for k in lv:
                v = spec[k][3]
                n = mono(str(v), 26, EMERALD, bold=True).move_to(nodes[k][1])
                an.append(ReplacementTransform(nodes[k][1], n))
                an.append(AM(nodes[k][0], lambda _m: _m.set_stroke(EMERALD, 4)))
            steps.append((an, 0.9))
        steps.append(([self.setcap("taskwait: chờ con rồi cộng", EMERALD)], 0.6))
        deep = [AM(nodes[k][0], lambda _m: _m.set_fill("#2A2F3A", 1).set_stroke(TEXT_MUTED, 3)) for k in ["f2l", "f1a", "f1b", "f0b", "f1c", "f0c"]]
        steps.append((deep + [self.setcap("cutoff: nhánh nhỏ chạy tuần tự", AMBER)], 1.0))
        play_voiced(self, "02_12", steps)





    # ------------------------------------------------------------ 02_16
    def seg_16(self):
        hdr = make_header("Lambda bắt chỉ số vòng lặp", "[&] vs [&, k]", CORAL)
        bad = make_code_box(["for (int k = 0; k < 4; k++)", "  th.emplace_back([&] { dung(k); });"],
                            7.2, 18, CORAL, "Sai: k bắt theo tham chiếu").move_to(UP * 1.65)
        good = make_code_box(["for (int k = 0; k < 4; k++)", "  th.emplace_back([&, k] { dung(k); });"],
                             7.2, 18, EMERALD, "Đúng: k bắt theo giá trị").move_to(UP * 1.65)
        kb = rbox(2.2, 1.4, CYAN).move_to(LEFT * 3.8 + DOWN * 0.6)
        kn = tx("biến k (một ô duy nhất)", 17, TEXT_MUTED).next_to(kb, UP, buff=0.1)
        kv = mono("0", 40, CYAN, bold=True).move_to(kb)
        ys = [0.1, -0.5, -1.1, -1.7]
        thr = [labeled(f"T{i}", 1.3, 0.5, TH[i], 18, bold=True).move_to(RIGHT * 0.6 + UP * ys[i]) for i in range(4)]
        arr = [Arrow(thr[i].get_left(), kb.get_right() + UP * (0.45 - 0.3 * i), buff=0.08, color=CORAL,
                     stroke_width=3, max_tip_length_to_length_ratio=0.15) for i in range(4)]
        vals = [mono("k = ?", 20, TEXT_MUTED).move_to(RIGHT * 3.2 + UP * ys[i]) for i in range(4)]
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(bad)], 0.8),
                 ([FadeIn(kb), FadeIn(kn), FadeIn(kv), *[FadeIn(t) for t in thr], *[FadeIn(v) for v in vals]], 0.8),
                 ([*[GrowArrow(a) for a in arr]], 0.8)]
        for n in (1, 2, 3, 4):
            nv = mono(str(n), 40, CYAN if n < 4 else CORAL, bold=True).move_to(kb)
            steps.append(([ReplacementTransform(kv, nv)], 0.4))
            kv = nv
        v4 = [mono("k = 4 ✗", 20, CORAL, bold=True).move_to(vals[i]) for i in range(4)]
        steps.append(([*[ReplacementTransform(vals[i], v4[i]) for i in range(4)], AM(kb, lambda _m: _m.set_stroke(CORAL, 4))], 0.9))
        v0 = [mono(f"k = {i} ✓", 20, TH[i], bold=True).move_to(v4[i]) for i in range(4)]
        steps.append(([ReplacementTransform(bad, good), *[FadeOut(a) for a in arr],
                       *[ReplacementTransform(v4[i], v0[i]) for i in range(4)],
                       AM(kb, lambda _m: _m.set_stroke(CYAN, 2)),
                       self.setcap("Chỉ số vòng lặp: bắt theo giá trị", EMERALD)], 1.2))
        play_voiced(self, "02_16", steps)

    # ------------------------------------------------------------ 02_17
    def seg_17(self):
        hdr = make_header("Đo thời gian: clock() sai", "wall time", AMBER)
        u = 0.8
        x0 = -6.0
        lanes = [Rectangle(width=2 * u, height=0.36, fill_color=TH[i], fill_opacity=0.95, stroke_width=0)
                 .move_to(RIGHT * (x0 + u) + UP * (1.7 - 0.5 * i)) for i in range(4)]
        ll = [tx(f"T{i}: 2 s", 16, DARK, bold=True).move_to(lanes[i]) for i in range(4)]
        brace = Brace(VGroup(*lanes), RIGHT, color=AMBER, buff=0.12)
        wall = tx("thời gian thực (real) = 2 s", 19, AMBER, bold=True).next_to(brace, RIGHT, buff=0.15)
        sumbar = VGroup(*[Rectangle(width=2 * u, height=0.36, fill_color=TH[i], fill_opacity=0.95, stroke_width=0)
                          .move_to(RIGHT * (x0 + u + 2 * u * i) + DOWN * 0.7) for i in range(4)])
        sl = tx("clock() = tổng CPU = 8 s", 19, CORAL, bold=True).next_to(sumbar, DOWN, buff=0.15).align_to(sumbar, LEFT)
        c1 = labeled("clock(): 8 / 8 = 1,0 → tưởng không tăng tốc", 6.0, 0.62, CORAL, 18, bold=True).move_to(RIGHT * 3.2 + DOWN * 1.65)
        c2 = labeled("steady_clock / omp_get_wtime: 8 / 2 = 4", 6.0, 0.62, EMERALD, 18, bold=True).move_to(RIGHT * 3.2 + DOWN * 2.45)
        steps = [([FadeIn(hdr)], 0.4),
                 ([*[GrowFromEdge(l, LEFT) for l in lanes], *[FadeIn(t) for t in ll]], 1.2),
                 ([GrowFromCenter(brace), FadeIn(wall)], 0.8),
                 ([FadeIn(sumbar, lag_ratio=0.25), FadeIn(sl)], 1.4),
                 ([FadeIn(c1, shift=UP * 0.1)], 0.9),
                 ([FadeIn(c2, shift=UP * 0.1), self.setcap("Đo song song: dùng đồng hồ thực, không dùng clock()", AMBER)], 1.0)]
        play_voiced(self, "02_17", steps)

    # ------------------------------------------------------------ 02_18
    def seg_18(self):
        hdr = make_header("single, masked, barrier", "OpenMP 5.1", VIOLET)
        x0, ys = -5.0, [1.3, 0.55, -0.2, -0.95]
        lanes = [DashedLine(RIGHT * x0 + UP * y, RIGHT * 5.6 + UP * y, color=BORDER_DIM, stroke_width=1.5) for y in ys]
        ln = [tx(f"T{i}", 18, TH[i], bold=True).move_to(RIGHT * -5.7 + UP * ys[i]) for i in range(4)]

        def blk(i, xa, xb, col, op=0.95, lab=None):
            r = Rectangle(width=xb - xa, height=0.4, fill_color=col, fill_opacity=op, stroke_width=0).move_to(RIGHT * (xa + xb) / 2 + UP * ys[i])
            return r

        def vline(x, col):
            return DashedLine(RIGHT * x + UP * 1.75, RIGHT * x + DOWN * 1.35, color=col, stroke_width=3)
        # pha 1: single
        s_work = blk(2, -4.9, -3.3, AMBER)
        s_wait = [blk(i, -4.9, -3.3, "#2A2F3A", 0.9) for i in (0, 1, 3)]
        s_lab = mono("single", 20, AMBER, bold=True).move_to(RIGHT * -4.1 + UP * 2.2)
        s_bar = vline(-3.2, AMBER)
        s_bl = tx("rào chắn ngầm", 15, AMBER).move_to(RIGHT * -3.2 + DOWN * 1.65)
        # pha 2: masked
        m_work = blk(0, -2.9, -1.3, EMERALD)
        m_go = [blk(i, -2.9, -1.3, TH[i], 0.55) for i in (1, 2, 3)]
        m_lab = mono("masked", 20, EMERALD, bold=True).move_to(RIGHT * -2.1 + UP * 2.2)
        m_note = tx("chỉ luồng 0, các luồng khác không chờ", 15, EMERALD).move_to(RIGHT * -1.6 + DOWN * 2.15)
        # pha 3: barrier
        lens = [1.4, 0.7, 1.1, 0.9]
        b_work = [blk(i, -1.1, -1.1 + lens[i], TH[i], 0.85) for i in range(4)]
        b_wait = [blk(i, -1.1 + lens[i], 0.5, "#2A2F3A", 0.9) for i in range(4)]
        b_lab = mono("barrier", 20, VIOLET, bold=True).move_to(RIGHT * -0.3 + UP * 2.2)
        b_bar = vline(0.6, VIOLET)
        b_bl = tx("chờ đủ 4 luồng", 15, VIOLET).move_to(RIGHT * 0.6 + DOWN * 1.65)
        after = [blk(i, 0.8, 2.0, TH[i], 0.95) for i in range(4)]
        steps = [([FadeIn(hdr)], 0.4),
                 ([*[Create(l) for l in lanes], *[FadeIn(t) for t in ln]], 0.8),
                 ([FadeIn(s_lab), GrowFromEdge(s_work, LEFT), *[GrowFromEdge(w, LEFT) for w in s_wait]], 1.0),
                 ([Create(s_bar), FadeIn(s_bl)], 0.7),
                 ([FadeIn(m_lab), GrowFromEdge(m_work, LEFT), *[GrowFromEdge(w, LEFT) for w in m_go], FadeIn(m_note)], 1.1),
                 ([FadeIn(b_lab), *[GrowFromEdge(w, LEFT) for w in b_work]], 1.0),
                 ([*[GrowFromEdge(w, LEFT) for w in b_wait], Create(b_bar), FadeIn(b_bl)], 0.9),
                 ([*[GrowFromEdge(w, LEFT) for w in after]], 0.8),
                 ([self.setcap("master đã lỗi thời từ OpenMP 5.1: dùng masked", VIOLET)], 0.6)]
        play_voiced(self, "02_18", steps)

    # ------------------------------------------------------------ 02_19
    def seg_19(self):
        hdr = make_header("task: biến mặc định là firstprivate", "task / taskwait", VIOLET)
        lines = ["#pragma omp parallel + single", "#pragma omp task", "right = sum(a, mid, hi);",
                 "#pragma omp taskwait", "return left + right;"]
        ys = [1.75, 0.95, 0.15, -0.65, -1.45]
        chips = [labeled(s, 5.6, 0.58, c, 16, MONO).move_to(LEFT * 3.6 + UP * y)
                 for s, y, c in zip(lines, ys, [TEXT_MUTED, VIOLET, TEXT_MUTED, AMBER, TEXT_MUTED])]
        pb = rbox(2.4, 1.3, CYAN).move_to(RIGHT * 4.2 + UP * 1.2)
        pn = tx("left của luồng cha", 16, TEXT_MUTED).next_to(pb, UP, buff=0.08)
        pv_ = mono("?", 36, CYAN, bold=True).move_to(pb)
        tb = rbox(2.4, 1.3, VIOLET).move_to(RIGHT * 4.2 + DOWN * 1.1)
        tn = tx("bản sao trong task", 16, TEXT_MUTED).next_to(tb, DOWN, buff=0.08)
        tv = mono("?", 36, VIOLET, bold=True).move_to(tb)
        copyarr = Arrow(pb.get_bottom(), tb.get_top(), buff=0.08, color=VIOLET, stroke_width=3)
        cl = tx("sao chép", 15, VIOLET).next_to(copyarr, RIGHT, buff=0.1)
        pv6 = mono("?", 36, CORAL, bold=True).move_to(pb)
        tv6 = mono("6", 36, VIOLET, bold=True).move_to(tb)
        bad = tx("left vẫn ?  → kết quả sai", 18, CORAL, bold=True).move_to(RIGHT * 1.3 + DOWN * 0.0)
        shared_chip = labeled("#pragma omp task shared(left)", 5.6, 0.58, EMERALD, 16, MONO).move_to(chips[1])
        sh_arr = Arrow(chips[1].get_right(), pb.get_left(), buff=0.1, color=EMERALD, stroke_width=4)
        pv_ok = mono("6", 36, EMERALD, bold=True).move_to(pb)
        wait_note = tx("chờ task con xong rồi mới return", 16, AMBER, bold=True).next_to(chips[3], RIGHT, buff=0.25)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(chips[0]), FadeIn(chips[1]), FadeIn(chips[2])], 0.9),
                 ([FadeIn(pb), FadeIn(pn), FadeIn(pv_)], 0.6),
                 ([GrowArrow(copyarr), FadeIn(tb), FadeIn(tn), FadeIn(tv), FadeIn(cl)], 0.9),
                 ([ReplacementTransform(tv, tv6), Indicate(chips[1], color=VIOLET)], 0.8),
                 ([ReplacementTransform(pv_, pv6), AM(pb, lambda _m: _m.set_stroke(CORAL, 4)), FadeIn(bad)], 0.9),
                 ([FadeOut(bad), FadeOut(copyarr), FadeOut(cl), FadeOut(tb), FadeOut(tn), FadeOut(tv6),
                   ReplacementTransform(chips[1], shared_chip)], 0.9),
                 ([GrowArrow(sh_arr), ReplacementTransform(pv6, pv_ok), AM(pb, lambda _m: _m.set_stroke(EMERALD, 4))], 0.9),
                 ([FadeIn(chips[3]), FadeIn(chips[4]), FadeIn(wait_note)], 0.9),
                 ([Indicate(chips[3], color=AMBER), self.setcap("Quên shared → task ghi vào bản sao", CORAL)], 0.8)]
        play_voiced(self, "02_19", steps)

    # ------------------------------------------------------------ 02_20
    def seg_20(self):
        hdr = make_header("Phương trình nhiệt 2D", "collapse(2) · barrier", EMERALD)
        n, cs = 8, 0.38
        cells = VGroup()
        for r in range(n):
            for c in range(n):
                sq = Square(side_length=cs, stroke_color=BORDER_DIM, stroke_width=1, fill_color=TH[r // 2], fill_opacity=0.35)
                sq.move_to(LEFT * 4.1 + RIGHT * (c - 3.5) * cs + UP * (0.3 - (r - 3.5) * cs))
                cells.add(sq)
        bands = [tx(f"T{i}", 16, TH[i], bold=True).move_to(LEFT * 6.0 + UP * (0.3 - (2 * i + 0.5 - 3.5) * cs)) for i in range(4)]
        ctr = 3 * n + 4
        cross = VGroup(*[cells[ctr + d].copy().set_fill(AMBER, 0.9).set_stroke(AMBER, 3) for d in (0, -1, 1, -n, n)])
        st = tx("5 điểm: giữa + 4 lân cận", 17, AMBER, bold=True).move_to(LEFT * 4.1 + DOWN * 2.15)
        omp = labeled("OpenMP: collapse(2) gộp vòng i, j", 5.2, 0.55, AMBER, 16, bold=True).move_to(RIGHT * 3.4 + UP * 2.1)
        cpp = labeled("C++: mỗi jthread một khối hàng", 5.2, 0.55, CYAN, 16, bold=True).move_to(RIGHT * 3.4 + UP * 1.4)
        ub = labeled("u", 1.5, 0.7, CYAN, 22, MONO, bold=True).move_to(RIGHT * 2.2 + UP * 0.1)
        nb = labeled("unew", 1.5, 0.7, EMERALD, 22, MONO, bold=True).move_to(RIGHT * 4.9 + UP * 0.1)
        comp = Arrow(ub.get_right(), nb.get_left(), buff=0.08, color=TEXT_MUTED, stroke_width=3)
        dots = [Dot(radius=0.16, color=TH[i]).move_to(RIGHT * (1.6 + 0.8 * i) + DOWN * 1.5) for i in range(4)]
        bar = DashedLine(RIGHT * 1.0 + DOWN * 1.2, RIGHT * 5.4 + DOWN * 1.2, color=VIOLET, stroke_width=4)
        bl = tx("std::barrier(4, swap)", 17, VIOLET, MONO, True).move_to(RIGHT * 3.4 + DOWN * 2.1)
        swp = tx("hàm hoàn tất: đổi con trỏ, chạy 1 lần", 16, VIOLET).move_to(RIGHT * 3.4 + DOWN * 0.85)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(cells, lag_ratio=0.01), *[FadeIn(b) for b in bands]], 1.0),
                 ([FadeIn(cross), FadeIn(st)], 0.8),
                 ([FadeIn(omp), FadeIn(cpp)], 0.8),
                 ([FadeIn(ub), FadeIn(nb), GrowArrow(comp)], 0.8),
                 ([*[FadeIn(d) for d in dots], Create(bar)], 0.8),
                 ([*[AM(d, lambda _m, i=i: _m.move_to(RIGHT * (1.6 + 0.8 * i) + DOWN * 1.2)) for i, d in enumerate(dots)], FadeIn(bl)], 0.9),
                 ([AM(ub, lambda _m: _m.move_to(RIGHT * 4.9 + UP * 0.1)), AM(nb, lambda _m: _m.move_to(RIGHT * 2.2 + UP * 0.1)),
                   FadeIn(swp), AM(bar, lambda _m: _m.set_color(EMERALD))], 1.2),
                 ([self.setcap("Hoàn tất của barrier thay rào chắn thứ hai", VIOLET)], 0.6)]
        play_voiced(self, "02_20", steps)

    # ------------------------------------------------------------ 02_21
    def seg_21(self):
        hdr = make_header("Gắn luồng và first touch", "NUMA", CYAN)
        centers = [LEFT * 3.3 + DOWN * 0.15, RIGHT * 3.3 + DOWN * 0.15]
        nodes, cores, mems, nl = [], [], [], []
        for k, cpt in enumerate(centers):
            nb = rbox(5.6, 3.5, BORDER_DIM, fill=PANEL_BG, op=0.6).move_to(cpt)
            nt = tx(f"Nút NUMA {k}", 17, TEXT_MUTED, bold=True).move_to(cpt + UP * 1.45)
            cr = VGroup(*[rbox(0.8, 0.7, BORDER_DIM) for _ in range(4)]).arrange(RIGHT, buff=0.25).move_to(cpt + UP * 0.5)
            mm = rbox(4.8, 0.8, BORDER_DIM).move_to(cpt + DOWN * 0.95)
            nl.append(tx("bộ nhớ", 14, TEXT_MUTED).move_to(cpt + DOWN * 1.6))
            nodes.append(nb); cores.append(cr); mems.append(mm); nl.append(nt)
        mode = mono("OMP_PROC_BIND=close", 22, CYAN, bold=True).move_to(UP * 2.3)
        th = [Dot(radius=0.2, color=TH[i]).move_to(cores[0][i]) for i in range(4)]
        tl = [mono(f"{i}", 14, DARK, bold=True).move_to(th[i]) for i in range(4)]
        thg = [VGroup(th[i], tl[i]) for i in range(4)]
        spread_pos = [cores[0][0], cores[0][2], cores[1][0], cores[1][2]]
        pages = [rbox(0.95, 0.5, TH[i], fill=TH[i], op=0.55, sw=2, r=0.06) for i in range(4)]
        pl = [mono(f"P{i}", 16, TEXT_MAIN, bold=True).move_to(pages[i]) for i in range(4)]
        pg = [VGroup(pages[i], pl[i]) for i in range(4)]
        for i in range(4):
            pg[i].move_to(mems[0].get_center() + LEFT * 1.7 + RIGHT * 1.15 * i)
        rem = [Arrow(spread_pos[i].get_bottom() + DOWN * 0.05, pg[i].get_top(), buff=0.05, color=CORAL, stroke_width=3,
                     max_tip_length_to_length_ratio=0.12) for i in (2, 3)]
        mode2 = mono("OMP_PROC_BIND=spread", 22, AMBER, bold=True).move_to(UP * 2.3)
        mode3 = tx("khởi tạo tuần tự: mọi trang ở nút 0", 20, CORAL, bold=True).move_to(UP * 2.3)
        mode4 = tx("khởi tạo song song: trang nằm gần luồng", 20, EMERALD, bold=True).move_to(UP * 2.3)
        steps = [([FadeIn(hdr)], 0.4),
                 ([*[FadeIn(g) for g in nodes], *[FadeIn(g) for g in cores], *[FadeIn(g) for g in mems], *[FadeIn(g) for g in nl], FadeIn(mode)], 1.0),
                 ([*[FadeIn(g, scale=0.6) for g in thg]], 0.7),
                 ([Transform(mode, mode2), *[AM(thg[i], lambda _m, i=i: _m.move_to(spread_pos[i])) for i in range(4)]], 1.2),
                 ([Transform(mode, mode3), *[FadeIn(p) for p in pg]], 1.0),
                 ([*[GrowArrow(a) for a in rem]], 0.8),
                 ([Transform(mode, mode4), *[FadeOut(a) for a in rem],
                   *[AM(pg[i], lambda _m, i=i: _m.move_to(mems[1].get_center() + LEFT * 1.7 + RIGHT * 1.15 * (i - 2))) for i in (2, 3)]], 1.2),
                 ([*[AM(pages[i], lambda _m: _m.set_stroke(EMERALD, 4)) for i in range(4)],
                   self.setcap("Chia việc khi khởi tạo giống lúc tính toán", EMERALD)], 0.8)]
        play_voiced(self, "02_21", steps)

    # ------------------------------------------------------------ 02_22
    def seg_22(self):
        hdr = make_header("ThreadSanitizer và quy trình", "-fsanitize=thread", CORAL)
        rep = make_code_box(["WARNING: ThreadSanitizer: data race",
                             "Read of size 8 by thread T2:",
                             "  #0 operator() 06_counter.cpp:26",
                             "Previous write of size 8 by thread T1:",
                             "  #0 operator() 06_counter.cpp:26",
                             "Location is global 'counter'"], 7.0, 16, CORAL, "Báo cáo race").move_to(LEFT * 2.8 + UP * 0.75)
        c1 = labeled("chậm 5–15 lần khi kiểm tra", 4.6, 0.62, AMBER, 17, bold=True).move_to(RIGHT * 4.3 + UP * 1.6)
        c2 = labeled("chỉ thấy race trên đường đã chạy", 4.6, 0.62, VIOLET, 17, bold=True).move_to(RIGHT * 4.3 + UP * 0.8)
        c3 = labeled("dùng được cả OpenMP", 4.6, 0.62, EMERALD, 17, bold=True).move_to(RIGHT * 4.3 + UP * 0.0)
        names = ["1 Bản tuần tự", "2 default(none)", "3 So kết quả", "4 TSan", "5 time / perf"]
        cols = [CYAN, AMBER, EMERALD, CORAL, VIOLET]
        chips = VGroup(*[labeled(s, 2.3, 0.66, c, 17, bold=True) for s, c in zip(names, cols)]).arrange(RIGHT, buff=0.22).move_to(DOWN * 2.0)
        arrs = [Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.02, color=TEXT_MUTED, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.5) for i in range(4)]
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(rep)], 1.0),
                 ([FadeIn(c1, shift=LEFT * 0.1)], 0.6), ([FadeIn(c2, shift=LEFT * 0.1)], 0.6), ([FadeIn(c3, shift=LEFT * 0.1)], 0.6),
                 ([*[FadeIn(c, shift=UP * 0.1) for c in chips], *[GrowArrow(a) for a in arrs]], 1.2),
                 ([Indicate(chips[3], color=CORAL, scale_factor=1.15)], 0.7),
                 ([self.setcap("Đo trước, tối ưu sau", AMBER)], 0.5)]
        play_voiced(self, "02_22", steps)

    # ------------------------------------------------------------ helpers (map tables)
    def maptable(self, rows, lcol, rcol, lw=3.6, rw=4.6, y0=2.05, dy=0.68):
        L, R, A = [], [], []
        for i, (a, b) in enumerate(rows):
            y = y0 - dy * i
            l = labeled(a, lw, 0.52, lcol, 17, MONO, bold=True).move_to(LEFT * 3.7 + UP * y)
            r = labeled(b, rw, 0.52, rcol, 17, MONO, bold=True).move_to(RIGHT * 2.9 + UP * y)
            ar = Arrow(l.get_right(), r.get_left(), buff=0.08, color=TEXT_MUTED, stroke_width=3,
                       max_tip_length_to_length_ratio=0.25)
            L.append(l)
            R.append(r)
            A.append(ar)
        return L, R, A

    # ------------------------------------------------------------ 02_24
    def seg_24(self):
        hdr = make_header("C++20: bốn công cụ đồng bộ", "C++ threads", AMBER)
        names = [("mutex", "một luồng / đoạn găng", CYAN), ("barrier", "chờ đủ N luồng", AMBER),
                 ("condition_variable", "chờ điều kiện", EMERALD), ("counting_semaphore", "tối đa k luồng", VIOLET)]
        rows = VGroup()
        for i, (a, b, c) in enumerate(names):
            r1 = labeled(a, 3.3, 0.55, c, 16, MONO, bold=True)
            r2 = tx(b, 18, TEXT_MAIN).next_to(r1, RIGHT, buff=0.2)
            g = VGroup(r1, r2).move_to(LEFT * 3.2 + UP * (1.9 - 0.8 * i))
            g.align_to(LEFT * 6.2, LEFT)
            rows.add(g)
        res = rbox(3.0, 2.2, VIOLET).move_to(RIGHT * 4.0 + UP * 0.9)
        rl = tx("tài nguyên, k = 2", 17, VIOLET, bold=True).move_to(res.get_top() + DOWN * 0.3)
        ts = [labeled(f"T{i}", 0.8, 0.5, TH[i], 18, bold=True).move_to(RIGHT * 1.0 + UP * (1.8 - 0.65 * i)) for i in range(4)]
        slot = [RIGHT * 3.4 + DOWN * 0.1 + UP * 0.9 * 0, RIGHT * 4.6 + DOWN * 0.1 + UP * 0.9 * 0]
        slot = [RIGHT * 3.4 + UP * 0.6, RIGHT * 4.6 + UP * 0.6]
        wait = tx("T2, T3 chờ", 18, CORAL, bold=True).move_to(RIGHT * 4.0 + DOWN * 1.0)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(rows, lag_ratio=0.25)], 1.6),
                 ([FadeIn(res), FadeIn(rl), *[FadeIn(t) for t in ts]], 0.8),
                 ([AM(ts[0], lambda _m: _m.move_to(slot[0])), AM(ts[1], lambda _m: _m.move_to(slot[1]))], 1.0),
                 ([FadeIn(wait), AM(ts[2][0], lambda _m: _m.set_stroke(CORAL, 4)), AM(ts[3][0], lambda _m: _m.set_stroke(CORAL, 4))], 0.9),
                 ([AM(ts[0], lambda _m: _m.move_to(RIGHT * 4.0 + DOWN * 2.1)), FadeOut(wait)], 0.9),
                 ([AM(ts[2], lambda _m: _m.move_to(slot[0]))], 0.9),
                 ([AM(ts[3][0], lambda _m: _m.set_stroke(TH[3], 2))], 0.3),
                 ([self.setcap("HPC: mutex và barrier dùng nhiều nhất", AMBER)], 0.8)]
        play_voiced(self, "02_24", steps)

    # ------------------------------------------------------------ 02_25
    def seg_25(self):
        hdr = make_header("C++ threads chạy trên Pthreads", "Linux", AMBER)
        rows = [("std::jthread", "pthread_create"), ("join()", "pthread_join"), ("std::mutex", "pthread_mutex_t"),
                ("condition_variable", "pthread_cond_t"), ("std::barrier", "pthread_barrier_t"),
                ("counting_semaphore", "sem_t")]
        L, R, A = self.maptable(rows, CYAN, TEAL)
        ct = tx("C++", 20, CYAN, bold=True).move_to(LEFT * 3.7 + UP * 2.65)
        pt = tx("Pthreads (C)", 20, TEAL, bold=True).move_to(RIGHT * 2.9 + UP * 2.65)
        meas = labeled("tổng mảng 1 luồng: 0,072 s (C++) và 0,074 s (Pthreads)", 8.6, 0.55, AMBER, 18, bold=True).move_to(DOWN * 2.2)
        steps = [([FadeIn(hdr), FadeIn(ct), FadeIn(pt)], 0.5)]
        for l, r, a in zip(L, R, A):
            steps.append(([FadeIn(l), GrowArrow(a), FadeIn(r)], 0.55))
        steps += [([FadeIn(meas, shift=UP * 0.1)], 0.9),
                  ([self.setcap("Chỉ cần đọc hiểu Pthreads; native_handle() trả pthread_t", AMBER)], 0.8)]
        play_voiced(self, "02_25", steps)

    # ------------------------------------------------------------ 02_26
    def seg_26(self):
        hdr = make_header("Đối chiếu OpenMP và C++ threads", "đồng bộ", AMBER)
        rows = [("omp critical", "mutex + scoped_lock"), ("omp atomic", "std::atomic<T>"), ("omp barrier", "std::barrier"),
                ("omp single", "1 luồng, rồi barrier"), ("omp masked", "if (id==0): không rào"), ("omp ordered", "condition_variable")]
        L, R, A = self.maptable(rows, ORANGE, CYAN)
        ct = tx("OpenMP", 20, ORANGE, bold=True).move_to(LEFT * 3.7 + UP * 2.65)
        pt = tx("C++ threads", 20, CYAN, bold=True).move_to(RIGHT * 2.9 + UP * 2.65)
        trap = labeled("Bẫy: viết  #pragma barrier  thiếu omp, bị bỏ qua", 9.4, 0.6, CORAL, 19, bold=True).move_to(DOWN * 2.35)
        steps = [([FadeIn(hdr), FadeIn(ct), FadeIn(pt)], 0.5)]
        for l, r, a in zip(L, R, A):
            steps.append(([FadeIn(l), GrowArrow(a), FadeIn(r)], 0.55))
        steps += [([FadeIn(trap, shift=UP * 0.1), self.setcap("master đã lỗi thời từ OpenMP 5.1: dùng masked", AMBER)], 1.0)]
        play_voiced(self, "02_26", steps)

    # ------------------------------------------------------------ 02_27
    def seg_27(self):
        hdr = make_header("jthread và stop_token", "C++20", AMBER)
        mainl = tx("main", 18, CYAN, bold=True).move_to(LEFT * 5.7 + UP * 1.5)
        work = tx("worker", 18, EMERALD, bold=True).move_to(LEFT * 5.7 + DOWN * 0.3)
        lm = Line(LEFT * 4.8 + UP * 1.5, RIGHT * 5.4 + UP * 1.5, color=CYAN, stroke_width=3)
        lw = Line(LEFT * 4.8 + DOWN * 0.3, RIGHT * 5.4 + DOWN * 0.3, color=EMERALD, stroke_width=3)
        sl = labeled("sleep 50 ms", 2.6, 0.5, CYAN, 16, bold=True).move_to(LEFT * 3.2 + UP * 1.5)
        rq = labeled("request_stop()", 2.6, 0.5, AMBER, 16, MONO, bold=True).move_to(RIGHT * 0.6 + UP * 1.5)
        flag = labeled("stop_requested() = false", 4.2, 0.55, EMERALD, 17, MONO, bold=True).move_to(LEFT * 1.8 + DOWN * 1.3)
        flag2 = labeled("stop_requested() = true", 4.2, 0.55, AMBER, 17, MONO, bold=True).move_to(LEFT * 1.8 + DOWN * 1.3)
        n0 = mono("n = 0", 22, EMERALD, bold=True).move_to(RIGHT * 3.4 + DOWN * 0.3 + UP * 0.5)
        n1 = mono("n = 24", 22, EMERALD, bold=True).move_to(RIGHT * 3.4 + DOWN * 0.3 + UP * 0.5)
        n2 = mono("n = 48", 22, AMBER, bold=True).move_to(RIGHT * 3.4 + DOWN * 0.3 + UP * 0.5)
        out = mono("dung sau 48 vong", 22, AMBER, bold=True).move_to(RIGHT * 3.4 + DOWN * 1.3)
        cmp_ = labeled("std::thread: chỉ di chuyển, quên join() thì terminate", 8.4, 0.55, CORAL, 18, bold=True).move_to(DOWN * 2.3)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(mainl), FadeIn(work), Create(lm), Create(lw), FadeIn(flag), FadeIn(n0)], 1.0),
                 ([FadeIn(sl)], 0.6),
                 ([Transform(n0, n1)], 1.2),
                 ([FadeIn(rq, shift=DOWN * 0.1)], 0.7),
                 ([Transform(flag, flag2), Transform(n0, n2)], 1.0),
                 ([FadeIn(out)], 0.7),
                 ([FadeIn(cmp_), self.setcap("Hủy jthread = request_stop() rồi join()", AMBER)], 1.0)]
        play_voiced(self, "02_27", steps)

    # ------------------------------------------------------------ 02_28
    def seg_28(self):
        hdr = make_header("Chọn C++ threads hay OpenMP", "quyết định", AMBER)
        rows = [("Vòng lặp trên mảng", "OpenMP", ORANGE), ("Song song hóa dần mã cũ", "OpenMP", ORANGE),
                ("Đệ quy, cây, không đều", "OpenMP task", ORANGE), ("Luồng sống lâu: máy chủ, I/O", "C++ threads", CYAN),
                ("Hàng đợi, chờ điều kiện", "C++ threads", CYAN), ("Gắn luồng vào lõi", "Pthreads qua native_handle()", TEAL)]
        gs = VGroup()
        for i, (a, b, c) in enumerate(rows):
            l = labeled(a, 5.2, 0.55, BORDER_DIM, 18).move_to(LEFT * 2.6 + UP * (2.0 - 0.72 * i))
            r = labeled(b, 4.2, 0.55, c, 18, bold=True).move_to(RIGHT * 3.2 + UP * (2.0 - 0.72 * i))
            gs.add(VGroup(l, r))
        hl = rbox(11.6, 0.68, AMBER, fill=AMBER, op=0.12, sw=3).move_to(gs[0])
        steps = [([FadeIn(hdr)], 0.4), ([FadeIn(gs, lag_ratio=0.2)], 2.0),
                 ([FadeIn(hl)], 0.5), ([AM(hl, lambda _m: _m.move_to(gs[3]))], 1.0),
                 ([AM(hl, lambda _m: _m.move_to(gs[5]))], 1.0),
                 ([self.setcap("Có thể kết hợp: chương trình C++ threads chứa vùng OpenMP", AMBER)], 0.9)]
        play_voiced(self, "02_28", steps)

    # ------------------------------------------------------------ 02_29
    def seg_29(self):
        hdr = make_header("Không có lịch tốt nhất", "schedule", AMBER)
        panels = [("Tải đều", [("static", 0.039, EMERALD), ("dynamic,1", 3.648, CORAL), ("guided", 0.038, CYAN)], 3.648, -3.2),
                  ("Mandelbrot: tải bất thường", [("static", 0.420, CORAL), ("dynamic,1", 0.159, EMERALD), ("guided", 0.268, AMBER)], 0.420, 3.2)]
        allm = []
        bars = []
        for title, items, mx, cx in panels:
            tt = tx(title, 19, TEXT_MAIN, bold=True).move_to(RIGHT * cx + UP * 2.4)
            allm.append(tt)
            pb = []
            for j, (nm, v, c) in enumerate(items):
                y = 1.4 - 0.9 * j
                w = max(0.06, 3.0 * v / mx)
                lab = mono(nm, 15, TEXT_MUTED).move_to(RIGHT * (cx - 2.8) + UP * y).align_to(RIGHT * (cx - 3.0), LEFT)
                bar = Rectangle(width=w, height=0.5, fill_color=c, fill_opacity=0.95, stroke_width=0)
                bar.move_to(RIGHT * (cx - 1.5) + UP * y).align_to(RIGHT * (cx - 1.5), LEFT)
                val = tx(f"{v:.3f} s".replace(".", ","), 16, TEXT_MAIN, bold=True).next_to(bar, RIGHT, buff=0.1)
                allm.append(lab)
                pb.append((bar, val))
            bars.append(pb)
        n1 = labeled("dynamic,1 chậm gần 100 lần", 4.8, 0.55, CORAL, 17, bold=True).move_to(LEFT * 3.2 + DOWN * 1.7)
        n2 = labeled("guided kém hơn dynamic,1", 4.8, 0.55, AMBER, 17, bold=True).move_to(RIGHT * 3.2 + DOWN * 1.7)
        steps = [([FadeIn(hdr), *[FadeIn(m) for m in allm]], 0.8),
                 ([*[GrowFromEdge(b, LEFT) for b, v in bars[0]], *[FadeIn(v) for b, v in bars[0]]], 1.2),
                 ([FadeIn(n1)], 0.7),
                 ([*[GrowFromEdge(b, LEFT) for b, v in bars[1]], *[FadeIn(v) for b, v in bars[1]]], 1.2),
                 ([FadeIn(n2), self.setcap("8 luồng: mọi kiểu đánh đổi cân bằng tải và chi phí điều phối", AMBER)], 1.0)]
        play_voiced(self, "02_29", steps)

    # ------------------------------------------------------------ 02_30
    def seg_30(self):
        hdr = make_header("Task: ngưỡng cutoff", "OpenMP", AMBER)
        data = [("10^3", 0.047, "≈ 130 000 task", CORAL), ("10^5", 0.012, "≈ 1000 task", EMERALD),
                ("10^6", 0.013, "≈ 130 task", EMERALD), ("10^8", 0.037, "1 task", AMBER)]
        base = DOWN * 1.2
        axis = Line(LEFT * 5.2 + base, RIGHT * 1.4 + base, color=TEXT_MUTED, stroke_width=2)
        bars, labs = [], []
        for i, (c, v, t, col) in enumerate(data):
            h = 3.2 * v / 0.047
            x = -4.5 + 1.5 * i
            b = Rectangle(width=0.9, height=h, fill_color=col, fill_opacity=0.95, stroke_width=0)
            b.move_to(RIGHT * x + base, aligned_edge=DOWN)
            b.align_to(base, DOWN)
            vl = tx(f"{v:.3f} s".replace(".", ","), 16, TEXT_MAIN, bold=True).next_to(b, UP, buff=0.08)
            cl = mono(f"cutoff {c}", 14, TEXT_MUTED).move_to(RIGHT * x + DOWN * 1.55)
            tl = tx(t, 14, col).move_to(RIGHT * x + DOWN * 1.95)
            bars.append(b)
            labs.append(VGroup(vl, cl, tl))
        notes = VGroup(tx("cutoff quá thấp:", 19, CORAL, bold=True), tx("quá nhiều task, chậm hơn tuần tự", 18, TEXT_MAIN),
                       tx("cutoff 10^8: chỉ 1 task = tuần tự", 18, AMBER),
                       tx("n = 10^8, 8 luồng", 16, TEXT_MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 4.3 + UP * 0.8)
        steps = [([FadeIn(hdr), Create(axis)], 0.6)]
        for b, l in zip(bars, labs):
            steps.append(([GrowFromEdge(b, DOWN), FadeIn(l)], 0.8))
        steps += [([FadeIn(notes, lag_ratio=0.2)], 1.2),
                  ([self.setcap("Hạt quá mịn: chi phí quản lý nuốt lợi ích", AMBER)], 0.8)]
        play_voiced(self, "02_30", steps)

    # ------------------------------------------------------------ 02_31
    def seg_31(self):
        hdr = make_header("Tổng mảng: chạm băng thông bộ nhớ", "speedup", AMBER)
        data = [(1, 1.00), (2, 1.95), (4, 2.88), (8, 3.00), (12, 3.00)]
        base = DOWN * 1.6
        u = 0.32
        bars, ideal, labs = [], [], []
        for i, (t, s) in enumerate(data):
            x = -4.8 + 1.4 * i
            b = Rectangle(width=0.8, height=u * s, fill_color=EMERALD if t < 4 else AMBER, fill_opacity=0.95, stroke_width=0)
            b.move_to(RIGHT * x + base, aligned_edge=DOWN)
            b.align_to(base, DOWN)
            gh = Rectangle(width=0.8, height=u * t, stroke_color=TEXT_MUTED, stroke_width=1.5, fill_opacity=0)
            gh.move_to(RIGHT * x + base, aligned_edge=DOWN)
            gh.align_to(base, DOWN)
            vl = tx(f"{s:.2f}".replace(".", ",") + "×", 16, TEXT_MAIN, bold=True).next_to(b, UP, buff=0.08) if t < 12 else \
                tx("3,00×", 16, TEXT_MAIN, bold=True).next_to(b, UP, buff=0.08)
            cl = tx(f"{t} luồng", 15, TEXT_MUTED).move_to(RIGHT * x + base + DOWN * 0.3)
            bars.append(b)
            ideal.append(gh)
            labs.append(VGroup(vl, cl))
        ax = Line(LEFT * 5.5 + base, RIGHT * 1.2 + base, color=TEXT_MUTED, stroke_width=2)
        il = tx("khung xám = lý tưởng", 16, TEXT_MUTED).move_to(RIGHT * 4.0 + DOWN * 1.1)
        info = VGroup(tx("mỗi phần tử: 1 phép cộng,", 18, TEXT_MAIN), tx("nhưng đọc 8 byte từ RAM", 18, TEXT_MAIN),
                      tx("8 luồng: 1,6 GB / 0,024 s", 18, AMBER, bold=True),
                      tx("≈ 67 GB/s: gần trần băng thông", 18, CORAL, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 4.0 + UP * 0.6)
        steps = [([FadeIn(hdr), Create(ax), FadeIn(il)], 0.6)]
        for b, gh, l in zip(bars, ideal, labs):
            steps.append(([FadeIn(gh), GrowFromEdge(b, DOWN), FadeIn(l)], 0.8))
        steps += [([FadeIn(info, lag_ratio=0.25)], 1.6),
                  ([self.setcap("Memory-bound: thêm lõi không giúp", AMBER)], 0.8)]
        play_voiced(self, "02_31", steps)
