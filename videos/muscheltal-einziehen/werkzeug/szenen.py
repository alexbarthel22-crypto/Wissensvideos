import json
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


def drops(cid, n, seed, t, cx, cy, ch, spread=520, up=700):
    """Partikel (Emoji) fliegen aus (cx, cy) heraus."""
    html = "".join(f'<div class="pt" id="{cid}{i}" style="left:{cx - 40}px;top:{cy - 40}px">{ch}</div>' for i in range(n))
    js = f"""      {{ const R = rng({seed}); for (let i = 0; i < {n}; i++) {{ const dx = (R() - .5) * {spread} * 2, dy = -{up} * (.5 + R() * .6);
        tl.fromTo("#{cid}" + i, {{ opacity: 0, x: 0, y: 0, scale: .4, rotation: 0 }}, {{ opacity: 1, x: dx * .6, y: dy * .6, scale: 1, rotation: (R() - .5) * 400, duration: .4, ease: "power3.out" }}, {t});
        tl.to("#{cid}" + i, {{ x: dx, y: dy * .6 + 900, opacity: 0, rotation: "+=" + Math.round((R() - .5) * 300), duration: 1.3, ease: "power1.in" }}, {t} + .4); }} }}"""
    return html, js
PT = ".pt { position: absolute; width: 80px; height: 80px; font-size: 70px; text-align: center; line-height: 80px; opacity: 0; }"

CAN = """.can { position: absolute; top: -200px; width: 64px; height: 168px; background: url(assets/img/can.png) center/contain no-repeat; opacity: 0; filter: drop-shadow(0 6px 6px rgba(0,0,0,.35)); }"""

FL = """    .fl { position: absolute; inset: 0; background: #fff; opacity: 0; }"""

def rain(cid, n, seed, t0, t1):
    html = "".join(f'<div class="can" id="{cid}{i}" data-layout-ignore></div>' for i in range(n))
    js = f"""      {{ const R = rng({seed}), T0 = {t0}, T1 = {t1}; for (let i = 0; i < {n}; i++) {{ const x = 20 + R() * 1000, d = .9 + R() * .7, st = T0 + R() * Math.max(.1, T1 - T0 - d);
        document.getElementById("{cid}" + i).style.left = x + "px"; const sz = .7 + R() * .6; document.getElementById("{cid}" + i).style.transform = "scale(" + sz + ")";
        const y0 = (T0 === 0 && i < {n} / 3) ? 200 + R() * 1500 : 0, st2 = y0 ? 0 : st;
        tl.fromTo("#{cid}" + i, {{ opacity: 1, y: y0, rotation: (R() - .5) * 60 }}, {{ y: 2300, rotation: "+=" + Math.round((R() - .5) * 540), duration: y0 ? d * (2300 - y0) / 2300 + .2 : d, ease: y0 ? "none" : "power1.in" }}, st2); }} }}"""
    return html, js

BIG = """.big { position: absolute; left: 0; right: 0; width: fit-content; max-width: 980px; white-space: nowrap; margin: 0 auto; text-align: center; padding: 10px 26px 20px; border-radius: 36px; color: #fff; font-family: "Lilita One", sans-serif; line-height: 1; box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3); }"""
CMT = """.cmt { position: absolute; left: 140px; width: 800px; border-radius: 30px; padding: 8px; background: linear-gradient(135deg, #5fe0ff, #ff7ac0); box-shadow: 0 14px 30px rgba(0,0,0,.45); transform: rotate(-1.5deg); }
    .cmt img { display: block; width: 100%; border-radius: 23px; }"""



NEU = ["johanna_prx", "miskicelma2701", "najlahasa307", "jonas_mtb156", "d9750075"]

