"""On-screen exam drills (3 per module). Generated from the practice-quiz question bank."""

DRILLS = {
  "M1": [
    {
      "q": "Amdahl: 90% parallel code. Max speedup with unlimited processors?",
      "opts": [
        "9x",
        "10x",
        "90x",
        "Unlimited"
      ],
      "ans": 1,
      "say_q": "If ninety percent of a program can be parallelized, what is the maximum speedup with unlimited processors?",
      "say_a": "Ten times. The serial ten percent never shrinks, so speedup is capped at one over zero point one, which is ten."
    },
    {
      "q": "Which PRAM model is the most restrictive, so its algorithms run on all others?",
      "opts": [
        "CRCW",
        "CREW",
        "EREW",
        "ERCW"
      ],
      "ans": 2,
      "say_q": "Which PRAM model is the most restrictive, so that its algorithms also run correctly on all the other models?",
      "say_a": "EREW, exclusive read exclusive write. An EREW algorithm never relies on concurrent access, so it works on CREW and CRCW too, but not the other way around."
    },
    {
      "q": "Isoefficiency: system X needs W = Θ(p log p), system Y needs W = Θ(p²). Which is more scalable?",
      "opts": [
        "X",
        "Y",
        "Equally scalable",
        "Cannot tell"
      ],
      "ans": 0,
      "say_q": "System X has isoefficiency of order p log p, and system Y has order p squared. Which one is more scalable?",
      "say_a": "System X. Isoefficiency is how fast the problem size must grow to keep efficiency constant. Slower growth, p log p instead of p squared, means a more scalable system."
    }
  ],
  "M2": [
    {
      "q": "OpenMP: which clause makes each thread sum privately, then combine once?",
      "opts": [
        "critical",
        "reduction(+:sum)",
        "atomic",
        "firstprivate(sum)"
      ],
      "ans": 1,
      "say_q": "In OpenMP, which clause gives each thread its own private sum and combines them once at the end?",
      "say_a": "Reduction plus colon sum. Each thread starts at zero and the partial sums are combined once, so it is far faster than critical or atomic, which synchronize every iteration."
    },
    {
      "q": "Java: calling wait() outside a synchronized block causes what?",
      "opts": [
        "A deadlock",
        "Nothing happens",
        "IllegalMonitorStateException",
        "The thread is terminated"
      ],
      "ans": 2,
      "say_q": "In Java, what happens if you call wait outside a synchronized block on that object?",
      "say_a": "An IllegalMonitorStateException is thrown. wait, notify and notifyAll must be called while holding the object's lock, because wait releases that lock."
    },
    {
      "q": "1000 iterations, 4 threads, schedule(static): thread 2 gets which iterations?",
      "opts": [
        "500 to 749",
        "250 to 499",
        "2, 6, 10, ...",
        "750 to 999"
      ],
      "ans": 0,
      "say_q": "A one-thousand-iteration loop runs with schedule static on four threads. Which iterations does thread two get?",
      "say_a": "Iterations 500 to 749. Default static gives each thread one contiguous block of about N over p, which is 250 iterations each."
    }
  ],
  "M3": [
    {
      "q": "Both ranks MPI_Send 1005 ints, then MPI_Recv (eager limit 4096 B). Result?",
      "opts": [
        "Finishes fine",
        "Deadlock (rendezvous)",
        "Error: buffer too small",
        "Messages arrive out of order"
      ],
      "ans": 1,
      "say_q": "Two ranks both call MPI Send with one thousand and five integers before receiving, with a 4096 byte eager limit. What happens?",
      "say_a": "Deadlock. 4020 bytes plus header exceeds the eager limit, so rendezvous makes each Send wait for a Recv that never starts. Fix it with MPI Sendrecv or non-blocking calls."
    },
    {
      "q": "4 ranks hold v = 1,2,3,4. MPI_Scan with MPI_SUM: value on rank 3?",
      "opts": [
        "4",
        "6",
        "10",
        "1"
      ],
      "ans": 2,
      "say_q": "Four ranks hold one, two, three and four. After an inclusive MPI Scan with sum, what does rank three hold?",
      "say_a": "Ten. Scan is an inclusive prefix reduction, so rank three gets one plus two plus three plus four."
    },
    {
      "q": "Which send mode drops the message silently if the receiver isn't ready?",
      "opts": [
        "Synchronous",
        "Buffered",
        "Standard",
        "Ready"
      ],
      "ans": 3,
      "say_q": "According to the slides, which MPI send mode drops the message silently if the receiver is not ready?",
      "say_a": "Ready send. It completes immediately and only works if the matching receive is already posted; buffered send instead keeps the data in a user buffer."
    }
  ],
  "M4": [
    {
      "q": "A __global__ CUDA kernel must have which return type?",
      "opts": [
        "int",
        "void",
        "float",
        "Any type"
      ],
      "ans": 1,
      "say_q": "What return type must a global CUDA kernel have?",
      "say_a": "Void. A kernel is launched by the CPU and runs on the GPU, so it cannot return a value. It writes results into device memory, which the host then copies back with cudaMemcpy."
    },
    {
      "q": "Two threads in DIFFERENT blocks of one grid need to sync. What is True?",
      "opts": [
        "Use __syncthreads()",
        "Use shared memory",
        "They cannot sync reliably",
        "Spin on a global lock"
      ],
      "ans": 2,
      "say_q": "Two threads in different blocks of the same grid need to synchronize. What is True?",
      "say_a": "They cannot synchronize reliably. Blocks may run in any order, so both are not guaranteed to be alive together. Use a new kernel launch as a global barrier."
    },
    {
      "q": "SAXPY with 256 threads/block, n = 1000: how many blocks are launched?",
      "opts": [
        "3",
        "5",
        "1000",
        "4"
      ],
      "ans": 3,
      "say_q": "SAXPY uses 256 threads per block and n equals one thousand. How many blocks are launched?",
      "say_a": "Four. n plus 255, divided by 256, is 1255 over 256, which truncates to 4. That gives 1024 threads, and the if i less than n check idles the last 24."
    }
  ],
  "M5": [
    {
      "q": "Find-Max with accelerated cascading: what are its (work, time)?",
      "opts": [
        "O(n), O(log log n)",
        "O(n^2), O(1)",
        "O(n log log n), O(log log n)",
        "O(n), O(log n)"
      ],
      "ans": 0,
      "say_q": "Using accelerated cascading, what work and time does parallel Find-Max achieve?",
      "say_a": "Order n work and order log log n time. A balanced tree first cuts n down to n over log log n candidates at linear cost, then the DLDT tree finishes in log log n steps."
    },
    {
      "q": "Bitonic sort network for n = 16: how many comparator columns?",
      "opts": [
        "4",
        "16",
        "10",
        "8"
      ],
      "ans": 2,
      "say_q": "How many columns of comparators does a bitonic sorting network need for sixteen elements?",
      "say_a": "Ten. With log n equal to four, the depth is four times five over two, which is ten. That is order log squared n."
    },
    {
      "q": "Sample sort on p = 4 processors: how many samples are sorted to pick the splitters?",
      "opts": [
        "12",
        "16",
        "3",
        "4"
      ],
      "ans": 0,
      "say_q": "In sample sort on four processors, how many samples are gathered and sorted to choose the global splitters?",
      "say_a": "Twelve. Each processor picks p minus one, which is three, equally spaced samples, so p times p minus one is twelve. Then p minus one, which is three, global splitters are chosen."
    }
  ]
}


def drill_segments():
    segs = {}
    for mod, items in DRILLS.items():
        for i, it in enumerate(items, 1):
            segs[f"d{mod}_{i}_q"] = it["say_q"] + " Read the four options, and pause the video if you need more time."
            segs[f"d{mod}_{i}_a"] = f"The answer is {'ABCD'[it['ans']]}. " + it["say_a"]
    return segs
