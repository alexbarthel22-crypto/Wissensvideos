#!/usr/bin/env python3
"""Baut ein HyperFrames-Projekt aus script.json + assets/voice/timings.json.

Schreibt:
  index.html                 Root: Hintergrund, Szenen-Hosts, HUD, Untertitel, Ton
  compositions/hud.html      Kapitel-Marke oben + Checkliste oben links
  compositions/captions.html Karaoke-Untertitel (Wort für Wort, Schlüsselwörter farbig)
  compositions/<szene>.html  aus scenes/<szene>.html, Platzhalter __CUES__ / __DUR__ ersetzt

Szenen-Vorlagen greifen über at("L3", "Start") bzw. at("L3", 2) auf Wortzeiten
relativ zum Szenenstart zu; line("L3") liefert [start, ende].
"""
import html
import json
import random
import re
import shutil
import sys
from pathlib import Path

import soundfile as sf

SFX_DIR = next((p for p in [*Path("/root/.claude/plugins/cache/hyperframes").glob("*/*/skills/media-use/audio/assets/sfx"),
                            *Path("/root/.npm/_npx").glob("*/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx")]
                if (p / "manifest.json").exists()),
               Path("/root/.claude/plugins/cache/hyperframes/hyperframes/0.8.217/skills/media-use/audio/assets/sfx"))
W, H = 1080, 1920
COLORS = {"y": "#ffd43b", "r": "#ff3b55", "p": "#ff4fb0", "g": "#39e27a", "b": "#4da3ff", "c": "#3fe3ea"}
WHOOSHES = ["whoosh-short", "whoosh"]  # nur kurze; lange Whooshes/Glitches rauschen unter der Stimme
# ohne HyperFrames-Plugin: Effekte kommen aus assets/sfx des Projekts
MANIFEST = json.loads((SFX_DIR / "manifest.json").read_text()) if (SFX_DIR / "manifest.json").exists() else {}
VENDOR = Path(__file__).resolve().parent / "vendor"


def esc(s):
    return html.escape(s, quote=True)


def norm(s):
    return re.sub(r"[^\wäöüß]", "", s.lower())


def scene_windows(script, timings):
    lines = {l["id"]: l for l in timings["lines"]}
    scenes = script["scenes"]
    starts = []
    for i, sc in enumerate(scenes):
        first = lines[sc["lines"][0]["id"]]
        starts.append(0.0 if i == 0 else round(first["start"] - 0.2, 3))
    out = []
    for i, sc in enumerate(scenes):
        last = lines[sc["lines"][-1]["id"]]
        end = starts[i + 1] if i + 1 < len(scenes) else round(last["end"] + sc.get("hold", 2.0), 3)
        out.append((sc, starts[i], end))
    return out, lines


def cues_for(scene, start, end, lines):
    c = {"__dur": round(end - start, 3)}
    for ln in scene["lines"]:
        l = lines[ln["id"]]
        c[ln["id"]] = [round(l["start"] - start, 3), round(l["end"] - start, 3)]
        c[ln["id"] + ".words"] = [[norm(w["display"]), round(w["start"] - start, 3), round(w["end"] - start, 3)]
                                 for w in l["words"]]
    return c


PLACEHOLDER = """<template>
  <style>#root { position: absolute; inset: 0; }</style>
  <div id="root" data-composition-id="SID" data-start="0" data-duration="__DUR__" data-width="1080" data-height="1920">
    <div id="SID-ph" class="clip" data-start="0" data-duration="__DUR__" style="position:absolute;left:0;top:700px;width:100%;
      text-align:center;color:#555;font:700 40px Inter">SID</div>
  </div>
  <script>window.__timelines["SID"] = gsap.timeline({ paused: true });</script>
</template>
"""

CUE_HELPERS = r"""
      const C = __CUES__;
      const line = (id) => C[id];
      const at = (id, word, which = 0) => {
        const ws = C[id + ".words"];
        if (typeof word === "number") return ws[word][1 + which];
        const key = String(word).toLowerCase().replace(/[^\p{L}\p{N}_]/gu, "");
        const hit = ws.find((w) => w[0].startsWith(key));
        if (!hit) throw new Error("cue not found: " + id + " " + word);
        return hit[1 + which];
      };
      // Zähler: schreibt Zahlen im deutschen Format (4.100.000.000) als Funktion der Timeline-Zeit
      const fmt = (n) => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
      const count = (tl, sel, from, to, t, d, pre = "", post = "", ease = "power2.out") => {
        const el = document.querySelector(sel);
        const o = { v: from };
        el.textContent = pre + fmt(from) + post;
        tl.to(o, { v: to, duration: d, ease, onUpdate: () => { el.textContent = pre + fmt(o.v) + post; } }, t);
      };
      // deterministischer Zufall
      const rng = (seed) => () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let x = Math.imul(seed ^ (seed >>> 15), 1 | seed);
        x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x; return ((x ^ (x >>> 14)) >>> 0) / 4294967296; };
"""


