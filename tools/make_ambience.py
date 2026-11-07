#!/usr/bin/env python3
"""Lizenzfreie Südsee-Atmo, komplett im Code erzeugt: rollende Wellen, Brandungsrauschen, Möwen.

  python3 tools/make_ambience.py <ausgabe.wav> <dauer_s> [--duck sprache.wav] [--lufs -30] [--seed 5]
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100


def gull(rng):
    """Ein Möwenruf: 2–4 'kjau'-Silben mit fallender Tonhöhe, Obertönen und leichtem Vibrato."""
    out = []
    for _ in range(rng.integers(2, 5)):
        d = rng.uniform(.18, .32)
        t = np.arange(int(SR * d)) / SR
        f0 = rng.uniform(1500, 2100)
        f = f0 * (1 + .25 * np.exp(-t * 18)) * (1 - .35 * t / d) * (1 + .02 * np.sin(2 * np.pi * 28 * t))
        ph = 2 * np.pi * np.cumsum(f) / SR
        s = np.sin(ph) + .55 * np.sin(2 * ph) + .3 * np.sin(3 * ph) + .12 * np.sin(5 * ph)
        env = np.minimum(1, t / .015) * np.clip((d - t) / .06, 0, 1) * (0.6 + .4 * np.sin(np.pi * t / d))
        out.append(s * env)
        out.append(np.zeros(int(SR * rng.uniform(.04, .12))))
    return np.concatenate(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("duration", type=float)
    ap.add_argument("--duck")
    ap.add_argument("--lufs", type=float, default=-30)
    ap.add_argument("--seed", type=int, default=5)
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    d = a.duration + 1
    with tempfile.TemporaryDirectory() as tmp:
        waves = Path(tmp) / "waves.wav"
        # Wellen: tiefes braunes Rauschen, das alle ~6–7 s anschwillt (Welle rollt an), plus helleres Brandungs-Zischen
        fc = (f"anoisesrc=d={d}:c=brown:a=0.9:seed=3,lowpass=f=700,highpass=f=45,"
              f"volume='0.25+0.75*pow(sin(PI*t/6.6),4)':eval=frame[a];"
              f"anoisesrc=d={d}:c=pink:a=0.5:seed=8,highpass=f=1800,lowpass=f=7000,"
              f"volume='0.05+0.5*pow(sin(PI*(t+0.6)/6.6),8)':eval=frame[b];"
              f"anoisesrc=d={d}:c=brown:a=0.7:seed=11,lowpass=f=500,"
              f"volume='0.2+0.6*pow(sin(PI*(t+3.1)/8.3),4)':eval=frame[c];"
              f"[a][b][c]amix=inputs=3:normalize=0,aformat=channel_layouts=stereo")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", fc,
                        "-t", str(d), "-ar", str(SR), waves], check=True)
        w, _ = sf.read(waves, dtype="float32")
        w = w / (np.max(np.abs(w)) + 1e-9) * .8
        # Möwen: alle 3–7 s ein Ruf, zufällig links/rechts, mit leichtem Echo
        rng = np.random.default_rng(a.seed)
        g = np.zeros_like(w)
        t = rng.uniform(.8, 2.5)
        while t < d - 1.5:
            call = gull(rng) * rng.uniform(.10, .18)
            i = int(t * SR)
            e = min(len(g), i + len(call))
            pan = rng.uniform(.2, .8)
            g[i:e, 0] += call[:e - i] * (1 - pan)
            g[i:e, 1] += call[:e - i] * pan
            t += rng.uniform(3, 7)
        k = int(.11 * SR)
        g[k:] += g[:-k] * .25
        mix = w + g
        raw = Path(tmp) / "raw.wav"
        sf.write(raw, (mix / np.max(np.abs(mix)) * .89)[: int(SR * a.duration)], SR)
        if a.duck:
            fc = ("[1:a]aformat=channel_layouts=stereo,aresample=44100,apad[sc];"
                  "[0:a][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=400:makeup=1[m];"
                  f"[m]loudnorm=I={a.lufs}:TP=-4:LRA=11[o]")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-i", a.duck, "-filter_complex", fc, "-map", "[o]", "-ar", str(SR), out], check=True)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"loudnorm=I={a.lufs}:TP=-4:LRA=11", "-ar", str(SR), out], check=True)
    print(f"Atmo: {out} ({a.duration:.1f} s)")


if __name__ == "__main__":
    main()
