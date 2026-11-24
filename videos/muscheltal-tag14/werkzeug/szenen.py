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

# s01 – Hook: Stell dir einen Wolkenkratzer vor … in den Ozean statt in die Wolken → Meeresgrund (Wortzeiten gemessen)
scene("s01", NEO + """
    #dw { position: absolute; left: 0; top: 320px; width: 1080px; height: 3800px; } #sky { position: absolute; left: 0; top: 0; width: 1080px; height: 330px; background: #bdefff; }
    #hk { position: absolute; left: 60px; right: 60px; top: 470px; text-align: center; font-family: "Lilita One", sans-serif; line-height: 1.02; -webkit-text-stroke: 18px #0a0418; paint-order: stroke fill; }
    #hk .w { display: inline-block; position: relative; color: #fff; font-size: 96px; margin: 0 .06em; transform-origin: 50% 60%; }
    #hk #w3 { color: #ffd23f; font-size: 104px; } #hk #w10 { color: #3ff0ff; } #hk #w14 { color: #b6ff3b; } #hk #w0, #hk #w5, #hk #w8, #hk #w11 { transform-origin: 12% 60%; } #hk #w2, #hk #w7, #hk #w10, #hk #w14 { transform-origin: 88% 60%; }
    .rg { position: absolute; left: 540px; width: 300px; height: 300px; margin: -150px; border-radius: 50%; border: 18px solid #3ff0ff; box-shadow: 0 0 50px #3ff0ff; opacity: 0; }
    .sp { position: absolute; font-size: 80px; opacity: 0; } #wow { position: absolute; left: 780px; top: 1100px; font-size: 170px; opacity: 0; }
    .cl { position: absolute; font-size: 200px; opacity: .95; } .cx { position: absolute; font-size: 170px; opacity: 0; }
    #ar { position: absolute; left: 860px; top: 1280px; font-size: 130px; opacity: 0; }
    #s2 { top: 1450px; font-size: 56px; }
    #s1 { top: 230px; font-size: 104px; white-space: nowrap; }
    #mg { position: absolute; left: 0; right: 0; top: 1300px; text-align: center; font: 400 64px "Lilita One", sans-serif; color: #fff; opacity: 0; -webkit-text-stroke: 10px #0a0418; paint-order: stroke fill; }""",
"""      <div id="sky"></div><div id="dw"><svg id="dv" viewBox="0 0 1080 3800" width="1080" height="3800"><defs><linearGradient id="wg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bdefff"/><stop offset=".26" stop-color="#7fd8ff"/><stop offset=".3" stop-color="#2fb7e8"/><stop offset=".6" stop-color="#0a5a92"/><stop offset=".92" stop-color="#04122a"/><stop offset="1" stop-color="#04122a"/></linearGradient></defs><rect width="1080" height="3800" fill="url(#wg)"/><path d="M0 1120 Q135 1095 270 1120 T540 1120 T810 1120 T1080 1120 L1080 1150 L0 1150Z" fill="#fff" opacity=".7"/><rect x="390" y="1150" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="1180" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.95"/><rect x="480" y="1180" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.95"/><rect x="550" y="1180" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.95"/><rect x="620" y="1180" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.95"/><rect x="390" y="1290" width="300" height="140" fill="#f6c3b0" stroke="#c9826a" stroke-width="4"/><rect x="410" y="1320" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.92"/><rect x="480" y="1320" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.92"/><rect x="550" y="1320" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.92"/><rect x="620" y="1320" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.92"/><rect x="390" y="1430" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="1460" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.89"/><rect x="480" y="1460" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.89"/><rect x="550" y="1460" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.89"/><rect x="620" y="1460" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.89"/><rect x="390" y="1570" width="300" height="140" fill="#f6c3b0" stroke="#c9826a" stroke-width="4"/><rect x="410" y="1600" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.86"/><rect x="480" y="1600" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.86"/><rect x="550" y="1600" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.86"/><rect x="620" y="1600" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.86"/><rect x="390" y="1710" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="1740" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.83"/><rect x="480" y="1740" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.83"/><rect x="550" y="1740" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.83"/><rect x="620" y="1740" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.83"/><rect x="390" y="1850" width="300" height="140" fill="#f6c3b0" stroke="#c9826a" stroke-width="4"/><rect x="410" y="1880" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.80"/><rect x="480" y="1880" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.80"/><rect x="550" y="1880" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.80"/><rect x="620" y="1880" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.80"/><rect x="390" y="1990" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="2020" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.77"/><rect x="480" y="2020" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.77"/><rect x="550" y="2020" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.77"/><rect x="620" y="2020" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.77"/><rect x="390" y="2130" width="300" height="140" fill="#f6c3b0" stroke="#c9826a" stroke-width="4"/><rect x="410" y="2160" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.74"/><rect x="480" y="2160" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.74"/><rect x="550" y="2160" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.74"/><rect x="620" y="2160" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.74"/><rect x="390" y="2270" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="2300" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.71"/><rect x="480" y="2300" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.71"/><rect x="550" y="2300" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.71"/><rect x="620" y="2300" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.71"/><rect x="390" y="2410" width="300" height="140" fill="#f6c3b0" stroke="#c9826a" stroke-width="4"/><rect x="410" y="2440" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.68"/><rect x="480" y="2440" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.68"/><rect x="550" y="2440" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.68"/><rect x="620" y="2440" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.68"/><rect x="390" y="2550" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="2580" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.65"/><rect x="480" y="2580" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.65"/><rect x="550" y="2580" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.65"/><rect x="620" y="2580" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.65"/><rect x="390" y="2690" width="300" height="140" fill="#f6c3b0" stroke="#c9826a" stroke-width="4"/><rect x="410" y="2720" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.62"/><rect x="480" y="2720" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.62"/><rect x="550" y="2720" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.62"/><rect x="620" y="2720" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.62"/><rect x="390" y="2830" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="2860" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.59"/><rect x="480" y="2860" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.59"/><rect x="550" y="2860" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.59"/><rect x="620" y="2860" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.59"/><rect x="390" y="2970" width="300" height="140" fill="#f6c3b0" stroke="#c9826a" stroke-width="4"/><rect x="410" y="3000" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.56"/><rect x="480" y="3000" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.56"/><rect x="550" y="3000" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.56"/><rect x="620" y="3000" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.56"/><rect x="390" y="3110" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="3140" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.53"/><rect x="480" y="3140" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.53"/><rect x="550" y="3140" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.53"/><rect x="620" y="3140" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.53"/><rect x="390" y="3250" width="300" height="140" fill="#f6c3b0" stroke="#c9826a" stroke-width="4"/><rect x="410" y="3280" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.50"/><rect x="480" y="3280" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.50"/><rect x="550" y="3280" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.50"/><rect x="620" y="3280" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.50"/><rect x="390" y="3390" width="300" height="140" fill="#f0b39e" stroke="#c9826a" stroke-width="4"/><rect x="410" y="3420" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.47"/><rect x="480" y="3420" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.47"/><rect x="550" y="3420" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.47"/><rect x="620" y="3420" width="48" height="70" rx="20" fill="#ffe9a0" opacity="0.47"/><rect x="330" y="980" width="420" height="170" rx="10" fill="#f4b9a4" stroke="#c9826a" stroke-width="6"/><path d="M380 980 Q540 800 700 980Z" fill="#e8846a" stroke="#c9826a" stroke-width="6"/><circle cx="540" cy="830" r="34" fill="#fff"/><rect x="470" y="1040" width="140" height="110" rx="60" fill="#8a5a2b"/><text x="150" y="1300" font-size="70" opacity=".9">🐡</text><text x="860" y="1450" font-size="80" opacity=".9">🪼</text><text x="120" y="1600" font-size="70" opacity=".9">🐠</text><text x="860" y="1750" font-size="60" opacity=".9">🐠</text><text x="120" y="1900" font-size="70" opacity=".9">🦑</text><text x="200" y="2050" font-size="70" opacity=".9">🪼</text><text x="120" y="2200" font-size="80" opacity=".9">🐠</text><text x="120" y="2350" font-size="80" opacity=".9">🐠</text><text x="880" y="2500" font-size="70" opacity=".9">🐠</text><text x="880" y="2650" font-size="60" opacity=".9">🐟</text><text x="200" y="2800" font-size="80" opacity=".9">🪼</text><text x="880" y="2950" font-size="60" opacity=".9">🐠</text><text x="120" y="3100" font-size="60" opacity=".9">🐠</text><text x="200" y="3250" font-size="60" opacity=".9">🐠</text><path d="M0 3560 Q200 3500 400 3550 T800 3540 T1080 3560 L1080 3800 L0 3800Z" fill="#e8c98a"/><path d="M150 3560 q-20 -120 10 -200 M180 3560 q30 -100 0 -170 M900 3560 q-25 -140 15 -230 M930 3560 q30 -110 -5 -190" stroke="#2fae6a" stroke-width="14" fill="none" stroke-linecap="round"/><text x="230" y="3640" font-size="90">🪸</text><text x="760" y="3650" font-size="90">🪸</text><text x="600" y="3700" font-size="70">⭐</text><text x="320" y="3720" font-size="60">🐚</text><rect x="390" y="3530" width="300" height="40" fill="#c9826a"/></svg></div>
      <div id="hk"><span class="w" id="w0">STELL</span><span class="w" id="w1">DIR</span><span class="w" id="w2">EINEN</span><br><span class="w" id="w3">WOLKENKRATZER</span><span class="w" id="w4">VOR …</span><br><span class="w" id="w5">ABER</span><span class="w" id="w6">ER</span><span class="w" id="w7">GEHT</span><br><span class="w" id="w8">IN</span><span class="w" id="w9">DEN</span><span class="w" id="w10">OZEAN –</span><br><span class="w" id="w11">STATT</span><span class="w" id="w12">IN</span><span class="w" id="w13">DIE</span><span class="w" id="w14">WOLKEN!</span></div>
      <div class="rg" id="rg0"></div><div class="rg" id="rg1"></div><div class="rg" id="rg2"></div><div class="sp" id="sk0" style="left:500px;top:400px">✨</div><div class="sp" id="sk1" style="left:500px;top:400px">⭐</div><div class="sp" id="sk2" style="left:500px;top:400px">💥</div><div class="sp" id="sk3" style="left:500px;top:400px">✨</div><div class="sp" id="sk4" style="left:500px;top:400px">⭐</div><div class="sp" id="sk5" style="left:500px;top:400px">💥</div><div class="sp" id="sk6" style="left:500px;top:400px">✨</div><div class="sp" id="sk7" style="left:500px;top:400px">⭐</div><div id="wow">🤯</div><div class="cl" id="cl0" style="left:90px;top:230px">☁️</div><div class="cl" id="cl1" style="left:730px;top:190px">☁️</div><div class="cx" id="cx0" style="left:110px;top:230px">❌</div><div class="cx" id="cx1" style="left:750px;top:190px">❌</div>
      <div id="ar">⬇️</div>
      <div id="s2" class="neo pk">🌊 BIS AUF DEN MEERESGRUND!</div>
      <div id="s1" class="big">🫧 <span class="c">SUNKEN</span> <span class="g">PEARL</span></div>
      <div class="fl"></div>""",
"""      const ws = [["stell",.02,.16],["dir",.18,.37],["einen",.40,.55],["wolkenkratzer",.62,1.25],["vor",1.28,1.42],["aber",1.70,1.85],["er",2.04,2.12],["geht",2.14,2.25],["in",2.38,2.47],["den",2.52,2.63],["ozean",2.66,2.97],["statt",3.12,3.31],["in",3.38,3.62],["die",3.64,3.89],["wolken",3.92,4.45]] /* aus narration.wav gemessen (normale Stimme) */,
        SC = [1.6, 1.7, 1.5, 1.08, 1.6, 1.6, 1.8, 1.6, 1.8, 1.7, 1.35, 1.3, 1.8, 1.7, 1.12], COL = ws.map((w, i) => i === 3 ? "#ffd23f" : i === 10 ? "#3ff0ff" : i === 14 ? "#b6ff3b" : "#ffffff");
      tl.fromTo("#hk", { scale: 1.2 }, { scale: 1, duration: .18, ease: "power3.out" }, 0);
      """ + FLASH(0, .9) + """
      ws.forEach((w, i) => { const id = "#w" + i, t0 = Math.max(0, w[1] - .03);
        tl.set(id, { zIndex: 5 }, t0);
        tl.fromTo(id, { scale: 1, color: COL[i], textShadow: "0 0 0px #fff" }, { scale: SC[i], color: COL[i] === "#ffffff" ? "#ffd23f" : "#ffffff", textShadow: "0 0 50px #3ff0ff, 0 0 120px #3ff0ff", duration: .07, ease: "power4.out", immediateRender: false }, t0);
        tl.to(id, { scale: 1, color: COL[i], textShadow: "0 0 0px #fff", duration: .2, ease: "back.out(2)" }, Math.max(t0 + .1, w[2] - .08));
        tl.set(id, { zIndex: 1 }, w[2] + .15);
        tl.fromTo(".fl", { opacity: .3 }, { opacity: 0, duration: .12, immediateRender: false }, t0);
        [[10,-6],[-12,6],[0,0]].forEach(([x, y], n) => tl.to("#s01-stage", { x, y, duration: .03, ease: "none" }, t0 + n * .03)); });
      const BOOM = (t, y, col, k) => {
        tl.fromTo("#rg" + k, { opacity: 1, scale: .2, y, borderColor: col }, { opacity: 0, scale: 3.2, duration: .6, ease: "power2.out", immediateRender: false }, t);
        for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2 + k; tl.fromTo("#sk" + i, { opacity: 1, x: 0, y: y - 400 + 340, scale: .5 }, { opacity: 0, x: Math.cos(a) * 420, y: y - 60 + Math.sin(a) * 300, scale: 1.4, duration: .7, ease: "power2.out", immediateRender: false }, t); }
        [[30,-18],[-34,16],[26,20],[-20,-14],[0,0]].forEach(([x, yy], n) => tl.to("#s01-stage", { x, y: yy, duration: .04, ease: "none" }, t + n * .04));
        tl.fromTo(".fl", { opacity: .45 }, { opacity: 0, duration: .25, immediateRender: false }, t); };
      BOOM(.6, 610, "#ffd23f", 0); BOOM(2.64, 830, "#3ff0ff", 1); BOOM(3.9, 930, "#b6ff3b", 2);
      tl.fromTo("#wow", { opacity: 0, scale: .2, rotation: -30 }, { opacity: 1, scale: 1, rotation: 8, duration: .3, ease: "back.out(3)" }, 2.66);
      tl.to("#wow", { opacity: 0, scale: .6, duration: .25 }, 3.4);
      tl.to("#hk", { scale: 1.04, duration: .7, yoyo: true, repeat: 3, ease: "sine.inOut" }, 1.3);
      const B = line("L1b")[0], E = C.__dur;
      tl.fromTo("#ar", { opacity: 0, y: -40 }, { opacity: 1, y: 60, duration: .35, yoyo: true, repeat: 5, ease: "sine.inOut" }, 2.66);
      [0, 1].forEach(i => tl.fromTo("#cx" + i, { opacity: 0, scale: 3, rotation: -20 }, { opacity: 1, scale: 1, rotation: 0, duration: .22, ease: "back.out(3)" }, 3.9 + i * .12));
      tl.to([".cl", ".cx"], { y: -500, opacity: 0, duration: .7, ease: "power2.in" }, 4.5);
      tl.fromTo("#dw", { y: 0 }, { y: -2200, duration: B + 1.5 - 4.45, ease: "power2.inOut" }, 4.45);
      tl.to("#sky", { y: -400, duration: .6, ease: "power2.in" }, 4.45);
      tl.to("#hk", { opacity: 0, y: -100, duration: .25 }, B - .25);
      """ + Z("#s2", "B - .05") + """
      tl.fromTo("#dw", { opacity: 1 }, { opacity: 0, duration: .45, immediateRender: false }, at("L1b", "Sunken") - .2);
      tl.to("#s2", { opacity: 0, duration: .2 }, at("L1b", "Sunken") - .1);
      """ + Z("#s1", 'at("L1b", "Sunken") - .05') + SHAKE("s01", 'at("L1b", "Sunken")') + FLASH('at("L1b", "Sunken")', .8), wipe_in=False)

