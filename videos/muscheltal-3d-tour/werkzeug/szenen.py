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




GL = """.gl { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; padding: 18px 34px 20px; border-radius: 28px;
      background: rgba(255,255,255,.16); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); box-shadow: inset 0 0 0 1.5px rgba(255,255,255,.55), 0 20px 50px rgba(30,10,40,.35);
      color: #fff; font-family: "Inter", sans-serif; text-align: center; }
    .gl small { display: block; font-weight: 700; font-size: 26px; letter-spacing: .32em; text-transform: uppercase; opacity: .85; }
    .gl b { display: block; font-weight: 900; font-size: 92px; letter-spacing: -.02em; line-height: 1; }"""

# s00 – Cold Open: Spannung → WAS WAR DAS?! → Wal → Schildkröten-Wanderung
scene("s00", GL + """
    #vg0 { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 35%, rgba(0,10,30,.75) 100%); }
    #fl0 { position: absolute; inset: 0; background: #fff; opacity: 0; }
    #q0 { top: 250px; } #q0 b { font-size: 70px; }
    .stk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 240px; padding: 14px 44px 26px; border-radius: 40px; font-family: "Lilita One", sans-serif; text-align: center; line-height: .95; color: #ffe14a;
      background: linear-gradient(160deg, #ff3d7f, #ff7a2a); box-shadow: 0 0 0 9px #fff, 0 0 0 16px #2a1b12, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(255,90,60,.6); text-shadow: 0 7px 0 #8a1035; }
    #w0 { font-size: 150px; transform: rotate(-4deg); }
    #w1 { font-size: 160px; background: linear-gradient(160deg, #1f8ff0, #36d1dc); text-shadow: 0 7px 0 #0b3d7a; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0b2340, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(60,180,255,.7); }
    #w1 small, #w0 small { display: block; font-size: 56px; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.3); }
    #rr0, #rr1 { position: absolute; left: 540px; top: 520px; width: 220px; height: 220px; margin: -110px; border-radius: 50%; border: 22px solid #fff; opacity: 0; }
    #rr1 { border-color: #36d1dc; }
    #s0t { top: 250px; } #s0t b { font-size: 76px; } #s0t b span { color: #9dffb0; }
    .pt { position: absolute; font-size: 84px; line-height: 1; width: 84px; height: 84px; opacity: 0; }""",
"""      <div id="vg0"></div>
      <div id="q0" class="gl"><small>Psst …</small><b>👀 da draußen …</b></div>
      <div id="rr0"></div><div id="rr1"></div>
      """ + """<div class="pt" id="pa0" style="left:498px;top:478px">💥</div><div class="pt" id="pa1" style="left:498px;top:478px">💦</div><div class="pt" id="pa2" style="left:498px;top:478px">🌊</div><div class="pt" id="pa3" style="left:498px;top:478px">✨</div><div class="pt" id="pa4" style="left:498px;top:478px">💥</div><div class="pt" id="pa5" style="left:498px;top:478px">💦</div><div class="pt" id="pa6" style="left:498px;top:478px">🌊</div><div class="pt" id="pa7" style="left:498px;top:478px">✨</div><div class="pt" id="pa8" style="left:498px;top:478px">💥</div><div class="pt" id="pa9" style="left:498px;top:478px">💦</div><div class="pt" id="pa10" style="left:498px;top:478px">🌊</div><div class="pt" id="pa11" style="left:498px;top:478px">✨</div><div class="pt" id="pa12" style="left:498px;top:478px">💥</div><div class="pt" id="pa13" style="left:498px;top:478px">💦</div>""" + """
      <div id="w0" class="stk">WAS WAR<br>DAS?! 😱</div>
      <div id="w1" class="stk"><small>direkt vor meiner Insel</small>🐋 EIN WAL!</div>
      <div id="s0t" class="gl"><small>Und am Strand</small><b>🐢 <span>Schildkröten-</span><br>Wanderung!</b></div>
      <div id="fl0"></div>""",
"""      const W = at("L0b", "WAS"), A = at("L0c", "WAL"), K = line("L0d")[0];
      tl.fromTo("#vg0", { opacity: 1 }, { opacity: 0, duration: .4 }, W - .1);
      tl.fromTo("#q0", { opacity: 0, y: 30, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, .15);
      tl.to("#q0", { scale: 1.04, duration: .5, yoyo: true, repeat: 3, ease: "sine.inOut" }, .8);
      tl.to("#q0", { opacity: 0, scale: .8, duration: .2 }, W - .15);
      tl.fromTo("#fl0", { opacity: .9 }, { opacity: 0, duration: .35, ease: "power2.out", immediateRender: false }, W - .03);
      tl.fromTo("#rr0", { scale: .2, opacity: 1 }, { scale: 6, opacity: 0, duration: .8, ease: "power3.out", immediateRender: false }, W);
      tl.fromTo("#rr1", { scale: .2, opacity: 1 }, { scale: 8, opacity: 0, duration: 1, ease: "power3.out", immediateRender: false }, W + .1);
      tl.fromTo("#pa0", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 287, y: 98, scale: 1.10, rotation: 60, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.00);
      tl.fromTo("#pa1", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 308, y: 315, scale: 1.45, rotation: -77, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.03);
      tl.fromTo("#pa2", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 197, y: 553, scale: 1.80, rotation: 94, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.06);
      tl.fromTo("#pa3", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -23, y: 329, scale: 1.10, rotation: -111, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.09);
      tl.fromTo("#pa4", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -210, y: 400, scale: 1.45, rotation: 128, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.00);
      tl.fromTo("#pa5", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -446, y: 334, scale: 1.80, rotation: -145, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.03);
      tl.fromTo("#pa6", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -297, y: 49, scale: 1.10, rotation: 162, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.06);
      tl.fromTo("#pa7", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -401, y: -137, scale: 1.45, rotation: -179, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.09);
      tl.fromTo("#pa8", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -396, y: -404, scale: 1.80, rotation: 196, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.00);
      tl.fromTo("#pa9", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -109, y: -307, scale: 1.10, rotation: -213, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.03);
      tl.fromTo("#pa10", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 32, y: -461, scale: 1.45, rotation: 230, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.06);
      tl.fromTo("#pa11", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 270, y: -514, scale: 1.80, rotation: -247, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.09);
      tl.fromTo("#pa12", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 248, y: -186, scale: 1.10, rotation: 264, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.00);
      tl.fromTo("#pa13", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 415, y: -68, scale: 1.45, rotation: -281, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L0b", "WAS") + 0.03);
      tl.fromTo("#w0", { opacity: 0, scale: 2.4, rotation: -14 }, { opacity: 1, scale: 1, rotation: -4, duration: .3, ease: "back.out(3)" }, W - .02);
      [[16,-10,-1],[-18,8,-7],[12,12,-2],[-10,-8,-6],[6,4,-3],[0,0,-4]].forEach(([x, y, r], i) => tl.to("#w0", { x, y, rotation: r, duration: .05, ease: "none" }, W + .3 + i * .05));
      tl.to("#w0", { opacity: 0, scale: .6, duration: .18, ease: "power2.in" }, A - .25);
      tl.fromTo("#w1", { opacity: 0, scale: .3, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: .45, ease: "back.out(2.6)" }, A - .1);
      tl.to("#w1", { y: -10, duration: .5, yoyo: true, repeat: 3, ease: "sine.inOut" }, A + .4);
      tl.to("#w1", { opacity: 0, scale: .7, duration: .2 }, K - .2);
      tl.fromTo("#s0t", { opacity: 0, scale: 1.3, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .4, ease: "back.out(2)" }, K - .05);""")

