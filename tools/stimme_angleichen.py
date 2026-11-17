#!/usr/bin/env python3
"""Gemini-TTS: einzelne Zeilen, die „rauchig“/heller klingen als der Rest, neu würfeln und die passendste Variante
in den Cache legen (danach tts_de.py ohne --redo laufen lassen).
  python3 tools/stimme_angleichen.py <projekt> --model gemini-3.8-flash-tts --voice Puck --ids L1,L8 [--n 3] [--check]
Maß: spektraler Schwerpunkt der stimmhaften Abschnitte (Hz). --check zeigt nur die Werte aller Zeilen."""
import argparse, hashlib, json, os, sys
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, str(Path(__file__).parent)); import tts_de as T

def cent(pcm, sr):
    if pcm.ndim > 1: pcm = pcm.mean(axis=1)
    N, cs = 1024, []
    for i in range(0, len(pcm) - N, N // 2):
        fr = pcm[i:i + N] * np.hanning(N)
        if np.abs(fr).mean() < 0.02: continue
        sp = np.abs(np.fft.rfft(fr)); fq = np.fft.rfftfreq(N, 1 / sr)
        if sp[(fq > 80) & (fq < 400)].sum() < sp.sum() * 0.15: continue
        cs.append((sp * fq).sum() / sp.sum())
    return float(np.median(cs)) if cs else 0.0

ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--model", required=True); ap.add_argument("--voice", default="Puck")
ap.add_argument("--ids", default=""); ap.add_argument("--n", type=int, default=3); ap.add_argument("--check", action="store_true")
a = ap.parse_args(); P = Path(a.project); C = P / "assets/voice/gemini_cache"
d = json.load(open(P / "script.json")); L = []
for s in d["scenes"]:
    for l in s["lines"]:
        sp = " ".join(w["spoken"] for w in T.parse_tokens(l["text"]))
        h = hashlib.sha1(json.dumps([sp, l.get("style"), a.voice, a.model]).encode()).hexdigest()[:16]
        L.append((l["id"], sp, l.get("style"), C / f"{h}.wav"))
val = {i: cent(*sf.read(p, dtype="float32")) for i, _, _, p in L if p.exists()}
ref = float(np.median(list(val.values())))
print("Bezug (Median):", round(ref), "Hz"); [print(f"  {i}: {round(v)}") for i, v in val.items()]
if a.check: sys.exit()
key = os.environ["GEMINI_API_KEY"]
for i, sp, st, p in L:
    if i not in a.ids.split(","): continue
    best = (abs(val.get(i, 9e9) - ref), None)
    for k in range(a.n):
        pcm, sr = T.gemini_line(sp, st, a.voice, a.model, key, len(sp.split()))
        c = cent(pcm, sr); print(f"  {i} Variante {k}: {round(c)} Hz", flush=True)
        if abs(c - ref) < best[0]: best = (abs(c - ref), (pcm, sr, c))
    if best[1]:
        sf.write(p, best[1][0], best[1][1]); print(f"→ {i}: {round(best[1][2])} Hz übernommen")
    else: print(f"→ {i}: bisherige Aufnahme bleibt")
