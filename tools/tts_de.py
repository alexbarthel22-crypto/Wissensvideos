#!/usr/bin/env python3
"""Deutsche Sprachspur + Wort-Timings aus script.json.

Erzeugt <projekt>/assets/voice/narration.wav und <projekt>/assets/voice/timings.json.

Backends:
  coqui  – Thorsten VITS (22 kHz, natürlicher), braucht das coqui-venv
  piper  – Piper-Stimmen (16 kHz), schneller Fallback

Wort-Timings: Piper/Coqui liefern keine Wortzeiten. Jede Zeile wird einzeln
synthetisiert; Pausen in der Zeile werden per Energie erkannt und den
Satzzeichen zugeordnet, innerhalb eines Abschnitts wird nach Silben verteilt.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

CACHE = Path(os.environ.get("TIKTOK_CACHE", Path.home() / ".cache" / "tiktok-tts"))
SR = 44100
GAP_LINE = 0.28      # Pause zwischen Zeilen derselben Szene
GAP_SCENE = 0.45     # Pause zwischen Szenen
LEAD_IN = 0.25       # Stille am Anfang
COLOR_RE = re.compile(r"^\*([yrpgb]):")
PUNCT_RE = re.compile(r"[,.;:?!…]+[\"“”]?$")


def parse_tokens(text):
    """'*y:19.|neunzehnten' -> {display, spoken, color, group}."""
    words, group = [], 0
    for raw in text.split():
        if raw == "/":
            group += 1
            continue
        color = None
        m = COLOR_RE.match(raw)
        if m:
            color, raw = m.group(1), raw[m.end():]
        display, _, spoken = raw.partition("|")
        spoken = spoken or display
        words.append({
            "display": display.replace("_", " "),
            "spoken": spoken.replace("_", " ").replace("-", " ") if "|" in raw else spoken.replace("_", " "),
            "color": color,
            "group": group,
        })
    return words


def syllables(word):
    w = re.sub(r"[^a-zäöüß]", "", word.lower())
    n = len(re.findall(r"[aeiouäöüy]+", w))
    return max(1, n) + len(w) * 0.04


def synth_piper(texts, voice_dir):
    from piper import PiperVoice
    model = next(Path(voice_dir).glob("*.onnx"))
    voice = PiperVoice.load(str(model))
    out = []
    for t in texts:
        chunks = [c.audio_float_array for c in voice.synthesize(t)]
        out.append((np.concatenate(chunks), voice.config.sample_rate))
    return out


def synth_coqui(texts, model_dir, python):
    """Läuft im separaten venv; schreibt WAVs in ein Temp-Verzeichnis."""
    tmp = Path(tempfile.mkdtemp())
    (tmp / "lines.json").write_text(json.dumps(texts, ensure_ascii=False))
    code = f"""
import json
from TTS.api import TTS
texts = json.load(open({str(tmp / 'lines.json')!r}))
tts = TTS(model_path={str(Path(model_dir) / 'model_file.pth')!r}, config_path={str(Path(model_dir) / 'config.json')!r})
for i, t in enumerate(texts):
    tts.tts_to_file(text=t, file_path={str(tmp)!r} + f'/{{i:03d}}.wav')
