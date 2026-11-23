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

# s01 – Sonniger Strand mit Riesen-Muschel → POOF → alles grau
scene("s01", """
    .neo { position: absolute; left: 60px; right: 190px; margin: 0 auto; width: fit-content; max-width: 830px; padding: 14px 34px 18px; border-radius: 30px; opacity: 0;
      background: linear-gradient(160deg, rgba(24,10,48,.88), rgba(8,4,24,.9)); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.7), inset 0 0 24px rgba(63,240,255,.25);
      font-family: "Lilita One", sans-serif; color: #fff; text-align: center; line-height: 1.02; white-space: nowrap; }
    .neo.pk { border-color: #ff3dbd; box-shadow: 0 0 30px rgba(255,61,189,.75), inset 0 0 24px rgba(255,61,189,.25); }
    .neo.li { border-color: #b6ff3b; box-shadow: 0 0 30px rgba(182,255,59,.7), inset 0 0 24px rgba(182,255,59,.25); }
    .neo small { display: block; font: 900 30px Inter, sans-serif; letter-spacing: .14em; color: #3ff0ff; margin-bottom: 6px; }
    .neo.pk small { color: #ff3dbd; } .neo.li small { color: #b6ff3b; }
    .big { position: absolute; left: 60px; right: 190px; text-align: center; font-family: "Lilita One", sans-serif; color: #fff; line-height: .92; opacity: 0;
      -webkit-text-stroke: 16px #0a0418; paint-order: stroke fill; }
    .big .c { color: #3ff0ff; } .big .p { color: #ff3dbd; } .big .l { color: #b6ff3b; }
    .gl1 { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(63,240,255,.18) 0 3px, rgba(255,61,189,0) 3px 9px); mix-blend-mode: screen; }
    #sky1 { position: absolute; inset: 0; background: linear-gradient(180deg, #4fd2ff 0%, #a8ecff 45%, #ffe3a3 46%, #ffd27a 100%); }
    #sea1 { position: absolute; left: 0; right: 0; top: 820px; height: 260px; background: linear-gradient(180deg, #1fb6d9, #0f8fb8); }
    #sun1 { position: absolute; left: 700px; top: 180px; width: 220px; height: 220px; border-radius: 50%; background: #ffe14a; box-shadow: 0 0 90px #ffd23f; }
    #sh1 { position: absolute; left: 290px; top: 900px; width: 500px; height: 500px; }
    #poof { position: absolute; left: 240px; top: 860px; width: 600px; height: 600px; border-radius: 50%; background: radial-gradient(circle, #fff 0 30%, rgba(220,220,220,.8) 50%, rgba(200,200,200,0) 70%); opacity: 0; }
    #gr1 { position: absolute; inset: 0; backdrop-filter: grayscale(1) brightness(.75); -webkit-backdrop-filter: grayscale(1) brightness(.75); opacity: 0; }
    #q1 { top: 240px; font-size: 160px; } #q1b { top: 600px; font-size: 110px; }""",
"""      <div id="sky1"></div><div id="sun1"></div><div id="sea1"></div>
      <div id="sh1"><svg viewBox="0 0 64 64" style="width:100%;height:100%"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></svg></div>
      <div id="poof"></div><div id="gr1"></div>
      <div id="q0" class="big" style="top:300px;font-size:170px">EINE <span class="c">WELT</span></div>
      <div id="q1" class="big">OHNE <span class="p">MUSCHELN</span>?!</div>
      <div id="q1b" class="neo pk">🐚 ➜ 💨</div>""",
"""      const O = at("L1", "OHNE"), M = at("L1", "Muscheln");
      tl.fromTo("#q0", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, .02);
      tl.to("#q0", { opacity: 0, y: -80, duration: .12 }, O - .12);
      tl.fromTo("#sh1", { scale: 1 }, { scale: 1.1, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0);
      tl.fromTo("#q1", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, O - .05);
      tl.to("#sh1", { scale: 0, rotation: 200, opacity: 0, duration: .25, ease: "back.in(2)" }, M + .1);
      tl.fromTo("#poof", { opacity: 1, scale: .3 }, { opacity: 0, scale: 1.8, duration: .6, ease: "power2.out", immediateRender: false }, M + .3);
      tl.to("#gr1", { opacity: 1, duration: .3 }, M + .35);
      tl.to("#sun1", { y: 500, duration: .5, ease: "power2.in" }, M + .35);
      tl.fromTo("#q1b", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, M + .3);
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s01-stage", { x, y, duration: .04, ease: "none" }, M + .3 + i * .04));""")

