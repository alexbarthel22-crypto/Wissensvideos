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


# s01 – Countdown 3 – 2 – 1 (riesig), dann „WER WIRD UNSER TÜRSTEHER?“ – Club oben frei
QL = [[("GTA-6-FIEBER", "GTA")], [("AUF", "auf")], [("MUSCHEL-TAL!", "Muschel")]]
QW = [w for ln in QL for w in ln]
YW = ()
CT0 = ["0", 'at("L1", "zwei") - .08', 'at("L1", "eins") - .08']
CT1 = ['at("L1", "zwei") - .1', 'at("L1", "eins") - .1', "wr - .26"]
CD = [("3", "Drei", "#ff2e7e"), ("2", "zwei", "#00e5ff"), ("1", "eins", "#ffe500")]
FW = [(7, [(200, 180), (880, 220), (540, 420)]), (8, [(120, 520), (960, 380), (420, 200), (700, 560)]), (9, [(300, 300), (800, 160), (540, 640), (980, 640)]), (10, [(180, 420), (640, 240), (900, 480), (420, 560), (760, 80)]), (4, [(160, 200), (920, 560)]), (5, [(880, 150), (150, 520)]), (6, [(540, 120), (260, 300), (820, 260)]), (0, [(230, 330), (850, 260), (560, 520)]), (1, [(820, 380), (200, 230), (540, 160)]), (2, [(300, 420), (780, 300), (180, 650), (900, 620)]), (3, [(540, 260), (220, 480), (860, 470), (380, 140), (700, 130)])]
FWC = ["#ff2e9a", "#00e5ff", "#ffe500", "#7cff6a", "#b46bff", "#ff8a1a", "#ffffff"]
SP = [(30, 930, 70), (985, 960, 60), (20, 1230, 52), (1000, 1260, 66), (50, 1520, 48), (975, 1540, 56), (470, 880, 44)]
scene("s01", LILITA + "\n    " + CF_CSS.replace("top: 700px", "top: 1120px") + """
    #s01-hk { position: absolute; left: 20px; right: 20px; top: 960px; text-align: center; font-family: "Lilita One", sans-serif; }
    #s01-hk .ln { display: block; width: fit-content; margin: 0 auto 16px; padding: 4px 34px 14px; border-radius: 30px; line-height: 1.05; white-space: nowrap; transform-origin: 50% 60%; opacity: 0; }
    #s01-hk #s01-l2 { background: #111; font-size: 140px; box-shadow: 0 0 0 8px #00e5ff, 0 14px 0 rgba(0,0,0,.4), 0 0 60px 16px rgba(0,229,255,.75); }
    #s01-hk #s01-l1 { background: #00b8f0; font-size: 120px; box-shadow: 0 0 0 7px #1a0f08, 0 12px 0 rgba(0,0,0,.4), 0 0 50px 12px rgba(0,200,255,.6); }
    #s01-hk #s01-l0 { background: #ffe500; font-size: 118px; box-shadow: 0 0 0 8px #1a0f08, 0 14px 0 rgba(0,0,0,.4), 0 0 60px 18px rgba(255,229,0,.75); }
    #s01-hk #s01-l0 span { color: #1a0f08; -webkit-text-stroke: 0; }
    #s01-hk #s01-l2 span { color: #ffe500; }
    #s01-hk span { position: relative; display: inline-block; margin: 0 .08em; color: #fff; -webkit-text-stroke: 8px #1a0f08; paint-order: stroke fill; transform-origin: 50% 65%; }
    .cd { position: absolute; left: 0; right: 0; top: 760px; height: 760px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 720px; line-height: 760px; color: #fff; -webkit-text-stroke: 26px #1a0f08; paint-order: stroke fill; opacity: 0; }
    #s01-rv { position: absolute; inset: 0; box-shadow: inset 0 0 140px 50px rgba(255,10,20,.9); opacity: 0; }
    #s01-bu { position: absolute; left: -310px; top: 560px; width: 1700px; height: 1700px; border-radius: 50%; background: repeating-conic-gradient(rgba(255,240,120,.55) 0 7deg, rgba(255,255,255,0) 7deg 18deg); -webkit-mask: radial-gradient(circle, #000 18%, transparent 52%); opacity: 0; }
    #s01-gl { position: absolute; left: 40px; right: 40px; top: 940px; height: 640px; border-radius: 50%; background: radial-gradient(closest-side, rgba(255,230,60,.55), rgba(255,60,160,.25) 60%, rgba(255,60,160,0)); opacity: 0; }
    .s01-sp { position: absolute; color: #fff; text-shadow: 0 0 18px #fff, 0 0 34px #ffe14a; opacity: 0; line-height: 1; }
    .fw { position: absolute; width: 14px; height: 14px; margin: -7px 0 0 -7px; border-radius: 50%; opacity: 0; }
    .fwr { position: absolute; width: 10px; height: 10px; margin: -5px 0 0 -5px; border-radius: 50%; background: #fff; box-shadow: 0 0 14px 6px #fff; opacity: 0; }
    .cw { position: absolute; inset: 0; opacity: 0; mix-blend-mode: screen; }
    .cdg { position: absolute; left: 0; right: 0; top: 760px; height: 760px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 720px; line-height: 760px; color: transparent; -webkit-text-stroke: 10px #fff; opacity: 0; }
    .spt { position: absolute; bottom: -200px; width: 380px; height: 2300px; transform-origin: 50% 100%; background: linear-gradient(0deg, rgba(255,255,255,.35), rgba(255,255,255,0) 85%); clip-path: polygon(42% 100%, 58% 100%, 100% 0, 0 0); mix-blend-mode: screen; opacity: 0; }
    .cc { position: absolute; width: 18px; height: 30px; border-radius: 4px; opacity: 0; }
    .gld { position: absolute; width: 10px; height: 10px; border-radius: 50%; background: #ffe14a; box-shadow: 0 0 10px 4px #ffd23f; opacity: 0; }
    #s01-fin { position: absolute; left: 0; right: 0; top: 0; text-align: center; opacity: 0; }
    .shk { position: absolute; left: 290px; top: 890px; width: 500px; height: 500px; border-radius: 50%; border: 18px solid #fff; opacity: 0; }
    #s01-fl { position: absolute; inset: 0; background: radial-gradient(circle at 50% 70%, rgba(255,255,255,.9), rgba(255,255,255,0) 55%); opacity: 0; }""",
"""      <div id="s01-bu" data-layout-ignore></div>
      <div id="s01-gl" data-layout-ignore></div>
      """ + "".join(f'<div class="s01-sp" id="s01-sp{k}" data-layout-ignore style="left:{x}px;top:{y}px;font-size:{f}px">✦</div>' for k, (x, y, f) in enumerate(SP)) + """
      """ + "".join(f'<div class="cd" id="s01-cd{k}" data-layout-ignore style="text-shadow: 0 0 60px {c}, 0 0 120px {c}">{n}</div>' for k, (n, w, c) in enumerate(CD)) + """
      """ + "".join(f'<div class="fwr" id="s01-r{b}-{j}" data-layout-ignore style="left:{x}px;top:{y}px"></div>' + "".join(f'<div class="fw" id="s01-f{b}-{j}-{q}" data-layout-ignore style="left:{x}px;top:{y}px;background:{FWC[(j * 3 + q) % 7]};box-shadow:0 0 12px 4px {FWC[(j * 3 + q) % 7]}"></div>' for q in range(22)) for b, pts in FW for j, (x, y) in enumerate(pts)) + "".join(f'<div class="shk" id="s01-sh{k}" data-layout-ignore style="border-color:{c};box-shadow:0 0 40px 10px {c}"></div>' for k, (n, w, c) in enumerate(CD)) + """
      """ + "".join(f'<div class="cw" id="s01-cw{k}" data-layout-ignore style="background: radial-gradient(circle at 50% 60%, {c}, transparent 75%)"></div>' + "".join(f'<div class="cdg" id="s01-g{k}-{g}" data-layout-ignore style="-webkit-text-stroke-color:{c}">{n}</div>' for g in range(2)) for k, (n, w, c) in enumerate(CD)) + """
      <div class="spt" id="s01-sp-l" data-layout-ignore style="left:-60px"></div><div class="spt" id="s01-sp-r" data-layout-ignore style="right:-60px"></div>
      """ + "".join(f'<div class="cc" id="s01-cc{q}" data-layout-ignore style="left:{-10 if q % 2 == 0 else 1070}px;top:1900px;background:{FWC[q % 7]}"></div>' for q in range(90)) + "".join(f'<div class="gld" id="s01-gd{q}" data-layout-ignore style="left:{(q * 137) % 1060 + 10}px;top:-30px"></div>' for q in range(50)) + """
      <div id="s01-cfx"></div>
      <div id="s01-fl" data-layout-ignore></div>
      <div id="s01-rv" data-layout-ignore></div>
      <div id="s01-hk">""" + "".join('<div class="ln" id="s01-l' + str(j) + '">' + "".join(f'<span id="s01-w{QW.index(w)}">{w[0]}</span>' for w in ln) + '</div>' for j, ln in enumerate(QL)) + """</div>""",
"""      const ts = at("L1", "Muschel"), wr = at("L1", "GTA");
      tl.fromTo("#s01-bu", { opacity: .9, scale: .6, rotation: 0 }, { opacity: .9, scale: 1, rotation: 70, duration: 3.2, ease: "none", immediateRender: true }, 0);
      tl.fromTo("#s01-gl", { opacity: .6 }, { opacity: 1, duration: .25, yoyo: true, repeat: 11, ease: "sine.inOut", immediateRender: true }, 0);
      tl.fromTo("#s01-rv", { opacity: .45 }, { opacity: 1, duration: .14, yoyo: true, repeat: 17, ease: "sine.inOut", immediateRender: false }, 0);
      """ + "\n      ".join(f'tl.fromTo("#s01-sp{k}", {{ opacity: 0, scale: .2, rotation: 0 }}, {{ opacity: 1, scale: 1.2, rotation: 90, duration: .22, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {k * .13:.2f});' for k in range(len(SP))) + """
      """ + "\n      ".join(
        (f'{{ const t0 = {CT0[k]}, t1 = {CT1[k]};'
         f' tl.fromTo("#s01-cd{k}", {{ opacity: {"1" if k == 0 else "0"}, scale: {"1.5" if k == 0 else "3.6"}, rotation: {(-14, 18, -22)[k]}, filter: "blur({"0" if k == 0 else "18"}px) brightness(2)" }}, {{ opacity: 1, scale: 1, rotation: 0, filter: "blur(0px) brightness(1)", duration: .2, ease: "expo.out", immediateRender: {"true" if k == 0 else "false"} }}, t0);'
         f' tl.to("#s01-cd{k}", {{ scale: 1.12, duration: .12, yoyo: true, repeat: 3, ease: "sine.inOut" }}, t0 + .22);'
         f' tl.fromTo("#s01-cw{k}", {{ opacity: .85 }}, {{ opacity: 0, duration: .45, ease: "power2.out", immediateRender: false }}, t0);'
         f' tl.fromTo("#s01-g{k}-0", {{ opacity: .9, scale: 1 }}, {{ opacity: 0, scale: 1.9, duration: .45, ease: "power2.out", immediateRender: false }}, t0 + .05);'
         f' tl.fromTo("#s01-g{k}-1", {{ opacity: .7, scale: 1 }}, {{ opacity: 0, scale: 2.6, duration: .6, ease: "power2.out", immediateRender: false }}, t0 + .15);'
         f' tl.fromTo("#s01-stage", {{ scale: 1.07 }}, {{ scale: 1, duration: .3, ease: "power2.out", immediateRender: false }}, t0);'
         f' tl.to("#s01-cd{k}", {{ rotation: {(-5, 6, -7)[k]}, duration: .1, yoyo: true, repeat: 3, ease: "sine.inOut" }}, t0 + .25);'
         f' tl.fromTo("#s01-sh{k}", {{ opacity: 1, scale: .2 }}, {{ opacity: 0, scale: 2.6, duration: .55, ease: "power2.out", immediateRender: false }}, t0 + .02);'
         f' tl.fromTo("#s01-bu", {{ scale: 1.25 }}, {{ scale: 1, duration: .4, ease: "power2.out", immediateRender: false }}, t0);'
         f' tl.fromTo("#s01-fl", {{ opacity: .85 }}, {{ opacity: 0, duration: .3, immediateRender: false }}, t0);'
         f' tl.to("#s01-cd{k}", {{ x: 14, duration: .04, yoyo: true, repeat: 5, ease: "none" }}, t0 + .08);'
         f' tl.to("#s01-cd{k}", {{ opacity: 0, scale: .6, duration: .1, ease: "power2.in" }}, t1); }}')
        for k, (n, w, c) in enumerate(CD)) + """
      """ + "\n      ".join(
        f'tl.fromTo("#s01-l{j}", {{ opacity: 0, scaleX: .1 }}, {{ opacity: 1, scaleX: 1, duration: .14, ease: "back.out(2.4)" }}, at("L1", "{ln[0][1]}") - .16);'
        f' tl.fromTo("#s01-l{j}", {{ filter: "brightness(2.3) saturate(1.4)" }}, {{ filter: "brightness(1) saturate(1)", duration: .4, ease: "power2.out", immediateRender: false }}, at("L1", "{ln[0][1]}"));'
        f' tl.to("#s01-l{j}", {{ filter: "brightness(1.35)", duration: .16, yoyo: true, repeat: 7, ease: "sine.inOut" }}, at("L1", "{ln[0][1]}") + .45);'
        for j, ln in enumerate(QL)) + """
      """ + "\n      ".join(
        (f'tl.fromTo("#s01-w{i}", {{ opacity: 0, x: {(-1 if i % 2 == 0 else 1) * 1300}, scale: 2.4, rotation: {(-1 if i % 2 == 0 else 1) * 30}, filter: "blur(12px)" }}, {{ opacity: 1, x: 0, scale: 1, rotation: 0, filter: "blur(0px)", duration: .17, ease: "expo.out" }}, at("L1", "{k}") - .14);'
         if w != "MUSCHEL-TAL!" else
         f'tl.fromTo("#s01-w{i}", {{ opacity: 0, scale: 5, filter: "blur(16px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: .2, ease: "expo.out" }}, at("L1", "{k}") - .16);')
        + f' tl.to("#s01-hk", {{ y: 14, duration: .05, yoyo: true, repeat: 1, ease: "none" }}, at("L1", "{k}") + .03);'
        for i, (w, k) in enumerate(QW)) + """
      tl.fromTo("#s01-fl", { opacity: .9 }, { opacity: 0, duration: .4, immediateRender: false }, ts);
      tl.fromTo("#s01-sp-l", { opacity: .9, rotation: 35 }, { opacity: .9, rotation: -10, duration: .4, yoyo: true, repeat: 6, ease: "sine.inOut", immediateRender: true }, 0);
      tl.fromTo("#s01-sp-r", { opacity: .9, rotation: -35 }, { opacity: .9, rotation: 10, duration: .4, yoyo: true, repeat: 6, ease: "sine.inOut", immediateRender: true }, 0);
      tl.to(["#s01-sp-l", "#s01-sp-r"], { opacity: 0, duration: .3 }, wr + .6);
      { const R = rng(31); const TB = [0, at("L1", "zwei") - .08, at("L1", "eins") - .08, wr - .05, .4, at("L1", "zwei") + .38, at("L1", "eins") + .3, wr + .2, wr + .45, wr + .75, wr + 1.05];
      """ + "\n      ".join(f'{{ const T = TB[{b}] + {j * .07:.2f}; tl.fromTo("#s01-r{b}-{j}", {{ opacity: 1, y: {380 + j * 40}, scale: .6 }}, {{ y: 0, scale: 1, duration: .2, ease: "power2.out", immediateRender: false }}, Math.max(0, T - .2)); tl.to("#s01-r{b}-{j}", {{ opacity: 0, scale: 3, duration: .12 }}, T);'
        + "".join(f' {{ const a = {q} / 22 * Math.PI * 2 + R() * .3, v = 170 + R() * 150; tl.fromTo("#s01-f{b}-{j}-{q}", {{ opacity: 1, x: 0, y: 0, scale: 1.2 }}, {{ x: Math.cos(a) * v, y: Math.sin(a) * v, scale: .9, duration: .45, ease: "power3.out", immediateRender: false }}, T); tl.to("#s01-f{b}-{j}-{q}", {{ y: "+=120", opacity: 0, scale: .3, duration: .55, ease: "power1.in" }}, T + .45); }}' for q in range(22)) + ' }' for b, pts in FW for j, (x, y) in enumerate(pts)) + """ }
      { const R2 = rng(97); for (let q = 0; q < 90; q++) { const L = q % 2 === 0, T = wr + (q % 30) * .012, vx = (L ? 1 : -1) * (250 + R2() * 520), vy = -(1100 + R2() * 700);
          tl.fromTo("#s01-cc" + q, { opacity: 1, x: 0, y: 0, rotation: 0 }, { x: vx, y: vy, rotation: (R2() - .5) * 900, duration: .55, ease: "power3.out", immediateRender: false }, T);
          tl.to("#s01-cc" + q, { y: vy + 900, x: vx * 1.25, rotation: "+=" + Math.round((R2() - .5) * 600), opacity: 0, duration: 1.4, ease: "power1.in" }, T + .55); }
        for (let q = 0; q < 50; q++) { const T = wr + .1 + R2() * .9; tl.fromTo("#s01-gd" + q, { opacity: 1, y: 0 }, { y: 1500 + R2() * 600, duration: 1.6 + R2() * .8, ease: "none", immediateRender: false }, T); tl.to("#s01-gd" + q, { opacity: 0, duration: .3 }, T + 1.4); } }
      tl.fromTo("#s01-fl", { opacity: 1 }, { opacity: 0, duration: .5, immediateRender: false }, wr - .02);
      tl.fromTo("#s01-stage", { scale: 1.1 }, { scale: 1, duration: .45, ease: "power2.out", immediateRender: false }, wr - .02);
      tl.to("#s01-stage", { x: 14, duration: .04, yoyo: true, repeat: 11, ease: "none" }, wr);
      """ + "\n      ".join(f'tl.fromTo("#s01-cw{k}", {{ opacity: .7 }}, {{ opacity: 0, duration: .35, ease: "power2.out", immediateRender: false }}, wr + {k * .22:.2f});' for k in range(3)) + """
      { """ + CONF_JS.replace("SEED", "77").replace("BOX", "s01-cfx").replace("T0", "(wr - .05)") + """ }
      tl.to("#s01-l0", { scale: 1.05, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, wr + .3); tl.to("#s01-l2", { scale: 1.05, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, ts + .3);
      tl.to("#s01-hk", { x: 16, duration: .04, yoyo: true, repeat: 7, ease: "none" }, ts + .05);""")