# s01 – Willkommen in Muschel-Tal: 790 zählt hoch, Sonnenstrahlen, Konfetti
scene("s01", """
    #ray1 { position: absolute; left: 540px; top: 560px; width: 1100px; height: 1100px; margin: -550px; border-radius: 50%; opacity: 0;
      background: repeating-conic-gradient(rgba(255,225,74,.55) 0deg 9deg, rgba(255,225,74,0) 9deg 22deg); -webkit-mask: radial-gradient(circle, #000 20%, transparent 68%); mask: radial-gradient(circle, #000 20%, transparent 68%); }
    #wk1 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 230px; text-align: center; font-family: "Lilita One", sans-serif; }
    #wk1 small { display: inline-block; font-size: 46px; color: #e8467c; background: #fff; padding: 6px 30px 10px; border-radius: 40px; box-shadow: 0 8px 0 rgba(0,0,0,.2); transform: rotate(-2deg); }
    #wk1 b { display: block; margin-top: 6px; font-weight: 400; font-size: 150px; line-height: 1; color: #fff; letter-spacing: .01em;
      text-shadow: 0 4px 0 #e8467c, 0 8px 0 #e8467c, 0 12px 0 #b8245a, 0 16px 0 #8a1035, 0 22px 30px rgba(0,0,0,.45); }
    #nm1 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 330px; text-align: center; font-family: "Lilita One", sans-serif; opacity: 0; }
    #nm1 b { display: block; font-weight: 400; font-size: 250px; line-height: .9; color: #ffe14a;
      text-shadow: 0 6px 0 #ff9a1a, 0 12px 0 #e8601a, 0 18px 0 #8a3510, 0 26px 40px rgba(0,0,0,.5), 0 0 60px rgba(255,200,60,.6); }
    #nm1 small { display: inline-block; margin-top: 10px; font-size: 58px; color: #fff; background: #2a1b12; padding: 4px 30px 10px; border-radius: 30px; letter-spacing: .04em; }
    #al1 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 700px; padding: 10px 46px 22px; border-radius: 44px; overflow: hidden; opacity: 0;
      background: linear-gradient(160deg, #ff3d7f, #ff7ac0); box-shadow: 0 0 0 8px #fff, 0 0 0 14px #2a1b12, 0 20px 0 rgba(0,0,0,.25), 0 0 70px rgba(255,61,127,.6);
      font-family: "Lilita One", sans-serif; font-size: 80px; line-height: 1; color: #fff; text-shadow: 0 6px 0 #8a1035; white-space: nowrap; }
    #al1 span { color: #ffe14a; }
    #sh1 { position: absolute; top: -20%; left: -40%; width: 30%; height: 140%; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.75), rgba(255,255,255,0)); transform: rotate(18deg); }
    .sp1 { position: absolute; font-size: 60px; opacity: 0; }
    .pt { position: absolute; font-size: 84px; line-height: 1; width: 84px; height: 84px; opacity: 0; }""",
"""      <div id="ray1"></div>
      <div id="wk1"><small>Willkommen in</small><b>MUSCHEL-TAL</b></div>
      <div id="nm1"><b id="n1">0</b><small>BEWOHNER 🏠</small></div>
      <div class="sp1" id="sp0" style="left:170px;top:360px">✨</div><div class="sp1" id="sp1" style="left:840px;top:330px">✨</div><div class="sp1" id="sp2" style="left:220px;top:600px">⭐</div><div class="sp1" id="sp3" style="left:800px;top:620px">✨</div>
      """ + """<div class="pt" id="pb0" style="left:498px;top:658px">🎉</div><div class="pt" id="pb1" style="left:498px;top:658px">💖</div><div class="pt" id="pb2" style="left:498px;top:658px">🏝️</div><div class="pt" id="pb3" style="left:498px;top:658px">✨</div><div class="pt" id="pb4" style="left:498px;top:658px">🐚</div><div class="pt" id="pb5" style="left:498px;top:658px">🥳</div><div class="pt" id="pb6" style="left:498px;top:658px">🎉</div><div class="pt" id="pb7" style="left:498px;top:658px">💖</div><div class="pt" id="pb8" style="left:498px;top:658px">🏝️</div><div class="pt" id="pb9" style="left:498px;top:658px">✨</div><div class="pt" id="pb10" style="left:498px;top:658px">🐚</div><div class="pt" id="pb11" style="left:498px;top:658px">🥳</div><div class="pt" id="pb12" style="left:498px;top:658px">🎉</div><div class="pt" id="pb13" style="left:498px;top:658px">💖</div><div class="pt" id="pb14" style="left:498px;top:658px">🏝️</div><div class="pt" id="pb15" style="left:498px;top:658px">✨</div>""" + """
      <div id="al1"><span>ALLE</span> meine Follower! 💖<div id="sh1"></div></div>""",
"""      const t0 = line("L1")[0], H = at("L1", "Hier"), A = at("L1", "ALLE");
      tl.fromTo("#wk1 small", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, t0 - .15);
      tl.fromTo("#wk1 b", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: 0, duration: .5, ease: "elastic.out(1, .55)" }, t0 + .1);
      tl.to("#wk1 b", { scale: 1.05, duration: .35, yoyo: true, repeat: 1, ease: "sine.inOut" }, t0 + .7);
      tl.to("#wk1", { opacity: 0, y: -60, scale: .8, duration: .25, ease: "power2.in" }, H - .3);
      tl.fromTo("#ray1", { opacity: 0, rotation: 0, scale: .5 }, { opacity: 1, scale: 1, duration: .4, ease: "power2.out" }, H - .1);
      tl.to("#ray1", { rotation: 90, duration: 6, ease: "none" }, H - .1);
      tl.fromTo("#nm1", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .45, ease: "back.out(2.4)" }, H - .1);
      count(tl, "#n1", 0, 790, H, 1.1, "", "", "power2.out");
      tl.fromTo("#nm1 b", { scale: 1 }, { scale: 1.12, duration: .15, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 60%" }, H + 1.1);
      ["#sp0", "#sp1", "#sp2", "#sp3"].forEach((q, i) => tl.fromTo(q, { opacity: 0, scale: .2, rotation: 0 }, { opacity: 1, scale: 1.2, rotation: 90, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }, H + .2 + i * .18));
      tl.fromTo("#al1", { opacity: 0, scale: 2.2, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: .32, ease: "back.out(3)" }, A - .08);
      [[14,-8,2],[-14,6,-2],[8,6,1],[0,0,0]].forEach(([x, y, r], i) => tl.to("#al1", { x, y, rotation: r, duration: .05, ease: "none" }, A + .25 + i * .05));
      tl.fromTo("#sh1", { left: "-40%" }, { left: "130%", duration: .7, ease: "power2.inOut", immediateRender: false }, A + .35);
      tl.fromTo("#sh1", { left: "-40%" }, { left: "130%", duration: .7, ease: "power2.inOut", immediateRender: false }, A + 1.3);
      tl.fromTo("#pb0", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 287, y: 98, scale: 1.10, rotation: 60, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.00);
      tl.fromTo("#pb1", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 323, y: 295, scale: 1.45, rotation: -77, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.03);
      tl.fromTo("#pb2", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 252, y: 525, scale: 1.80, rotation: 94, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.06);
      tl.fromTo("#pb3", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 28, y: 329, scale: 1.10, rotation: -111, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.09);
      tl.fromTo("#pb4", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -124, y: 441, scale: 1.45, rotation: 128, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.00);
      tl.fromTo("#pb5", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -345, y: 457, scale: 1.80, rotation: -145, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.03);
      tl.fromTo("#pb6", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -265, y: 154, scale: 1.10, rotation: 162, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.06);
      tl.fromTo("#pb7", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -418, y: 43, scale: 1.45, rotation: -179, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.09);
      tl.fromTo("#pb8", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -516, y: -176, scale: 1.80, rotation: 196, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.00);
      tl.fromTo("#pb9", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -231, y: -211, scale: 1.10, rotation: -213, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.03);
      tl.fromTo("#pb10", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -196, y: -409, scale: 1.45, rotation: 230, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.06);
      tl.fromTo("#pb11", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: -50, y: -591, scale: 1.80, rotation: -247, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.09);
      tl.fromTo("#pb12", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 89, y: -315, scale: 1.10, rotation: 264, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.00);
      tl.fromTo("#pb13", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 268, y: -356, scale: 1.45, rotation: -281, opacity: 0, duration: 1.15, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.03);
      tl.fromTo("#pb14", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 478, y: -277, scale: 1.80, rotation: 298, opacity: 0, duration: 1.40, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.06);
      tl.fromTo("#pb15", { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: 299, y: -31, scale: 1.10, rotation: -315, opacity: 0, duration: 0.90, ease: "power3.out", immediateRender: false }, at("L1", "ALLE") + 0.09);""", blur=False)

