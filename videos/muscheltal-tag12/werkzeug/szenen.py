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

# s01 – Tag 1 (leer) → Glitch → Tag 12 (voll)
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
    .rg { position: absolute; left: 475px; top: 360px; width: 300px; height: 300px; margin: -150px; border-radius: 50%; border: 20px solid #3ff0ff; opacity: 0; box-shadow: 0 0 40px #3ff0ff; } #rg1 { border-color: #ff3dbd; box-shadow: 0 0 40px #ff3dbd; } #rg2 { border-color: #b6ff3b; box-shadow: 0 0 40px #b6ff3b; }
    .pt { position: absolute; font-size: 90px; line-height: 1; width: 90px; height: 90px; opacity: 0; }
    #t1 { position: absolute; inset: 0; background: url(bilder/tag1.jpg) center/cover; }
    #d1 { top: 260px; font-size: 200px; } #d2 { top: 260px; font-size: 200px; }
    #lb1 { top: 520px; font-size: 56px; } #lb2 { top: 520px; font-size: 56px; }""",
"""      <div id="t1"></div>
      <div id="d1" class="big">TAG <span class="c">1</span></div>
      <div id="lb1" class="neo"><small>VORHER</small>nur leere Wiese 🌱</div>
      <div id="d2" class="big">TAG <span class="p">12</span></div>
      <div id="lb2" class="neo pk"><small>JETZT</small>DAS HIER 🤯</div>
      <div class="gl1"></div>
      <div id="fl1" style="position:absolute;inset:0;background:#fff;opacity:0"></div>
      <div class="rg" id="rg0"></div><div class="rg" id="rg1"></div><div class="rg" id="rg2"></div>
      """ + "".join(f'<div class="pt" id="pa{i}" style="left:433px;top:330px">{e}</div>' for i, e in enumerate("💥⚡🤯✨💥⚡🤯✨💥⚡🤯✨")) + """""",
"""      const B = line("L1b")[0];
      tl.fromTo("#d1", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, .02);
      tl.fromTo("#lb1", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L1", "nur") - .05);
      tl.to(["#d1", "#lb1"], { opacity: 0, scale: .6, duration: .12 }, B - .12);
      tl.to("#t1", { opacity: 0, scale: 1.25, duration: .25, ease: "power2.in" }, B - .1);
      [0,.05,.1,.15].forEach((d, i) => tl.to("#s01-stage", { x: i % 2 ? -14 : 14, duration: .03, ease: "none" }, B - .05 + d)); tl.to("#s01-stage", { x: 0, duration: .03 }, B - .05 + .2); tl.fromTo(".gl1", { opacity: .9 }, { opacity: 0, duration: .3, immediateRender: false }, B - .05);
      tl.fromTo("#d2", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, B);
      tl.fromTo("#lb2", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L1b", "DAS") - .05);
      tl.to("#d2", { scale: 1.08, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut" }, B + .4);
      const BOOM = t => { tl.fromTo("#fl1", { opacity: .85 }, { opacity: 0, duration: .3, ease: "power2.out", immediateRender: false }, t);
        ["#rg0", "#rg1", "#rg2"].forEach((q, i) => tl.fromTo(q, { opacity: 1, scale: .2 }, { opacity: 0, scale: 5, duration: .8, ease: "power3.out", immediateRender: false }, t + i * .08));
        [[22,-12],[-24,10],[18,14],[-14,-10],[10,6],[0,0]].forEach(([x, y], i) => tl.to("#s01-stage", { x, y, duration: .04, ease: "none" }, t + .02 + i * .04)); };
      BOOM(.02);
      [...Array(12).keys()].forEach(i => { const a = i / 12 * 6.283, r = 320 + (i % 3) * 120; tl.fromTo("#pa" + i, { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: Math.cos(a) * r * .8, y: Math.sin(a) * r, scale: 1.4, rotation: (i % 2 ? 1 : -1) * 200, opacity: 0, duration: 1.1, ease: "power3.out", immediateRender: false }, B + .02 + (i % 3) * .05); });
      BOOM(B - .02);
      tl.fromTo("#d1", { rotation: -12 }, { rotation: 0, duration: .5, ease: "elastic.out(1.2,.4)", immediateRender: false }, .02);
      tl.fromTo("#d2", { rotation: 14 }, { rotation: 0, duration: .5, ease: "elastic.out(1.2,.4)", immediateRender: false }, B);
      tl.fromTo("#d2 .p", { textShadow: "0 0 0px #ff3dbd" }, { textShadow: "0 0 70px #ff3dbd", duration: .2, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false }, B + .3);""")

# s02 – Blitzschnitte Gebäude, Namen ploppen
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
    .tg { top: 300px; font-size: 76px; }
    #e2 { top: 300px; font-size: 64px; }""",