# s01b – Das ist Muschel-Tal: die Welt, in der ihr alles entscheidet
scene("s01b", LILITA + "\n    " + PILL + """
    #s1b-lg { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 300px; font-family: "Lilita One", sans-serif; font-size: 150px; line-height: 1; color: #fff; -webkit-text-stroke: 16px #1a0f08; paint-order: stroke fill; filter: drop-shadow(0 12px 0 rgba(0,0,0,.3)); }
    #s1b-lg b { font-weight: 400; color: #ffe14a; }
    #s1b-e { top: 480px; font-size: 50px; background: linear-gradient(100deg, #ff2e7e, #7b3fe0); }""",
"""      <div id="s1b-lg" data-layout-ignore>MUSCHEL-<b>TAL</b></div>
      <div id="s1b-e" class="pl">🏠 Folgen = Hütte mit deinem @Namen</div>""",
"""      const t0 = line("L1b")[0], mu = at("L1b", "Muschel-Tal"), en = at("L1b", "Hütte");
      tl.fromTo("#s1b-lg", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(1.8)" }, mu - .15);
      tl.fromTo("#s1b-e", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, en - .2);
      tl.to("#s1b-e", { scale: 1.08, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut" }, en + .3);""")


SLOT_CSS = """    .sl-dim { position: absolute; inset: 0; background: rgba(10,12,40,.5); }
    .sl-box { position: absolute; left: 190px; width: 700px; top: 480px; height: 390px; border-radius: 34px; background: #fff; overflow: hidden; box-shadow: 0 0 0 7px #2a1b12, 0 0 0 14px #ffc93c, 0 0 0 19px #2a1b12, 0 18px 0 rgba(0,0,0,.35); }
    .sl-band { position: absolute; left: 0; right: 0; top: 130px; height: 130px; background: #fff3c4; border-top: 5px solid #ffc93c; border-bottom: 5px solid #ffc93c; }
    .sl-col { position: absolute; left: 0; right: 0; top: 0; }
    .sl-r { height: 130px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #23285a; white-space: nowrap; }
    .sl-sh { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,.95)); }
    .sl-fv { position: absolute; left: 60px; width: 960px; top: 905px; text-align: center; white-space: nowrap; font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; color: #fff; text-shadow: 0 2px 6px rgba(0,0,0,.6); }"""
