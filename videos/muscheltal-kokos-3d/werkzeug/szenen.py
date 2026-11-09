import sys
from pathlib import Path
D = Path(sys.argv[1]); LOGO = Path(sys.argv[2]).read_text().strip()
SHELL = '<svg viewBox="0 0 64 64"><path d="M32 47 L8.8 40.8 Q5.0 34.0 12.7 32.7 Q11.6 25.0 19.2 26.7 Q21.0 19.1 27.5 23.4 Q32.0 17.0 36.5 23.4 Q43.0 19.1 44.8 26.7 Q52.4 25.0 51.3 32.7 Q59.0 34.0 55.2 40.8 Z" fill="#ffc7b2" stroke="#2a1b12" stroke-width="3" stroke-linejoin="round"/><path d="M32 45L13.9 33.6M32 45L20.0 27.9M32 45L27.8 24.9M32 45L36.2 24.9M32 45L44.0 27.9M32 45L50.1 33.6" stroke="#c43d6b" stroke-width="2" stroke-linecap="round"/></svg>'
LILITA = '@font-face { font-family: "Lilita One"; src: url("assets/fonts/LilitaOne-Regular.woff2") format("woff2"); font-weight: 400; }'

def scene(sid, css, html, js, blur=True):
    end = f'tl.to("#{sid}-stage > *", {{ opacity: 0, filter: "blur(8px)", duration: 0.18 }}, C.__dur - 0.18);' if blur else ""
    (D / f"{sid}.html").write_text(f"""<template>
  <style>
    /*__COMMON_CSS__*/
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-start="0" data-duration="__DUR__" data-width="1080" data-height="1920">
    <div id="{sid}-stage" class="clip stage" data-start="0" data-duration="__DUR__" data-track-index="0">
{html}
    </div>
  </div>
  <script>
    (() => {{
      /*__CUE_HELPERS__*/
      /*__COMMON_JS__*/
      wrapBt("#{sid}-stage");
      const tl = gsap.timeline({{ paused: true }});
{js}
      {end}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
""")

def tk(cid, col, ini, user, text, likes, extra=""):
    return (f'<div id="{cid}" class="tk-c"><div class="tk-a" style="background:{col}">{ini}</div><div><div class="tk-u">{user}{extra}</div>'
            f'<div class="tk-t">{text}</div><div class="tk-m">vor 2 Std.<span>Antworten</span></div></div>'
            f'<div class="tk-l"><div class="hz"></div><i>{likes}</i></div></div>')


