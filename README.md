# Parallel & High-Performance Computing: final-exam prep

**Live quiz (GitHub Pages): https://png261.github.io/parallel-computing-exam-prep/**

Scope: Chapter 1 + Chapter 2 slides and the three updated notes (chuong 3 = C++ threads + OpenMP, chuong 4 = MPI, chuong 5 = CUDA).
Target exam: 40–60 multiple-choice questions + 1–2 short essays, 60–70 minutes, closed book, calculator only.

## Repository layout

| Folder | Contents |
|---|---|
| [`quiz/`](quiz) | Interactive question banks (open the HTML file in a browser, no server needed) |
| [`slides/`](slides) | Lecture slides: Chapter 1 and Chapter 2 (PDF) |
| [`notes/`](notes) | Updated Vietnamese notes: `ch03_cpp_threads_openmp_vi`, `ch04_mpi_vi`, `ch05_cuda_vi` |
| [`video/vi/`](video/vi) | Source of the Vietnamese review video (Manim scenes + narration, voice: VieNeu-TTS) |
| [`video/en/`](video/en) | Source of the older English video (previous scope: Ch. 1–12, not updated) |

The rendered Vietnamese review video (59 min, mascot "Bé Core", everyday analogies, predict-then-reveal moments, 12 game-style drills, chapter markers per module) is on the [Releases page](../../releases/latest) (too large for normal commits).

## Quiz
- [`quiz/practice_quiz_vi.html`](quiz/practice_quiz_vi.html): Vietnamese, 395 multiple-choice questions + 16 essays, each with an answer and explanation.
- [`quiz/practice_quiz.html`](quiz/practice_quiz.html): English version of the same bank.
- Game layer: XP, levels, answer streaks, badges per module, toasts and confetti (progress is stored in your browser).
- Study mode shows the answer immediately; exam mode hides it until you press Grade; the mock exam draws 50 MCQs (12 Ch.1–2, 14 chuong 3, 12 chuong 4, 12 chuong 5) + 2 essays with a 65-minute timer.
- Math is rendered with [KaTeX](https://katex.org) (bundled in `quiz/katex/`; keep that folder next to the HTML files).

## Rebuilding the Vietnamese video
```bash
pip install manim vieneu soundfile numpy      # also needs ffmpeg and espeak-ng
cd video/vi
python generate_audio.py                      # VieNeu-TTS -> tts_wav/ (voice "Mai Anh")
manim -qm s01_foundations.py Scene01Foundations   # repeat for s02..s06, then join the scenes with ffmpeg
```
Narration text lives in `narr_vi_*.json`; voice: [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS).
