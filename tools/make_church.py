#!/usr/bin/env python3
"""Synthetische Kirchen-Sounds für die Prophet-Peter-Serie (keine Downloads nötig).

  python3 tools/make_church.py videos/<slug>/assets/sfx
schreibt holy-sting.wav (Glockenschlag + Orgel-Akkord, Frame-0-Hook), bell-hit.wav (kurze Glocke), coin.wav (Münze im Klingelbeutel).
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100


def bell(f0, dur, amp=1.0):
    t = np.arange(int(SR * dur)) / SR
    # klassische Glocken-Teiltöne (Hum, Prime, Terz, Quinte, Oktave …) mit eigener Abklingzeit
    parts = [(0.5, 1.0, 2.6), (1.0, 0.8, 1.8), (1.19, 0.55, 1.4), (1.5, 0.35, 1.1), (2.0, 0.5, 0.9),
             (2.52, 0.25, 0.6), (3.0, 0.18, 0.45), (4.07, 0.12, 0.3)]
    y = sum(a * np.sin(2 * np.pi * f0 * r * t + r) * np.exp(-t / d) for r, a, d in parts)
    y *= 1 - np.exp(-t / 0.002)
    return amp * y / np.abs(y).max()


def organ(freqs, dur, attack=0.35):
    t = np.arange(int(SR * dur)) / SR
    y = np.zeros_like(t)
    for f in freqs:
        for h, a in [(1, 1), (2, 0.5), (3, 0.25), (4, 0.18), (6, 0.08)]:
            y += a * np.sin(2 * np.pi * f * h * t) * (1 + 0.004 * np.sin(2 * np.pi * 5.2 * t))
    env = np.minimum(1, t / attack) * np.exp(-np.maximum(0, t - 0.9) / 0.55)
    return y * env / np.abs(y).max()


def coin():
    t = np.arange(int(SR * 0.7)) / SR
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in [(2637, 1, .25), (3951, .6, .18), (5274, .4, .12), (6645, .25, .08)])
    second = np.zeros_like(y); k = int(SR * 0.09); second[k:] = 0.55 * y[: len(y) - k]
    return (y + second) / np.abs(y + second).max()


def fade_out(y, sec=0.08):
    n = int(SR * sec); y[-n:] *= np.linspace(1, 0, n); return y


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    dur = 2.4
    b = bell(196, dur)                                   # tiefe Glocke G3
    o = organ([146.83, 220.0, 293.66, 349.23], dur) * 0.55  # d-Moll, Orgel
    y = b * 0.85 + o
    y = fade_out(y / np.abs(y).max() * 0.9)
    sf.write(out / "holy-sting.wav", np.stack([y, y], 1), SR)
    h = fade_out(bell(392, 1.3) * 0.85)
    sf.write(out / "bell-hit.wav", np.stack([h, h], 1), SR)
    c = fade_out(coin() * 0.8)
    sf.write(out / "coin.wav", np.stack([c, c], 1), SR)
    print("ok:", *(p.name for p in sorted(out.glob("*.wav"))))


if __name__ == "__main__":
    main()
