import json
import sys
from pathlib import Path
D = Path(sys.argv[1]); LOGO = Path(sys.argv[2]).read_text().strip()
SHELL = '<svg viewBox="0 0 64 64"><path d="M32 47 L8.8 40.8 Q5.0 34.0 12.7 32.7 Q11.6 25.0 19.2 26.7 Q21.0 19.1 27.5 23.4 Q32.0 17.0 36.5 23.4 Q43.0 19.1 44.8 26.7 Q52.4 25.0 51.3 32.7 Q59.0 34.0 55.2 40.8 Z" fill="#ffc7b2" stroke="#2a1b12" stroke-width="3" stroke-linejoin="round"/><path d="M32 45L13.9 33.6M32 45L20.0 27.9M32 45L27.8 24.9M32 45L36.2 24.9M32 45L44.0 27.9M32 45L50.1 33.6" stroke="#c43d6b" stroke-width="2" stroke-linecap="round"/></svg>'
LILITA = '@font-face { font-family: "Lilita One"; src: url("assets/fonts/LilitaOne-Regular.woff2") format("woff2"); font-weight: 400; }'

V1 = """
    .stk { background: rgba(255,255,255,.94) !important; border: 10px solid #e8467c; color: #e8467c !important; text-shadow: none !important; box-shadow: 0 9px 0 rgba(0,0,0,.25) !important;
      font-family: "Inter", sans-serif !important; font-weight: 900; font-size: 76px !important; padding: 6px 30px 12px !important; border-radius: 40px !important; line-height: 1.05 !important; max-width: 900px; }
    .stk small { color: #2a1b12 !important; font-size: 36px !important; text-shadow: none !important; font-weight: 800; }
    .stk.bl { border-color: #2f7fe0; color: #2f7fe0 !important; } .stk.gr { border-color: #2fbf6a; color: #1f9a52 !important; } .stk.go { border-color: #ffd23f; color: #2a1b12 !important; background: #ffd23f !important; }
    #h4 { border-color: #7b4fe0; color: #7b4fe0 !important; background: rgba(255,255,255,.94) !important; }
    .gl { background: #7b4fe0 !important; backdrop-filter: none !important; -webkit-backdrop-filter: none !important; border-radius: 22px !important; box-shadow: 0 9px 0 rgba(0,0,0,.28) !important; padding: 8px 28px 12px !important; }
    .gl small { font: 900 24px Inter, sans-serif !important; letter-spacing: .15em !important; opacity: .9; }
    .gl b { font-size: 54px !important; }
    .ch6, #tg2, #fr8 { font-family: "Inter", sans-serif !important; font-weight: 900 !important; font-size: 50px !important; box-shadow: 0 9px 0 rgba(0,0,0,.28) !important; }
    #f2 { font-size: 48px !important; }"""

def scene(sid, css, html, js, blur=True):
    css = css + V1
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

# s01 – Golden Pearl bei Nacht
scene("s01", GL + """
    .stamp { position: absolute; padding: 6px 30px 10px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.94); font-family: "Inter", sans-serif; font-weight: 900; font-size: 84px; opacity: 0; }
    #st1 { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 290px; color: #c99a00; border-color: #ffd23f; transform: rotate(-6deg); }
    .sp { position: absolute; width: 70px; height: 70px; opacity: 0; }""",
"""      <div id="st1" class="stamp">💎 GOLDEN PEARL</div>
      <svg class="sp" style="left:120px;top:250px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#ffd23f"/></svg>
      <svg class="sp" style="left:880px;top:420px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#fff"/></svg>
      <svg class="sp" style="left:170px;top:560px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#fff"/></svg>""",
"""      const G = at("L1", "Golden");
      tl.fromTo("#st1", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, G - .05);
      tl.fromTo("#st1", { x: 0 }, { x: 10, duration: .04, yoyo: true, repeat: 7, ease: "none" }, G + .25);
      tl.fromTo(".sp", { scale: .2, opacity: 0, rotation: 0 }, { scale: 1.4, opacity: 1, rotation: 90, duration: .35, ease: "back.out(3)", stagger: .15, yoyo: true, repeat: 5 }, 0);""")

