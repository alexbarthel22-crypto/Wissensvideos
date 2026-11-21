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

# s01 – Hook: Wem gehört das Golden Pearl? + drei Neuheiten
scene("s01", GL + """
    .stamp { position: absolute; padding: 6px 30px 10px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.95); font-family: "Inter", sans-serif; font-weight: 900; font-size: 76px; opacity: 0; white-space: nowrap; }
    .nr { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 250px; padding: 4px 34px 12px; border-radius: 30px; background: #ffd23f; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 96px; box-shadow: 0 0 0 8px #2a1b12, 0 12px 0 rgba(0,0,0,.3); transform: rotate(-4deg); opacity: 0; }
    .card { position: absolute; border-radius: 28px; border: 9px solid #fff; overflow: hidden; box-shadow: 0 0 0 5px #2a1b12, 0 16px 0 rgba(0,0,0,.35); opacity: 0; background: #fff; }
    .card img { display: block; width: 100%; }
    .lab { position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%); white-space: nowrap; padding: 4px 18px 8px; border-radius: 18px; background: #2a1b12; color: #ffd23f; font: 900 32px Inter, sans-serif; }
    #q1 { position: absolute; left: 0; right: 0; top: 300px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 300px; color: #ffe14a; opacity: 0; -webkit-text-stroke: 14px #2a1b12; paint-order: stroke fill; }
    #st1 { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 280px; color: #c99a00; border-color: #ffd23f; transform: rotate(-5deg); }
    #n1 { position: absolute; left: 0; right: 0; top: 300px; display: flex; justify-content: center; gap: 30px; }
    #n1 div { width: 190px; height: 190px; border-radius: 50%; background: #e8467c; color: #fff; font: 400 130px/190px "Lilita One", sans-serif; text-align: center; box-shadow: 0 0 0 9px #fff, 0 14px 0 rgba(0,0,0,.3); opacity: 0; }
    #n1 div:nth-child(2) { background: #0a9fa6; } #n1 div:nth-child(3) { background: #7b4fe0; }""",
"""      <div id="q1">?</div>
      <div id="st1" class="stamp">💎 WER GEWINNT?</div>
      <div id="n1"><div>1</div><div>2</div><div>3</div></div>""",
"""      const G = at("L1", "Golden"), D = at("L1b", "drei");
      tl.fromTo("#q1", { opacity: 0, scale: .3, rotation: -30 }, { opacity: 1, scale: 1, rotation: 0, duration: .45, ease: "back.out(3)" }, at("L1", "gezogen"));
      tl.to("#q1", { rotation: 12, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L1", "gezogen") + .5);
      tl.to("#q1", { opacity: 0, scale: 2, duration: .2 }, G - .2);
      tl.fromTo("#st1", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, G - .05);
      tl.to("#st1", { opacity: 0, duration: .2 }, D - .3);
      tl.fromTo("#n1 div", { opacity: 0, scale: .2, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: .35, ease: "back.out(3)", stagger: .18 }, D - .05);""")

# s02 – Neu 1: Hütte von innen
scene("s02", GL + """
    .stamp { position: absolute; padding: 6px 30px 10px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.95); font-family: "Inter", sans-serif; font-weight: 900; font-size: 76px; opacity: 0; white-space: nowrap; }
    .nr { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 250px; padding: 4px 34px 12px; border-radius: 30px; background: #ffd23f; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 96px; box-shadow: 0 0 0 8px #2a1b12, 0 12px 0 rgba(0,0,0,.3); transform: rotate(-4deg); opacity: 0; }
    .card { position: absolute; border-radius: 28px; border: 9px solid #fff; overflow: hidden; box-shadow: 0 0 0 5px #2a1b12, 0 16px 0 rgba(0,0,0,.35); opacity: 0; background: #fff; }
    .card img { display: block; width: 100%; }
    .lab { position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%); white-space: nowrap; padding: 4px 18px 8px; border-radius: 18px; background: #2a1b12; color: #ffd23f; font: 900 32px Inter, sans-serif; }
    #c2a { left: 70px; top: 420px; width: 560px; transform: rotate(-4deg); }
    #c2b { left: 450px; top: 760px; width: 560px; transform: rotate(4deg); }
    #st2 { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1230px; color: #8a5a2b; border-color: #8a5a2b; transform: rotate(-3deg); font-size: 64px; }""",
"""      <div class="nr" id="nr2">NEU #1</div>
      <div class="card" id="c2a"><img src="bilder/innen_haupt.jpg"><div class="lab">🏖️ Strandhaus</div></div>
      <div class="card" id="c2b"><img src="bilder/innen_kerem.jpg"><div class="lab">🥥 Kokos-Lodge</div></div>
      <div id="st2" class="stamp">🚪 DEINE HÜTTE VON INNEN</div>""",
"""      tl.fromTo("#nr2", { opacity: 0, scale: .3, rotation: -20 }, { opacity: 1, scale: 1, rotation: -4, duration: .4, ease: "back.out(3)" }, line("L2")[0] - .05); tl.to("#nr2", { opacity: 0, y: -40, duration: .2 }, line("L2b")[0] - .2);
      tl.fromTo("#c2a", { opacity: 0, x: -400, rotation: -20 }, { opacity: 1, x: 0, rotation: -4, duration: .5, ease: "back.out(1.8)" }, at("L2", "Hütte") - .1);
      tl.fromTo("#c2b", { opacity: 0, x: 400, rotation: 20 }, { opacity: 1, x: 0, rotation: 4, duration: .5, ease: "back.out(1.8)" }, at("L2b", "Kokos-Lodge") - .2);
      tl.fromTo("#st2", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, at("L2b", "bald") - .1);""")