def build_scene(project, scene, start, end, lines):
    src = project / "scenes" / f"{scene['id']}.html"
    if not src.exists():
        print(f"  ! Szenen-Vorlage fehlt, Platzhalter: {src.name}")
        text = PLACEHOLDER.replace("SID", scene["id"])
    else:
        text = src.read_text()
    text = text.replace("/*__CUE_HELPERS__*/", CUE_HELPERS)
    common = project / "scenes" / "_common.css"
    if common.exists():
        text = text.replace("/*__COMMON_CSS__*/", common.read_text())
    common_js = project / "scenes" / "_common.js"
    if common_js.exists():
        text = text.replace("/*__COMMON_JS__*/", common_js.read_text())
    text = text.replace("__CUES__", json.dumps(cues_for(scene, start, end, lines), ensure_ascii=False))
    text = text.replace("__DUR__", f"{end - start:.3f}")
    (project / "compositions" / f"{scene['id']}.html").write_text(text)


def caption_groups(timings, windows):
    """Gruppen pro Zeile; jede Gruppe endet spätestens beim Start der nächsten."""
    groups = []
    for l in timings["lines"]:
        by = {}
        for w in l["words"]:
            by.setdefault(w["group"], []).append(w)
        for g in sorted(by):
            ws = [w for w in by[g] if w["display"].strip() not in ("–", "-", "—")]  # Gedankenstrich am Satzende nicht anzeigen
            for w in ws:
                if w["display"].rstrip().endswith((" –", " -", " —")):
                    w["display"] = w["display"].rstrip()[:-2].rstrip()
            if not ws:
                continue
            groups.append({"words": ws, "start": round(ws[0]["start"] - 0.06, 3), "end": round(ws[-1]["end"] + 0.25, 3)})
    if windows in ("single", "single_full"):  # ein Wort pro Einblendung (TikTok-Stil); single_full: erster Satz bleibt ganz stehen
        keep = groups[:1] if windows == "single_full" else []
        groups = keep + [{"words": [w], "start": round(w["start"] - 0.04, 3), "end": round(w["end"] + 0.35, 3)} for g in groups[len(keep):] for w in g["words"]]
    for a, b in zip(groups, groups[1:]):
        a["end"] = min(a["end"], b["start"])
    groups[0]["start"] = max(groups[0]["start"], 0.15)
    return groups


