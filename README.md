# Parallel & High-Performance Computing: final-exam prep

Study material for a university course on parallel computing (Chapters 1–12 plus updated C++ threads, OpenMP, MPI and CUDA notes).
Target exam: 40–60 multiple-choice questions + 1–2 short essays, 60–70 minutes, closed book, calculator only.

## Repository layout

| Folder | Contents |
|---|---|
| [`quiz/`](quiz) | Interactive question banks (open the HTML file in a browser, no server needed) |
| [`slides/`](slides) | Lecture slides, Chapters 1–12 (PDF) |
| [`notes/`](notes) | Updated Vietnamese notes: C++ threads + OpenMP (ch. 3), MPI (ch. 4), CUDA (ch. 5) |
| [`video/vi/`](video/vi) | Source of the Vietnamese review video (Manim scenes + narration, voice: VieNeu-TTS) |
| [`video/en/`](video/en) | Source of the English review video |

Rendered videos are on the [Releases page](../../releases/tag/v1.0.0) (too large for normal commits):
the Vietnamese video (51 min, chapter markers per module) and the English video (33 min).

## Quiz
- [`quiz/practice_quiz_vi.html`](quiz/practice_quiz_vi.html): Vietnamese, 461 multiple-choice questions + 17 essays, each with an answer and explanation.
- [`quiz/practice_quiz.html`](quiz/practice_quiz.html): English version of the same bank.
- Study mode shows the answer immediately; exam mode hides it until you press Grade; the mock exam draws 50 MCQs + 2 essays with a 65-minute timer.
- Math is rendered with [KaTeX](https://katex.org) (bundled in `quiz/katex/`; keep that folder next to the HTML files).

## Rebuilding the Vietnamese video
```bash
pip install manim vieneu soundfile numpy      # also needs ffmpeg and espeak-ng
cd video/vi
python generate_audio.py                      # VieNeu-TTS -> tts_wav/ (voice "Mai Anh")
manim -qm s01_foundations.py Scene01Foundations   # repeat for s02..s06, then join the scenes with ffmpeg
```
Narration text lives in `narr_vi_*.json`; voice: [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS).