# s01 – Hook: Zähler rast auf 787, Einwohnerliste scrollt im Hintergrund
scene("s01", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #e1-rv { position: absolute; inset: 0; box-shadow: inset 0 0 140px 50px rgba(255,40,160,.85); opacity: 0; }
    #e1-dim { position: absolute; inset: 0; background: radial-gradient(circle at 50% 42%, rgba(20,10,50,.25), rgba(20,10,50,.75)); }
    #e1-fl { position: absolute; inset: 0; background: #fff; opacity: 0; }
    #e1-n { position: absolute; left: 0; right: 0; top: 380px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 300px; line-height: 1; color: #ffe14a; -webkit-text-stroke: 18px #1a0f08; paint-order: stroke fill; text-shadow: 0 0 70px #ff9a1a; }
    #e1-a { top: 720px; font-size: 96px; background: #ff2e7e; transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(255,46,126,.7); }
    #e1-b { top: 880px; font-size: 64px; background: #00b8f0; box-shadow: 0 0 0 7px #1a0f08, 0 12px 0 rgba(0,0,0,.3), 0 0 50px 12px rgba(0,200,255,.6); }""",
"""      <div id="e1-dim" data-layout-ignore></div>
      <div id="e1-rv" data-layout-ignore></div>
      <div id="e1-fl" data-layout-ignore></div>
      <div id="e1-n" data-layout-ignore>0</div>
      <div id="e1-a" class="big">👥 MENSCHEN</div>
      <div id="e1-b" class="pl">wohnen schon in Muschel-Tal! 🏝️</div>""",
"""      const me = at("L1", "Menschen"), wo = at("L1", "wohnen");
      tl.fromTo("#e1-rv", { opacity: .45 }, { opacity: 1, duration: .14, yoyo: true, repeat: 15, ease: "sine.inOut", immediateRender: false }, 0);
      count(tl, "#e1-n", 0, 787, 0, me - .05, "", "", "power2.out");
      tl.fromTo("#e1-n", { scale: .6 }, { scale: 1, duration: me, ease: "power2.out", immediateRender: true }, 0);
      tl.fromTo("#e1-fl", { opacity: .9 }, { opacity: 0, duration: .4, immediateRender: false }, me - .05);
      tl.to("#e1-n", { scale: 1.12, duration: .1, yoyo: true, repeat: 1 }, me - .05);
      tl.to("#e1-n", { x: 14, duration: .04, yoyo: true, repeat: 7, ease: "none" }, me);
      tl.fromTo("#e1-a", { opacity: 0, scale: 3.4 }, { opacity: 1, scale: 1, duration: .26, ease: "back.out(1.8)" }, me - .1);
      tl.fromTo("#e1-b", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, wo - .1);
      tl.to("#e1-b", { scale: 1.06, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, wo + .3);""", blur=True)

# s02 – Alle Bewohner auf einer viel zu kleinen Insel → plötzlich modernisiert und vergrößert
import csv as _csv, math as _m, random as _r
FIG = ["🧍🏻‍♀️", "🧍🏽‍♂️", "🧍🏼", "🧍🏿‍♀️", "🧍🏻‍♂️", "🧍🏾", "🧍🏼‍♀️", "🧍🏽", "💃🏻", "🕺🏽", "🧍🏿‍♂️", "🧍🏻"]
EW = [r["name"] for r in _csv.DictReader(open(Path(__file__).resolve().parents[3] / "muscheltal/daten/einwohner.csv"))]
_rg = _r.Random(7); CX, CY = 540, 760
SMALL, BIG2 = [], []
for k, n in enumerate(EW):
    a = _rg.random() * 6.283; rr = _m.sqrt(_rg.random())
    if k % 37 == 0: rr = 1.15 + _rg.random() * .25          # ein paar purzeln ins Wasser
    SMALL.append((CX + _m.cos(a) * rr * 175, CY + _m.sin(a) * rr * 120))
cols = 22
for k in range(len(EW)):
    while True:
        gx, gy = _rg.uniform(-1, 1), _rg.uniform(-1, 1)
        if gx * gx + gy * gy < .93: break
    BIG2.append((CX + gx * 470, CY + gy * 440))