def build_captions(project, timings, windows, total, big=False, opt=None):
    """opt (script.json "captions"): pop (Wort-Pop), left/right/top/size (TikTok-Sicherheitsbereich), first_at_zero (erster Satz ab Frame 0)."""
    opt = opt or {}
    big = big or opt.get("pop", False)
    groups = caption_groups(timings, ("single_full" if opt.get("first_full") else "single") if opt.get("single") else windows)
    if opt.get("merge_first") and not opt.get("single"):  # erste k Untertitel-Gruppen als ein Satz ab Frame 0 (z. B. Ausruf + Satz)
        k = opt["merge_first"]
        groups = [{"words": [w for g in groups[:k] for w in g["words"]], "start": groups[0]["start"], "end": groups[k - 1]["end"]}] + groups[k:]
    if opt.get("first_at_zero"):
        groups[0]["start"] = 0.0
    if opt.get("merge_last"):  # letzte k Gruppen als ganzer Schluss-Satz (z. B. Frage an die Zuschauer)
        k = opt["merge_last"]
        groups = groups[:-k] + [{"words": [w for g in groups[-k:] for w in g["words"]], "start": groups[-k]["start"], "end": groups[-1]["end"]}]
    if not opt.get("last_off"):  # last_off: letzte Zeile verschwindet nach dem Aussprechen
        groups[-1]["end"] = round(total - 0.05, 3)  # letzte Zeile (Frage an die Zuschauer) bleibt stehen
    rows, js = [], []
    bars = opt.get("bars")
    bar_cols = opt.get("bar_colors", ["#e8467c", "#0a9fa6", "#7b4fe0", "#2f7fe0"])
    for gi, g in enumerate(groups):
        spans = []
        for wi, w in enumerate(g["words"]):
            wid = f"cw{gi}-{wi}"
            col = w["color"]
            fs = f' style="font-size:{10.5 / len(w["display"]):.2f}em"' if opt.get("single") and len(w["display"]) > 11 and not (gi == 0 and opt.get("first_full")) else ""  # lange Wörter passen in die Breite
            spans.append(f'<span id="{wid}" class="w{" k-" + col if col else ""}"{fs}>{esc(w["display"].upper())}</span>')
            target = (opt.get("key_color", "#ffe45c") if bars else COLORS[col]) if col else "#ffffff"
            if gi == 0 and opt.get("hook_text"):  # eigener Farbsatz für den Einstieg (z. B. dunkle Schrift auf Gelb)
                target = opt.get("hook_key", target) if col else opt["hook_text"]
            glow = ("0 3px 0 rgba(0,0,0,.35)" if bars else f"0 0 26px {COLORS[col]}aa, 0 5px 0 rgba(0,0,0,.55)") if col else ("0 3px 0 rgba(0,0,0,.35)" if bars else "0 5px 0 rgba(0,0,0,.55)")
            if opt.get("single"):
                glow = "0 8px 0 rgba(0,0,0,.35)"
            if gi < opt.get("hook_groups", 1) and opt.get("first_full"):  # Einstieg: ganzer Satz steht, gesprochenes Wort leuchtet auf
                nxt = g["words"][wi + 1]["start"] if wi + 1 < len(g["words"]) else w["end"] + 0.25
                js.append(f'tl.fromTo("#{wid}", {{ color: "#ffffff", scale: 1 }}, {{ color: "#ffc93c", {('fontSize: "' + opt["first_grow_map"][w["display"].upper()] + '"') if w["display"].upper() in opt.get("first_grow_map", {}) else ('scale: ' + str(opt.get("first_scale_map", {}).get(w["display"].upper(), opt.get("first_scale", 1.16))))}, zIndex: 10,{(' boxShadow: "' + opt["first_shadow_map"][w["display"].upper()] + '",') if w["display"].upper() in opt.get("first_shadow_map", {}) else ""} duration: 0.09, ease: "power2.out", immediateRender: false }}, {max(0, w["start"] - 0.03):.3f});')
                js.append(f'tl.to("#{wid}", {{ color: "#ffffff", {('fontSize: "1em"') if w["display"].upper() in opt.get("first_grow_map", {}) else 'scale: 1'}, zIndex: 1,{(' boxShadow: "' + opt.get("first_shadow_rest", "none") + '",') if w["display"].upper() in opt.get("first_shadow_map", {}) else ""} duration: 0.1, ease: "power1.out" }}, {nxt - 0.03:.3f});')
                continue
            if gi == 0 and opt.get("hook_shadow"):
                glow = opt["hook_shadow"]
            js.append(f'tl.to("#{wid}", {{ color: "{target}", textShadow: "{glow}", duration: 0.08, ease: "power1.out" }}, {w["start"] - 0.02:.3f});')
            if big and not (gi == 0 and wi == 0 and opt.get("first_at_zero")):  # Wort hüpft beim Sprechen kurz an (erstes Wort steht ruhig für das Vorschaubild)
                if gi == 0 and opt.get("hook_punch"):  # Einstieg: jedes Wort knallt deutlich auf
                    js.append(f'tl.fromTo("#{wid}", {{ scale: 1.7, y: -30, rotation: {(-10, 8, -7, 9)[wi % 4]} }}, {{ scale: 1, y: 0, rotation: 0, duration: 0.42, ease: "elastic.out(1.1, 0.45)", immediateRender: false }}, {w["start"] - 0.03:.3f});')
                else:
                    js.append(f'tl.fromTo("#{wid}", {{ scale: {opt.get("pop_scale", 1.16)}, y: -8, rotation: {(-4, 3, -2, 4)[wi % 4]} }}, {{ scale: 1, y: 0, rotation: 0, duration: 0.28, ease: "back.out(3)", immediateRender: false }}, {w["start"] - 0.02:.3f});')
        dur = round(g["end"] - g["start"], 3)
        rows.append(f'    <div id="cg{gi}" class="clip grp" data-start="{g["start"]:.3f}" data-duration="{dur}" data-track-index="{gi % 2}">'
                    f'<div id="cgi{gi}" class="inner{" " + opt["first_class"] if gi < opt.get("hook_groups", 1) and opt.get("first_class") else ""}{" hk" if gi == 0 and opt.get("first_full") else ""}"{" data-layout-allow-overlap" if big else ""}>'
                    + (f'<span class="bar" style="background:{bar_cols[gi % len(bar_cols)]}">{" ".join(spans)}</span>' if bars else " ".join(spans)) + '</div></div>')
        if gi == 0 and opt.get("first_at_zero"):  # erster Satz steht ab Frame 0 (Thumbnail)
            js.append(f'tl.set("#cgi{gi}", {{ scale: 1, opacity: 1 }}, 0);')
            if opt.get("hook_punch"):  # ganzer Satz: Schlag auf dem letzten Wort, danach lebendiges Wippen
                lw = g["words"][-1]["start"]
                js.append(f'tl.fromTo("#cgi{gi}", {{ scale: 1.22, rotation: -4 }}, {{ scale: 1, rotation: 0, duration: 0.6, ease: "elastic.out(1, 0.35)", immediateRender: false }}, {lw - 0.02:.3f});')
        else:
            if opt.get("vary"):  # jede Gruppe kommt anders herein, Balken leicht schräg
                fr, to = ENTRANCES[gi % len(ENTRANCES)]
                rot = (-2, 1.5, -1, 2.2, -1.6, 1)[gi % 6]
                js.append(f'tl.fromTo("#cgi{gi}", {{ opacity: 0, {fr} }}, {{ opacity: 1, rotation: {rot}, {to} }}, {g["start"]:.3f});')
            elif opt.get("single"):  # Wort ploppt auf
                d = max(0.05, min(0.2, g["end"] - g["start"] - 0.1))
                js.append(f'tl.fromTo("#cgi{gi}", {{ scale: 0.35, opacity: 0, y: 30 }}, {{ scale: 1, opacity: 1, y: 0, duration: {d:.3f}, ease: "back.out(2.8)" }}, {g["start"]:.3f});')
            else:
                js.append(f'tl.fromTo("#cgi{gi}", {{ scale: 0.86, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.16, ease: "back.out(2.2)" }}, {g["start"]:.3f});')
        if not opt.get("single"):
            js.append(f'tl.to("#cgi{gi}", {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, {g["end"] - 0.08:.3f});')
        js.append(f'tl.set("#cgi{gi}", {{ opacity: 0 }}, {g["end"]:.3f});')
    doc = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .grp {{ position: absolute; left: 0; width: 100%; top: 1150px; height: 220px; overflow: visible; }}
    .inner {{ position: absolute; left: 70px; right: 70px; top: 0; text-align: center;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 80px; line-height: 1.04;
      letter-spacing: -0.01em; transform-origin: 50% 40%; }}
    .w {{ color: #7d8197; text-shadow: 0 5px 0 rgba(0,0,0,.55); }}{BIG_CAP if big else ""}{safe_css(opt)}
  </style>
  <div id="root" data-composition-id="captions" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}"
       data-layout-allow-caption-zone>
{chr(10).join(rows)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10) + "    ".join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
    (project / "compositions" / "captions.html").write_text(doc)


ENTRANCES = [
    ("scale: 0.5, rotation: -8", "scale: 1, duration: 0.28, ease: \"back.out(2.6)\""),
    ("x: -260, skewX: -18", "x: 0, skewX: 0, duration: 0.26, ease: \"power4.out\""),
    ("y: 120, scale: 0.9", "y: 0, scale: 1, duration: 0.42, ease: \"bounce.out\""),
    ("scaleX: 0.2, scaleY: 1.4", "scaleX: 1, scaleY: 1, duration: 0.34, ease: \"elastic.out(1, 0.5)\""),
    ("x: 260, skewX: 18", "x: 0, skewX: 0, duration: 0.26, ease: \"power4.out\""),
    ("y: -110, rotation: 10", "y: 0, duration: 0.32, ease: \"back.out(2.2)\""),
    ("scale: 1.8, filter: \"blur(10px)\"", "scale: 1, filter: \"blur(0px)\", duration: 0.24, ease: \"expo.out\""),
]


def safe_css(o):
    keys = {"left": "left", "right": "right", "size": "font-size"}
    inner = "; ".join(f"{css}: {o[k]}px" for k, css in keys.items() if k in o)
    out = f"\n    .inner {{ {inner}; }}" if inner else ""
    if o.get("bars"):
        out += ("\n    .bar { padding: .04em .26em .1em; border-radius: .2em; line-height: 1.34; -webkit-box-decoration-break: clone; box-decoration-break: clone;"
                " box-shadow: 0 6px 0 rgba(0,0,0,.28); } .inner .w { text-shadow: 0 3px 0 rgba(0,0,0,.35); }")
    if o.get("css"):
        out += "\n    " + o["css"]
    if "top" in o:
        out += f"\n    .grp {{ top: {o['top']}px; }}"
    if "color" in o:
        out += f"\n    .w {{ color: {o['color']}; }}"
    return out


BIG_CAP = """
    .inner {{ font-size: 92px; line-height: 1.06; }}
    .w {{ display: inline-block; transform-origin: 50% 70%; }}""".replace("{{", "{").replace("}}", "}")
TITLE_COLS = ["#ffd43b", "#ff4fb0", "#4da3ff", "#39e27a", "#ff8a3d", "#b06bff"]
POP_HUD = """
    .tag { top: 150px; height: 104px; }
    .tagt { height: 100px; min-width: 520px; padding: 0 34px; font-size: 54px; letter-spacing: 0.08em; color: #ffd43b;
      border: 4px solid #ffd43b; border-radius: 14px; background: rgba(10,12,29,.88);
      text-shadow: 0 0 22px rgba(255,212,59,.6); box-shadow: 0 0 26px rgba(255,212,59,.4); }
"""

BIG_HUD = """
    .btag { position: absolute; left: 0; width: 100%; top: 130px; height: 250px; }
    .kick { position: absolute; left: 0; right: 0; top: 0; margin: 0 auto; width: fit-content; padding: 4px 24px;
      font-family: "Space Mono", monospace; font-weight: 700; font-size: 36px; letter-spacing: .14em; color: #0b0e22;
      background: #ffd43b; border-radius: 10px; box-shadow: 0 0 30px rgba(255,212,59,.5); }
    .ttl { position: absolute; left: 0; right: 0; top: 100px; text-align: center; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 136px; line-height: 1; letter-spacing: -.02em; }
    .ttl span { display: inline-block; -webkit-text-stroke: 4px #0b0e22; paint-order: stroke fill; }
"""


def build_hud_big(project, script, windows, total):
    """Große Kapitel-Überschrift: Kicker-Pille + riesiger Titel, Buchstaben fallen hüpfend ein und wippen weiter."""
    tags, checks, js, n = [], [], [], 0
    for i, (sc, s, e) in enumerate(windows):
        kick, _, title = (p.strip() for p in sc["tag"].partition("·")) if "·" in sc["tag"] else ("", "", sc["tag"])
        col = TITLE_COLS[i % len(TITLE_COLS)]
        letters = "".join(f'<span id="t{i}l{k}" style="color:{col};text-shadow:0 0 34px {col}99,0 8px 0 rgba(0,0,0,.5)">{esc(ch) if ch != " " else "&nbsp;"}</span>'
                          for k, ch in enumerate(title))
        tags.append(f'      <div id="tag{i}" class="clip btag" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="1">'
                    + (f'<div id="tag{i}k" class="kick">{esc(kick)}</div>' if kick else "")
                    + (f'<div id="tag{i}t" class="ttl">{letters}</div>' if title else "") + '</div>')
        t0 = s if i > 0 else 0.0
        if kick:
            js.append(f'tl.fromTo("#tag{i}k", {{ opacity: 0, x: -260, skewX: -20 }}, {{ opacity: 1, x: 0, skewX: 0, duration: 0.35, ease: "back.out(2)" }}, {t0:.3f});')
        if title:
            ls = f'"#tag{i}t span"'
            js.append(f'tl.fromTo({ls}, {{ opacity: 0, y: -120, scale: 1.8, rotation: (k) => [-14, 10, -8, 12][k % 4] }}, '
                      f'{{ opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.4)", stagger: 0.04 }}, {t0 + 0.08:.3f});')
            reps = max(1, int((e - s - 1.0) / 0.5))
            js.append(f'tl.to({ls}, {{ y: -14, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: {reps * 2 - 1}, stagger: {{ each: 0.06 }} }}, {t0 + 0.75:.3f});')
            js.append(f'tl.fromTo("#tag{i}t", {{ scale: 1 }}, {{ scale: 1.07, duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out" }}, {t0 + 0.55:.3f});')
        if sc.get("check"):
            n += 1
            cid = f"chk{n}"
            checks.append(f'      <div id="{cid}" class="clip chk" data-start="{s + 0.5:.3f}" data-duration="{total - s - 0.5:.3f}" '
                          f'data-track-index="2" data-layout-ignore style="top:{416 + (n - 1) * 37}px">'
                          f'<span id="{cid}t" class="chkt ok">{n}. {esc(sc["check"])} <b>✓</b></span></div>')
            js.append(f'tl.fromTo("#{cid}t", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.25, ease: "power3.out" }}, {s + 0.5:.3f});')
    return tags, checks, js


def build_hud(project, script, windows, total):
    tags, checks, js, n = [], [], [], 0
    big = script.get("hud") == "big"
    pop = script.get("hud") == "pop"
    if big:
        tags, checks, js = build_hud_big(project, script, windows, total)
    for i, (sc, s, e) in enumerate(windows if not big else []):
        tid = f"tag{i}"
        if not sc["tag"]:  # leere Marke = keine Kapitel-Marke in dieser Szene
            continue
        tags.append(f'      <div id="{tid}" class="clip tag" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="1">'
                    f'<span id="{tid}t" class="tagt">{esc(sc["tag"])}</span></div>')
        if pop:  # große Marke, knallt mit Zoom/Unschärfe/Zittern + Glow-Blitz herein
            js.append(f'tl.fromTo("#{tid}t", {{ opacity: 0, scale: 2.4, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }}, {s:.3f});')
            js.append(f'tl.fromTo("#{tid}t", {{ x: -10 }}, {{ x: 0, duration: 0.05, repeat: 4, yoyo: true, ease: "none" }}, {s + 0.42:.3f});')
            js.append(f'tl.fromTo("#{tid}t", {{ boxShadow: "0 0 80px rgba(255,212,59,.95)" }}, {{ boxShadow: "0 0 26px rgba(255,212,59,.4)", duration: 0.7, ease: "power2.out" }}, {s + 0.42:.3f});')
        elif i > 0:  # erste Marke steht ab Frame 0 (Thumbnail/Hook)
            js.append(f'tl.fromTo("#{tid}t", {{ opacity: 0, y: -8 }}, {{ opacity: 1, y: 0, duration: 0.22, ease: "power3.out" }}, {s:.3f});')
        if sc.get("check"):
            n += 1
            cid = f"chk{n}"
            checks.append(f'      <div id="{cid}" class="clip chk" data-start="{s + 0.5:.3f}" data-duration="{total - s - 0.5:.3f}" '
                          f'data-track-index="2" data-layout-ignore style="top:{258 + (n - 1) * 37}px">'
                          f'<span id="{cid}t" class="chkt{" ok" if script.get("check_ok") else ""}">{n}. {esc(sc["check"])} <b>{"✓" if script.get("check_ok") else "✕"}</b></span></div>')
            js.append(f'tl.fromTo("#{cid}t", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.25, ease: "power3.out" }}, {s + 0.5:.3f});')
    if script.get("progress") == "muschel":  # eigener Fortschrittsbalken unten: Welle spült eine kleine Muschel nach vorne
        wave = "M0 30 " + " ".join(f"Q{x + 20} {26 if (x // 40) % 2 == 0 else 34} {x + 40} 30" for x in range(0, W, 40))
        tags.append(f'''      <div id="pg" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="3" data-layout-ignore style="position:absolute;left:0;top:{H - 70}px;width:{W}px;height:70px">
        <svg width="{W}" height="70" viewBox="0 0 {W} 60" style="position:absolute;left:0;top:10px;overflow:visible"><defs><clipPath id="pgc"><rect id="pgr" x="0" y="0" width="0" height="60"/></clipPath></defs>
          <path d="{wave}" fill="none" stroke="rgba(255,255,255,.3)" stroke-width="3" stroke-linecap="round"/>
          <path d="{wave}" fill="none" stroke="rgba(110,220,255,.85)" stroke-width="4" stroke-linecap="round" clip-path="url(#pgc)"/></svg>
        <div id="pgs" style="position:absolute;left:-30px;top:-2px;width:60px;height:46px">
          <svg viewBox="0 0 60 46" width="60" height="46"><defs><radialGradient id="pgsh" cx=".5" cy=".95" r=".95"><stop offset="0" stop-color="#fffaf2"/><stop offset=".55" stop-color="#ffd2c0"/><stop offset="1" stop-color="#ef7aa0"/></radialGradient></defs>
          <path d="M6 40 Q18 31 30 38 Q42 31 54 40" fill="none" stroke="rgba(255,255,255,.85)" stroke-width="2.5" stroke-linecap="round"/>
          <g transform="translate(30 22)"><path d="M0 13 L-15.5 8.8 Q-18 3.6 -13 2.6 Q-13.6 -3 -8.6 -2 Q-7.6 -7.6 -3 -5 Q0 -9.4 3 -5 Q7.6 -7.6 8.6 -2 Q13.6 -3 13 2.6 Q18 3.6 15.5 8.8 Z" fill="url(#pgsh)" stroke="#5a2a32" stroke-width="1.1" stroke-linejoin="round"/>
          <path d="M0 12 L-12.6 3.4 M0 12 L-8 -1.2 M0 12 L-2.8 -3.4 M0 12 L2.8 -3.4 M0 12 L8 -1.2 M0 12 L12.6 3.4" stroke="#c94a74" stroke-width=".9" stroke-linecap="round" opacity=".8"/>
          <path d="M-4.5 13.4 L-2.6 10.4 H2.6 L4.5 13.4 Z" fill="#ffcdb5" stroke="#5a2a32" stroke-width=".9" stroke-linejoin="round"/><path d="M-9 -0.5 Q-6 -3 -3 -2.4" stroke="#fff" stroke-width="1.2" fill="none" stroke-linecap="round" opacity=".9"/></g></svg></div>
      </div>''')
        js.append(f'tl.fromTo("#pgr", {{ attr: {{ width: 0 }} }}, {{ attr: {{ width: {W} }}, duration: {total:.3f}, ease: "none" }}, 0);')
        js.append(f'tl.fromTo("#pgs", {{ x: 0 }}, {{ x: {W}, duration: {total:.3f}, ease: "none" }}, 0);')
        js.append(f'tl.fromTo("#pgs", {{ y: 0, rotation: -6 }}, {{ y: -3, rotation: 6, duration: 0.6, yoyo: true, repeat: {int(total / 0.6)}, ease: "sine.inOut" }}, 0);')
    doc = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .tag {{ position: absolute; left: 0; width: 100%; top: 176px; height: 64px; }}
    .tagt {{ position: absolute; left: 0; right: 0; top: 0; margin: 0 auto; width: fit-content; min-width: 420px; padding: 0 26px; height: 62px;
      display: flex; align-items: center; justify-content: center;
      font-family: "Space Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.12em;
      color: #f4d27a; border: 3px solid #b8944a; border-radius: 8px; background: rgba(14,17,36,.65); }}
    .chk {{ position: absolute; left: 0; width: 100%; height: 34px; }}
    .chkt {{ position: absolute; left: 30px; top: 0; padding: 2px 10px;
      font-family: "Space Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.04em;
      color: #ff7a8c; border: 2px solid #c8314a; border-radius: 6px; background: rgba(40,10,24,.55); }}
    .chkt b {{ color: #ff3b55; margin-left: 6px; }}
    .chkt.ok {{ color: #8affb6; border-color: #1f9a52; background: rgba(8,40,22,.6); }}
    .chkt.ok b {{ color: #39e27a; }}{BIG_HUD if big else POP_HUD if pop else ""}
  </style>
  <div id="root" data-composition-id="hud" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">
{chr(10).join(tags)}
{chr(10).join(checks)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10) + "    ".join(js)}
    window.__timelines["hud"] = tl;
  </script>
</template>
"""
    (project / "compositions" / "hud.html").write_text(doc)


def resolve_sfx_time(spec, windows, lines):
    """'L4:Server' -> absolute Zeit des Wortes; 's03+0.4' -> Szenenstart + Offset."""
    m = re.match(r"^(L\d+[a-z]*):(.+?)([+-][\d.]+)?$", spec)
    if m:
        l = lines[m.group(1)]
        key = norm(m.group(2))
        w = next(w for w in l["words"] if norm(w["display"]).startswith(key))
        return w["start"] + float(m.group(3) or 0)
    m = re.match(r"^(s\d+[a-z]*)([+-][\d.]+)?$", spec)
    sc = next(s for s in windows if s[0]["id"] == m.group(1))
    return sc[1] + float(m.group(2) or 0)


def stars_svg(seed=19):
    rnd = random.Random(seed)
    dots = []
    for _ in range(140):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.choice([1.2, 1.6, 2.2, 2.8])
        o = rnd.uniform(0.15, 0.6)
        dots.append(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{r}' fill='%23cfd6ff' opacity='{o:.2f}'/>")
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{''.join(dots)}</svg>"


def build_world(project, windows, lines, total):
    """Optionale durchgehende Hintergrund-Ebene (scenes/_world.html) mit allen Wort-Zeiten (absolut) und Szenenfenstern."""
    src = project / "scenes" / "_world.html"
    if not src.exists():
        return False
    c = {"__dur": round(total, 3)}
    for sc, s, e in windows:
        c[sc["id"]] = [round(s, 3), round(e, 3)]
    for lid, l in lines.items():
        c[lid] = [round(l["start"], 3), round(l["end"], 3)]
        c[lid + ".words"] = [[norm(w["display"]), round(w["start"], 3), round(w["end"], 3)] for w in l["words"]]
    text = src.read_text().replace("/*__CUE_HELPERS__*/", CUE_HELPERS).replace("__CUES__", json.dumps(c, ensure_ascii=False))
    (project / "compositions" / "world.html").write_text(text.replace("__DUR__", f"{total:.3f}"))
    return True


def build_index(project, script, windows, lines, total, world=False):
    hosts = []
    for i, (sc, s, e) in enumerate(windows):
        hosts.append(f'      <div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" '
                     f'data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="{W}" data-height="{H}" style="z-index:2"></div>')
    # Ton: Whoosh auf jedem Szenenwechsel (rotierend) + Effekte aus script.json
    sfx_dir = project / "assets" / "sfx"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    audio, k = [], 0
    placements = [(WHOOSHES[i % 2], s - 0.12, 0.25) for i, (sc, s, e) in enumerate(windows) if i > 0]
    for sc, s, e in windows:
        for fx in sc.get("sfx", []):
            placements.append((fx["name"], resolve_sfx_time(fx["at"], windows, lines), fx.get("volume", 0.5)))
    for name, t, vol in sorted(placements, key=lambda p: p[1]):
        if name in MANIFEST:
            shutil.copy(SFX_DIR / f"{name}.mp3", sfx_dir / f"{name}.mp3")
            fname, dur = f"{name}.mp3", MANIFEST[name]["duration"]
        else:  # eigener Sound im Projekt, z. B. assets/sfx/purge-siren.wav (tools/make_siren.py)
            fname = next(p.name for p in sfx_dir.glob(name + ".*"))
            dur = round(sf.info(sfx_dir / fname).duration, 3)
        k += 1
        audio.append(f'      <audio id="fx{k}" class="clip" src="assets/sfx/{fname}" data-start="{max(0, t):.3f}" data-duration="{dur}" '
                     f'data-track-index="{10 + k}" data-volume="{vol}"></audio>')
    THREE_TAG = '\n    <script src="assets/vendor/three.min.js"></script>' if (project / "assets" / "vendor" / "three.min.js").exists() else ""
    doc = f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>{THREE_TAG}
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #0c0f22; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #bg {{ position: absolute; inset: 0; z-index: 0;
        background: {script.get("bg") or ('url("data:image/svg+xml;utf8,' + stars_svg() + '"), radial-gradient(ellipse 80% 55% at 50% 42%, #1c2250 0%, #121634 45%, #0a0c1d 100%)')}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">
      <div id="bg" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="0"></div>
{chr(10).join(hosts)}
{f'      <video id="bgvid" class="clip" src="{script["bgvideo"]["src"]}" data-start="0" data-duration="{total:.3f}" data-track-index="3" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1"></video>' if script.get("bgvideo") else ""}
{f'      <div id="world" data-composition-id="world" data-composition-src="compositions/world.html" data-start="0" data-duration="{total:.3f}" data-track-index="4" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:1"></div>' if world else ""}
      <div id="hud" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="{total:.3f}"
           data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:5"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0"
           data-duration="{total:.3f}" data-track-index="3" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:6"></div>
      <audio id="vo" class="clip" src="assets/voice/narration.wav" data-start="0" data-track-index="9" data-volume="1"></audio>
{f'      <audio id="music" class="clip" src="{script["music"]["src"]}" data-start="0" data-duration="{total:.3f}" data-track-index="8" data-volume="{script["music"].get("volume", 1)}"></audio>' if script.get("music") else ""}
{f'      <audio id="ambience" class="clip" src="{script["ambience"]["src"]}" data-start="0" data-duration="{total:.3f}" data-track-index="7" data-volume="{script["ambience"].get("volume", 1)}"></audio>' if script.get("ambience") else ""}
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    (project / "index.html").write_text(doc)


def main():
    project = Path(sys.argv[1])
    script = json.loads((project / "script.json").read_text())
    timings = json.loads((project / "assets" / "voice" / "timings.json").read_text())
    windows, lines = scene_windows(script, timings)
    total = windows[-1][2]
    (project / "compositions").mkdir(exist_ok=True)
    (project / "assets" / "vendor").mkdir(parents=True, exist_ok=True)
    shutil.copy(VENDOR / "gsap.min.js", project / "assets" / "vendor" / "gsap.min.js")
    for sc, s, e in windows:
        build_scene(project, sc, s, e, lines)
    build_captions(project, timings, windows, total, script.get("hud") == "big", script.get("captions"))
    build_hud(project, script, windows, total)
    world = build_world(project, windows, lines, total)
    build_index(project, script, windows, lines, total, world)
    for sc, s, e in windows:
        print(f"{sc['id']}: {s:6.2f} – {e:6.2f}  ({e - s:4.2f} s)  {sc['tag']}")
    print(f"Gesamt: {total:.2f} s")


if __name__ == "__main__":
    main()
