from manim import *
from scene_utils import (
    setup_bg, make_header, make_card, make_trap_banner, clear_stage, play_voiced,
    make_grid_box, make_bar_chart, make_code_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, SANS, MONO,
)


def seg_01_09(self):
    hdr = make_header("Decomposition Techniques & Task Mapping", "Chapter 7", VIOLET)
    dec = make_card(
        "4 Decomposition Techniques",
        [
            "• Recursive: divide & conquer (quicksort, min)",
            "• Data: partition input/output/intermediate",
            "    -> owner-computes rule (most widely used)",
            "• Exploratory: search space (15-puzzle)",
            "    -> speedup anomalies (super/sub-linear)",
            "• Speculative: guess next branch; may waste/undo",
            "• Hybrid: mix of the above",
        ],
        width=6.1, accent=VIOLET, title_size=18, body_size=14,
    ).to_edge(LEFT, buff=0.45).shift(DOWN * 0.15)

    # block vs cyclic strip (8 rows over 4 procs)
    cols = [CYAN, AMBER, EMERALD, CORAL]
    def strip(owner, label):
        cells = VGroup(*[
            Square(0.3, color=cols[o], fill_color=cols[o], fill_opacity=0.55, stroke_width=1.2)
            for o in owner
        ]).arrange(RIGHT, buff=0.04)
        t = Text(label, font=MONO, font_size=13, color=TEXT_MAIN).next_to(cells, LEFT, buff=0.15)
        return VGroup(t, cells)
    s_block = strip([p for p in range(4) for _ in range(4)], "Block       ")
    s_cyc = strip([p for _ in range(4) for p in range(4)], "Cyclic      ")
    s_bc = strip([p for _ in range(2) for p in range(4) for _ in range(2)], "Block-cyc(2)")
    strips = VGroup(s_block, s_cyc, s_bc).arrange(DOWN, aligned_edge=RIGHT, buff=0.18)
    map_card = make_card(
        "Mapping: Static vs Dynamic",
        [
            "• Static: before run; known, uniform task cost",
            "• Dynamic: during run; unknown / generated tasks",
            "   - Centralized: master-slave work queue",
            "   - Distributed: push or pull (work stealing)",
        ],
        width=6.1, accent=EMERALD, title_size=18, body_size=14,
    )
    right = VGroup(strips, map_card).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.15)
    trap = make_trap_banner("Equal task COUNT per processor != load balance (task sizes + DAG matter)")
    play_voiced(self, "01_09", [
        ([FadeIn(hdr)], 0.5),
        ([FadeIn(dec, shift=RIGHT * 0.1)], 3.5),
        ([LaggedStart(*[FadeIn(s) for s in strips], lag_ratio=0.4)], 2.5),
        ([FadeIn(map_card), FadeIn(trap)], 2.0),
    ])
    clear_stage(self)


def seg_01_10(self):
    hdr = make_header("Overheads, Scalability & Isoefficiency", "Chapter 7", EMERALD)
    src = make_card(
        "Sources of Overhead  To = p*Tp - Ts",
        ["• Interprocess communication", "• Idling: imbalance, sync, serial parts", "• Excess computation"],
        width=6.1, accent=CORAL, title_size=17, body_size=14,
    )
    ex = make_card(
        "Worked: add n numbers on p procs",
        [
            "Tp = n/p + 2 log2 p",
            "n=64,  p=8: Tp = 8 + 6 = 14",
            "   S = 64/14 = 4.57   E = 57%",
            "n=512, p=8: Tp = 64 + 6 = 70",
            "   S = 512/70 = 7.31  E = 91%",
            "To = 2p log p  ->  W = Θ(p log p)",
        ],
        width=6.1, accent=AMBER, title_size=17, body_size=15, code_body=True,
    )
    left = VGroup(src, ex).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(LEFT, buff=0.45).shift(DOWN * 0.2)
    chart = make_bar_chart([57, 80, 91], ["n=64", "n=192", "n=512"], [CORAL, AMBER, EMERALD],
                           max_val=100, width=4.6, height=2.6, unit="%")
    ctitle = Text("Efficiency at p = 8 as n grows", font=SANS, font_size=16, weight=BOLD, color=TEXT_MAIN)
    rgrp = VGroup(ctitle, chart).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.8).shift(UP * 0.2)
    trap = make_trap_banner("Fixed n, more p -> E falls.  Fixed p, more n -> E rises.  Slower isoefficiency = more scalable")
    play_voiced(self, "01_10", [
        ([FadeIn(hdr), FadeIn(src)], 2.0),
        ([FadeIn(ex)], 3.0),
        ([FadeIn(ctitle), Create(chart[0]), Create(chart[1])], 1.0),
        ([LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart[2]], lag_ratio=0.5)], 3.0),
        ([FadeIn(trap)], 1.0),
    ])
    clear_stage(self)