def names(f): return (D.parent / "werkzeug" / f).read_text().split()
def slot_col(cid, ns): return f'<div class="sl-col" id="{cid}">' + "".join(f'<div class="sl-r" id="{cid}-{i}">@{n}</div>' for i, n in enumerate(ns)) + "</div>"
def slot_js(cid, band, ns, w, t0, tb):
    W = ns.index(w)
    return f"""      {{ const T0 = {t0}, TB = {tb}, H = 130, W = {W}, T1 = TB - 1.1;
      tl.set("#{cid}", {{ y: 0 }}, 0);
      tl.fromTo("#{cid}", {{ y: 0 }}, {{ y: -(W - 9) * H, duration: T1 - T0, ease: "none", immediateRender: false }}, T0);
      tl.fromTo("#{cid}", {{ y: -(W - 9) * H }}, {{ y: -(W - 1) * H, duration: 1.1, ease: "power3.out", immediateRender: false }}, T1);
      tl.fromTo("#{cid}", {{ filter: "blur(5px)" }}, {{ filter: "blur(0px)", duration: 1.0, ease: "power2.in", immediateRender: false }}, T1);
      tl.to("#{cid}-" + W, {{ color: "#2e9e5b", scale: 1.15, duration: .2, ease: "back.out(3)" }}, TB);
      tl.to("#{band}", {{ backgroundColor: "#7dff9e", duration: .15, yoyo: true, repeat: 5 }}, TB); }}
"""


