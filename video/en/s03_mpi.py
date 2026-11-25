from manim import *
from scene_utils import play_module_drills
from scene_utils import (
    setup_bg, make_header, make_card, make_code_box, make_trap_banner,
    clear_stage, play_voiced, make_grid_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, SANS, MONO
)


class Scene03MPI(Scene):
    def construct(self):
        setup_bg(self)

        # 03_01: Communicator, 6 Golden Functions, Element Count & Non-Overtaking
        hdr = make_header("Module 3: MPI Foundations & Rules", "Ch. 4 + MPI-4.1", CYAN)
        comm_box = make_card(
            "Communicator = Group + Context",
            [
                "• Default: MPI_COMM_WORLD (ranks 0 .. size - 1)",
                "• Six Golden Functions:",
                "  MPI_Init(&argc, &argv)       MPI_Finalize()",
                "  MPI_Comm_size(comm, &size)   MPI_Comm_rank(comm, &rank)",
                "  MPI_Send(buf, count, type, dest, tag, comm)",
                "  MPI_Recv(buf, count, type, src, tag, comm, &status)",
            ],
            width=6.3, accent=CYAN, title_size=18, body_size=13, code_body=True
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.35)

        rules = make_card(
            "Point-to-Point Rules",
            [
                "• count = ELEMENT count (NOT bytes!)",
                "• Recv buffer must be >= incoming message",
                "• Non-overtaking: msgs from same (src, dest, comm)",
                "  always arrive in exact send order!",
                "• Wildcards (Recv only): MPI_ANY_SOURCE, MPI_ANY_TAG",
                "• Modes: Send, Ssend (sync), Bsend (buf), Rsend (ready)",
            ],
            width=5.85, accent=AMBER, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.35)

        play_voiced(self, "03_01", [
            ([FadeIn(hdr), FadeIn(comm_box)], 2.6),
            ([FadeIn(rules)], 2.6),
        ])
        clear_stage(self)

        # 03_02: Ping-Pong Latency/Bandwidth Model & Calculator Walkthrough
        hdr = make_header("Ping-Pong Cost Model: t(n) = α + n / β", "Updated Ch. 4", AMBER)
        n0 = make_grid_box("Rank 0", w=1.4, h=0.8, color=CYAN).move_to(LEFT * 4.5 + UP * 1.35)
        n1 = make_grid_box("Rank 1", w=1.4, h=0.8, color=EMERALD).move_to(LEFT * 0.8 + UP * 1.35)
        pkt = Dot(color=AMBER, radius=0.14).move_to(n0.get_right() + RIGHT * 0.2)
        path = Arrow(n0.get_right(), n1.get_left(), color=TEXT_MUTED, buff=0.1)

        bench = make_card(
            "Measured Latency (Ryzen 9900X)",
            [
                "• Same-chiplet shm: α = 0.106 μs, β <= 47 GB/s",
                "• Cross-chiplet shm: α = 0.274 μs, β ≈ 12 GB/s",
                "• TCP loopback: α = 2.63 μs (25x slower due to kernel!)",
                "• Rule: Aggregate small msgs into fewer large ones!",
            ],
            width=5.9, accent=CYAN, title_size=17, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(DOWN * 0.95)

        calc = make_card(
            "Calculator Walkthrough",
            [
                "Given: α = 2.5 μs, β = 20 GB/s (20×10^9 B/s)",
                "Message size: n = 1,000,000 B (1 MB)",
                "",
                "n / β = 10^6 / (20×10^9) = 50 × 10^-6 s = 50.0 μs",
                "t(n)  = 2.5 μs + 50.0 μs = 52.5 μs (one-way)",
                "Round-trip = 2 × 52.5 = 105.0 μs",
            ],
            width=5.95, accent=EMERALD, title_size=18, body_size=14, code_body=True
        ).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.45)

        play_voiced(self, "03_02", [
            ([FadeIn(hdr, n0, n1, path, pkt)], 1.0),
            ([pkt.animate.move_to(n1.get_left() + LEFT * 0.2)], 1.2),
            ([FadeIn(bench)], 1.8),
            ([FadeIn(calc)], 2.2),
        ])
        clear_stage(self)

        # 03_03: Eager vs Rendezvous Deadlock + 3 Fixes
        hdr = make_header("Eager vs. Rendezvous Deadlock & 3 Safe Fixes", "Updated Ch. 4", CORAL)
        r0 = make_grid_box("Rank 0\nSend(1); Recv(1);", w=2.3, h=1.0, color=CYAN, font_size=13).move_to(LEFT * 4.7 + UP * 1.5)
        r1 = make_grid_box("Rank 1\nSend(0); Recv(0);", w=2.3, h=1.0, color=EMERALD, font_size=13).move_to(LEFT * 0.5 + UP * 1.5)
        a01 = Arrow(r0.get_right() + UP * 0.18, r1.get_left() + UP * 0.18, color=CORAL)
        a10 = Arrow(r1.get_left() + DOWN * 0.18, r0.get_right() + DOWN * 0.18, color=CORAL)
        dl = Text("N > 4096 B (Rendezvous): BOTH BLOCK!", font=SANS, font_size=15, weight=BOLD, color=CORAL).next_to(VGroup(r0, r1), DOWN, buff=0.22)

        eager = make_card(
            "OpenMPI Eager Limit = 4096 B",
            [
                "• N=1004 ints (4016 B + hdr): Eager -> passes",
                "• N=1005 ints (4020 B + hdr): Rendezvous -> DEADLOCKS!",
                "• Testing tip: run with MPI_Ssend + odd ranks!",
            ],
            width=5.8, accent=AMBER, title_size=17, body_size=14
        ).to_edge(LEFT, buff=0.45).to_edge(DOWN, buff=0.4)

        fixes = make_code_box(
            [
                "// 1. Ordered (even Send/Recv, odd Recv/Send)",
                "// 2. MPI_Sendrecv (combined atomic exchange):",
                "MPI_Sendrecv(out, N, MPI_INT, peer, 0,",
                "             in,  N, MPI_INT, peer, 0, comm, ...);",
                "// 3. Non-blocking (never touch buffers early):",
                "MPI_Irecv(..., &r[0]); MPI_Isend(..., &r[1]);",
                "MPI_Waitall(2, r, MPI_STATUSES_IGNORE);",
            ],
            width=6.05, font_size=13, accent=EMERALD, title_str="3 Deadlock-Free Solutions"
        ).to_edge(RIGHT, buff=0.45).to_edge(DOWN, buff=0.4)

        play_voiced(self, "03_03", [
            ([FadeIn(hdr, r0, r1)], 1.0),
            ([GrowArrow(a01), GrowArrow(a10), FadeIn(dl), FadeIn(eager)], 2.6),
            ([FadeIn(fixes)], 2.8),
        ])
        clear_stage(self)

        # 03_04: Collectives
        hdr = make_header("MPI Collective Operations (O(log p) Tree)", "Ch. 4 + Updated Notes", EMERALD)
        grid = VGroup(
            make_card("MPI_Bcast", ["Root sends 1 value to all"], width=3.9, accent=CYAN, title_size=17, body_size=14),
            make_card("Scatter / Gather", ["Split from / collect to root"], width=3.9, accent=CYAN, title_size=17, body_size=14),
            make_card("MPI_Allgather", ["Every rank gets full array"], width=3.9, accent=AMBER, title_size=17, body_size=14),
            make_card("Reduce vs Allreduce", ["Result on root vs ALL ranks"], width=3.9, accent=EMERALD, title_size=17, body_size=14),
            make_card("MPI_Scan (Prefix)", ["Rank i gets v0 + ... + vi"], width=3.9, accent=VIOLET, title_size=17, body_size=14),
            make_card("MPI_Alltoall", ["Personalized transpose"], width=3.9, accent=CORAL, title_size=17, body_size=14),
        ).arrange_in_grid(rows=2, cols=3, buff=0.28).move_to(UP * 0.2)
        rule = make_trap_banner("ALL ranks in the communicator MUST call the exact same collectives in the exact same order!")

        play_voiced(self, "03_04", [
            ([FadeIn(hdr)], 0.6),
            ([LaggedStart(*[FadeIn(c, scale=0.95) for c in grid], lag_ratio=0.18)], 3.8),
            ([FadeIn(rule)], 1.0),
        ])
        clear_stage(self)

        # 03_05: Timing, Halo MPI_PROC_NULL, Primes Cyclic Trap & Hybrid
        hdr = make_header("MPI Timing, Halo Exchange, Load Balance & Hybrid", "Updated Ch. 4", VIOLET)
        left = make_card(
            "Timing & Boundary Halo",
            [
                "• Timing: MPI_Barrier -> MPI_Wtime()",
                "  -> MPI_Reduce(&t, &tmax, ..., MPI_MAX, 0, comm)",
                "• Halo Exchange: boundary ranks use MPI_PROC_NULL",
                "  up = (rank > 0) ? rank - 1 : MPI_PROC_NULL;",
                "  -> MPI_Sendrecv becomes a safe no-op!",
            ],
            width=6.05, accent=CYAN, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.25)

        right = make_card(
            "Load Balance & Hybrid MPI+OpenMP",
            [
                "• Primes < 2e7 (12 ranks):",
                "  block: 0.721s | cyclic: 1.539s (WORST!) | mgr-wkr: 0.554s",
                "  Why? With p=12, only ranks {1,5,7,11} get primes > 3!",
                "• Hybrid MPI + OpenMP (1 rank/node + threads):",
                "  MPI_Init_thread(..., MPI_THREAD_FUNNELED, ...)",
            ],
            width=6.1, accent=AMBER, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.25)

        play_voiced(self, "03_05", [
            ([FadeIn(hdr), FadeIn(left)], 2.8),
            ([FadeIn(right)], 3.0),
        ])
        clear_stage(self)
        play_module_drills(self, "M3", "MPI")