# s02 – Innenansicht Tiefsee-Suite: unter Wasser wohnen + Frage
scene("s02", NEO + """
    #i1 { top: 210px; font-size: 68px; white-space: nowrap; }
    #iv { position: absolute; left: 220px; top: 360px; width: 640px; height: 713px; border-radius: 40px; overflow: hidden; opacity: 0;
      box-shadow: 0 0 0 8px #3ff0ff, 0 0 50px rgba(63,240,255,.8); background: url(bilder/innen.png) center / 100% 100% no-repeat; }
    #i3 { top: 1540px; font-size: 60px; }""",
"""      <div id="i1" class="big">🫧 <span class="c">UNTER WASSER</span> WOHNEN</div>
      <div id="iv"></div>
      <div id="i3" class="neo pk">🤔 WÜRDEST DU HIER WOHNEN WOLLEN?</div>
      <div class="fl"></div>""",
"""      const t = line("L2")[0], Q = line("L2b")[0];
      """ + Z("#i1", "t - .05") + """
      tl.fromTo("#iv", { opacity: 0, scale: .4, rotation: -6 }, { opacity: 1, scale: 1, rotation: 0, duration: .4, ease: "back.out(1.8)" }, t + .1);
      tl.fromTo("#iv", { backgroundSize: "100% 100%" }, { backgroundSize: "114% 114%", duration: 3, ease: "none", immediateRender: false }, t + .5);
      """ + Z("#i3", "Q - .05") + FLASH("Q", .5) + """
      tl.to("#i3", { scale: 1.07, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut" }, Q + .4);""")

