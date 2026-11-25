from manim import *
import numpy as np
from extras import seg_05_06, seg_05_07, seg_05_08, seg_05_09
from scene_utils import play_module_drills, get_duration
from scene_utils import (
    setup_bg, make_header, make_card, make_trap_banner, make_bar_chart,
    clear_stage, play_voiced, make_grid_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, BORDER_DIM, SANS, MONO
)

RANKC = [CYAN, AMBER, EMERALD, VIOLET]
GREY = "#3B424C"


# ---------------------------------------------------------------- helpers
def T(s, size=18, color=TEXT_MAIN, font=SANS, bold=False):
    return Text(s, font=font, font_size=size, color=color, weight=BOLD if bold else NORMAL)


def P3(x, y):
    return np.array([x, y, 0.0])


def node(label, pos, color=CYAN, r=0.28, fs=18):
    c = Circle(radius=r, color=color, fill_color=PANEL_BG, fill_opacity=1, stroke_width=2.5)
    t = T(label, fs, TEXT_MAIN, MONO, True)
    return VGroup(c, t).move_to(pos)


def cell(label, w, h, color=BORDER_DIM, fs=16, fill=PANEL_BG, tcolor=TEXT_MAIN):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.06, color=color,
                         fill_color=fill, fill_opacity=0.95, stroke_width=2)
    t = T(label, fs, tcolor, MONO, True)
    if t.width > w - 0.1:
        t.scale_to_fit_width(w - 0.1)
    t.move_to(r)
    return VGroup(r, t)


def take(s, color=AMBER, y=-3.1):
    t = T(s, 20, color, SANS, True)
    if t.width > 12.0:
        t.scale_to_fit_width(12.0)
    return t.move_to(P3(0, y))


def elink(a, b, color=TEXT_MUTED, w=2.5, r=0.28):
    return Line(a[0].get_center(), b[0].get_center(), buff=r, color=color, stroke_width=w)


def mat(n, m, cs, colorfn, op=0.6):
    g = VGroup()
    for i in range(n):
        for j in range(m):
            col = colorfn(i, j)
            sq = Square(cs, color=col, fill_color=col, fill_opacity=op, stroke_width=1.5)
            sq.move_to(P3((j - (m - 1) / 2) * cs, -(i - (n - 1) / 2) * cs))
            g.add(sq)
    return g


def V(scene, sid, steps):
    """play_voiced, stretching run_times to fill the audio when it is longer."""
    tot = sum(rt for _, rt in steps)
    f = max(1.0, min(3.0, (get_duration(sid) - 0.8) / tot))
    play_voiced(scene, sid, [(a, rt * f) for a, rt in steps])


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