# s02 – Türsteher-Verlosung im KOK(O)S
JT = [("L2a", "L2aw", "🎁 Du gewinnst: Job als Türsteher", "🕶️ im Kokos-Club · Kokos-Küste", "marl33n.fls_1301", "#8e2bd6")]
NST = [names("slot_2.txt")]
scene("s02", LILITA + "\n    " + PILL + "\n    " + CF_CSS.replace("top: 700px", "top: 640px") + "\n" + SLOT_CSS + """
    #st-lv { top: 280px; font-size: 52px; background: #8e2bd6; }
    #st-lv2 { top: 390px; font-size: 40px; background: #fff; color: #2a1b12; }
    .st-o { top: 250px; font-size: 54px; font-family: "Lilita One", sans-serif; font-weight: 400; }
    .st-d { top: 360px; font-size: 40px; background: #fff; color: #2a1b12; }
    #st-box { left: 60px; width: 960px; top: 470px; } #st-box .sl-r { font-size: 62px; }
    .st-w { top: 900px; font-size: 48px; background: #2e9e5b; }""",
"""      <div id="st-dim" class="sl-dim"></div>
      <div id="st-lv" class="pl">📝 Ihr habt euch beworben!</div>
      <div id="st-lv2" class="pl">🔴 Jetzt LIVE verlost</div>
      """ + "\n      ".join(f'<div id="st-o{i}" class="pl st-o" style="background:{c}">{o}</div><div id="st-d{i}" class="pl st-d">{t}</div>' for i, (a, w, o, t, n, c) in enumerate(JT)) + """
      <div id="st-box" class="sl-box"><div id="st-band" class="sl-band"></div>""" + "".join(slot_col(f"st-c{i}", NST[i]) for i in range(1)) + """<div class="sl-sh" data-layout-ignore></div></div>
      """ + "".join(f'<div id="st-cf{i}"></div>' for i in range(1)) + "\n      " + "\n      ".join(f'<div id="st-w{i}" class="pl st-w">🎉 @{n} ist unser Türsteher!</div>' for i, (a, w, o, t, n, c) in enumerate(JT)),
"""      const t3 = line("L2")[0], dk = at("L2", "beworben");
      tl.fromTo("#st-lv", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, dk - .15);
      tl.fromTo("#st-lv2", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, dk + .35);
      tl.to(["#st-lv", "#st-lv2"], { opacity: 0, duration: .2 }, line("L2a")[0] - .3);
            tl.set(["#st-box", "#st-dim"], { opacity: 0 }, 0);
""" + "".join(f"""      tl.fromTo("#st-o{i}", {{ opacity: 0, scale: 2.2 }}, {{ opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }}, line("{a}")[0] - .1);
      tl.fromTo("#st-d{i}", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }}, line("{a}")[0] + .4);
      tl.fromTo("#st-dim", {{ opacity: {0 if i == 0 else .0} }}, {{ opacity: 1, duration: .25, immediateRender: false }}, line("{a}")[1] + .05);
      tl.fromTo("#st-box", {{ opacity: 0, scale: .5 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, line("{a}")[1] + .05);
      tl.set(["#st-c0"], {{ opacity: 0 }}, line("{a}")[1]); tl.set("#st-c{i}", {{ opacity: 1 }}, line("{a}")[1]); tl.set("#st-band", {{ backgroundColor: "#fff3c4" }}, line("{a}")[1]);
""" + slot_js(f"st-c{i}", "st-band", NST[i], n, f'line("{a}")[1] + .2', f'line("{w}")[0] - .25') + "      { " + CONF_JS.replace("SEED", str(71 + i)).replace("BOX", f"st-cf{i}").replace("T0", f'(line("{w}")[0] - .25)') + " }\n" + f"""      tl.to(["#st-box", "#st-dim"], {{ opacity: 0, duration: .25 }}, line("{w}")[1] + .2);
      tl.fromTo("#st-w{i}", {{ opacity: 0, scale: .4 }}, {{ opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }}, line("{w}")[1] + .2);
      tl.to(["#st-w{i}", "#st-o{i}", "#st-d{i}"], {{ opacity: 0, duration: .2 }}, {f'line("{JT[i+1][0]}")[0] - .3' if i < 0 else f'line("{w}")[1] + 2.0'});
""" for i, (a, w, o, t, n, c) in enumerate(JT)))