# s02 – Jede Hütte = echter Follower
scene("s02", GL + """
    #t2 { top: 250px; } #t2 b { font-size: 64px; }""",
"""      <div id="t2" class="gl"><small>Jede Hütte</small><b>= 1 echter Follower</b></div>""",
"""      const t = line("L2b")[0];
      tl.fromTo("#t2", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, t - .2);""")

# s02n – Siehst du dich? → Kommentar „Wo bin ich?“
scene("s02n", GL + """
    #t2n { top: 230px; } #t2n b { font-size: 104px; color: #ffe08a; }
    #c2n { position: absolute; left: 90px; top: 520px; display: flex; gap: 18px; align-items: center; padding: 18px 30px 20px 18px; border-radius: 40px; background: rgba(255,255,255,.96); box-shadow: 0 16px 40px rgba(0,0,0,.3); font-family: "Inter", sans-serif; }
    #c2n i { width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg,#ff6fa3,#ffd23f); display: grid; place-items: center; font-style: normal; font-size: 40px; }
    #c2n div small { display: block; font-size: 26px; color: #888; font-weight: 700; } #c2n div b { font-size: 50px; color: #161823; font-weight: 900; }""",
"""      <div id="t2n" class="gl"><b>Siehst du dich? 👀</b></div>
      <div id="c2n"><i>💬</i><div><small>Dein Kommentar</small><b>Wo bin ich?</b></div></div>""",
"""      const t = line("L2c")[0];
      tl.fromTo("#t2n", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }, t - .1);
      tl.fromTo("#c2n", { opacity: 0, x: -60, scale: .8 }, { opacity: 1, x: 0, scale: 1, duration: .4, ease: "back.out(2)" }, at("L2c", "Wenn"));
      tl.to("#c2n", { scale: 1.06, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L2c", "Wenn") + .8);""")

