import hashlib, json, re, subprocess, sys, wave
from pathlib import Path
import numpy as np
import soundfile as sf
from vieneu import Vieneu
from narration_data import SEGMENTS

VOICE = "Mai Anh"
TEMPO = 1.0  # natural speed
OUT_DIR = Path(__file__).resolve().parent / "tts_wav"
OUT_DIR.mkdir(parents=True, exist_ok=True)
meta_path, hash_path = OUT_DIR / "durations.json", OUT_DIR / "hashes.json"
durations = json.loads(meta_path.read_text()) if meta_path.exists() else {}
hashes = json.loads(hash_path.read_text()) if hash_path.exists() else {}

# Pronunciation helper: make acronyms / identifiers easier for the Vietnamese TTS.
PRON = [
    (r"std::jthread", "std jay thread"), (r"std::thread", "std thread"), (r"std::", "std "),
    (r"MPI_([A-Za-z_]+)", lambda m: "em pi ai " + m.group(1).replace("_", " ")),
    (r"\bMPI\b", "em pi ai"), (r"\bCUDA\b", "cu đa"), (r"\bGPU\b", "gi pi diu"), (r"\bCPU\b", "xi pi diu"),
    (r"\bPRAM\b", "pi ram"), (r"\bEREW\b", "e rew"), (r"\bCREW\b", "crew"), (r"\bCRCW\b", "xi ar xi đáp liu"),
    (r"\bSIMD\b", "sim đi"), (r"\bMIMD\b", "mim đi"), (r"\bSISD\b", "sít đi"), (r"\bMISD\b", "mít đi"),
    (r"\bSAXPY\b", "sắc pi"), (r"\bPCIe\b", "pi xi ai ê"), (r"\bSPMD\b", "ét pi em đi"),
    (r"\bOpenMP\b", "Open em pi"), (r"\bNUMA\b", "niu ma"), (r"\bUMA\b", "diu ma"), (r"\bSMP\b", "ét em pi"),
    (r"\bDAG\b", "đác"), (r"\bBFS\b", "bi ép ét"), (r"\bDFS\b", "đi ép ét"),
    (r"_", " "),
]
def prep(t):
    for pat, rep in PRON:
        t = re.sub(pat, rep, t)
    return t

tts = Vieneu()
voice = tts.get_preset_voice(VOICE)
SR = int(tts.sample_rate)  # VieNeu v3 outputs 48 kHz
made = 0
only = set(sys.argv[1:])
for key, text in SEGMENTS.items():
    if only and key not in only:
        continue
    spoken = prep(text)
    h = hashlib.sha1((VOICE + str(TEMPO) + "sr48k" + spoken).encode()).hexdigest()
    wav_path = OUT_DIR / f"{key}.wav"
    if hashes.get(key) == h and wav_path.exists() and key in durations:
        continue
    audio = np.asarray(tts.infer(text=spoken, voice=voice), dtype=np.float32)
    tmp = OUT_DIR / f"{key}.raw.wav"
    sf.write(str(tmp), audio, SR)
    subprocess.run(["ffmpeg", "-y", "-i", str(tmp), "-filter:a", f"atempo={TEMPO}", "-ar", "44100", "-ac", "1", str(wav_path)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    tmp.unlink(missing_ok=True)
    with wave.open(str(wav_path), "rb") as w:
        durations[key] = round(w.getnframes() / float(w.getframerate()), 3)
    hashes[key] = h
    made += 1
    print(key, durations[key], flush=True)
    meta_path.write_text(json.dumps(durations, indent=2)); hash_path.write_text(json.dumps(hashes, indent=2))

for k in list(durations):
    if k not in SEGMENTS:
        durations.pop(k); hashes.pop(k, None)
meta_path.write_text(json.dumps(durations, indent=2)); hash_path.write_text(json.dumps(hashes, indent=2))
tot = sum(durations.values())
print(f"Generated {made} clips; {len(durations)} total, audio = {tot:.1f}s ({tot/60:.1f} min)")
