#!/usr/bin/env python3
"""Prüft die fertige Sprachspur: jede Zeile einzeln von Gemini abschreiben lassen und mit dem Soll-Text vergleichen.
  python3 tools/check_cuts.py videos/<slug>
Meldet Zeilen, deren Anfang/Ende nicht stimmt (Wort in der falschen Zeile) → in script.json "cut_shift": {"L17": -1} korrigieren."""
import base64, io, json, os, re, sys, time, urllib.request
from pathlib import Path
import numpy as np, soundfile as sf
proj = Path(sys.argv[1]); key = os.environ["GEMINI_API_KEY"]
t = json.load(open(proj / "assets/voice/timings.json"))
a, sr = sf.read(proj / "assets/voice/narration.wav", dtype="float32"); a = a if a.ndim == 1 else a.mean(1)
norm = lambda w: re.sub(r"[^a-zäöüß0-9]", "", w.lower())
for l in t["lines"]:
    seg = a[max(0, int((l["start"] - 0.05) * sr)): int((l["end"] + 0.05) * sr)]
    buf = io.BytesIO(); sf.write(buf, seg, sr, format="WAV", subtype="PCM_16")
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(buf.getvalue()).decode()}},
                                    {"text": "Schreibe wörtlich ab, was gesprochen wird (deutsch), auch einzelne kurze Wörter am Anfang und Ende. Nur der Text."}]}],
            "generationConfig": {"temperature": 0}}
    for w in (0, 20, 60):
        time.sleep(w)
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={key}",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=200).read())
            got = r["candidates"][0]["content"]["parts"][-1]["text"].strip(); break
        except Exception as e:  # noqa: BLE001
            got = f"(Fehler {e})"
    exp = [norm(w["spoken"] if "spoken" in w else w["display"]) for w in l["words"]]
    g = [norm(x) for x in got.split() if norm(x)]
    ok = bool(g) and g[0] == exp[0] and g[-1] == exp[-1]
    print(f"{'OK ' if ok else '!! '} {l['id']:4s} {got}")
