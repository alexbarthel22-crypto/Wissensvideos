import json
import sys
from pathlib import Path
D = Path(sys.argv[1]); LOGO = Path(sys.argv[2]).read_text().strip()
SHELL = '<svg viewBox="0 0 64 64"><path d="M32 47 L8.8 40.8 Q5.0 34.0 12.7 32.7 Q11.6 25.0 19.2 26.7 Q21.0 19.1 27.5 23.4 Q32.0 17.0 36.5 23.4 Q43.0 19.1 44.8 26.7 Q52.4 25.0 51.3 32.7 Q59.0 34.0 55.2 40.8 Z" fill="#ffc7b2" stroke="#2a1b12" stroke-width="3" stroke-linejoin="round"/><path d="M32 45L13.9 33.6M32 45L20.0 27.9M32 45L27.8 24.9M32 45L36.2 24.9M32 45L44.0 27.9M32 45L50.1 33.6" stroke="#c43d6b" stroke-width="2" stroke-linecap="round"/></svg>'
LILITA = '@font-face { font-family: "Lilita One"; src: url("assets/fonts/LilitaOne-Regular.woff2") format("woff2"); font-weight: 400; }'

V1 = ""

def scene(sid, css, html, js, blur=True, wipe_in=True):
    css = css + V1 + """
    .wp { position: absolute; left: -140px; top: 0; width: 1360px; height: 1920px; transform: skewX(-12deg); z-index: 50;
      background: linear-gradient(90deg, #13c8d8 0%, #3ff0ff 30%, #ff3dbd 70%, #7a3dff 100%); pointer-events: none; }
    .wp::after { content: "🐚"; position: absolute; left: 50%; top: 50%; font-size: 200px; transform: translate(-50%, -50%) skewX(12deg); }"""
    html = html + '\n      <div class="wp" data-layout-ignore></div>'
    end = (f'tl.fromTo("#{sid}-stage .wp", {{ xPercent: 110 }}, {{ xPercent: 0, duration: 0.22, ease: "power2.in", immediateRender: false }}, C.__dur - 0.22);') if blur else ""
    if wipe_in:
        js = f'      tl.fromTo("#{sid}-stage .wp", {{ xPercent: 0 }}, {{ xPercent: -110, duration: 0.32, ease: "power2.out" }}, 0);\n' + js
    else:
        js = f'      tl.set("#{sid}-stage .wp", {{ xPercent: 110 }}, 0);\n' + js
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

SLOT_CSS = """.slot { position: absolute; left: 110px; width: 720px; height: 300px; border-radius: 30px; background: #fff; overflow: hidden; opacity: 0;
      box-shadow: 0 0 0 7px var(--c), 0 0 40px var(--c); }
    .slot .col { position: absolute; left: 0; right: 0; top: 0; }
    .slot .col div { height: 100px; display: grid; place-items: center; font: 900 46px Inter, sans-serif; color: #1a0f08; white-space: nowrap; }
    .slot .col .win { color: #ff3dbd; font-size: 54px; }
    .slot .band { position: absolute; left: 10px; right: 10px; top: 100px; height: 100px; border-radius: 20px; border: 5px solid var(--c); background: rgba(255,255,255,.0); }
    .slot .fd { position: absolute; left: 0; right: 0; top: 0; bottom: 0; background: linear-gradient(#fff 0%, rgba(255,255,255,0) 32%, rgba(255,255,255,0) 68%, #fff 100%); }
    .slot .pt2 { position: absolute; top: 128px; font-size: 44px; } 
    .slk { position: absolute; left: 110px; width: 720px; text-align: center; font: 900 34px Inter, sans-serif; letter-spacing: .12em; color: #fff; opacity: 0;
      -webkit-text-stroke: 8px #0a0418; paint-order: stroke fill; }"""
def slot(sid, names, win, top, col, label):
    rows = names + [win, names[0]]
    return (f'<div class="slk" id="{sid}k" style="top:{top-52}px">{label}</div><div class="slot" id="{sid}" style="top:{top}px;--c:{col}">'
            f'<div class="col" id="{sid}c">' + "".join(f'<div{" class=win" if i == len(names) else ""} id="{sid}r{i}">{n}</div>' for i, n in enumerate(rows))
            + f'</div><div class="fd"></div><div class="band"></div><div class="pt2" style="left:24px">▶</div><div class="pt2" style="right:24px">◀</div></div>')
