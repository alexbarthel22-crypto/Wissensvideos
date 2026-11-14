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



# Story Tag 7 – Überblick Haupt-Insel: Tag 7 online, 1.000 Likes, LIVE-Insel, Spiel bei 1.000
scene("s01", LILITA + "\n    " + PILL + "\n    " + BIG + "\n    " + PT + "\n" + FOLLOW + """
    #st-t { top: 270px; font-size: 92px; background: linear-gradient(135deg, #ff2e7e, #7b3fe0); transform: rotate(-2deg); }
    #st-l { top: 270px; font-size: 100px; background: #e8262f; transform: rotate(-2deg); }
    #st-d { top: 430px; font-size: 54px; background: #fff; color: #e8262f; }
    #st-v { top: 270px; font-size: 76px; background: #e8101e; transform: rotate(-2deg); box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3), 0 0 50px 14px rgba(255,20,30,.6); }
    #st-dot { display: inline-block; width: 40px; height: 40px; border-radius: 50%; background: #fff; margin-right: 16px; vertical-align: 6px; }
    #st-n { top: 420px; font-size: 44px; background: #fff; color: #2a1b12; }
    #st-g { position: absolute; left: 80px; right: 80px; top: 270px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #st-g .r { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 40px; } #st-g .r b { font-size: 64px; color: #7b3fe0; }
    #st-g .bar { height: 30px; border-radius: 15px; background: #ece4d8; margin-top: 10px; overflow: hidden; } #st-g .bar i { display: block; height: 100%; width: 0; border-radius: 15px; background: linear-gradient(90deg, #ff2e7e, #7b3fe0, #2fb3ff); }
    #st-btn { top: 280px; } #st-hand { left: 690px; top: 330px; }""",
"""      <div id="st-t" class="big">🎬 TAG 7 IST ONLINE!</div>
      <div id="st-l" class="big">❤️ 1.000 LIKES!</div>
      <div id="st-d" class="pl">🥹 DANKE an euch alle!</div>
      <div id="st-v" class="big"><span id="st-dot"></span>NEU: LIVESTREAMS</div>
      <div id="st-n" class="pl">🏝️ Baut eine neue Insel von Anfang an!</div>
      <div id="st-g"><div class="r"><div>🎮 Spiel startet bei</div><div><b id="st-c">0</b> / 1.000</div></div><div class="bar"><i id="st-b"></i></div></div>
      <div id="st-btn" class="fbtn">+ Folgen<div id="st-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="st-hand" class="fhand" data-layout-ignore>👆</div>""" + drops("st-h", 22, 7, 'at("L2", "Likes")', 540, 520, "❤️", 560, 760)[0],
"""      const l2 = line("L2")[0], l3 = line("L3")[0], l4 = line("L4")[0], l5 = line("L5")[0], li = at("L2", "Likes"), da = at("L2", "danke"), ne = at("L3", "neue"), fo = at("L5", "Folg");
      tl.fromTo("#st-t", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, 0);
      tl.to("#st-t", { opacity: 0, y: -30, duration: .2 }, l2 - .25);
      tl.fromTo("#st-l", { opacity: 0, scale: .2 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, li - .3);
      tl.to("#st-l", { scale: 1.1, duration: .15, yoyo: true, repeat: 5, ease: "sine.inOut" }, li);
      tl.fromTo("#st-d", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, da - .2);
      tl.to(["#st-l", "#st-d"], { opacity: 0, y: -30, duration: .2 }, l3 - .25);
      tl.fromTo("#st-v", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, l3 - .05);
      tl.to("#st-dot", { opacity: .15, duration: .25, yoyo: true, repeat: 13, ease: "steps(1)" }, l3 + .3);
      tl.fromTo("#st-n", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, ne - .2);
      tl.to(["#st-v", "#st-n"], { opacity: 0, y: -30, duration: .2 }, l4 - .25);
      tl.fromTo("#st-g", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, l4 - .1);
      count(tl, "#st-c", 0, 721, l4 + .1, 1.4, "", "", "power2.out");
      tl.fromTo("#st-b", { width: "0%" }, { width: "72.1%", duration: 1.4, ease: "power2.out" }, l4 + .1);
      tl.to("#st-g", { opacity: 0, y: -30, duration: .2 }, l5 - .25);
      tl.fromTo("#st-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, l5 - .1);
      tl.fromTo("#st-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, l5);
      tl.to("#st-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .3);
      tl.to("#st-btn2", { opacity: 1, duration: .05 }, fo + .4);
      tl.to("#st-hand", { opacity: 0, duration: .2 }, fo + .8);
""" + drops("st-h", 22, 7, 'at("L2", "Likes")', 540, 520, "❤️", 560, 760)[1], blur=False)
