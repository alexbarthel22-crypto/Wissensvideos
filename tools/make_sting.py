#!/usr/bin/env python3
"""Aufmerksamkeits-Sound für Frame 0: Elektro-Zap + Gameboy-Arpeggio ("Item erhalten").

  python3 tools/make_sting.py <ausgabe.wav> [--duck 0.85]

Deterministisch (fester Seed). Nach --duck Sekunden wird alles leiser, damit die Stimme klar bleibt.
"""
import argparse

import numpy as np
import soundfile as sf

SR = 44100


def square(f, t, duty=0.5):
    return np.where((f * t) % 1 < duty, 1.0, -1.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--dur", type=float, default=2.6)
    ap.add_argument("--duck", type=float, default=0.85)
    args = ap.parse_args()
    n = int(args.dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(25)

    # 1) Elektrischer Zap: dichte Funken-Impulse, Bandpass-artig durch Differenz zweier Tiefpässe
    sparks = np.zeros(n)
    for _ in range(420):
        i = int(rng.uniform(0, 0.55) ** 1.6 * SR)
        sparks[i] += rng.uniform(-1, 1)
    buzz = np.sin(2 * np.pi * 60 * t) * 0.6 + np.sin(2 * np.pi * 120 * t) * 0.3
    zap = np.convolve(sparks, np.exp(-np.arange(200) / 25), mode="same") + buzz * (t < 0.55)
    zap *= np.exp(-t / 0.22)
    hp = zap - np.convolve(zap, np.ones(9) / 9, mode="same")  # Höhen = Knistern
    zap = 0.6 * hp / np.max(np.abs(hp)) + 0.4 * zap / np.max(np.abs(zap))

    # 2) Gameboy-Arpeggio (Pulswelle), startet mit dem Zap: C6 E6 G6 C7
    arp = np.zeros(n)
    notes = [1046.5, 1318.5, 1568.0, 2093.0]
    for k, f in enumerate(notes):
        a, b = 0.05 + k * 0.075, 0.05 + k * 0.075 + (0.3 if k == 3 else 0.07)
        m = (t >= a) & (t < b)
        env = np.exp(-(t - a) / (0.25 if k == 3 else 0.05))
        arp += square(f, t, 0.25) * m * env
    out = 0.55 * zap + 0.45 * arp / np.max(np.abs(arp))

    # kurzer Hall für Größe
    ir_t = np.arange(int(0.6 * SR)) / SR
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.15)
    ir[0] = 8.0
    wet = np.convolve(out, ir)[:n]
    out = 0.7 * out / np.max(np.abs(out)) + 0.3 * wet / np.max(np.abs(wet))

    duck = 1 - 0.8 * np.clip((t - args.duck) / 0.25, 0, 1)
    fade = np.minimum(1, (args.dur - t) / 0.4)
    out *= duck * fade
    out = out / np.max(np.abs(out)) * 0.89
    sf.write(args.out, out.astype("float32"), SR)
    print(f"{args.out}: {args.dur:.1f} s")


if __name__ == "__main__":
    main()
