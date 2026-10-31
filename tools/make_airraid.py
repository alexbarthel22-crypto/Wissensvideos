#!/usr/bin/env python3
"""Realistische Luftschutz-/Zivilschutzsirene (mechanisch, wie in Katastrophenfilmen): langsames Hochlaufen
des Rotors, auf- und abschwellendes Heulen, Zweiklang (kleine Terz), Luftrauschen, Echo zwischen Häusern.
Eigene Synthese, kein Filmton.   python3 tools/make_airraid.py <ausgabe.wav> [--dur 7] [--duck 0.9]"""
import argparse
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100


def tone(f, harm=18):
    ph = 2 * np.pi * np.cumsum(f) / SR
    return sum(np.sin(n * ph) / n ** 1.05 for n in range(1, harm + 1))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--dur", type=float, default=7.0)
    ap.add_argument("--duck", type=float, default=0.0, help="ab hier leiser (Stimme setzt ein); 0 = nie")
    a = ap.parse_args()
    t = np.arange(int(SR * a.dur)) / SR
    spin = np.clip(t / 2.2, 0, 1) ** 0.6                       # Rotor läuft hoch
    wail = 1 + 0.07 * np.sin(2 * np.pi * 0.22 * t - 1.2)        # langsames Auf-und-Ab
    f1 = (150 + 330 * spin) * wail
    x = tone(f1) + 0.8 * tone(f1 * 1.19)                         # kleine Terz
    x += 0.25 * tone(f1 * 0.5, 6)
    noise = sosfilt(butter(2, [300, 2500], btype="band", fs=SR, output="sos"), np.random.default_rng(1).standard_normal(len(t)))
    x += 0.6 * noise * (0.5 + 0.5 * spin) * (0.6 + 0.4 * np.sin(2 * np.pi * f1 / 8 * t))
    env = np.minimum(t / 0.4, 1) * np.minimum((a.dur - t) / 1.5, 1).clip(0, 1)
    x = np.tanh(x / np.abs(x).max() * 2.2) * env
    x = sosfilt(butter(2, [180, 6000], btype="band", fs=SR, output="sos"), x)
    L = x.copy(); R = x.copy()
    for d, g in [(0.21, 0.35), (0.47, 0.22), (0.83, 0.12)]:     # Echo von Häuserwänden
        n = int(d * SR); L[n:] += g * x[:-n]; R[n + 900:] += g * x[:-(n + 900)]
    if a.duck:
        k = np.clip((t - a.duck) / 0.5, 0, 1); L *= 1 - 0.55 * k; R *= 1 - 0.55 * k
    y = np.stack([L, R], 1); y = y / np.abs(y).max() * 0.92
    sf.write(a.out, y, SR); print(f"{a.out}: {a.dur:.1f} s")


if __name__ == "__main__":
    main()