# s02 – Muschelpalast stürzt ein
scene("s02", """
    .neo { position: absolute; left: 60px; right: 190px; margin: 0 auto; width: fit-content; max-width: 830px; padding: 14px 34px 18px; border-radius: 30px; opacity: 0;
      background: linear-gradient(160deg, rgba(24,10,48,.88), rgba(8,4,24,.9)); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.7), inset 0 0 24px rgba(63,240,255,.25);
      font-family: "Lilita One", sans-serif; color: #fff; text-align: center; line-height: 1.02; white-space: nowrap; }
    .neo.pk { border-color: #ff3dbd; box-shadow: 0 0 30px rgba(255,61,189,.75), inset 0 0 24px rgba(255,61,189,.25); }
    .neo.li { border-color: #b6ff3b; box-shadow: 0 0 30px rgba(182,255,59,.7), inset 0 0 24px rgba(182,255,59,.25); }
    .neo small { display: block; font: 900 30px Inter, sans-serif; letter-spacing: .14em; color: #3ff0ff; margin-bottom: 6px; }
    .neo.pk small { color: #ff3dbd; } .neo.li small { color: #b6ff3b; }
    .big { position: absolute; left: 60px; right: 190px; text-align: center; font-family: "Lilita One", sans-serif; color: #fff; line-height: .92; opacity: 0;
      -webkit-text-stroke: 16px #0a0418; paint-order: stroke fill; }
    .big .c { color: #3ff0ff; } .big .p { color: #ff3dbd; } .big .l { color: #b6ff3b; }
    .gl1 { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(63,240,255,.18) 0 3px, rgba(255,61,189,0) 3px 9px); mix-blend-mode: screen; }
    #bg2 { position: absolute; inset: 0; background: linear-gradient(180deg, #6b6f7a, #9aa0aa 60%, #c8c0b0 61%, #a89f8e 100%); }
    #pal { position: absolute; left: 140px; top: 560px; width: 800px; height: 700px; transform-origin: 50% 100%; }
    #pal .b { position: absolute; left: 60px; right: 60px; bottom: 0; height: 300px; background: #e9d8e0; border: 8px solid #6b4a5a; border-radius: 12px; }
    #pal .fan { position: absolute; left: 150px; width: 500px; height: 500px; bottom: 210px; }
    #pal .t { position: absolute; bottom: 0; width: 110px; height: 420px; background: #d9b8c8; border: 8px solid #6b4a5a; border-radius: 10px 10px 0 0; }
    .dust { position: absolute; width: 260px; height: 260px; border-radius: 50%; background: radial-gradient(circle, rgba(200,190,170,.95), rgba(200,190,170,0) 70%); opacity: 0; }
    #crk { position: absolute; left: 520px; top: 560px; width: 30px; height: 700px; opacity: 0; }
    #t2 { top: 240px; font-size: 170px; } #t2b { top: 430px; font-size: 96px; }""",
"""      <div id="bg2"></div>
      <div id="pal"><div class="t" style="left:0"></div><div class="t" style="right:0"></div><div class="b"></div><div class="fan"><svg viewBox="0 0 64 64" style="width:100%;height:100%"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></svg></div></div>
      <svg id="crk" viewBox="0 0 30 700"><path d="M15 0 L5 120 L25 220 L8 360 L22 480 L10 700" stroke="#2a1b12" stroke-width="8" fill="none"/></svg>
      """ + "".join(f'<div class="dust" id="du{i}" style="left:{80+i*200}px;top:1100px"></div>' for i in range(5)) + """
      <div id="t2" class="big"><span class="p">PALAST</span></div>
      <div id="t2b" class="neo pk">💥 EINGESTÜRZT!</div>""",
"""      const E = at("L2", "eingestürzt");
      tl.fromTo("#t2", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, line("L2")[0]);
      tl.fromTo("#crk", { opacity: 0 }, { opacity: 1, duration: .1 }, E - .3);
      tl.to("#pal .fan", { y: 300, rotation: 35, duration: .4, ease: "power3.in" }, E);
      tl.to("#pal", { scaleY: .25, rotation: -6, duration: .45, ease: "power3.in" }, E);
      tl.to("#crk", { opacity: 0, duration: .1 }, E + .3);
      [0,1,2,3,4].forEach(i => tl.fromTo("#du" + i, { opacity: 1, scale: .3, y: 0 }, { opacity: 0, scale: 2.4, y: -300, duration: 1, ease: "power2.out", immediateRender: false }, E + .3 + i * .04));
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s02-stage", { x, y, duration: .04, ease: "none" }, E + .3 + i * .04));
      tl.fromTo("#t2b", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, E + .2);""")

