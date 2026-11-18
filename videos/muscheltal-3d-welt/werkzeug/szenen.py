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

# s01 – AUF DIESER INSEL WOHNEN ALLE MEINE FOLLOWER – groß, ab Sekunde 0, mit Blitz
scene("s01", GL + """
    #fl1 { position: absolute; inset: 0; background: #fff; }
    #t1 { top: 220px; padding: 28px 46px 36px; }
    #t1 small { font-size: 50px; letter-spacing: 0; text-transform: none; opacity: 1; font-weight: 900; color: #fff; }
    #t1 b { font-size: 132px; line-height: .98; letter-spacing: -.02em; }
    #t1 b span { color: #ffe08a; text-shadow: 0 6px 30px rgba(255,120,60,.6); }""",
"""      <div id="t1" class="gl"><small>Auf dieser Insel wohnen</small><b>ALLE meine<br><span>Follower</span></b></div>
      <div id="fl1"></div>""",
"""      tl.fromTo("#fl1", { opacity: .9 }, { opacity: 0, duration: .35, ease: "power2.out" }, 0);
      tl.fromTo("#t1", { scale: 1.45, rotation: -4 }, { scale: 1, rotation: 0, duration: .4, ease: "back.out(2.2)" }, 0);
      tl.fromTo("#t1 b", { scale: 1 }, { scale: 1.1, duration: .18, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 50%" }, at("L1", "ALLE") - .03);
      tl.fromTo("#t1 b span", { scale: 1 }, { scale: 1.16, duration: .2, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 60%" }, at("L1", "Follower") - .03);""", blur=False)

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
BN = [("L3", "Dönerbude", "🥙 Dönerbude"), ("L3", "Bäckerei", "🥐 Bäckerei"), ("L3s", "Strandbar", "🍹 Strandbar"), ("L3s", "Tierheim", "🐾 Tierheim · im Bau"), ("L3k", "Kokos-Club", "🪩 Kokos-Club"), ("L3g", "Game", "🎮 Game Lagoon"), ("L3c", "Freiluftkino", "🎬 Freiluftkino")]
scene("s03", GL + """
    .bn { top: 240px; } .bn b { font-size: 70px; }""",
"""""" + "".join(f'<div id="bn{i}" class="gl bn"><small>{"Hauptinsel" if l in ("L3", "L3s") else "Kokos-Küste"}</small><b>{t}</b></div>' for i, (l, w, t) in enumerate(BN)) + """""",
"""""" + "\n".join(f'      tl.fromTo("#bn{i}", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, at("{l}", "{w}") - .25);' + (f' tl.to("#bn{i}", {{ opacity: 0, duration: .15 }}, at("{BN[i+1][0]}", "{BN[i+1][1]}") - .4);' if i < len(BN) - 1 else ' tl.to("#bn6", { opacity: 0, duration: .25 }, line("L3c")[1] + .5);') for i, (l, w, t) in enumerate(BN)))

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
    #t6 { top: 230px; } #t6 b { font-size: 92px; color: #ffe08a; }
    #c6 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 520px; padding: 20px 40px 24px; border-radius: 44px; background: #fe2c55; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; box-shadow: 0 18px 40px rgba(254,44,85,.45); }""",
"""      <div id="t6" class="gl"><small>Eure Inselwelt</small><b>Was fehlt noch? 🤔</b></div>
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
