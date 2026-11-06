#!/usr/bin/env python3
"""Eigene, lizenzfreie Hintergrundmusik. --style gospel (Standard) = „Sekten-Gospel“, --style epic = „Heiliger Trailer“ (112 BPM, Streicher, Blech, Chor, Pauken).
„Sekten-Gospel“: Kirchenorgel + Chorfläche + Bass + leichter Gospel-Groove (96 BPM),
spärliche Glöckchen, Hall. Unter der Stimme automatisch abgesenkt (Ducking).

  python3 tools/make_music.py videos/<slug>/assets/sfx/music-gospel.wav <Gesamtdauer> --duck videos/<slug>/assets/voice/narration.wav
In script.json als sfx: {"name": "music-gospel", "at": "s01+0.0", "volume": 0.3}  (RMS der Datei ≈ -20 dBFS)
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).parent))
from make_pad import SR, bell, pad_voice, reverb  # noqa: E402

BPM = 96
BEAT = 60 / BPM
# D-Dur, Gospel-Kadenz: D – G/D – Bm – A (je 1 Takt = 4 Schläge)
PROG = [[146.83, 220.0, 293.66, 369.99], [146.83, 196.0, 246.94, 293.66], [123.47, 185.0, 246.94, 293.66], [110.0, 164.81, 220.0, 277.18]]
BASS = [73.42, 98.0, 61.74, 55.0]


def organ(f, n, rng):
    t = np.arange(n) / SR
    y = np.zeros(n)
    for h, a in [(0.5, 0.35), (1, 1.0), (2, 0.6), (3, 0.3), (4, 0.25), (6, 0.12), (8, 0.08)]:  # Register 16', 8', 4', 2 2/3' …
        y += a * np.sin(2 * np.pi * f * h * t * (1 + 0.0007 * np.sin(2 * np.pi * 5.8 * t)))
    return y


def kick(n):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * (48 + 90 * np.exp(-t / 0.04)) * t) * np.exp(-t / 0.18)


def clap(n, rng):
    t = np.arange(n) / SR
    y = rng.standard_normal(n) * (np.exp(-t / 0.06) + 0.6 * np.exp(-np.abs(t - 0.012) / 0.004) + 0.5 * np.exp(-np.abs(t - 0.024) / 0.004))
    y = np.convolve(y, np.array([1, -0.85]), mode="same")  # Hochpass-artig
    return y * 0.5


def shaker(n, rng):
    t = np.arange(n) / SR
    y = rng.standard_normal(n) * np.exp(-t / 0.025)
    return np.convolve(y, np.array([1, -0.95]), mode="same") * 0.18


def place(buf, x, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(buf):
        return
    m = min(len(x), len(buf) - i)
    buf[i:i + m] += g * x[:m]


def saw(f, n, nh=12):
    t = np.arange(n) / SR
    return sum(((-1) ** (h + 1)) * np.sin(2 * np.pi * f * h * t) / h for h in range(1, nh + 1))


def epic(duration, rng):
    """„Heiliger Trailer“: 112 BPM, D – A – Hm – G, Streicher-Achtel, Blech-Akkorde, Chor, Pauken, Becken-Swell."""
    bpm = 112; beat = 60 / bpm; bar = 4 * beat
    prog = [[146.83, 220.0, 293.66, 369.99], [110.0, 164.81, 220.0, 277.18], [123.47, 185.0, 246.94, 293.66], [98.0, 146.83, 196.0, 246.94]]
    roots = [146.83, 110.0, 123.47, 98.0]
    n = int(SR * (duration + 3))
    strings, brass, choir, perc, cym = (np.zeros(n) for _ in range(5))
    k = 0
    while k * bar < duration + 2:
        t0 = k * bar; ch = prog[k % 4]
        for e8 in range(8):  # Streicher-Ostinato: Grundton / Quinte / Oktave im Wechsel
            f = [ch[0] * 2, ch[2] * 2, ch[3] * 2, ch[2] * 2][e8 % 4]
            m = int(SR * beat / 2 * 0.95); tt = np.arange(m) / SR
            place(strings, saw(f, m, 8) * np.minimum(1, tt / 0.01) * np.exp(-tt / 0.22), t0 + e8 * beat / 2)
        m = int(SR * bar * 1.05); tt = np.arange(m) / SR  # Blech: weicher Akkord-Swell
        b = sum(saw(f, m, 10) for f in ch[:3]) * np.minimum(1, tt / 0.35) * np.clip((bar * 1.05 - tt) / 0.3, 0, 1)
        place(brass, np.convolve(b, np.ones(10) / 10, mode="same"), t0)
        tt2 = np.arange(int(SR * (bar + 1.0))) / SR
        place(choir, sum(pad_voice(f * 2, tt2, rng) for f in ch[1:]) * np.minimum(1, tt2 / 0.5) * np.clip((bar + 1.0 - tt2) / 1.0, 0, 1), t0)
        for bb, g in ((0, 1.0), (2, 0.8), (3.5, 0.5)):  # Pauke (tief, gestimmt auf den Grundton)
            mm = int(SR * 0.7); tp = np.arange(mm) / SR
            place(perc, np.sin(2 * np.pi * roots[k % 4] / 2 * tp * (1 + 0.3 * np.exp(-tp / 0.03))) * np.exp(-tp / 0.35) * g, t0 + bb * beat)
        if k % 4 == 3:  # Becken-Swell in den nächsten Abschnitt
            mm = int(SR * bar); tc = np.arange(mm) / SR
            c = rng.standard_normal(mm); c = np.convolve(c, np.array([1, -0.97]), mode="same")
            place(cym, c * (tc / bar) ** 3 * 0.25, t0)
        k += 1
    nz = lambda x: x / (np.abs(x).max() + 1e-9)
    return 0.42 * nz(strings) + 0.4 * nz(brass) + 0.35 * nz(choir) + 0.6 * nz(perc) + 0.3 * nz(cym)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("duration", type=float)
    ap.add_argument("--style", choices=["gospel", "epic"], default="gospel")
    ap.add_argument("--duck"); ap.add_argument("--groove-from", type=float, default=2.5, help="Groove setzt ab dieser Sekunde ein")
    a = ap.parse_args()
    rng = np.random.default_rng(7)
    n = int(SR * (a.duration + 3)); bar = 4 * BEAT
    org, choir, bass, drums, bells = (np.zeros(n) for _ in range(5))
    k = 0
    while k * bar < a.duration + 2:
        t0 = k * bar; ch = PROG[k % 4]
        # Orgel: Akkord auf Schlag 1 + kurzer Gospel-Anschlag auf „und“ von 2 und 4
        seg = sum(organ(f, int(SR * bar * 1.02), rng) for f in ch)
        env = np.minimum(1, np.arange(len(seg)) / (SR * 0.03)) * np.clip((len(seg) - np.arange(len(seg))) / (SR * 0.25), 0, 1)
        place(org, seg * env * 0.8, t0)
        for off in (1.5, 3.5):
            st = sum(organ(f * 2, int(SR * BEAT * 0.4), rng) for f in ch[1:])
            e = np.exp(-np.arange(len(st)) / (SR * 0.12)); place(org, st * e * 0.35, t0 + off * BEAT)
        # Chorfläche (aah), weich überblendet
        tt = np.arange(int(SR * (bar + 1.0))) / SR
        cseg = sum(pad_voice(f * 2, tt, rng) for f in ch[1:]) * np.minimum(1, tt / 0.6) * np.clip((bar + 1.0 - tt) / 1.0, 0, 1)
        place(choir, cseg, t0)
        # Bass: Grundton auf 1 und 3, Durchgang auf 4-und
        for b, f in ((0, BASS[k % 4]), (2, BASS[k % 4]), (3.5, BASS[(k + 1) % 4] * 1.12)):
            m = int(SR * BEAT * (0.9 if b < 3 else 0.45)); tb = np.arange(m) / SR
            place(bass, (np.sin(2 * np.pi * f * tb) + 0.3 * np.sin(4 * np.pi * f * tb)) * np.exp(-tb / 0.5) * np.minimum(1, tb / 0.01), t0 + b * BEAT)
        # Groove ab groove_from: Kick 1 & 3 (+ „und“ von 2), Clap 2 & 4, Shaker Achtel
        if t0 >= a.groove_from - 0.01:
            for b in (0, 1.5, 2):
                place(drums, kick(int(SR * 0.35)), t0 + b * BEAT, 0.9 if b != 1.5 else 0.5)
            for b in (1, 3):
                place(drums, clap(int(SR * 0.2), rng), t0 + b * BEAT, 0.55)
            for e8 in range(8):
                place(drums, shaker(int(SR * 0.08), rng), t0 + e8 * BEAT / 2, 0.7 if e8 % 2 else 0.4)
        if k % 2 == 1:
            place(bells, bell([1174.66, 1479.98, 1760.0][k % 3], 2.0), t0 + 2 * BEAT, 0.12)
        k += 1
    norm = lambda x: x / (np.abs(x).max() + 1e-9)
    y = 0.55 * norm(org) + 0.35 * norm(choir) + 0.45 * norm(bass) + 0.5 * norm(drums) + norm(bells) * 0.25
    if a.style == "epic":
        y = epic(a.duration, rng)
    y = reverb(y, 2.2, 0.28)[:int(SR * a.duration)]
    y = np.convolve(y, np.ones(4) / 4, mode="same")  # dezent weicher
    t = np.arange(len(y)) / SR
    if a.duck:
        v, vsr = sf.read(a.duck, dtype="float32")
        v = v.mean(1) if v.ndim > 1 else v
        hop = int(vsr * 0.02)
        e = np.array([np.sqrt((v[i:i + hop] ** 2).mean()) for i in range(0, len(v), hop)])
        g = np.ones(len(e)); cur = 1.0
        for i, x in enumerate(e > 0.02):
            tgt = 0.5 if x else 1.0
            cur += (tgt - cur) * (0.35 if tgt < cur else 0.06); g[i] = cur
        y *= np.interp(t, np.arange(len(g)) * 0.02, g)
    fi, fo = int(SR * 0.4), int(SR * 2.0)
    y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
    y *= 10 ** (-20 / 20) / np.sqrt((y ** 2).mean())
    y = np.clip(y, -0.99, 0.99)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sf.write(a.out, np.stack([y, y], 1).astype("float32"), SR)
    print(f"{a.out}: {a.duration:.1f} s, {BPM} BPM")


if __name__ == "__main__":
    main()