# s03 – grauer, leerer Strand mit Regen und trauriger Sonne
scene("s03", """
    .neo { position: absolute; left: 60px; right: 190px; margin: 0 auto; width: fit-content; max-width: 830px; padding: 14px 34px 18px; border-radius: 30px; opacity: 0;
      background: linear-gradient(160deg, rgba(24,10,48,.88), rgba(8,4,24,.9)); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.7), inset 0 0 24px rgba(63,240,255,.25);
      font-family: "Lilita One", sans-serif; color: #fff; text-align: center; line-height: 1.02; white-space: nowrap; }
    .neo.pk { border-color: #ff3dbd; box-shadow: 0 0 30px rgba(255,61,189,.75), inset 0 0 24px rgba(255,61,189,.25); }
    .neo.li { border-color: #b6ff3b; box-shadow: 0 0 30px rgba(182,255,59,.7), inset 0 0 24px rgba(182,255,59,.25); }
    .neo small { display: block; font: 900 30px Inter, sans-serif; letter-spacing: .14em; color: #3ff0ff; margin-bottom: 6px; }
    .neo.pk small { color: #ff3dbd; } .neo.li small { color: #b6ff3b; }
    .big { position: absolute; left: 60px; right: 190px; text-align: center; font-family: "Lilita One", sans-serif; color: #fff; line-height: .92; opacity: 0;
      -webkit-text-stroke: 16px #0a0418; paint-order: stroke fill; }
    .big .c { color: #3ff0ff; } .big .p { color: #ff3dbd; } .big .l { color: #b6ff3b; }
    .gl1 { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(63,240,255,.18) 0 3px, rgba(255,61,189,0) 3px 9px); mix-blend-mode: screen; }
    #bg3 { position: absolute; inset: 0; background: linear-gradient(180deg, #5b616b 0%, #7c828c 50%, #8d8a80 51%, #6f6c63 100%); }
    #rain { position: absolute; inset: -200px 0 0 0; background: repeating-linear-gradient(105deg, rgba(220,230,240,.0) 0 22px, rgba(220,230,240,.55) 22px 25px); }
    #ss { position: absolute; left: 380px; top: 470px; width: 320px; height: 320px; border-radius: 50%; background: #c9c39a; border: 10px solid #8a8460; }
    #ss svg { width: 100%; height: 100%; }
    #tumb { position: absolute; left: -200px; top: 1180px; width: 140px; height: 140px; border-radius: 50%; border: 10px dashed #9c8f6a; }
    #t3 { top: 240px; font-size: 170px; } #t3b { top: 1000px; font-size: 104px; }""",
"""      <div id="bg3"></div><div id="rain"></div>
      <div id="ss"><svg viewBox="0 0 100 100"><circle cx="34" cy="40" r="5" fill="#4a4530"/><circle cx="66" cy="40" r="5" fill="#4a4530"/><path d="M30 72 Q50 56 70 72" stroke="#4a4530" stroke-width="5" fill="none"/><path d="M34 47 Q31 56 34 60" stroke="#6fb4ff" stroke-width="4" fill="none"/></svg></div>
      <div id="tumb"></div>
      <div id="t3" class="big">STRAND</div>
      <div id="t3b" class="neo">🌧️ GRAU &amp; LEER</div>""",
"""      const t = line("L3")[0];
      tl.fromTo("#rain", { y: 0 }, { y: 400, duration: 2, ease: "none" }, t - .2);
      tl.fromTo("#tumb", { x: 0, rotation: 0 }, { x: 1400, rotation: 720, duration: 1.8, ease: "none" }, t);
      tl.fromTo("#ss", { y: 40 }, { y: 70, duration: .5, yoyo: true, repeat: 3, ease: "sine.inOut" }, t);
      tl.fromTo("#t3", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#t3b", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, at("L3", "grau") - .05);""")