# s02 – Spiel fast fertig
scene("s02", GL + """
    #g2 { top: 270px; } #g2 b { font-size: 64px; }
    #pb2 { position: absolute; left: 140px; right: 140px; top: 470px; opacity: 0; }
    #pb2 .tr { height: 72px; border-radius: 36px; background: rgba(0,0,0,.55); box-shadow: 0 0 0 7px #fff; overflow: hidden; }
    #pb2 .fi { height: 100%; width: 0; border-radius: 36px; background: linear-gradient(90deg,#ffd23f,#e8467c); }
    #pb2 .lb { margin-top: 14px; text-align: center; font: 900 48px Inter, sans-serif; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.5); }""",
"""      <div id="g2" class="gl"><small>🛠️ in den letzten Zügen</small><b>🎮 Das Spiel</b></div>
      <div id="pb2"><div class="tr"><div class="fi"></div></div><div class="lb">fast fertig … 🚀</div></div>""",
"""      const t = line("L2")[0];
      tl.fromTo("#g2", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .4, ease: "back.out(2)" }, t - .1);
      tl.fromTo("#pb2", { opacity: 0 }, { opacity: 1, duration: .3 }, t + .2);
      tl.fromTo("#pb2 .fi", { width: "0%" }, { width: "94%", duration: 2.2, ease: "power2.out" }, t + .3);""")

# s03 – Freunde einladen, erste 1.000
scene("s03", GL + """
    .stamp { position: absolute; padding: 6px 30px 10px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.94); font-family: "Inter", sans-serif; font-weight: 900; font-size: 72px; opacity: 0; }
    #st3 { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 280px; color: #2fbf6a; border-color: #2fbf6a; transform: rotate(-4deg); }
    #n3 { position: absolute; left: 0; right: 0; top: 470px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 150px; color: #ffe14a; opacity: 0;
      text-shadow: 0 6px 0 #ff9a1a, 0 12px 0 #8a3510, 0 20px 30px rgba(0,0,0,.5); }
    #n3 small { display: block; font: 900 44px Inter, sans-serif; color: #fff; }""",
"""      <div id="st3" class="stamp">👯 FREUNDE EINLADEN!</div>
      <div id="n3">1.000<small>die ersten Plätze ⭐</small></div>""",
"""      const t = line("L3")[0], E = at("L3", "ersten");
      tl.fromTo("#st3", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, at("L3", "Freunde") - .1);
      tl.fromTo("#n3", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .4, ease: "back.out(2.5)" }, E - .1);
      tl.to("#n3", { scale: 1.08, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, E + .4);""")

# s04 – Vorteile + Folgen
scene("s04", GL + """
    .stamp { position: absolute; padding: 6px 30px 10px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.94); font-family: "Inter", sans-serif; font-weight: 900; font-size: 76px; opacity: 0; }
    #st4 { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 280px; color: #c99a00; border-color: #ffd23f; transform: rotate(-4deg); }
    #f4 { position: absolute; left: 0; right: 0; margin: 0 auto; top: 470px; width: 440px; height: 112px; border-radius: 56px; background: #fe2c55; color: #fff; font: 800 54px/112px Inter, sans-serif; text-align: center; opacity: 0; box-shadow: 0 14px 30px rgba(0,0,0,.35); }""",
"""      <div id="st4" class="stamp">👑 VORTEILE IM SPIEL</div>
      <div id="f4">+ Folgen</div>""",
"""      const V = at("L4", "Vorteile"), F = at("L4", "Folg");
      tl.fromTo("#st4", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, V - .1);
      tl.fromTo("#f4", { opacity: 0, scale: .5 }, { opacity: 1, scale: 1, duration: .4, ease: "back.out(2.5)" }, F - .05);
      tl.to("#f4", { scale: 1.08, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, F + .4);""", blur=False)
