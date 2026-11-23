import json
import sys
from pathlib import Path
D = Path(sys.argv[1]); LOGO = Path(sys.argv[2]).read_text().strip()
SHELL = '<svg viewBox="0 0 64 64"><path d="M32 47 L8.8 40.8 Q5.0 34.0 12.7 32.7 Q11.6 25.0 19.2 26.7 Q21.0 19.1 27.5 23.4 Q32.0 17.0 36.5 23.4 Q43.0 19.1 44.8 26.7 Q52.4 25.0 51.3 32.7 Q59.0 34.0 55.2 40.8 Z" fill="#ffc7b2" stroke="#2a1b12" stroke-width="3" stroke-linejoin="round"/><path d="M32 45L13.9 33.6M32 45L20.0 27.9M32 45L27.8 24.9M32 45L36.2 24.9M32 45L44.0 27.9M32 45L50.1 33.6" stroke="#c43d6b" stroke-width="2" stroke-linecap="round"/></svg>'
LILITA = '@font-face { font-family: "Lilita One"; src: url("assets/fonts/LilitaOne-Regular.woff2") format("woff2"); font-weight: 400; }'

V1 = ""

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

NEO = """
    .neo { position: absolute; left: 60px; right: 190px; margin: 0 auto; width: fit-content; max-width: 830px; padding: 14px 34px 18px; border-radius: 30px; opacity: 0;
      background: linear-gradient(160deg, rgba(24,10,48,.9), rgba(8,4,24,.92)); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.7), inset 0 0 24px rgba(63,240,255,.25);
      font-family: "Lilita One", sans-serif; color: #fff; text-align: center; line-height: 1.02; white-space: normal; }
    .neo.pk { border-color: #ff3dbd; box-shadow: 0 0 30px rgba(255,61,189,.75), inset 0 0 24px rgba(255,61,189,.25); }
    .neo.li { border-color: #b6ff3b; box-shadow: 0 0 30px rgba(182,255,59,.7), inset 0 0 24px rgba(182,255,59,.25); }
    .neo.go { border-color: #ffd23f; box-shadow: 0 0 34px rgba(255,210,63,.8), inset 0 0 24px rgba(255,210,63,.25); }
    .neo small { display: block; font: 900 30px Inter, sans-serif; letter-spacing: .14em; color: #3ff0ff; margin-bottom: 6px; }
    .neo.pk small { color: #ff3dbd; } .neo.li small { color: #b6ff3b; } .neo.go small { color: #ffd23f; }
    .big { position: absolute; left: 60px; right: 190px; text-align: center; font-family: "Lilita One", sans-serif; color: #fff; line-height: .92; opacity: 0;
      -webkit-text-stroke: 16px #0a0418; paint-order: stroke fill; }
    .big .c { color: #3ff0ff; } .big .p { color: #ff3dbd; } .big .l { color: #b6ff3b; } .big .g { color: #ffd23f; }
    .fl { position: absolute; inset: 0; background: #fff; opacity: 0; }
"""
def Z(sel, t):
    return f'tl.fromTo("{sel}", {{ opacity: 0, scale: 3, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: .24, ease: "back.out(2.2)" }}, {t});'
def OUT(sel, t):
    return f'tl.to("{sel}", {{ opacity: 0, scale: .6, duration: .14, ease: "power2.in" }}, {t});'
def SHAKE(sid, t):
    return f'[[22,-12],[-24,10],[16,14],[-12,-10],[0,0]].forEach(([x, y], i) => tl.to("#{sid}-stage", {{ x, y, duration: .04, ease: "none" }}, {t} + i * .04));'
def FLASH(t, o=.8):
    return f'tl.fromTo(".fl", {{ opacity: {o} }}, {{ opacity: 0, duration: .28, immediateRender: false }}, {t});'
CMT_ = ""