# s04 – arbeitslose Krabbe mit Schild
scene("s04", """
    .neo { position: absolute; left: 60px; right: 190px; margin: 0 auto; width: fit-content; max-width: 830px; padding: 14px 34px 18px; border-radius: 30px; opacity: 0;
      background: linear-gradient(160deg, rgba(24,10,48,.88), rgba(8,4,24,.9)); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.7), inset 0 0 24px rgba(63,240,255,.25);
      font-family: "Lilita One", sans-serif; color: #fff; text-align: center; line-height: 1.02; white-space: nowrap; }
    .neo.pk { border-color: #ff3dbd; box-shadow: 0 0 30px rgba(255,61,189,.75), inset 0 0 24px rgba(255,61,189,.25); }
    .neo.li { border-color: #b6ff3b; box-shadow: 0 0 30px rgba(182,255,59,.7), inset 0 0 24px rgba(182,255,59,.25); }
    .neo small { display: block; font: 900 30px Inter, sans-serif; letter-spacing: .14em; color: #3ff0ff; margin-bottom: 6px; }
    .neo.pk small { color: #ff3dbd; } .neo.li small { color: #b6ff3b; }
    .big { position: absolute; left: 60px; right: 190px; text-align: center; font-family: "Lilita One", sans-serif; color: #fff; line-height: .92; opacity: 0;
      -webkit-text-stroke: 16px #0a0418; paint-order: stroke fill; }
    .big .c { color: #3ff0ff; } .big .p { color: #ff3dbd; } .big .l { color: #b6ff3b; }
    .gl1 { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(63,240,255,.18) 0 3px, rgba(255,61,189,0) 3px 9px); mix-blend-mode: screen; }
    #bg4 { position: absolute; inset: 0; background: linear-gradient(180deg, #6b707a, #8b8f98 55%, #9b8f78 56%, #7d7360 100%); }
    #cr { position: absolute; left: 290px; top: 760px; width: 500px; height: 420px; }
    #sg { position: absolute; left: 330px; top: 520px; width: 420px; padding: 24px 0 30px; background: #c9a46a; border: 10px solid #6b4a26; border-radius: 10px; font: 400 72px/1 "Lilita One", sans-serif; color: #2a1b12; text-align: center; transform: rotate(-6deg); }
    #t4 { top: 240px; font-size: 160px; } #t4b { top: 1240px; font-size: 104px; }""",
"""      <div id="bg4"></div>
      <div id="sg">SUCHE<br>JOB 😭</div>
      <svg id="cr" viewBox="0 0 200 170"><ellipse cx="100" cy="110" rx="70" ry="45" fill="#e2553f" stroke="#8a2a1a" stroke-width="5"/>
        <path d="M30 110 L5 135 M38 125 L15 155 M162 110 L195 135 M170 125 L185 155" stroke="#8a2a1a" stroke-width="7" stroke-linecap="round"/>
        <path d="M45 80 L25 35 M155 80 L175 35" stroke="#8a2a1a" stroke-width="7"/><circle cx="25" cy="30" r="17" fill="#e2553f" stroke="#8a2a1a" stroke-width="5"/><circle cx="175" cy="30" r="17" fill="#e2553f" stroke="#8a2a1a" stroke-width="5"/>
        <circle cx="80" cy="95" r="9" fill="#fff"/><circle cx="120" cy="95" r="9" fill="#fff"/><circle cx="80" cy="98" r="4" fill="#111"/><circle cx="120" cy="98" r="4" fill="#111"/>
        <path d="M82 130 Q100 118 118 130" stroke="#5a1a10" stroke-width="5" fill="none"/>
        <path id="tr1" d="M78 106 Q74 118 78 126" stroke="#6fb4ff" stroke-width="5" fill="none"/><path d="M122 106 Q126 118 122 126" stroke="#6fb4ff" stroke-width="5" fill="none"/></svg>
      <div id="t4" class="big"><span class="p">KRABBEN</span></div>
      <div id="t4b" class="neo pk">🦀 ARBEITSLOS!</div>""",
"""      const t = line("L4")[0], A = at("L4", "arbeitslos");
      tl.fromTo("#t4", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#cr", { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: .3, ease: "back.out(2)" }, t);
      tl.fromTo("#sg", { y: -400, rotation: -30 }, { y: 0, rotation: -6, duration: .4, ease: "bounce.out" }, t + .1);
      tl.to("#cr", { rotation: 4, duration: .12, yoyo: true, repeat: 7, ease: "sine.inOut" }, A);
      tl.fromTo("#t4b", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, A - .05);""")