# s03 – Neu 2: Minispiele + Duelle
scene("s03", GL + """
    .stamp { position: absolute; padding: 6px 30px 10px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.95); font-family: "Inter", sans-serif; font-weight: 900; font-size: 76px; opacity: 0; white-space: nowrap; }
    .nr { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 250px; padding: 4px 34px 12px; border-radius: 30px; background: #ffd23f; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 96px; box-shadow: 0 0 0 8px #2a1b12, 0 12px 0 rgba(0,0,0,.3); transform: rotate(-4deg); opacity: 0; }
    .card { position: absolute; border-radius: 28px; border: 9px solid #fff; overflow: hidden; box-shadow: 0 0 0 5px #2a1b12, 0 16px 0 rgba(0,0,0,.35); opacity: 0; background: #fff; }
    .card img { display: block; width: 100%; }
    .lab { position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%); white-space: nowrap; padding: 4px 18px 8px; border-radius: 18px; background: #2a1b12; color: #ffd23f; font: 900 32px Inter, sans-serif; }
    .g3 { width: 300px; } 
    #g30 { left: 90px; top: 360px; transform: rotate(-6deg); } #g31 { left: 400px; top: 330px; transform: rotate(3deg); } #g32 { left: 710px; top: 370px; transform: rotate(-2deg); }
    #st3 { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 880px; color: #7b4fe0; border-color: #7b4fe0; transform: rotate(-3deg); }
    #st3b { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1000px; color: #c99a00; border-color: #ffd23f; transform: rotate(2deg); font-size: 56px; }""",
"""      <div class="nr" id="nr3">NEU #2</div>
      <div class="card g3" id="g30"><img src="bilder/spiele/turm.jpg"></div>
      <div class="card g3" id="g31"><img src="bilder/spiele/memory.jpg"></div>
      <div class="card g3" id="g32"><img src="bilder/spiele/krebs.jpg"></div>
      <div id="st3" class="stamp">⚔️ DUELL!</div>
      <div id="st3b" class="stamp">🏆 TOP 3 = MUSCHELN</div>""",
"""      tl.fromTo("#nr3", { opacity: 0, scale: .3, rotation: -20 }, { opacity: 1, scale: 1, rotation: -4, duration: .4, ease: "back.out(3)" }, line("L3")[0] - .05); tl.to("#nr3", { opacity: 0, y: -40, duration: .2 }, line("L3b")[0] - .2);
      ["#g30", "#g31", "#g32"].forEach((q, i) => tl.fromTo(q, { opacity: 0, y: 300, scale: .6 }, { opacity: 1, y: 0, scale: 1, duration: .45, ease: "back.out(2)" }, at("L3", "vier") - .1 + i * .15));
      tl.fromTo("#st3", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, at("L3b", "Duell") - .1);
      [[14,-8],[-14,6],[8,6],[0,0]].forEach(([x, y], i) => tl.to("#st3", { x, y, duration: .05, ease: "none" }, at("L3b", "Duell") + .3 + i * .05));
      tl.fromTo("#st3b", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, at("L3b", "Top") - .1);""")