"""      <div id="g0" class="neo tg">🏰 PALAST</div><div id="g1" class="neo pk tg">🪩 CLUB</div><div id="g2" class="neo li tg">🎬 KINO</div><div id="g3" class="neo pk tg">💎 GOLDEN PEARL</div>
      <div id="e2" class="neo li"><small>UND DAS BESTE</small>GEBAUT VON EUCH 💚</div>
      <div class="gl1"></div>""",
"""      const W = ["Palast", "Club", "Kino", "Golden"].map(w => at("L2", w));
      W.forEach((t, i) => { tl.fromTo("#g" + i, { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, t - .04); if (i < 3) tl.to("#g" + i, { opacity: 0, duration: .06 }, W[i + 1] - .08); tl.fromTo(".gl1", { opacity: .7 }, { opacity: 0, duration: .2, immediateRender: false }, t - .05); });
      tl.to("#g3", { opacity: 0, duration: .15 }, line("L2b")[0] - .15);
      tl.fromTo("#e2", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, line("L2b")[0]);""")

# s03 – Tierheim fertig, süße Tiere, Haustier holen
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
    #h3 { top: 250px; font-size: 50px; }
    .ti { position: absolute; width: 240px; height: 240px; border-radius: 34px; background: center/cover; border: 6px solid #fff; box-shadow: 0 0 0 4px #ff3dbd, 0 0 30px rgba(255,61,189,.6); opacity: 0; }
    #ti0 { left: 70px; top: 520px; } #ti1 { left: 340px; top: 500px; } #ti2 { left: 610px; top: 520px; }
    #ti3 { left: 70px; top: 800px; } #ti4 { left: 340px; top: 780px; } #ti5 { left: 610px; top: 800px; }
    #b3 { top: 250px; font-size: 54px; }""",
"""      <div id="h3" class="neo li"><small>🐾 TIERHEIM PFOTENKUSS</small>FERTIG – KEINE STREUNER MEHR!</div>
      """ + "".join(f'<div class="ti" id="ti{i}" style="background-image:url(bilder/{a}.jpg)"></div>' for i, a in enumerate(["hund","katze","hase","schildi","schwein","robbe"])) + """
      <div id="b3" class="neo pk"><small>WENN DAS SPIEL STARTET</small>DEIN EIGENES HAUSTIER 💗</div>""",
"""      tl.fromTo("#h3", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, line("L3")[0] - .05);
      [0,1,2,3,4,5].forEach(i => tl.fromTo("#ti" + i, { opacity: 0, scale: .2, rotation: (i % 2 ? 20 : -20) }, { opacity: 1, scale: 1, rotation: 0, duration: .35, ease: "back.out(3)" }, at("L3", "keine") + i * .12));
      tl.to(".ti", { y: -14, duration: .35, yoyo: true, repeat: 7, ease: "sine.inOut", stagger: .08 }, at("L3", "keine") + .9);
      tl.to("#h3", { opacity: 0, duration: .15 }, at("L3b", "Haustier") - .4);
      tl.fromTo("#b3", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L3b", "Haustier") - .3);""")

# s04 – 3 Jobs gesucht + Türsteher-Info
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
    #j4 { top: 260px; font-size: 64px; }
    #n4 { position: absolute; left: 60px; right: 190px; top: 420px; display: flex; justify-content: center; gap: 24px; }
    #n4 div { width: 200px; height: 200px; border-radius: 40px; background: rgba(10,4,24,.9); border: 5px solid #b6ff3b; box-shadow: 0 0 24px rgba(182,255,59,.7); display: grid; place-items: center; font-size: 120px; opacity: 0; }
    #q4 { top: 300px; font-size: 170px; }
    #c4 { top: 650px; font-size: 46px; }""",
"""      <div id="j4" class="neo li"><small>🐾 TIERHEIM SUCHT</small>3 LEUTE FÜRS TEAM</div>
      <div id="n4"><div>💼</div><div>💼</div><div>💼</div></div>
      <div id="q4" class="big">WER <span class="p">WILL?</span></div>
      <div id="c4" class="neo pk">💬 SCHREIB'S IN DIE KOMMENTARE</div>
      <div class="gl1"></div>""",
