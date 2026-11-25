from manim import *
from scene_utils import (
    setup_bg, make_header, make_card, clear_stage, play_voiced,
    CYAN, AMBER, EMERALD, CORAL
)


class Scene06Summary(Scene):
    def construct(self):
        setup_bg(self)

        hdr = make_header("Final Closed-Book Checklist & Exam Pacing", "60–70 Minutes", AMBER)
        left = make_card(
            "Must-Know Calculator Formulas",
            [
                "1. Amdahl: 1 / (P/N + (1-P)) -> max 1/(1-P)",
                "2. Metrics: S = Ts/Tp | E = S/p | To = p*Tp - Ts",
                "3. MPI Ping-Pong: t(n) = α + n/β (watch μs vs ms!)",
                "4. CUDA Grid: (n + B - 1)/B | idx = blockIdx.x*B + threadIdx.x",
                "5. SAXPY BW: (3 * n * 4 B) / t_kernel",
                "6. Euler Subtree: v[A] - v[C] + 1 | Post: |V| - v[C] + 1",
            ],
            width=6.1, accent=CYAN, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.4)

        right = make_card(
            "Top Code Traps to Spot Instantly",
            [
                "• C++: std::thread no join -> crash; volatile != sync",
                "• C++: false sharing -> alignas(64); 2 atomics != invariant",
                "• OMP: task vars default firstprivate (need shared(left))",
                "• OMP: masked replaces master; #pragma barrier typo ignored",
                "• OMP: static,1 primes bad; dynamic,1 uniform 100x slow",
                "• MPI: mutual Send > 4KB deadlocks -> Sendrecv / Isend+Irecv",
                "• CUDA: max 1024 threads/blk; launch async; PCIe dominates",
            ],
            width=6.1, accent=CORAL, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.4)

        pacing = make_card(
            "65-Minute Plan:  0–40m (MCQs)  |  40–60m (Short Essays)  |  60–65m (Verify Units & Traps)",
            ["Next: practice_quiz.html: Study mode (learn every answer), then Exam mode with the 65:00 timer"],
            width=12.25, accent=EMERALD, title_size=16, body_size=15
        ).to_edge(DOWN, buff=0.3)

        play_voiced(self, "06_01", [
            ([FadeIn(hdr), FadeIn(left), FadeIn(right)], 2.2),
            ([FadeIn(pacing, shift=UP * 0.15)], 1.2),
        ])
        clear_stage(self)