# s04 – Neu 3: Angeln
scene("s04", GL + """
    .stamp { position: absolute; padding: 6px 30px 10px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.95); font-family: "Inter", sans-serif; font-weight: 900; font-size: 76px; opacity: 0; white-space: nowrap; }
    .nr { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 250px; padding: 4px 34px 12px; border-radius: 30px; background: #ffd23f; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 96px; box-shadow: 0 0 0 8px #2a1b12, 0 12px 0 rgba(0,0,0,.3); transform: rotate(-4deg); opacity: 0; }
    .card { position: absolute; border-radius: 28px; border: 9px solid #fff; overflow: hidden; box-shadow: 0 0 0 5px #2a1b12, 0 16px 0 rgba(0,0,0,.35); opacity: 0; background: #fff; }
    .card img { display: block; width: 100%; }
    .lab { position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%); white-space: nowrap; padding: 4px 18px 8px; border-radius: 18px; background: #2a1b12; color: #ffd23f; font: 900 32px Inter, sans-serif; }
    .fi { position: absolute; width: 330px; height: 330px; border-radius: 50%; background: radial-gradient(circle, #e7f6ff, #8fd3f4); box-shadow: 0 0 0 9px #fff, 0 0 0 15px #2a1b12; display: grid; place-items: center; font-size: 190px; opacity: 0; }
    #f40 { left: 140px; top: 520px; } #f41 { left: 610px; top: 560px; }
    #st4 { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 980px; color: #0a9fa6; border-color: #0a9fa6; transform: rotate(-3deg); }""",
"""      <div class="nr" id="nr4">NEU #3</div>
      <div class="fi" id="f40">🪼</div><div class="fi" id="f41">🌿</div>
      <div id="st4" class="stamp">🎣 NEU IM FISCH-ALBUM</div>""",
"""      tl.fromTo("#nr4", { opacity: 0, scale: .3, rotation: -20 }, { opacity: 1, scale: 1, rotation: -4, duration: .4, ease: "back.out(3)" }, line("L4")[0] - .05); tl.to("#nr4", { opacity: 0, y: -40, duration: .2 }, line("L4")[1] - .1);
      tl.fromTo("#f40", { opacity: 0, y: 300, rotation: -40 }, { opacity: 1, y: 0, rotation: 0, duration: .5, ease: "back.out(2.5)" }, at("L4", "Quallen") - .1);
      tl.fromTo("#f41", { opacity: 0, y: 300, rotation: 40 }, { opacity: 1, y: 0, rotation: 0, duration: .5, ease: "back.out(2.5)" }, at("L4", "Seegras") - .1);
      tl.to(["#f40", "#f41"], { y: -20, duration: .4, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L4", "Seegras") + .4);
      tl.fromTo("#st4", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, at("L4", "Angeln") - .1);""")

