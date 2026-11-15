#!/usr/bin/env python3
"""Lizenzfreie, fröhliche Lagunen-Musik fürs Leuchtturm-Rennen – komplett im Code erzeugt (eigene Komposition).
Stimmung: sonnige Unterwasser-/Korallen-Lobby – Steeldrum, Kalimba, „Aah“-Chor, Pizzicato, federnder Bass, leichte Percussion.

  python3 tools/make_music_lagune.py <ausgabe.mp3> <dauer_s> [--seed 1]
"""
import argparse, subprocess, tempfile
from pathlib import Path
import numpy as np
import soundfile as sf

SR = 44100
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def t_(dur):
    return np.arange(int(SR * dur)) / SR


def steeldrum(f, dur=0.9):
    t = t_(dur)
    s = (np.sin(2*np.pi*f*t) * np.exp(-t*3.2) + .55*np.sin(2*np.pi*2.0*f*t) * np.exp(-t*4.5)
         + .32*np.sin(2*np.pi*3.01*f*t) * np.exp(-t*7) + .18*np.sin(2*np.pi*4.03*f*t) * np.exp(-t*11))
    return s * (1 - np.exp(-t*600)) * (1 + .25*np.exp(-t*30))


def kalimba(f, dur=1.2):
    t = t_(dur)
    s = np.sin(2*np.pi*f*t) * np.exp(-t*3.5) + .28*np.sin(2*np.pi*5.4*f*t) * np.exp(-t*18)
    return s * (1 - np.exp(-t*900))


def pizz(f, dur=.35):
    t = t_(dur)
    s = sum((1/k) * np.sin(2*np.pi*k*f*t) * np.exp(-t*(9+k*3)) for k in range(1, 6))
    return s * (1 - np.exp(-t*800))


FORM = {"a": [(800, 1.0, 90), (1150, .55, 110), (2900, .18, 160)],
        "o": [(450, 1.0, 80), (800, .5, 100), (2830, .1, 150)],
        "u": [(325, 1.0, 70), (700, .3, 90), (2530, .06, 150)]}


def chor(f, dur, vokal="a", attack=.35):
    """Additiver „Aah“-Chor: Obertöne werden durch Vokal-Formanten geformt, 3 leicht verstimmte Stimmen, Vibrato."""
    t = t_(dur)
    out = np.zeros_like(t)
    for det, ph in ((-.06, 0), (0, 1.3), (.07, 2.1)):
        ff = f * 2 ** (det / 12)
        vib = 1 + .006 * np.sin(2*np.pi*5.2*t + ph) * np.clip(t/.6, 0, 1)
        phase = 2*np.pi*np.cumsum(ff*vib)/SR
        for k in range(1, 22):
            fk = ff * k
            if fk > 5000:
                break
            a = sum(g*np.exp(-((fk-fc)/bw)**2) for fc, g, bw in FORM[vokal]) + .02/k
            out += a * np.sin(k*phase + ph*k)
    env = np.clip(t/attack, 0, 1) * np.clip((dur - t)/.4, 0, 1)
    return out * env / 3


def bass(f, dur=.42):
    t = t_(dur)
    return (np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t)*np.exp(-t*8)) * np.exp(-t*3) * (1-np.exp(-t*300))


def kick(rnd):
    t = t_(.25)
    return np.sin(2*np.pi*np.cumsum(55 + 90*np.exp(-t*30))/SR) * np.exp(-t*14)


def clap(rnd):
    n = int(SR*.18); x = rnd.normal(0, 1, n); x = np.diff(np.concatenate(([0], x)))
    t = np.arange(n)/SR
    env = np.exp(-t*28) + sum(np.exp(-((t-d)/.003)**2) for d in (0, .011, .022))*.6
    return x * env * .5


def shaker(rnd):
    n = int(SR*.07); x = np.diff(np.concatenate(([0], rnd.normal(0, 1, n))))
    return x * np.exp(-np.linspace(0, 6, n)) * (1-np.exp(-np.linspace(0, 40, n)))


def bongo(f, rnd):
    t = t_(.18)
    return np.sin(2*np.pi*np.cumsum(f*(1+.4*np.exp(-t*40)))/SR) * np.exp(-t*22)


def add(buf, sig, t, g=1.0):
    i = int(t*SR)
    if i >= len(buf): return
    e = min(len(buf), i+len(sig)); buf[i:e] += sig[:e-i]*g


# Akkorde als Stufen in Dur (0=I …), Voicing mit add9/maj7-Farbe
STUFEN = {0: [0, 4, 7, 11, 14], 1: [2, 5, 9, 12, 16], 3: [5, 9, 12, 16, 19], 4: [7, 11, 14, 17, 21], 5: [9, 12, 16, 19, 23], 2: [4, 7, 11, 14, 18]}
FOLGEN = [[0, 4, 5, 3], [3, 0, 4, 5], [0, 2, 3, 4], [5, 3, 0, 4], [0, 3, 1, 4]]
DUR = [0, 2, 4, 5, 7, 9, 11]


