#!/usr/bin/env python3
"""Leise, „göttliche“ Hintergrundmusik (synthetisch, keine Lizenzfragen): Chor-/Orgelfläche mit sanften Akkordwechseln,
Hall und vereinzelten hohen Glöckchen. Wird unter der Stimme automatisch abgesenkt (Ducking).

  python3 tools/make_pad.py videos/<slug>/assets/sfx/divine-pad.wav 52.4 --duck videos/<slug>/assets/voice/narration.wav
Danach in script.json als sfx: {"name": "divine-pad", "at": "s01+0.0", "volume": 0.25}  (RMS der Datei ≈ -20 dBFS)
"""
import argparse
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100
# D-Dur: D – h-Moll – G – A (je 4 s), weich gesetzt
CHORDS = [[146.83, 220.0, 293.66, 369.99], [123.47, 246.94, 293.66, 369.99], [98.0, 196.0, 293.66, 392.0], [110.0, 220.0, 277.18, 329.63]]


def pad_voice(f, t, rng):
    y = np.zeros_like(t)
    for det in (-6, 0, 6):  # Cent, leicht schwebend wie ein Chor
        ff = f * 2 ** (det / 1200) * (1 + 0.003 * np.sin(2 * np.pi * rng.uniform(4.5, 5.5) * t + rng.uniform(0, 6)))
        ph = 2 * np.pi * np.cumsum(ff) / SR
        for h, a in [(1, 1.0), (2, 0.45), (3, 0.22), (4, 0.12), (5, 0.06)]:
            y += a * np.sin(h * ph)
    return y


def bell(f, dur=2.5):
    t = np.arange(int(SR * dur)) / SR
    y = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d) for r, a, d in [(1, 1, .9), (2.0, .4, .5), (3.0, .2, .3), (4.2, .1, .2)])
    return y * (1 - np.exp(-t / 0.004))


def reverb(y, sec=2.8, wet=0.45, seed=3):
    r = np.random.default_rng(seed)
    n = int(SR * sec)
    ir = r.standard_normal(n) * np.exp(-np.arange(n) / (SR * sec / 6))
    ir /= np.sqrt((ir ** 2).sum())
    # FFT-Faltung (schnell)
    L = len(y) + n - 1; N = 1 << (L - 1).bit_length()
    w = np.fft.irfft(np.fft.rfft(y, N) * np.fft.rfft(ir, N), N)[: len(y)]
    return (1 - wet) * y + wet * w * (np.sqrt((y ** 2).mean()) / (np.sqrt((w ** 2).mean()) + 1e-9))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("duration", type=float)
    ap.add_argument("--duck", help="Sprachspur: Musik darunter um ~6 dB absenken")
    ap.add_argument("--chord", type=float, default=4.0, help="Sekunden pro Akkord")
    a = ap.parse_args()
    rng = np.random.default_rng(12)
    n = int(SR * a.duration); t = np.arange(n) / SR
    y = np.zeros(n)
    k = 0
    while k * a.chord < a.duration:
        t0 = k * a.chord; t1 = min(a.duration, t0 + a.chord + 1.5)
        i0, i1 = int(t0 * SR), int(t1 * SR); tt = t[i0:i1] - t0
        env = np.minimum(1, tt / 1.2) * np.clip((t1 - t0 - tt) / 1.5, 0, 1)  # weiche Überblendung zwischen Akkorden
        seg = sum(pad_voice(f, tt, rng) for f in CHORDS[k % len(CHORDS)])
        y[i0:i1] += seg * env
        k += 1
    # tiefe Wärme (Grundton, sehr leise) + Glöckchen in D-Dur-Pentatonik, spärlich
    y += 0.25 * np.sin(2 * np.pi * 73.42 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t))
    y /= np.abs(y).max()
    notes = [1174.66, 1318.51, 1479.98, 1760.0, 1975.53]
    for tb in np.arange(1.5, a.duration - 2, 3.2):
        b = bell(notes[rng.integers(len(notes))]) * 0.18
        i = int((tb + rng.uniform(0, 1.2)) * SR); m = min(len(b), n - i); y[i:i + m] += b[:m]
    y = reverb(y)
    # sanfter Tiefpass gegen Zischeln (gleitender Mittelwert) – nichts soll mit der Stimme konkurrieren
    y = np.convolve(y, np.ones(6) / 6, mode="same")
    if a.duck:
        v, vsr = sf.read(a.duck, dtype="float32")
        if v.ndim > 1: v = v.mean(1)
        hop = int(vsr * 0.02)
        e = np.array([np.sqrt((v[i:i + hop] ** 2).mean()) for i in range(0, len(v), hop)])
        on = (e > 0.02).astype(float)
        g = np.ones_like(on); cur = 1.0
        for i, x in enumerate(on):  # schnell runter, langsam wieder hoch
            tgt = 0.5 if x else 1.0
            cur += (tgt - cur) * (0.35 if tgt < cur else 0.06); g[i] = cur
        gt = np.interp(t, np.arange(len(g)) * 0.02, g)
        y *= gt
    fi, fo = int(SR * 1.5), int(SR * 2.5)
    y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
    y *= 10 ** (-20 / 20) / np.sqrt((y ** 2).mean())  # RMS ≈ -20 dBFS
    y = np.clip(y, -0.99, 0.99)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sf.write(a.out, np.stack([y, y], 1).astype("float32"), SR)
    print(f"{a.out}: {a.duration:.1f} s")


if __name__ == "__main__":
    main()
