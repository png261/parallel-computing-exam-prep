from manim import *
from scene_utils import play_module_drills
from scene_utils import (
    setup_bg, make_header, make_card, make_code_box, make_trap_banner,
    clear_stage, make_bar_chart, play_voiced, make_grid_box,
    CYAN, AMBER, EMERALD, CORAL, VIOLET, TEXT_MAIN, TEXT_MUTED, PANEL_BG, SANS, MONO
)


class Scene04CUDA(Scene):
    def construct(self):
        setup_bg(self)

        # 04_01: CPU vs GPU & Latency Hiding
        hdr = make_header("Module 4: CPU (Latency) vs. GPU (Throughput)", "Ch. 5 + RTX 4070", EMERALD)
        cpu = make_card(
            "CPU: Latency-Optimized",
            [
                "• Few complex cores + huge L3 caches",
                "• Branch prediction + out-of-order logic",
                "• Minimizes latency of 1–2 threads/core",
            ],
            width=5.9, accent=CYAN, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.45)

        gpu = make_card(
            "GPU: Throughput-Optimized (SMs)",
            [
                "• Thousands of simple cores in SMs",
                "• High-bandwidth GDDR / HBM memory",
                "• RTX 4070: 46 SMs = 5,888 cores | 438 GB/s",
                "• Zero-cost warp switching hides 400–800 cycle stall!",
            ],
            width=6.1, accent=EMERALD, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.45)

        warps = VGroup(*[make_grid_box(f"Warp {i}", w=1.45, h=0.55, color=AMBER if i == 1 else CYAN, font_size=13) for i in range(4)]).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.55)
        w_lbl = Text("Warp 0 stalls on DRAM -> SM instantaneously switches to Warp 1!", font=SANS, font_size=15, color=AMBER).next_to(warps, UP, buff=0.2)

        play_voiced(self, "04_01", [
            ([FadeIn(hdr), FadeIn(cpu)], 2.0),
            ([FadeIn(gpu)], 2.2),
            ([FadeIn(warps, w_lbl)], 1.6),
        ])
        clear_stage(self)

        # 04_02: Qualifiers, Thread Hierarchy & Indexing
        hdr = make_header("CUDA Execution Model & Thread Indexing", "Ch. 5 + Updated CUDA", CYAN)
        hier = VGroup(
            make_grid_box("Grid (blocks)", w=2.2, h=0.6, color=VIOLET, font_size=14),
            Arrow(ORIGIN, RIGHT * 0.6, color=TEXT_MUTED),
            make_grid_box("Block (<=1024 T)", w=2.3, h=0.6, color=EMERALD, font_size=14),
            Arrow(ORIGIN, RIGHT * 0.6, color=TEXT_MUTED),
            make_grid_box("Thread (SP)", w=1.9, h=0.6, color=CYAN, font_size=14),
        ).arrange(RIGHT, buff=0.18).move_to(UP * 1.95)

        code = make_code_box(
            [
                "__global__ void saxpy(int n, float a, float *x, float *y) {",
                "    int idx = blockIdx.x * blockDim.x + threadIdx.x;",
                "    if (idx < n) y[idx] = a * x[idx] + y[idx];",
                "}",
                "// Grid ceiling: nblocks = (n + blockSize - 1) / blockSize;",
                "// 2D Row-Major: ix = blockIdx.x*blockDim.x + threadIdx.x;",
                "//               iy = blockIdx.y*blockDim.y + threadIdx.y;",
                "//               idx = iy * dimx + ix;",
            ],
            width=11.8, font_size=14, accent=EMERALD, title_str="__global__ Rules: Host-launched, GPU-run, returns void, no variadics/static"
        ).move_to(DOWN * 0.35)

        play_voiced(self, "04_02", [
            ([FadeIn(hdr), FadeIn(hier)], 1.6),
            ([FadeIn(code)], 3.2),
        ])
        clear_stage(self)

        # 04_03: Async Launch & Block Independence
        hdr = make_header("Synchronization & Block Independence Rule", "Ch. 5 + Updated CUDA", CORAL)
        s1 = make_card(
            "Rule 1: Kernel Launch is Asynchronous!",
            [
                "• kernel<<<grid, block>>>(...) returns immediately to CPU",
                "• Call cudaDeviceSynchronize() (or blocking cudaMemcpy)",
                "  before reading GPU printf() or output arrays!",
                "• <<<1, 2000>>> FAILS: max 1024 threads per block!",
            ],
            width=6.05, accent=AMBER, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.25)

        s2 = make_card(
            "Rule 2: Blocks Are Independent!",
            [
                "• Threads in SAME block sync via __syncthreads()",
                "• Blocks run on SMs in arbitrary order, no preemption",
                "• Inter-block locks inside kernel can DEADLOCK",
                "  (waiting block holds SM needed by lock-holder block)!",
            ],
            width=6.05, accent=CORAL, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.25)

        play_voiced(self, "04_03", [
            ([FadeIn(hdr), FadeIn(s1)], 2.6),
            ([FadeIn(s2)], 2.6),
        ])
        clear_stage(self)

        # 04_04: Memory Hierarchy, Pinned & Unified Memory
        hdr = make_header("CUDA Memory Hierarchy, Pinned & Unified Memory", "Ch. 5 + 256 MiB Benchmark", VIOLET)
        mem = make_card(
            "Device Memory Levels",
            [
                "• Registers & Local: per-thread scope & lifetime",
                "• Shared (__shared__): per-block (~48 KB), few cycles,",
                "  does NOT persist across separate kernel launches",
                "• Global (DRAM): grid/app lifetime, 400–800 cycles",
            ],
            width=6.0, accent=CYAN, title_size=18, body_size=14
        ).to_edge(LEFT, buff=0.45).shift(UP * 0.25)

        xfer = make_card(
            "Host–Device Transfers (256 MiB)",
            [
                "• Pinned Host (cudaMallocHost): page-locked!",
                "  Boosts D2H from 21.3 -> 26.4 GB/s (req. for async)",
                "• Unified Memory (cudaMallocManaged):",
                "  No prefetch (page faults): 27.5 ms",
                "  With prefetch: 11.7 ms  |  GPU-resident: 1.23 ms!",
            ],
            width=6.1, accent=EMERALD, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.25)

        play_voiced(self, "04_04", [
            ([FadeIn(hdr), FadeIn(mem)], 2.6),
            ([FadeIn(xfer)], 2.8),
        ])
        clear_stage(self)

        # 04_05: SAXPY PCIe Bottleneck & Bandwidth Math
        hdr = make_header("SAXPY PCIe Bottleneck & Bandwidth Formula", "RTX 4070 (n = 2^26 floats)", CORAL)
        bars = make_bar_chart(
            values=[15.1, 1.84, 40.4],
            labels=["CPU Serial", "GPU Kernel", "GPU Total"],
            colors=[CYAN, EMERALD, CORAL],
            max_val=45.0, width=5.3, height=2.65, unit="ms"
        ).to_edge(LEFT, buff=0.55).shift(DOWN * 0.55)
        b_lbl = Text("1-Pass SAXPY: Kernel 8x faster, Total 2.7x SLOWER!", font=SANS, font_size=16, weight=BOLD, color=TEXT_MAIN).next_to(bars, UP, buff=0.18)

        math_card = make_card(
            "Exam Math & Optimization Labs",
            [
                "• H2D (25.2 ms) + Kernel (1.84 ms) + D2H (13.2 ms) = 40.4 ms",
                "• SAXPY accesses 3 floats/elem (read x, read y, write y):",
                "  BW = (3 * n * 4 bytes) / t_kernel",
                "• Fix: Keep data GPU-resident across multiple passes!",
                "• Labs: Strided access drops 447 -> 100 GB/s;",
                "  Warp divergence doubles runtime (0.62 -> 1.23 ms)",
            ],
            width=6.05, accent=AMBER, title_size=18, body_size=14
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.1)

        play_voiced(self, "04_05", [
            ([FadeIn(hdr), FadeIn(b_lbl), Create(bars)], 2.2),
            ([FadeIn(math_card)], 3.2),
        ])
        clear_stage(self)
        play_module_drills(self, "M4", "CUDA")