# s01 – Hook: Satz ab Frame 0 sichtbar, gesprochenes Wort blitzt riesig auf
scene("s01", NEO + """
    #hk { position: absolute; left: 60px; right: 60px; top: 230px; text-align: center; font-family: "Lilita One", sans-serif; line-height: 1.0; -webkit-text-stroke: 18px #0a0418; paint-order: stroke fill; }
    #hk .w { display: inline-block; position: relative; color: #fff; font-size: 170px; margin: 0 .06em; transform-origin: 50% 60%; }
    #hk #w0 { color: #ffd23f; } #hk #w1 { color: #ffd23f; } #hk #w2 { font-size: 130px; color: #3ff0ff; } #hk #w3, #hk #w4 { color: #ff3dbd; }
    #hk #w0 { transform-origin: 10% 60%; } #hk #w1 { transform-origin: 90% 60%; }
    #g1 { top: 1000px; font-size: 66px; white-space: normal; width: 820px; }""",
"""      <div id="hk"><span class="w" id="w0">TAG</span><span class="w" id="w1">13</span><br><span class="w" id="w2">MUSCHEL-TAL</span><br><span class="w" id="w3">WÄHLT</span><br><span class="w" id="w4">NEU!</span></div>
      <div id="g1" class="neo pk"><small>🎁 UND DANN NOCH …</small>JEMAND GEHEIMNISVOLLES HAT EUCH WAS GESCHENKT</div>
      <div class="fl"></div>""",
"""      const ws = [["tag",.04,.19],["13",.22,.77],["muscheltal",.89,1.31],["wählt",1.34,1.89],["neu",1.94,2.23]] /* aus narration.wav gemessen – bei neuer Stimme neu messen */, SC = [1.9, 1.9, 1.18, 1.45, 1.45], COL = ["#ffd23f", "#ffd23f", "#3ff0ff", "#ff3dbd", "#ff3dbd"];
      tl.fromTo("#hk", { scale: 1.2 }, { scale: 1, duration: .18, ease: "power3.out" }, 0);
      """ + FLASH(0, .9) + """
      ws.slice(0, 5).forEach((w, i) => { const id = "#w" + i, t0 = Math.max(0, w[1] - .03);
        tl.set(id, { zIndex: 5 }, t0);
        tl.fromTo(id, { scale: 1, color: COL[i], textShadow: "0 0 0px #fff" }, { scale: SC[i], color: "#ffffff", textShadow: "0 0 50px " + COL[i] + ", 0 0 120px " + COL[i], duration: .07, ease: "power4.out", immediateRender: false }, t0);
        tl.to(id, { scale: 1, color: COL[i], textShadow: "0 0 0px #fff", duration: .2, ease: "back.out(2)" }, Math.max(t0 + .1, w[2] - .08));
        tl.set(id, { zIndex: 1 }, w[2] + .15);
        tl.fromTo(".fl", { opacity: .3 }, { opacity: 0, duration: .12, immediateRender: false }, t0);
        [[10,-6],[-12,6],[0,0]].forEach(([x, y], n) => tl.to("#s01-stage", { x, y, duration: .03, ease: "none" }, t0 + n * .03)); });
      const B = line("L1b")[0];
      """ + Z("#g1", "B") + """
      tl.to("#g1", { scale: 1.06, duration: .22, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L1b", "geschenkt"));""")

# s02 – Neuwahl Bürgermeister + Palast-Leitung, Bürgermeister soll sich melden
scene("s02", NEO + """
    #b1 { top: 230px; font-size: 150px; }
    #b2 { top: 460px; font-size: 76px; } #b3 { top: 620px; font-size: 76px; }
    #b4 { top: 460px; font-size: 70px; white-space: normal; width: 820px; } #b5 { top: 780px; font-size: 58px; white-space: normal; width: 780px; }""",
"""      <div id="b1" class="big"><span class="p">NEU</span>WAHL! 🗳️</div>
      <div id="b2" class="neo go">👑 BÜRGERMEISTER</div>
      <div id="b3" class="neo">🏰 PALAST-LEITUNG</div>
      <div id="b4" class="neo pk"><small>📩 NEUER BÜRGERMEISTER</small>MELDE DICH BEI UNS!</div>
      <div id="b5" class="neo li">⚖️ DU TRIFFST DIE NÄCHSTE ENTSCHEIDUNG</div>
      <div class="fl"></div>""",
"""      const t = line("L2")[0], M = line("L2b")[0];
      """ + Z("#b1", "t - .05") + FLASH("t", .5) + """
      """ + Z("#b2", 'at("L2", "Bürgermeister") - .05') + SHAKE("s02", 'at("L2", "Bürgermeister")') + """
      """ + Z("#b3", 'at("L2", "Palast") - .05') + SHAKE("s02", 'at("L2", "Palast")') + """
      """ + OUT("#b2", "M - .15") + OUT("#b3", "M - .15") + """
      """ + Z("#b4", 'at("L2b", "Melde") - .05') + """
      tl.to("#b4", { scale: 1.06, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L2b", "Melde") + .4);
      """ + Z("#b5", 'at("L2b", "nächste") - .05'))

