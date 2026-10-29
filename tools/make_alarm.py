#!/usr/bin/env python3
"""Erzeugt einen Notfall-Alarm (wie ein Warn-Alarm auf dem Handy) als Aufmerksamkeits-Sound für den Videoanfang.

Zweiklang 853 + 960 Hz, schnelle Dreier-Pulse, leicht übersteuert, kurzer Hall. Steht die ersten
0,85 s allein und läuft dann leiser unter der Stimme weiter.

  python3 tools/make_alarm.py <ausgabe.wav> [--dur 4.0]
"""
import argparse

import numpy as np
import soundfile as sf

SR = 44100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--dur", type=float, default=4.0)
    ap.add_argument("--duck", type=float, default=0.85, help="ab hier (Stimme setzt ein) leiser")
    args = ap.parse_args()

    t = np.arange(int(args.dur * SR)) / SR
    tone = np.sin(2 * np.pi * 853 * t) + np.sin(2 * np.pi * 960 * t)
    tone = np.tanh(2.2 * tone)  # rau wie ein Handy-Lautsprecher
    # Muster: drei kurze Pulse (0,14 s an / 0,06 s aus), dann 0,2 s Pause
    ph = t % 0.8
    gate = np.zeros_like(t)
    for k in range(3):
        on = (ph >= k * 0.2) & (ph < k * 0.2 + 0.14)
        gate[on] = 1.0
    # weiche Flanken gegen Klicks
    kern = np.ones(int(0.004 * SR)) / int(0.004 * SR)
    gate = np.convolve(gate, kern, mode="same")
    dry = tone * gate
    rng = np.random.default_rng(853)
    ir_t = np.arange(int(0.5 * SR)) / SR
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.12)
    ir[0] = 8.0
    wet = np.convolve(dry, ir)[: len(dry)]
    out = 0.7 * dry / np.max(np.abs(dry)) + 0.3 * wet / np.max(np.abs(wet))
    duck = 1 - 0.8 * np.clip((t - args.duck) / 0.25, 0, 1)
    fade = np.minimum(1, (args.dur - t) / 0.8)
    out *= duck * fade
    out = out / np.max(np.abs(out[: int(args.duck * SR)])) * 0.85
    sf.write(args.out, out.astype("float32"), SR)
    print(f"{args.out}: {args.dur:.1f} s")


if __name__ == "__main__":
    main()