# s03 – Gebäude-Namen erscheinen passend zu den Schnitten
BN = [("L3", "Dönerbude", "🥙 Dönerbude"), ("L3", "Bäckerei", "🥐 Bäckerei"), ("L3s", "Strandbar", "🍹 Strandbar"), ("L3t", "Tierheim", "🐾 Tierheim Pfotenkuss · offen!"), ("L3k", "Lagerfeuer", "🔥 Lagerfeuer"), ("L3g", "Kokos-Club", "🪩 Kokos-Club"), ("L3g", "Game", "🎮 Game Lagoon"), ("L3c", "Freiluftkino", "🎬 Freiluftkino")]
scene("s03", GL + """
    .bn { top: 240px; } .bn b { font-size: 70px; }""",
"""""" + "".join(f'<div id="bn{i}" class="gl bn"><small>{"Hauptinsel" if l in ("L3", "L3s", "L3t") else "Kokos-Küste"}</small><b>{t}</b></div>' for i, (l, w, t) in enumerate(BN)) + """""",
"""""" + "\n".join(f'      tl.fromTo("#bn{i}", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, at("{l}", "{w}") - .25);' + (f' tl.to("#bn{i}", {{ opacity: 0, duration: .15 }}, at("{BN[i+1][0]}", "{BN[i+1][1]}") - .4);' if i < len(BN) - 1 else f' tl.to("#bn{i}", {{ opacity: 0, duration: .25 }}, line("L3c")[1] + .5);') for i, (l, w, t) in enumerate(BN)))

