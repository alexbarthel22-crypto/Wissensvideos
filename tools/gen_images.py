#!/usr/bin/env python3
"""Erzeugt Szenenbilder mit Gemini-Bildmodell im Stil von Referenzbildern.

  python3 tools/gen_images.py videos/<slug> [--only name1,name2] [--force]

images.json: {"style": "...", "refs": ["assets/ref/a.jpg", ...], "model": "...",
              "images": {"name": "Bildbeschreibung" | {"edit": "basisname", "prompt": "..."}}}
Ergebnis: assets/img/<name>.png (1080x1920, zugeschnitten). Vorhandene Bilder werden übersprungen.
"""
import argparse, base64, io, json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image

KEY = os.environ.get("GEMINI_API_KEY")


def call(model, parts):
    body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}}}
    for a in range(5):
        try:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}",
                                         data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            d = json.load(urllib.request.urlopen(req, timeout=240))
            for p in d["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    return base64.b64decode(p["inlineData"]["data"])
            raise KeyError("kein Bild")
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            if a == 4:
                raise
            time.sleep(5 * (a + 1))


def part(path):
    return {"inline_data": {"mime_type": "image/png" if str(path).endswith(".png") else "image/jpeg", "data": base64.b64encode(Path(path).read_bytes()).decode()}}


def fit(b, out):
    im = Image.open(io.BytesIO(b)).convert("RGB")
    s = max(1080 / im.width, 1920 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - 1080) // 2, (im.height - 1920) // 2
    im.crop((l, t, l + 1080, t + 1920)).save(out)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--only"); ap.add_argument("--force", action="store_true")
    a = ap.parse_args(); proj = Path(a.project); cfg = json.loads((proj / "images.json").read_text())
    model = cfg.get("model", "gemini-3.1-flash-image"); refs = [proj / r for r in cfg.get("refs", [])]
    outd = proj / "assets" / "img"; outd.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    items = {k: v for k, v in cfg["images"].items() if (not only or k in only) and (a.force or not (outd / f"{k}.png").exists())}
    base = {k: v for k, v in items.items() if isinstance(v, str)}
    edits = {k: v for k, v in items.items() if not isinstance(v, str)}

    def gen(k):
        p = [part(r) for r in refs] + [{"text": cfg["style"] + "\n\nSCENE: " + base[k]}]
        fit(call(model, p), outd / f"{k}.png"); print("ok", k, flush=True)

    def edit(k):
        v = edits[k]
        fit(call(model, [part(outd / f"{v['edit']}.png"), {"text": v["prompt"]}]), outd / f"{k}.png"); print("ok", k, flush=True)

    with ThreadPoolExecutor(6) as ex:
        list(ex.map(gen, base))
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(edit, edits))


if __name__ == "__main__":
    main()