# s03 – Tierheim-Team: 4 Namen
scene("s03", NEO + """
    #c1 { top: 250px; font-size: 80px; white-space: nowrap; }
    .nm { position: absolute; width: 390px; padding: 18px 10px 20px; border-radius: 26px; background: #fff; color: #1a0f08; text-align: center; opacity: 0;
      font: 900 33px Inter, sans-serif; box-shadow: 0 0 0 6px #ff7a59, 0 12px 0 rgba(0,0,0,.3); }
    .nm b { display: block; font-size: 54px; line-height: 1; margin-bottom: 6px; }
    #c6 { top: 860px; font-size: 64px; }""",
"""      <div id="c1" class="big">🐾 <span class="l">TIERHEIM</span>-TEAM</div>
      <div id="n0" class="nm" style="left:70px;top:430px"><b>🐶</b>@swg.seliii</div>
      <div id="n1" class="nm" style="left:480px;top:430px"><b>🐱</b>@j7summ3r</div>
      <div id="n2" class="nm" style="left:70px;top:620px"><b>🐰</b>@el1naa_13</div>
      <div id="n3" class="nm" style="left:480px;top:620px"><b>🐹</b>@theycallmealeaaa</div>
      <div id="c6" class="neo pk">💖 WILLKOMMEN IM TEAM!</div>
      <div class="fl"></div>""",
"""      const t = line("L3")[0], V = at("L3", "vier");
      """ + Z("#c1", "t - .05") + """
      [0, 1, 2, 3].forEach(i => tl.fromTo("#n" + i, { opacity: 0, scale: .2, rotation: i % 2 ? 12 : -12 }, { opacity: 1, scale: 1, rotation: i % 2 ? 2 : -2, duration: .3, ease: "back.out(2.6)" }, V - .1 + i * .22));
      """ + Z("#c6", 'at("L3", "willkommen") - .05') + FLASH('at("L3", "willkommen")', .5))

# s04 – Geschenk des Schöpfers: Anlegestelle fertig, Fähre Seestern
scene("s04", NEO + """
    #a1 { top: 230px; font-size: 120px; }
    #a2 { top: 440px; font-size: 54px; } #a3 { top: 610px; font-size: 62px; }
    #a4 { top: 450px; font-size: 64px; } #a5 { top: 610px; font-size: 58px; }""",
"""      <div id="a1" class="big">🎁 DAS <span class="g">GESCHENK</span></div>
      <div id="a2" class="neo pk"><small>🔮 VOM GEHEIMNISVOLLEN</small>SCHÖPFER VON MUSCHEL-TAL</div>
      <div id="a3" class="neo li">⚓ ANLEGESTELLE FERTIG!</div>
      <div id="a4" class="neo go">⛴️ FÄHRE „SEESTERN“</div>
      <div id="a5" class="neo">🏝️ ⇄ 🥥 ZWISCHEN DEN INSELN!</div>
      <div class="fl"></div>""",
"""      const t = line("L4")[0], F = line("L4b")[0];
      """ + Z("#a1", "t - .05") + """
      """ + Z("#a2", 'at("L4", "geheimnisvolle") - .05') + FLASH('at("L4", "Schöpfer")', .6) + """
      """ + Z("#a3", 'at("L4", "Anlegestelle") - .05') + SHAKE("s04", 'at("L4", "Anlegestelle")') + """
      """ + OUT("#a2", "F - .15") + OUT("#a3", "F - .15") + """
      """ + Z("#a4", 'at("L4b", "Fähre") - .05') + """
      """ + Z("#a5", 'at("L4b", "zwischen") - .05'))

