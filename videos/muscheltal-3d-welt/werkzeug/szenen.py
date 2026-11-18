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

# s01 – Titel: MUSCHEL-TAL · 3D
scene("s01", GL + """
    #t1 { top: 250px; }
    #t1 b span { color: #ffe08a; text-shadow: 0 4px 20px rgba(120,20,60,.5); }
    #t1 i { display: inline-block; margin-left: 14px; padding: 4px 16px 6px; border-radius: 14px; background: #fff; color: #e8467c; font-style: normal; font-size: 56px; font-weight: 900; vertical-align: 14px; }""",
"""      <div id="t1" class="gl"><small>Willkommen in</small><b><span>Muschel-Tal</span><i>3D</i></b></div>""",
"""      const t = line("L1")[0];
      tl.fromTo("#t1", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .7, ease: "power3.out" }, Math.max(0, t - .3));""")

# s02 – Jede Hütte = echter Follower
scene("s02", GL + """
    #t2 { top: 250px; } #t2 b { font-size: 64px; }""",
"""      <div id="t2" class="gl"><small>Jede Hütte</small><b>= 1 echter Follower</b></div>""",
"""      const t = line("L2")[0];
      tl.fromTo("#t2", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, t - .2);""")

# s03 – Zahlen: Haupt-Insel / Kokos-Küste
scene("s03", GL + """
    #c1 { top: 230px; left: 70px; right: auto; margin: 0; } #c2 { top: 230px; right: 70px; left: auto; margin: 0; }
    #c1 b, #c2 b { font-size: 110px; }""",
"""      <div id="c1" class="gl"><b id="n1">0</b><small>Haupt-Insel</small></div>
      <div id="c2" class="gl"><b id="n2">0</b><small>Kokos-Küste</small></div>""",
"""      const a = at("L3", "506"), k = at("L3", "284");
      tl.fromTo("#c1", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .5, ease: "power3.out" }, a - .3);
      count(tl, "#n1", 0, 506, a - .2, .9, "", "", "power2.out");
      tl.fromTo("#c2", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .5, ease: "power3.out" }, k - .3);
      count(tl, "#n2", 0, 284, k - .2, .9, "", "", "power2.out");""")

# s04 – jeden Tag neue Leute
scene("s04", GL + """
    #t4 { top: 250px; } #t4 b { font-size: 70px; }""",
"""      <div id="t4" class="gl"><small>Jeden Tag</small><b>+ neue Nachbarn</b></div>""",
"""      const t = line("L4")[0];
      tl.fromTo("#t4", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, t - .2);""")

# s05 – Folg mir
scene("s05", GL + """
    #t5 { top: 250px; } #t5 b { font-size: 76px; }
    #f5 { position: absolute; left: 0; right: 0; margin: 0 auto; top: 520px; width: 440px; height: 112px; border-radius: 56px; background: #fe2c55; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 50px; display: grid; place-items: center; box-shadow: 0 18px 40px rgba(254,44,85,.45); }""",
"""      <div id="t5" class="gl"><small>Deine Hütte wartet</small><b>@muscheltal</b></div>
      <div id="f5">+ Folgen</div>""",
"""      const t = line("L5")[0], fo = at("L5", "Folg");
      tl.fromTo("#t5", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, t - .2);
      tl.fromTo("#f5", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .45, ease: "back.out(2)" }, fo);
      tl.to("#f5", { scale: 1.06, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, fo + .5);""", blur=False)
