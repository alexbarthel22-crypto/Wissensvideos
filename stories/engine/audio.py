"""Procedural score + sound design for an episode, mixed with the voice track.

Usage: python3 engine/audio.py out/folge01
Reads timeline.json and voice.npy, writes mix.wav (stereo, 48 kHz).
"""
import json
import os
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
rng = np.random.default_rng(7)


def hz(note):
    names = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6,
             "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    name, octave = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[name] + 12 * (octave + 1) - 69) / 12)


CHORDS = {
    "Dm": ["D2", "D3", "F3", "A3", "D4", "F4"],
    "D": ["D2", "D3", "F#3", "A3", "D4", "F#4", "A4"],
    "Bb": ["Bb1", "Bb2", "D3", "F3", "Bb3", "D4"],
    "F": ["F2", "C3", "F3", "A3", "C4", "F4"],
    "C": ["C2", "C3", "E3", "G3", "C4", "E4"],
    "Gm": ["G1", "G2", "D3", "G3", "Bb3", "D4"],
    "A": ["A1", "A2", "E3", "A3", "C#4", "E4"],
    "Asus": ["A1", "A2", "E3", "A3", "D4", "E4"],
    "Eb": ["Eb2", "Eb3", "G3", "Bb3", "Eb4"],
    "G": ["G1", "G2", "D3", "G3", "B3", "D4"],
    "Bm": ["B1", "B2", "F#3", "B3", "D4", "F#4"],
}


class Bus:
    def __init__(self, dur):
        self.buf = np.zeros((2, int(dur * SR) + SR * 6), dtype=np.float32)

    def add(self, sig, t, gain=1.0, pan=0.0):
        if sig.ndim == 1:
            sig = np.vstack([sig * np.sqrt((1 - pan) / 2), sig * np.sqrt((1 + pan) / 2)]) * np.sqrt(2)
        i = int(max(t, 0) * SR)
        n = min(sig.shape[1], self.buf.shape[1] - i)
        if n > 0:
            self.buf[:, i:i + n] += sig[:, :n] * gain


def env(n, attack, release, total=None):
    e = np.ones(n, dtype=np.float32)
    a, r = int(attack * SR), int(release * SR)
    if a:
        e[:a] = np.linspace(0, 1, a) ** 1.5
    if r:
        e[-r:] *= np.linspace(1, 0, r) ** 1.5
    return e


def lowpass(x, f, order=2):
    return sosfilt(butter(order, f, fs=SR, output="sos"), x).astype(np.float32)


def highpass(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x).astype(np.float32)


def pad(chord, dur, bright=4, attack=1.6, release=2.4):
    """Warm detuned string/choir-like pad, stereo."""
    total = dur + release
    t = np.arange(int(total * SR)) / SR
    out = np.zeros((2, len(t)), dtype=np.float32)
    for k, note in enumerate(CHORDS[chord]):
        f0 = hz(note)
        for side, det in ((0, -0.0018), (1, 0.0021)):
            f = f0 * (1 + det + 0.0006 * k)
            vib = 1 + 0.0012 * np.sin(2 * np.pi * (4.6 + 0.3 * k) * t + k)
            phase = 2 * np.pi * f * np.cumsum(vib) / SR
            s = np.zeros_like(t, dtype=np.float32)
            for h in range(1, bright + 1):
                if f * h > 9000:
                    break
                s += np.sin(h * phase + h * k).astype(np.float32) / h ** 1.25
            out[side] += s / (1 + 0.35 * k)
    e = env(len(t), attack, release)
    e[int(dur * SR):] = np.linspace(e[int(dur * SR)], 0, len(t) - int(dur * SR))
    return out * e * 0.11


def bell(note, dur=3.0, bright=1.0):
    t = np.arange(int(dur * SR)) / SR
    f = hz(note) if isinstance(note, str) else note
    s = (np.sin(2 * np.pi * f * t) + 0.45 * bright * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3)
         + 0.25 * bright * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6))
    return (s * np.exp(-t * 1.7) * env(len(t), 0.004, 0.05)).astype(np.float32) * 0.22


def boom(dur=4.0, f0=90, f1=32, noise=0.6):
    t = np.arange(int(dur * SR)) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 7)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.3)
    n = lowpass(rng.standard_normal(len(t)).astype(np.float32), 600) * np.exp(-t * 5) * noise
    return np.tanh(1.6 * (s + n)).astype(np.float32) * 0.9


def drum(f0=70, dur=1.2):
    t = np.arange(int(dur * SR)) / SR
    f = f0 * (0.55 + 0.45 * np.exp(-t * 25))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5.5)
    n = lowpass(rng.standard_normal(len(t)).astype(np.float32), 1800) * np.exp(-t * 30) * 0.5
    return np.tanh(2 * (s + n)).astype(np.float32) * 0.6


def riser(dur):
    t = np.arange(int(dur * SR)) / SR
    n = rng.standard_normal(len(t)).astype(np.float32)
    out = np.zeros_like(n)
    steps = 24
    for i in range(steps):
        a, b = i * len(t) // steps, (i + 1) * len(t) // steps
        fc = 300 * (14000 / 300) ** (i / steps)
        out[a:b] = lowpass(n[max(0, a - 2000):b], fc)[-(b - a):]
    tone = np.sin(2 * np.pi * np.cumsum(110 * 2 ** (3 * t / dur)) / SR) * 0.4
    return ((out * 0.5 + tone) * (t / dur) ** 2.2).astype(np.float32) * 0.5


def zap(dur=1.4):
    t = np.arange(int(dur * SR)) / SR
    f = 2400 * np.exp(-t * 4) + 120
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3 + rng.standard_normal(len(t)) * 0.5
    return (highpass(lowpass(s.astype(np.float32), 7000), 200) * np.exp(-t * 3.5)).astype(np.float32) * 0.6


def tone(f, dur, attack=0.5, release=1.5, amp=0.08):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * f * t) * env(len(t), attack, release) * amp).astype(np.float32)