# s05 – Goldene Kokoshütte für Bewohner Nr. 1.000
scene("s05", NEO + """
    #h1 { top: 210px; font-size: 118px; }
    #h1 .g { text-shadow: 0 0 40px rgba(255,210,63,.9); }
    #h2 { top: 1450px; font-size: 64px; }
    #h3 { top: 1600px; font-size: 96px; }
    .sp { position: absolute; font-size: 70px; opacity: 0; }""",
"""      <div id="h1" class="big">DIE <span class="g">GOLDENE</span><br><span class="g">KOKOSHÜTTE</span> ✨</div>
      <div id="h2" class="neo go"><small>RESERVIERT FÜR</small>🏠 BEWOHNER NR. 1.000</div>
      <div id="h3" class="big">BIST DAS <span class="l">DU?</span> 👀</div>
      """ + "".join(f'<div class="sp" id="sp{i}" style="left:{x}px;top:{y}px">✨</div>' for i, (x, y) in enumerate([(260, 760), (700, 720), (330, 1000), (640, 1040), (480, 640)])) + """
      <div class="fl"></div>""",
"""      const t = line("L5")[0], T = line("L5b")[0];
      """ + Z("#h1", 'at("L5", "goldene") - .05') + FLASH('at("L5", "goldene")', .7) + """
      [0,1,2,3,4].forEach(i => tl.fromTo("#sp" + i, { opacity: 0, scale: .2 }, { opacity: 1, scale: 1.3, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L5", "goldene") + i * .15));
      """ + Z("#h2", 'at("L5b", "tausendste") - .05') + """
      """ + Z("#h3", 'at("L5b", "DU") - .1') + SHAKE("s05", 'at("L5b", "DU")'))

# s06 – Bei 1.000 Bewohnern startet das Spiel: 819 / noch 181
scene("s06", NEO + """
    #r7 { top: 240px; font-size: 64px; white-space: normal; width: 820px; }
    #br { position: absolute; left: 80px; right: 210px; top: 500px; padding: 20px; border-radius: 30px; background: rgba(10,4,24,.96); opacity: 0; }
    #br .tr { height: 90px; border-radius: 45px; background: rgba(10,4,24,.85); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.6); overflow: hidden; }
    #br .fi { height: 100%; width: 0; background: linear-gradient(90deg, #3ff0ff, #ff3dbd); }
    #br .lb { display: flex; justify-content: space-between; margin-top: 16px; font: 400 64px "Lilita One", sans-serif; color: #fff; -webkit-text-stroke: 10px #0a0418; paint-order: stroke fill; }
    #br .lb span:last-child { color: #b6ff3b; }
    #k7 { top: 760px; font-size: 76px; }""",
"""      <div id="r7" class="neo li"><small>🎮 BEI 1.000 BEWOHNERN</small>STARTET DAS SPIEL!</div>
      <div id="br"><div class="tr"><div class="fi"></div></div><div class="lb"><span id="cn">0</span><span>1.000</span></div></div>
      <div id="k7" class="neo pk"><small>ES FEHLEN NUR NOCH</small>181 BEWOHNER 👀</div>
      <div class="fl"></div>""",
"""      const t = line("L6")[0], N = line("L6b")[0];
      """ + Z("#r7", 'at("L6", "startet") - .05') + SHAKE("s06", 'at("L6", "startet")') + """
      tl.fromTo("#br", { opacity: 0 }, { opacity: 1, duration: .25 }, N - .1);
      tl.fromTo("#br .fi", { width: "0%" }, { width: "81.9%", duration: 1.4, ease: "power2.out" }, N);
      count(tl, "#cn", 0, 819, N, 1.4);
      """ + Z("#k7", 'at("L6b", "181") - .05') + FLASH('at("L6b", "181")', .5) + """
      tl.to("#k7", { scale: 1.07, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L6b", "181") + .4);""")

