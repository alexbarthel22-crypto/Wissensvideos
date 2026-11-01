#!/usr/bin/env python3
"""Schnittliste: welche animierte Einstellung wann läuft; passt Clips per Zeitlupe/Ping-Pong an die Sprechzeit an."""
import json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from build_video import scene_windows

P = Path(__file__).parent
SHOTS = {
 "s01": [("c45", None), ("brain", ("L2", "Gehirn", -0.05))],
 "s02": [("watch", None), ("typing", ("L3", "Und", -0.05)), ("panic", ("L4", "plötzlich", -0.1))],
 "s03": [("waiting", None), ("stopwatch", ("L6", None, -0.05))],
 "s04": [("neurons", None), ("student", ("L8", None, -0.05))],
 "s05": [("flow", None), ("melt", ("L10", None, -0.05))],
 "s06": [("lab", None)],
 "s07": [("route", None), ("map", ("L13", None, -0.1))],
 "s10": [("shower", None), ("dress", ("L13b", "Anziehen", -0.1)), ("door", ("L13d", None, -0.05))],
 "s08": [("think", None), ("plan", ("L15", None, -0.05))],
 "s09": [("point", None)],
}
key = lambda s: re.sub(r"[^\w]", "", s.lower())
script = json.loads((P / "script.json").read_text()); tim = json.loads((P / "assets/voice/timings.json").read_text())
wins, lines = scene_windows(script, tim)
out = {}
(P / "assets/vid").mkdir(exist_ok=True)
for sc, s0, s1 in wins:
    sid = sc["id"]; res = []
    times = []
    for name, cue in SHOTS[sid]:
        if cue is None: t = 0.0
        else:
            lid, w, off = cue; l = lines[lid]
            t = (l["start"] if w is None else next(x["start"] for x in l["words"] if key(x["display"]).startswith(key(w)))) + off - s0
        times.append(round(max(0.0, t), 3))
    for k, (name, _) in enumerate(SHOTS[sid]):
        t = times[k]; t2 = times[k + 1] if k + 1 < len(times) else round(s1 - s0, 3)
        dur = round(t2 - t, 3); target = dur + 0.3
        raw = P / f"assets/vid/raw/{name}.mp4"; dst = P / f"assets/vid/{sid}_{k}.mp4"
        L = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", raw]).decode())
        f = target / L
        chain = "[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[v];[v]" if f > 1.9 else "[0:v]"
        if f > 1.9: f = target / (2 * L)
        f = max(f, 1.0)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-filter_complex",
                        chain + f"setpts={f:.4f}*PTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p", "-an", "-t", f"{target:.3f}",
                        "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", dst], check=True)
        res.append({"src": f"assets/vid/{sid}_{k}.mp4", "start": t, "dur": dur})
        print(sid, k, name, t, dur, f"x{f:.2f}")
    out[sid] = res
(P / "shots.json").write_text(json.dumps(out, indent=1))