# s03 – Ergebnis der Abstimmung (Screenshot ohne Profilbild)
scene("s03", NEO + """
    #r1 { top: 220px; font-size: 110px; white-space: nowrap; }
    #pi { position: absolute; left: 60px; top: 420px; width: 830px; height: 347px; border-radius: 28px; opacity: 0; background: url(bilder/abstimmung.png) center/cover;
      box-shadow: 0 0 0 6px #ffd23f, 0 20px 50px rgba(0,0,0,.5); }
    #r3 { top: 830px; font-size: 70px; }""",
"""      <div id="r1" class="big">🗳️ <span class="g">EURE WAHL</span></div>
      <div id="pi"></div>
      <div id="r3" class="neo pk">🐱 KATZENCAFÉ GEWINNT!</div>
      <div class="fl"></div>""",
"""      const t = line("L3")[0], K = at("L3", "Katzencafé");
      """ + Z("#r1", "t - .05") + """
      tl.fromTo("#pi", { opacity: 0, y: 80, scale: .8 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2)" }, t + .2);
      tl.to("#pi", { scale: 1.04, duration: .15, yoyo: true, repeat: 1 }, at("L3", "78"));
      """ + Z("#r3", "K - .05") + SHAKE("s03", "K") + FLASH("K", .6))

# s04 – Café Miau fertig, Team Lilly, Insa, Lilly
scene("s04", NEO + """
    #c1 { top: 220px; font-size: 110px; white-space: nowrap; }
    #c2 { top: 370px; font-size: 56px; }
    .nm { position: absolute; top: 1570px; width: 262px; padding: 14px 6px 16px; border-radius: 24px; background: #fff; color: #1a0f08; text-align: center; opacity: 0;
      font: 900 26px Inter, sans-serif; box-shadow: 0 0 0 6px #ff3dbd, 0 10px 0 rgba(0,0,0,.3); }
    .nm b { display: block; font: 400 46px/1 "Lilita One", sans-serif; color: #ff3dbd; margin-bottom: 4px; }""",
"""      <div id="c1" class="big">🐱 <span class="p">CAFÉ MIAU</span></div>
      <div id="c2" class="neo li">✅ FERTIG GEBAUT!</div>
      <div id="n0" class="nm" style="left:60px"><b>LILLY ⭐</b>@lillyf.r1</div>
      <div id="n1" class="nm" style="left:344px"><b>INSA</b>@insa.t_sp</div>
      <div id="n2" class="nm" style="left:628px"><b>LILLY</b>@lillyyyy7597</div>
      <div class="fl"></div>""",
"""      const t = line("L4")[0], LW = C["L4.words"].filter(w => w[0].startsWith("lilly")), IN = at("L4", "Insa");
      """ + Z("#c1", "t - .05") + """
      """ + Z("#c2", 'at("L4", "fertig") - .05') + FLASH('at("L4", "fertig")', .5) + """
      [[0, LW[0][1]], [1, IN], [2, (LW[1] || LW[0])[1]]].forEach(([i, a]) => tl.fromTo("#n" + i, { opacity: 0, scale: .2, rotation: i % 2 ? 10 : -10 }, { opacity: 1, scale: 1, rotation: 0, duration: .28, ease: "back.out(2.6)" }, a - .08));""")