def seg_05_06(self):
    hdr = make_header("Worked Trace: Prefix Sum by Pointer Jumping", "Chapter 10", CYAN)
    rows = [
        ("A  ", [3, 1, 4, 1, 5, 9, 2, 6], TEXT_MUTED),
        ("d=1", [3, 4, 5, 5, 6, 14, 11, 8], CYAN),
        ("d=2", [3, 4, 8, 9, 11, 19, 17, 22], AMBER),
        ("d=4", [3, 4, 8, 9, 14, 23, 25, 31], EMERALD),
    ]
    grid = VGroup()
    for lbl, vals, col in rows:
        cells = VGroup(*[make_grid_box(str(v), w=0.85, h=0.55, color=col, font_size=17) for v in vals]).arrange(RIGHT, buff=0.12)
        t = Text(lbl, font=MONO, font_size=17, color=col).next_to(cells, LEFT, buff=0.3)
        grid.add(VGroup(t, cells))
    grid.arrange(DOWN, buff=0.38, aligned_edge=RIGHT).move_to(LEFT * 1.6 + UP * 0.25)
    # arrows showing distance for one element per step
    def arrow(r_from, r_to, i_src, i_dst, col):
        a = grid[r_from][1][i_src]
        b = grid[r_to][1][i_dst]
        return Arrow(a.get_bottom(), b.get_top(), buff=0.04, color=col, stroke_width=3, max_tip_length_to_length_ratio=0.2)
    a1 = VGroup(arrow(0, 1, 6, 7, CYAN), arrow(0, 1, 7, 7, CYAN))
    a2 = VGroup(arrow(1, 2, 5, 7, AMBER), arrow(1, 2, 7, 7, AMBER))
    a3 = VGroup(arrow(2, 3, 3, 7, EMERALD), arrow(2, 3, 7, 7, EMERALD))
    info = make_card(
        "Rule",
        ["P_k[i] = P_k-1[i] + P_k-1[i - 2^(k-1)]", "Steps: log2 n  (8 -> 3)", "Model: EREW PRAM", "Cost n log n: not cost-optimal", "Tree root finding: O(log h)"],
        width=4.0, accent=VIOLET, title_size=16, body_size=13, code_body=True,
    ).to_edge(RIGHT, buff=0.35).shift(UP * 0.2)
    play_voiced(self, "05_06", [
        ([FadeIn(hdr), FadeIn(grid[0])], 2.5),
        ([FadeIn(info)], 2.0),
        ([Create(a1), FadeIn(grid[1])], 3.0),
        ([FadeOut(a1), Create(a2), FadeIn(grid[2])], 3.0),
        ([FadeOut(a2), Create(a3), FadeIn(grid[3])], 3.5),
    ])
    clear_stage(self)