def slotjs(sid, n, t0, tw):
    # Rad läuft (erste Zeile in der Mitte) und bremst genau auf dem Gewinner ab (Zeile n in der Mitte)
    return (f'tl.fromTo(["#{sid}", "#{sid}k"], {{ opacity: 0, scale: .5 }}, {{ opacity: 1, scale: 1, duration: .25, ease: "back.out(2.5)" }}, {t0} - .3);\n'
            f'      tl.fromTo("#{sid}c", {{ y: 100 }}, {{ y: 100 - {n} * 100, duration: {tw} - ({t0}), ease: "sine.out" }}, {t0});\n'
            f'      tl.fromTo("#{sid}c", {{ filter: "blur(3px)" }}, {{ filter: "blur(0px)", duration: ({tw} - ({t0})) * .8, ease: "power2.in", immediateRender: false }}, {t0});\n'
            f'      tl.fromTo("#{sid}r{n}", {{ scale: 1 }}, {{ scale: 1.15, duration: .15, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {tw});')


GULL_CSS = """#gl { position: absolute; left: 0; top: 0; width: 780px; height: 450px; opacity: 0; }
    #gl .gf { position: absolute; inset: 0; width: 780px; height: 450px; opacity: 0; }"""
def gulljs(t0, dur, y0, y1):
    return (f'tl.set("#gl", {{ opacity: 1 }}, {t0}); tl.fromTo("#gl", {{ x: -800, y: {y0} }}, {{ x: 1140, y: {y1}, duration: {dur}, ease: "none" }}, {t0}); tl.set("#gl", {{ opacity: 0 }}, {t0} + {dur});\n'
            f'      for (let k = 0; k < Math.ceil({dur} / .06); k++) {{ const i = k % 8, a = {t0} + k * .06; tl.set("#gf" + i, {{ opacity: 1 }}, a); tl.set("#gf" + i, {{ opacity: 0 }}, a + .06); }}')


# s01 – Hook: Neu in Muschel-Tal: das Sunken Pearl (Wortzeiten gemessen) + Sonnenuntergang
scene("s01", NEO + """
    #hk { position: absolute; left: 60px; right: 60px; top: 250px; text-align: center; font-family: "Lilita One", sans-serif; line-height: 1.04; -webkit-text-stroke: 18px #0a0418; paint-order: stroke fill; }
    #hk .w { display: inline-block; position: relative; color: #fff; font-size: 128px; margin: 0 .06em; transform-origin: 50% 60%; }
    #hk #w0 { color: #ffd23f; } #hk #w2 { color: #ffb38a; font-size: 120px; } #hk #w4 { color: #3ff0ff; } #hk #w5 { color: #ff3dbd; }
    #hk #w0 { transform-origin: 15% 60%; } #hk #w1 { transform-origin: 85% 60%; }
    .rg { position: absolute; left: 540px; top: 0; width: 300px; height: 300px; margin: -150px; border-radius: 50%; border: 18px solid #ffd23f; box-shadow: 0 0 50px #ffd23f; opacity: 0; }
    #b1 { top: 1450px; font-size: 52px; } #b2 { top: 1600px; font-size: 52px; }""",
"""      <div id="hk"><span class="w" id="w0">NEU</span><span class="w" id="w1">IN</span><br><span class="w" id="w2">MUSCHEL-TAL:</span><br><span class="w" id="w3">DAS</span><span class="w" id="w4">SUNKEN</span><br><span class="w" id="w5">PEARL!</span></div>
      <div class="rg" id="rg0"></div><div class="rg" id="rg1"></div>
      <div id="b1" class="neo pk">🏙️ EIN WOLKENKRATZER INS MEER</div>
      <div id="b2" class="neo go">🌅 IM SONNENUNTERGANG</div>
      <div class="fl"></div>""",
"""      const ws = [["neu",.04,.20],["in",.22,.43],["muscheltal",.50,1.29],["das",1.54,1.82],["sunken",1.84,2.19],["pearl",2.24,2.58]] /* aus narration.wav gemessen */, SC = [1.9, 1.9, 1.12, 1.7, 1.45, 1.6];
      tl.fromTo("#hk", { scale: 1.2 }, { scale: 1, duration: .18, ease: "power3.out" }, 0);
      """ + FLASH(0, .9) + """
      ws.forEach((w, i) => { const id = "#w" + i, t0 = Math.max(0, w[1] - .03), col = getComputedStyle(document.querySelector(id)).color;
        tl.set(id, { zIndex: 5 }, t0);
        tl.fromTo(id, { scale: 1, textShadow: "0 0 0px #fff" }, { scale: SC[i], textShadow: "0 0 50px #ffd23f, 0 0 120px #ff3dbd", duration: .07, ease: "power4.out", immediateRender: false }, t0);
        tl.to(id, { scale: 1, textShadow: "0 0 0px #fff", duration: .2, ease: "back.out(2)" }, Math.max(t0 + .1, w[2] - .08));
        tl.set(id, { zIndex: 1 }, w[2] + .15);
        tl.fromTo(".fl", { opacity: .3 }, { opacity: 0, duration: .12, immediateRender: false }, t0);
        [[10,-6],[-12,6],[0,0]].forEach(([x, y], n) => tl.to("#s01-stage", { x, y, duration: .03, ease: "none" }, t0 + n * .03)); });
      [[1.84, 560, 0], [2.24, 690, 1]].forEach(([t, y, k]) => { tl.fromTo("#rg" + k, { opacity: 1, scale: .2, y }, { opacity: 0, scale: 3, duration: .6, ease: "power2.out", immediateRender: false }, t);
        [[26,-16],[-28,14],[18,16],[0,0]].forEach(([x, yy], n) => tl.to("#s01-stage", { x, y: yy, duration: .04, ease: "none" }, t + n * .04)); });
      const B = line("L1b")[0];
      tl.to("#hk", { scale: .78, y: -150, duration: .35, ease: "power2.inOut" }, B - .1);
      """ + Z("#b1", 'at("L1b", "Wolkenkratzer") - .05') + """
      """ + Z("#b2", 'at("L1b", "Sonnenuntergang") - .05') + FLASH('at("L1b", "Sonnenuntergang")', .4), wipe_in=False)