def drone(dur, root="D1", grit=0.0):
    t = np.arange(int(dur * SR)) / SR
    f = hz(root)
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.003 * t) + 0.25 * np.sin(2 * np.pi * f * 3.01 * t)
    s *= 1 + 0.25 * np.sin(2 * np.pi * 0.13 * t)
    if grit:
        s = np.tanh(s * (1 + 4 * grit))
    return (lowpass(s.astype(np.float32), 900) * env(len(t), 2.0, 2.5) * 0.12).astype(np.float32)


def lead(note, dur, bright=9, attack=0.06, release=0.5):
    """Brass/horn-like lead voice with vibrato, doubled an octave below."""
    total = dur + release
    t = np.arange(int(total * SR)) / SR
    f0 = hz(note)
    out = np.zeros((2, len(t)), dtype=np.float32)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t) * np.clip(t / 0.4, 0, 1)
    for side, det in ((0, -0.002), (1, 0.002)):
        for mult, amp in ((1, 1.0), (0.5, 0.55)):
            ph = 2 * np.pi * f0 * mult * (1 + det) * np.cumsum(vib) / SR
            for h in range(1, bright + 1):
                if f0 * mult * h > 8000:
                    break
                out[side] += amp * np.sin(h * ph).astype(np.float32) / h ** 1.1
    e = env(len(t), attack, release)
    e[int(dur * SR):] = np.linspace(e[int(dur * SR)], 0, len(t) - int(dur * SR))
    swell = 0.75 + 0.25 * np.clip(t / max(dur, 0.1), 0, 1)
    return out * e * swell * 0.05


def ostinato(bus, t0, t1, roots, step, gain=0.5):
    """Driving staccato low strings."""
    t, i = t0, 0
    while t < t1:
        r = roots[int((t - t0) / (step * 8)) % len(roots)]
        note = r + ("2" if i % 2 == 0 else "3")
        bus.add(pad_note(note, step * 0.7, 7), t, gain * (1.0 if i % 4 == 0 else 0.7), 0.3 * (-1) ** i)
        t += step
        i += 1


def pad_note(note, dur, bright):
    t = np.arange(int((dur + 0.15) * SR)) / SR
    f = hz(note)
    s = np.zeros_like(t, dtype=np.float32)
    for h in range(1, bright + 1):
        s += np.sin(2 * np.pi * f * h * t).astype(np.float32) / h
    return s * env(len(t), 0.01, 0.15) * 0.12


# The series' leitmotif: (note, beats)
MOTIF = [("D4", 1), ("A4", 1), ("G4", 0.5), ("F4", 0.5), ("E4", 1), ("F4", 0.5), ("G4", 0.5), ("A4", 2),
         ("Bb4", 1), ("A4", 0.5), ("G4", 0.5), ("F4", 1), ("E4", 1), ("D4", 2)]


