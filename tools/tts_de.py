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
GAP_LINE = 0.22      # Pause zwischen Zeilen derselben Szene
GAP_SCENE = 0.38     # Pause zwischen Szenen
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


def synth_piper(texts, voice_dir, scales, noise):
    from piper import PiperVoice
    from piper.config import SynthesisConfig
    model = next(Path(voice_dir).glob("*.onnx"))
    voice = PiperVoice.load(str(model))
    out = []
    for t, ls in zip(texts, scales):
        cfg = SynthesisConfig(length_scale=ls, noise_scale=noise, noise_w_scale=0.9)
        chunks = [c.audio_float_array for c in voice.synthesize(t, syn_config=cfg)]
        out.append((np.concatenate(chunks), voice.config.sample_rate))
    return out


def synth_coqui(texts, model_dir, python, scales, noise):
    """Läuft im separaten venv; schreibt WAVs in ein Temp-Verzeichnis."""
    tmp = Path(tempfile.mkdtemp())
    (tmp / "lines.json").write_text(json.dumps({"texts": texts, "scales": scales}, ensure_ascii=False))
    model = next(p for p in Path(model_dir).iterdir() if p.name.startswith("model_file"))
    code = f"""
import json
from TTS.api import TTS
job = json.load(open({str(tmp / 'lines.json')!r}))
tts = TTS(model_path={str(model)!r}, config_path={str(Path(model_dir) / 'config.json')!r})
m = tts.synthesizer.tts_model
m.inference_noise_scale = {noise}
m.inference_noise_scale_dp = 0.9
kw = {{}}
if tts.is_multi_speaker and tts.speakers: kw["speaker"] = tts.speakers[0]
if tts.is_multi_lingual and tts.languages: kw["language"] = tts.languages[0]
for i, (t, ls) in enumerate(zip(job["texts"], job["scales"])):
    m.length_scale = ls
    tts.tts_to_file(text=t, file_path={str(tmp)!r} + f'/{{i:03d}}.wav', **kw)
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


# Sprachverständlichkeit: Rumpeln weg, Präsenz (2–4 kHz) und Luft anheben, gleichmäßige Lautstärke
CLARITY = ("highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3000:t=q:w=1.2:g=4,"
           "equalizer=f=7500:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2")


def clarity(audio):
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "a.wav", Path(d) / "b.wav"
        sf.write(src, audio, SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", CLARITY, dst], check=True)
        a, _ = sf.read(dst, dtype="float32")
    return a


def voiced_frames(audio, thresh_db=-36, min_blip=4):
    """Pro 10-ms-Frame: Sprache ja/nein. Ausreißer kürzer als min_blip Frames (Knackser, Atem) zählen als Stille."""
    hop = int(0.01 * SR)
    n = len(audio) // hop
    rms = np.sqrt(np.mean(audio[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    v = 20 * np.log10(rms) > thresh_db
    i = 0
    while i < n:
        if v[i]:
            j = i
            while j < n and v[j]:
                j += 1
            if j - i < min_blip:
                v[i:j] = False
            i = j
        else:
            i += 1
    return v


def trim(audio):
    v = np.where(voiced_frames(audio))[0]
    if len(v) == 0:
        return audio
    hop = int(0.01 * SR)
    return audio[max(0, v[0] * hop - int(0.03 * SR)): min(len(audio), (v[-1] + 1) * hop + int(0.08 * SR))]


def pauses(audio, min_len=0.11):
    """Stille-Abschnitte innerhalb der Zeile: [(start, end), ...] in Sekunden."""
    v = voiced_frames(audio)
    res, start = [], None
    for i, voiced in enumerate(v):
        if not voiced and start is None:
            start = i
        elif voiced and start is not None:
            if (i - start) * 0.01 >= min_len and start > 3:
                res.append((start * 0.01, i * 0.01))
            start = None
    return res


def compress_pauses(audio, max_gap=0.3):
    """Kürzt Sprechpausen innerhalb einer Zeile auf max_gap (Coqui setzt ~0,5–1 s zwischen Sätze)."""
    out, last = [], 0
    for a, b in pauses(audio, min_len=max_gap):
        cut_a = int((a + max_gap / 2) * SR)
        cut_b = int((b - max_gap / 2) * SR)
        if cut_b > cut_a:
            out.append(audio[last:cut_a])
            last = cut_b
    out.append(audio[last:])
    return np.concatenate(out)


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
    ap.add_argument("--speed", type=float, default=1.0, help="Grundtempo (>1 = schneller); pro Zeile mit 'speed' feinjustierbar")
    ap.add_argument("--voice", default="css10", help="Stimme im Cache: css10 (weiblich, coqui), thorsten-vits (männlich, coqui), "
                    "voice-de-kerstin-low / voice-de-ramona-low (weiblich, piper), voice-de-thorsten-low")
    ap.add_argument("--max-gap", type=float, default=0.3, help="längste Pause innerhalb einer Zeile in Sekunden")
    ap.add_argument("--noise", type=float, default=0.75, help="Ausdruck/Variation der Stimme (0.33 monoton … 0.9 lebhaft)")
    args = ap.parse_args()

    if not args.voice_dir:
        args.voice_dir = str(CACHE / (args.voice if args.voice != "css10" else "css10-vits"))
    project = Path(args.project)
    script = json.loads((project / "script.json").read_text())
    lines = []
    for si, scene in enumerate(script["scenes"]):
        for li, line in enumerate(scene["lines"]):
            words = parse_tokens(line["text"])
            spoken = " ".join(w["spoken"] for w in words)
            lines.append({"scene": scene["id"], "id": line["id"], "words": words, "spoken": spoken,
                          "new_scene": li == 0 and si > 0, "pause": line.get("pause", 0.0),
                          "scale": round(1.0 / (args.speed * line.get("speed", 1.0)), 3)})

    texts = [l["spoken"] for l in lines]
    scales = [l["scale"] for l in lines]
    if args.backend == "piper":
        raw = synth_piper(texts, args.voice_dir, scales, args.noise)
    else:
        raw = synth_coqui(texts, args.voice_dir, args.coqui_python, scales, args.noise)

    out_dir = project / "assets" / "voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    pieces, t = [np.zeros(int(LEAD_IN * SR), dtype="float32")], LEAD_IN
    for line, (audio, sr) in zip(lines, raw):
        audio = compress_pauses(trim(clarity(resample(audio.astype("float32"), sr))), args.max_gap)
        if line["new_scene"]:
            gap = GAP_SCENE
        elif len(pieces) > 1:
            gap = GAP_LINE
        else:
            gap = 0
        gap += line["pause"]
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
        for k in ("new_scene", "pause", "scale"):
            l.pop(k)
    (out_dir / "timings.json").write_text(json.dumps({"duration": round(len(audio) / SR, 3), "lines": lines},
                                                     ensure_ascii=False, indent=1))
    print(f"narration.wav: {len(audio) / SR:.2f} s, {len(lines)} Zeilen")


if __name__ == "__main__":
    main()
