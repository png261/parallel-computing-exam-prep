# Parallel & High-Performance Computing: final-exam prep

Study material for a university course on parallel computing (Chapters 1–12 plus updated C++ threads, OpenMP, MPI and CUDA notes).
Exam format it targets: 40–60 multiple-choice questions + 1–2 short essays, 60–70 minutes, closed book, calculator only.

## Quiz (open in a browser, no server needed)
- `practice_quiz_vi.html`: Vietnamese, 461 multiple-choice questions + 17 essays, each with an answer and explanation.
- `practice_quiz.html`: English version of the same bank.
- Study mode shows the answer immediately; exam mode hides it until you press Grade; the mock exam draws 50 MCQs + 2 essays with a 65-minute timer.
- Math is rendered with [KaTeX](https://katex.org) (bundled in `katex/`; keep that folder next to the HTML files).

## Review video source (Manim)
- `manim_exam_video/`: English version (narration via macOS `say`).
- `manim_exam_video_vi/`: Vietnamese, diagram-first version, narrated with [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS) (voice "Mai Anh").
- Narration text is in `narr_vi_*.json` / `narration_data.py`.

Build (Vietnamese): `pip install manim vieneu soundfile numpy`, then in `manim_exam_video_vi/` run `python generate_audio.py` (writes `tts_wav/`), then `manim -qm s01_foundations.py Scene01Foundations` (and s02–s06) and concatenate the scenes with ffmpeg.

The lecture slides and rendered videos are not included in this repository.