def seg_05_07(self):
    hdr = make_header("Worked Trace: Euler Tour on a Binary Tree", "Chapter 10", VIOLET)
    pos = {1: LEFT * 4.6 + UP * 1.7, 2: LEFT * 5.6 + UP * 0.6, 3: LEFT * 3.6 + UP * 0.6,
           4: LEFT * 6.2 + DOWN * 0.5, 5: LEFT * 5.0 + DOWN * 0.5, 6: LEFT * 3.6 + DOWN * 0.5}
    nodes = {k: VGroup(Circle(0.28, color=CYAN, fill_color=PANEL_BG, fill_opacity=1, stroke_width=2),
                       Text(str(k), font=MONO, font_size=18, color=TEXT_MAIN)).move_to(p) for k, p in pos.items()}
    edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), color=TEXT_MUTED, stroke_width=2)
                     for a, b in [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]])
    for n in nodes.values():
        n.set_z_index(2)
    tree = VGroup(edges, *nodes.values())
    seq = ["1A", "2A", "4A", "4B", "4C", "2B", "5A", "5B", "5C", "2C", "1B", "3A", "6A", "6B", "6C", "3B", "3C", "1C"]
    w_pre = [1 if s.endswith("A") else 0 for s in seq]
    suf = [sum(w_pre[i:]) for i in range(len(seq))]
    cells = VGroup()
    for s, w, sv in zip(seq, w_pre, suf):
        col = AMBER if s.endswith("A") else TEXT_MUTED
        box = make_grid_box(s, w=0.62, h=0.42, color=col, font_size=13)
        wt = Text(str(w), font=MONO, font_size=12, color=col).next_to(box, DOWN, buff=0.06)
        st = Text(str(sv), font=MONO, font_size=13, weight=BOLD, color=EMERALD).next_to(wt, DOWN, buff=0.06)
        cells.add(VGroup(box, wt, st))
    cells.arrange(RIGHT, buff=0.05).to_edge(DOWN, buff=1.05)
    if cells.width > 12.8:
        cells.scale_to_fit_width(12.8)
    lbl_w = Text("w", font=MONO, font_size=12, color=TEXT_MUTED).next_to(cells[0][1], LEFT, buff=0.12)
    lbl_s = Text("S", font=MONO, font_size=12, color=EMERALD).next_to(cells[0][2], LEFT, buff=0.12)
    table = make_card(
        "Same list, different weights",
        [
            "Preorder : A=1 B=0 C=0  pos = |V| - v[A] + 1",
            "Inorder  : A=0 B=1 C=0  pos = |V| - v[B] + 1",
            "Postorder: A=0 B=0 C=1  pos = |V| - v[C] + 1",
            "Depth    : A=1 B=0 C=-1 depth = |v[A]|",
            "Size(C=1): v[A] - v[C] + 1  (node 2: 6-4+1=3)",
        ],
        width=7.4, accent=EMERALD, title_size=16, body_size=13, code_body=True,
    ).to_edge(RIGHT, buff=0.35).shift(UP * 0.95)
    result = Text("Preorder: 1 -> 2 -> 4 -> 5 -> 3 -> 6", font=MONO, font_size=17, weight=BOLD, color=AMBER).to_edge(DOWN, buff=0.35)
    play_voiced(self, "05_07", [
        ([FadeIn(hdr), Create(edges), *[FadeIn(n) for n in nodes.values()]], 3.5),
        ([LaggedStart(*[FadeIn(c[0]) for c in cells], lag_ratio=0.15)], 4.0),
        ([*[FadeIn(c[1]) for c in cells], FadeIn(lbl_w)], 2.5),
        ([LaggedStart(*[FadeIn(c[2]) for c in reversed(cells)], lag_ratio=0.1), FadeIn(lbl_s)], 3.0),
        ([FadeIn(result)], 2.5),
        ([FadeIn(table)], 2.0),
    ])
    clear_stage(self)


