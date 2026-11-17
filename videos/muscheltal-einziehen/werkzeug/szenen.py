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
      <div id="e1-b" class="pl">wohnen schon auf Muschel-Tal! 🏝️</div>""",
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

# s02 – Zoom aus einer Hütte auf die ganze Insel
scene("s02", LILITA + "\n    " + PILL + """
    #e2-p { top: 250px; font-size: 48px; background: linear-gradient(100deg, #ff2e7e, #7b3fe0); }
    #e2-r { position: absolute; left: 390px; top: 810px; width: 300px; height: 300px; border-radius: 50%; border: 12px solid #ffe14a; box-shadow: 0 0 40px 10px rgba(255,225,74,.8); opacity: 0; }""",
"""      <div id="e2-r" data-layout-ignore></div>
      <div id="e2-p" class="pl">🏠 Folgen = Hütte mit deinem @Namen</div>""",
"""      const t2 = line("L2")[0], fo = at("L2", "folgt");
      tl.fromTo("#e2-r", { opacity: 1, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2)", immediateRender: false }, t2 - .3);
      tl.to("#e2-r", { scale: 1.12, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut" }, t2 + .1);
      tl.to("#e2-r", { opacity: 0, scale: .2, duration: .3 }, t2 + .9);
      tl.fromTo("#e2-p", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .1);
      tl.to("#e2-p", { scale: 1.06, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, fo + .4);""")

# s03 – Neu eingezogen: die 5 Neuesten
scene("s03", LILITA + "\n    " + PILL + """
    #e3-c { position: absolute; left: 120px; right: 120px; top: 230px; padding: 18px 26px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #1a0f08, 0 14px 0 rgba(0,0,0,.3), 0 0 50px 12px rgba(46,158,91,.5); font-family: "Inter", sans-serif; }
    #e3-c .h { font-family: "Lilita One", sans-serif; font-size: 56px; color: #2e9e5b; text-align: center; margin-bottom: 6px; }
    #e3-c .r { display: flex; align-items: center; gap: 16px; font-weight: 900; font-size: 42px; color: #2a1b12; padding: 8px 4px; border-top: 3px solid #eef3e8; }
    #e3-c .r b { font-size: 40px; }
    #e3-c .r i { margin-left: auto; font-style: normal; font-size: 26px; color: #fff; background: #ff2e7e; padding: 2px 12px 4px; border-radius: 10px; }""",
"""      <div id="e3-c"><div class="h">🆕 Neu eingezogen</div>""" + "".join(f'<div class="r" id="e3-r{k}"><b>🛖</b>@{n}<i>NEU</i></div>' for k, n in enumerate(NEU)) + """</div>""",
"""      const t3 = line("L3")[0];
      tl.fromTo("#e3-c", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, t3 - .1);
      tl.fromTo("#e3-c .r", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: .22, stagger: .3, ease: "back.out(2.4)" }, t3 + .25);""")

# s04 – Noch 213 bis 1.000 – dann wird es ein Spiel
scene("s04", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #e4-h { position: absolute; left: 70px; right: 70px; top: 260px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #e4-h .r { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 42px; } #e4-h .r b { font-size: 66px; color: #2e9e5b; }
    #e4-h .bar { height: 34px; border-radius: 17px; background: #ece4d8; margin-top: 10px; overflow: hidden; } #e4-h .bar i { display: block; height: 100%; width: 0; border-radius: 17px; background: linear-gradient(90deg, #2e9e5b, #8be06a); }
    #e4-h .f { margin-top: 8px; font-weight: 900; font-size: 34px; color: #e2560c; }
    #e4-s { top: 560px; font-size: 76px; background: linear-gradient(135deg, #ff2e9a, #7b3fe0); transform: rotate(-2deg); box-shadow: 0 0 0 8px #1a0f08, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 16px rgba(255,46,154,.65); }""",
"""      <div id="e4-h"><div class="r"><div>🏝️ Bewohner</div><div><b id="e4-n">0</b> / 1.000</div></div><div class="bar"><i id="e4-b"></i></div><div class="f">Nur noch 213!</div></div>
      <div id="e4-s" class="big">🎮 DANN: DAS SPIEL!</div>""",
"""      const t4 = line("L4")[0], sp = at("L4", "Spiel");
      tl.fromTo("#e4-h", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, t4 - .1);
      count(tl, "#e4-n", 0, 787, t4 + .2, 1.2, "", "", "power2.out");
      tl.fromTo("#e4-b", { width: "0%" }, { width: "78.7%", duration: 1.2, ease: "power2.out" }, t4 + .2);
      tl.fromTo("#e4-s", { opacity: 0, scale: 3.2 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, sp - .15);
      tl.to("#e4-s", { x: 10, duration: .05, yoyo: true, repeat: 7, ease: "none" }, sp + .2);""")

# s05 – Folg mir und zieh heute noch ein (leere Hütte mit „@Dein Name?“)
scene("s05", LILITA + "\n    " + PILL + "\n" + FOLLOW + "\n    " + CF_CSS.replace("top: 700px", "top: 760px") + """
    #e5-btn { top: 260px; } #e5-hand { left: 690px; top: 310px; }
    #e5-hut { position: absolute; left: 0; right: 0; margin: 0 auto; top: 440px; width: 420px; text-align: center; }
    #e5-hut .e { font-size: 230px; line-height: 1; filter: drop-shadow(0 12px 0 rgba(0,0,0,.25)); }
    #e5-hut .n { display: inline-block; margin-top: -10px; padding: 6px 26px 10px; border-radius: 18px; background: #fff; box-shadow: 0 0 0 5px #1a0f08; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #e8467c; }""",
"""      <div id="e5-btn" class="fbtn">+ Folgen<div id="e5-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="e5-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="e5-hut"><div class="e">🛖</div><div class="n" id="e5-name">@Dein Name?</div></div>
      <div id="e5-cf"></div>""",
"""      const t5 = line("L5")[0], fo = at("L5", "Folg"), he = at("L5", "heute");
      tl.fromTo("#e5-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, t5 - .2);
      tl.fromTo("#e5-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo);
      tl.to("#e5-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .3);
      tl.to("#e5-btn2", { opacity: 1, duration: .05 }, fo + .4);
      tl.to("#e5-hand", { opacity: 0, duration: .2 }, fo + .8);
      tl.fromTo("#e5-hut", { opacity: 0, scale: .2, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: .35, ease: "back.out(2.2)" }, fo + .45);
      tl.to("#e5-name", { scale: 1.1, duration: .18, yoyo: true, repeat: 7, ease: "sine.inOut" }, he);
      { """ + CONF_JS.replace("SEED", "55").replace("BOX", "e5-cf").replace("T0", "(fo + .45)") + """ }""", blur=False)
