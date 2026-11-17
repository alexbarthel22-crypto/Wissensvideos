"""Nach tts_de.py + fix_timings.py ausführen. Misst „Drei“, „zwei“, „eins“ in der Aufnahme (Lautstärke)
und setzt sie auf einen festen Takt (0,0 / 0,8 / 1,6 s); der Rest der Zeile folgt ab 2,15 s. Alle Zeiten werden verschoben."""
import json, numpy as np, soundfile as sf
BEAT, REST_AT = 0.8, 2.15
a, sr = sf.read("assets/voice/narration.wav", dtype="float32")
t = json.load(open("assets/voice/timings.json")); L1 = t["lines"][0]
h = int(sr * .01); e = np.array([np.abs(a[i:i + h]).mean() for i in range(0, int(L1["end"] * sr), h)])
segs, s = [], None
for i, b in enumerate(e > 0.02):
    if b and s is None: s = i
    if not b and s is not None: segs.append([s, i]); s = None
if s is not None: segs.append([s, len(e)])
m = []
for sg in segs:
    if m and sg[0] - m[-1][1] <= 3: m[-1][1] = sg[1]
    else: m.append(sg)
w = [(x * .01, y * .01) for x, y in m]
# Zahlwörter ohne Pause dazwischen (z. B. „zwei-eins“): zu langen Abschnitt an der leisesten Stelle teilen
k = 0
while k < min(3, len(w)):
    x0, x1 = w[k]
    if x1 - x0 > .55 and k < 3:
        i0, i1 = int(x0 * 100 + (x1 - x0) * 30), int(x0 * 100 + (x1 - x0) * 75)
        sm = np.convolve(e, np.ones(3) / 3, mode="same")
        cut_i = i0 + int(np.argmin(sm[i0:i1]))
        w[k:k + 1] = [(x0, cut_i * .01), (cut_i * .01 + .01, x1)]
    else:
        k += 1
# Rest der Zeile beginnt beim ersten LAUTEN Abschnitt nach „eins“ (leise Atmer davor ignorieren)
pk = lambda x0, x1: e[int(x0 * 100):int(x1 * 100) + 1].max()
w = w[:3] + [x for x in w[3:] if pk(*x) > 0.1][:1] + [x for x in w[3:] if pk(*x) <= 0.1][:0]
assert len(w) >= 4, w
cut = [0.0, (w[0][1] + w[1][0]) / 2, (w[1][1] + w[2][0]) / 2, (w[2][1] + w[3][0]) / 2]   # Grenzen Drei|zwei|eins|Rest
clip = lambda p, q: a[int(p * sr):int(q * sr)]
out = np.zeros(int(REST_AT * sr), dtype=a.dtype)
for k in range(3):
    c = clip(cut[k], cut[k + 1]); o = int(k * BEAT * sr); out[o:o + len(c)] = c[:len(out) - o]
rest = a[int(cut[3] * sr):]; sh = REST_AT - cut[3]
a2 = np.concatenate([out, rest])
on = [w[k][0] - cut[k] + k * BEAT for k in range(3)]
hook_on, hook_end = w[3][0] + sh, L1["end"] + sh
ws = L1["words"]; n = len(ws) - 4            # Drei, zwei, eins, –, dann Hook-Wörter
syl = [max(1, sum(ch in "aeiouäöüy" for ch in x["display"].lower())) for x in ws[4:]]
tot = sum(syl); tcur = hook_on
for k in range(3): ws[k]["start"], ws[k]["end"] = round(on[k], 3), round(on[k] + (w[k][1] - w[k][0]), 3)
ws[3]["start"], ws[3]["end"] = round(on[2] + .3, 3), round(hook_on, 3)
for x, sy in zip(ws[4:], syl):
    d = (hook_end - hook_on) * sy / tot; x["start"], x["end"] = round(tcur, 3), round(tcur + d, 3); tcur += d
L1["start"], L1["end"] = 0.0, round(hook_end, 3)
for l in t["lines"][1:]:
    for x in l["words"]: x["start"], x["end"] = round(x["start"] + sh, 3), round(x["end"] + sh, 3)
    l["start"], l["end"] = round(l["start"] + sh, 3), round(l["end"] + sh, 3)
t["duration"] = round(len(a2) / sr, 3)
sf.write("assets/voice/narration.wav", a2, sr)
json.dump(t, open("assets/voice/timings.json", "w"), ensure_ascii=False, indent=1)
print("Wörter:", [(round(x, 2), round(y, 2)) for x, y in w[:4]], "→ Einsätze", [round(x, 2) for x in on], "Hook ab", round(hook_on, 2))