"""
    subprocess.run([python, "-c", code], check=True)
    out = []
    for i in range(len(texts)):
        a, sr = sf.read(tmp / f"{i:03d}.wav", dtype="float32")
        out.append((a, sr))
    return out


def resample(audio, sr):
    if sr == SR:
        return audio
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "a.wav", Path(d) / "b.wav"
        sf.write(src, audio, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ar", str(SR), "-ac", "1", dst], check=True)
        a, _ = sf.read(dst, dtype="float32")
    return a


def trim(audio, thresh=0.012):
    idx = np.where(np.abs(audio) > thresh)[0]
    if len(idx) == 0:
        return audio
    a, b = max(0, idx[0] - int(0.02 * SR)), min(len(audio), idx[-1] + int(0.06 * SR))
    return audio[a:b]


def pauses(audio, min_len=0.11, thresh_db=-38):
    """Stille-Abschnitte innerhalb der Zeile: [(start, end), ...] in Sekunden."""
    hop = int(0.01 * SR)
    frames = len(audio) // hop
    rms = np.array([np.sqrt(np.mean(audio[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(frames)])
    silent = 20 * np.log10(rms + 1e-9) < thresh_db
    res, start = [], None
    for i, s in enumerate(silent):
        if s and start is None:
            start = i
        elif not s and start is not None:
            if (i - start) * 0.01 >= min_len and start > 3:
                res.append((start * 0.01, i * 0.01))
            start = None
    return res


def word_times(words, duration, audio):
    """Verteilt die Wörter auf die Sprechabschnitte zwischen den Pausen."""
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if PUNCT_RE.search(w["display"]) and i < len(words) - 1:
            chunks.append(cur)
            cur = []
    chunks.append(cur)
    gaps = sorted(pauses(audio), key=lambda p: p[1] - p[0], reverse=True)[: len(chunks) - 1]
    gaps = sorted(gaps)
    if len(gaps) == len(chunks) - 1:
        bounds, t = [], 0.0
        for g in gaps:
            bounds.append((t, g[0]))
            t = g[1]
        bounds.append((t, duration))
    else:  # Fallback: ganze Zeile nach Silben
        chunks, bounds = [list(range(len(words)))], [(0.0, duration)]
    times = [None] * len(words)
    for chunk, (a, b) in zip(chunks, bounds):
        weights = [syllables(words[i]["spoken"]) for i in chunk]
        total, t = sum(weights), a
        for i, wt in zip(chunk, weights):
            d = (b - a) * wt / total
            times[i] = (round(t, 3), round(t + d, 3))
            t += d
    return times


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--backend", choices=["coqui", "piper"], default="coqui")
    ap.add_argument("--voice-dir", help="Piper-Stimmenordner oder Coqui-Modellordner (Standard: aus tools/setup.sh)")
    ap.add_argument("--coqui-python", default=str(CACHE / "coqui" / "bin" / "python"))
    ap.add_argument("--speed", type=float, default=1.0, help=">1 = schneller (atempo)")
    args = ap.parse_args()

    if not args.voice_dir:
        args.voice_dir = str(CACHE / ("thorsten-vits" if args.backend == "coqui" else "voice-de-thorsten-low"))
    project = Path(args.project)
    script = json.loads((project / "script.json").read_text())
    lines = []
    for si, scene in enumerate(script["scenes"]):
        for li, line in enumerate(scene["lines"]):
            words = parse_tokens(line["text"])
            spoken = " ".join(w["spoken"] for w in words)
            lines.append({"scene": scene["id"], "id": line["id"], "words": words, "spoken": spoken,
                          "new_scene": li == 0 and si > 0})

    texts = [l["spoken"] for l in lines]
    if args.backend == "piper":
        raw = synth_piper(texts, args.voice_dir)
    else:
        raw = synth_coqui(texts, args.voice_dir, args.coqui_python)

    out_dir = project / "assets" / "voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    pieces, t = [np.zeros(int(LEAD_IN * SR), dtype="float32")], LEAD_IN
    for line, (audio, sr) in zip(lines, raw):
        audio = trim(resample(audio.astype("float32"), sr))
        if args.speed != 1.0:
            with tempfile.TemporaryDirectory() as d:
                src, dst = Path(d) / "a.wav", Path(d) / "b.wav"
                sf.write(src, audio, SR)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter:a", f"atempo={args.speed}", dst], check=True)
                audio, _ = sf.read(dst, dtype="float32")
        if line["new_scene"]:
            gap = GAP_SCENE
        elif len(pieces) > 1:
            gap = GAP_LINE
        else:
            gap = 0
        pieces.append(np.zeros(int(gap * SR), dtype="float32"))
        t += gap
        dur = len(audio) / SR
        for w, (a, b) in zip(line["words"], word_times(line["words"], dur, audio)):
            w["start"], w["end"] = round(t + a, 3), round(t + b, 3)
        line["start"], line["end"] = round(t, 3), round(t + dur, 3)
        pieces.append(audio)
        t += dur
    pieces.append(np.zeros(int(0.5 * SR), dtype="float32"))
    audio = np.concatenate(pieces)
    audio = audio / max(1e-6, np.max(np.abs(audio))) * 0.89  # ~ -1 dBFS Spitze
    sf.write(out_dir / "narration.wav", audio, SR)
    for l in lines:
        l.pop("new_scene")
    (out_dir / "timings.json").write_text(json.dumps({"duration": round(len(audio) / SR, 3), "lines": lines},
                                                     ensure_ascii=False, indent=1))
    print(f"narration.wav: {len(audio) / SR:.2f} s, {len(lines)} Zeilen")


if __name__ == "__main__":
    main()