def motif(bus, t0, beat, voice="lead", transpose=0, gain=1.0, upto=None):
    t = t0
    names = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    for k, (n, b) in enumerate(MOTIF[:upto]):
        f = hz(n) * 2 ** (transpose / 12)
        midi = int(round(69 + 12 * np.log2(f / 440)))
        note = names[midi % 12] + str(midi // 12 - 1)
        if voice == "lead":
            bus.add(lead(note, b * beat * 0.95), t, gain, 0.1 * np.sin(k))
        else:
            bus.add(bell(note, 2.5 + b, 0.8), t, gain, 0.2 * np.sin(k))
        t += b * beat
    return t


def theme(music, fx, t0, beat=0.6, intro=2.2):
    """Main title: build-up, leitmotif over drums and ostinato, ignition hit."""
    fx.add(riser(intro), t0, 0.7)
    music.add(drone(intro + 10, "D1", grit=0.3), t0, 1.2)
    m0 = t0 + intro
    fx.add(boom(5, 90, 30, 0.9), m0, 1.1)
    fx.add(drum(50, 2), m0, 1.0)
    for i, c in enumerate(["Dm", "Bb", "Gm", "A"]):
        music.add(pad(c, 4 * beat * 0.95 if i < 3 else 1 * beat, bright=7, attack=0.3), m0 + [0, 4, 7, 10][i] * beat, 1.0)
    ostinato(music, m0, m0 + 13 * beat, ["D", "Bb", "G", "A"], beat / 2, 0.55)
    t, i = m0, 0
    while t < m0 + 13 * beat - 0.05:
        if i % 4 in (0, 3) or (i % 8 == 6):
            fx.add(drum(58 if i % 4 == 0 else 72), t, 0.55 if i % 4 == 0 else 0.35, 0.2 * np.sin(i))
        t += beat / 2
        i += 1
    end = motif(music, m0, beat, gain=1.1)
    hit = end - 2 * beat
    fx.add(boom(6, 110, 28, 1.0), hit, 1.3)
    fx.add(drum(46, 3), hit, 1.0)
    music.add(pad("Dm", 2.2, bright=10, attack=0.03, release=3.5), hit, 1.4)
    melody(music, hit, ["D5", "A5", "D6", "F6", "A6"], 0.12, 0.45, 4)
    return hit


def sparkles(bus, t0, t1, density=1.5, gain=0.5):
    notes = ["D6", "F6", "A6", "C7", "E6", "A5", "D7"]
    t = t0
    while t < t1:
        bus.add(bell(notes[rng.integers(len(notes))], 2.0, 0.6), t, gain * rng.uniform(0.3, 1), rng.uniform(-0.8, 0.8))
        t += rng.exponential(1 / density)


def progression(bus, t0, chords, each, bright=4, gain=1.0, attack=1.6):
    for i, c in enumerate(chords):
        bus.add(pad(c, each + 0.3, bright, attack=attack), t0 + i * each, gain)


def melody(bus, t0, notes, step, gain=0.5, length=2.5):
    for i, n in enumerate(notes):
        if n:
            bus.add(bell(n, length, 0.8), t0 + i * step, gain, 0.15 * np.sin(i))


def choir(chord, dur, attack=1.2, release=2.5, vowel="a"):
    """Formant-shaped choir 'aah' on a chord, stereo."""
    formants = {"a": [(800, 80), (1150, 90), (2900, 120)], "o": [(450, 70), (800, 80), (2830, 100)]}[vowel]
    total = dur + release
    t = np.arange(int(total * SR)) / SR
    out = np.zeros((2, len(t)), dtype=np.float32)
    for k, note in enumerate(CHORDS[chord][1:]):
        f0 = hz(note) * (2 if hz(note) < 150 else 1)
        for side in (0, 1):
            for voice in range(3):
                det = 1 + (voice - 1) * 0.0035 + side * 0.0012
                vib = 1 + 0.005 * np.sin(2 * np.pi * (5 + voice * 0.4) * t + voice + k)
                ph = 2 * np.pi * f0 * det * np.cumsum(vib) / SR
                s = np.zeros_like(t, dtype=np.float32)
                for h in range(1, 30):
                    fh = f0 * h
                    if fh > 5000:
                        break
                    amp = sum(np.exp(-((fh - fc) / bw) ** 2 / 2) * (1.0 if i == 0 else 0.6 / i) for i, (fc, bw) in enumerate(formants))
                    if amp > 0.01:
                        s += amp * np.sin(h * ph).astype(np.float32)
                out[side] += s / 3
    e = env(len(t), attack, release)
    e[int(dur * SR):] = np.linspace(e[int(dur * SR)], 0, len(t) - int(dur * SR))
    return out * e * 0.035


def cymbal(dur, swell=False):
    t = np.arange(int(dur * SR)) / SR
    n = highpass(rng.standard_normal(len(t)).astype(np.float32), 5000)
    if swell:
        e = (t / dur) ** 2.5
    else:
        e = np.exp(-t * 1.8) * env(len(t), 0.002, 0.3)
    return np.vstack([n * e, np.roll(n, 997) * e]) * 0.25


def snare_roll(dur, start_amp=0.1):
    t = np.arange(int(dur * SR)) / SR
    out = np.zeros(len(t), dtype=np.float32)
    k, gap = 0.0, 0.11
    while k < dur:
        i = int(k * SR)
        hit = highpass(rng.standard_normal(int(0.12 * SR)).astype(np.float32), 1500) * np.exp(-np.arange(int(0.12 * SR)) / SR * 35)
        n = min(len(hit), len(out) - i)
        out[i:i + n] += hit[:n] * (start_amp + (1 - start_amp) * (k / dur) ** 2)
        k += gap
        gap = max(0.035, gap * 0.95)
    return out * 0.35


def big_bell(note, dur=6.0):
    t = np.arange(int(dur * SR)) / SR
    f = hz(note)
    s = np.zeros_like(t)
    for ratio, amp, dec in ((0.5, 0.6, 0.5), (1, 1.0, 0.8), (1.19, 0.5, 1.2), (1.5, 0.4, 1.5), (2.0, 0.35, 1.8), (2.74, 0.25, 2.5), (3.76, 0.15, 3.5)):
        s += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t * dec)
    s += lowpass(rng.standard_normal(len(t)).astype(np.float32), 3000) * np.exp(-t * 40) * 0.3
    return (s * 0.25).astype(np.float32)


def whale_song(dur, base=180):
    t = np.arange(int(dur * SR)) / SR
    f = base * (1 + 0.45 * np.sin(2 * np.pi * t / dur * 1.5) ** 2 - 0.15 * (t / dur))
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.01 * np.sin(2 * np.pi * 6 * t))) / SR
    s = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    return (lowpass(s.astype(np.float32), 1500) * env(len(t), dur * 0.3, dur * 0.4) * 0.12).astype(np.float32)


def wind(dur, amp=0.1):
    t = np.arange(int(dur * SR)) / SR
    n = rng.standard_normal(len(t)).astype(np.float32)
    s = lowpass(highpass(n, 300), 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.17 * t))
    return (s * env(len(t), 2, 2) * amp).astype(np.float32)


def stab(chord, gain_bus, t, bus, gain=1.0):
    bus.add(pad(chord, 0.25, bright=11, attack=0.01, release=0.6), t, gain)


def epic_intro(music, fx, t0, beat=0.6):
    """Main title: choir swell, crash, leitmotif over drums and ostinato, snare build, title hit."""
    m0 = t0 + 3.0
    music.add(drone(17, "D1", grit=0.4), t0, 1.4)
    music.add(choir("Dm", 3.0, attack=2.6, release=0.6, vowel="o"), t0, 0.9)
    # one continuous swell that starts under the end of the previous scene and carries into the title
    fx.add(cymbal(4.0, swell=True), t0 - 1.0, 0.8)
    fx.add(riser(4.0), t0 - 1.0, 0.6)
    fx.add(boom(6, 100, 28, 1.0), m0, 1.3)
    fx.add(cymbal(4), m0, 1.0)
    for i, (c, at, ln) in enumerate((("Dm", 0, 4), ("Bb", 4, 3), ("Gm", 7, 3), ("A", 10, 3))):
        music.add(choir(c, ln * beat, attack=0.25, release=1.0), m0 + at * beat, 1.0)
        music.add(pad(c, ln * beat * 0.95, bright=7, attack=0.2), m0 + at * beat, 0.8)
    ostinato(music, m0, m0 + 17 * beat, ["D", "Bb", "G", "A"], beat / 2, 0.6)
    t, i = m0, 0
    while t < m0 + 13 * beat - 0.05:
        if i % 4 in (0, 3) or i % 8 == 6:
            fx.add(drum(56 if i % 4 == 0 else 70), t, 0.6 if i % 4 == 0 else 0.4, 0.2 * np.sin(i))
        if i % 8 == 4:
            fx.add(drum(110, 0.5), t, 0.3)
        t += beat / 2
        i += 1
    end = motif(music, m0, beat, gain=1.2)
    # build: snare roll, rising choir, brass stabs
    b0 = end
    fx.add(snare_roll(4 * beat), b0, 0.9)
    fx.add(cymbal(4 * beat, swell=True), b0, 0.7)
    for k, c in enumerate(["Bb", "C", "Asus", "A"]):
        music.add(choir(c, beat * 0.95, attack=0.05, release=0.3), b0 + k * beat, 1.0)
        stab(c, None, b0 + k * beat, music, 1.0)
        fx.add(drum(60), b0 + k * beat, 0.6)
    hit = b0 + 4 * beat
    fx.add(boom(7, 110, 26, 1.0), hit, 1.5)
    fx.add(cymbal(5), hit, 1.2)
    fx.add(drum(44, 3), hit, 1.0)
    music.add(choir("Dm", 2.5, attack=0.03, release=3.5), hit, 1.5)
    music.add(pad("Dm", 2.5, bright=11, attack=0.02, release=3.5), hit, 1.3)
    music.add(lead("D4", 2.5), hit, 1.0)
    music.add(lead("A4", 2.5), hit, 0.8)
    melody(music, hit, ["D5", "A5", "D6", "F6", "A6"], 0.1, 0.45, 4)
    return hit