# ---------------------------------------------------------------- 05_01 QuickHull
def seg_01(s):
    hdr = make_header("QuickHull: bao lồi song song", "Chương 8", VIOLET)
    Pts = [(-4.2, -0.1), (-3.2, 1.2), (-2.0, 1.9), (-0.6, 1.1), (0.9, 1.9), (2.3, 1.2), (4.2, 0.3),
           (2.8, -1.0), (0.8, -1.7), (-1.4, -1.4), (-2.6, -0.5), (0.2, 0.1), (-1.0, -0.2)]
    pos = lambda p: P3(p[0], p[1] - 0.2)
    dots = VGroup(*[Dot(pos(p), radius=0.1, color=TEXT_MAIN) for p in Pts])
    idx = {p: i for i, p in enumerate(Pts)}
    u = min(Pts); v = max(Pts)
    up = [p for p in Pts if cross(u, v, p) > 1e-9]
    lo = [p for p in Pts if cross(u, v, p) < -1e-9]
    pu = max(up, key=lambda p: cross(u, v, p))
    pl = min(lo, key=lambda p: cross(u, v, p))

    def inside(p, a, b, c):
        d = [cross(a, b, p), cross(b, c, p), cross(c, a, p)]
        return all(x >= -1e-9 for x in d) or all(x <= 1e-9 for x in d)

    def foot(p):
        a = np.array(u); b = np.array(v); q = np.array(p)
        t = np.dot(q - a, b - a) / np.dot(b - a, b - a)
        r = a + t * (b - a)
        return (r[0], r[1])

    inn_u = [p for p in up if p != pu and inside(p, u, pu, v)]
    inn_l = [p for p in lo if p != pl and inside(p, u, pl, v)]

    # monotone chain hull
    S = sorted(Pts)
    lower = []
    for p in S:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(S):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]

    lu = T("u", 20, CYAN, MONO, True).next_to(dots[idx[u]], LEFT, buff=0.12)
    lv = T("v", 20, CYAN, MONO, True).next_to(dots[idx[v]], RIGHT, buff=0.12)
    lpu = T("p", 20, AMBER, MONO, True).next_to(dots[idx[pu]], UP, buff=0.1)
    lpl = T("p'", 20, CORAL, MONO, True).next_to(dots[idx[pl]], DOWN, buff=0.1)
    line_uv = Line(pos(u), pos(v), color=CYAN, stroke_width=3)
    tri_u = Polygon(pos(u), pos(pu), pos(v), color=AMBER, stroke_width=2.5, fill_color=AMBER, fill_opacity=0.12)
    tri_l = Polygon(pos(u), pos(pl), pos(v), color=CORAL, stroke_width=2.5, fill_color=CORAL, fill_opacity=0.12)
    dist_u = DashedLine(pos(pu), pos(foot(pu)), color=AMBER, stroke_width=2.5)
    dist_l = DashedLine(pos(pl), pos(foot(pl)), color=CORAL, stroke_width=2.5)
    poly = Polygon(*[pos(p) for p in hull], color=EMERALD, stroke_width=5, fill_color=EMERALD, fill_opacity=0.1)

    V(s, "05_01", [
        ([FadeIn(hdr), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.08)], 2.0),
        ([Create(line_uv), FadeIn(lu), FadeIn(lv)], 1.5),
        ([dots[idx[p]].animate.set_color(AMBER) for p in up] + [dots[idx[p]].animate.set_color(CORAL) for p in lo], 1.5),
        ([Create(dist_u), FadeIn(lpu), Create(tri_u)], 2.0),
        ([dots[idx[p]].animate.set_opacity(0.2) for p in inn_u], 1.2),
        ([Create(dist_l), FadeIn(lpl), Create(tri_l)], 2.0),
        ([dots[idx[p]].animate.set_opacity(0.2) for p in inn_l], 1.2),
        ([Create(poly), FadeIn(take("Pivot = điểm xa đường nhất; bỏ điểm trong tam giác"))], 2.5),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_10 max tree + accelerated cascading
def seg_10(s):
    hdr = make_header("Tìm max: cây và Accelerated Cascading", "Chương 8", EMERALD)
    vals = [3, 8, 1, 9, 4, 7, 2, 6]
    lvl_y = [-1.0, 0.1, 1.2, 2.2]
    x0, dx = -5.2, 1.0
    cur = [cell(str(v), 0.7, 0.5, CYAN, 20).move_to(P3(x0 + i * dx, lvl_y[0])) for i, v in enumerate(vals)]
    leaves = VGroup(*cur)
    steps = [([FadeIn(hdr), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cur], lag_ratio=0.1)], 1.8)]
    note = T("", 18)
    allparents = VGroup()
    lab = T("Bước 1: 4 so sánh song song", 20, AMBER, SANS, True).move_to(P3(4.4, 0.8))
    labels = ["Bước 1: 4 so sánh song song", "Bước 2: 2 so sánh", "Bước 3: 1 so sánh"]
    level_vals = vals
    for l in range(3):
        nxt_vals = [max(level_vals[2 * i], level_vals[2 * i + 1]) for i in range(len(level_vals) // 2)]
        nxt = []
        anims = []
        for i, mv in enumerate(nxt_vals):
            a, b = cur[2 * i], cur[2 * i + 1]
            px = (a.get_center()[0] + b.get_center()[0]) / 2
            par = cell(str(mv), 0.7, 0.5, EMERALD, 20).move_to(P3(px, lvl_y[l + 1]))
            e1 = Line(a.get_top(), par.get_bottom(), color=TEXT_MUTED, stroke_width=2)
            e2 = Line(b.get_top(), par.get_bottom(), color=TEXT_MUTED, stroke_width=2)
            win = a if level_vals[2 * i] >= level_vals[2 * i + 1] else b
            lose = b if win is a else a
            anims += [Create(e1), Create(e2), TransformFromCopy(win, par), lose.animate.set_opacity(0.35)]
            nxt.append(par)
        if l == 0:
            steps.append(([FadeIn(lab)] + anims, 2.5))
        else:
            steps.append(([Transform(lab, T(labels[l], 20, AMBER, SANS, True).move_to(P3(4.4, 0.8)))] + anims, 2.5))
        cur = nxt
        level_vals = nxt_vals
    steps.append(([FadeIn(take("n phần tử: T = log n bước, công việc W = n"))], 1.5))
    V(s, "05_10", steps)
    clear_stage(s)

    # second half: compare strategies for n = 16
    hdr2 = make_header("Tìm max: so sánh với n = 16", "Chương 8", EMERALD)
    c1 = make_bar_chart([4, 1, 2], ["Cây", "All-Pairs", "DLDT"], [CYAN, CORAL, EMERALD], 4, width=4.6, height=2.6, unit="").move_to(P3(-3.3, -0.2))
    c2 = make_bar_chart([16, 256, 32], ["Cây", "All-Pairs", "DLDT"], [CYAN, CORAL, EMERALD], 256, width=4.6, height=2.6, unit="").move_to(P3(3.3, -0.2))
    t1 = T("Thời gian T", 22, TEXT_MAIN, SANS, True).move_to(P3(-3.3, 2.2))
    t2 = T("Công việc W", 22, TEXT_MAIN, SANS, True).move_to(P3(3.3, 2.2))
    comb = take("Cây vài tầng + DLDT: W = O(n) và T = O(log log n)", EMERALD)
    V(s, "05_10", [
        ([FadeIn(hdr2), FadeIn(t1), FadeIn(c1)], 3.0),
        ([FadeIn(t2), FadeIn(c2)], 3.0),
        ([FadeIn(comb)], 2.0),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_02 MatVec 1D vs 2D
def seg_02(s):
    hdr = make_header("Nhân ma trận với vector: 1D và 2D", "Chương 9", CYAN)
    cs = 0.42
    A1 = mat(4, 4, cs, lambda i, j: RANKC[i]).move_to(P3(-4.6, -0.4))
    plabs = VGroup(*[T("P%d" % i, 16, RANKC[i], MONO, True).next_to(A1[i * 4], LEFT, buff=0.15) for i in range(4)])
    xs = mat(1, 4, cs, lambda i, j: AMBER).move_to(P3(-2.5, 1.3))
    xl = T("x", 20, AMBER, MONO, True).next_to(xs, LEFT, buff=0.15)
    copies = VGroup(*[mat(1, 4, cs, lambda a, b: AMBER).move_to(P3(-2.5, A1[i * 4].get_center()[1])) for i in range(4)])
    title1 = T("1D theo hàng", 22, CYAN, SANS, True).move_to(P3(-3.6, 2.25))
    cnt1 = T("mỗi rank nhận 4 số", 18, TEXT_MUTED).move_to(P3(-3.6, -1.65))

    blk = [CYAN, AMBER, EMERALD, VIOLET]
    A2 = mat(4, 4, cs, lambda i, j: blk[(i // 2) * 2 + (j // 2)]).move_to(P3(3.0, -0.4))
    title2 = T("2D theo khối 2×2", 22, AMBER, SANS, True).move_to(P3(3.5, 2.25))
    xa = mat(1, 2, cs, lambda i, j: AMBER).move_to(P3(3.0 - 0.42, 1.3))
    xb = mat(1, 2, cs, lambda i, j: AMBER).move_to(P3(3.0 + 0.42, 1.3))
    top_y = -0.4 + 0.84 + 0.05
    arr = VGroup(*[Arrow(P3(xc, 1.3 - 0.25), P3(xc, top_y + 0.03), buff=0.0, color=AMBER, stroke_width=3, max_tip_length_to_length_ratio=0.4)
                   for xc in (3.0 - 0.42, 3.0 + 0.42)])
    ys = VGroup(mat(2, 1, cs, lambda i, j: VIOLET).move_to(P3(4.5, -0.4 + 0.42)),
                mat(2, 1, cs, lambda i, j: EMERALD).move_to(P3(4.5, -0.4 - 0.42)))
    yl = T("y", 20, VIOLET, MONO, True).move_to(P3(4.5, 0.95))
    harr = VGroup(*[Arrow(P3(3.9, -0.4 + dy), P3(4.2, -0.4 + dy), buff=0, color=TEXT_MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.5)
                    for dy in (0.42, -0.42)])
    cnt2 = T("mỗi rank nhận 2 số", 18, TEXT_MUTED).move_to(P3(3.4, -1.65))

    V(s, "05_02", [
        ([FadeIn(hdr), FadeIn(title1), FadeIn(A1), FadeIn(plabs)], 2.0),
        ([FadeIn(xs), FadeIn(xl)], 1.2),
        ([LaggedStart(*[TransformFromCopy(xs, c) for c in copies], lag_ratio=0.3)], 3.0),
        ([FadeIn(cnt1)], 1.0),
        ([FadeIn(title2), FadeIn(A2)], 2.0),
        ([FadeIn(xa), FadeIn(xb), *[GrowArrow(a) for a in arr]], 2.2),
        ([FadeIn(cnt2), FadeIn(ys), FadeIn(yl), *[GrowArrow(a) for a in harr]], 2.0),
        ([FadeIn(take("2D: mỗi rank chỉ nhận n/√p số thay vì n"))], 1.5),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_11 Cannon
def seg_11(s):
    hdr = make_header("Thuật toán Cannon trên lưới 3×3", "Chương 9", CYAN)

    def pos(i, j):
        return P3(-2.4 + (j - 1) * 1.85, 1.2 - i * 1.05)

    def mk(i, j, ka, kb):
        r = RoundedRectangle(width=1.7, height=0.85, corner_radius=0.08, color=BORDER_DIM,
                             fill_color=PANEL_BG, fill_opacity=0.95, stroke_width=1.8)
        a = T("A%d%d" % (i, ka), 17, CYAN, MONO, True)
        b = T("B%d%d" % (kb, j), 17, AMBER, MONO, True)
        ab = VGroup(a, b).arrange(RIGHT, buff=0.2).move_to(r)
        return VGroup(r, ab).move_to(pos(i, j))

    grid = [[mk(i, j, j, i) for j in range(3)] for i in range(3)]
    allc = VGroup(*[grid[i][j] for i in range(3) for j in range(3)])
    hl = RoundedRectangle(width=1.7, height=0.85, corner_radius=0.08, color=AMBER, stroke_width=5).move_to(pos(1, 1))
    lab = T("Ban đầu", 20, TEXT_MUTED).move_to(P3(-2.4, 2.25))

    def goto(f):
        return [Transform(grid[i][j], mk(i, j, f(i, j), f(i, j))) for i in range(3) for j in range(3)]

    title = T("Rank (1,1) cộng dồn", 18, AMBER, SANS, True).move_to(P3(4.0, 1.75))
    terms = [T("C11 = A12·B21", 20, TEXT_MAIN, MONO, True), T("+ A10·B01", 20, TEXT_MAIN, MONO, True), T("+ A11·B11", 20, TEXT_MAIN, MONO, True)]
    for k, t in enumerate(terms):
        t.move_to(P3(2.6, 0.95 - 0.55 * k), aligned_edge=LEFT)
    la = VGroup(Arrow(P3(3.9, -1.3), P3(3.1, -1.3), buff=0, color=CYAN, stroke_width=4), T("A", 18, CYAN, MONO, True).move_to(P3(4.2, -1.3)))
    lb = VGroup(Arrow(P3(5.4, -1.8), P3(5.4, -1.0), buff=0, color=AMBER, stroke_width=4), T("B", 18, AMBER, MONO, True).move_to(P3(5.75, -1.4)))

    def newlab(t):
        return Transform(lab, T(t, 20, TEXT_MUTED).move_to(P3(-2.4, 2.25)))

    V(s, "05_11", [
        ([FadeIn(hdr), FadeIn(lab), LaggedStart(*[FadeIn(c) for c in allc], lag_ratio=0.08)], 2.0),
        ([newlab("Lệch: A trái i, B lên j")] + goto(lambda i, j: (i + j) % 3), 3.0),
        ([Create(hl), FadeIn(title), FadeIn(terms[0])], 2.0),
        ([newlab("Dịch vòng 1"), FadeIn(la), FadeIn(lb)] + goto(lambda i, j: (i + j + 1) % 3) + [FadeIn(terms[1])], 3.0),
        ([newlab("Dịch vòng 2")] + goto(lambda i, j: (i + j + 2) % 3) + [FadeIn(terms[2])], 3.0),
        ([FadeIn(take("Sau 3 bước: C11 đủ 3 tích, chỉ trao đổi với láng giềng"))], 1.5),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_12 Gaussian elimination + mapping
def seg_12(s):
    hdr = make_header("Khử Gauss: cập nhật hạng 1", "Chương 9", AMBER)
    n = 6
    cs = 0.42
    base = "#2B323C"
    M = mat(n, n, cs, lambda i, j: BORDER_DIM, op=0.5).move_to(P3(-4.0, -0.2))
    for sq in M:
        sq.set_fill(base, 1)
    C = lambda i, j: M[i * n + j]
    kt = T("k = 0", 22, AMBER, MONO, True).move_to(P3(-4.0, 1.6))
    bt = T("Theo khối", 20, TEXT_MAIN, SANS, True).move_to(P3(0.9, 1.6))
    ct = T("Cyclic", 20, TEXT_MAIN, SANS, True).move_to(P3(3.7, 1.6))

    def bars(xc, owner):
        g = VGroup()
        for i in range(n):
            o = owner(i)
            r = RoundedRectangle(width=1.5, height=0.3, corner_radius=0.05, color=RANKC[o], fill_color=RANKC[o], fill_opacity=0.7, stroke_width=1.5)
            t = T("P%d" % o, 13, BG_DARK, MONO, True).move_to(r)
            g.add(VGroup(r, t).move_to(P3(xc, 1.0 - 0.5 * i)))
        return g
    B1 = bars(0.9, lambda i: i // 3)
    B2 = bars(3.7, lambda i: i % 2)

    steps = [([FadeIn(hdr), FadeIn(M), FadeIn(kt), FadeIn(bt), FadeIn(ct), FadeIn(B1), FadeIn(B2)], 2.0)]
    for k in range(4):
        piv = [C(k, j).animate.set_fill(CYAN, 0.9) for j in range(k, n)]
        sub = [C(i, j).animate.set_fill(AMBER, 0.75) for i in range(k + 1, n) for j in range(k, n)]
        newk = Transform(kt, T("k = %d" % k, 22, AMBER, MONO, True).move_to(P3(-4.0, 1.6)))
        steps.append(([newk] + piv, 1.3))
        steps.append((sub, 1.3))
        done = [C(k, j).animate.set_fill(GREY, 1) for j in range(k, n)]
        zero = [C(i, k).animate.set_fill("#0D1117", 1) for i in range(k + 1, n)]
        back = [C(i, j).animate.set_fill(base, 1) for i in range(k + 1, n) for j in range(k + 1, n)]
        grey1 = B1[k].animate.set_opacity(0.25)
        grey2 = B2[k].animate.set_opacity(0.25)
        steps.append((done + zero + back + [grey1, grey2], 1.3))
    idle = T("P0 rỗi!", 20, CORAL, SANS, True).move_to(P3(0.9, -1.95))
    busy = T("Cả hai còn việc", 20, EMERALD, SANS, True).move_to(P3(3.7, -1.95))
    steps.append(([FadeIn(idle), FadeIn(busy)], 1.5))
    steps.append(([FadeIn(take("Cyclic cân bằng tải hơn khi ma trận con co lại"))], 1.5))
    V(s, "05_12", steps)
    clear_stage(s)


BG_DARK = "#0D1117"


# ---------------------------------------------------------------- 05_19 pipeline Gantt
def seg_19(s):
    hdr = make_header("Pipeline cho khử Gauss 1D", "Chương 9", AMBER)
    u = 0.62
    x0 = -3.7
    KC = [CYAN, AMBER, EMERALD, VIOLET]

    def blk(t0, dur, y, color, txt=""):
        r = Rectangle(width=dur * u - 0.04, height=0.38, color=color, fill_color=color, fill_opacity=0.8, stroke_width=1)
        g = VGroup(r)
        if txt:
            g.add(T(txt, 13, BG_DARK, MONO, True).move_to(r))
        return g.move_to(P3(x0 + (t0 + dur / 2) * u, y))

    l1 = T("Không pipeline", 20, TEXT_MUTED, SANS, True).move_to(P3(-3.0, 2.35))
    top = []
    for k in range(4):
        top.append(blk(3 * k, 2, 1.85, CORAL))
        top.append(blk(3 * k + 2, 1, 1.85, KC[k], "k%d" % k))
    e1 = T("12 bước", 20, CORAL, MONO, True).move_to(P3(x0 + 12 * u + 0.8, 1.85))
    l2 = T("Pipeline", 20, EMERALD, SANS, True).move_to(P3(-4.3, 1.1))
    plabs = VGroup(*[T("P%d" % i, 15, TEXT_MUTED, MONO, True).move_to(P3(x0 - 0.45, 0.55 - 0.5 * i)) for i in range(4)])
    by_t = {}
    for k in range(4):
        for i in range(k, 4):
            by_t.setdefault(k + i, []).append(blk(k + i, 1, 0.55 - 0.5 * i, KC[k], "k%d" % k))
    e2 = T("7 bước", 20, EMERALD, MONO, True).move_to(P3(x0 + 7 * u + 0.8, -0.2))
    steps = [([FadeIn(hdr), FadeIn(l1)], 1.0),
             ([LaggedStart(*[FadeIn(b) for b in top], lag_ratio=0.12)], 4.0),
             ([FadeIn(e1)], 1.0),
             ([FadeIn(l2), FadeIn(plabs)], 1.0)]
    for t in range(7):
        steps.append(([FadeIn(b, shift=RIGHT * 0.15) for b in by_t[t]], 0.9))
    steps.append(([FadeIn(e2)], 1.0))
    steps.append(([FadeIn(take("Các vòng k chồng lên nhau theo đường chéo"))], 1.5))
    V(s, "05_19", steps)
    clear_stage(s)


# ---------------------------------------------------------------- 05_03 Euler tour + suffix sum
def seg_03(s):
    hdr = make_header("Euler Tour: thứ tự pre-order", "Chương 10", EMERALD)
    r_ = node("r", P3(0, 1.95), CYAN); a_ = node("a", P3(-1.6, 0.9), EMERALD); b_ = node("b", P3(1.6, 0.9), AMBER)
    e1 = elink(r_, a_); e2 = elink(r_, b_)
    names = ["rA", "aA", "aB", "aC", "rB", "bA", "bB", "bC", "rC"]
    ncol = {"r": CYAN, "a": EMERALD, "b": AMBER}
    w = [1, 1, 0, 0, 0, 1, 0, 0, 0]
    suf = [3, 2, 1, 1, 1, 1, 0, 0, 0]
    xs = [-4.9 + i * 1.1 for i in range(9)]
    row_n = [cell(nm, 1.0, 0.55, ncol[nm[0]], 16).move_to(P3(xs[i], -0.15)) for i, nm in enumerate(names)]
    row_w = [cell(str(w[i]), 1.0, 0.55, BORDER_DIM, 18, tcolor=AMBER if w[i] else TEXT_MUTED).move_to(P3(xs[i], -0.95)) for i in range(9)]
    row_s = [cell(str(suf[i]), 1.0, 0.55, BORDER_DIM, 18, tcolor=EMERALD).move_to(P3(xs[i], -1.75)) for i in range(9)]
    lbl = lambda t, y: T(t, 13, TEXT_MUTED).move_to(P3(-5.95, y)).set_x(-5.95)
    l1 = T("bản sao", 13, TEXT_MUTED).move_to(P3(-5.95, -0.15)); l2 = T("trọng số", 13, TEXT_MUTED).move_to(P3(-5.95, -0.95)); l3 = T("tổng hậu tố", 13, TEXT_MUTED).move_to(P3(-5.95, -1.75))
    for l in (l1, l2, l3):
        if l.width > 1.0:
            l.scale_to_fit_width(1.0)
    dot = Dot(r_.get_center(), radius=0.12, color=CORAL)
    path = VMobject().set_points_as_corners([r_.get_center(), a_.get_center(), r_.get_center(), b_.get_center(), r_.get_center()])
    nums = [T("1", 22, EMERALD, MONO, True).next_to(r_, RIGHT, buff=0.2),
            T("2", 22, EMERALD, MONO, True).next_to(a_, LEFT, buff=0.2),
            T("3", 22, EMERALD, MONO, True).next_to(b_, RIGHT, buff=0.2)]
    Aidx = [0, 1, 5]
    V(s, "05_03", [
        ([FadeIn(hdr), Create(e1), Create(e2), FadeIn(r_), FadeIn(a_), FadeIn(b_), FadeIn(l1)], 1.8),
        ([FadeIn(dot), MoveAlongPath(dot, path, rate_func=linear), LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in row_n], lag_ratio=0.45)], 4.5),
        ([FadeOut(dot), FadeIn(l2), LaggedStart(*[FadeIn(c) for c in row_w], lag_ratio=0.1)], 2.0),
        ([FadeIn(l3), LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in reversed(row_s)], lag_ratio=0.3)], 3.5),
        ([row_s[i][0].animate.set_stroke(EMERALD, width=5) for i in Aidx] + [FadeIn(n_) for n_ in nums], 2.5),
        ([FadeIn(take("Pre-order = |V| − v[A] + 1 = 3 − v[A] + 1"))], 1.5),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_13 RAKE
def seg_13(s):
    hdr = make_header("Co cây RAKE: bảy nút còn ba nút", "Chương 10", VIOLET)
    P = {"r": P3(0, 1.9), "a": P3(-2.4, 0.6), "b": P3(2.4, 0.6), "c": P3(-3.6, -0.8), "d": P3(-1.2, -0.8), "e": P3(1.2, -0.8), "f": P3(3.6, -0.8)}
    col = {"r": CYAN, "a": CYAN, "b": CYAN, "c": EMERALD, "d": EMERALD, "e": EMERALD, "f": EMERALD}
    N = {k: node(k, P[k], col[k]) for k in P}
    E = {"ra": elink(N["r"], N["a"]), "rb": elink(N["r"], N["b"]), "ac": elink(N["a"], N["c"]), "ad": elink(N["a"], N["d"]),
         "be": elink(N["b"], N["e"]), "bf": elink(N["b"], N["f"])}
    idxl = VGroup(*[T(str(i + 1), 18, TEXT_MUTED, MONO, True).next_to(N[k], DOWN, buff=0.15) for i, k in enumerate("cdef")])
    cnt = T("7 nút", 24, AMBER, SANS, True).move_to(P3(-5.2, 1.9))
    cnt2 = T("3 nút", 24, EMERALD, SANS, True).move_to(P3(-5.2, 1.9))
    ne1 = Line(P["r"], P["a"], buff=0.28, color=TEXT_MUTED, stroke_width=2.5)
    ne2 = Line(P["r"], P["b"], buff=0.28, color=TEXT_MUTED, stroke_width=2.5)
    V(s, "05_13", [
        ([FadeIn(hdr), *[Create(e) for e in E.values()], *[FadeIn(n) for n in N.values()], FadeIn(idxl), FadeIn(cnt)], 2.5),
        ([N["c"][0].animate.set_color(CORAL), N["e"][0].animate.set_color(CORAL), Indicate(N["c"]), Indicate(N["e"])], 2.0),
        ([N["a"][0].animate.set_color(CORAL), N["b"][0].animate.set_color(CORAL), E["ac"].animate.set_color(CORAL), E["be"].animate.set_color(CORAL)], 2.0),
        ([FadeOut(N["c"]), FadeOut(N["a"]), FadeOut(N["e"]), FadeOut(N["b"]), FadeOut(E["ra"]), FadeOut(E["rb"]),
          FadeOut(E["ac"]), FadeOut(E["ad"]), FadeOut(E["be"]), FadeOut(E["bf"]), FadeOut(idxl)], 1.5),
        ([N["d"].animate.move_to(P["a"]), N["f"].animate.move_to(P["b"])], 2.0),
        ([Create(ne1), Create(ne2), Transform(cnt, cnt2)], 1.5),
        ([FadeIn(take("RAKE: xóa lá và cha, nối anh em lên ông nội"))], 1.5),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_04 bitonic split
def seg_04(s):
    hdr = make_header("Bitonic Split: tách dãy thành hai nửa", "Chương 11", AMBER)
    vals = [2, 5, 7, 9, 8, 6, 4, 1]
    xs = [(i - 3.5) * 0.9 for i in range(8)]
    by = -0.5

    def bar(v, i, color):
        r = Rectangle(width=0.55, height=v * 0.24, color=color, fill_color=color, fill_opacity=0.8, stroke_width=1.5)
        t = T(str(v), 18, TEXT_MAIN, MONO, True).next_to(r, UP, buff=0.08)
        return VGroup(r, t).move_to(P3(xs[i], by + v * 0.12 + 0.18)).align_to(P3(0, by), DOWN) if False else VGroup(r, t)

    bars = []
    for i, v in enumerate(vals):
        r = Rectangle(width=0.55, height=v * 0.24, color=CYAN, fill_color=CYAN, fill_opacity=0.8, stroke_width=1.5)
        r.move_to(P3(xs[i], by + v * 0.12))
        t = T(str(v), 18, TEXT_MAIN, MONO, True).next_to(r, UP, buff=0.08)
        bars.append(VGroup(r, t))
    base = Line(P3(-4.2, by), P3(4.2, by), color=TEXT_MUTED, stroke_width=2)
    cap = T("Dãy bitonic: tăng rồi giảm", 20, TEXT_MUTED).move_to(P3(0, 2.3))
    cap2 = T("4 so sánh song song: i với i + 4", 20, AMBER, SANS, True).move_to(P3(0, 2.3))
    brs = []
    for i in range(4):
        y = by - 0.3 - 0.25 * i
        br = VMobject(color=RANKC[i], stroke_width=3).set_points_as_corners([P3(xs[i], by - 0.05), P3(xs[i], y), P3(xs[i + 4], y), P3(xs[i + 4], by - 0.05)])
        brs.append(br)
    p2, p3, p6, p7 = [b.get_center().copy() for b in (bars[2], bars[3], bars[6], bars[7])]
    def sw(i, j, col):
        dx = xs[j] - xs[i]
        g = bars[i]
        return AnimationGroup(g[0].animate.shift(RIGHT * dx).set_color(col).set_fill(col, 0.8), g[1].animate.shift(RIGHT * dx))
    left = [0, 1, 6, 7]
    right = [4, 5, 2, 3]
    tl = T("nửa nhỏ", 18, CYAN, SANS, True).move_to(P3(-1.8, -2.45))
    tr = T("nửa lớn", 18, AMBER, SANS, True).move_to(P3(1.8, -2.45))
    V(s, "05_04", [
        ([FadeIn(hdr), FadeIn(base), FadeIn(cap), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars], lag_ratio=0.1)], 2.5),
        ([Transform(cap, cap2)] + [Create(b) for b in brs], 3.0),
        ([sw(2, 6, AMBER), sw(6, 2, CYAN), sw(3, 7, AMBER), sw(7, 3, CYAN)], 2.5),
        ([FadeOut(b) for b in brs] + [bars[i][0].animate.set_color(AMBER).set_fill(AMBER, 0.8) for i in (4, 5)], 1.8),
        ([FadeIn(tl), FadeIn(tr)], 1.2),
        ([FadeIn(take("Mỗi nửa vẫn bitonic, lặp lại: log²n cột so sánh"))], 1.5),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_14 sample sort
def seg_14(s):
    hdr = make_header("Sample Sort trên 3 processor", "Chương 11", CYAN)
    data = [[14, 3, 9, 21, 6, 17], [8, 25, 1, 12, 19, 5], [11, 2, 23, 16, 7, 20]]
    ys = [1.5, 0.5, -0.5]
    cw, gap, X0 = 0.55, 0.62, -5.0
    mk = lambda v, x, y, c=BORDER_DIM: cell(str(v), cw, 0.5, c, 15).move_to(P3(x, y))
    plab = VGroup(*[T("P%d" % i, 16, RANKC[i], MONO, True).move_to(P3(-5.75, ys[i])) for i in range(3)])
    rows = [VGroup(*[mk(v, X0 + j * gap, ys[i]) for j, v in enumerate(d)]) for i, d in enumerate(data)]
    srt = [sorted(d) for d in data]
    lab = T("1 · Sắp xếp cục bộ", 20, TEXT_MUTED).move_to(P3(-2.5, 2.3))

    def nl(t):
        return Transform(lab, T(t, 20, TEXT_MUTED).move_to(P3(-2.5, 2.3)))

    srows = [VGroup(*[mk(v, X0 + j * gap, ys[i]) for j, v in enumerate(d)]) for i, d in enumerate(srt)]
    samples = [[srt[i][2], srt[i][4]] for i in range(3)]
    allsamp = [v for sm in samples for v in sm]
    ssorted = sorted(allsamp)
    sx = lambda k: 2.45 + k * 0.68
    samp_unsorted = VGroup(*[mk(v, sx(k), 1.5, AMBER) for k, v in enumerate(allsamp)])
    samp_sorted = VGroup(*[mk(v, sx(k), 1.5, AMBER) for k, v in enumerate(ssorted)])
    stxt = T("mẫu", 16, AMBER, SANS, True).move_to(P3(4.2, 2.15))
    spl = [ssorted[2], ssorted[4]]
    spl_t = T("splitter: %d và %d" % (spl[0], spl[1]), 18, CORAL, SANS, True).move_to(P3(4.2, 0.55))

    def bucket(v):
        return 0 if v <= spl[0] else (1 if v <= spl[1] else 2)
    BC = [CYAN, AMBER, EMERALD]
    # exchange targets
    dest = [[v for i in range(3) for v in srt[i] if bucket(v) == b] for b in range(3)]
    drows = [VGroup(*[mk(v, X0 + j * gap, ys[b], BC[b]) for j, v in enumerate(dest[b])]) for b in range(3)]
    for b in range(3):
        for c in drows[b]:
            c[0].set_stroke(BC[b]).set_fill(BC[b], 0.3)
    final = [VGroup(*[mk(v, X0 + j * gap, ys[b], BC[b]) for j, v in enumerate(sorted(dest[b]))]) for b in range(3)]
    for b in range(3):
        for c in final[b]:
            c[0].set_stroke(BC[b]).set_fill(BC[b], 0.3)
    curmap = {}

    steps = [([FadeIn(hdr), FadeIn(lab), FadeIn(plab), *[FadeIn(r) for r in rows]], 1.8),
             ([Transform(rows[i], srows[i]) for i in range(3)], 2.5)]
    samp_hl = []
    for i in range(3):
        for j in (2, 4):
            samp_hl.append(rows[i][j][0].animate.set_stroke(AMBER, width=5))
    steps.append(([nl("2 · Lấy 2 mẫu cách đều")] + samp_hl, 1.5))
    copies = []
    for i in range(3):
        for k, j in enumerate((2, 4)):
            copies.append(TransformFromCopy(rows[i][j], samp_unsorted[i * 2 + k]))
    steps.append(([FadeIn(stxt)] + copies, 2.5))
    steps.append(([nl("3 · Sắp xếp mẫu, chọn splitter"), Transform(samp_unsorted, samp_sorted)], 2.0))
    steps.append(([samp_unsorted[2][0].animate.set_stroke(CORAL, width=5).set_fill(CORAL, 0.5),
                   samp_unsorted[4][0].animate.set_stroke(CORAL, width=5).set_fill(CORAL, 0.5), FadeIn(spl_t)], 1.8))
    col_anims = []
    for i in range(3):
        for j, v in enumerate(srt[i]):
            b = bucket(v)
            col_anims.append(rows[i][j][0].animate.set_stroke(BC[b], width=3).set_fill(BC[b], 0.4))
    steps.append(([nl("4 · Chia bucket theo splitter")] + col_anims, 2.0))
    # exchange
    ex = []
    for b in range(3):
        for j, v in enumerate(dest[b]):
            src_i = [i for i in range(3) if v in srt[i]][0]
            src_j = srt[src_i].index(v)
            ex.append(ReplacementTransform(rows[src_i][src_j], drows[b][j]))
    steps.append(([nl("5 · Trao đổi all-to-all"), FadeOut(samp_unsorted), FadeOut(stxt), FadeOut(spl_t)] + ex, 3.0))
    steps.append(([nl("6 · Trộn cục bộ")] + [Transform(drows[b], final[b]) for b in range(3)], 2.5))
    V(s, "05_14", steps)
    clear_stage(s)


# ---------------------------------------------------------------- 05_15 CRCW quicksort pivot tree
def seg_15(s):
    hdr = make_header("CRCW Quicksort: cây pivot", "Chương 11", AMBER)
    vals = [5, 8, 2, 9, 1, 3, 7]
    cells = [cell(str(v), 0.8, 0.5, CYAN, 20).move_to(P3((i - 3) * 0.95, 2.1)) for i, v in enumerate(vals)]
    rootp = P3(0, 0.95)
    Pn = {5: rootp, 2: P3(-2.4, -0.2), 8: P3(2.4, -0.2), 1: P3(-3.6, -1.35), 3: P3(-1.2, -1.35), 7: P3(1.2, -1.35), 9: P3(3.6, -1.35)}
    N = {v: node(str(v), Pn[v], EMERALD, 0.28, 18) for v in Pn}
    arrows = VGroup(*[Line(c.get_bottom(), rootp + UP * 0.3, color=CORAL, stroke_width=2) for c in cells])
    arb = T("Arbitrary: 1 processor thắng", 18, CORAL, SANS, True).move_to(P3(4.2, 1.2))
    edges = [(5, 2), (5, 8), (2, 1), (2, 3), (8, 7), (8, 9)]
    E = {e: elink(N[e[0]], N[e[1]]) for e in edges}
    strip = [cell(str(v), 0.8, 0.5, EMERALD, 20).move_to(P3((i - 3) * 0.95, -2.4)) for i, v in enumerate([1, 2, 3, 5, 7, 8, 9])]
    ino = T("duyệt inorder", 18, TEXT_MUTED).move_to(P3(-5.0, -2.4))
    left = [cells[i] for i, v in enumerate(vals) if v in (2, 1, 3)]
    right = [cells[i] for i, v in enumerate(vals) if v in (8, 9, 7)]
    cell5 = cells[0]
    V(s, "05_15", [
        ([FadeIn(hdr), LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cells], lag_ratio=0.1)], 1.8),
        ([Create(arrows), FadeIn(arb)], 2.0),
        ([FadeOut(arrows), TransformFromCopy(cell5, N[5]), cell5[0].animate.set_color(EMERALD)], 2.0),
        ([c[0].animate.set_color(CYAN).set_fill(CYAN, 0.9) for c in left] + [c[0].animate.set_color(AMBER).set_fill(AMBER, 0.9) for c in right] + [FadeOut(arb)], 1.5),
        ([Create(E[(5, 2)]), Create(E[(5, 8)]), FadeIn(N[2]), FadeIn(N[8])], 2.0),
        ([Create(E[(2, 1)]), Create(E[(2, 3)]), Create(E[(8, 7)]), Create(E[(8, 9)]), FadeIn(N[1]), FadeIn(N[3]), FadeIn(N[7]), FadeIn(N[9])], 2.0),
        ([FadeIn(ino), LaggedStart(*[TransformFromCopy(N[v], strip[i]) for i, v in enumerate([1, 2, 3, 5, 7, 8, 9])], lag_ratio=0.5)], 4.0),
        ([FadeIn(take("Inorder của cây pivot = dãy đã sắp xếp"))], 1.5),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_05 Euler degree check
def seg_05(s):
    hdr = make_header("Kiểm tra Euler: bậc mọi đỉnh chẵn?", "Chương 12", VIOLET)
    # graph 1: bowtie
    G1 = {"A": P3(-4.6, 1.4), "B": P3(-4.6, -0.6), "C": P3(-3.1, 0.4), "D": P3(-1.6, 1.4), "E": P3(-1.6, -0.6)}
    G2 = {"F": P3(1.9, 1.4), "G": P3(4.3, 1.4), "H": P3(4.3, -0.6), "I": P3(1.9, -0.6)}
    N1 = {k: node(k, p, CYAN, 0.27, 17) for k, p in G1.items()}
    N2 = {k: node(k, p, CYAN, 0.27, 17) for k, p in G2.items()}
    ed1 = ["AB", "BC", "CA", "CD", "DE", "EC"]
    ed2 = ["FG", "GH", "HI", "IF", "FH"]
    E1 = [elink(N1[a], N1[b], r=0.27) for a, b in ed1]
    E2 = [elink(N2[a], N2[b], r=0.27) for a, b in ed2]
    deg1 = {"A": 2, "B": 2, "C": 4, "D": 2, "E": 2}
    deg2 = {"F": 3, "G": 2, "H": 3, "I": 2}
    dirs = {"A": UP, "B": DOWN, "C": DOWN, "D": UP, "E": DOWN, "F": UP, "G": UP, "H": DOWN, "I": DOWN}

    def dl(N, deg):
        return {k: T(str(d), 22, EMERALD if d % 2 == 0 else CORAL, MONO, True).next_to(N[k], dirs[k], buff=0.12) for k, d in deg.items()}
    D1 = dl(N1, deg1); D2 = dl(N2, deg2)
    ok = T("Có chu trình Euler", 22, EMERALD, SANS, True).move_to(P3(-3.1, -1.7))
    no = T("Không có (bậc lẻ)", 22, CORAL, SANS, True).move_to(P3(3.1, -1.7))
    V(s, "05_05", [
        ([FadeIn(hdr), *[Create(e) for e in E1 + E2], *[FadeIn(n) for n in list(N1.values()) + list(N2.values())]], 2.5),
        ([LaggedStart(*[FadeIn(d, scale=1.5) for d in list(D1.values()) + list(D2.values())], lag_ratio=0.15)], 3.0),
        ([N2["F"][0].animate.set_color(CORAL), N2["H"][0].animate.set_color(CORAL), Indicate(D2["F"]), Indicate(D2["H"])], 2.0),
        ([FadeIn(ok), FadeIn(no)], 1.5),
        ([FadeIn(take("Mỗi processor đếm bậc một đỉnh: Euler cần mọi bậc chẵn"))], 1.5),
    ])
    clear_stage(s)


# ---------------------------------------------------------------- 05_16 Floyd-Warshall
def seg_16(s):
    hdr = make_header("Floyd–Warshall: k tuần tự, (u,v) song song", "Chương 12", VIOLET)
    INF = float("inf")
    D = [[0, 3, INF, 9], [INF, 0, 1, INF], [INF, INF, 0, 2], [INF, INF, INF, 0]]
    fmt = lambda x: "∞" if x == INF else str(int(x))
    NP = [P3(-5.0, 1.0), P3(-2.8, 1.0), P3(-2.8, -1.4), P3(-5.0, -1.4)]
    N = [node(str(i + 1), NP[i], CYAN) for i in range(4)]
    def arr(i, j, w, off):
        a = Arrow(NP[i], NP[j], buff=0.3, color=TEXT_MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15, max_stroke_width_to_length_ratio=8)
        m = (NP[i] + NP[j]) / 2 + off
        return VGroup(a, T(str(w), 18, AMBER, MONO, True).move_to(m))
    EG = [arr(0, 1, 3, UP * 0.3), arr(1, 2, 1, RIGHT * 0.3), arr(2, 3, 2, DOWN * 0.3), arr(0, 3, 9, LEFT * 0.3)]
    cw, ch = 0.85, 0.62
    cpos = lambda i, j: P3(3.0 + (j - 1.5) * cw, 0.9 - i * ch)
    cells_ = [[cell(fmt(D[i][j]), cw - 0.05, ch - 0.05, BORDER_DIM, 18).move_to(cpos(i, j)) for j in range(4)] for i in range(4)]
    heads = VGroup(*[T(str(j + 1), 16, TEXT_MUTED, MONO, True).move_to(P3(cpos(0, j)[0], 1.55)) for j in range(4)],
                   *[T(str(i + 1), 16, TEXT_MUTED, MONO, True).move_to(P3(1.15, cpos(i, 0)[1])) for i in range(4)])
    allm = VGroup(*[c for r in cells_ for c in r])
    kt = T("", 22).move_to(P3(3.0, 2.15))
    steps = [([FadeIn(hdr), *[FadeIn(e) for e in EG], *[FadeIn(n) for n in N], FadeIn(allm), FadeIn(heads)], 2.5)]
    prev_hl = []
    cur = [r[:] for r in D]
    kt = T("k = 1", 22, AMBER, MONO, True).move_to(P3(3.0, 2.15))
    first = True
    for k in range(4):
        reset = []
        for (i, j) in prev_hl:
            reset.append(cells_[i][j][0].animate.set_stroke(BORDER_DIM, width=2).set_fill(PANEL_BG, 0.95))
        prev_hl = []
        hl = []
        for t in range(4):
            for (i, j) in ((k, t), (t, k)):
                if (i, j) not in prev_hl:
                    prev_hl.append((i, j))
                    hl.append(cells_[i][j][0].animate.set_stroke(AMBER, width=4))
        nodes_hl = [N[t][0].animate.set_color(AMBER if t == k else CYAN) for t in range(4)]
        ktn = T("k = %d" % (k + 1), 22, AMBER, MONO, True).move_to(P3(3.0, 2.15))
        if first:
            steps.append(([FadeIn(kt)] + hl + nodes_hl, 1.5)); first = False
        else:
            steps.append(([Transform(kt, ktn)] + reset + hl + nodes_hl, 1.5))
        new = [r[:] for r in cur]
        chg = []
        for i in range(4):
            for j in range(4):
                if cur[i][k] + cur[k][j] < cur[i][j]:
                    new[i][j] = cur[i][k] + cur[k][j]
                    chg.append((i, j))
        if chg:
            an = []
            for (i, j) in chg:
                an.append(Transform(cells_[i][j][1], T(fmt(new[i][j]), 18, EMERALD, MONO, True).move_to(cells_[i][j][1])))
                an.append(cells_[i][j][0].animate.set_fill(EMERALD, 0.45))
            steps.append((an, 1.8))
        cur = new
    steps.append(([FadeIn(take("Vòng k tuần tự; mọi cập nhật (u, v) trong một vòng chạy song song"))], 1.5))
    V(s, "05_16", steps)
    clear_stage(s)


# ---------------------------------------------------------------- 05_17 BFS
def seg_17(s):
    hdr = make_header("BFS song song theo từng tầng", "Chương 12", CYAN)
    P = {"s": P3(-4.8, 0.0), "a": P3(-2.6, 1.3), "b": P3(-2.6, -1.3), "c": P3(-0.4, 2.0), "d": P3(-0.4, 0.0), "e": P3(-0.4, -2.0), "f": P3(1.8, 0.0)}
    LC = [CYAN, EMERALD, AMBER, VIOLET]
    N = {k: node(k, p, BORDER_DIM) for k, p in P.items()}
    ed = ["sa", "sb", "ac", "ad", "bd", "be", "df", "ef"]
    E = {e: elink(N[e[0]], N[e[1]], r=0.28) for e in ed}
    levels = [["s"], ["a", "b"], ["c", "d", "e"], ["f"]]
    lvl_edges = [[], ["sa", "sb"], ["ac", "ad", "bd", "be"], ["df", "ef"]]
    barx = 3.7
    labs = VGroup(*[T("tầng %d" % i, 16, LC[i], SANS, True).move_to(P3(3.35, 1.2 - 0.7 * i)) for i in range(4)])
    bars = [Rectangle(width=0.7 * len(levels[i]), height=0.36, color=LC[i], fill_color=LC[i], fill_opacity=0.8, stroke_width=1)
            .move_to(P3(barx + 0.7 * len(levels[i]) / 2 + 0.2, 1.2 - 0.7 * i)) for i in range(4)]
    for i in range(4):
        bars[i].align_to(P3(4.2, 0), LEFT)
    conf = T("xung đột: 1 ghi thắng", 16, CORAL, SANS, True).move_to(P3(1.1, 1.05))
    steps = [([FadeIn(hdr), *[Create(e) for e in E.values()], *[FadeIn(n) for n in N.values()], FadeIn(labs)], 2.0)]
    steps.append(([N["s"][0].animate.set_color(LC[0]), FadeIn(bars[0])], 1.2))
    for L in (1, 2, 3):
        toks = []
        for e in lvl_edges[L]:
            toks.append(Dot(P[e[0]], radius=0.11, color=LC[L]))
        steps.append(([FadeIn(t) for t in toks] + [E[e].animate.set_color(LC[L]) for e in lvl_edges[L]], 0.8))
        moves = [toks[i].animate.move_to(P[lvl_edges[L][i][1]]) for i in range(len(toks))]
        steps.append((moves, 1.6))
        fin = [N[v][0].animate.set_color(LC[L]) for v in levels[L]] + [FadeOut(t) for t in toks] + [FadeIn(bars[L])]
        if L == 2:
            fin += [FadeIn(conf), Flash(N["d"], color=CORAL, flash_radius=0.6)]
        if L == 3:
            fin += [Flash(N["f"], color=CORAL, flash_radius=0.6)]
        if L == 3:
            fin += [FadeOut(conf)]
        steps.append((fin, 1.5))
    steps.append(([FadeIn(take("Mỗi tầng = một bước song song; Arbitrary CW chọn cha"))], 1.5))
    V(s, "05_17", steps)
    clear_stage(s)


# ---------------------------------------------------------------- 05_18 connected components
def seg_18(s):
    hdr = make_header("Thành phần liên thông: SV so với HCS", "Chương 12", EMERALD)
    PP = {1: P3(-4.2, 0.9), 2: P3(-2.2, 0.9), 3: P3(-0.2, 0.9), 4: P3(1.8, 0.9), 5: P3(-3.2, -1.7), 6: P3(-1.2, -1.7)}
    N = {k: node(str(k), p, BORDER_DIM, 0.3, 20) for k, p in PP.items()}
    gedges = [(1, 2), (2, 3), (3, 4), (5, 6)]
    GE = [elink(N[a], N[b], r=0.3, w=2) for a, b in gedges]

    def par(c, p, color=CYAN, ang=TAU / 6):
        a = CurvedArrow(N[c].get_top(), N[p].get_top(), angle=ang, color=color, stroke_width=3.5, tip_length=0.2)
        return a

    def par_low(c, p, color=CYAN):
        return CurvedArrow(N[c].get_bottom(), N[p].get_bottom(), angle=-TAU / 6, color=color, stroke_width=3.5, tip_length=0.2)
    a21, a32, a43 = par(2, 1), par(3, 2), par(4, 3)
    a65 = par_low(6, 5)
    a31 = par(3, 1, AMBER); a42 = par(4, 2, AMBER); a41 = par(4, 1, AMBER, TAU / 7)
    f1 = T("D(v) = D(D(v))", 22, AMBER, MONO, True).move_to(P3(4.5, 0.9))
    lab1 = T("1 · Grafting", 20, CYAN, SANS, True).move_to(P3(4.4, 2.0))
    lab2 = T("2 · Pointer jumping", 20, AMBER, SANS, True).move_to(P3(4.4, 2.0))
    hcs = T("HCS: ma trận kề, O(n²)", 18, CORAL, SANS, True).move_to(P3(4.2, 0.2))
    sv = T("SV: danh sách kề, O(m + n)", 18, EMERALD, SANS, True).move_to(P3(4.2, -0.4))
    trap = make_trap_banner("SV: vòng 1 không được grafting không điều kiện")
    V(s, "05_18", [
        ([FadeIn(hdr), *[Create(e) for e in GE], *[FadeIn(n) for n in N.values()]], 2.0),
        ([FadeIn(lab1), FadeIn(a21), FadeIn(a32), FadeIn(a43), FadeIn(a65)], 3.0),
        ([Transform(lab1, lab2), FadeIn(f1)], 1.5),
        ([Transform(a32, a31), Transform(a43, a42)], 3.0),
        ([Transform(a43, a41)], 2.5),
        ([N[k][0].animate.set_stroke(CYAN, width=4).set_fill(CYAN, 0.3) for k in (1, 2, 3, 4)] + [N[k][0].animate.set_stroke(AMBER, width=4).set_fill(AMBER, 0.3) for k in (5, 6)], 1.5),
        ([FadeOut(f1), FadeOut(lab1), FadeIn(hcs), FadeIn(sv), FadeIn(trap)], 2.0),
    ])
    clear_stage(s)


class Scene05Algorithms(Scene):
    def construct(self):
        setup_bg(self)
        seg_01(self)
        seg_10(self)
        seg_02(self)
        seg_11(self)
        seg_12(self)
        seg_19(self)
        seg_03(self)
        seg_13(self)
        seg_04(self)
        seg_14(self)
        seg_15(self)
        seg_05(self)
        seg_16(self)
        seg_17(self)
        seg_18(self)
        seg_05_06(self)
        seg_05_07(self)
        seg_05_08(self)
        seg_05_09(self)
        play_module_drills(self, "M5", "Ch 8-12")