BLD = [("🏰", 540, 360, 90), ("🎡", 250, 470, 70), ("🏨", 830, 470, 70), ("🌴", 110, 760, 60), ("🌴", 970, 760, 60), ("🎢", 260, 1110, 66), ("🏟️", 820, 1110, 66)]
scene("s02", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #i2-sea { position: absolute; inset: 0; background: radial-gradient(circle at 50% 40%, #3fd3e0, #0b7fae 70%, #075a86); }
    .wv { position: absolute; left: -100px; right: -100px; height: 10px; border-radius: 6px; background: rgba(255,255,255,.22); }
    #i2-isl { position: absolute; left: 340px; top: 620px; width: 400px; height: 280px; border-radius: 50%; background: radial-gradient(circle at 50% 45%, #7fd36a 0 58%, #f4dc9a 60% 74%, #8fe3ec 76%); box-shadow: 0 0 0 10px rgba(255,255,255,.35); }
    #i2-big { position: absolute; left: 30px; top: 290px; width: 1020px; height: 940px; border-radius: 48% 52% 50% 50%; background: radial-gradient(circle at 50% 45%, #7fd36a 0 70%, #f4dc9a 72% 84%, #8fe3ec 86%); box-shadow: 0 0 0 12px rgba(255,255,255,.35); opacity: 0; }
    #i2-grid { position: absolute; left: 130px; top: 380px; width: 820px; height: 760px; border-radius: 50%; background: repeating-linear-gradient(0deg, rgba(200,170,120,.55) 0 8px, transparent 8px 70px), repeating-linear-gradient(90deg, rgba(200,170,120,.55) 0 8px, transparent 8px 70px); opacity: 0; }
    .nm b { display: block; font-size: 30px; line-height: 1; text-align: center; margin-bottom: -1px; }
    .nm { position: absolute; transform: translate(-50%, -50%); text-align: center; padding: 0 3px 1px; border-radius: 6px; background: rgba(255,255,255,.7); box-shadow: 0 1px 0 rgba(0,0,0,.25); font-family: "Inter", sans-serif; font-weight: 800; font-size: 11px; color: #2a1b12; white-space: nowrap; }
    .bd { position: absolute; transform: translate(-50%, -50%); line-height: 1; opacity: 0; z-index: 3; filter: drop-shadow(0 8px 0 rgba(0,0,0,.3)) drop-shadow(0 0 18px rgba(255,255,255,.9)); }
    #i2-k { top: 170px; font-size: 64px; background: #e8101e; transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 50px 14px rgba(255,20,30,.6); }
    #i2-u { top: 170px; font-size: 76px; background: linear-gradient(135deg, #2e9e5b, #8be06a); transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(120,255,140,.6); }
    #i2-fl { position: absolute; inset: 0; background: #fff; opacity: 0; }
    #i2-rv { position: absolute; inset: 0; box-shadow: inset 0 0 150px 60px rgba(255,10,20,.95); opacity: 0; z-index: 5; }
    #i2-n { top: 170px; font-size: 80px; background: #ffe14a; color: #1a0f08; transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(255,225,74,.7); }
    #i2-q { top: 150px; font-size: 76px; background: linear-gradient(135deg, #ffb21a, #ff2e7e); transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(255,120,60,.6); }
    #i2-w { top: 1260px; font-size: 44px; background: #fff; color: #2a1b12; z-index: 4; }""",
"""      <div id="i2-sea" data-layout-ignore></div>
      """ + "".join(f'<div class="wv" data-layout-ignore style="top:{y}px"></div>' for y in (180, 330, 1290, 1450, 1620)) + """
      <div id="i2-big" data-layout-ignore></div><div id="i2-grid" data-layout-ignore></div>
      <div id="i2-isl" data-layout-ignore></div>
      """ + "".join(f'<div class="bd" id="i2-b{k}" data-layout-ignore style="left:{x}px;top:{y}px;font-size:{int(s * 1.45)}px">{e}</div>' for k, (e, x, y, s) in enumerate(BLD)) + """
      <div id="i2-names" data-layout-ignore>""" + "".join(f'<div class="nm" id="nm{k}" style="left:{x:.0f}px;top:{y:.0f}px"><b>{FIG[k % len(FIG)]}</b>@{n}</div>' for k, (n, (x, y)) in enumerate(zip(EW, SMALL))) + """</div>
      <div id="i2-fl" data-layout-ignore></div>
      <div id="i2-rv" data-layout-ignore></div>
      <div id="i2-n" class="big">👥 785 MENSCHEN</div>
      <div id="i2-k" class="big">😱 VIEL ZU KLEIN!</div>
      <div id="i2-u" class="big">⚡ UPGRADE!</div>
      <div id="i2-q" class="big">👀 SIEHST DU DICH?</div>
      <div id="i2-w" class="pl">💬 Nicht? Kommentiere: „Wo bin ich?“</div>""",
"""      const t2 = 0, kl = at("L1k", "klein"), up = at("L2b", "Upgrade");
      const BX = """ + json.dumps([[round(x - sx), round(y - sy)] for (x, y), (sx, sy) in zip(BIG2, SMALL)]) + """;
      tl.set("#i2-names", { opacity: 1 }, 0);
      tl.to("#i2-names", { x: 4, duration: .05, yoyo: true, repeat: 30, ease: "none" }, .5);
      tl.fromTo("#i2-rv", { opacity: .35 }, { opacity: 1, duration: .16, yoyo: true, repeat: Math.max(1, Math.round((kl + .9) / .16)), ease: "sine.inOut", immediateRender: true }, 0);
      tl.fromTo("#i2-n", { opacity: 1, scale: 1.3 }, { opacity: 1, scale: 1, duration: .25, ease: "expo.out", immediateRender: true }, 0);
      tl.to("#i2-n", { x: 10, duration: .05, yoyo: true, repeat: 9, ease: "none" }, .3);
      tl.to("#i2-n", { opacity: 0, scale: .5, duration: .18 }, kl - .3);
      tl.fromTo("#i2-k", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .26, ease: "back.out(1.8)" }, kl - .15);
      tl.to("#i2-k", { x: 12, duration: .04, yoyo: true, repeat: 9, ease: "none" }, kl + .15);
      tl.to("#i2-k", { opacity: 0, scale: .4, duration: .2 }, up - .25);
      tl.fromTo("#i2-fl", { opacity: 1 }, { opacity: 0, duration: .5, immediateRender: false }, up - .05);
      tl.to("#i2-isl", { opacity: 0, scale: 2.5, duration: .4, ease: "power2.out" }, up - .05);
      tl.fromTo("#i2-big", { opacity: 0, scale: .35 }, { opacity: 1, scale: 1, duration: .55, ease: "back.out(1.6)" }, up - .05);
      tl.fromTo("#i2-grid", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .55, ease: "back.out(1.6)" }, up + .05);
      for (let k = 0; k < BX.length; k++) tl.to("#nm" + k, { x: BX[k][0], y: BX[k][1], duration: .7, ease: "power3.out" }, up + (k % 50) * .004);
      """ + "\n      ".join(f'tl.fromTo("#i2-b{k}", {{ opacity: 0, scale: .2, y: -60 }}, {{ opacity: 1, scale: 1, y: 0, duration: .35, ease: "back.out(2.4)" }}, up + .3 + {k * .06:.2f});' for k in range(len(BLD))) + """
      tl.fromTo("#i2-u", { opacity: 0, scale: 3.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, up - .1);
      tl.to("#i2-u", { scale: 1.07, duration: .16, yoyo: true, repeat: 3, ease: "sine.inOut" }, up + .3);
      const sd = at("L2c", "Siehst"), wb = at("L2c", "Wo");
      tl.to("#i2-u", { opacity: 0, scale: .5, duration: .2 }, sd - .25);
      tl.fromTo("#i2-q", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, sd - .1);
      tl.to("#i2-q", { scale: 1.07, duration: .16, yoyo: true, repeat: 9, ease: "sine.inOut" }, sd + .3);
      tl.fromTo("#i2-w", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, wb - .2);
      tl.to("#i2-w", { scale: 1.08, duration: .18, yoyo: true, repeat: 7, ease: "sine.inOut" }, wb + .3);""")

# s03 – Folg mir und zieh mit auf die Inseln (Einwohnerliste im Hintergrund)
scene("s03", LILITA + "\n    " + PILL + "\n" + FOLLOW + "\n    " + CF_CSS.replace("top: 700px", "top: 760px") + """
    #e5-btn { top: 260px; } #e5-hand { left: 690px; top: 310px; }
    #e5-hut { position: absolute; left: 0; right: 0; margin: 0 auto; top: 440px; width: 420px; text-align: center; }
    #e5-hut .e { font-size: 230px; line-height: 1; filter: drop-shadow(0 12px 0 rgba(0,0,0,.25)); }
    #e5-hut .n { display: inline-block; margin-top: -10px; padding: 6px 26px 10px; border-radius: 18px; background: #fff; box-shadow: 0 0 0 5px #1a0f08; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #e8467c; }""",
"""      <div id="e5-dim" data-layout-ignore style="position:absolute;inset:0;background:rgba(10,12,40,.55)"></div>
      <div id="e5-btn" class="fbtn">+ Folgen<div id="e5-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="e5-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="e5-hut"><div class="e">🛖</div><div class="n" id="e5-name">@Dein Name?</div></div>
      <div id="e5-cf"></div>""",
"""      const t5 = line("L3")[0], fo = at("L3", "Folg"), he = at("L3", "Inseln");
      tl.fromTo("#e5-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, t5 - .2);
      tl.fromTo("#e5-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo);
      tl.to("#e5-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .3);
      tl.to("#e5-btn2", { opacity: 1, duration: .05 }, fo + .4);
      tl.to("#e5-hand", { opacity: 0, duration: .2 }, fo + .8);
      tl.fromTo("#e5-hut", { opacity: 0, scale: .2, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: .35, ease: "back.out(2.2)" }, fo + .45);
      tl.to("#e5-name", { scale: 1.1, duration: .18, yoyo: true, repeat: 7, ease: "sine.inOut" }, he);
      { """ + CONF_JS.replace("SEED", "55").replace("BOX", "e5-cf").replace("T0", "(fo + .45)") + """ }""")

# s04 – Ziel 1.000: kostenloses eigenes Spiel
F6 = [("🗺️", "Welt erkunden", "#2e9e5b", "erkunden"), ("🎨", "Dekorieren", "#ffb21a", "dekorieren"), ("🐶", "Haustiere holen", "#e8467c", "Haustiere"), ("👯", "Freunde finden", "#7b3fe0", "Freunde"), ("✨", "und mehr!", "#00b8f0", "mehr")]
scene("s04", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #g4-dim { position: absolute; inset: 0; background: rgba(10,12,40,.55); opacity: 0; }
    #g4-fl { position: absolute; inset: 0; background: #fff; opacity: 0; }
    #g4-n { position: absolute; left: 0; right: 0; top: 160px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 230px; line-height: 1; color: #ffe14a; -webkit-text-stroke: 16px #1a0f08; paint-order: stroke fill; text-shadow: 0 0 60px #ffb21a; opacity: 0; }
    #g4-l { top: 410px; font-size: 46px; background: #fff; color: #2a1b12; }
    #g4-s { top: 520px; font-size: 66px; background: linear-gradient(135deg, #ff2e9a, #7b3fe0); transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(255,46,154,.65); }
    .fc { position: absolute; width: 440px; height: 190px; border-radius: 28px; background: #fff; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.3); overflow: hidden; opacity: 0; }
    .fc .fe { height: 120px; display: grid; place-items: center; font-size: 84px; background: linear-gradient(180deg, #bfefff, #fff); }
    .fc .fl { height: 70px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 38px; color: #fff; }""",
"""      <div id="g4-dim" data-layout-ignore></div><div id="g4-fl" data-layout-ignore></div>
      <div id="g4-n" data-layout-ignore>1.000</div>
      <div id="g4-l" class="pl">🏝️ Bewohner – dann gibt's</div>
      <div id="g4-s" class="big">🎮 DEIN GRATIS-SPIEL!</div>
      """ + "".join(f'<div class="fc" id="g4-c{i}" style="left:{(320 if i == 4 else 80 + (i % 2) * 480)}px;top:{670 + (i // 2) * 220}px"><div class="fe">{e}</div><div class="fl" style="background:{c}">{n}</div></div>' for i, (e, n, c, k) in enumerate(F6)),
"""      const t4 = line("L4")[0], n1 = at("L4", "1.000"), sp = at("L4", "Spiel");
      tl.fromTo("#g4-dim", { opacity: 0 }, { opacity: 1, duration: .3 }, t4 - .2);
      tl.fromTo("#g4-n", { opacity: 0, scale: 4, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .25, ease: "expo.out" }, n1 - .1);
      tl.to("#g4-n", { scale: 1.07, duration: .16, yoyo: true, repeat: 7, ease: "sine.inOut" }, n1 + .3);
      tl.fromTo("#g4-l", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, n1 + .3);
      tl.fromTo("#g4-fl", { opacity: .9 }, { opacity: 0, duration: .35, immediateRender: false }, sp);
      tl.fromTo("#g4-s", { opacity: 0, scale: 3.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, sp - .1);
      tl.to("#g4-s", { x: 12, duration: .04, yoyo: true, repeat: 9, ease: "none" }, sp + .2);
      """ + "\n      ".join(f'tl.fromTo("#g4-c{i}", {{ opacity: 0, scale: .3, rotation: {(-8, 8, -8, 8, 0)[i]} }}, {{ opacity: 1, scale: 1, rotation: 0, duration: .3, ease: "back.out(2.4)" }}, at("L4b", "{k}") - .15); tl.to("#g4-c{i}", {{ scale: 1.06, duration: .16, yoyo: true, repeat: 3, ease: "sine.inOut" }}, at("L4b", "{k}") + .2);' for i, (e, n, c, k) in enumerate(F6)), blur=False)
