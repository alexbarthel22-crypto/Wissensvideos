#!/usr/bin/env python3
"""Synthetische Kirchen-Sounds für die Prophet-Peter-Serie (keine Downloads nötig).

  python3 tools/make_church.py videos/<slug>/assets/sfx
schreibt holy-sting.wav (Glockenschlag + Orgel-Akkord), bell-hit.wav (kurze Glocke), coin.wav (Münze im Klingelbeutel),
angel-choir.wav (Engelschor „Aaah“, D-Dur), goat.wav (Ziege „Mäh-äh-äh“), sad-trombone.wav (traurige Posaune), record-scratch.wav (Plattenkratzer), creak.wav (rostiges Tor), shimmer.wav (Glitzer-Arpeggio).
Optional: --choir <datei.mp3> -> choir-intro.wav (erste 2,6 s, ausgeblendet); --bell <datei.mp3> schneidet den lautesten Glockenschlag heraus -> church-bell.wav (für Frame 0).
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100


def bell(f0, dur, amp=1.0):
    t = np.arange(int(SR * dur)) / SR
    # klassische Glocken-Teiltöne (Hum, Prime, Terz, Quinte, Oktave …) mit eigener Abklingzeit
    parts = [(0.5, 1.0, 2.6), (1.0, 0.8, 1.8), (1.19, 0.55, 1.4), (1.5, 0.35, 1.1), (2.0, 0.5, 0.9),
             (2.52, 0.25, 0.6), (3.0, 0.18, 0.45), (4.07, 0.12, 0.3)]
    y = sum(a * np.sin(2 * np.pi * f0 * r * t + r) * np.exp(-t / d) for r, a, d in parts)
    y *= 1 - np.exp(-t / 0.002)
    return amp * y / np.abs(y).max()


def organ(freqs, dur, attack=0.35):
    t = np.arange(int(SR * dur)) / SR
    y = np.zeros_like(t)
    for f in freqs:
        for h, a in [(1, 1), (2, 0.5), (3, 0.25), (4, 0.18), (6, 0.08)]:
            y += a * np.sin(2 * np.pi * f * h * t) * (1 + 0.004 * np.sin(2 * np.pi * 5.2 * t))
    env = np.minimum(1, t / attack) * np.exp(-np.maximum(0, t - 0.9) / 0.55)
    return y * env / np.abs(y).max()


def coin():
    t = np.arange(int(SR * 0.7)) / SR
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in [(2637, 1, .25), (3951, .6, .18), (5274, .4, .12), (6645, .25, .08)])
    second = np.zeros_like(y); k = int(SR * 0.09); second[k:] = 0.55 * y[: len(y) - k]
    return (y + second) / np.abs(y + second).max()


def fade_out(y, sec=0.08):
    n = int(SR * sec); y[-n:] *= np.linspace(1, 0, n); return y


def formant_voice(f0, t, formants, nh=40):
    """Harmonische Quelle, Amplituden nach Formant-Hüllkurve (Quelle-Filter im Frequenzbereich)."""
    ph = 2 * np.pi * np.cumsum(f0) / SR
    y = np.zeros_like(t)
    for h in range(1, nh + 1):
        fh = h * np.median(f0)
        if fh > 9000:
            break
        a = sum(g * np.exp(-((fh - F) / B) ** 2) for F, B, g in formants) + 0.02
        y += a / h ** 0.3 * np.sin(h * ph)
    return y


def reverb(y, sec=1.6, wet=0.35, seed=4):
    r = np.random.default_rng(seed)
    ir = r.standard_normal(int(SR * sec)) * np.exp(-np.arange(int(SR * sec)) / (SR * sec / 5))
    w = np.convolve(y, ir)
    d = np.concatenate([y, np.zeros(len(w) - len(y))])
    return d + wet * w / np.abs(w).max() * np.abs(y).max()


def choir(dur=3.0):
    t = np.arange(int(SR * dur)) / SR
    A = [(800, 160, 1.0), (1150, 200, 0.6), (2900, 300, 0.25), (3300, 300, 0.12)]
    rng = np.random.default_rng(9)
    y = np.zeros_like(t)
    for f in [293.66, 369.99, 440.0, 587.33, 739.99]:
        for k in range(4):
            det = 2 ** (rng.uniform(-12, 12) / 1200)
            vib = 1 + 0.006 * np.sin(2 * np.pi * rng.uniform(4.8, 6.0) * t + rng.uniform(0, 6))
            y += formant_voice(f * det * vib, t, A)
    env = np.minimum(1, t / 0.45) * np.clip((dur - t) / 0.9, 0, 1)
    y = reverb(y * env / np.abs(y).max(), 1.8, 0.5)
    return y / np.abs(y).max()


def goat():
    dur = 1.0
    t = np.arange(int(SR * dur)) / SR
    f0 = 390 * (1 - 0.12 * t) * (1 + 0.05 * np.sin(2 * np.pi * 8.5 * t))
    y = formant_voice(f0, t, [(650, 140, 1.0), (1800, 220, 0.7), (2600, 260, 0.35)], nh=25)
    trem = 0.55 + 0.45 * np.sin(2 * np.pi * 8.5 * t) ** 2
    env = np.minimum(1, t / 0.04) * np.clip((dur - t) / 0.25, 0, 1)
    y = y * trem * env
    return y / np.abs(y).max()


def creak():
    dur = 1.1
    n = int(SR * dur); y = np.zeros(n); t = 0.0
    rng = np.random.default_rng(2)
    while t < dur - 0.02:
        rate = 28 + 40 * (t / dur) + 10 * np.sin(t * 9)
        i = int(t * SR); y[i] += rng.uniform(0.6, 1.0); t += 1 / rate
    k = np.arange(int(SR * 0.03)) / SR
    ir = sum(np.sin(2 * np.pi * f * k) * np.exp(-k / d) for f, d in [(820, .01), (1560, .006), (2400, .004)])
    y = np.convolve(y, ir)[:n]
    y *= np.minimum(1, np.arange(n) / (SR * 0.05)) * np.clip((dur - np.arange(n) / SR) / 0.2, 0, 1)
    return y / np.abs(y).max()


def shimmer():
    out = np.zeros(int(SR * 1.6))
    for i, f in enumerate([1318.5, 1567.98, 1975.5, 2637.0, 3136.0]):
        b = bell(f * 2, 1.0) * 0.6
        k = int(SR * i * 0.07); out[k:k + len(b)] += b[: len(out) - k]
    return out / np.abs(out).max()


def crack():
    """Ast bricht: trockenes Knacken (mehrere kurze Rauschimpulse, Holzresonanz) + Splittern."""
    dur = 0.7; n = int(SR * dur); rng = np.random.default_rng(5)
    y = np.zeros(n)
    for t0, a in [(0.0, 1.0), (0.018, 0.8), (0.05, 0.55), (0.09, 0.4), (0.16, 0.25), (0.23, 0.15)]:
        k = int(t0 * SR); m = int(SR * 0.03)
        y[k:k + m] += a * rng.standard_normal(m) * np.exp(-np.arange(m) / (SR * 0.004))
    kk = np.arange(int(SR * 0.05)) / SR
    ir = sum(np.sin(2 * np.pi * f * kk) * np.exp(-kk / d) for f, d in [(320, .02), (740, .012), (1900, .006)])
    y = np.convolve(y, ir)[:n] + 0.3 * y
    return y / np.abs(y).max()


def sad_trombone():
    """„Wah-wah-wah-waaah“: vier absteigende Posaunentöne, der letzte mit Vibrato."""
    out = []
    for f, d, vib in [(233.08, 0.38, 0), (220.0, 0.38, 0), (207.65, 0.38, 0), (196.0, 1.25, 1)]:
        t = np.arange(int(SR * d)) / SR
        f0 = f * (1 + (0.035 * np.sin(2 * np.pi * 6 * t) * np.minimum(1, t / 0.3) if vib else 0)) * (1 - 0.02 * t / d)
        y = formant_voice(f0, t, [(500, 180, 1.0), (1100, 260, 0.7), (2400, 400, 0.3)], nh=30)
        env = np.minimum(1, t / 0.04) * np.clip((d - t) / 0.08, 0, 1) * (0.75 + 0.25 * np.minimum(1, t / 0.12))
        if vib:
            env *= np.clip((d - t) / 0.5, 0, 1) ** 0.5
        out.append(y * env)
    y = np.concatenate(out)
    return y / np.abs(y).max()


def record_scratch():
    """Plattenkratzer: gefiltertes Rauschen mit schneller Tonhöhen-Kurve vor und zurück."""
    dur = 0.45; n = int(SR * dur); t = np.arange(n) / SR
    rng = np.random.default_rng(8)
    sweep = 1200 + 2600 * np.abs(np.sin(2 * np.pi * 2.6 * t))
    ph = 2 * np.pi * np.cumsum(sweep) / SR
    y = (0.6 * np.sin(ph) + 0.4 * np.sin(2.01 * ph)) * (0.5 + 0.5 * rng.standard_normal(n).clip(-2, 2) / 2)
    y *= np.minimum(1, t / 0.01) * np.clip((dur - t) / 0.08, 0, 1)
    return y / np.abs(y).max()


def clip(path, t0, t1, fade=0.4):
    import subprocess, tempfile
    with tempfile.TemporaryDirectory() as d:
        w = Path(d) / "c.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-ac", "2", "-ar", str(SR), str(w)], check=True)
        a, _ = sf.read(w)
    a = a[int(t0 * SR): int(t1 * SR)].copy(); n = int(SR * fade); a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a / np.abs(a).max() * 0.95


def loudest_strike(path, dur=3.6):
    import subprocess, tempfile
    with tempfile.TemporaryDirectory() as d:
        w = Path(d) / "b.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-ac", "2", "-ar", str(SR), str(w)], check=True)
        a, _ = sf.read(w)
    m = np.abs(a).max(1)
    peak = int(np.argmax(m))
    # Anschlag = letzter Punkt vor dem Spitzenwert, an dem der Pegel unter 40 % lag
    i = peak
    while i > 0 and m[max(0, i - 200):i].max() > 0.4 * m[peak]:
        i -= 200
    i = max(0, i - int(SR * 0.06))  # Anschlag vollständig mitnehmen
    a = a[i: i + int(SR * dur)].copy()
    a[:64] *= np.linspace(0, 1, 64)[:, None]
    n = int(SR * 1.2); a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a / np.abs(a).max() * 0.95, i / SR


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    if "--bell" in sys.argv:
        b, t0 = loudest_strike(sys.argv[sys.argv.index("--bell") + 1])
        sf.write(out / "church-bell.wav", b, SR)
        print(f"church-bell.wav: lautester Schlag ab {t0:.2f} s der Quelle")
    if "--choir" in sys.argv:  # hochgeladener Engelschor: erster Anschwellbogen (0–2,6 s)
        sf.write(out / "choir-intro.wav", clip(sys.argv[sys.argv.index("--choir") + 1], 0.0, 2.6), SR)
    for name, y, v in [("sad-trombone", sad_trombone(), 0.85), ("record-scratch", record_scratch(), 0.7), ("crack", crack(), 0.9), ("angel-choir", choir(), 0.85), ("goat", goat(), 0.8), ("creak", creak(), 0.7), ("shimmer", shimmer(), 0.7)]:
        y = fade_out(y * v)
        sf.write(out / f"{name}.wav", np.stack([y, y], 1), SR)
    dur = 2.4
    b = bell(196, dur)                                   # tiefe Glocke G3
    o = organ([146.83, 220.0, 293.66, 349.23], dur) * 0.55  # d-Moll, Orgel
    y = b * 0.85 + o
    y = fade_out(y / np.abs(y).max() * 0.9)
    sf.write(out / "holy-sting.wav", np.stack([y, y], 1), SR)
    h = fade_out(bell(392, 1.3) * 0.85)
    sf.write(out / "bell-hit.wav", np.stack([h, h], 1), SR)
    c = fade_out(coin() * 0.8)
    sf.write(out / "coin.wav", np.stack([c, c], 1), SR)
    print("ok:", *(p.name for p in sorted(out.glob("*.wav"))))


if __name__ == "__main__":
    main()
