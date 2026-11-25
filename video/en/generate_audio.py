import hashlib
import json
import subprocess
import wave
from pathlib import Path
from narration_data import SEGMENTS

OUT_DIR = Path(__file__).resolve().parent / "tts_wav"
OUT_DIR.mkdir(parents=True, exist_ok=True)
meta_path = OUT_DIR / "durations.json"
hash_path = OUT_DIR / "hashes.json"
durations = json.loads(meta_path.read_text()) if meta_path.exists() else {}
hashes = json.loads(hash_path.read_text()) if hash_path.exists() else {}

made = 0
for key, text in SEGMENTS.items():
    h = hashlib.sha1(text.encode()).hexdigest()
    wav_path = OUT_DIR / f"{key}.wav"
    if hashes.get(key) == h and wav_path.exists() and key in durations:
        continue
    aiff_path = OUT_DIR / f"{key}.aiff"
    subprocess.run(["say", "-v", "Samantha", "-r", "182", "-o", str(aiff_path), text], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(aiff_path), "-ar", "44100", "-ac", "1", str(wav_path)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    aiff_path.unlink(missing_ok=True)
    with wave.open(str(wav_path), "rb") as w:
        durations[key] = round(w.getnframes() / float(w.getframerate()), 3)
    hashes[key] = h
    made += 1

for k in list(durations):
    if k not in SEGMENTS:
        durations.pop(k); hashes.pop(k, None)
meta_path.write_text(json.dumps(durations, indent=2))
hash_path.write_text(json.dumps(hashes, indent=2))
tot = sum(durations.values())
print(f"Regenerated {made} clips; {len(durations)} total, audio = {tot:.1f}s ({tot/60:.1f} min)")
