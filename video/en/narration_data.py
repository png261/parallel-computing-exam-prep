"""
Deep-dive narration scripts for all 6 modules of Parallel & High-Performance Computing.
Strictly grounded in Chapters 1-12 + updated C++20/OpenMP/MPI/CUDA lecture notes.
"""

SEGMENTS = {
    # ================= MODULE 1: FOUNDATIONS (Ch 1, 2, 7) =================
    "01_01": (
        "Welcome to the complete deep-dive exam review for Parallel and High-Performance Computing. "
        "Your exam is closed-book with only a pocket calculator allowed, consisting of forty to sixty multiple choice questions "
        "plus one or two short essays in sixty to seventy minutes. Let us master every concept, derivation, and code trap step by step."
    ),
    "01_02": (
        "Why did single-core CPUs stop getting faster? Three physical walls stopped serial scaling. "
        "First, transmission speed: light travels thirty centimeters per nanosecond, and signals in copper travel only nine centimeters per nanosecond. "
        "Second, atomic limits on transistor miniaturization. Third, the Power Wall: dynamic power scales as frequency times voltage squared, "
        "and voltage cannot drop lower without losing the distinction between zero and one."
    ),
    "01_03": (
        "Flynn's taxonomy classifies architectures by instruction and data streams. "
        "SISD is a classic single-CPU sequential computer. SIMD executes one instruction in synchronous lockstep across multiple data elements, "
        "just like GPU warps or vector pipelines. MISD feeds one data stream into multiple instruction streams, used conceptually in multi-filter signal processing. "
        "MIMD is today's norm: independent cores or nodes running different instructions on different data, either synchronously or asynchronously."
    ),
    "01_04": (
        "Next, compare memory architectures. In CC-UMA or symmetric multiprocessors, all cores share one memory bus with uniform latency, "
        "but bus and cache-coherency traffic limit scaling to tens of processors. "
        "CC-NUMA links multiple SMPs together, reaching hundreds of processors, though remote memory across the link is slower than local memory. "
        "Distributed memory scales to thousands of processors because each node has private RAM and zero hardware coherency overhead, "
        "at the cost of explicit message-passing code."
    ),
    "01_05": (
        "Now let us work through the pocket-calculator formulas you must memorize. "
        "Speedup S equals serial time Ts divided by parallel time Tp. Efficiency E equals speedup divided by processor count p. "
        "Cost is p times Tp, and a formulation is cost-optimal when p times Tp matches the best serial complexity Theta of Ts. "
        "Total parallel overhead To equals p times Tp minus Ts. For example, if Ts is 120 seconds and 8 processors finish in 20 seconds, "
        "speedup is 6, efficiency is 75 percent, and overhead is 160 minus 120, which equals 40 seconds."
    ),
    "01_06": (
        "Amdahl's Law bounds speedup when a fraction S equal to 1 minus P must run serially. "
        "With N processors, speedup is 1 divided by the quantity P over N plus 1 minus P. "
        "As N approaches infinity, speedup can never exceed 1 over 1 minus P. "
        "With 90 percent parallel code, even ten thousand processors stay below 10x speedup. "
        "Walk through an exam example: if P is 0.85 and N is 17, then 0.85 over 17 is 0.05, plus 0.15 serial gives 0.20, so speedup is exactly 5.00x."
    ),
    "01_07": (
        "Chapter 2 introduces the idealized PRAM model: unit-time shared memory without communication latency, used to prove theoretical lower bounds. "
        "Notice the hierarchy: EREW is strictly weaker than CREW, which is weaker than CRCW. Any algorithm valid on EREW works on CREW and CRCW, never the reverse. "
        "On EREW PRAM, balanced binary tree reduction, doubling broadcast, and pointer-jumping list ranking all achieve O of log n time using O of n processors."
    ),
    "01_08": (
        "Chapter 7 formalizes decomposition and dependencies. In a task-dependency DAG, the critical path—the longest weighted path—sets the minimum parallel time. "
        "Be careful of exploratory decomposition, like searching a 15-puzzle: it can exhibit speedup anomalies, either superlinear speedup or engineered slow-down. "
        "Finally, distinguish loop dependencies: a loop-carried dependency crosses iterations and requires synchronization or communication, "
        "while a loop-independent dependency stays inside each iteration so iterations can run freely in parallel."
    ),

    # ================= MODULE 2: C++20 THREADS, OPENMP, JAVA (Ch 3, 6 + chuong3_vi) =================
    "02_01": (
        "Module 2 covers shared-memory programming with C++20 threads, OpenMP, and Java concurrency. "
        "On Linux, both C++ std::jthread in libstdc++ and OpenMP directives in libgomp compile down to POSIX threads in glibc, "
        "which invoke Linux kernel clone3 and futex system calls."
    ),
    "02_02": (
        "Watch the crucial difference between C++11 std::thread and C++20 std::jthread. "
        "If a joinable std::thread goes out of scope without calling join or detach, the program immediately calls std::terminate and crashes. "
        "std::jthread fixes this using RAII: its destructor automatically calls request_stop and join, and it passes a std::stop_token for clean cooperative cancellation. "
        "Also remember two classic C++ bugs: always capture loop indices by value, like bracket ampersand comma k, to avoid a data race, "
        "and use std::chrono::steady_clock for wall-clock timing because clock() sums CPU time across all threads."
    ),
    "02_03": (
        "Never mistake volatile for thread synchronization! In C++, any unsynchronized concurrent read and write where at least one is a write is a data race—which is Undefined Behavior. "
        "In the course benchmark with 4 threads doing 10 million increments each, a volatile counter lost 60 to 70 percent of updates. "
        "Putting a std::mutex inside the loop took 1.399 seconds because of 40 million kernel lock calls. "
        "Using std::atomic reduced that to 0.210 seconds, but cores still bounced the cache line. "
        "Accumulating in a local variable and merging once at the end took just 0.002 seconds—700 times faster than a per-iteration mutex!"
    ),
    "02_04": (
        "When do you choose std::atomic versus std::mutex? "
        "std::atomic only protects one variable and one operation. If you have an invariant across two variables, like sum equals 2 times count, "
        "updating two separate atomics breaks the invariant thousands of times; you must protect both together with a std::mutex and std::scoped_lock. "
        "In C++20, std::barrier even accepts a completion callback that executes once per phase—for instance swapping grid pointers in the 2D heat equation—eliminating a second barrier."
    ),
    "02_05": (
        "One of the most subtle hardware traps is False Sharing. Suppose 8 threads increment different elements cnt[0] through cnt[7] of a shared array. "
        "There is no data race, yet all 8 slots sit inside the same 64-byte CPU cache line! "
        "Every write invalidates the cache line on the other 7 cores, slowing 8 threads down to 0.719 seconds—20 times slower than a single thread! "
        "The fix is either padding each slot with alignas(64) or accumulating in thread-local variables. "
        "Similarly, on NUMA servers, Linux first-touch places memory pages on whichever NUMA node writes them first, so always initialize arrays in parallel using the same loop partitioning as computation."
    ),
    "02_06": (
        "Now let us turn to OpenMP's fork-join model and data-scoping clauses. "
        "With private(x), each thread receives an uninitialized local copy, and the original variable outside stays untouched. "
        "With firstprivate(x), each copy is initialized from the outer value, while the outer variable still stays unchanged afterward. "
        "With lastprivate(x), the thread running the sequentially last iteration writes its value back to the original variable. "
        "And for reductions, never put critical or atomic inside a tight loop: in the 8-thread pi benchmark, critical was 176 times slower than serial, "
        "atomic was 44 times slower, whereas reduction(+:sum) gave a 7.9x speedup."
    ),
    "02_07": (
        "OpenMP loop scheduling and modern updates hold several high-frequency exam traps. "
        "Default static scheduling gives contiguous blocks with great cache locality. "
        "Never use static,1 for prime counting: even-numbered threads receive only even numbers, finish immediately, and leave odd threads doing all the work! "
        "Conversely, never use dynamic,1 on a uniform loop: dispatching one iteration at a time adds 100x synchronization overhead. "
        "For OpenMP 5.1 and 6.0 updates: #pragma omp masked replaces #pragma omp master, which is deprecated, and neither has an implicit barrier—unlike #pragma omp single, which does. "
        "And inside #pragma omp task, variables default to firstprivate, so you must write shared(left) and call #pragma omp taskwait, plus use a cutoff threshold!"
    ),
    "02_08": (
        "Finally, review Chapter 6 on Java Multithreading. Prefer implementing Runnable over extending Thread, and always call start() to spawn a thread—calling run() directly runs synchronously on the caller's thread. "
        "Monitor methods wait(), notify(), and notifyAll() must be called inside a synchronized block on the same object, otherwise Java throws IllegalMonitorStateException. "
        "Remember wait() atomically releases the lock and reacquires it upon wakeup, and should always sit inside a while loop. "
        "Explicit ReentrantLock(true) enables fairness for the longest-waiting thread, preventing starvation at slightly lower throughput."
    ),

    # ================= MODULE 3: MPI (Ch 4 + chuong4_mpi_vi) =================
    "03_01": (
        "Module 3 covers distributed-memory programming with MPI. Every MPI communicator combines a Group of processes and a Context domain; the default is MPI_COMM_WORLD. "
        "Memorize the six golden functions: MPI_Init, MPI_Finalize, MPI_Comm_size, MPI_Comm_rank, MPI_Send, and MPI_Recv. "
        "A crucial rule: count specifies the number of elements of the MPI_Datatype, never the number of bytes! "
        "Also, MPI guarantees non-overtaking: two messages sent in order between the same sender and receiver in the same communicator arrive in exact send order."
    ),
    "03_02": (
        "For pocket-calculator questions, know the ping-pong communication model: one-way time t(n) equals alpha plus n divided by beta, "
        "where alpha is latency and beta is bandwidth. Small messages are latency-bound, while large messages are bandwidth-bound, "
        "so always aggregate many small messages into fewer large ones. "
        "On the Ryzen benchmark, shared-memory latency was 0.106 microseconds, whereas TCP loopback latency jumped 25 times higher to 2.63 microseconds because of the OS kernel stack. "
        "For example, if alpha is 2.5 microseconds and beta is 20 gigabytes per second, a 1-megabyte message takes 2.5 plus 50, equaling 52.5 microseconds."
    ),
    "03_03": (
        "Why does mutual MPI_Send between Rank 0 and Rank 1 work for small arrays and deadlock for large ones? "
        "Because MPI uses two protocols. Small messages—up to 4096 bytes including header in OpenMPI shared memory—use the Eager protocol: MPI copies the data into a buffer and MPI_Send returns immediately. "
        "At 1005 integers, exceeding 4096 bytes, MPI switches to the Rendezvous protocol: MPI_Send blocks until the matching MPI_Recv starts. Both ranks block forever! "
        "Three clean fixes exist: first, ordered Send/Recv across even and odd ranks; second, combined MPI_Sendrecv, ideal for halo exchanges; "
        "and third, non-blocking MPI_Irecv plus MPI_Isend followed by MPI_Waitall—making sure you never read or modify buffers before Wait completes. "
        "Pro testing tip: test with MPI_Ssend and odd rank counts to expose latent deadlocks."
    ),
    "03_04": (
        "MPI collective operations scale in O of log p steps using tree algorithms, and every process in the communicator must call the same collectives in the exact same order. "
        "Distinguish them carefully: MPI_Bcast sends one value to all; Scatter splits an array and Gather collects chunks to root; "
        "MPI_Allgather gives every rank the full concatenated array; MPI_Reduce combines to root while MPI_Allreduce gives the reduced result to every rank; "
        "MPI_Scan computes an inclusive prefix reduction where rank i receives elements 0 through i; and MPI_Alltoall performs a personalized transpose exchange."
    ),
    "03_05": (
        "Three practical MPI patterns frequently tested on exams: First, to time an MPI job, call MPI_Barrier, record MPI_Wtime before and after work, "
        "and take MPI_Reduce with MPI_MAX, because parallel runtime equals the slowest rank. "
        "Second, in 2D Heat Jacobi halo exchanges, assign boundary neighbors to MPI_PROC_NULL so MPI_Sendrecv executes a safe no-op without special-case if-branches. "
        "Third, in the 12-rank prime counting benchmark, cyclic partitioning was slowest at 1.539 seconds because only ranks 1, 5, 7, and 11 receive numbers coprime to 2 and 3, starving 8 ranks! Dynamic manager-worker won at 0.554 seconds. "
        "And for hybrid MPI plus OpenMP across nodes, initialize with MPI_Init_thread and MPI_THREAD_FUNNELED."
    ),

    # ================= MODULE 4: CUDA (Ch 5 + chuong5_cuda_vi) =================
    "04_01": (
        "Module 4 covers GPU programming with CUDA. While CPUs are latency-optimized with large caches and branch predictors, "
        "GPUs are throughput-optimized: thousands of simpler cores grouped into Streaming Multiprocessors, or SMs, backed by high-bandwidth GDDR or HBM memory. "
        "An RTX 4070 packs 46 SMs totaling 5,888 CUDA cores and 438 gigabytes per second of empirical memory bandwidth. "
        "Instead of huge caches, GPUs hide 400 to 800 cycles of global DRAM latency via massive multithreading—switching instantaneously to another ready warp whenever one warp stalls."
    ),
    "04_02": (
        "Understand the CUDA execution model and indexing math. A __global__ kernel is launched from the host CPU, executes on the GPU, and must return void. "
        "Threads are grouped into blocks—with a hard hardware limit of 1,024 threads per block—and blocks form a grid. "
        "To compute the grid size, use integer ceiling division: (n + blockSize - 1) / blockSize. "
        "In 1D, global index idx equals blockIdx.x times blockDim.x plus threadIdx.x. "
        "In 2D row-major images of width dimx, compute ix for column and iy for row, then idx equals iy times dimx plus ix. Always guard bounds with if (idx < n)."
    ),
    "04_03": (
        "Two vital CUDA synchronization rules: First, kernel launches are asynchronous! The CPU immediately moves to the next line, so you must call cudaDeviceSynchronize() or a blocking cudaMemcpy before reading results. "
        "Second, blocks are completely independent and execute in arbitrary order without preemption. Threads inside the same block share fast __shared__ memory and synchronize via __syncthreads(), "
        "but inter-block lock synchronization inside a kernel can deadlock if a waiting block occupies an SM needed by the lock-holding block."
    ),
    "04_04": (
        "Let us examine CUDA's memory hierarchy and host-device transfers. Registers and local memory belong to each thread. "
        "Shared memory—around 48 kilobytes per block with few-cycle latency—lives only for the duration of the block and does not persist across kernel launches. "
        "Global DRAM persists across sequential launches. To speed up PCIe transfers, allocate pinned page-locked host memory with cudaMallocHost, which boosted D2H speed to 26.4 gigabytes per second. "
        "Unified Memory via cudaMallocManaged shares one pointer across CPU and GPU, dropping from 27.5 milliseconds with on-demand page faults down to 11.7 milliseconds with prefetch, and 1.23 milliseconds when already resident."
    ),
    "04_05": (
        "Here is a classic exam calculation: the SAXPY PCIe bottleneck. On an RTX 4070 for 67 million floats, the SAXPY kernel itself ran in just 1.84 milliseconds—8 times faster than the CPU's 15.1 milliseconds. "
        "However, host-to-device copy took 25.2 milliseconds and device-to-host took 13.2 milliseconds, making total GPU time 40.4 milliseconds—more than twice as slow as the CPU! "
        "Why? Because SAXPY has low arithmetic intensity: each element reads x, reads y, and writes y—12 bytes per float. Effective kernel bandwidth is 3 times n times 4 bytes divided by t_kernel. "
        "To beat the CPU, keep data resident on the GPU across multiple kernel operations so PCIe transfer is amortized. Also recall from the performance labs that non-coalesced strided memory drops bandwidth from 447 to 100 GB/s, and warp branch divergence doubles kernel runtime."
    ),

    # ================= MODULE 5: ALGORITHMS Ch 8-12 =================
    "05_01": (
        "Module 5 synthesizes the parallel algorithms from Chapters 8 through 12. "
        "In Chapter 8, Parallel QuickHull finds min and max x-coordinate vertices, picks a pivot maximizing cross-product distance from the baseline, eliminates interior points whose triangle angle sum equals 2 pi, and recurses in parallel. "
        "Next, Accelerated Cascading combines a fast but non-optimal algorithm with a slower cost-optimal one. "
        "For Find-Max on CRCW PRAM: a balanced tree takes O(log n) time and O(n) work; all-pairs comparison takes O(1) time but O(n squared) work; and a Doubly Logarithmic Depth Tree takes O(log log n) time and O(n log log n) work. "
        "By running the balanced tree for ceil(log log log n) levels to shrink candidates to n over log log n, then running DLDT, we achieve BOTH optimal O(n) work AND O(log log n) time!"
    ),
    "05_02": (
        "Chapter 9 covers dense linear algebra and PDEs. For 1D matrix-vector multiplication, each rank needs the whole vector x via an all-to-all broadcast. "
        "For matrix-matrix multiplication on a 2D mesh, Cannon's algorithm stays memory-efficient by initially skewing A and B blocks and performing cyclic shifts. The 3D DNS algorithm scales up to n cubed processors. "
        "In Gaussian elimination, cyclic row mapping balances shrinking active rows much better than block mapping; 1D pipelined is cost-optimal with n processors, and 2D pipelined with n squared processors. "
        "And for the 2D Heat PDE 5-point stencil, each time step exchanges boundary ghost rows with neighbors before updating interior points."
    ),
    "05_03": (
        "Chapter 10 uses Prefix Sum, Pointer Jumping, and the Euler Tour Technique to parallelize trees in O(log n) time. "
        "For a binary tree, split every node v into three linked-list copies: v[A] before visiting left, v[B] between left and right, and v[C] after right. "
        "Running parallel Suffix Sum on this list answers every tree query using exact formulas: "
        "With Pre-order weights (1, 0, 0), position is |V| minus v[A] plus 1. With In-order (0, 1, 0), |V| minus v[B] plus 1. With Post-order (0, 0, 1), |V| minus v[C] plus 1. "
        "With Depth weights (1, 0, -1), Depth is |v[A]|. And with weights (0, 0, 1), Subtree Size is v[A] minus v[C] plus 1, and leaves satisfy v[A] = v[B] = v[C]! "
        "Tree Contraction then reduces the tree to 3 nodes in O(log n) rounds by RAKE-ing odd-indexed left leaves, then odd-indexed right leaves, and compressing to even indices to avoid adjacent-parent conflicts."
    ),
    "05_04": (
        "Chapter 11 covers parallel sorting. A Bitonic sequence increases then decreases; a Bitonic Split splits it into lower and upper bitonic halves in parallel, giving a sorting network of Theta(log squared n) comparator columns mapped onto Hypercubes or Row-Major Shuffled Meshes. "
        "CRCW Parallel Quicksort builds a binary tree of pivots via Arbitrary concurrent writes and reads sorted output via inorder traversal. "
        "Sample Sort sorts local n/p chunks, picks p-1 samples per processor, sorts all p(p-1) samples to pick p-1 global splitters, buckets local data, exchanges all-to-all, and merges."
    ),
    "05_05": (
        "Chapter 12 covers parallel graph algorithms. Verify Eulerian graphs by checking all vertex degrees are even, and check a k-clique in O(1) time on PRAM ERCW with k squared processors. "
        "Floyd-Warshall runs the outer k loop sequentially while parallelizing all (u, v) distance updates. DFS has no direct parallel equivalent, whereas level-by-level Parallel BFS resolves duplicate vertex discovery with Arbitrary Concurrent Write. "
        "Finally, compare Connected Components algorithms: HCS uses an adjacency matrix and compresses to star trees in O(log n) per round at O(n squared) cost. "
        "Shiloach-Vishkin uses an adjacency list and reduces each round to O(1) using Grafting and single-step Pointer Jumping, achieving O(m + n) cost. "
        "Remember the critical SV rule: general unconditioning grafting is only allowed from iteration 2 onward so star trees in iteration 1 cannot form cycles!"
    ),

    # ================= MODULE 6: EXAM STRATEGY =================
    "06_01": (
        "You now have every architecture law, API signature, benchmark pitfall, and algorithm complexity. "
        "On exam day, pace your 65 minutes: spend 40 minutes on the 40 to 60 MCQs, 20 minutes on the short essays, and 5 minutes checking calculator unit conversions and code traps. "
        "Practice right away using practice_quiz.html and the 50-question timed mock exam. Good luck!"
    ),
}