def squeak(n=2, base=2600, gap=0.11, seed=0):
    """Tiny, cute squeak of the moon mouse."""
    r = np.random.default_rng(seed)
    out = np.zeros(int((n * gap + 0.2) * SR), dtype=np.float32)
    for k in range(n):
        d = 0.08 + 0.03 * r.random()
        t = np.arange(int(d * SR)) / SR
        f = base * (1 + 0.15 * r.random()) * (1 + 0.5 * t / d) * (1 + 0.03 * np.sin(2 * np.pi * 40 * t))
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2
        i = int(k * gap * SR)
        out[i:i + len(x)] += x.astype(np.float32) * 0.25
    return out


def epic_outro(music, fx, t0, t1):
    """Distinct closing theme: heroic I-V-vi-IV in F, soaring strings, turning to D major with the motif's head.
    Everything resolves and decays before t1, so nothing is cut off at the end of the video."""
    beat = 0.62
    prog = ["F", "C", "Dm", "Bb"]
    for k, c in enumerate(prog):
        music.add(pad(c, 4 * beat, bright=6, attack=0.6, release=1.2), t0 + k * 4 * beat, 0.9)
        music.add(choir(c, 4 * beat, attack=0.8, release=1.2), t0 + k * 4 * beat, 0.7)
    arp = {"F": ["F4", "A4", "C5", "A4"], "C": ["C4", "E4", "G4", "E4"], "Dm": ["D4", "F4", "A4", "F4"], "Bb": ["Bb3", "D4", "F4", "D4"]}
    for k, c in enumerate(prog):
        for j in range(8):
            music.add(bell(arp[c][j % 4], 1.6, 0.6), t0 + k * 4 * beat + j * beat / 2, 0.22, 0.3 * (-1) ** j)
    fin = t0 + 16 * beat
    tune = [("A4", 2), ("C5", 1), ("F5", 1), ("E5", 2), ("D5", 1), ("C5", 1)]
    tt = t0 + 8 * beat
    for n, bts in tune:
        music.add(lead(n, bts * beat * 0.95, bright=6, attack=0.15, release=0.3), tt, 0.8)
        tt += bts * beat
    t = t0 + 8 * beat
    while t < fin - 2 * beat:
        fx.add(drum(58), t, 0.45)
        fx.add(drum(72), t + beat * 1.5, 0.3)
        t += 2 * beat
    fx.add(snare_roll(2 * beat), fin - 2 * beat, 0.7)
    fx.add(boom(5, 100, 26, 1.0), fin, 1.2)
    fx.add(cymbal(4), fin, 0.9)
    hold = max(2.0, t1 - fin - 2.4)
    music.add(choir("D", hold, attack=0.05, release=2.2), fin, 1.3)
    music.add(pad("D", hold, bright=10, attack=0.05, release=2.2), fin, 1.1)
    th = fin
    for n, bts in [("D4", 1), ("A4", 1), ("G4", 0.5), ("F#4", 0.5), ("A4", 3)]:
        music.add(lead(n, bts * 0.6 * 0.95, release=0.6), th, 1.1)
        th += bts * 0.6
    return fin