def seg_05_08(self):
    hdr = make_header("Worked Trace: Bitonic Sort on 8 Elements", "Chapter 11", AMBER)
    stages = [
        ("input", [3, 7, 4, 8, 6, 2, 1, 5]),
        ("stage 1 (pairs ↑↓)", [3, 7, 8, 4, 2, 6, 5, 1]),
        ("stage 2 (bitonic)", [3, 4, 7, 8, 6, 5, 2, 1]),
        ("split d=4", [3, 4, 2, 1, 6, 5, 7, 8]),
        ("split d=2", [2, 1, 3, 4, 6, 5, 7, 8]),
        ("split d=1", [1, 2, 3, 4, 5, 6, 7, 8]),
    ]
    rows = VGroup()
    for i, (lbl, vals) in enumerate(stages):
        cols = [CYAN] * 8
        if lbl.startswith("split d=4"):
            cols = [CYAN] * 4 + [CORAL] * 4
        if i == len(stages) - 1:
            cols = [EMERALD] * 8
        cells = VGroup(*[make_grid_box(str(v), w=0.6, h=0.42, color=c, font_size=16) for v, c in zip(vals, cols)]).arrange(RIGHT, buff=0.08)
        t = Text(lbl, font=MONO, font_size=14, color=TEXT_MUTED).next_to(cells, LEFT, buff=0.25)
        rows.add(VGroup(t, cells))
    rows.arrange(DOWN, buff=0.17, aligned_edge=RIGHT).to_edge(LEFT, buff=0.5).shift(DOWN * 0.15)
    side = make_card(
        "Bitonic split of s (length n)",
        [
            "s1[i] = min(s[i], s[i+n/2])",
            "s2[i] = max(s[i], s[i+n/2])",
            "every s1 <= every s2; both bitonic",
            "",
            "Depth for n = 2^k:",
            "  1 + 2 + ... + k = k(k+1)/2",
            "  n=8 -> 6 cols, n=16 -> 10",
            "  Θ(log² n) comparator columns",
        ],
        width=5.1, accent=AMBER, title_size=16, body_size=14, code_body=True,
    ).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.15)
    play_voiced(self, "05_08", [
        ([FadeIn(hdr), FadeIn(rows[0])], 2.5),
        ([FadeIn(rows[1])], 3.0),
        ([FadeIn(rows[2])], 4.0),
        ([FadeIn(rows[3]), FadeIn(side)], 5.0),
        ([FadeIn(rows[4]), FadeIn(rows[5])], 3.5),
    ])
    clear_stage(self)


def seg_05_09(self):
    hdr = make_header("Case Study: Heat Equation as an SPMD MPI Program", "Chapter 9", CORAL)
    stencil = make_code_box(
        [
            "dC = D/(dx*dx) * (u + d + l + r - 4*c)",
            "C  = C + dt * dC          // each step",
        ],
        width=6.4, font_size=15, accent=VIOLET, title_str="5-point stencil (explicit Euler)",
    ).to_edge(LEFT, buff=0.45).shift(UP * 1.45)
    steps = make_card(
        "SPMD steps (row decomposition)",
        [
            "B1  Root reads input grid m x n",
            "B2  mc = m / NP rows per rank",
            "B3  MPI_Scatter(C, mc*n, ...) from root",
            "B4  loop: exchange boundary rows Cu, Cd",
            "         then compute FD on local rows",
            "B5  MPI_Gather(Cs, mc*n, ...) to root",
        ],
        width=6.4, accent=CYAN, title_size=17, body_size=14, code_body=True,
    ).next_to(stencil, DOWN, buff=0.25).align_to(stencil, LEFT)
    ranks = VGroup()
    cols = [CYAN, AMBER, EMERALD]
    for r in range(3):
        rect = Rectangle(width=3.6, height=1.0, color=cols[r], fill_color=cols[r], fill_opacity=0.18, stroke_width=2)
        t = Text(f"CPU{r}: mc rows", font=MONO, font_size=14, color=TEXT_MAIN).move_to(rect)
        ranks.add(VGroup(rect, t))
    ranks.arrange(DOWN, buff=0.45).to_edge(RIGHT, buff=1.4).shift(UP * 0.1)
    halo = VGroup()
    for r in range(2):
        down = Arrow(ranks[r].get_bottom() + RIGHT * 0.8, ranks[r + 1].get_top() + RIGHT * 0.8, buff=0.04, color=AMBER, stroke_width=3)
        up = Arrow(ranks[r + 1].get_top() + LEFT * 0.8, ranks[r].get_bottom() + LEFT * 0.8, buff=0.04, color=EMERALD, stroke_width=3)
        halo.add(down, up)
    hl = VGroup(
        Text("last row -> next rank's Cu", font=MONO, font_size=12, color=AMBER),
        Text("first row -> prev rank's Cd", font=MONO, font_size=12, color=EMERALD),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ranks, DOWN, buff=0.25)
    trap = make_trap_banner("Neighbour dependency: shared memory = sync; distributed = communication + sync")
    play_voiced(self, "05_09", [
        ([FadeIn(hdr), FadeIn(stencil)], 4.0),
        ([FadeIn(steps)], 3.0),
        ([LaggedStart(*[FadeIn(r) for r in ranks], lag_ratio=0.3)], 2.5),
        ([Create(halo), FadeIn(hl)], 3.0),
        ([FadeIn(trap)], 1.0),
    ])
    clear_stage(self)