# s05 – Verlosung Inhaber Golden Pearl
NAMES = ["prvt.lott1", "_bruno_017", "malin3270", "martha_smile", "d9750075", "linchen.fks", "lena.bhg", "marijadukic11", "in.yor_dreams", "vico_drks", "julia.m.m.17", "julia.cbl", "maestronewyork", "k1905_0", "the_girl_indahood77", "lilli.ber7in"]
scene("s05", GL + """
    .stamp { position: absolute; padding: 6px 30px 10px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.95); font-family: "Inter", sans-serif; font-weight: 900; font-size: 76px; opacity: 0; white-space: nowrap; }
    .nr { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 250px; padding: 4px 34px 12px; border-radius: 30px; background: #ffd23f; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 96px; box-shadow: 0 0 0 8px #2a1b12, 0 12px 0 rgba(0,0,0,.3); transform: rotate(-4deg); opacity: 0; }
    .card { position: absolute; border-radius: 28px; border: 9px solid #fff; overflow: hidden; box-shadow: 0 0 0 5px #2a1b12, 0 16px 0 rgba(0,0,0,.35); opacity: 0; background: #fff; }
    .card img { display: block; width: 100%; }
    .lab { position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%); white-space: nowrap; padding: 4px 18px 8px; border-radius: 18px; background: #2a1b12; color: #ffd23f; font: 900 32px Inter, sans-serif; }
    #l5 { top: 260px; } #l5 b { font-size: 60px; }
    #rl { position: absolute; left: 90px; right: 90px; top: 560px; height: 170px; border-radius: 40px; overflow: hidden; background: #fff; box-shadow: 0 0 0 9px #ffd23f, 0 0 0 16px #2a1b12, 0 20px 40px rgba(0,0,0,.4); opacity: 0; }
    #rl .r { position: absolute; left: 0; right: 0; top: 0; }
    #rl .r div { height: 170px; font: 400 74px/170px "Lilita One", sans-serif; color: #2a1b12; text-align: center; white-space: nowrap; }
    #wn { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 520px; color: #2a1b12; background: #ffd23f; border-color: #fff; font-size: 96px; transform: rotate(-3deg); box-shadow: 0 0 0 7px #2a1b12, 0 0 90px rgba(255,210,60,.9); }
    #wn small { display: block; font-size: 40px; text-align: center; }
    #gp5 { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 820px; color: #c99a00; border-color: #ffd23f; transform: rotate(2deg); font-size: 60px; }
    .pt { position: absolute; font-size: 84px; line-height: 1; width: 84px; height: 84px; opacity: 0; }""",
"""      <div id="l5" class="gl"><small>🎁 Verlosung unter allen Followern</small><b>👑 Inhaber Golden Pearl</b></div>
      <div id="rl"><div class="r">""" + "".join(f"<div>@{n}</div>" for n in NAMES) + """<div>@taliasonnen</div></div></div>
      <div id="wn" class="stamp"><small>🎉 GEWONNEN!</small>@taliasonnen</div>
      <div id="gp5" class="stamp">💎 DAS GOLDEN PEARL GEHÖRT DIR</div>
      """ + "".join(f'<div class="pt" id="pc{i}" style="left:498px;top:600px">{e}</div>' for i, e in enumerate("🎉💎✨🥳🎊⭐🎉💎✨🥳🎊⭐")) + """""",
"""      const t = line("L5")[0], S = line("L5b")[0], W = line("L5c")[0];
      tl.fromTo("#l5", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .4, ease: "back.out(2)" }, t - .1);
      tl.fromTo("#rl", { opacity: 0, scale: .7 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }, S - .4);
      tl.fromTo("#rl .r", { y: 0 }, { y: -170 * """ + str(len(NAMES)) + """, duration: W - S + .35, ease: "power3.inOut" }, S - .1);
      tl.to("#rl", { opacity: 0, scale: 1.2, duration: .2 }, W + .25);
      tl.to("#l5", { opacity: 0, duration: .2 }, W + .25);
      tl.fromTo("#wn", { opacity: 0, scale: 2.4, rotation: -12 }, { opacity: 1, scale: 1, rotation: -3, duration: .35, ease: "back.out(3)" }, W + .25);
      [[14,-8],[-14,6],[8,6],[0,0]].forEach(([x, y], i) => tl.to("#wn", { x, y, duration: .05, ease: "none" }, W + .6 + i * .05));
      [...Array(12).keys()].forEach(i => { const a = i / 12 * 6.283, r = 320 + (i % 3) * 120; tl.fromTo("#pc" + i, { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: Math.cos(a) * r, y: Math.sin(a) * r * .9, scale: 1.3, rotation: 200, opacity: 0, duration: 1.3, ease: "power3.out", immediateRender: false }, W + .3 + (i % 3) * .04); });
      tl.fromTo("#gp5", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .35, ease: "elastic.out(1.2, .4)" }, at("L5d", "gehört") - .1);""")

# s07 – Folg mir
scene("s06", GL + """
    #t7 { top: 250px; } #t7 b { font-size: 76px; }
    #f7 { position: absolute; left: 0; right: 0; margin: 0 auto; top: 520px; width: 440px; height: 112px; border-radius: 56px; background: #fe2c55; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 50px; display: grid; place-items: center; box-shadow: 0 18px 40px rgba(254,44,85,.45); }""",
"""      <div id="t7" class="gl"><small>Deine Hütte wartet</small><b>@muscheltal</b></div>
      <div id="f7">+ Folgen</div>""",
"""      const t = line("L6")[0], fo = at("L6", "Folg");
      tl.fromTo("#t7", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, t - .2);
      tl.fromTo("#f7", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .45, ease: "back.out(2)" }, fo);
      tl.to("#f7", { scale: 1.06, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, fo + .5);""", blur=False)