def score(tl):
    S = {s["id"]: s for s in tl["scenes"]}
    C = tl["cues"]
    LN = lambda sc, i: [l for l in tl["lines"] if l["scene"] == sc][i]
    music, fx = Bus(tl["duration"]), Bus(tl["duration"])
    dur = lambda sc: S[sc]["end"] - S[sc]["start"]

    # Cold open
    if "kalt" in S:
        s = S["kalt"]
        music.add(drone(dur("kalt") + 1, "D1"), s["start"], 1.0)
        music.add(pad("Dm", dur("kalt"), bright=2, attack=4), s["start"], 0.5)
        melody(music, 1.2, ["A5", None, "F5", None, "E5", None, "D5"], 1.2, 0.3, 4)
        sparkles(music, 0.5, s["end"], 0.8, 0.25)
        kl = [l for l in tl["lines"] if l["scene"] == "kalt"]
        if "ex_hit" in C:
            # the hook line: a whoosh that lands with a hit and a crash right when the text slams in
            fx.add(boom(5, 100, 28, 0.8), 0.0, 0.8)
            fx.add(cymbal(3), 0.0, 0.5)
            fx.add(tone(hz("A6"), 2.5, 0.01, 2.2, 0.04), 0.03, 1.0, 0.3)
        if "frage" in C:
            fx.add(bell("A5", 2.0, 0.8), C["frage"], 0.3, -0.3)
            fx.add(bell("E6", 2.0, 0.8), C["frage"] + 0.12, 0.25, 0.3)
        invite = kl[-1]["start"] if len(kl) >= 5 else s["end"]
        t = s["start"] + 0.4
        while t < invite - 0.6:
            fx.add(drum(48, 0.7), t, 0.32)
            fx.add(drum(48, 0.7), t + 0.28, 0.2)
            fx.add(bell("A6", 0.25, 0.2), t + 0.7, 0.08, 0.5)
            t += 1.4
        if len(kl) >= 5:
            music.add(pad("D", s["end"] - invite + 2.5, bright=5, attack=1.5, release=2.0), invite - 0.3, 0.8)
            music.add(choir("D", s["end"] - invite + 2, attack=1.8, release=2.0, vowel="o"), invite, 0.45)
        else:
            fx.add(boom(4, 70, 26, 0.6), kl[-1]["end"] + 0.1, 0.7)

    # Main title
    if "intro" in S:
        C["title_hit"] = round(epic_intro(music, fx, S["intro"]["start"]), 3)

    # Valdoria: dreamy, whale song, music-box leitmotif
    if "welt" in S:
        s = S["welt"]
        each = dur("welt") / 6
        progression(music, s["start"], ["D", "G", "Bm", "A", "G", "D"], each, bright=3, gain=0.85, attack=2.0)
        music.add(choir("D", dur("welt") - 2, attack=4, release=3, vowel="o"), s["start"] + 1, 0.35)
        motif(music, s["start"] + 2.0, 0.85, voice="bell", transpose=12, gain=0.3)
        sparkles(music, s["start"], s["end"], 1.5, 0.28)
        wl = LN("welt", 2)
        for k, base in enumerate((170, 210, 150)):
            music.add(whale_song(6, base), wl["start"] - 1 + k * 3.2, 1.0, 0.5 * (-1) ** k)
        music.add(wind(dur("welt"), 0.05), s["start"], 1.0)

    # Aurelion in the treetops
    if "stadt" in S:
        s = S["stadt"]
        each = dur("stadt") / 4
        progression(music, s["start"], ["Dm", "Bb", "F", "C"], each, bright=4, gain=0.8)
        mb = ["D5", "F5", "A5", "F5", "D5", "A4", "C5", "D5", "D5", "F5", "Bb5", "A5", "F5", "D5", "C5", "Bb4",
              "C5", "F5", "A5", "G5", "F5", "C5", "A4", "C5", "E5", "G5", "C6", "G5", "E5", "D5", "C5", "A4"]
        melody(music, s["start"] + 0.3, mb, each / 8, 0.24, 2.2)
        music.add(drone(dur("stadt"), "D1"), s["start"], 0.6)

    # The Order of the High Flame: solemn choir and organ
    if "lichtkrone" in S:
        s = S["lichtkrone"]
        kl = [l for l in tl["lines"] if l["scene"] == "lichtkrone"]
        burn = kl[4] if len(kl) > 4 else None
        quiet = (burn["start"] - 0.9) if burn else s["end"]
        each = (quiet - s["start"]) / 4
        for i, c in enumerate(["Dm", "Gm", "A", "Dm"]):
            music.add(choir(c, each + 0.3, attack=1.5, release=0.8 if i == 3 else 2.0), s["start"] + i * each, 0.8)
            music.add(pad(c, each + 0.3, bright=6, attack=1.0, release=0.8 if i == 3 else 2.4), s["start"] + i * each, 0.6)
        music.add(drone(quiet - s["start"] + 0.5, "D1"), s["start"], 1.0)
        if burn:
            hit = burn["start"] + (burn["end"] - burn["start"]) * 0.55
            fx.add(boom(6, 80, 24, 1.0), hit, 1.2)
            fx.add(drum(42, 2.5), hit, 1.0)
            fx.add(cymbal(4), hit, 0.6)
            stab("Eb", None, hit, music, 1.1)
            music.add(drone(s["end"] - hit + 1.5, "Eb1", grit=1.0), hit, 1.2)
            music.add(choir("Dm", s["end"] - hit + 1, attack=0.05, release=1.5, vowel="o"), hit, 0.8)
        else:
            b = kl[3]
            fx.add(boom(5, 80, 26, 0.9), b["end"] - 0.4, 1.0)
            music.add(drone(3, "Eb1", grit=1.0), b["end"] - 0.4, 1.3)

    # Seraphine: ominous hall, heartbeat
    if "seraphine_vor" in S:
        s = S["seraphine_vor"]
        music.add(drone(dur("seraphine_vor") + 1, "D1", grit=0.4), s["start"], 1.2)
        music.add(choir("Eb", 6, attack=2, release=3, vowel="o"), s["start"] + 2, 0.6)
        music.add(choir("Dm", dur("seraphine_vor") - 8, attack=2, release=3, vowel="o"), s["start"] + 8, 0.6)
        t = s["start"] + 1
        while t < s["end"]:
            fx.add(drum(46, 0.8), t, 0.3)
            fx.add(drum(46, 0.8), t + 0.32, 0.2)
            t += 1.6
        fx.add(big_bell("D3", 7), LN("seraphine_vor", 1)["start"] - 0.6, 0.6)

    # Lunara's theme: hopeful and fragile
    if "lunara" in S:
        s = S["lunara"]
        ll = [l for l in tl["lines"] if l["scene"] == "lunara"]
        arp = {"F": ["F4", "A4", "C5", "A4"], "C": ["C4", "E4", "G4", "E4"], "Dm": ["D4", "F4", "A4", "F4"], "Bb": ["Bb3", "D4", "F4", "D4"], "A": ["A3", "C#4", "E4", "C#4"], "Gm": ["G3", "Bb3", "D4", "Bb3"]}
        bo = next((l for l in ll if l["who"] == "BO"), None)
        sad0 = ll[5]["start"] - 0.4 if bo else s["start"] + dur("lunara") / 2
        happy = ["F", "C", "Dm", "Bb"]
        each = (sad0 - s["start"]) / len(happy)
        progression(music, s["start"], happy, each, bright=4, gain=0.7, attack=1.5)
        for k, c in enumerate(happy):
            for j in range(8):
                tt = s["start"] + k * each + j * each / 8
                if bo and bo["start"] - 0.5 < tt < bo["end"] + 0.3:
                    continue
                music.add(bell(arp[c][j % 4], 1.6, 0.6), tt, 0.16, 0.3 * (-1) ** j)
        if bo:
            # comic pizzicato: short, bouncy plucks while Bo grumbles
            notes = ["C5", "G4", "C5", "E5", "D5", "B4", "G4", "C5", "G5", "C5"]
            step = (bo["end"] - bo["start"] + 0.4) / len(notes)
            for j, n in enumerate(notes):
                music.add(bell(n, 0.35, 1.4), bo["start"] - 0.2 + j * step, 0.3, 0.5 * (-1) ** j)
            fx.add(bell("C7", 0.3, 0.3), bo["end"] + 0.2, 0.12)
        # the mother: sparse, minor, a soft choir
        sad = ["Dm", "Bb", "Gm", "A"]
        each2 = (s["end"] - sad0) / len(sad)
        for k, c in enumerate(sad):
            music.add(pad(c, each2 + 0.4, bright=2, attack=2.0), sad0 + k * each2, 0.55)
            music.add(choir(c, each2, attack=2.0, release=2.0, vowel="o"), sad0 + k * each2, 0.3)
            for j in range(3):
                music.add(bell(arp[c][j], 2.4, 0.35), sad0 + k * each2 + j * each2 / 3, 0.12, 0.25 * (-1) ** j)
        motif(music, ll[-2]["start"], 0.75, voice="bell", transpose=12, gain=0.24, upto=8)

    # Kael: nostalgic strings, then cold
    if "kael_vor" in S:
        s = S["kael_vor"]
        cold = LN("kael_vor", 4)["start"]
        each = (cold - s["start"]) / 4
        progression(music, s["start"], ["Bb", "F", "Gm", "Dm"], each, bright=3, gain=0.75, attack=2.0)
        m = LN("kael_vor", 3)
        music.add(tone(hz("D6"), m["end"] - m["start"] + 2, 0.5, 1.5, 0.02), m["start"] - 0.5, 1.0)
        progression(music, cold, ["Dm", "Eb"], (s["end"] - cold) / 2, bright=5, gain=0.7, attack=1.0)
        music.add(drone(s["end"] - cold + 1, "D1", grit=0.3), cold, 1.0)

    # Falling star: trembling pendant, riser, impact
    if "fall" in S:
        s = S["fall"]
        music.add(drone(dur("fall"), "D1", grit=0.5), s["start"], 1.2)
        t = s["start"] + 1.5
        while t < C["impact"]:
            fx.add(bell("A6", 0.4, 0.3), t, 0.25, 0.4)
            t += max(0.08, 0.35 * (C["impact"] - t) / (C["impact"] - s["start"]))
        fx.add(riser(C["impact"] - C["streak"] + 1.5), C["streak"] - 1.5, 1.0)
        fx.add(boom(6, 110, 28, 1.0), C["impact"], 1.3)
        fx.add(drum(45, 3), C["impact"], 1.0)
        fx.add(cymbal(4), C["impact"], 0.8)
        fx.add(tone(hz("A6"), 4, 0.01, 3.5, 0.04), C["impact"] + 0.1, 1.0, 0.3)
        music.add(pad("Asus", s["end"] - C["impact"] + 1, bright=3, attack=1.0), C["impact"] + 0.4, 0.6)

    # Forbidden ruins: wind among stone trees, modal tension
    if "ruinen" in S:
        s = S["ruinen"]
        each = dur("ruinen") / 6
        progression(music, s["start"], ["Dm", "Eb", "Dm", "Eb", "Dm", "Eb"], each, bright=3, gain=0.7, attack=2.5)
        music.add(drone(dur("ruinen") + 1, "D1"), s["start"], 1.0)
        music.add(wind(dur("ruinen"), 0.08), s["start"], 1.0)
        sparkles(music, LN("ruinen", 4)["start"] - 1, s["end"], 1.2, 0.3)

    # Bond
    if "bund" in S:
        s = S["bund"]
        music.add(pad("Asus", C["touch"] - s["start"] + 0.2, bright=6, attack=C["touch"] - s["start"] - 0.5), s["start"], 1.0)
        music.add(choir("Asus", C["touch"] - s["start"], attack=C["touch"] - s["start"] - 0.3, release=0.3), s["start"], 0.8)
        fx.add(riser(C["touch"] - s["start"]), s["start"], 0.5)
        fx.add(boom(5, 95, 30, 0.7), C["touch"], 1.0)
        fx.add(cymbal(4), C["touch"], 0.7)
        music.add(pad("D", s["end"] - C["touch"] + 0.5, bright=10, attack=0.08, release=3), C["touch"], 1.2)
        music.add(choir("D", s["end"] - C["touch"], attack=0.1, release=3), C["touch"], 1.0)
        melody(music, C["touch"], ["D6", "A5", "F#5", "D5", "A5", "D6", "F#6", "A6"], 0.18, 0.4, 3)
        sparkles(music, C["touch"], s["end"], 3, 0.35)

    # Alarm bells of the High Flame
    if "glocken" in S:
        s = S["glocken"]
        t, k = C["glocke"], 0
        while t < s["end"] + 1:
            fx.add(big_bell(["D3", "A2"][k % 2], 5), t, 0.9 - 0.3 * (k % 2), 0.4 * (-1) ** k)
            t += 1.5
            k += 1
        music.add(drone(dur("glocken") + 1, "D1", grit=0.6), s["start"], 1.3)
        t, gap = s["start"] + 4, 0.6
        while t < s["end"]:
            fx.add(drum(62), t, 0.45)
            t += gap
            gap = max(0.25, gap * 0.97)
        fx.add(riser(6), s["end"] - 6, 0.6)

    # The Order arrives: war drums, brass; horror stab on "eine ganze Welt verbrannt"
    if "orden" in S:
        s = S["orden"]
        each = dur("orden") / 4
        progression(music, s["start"], ["Dm", "Bb", "Gm", "A"], each, bright=7, gain=0.8)
        beat = 60 / 84
        t, i = s["start"], 0
        while t < s["end"]:
            if [1, 0, 0, 1, 1, 0, 1, 0][i % 8]:
                fx.add(drum(62 if i % 8 == 0 else 78), t, 0.5 if i % 8 == 0 else 0.32, 0.2 * np.sin(i))
            t += beat / 2
            i += 1
        horror = LN("orden", 2)
        stab("Eb", None, horror["start"] + 0.2, music, 1.3)
        fx.add(boom(4, 90, 30, 0.8), horror["start"] + 0.2, 0.9)
        music.add(drone(dur("orden") + 1, "D1", grit=0.3), s["start"], 1.0)

    # Kael: heartbeat; the desperate refusal swells
    if "kael" in S:
        s = S["kael"]
        each = dur("kael") / 6
        progression(music, s["start"], ["Dm", "Bb", "F", "A", "Dm", "Bb"], each, bright=4, gain=0.75, attack=2.0)
        t = s["start"]
        while t < s["end"]:
            fx.add(drum(48, 0.8), t, 0.35)
            fx.add(drum(48, 0.8), t + 0.32, 0.22)
            t += 1.45
        cries = [l for l in tl["lines"] if l["scene"] == "kael" and l["who"] == "KAEL" and "nicht!" in l["text"]]
        for cry in cries:
            music.add(choir("Bb", cry["end"] - cry["start"] + 2, attack=0.6, release=2), cry["start"] - 0.3, 1.0)

    # Attack
    if "angriff" in S:
        s = S["angriff"]
        t, gap = s["start"], 0.42
        while t < C["fallen"] - 0.2:
            fx.add(drum(70), t, 0.5)
            t += gap
            gap = max(0.14, gap * 0.94)
        music.add(pad("Eb", C["fallen"] - s["start"], bright=8, attack=2.5, release=0.3), s["start"], 1.0)
        fx.add(zap(), C["bolt"], 1.0)
        fx.add(boom(3, 120, 40, 0.8), C["bolt"] + 0.05, 0.7)
        fx.add(boom(7, 100, 26, 1.0), C["fallen"], 1.4)
        fx.add(tone(3400, 3.5, 0.02, 3.2, 0.025), C["fallen"] + 0.2, 1.0)

    # Farewell
    if "abschied" in S:
        s = S["abschied"]
        each = (dur("abschied") - 1.0) / 6
        progression(music, s["start"] + 1.0, ["Bb", "F", "Gm", "Dm", "Bb", "A"], each, bright=3, gain=0.7, attack=3.0)
        music.add(choir("Dm", dur("abschied") - 4, attack=5, release=3, vowel="o"), s["start"] + 3, 0.4)
        melody(music, s["start"] + 1.5, ["D5", None, "C5", "Bb4", None, "A4", None, None,
                                          "Bb4", None, "A4", "G4", None, "F4", None, None,
                                          "G4", None, "A4", "Bb4", None, "D5", None, None,
                                          "A4", None, None, None, "D4"], each / 5, 0.28, 3.5)

    # Awakening
    if "erwachen" in S:
        s = S["erwachen"]
        music.add(drone(dur("erwachen") + 1.5, "D1", grit=1.0), s["start"], 1.6)
        music.add(drone(dur("erwachen") + 1.5, "Eb1", grit=0.8), s["start"] + 1.0, 0.9)
        fx.add(riser(C["schwarz"] - s["start"]), s["start"], 0.5)
        fx.add(boom(5, 80, 25, 0.9), C["schwarz"], 1.1)
        t, k = C["erloeschen"], 0
        notes = ["A6", "F6", "D6", "A5", "F5", "D5", "A4", "F4", "D4"]
        while t < s["end"] + 0.4 and k < len(notes):
            fx.add(bell(notes[k], 1.6, 0.4), t, 0.5, (-1) ** k * 0.5)
            fx.add(drum(40, 1.0), t, 0.3)
            t += 0.5
            k += 1
        music.add(whale_song(4, 140), LN("erwachen", 2)["end"] - 3.5, 0.8)

    # Last star
    if "letzter" in S:
        s = S["letzter"]
        mother = [l for l in tl["lines"] if l["who"] == "MUTTER"]
        sis = C["schwester"]
        music.add(tone(hz("A5"), sis - s["start"], 2.0, 0.6, 0.035), s["start"], 1.0)
        music.add(pad("D", sis - mother[0]["start"] + 0.6, bright=3, attack=3.0, release=0.4), mother[0]["start"] - 1.0, 0.75)
        motif(music, mother[0]["start"] - 0.5, 0.75, voice="bell", transpose=12, gain=0.25, upto=8)
        fx.add(boom(6, 70, 24, 1.0), sis, 1.3)
        music.add(drone(s["end"] - sis + 2, "Eb1", grit=1.0), sis, 1.5)
        music.add(pad("Eb", s["end"] - sis + 1, bright=5, attack=0.05), sis, 0.7)

    # Revelation
    if "ende" in S:
        s = S["ende"]
        music.add(drone(dur("ende") + 1, "D1", grit=0.6), s["start"], 1.3)
        progression(music, s["start"], ["Dm", "Bb"], dur("ende") / 2, bright=8, gain=0.8, attack=0.5)
        music.add(choir("Dm", dur("ende"), attack=1.5, release=0.5), s["start"], 0.8)
        fx.add(riser(dur("ende")), s["start"], 0.9)
        t, gap = s["start"], 0.5
        while t < s["end"] - 0.1:
            fx.add(drum(60), t, 0.5)
            t += gap
            gap = max(0.13, gap * 0.9)
        fx.add(boom(5, 100, 30, 1.0), s["end"], 1.2)

    # Sting
    if "sting" in S:
        s = S["sting"]
        t = s["start"] + 0.3
        while t < s["end"]:
            fx.add(drum(44, 0.8), t, 0.45)
            fx.add(drum(44, 0.8), t + 0.3, 0.3)
            t += 1.2
        music.add(tone(hz("D6") * 1.06, dur("sting"), 0.5, 0.5, 0.02), s["start"], 1.0)

    # Previously on: the leitmotif as a fragile memory, darkening toward the Order
    if "rueckblick" in S:
        s = S["rueckblick"]
        last = LN("rueckblick", 3)
        progression(music, s["start"], ["D", "Bm", "G", "A"], (last["start"] - s["start"]) / 4, bright=3, gain=0.7, attack=1.5)
        motif(music, s["start"] + 0.8, 0.7, voice="bell", transpose=12, gain=0.25, upto=8)
        sparkles(music, s["start"], last["start"], 1.2, 0.25)
        touch = LN("rueckblick", 2)
        fx.add(boom(4, 95, 30, 0.6), touch["start"] - 0.1, 0.8)
        music.add(drone(s["end"] - last["start"] + 1, "D1", grit=0.6), last["start"] - 0.5, 1.2)
        music.add(pad("Dm", s["end"] - last["start"] + 0.5, bright=6, attack=0.8), last["start"] - 0.3, 0.8)
        t = last["start"]
        while t < s["end"]:
            fx.add(drum(62), t, 0.4)
            t += 0.5

    # The blade: time slows, heartbeat races, everything rises toward the strike
    if "klinge" in S:
        s = S["klinge"]
        hit = C["hieb"]
        music.add(drone(hit - s["start"] + 0.5, "D1", grit=0.8), s["start"], 1.4)
        music.add(pad("Bb", (hit - s["start"]) / 2 + 0.5, bright=4, attack=2.0), s["start"], 0.7)
        music.add(pad("Eb", (hit - s["start"]) / 2, bright=7, attack=2.0, release=0.2), s["start"] + (hit - s["start"]) / 2, 0.8)
        music.add(choir("Dm", hit - s["start"], attack=4, release=0.2, vowel="o"), s["start"], 0.6)
        music.add(tone(hz("D6") * 1.06, hit - s["start"], 3.0, 0.05, 0.03), s["start"], 1.0)
        t, gap = s["start"] + 0.2, 1.1
        while t < hit - 0.15:
            fx.add(drum(46, 0.8), t, 0.45)
            fx.add(drum(46, 0.8), t + min(0.3, gap * 0.3), 0.3)
            t += gap
            gap = max(0.32, gap * 0.93)
        fx.add(riser(5), hit - 5, 0.8)
        fx.add(tone(4200, 1.2, 0.01, 1.1, 0.03), hit - 0.5, 1.0, 0.4)

    # Cut to black: almost silence, then the scream that ends the episode
    if "nacht" in S:
        s = S["nacht"]
        fx.add(boom(7, 120, 26, 1.0), s["start"], 1.4)
        fx.add(cymbal(5), s["start"], 0.6)
        music.add(tone(hz("A5"), dur("nacht"), 0.1, 2.0, 0.02), s["start"] + 0.2, 1.0)
        music.add(drone(dur("nacht") + 1, "D1", grit=0.3), s["start"] + 1.0, 0.8)
        t = s["start"] + 1.5
        while t < C["schrei"] - 0.5:
            fx.add(drum(42, 1.0), t, 0.3)
            fx.add(drum(42, 1.0), t + 0.35, 0.2)
            t += 1.6
        stab("Eb", None, C["schrei"], music, 1.3)
        fx.add(boom(5, 90, 28, 1.0), C["schrei"], 1.2)

    # The moon mouse
    for name, n, base in (("maus_hallo", 3, 2800), ("hicks", 1, 3400), ("schreck", 2, 3600), ("knopf", 2, 3000)):
        if name in C:
            fx.add(squeak(n, base, seed=len(name)), C[name], 0.9, 0.2)
            if name == "hicks":
                fx.add(bell("E7", 0.8, 0.2), C[name] + 0.05, 0.25)

    # Outro
    if "outro" in S:
        s = S["outro"]
        C["outro_hit"] = round(epic_outro(music, fx, s["start"] + 0.2, s["end"]), 3)
    return music, fx