"""      tl.fromTo("#j4", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, line("L4")[0] - .05);
      tl.fromTo("#n4 div", { opacity: 0, scale: .2, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: .3, ease: "back.out(3)", stagger: .15 }, at("L4", "drei") - .05);
      [0,.05,.1,.15].forEach((d, i) => tl.to("#s04-stage", { x: i % 2 ? -14 : 14, duration: .03, ease: "none" }, line("L4b")[0] + d)); tl.to("#s04-stage", { x: 0, duration: .03 }, line("L4b")[0] + .2); tl.fromTo(".gl1", { opacity: .9 }, { opacity: 0, duration: .3, immediateRender: false }, line("L4b")[0]);
      tl.fromTo("#q4", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, line("L4b")[0]);
      tl.to("#q4", { rotation: -4, duration: .12, yoyo: true, repeat: 5, ease: "sine.inOut" }, line("L4b")[0] + .3);
      tl.to(["#j4", "#n4"], { opacity: 0, duration: .15 }, line("L4b")[0] - .1);
      tl.fromTo("#c4", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L4b", "Kommentare") - .2);""")

# s05 – Neuheiten: Golden Pearl Minispiele, Hütte mit Tür + Licht
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
    .ph { position: absolute; border-radius: 34px; overflow: hidden; border: 6px solid #fff; box-shadow: 0 0 0 4px #3ff0ff, 0 0 40px rgba(63,240,255,.6); opacity: 0; }
    .ph img { display: block; width: 100%; }
    #p5a { left: 150px; top: 380px; width: 640px; height: 860px; } #p5a img { margin-top: -10px; }
    #p5b { left: 90px; top: 400px; width: 760px; }
    #n5 { top: 250px; font-size: 64px; } #m5 { top: 250px; font-size: 58px; }""",
"""      <div id="n5" class="neo pk"><small>NEU 💎</small>4 MINISPIELE IM GOLDEN PEARL</div>
      <div class="ph" id="p5a"><img src="bilder/gp_menu_c.jpg"></div>
      <div id="m5" class="neo li"><small>NEU 🏠</small>HÜTTE MIT TÜR &amp; LICHT</div>
      <div class="ph" id="p5b"><img src="bilder/huette_neu_c.jpg"></div>
      <div class="gl1"></div>""",
"""      const B = line("L6b")[0];
      tl.fromTo("#n5", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, line("L6")[0]);
      tl.fromTo("#p5a", { opacity: 0, y: 400, rotation: 8 }, { opacity: 1, y: 0, rotation: -2, duration: .45, ease: "back.out(1.8)" }, at("L6", "Golden") - .1);
      tl.to(["#n5", "#p5a"], { opacity: 0, x: -300, duration: .2, ease: "power2.in" }, B - .2);
      [0,.05,.1,.15].forEach((d, i) => tl.to("#s05-stage", { x: i % 2 ? -14 : 14, duration: .03, ease: "none" }, B - .05 + d)); tl.to("#s05-stage", { x: 0, duration: .03 }, B - .05 + .2); tl.fromTo(".gl1", { opacity: .9 }, { opacity: 0, duration: .3, immediateRender: false }, B - .05);
      tl.fromTo("#m5", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, B);
      tl.fromTo("#p5b", { opacity: 0, x: 400, rotation: -8 }, { opacity: 1, x: 0, rotation: 2, duration: .45, ease: "back.out(1.8)" }, at("L6b", "Hütten") - .05);""")

# s06 – Fahrzeuge 2x, Freunde einladen +10/+10
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
    .ph { position: absolute; border-radius: 34px; overflow: hidden; border: 6px solid #fff; box-shadow: 0 0 0 4px #ff3dbd, 0 0 40px rgba(255,61,189,.6); opacity: 0; }
    .ph img { display: block; width: 100%; }
    #p6 { left: 150px; top: 400px; width: 640px; height: 760px; } #p6 img { margin-top: -60px; }
    #x6 { top: 250px; font-size: 64px; }
    #s6 { top: 1000px; font-size: 200px; }
    #f6 { top: 250px; font-size: 62px; }
    #pl { position: absolute; left: 60px; right: 190px; top: 460px; display: flex; justify-content: center; gap: 40px; }
    #pl div { width: 300px; padding: 30px 0 34px; border-radius: 40px; background: rgba(10,4,24,.9); border: 5px solid #b6ff3b; box-shadow: 0 0 30px rgba(182,255,59,.7); text-align: center; font: 400 110px/1 "Lilita One", sans-serif; color: #b6ff3b; opacity: 0; }
    #pl div small { display: block; font: 900 36px Inter, sans-serif; color: #fff; margin-top: 10px; }""",
"""      <div id="x6" class="neo pk"><small>🛵 MOPED &amp; E-SCOOTER</small>DOPPELT SO SCHNELL</div>
      <div class="ph" id="p6"><img src="bilder/moped.jpg"></div>
      <div id="s6" class="big"><span class="p">2×</span></div>
      <div id="f6" class="neo li"><small>👯 FREUNDE EINLADEN</small>IHR BEIDE BEKOMMT</div>
      <div id="pl"><div>+10🐚<small>DU</small></div><div>+10🐚<small>DEIN FREUND</small></div></div>
      <div class="gl1"></div>""",
"""      const B = line("L7b")[0];
      tl.fromTo("#x6", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, line("L7")[0]);
      tl.fromTo("#p6", { opacity: 0, x: -500 }, { opacity: 1, x: 0, duration: .35, ease: "power3.out" }, line("L7")[0] + .1);
      tl.to("#p6", { x: 30, duration: 1.6, ease: "none" }, line("L7")[0] + .45);
      tl.fromTo("#s6", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L7", "doppelt"));
      tl.to(["#x6", "#p6", "#s6"], { opacity: 0, duration: .15 }, B - .15);
      [0,.05,.1,.15].forEach((d, i) => tl.to("#s06-stage", { x: i % 2 ? -14 : 14, duration: .03, ease: "none" }, B - .05 + d)); tl.to("#s06-stage", { x: 0, duration: .03 }, B - .05 + .2); tl.fromTo(".gl1", { opacity: .9 }, { opacity: 0, duration: .3, immediateRender: false }, B - .05);
      tl.fromTo("#f6", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, B);
      tl.fromTo("#pl div", { opacity: 0, scale: .2, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: .35, ease: "back.out(3)", stagger: .2 }, at("L7b", "beide") - .1);
      tl.to("#pl div", { scale: 1.08, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L7b", "zehn") + .3);""")

