"""Synthesize every line of an episode with Google Cloud TTS and build the timeline.

Usage: python3 engine/tts.py story/folge01.json out/folge01
Writes <out>/voice/*.wav (cached), <out>/timeline.json and <out>/voice.wav.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
import base64
import wave

import numpy as np

SR = 48000
API = "https://texttospeech.googleapis.com/v1/text:synthesize"

FX = {
    # ethereal, slightly higher, shimmering echo
    "stern": "asetrate=48000*1.05,aresample=48000,atempo=0.9524,"
             "aecho=0.8:0.75:70|140|260:0.35|0.25|0.15,highpass=f=140",
    # the star unmasked: deeper, heavier, darker tail
    "dunkel": "asetrate=48000*0.84,aresample=48000,atempo=1.19,"
              "aecho=0.8:0.8:90|210|420:0.4|0.28|0.18,lowpass=f=6500",
    # a voice from very far away
    "fern": "highpass=f=260,lowpass=f=5200,aecho=0.8:0.85:120|340|700:0.45|0.3|0.2",
}


def synth(text, voice, rate, path):
    body = {
        "input": {"text": text},
        "voice": {"languageCode": "de-DE", "name": voice},
        "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000, "speakingRate": rate},
    }
    req = urllib.request.Request(
        API, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": os.environ["GOOGLE_TTS_API_KEY"]})
    with urllib.request.urlopen(req, timeout=60) as r:
        audio = base64.b64decode(json.load(r)["audioContent"])
    with open(path, "wb") as f:
        f.write(audio)


def load_wav(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def process(raw, fx, path):
    filters = "aresample=48000" + ("," + FX[fx] if fx else "") + ",apad=pad_dur=0.0"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", filters,
                    "-ac", "1", "-ar", str(SR), path], check=True)


def trim_silence(x, thresh=0.01):
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(0.03 * SR))
    b = min(len(x), idx[-1] + int(0.12 * SR))
    return x[a:b]


def resolve_cue(spec, scene_start, line_starts):
    if isinstance(spec, (int, float)):
        return scene_start + spec
    m = re.fullmatch(r"L(\d+)([+-][\d.]+)?", spec)
    return line_starts[int(m.group(1))] + float(m.group(2) or 0)


def main(story_path, out_dir):
    story = json.load(open(story_path))
    vdir = os.path.join(out_dir, "voice")
    os.makedirs(vdir, exist_ok=True)

    t = 0.0
    timeline = {k: story[k] for k in ("serie", "folge", "titel")}
    timeline["scenes"], timeline["lines"], timeline["cues"] = [], [], {}
    clips = []
    for scene in story["scenes"]:
        start = t
        t += scene.get("pre", 0.5)
        line_starts = []
        for i, line in enumerate(scene["lines"]):
            v = story["voices"][line["who"]]
            rate = line.get("rate", v.get("rate", 1.0))
            key = hashlib.sha1(f"{v['name']}|{rate}|{line['text']}".encode()).hexdigest()[:12]
            raw = os.path.join(vdir, f"{key}.raw.wav")
            fin = os.path.join(vdir, f"{key}.{v.get('fx', 'clean')}.wav")
            if not os.path.exists(raw):
                print("TTS", line["who"], line["text"][:50])
                synth(line["text"], v["name"], rate, raw)
            if not os.path.exists(fin):
                process(raw, v.get("fx"), fin)
            audio = trim_silence(load_wav(fin))
            if i > 0:
                t += line.get("pre", 0.45)
            line_starts.append(t)
            dur = len(audio) / SR
            clips.append((t, audio))
            timeline["lines"].append({"scene": scene["id"], "who": line["who"], "label": v["label"],
                                      "text": line["text"], "start": round(t, 3), "end": round(t + dur, 3)})
            t += dur
        t += scene.get("post", 0.5)
        timeline["scenes"].append({"id": scene["id"], "start": round(start, 3), "end": round(t, 3)})
        for name, spec in scene.get("cues", {}).items():
            timeline["cues"][name] = round(resolve_cue(spec, start, line_starts), 3)

    timeline["duration"] = round(t, 3)
    track = np.zeros(int(t * SR) + SR, dtype=np.float32)
    for start, audio in clips:
        i = int(start * SR)
        track[i:i + len(audio)] += audio
    np.save(os.path.join(out_dir, "voice.npy"), track)
    json.dump(timeline, open(os.path.join(out_dir, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    print(f"Dauer: {t:.1f}s  ({int(t // 60)}:{int(t % 60):02d})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