# s04 – 790 Bewohner
scene("s04", GL + """
    #t4 { top: 250px; } #t4 b { font-size: 120px; }""",
"""      <div id="t4" class="gl"><b id="n4">0</b><small>Bewohner · täglich mehr</small></div>""",
"""      const t = line("L4")[0];
      tl.fromTo("#t4", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, t - .2);
      count(tl, "#n4", 0, 790, t, 1.0, "", "", "power2.out");""")

# s05 – Freunde markieren = Nachbarn werden
scene("s05", GL + """
    #t5 { top: 230px; } #t5 b { font-size: 84px; } #t5 b span { color: #7dffb0; }
    #c5 { position: absolute; left: 90px; top: 540px; display: flex; gap: 18px; align-items: center; padding: 18px 30px 20px 18px; border-radius: 40px; background: rgba(255,255,255,.96); box-shadow: 0 16px 40px rgba(0,0,0,.3); font-family: "Inter", sans-serif; }
    #c5 i { width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg,#2fb3a0,#7dffb0); display: grid; place-items: center; font-style: normal; font-size: 40px; }
    #c5 div small { display: block; font-size: 26px; color: #888; font-weight: 700; } #c5 div b { font-size: 46px; color: #161823; font-weight: 900; } #c5 div b em { color: #fe2c55; font-style: normal; }""",
"""      <div id="t5" class="gl"><small>Neben Freunden wohnen?</small><b>👯 <span>Markier sie!</span></b></div>
      <div id="c5"><i>🏝️</i><div><small>Dein Kommentar</small><b><em>@deinbestie</em> wir ziehen ein!</b></div></div>""",
"""      const t = line("L5f")[0];
      tl.fromTo("#t5", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }, t - .1);
      tl.fromTo("#c5", { opacity: 0, x: -60, scale: .8 }, { opacity: 1, x: 0, scale: 1, duration: .4, ease: "back.out(2)" }, at("L5f", "Markier") - .1);""")