def reverb(x, seconds, wet, seed):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    decay = np.exp(-np.arange(n) / SR * 6.9 / seconds)
    out = np.empty_like(x)
    for ch in range(2):
        ir = r.standard_normal(n) * decay
        ir = lowpass(ir.astype(np.float32), 5000)
        ir /= np.sqrt(np.sum(ir ** 2))
        out[ch] = fftconvolve(x[ch], ir)[:x.shape[1]]
    return x * (1 - wet) + out * wet * 1.6


def main(out_dir):
    tl = json.load(open(os.path.join(out_dir, "timeline.json")))
    voice = np.load(os.path.join(out_dir, "voice.npy"))
    music, fx = score(tl)
    json.dump(tl, open(os.path.join(out_dir, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    n = music.buf.shape[1]
    voice = np.pad(voice, (0, max(0, n - len(voice))))[:n]

    # Duck the music under dialogue
    e = np.abs(voice)
    k = int(0.25 * SR)
    e = np.convolve(e, np.ones(k) / k, mode="same")
    duck = 1 - 0.75 * np.clip(e * 14, 0, 1)
    m = reverb(music.buf, 3.2, 0.45, 1) * duck
    f = reverb(fx.buf, 2.2, 0.25, 2) * (1 - 0.3 * np.clip(e * 14, 0, 1))
    v = np.vstack([voice, voice])
    v = reverb(v, 1.2, 0.06, 3)
    mix = v * 1.0 + m * 0.36 + f * 0.4
    mix = mix[:, :int((tl["duration"] + 0.2) * SR)]
    # gentle master fade so the last chord never stops abruptly
    nf = int(1.5 * SR)
    mix[:, -nf:] *= np.linspace(1, 0, nf) ** 1.5
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    mix /= max(1e-6, np.abs(mix).max()) / 0.95
    pcm = (mix.T * 32767).astype(np.int16)
    with wave.open(os.path.join(out_dir, "mix.wav"), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("mix.wav", pcm.shape[0] / SR, "s")


if __name__ == "__main__":
    main(sys.argv[1])