# s05 – Wal mit Koffer zieht aus
scene("s05", """
    .neo { position: absolute; left: 60px; right: 190px; margin: 0 auto; width: fit-content; max-width: 830px; padding: 14px 34px 18px; border-radius: 30px; opacity: 0;
      background: linear-gradient(160deg, rgba(24,10,48,.88), rgba(8,4,24,.9)); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.7), inset 0 0 24px rgba(63,240,255,.25);
      font-family: "Lilita One", sans-serif; color: #fff; text-align: center; line-height: 1.02; white-space: nowrap; }
    .neo.pk { border-color: #ff3dbd; box-shadow: 0 0 30px rgba(255,61,189,.75), inset 0 0 24px rgba(255,61,189,.25); }
    .neo.li { border-color: #b6ff3b; box-shadow: 0 0 30px rgba(182,255,59,.7), inset 0 0 24px rgba(182,255,59,.25); }
    .neo small { display: block; font: 900 30px Inter, sans-serif; letter-spacing: .14em; color: #3ff0ff; margin-bottom: 6px; }
    .neo.pk small { color: #ff3dbd; } .neo.li small { color: #b6ff3b; }
    .big { position: absolute; left: 60px; right: 190px; text-align: center; font-family: "Lilita One", sans-serif; color: #fff; line-height: .92; opacity: 0;
      -webkit-text-stroke: 16px #0a0418; paint-order: stroke fill; }
    .big .c { color: #3ff0ff; } .big .p { color: #ff3dbd; } .big .l { color: #b6ff3b; }
    .gl1 { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(63,240,255,.18) 0 3px, rgba(255,61,189,0) 3px 9px); mix-blend-mode: screen; }
    #bg5 { position: absolute; inset: 0; background: linear-gradient(180deg, #66707e, #8a93a0 40%, #3f5f78 41%, #2a4458 100%); }
    #wh { position: absolute; left: 140px; top: 820px; width: 700px; height: 420px; }
    #bye { position: absolute; left: 640px; top: 700px; font: 400 80px "Lilita One", sans-serif; color: #fff; -webkit-text-stroke: 10px #0a0418; paint-order: stroke fill; opacity: 0; transform: rotate(8deg); }
    #t5 { top: 240px; font-size: 140px; } #t5b { top: 560px; font-size: 104px; }""",
"""      <div id="bg5"></div>
      <svg id="wh" viewBox="0 0 350 210"><path d="M20 120 Q40 40 160 50 Q270 55 300 110 Q320 150 260 170 Q150 195 60 170 Q20 160 20 120 Z" fill="#4a6380" stroke="#22364a" stroke-width="5"/>
        <path d="M290 110 L345 70 L335 120 L345 165 Z" fill="#4a6380" stroke="#22364a" stroke-width="5"/><path d="M40 150 Q150 185 270 160" fill="#dfe8ee"/>
        <circle cx="80" cy="100" r="8" fill="#fff"/><circle cx="80" cy="102" r="4" fill="#111"/><path d="M60 128 Q75 118 92 128" stroke="#22364a" stroke-width="4" fill="none"/>
        <path d="M78 108 Q74 120 78 128" stroke="#9fd8ff" stroke-width="4" fill="none"/>
        <rect x="150" y="10" width="90" height="60" rx="8" fill="#b5651d" stroke="#5a3010" stroke-width="5"/><rect x="180" y="0" width="30" height="14" rx="5" fill="none" stroke="#5a3010" stroke-width="5"/>
        <rect x="160" y="30" width="22" height="18" rx="3" fill="#ffd23f"/></svg>
      <div id="bye">TSCHÜSS! 👋</div>
      <div id="t5" class="big">SOGAR DER <span class="c">WAL</span></div>
      <div id="t5b" class="neo">🧳 ZIEHT AUS!</div>""",
"""      const t = line("L5")[0], A = at("L5", "aus");
      tl.fromTo("#t5", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#wh", { x: -200 }, { x: 900, duration: 1.8, ease: "power1.in" }, t + .1);
      tl.to("#wh", { y: -20, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, t + .1);
      tl.fromTo("#bye", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, A - .1);
      tl.fromTo("#t5b", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, A - .05);""")