# s05 – Fähre Seestern: zwischen den Inseln, ganze Inselwelt erkunden
scene("s05", NEO + GULL_CSS + """
    #f1 { top: 220px; font-size: 96px; white-space: nowrap; }
    #f2 { top: 380px; font-size: 72px; }
    #f3 { top: 1580px; font-size: 50px; }""",
"""      <div id="f1" class="big">⛴️ FÄHRE <span class="c">SEESTERN</span></div>
      <div id="f2" class="neo go">🐚 ⇄ 🥥 ⇄ 🫧</div>
      <div id="gl"><img class="gf" id="gf0" src="bilder/moewe/m0.png"><img class="gf" id="gf1" src="bilder/moewe/m1.png"><img class="gf" id="gf2" src="bilder/moewe/m2.png"><img class="gf" id="gf3" src="bilder/moewe/m3.png"><img class="gf" id="gf4" src="bilder/moewe/m4.png"><img class="gf" id="gf5" src="bilder/moewe/m5.png"><img class="gf" id="gf6" src="bilder/moewe/m6.png"><img class="gf" id="gf7" src="bilder/moewe/m7.png"></div>
""",
"""      const t = line("L5")[0];
      """ + Z("#f1", 'at("L5", "Fähre") - .05') + """
      """ + Z("#f2", 'at("L5", "zwischen") - .05') + """
      """ + gulljs('at("L5", "Fähre")', 3.2, 620, 520) + """
      tl.to("#f2", { scale: 1.08, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L5", "zwischen") + .3);""")