def melodie(rnd, akk, laenge=8):
    """Sanglich-hüpfende Melodie: Akkordtöne auf Schlägen, Durchgänge dazwischen."""
    toene = []
    ton = rnd.choice([12, 16, 19])
    rhythmen = [[0, 1, 2, 3, 4, 6], [0, 1.5, 2, 3, 4, 5, 6], [0, 2, 2.5, 3, 4, 6, 7], [0, .5, 1, 2, 4, 4.5, 5, 6]]
    for zeit in rhythmen[rnd.integers(len(rhythmen))]:
        ziel = [a+12 for a in STUFEN[akk]] if int(zeit) == zeit else None
        if ziel:
            ton = min(ziel, key=lambda z: abs(z-ton) + rnd.uniform(0, 3))
        else:
            schritte = [x+12*o for o in (1, 2) for x in DUR]
            ton = min(schritte, key=lambda z: abs(z-(ton + rnd.choice([-2, -1, 1, 2]))))
        toene.append((zeit, ton))
    return toene


def make(dur, seed=1):
    rnd = np.random.default_rng(seed)
    grund = [60, 62, 65, 67, 57][seed % 5]            # C, D, F, G, A Dur
    bpm = [116, 112, 120, 108, 118][seed % 5]
    beat = 60/bpm; takt = 4*beat
    n = int(SR*(dur+3))
    spuren = {k: np.zeros(n) for k in ("steel", "kal", "chor", "pizz", "bass", "perc")}
    folge = FOLGEN[seed % len(FOLGEN)]
    motive = [[melodie(rnd, a) for a in folge] for _ in range(2)]
    takte = int(dur/takt)+1
    for b in range(takte):
        t0 = b*takt; teil = (b // 8) % 4          # 0 Intro/leicht, 1 voll, 2 Chor-Teil, 3 voll
        if b < 4: teil = -1
        akk = folge[b % 4]; acc = STUFEN[akk]
        # Chor-Pad (immer, im Intro allein)
        for i, s in enumerate(acc[:4]):
            add(spuren["chor"], chor(hz(grund+s-12), takt+.3, "aou"[(b//4) % 3] if teil != 2 else "a"), t0, .07 if teil != 2 else .1)
        # Kalimba-Arpeggio (Achtel)
        muster = [0, 2, 1, 3, 4, 2, 3, 1]
        for e in range(8):
            if teil == -1 and e % 2: continue
            add(spuren["kal"], kalimba(hz(grund+acc[muster[e]]+12)), t0+e*beat/2+rnd.uniform(0, .006), .16 if e % 2 == 0 else .1)
        if teil >= 0:
            # federnder Bass: 1, (2+), 3, 4+
            r = grund + acc[0] - 24
            for zeit, ver, g in ((0, 0, .7), (1.5, 0, .45), (2, 7, .55), (3.5, 12, .4)):
                add(spuren["bass"], bass(hz(r+ver)), t0+zeit*beat, g)
            # Percussion
            for e in range(8):
                add(spuren["perc"], shaker(rnd), t0+e*beat/2, .08 if e % 2 else .12)
            add(spuren["perc"], kick(rnd), t0, .55); add(spuren["perc"], kick(rnd), t0+2*beat, .45)
            add(spuren["perc"], clap(rnd), t0+beat, .35); add(spuren["perc"], clap(rnd), t0+3*beat, .35)
            for zeit, f in ((1.75, 330), (2.5, 250), (3.25, 330), (3.75, 220)):
                add(spuren["perc"], bongo(f, rnd), t0+zeit*beat, .18)
            # Pizzicato-Gegenstimme
            if teil in (1, 3):
                for zeit in (.5, 1.5, 2.5, 3.5):
                    add(spuren["pizz"], pizz(hz(grund+acc[rnd.integers(1, 4)])), t0+zeit*beat, .16)
        # Melodie: Steeldrum (Teil 1/3), Chor-„uuh“ (Teil 2)
        mot = motive[(b//4) % 2][b % 4]
        if teil in (1, 3):
            for zeit, ton in mot:
                add(spuren["steel"], steeldrum(hz(grund+ton)), t0+zeit*beat/2, .26)
                if teil == 3: add(spuren["steel"], steeldrum(hz(grund+ton+12)), t0+zeit*beat/2+.002, .07)
        elif teil == 2:
            for i, (zeit, ton) in enumerate(mot):
                lang = ((mot[i+1][0] if i+1 < len(mot) else 8) - zeit)*beat/2
                add(spuren["chor"], chor(hz(grund+ton), max(.25, lang+.05), "u", .06), t0+zeit*beat/2, .16)
    g = {"steel": (1, .8), "kal": (.7, 1), "chor": (1, 1), "pizz": (1, .6), "bass": (.9, .9), "perc": (.75, .9)}
    L = sum(spuren[k]*g[k][0] for k in spuren); R = sum(spuren[k]*g[k][1] for k in spuren)
    st = np.stack([L, R], 1)
    for d, gg in ((.11, .2), (.19, .13), (.31, .08)):      # Raum
        k = int(d*SR); st[k:] += st[:-k]*gg
    st = st[:int(SR*dur)]
    fade = int(SR*2.5); st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    st[:int(SR*.05)] *= np.linspace(0, 1, int(SR*.05))[:, None]
    return st/np.max(np.abs(st))*.89


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("duration", type=float); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--lufs", type=float, default=-20)
    a = ap.parse_args()
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        raw = Path(d)/"raw.wav"; sf.write(raw, make(a.duration, a.seed), SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"loudnorm=I={a.lufs}:TP=-2:LRA=11", "-ar", str(SR), "-b:a", "160k", out], check=True)
    print(f"Musik: {out}")


if __name__ == "__main__":
    main()
