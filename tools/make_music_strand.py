#!/usr/bin/env python3
"""Ruhige Strand-/Urlaubsmusik für Muschel-Tal LIVE („strand“) – kein Klingklang, keine hohen Töne.

  python3 tools/make_music_strand.py <ausgabe.mp3> <dauer_s> --seed 1 [--bpm 66] [--tonart 0]

Langsam (ca. 66 bpm), Lounge-Stimmung wie Sonnenuntergang am Strand: weicher Akkord-Teppich (maj7/9),
warmer runder Bass, ganz leise gedämpfte Gitarre (dunkel, nur 2 Anschläge pro Takt), weicher Kick und
gebürstetes Rauschen statt Shaker, sparsame tiefe Flöten-Melodie (lange Töne, Vibrato), leise Wellen.
Alles über ca. 1,8 kHz wird abgesenkt – keine hellen, klimpernden Töne.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

from make_music_live import SR, add, midi_hz, pluck, akkord, PENTA, DUR_SKALA

FOLGEN = [[0, 5, 1, 4], [0, 3, 0, 4], [5, 3, 0, 4], [0, 5, 3, 4], [3, 4, 0, 0], [0, 2, 3, 4]]


def zeit(d):
    return np.arange(int(SR * d)) / SR


def teppich(freqs, d):
    """sehr weicher Akkord: langsames Ein-/Ausblenden, leichte Schwebung, kaum Obertöne"""
    t = zeit(d)
    env = np.minimum(1, t / 2.2) * np.minimum(1, np.maximum(0, (d - t) / 2.0))
    s = np.zeros(len(t))
    for f in freqs:
        for dd in (-0.18, 0.0, 0.2):
            s += np.sin(2 * np.pi * (f + dd) * t) + 0.12 * np.sin(4 * np.pi * (f + dd) * t)
    return s * env / max(1, len(freqs) * 3)


def bass(f, d):
    t = zeit(d)
    env = (1 - np.exp(-t * 40)) * np.exp(-t * 1.1)
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) * np.exp(-t * 4)) * env


def kick(d=0.5):
    t = zeit(d)
    fr = 52 + 40 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 9)


def buerste(rnd, d=0.45):
    """weich gebürstetes Rauschen (tief gefiltert) statt Shaker"""
    n = int(SR * d)
    w = rnd.normal(0, 1, n)
    k = 60
    w = np.convolve(w, np.ones(k) / k, mode="same")
    t = np.arange(n) / SR
    return w * (1 - np.exp(-t * 30)) * np.exp(-t * 7)


def floete(f, d):
    """tiefe, weiche Flöte: langsamer Einsatz, Vibrato, fast reiner Sinus"""
    t = zeit(d)
    env = np.minimum(1, t / 0.35) * np.minimum(1, np.maximum(0, (d - t) / 0.6))
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * t) * np.minimum(1, t / 0.8)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    return (np.sin(ph) + 0.08 * np.sin(2 * ph)) * env


def wellen(rnd, d):
    n = int(SR * d)
    w = rnd.normal(0, 1, n)
    for k in (180, 90):
        w = np.convolve(w, np.ones(k) / k, mode="same")
    t = np.arange(n) / SR
    hub = 0.5 + 0.5 * np.sin(2 * np.pi * t / 9.5) ** 2
    return w * hub


def make(dur, bpm, seed, tonart):
    rnd = np.random.default_rng(seed)
    beat = 60 / bpm
    takt = beat * 4
    n = int(SR * (dur + 8))
    S = {k: np.zeros(n) for k in ("pad", "bas", "git", "mel", "rhy", "mee")}
    g = 50 + tonart                                     # Grundton tief (D3 + Tonart)
    takte = int(dur / takt) + 1
    folge = FOLGEN[rnd.integers(len(FOLGEN))]
    for b in range(takte):
        tb = b * takt
        if b % 8 == 0 and b:
            folge = FOLGEN[rnd.integers(len(FOLGEN))]
        teil = (b // 8) % 4                             # 0 ruhig, 1 mit Rhythmus, 2 mit Melodie, 3 ruhig
        stufe = folge[b % 4]
        ak = akkord(stufe, g)
        sept = g + DUR_SKALA[(stufe + 6) % 7] + 12 * ((stufe + 6) // 7)
        none = g + DUR_SKALA[(stufe + 1) % 7] + 12 * ((stufe + 1) // 7) + 12
        add(S["pad"], teppich([midi_hz(m) for m in ak + [sept, none]], takt + 2.4), tb, .3)
        add(S["bas"], bass(midi_hz(ak[0] - 12), beat * 2.6), tb, .55)
        add(S["bas"], bass(midi_hz(ak[0] - 12 + 7), beat * 1.6), tb + 2.5 * beat, .28)
        # gedämpfte, dunkle Gitarre: nur 2 weiche Anschläge pro Takt (kein Gezupfe)
        for tt, gn in ((0, .12), (1.5 * beat, .08)):
            for k, m in enumerate(ak):
                add(S["git"], pluck(midi_hz(m), 1.2, .06), tb + tt + k * 0.018, gn)
        if teil in (1, 2):
            add(S["rhy"], kick(), tb, .35)
            add(S["rhy"], kick(), tb + 2.5 * beat, .18)
            add(S["rhy"], buerste(rnd), tb + beat, .1)
            add(S["rhy"], buerste(rnd), tb + 3 * beat, .1)
        if teil == 2 and b % 2 == 0:
            pos = 0.0
            while pos < 7.5:
                if rnd.random() < .55:
                    lang = float(rnd.choice([2, 3, 4]))
                    i = int(rnd.integers(0, 7))
                    m = g + 12 + PENTA[i % 5] + 12 * (i // 5)  # D4 bis ca. A4 – tief und warm
                    add(S["mel"], floete(midi_hz(m), lang * beat * .95), tb + pos * beat, .2)
                    pos += lang
                else:
                    pos += 1.0
    add(S["mee"], wellen(rnd, dur + 4), 0, .05)
    L = S["pad"] + S["bas"] + S["git"] * 1.0 + S["mel"] * .85 + S["rhy"] + S["mee"]
    R = S["pad"] + S["bas"] + S["git"] * .8 + S["mel"] * 1.0 + S["rhy"] * .95 + S["mee"] * 1.1
    st = np.stack([L, R], 1)
    for d, gn in ((.13, .2), (.23, .12), (.37, .07)):    # weicher, warmer Raum
        k = int(d * SR)
        st[k:] += st[:-k] * gn
    st = st[: int(SR * dur)]
    f = int(SR * 5)
    st[-f:] *= np.linspace(1, 0, f)[:, None]
    st[: int(SR * 3)] *= np.linspace(0, 1, int(SR * 3))[:, None]
    return st / np.max(np.abs(st)) * 0.85


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("duration", type=float)
    ap.add_argument("--bpm", type=float, default=66)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--tonart", type=int, default=0)
    ap.add_argument("--lufs", type=float, default=-22)
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        raw = Path(d) / "raw.wav"
        sf.write(raw, make(a.duration, a.bpm, a.seed, a.tonart), SR)
        filt = f"lowpass=f=1800:poles=2,highshelf=f=1200:g=-6,lowshelf=f=180:g=2,loudnorm=I={a.lufs}:TP=-2:LRA=9"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", filt, "-ar", str(SR), "-b:a", "96k", out], check=True)
    print(f"Musik (strand): {out} ({a.duration:.0f} s, {a.bpm:g} bpm, Tonart {a.tonart:+d})")


if __name__ == "__main__":
    main()