# s06 – Verlosung: Job bei CocoCare (Glücksrad, Python secrets)
scene("s06", NEO + SLOT_CSS + CF_CSS + """
    #j1 { top: 220px; font-size: 100px; white-space: nowrap; }
    #j2 { top: 380px; font-size: 56px; }
    #j3 { top: 960px; font-size: 76px; }
    #j4 { top: 1570px; font-size: 52px; }""",
"""      <div id="j1" class="big">🎰 <span class="g">VERLOSUNG!</span></div>
      <div id="j2" class="neo li"><small>🌸 1 JOB BEI</small>COCOCARE</div>
      """ + slot("sg", ["@leeland205", "@louisa_sel", "@mia_v005", "@zuza_.2281", "@mia2201e0", "@tinaa.793", "@litreally_nightwing", "@_ph1l0.s0ph14_", "@burgerpuffel", "@jxst_lea.tiktok", "@just_fabs_", "@minuscha99", "@alex.erklaert", "@sophieee_nrb", "@tamiajustine5", "@lea.02082009"], "@keineahnung1.7", 620, "#5fc8a8", "") + """
      <div id="j3" class="neo li">🎉 GLÜCKWUNSCH!</div>
      <div id="cfb" style="position:absolute;inset:0"></div>
      <div class="fl"></div>""",
"""      const t = line("L6")[0], G = at("L6", "CocoCare"), W = line("L6b")[0];
      """ + Z("#j1", 'at("L6", "Job") - .05') + FLASH('at("L6", "Job")', .5) + """
      """ + Z("#j2", 'at("L6", "Job") - .05') + """
      """ + slotjs("sg", 16, "G + .3", "W") + """
      """ + SHAKE("s06", "W") + FLASH("W", .8) + """
      """ + Z("#j3", "W") + """
      { """ + CONF_JS.replace("BOX", "cfb").replace("SEED", "77").replace("T0", "W") + """ }"""
      )

