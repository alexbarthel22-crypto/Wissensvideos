#!/usr/bin/env python3
"""Entspannte, gemütliche Strandmusik für Muschel-Tal LIVE („cozy“) – ohne hohe, schrille Töne.

  python3 tools/make_music_cozy.py <ausgabe.mp3> <dauer_s> --seed 1 [--bpm 80] [--tonart 0]

Langsam (ca. 80 bpm), tiefe und weiche Klänge: gezupfte Nylon-Gitarre, warmer Pad-Teppich mit Septimen,
sanftes E-Piano (Rhodes-artig) als Melodie, weicher Bass, leise tiefe Conga. Kein Shaker, keine Steeldrum,
keine hohe Marimba. Am Ende wird alles über ca. 3 kHz sanft abgeschnitten.
Songform mit wechselnden Teilen und Akkordfolgen, damit es über 7 Minuten nicht eintönig wird.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

from make_music_live import SR, add, bass, midi_hz, pluck, akkord, PENTA, DUR_SKALA

# ruhige, warme Akkordfolgen (Stufen der Tonleiter)
FOLGEN = [[0, 5, 3, 4], [3, 4, 0, 5], [0, 3, 0, 4], [5, 3, 0, 4], [0, 2, 3, 3], [3, 0, 4, 0], [0, 5, 1, 4]]


def zeit(dauer):
    return np.arange(int(SR * dauer)) / SR


def rhodes(f, dauer=1.6):
    """Weiches E-Piano: Grundton + leiser Oberton, langsames Tremolo, sanftes Abklingen."""
    t = zeit(dauer)
    env = np.exp(-t * 1.6) * (1 - np.exp(-t * 60))
    trem = 1 + 0.12 * np.sin(2 * np.pi * 4.5 * t)
    return (np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)) * env * trem


def warmpad(freqs, dauer):
    t = zeit(dauer)
    env = np.minimum(1, t / 1.5) * np.minimum(1, np.maximum(0, (dauer - t) / 1.5))
    s = np.zeros(len(t))
    for f in freqs:
        for d in (-0.25, 0.0, 0.25):
            s += np.sin(2 * np.pi * (f + d) * t)
    return s * env / max(1, len(freqs) * 3)


def weicher_bass(f, dauer=1.4):
    t = zeit(dauer)
    env = np.exp(-t * 2.2) * (1 - np.exp(-t * 80))
    return np.sin(2 * np.pi * f * t) * env


def conga(f=110, dauer=0.35):
    t = zeit(dauer)
    fr = f * (1 + 0.3 * np.exp(-t * 30))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 11)


def melodie(rnd, takte):
    noten, pos, idx = [], 0, int(rnd.integers(2, 6))
    while pos < takte * 8:
        if rnd.random() < 0.42:
            idx = int(np.clip(idx + rnd.choice([-2, -1, -1, 0, 1, 1, 2]), 0, 8))
            laenge = int(rnd.choice([2, 3, 4, 4, 6]))
            noten.append((pos, idx, laenge))
            pos += laenge
        else:
            pos += int(rnd.choice([2, 2, 4]))
    return noten


def make(dur, bpm, seed, tonart):
    rnd = np.random.default_rng(seed)
    beat = 60 / bpm
    takt = beat * 4
    n = int(SR * (dur + 6))
    spur = {k: np.zeros(n) for k in ("git", "mel", "bas", "pad", "perc")}

    def teil(art):
        return {"art": art, "folge": FOLGEN[rnd.integers(len(FOLGEN))], "mel": melodie(rnd, 4)}

    strophe, refrain = teil("strophe"), teil("refrain")
    plan, t, runde = [], 0.0, 0
    while t < dur:
        for art, takte in [("intro", 4), ("strophe", 8), ("refrain", 8), ("ruhig", 4), ("strophe", 8), ("refrain", 8), ("ruhig", 8)]:
            if art == "intro" and runde:
                continue
            tl = dict(strophe if art == "strophe" else refrain if art == "refrain" else teil(art))
            if art == "strophe" and runde:
                tl["mel"] = melodie(rnd, 4)
            plan.append((t, takte, tl))
            t += takte * takt
            if t >= dur:
                break
        runde += 1
        if runde % 2 == 0:
            strophe, refrain = teil("strophe"), teil("refrain")

    g = 55 + tonart                                     # Grundton tief (G3 + Tonart)
    for t0, takte, tl in plan:
        art = tl["art"]
        laut = {"intro": .55, "strophe": .8, "refrain": .95, "ruhig": .5}[art]
        for b in range(takte):
            tb = t0 + b * takt
            stufe = tl["folge"][b % 4]
            ak = akkord(stufe, g)
            sept = g + DUR_SKALA[(stufe + 6) % 7] + 12 * ((stufe + 6) // 7)   # Septime für den warmen Klang
            # Pad: Akkord mit Septime, sehr weich
            add(spur["pad"], warmpad([midi_hz(m) for m in ak + [sept]], takt + 1.6), tb, .22 * laut)
            # Gitarre: ruhiges Zupfmuster in Achteln, tiefe Lage
            muster = [ak[0] - 12, ak[2], ak[1] + 12, ak[2], ak[0], ak[2], ak[1] + 12, ak[2]]
            for e8, m in enumerate(muster):
                if art == "ruhig" and e8 % 2:
                    continue
                add(spur["git"], pluck(midi_hz(m), 2.0, .18), tb + e8 * beat / 2 + rnd.uniform(0, .012), (.16 if e8 % 2 else .21) * laut)
            # Bass: weich auf 1 und 3
            if art != "intro":
                add(spur["bas"], weicher_bass(midi_hz(ak[0] - 24)), tb, .5 * laut)
                add(spur["bas"], weicher_bass(midi_hz(ak[0] - 24) * 1.5), tb + 2 * beat, .3 * laut)
            # leise tiefe Conga auf 2 und 4 (nicht in ruhigen Teilen)
            if art in ("strophe", "refrain"):
                add(spur["perc"], conga(105), tb + beat, .16)
                add(spur["perc"], conga(92), tb + 3 * beat, .14)
                if b % 2:
                    add(spur["perc"], conga(120), tb + 3.5 * beat, .08)
            # Melodie: E-Piano in mittlerer Lage
            if art != "intro" or b >= 2:
                versatz = 0 if (b // 4) % 2 == 0 else int(rnd.choice([-1, 1]))
                for pos, idx, laenge in tl["mel"]:
                    if pos // 8 != b % 4:
                        continue
                    i = idx + versatz
                    m = g + 12 + PENTA[i % 5] + 12 * (i // 5)
                    add(spur["mel"], rhodes(midi_hz(m), laenge * beat / 2 + 1.0), tb + (pos % 8) * beat / 2, .24 * laut)

    s = spur
    links = s["git"] * 1.0 + s["mel"] * .75 + s["bas"] * .95 + s["pad"] * 1.0 + s["perc"] * .7
    rechts = s["git"] * .8 + s["mel"] * .95 + s["bas"] * .95 + s["pad"] * 1.0 + s["perc"] * .9
    st = np.stack([links, rechts], 1)
    for d, gn in ((.11, .18), (.19, .11), (.31, .06)):    # weicher Raum
        k = int(d * SR)
        st[k:] += st[:-k] * gn
    st = st[: int(SR * dur)]
    fade = int(SR * 4)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    st[: int(SR * 2)] *= np.linspace(0, 1, int(SR * 2))[:, None]
    return st / np.max(np.abs(st)) * 0.85


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("duration", type=float)
    ap.add_argument("--bpm", type=float, default=80)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--tonart", type=int, default=0)
    ap.add_argument("--lufs", type=float, default=-22)
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        raw = Path(d) / "raw.wav"
        sf.write(raw, make(a.duration, a.bpm, a.seed, a.tonart), SR)
        # alles über ca. 3 kHz sanft absenken (keine schrillen Höhen), Tiefen leicht wärmer
        filt = f"lowpass=f=3200:poles=2,highshelf=f=2000:g=-4,lowshelf=f=200:g=1.5,loudnorm=I={a.lufs}:TP=-2:LRA=9"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", filt, "-ar", str(SR), "-b:a", "96k", out], check=True)
    print(f"Musik (cozy): {out} ({a.duration:.0f} s, {a.bpm:g} bpm, Tonart {a.tonart:+d})")


if __name__ == "__main__":
    main()
