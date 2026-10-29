#!/usr/bin/env python3
"""Erzeugt eine "Purge"-Sirene (Luftschutzsirene) als Aufmerksamkeits-Sound für den Videoanfang.

Zwei Rotoren im Abstand einer kleinen Terz (der typische unheimliche Purge-Klang), Hochlaufen,
leichtes Schwanken, langes Ausklingen, Hall. Deterministisch (fester Seed).

  python3 tools/make_siren.py <ausgabe.wav> [--dur 4.5]
"""
import argparse

import numpy as np
import soundfile as sf

SR = 44100


def rotor(f_curve, harmonics=14):
    phase = 2 * np.pi * np.cumsum(f_curve) / SR
    out = np.zeros_like(f_curve)
    for n in range(1, harmonics + 1):
        out += np.sin(n * phase) / n ** 1.15
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--dur", type=float, default=4.5)
    ap.add_argument("--duck", type=float, default=0.85, help="ab hier (Stimme setzt ein) leiser")
    args = ap.parse_args()

    t = np.arange(int(args.dur * SR)) / SR
    # Hochlaufen in 0,9 s auf 470 Hz, leichtes Wobbeln, ab 2,4 s langsames Abfallen
    rise = 1 - np.exp(-t / 0.32)
    fall = np.clip((t - 2.4) / (args.dur - 2.4), 0, 1) ** 1.6
    base = 140 + 330 * rise - 200 * fall
    base *= 1 + 0.012 * np.sin(2 * np.pi * 0.9 * t)
    sig = rotor(base) + 0.8 * rotor(base * 1.19)  # kleine Terz
    # leichtes Rotor-Flattern
    sig *= 1 + 0.18 * np.sin(2 * np.pi * 11 * t)
    # Tiefpass (einfacher One-Pole) gegen Härte
    a = np.exp(-2 * np.pi * 2600 / SR)
    lp = np.zeros_like(sig)
    acc = 0.0
    for i, x in enumerate(sig):
        acc = (1 - a) * x + a * acc
        lp[i] = acc
    # Hüllkurve: schnell da (Frame 0 soll knallen), Ausklingen
    env = np.minimum(1, t / 0.05) * (1 - 0.85 * fall)
    dry = lp * env
    # Hall: exponentiell abklingendes Rauschen als Impulsantwort
    rng = np.random.default_rng(1911)
    ir_t = np.arange(int(1.6 * SR)) / SR
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.45)
    ir[0] = 6.0
    wet = np.convolve(dry, ir)[: len(dry)]
    out = 0.55 * dry / np.max(np.abs(dry)) + 0.45 * wet / np.max(np.abs(wet))
    fade = np.minimum(1, (args.dur - t) / 0.6)
    # unter die Stimme absenken (~ -16 dB), damit der erste Satz klar bleibt
    duck = 1 - 0.84 * np.clip((t - args.duck) / 0.3, 0, 1)
    out *= fade * duck
    out = out / np.max(np.abs(out[: int(args.duck * SR)])) * 0.89  # Spitze im lauten Teil ~ -1 dBFS
    sf.write(args.out, out.astype("float32"), SR)
    print(f"{args.out}: {args.dur:.1f} s")


if __name__ == "__main__":
    main()
