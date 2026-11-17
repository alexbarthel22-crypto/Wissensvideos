"""Nach tts_de.py + fix_timings.py ausführen: Pausen nach „Drei“ und „zwei“ (Countdown) einfügen und alle Zeiten verschieben."""
import json, numpy as np, soundfile as sf
P = {"Drei": 0.45, "zwei": 0.45}
a, sr = sf.read("assets/voice/narration.wav", dtype="float32")
t = json.load(open("assets/voice/timings.json"))
ins = []
for w in t["lines"][0]["words"]:
    k = w["display"].strip(",.!?–- ")
    if k in P: ins.append((w["end"], P[k]))
for at, d in sorted(ins, reverse=True):
    i = int(at * sr); a = np.concatenate([a[:i], np.zeros(int(d * sr), dtype=a.dtype), a[i:]])
def sh(x):
    return x + sum(d for at, d in ins if x >= at - 0.03)
for l in t["lines"]:
    for w in l["words"]: w["start"], w["end"] = round(sh(w["start"]), 3), round(sh(w["end"]), 3)
    l["start"], l["end"] = round(sh(l["start"]), 3), round(sh(l["end"]), 3)
t["duration"] = round(t["duration"] + sum(d for _, d in ins), 3)
sf.write("assets/voice/narration.wav", a, sr)
json.dump(t, open("assets/voice/timings.json", "w"), ensure_ascii=False, indent=1)
print("Pausen eingefügt:", ins, "→", t["duration"])
