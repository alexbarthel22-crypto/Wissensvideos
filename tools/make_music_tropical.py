#!/usr/bin/env python3
"""Lizenzfreie Südsee-Musik, komplett im Code erzeugt (Ukulele-Strumming, Marimba-Melodie, Bass, Shaker).

  python3 tools/make_music_tropical.py <ausgabe.wav> <dauer_s> [--bpm 104] [--seed 3]
  python3 tools/make_music_tropical.py out.wav 54 --duck assets/voice/narration.wav --lufs -24

--duck: macht die Musik automatisch leiser, sobald gesprochen wird (Sidechain), danach Lautheit auf --lufs.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def hz(name):
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((NOTE[n] + 12 * (o + 1) - 69) / 12)


_cache = {}


def pluck(f, dur=1.6, bright=0.5):
    """Karplus-Strong-Saite (blockweise vektorisiert)."""
    key = (round(f, 2), dur, bright)
    if key in _cache:
        return _cache[key]
    n = int(SR * dur)
    p = max(2, int(round(SR / f)))
    rnd = np.random.default_rng(int(f * 100))
    y = np.zeros(n + p + 1)
    burst = rnd.uniform(-1, 1, p)
    burst = bright * burst + (1 - bright) * np.convolve(burst, np.ones(4) / 4, "same")  # weicherer Anschlag
    y[:p] = burst
    decay = 0.996
    k = p
    while k < n:
        e = min(k + p, n)
        seg = y[k - p:e - p]
        prev = y[k - p - 1:e - p - 1] if k - p - 1 >= 0 else np.concatenate(([0], y[k - p:e - p - 1]))
        y[k:e] = decay * 0.5 * (seg + prev[:len(seg)])
        k = e
    out = y[:n] * np.exp(-np.linspace(0, 3.2, n))
    _cache[key] = out
    return out


def marimba(f, dur=0.9):
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 7.5) * (1 - np.exp(-t * 400))
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 20) + 0.12 * np.sin(2 * np.pi * f * 10 * t) * np.exp(-t * 45)
    return s * env


def bass(f, dur=0.7):
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 4) * (1 - np.exp(-t * 200))
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * env


def shaker(dur=0.09, rnd=None):
    n = int(SR * dur)
    x = rnd.normal(0, 1, n)
    x = np.diff(np.concatenate(([0], x)))  # Hochpass
    return x * np.exp(-np.linspace(0, 6, n)) * (1 - np.exp(-np.linspace(0, 40, n)))


def add(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    e = min(len(buf), i + len(sig))
    buf[i:e] += sig[:e - i] * gain


def make(dur, bpm=104, seed=3):
    rnd = np.random.default_rng(seed)
    beat = 60 / bpm
    bar = beat * 4
    n = int(SR * (dur + 2))
    uke, mel, bas, shk = (np.zeros(n) for _ in range(4))
    chords = [["G4", "C4", "E4", "C5"], ["A4", "C4", "E4", "A4"], ["A4", "C4", "F4", "A4"], ["G4", "B3", "D4", "G4"]]  # C  Am  F  G
    roots = ["C2", "A1", "F2", "G2"]
    # Strumming: Ab Ab-Auf Auf-Ab-Auf (Achtel), leichte Verzögerung pro Saite
    strum = [(0, 1, 1.0), (2, 1, .8), (3, -1, .55), (5, -1, .6), (6, 1, .75), (7, -1, .5)]
    motif = [  # (Achtel im 2-Takt-Muster, Note)
        [(0, "E5"), (2, "G5"), (3, "A5"), (5, "G5"), (8, "E5"), (10, "D5"), (12, "C5")],
        [(0, "A5"), (2, "G5"), (4, "E5"), (6, "G5"), (8, "D5"), (11, "E5"), (12, "C5"), (14, "D5")],
    ]
    bars = int(dur / bar) + 2
    for b in range(bars):
        t0 = b * bar
        ch, ro = chords[b % 4], roots[b % 4]
        for e8, d, v in strum:
            order = ch if d > 0 else ch[::-1]
            for si, nm in enumerate(order):
                add(uke, pluck(hz(nm), 1.4, .45 if d > 0 else .3), t0 + e8 * beat / 2 + si * 0.011 + rnd.uniform(0, .004), v * .22)
        add(bas, bass(hz(ro)), t0, .55)
        add(bas, bass(hz(ro) * 1.5), t0 + 2 * beat, .35)
        for e8 in range(8):
            add(shk, shaker(rnd=rnd), t0 + e8 * beat / 2 + rnd.uniform(-.005, .005), .10 if e8 % 2 else .16)
        if b >= 2 and (b // 4) % 2 == 0:  # Melodie im Wechsel mit Pausen, damit es nicht nervt
            for e8, nm in motif[(b // 2) % 2] if b % 2 == 0 else []:
                add(mel, marimba(hz(nm)), t0 + e8 * beat / 2, .28)
    mix_l = uke * 1.0 + mel * .85 + bas * .9 + shk * .55
    mix_r = uke * .9 + mel * 1.0 + bas * .9 + shk * .75
    st = np.stack([mix_l, mix_r], 1)
    # kleiner Raum: zwei Echos
    for d, g in ((.083, .22), (.137, .14)):
        k = int(d * SR)
        st[k:] += st[:-k] * g
    st = st[: int(SR * dur)]
    fade = int(SR * 1.5)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    st[: int(SR * .05)] *= np.linspace(0, 1, int(SR * .05))[:, None]
    return st / np.max(np.abs(st)) * 0.89


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("duration", type=float)
    ap.add_argument("--bpm", type=float, default=104)
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--duck", help="Sprachspur: Musik wird darunter automatisch leiser")
    ap.add_argument("--lufs", type=float, default=-24, help="Ziel-Lautheit der Musik (Stimme liegt bei ca. -11 bis -14)")
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        raw = Path(d) / "raw.wav"
        sf.write(raw, make(a.duration, a.bpm, a.seed), SR)
        if a.duck:
            fc = ("[1:a]aformat=channel_layouts=stereo,aresample=44100,apad[sc];"
                  "[0:a][sc]sidechaincompress=threshold=0.02:ratio=10:attack=12:release=350:makeup=1[m];"
                  f"[m]loudnorm=I={a.lufs}:TP=-3:LRA=11[o]")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-i", a.duck, "-filter_complex", fc, "-map", "[o]",
                            "-ar", str(SR), out], check=True)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"loudnorm=I={a.lufs}:TP=-3:LRA=11", "-ar", str(SR), out], check=True)
    print(f"Musik: {out} ({a.duration:.1f} s, {a.bpm:g} bpm)")


if __name__ == "__main__":
    main()
