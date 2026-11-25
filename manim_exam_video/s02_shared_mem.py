from manim import *
from scene_utils import play_module_drills
from scene_utils import (
    setup_bg, make_header, make_card, make_code_box, make_trap_banner,
    clear_stage, make_bar_chart, play_voiced, make_grid_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, SANS, MONO
)


class Scene02SharedMem(Scene):
    def construct(self):
        setup_bg(self)

        # 02_01: 3-Layer Linux Threading Stack
        hdr = make_header("Module 2: Shared-Memory Threading Stack", "Updated C++20 / OpenMP", EMERALD)
        l1 = make_card("Layer 1: C++20 std::jthread (libstdc++)  |  OpenMP (libgomp)", ["High-level threads, RAII, directives"], width=10.5, accent=CYAN, title_size=18, body_size=15).move_to(UP * 1.55)
        l2 = make_card("Layer 2: POSIX Threads (glibc)", ["pthread_create(), pthread_mutex_t, pthread_barrier_t"], width=10.5, accent=EMERALD, title_size=18, body_size=15).move_to(ORIGIN)
        l3 = make_card("Layer 3: Linux Kernel", ["clone3() system call  +  futex() fast userspace mutex"], width=10.5, accent=AMBER, title_size=18, body_size=15).move_to(DOWN * 1.55)
        a1 = Arrow(l1.get_bottom(), l2.get_top(), color=TEXT_MAIN, buff=0.06)
        a2 = Arrow(l2.get_bottom(), l3.get_top(), color=TEXT_MAIN, buff=0.06)

        play_voiced(self, "02_01", [
            ([FadeIn(hdr), FadeIn(l1)], 1.4),
            ([GrowArrow(a1), FadeIn(l2)], 1.4),
            ([GrowArrow(a2), FadeIn(l3)], 1.4),
        ])
        clear_stage(self)

        # 02_02: std::thread vs std::jthread & traps
        hdr = make_header("C++11 std::thread vs. C++20 std::jthread", "Updated C++20", EMERALD)
        c_left = make_code_box(
            [
                "// C++11 std::thread TRAP:",
                "std::thread t(fn); // forget join() -> std::terminate()!",
                "",
                "// C++20 std::jthread (RAII + stop_token):",
                "std::jthread w([](std::stop_token st) {",
                "    while (!st.stop_requested()) { work(); }",
                "}); // ~jthread() calls request_stop() + join()",
            ],
            width=6.25, font_size=13, accent=EMERALD, title_str="RAII Lifecycle & Cancellation"
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.25)

        c_right = make_code_box(
            [
                "// TRAP 1: Lambda Loop Capture",
                "for (int k = 0; k < nt; ++k)",
                "  v.emplace_back([&, k] { f(k); }); // BY VALUE!",
                "",
                "// TRAP 2: Wall-Clock Timing",
                "auto t0 = std::chrono::steady_clock::now();",
                "// NEVER use clock() -> sums CPU time across threads!",
            ],
            width=5.95, font_size=13, accent=AMBER, title_str="Capture & Timing Traps"
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.25)
        trap = make_trap_banner("std::async does NOT guarantee a thread pool (C++20 has no standard thread pool)!")

        play_voiced(self, "02_02", [
            ([FadeIn(hdr), FadeIn(c_left)], 2.2),
            ([FadeIn(c_right)], 2.2),
            ([FadeIn(trap)], 1.0),
        ])
        clear_stage(self)

        # 02_03: volatile UB & Sync Benchmarks
        hdr = make_header("Data Races, volatile & Sync Benchmarks", "4 Threads × 10^7 Increments", CORAL)
        bars = make_bar_chart(
            values=[1.399, 0.210, 0.002],
            labels=["mutex", "atomic", "local+merge"],
            colors=[CORAL, AMBER, EMERALD],
            max_val=1.55, width=5.4, height=2.7, unit="s"
        ).to_edge(LEFT, buff=0.55).shift(DOWN * 0.55)
        b_title = Text("Runtime Comparison (lower is better)", font=SANS, font_size=17, weight=BOLD, color=TEXT_MAIN).next_to(bars, UP, buff=0.18)

        sync_notes = make_card(
            "Why 700x Difference?",
            [
                "• volatile counter: NOT sync! Data race = UB (loses 60–70%!)",
                "• mutex in loop (1.399s): 40M kernel futex locks (sys=2.45s)",
                "• atomic in loop (0.210s): no kernel lock, but cache-line bounces",
                "• local + 1 merge (0.002s): zero contention -> 700x faster!",
            ],
            width=6.15, accent=CYAN, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.1)

        play_voiced(self, "02_03", [
            ([FadeIn(hdr), FadeIn(sync_notes[0], sync_notes[1][0], sync_notes[1][1][0])], 1.8),
            ([FadeIn(b_title), Create(bars)], 2.2),
            ([*[FadeIn(item) for item in sync_notes[1][1][1:]]], 2.0),
        ])
        clear_stage(self)

        # 02_04: atomic vs mutex (multi-var invariant) & std::barrier
        hdr = make_header("std::atomic vs. std::mutex & std::barrier", "Updated C++20", CYAN)
        inv_bad = make_code_box(
            [
                "// BROKEN multi-variable invariant (tong == 2*dem):",
                "dem.fetch_add(1);   // <- another thread reads HERE!",
                "tong.fetch_add(2);  // broke 6,135 times in 10^6 reads!",
            ],
            width=6.05, font_size=13, accent=CORAL, title_str="std::atomic: 1 Variable, 1 Op ONLY"
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.65)

        inv_ok = make_code_box(
            [
                "// CORRECT: std::mutex protects compound state",
                "std::scoped_lock lk(mtx);",
                "dem += 1; tong += 2; // 0 invariant breaks!",
            ],
            width=6.05, font_size=13, accent=EMERALD, title_str="std::mutex: Multi-Variable Invariants"
        ).to_edge(LEFT, buff=0.45).shift(DOWN * 1.2)

        bar_card = make_card(
            "C++20 std::barrier & Pthreads Map",
            [
                "• std::barrier sync(nt, swap_pointers);",
                "  Completion callback runs ONCE per phase",
                "  before releasing threads (saves 2nd barrier!)",
                "• std::counting_semaphore <-> sem_t",
                "• std::condition_variable <-> pthread_cond_t",
            ],
            width=5.95, accent=AMBER, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.2)

        play_voiced(self, "02_04", [
            ([FadeIn(hdr), FadeIn(inv_bad)], 2.0),
            ([FadeIn(inv_ok)], 1.6),
            ([FadeIn(bar_card)], 2.0),
        ])
        clear_stage(self)

        # 02_05: False Sharing & NUMA First-Touch
        hdr = make_header("False Sharing & NUMA First-Touch", "Performance Engineering", CORAL)
        slots = VGroup(*[make_grid_box(f"cnt[{i}]", w=1.05, h=0.65, color=CYAN, font_size=14) for i in range(4)]).arrange(RIGHT, buff=0.05).move_to(LEFT * 3.2 + UP * 1.0)
        cline = SurroundingRectangle(slots, color=CORAL, buff=0.14, stroke_width=2.5)
        cl_lbl = Text("ONE 64-byte Cache Line -> Invalidates across cores!", font=SANS, font_size=15, weight=BOLD, color=CORAL).next_to(cline, DOWN, buff=0.2)

        padded = VGroup(*[make_grid_box(f"alignas(64)\ncnt[{i}]", w=1.35, h=0.75, color=EMERALD, font_size=12) for i in range(3)]).arrange(RIGHT, buff=0.25).move_to(LEFT * 3.2 + DOWN * 1.25)

        fs_card = make_card(
            "Measured Impact & NUMA Rule",
            [
                "• 1 thread:  0.036 s",
                "• 8 threads (shared line): 0.719 s (20x SLOWER!)",
                "• Fix: alignas(64) (0.037 s) or local var (0.038 s)",
                "• NUMA First-Touch: OS allocates pages on the",
                "  NUMA node that FIRST WRITES them -> init in parallel!",
            ],
            width=5.85, accent=EMERALD, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.15)

        play_voiced(self, "02_05", [
            ([FadeIn(hdr), FadeIn(slots, cline, cl_lbl)], 1.8),
            ([cline.animate.set_fill(CORAL, opacity=0.3)], 0.6),
            ([cline.animate.set_fill(CORAL, opacity=0.0), FadeIn(padded)], 1.5),
            ([FadeIn(fs_card)], 2.0),
        ])
        clear_stage(self)

        # 02_06: OpenMP Fork-Join, Clauses & Pi Reduction
        hdr = make_header("OpenMP: Fork-Join, Scoping & Reduction", "Ch. 3 + Benchmarks", CYAN)
        m0 = Line(LEFT * 5.8 + UP * 1.85, LEFT * 4.0 + UP * 1.85, color=CYAN, stroke_width=4)
        fk = VGroup(*[Line(LEFT * 4.0 + UP * 1.85, LEFT * 2.0 + UP * (2.25 - i * 0.27), color=EMERALD, stroke_width=2.5) for i in range(4)])
        jn = VGroup(*[Line(LEFT * 2.0 + UP * (2.25 - i * 0.27), LEFT * 0.3 + UP * 1.85, color=EMERALD, stroke_width=2.5) for i in range(4)])
        m1 = Line(LEFT * 0.3 + UP * 1.85, RIGHT * 0.8 + UP * 1.85, color=CYAN, stroke_width=4)
        fj_lbl = Text("#pragma omp parallel (Fork-Join)", font=MONO, font_size=14, color=CYAN).next_to(fk, UP, buff=0.1)

        scope_card = make_card(
            "Data-Sharing Clauses",
            [
                "• private(x): uninitialized copy; outer x unchanged",
                "• firstprivate(x): init from outer; outer unchanged",
                "• lastprivate(x): sequentially last iter writes back",
                "• default(none): forces explicit scoping (best practice)",
            ],
            width=6.2, accent=AMBER, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(DOWN * 0.9)

        pi_bars = make_bar_chart(
            values=[1.230, 0.307, 0.001],
            labels=["critical", "atomic", "reduction"],
            colors=[CORAL, AMBER, EMERALD],
            max_val=1.35, width=5.3, height=2.65, unit="s"
        ).to_edge(RIGHT, buff=0.55).shift(DOWN * 0.55)
        pi_lbl = Text("Pi (n=10^7, 8 Threads): critical=176x slower!", font=SANS, font_size=16, weight=BOLD, color=TEXT_MAIN).next_to(pi_bars, UP, buff=0.18)

        play_voiced(self, "02_06", [
            ([FadeIn(hdr), Create(m0), FadeIn(fj_lbl), Create(fk), Create(jn), Create(m1)], 1.8),
            ([FadeIn(scope_card)], 2.2),
            ([FadeIn(pi_lbl), Create(pi_bars)], 2.0),
        ])
        clear_stage(self)

        # 02_07: OpenMP Scheduling Traps & 5.1/6.0 Updates
        hdr = make_header("OpenMP Scheduling Traps & Modern Updates", "Ch. 3 + OpenMP 5.1/6.0", VIOLET)
        sched = make_card(
            "Scheduling Benchmarks (8 Threads)",
            [
                "• static (default): contiguous, best cache locality",
                "• static,1 on Primes (<2e7): WORST (1.473s vs 1.015s)!",
                "  Even threads only get even numbers -> sit idle!",
                "• dynamic,1 on Uniform: 100x SLOWER (3.648s vs 0.039s)!",
                "• guided: large -> shrinking chunks (good for decreasing load)",
            ],
            width=6.15, accent=CORAL, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.25)

        upd = make_card(
            "OpenMP 5.1 / 6.0 & Task Traps",
            [
                "• #pragma omp masked replaces master (deprecated 5.1)",
                "  NO implicit barrier (unlike #pragma omp single)",
                "• #pragma omp task: vars default to FIRSTPRIVATE!",
                "  Must write shared(left) + #pragma omp taskwait + cutoff!",
                "• #pragma barrier (missing 'omp') = silently ignored!",
            ],
            width=6.0, accent=EMERALD, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.25)

        play_voiced(self, "02_07", [
            ([FadeIn(hdr), FadeIn(sched)], 3.0),
            ([FadeIn(upd)], 3.0),
        ])
        clear_stage(self)

        # 02_08: Java Multithreading
        hdr = make_header("Java Multithreading & Concurrency", "Chapter 6", CYAN)
        j1 = make_card(
            "Threads & Monitors",
            [
                "• Implement Runnable (preferred) or extend Thread",
                "• t.start() spawns thread | t.run() runs synchronously!",
                "• Deprecated unsafe: stop(), suspend(), resume()",
                "• wait()/notify()/notifyAll() MUST be in synchronized:",
                "  else throws IllegalMonitorStateException!",
                "• wait() atomically releases lock & reacquires on wake",
            ],
            width=6.1, accent=CYAN, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.2)

        j2 = make_card(
            "Locks, Conditions & Pools",
            [
                "• ExecutorService via Executors factory",
                "• ReentrantLock(true): fair (longest-waiting first),",
                "  prevents starvation at lower throughput",
                "• Condition: await()/signal()/signalAll() in while-loop",
                "• Bounded buffer: 1 Lock + 2 Conditions (notEmpty, notFull)",
                "• Semaphore(permits, fair): acquire() / release()",
            ],
            width=6.0, accent=EMERALD, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.2)

        play_voiced(self, "02_08", [
            ([FadeIn(hdr), FadeIn(j1)], 2.8),
            ([FadeIn(j2)], 2.8),
        ])
        clear_stage(self)
        play_module_drills(self, "M2", "C++ / OpenMP / Java")
