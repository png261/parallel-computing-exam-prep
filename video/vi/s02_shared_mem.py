from manim import *
from scene_utils import *
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
        for fn in [self.seg_01, self.seg_02, self.seg_03, self.seg_09, self.seg_04, self.seg_05,
                   self.seg_06, self.seg_10, self.seg_07, self.seg_11, self.seg_12, self.seg_08,
                   self.seg_13, self.seg_14, self.seg_15, self.seg_16, self.seg_17, self.seg_18,
                   self.seg_19, self.seg_20, self.seg_21, self.seg_22, self.seg_23]:
            self.cap = None
            fn()
            clear_stage(self)

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

    # ------------------------------------------------------------ 02_08
    def seg_08(self):
        hdr = make_header("Java: trạng thái luồng", "Thread.State", AMBER)
        pos = {
            "NEW": (-5.2, 1.4), "RUNNABLE": (-1.4, 1.4), "TERMINATED": (4.8, 1.4),
            "BLOCKED": (-3.6, -1.5), "WAITING": (0.2, -1.5), "TIMED_WAITING": (4.0, -1.5),
        }
        cols = {"NEW": CYAN, "RUNNABLE": EMERALD, "TERMINATED": TEXT_MUTED, "BLOCKED": CORAL, "WAITING": AMBER, "TIMED_WAITING": VIOLET}
        bx = {}
        for k, (x, y) in pos.items():
            bx[k] = labeled(k, 2.5, 0.8, cols[k], 18, MONO, bold=True).move_to(RIGHT * x + UP * y)

        def arr(a, b, **kw):
            return Arrow(bx[a].get_edge_center(kw.get("sa", RIGHT)), bx[b].get_edge_center(kw.get("sb", LEFT)), buff=0.08, color=TEXT_MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        a_start = arr("NEW", "RUNNABLE")
        a_end = arr("RUNNABLE", "TERMINATED")
        a_b = DoubleArrow(bx["RUNNABLE"].get_bottom() + LEFT * 0.8, bx["BLOCKED"].get_top() + RIGHT * 0.3, buff=0.08, color=CORAL, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        a_w = DoubleArrow(bx["RUNNABLE"].get_bottom() + RIGHT * 0.1, bx["WAITING"].get_top() + LEFT * 0.3, buff=0.08, color=AMBER, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        a_t = DoubleArrow(bx["RUNNABLE"].get_bottom() + RIGHT * 0.9, bx["TIMED_WAITING"].get_top() + LEFT * 0.4, buff=0.08, color=VIOLET, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        l_s = mono("start()", 18, CYAN).next_to(a_start, UP, buff=0.05)
        l_e = mono("run() xong", 17, TEXT_MUTED).next_to(a_end, UP, buff=0.05)
        l_b = tx("khóa đang bận", 17, CORAL).next_to(bx["BLOCKED"], DOWN, buff=0.12)
        l_w = mono("wait() / notify()", 16, AMBER).next_to(bx["WAITING"], DOWN, buff=0.12)
        l_t = mono("sleep(t)", 17, VIOLET).next_to(bx["TIMED_WAITING"], DOWN, buff=0.12)
        d = Dot(radius=0.16, color=AMBER).move_to(bx["NEW"].get_corner(UL) + RIGHT * 0.05)
        d.set_z_index(5)
        r = bx["RUNNABLE"]

        def at(k, dy=0.65):
            return bx[k].get_corner(UL) + RIGHT * 0.05
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(VGroup(*bx.values()), lag_ratio=0.1)], 1.2),
                 ([FadeIn(d)], 0.2),
                 ([GrowArrow(a_start), FadeIn(l_s), AM(d, lambda _m: _m.move_to(at("RUNNABLE")))], 1.0),
                 ([Create(a_b), FadeIn(l_b), AM(d, lambda _m: _m.move_to(at("BLOCKED")))], 1.0),
                 ([AM(d, lambda _m: _m.move_to(at("RUNNABLE")))], 0.7),
                 ([Create(a_w), FadeIn(l_w), AM(d, lambda _m: _m.move_to(at("WAITING")))], 1.0),
                 ([AM(d, lambda _m: _m.move_to(at("RUNNABLE")))], 0.7),
                 ([Create(a_t), FadeIn(l_t), AM(d, lambda _m: _m.move_to(at("TIMED_WAITING")))], 1.0),
                 ([AM(d, lambda _m: _m.move_to(at("RUNNABLE")))], 0.7),
                 ([GrowArrow(a_end), FadeIn(l_e), AM(d, lambda _m: _m.move_to(at("TERMINATED")))], 1.0),
                 ([self.setcap("Luôn gọi start(), không gọi run()", AMBER)], 0.6)]
        play_voiced(self, "02_08", steps)

    # ------------------------------------------------------------ 02_13
    def seg_13(self):
        hdr = make_header("Producer–Consumer (đệm 3 ô)", "wait / notify", EMERALD)
        P = labeled("Producer", 2.0, 1.0, AMBER, 20, bold=True).move_to(LEFT * 5.2 + UP * 0.5)
        C = labeled("Consumer", 2.0, 1.0, VIOLET, 20, bold=True).move_to(RIGHT * 5.2 + UP * 0.5)
        slots = VGroup(*[rbox(1.0, 0.9, BORDER_DIM, op=1.0) for _ in range(3)]).arrange(RIGHT, buff=0.2).move_to(UP * 0.5)
        mon = rbox(4.2, 1.5, AMBER, fill=DARK, sw=3, op=0.0).move_to(slots)
        ml = tx("synchronized", 18, AMBER, MONO, True).next_to(mon, UP, buff=0.08)
        nf = labeled("notFull", 2.0, 0.55, EMERALD, 18, MONO, bold=True).move_to(LEFT * 1.4 + DOWN * 1.2)
        ne = labeled("notEmpty", 2.0, 0.55, BORDER_DIM, 18, MONO, bold=True).move_to(RIGHT * 1.4 + DOWN * 1.2)
        items = [tok(str(i + 1), AMBER, 0.6, 0.5, 22) for i in range(4)]
        wl = mono("wait()", 22, CORAL, bold=True).next_to(P, DOWN, buff=0.15)
        wl2 = mono("chạy tiếp", 20, EMERALD, bold=True).next_to(P, DOWN, buff=0.15)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(P), FadeIn(C), FadeIn(slots), FadeIn(mon), FadeIn(ml), FadeIn(nf), FadeIn(ne)], 1.0)]
        for i in range(3):
            items[i].move_to(P)
            steps += [([FadeIn(items[i], scale=0.8)], 0.2), ([AM(items[i], lambda _m: _m.move_to(slots[i]))], 0.7)]
            if i == 0:
                steps.append(([AM(ne[0], lambda _m: _m.set_stroke(EMERALD, 3))], 0.2))
        steps.append(([AM(nf[0], lambda _m: _m.set_stroke(CORAL, 3).set_fill("#2A1215", 1)), AM(P[0], lambda _m: _m.set_stroke(CORAL, 4)), FadeIn(wl),
                       self.setcap("Đệm đầy: Producer phải wait()", CORAL)], 1.0))
        steps.append(([AM(items[0], lambda _m: _m.move_to(C.get_left() + LEFT * 0.45))], 0.9))
        steps.append(([FadeOut(items[0]), AM(nf[0], lambda _m: _m.set_stroke(EMERALD, 3).set_fill(PANEL_BG, 1)), Indicate(nf, color=EMERALD),
                       self.setcap("Consumer lấy 1 → notify()", EMERALD)], 0.8))
        items[3].move_to(P)
        steps.append(([FadeOut(wl), FadeIn(wl2), AM(P[0], lambda _m: _m.set_stroke(AMBER, 2))], 0.5))
        steps += [([FadeIn(items[3], scale=0.8)], 0.2), ([AM(items[3], lambda _m: _m.move_to(slots[0]))], 0.7)]
        steps.append(([self.setcap("Luôn kiểm tra điều kiện trong while", AMBER)], 0.6))
        play_voiced(self, "02_13", steps)

    # ------------------------------------------------------------ 02_14
    def seg_14(self):
        hdr = make_header("Semaphore: 2 permit", "Semaphore(2)", CYAN)
        ths = [labeled(f"T{i}", 0.9, 0.7, TH[i], 20, MONO, bold=True).move_to(LEFT * 5.6 + UP * (1.3 - 0.9 * i)) for i in range(4)]
        sem = rbox(2.6, 2.2, AMBER).move_to(LEFT * 1.6 + UP * 0.0)
        sl = tx("Semaphore", 18, AMBER, bold=True).move_to(sem.get_top() + DOWN * 0.3)
        permits = [Dot(radius=0.22, color=AMBER).move_to(sem.get_center() + RIGHT * (-0.45 + 0.9 * i) + DOWN * 0.1) for i in range(2)]
        zone = rbox(3.6, 2.6, EMERALD).move_to(RIGHT * 4.2 + UP * 0.0)
        zl = tx("vùng găng", 18, EMERALD, bold=True).move_to(zone.get_top() + DOWN * 0.3)
        zs = [RIGHT * 3.4 + DOWN * 0.15, RIGHT * 5.0 + DOWN * 0.15]
        cnt = [mono("permits: 2", 24, AMBER, bold=True).move_to(DOWN * 1.9 + LEFT * 1.6)]
        for t_ in ths:
            t_.set_z_index(3)
        for p_ in permits:
            p_.set_z_index(4)
        r2 = SurroundingRectangle(ths[2], color=CORAL, buff=0.06, stroke_width=4, corner_radius=0.1)
        r3 = SurroundingRectangle(ths[3], color=CORAL, buff=0.06, stroke_width=4, corner_radius=0.1)

        def setc(n, col=AMBER):
            nw = mono(f"permits: {n}", 24, col, bold=True).move_to(cnt[0])
            a = ReplacementTransform(cnt[0], nw)
            cnt[0] = nw
            return a
        steps = [([FadeIn(hdr)], 0.4),
                 ([*[FadeIn(t) for t in ths], FadeIn(sem), FadeIn(sl), *[FadeIn(p) for p in permits], FadeIn(zone), FadeIn(zl), FadeIn(cnt[0])], 1.0),
                 ([AM(ths[0], lambda _m: _m.move_to(zs[0])), AM(permits[0], lambda _m: _m.move_to(zs[0] + DOWN * 0.7)), setc(1)], 1.0),
                 ([AM(ths[1], lambda _m: _m.move_to(zs[1])), AM(permits[1], lambda _m: _m.move_to(zs[1] + DOWN * 0.7)), setc(0, CORAL)], 1.0),
                 ([Create(r2), Create(r3), self.setcap("T2, T3 phải chờ (acquire bị chặn)", CORAL)], 1.0),
                 ([AM(permits[0], lambda _m: _m.move_to(sem.get_center() + RIGHT * -0.45 + DOWN * 0.1)), FadeOut(ths[0]), setc(1), self.setcap("T0 xong → release()", EMERALD)], 1.0),
                 ([FadeOut(r2)], 0.3),
                 ([AM(ths[2], lambda _m: _m.move_to(zs[0])), AM(permits[0], lambda _m: _m.move_to(zs[0] + DOWN * 0.7)), setc(0, CORAL)], 1.0),
                 ([self.setcap("Tối đa 2 luồng cùng lúc", AMBER)], 0.6)]
        play_voiced(self, "02_14", steps)

    # ------------------------------------------------------------ 02_15
    def seg_15(self):
        hdr = make_header("Deadlock: vòng chờ", "2 khóa", CORAL)
        A = labeled("Thread A", 2.0, 0.9, AMBER, 20, bold=True).move_to(LEFT * 4.8 + UP * 0.0)
        B = labeled("Thread B", 2.0, 0.9, VIOLET, 20, bold=True).move_to(RIGHT * 4.8 + UP * 0.0)
        L1 = labeled("Khóa 1", 1.8, 0.8, CYAN, 20, bold=True).move_to(UP * 1.5)
        L2 = labeled("Khóa 2", 1.8, 0.8, EMERALD, 20, bold=True).move_to(DOWN * 1.5)
        hold1 = Arrow(L1.get_left(), A.get_top() + UP * 0.0, buff=0.08, color=AMBER, stroke_width=5)
        hold2 = Arrow(L2.get_right(), B.get_bottom(), buff=0.08, color=VIOLET, stroke_width=5)
        want1 = DashedLine(A.get_bottom(), L2.get_left(), color=CORAL, stroke_width=4).add_tip()
        want2 = DashedLine(B.get_top(), L1.get_right(), color=CORAL, stroke_width=4).add_tip()
        hl = tx("giữ", 18, TEXT_MUTED)
        lbl_h1 = tx("giữ", 18, AMBER, bold=True).move_to((hold1.get_start() + hold1.get_end()) / 2 + UP * 0.35 + LEFT * 0.2)
        lbl_h2 = tx("giữ", 18, VIOLET, bold=True).move_to((hold2.get_start() + hold2.get_end()) / 2 + DOWN * 0.35 + RIGHT * 0.2)
        lbl_w1 = tx("chờ", 18, CORAL, bold=True).move_to((want1.get_start() + want1.get_end()) / 2 + DOWN * 0.35 + LEFT * 0.1)
        lbl_w2 = tx("chờ", 18, CORAL, bold=True).move_to((want2.get_start() + want2.get_end()) / 2 + UP * 0.35 + RIGHT * 0.1)
        dead = tx("DEADLOCK", 34, CORAL, bold=True).move_to(UP * 0.0)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(A), FadeIn(B), FadeIn(L1), FadeIn(L2)], 0.9),
                 ([GrowArrow(hold1), FadeIn(lbl_h1)], 0.8),
                 ([GrowArrow(hold2), FadeIn(lbl_h2)], 0.8),
                 ([Create(want1), FadeIn(lbl_w1)], 0.8),
                 ([Create(want2), FadeIn(lbl_w2)], 0.8),
                 ([FadeIn(dead, scale=1.4), AM(A[0], lambda _m: _m.set_stroke(CORAL, 5)), AM(B[0], lambda _m: _m.set_stroke(CORAL, 5))], 0.9),
                 ([self.setcap("A chờ B, B chờ A: không ai nhả khóa", CORAL)], 0.8),
                 ([FadeOut(want1), FadeOut(want2), FadeOut(lbl_w1), FadeOut(lbl_w2), FadeOut(dead), FadeOut(hold1), FadeOut(hold2),
                   FadeOut(lbl_h1), FadeOut(lbl_h2), AM(A[0], lambda _m: _m.set_stroke(AMBER, 2)), AM(B[0], lambda _m: _m.set_stroke(VIOLET, 2))], 0.8),
                 ]
        # fix: same order
        o1 = Arrow(A.get_top(), L1.get_left(), buff=0.08, color=EMERALD, stroke_width=4)
        o2 = Arrow(B.get_top(), L1.get_right(), buff=0.08, color=EMERALD, stroke_width=4)
        o3 = Arrow(A.get_bottom(), L2.get_left(), buff=0.08, color=EMERALD, stroke_width=4)
        o4 = Arrow(B.get_bottom(), L2.get_right(), buff=0.08, color=EMERALD, stroke_width=4)
        n1 = tx("1", 28, EMERALD, bold=True).move_to(UP * 1.5 + LEFT * 2.6 + UP * 0.45)
        n2 = tx("1", 28, EMERALD, bold=True).move_to(UP * 1.5 + RIGHT * 2.6 + UP * 0.45)
        n3 = tx("2", 28, EMERALD, bold=True).move_to(DOWN * 1.5 + LEFT * 2.6 + DOWN * 0.45)
        n4 = tx("2", 28, EMERALD, bold=True).move_to(DOWN * 1.5 + RIGHT * 2.6 + DOWN * 0.45)
        steps += [([Create(o1), Create(o2), FadeIn(n1), FadeIn(n2)], 0.9), ([Create(o3), Create(o4), FadeIn(n3), FadeIn(n4), self.setcap("Luôn khóa theo cùng một thứ tự", EMERALD)], 1.0)]
        play_voiced(self, "02_15", steps)

    # ============================================================ 02_16 .. 02_23 (bổ sung từ tài liệu cập nhật)
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

    # ------------------------------------------------------------ 02_23
    def seg_23(self):
        hdr = make_header("ReentrantLock: khóa công bằng", "Java", AMBER)
        mode = mono("new ReentrantLock()", 24, CORAL, bold=True).move_to(UP * 2.3)
        mode2 = mono("new ReentrantLock(true)", 24, EMERALD, bold=True).move_to(UP * 2.3)
        lock = rbox(2.2, 1.4, AMBER).move_to(RIGHT * 4.2 + UP * 0.3)
        ll = tx("khóa", 17, AMBER, bold=True).move_to(lock.get_top() + DOWN * 0.28)
        qx = [0.2, -1.4, -3.0]
        qn = ["A", "B", "C"]
        q = [labeled(f"{qn[i]}", 1.1, 0.7, TH[i], 22, bold=True).move_to(RIGHT * qx[i] + UP * 0.3) for i in range(3)]
        ql = tx("hàng chờ (A chờ lâu nhất)", 17, TEXT_MUTED).move_to(LEFT * 1.4 + UP * 1.1)
        holder = labeled("H", 0.8, 0.55, TEXT_MAIN, 20, bold=True).move_to(lock.get_center() + DOWN * 0.15)
        newd_pos = RIGHT * 1.9 + DOWN * 1.5
        newd = labeled("D mới đến", 1.7, 0.6, VIOLET, 18, bold=True).move_to(newd_pos)
        inlock = lock.get_center() + DOWN * 0.15
        res1 = tx("D chen ngang: A có thể bị đói", 19, CORAL, bold=True).move_to(LEFT * 1.0 + DOWN * 2.35)
        res2 = tx("A nhận khóa trước: công bằng", 19, EMERALD, bold=True).move_to(LEFT * 1.0 + DOWN * 2.35)
        steps = [([FadeIn(hdr)], 0.4),
                 ([FadeIn(mode), FadeIn(lock), FadeIn(ll), *[FadeIn(g) for g in q], FadeIn(ql), FadeIn(holder)], 1.0),
                 ([FadeIn(newd, shift=UP * 0.2)], 0.6),
                 ([FadeOut(holder)], 0.6),
                 ([AM(newd, lambda _m: _m.move_to(inlock).scale_to_fit_width(1.4)), FadeIn(res1)], 0.9),
                 ([AM(q[0][0], lambda _m: _m.set_stroke(CORAL, 4))], 0.5),
                 ([FadeOut(res1), AM(newd, lambda _m: _m.scale_to_fit_width(1.7).move_to(newd_pos)), AM(q[0][0], lambda _m: _m.set_stroke(TH[0], 2)),
                   Transform(mode, mode2), FadeIn(holder)], 1.0),
                 ([FadeOut(holder)], 0.6),
                 ([AM(q[0], lambda _m: _m.move_to(inlock)), FadeIn(res2),
                   self.setcap("Công bằng tránh đói, đổi lại thông lượng thấp hơn", AMBER)], 1.1)]
        play_voiced(self, "02_23", steps)
