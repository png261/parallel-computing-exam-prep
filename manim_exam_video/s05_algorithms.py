from manim import *
from extras import seg_05_06, seg_05_07, seg_05_08, seg_05_09
from scene_utils import play_module_drills
from scene_utils import (
    setup_bg, make_header, make_card, make_trap_banner,
    clear_stage, play_voiced, make_grid_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, SANS, MONO
)


class Scene05Algorithms(Scene):
    def construct(self):
        setup_bg(self)

        # 05_01: Chapter 8 — QuickHull & Accelerated Cascading
        hdr = make_header("Module 5: QuickHull & Accelerated Cascading", "Chapter 8", VIOLET)
        qh = make_card(
            "Parallel QuickHull",
            [
                "• Split by min/max x-coords (u, v) -> Upper & Lower Hull",
                "• Pivot p = max |(p1 - p) × (p2 - p)|",
                "• Eliminate points inside △(p, p1, p2) (angle sum = 2π)",
                "• PRAM mapping uses arrays F[i], P[i], Q[i], T[i]",
            ],
            width=5.95, accent=CYAN, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.3)

        ac = make_card(
            "Accelerated Cascading: Find-Max (CRCW)",
            [
                "• Balanced Tree (EREW): W = O(n),  T = O(log n)",
                "• All-Pairs (CRCW):     W = O(n^2), T = O(1)",
                "• DLDT (CRCW):          W = O(n log log n), T = O(log log n)",
                "• Combined: Tree for ⌈log log log n⌉ levels -> m = n / log log n",
                "  then DLDT on m -> BOTH W = O(n) AND T = O(log2 log2 n)!",
            ],
            width=6.15, accent=EMERALD, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.3)

        play_voiced(self, "05_01", [
            ([FadeIn(hdr), FadeIn(qh)], 2.5),
            ([FadeIn(ac)], 3.2),
        ])
        clear_stage(self)

        # 05_02: Chapter 9 — Dense Matrices, Gaussian Elim & Heat PDE
        hdr = make_header("Dense Linear Algebra & 2D Heat PDE", "Chapter 9", CYAN)
        m1 = make_card(
            "Matrix-Vector & Matrix-Matrix",
            [
                "• MatVec 1D row: requires all-to-all broadcast of x",
                "• MatMul Simple 2D: sqrt(p) × sqrt(p) mesh",
                "• Cannon's Algorithm: initial skew + cyclic block shifts",
                "• DNS (3D): up to n^3 processors, reduces along 3rd axis",
            ],
            width=6.0, accent=CYAN, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.3)

        m2 = make_card(
            "Gaussian Elimination & Heat PDE",
            [
                "• Steps: Division + Rank-1 update",
                "• 1D cyclic beats block (balances shrinking active rows)",
                "• Cost-optimal: 1D pipelined (n procs) | 2D (n^2 procs)",
                "• 2D Heat PDE (5-pt stencil): MPI_Scatter -> halo Send/Recv",
                "  + local FD update -> MPI_Gather",
            ],
            width=6.1, accent=AMBER, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.3)

        play_voiced(self, "05_02", [
            ([FadeIn(hdr), FadeIn(m1)], 2.6),
            ([FadeIn(m2)], 2.8),
        ])
        clear_stage(self)

        # 05_03: Chapter 10 — Euler Tour & Tree Contraction
        hdr = make_header("Tree Algorithms: Euler Tour & RAKE Contraction", "Chapter 10", EMERALD)
        r_node = Circle(radius=0.24, color=CYAN, fill_color=PANEL_BG, fill_opacity=1).move_to(LEFT * 4.2 + UP * 1.75)
        r_txt = Text("r", font=MONO, font_size=15, color=TEXT_MAIN).move_to(r_node)
        l_node = Circle(radius=0.24, color=EMERALD, fill_color=PANEL_BG, fill_opacity=1).move_to(LEFT * 5.2 + UP * 0.75)
        l_txt = Text("v", font=MONO, font_size=15, color=TEXT_MAIN).move_to(l_node)
        ri_node = Circle(radius=0.24, color=AMBER, fill_color=PANEL_BG, fill_opacity=1).move_to(LEFT * 3.2 + UP * 0.75)
        ri_txt = Text("w", font=MONO, font_size=15, color=TEXT_MAIN).move_to(ri_node)
        e1 = Line(r_node.get_bottom(), l_node.get_top(), color=TEXT_MUTED)
        e2 = Line(r_node.get_bottom(), ri_node.get_top(), color=TEXT_MUTED)
        split_lbl = Text("3 copies: v[A] -> left[A] -> v[B] -> right[A] -> v[C]", font=MONO, font_size=13, color=AMBER).move_to(LEFT * 3.7 + DOWN * 0.1)

        rake = make_card(
            "Tree Contraction (RAKE -> 3 nodes)",
            [
                "• RAKE leaf v (p(v)!=r): delete v & p(v), sib(v)->p(p(v))",
                "• Leaf test (0,0,1): v[A] == v[B] == v[C]",
                "• Rounds: odd left -> odd right -> keep even Z (O(log n))",
            ],
            width=5.8, accent=VIOLET, title_size=17, body_size=13
        ).to_edge(LEFT, buff=0.45).to_edge(DOWN, buff=0.35)

        formulas = make_card(
            "Suffix-Sum Formulas (O(log n) EREW)",
            [
                "• Pre-order  (1, 0,  0): Pos  = |V| - v[A] + 1",
                "• In-order   (0, 1,  0): Pos  = |V| - v[B] + 1",
                "• Post-order (0, 0,  1): Pos  = |V| - v[C] + 1",
                "• Depth      (1, 0, -1): Depth = |v[A]|",
                "• Subtree    (0, 0,  1): Size = v[A] - v[C] + 1",
                "• Tree Root / Tree Suffix-Sum: O(log h) on CREW",
            ],
            width=6.15, accent=EMERALD, title_size=18, body_size=14, code_body=True
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.15)

        play_voiced(self, "05_03", [
            ([FadeIn(hdr), Create(e1), Create(e2), FadeIn(r_node, r_txt, l_node, l_txt, ri_node, ri_txt, split_lbl)], 2.2),
            ([FadeIn(formulas)], 2.6),
            ([FadeIn(rake)], 2.0),
        ])
        clear_stage(self)

        # 05_04: Chapter 11 — Sorting
        hdr = make_header("Parallel Sorting: Bitonic, Quicksort & Sample Sort", "Chapter 11", AMBER)
        bitonic = make_card(
            "Bitonic Sort & CRCW Quicksort",
            [
                "• Bitonic Split: splits bitonic seq into s1 <= s2 (both bitonic)",
                "• Bitonic Sorting Network depth: Θ(log^2 n) comparator cols",
                "• Mapped to Hypercube & Row-Major Shuffled Mesh",
                "• CRCW Quicksort (Arbitrary CW): build pivot binary tree,",
                "  read sorted order via inorder traversal",
            ],
            width=6.05, accent=AMBER, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.3)

        sample = make_card(
            "Sample Sort (Data-Driven Splitters)",
            [
                "1) Each proc sorts its local n/p elements",
                "2) Pick p - 1 equally spaced local samples",
                "3) Gather & sort p(p - 1) samples -> pick p - 1 splitters",
                "4) Partition local data into p buckets using splitters",
                "5) All-to-all exchange buckets -> local merge",
            ],
            width=6.05, accent=CYAN, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.3)

        play_voiced(self, "05_04", [
            ([FadeIn(hdr), FadeIn(bitonic)], 2.8),
            ([FadeIn(sample)], 2.6),
        ])
        clear_stage(self)

        # 05_05: Chapter 12 — Graphs, HCS & Shiloach-Vishkin
        hdr = make_header("Parallel Graph Algorithms: BFS, HCS & SV", "Chapter 12", CYAN)
        g_left = make_card(
            "Basic Graph Problems & Traversal",
            [
                "• Euler check: all degrees even | Clique: O(1) ERCW (k^2 procs)",
                "• Floyd-Warshall APSP: sequential k, parallel (u, v) inner",
                "• DFS: inherently recursive (no parallel equiv in slides)",
                "• Parallel BFS: level-by-level frontier F[1..n],",
                "  duplicate parent conflict resolved by CW-ACR!",
            ],
            width=6.0, accent=VIOLET, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.35)

        g_right = make_card(
            "Connected Components: HCS vs. SV",
            [
                "• HCS: Adj Matrix, star compression/round -> O(n^2) cost",
                "• SV (Shiloach-Vishkin): Adj List, O(m+n) cost, O(1)/round!",
                "  1) Grafting: D(r_i) = v  |  2) Pointer Jump: D(v) = D(D(v))",
                "  Root/child test: D(v) == D(D(v))",
                "  TRAP: General unconditioning grafting ONLY from iter 2+!",
            ],
            width=6.15, accent=EMERALD, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.35)
        trap = make_trap_banner("SV forbids general unconditioning grafting in iteration 1 so star trees cannot form cycles!")

        play_voiced(self, "05_05", [
            ([FadeIn(hdr), FadeIn(g_left)], 2.6),
            ([FadeIn(g_right), FadeIn(trap)], 3.0),
        ])
        clear_stage(self)
        seg_05_06(self)
        seg_05_07(self)
        seg_05_08(self)
        seg_05_09(self)
        play_module_drills(self, "M5", "Ch 8-12")
