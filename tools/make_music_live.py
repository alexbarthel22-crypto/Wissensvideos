#!/usr/bin/env python3
"""Lange, abwechslungsreiche Südsee-Musik für Muschel-Tal LIVE – lizenzfrei, komplett im Code erzeugt.

  python3 tools/make_music_live.py <ausgabe.mp3> <dauer_s> --seed 1 [--bpm 100] [--tonart 0]

Anders als make_music_tropical.py (kurze Videos) wiederholt sich hier nichts schnell:
- Songform aus Teilen (Intro, Strophe, Refrain, Zwischenteil, ruhige Stelle) mit eigenen Akkordfolgen
- Melodien werden pro Teil neu erfunden (Frage/Antwort-Phrasen aus der Tonleiter), Refrain kehrt variiert wieder
- wechselnde Instrumente: Ukulele (Strumming oder gezupft), Marimba, Steeldrum, Flöte, Pad, Bass, Shaker, Bongos
- sanfte Übergänge (Fills, Becken-Swell), Tonart-Rückung nach oben im zweiten Durchgang
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100
DUR_SKALA = [0, 2, 4, 5, 7, 9, 11]                    # Dur-Tonleiter in Halbtönen
PENTA = [0, 2, 4, 7, 9]                                # Pentatonik für Melodien (klingt immer „sonnig“)


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


_cache = {}


def pluck(f, dur=1.4, bright=0.45):
    key = (round(f, 2), dur, bright)
    if key in _cache:
        return _cache[key]
    n = int(SR * dur)
    p = max(2, int(round(SR / f)))
    rnd = np.random.default_rng(int(f * 100))
    y = np.zeros(n + p + 1)
    burst = rnd.uniform(-1, 1, p)
    burst = bright * burst + (1 - bright) * np.convolve(burst, np.ones(4) / 4, "same")
    y[:p] = burst
    k = p
    while k < n:
        e = min(k + p, n)
        seg = y[k - p:e - p]
        prev = y[k - p - 1:e - p - 1] if k - p - 1 >= 0 else np.concatenate(([0], y[k - p:e - p - 1]))
        y[k:e] = 0.996 * 0.5 * (seg + prev[:len(seg)])
        k = e
    out = y[:n] * np.exp(-np.linspace(0, 3.2, n))
    _cache[key] = out
    return out


def env_t(dur):
    return np.arange(int(SR * dur)) / SR


def marimba(f, dur=0.9):
    t = env_t(dur)
    env = np.exp(-t * 7.5) * (1 - np.exp(-t * 400))
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 20)) * env


def steeldrum(f, dur=1.1):
    t = env_t(dur)
    env = np.exp(-t * 4.5) * (1 - np.exp(-t * 300))
    s = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 3)
         + 0.28 * np.sin(2 * np.pi * f * 2.98 * t) * np.exp(-t * 6) + 0.15 * np.sin(2 * np.pi * f * 4.2 * t) * np.exp(-t * 9))
    return s * env


def floete(f, dur=0.8):
    t = env_t(dur)
    att = np.minimum(1, t / 0.06)
    rel = np.minimum(1, np.maximum(0, (dur - t) / 0.12))
    vib = np.sin(2 * np.pi * 5.2 * t) * 0.004 * np.minimum(1, t / 0.3)
    ph = 2 * np.pi * f * np.cumsum(1 + vib) / SR
    rnd = np.random.default_rng(int(f))
    hauch = np.convolve(rnd.normal(0, 1, len(t)), np.ones(30) / 30, "same") * 0.05
    return (np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph) + hauch) * att * rel


def pad(freqs, dur):
    t = env_t(dur)
    env = np.minimum(1, t / 0.8) * np.minimum(1, np.maximum(0, (dur - t) / 0.8))
    s = np.zeros(len(t))
    for f in freqs:
        for d in (-0.15, 0.15):
            s += np.sin(2 * np.pi * (f + d) * t) + 0.3 * np.sin(2 * np.pi * 2 * (f + d) * t)
    return s * env / max(1, len(freqs))


def bass(f, dur=0.6):
    t = env_t(dur)
    env = np.exp(-t * 4) * (1 - np.exp(-t * 200))
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * env


def shaker(rnd, dur=0.09):
    n = int(SR * dur)
    x = np.diff(np.concatenate(([0], rnd.normal(0, 1, n))))
    return x * np.exp(-np.linspace(0, 6, n)) * (1 - np.exp(-np.linspace(0, 40, n)))


def bongo(f, dur=0.25):
    t = env_t(dur)
    fr = f * (1 + 0.6 * np.exp(-t * 40))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 18)


def swell(rnd, dur=1.6):
    n = int(SR * dur)
    x = np.diff(np.concatenate(([0], rnd.normal(0, 1, n))))
    return x * np.linspace(0, 1, n) ** 2 * 0.5


def add(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf) or i < 0:
        return
    e = min(len(buf), i + len(sig))
    buf[i:e] += sig[:e - i] * gain


# Akkordfolgen als Stufen der Tonleiter (0 = I, 3 = IV, 4 = V, 5 = vi, 1 = ii, 2 = iii)
FOLGEN = [[0, 5, 3, 4], [0, 3, 0, 4], [5, 3, 0, 4], [0, 2, 3, 4], [3, 4, 0, 5], [0, 4, 5, 3], [1, 4, 0, 0], [3, 0, 4, 5], [0, 3, 5, 4], [5, 4, 3, 4]]


def akkord(stufe, grund):
    """Dreiklang (MIDI) zur Stufe in der Tonart grund."""
    return [grund + DUR_SKALA[(stufe + k) % 7] + 12 * ((stufe + k) // 7) for k in (0, 2, 4)]


def erfinde_melodie(rnd, takte, dichte):
    """Melodie als Liste (Achtel-Position, Pentatonik-Index, Länge in Achteln) über `takte` Takte."""
    noten, pos, idx = [], 0, rnd.integers(3, 7)
    while pos < takte * 8:
        if rnd.random() < dichte:
            idx = int(np.clip(idx + rnd.choice([-2, -1, -1, 0, 1, 1, 2]), 0, 10))
            laenge = int(rnd.choice([1, 1, 2, 2, 3, 4]))
            noten.append((pos, idx, laenge))
            pos += laenge
        else:
            pos += int(rnd.choice([1, 2]))
        if pos % 16 == 14 and rnd.random() < 0.6:   # Atempause am Phrasenende
            pos += 2
    return noten


def make(dur, bpm, seed, tonart):
    rnd = np.random.default_rng(seed)
    beat = 60 / bpm
    takt = beat * 4
    n = int(SR * (dur + 4))
    spuren = {k: np.zeros(n) for k in ("uke", "mel", "bas", "pad", "perc")}

    # Teile mit eigenem Material
    def neuer_teil(art):
        return {
            "art": art,
            "folge": FOLGEN[rnd.integers(len(FOLGEN))],
            "melodie": erfinde_melodie(rnd, 4, {"intro": .35, "strophe": .55, "refrain": .75, "zwischen": .5, "ruhig": .3}[art]),
            "instr": rnd.choice(["marimba", "steeldrum", "floete"]),
            "zupfen": art in ("ruhig", "intro") or rnd.random() < .3,
        }
    strophe, refrain = neuer_teil("strophe"), neuer_teil("refrain")
    form = []
    t = 0.0
    durchgang = 0
    while t < dur:
        plan = [("intro", 4)] if t == 0 else []
        plan += [("strophe", 8), ("refrain", 8), ("zwischen", 4), ("strophe", 8), ("refrain", 8), ("ruhig", 8)]
        for art, takte in plan:
            if art == "strophe":
                teil = dict(strophe)
                if durchgang:                      # zweite Runde: neue Melodie, gleicher Charakter
                    teil["melodie"] = erfinde_melodie(rnd, 4, .55)
                    teil["instr"] = rnd.choice(["marimba", "steeldrum", "floete"])
            elif art == "refrain":
                teil = dict(refrain)
                if durchgang % 2:
                    teil["instr"] = rnd.choice(["marimba", "steeldrum", "floete"])
            else:
                teil = neuer_teil(art)
            form.append((t, takte, teil, tonart + (2 if durchgang % 3 == 2 else 0)))
            t += takte * takt
            if t >= dur:
                break
        durchgang += 1
        if durchgang % 2 == 0:                     # nach zwei Runden komplett neues Material
            strophe, refrain = neuer_teil("strophe"), neuer_teil("refrain")

    strum = [(0, 1, 1.0), (2, 1, .8), (3, -1, .55), (5, -1, .6), (6, 1, .75), (7, -1, .5)]
    for t0_teil, takte, teil, grund in form:
        art = teil["art"]
        laut = {"intro": .6, "strophe": .85, "refrain": 1.0, "zwischen": .8, "ruhig": .5}[art]
        g = 60 + grund                              # Tonart (C4 = 60)
        for b in range(takte):
            t0 = t0_teil + b * takt
            stufe = teil["folge"][b % 4]
            ak = akkord(stufe, g)
            # Ukulele: strummen oder zupfen
            if teil["zupfen"]:
                muster = [0, 2, 1, 2, 0, 2, 1, 2]
                for e8, k in enumerate(muster):
                    add(spuren["uke"], pluck(midi_hz(ak[k] + 12), 1.2, .35), t0 + e8 * beat / 2 + rnd.uniform(0, .006), .2 * laut)
            else:
                stimmen = [ak[2], ak[0] + 12, ak[1] + 12, ak[2] + 12]
                for e8, d, v in strum:
                    if art == "zwischen" and e8 in (3, 7):
                        continue
                    order = stimmen if d > 0 else stimmen[::-1]
                    for si, m in enumerate(order):
                        add(spuren["uke"], pluck(midi_hz(m), 1.3, .45 if d > 0 else .3), t0 + e8 * beat / 2 + si * .011 + rnd.uniform(0, .004), v * .2 * laut)
            # Bass
            wurzel = midi_hz(ak[0] - 24)
            if art != "intro":
                add(spuren["bas"], bass(wurzel), t0, .55 * laut)
                add(spuren["bas"], bass(wurzel * 1.5), t0 + 2 * beat, .35 * laut)
                if art == "refrain":
                    add(spuren["bas"], bass(wurzel * 2), t0 + 3.5 * beat, .25)
            # Pad in ruhigen Teilen und im Refrain
            if art in ("ruhig", "refrain", "intro"):
                add(spuren["pad"], pad([midi_hz(m) for m in ak], takt + .4), t0, .12 if art == "refrain" else .2)
            # Percussion
            if art not in ("intro", "ruhig") or b >= takte - 2:
                for e8 in range(8):
                    add(spuren["perc"], shaker(rnd), t0 + e8 * beat / 2 + rnd.uniform(-.005, .005), (.1 if e8 % 2 else .16) * laut)
            if art in ("refrain", "zwischen"):
                for e8, f in ((0, 180), (3, 240), (6, 240), (7, 180)):
                    add(spuren["perc"], bongo(f), t0 + e8 * beat / 2, .22)
            # Melodie (4-Takt-Phrase, in Takt 5–8 als Antwort eine Stufe versetzt)
            if art != "intro" or b >= 2:
                phrase_b = b % 4
                versatz = 0 if (b // 4) % 2 == 0 else int(rnd.choice([-1, 1, 2]))
                for pos, idx, laenge in teil["melodie"]:
                    if pos // 8 != phrase_b:
                        continue
                    i = idx + versatz
                    m = g + 12 + PENTA[i % 5] + 12 * (i // 5)
                    f = midi_hz(m)
                    zeit = t0 + (pos % 8) * beat / 2
                    instr = teil["instr"]
                    if instr == "marimba":
                        add(spuren["mel"], marimba(f), zeit, .26)
                    elif instr == "steeldrum":
                        add(spuren["mel"], steeldrum(f), zeit, .22)
                    else:
                        add(spuren["mel"], floete(f, laenge * beat / 2 * .95 + .05), zeit, .2)
        # Übergang: Becken-Swell und Bongo-Fill vor jedem Teilwechsel
        ende = t0_teil + takte * takt
        add(spuren["perc"], swell(rnd), ende - 1.6, .12)
        for k in range(4):
            add(spuren["perc"], bongo(200 + k * 25), ende - beat + k * beat / 4, .2)

    s = spuren
    links = s["uke"] * 1.0 + s["mel"] * .8 + s["bas"] * .9 + s["pad"] * .9 + s["perc"] * .55
    rechts = s["uke"] * .85 + s["mel"] * 1.0 + s["bas"] * .9 + s["pad"] * .9 + s["perc"] * .75
    st = np.stack([links, rechts], 1)
    for d, gn in ((.083, .22), (.137, .14), (.21, .08)):
        k = int(d * SR)
        st[k:] += st[:-k] * gn
    st = st[: int(SR * dur)]
    fade = int(SR * 3)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    st[: int(SR * .05)] *= np.linspace(0, 1, int(SR * .05))[:, None]
    return st / np.max(np.abs(st)) * 0.89


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("duration", type=float)
    ap.add_argument("--bpm", type=float, default=100)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--tonart", type=int, default=0, help="Halbtöne über C")
    ap.add_argument("--lufs", type=float, default=-20)
    ap.add_argument("--kbps", type=int, default=96)
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        raw = Path(d) / "raw.wav"
        sf.write(raw, make(a.duration, a.bpm, a.seed, a.tonart), SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"loudnorm=I={a.lufs}:TP=-2:LRA=11",
                        "-ar", str(SR), "-b:a", f"{a.kbps}k", out], check=True)
    print(f"Musik: {out} ({a.duration:.0f} s, {a.bpm:g} bpm, Tonart +{a.tonart})")


if __name__ == "__main__":
    main()
