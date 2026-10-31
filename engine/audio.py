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


def score(tl):
    S = {s["id"]: s for s in tl["scenes"]}
    C = tl["cues"]
    music, fx = Bus(tl["duration"]), Bus(tl["duration"])

    # Cold open: low drone, distant bells, sparkles
    s = S["kalt"]
    music.add(drone(s["end"] - s["start"] + 1, "D1"), s["start"], 1.0)
    music.add(pad("Dm", s["end"] - s["start"], bright=2, attack=4), s["start"], 0.5)
    melody(music, 1.2, ["A5", None, "F5", None, "E5", None, "D5"], 1.1, 0.3, 4)
    sparkles(music, 0.5, s["end"], 0.8, 0.25)

    # Main title with the leitmotif
    s = S["intro"]
    tl["cues"]["title_hit"] = round(theme(music, fx, s["start"]), 3)

    # Dream world: shimmering major harmonies, music-box leitmotif, choir
    s = S["welt"]
    each = (s["end"] - s["start"]) / 4
    progression(music, s["start"], ["D", "G", "Bm", "A"], each, bright=3, gain=0.85, attack=2.0)
    motif(music, s["start"] + 1.0, (s["end"] - s["start"] - 4) / 13, voice="bell", transpose=12, gain=0.35)
    sparkles(music, s["start"], s["end"], 2.0, 0.3)
    for k in range(4):
        music.add(tone(hz("A5") * [1, 1.5, 1.25, 2][k], 6, 2, 3, 0.02), s["start"] + k * 4.5, 1.0, 0.5 * (-1) ** k)

    # City of lanterns: gentle progression and music box
    s = S["stadt"]
    each = (s["end"] - s["start"]) / 4
    progression(music, s["start"], ["Dm", "Bb", "F", "C"], each, bright=4, gain=0.8)
    mb = ["D5", "F5", "A5", "F5", "D5", "A4", "C5", "D5",
          "D5", "F5", "Bb5", "A5", "F5", "D5", "C5", "Bb4",
          "C5", "F5", "A5", "G5", "F5", "C5", "A4", "C5",
          "E5", "G5", "C6", "G5", "E5", "D5", "C5", "A4"]
    melody(music, s["start"] + 0.3, mb, each / 8, 0.25, 2.2)
    music.add(drone(s["end"] - s["start"], "D1"), s["start"], 0.6)
    last = [l for l in tl["lines"] if l["scene"] == "stadt"][-1]
    fx.add(riser(s["end"] - last["start"] + 0.5), last["start"], 0.5)

    # Falling star: riser, impact, ringing
    rise = C["impact"] - C["streak"]
    fx.add(riser(rise), C["streak"], 0.9)
    fx.add(boom(6, 110, 28, 1.0), C["impact"], 1.3)
    fx.add(drum(45, 3), C["impact"], 1.0)
    fx.add(tone(hz("A6"), 4, 0.01, 3.5, 0.04), C["impact"] + 0.1, 1.0, 0.3)
    s = S["fall"]
    music.add(pad("Asus", s["end"] - C["impact"], bright=3, attack=1.0), C["impact"] + 0.4, 0.6)

    # Ruins: modal tension Dm/Eb, sparkles around the star
    s = S["ruinen"]
    each = (s["end"] - s["start"]) / 4
    progression(music, s["start"], ["Dm", "Eb", "Dm", "Eb"], each, bright=3, gain=0.75, attack=2.5)
    music.add(drone(s["end"] - s["start"] + 1, "D1"), s["start"], 1.0)
    sparkles(music, s["start"] + 3, s["end"], 1.2, 0.3)

    # Bond: swell to the touch, then bright D major
    s = S["bund"]
    music.add(pad("Asus", C["touch"] - s["start"] + 0.2, bright=6, attack=C["touch"] - s["start"] - 0.5), s["start"], 1.0)
    fx.add(riser(C["touch"] - s["start"]), s["start"], 0.5)
    fx.add(boom(5, 95, 30, 0.7), C["touch"], 1.0)
    music.add(pad("D", s["end"] - C["touch"] + 0.5, bright=10, attack=0.08, release=3), C["touch"], 1.2)
    melody(music, C["touch"], ["D6", "A5", "F#5", "D5", "A5", "D6", "F#6", "A6"], 0.18, 0.4, 3)
    sparkles(music, C["touch"], s["end"], 3, 0.35)

    # The Order: war drums, darker progression
    s = S["orden"]
    each = (s["end"] - s["start"]) / 4
    progression(music, s["start"], ["Dm", "Bb", "Gm", "A"], each, bright=7, gain=0.8)
    beat = 60 / 84
    t = s["start"]
    pattern = [1, 0, 0, 1, 1, 0, 1, 0]
    i = 0
    while t < S["kael"]["start"]:
        if pattern[i % 8]:
            fx.add(drum(62 if i % 8 == 0 else 78), t, 0.55 if i % 8 == 0 else 0.35, 0.2 * np.sin(i))
        t += beat / 2
        i += 1
    music.add(drone(s["end"] - s["start"] + 1, "D1", grit=0.3), s["start"], 1.0)

    # Kael: heartbeat pulse under strings
    s = S["kael"]
    each = (s["end"] - s["start"]) / 4
    progression(music, s["start"], ["Dm", "Bb", "F", "A"], each, bright=4, gain=0.75, attack=2.0)
    t = s["start"]
    while t < s["end"]:
        fx.add(drum(48, 0.8), t, 0.35)
        fx.add(drum(48, 0.8), t + 0.32, 0.22)
        t += 1.45

    # Attack: drums accelerate, zap, the fall, then silence
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

    # Farewell: sad progression, sparse piano-like bells
    s = S["abschied"]
    each = (s["end"] - s["start"] - 1.0) / 4
    progression(music, s["start"] + 1.0, ["Bb", "F", "Gm", "Dm"], each, bright=3, gain=0.7, attack=3.0)
    melody(music, s["start"] + 1.5, ["D5", None, "C5", "Bb4", None, "A4", None, None,
                                      "Bb4", None, "A4", "G4", None, "F4", None, None,
                                      "G4", None, "A4", "Bb4", None, "D5", None, None,
                                      "A4", None, None, None, "D4"], each / 7, 0.3, 3.5)

    # Awakening: corrupted drone, black runes, stars going out
    s = S["erwachen"]
    music.add(drone(s["end"] - s["start"] + 1.5, "D1", grit=1.0), s["start"], 1.6)
    music.add(drone(s["end"] - s["start"] + 1.5, "Eb1", grit=0.8), s["start"] + 1.0, 0.9)
    fx.add(riser(C["schwarz"] - s["start"]), s["start"], 0.5)
    fx.add(boom(5, 80, 25, 0.9), C["schwarz"], 1.1)
    t, k = C["erloeschen"], 0
    notes = ["A6", "F6", "D6", "A5", "F5", "D5", "A4", "F4", "D4"]
    while t < s["end"] + 0.4 and k < len(notes):
        fx.add(bell(notes[k], 1.6, 0.4), t, 0.5, (-1) ** k * 0.5)
        fx.add(drum(40, 1.0), t, 0.3)
        t += 0.42
        k += 1

    # The last star: near silence, warm hope under the mother, then the reveal
    s = S["letzter"]
    mother = [l for l in tl["lines"] if l["who"] == "MUTTER"]
    sis = C["schwester"]
    music.add(tone(hz("A5"), sis - s["start"], 2.0, 0.6, 0.035), s["start"], 1.0)
    music.add(pad("D", sis - mother[0]["start"] + 0.6, bright=3, attack=3.0, release=0.4), mother[0]["start"] - 1.0, 0.75)
    motif(music, mother[0]["start"] - 0.5, 0.75, voice="bell", transpose=12, gain=0.25, upto=8)
    fx.add(boom(6, 70, 24, 1.0), sis, 1.3)
    music.add(drone(s["end"] - sis + 2, "Eb1", grit=1.0), sis, 1.5)
    music.add(pad("Eb", s["end"] - sis + 1, bright=5, attack=0.05), sis, 0.7)

    # Revelation: drums and riser build relentlessly
    s = S["ende"]
    music.add(drone(s["end"] - s["start"] + 1, "D1", grit=0.6), s["start"], 1.3)
    progression(music, s["start"], ["Dm", "Bb"], (s["end"] - s["start"]) / 2, bright=8, gain=0.8, attack=0.5)
    fx.add(riser(s["end"] - s["start"]), s["start"], 0.9)
    t, gap = s["start"], 0.5
    while t < s["end"] - 0.1:
        fx.add(drum(60), t, 0.5)
        t += gap
        gap = max(0.13, gap * 0.9)
    fx.add(boom(5, 100, 30, 1.0), s["end"], 1.2)

    # Sting: silence, a heartbeat, Seraphine's order
    s = S["sting"]
    t = s["start"] + 0.3
    while t < s["end"]:
        fx.add(drum(44, 0.8), t, 0.45)
        fx.add(drum(44, 0.8), t + 0.3, 0.3)
        t += 1.2
    music.add(tone(hz("D6") * 1.06, s["end"] - s["start"], 0.5, 0.5, 0.02), s["start"], 1.0)

    # End card: leitmotif reprise, final hit
    s = S["abspann"]
    beat = 0.5
    for i, c in enumerate(["Dm", "Bb"]):
        music.add(pad(c, 4 * beat, bright=8, attack=0.2), s["start"] + i * 4 * beat, 1.0)
    end = motif(music, s["start"], beat, gain=1.1, upto=8)
    ostinato(music, s["start"], end, ["D", "Bb"], beat / 2, 0.5)
    fx.add(boom(6, 100, 28, 1.0), s["start"], 1.0)
    fx.add(boom(6, 110, 26, 1.0), end, 1.3)
    music.add(pad("Dm", 2.0, bright=10, attack=0.03, release=3.0), end, 1.3)
    tl["cues"]["end_hit"] = round(end, 3)
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
    duck = 1 - 0.65 * np.clip(e * 14, 0, 1)
    m = reverb(music.buf, 3.2, 0.45, 1) * duck
    f = reverb(fx.buf, 2.2, 0.25, 2) * (1 - 0.3 * np.clip(e * 14, 0, 1))
    v = np.vstack([voice, voice])
    v = reverb(v, 1.2, 0.06, 3)
    mix = v * 1.0 + m * 0.75 + f * 0.6
    mix = mix[:, :int((tl["duration"] + 0.2) * SR)]
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