# s07 – Fast bereit: 823 / 1.000, noch 177
scene("s07", """
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
    #r7 { top: 250px; font-size: 64px; }
    #br { position: absolute; left: 100px; right: 230px; top: 470px; opacity: 0; }
    #br .tr { height: 90px; border-radius: 45px; background: rgba(10,4,24,.85); border: 5px solid #3ff0ff; box-shadow: 0 0 30px rgba(63,240,255,.6); overflow: hidden; }
    #br .fi { height: 100%; width: 0; background: linear-gradient(90deg, #3ff0ff, #ff3dbd); }
    #br .lb { display: flex; justify-content: space-between; margin-top: 16px; font: 400 64px "Lilita One", sans-serif; color: #fff; -webkit-text-stroke: 10px #0a0418; paint-order: stroke fill; }
    #br .lb span:last-child { color: #b6ff3b; }
    #k7 { top: 700px; font-size: 76px; }""",
"""      <div id="r7" class="neo li"><small>🎮 DAS SPIEL</small>FAST BEREIT!</div>
      <div id="br"><div class="tr"><div class="fi"></div></div><div class="lb"><span>823</span><span>1.000</span></div></div>
      <div id="k7" class="neo pk"><small>ES FEHLEN NUR NOCH</small>177 SPIELER 👀</div>
      <div class="gl1"></div>""",
"""      tl.fromTo("#r7", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, line("L8")[0]);
      tl.fromTo("#br", { opacity: 0 }, { opacity: 1, duration: .25 }, line("L8")[0] + .4);
      tl.fromTo("#br .fi", { width: "0%" }, { width: "82.3%", duration: 1.6, ease: "power2.out" }, line("L8")[0] + .5);
      [0,.05,.1,.15].forEach((d, i) => tl.to("#s07-stage", { x: i % 2 ? -14 : 14, duration: .03, ease: "none" }, at("L8b", "177") - .05 + d)); tl.to("#s07-stage", { x: 0, duration: .03 }, at("L8b", "177") - .05 + .2); tl.fromTo(".gl1", { opacity: .9 }, { opacity: 0, duration: .3, immediateRender: false }, at("L8b", "177") - .05);
      tl.fromTo("#k7", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L8b", "177") - .05);
      tl.to("#k7", { scale: 1.07, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L8b", "177") + .4);""")

# s05 – Outro
scene("s08", """
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
    #o5 { top: 280px; font-size: 140px; }
    #f5 { position: absolute; left: 60px; right: 190px; margin: 0 auto; top: 520px; width: 440px; height: 112px; border-radius: 56px; background: #ff3dbd; color: #fff; font: 900 54px/112px Inter, sans-serif; text-align: center; opacity: 0; box-shadow: 0 0 40px rgba(255,61,189,.8); }
    #z5 { top: 680px; font-size: 60px; }""",
"""      <div id="o5" class="big">FOLG <span class="c">MIR</span></div>
      <div id="f5">+ Folgen</div>
      <div id="z5" class="neo li">🏠 & ZIEH HEUTE EIN!</div>""",
"""      tl.fromTo("#o5", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L5", "Folg") - .05);
      tl.fromTo("#f5", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L5", "Folg") + .25);
      tl.to("#f5", { scale: 1.08, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L5", "Folg") + .6);
      tl.fromTo("#z5", { opacity: 0, scale: 2.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "power4.out" }, at("L5", "zieh") - .05);""", blur=False)
