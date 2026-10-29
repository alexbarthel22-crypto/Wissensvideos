#!/usr/bin/env python3
"""Herzschlag (lub-dub) mit steigendem Tempo als WAV.
Aufruf: python3 tools/make_heartbeat.py <out.wav> <dauer_s> <bpm_start> <bpm_ende>"""
import sys
import numpy as np
import soundfile as sf

SR = 44100


def thump(f0, dur, amp):
    t = np.arange(int(SR * dur)) / SR
    f = f0 * (1 + 0.6 * np.exp(-t * 30))  # kurzer Pitch-Drop wie ein dumpfer Schlag
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14) * (1 - np.exp(-t * 400))


def main():
    out, dur, b0, b1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    y = np.zeros(int(SR * (dur + 0.5)))
    t = 0.05
    while t < dur - 0.3:
        bpm = b0 + (b1 - b0) * t / dur
        for off, a in ((0.0, 1.0), (0.24 * 60 / bpm, 0.7)):
            s = int(SR * (t + off)); x = thump(55, 0.35, a); y[s:s + len(x)] += x[: len(y) - s]
        t += 60 / bpm
    y = y[: int(SR * dur)]
    y[-int(SR * 0.3):] *= np.linspace(1, 0, int(SR * 0.3))
    y = 0.9 * y / np.abs(y).max()
    sf.write(out, np.stack([y, y], 1), SR)
    print(f"{out}: {dur:.1f} s, {b0:.0f}→{b1:.0f} bpm")


if __name__ == "__main__":
    main()