# s02 – Fähre Seestern fährt los (Kamera folgt) + Muschel-Möwe
scene("s02", NEO + GULL_CSS + """
    #f1 { top: 230px; font-size: 100px; white-space: nowrap; }
    #f2 { top: 390px; font-size: 72px; }""",
"""      <div id="f1" class="big">⛴️ FÄHRE <span class="c">SEESTERN</span></div>
      <div id="f2" class="neo go">🐚 ⇄ 🥥 ⇄ 🫧</div>
      <div id="gl"><img class="gf" id="gf0" src="bilder/moewe/m0.png"><img class="gf" id="gf1" src="bilder/moewe/m1.png"><img class="gf" id="gf2" src="bilder/moewe/m2.png"><img class="gf" id="gf3" src="bilder/moewe/m3.png"><img class="gf" id="gf4" src="bilder/moewe/m4.png"><img class="gf" id="gf5" src="bilder/moewe/m5.png"><img class="gf" id="gf6" src="bilder/moewe/m6.png"><img class="gf" id="gf7" src="bilder/moewe/m7.png"></div>""",
"""      const t = line("L2")[0];
      """ + Z("#f1", 'at("L2", "Fähre") - .05') + """
      """ + Z("#f2", 'at("L2", "zwischen") - .05') + """
      tl.to("#f2", { scale: 1.08, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L2", "zwischen") + .3);
      """ + gulljs("t + .2", 2.6, 560, 470))

# s03 – Freunde einladen = Nachbarn
scene("s03", NEO + """
    #n1 { top: 220px; font-size: 92px; white-space: nowrap; }
    #nb { position: absolute; left: 110px; width: 720px; top: 420px; height: 300px; opacity: 0; }
    .hu { position: absolute; top: 0; width: 280px; text-align: center; }
    .hu b { display: block; font-size: 170px; line-height: 1; }
    .hu i { display: inline-block; margin-top: 8px; padding: 6px 18px 10px; border-radius: 18px; background: #fff; color: #1a0f08; font: 900 30px Inter, sans-serif; font-style: normal; box-shadow: 0 0 0 5px var(--c); }
    #hz { position: absolute; left: 300px; top: 40px; width: 120px; text-align: center; font-size: 110px; }""",
"""      <div id="n1" class="big">👯 <span class="l">LAD FREUNDE EIN</span></div>
      <div id="nb"><div class="hu" style="left:0;--c:#3ff0ff"><b>🛖</b><i>DU</i></div><div id="hz">💞</div><div class="hu" style="left:440px;--c:#ff3dbd"><b>🛖</b><i>DEIN FREUND</i></div></div>""",
"""      const t = line("L3")[0], NB = at("L3", "Nachbarn");
      """ + Z("#n1", "t - .05") + """
      tl.fromTo("#nb", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, t + .3);
      tl.fromTo("#hz", { scale: .3 }, { scale: 1.3, duration: .25, ease: "back.out(3)", yoyo: true, repeat: 3 }, NB - .05);
      """ + SHAKE("s03", "NB"))

# s04 – Das Spiel beginnt bald + Folgen
scene("s04", NEO + FOLLOW + """
    #s1 { top: 250px; font-size: 120px; }
    #fb { top: 560px; opacity: 0; }""",
"""      <div id="s1" class="big">🎮 BALD<br><span class="g">GEHT'S LOS!</span></div>
      <div id="fb" class="fbtn">+ Folgen<div class="fbtn2">✓ Eingezogen</div></div>
      <div class="fl"></div>""",
"""      const t = line("L4")[0];
      """ + Z("#s1", 'at("L4", "Spiel") - .05') + FLASH('at("L4", "Spiel")', .6) + SHAKE("s04", 'at("L4", "Spiel")') + """
      tl.to("#s1", { scale: 1.07, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L4", "bald") + .2);
      """ + Z("#fb", 'at("L4", "bald") + .3') + """
      tl.to("#fb .fbtn2", { opacity: 1, duration: .15 }, at("L4", "bald") + 1.3);""", blur=False)