# s07 – Security fürs Golden Pearl gesucht
scene("s07", NEO + """
    #g1 { top: 220px; font-size: 120px; white-space: nowrap; }
    #g2 { top: 360px; font-size: 92px; }
    #g3 { top: 560px; font-size: 56px; }
    #g4 { top: 1590px; font-size: 44px; }""",
"""      <div id="g1" class="big">🕶️ <span class="g">SECURITY</span></div>
      <div id="g2" class="big"><span class="p">GESUCHT!</span></div>
      <div id="g3" class="neo go">✨ FÜRS GOLDEN PEARL</div>
      <div class="fl"></div>""",
"""      const t = line("L7")[0], SE = at("L7", "Security");
      """ + Z("#g3", 'at("L7", "Golden") - .05') + """
      """ + Z("#g1", "SE - .05") + Z("#g2", "SE + .15") + SHAKE("s07", "SE") + FLASH("SE", .6) + """
      tl.to("#g3", { scale: 1.06, duration: .22, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L7", "Bewerbt"));""")

# s08 – 819 / 1.000, Spielstart, Folgen ganz am Ende
scene("s08", NEO + FOLLOW + """
    #r7 { top: 240px; font-size: 60px; }
    #br { position: absolute; left: 80px; right: 210px; top: 480px; padding: 20px; border-radius: 30px; background: rgba(10,4,24,.96); opacity: 0; }
    #br .tr { height: 80px; border-radius: 40px; background: rgba(10,4,24,.85); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.6); overflow: hidden; }
    #br .fi { height: 100%; width: 0; background: linear-gradient(90deg, #3ff0ff, #ff3dbd); }
    #br .lb { display: flex; justify-content: space-between; margin-top: 14px; font: 400 60px "Lilita One", sans-serif; color: #fff; }
    #br .lb span:last-child { color: #b6ff3b; }
    #o9 { top: 260px; font-size: 150px; }
    #f9 { top: 480px; opacity: 0; }""",
"""      <div id="r7" class="neo li"><small>🎮 BEI 1.000 BEWOHNERN</small>STARTET DAS SPIEL!</div>
      <div id="br"><div class="tr"><div class="fi"></div></div><div class="lb"><span id="cn">0</span><span>1.000</span></div></div>
      <div id="o9" class="big">FOLG <span class="p">MIR</span></div>
      <div id="f9" class="fbtn">+ Folgen<div class="fbtn2">✓ Eingezogen</div></div>
      <div class="fl"></div>""",
"""      const t = at("L8", "819"), F = line("L8b")[0];
      tl.fromTo("#br", { opacity: 0 }, { opacity: 1, duration: .25 }, t - .05);
      tl.fromTo("#br .fi", { width: "0%" }, { width: "81.9%", duration: 1.3, ease: "power2.out" }, t);
      count(tl, "#cn", 0, 819, t, 1.3);
      """ + Z("#r7", 'at("L8", "1.000") - .05') + """
      """ + OUT("#r7", "F - .15") + OUT("#br", "F - .15") + """
      """ + Z("#o9", "F - .05") + FLASH("F", .5) + SHAKE("s08", "F") + """
      """ + Z("#f9", "F + .2") + """
      tl.to("#f9 .fbtn2", { opacity: 1, duration: .15 }, at("L8b", "zieh") + .2);
      tl.to("#f9", { scale: 1.12, duration: .15, yoyo: true, repeat: 1 }, at("L8b", "zieh") + .2);""", blur=False)