def cards(pref, items, top):
    out = []
    for i, (em, lab, col) in enumerate(items):
        x = 90 + (i % 2) * 460; y = top + (i // 2) * 300
        out.append(f'<div id="{pref}{i}" class="wc" style="left:{x}px;top:{y}px"><div class="wce">{em}</div><div class="wcl" style="background:{col}">{lab}</div></div>')
    return "\n      ".join(out)

CONF_JS = """const R = rng(SEED), box = document.getElementById("BOX"), cols = ["#ffd23f", "#e8467c", "#2fb3a0", "#fff", "#7b4fe0", "#ff7a59"];
      for (let k = 0; k < 60; k++) { const d = document.createElement("div"); d.className = "cf"; d.style.background = cols[k % cols.length]; box.appendChild(d);
        const a = R() * Math.PI * 2, v = 380 + R() * 560, dx = Math.cos(a) * v, dy = Math.sin(a) * v * .8 - 300;
        tl.fromTo(d, { opacity: 0, x: 0, y: 0, rotation: 0, scale: .6 }, { opacity: 1, x: dx * .7, y: dy * .7, rotation: (R() - .5) * 720, scale: 1, duration: .45, ease: "power3.out" }, T0);
        tl.to(d, { x: dx, y: dy + 700, rotation: "+=" + Math.round((R() - .5) * 540), opacity: 0, duration: 1.4, ease: "power1.in" }, T0 + .45); }"""
CF_CSS = ".cf { position: absolute; left: 530px; top: 700px; width: 20px; height: 30px; border-radius: 4px; }"
WC_CSS = """.wc { position: absolute; width: 400px; height: 270px; border-radius: 34px; background: #fff; box-shadow: 0 0 0 6px #1a0f08, 0 14px 0 rgba(0,0,0,.35); overflow: hidden; }
    .wce { height: 180px; display: grid; place-items: center; font-size: 120px; background: linear-gradient(180deg, #bfefff, #fff); }
    .wcl { height: 90px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; color: #fff; }"""



PILL = """.pl { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; padding: 8px 28px 12px; border-radius: 999px; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); white-space: nowrap; }"""
FOLLOW = """    .fbtn { position: absolute; left: 0; right: 0; margin: 0 auto; width: 420px; height: 120px; border-radius: 60px; background: #fe2c55; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; display: grid; place-items: center; box-shadow: 0 0 0 5px #2a1b12, 0 12px 0 rgba(0,0,0,.25); }
    .fbtn2 { position: absolute; inset: 0; border-radius: 60px; background: #fff; color: #0a78c2; display: grid; place-items: center; opacity: 0; }
    .fhand { position: absolute; font-size: 120px; }"""

import math as _m
_CP, _CL = (0.0, 2.9, 12.5), (0.0, 1.7, 0.0)
def _sub(a, b): return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
def _nrm(v): l = _m.sqrt(sum(x*x for x in v)); return [x/l for x in v]
def _cr(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
_F = _nrm(_sub(_CL, _CP)); _R = _nrm(_cr(_F, [0, 1, 0])); _U = _cr(_R, _F); _TH = _m.tan(_m.radians(25)); _AS = 1080/1920
def P(x, y, z):
    d = _sub((x, y, z), _CP); X = sum(a*b for a, b in zip(d, _R)); Y = sum(a*b for a, b in zip(d, _U)); Z = sum(a*b for a, b in zip(d, _F))
    return (540 + X/(Z*_TH*_AS)*540, 960 - Y/(Z*_TH)*960)
def poly(pts, close=True): return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")
def ell3(cx, cy, cz, rx, ry, n=64, a0=0, a1=2*_m.pi): return [P(cx + rx*_m.cos(a0 + (a1-a0)*k/n), cy + ry*_m.sin(a0 + (a1-a0)*k/n), cz) for k in range(n+1)]
def arch3(w, h, z, n=24):
    pts = [(-w/2, 0), (-w/2, h - w/2)] + [(-w/2*_m.cos(k/n*_m.pi), h - w/2 + w/2*_m.sin(k/n*_m.pi)) for k in range(1, n)] + [(w/2, h - w/2), (w/2, 0)]
    return [P(x, y, z) for x, y in pts]
def rotXYZ(v, rx, ry, rz):
    x, y, z = v; c, s_ = _m.cos(rz), _m.sin(rz); x, y = x*c - y*s_, x*s_ + y*c
    c, s_ = _m.cos(ry), _m.sin(ry); x, z = x*c + z*s_, -x*s_ + z*c
    c, s_ = _m.cos(rx), _m.sin(rx); y, z = y*c - z*s_, y*s_ + z*c
    return (x, y, z)
def bez(p0, p1, p2, p3, n=16): return [tuple((1-t)**3*a + 3*(1-t)**2*t*b + 3*(1-t)*t*t*c + t**3*d for a, b, c, d in zip(p0, p1, p2, p3)) for t in [k/n for k in range(n+1)]]
def leaf3(rz, ry):
    loc = bez((0, 0), (.5, .3), (.62, 1.25), (0, 1.9)) + bez((0, 1.9), (-.62, 1.25), (-.5, .3), (0, 0))[1:]
    pts = []
    for x, y in loc: v = rotXYZ((x, y, 0), -.35, ry, rz); pts.append(P(v[0], v[1] + 3.25, v[2] - .1))
    rib = [P(*[a + b for a, b in zip(rotXYZ((0, y, .06), -.35, ry, rz), (0, 3.25, -.1))]) for y in (.15, 1.7)]
    return pts, rib
C0 = (0, 1.62, 0); DC = (0, 1.0, .74)
def onEll(x, y): k = 1 - (x/1.4)**2 - ((y - 1)/1.288)**2; return (x, y, .74 + 1.008*_m.sqrt(max(.02, k)))
shell = ell3(0, 1.62, 0, 1.75, 1.75); dome = ell3(0, 1.0, .74, 1.4, 1.288, 64, _m.radians(-38), _m.radians(218))
pores = []
for px, py, r in [(-.4, 2.68, .2), (.4, 2.68, .2), (0, 2.25, .16)]:
    z = _m.sqrt(1.75**2 - px*px - (py - 1.62)**2); pores.append((P(px, py, z), r*95))
door_o, door_i = arch3(1.02, 1.42, 1.83), arch3(.74, 1.24, 1.83)
wp = (.95, 1.55, _m.sqrt(1.75**2 - .95**2 - (1.55 - 1.62)**2) + .01); wc = P(*wp)
leaves = [leaf3(.95, .25), leaf3(-.85, -.2)]
pots = [(sx*.9, 1.95) for sx in (-1, 1)]
stones = [P((0.0), .03, 2.3 + k*.6) for k in range(4)]
ground = ell3(.2, 0, .3, 2.6, .01, 48)
# Faserstriche (2D, auf Schale/Kuppel)
import random as _r; _r.seed(7)
fibers = []
for k in range(46):
    if k % 2: x, y = _r.uniform(-1.2, 1.2), _r.uniform(.4, 1.9); pz = onEll(x, y); a = P(*pz); 
    else:
        th = _r.uniform(-1.1, 1.1); ph = _r.uniform(.15, 1.25); x = 1.75*_m.sin(th)*_m.cos(ph-.6); y = 1.62 + 1.75*_m.sin(ph-.2)*.9; z = _m.sqrt(max(.05, 1.75**2 - x*x - (y-1.62)**2)); a = P(x, y, z)
    ang = _r.uniform(-1.2, 1.2); L_ = _r.uniform(14, 26); fibers.append((a[0], a[1], a[0] + _m.cos(ang)*L_, a[1] + _m.sin(ang)*L_))
SC = P(0, 1.62, 0); SR = abs(P(1.75, 1.62, 0)[0] - SC[0])
strokes = [(poly(shell, False), "s", 1.0), (poly(dome, False), "s", .7)]
strokes += [(poly(l, True), "s", .45) for l, _ in leaves] + [(poly(r, False), "s", .12) for _, r in leaves]
strokes += [(f"M{c[0]+rr:.1f},{c[1]:.1f} A{rr:.1f},{rr*.9:.1f} 0 1,1 {c[0]-rr:.1f},{c[1]:.1f} A{rr:.1f},{rr*.9:.1f} 0 1,1 {c[0]+rr:.1f},{c[1]:.1f}", "s", .12) for c, rr in pores]
strokes += [(poly(door_o, False), "s", .45), (poly(door_i, False), "s", .35)]
wr = abs(P(wp[0] + .36, wp[1], wp[2])[0] - wc[0]); strokes += [(f"M{wc[0]+wr:.1f},{wc[1]:.1f} A{wr:.1f},{wr:.1f} 0 1,1 {wc[0]-wr:.1f},{wc[1]:.1f} A{wr:.1f},{wr:.1f} 0 1,1 {wc[0]+wr:.1f},{wc[1]:.1f}", "s", .2)]
for px, pz in pots:
    a, b, c, d = P(px - .2, .3, pz), P(px + .2, .3, pz), P(px + .15, 0, pz), P(px - .15, 0, pz); strokes.append((poly([a, b, c, d]), "s", .1))
    for k in range(5): q = P(px + (k - 2)*.08, .45 + (k % 2)*.08, pz); strokes.append((f"M{q[0]+7:.1f},{q[1]:.1f} A7,7 0 1,1 {q[0]-7:.1f},{q[1]:.1f} A7,7 0 1,1 {q[0]+7:.1f},{q[1]:.1f}", "f", .04))
for q in stones: strokes.append((f"M{q[0]+30:.1f},{q[1]:.1f} A30,9 0 1,1 {q[0]-30:.1f},{q[1]:.1f} A30,9 0 1,1 {q[0]+30:.1f},{q[1]:.1f}", "s", .06))
strokes.append((poly(ground, False), "s", .3))
strokes += [(f"M{a:.1f},{b:.1f} L{c:.1f},{d:.1f}", "f", .015) for a, b, c, d in fibers]
FILLS = [(poly(shell), "url(#gSh)"), (poly(dome), "url(#gDo)")] + [(poly(l), "url(#gLf)") for l, _ in leaves] + \
        [(poly(door_o), "#a39ca0"), (poly(door_i), "#fff0a0")] + [(f"M{c[0]+rr:.1f},{c[1]:.1f} A{rr:.1f},{rr*.9:.1f} 0 1,1 {c[0]-rr:.1f},{c[1]:.1f} A{rr:.1f},{rr*.9:.1f} 0 1,1 {c[0]+rr:.1f},{c[1]:.1f}", "#16111b") for c, rr in pores] + \
        [(f"M{wc[0]+wr:.1f},{wc[1]:.1f} A{wr:.1f},{wr:.1f} 0 1,1 {wc[0]-wr:.1f},{wc[1]:.1f} A{wr:.1f},{wr:.1f} 0 1,1 {wc[0]+wr:.1f},{wc[1]:.1f}", "#a39ca0"),
         (f"M{wc[0]+wr*.78:.1f},{wc[1]:.1f} A{wr*.78:.1f},{wr*.78:.1f} 0 1,1 {wc[0]-wr*.78:.1f},{wc[1]:.1f} A{wr*.78:.1f},{wr*.78:.1f} 0 1,1 {wc[0]+wr*.78:.1f},{wc[1]:.1f}", "#fff0a0")]
DEFS = '<defs><radialGradient id="gSh" cx=".4" cy=".3" r=".8"><stop offset="0" stop-color="#55404c"/><stop offset="1" stop-color="#2a1d25"/></radialGradient><radialGradient id="gDo" cx=".45" cy=".35" r=".8"><stop offset="0" stop-color="#8a634f"/><stop offset="1" stop-color="#55392f"/></radialGradient><linearGradient id="gLf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f9a6e"/><stop offset="1" stop-color="#2a5e44"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="3"/></filter></defs>'
SVG = ('<svg id="s01-svg" width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0">' + DEFS +
       '<g id="s01-fill" opacity="0">' + "".join(f'<path d="{d}" fill="{c}"/>' for d, c in FILLS) + '</g>' +
       '<g id="s01-lines">' + "".join(f'<path class="sp" d="{d}" fill="none" stroke="#fff" stroke-width="{9 if kind == "s" else 5}" stroke-linecap="round" stroke-linejoin="round"/>' for d, kind, w in strokes) + '</g></svg>')
WTS = [w for _, _, w in strokes]
scene("s01", LILITA + "\n    " + PILL + """
    #s01-lines path { filter: drop-shadow(0 0 3px rgba(0,0,0,.5)); }
    #s01-pen { position: absolute; left: 0; top: 0; font-size: 110px; }
    #s01-hk { position: absolute; left: 0; right: 0; top: 290px; text-align: center; }
    .hk-l { display: table; margin: 14px auto 0; background: #e8262f; border-radius: 30px; padding: 2px 34px 12px; font-family: "Lilita One", sans-serif; font-size: 104px; line-height: 1.05; color: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 9px 0 rgba(0,0,0,.25); }
    .hk-w { display: inline-block; margin: 0 .08em; transform-origin: 50% 60%; position: relative; }
    #hw2 { margin-right: .22em; }
    #s01-stk { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 330px; color: #e8433c; border-color: #e8433c; background: #fff; transform: rotate(-5deg); font-size: 54px; white-space: nowrap; }
    #s01-fl { position: absolute; inset: 0; background: #fff; opacity: 0; }""",
"""
      <div id="s01-hk"><div class="hk-l"><span class="hk-w" id="hw0">DAS</span><span class="hk-w" id="hw1">KÖNNTE</span></div><div class="hk-l"><span class="hk-w" id="hw2">DEIN</span><span class="hk-w" id="hw3">HAUS</span></div><div class="hk-l"><span class="hk-w" id="hw4">SEIN!</span></div></div>
      <div id="s01-fl"></div>""",
"""      const TH = .42;
      tl.fromTo("#s01-fl", { opacity: 0 }, { opacity: .6, duration: .05, yoyo: true, repeat: 1, immediateRender: false }, TH);
      tl.fromTo("#s01-hk", { y: 0 }, { y: 16, duration: .05, yoyo: true, repeat: 3, immediateRender: false }, TH);
      const hk = ["Das", "könnte", "dein", "Haus", "sein"];
      tl.set("#s01-hk", { opacity: 1 }, 0);
      hk.forEach((w, i) => { const t0 = Math.max(0, at("L1", w) - .03); tl.set("#hw" + i, { zIndex: 5 }, t0); tl.fromTo("#hw" + i, { scale: 1 }, { scale: .5, duration: .05, immediateRender: false }, t0); tl.to("#hw" + i, { scale: [1.8, 1.5, 3.2, 2.0, 1.9][i], duration: .13, ease: "power2.out" }, t0 + .05); tl.to("#hw" + i, { scale: i === 2 ? 1.18 : 1, color: "#ffe14d", textShadow: "0 0 26px rgba(255,225,77,1), 0 0 8px rgba(255,255,200,1)", duration: .22, ease: "back.out(2.5)" }, t0 + .18); tl.to("#hw" + i, { textShadow: "0 0 0px rgba(255,225,77,0), 0 0 0px rgba(255,255,200,0)", duration: .5 }, t0 + .45); });
""", blur=False)

scene("s02", PILL + """
    #s02-t { top: 300px; font-size: 58px; background: #e2560c; }
    #s02-n { top: 420px; font-size: 48px; background: #fff; color: #2a1b12; }""",
"""      <div id="s02-t" class="pl">🏠 1 FOLLOWER = 1 HÜTTE</div>
      <div id="s02-n" class="pl">✍️ mit <span style="color:#e8467c">deinem @Namen</span></div>""",
"""      tl.fromTo("#s02-t", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.6)" }, at("L3", "Jeder") - .1);
      tl.fromTo("#s02-n", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, at("L3", "Namen") - .25);
      tl.to("#s02-n", { scale: 1.07, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L3", "Namen") + .2);""")

scene("s03", PILL + """
    #s03-t { top: 300px; font-size: 54px; background: #e8433c; }
    #s03-c { position: absolute; left: 0; right: 0; margin: 0 auto; top: 410px; width: fit-content; padding: 4px 36px 10px; border-radius: 36px; background: #fff; border: 6px solid #ff6a1a;
      font-family: "Inter", sans-serif; color: #2a1b12; font-weight: 900; font-size: 38px; display: flex; align-items: baseline; gap: 14px; box-shadow: 0 10px 0 rgba(0,40,80,.3); }
    #s03-c b { font-size: 92px; color: #e2560c; line-height: 1; }""",
"""      <div id="s03-t" class="pl">🔥 FRISCH EINGEZOGEN</div>
      <div id="s03-c"><b id="s03-n">0</b>BEWOHNER</div>""",
"""      const he = at("L4", "heute");
      tl.fromTo("#s03-t", { opacity: 0, y: -50 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, he - .2);
      tl.fromTo("#s03-c", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, he);
      count(tl, "#s03-n", 0, 653, he + .1, 1.4, "", "", "power3.in");
      tl.fromTo("#s03-c", { scale: 1 }, { scale: 1.3, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, he + 1.5);""")

CARD = """    .bc { position: absolute; left: 80px; width: 920px; height: 150px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.3);
      display: flex; align-items: center; gap: 20px; padding: 0 28px; font-family: "Inter", sans-serif; color: #23285a; }
    .bc .e { font-size: 72px; } .bc .m { flex: 1; } .bc b { font-size: 40px; font-weight: 900; display: block; line-height: 1.1; } .bc small { display: block; font-size: 30px; font-weight: 800; color: #e2560c; margin-top: 4px; }
    .bc .z { font-size: 26px; font-weight: 900; color: #6b6f8a; text-align: center; line-height: 1.1; } .bc .z i { font-style: normal; font-size: 40px; color: #e2560c; display: block; }"""
scene("s04", PILL + "\n" + CARD + """
    #s04-t { top: 290px; font-size: 54px; background: #e2560c; }""",
"""      <div id="s04-t" class="pl">🏗️ AKTUELL IM BAU</div>
      <div id="s04-h" class="bc" style="top:400px"><div class="e">🏨</div><div class="m"><b>Hotel Sandkorn</b><small>Hier wohnen &amp; arbeiten viele von euch</small></div><div class="z">ab<i>800</i>Bewohnern</div></div>
      <div id="s04-a" class="bc" style="top:580px"><div class="e">⚓</div><div class="m"><b>Anlegestelle</b><small>Von Insel zu Insel reisen ⛵</small></div><div class="z">ab<i>900</i>Bewohnern</div></div>""",
"""      const ge = at("L5", "gebaut"), ho = at("L5", "Hotel"), an = at("L5", "Anlegestelle");
      tl.fromTo("#s04-t", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.6)" }, ge - .3);
      tl.fromTo("#s04-h", { opacity: 0, x: -140 }, { opacity: 1, x: 0, duration: .35, ease: "back.out(2)" }, ho - .2);
      tl.to("#s04-h", { scale: 1.05, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L5", "wohnen"));
      tl.fromTo("#s04-a", { opacity: 0, x: 140 }, { opacity: 1, x: 0, duration: .35, ease: "back.out(2)" }, an - .2);
      tl.to("#s04-a", { scale: 1.05, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L5", "Insel"));""")

scene("s05", PILL + "\n" + FOLLOW + """
    #s05-w { top: 290px; font-size: 52px; background: #18a6b8; }
    #s05-a { top: 400px; font-size: 44px; background: #2e9e5b; }
    #s05-btn { top: 520px; } #s05-hand { left: 690px; top: 570px; }
    #s05-h { top: 670px; font-size: 56px; background: #fe2c55; }
    #s05-f { top: 780px; font-size: 40px; background: #e2560c; }""",
"""      <div id="s05-w" class="pl">🗺️ ENTDECKE MUSCHEL-TAL</div>
      <div id="s05-a" class="pl">🌱 Von Anfang an dabei sein!</div>
      <div id="s05-btn" class="fbtn">+ Folgen<div id="s05-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s05-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s05-h" class="pl">@muscheltal</div>
      <div id="s05-f" class="pl">🏠 Eigene Hütte mit Namen – für immer!</div>""",
"""      const en = at("L6", "Entdecke"), af = at("L6", "Anfang"), fo = at("L6", "folgen");
      tl.fromTo("#s05-w", { opacity: 0, scale: .3, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.6)" }, en - .1);
      tl.fromTo("#s05-a", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, af - .2);
      tl.fromTo("#s05-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .6);
      tl.fromTo("#s05-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .35);
      tl.to("#s05-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo);
      tl.to("#s05-btn2", { opacity: 1, duration: .05 }, fo + .1);
      tl.fromTo("#s05-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .1);
      tl.to("#s05-hand", { opacity: 0, duration: .25 }, fo + .6);
      tl.fromTo("#s05-h", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, fo + .3);
      tl.to("#s05-h", { scale: 1.07, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, fo + .7);
      const im = at("L6", "immer");
      tl.fromTo("#s05-f", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, at("L6", "eigene") - .2);
      tl.to("#s05-f", { scale: 1.08, duration: .22, yoyo: true, repeat: 5, ease: "sine.inOut" }, im);""", blur=False)