# s07 – Freunde markieren + Folgen
scene("s07", NEO + CMT_ + FOLLOW + """
    #m1 { top: 230px; font-size: 104px; }
    #m2 { position: absolute; left: 110px; width: 720px; top: 500px; border-radius: 30px; padding: 22px 26px; background: #fff; opacity: 0; box-shadow: 0 14px 30px rgba(0,0,0,.45); font: 700 40px/1.3 Inter, sans-serif; color: #111; }
    #m2 b { color: #fe2c55; } #m2 small { display: block; font-size: 28px; color: #888; margin-top: 8px; }
    #fb { top: 800px; opacity: 0; }""",
"""      <div id="m1" class="big">👯 <span class="l">MARKIERE</span><br>DEINE FREUNDE</div>
      <div id="m2"><b>@deine.beste</b> zieh neben mich! 🏡🐚<small>❤️ 24 · Antworten</small></div>""",
"""      const t = line("L7")[0];
      """ + Z("#m1", "t - .05") + """
      tl.fromTo("#m2", { opacity: 0, y: 60, rotation: -3 }, { opacity: 1, y: 0, rotation: -1.5, duration: .3, ease: "back.out(2)" }, at("L7", "neben") - .2);""")

# s08 – Abstimmung: Katzencafé oder Hotel Sandkorn
scene("s08", NEO + """
    #v1 { top: 210px; font-size: 96px; white-space: nowrap; }
    #v2 { top: 360px; font-size: 46px; }
    .vc { position: absolute; top: 640px; width: 340px; height: 380px; border-radius: 34px; background: #fff; overflow: hidden; opacity: 0; box-shadow: 0 0 0 7px var(--c), 0 0 40px var(--c); }
    .vc .e { height: 250px; display: grid; place-items: center; font-size: 110px; white-space: nowrap; background: linear-gradient(180deg, #fff3d6, #fff); }
    .vc .l { height: 130px; display: grid; place-items: center; font: 400 50px/1 "Lilita One", sans-serif; color: #fff; background: var(--c); text-align: center; }
    #vs { position: absolute; left: 405px; top: 785px; width: 110px; text-align: center; font: 400 66px "Lilita One", sans-serif; color: #ffd23f; -webkit-text-stroke: 12px #0a0418; paint-order: stroke fill; opacity: 0; }
    #v5 { top: 1560px; font-size: 50px; }
    #v6 { top: 1580px; font-size: 52px; }""",
"""      <div id="v1" class="big">🗳️ <span class="g">ABSTIMMUNG!</span></div>
      <div id="v2" class="neo pk"><small>🔮 DER SCHÖPFER VON MUSCHEL-TAL</small>SCHENKT EUCH NOCH EIN GEBÄUDE</div>
      <div class="vc" id="v3" style="left:60px;--c:#ff3dbd"><div class="e">🐱☕</div><div class="l">KATZEN-<br>CAFÉ</div></div>
      <div id="vs">VS</div>
      <div class="vc" id="v4" style="left:520px;--c:#13a8d0"><div class="e">🏨</div><div class="l">HOTEL<br>SANDKORN</div></div>
      <div id="v5" class="neo li">💬 STIMMT IN DEN KOMMIS AB!</div>
      <div class="fl"></div>""",
"""      const t = line("L8")[0], K = line("L8b")[0], A = line("L8c")[0];
      """ + Z("#v1", "t - .05") + FLASH("t", .5) + """
      """ + Z("#v2", 'at("L8", "Gebäude") - .1') + """
      tl.fromTo("#v3", { opacity: 0, x: -300, rotation: -12 }, { opacity: 1, x: 0, rotation: -3, duration: .35, ease: "back.out(2)" }, at("L8b", "Katzencafé") - .1);
      tl.fromTo("#vs", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, at("L8b", "oder") - .05);
      tl.fromTo("#v4", { opacity: 0, x: 300, rotation: 12 }, { opacity: 1, x: 0, rotation: 3, duration: .35, ease: "back.out(2)" }, at("L8b", "Hotel") - .1);
      """ + SHAKE("s08", 'at("L8b", "Hotel")') + """
      tl.to("#vs", { scale: 1.2, duration: .2, yoyo: true, repeat: 9, ease: "sine.inOut" }, at("L8b", "Hotel") + .4);
      """ + Z("#v5", 'at("L8c", "Kommentaren") - .1') + """
      tl.to(["#v3", "#v4"], { y: -14, duration: .5, yoyo: true, repeat: 5, ease: "sine.inOut" }, A + .5);""")