# s06 – Was fehlt euch noch? Kommentiert es!
scene("s06", GL + """
    #t6 { top: 230px; } #t6 b { font-size: 72px; color: #ffe08a; }
    #c6 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 520px; padding: 20px 40px 24px; border-radius: 44px; background: #fe2c55; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; box-shadow: 0 18px 40px rgba(254,44,85,.45); }""",
"""      <div id="t6" class="gl"><small>Ihr entscheidet</small><b>Was baue ich als Nächstes? 🤔</b></div>
      <div id="c6">💬 Kommentiert es!</div>""",
"""      const t = line("L5k")[0];
      tl.fromTo("#t6", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }, t - .1);
      tl.fromTo("#c6", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .4, ease: "back.out(2.2)" }, at("L5k", "Kommentiert") - .1);
      tl.to("#c6", { scale: 1.07, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L5k", "Kommentiert") + .5);""")

# s07 – Folg mir
scene("s07", GL + """
    #t7 { top: 250px; } #t7 b { font-size: 76px; }
    #f7 { position: absolute; left: 0; right: 0; margin: 0 auto; top: 520px; width: 440px; height: 112px; border-radius: 56px; background: #fe2c55; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 50px; display: grid; place-items: center; box-shadow: 0 18px 40px rgba(254,44,85,.45); }""",
"""      <div id="t7" class="gl"><small>Deine Hütte wartet</small><b>@muscheltal</b></div>
      <div id="f7">+ Folgen</div>""",
"""      const t = line("L5")[0], fo = at("L5", "Folg");
      tl.fromTo("#t7", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, t - .2);
      tl.fromTo("#f7", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .45, ease: "back.out(2)" }, fo);
      tl.to("#f7", { scale: 1.06, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, fo + .5);""", blur=False)
