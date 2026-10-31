"""Synthesize every line of an episode with Google Cloud TTS and build the timeline.

Usage: python3 engine/tts.py story/folge01.json out/folge01
Writes <out>/voice/*.wav (cached), <out>/timeline.json and <out>/voice.npy.

With GEMINI_API_KEY set, lines are voiced by Gemini TTS using each voice's persona and
each line's "style" as acting direction; otherwise Cloud TTS Chirp 3 HD voices are used.
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
GEMINI_API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_MODEL = os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-pro-preview-tts")
ENGINE = "gemini" if os.environ.get("GEMINI_API_KEY") else "chirp"

# Presence boost and gentle compression for intelligibility under music
CLARITY = "highpass=f=75,equalizer=f=3200:t=q:w=1.2:g=3,equalizer=f=250:t=q:w=1:g=-2,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120"

FX = {
    # ethereal, slightly higher, shimmering echo
    "stern": "asetrate=48000*1.03,aresample=48000,atempo=0.9709,"
             "aecho=0.9:0.6:60|130|240:0.22|0.14|0.08,highpass=f=120",
    # the star unmasked: deeper, heavier, darker tail
    "dunkel": "asetrate=48000*0.88,aresample=48000,atempo=1.1364,"
              "aecho=0.9:0.65:80|190|380:0.28|0.18|0.1,lowpass=f=7500",
    # a voice from very far away
    "fern": "highpass=f=200,lowpass=f=6500,aecho=0.9:0.7:110|300|620:0.3|0.2|0.12",
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


def synth_gemini(text, voice, line, path):
    direction = f"{voice.get('persona', '')} Sprich auf Hochdeutsch mit sehr klarer, deutlicher Aussprache."
    if line.get("style"):
        direction += f" Spielweise: {line['style']}."
    body = {
        "contents": [{"parts": [{"text": f"{direction}\nSprich genau diesen Text:\n{text}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice["gemini"]}}},
        },
    }
    req = urllib.request.Request(
        GEMINI_API.format(model=GEMINI_MODEL), data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    with urllib.request.urlopen(req, timeout=120) as r:
        part = json.load(r)["candidates"][0]["content"]["parts"][0]["inlineData"]
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(base64.b64decode(part["data"]))


def load_wav(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def process(raw, fx, path):
    filters = "aresample=48000," + CLARITY + ("," + FX[fx] if fx else "")
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
    timeline = {k: story[k] for k in ("serie", "folge", "titel", "tagline")}
    timeline["scenes"], timeline["lines"], timeline["cues"] = [], [], {}
    clips = []
    for scene in story["scenes"]:
        start = t
        t += scene.get("pre", 0.5)
        line_starts = []
        for i, line in enumerate(scene["lines"]):
            v = story["voices"][line["who"]]
            rate = line.get("rate", v.get("rate", 1.0))
            if ENGINE == "gemini":
                ident = f"gemini|{GEMINI_MODEL}|{v['gemini']}|{v.get('persona')}|{line.get('style')}|{line['text']}"
            else:
                ident = f"{v['name']}|{rate}|{line['text']}"
            key = hashlib.sha1(ident.encode()).hexdigest()[:12]
            raw = os.path.join(vdir, f"{key}.raw.wav")
            fin = os.path.join(vdir, f"{key}.{v.get('fx', 'clean')}.v2.wav")
            if not os.path.exists(raw):
                print("TTS", line["who"], line["text"][:50])
                if ENGINE == "gemini":
                    synth_gemini(line["text"], v, line, raw)
                else:
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
                                      "text": line.get("display", line["text"]), "start": round(t, 3), "end": round(t + dur, 3)})
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