# s06 – Farbe zurück, Muschelregen, Insel, Folgen
scene("s06", """
    .neo { position: absolute; left: 60px; right: 190px; margin: 0 auto; width: fit-content; max-width: 830px; padding: 14px 34px 18px; border-radius: 30px; opacity: 0;
      background: linear-gradient(160deg, rgba(24,10,48,.88), rgba(8,4,24,.9)); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.7), inset 0 0 24px rgba(63,240,255,.25);
      font-family: "Lilita One", sans-serif; color: #fff; text-align: center; line-height: 1.02; white-space: nowrap; }
    .neo.pk { border-color: #ff3dbd; box-shadow: 0 0 30px rgba(255,61,189,.75), inset 0 0 24px rgba(255,61,189,.25); }
    .neo.li { border-color: #b6ff3b; box-shadow: 0 0 30px rgba(182,255,59,.7), inset 0 0 24px rgba(182,255,59,.25); }
    .neo small { display: block; font: 900 30px Inter, sans-serif; letter-spacing: .14em; color: #3ff0ff; margin-bottom: 6px; }
    .neo.pk small { color: #ff3dbd; } .neo.li small { color: #b6ff3b; }
    .big { position: absolute; left: 60px; right: 190px; text-align: center; font-family: "Lilita One", sans-serif; color: #fff; line-height: .92; opacity: 0;
      -webkit-text-stroke: 16px #0a0418; paint-order: stroke fill; }
    .big .c { color: #3ff0ff; } .big .p { color: #ff3dbd; } .big .l { color: #b6ff3b; }
    .gl1 { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(0deg, rgba(63,240,255,.18) 0 3px, rgba(255,61,189,0) 3px 9px); mix-blend-mode: screen; }
    #bg6 { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 55%, #3ff0ff 0%, #13a8d0 40%, #0a5a92 100%); }
    #isl { position: absolute; left: 190px; top: 700px; width: 700px; height: 460px; border-radius: 50%; background: radial-gradient(ellipse, #7fd36a 0 55%, #ffe3a3 56% 68%, rgba(255,227,163,0) 70%); }
    #isl .pal { position: absolute; left: 250px; top: 120px; width: 200px; height: 200px; }
    .sh { position: absolute; width: 110px; height: 110px; opacity: 0; }
    #t6 { top: 230px; font-size: 130px; } #t6b { top: 420px; font-size: 150px; }
    #f6 { position: absolute; left: 60px; right: 190px; margin: 0 auto; top: 1240px; width: 440px; height: 112px; border-radius: 56px; background: #ff3dbd; color: #fff; font: 900 54px/112px Inter, sans-serif; text-align: center; opacity: 0; box-shadow: 0 0 40px rgba(255,61,189,.8); }""",
"""      <div id="bg6"></div>
      <div id="isl"><div class="pal"><svg viewBox="0 0 64 64" style="width:100%;height:100%"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></svg></div></div>
      """ + "".join(f'<div class="sh" id="r{i}" style="left:{60+(i*137)%820}px;top:-150px"><svg viewBox="0 0 64 64" style="width:100%;height:100%"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></svg></div>' for i in range(14)) + """
      <div id="t6" class="big">ZUM <span class="l">GLÜCK</span></div>
      <div id="t6b" class="big"><span class="p">MUSCHEL-TAL</span> 🐚</div>
      <div id="f6">+ Folgen</div>""",
"""      const t = line("L6")[0], M = at("L6", "Muschel-Tal"), F = at("L6", "Folg");
      tl.fromTo("#bg6", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: .35, ease: "power3.out" }, t - .1);
      tl.fromTo("#isl", { scale: .2, opacity: 0 }, { scale: 1, opacity: 1, duration: .45, ease: "back.out(2)" }, t);
      [...Array(14).keys()].forEach(i => tl.fromTo("#r" + i, { opacity: 1, y: 0, rotation: 0 }, { y: 2200, rotation: (i % 2 ? 1 : -1) * 400, duration: 1.6 + (i % 4) * .2, ease: "power1.in", immediateRender: false }, t + (i % 5) * .08));
      tl.fromTo("#t6", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#t6b", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, M - .05);
      tl.to("#t6b", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, M + .3);
      tl.fromTo("#f6", { opacity: 0, scale: .5 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(3)" }, F - .05);""", blur=False)