# s09 – Folgen ganz am Ende
scene("s09", NEO + FOLLOW + """
    #o9 { top: 300px; font-size: 150px; }
    #f9 { top: 520px; opacity: 0; }
    #z9 { top: 720px; font-size: 64px; }""",
"""      <div id="o9" class="big">FOLG <span class="p">MIR</span></div>
      <div id="f9" class="fbtn">+ Folgen<div class="fbtn2">✓ Eingezogen</div></div>
      <div class="fl"></div>""",
"""      const F = at("L9", "Folg");
      """ + Z("#o9", "F - .05") + FLASH("F", .5) + """
      """ + Z("#f9", "F + .25") + """
      tl.to("#f9", { scale: 1.08, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, F + .6);
      tl.to("#f9 .fbtn2", { opacity: 1, duration: .15 }, at("L9", "heute") + .3);
      tl.to("#f9", { scale: 1.12, duration: .15, yoyo: true, repeat: 1 }, at("L9", "heute") + .3);""", blur=False)

# s10 – Verlosung: Job in der Game Lagoon
scene("s10", NEO + CF_CSS + """
    #j1 { top: 220px; font-size: 100px; white-space: nowrap; }
    #j2 { top: 420px; font-size: 60px; }
    #sl { position: absolute; left: 110px; width: 720px; top: 600px; height: 150px; border-radius: 34px; background: #fff; overflow: hidden; opacity: 0;
      box-shadow: 0 0 0 8px #ff3dbd, 0 0 50px rgba(255,61,189,.8); }
    #sl div { position: absolute; left: 0; right: 0; top: 0; height: 150px; display: grid; place-items: center; text-align: center; font: 900 54px Inter, sans-serif; color: #1a0f08; white-space: nowrap; opacity: 0; }
    #sl #wn { color: #ff3dbd; font-size: 64px; }
    #j3 { top: 820px; font-size: 76px; }
    #j4 { top: 1460px; font-size: 56px; }""",
"""      <div id="j1" class="big">🎰 <span class="g">VERLOSUNG!</span></div>
      <div id="j2" class="neo"><small>🎮 1 JOB IN DER</small>GAME LAGOON</div>
      <div id="sl">""" + "".join(f'<div id="rl{i}">{n}</div>' for i, n in enumerate(["@haylie.aeriana", "@lxna826", "@val3n14tina", "@alekskabhv", "@reba_thx", "@amelie.aburg", "@emiliaxlove1", "@probablyfiona", "@polina_ok150", "@skaly.ksss"])) + """<div id="wn">@d9750075</div></div>
      <div id="j3" class="neo li">🎉 GLÜCKWUNSCH!</div>
      <div id="j4" class="neo pk">📩 MELDE DICH BEI UNS!</div>
      <div id="cfb" style="position:absolute;inset:0"></div>
      <div class="fl"></div>""",
"""      const t = line("L10")[0], G = at("L10", "geht"), W = line("L10b")[0];
      """ + Z("#j1", "t - .05") + FLASH("t", .5) + """
      """ + Z("#j2", 'at("L10", "Job") - .05') + """
      tl.fromTo("#sl", { opacity: 0, scale: .5 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2.5)" }, G - .3);
      for (let i = 0; i < 10; i++) { const a = G - .1 + i * ((W - G) / 10); tl.set("#rl" + i, { opacity: 1 }, a); tl.set("#rl" + i, { opacity: 0 }, a + (W - G) / 10); }
      tl.fromTo("#wn", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, W - .05);
      """ + SHAKE("s10", "W") + FLASH("W", .8) + """
      """ + Z("#j3", "W") + """
      """ + CONF_JS.replace("BOX", "cfb").replace("SEED", "77").replace("T0", "W") + """
      """ + Z("#j4", 'at("L10b", "Melde") - .05'))