# s02d – Erste Amtshandlung von Bürgermeisterin Sophia: Döner nur noch 2 €
scene("s02d", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #sd-b { top: 210px; font-size: 64px; background: #e8467c; transform: rotate(-2deg); }
    #sd-n { top: 330px; font-size: 40px; background: #fff; color: #2a1b12; }
    #sd-p { top: 210px; font-size: 76px; background: linear-gradient(135deg, #ffe14a, #ff6a1a); color: #fff; transform: rotate(-2deg); box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(255,180,40,.7); }
    .cm9 { position: absolute; left: 110px; width: 860px; padding: 10px; border-radius: 30px; background: linear-gradient(135deg, #ffe14a, #ff2e7e, #7b3fe0); box-shadow: 0 0 0 6px #1a0f08, 0 14px 0 rgba(0,0,0,.35), 0 0 50px 12px rgba(255,60,160,.6); transform: rotate(-1.5deg); }
    .cm9 img { display: block; width: 100%; border-radius: 20px; }
    .cm9-t { position: absolute; left: 30px; top: -38px; padding: 4px 20px 8px; border-radius: 16px; background: #2e9e5b; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 34px; box-shadow: 0 0 0 5px #1a0f08; transform: rotate(-2deg); white-space: nowrap; }
    #sd-c { top: 450px; }""",
"""      <div id="sd-b" class="big">🏛️ ERSTE AMTSHANDLUNG</div>
      <div id="sd-n" class="pl">Bürgermeisterin @sophia.tsnr</div>
      <div id="sd-p" class="big">🥙 DÖNER NUR 2 €!</div>
      <div id="sd-c" class="cm9"><div class="cm9-t">📜 Sophia hat entschieden:</div><img src="assets/img/sophia_amtshandlung.jpg"></div>""",
"""      const t = line("L2d")[0], dn = at("L2d", "Döner"), te = line("L2e")[0];
      tl.fromTo("#sd-b", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, t - .05);
      tl.fromTo("#sd-n", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, at("L2d", "Sophia") - .1);
      tl.fromTo("#sd-c", { opacity: 0, scale: .3, rotation: -12 }, { opacity: 1, scale: 1, rotation: -1.5, duration: .35, ease: "back.out(2.2)" }, at("L2d", "Sophia") + .3);
      tl.to(["#sd-b", "#sd-n"], { opacity: 0, y: -30, duration: .2 }, dn - .25);
      tl.fromTo("#sd-p", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, dn - .1);
      tl.to("#sd-p", { scale: 1.06, duration: .18, yoyo: true, repeat: 9, ease: "sine.inOut" }, dn + .3);
      tl.to("#sd-c", { scale: 1.03, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, te);""")

# s03g – Game Lagoon: nur das Gebäude, keine Textfelder (Kamera fährt langsam heran)
scene("s03g", LILITA, """      <div></div>""", """      """)

# s03j – 8 Jobs gleichzeitig: große Ankündigung, 8 Glücksräder auf einem Bildschirm, Gebäude im Hintergrund
J8 = [("🍬", "Kiosk Kunterbunt", "#ff6a9a"), ("🧴", "CocoCare", "#2fb3a0"), ("🧋", "Boba Beach", "#d4469c"), ("👗", "Coast & Cotton", "#7b3fe0"),
      ("🍹", "Strandbar", "#ff8a1a"), ("🍕", "Porto Pizza", "#e8433c"), ("🛒", "Meerkauf", "#1f8fd6"), ("🎮", "Game Lagoon", "#ff2e9a")]
JN = [names(f"jslot_{i}.txt") for i in range(8)]
JW = 24
scene("s03j", LILITA + "\n    " + PILL + "\n    " + BIG + "\n    " + CF_CSS.replace("top: 700px", "top: 640px") + """
    #sj-dim { position: absolute; left: 0; right: 0; top: 0; height: 1920px; background: linear-gradient(180deg, rgba(10,12,40,.65), rgba(10,12,40,.45) 85%, rgba(10,12,40,0)); opacity: 0; }
    #sj-fl { position: absolute; inset: 0; background: #fff; opacity: 0; }
    #sj-8 { position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 250px; line-height: 1; color: #ffe14a; -webkit-text-stroke: 18px #1a0f08; paint-order: stroke fill; text-shadow: 0 0 60px #ff2e9a, 0 0 120px #ffb21a; opacity: 0; }
    #sj-a { top: 640px; font-size: 62px; background: #e8101e; transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(255,30,30,.7); }
    #sj-h { top: 120px; font-size: 56px; background: linear-gradient(135deg, #ffb21a, #ff2e9a); }
    #sj-win { top: 120px; font-size: 56px; background: linear-gradient(135deg, #2e9e5b, #8be06a); }
    .jc { position: absolute; width: 500px; height: 280px; border-radius: 24px; background: #fff; overflow: hidden; box-shadow: 0 0 0 5px #1a0f08, 0 10px 0 rgba(0,0,0,.3); opacity: 0; }
    .jc .jl { height: 110px; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 38px; color: #fff; white-space: nowrap; line-height: 1.1; }
    .jc .jl small { font-size: 24px; opacity: .9; letter-spacing: .04em; }
    .jc .jw { position: relative; height: 170px; overflow: hidden; background: #fff8dc; }
    .jc .jcol { position: absolute; left: 0; right: 0; top: 0; }
    .jc .jr { height: 170px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #23285a; white-space: nowrap; }
    .jc .jsh { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,248,220,.9), rgba(255,248,220,0) 30%, rgba(255,248,220,0) 70%, rgba(255,248,220,.9)); }
    .jg { position: absolute; width: 500px; height: 280px; border-radius: 24px; box-shadow: 0 0 0 7px #ffe14a, 0 0 40px 14px rgba(255,225,74,.85); opacity: 0; }""",
"""      <div id="sj-dim" data-layout-ignore></div>
      <div id="sj-fl" data-layout-ignore></div>
      <div id="sj-8" data-layout-ignore>8 JOBS</div>
      <div id="sj-a" class="big">⚡ ALLE GLEICHZEITIG! ⚡</div>
      <div id="sj-h" class="pl">🎰 8 JOBS · 1 VERLOSUNG</div>
      <div id="sj-win" class="pl">🎉 GLÜCKWUNSCH AN ALLE 8!</div>
      """ + "".join(f'<div class="jc" id="sj-c{i}" style="left:{28 + (i % 2) * 524}px;top:{230 + (i // 2) * 296}px"><div class="jl" style="background:{c}"><small>🎁 DU GEWINNST:</small>{e} {n}</div><div class="jw"><div class="jcol" id="sj-col{i}">' + "".join(f'<div class="jr" id="sj-r{i}-{k}">@{nm}</div>' for k, nm in enumerate(JN[i])) + '</div><div class="jsh" data-layout-ignore></div></div></div>' f'<div class="jg" id="sj-g{i}" data-layout-ignore style="left:{28 + (i % 2) * 524}px;top:{230 + (i // 2) * 296}px"></div>' for i, (e, n, c) in enumerate(J8)) + """
      <div id="sj-cf"></div>""",
"""      const t8 = line("L8")[0], gr = at("L8", "Großes"), ac = at("L8", "acht"), gz = at("L8", "gleichzeitig"), te = line("L8")[1], tw = line("L8w")[0];
      tl.fromTo("#sj-dim", { opacity: 0 }, { opacity: 1, duration: .3 }, t8);
      tl.fromTo("#sj-fl", { opacity: .9 }, { opacity: 0, duration: .35, immediateRender: false }, ac);
      tl.fromTo("#sj-8", { opacity: 0, scale: 4, rotation: -10, filter: "blur(16px)" }, { opacity: 1, scale: 1, rotation: 0, filter: "blur(0px)", duration: .25, ease: "expo.out" }, ac - .1);
      tl.to("#sj-8", { x: 16, duration: .04, yoyo: true, repeat: 9, ease: "none" }, ac + .15);
      tl.to("#sj-8", { scale: 1.08, duration: .16, yoyo: true, repeat: 5, ease: "sine.inOut" }, ac + .55);
      tl.fromTo("#sj-a", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, gz - .1);
      tl.fromTo("#sj-fl", { opacity: .7 }, { opacity: 0, duration: .3, immediateRender: false }, gz);
      tl.to(["#sj-8", "#sj-a"], { opacity: 0, scale: .5, y: -200, duration: .25, ease: "power2.in" }, te + .15);
      tl.fromTo("#sj-h", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, te + .3);
      const T0 = te + .45, H = 170, W = """ + str(JW) + """, SP = (tw - .5) - T0;
      """ + "\n      ".join(
        f'tl.fromTo("#sj-c{i}", {{ opacity: 0, scale: .4 }}, {{ opacity: 1, scale: 1, duration: .25, ease: "back.out(2.2)" }}, T0 - .1 + {i * .04:.2f});'
        f' tl.fromTo("#sj-col{i}", {{ y: 0 }}, {{ y: -W * H, duration: SP * {.62 + i * .05:.2f}, ease: "power3.out", immediateRender: false }}, T0);'
        f' tl.fromTo("#sj-col{i}", {{ filter: "blur(4px)" }}, {{ filter: "blur(0px)", duration: SP * {.62 + i * .05:.2f}, ease: "power3.in", immediateRender: false }}, T0);'
        f' tl.to("#sj-r{i}-{JW}", {{ color: "#1d9e4b", scale: 1.12, duration: .15, ease: "back.out(3)" }}, T0 + SP * {.62 + i * .05:.2f});'
        f' tl.fromTo("#sj-g{i}", {{ opacity: 1 }}, {{ opacity: 0, duration: .5, immediateRender: false }}, T0 + SP * {.62 + i * .05:.2f});'
        for i in range(8)) + """
      { """ + CONF_JS.replace("SEED", "61").replace("BOX", "sj-cf").replace("T0", "tw") + """ }
      tl.to(".jc", { scale: 1.04, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, tw);
      tl.to("#sj-h", { opacity: 0, duration: .15 }, tw - .1);
      tl.fromTo("#sj-win", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, tw - .05);""")

# s04 – Streuner + Tierheim: 787 / 800
scene("s04", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s4-s { top: 280px; font-size: 54px; background: #e8262f; }
    #s4-h { position: absolute; left: 70px; right: 70px; top: 280px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s4-h .r { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 42px; } #s4-h .r b { font-size: 66px; color: #2e9e5b; }
    #s4-h .bar { height: 30px; border-radius: 15px; background: #ece4d8; margin-top: 10px; overflow: hidden; } #s4-h .bar i { display: block; height: 100%; width: 0; border-radius: 15px; background: linear-gradient(90deg, #2e9e5b, #8be06a); }
    #s4-h .f { margin-top: 8px; font-weight: 900; font-size: 34px; color: #e2560c; }
    #s4-ff { top: 600px; font-size: 54px; background: linear-gradient(100deg, #ff6a1a, #ff2e7e); }""",
"""      <div id="s4-s" class="pl">🐱🐶 Streuner überall!</div>
      <div id="s4-h"><div class="r"><div>🐾 Tierheim Pfotenkuss</div><div><b id="s4-n">0</b> / 800</div></div><div class="bar"><i id="s4-b"></i></div><div class="f">Bei 800 Bewohnern wird gebaut</div></div>
      <div id="s4-ff" class="pl">🔥 Nur noch 13!</div>""",
"""      const t4 = line("L4")[0], t4b = line("L4b")[0], wi = at("L4b", "787"), fu = at("L4b", "13");
      tl.fromTo("#s4-s", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, t4);
      tl.to("#s4-s", { x: 10, duration: .05, yoyo: true, repeat: 7, ease: "none" }, t4 + .4);
      tl.to("#s4-s", { opacity: 0, y: -30, duration: .2 }, t4b - .25);
      tl.fromTo("#s4-h", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, t4b - .1);
      count(tl, "#s4-n", 0, 787, t4b + .2, wi - t4b + .2, "", "", "power2.out");
      tl.fromTo("#s4-b", { width: "0%" }, { width: "98.4%", duration: wi - t4b + .2, ease: "power2.out" }, t4b + .2);
      tl.fromTo("#s4-ff", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fu - .2);
      tl.to("#s4-ff", { scale: 1.1, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, fu + .2);""")

# s04b – LIVE-Hinweis: komm rein und bau mit an der LIVE-Insel
scene("s04b", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s4l-b { top: 270px; font-size: 88px; background: #e8101e; transform: rotate(-2deg); box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3), 0 0 50px 14px rgba(255,20,30,.6); }
    #s4l-dot { display: inline-block; width: 44px; height: 44px; border-radius: 50%; background: #fff; margin-right: 16px; vertical-align: 6px; }
    #s4l-e { top: 430px; font-size: 48px; background: #fff; color: #2a1b12; }
    #s4l-pa { position: absolute; left: 928px; top: 950px; width: 130px; height: 150px; }
    #s4l-ring { position: absolute; left: 5px; top: 0; width: 120px; height: 120px; border-radius: 50%; background: conic-gradient(#ff1f4b, #ff6a1a, #ff1f4b, #ff2e7e, #ff1f4b); box-shadow: 0 0 40px 10px rgba(255,30,70,.8); }
    #s4l-pic { position: absolute; left: 15px; top: 10px; width: 100px; height: 100px; border-radius: 50%; overflow: hidden; background: #fff; border: 4px solid #fff; }
    #s4l-pic svg { width: 100%; height: 100%; }
    #s4l-lb { position: absolute; left: 0; right: 0; margin: 0 auto; top: 108px; width: fit-content; padding: 1px 12px 4px; border-radius: 8px; background: #ff1f4b; border: 3px solid #fff; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 24px; }
    #s4l-ph { left: auto; right: 12px; margin: 0; top: 1124px; font-size: 26px; padding: 5px 13px 8px; background: #ff1f4b; box-shadow: 0 0 0 5px #fff, 0 10px 0 rgba(0,0,0,.25); }""",
"""      <div id="s4l-b" class="big"><span id="s4l-dot"></span>LIVE-INSEL</div>
      <div id="s4l-e" class="pl">🏗️ Komm rein & bau mit!</div>
      <div id="s4l-pa" data-layout-ignore><div id="s4l-ring"></div><div id="s4l-pic">""" + LOGO + """</div><div id="s4l-lb">LIVE</div></div>
      <div id="s4l-ph" class="pl">👆 Tippen!</div>""",
"""      const t = line("L4c")[0], lv = at("L4c", "LIVE"), ko = at("L4c", "Komm");
      tl.fromTo("#s4l-b", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, lv - .15);
      tl.to("#s4l-dot", { opacity: .15, duration: .25, yoyo: true, repeat: 11, ease: "steps(1)" }, lv + .2);
      tl.fromTo("#s4l-pa", { opacity: 0, scale: .2 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, lv);
      tl.fromTo("#s4l-ring", { scale: 1, rotation: 0 }, { scale: 1.15, rotation: 40, duration: .3, yoyo: true, repeat: 9, ease: "sine.inOut" }, lv + .3);
      tl.fromTo("#s4l-ph", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, lv + .3);
      tl.to("#s4l-ph", { y: -12, duration: .25, yoyo: true, repeat: 7, ease: "sine.inOut" }, lv + .7);
      tl.fromTo("#s4l-e", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, ko - .15);
      tl.to("#s4l-e", { scale: 1.08, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, ko + .3);""")

# s06 – Ankündigung: Bei 1.000 Bewohnern wird Muschel-Tal zum Spiel
F6 = [("🗺️", "Welt erkunden", "#2e9e5b", "Welt"), ("🐚", "Muscheln sammeln", "#ffb21a", "Muscheln"), ("🛍️", "Sachen kaufen", "#e8467c", "Sachen"), ("👯", "Freunde finden", "#7b3fe0", "Freunde")]
scene("s06", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s6-dim { position: absolute; left: 0; right: 0; top: 0; height: 1100px; background: linear-gradient(180deg, rgba(10,12,40,.6), rgba(10,12,40,.35) 80%, rgba(10,12,40,0)); opacity: 0; }
    #s6-fl { position: absolute; inset: 0; background: #fff; opacity: 0; }
    #s6-n { position: absolute; left: 0; right: 0; top: 200px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 250px; line-height: 1; color: #ffe14a; -webkit-text-stroke: 16px #1a0f08; paint-order: stroke fill; text-shadow: 0 0 60px #ffb21a; opacity: 0; }
    #s6-l { top: 470px; font-size: 52px; background: #fff; color: #2a1b12; }
    #s6-s { top: 590px; font-size: 84px; background: linear-gradient(135deg, #ff2e9a, #7b3fe0); transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(255,46,154,.65); }
    .fc { position: absolute; width: 470px; height: 230px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.3); overflow: hidden; opacity: 0; }
    .fc .fe { height: 150px; display: grid; place-items: center; font-size: 100px; background: linear-gradient(180deg, #bfefff, #fff); }
    .fc .fl { height: 80px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; color: #fff; }""",
"""      <div id="s6-dim" data-layout-ignore></div>
      <div id="s6-fl" data-layout-ignore></div>
      <div id="s6-n" data-layout-ignore>1.000</div>
      <div id="s6-l" class="pl">🏝️ Bewohner – dann geht's los!</div>
      <div id="s6-s" class="big">🎮 DAS SPIEL!</div>
      """ + "".join(f'<div class="fc" id="s6-c{i}" style="left:{50 + (i % 2) * 510}px;top:{260 + (i // 2) * 270}px"><div class="fe">{e}</div><div class="fl" style="background:{c}">{n}</div></div>' for i, (e, n, c, k) in enumerate(F6)),
"""      const t9 = line("L9")[0], n1 = at("L9", "1.000"), sp = at("L9", "Spiel"), tb = line("L9b")[0];
      tl.fromTo("#s6-dim", { opacity: 0 }, { opacity: 1, duration: .3 }, t9);
      tl.fromTo("#s6-n", { opacity: 0, scale: 4, rotation: -8, filter: "blur(14px)" }, { opacity: 1, scale: 1, rotation: 0, filter: "blur(0px)", duration: .25, ease: "expo.out" }, n1 - .1);
      tl.to("#s6-n", { scale: 1.07, duration: .16, yoyo: true, repeat: 7, ease: "sine.inOut" }, n1 + .3);
      tl.fromTo("#s6-l", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, n1 + .25);
      tl.fromTo("#s6-fl", { opacity: .9 }, { opacity: 0, duration: .35, immediateRender: false }, sp);
      tl.fromTo("#s6-s", { opacity: 0, scale: 3.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, sp - .1);
      tl.to("#s6-s", { x: 12, duration: .04, yoyo: true, repeat: 9, ease: "none" }, sp + .2);
      tl.to(["#s6-n", "#s6-l", "#s6-s"], { opacity: 0, scale: .6, duration: .22, ease: "power2.in" }, tb - .25);
      """ + "\n      ".join(f'tl.fromTo("#s6-c{i}", {{ opacity: 0, scale: .3, rotation: {(-8, 8, -8, 8)[i]} }}, {{ opacity: 1, scale: 1, rotation: 0, duration: .3, ease: "back.out(2.4)" }}, at("L9b", "{k}") - .15); tl.to("#s6-c{i}", {{ scale: 1.06, duration: .16, yoyo: true, repeat: 3, ease: "sine.inOut" }}, at("L9b", "{k}") + .2);' for i, (e, n, c, k) in enumerate(F6)))

# s05 – Folg mir + Kommentar: Wer wird Türsteher?
scene("s05", LILITA + "\n    " + PILL + "\n" + FOLLOW + """
    #s5-btn { top: 280px; } #s5-hand { left: 690px; top: 330px; }
    #s5-t { top: 445px; font-size: 64px; background: linear-gradient(135deg, #2e9e5b, #8be06a); font-family: "Lilita One", sans-serif; font-weight: 400; transform: rotate(-2deg); }
    #s5-h { top: 590px; font-size: 44px; background: #fff; color: #2e9e5b; }""",
"""      <div id="s5-btn" class="fbtn">+ Folgen<div id="s5-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s5-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s5-t" class="pl">🎮 Sei dabei, wenn's losgeht!</div>
      <div id="s5-h" class="pl">🐚 Bei 1.000 startet das Spiel!</div>""",
"""      const t5 = line("L5")[0], fo = at("L5", "Folg"), du = at("L5", "dabei"), ti = at("L5", "losgeht");
      tl.fromTo("#s5-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .2);
      tl.fromTo("#s5-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .1);
      tl.to("#s5-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .2);
      tl.to("#s5-btn2", { opacity: 1, duration: .05 }, fo + .3);
      tl.to("#s5-hand", { opacity: 0, duration: .2 }, fo + .7);
      tl.fromTo("#s5-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, du - .2);
      tl.to("#s5-t", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, du + .3);
      tl.fromTo("#s5-h", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, ti - .3);""", blur=False)
