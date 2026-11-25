from manim import *
from extras import seg_01_09, seg_01_10
from scene_utils import play_module_drills
from scene_utils import (
    setup_bg, make_header, make_card, make_trap_banner, clear_stage,
    play_voiced, make_grid_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, SANS, MONO
)


class Scene01Foundations(Scene):
    def construct(self):
        setup_bg(self)

        # 01_01: Intro & Exam Profile
        title = Text("Parallel & High-Performance Computing", font=SANS, font_size=38, weight=BOLD, color=CYAN)
        sub = Text("Deep-Dive Voice Lecture — Chapters 1–12 + Updated C++20 / OpenMP / MPI / CUDA",
                   font=SANS, font_size=18, color=TEXT_MAIN).next_to(title, DOWN, buff=0.25)
        exam_card = make_card(
            "Exam Format & Rules",
            [
                "• 40–60 Objective MCQs  +  1–2 Short Essay Questions",
                "• Duration: 60–70 minutes",
                "• Closed-book: NO notes or electronics (pocket calculator ONLY)",
                "• Focus: Derivations, Code Traps, Complexities, Updated Specs",
            ],
            width=10.8, accent=AMBER, title_size=21, body_size=18
        ).next_to(sub, DOWN, buff=0.45)

        play_voiced(self, "01_01", [
            ([FadeIn(title, shift=UP * 0.2), FadeIn(sub)], 1.0),
            ([Create(exam_card[0]), FadeIn(exam_card[1])], 1.4),
        ])
        clear_stage(self)

        # 01_02: Why Serial Stopped (3 Physical Walls)
        hdr = make_header("Why Serial Scaling Stopped: 3 Physical Walls", "Chapter 1 & 5", CYAN)
        light_line = Line(LEFT * 5.6 + UP * 1.7, RIGHT * 0.5 + UP * 1.7, color=CYAN, stroke_width=4)
        light_lbl = Text("Speed of light: 30 cm / ns", font=MONO, font_size=15, color=CYAN).next_to(light_line, UP, buff=0.1)
        cu_line = Line(LEFT * 5.6 + UP * 0.95, LEFT * 3.7 + UP * 0.95, color=AMBER, stroke_width=4)
        cu_lbl = Text("Copper wire limit: 9 cm / ns (forces smaller chips)", font=MONO, font_size=15, color=AMBER).next_to(cu_line, RIGHT, buff=0.2)

        wall_mini = make_card(
            "Wall 2: Miniaturization",
            ["• Atomic/molecular limits on transistor size", "• Economic cost of pushing 1 core higher"],
            width=5.8, accent=VIOLET, title_size=18, body_size=15
        ).to_edge(LEFT, buff=0.55).shift(DOWN * 1.1)

        wall_pwr = make_card(
            "Wall 3: The Power Wall",
            ["• Power ~ Clock Frequency × Voltage^2", "• Voltage cannot drop further without losing 0 vs 1!"],
            width=5.8, accent=CORAL, title_size=18, body_size=15
        ).to_edge(RIGHT, buff=0.55).shift(DOWN * 1.1)

        play_voiced(self, "01_02", [
            ([FadeIn(hdr)], 0.5),
            ([Create(light_line), FadeIn(light_lbl), Create(cu_line), FadeIn(cu_lbl)], 1.6),
            ([FadeIn(wall_mini)], 1.2),
            ([FadeIn(wall_pwr)], 1.4),
        ])
        clear_stage(self)

        # 01_03: Flynn's Taxonomy
        hdr = make_header("Flynn's Classical Taxonomy (1966)", "Chapter 1", CYAN)
        cells = VGroup(
            make_card("SISD (Sequential)", ["1 Instruction, 1 Data stream", "Deterministic single-CPU PC"], width=5.9, accent=TEXT_MUTED, body_size=15),
            make_card("SIMD (Lockstep)", ["1 Instruction, Multiple Data", "Synchronous & deterministic (GPU warps)"], width=5.9, accent=CYAN, body_size=15),
            make_card("MISD (Experimental)", ["Multiple Instr, 1 Data stream", "Multi-filter signal / multi-cipher"], width=5.9, accent=VIOLET, body_size=15),
            make_card("MIMD (Most Common)", ["Multiple Instr, Multiple Data", "Sync or Async (Multi-core, Clusters)"], width=5.9, accent=EMERALD, body_size=15),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(DOWN * 0.2)

        play_voiced(self, "01_03", [
            ([FadeIn(hdr)], 0.5),
            ([FadeIn(cells[0])], 1.0),
            ([FadeIn(cells[1]), cells[1][0].animate.set_stroke(AMBER, width=3.5)], 1.4),
            ([cells[1][0].animate.set_stroke(CYAN, width=1.8), FadeIn(cells[2])], 1.2),
            ([FadeIn(cells[3])], 1.2),
        ])
        clear_stage(self)

        # 01_04: Memory Architectures (CC-UMA vs CC-NUMA vs Distributed)
        hdr = make_header("Memory Architectures & Scalability", "Chapter 1", AMBER)
        uma = make_card(
            "CC-UMA (SMP)",
            ["• Uniform access time", "• Single shared bus", "• Coherency hardware", "• Scales: 10s of procs"],
            width=3.85, accent=CYAN, title_size=18, body_size=14
        )
        numa = make_card(
            "CC-NUMA",
            ["• Links 2+ SMPs", "• Remote access slower", "• Coherency across link", "• Scales: 100s of procs"],
            width=3.85, accent=AMBER, title_size=18, body_size=14
        )
        dist = make_card(
            "Distributed Memory",
            ["• Private local RAM only", "• Explicit comm (MPI)", "• No coherency traffic", "• Scales: 1000s of procs"],
            width=3.85, accent=EMERALD, title_size=18, body_size=14
        )
        row = VGroup(uma, numa, dist).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        hyb = make_trap_banner("Today's largest supercomputers use Hybrid Distributed-Shared Memory (SMP nodes + MPI)!")

        play_voiced(self, "01_04", [
            ([FadeIn(hdr)], 0.5),
            ([FadeIn(uma)], 1.5),
            ([FadeIn(numa)], 1.5),
            ([FadeIn(dist), FadeIn(hyb)], 1.8),
        ])
        clear_stage(self)

        # 01_05: Performance Metrics & Worked Example
        hdr = make_header("Performance Metrics (Pocket-Calculator Formulas)", "Ch. 1 & Ch. 7", EMERALD)
        f_card = make_card(
            "Core Definitions",
            [
                "• Speedup:     S = Ts / Tp",
                "• Efficiency:  E = S / p = Ts / (p * Tp)",
                "• Cost (Work): Cost = p * Tp",
                "  Cost-optimal iff  p * Tp = Θ(Ts)",
                "• Overhead:    To = p * Tp - Ts",
            ],
            width=6.0, accent=CYAN, title_size=19, body_size=15, code_body=True
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.2)

        ex_card = make_card(
            "Worked Example: Ts = 120s, p = 8, Tp = 20s",
            [
                "1) S  = 120 / 20 = 6.0x",
                "2) E  = 6.0 / 8  = 0.75 = 75%",
                "3) Cost = 8 × 20 = 160 proc-sec",
                "4) To = 160 - 120 = 40 s overhead",
            ],
            width=5.9, accent=AMBER, title_size=18, body_size=15, code_body=True
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.2)
        iso_trap = make_trap_banner("Isoefficiency: LOWER problem-size growth rate with p means MORE scalable!")

        play_voiced(self, "01_05", [
            ([FadeIn(hdr), FadeIn(f_card)], 1.8),
            ([FadeIn(ex_card)], 2.0),
            ([FadeIn(iso_trap)], 1.0),
        ])
        clear_stage(self)

        # 01_06: Amdahl's Law
        hdr = make_header("Amdahl's Law: The Serial Bottleneck", "Chapter 1", AMBER)
        axes = Axes(
            x_range=[0, 100, 20], y_range=[0, 12, 2],
            x_length=5.4, y_length=3.3,
            axis_config={"color": TEXT_MUTED, "include_numbers": False, "include_ticks": True}
        ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.25)
        ticks = VGroup(
            *[Text(str(x), font=MONO, font_size=12, color=TEXT_MUTED).next_to(axes.c2p(x, 0), DOWN, buff=0.08) for x in (0, 20, 40, 60, 80, 100)],
            *[Text(str(y), font=MONO, font_size=12, color=TEXT_MUTED).next_to(axes.c2p(0, y), LEFT, buff=0.08) for y in (2, 4, 6, 8, 10, 12)],
        )
        c90 = axes.plot(lambda n: 1.0 / (0.90 / max(n, 1) + 0.10), x_range=[1, 100], color=CYAN, stroke_width=3)
        c50 = axes.plot(lambda n: 1.0 / (0.50 / max(n, 1) + 0.50), x_range=[1, 100], color=CORAL, stroke_width=3)
        asym = DashedLine(axes.c2p(0, 10), axes.c2p(100, 10), color=CYAN, stroke_width=1.5)
        l90 = Text("P=0.90 -> max 10x", font=SANS, font_size=14, color=CYAN).next_to(asym, UP, buff=0.05).align_to(asym, RIGHT)

        amd_card = make_card(
            "Amdahl's Law Walkthrough",
            [
                "• Formula: S(N) = 1 / (P/N + (1 - P))",
                "• Upper Bound (N -> ∞): 1 / (1 - P)",
                "• Exam Calc (P = 0.85, N = 17):",
                "  0.85 / 17 = 0.05",
                "  0.05 + 0.15 = 0.20",
                "  S(17) = 1 / 0.20 = 5.00x (max 6.67x)",
            ],
            width=6.0, accent=EMERALD, title_size=18, body_size=15, code_body=True
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.15)

        play_voiced(self, "01_06", [
            ([FadeIn(hdr), Create(axes), FadeIn(ticks)], 1.2),
            ([Create(c90), Create(c50), Create(asym), FadeIn(l90)], 1.8),
            ([FadeIn(amd_card)], 2.0),
        ])
        clear_stage(self)

        # 01_07: PRAM Hierarchy & Binary Tree Sum
        hdr = make_header("PRAM Models & Basic Parallel Paradigms", "Chapter 2", VIOLET)
        hier = Text("EREW  ⊂  CREW  ⊂  CRCW  (PCR / ECR / ACR / Combining)", font=MONO, font_size=18, weight=BOLD, color=AMBER).move_to(UP * 2.1)

        # Animated 4->2->1 Binary Tree
        lv0 = VGroup(*[make_grid_box(f"A[{i}]", w=0.85, h=0.5, color=CYAN, font_size=13) for i in range(4)]).arrange(RIGHT, buff=0.25).move_to(LEFT * 3.4 + DOWN * 0.7)
        lv1 = VGroup(*[make_grid_box("+", w=0.85, h=0.5, color=EMERALD, font_size=14) for _ in range(2)]).arrange(RIGHT, buff=1.35).move_to(LEFT * 3.4 + UP * 0.35)
        lv2 = make_grid_box("Sum", w=1.0, h=0.5, color=AMBER, font_size=14).move_to(LEFT * 3.4 + UP * 1.35)
        edges = VGroup(
            Line(lv0[0].get_top(), lv1[0].get_bottom(), color=TEXT_MUTED),
            Line(lv0[1].get_top(), lv1[0].get_bottom(), color=TEXT_MUTED),
            Line(lv0[2].get_top(), lv1[1].get_bottom(), color=TEXT_MUTED),
            Line(lv0[3].get_top(), lv1[1].get_bottom(), color=TEXT_MUTED),
            Line(lv1[0].get_top(), lv2.get_bottom(), color=TEXT_MUTED),
            Line(lv1[1].get_top(), lv2.get_bottom(), color=TEXT_MUTED),
        )

        pram_list = make_card(
            "4 Basic PRAM Paradigms (EREW, O(log n))",
            [
                "• Balanced Tree: Sum, Scalar Product, Boolean-AND",
                "• Doubling: Broadcast x from P1 to n procs",
                "• Pointer Jumping: List Ranking (3-step EREW)",
                "• Partitioning: Parallel Merge via Binary Search",
            ],
            width=6.05, accent=VIOLET, title_size=18, body_size=15
        ).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.25)

        play_voiced(self, "01_07", [
            ([FadeIn(hdr), FadeIn(hier)], 1.3),
            ([FadeIn(lv0)], 1.0),
            ([*[Create(e) for e in edges[:4]], FadeIn(lv1)], 1.2),
            ([*[Create(e) for e in edges[4:]], FadeIn(lv2), FadeIn(pram_list)], 1.8),
        ])
        clear_stage(self)

        # 01_08: DAG Critical Path & Loop Dependencies
        hdr = make_header("Decomposition, Critical Path & Loop Dependencies", "Chapter 7", CYAN)
        n1 = make_grid_box("T1(3)", w=1.0, h=0.5, color=CORAL).move_to(LEFT * 4.8 + UP * 1.1)
        n2 = make_grid_box("T2(5)", w=1.0, h=0.5, color=CORAL).move_to(LEFT * 2.8 + UP * 1.55)
        n3 = make_grid_box("T3(2)", w=1.0, h=0.5, color=CYAN).move_to(LEFT * 2.8 + UP * 0.55)
        n4 = make_grid_box("T4(4)", w=1.0, h=0.5, color=CORAL).move_to(LEFT * 0.8 + UP * 1.1)
        dag_e = VGroup(
            Arrow(n1.get_right(), n2.get_left(), color=CORAL, buff=0.05),
            Arrow(n1.get_right(), n3.get_left(), color=TEXT_MUTED, buff=0.05),
            Arrow(n2.get_right(), n4.get_left(), color=CORAL, buff=0.05),
            Arrow(n3.get_right(), n4.get_left(), color=TEXT_MUTED, buff=0.05),
        )
        cp_lbl = Text("Critical Path = 3 + 5 + 4 = 12 (min time)", font=SANS, font_size=15, weight=BOLD, color=CORAL).move_to(LEFT * 2.8 + DOWN * 0.15)

        dep_card = make_card(
            "Decompositions & Dependencies",
            [
                "• Exploratory (15-puzzle): speedup anomalies!",
                "• Speculative: misprediction -> rollback cost",
                "• Loop-Carried: iter i+1 needs iter i -> Sync/Comm",
                "• Loop-Independent: intra-iter only -> Parallel!",
            ],
            width=6.05, accent=EMERALD, title_size=18, body_size=15
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.25)
        trap = make_trap_banner("Equal work per processor does NOT guarantee load balance — DAG dependencies matter!")

        play_voiced(self, "01_08", [
            ([FadeIn(hdr), FadeIn(n1, n2, n3, n4), Create(dag_e)], 1.6),
            ([FadeIn(cp_lbl)], 1.2),
            ([FadeIn(dep_card), FadeIn(trap)], 2.0),
        ])
        clear_stage(self)
        seg_01_09(self)
        seg_01_10(self)
        play_module_drills(self, "M1", "Ch 1, 2, 7")
