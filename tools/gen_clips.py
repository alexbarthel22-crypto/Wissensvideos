#!/usr/bin/env python3
"""Animiert Szenenbilder (assets/img/<name>.png) mit gemini-omni-1.1-flash (Interactions-API) zu ~4-s-Clips.

  python3 tools/gen_clips.py videos/<slug> [--only a,b] [--force]
Bewegungsanweisungen aus clips.json {"name": "Bewegung …"} → assets/vid/raw/<name>.mp4
"""
import argparse, base64, json, os, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KEY = os.environ.get("GEMINI_API_KEY")
SUFFIX = (" Animate this exact image into a 4 second vertical 9:16 video. Keep the art style, characters, faces and composition identical,"
          " natural lifelike motion. No text, no captions, no subtitles, no audio.")


def anim(img, prompt, out):
    body = {"model": os.environ.get("OMNI_MODEL", "gemini-omni-1.1-flash"), "input": [
        {"type": "image", "data": base64.b64encode(img.read_bytes()).decode(), "mime_type": "image/png"}, {"type": "text", "text": prompt + SUFFIX}]}
    for a in range(10):
        try:
            req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions", data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
            d = json.load(urllib.request.urlopen(req, timeout=600))
            for st in d.get("steps", []):
                for c in st.get("content", []) or []:
                    if c.get("type") == "video":
                        out.write_bytes(base64.b64decode(c["data"])); return
            raise KeyError("kein Video")
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            print("retry", out.name, e, flush=True)
            if a == 9:
                raise
            time.sleep(min(90, 15 * (a + 1)))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--only"); ap.add_argument("--force", action="store_true")
    a = ap.parse_args(); p = Path(a.project); cfg = json.loads((p / "clips.json").read_text())
    outd = p / "assets" / "vid" / "raw"; outd.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    todo = [k for k in cfg if (not only or k in only) and (a.force or not (outd / f"{k}.mp4").exists())]

    def job(k):
        try:
            anim(p / "assets" / "img" / f"{k}.png", cfg[k], outd / f"{k}.mp4"); print("ok", k, flush=True)
        except Exception as e:
            print("FEHLER", k, e, flush=True)
    with ThreadPoolExecutor(1) as ex:
        list(ex.map(job, todo))


if __name__ == "__main__":
    main()