# ================= NEW DEEP-DIVE SEGMENTS (v2) =================
NEW_SEGMENTS = {
    "01_09": (
        "Chapter 7 lists four decomposition techniques. Recursive decomposition uses divide and conquer, like quicksort or finding a minimum. "
        "Data decomposition partitions input, output, or intermediate data, then assigns work with the owner-computes rule. It is the most widely used. "
        "Exploratory decomposition searches a solution space, like the fifteen puzzle. Speculative decomposition guesses the outcome of a branch and may waste or undo work. "
        "After decomposing, we map tasks to processes. Static mapping uses block, cyclic, block-cyclic, or random block distributions, and suits tasks with known, uniform cost. "
        "Dynamic mapping moves work during execution, either centrally with a master and workers, or distributed with push or pull work stealing."
    ),
    "01_10": (
        "Why does efficiency drop? Overhead comes from three sources: communication, idling caused by load imbalance or synchronization, and excess computation. "
        "Take the classic example of adding n numbers on p processors. Each processor adds n over p numbers, then a tree reduction takes two log p steps. "
        "So T p equals n over p plus two log p. With n equal to sixty four and p equal to eight, T p is eight plus six, which is fourteen. Speedup is sixty four over fourteen, about four point six, and efficiency is about fifty seven percent. "
        "Keep p at eight but grow n to five hundred twelve: T p is seventy, and efficiency rises to ninety one percent. "
        "Total overhead is two p log p, so n must grow like p log p to keep efficiency constant. That growth rate is the isoefficiency function, and a lower rate means a more scalable system."
    ),
    "05_06": (
        "Let us trace the pointer jumping prefix sum from Chapter 10 on eight numbers: three, one, four, one, five, nine, two, six. "
        "At step k, every element i adds the value two to the power k minus one positions to its left. "
        "Step one, distance one, gives three, four, five, five, six, fourteen, eleven, eight. "
        "Step two, distance two, gives three, four, eight, nine, eleven, nineteen, seventeen, twenty two. "
        "Step three, distance four, gives the final prefix sums: three, four, eight, nine, fourteen, twenty three, twenty five, thirty one. "
        "That is log two of n steps, which is three steps for eight elements, and each step uses exclusive reads and writes, so it runs on EREW PRAM. "
        "The same jumping trick finds the root of every tree in a forest in O of log h time, where h is the height of the tallest tree."
    ),
    "05_07": (
        "Now the Euler tour technique on the binary tree from the slides: node one has children two and three, node two has children four and five, and node three has child six. "
        "Split each node into A, B and C copies and link them into one list: one A, two A, four A, four B, four C, two B, five A, and so on, ending at one C. "
        "For preorder, give A a weight of one and B and C a weight of zero, then compute the suffix sum along the list. "
        "Node one gets six, node two gets five, node four gets four. The position is the number of nodes minus v A plus one, so the order is one, two, four, five, three, six. "
        "Change the weights and the same list solves other problems. B equals one gives inorder. C equals one gives postorder. A equals one and C equals minus one gives depth. "
        "With C equals one, the subtree size is v A minus v C plus one. For node two, that is six minus four plus one, which equals three."
    ),
    "05_08": (
        "Let us sort eight numbers with a bitonic network: three, seven, four, eight, six, two, one, five. "
        "Stage one sorts pairs in alternating directions, giving three, seven, eight, four, two, six, five, one. "
        "Stage two merges blocks of four, the first ascending and the second descending, giving three, four, seven, eight, six, five, two, one, a bitonic sequence. "
        "Stage three is a bitonic split at distance four. Element i is compared with element i plus four. The smaller values go to the low half, three, four, two, one, and the larger values go to the high half, six, five, seven, eight. "
        "Every low value is less than or equal to every high value, and both halves are still bitonic. Splits at distance two and one finish the sort. "
        "Counting comparator columns: one plus two plus three equals six. In general, for n equal to two to the k, the depth is k times k plus one over two, which is Theta of log squared n."
    ),
    "05_09": (
        "Chapter 9 ends with a full SPMD case study, the heat equation. Every grid point is updated from its up, down, left and right neighbours: "
        "d C equals D over d x squared, times u plus d plus l plus r minus four c. Then C increases by d t times d C at each time step. "
        "The MPI program has five steps. B one: the root reads the input. B two: split the m by n grid by rows, so each rank owns m c equals m over N P rows. "
        "B three: MPI Scatter distributes the rows. B four: each step, exchange boundary rows, receiving C u from rank minus one and C d from rank plus one, then compute locally. "
        "B five: MPI Gather collects the result at the root. The stencil creates the data dependency. Shared memory resolves it with synchronization; distributed memory needs both communication and synchronization."
    ),
}
SEGMENTS.update(NEW_SEGMENTS)

SEGMENTS["06_01"] = (
    "You now have the architecture laws, API traps, calculator formulas and algorithm complexities for all twelve chapters. "
    "On exam day, pace your time: about forty minutes for the multiple choice questions, twenty minutes for the short essays, and five minutes to check units and code traps. "
    "Next, open practice quiz dot html. Use study mode to learn every question with its answer, then switch to exam mode with the timer. Good luck!"
)

# Drill narration is generated from drill_data.py
try:
    from drill_data import drill_segments
    SEGMENTS.update(drill_segments())
except ImportError:
    pass
