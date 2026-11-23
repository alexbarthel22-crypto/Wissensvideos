import json
import sys
from pathlib import Path
D = Path(sys.argv[1]); LOGO = Path(sys.argv[2]).read_text().strip()
SHELL = '<svg viewBox="0 0 64 64"><path d="M32 47 L8.8 40.8 Q5.0 34.0 12.7 32.7 Q11.6 25.0 19.2 26.7 Q21.0 19.1 27.5 23.4 Q32.0 17.0 36.5 23.4 Q43.0 19.1 44.8 26.7 Q52.4 25.0 51.3 32.7 Q59.0 34.0 55.2 40.8 Z" fill="#ffc7b2" stroke="#2a1b12" stroke-width="3" stroke-linejoin="round"/><path d="M32 45L13.9 33.6M32 45L20.0 27.9M32 45L27.8 24.9M32 45L36.2 24.9M32 45L44.0 27.9M32 45L50.1 33.6" stroke="#c43d6b" stroke-width="2" stroke-linecap="round"/></svg>'
LILITA = '@font-face { font-family: "Lilita One"; src: url("assets/fonts/LilitaOne-Regular.woff2") format("woff2"); font-weight: 400; }'

V1 = ""

def scene(sid, css, html, js, blur=True):
    css = css + "\n    .neo { width: auto !important; max-width: none !important; white-space: normal !important; }"
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

COMMON7 = """
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
    .art { position: absolute; inset: 0; width: 1080px; height: 1920px; }
    .H { top: 220px; } .B { top: 1520px; }
"""

# s01 – Volle Muschelstrand-Idylle: alle Muscheln heben ab und fliegen weg → leerer Strand
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
    .art { position: absolute; inset: 0; width: 1080px; height: 1920px; }
    .H { top: 220px; } .B { top: 1520px; }
    #s1a { top: 220px; font-size: 140px; } #s1b { top: 380px; font-size: 175px; }""",
"""      <svg class="art" viewBox="0 0 1080 1920"><defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fd8ff"/><stop offset=".5" stop-color="#bff1ff"/><stop offset="1" stop-color="#ffe2a0"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#g1)"/><rect y="760" width="1080" height="300" fill="#1fb6d9"/><path d="M-60 800 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M-60 910 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M120 800 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M120 910 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M300 800 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M300 910 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M480 800 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M480 910 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M660 800 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M660 910 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M840 800 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M840 910 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M1020 800 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M1020 910 q35 -18 70 0 q35 18 70 0" stroke="#c9f5ff" stroke-width="6" fill="none" opacity=".7"/><path d="M0 1020 Q540 960 1080 1020 L1080 1920 L0 1920Z" fill="#ffd98a"/><circle cx="0" cy="1100" r="4" fill="#e8b860"/><circle cx="97" cy="1153" r="4" fill="#e8b860"/><circle cx="194" cy="1206" r="4" fill="#e8b860"/><circle cx="291" cy="1259" r="4" fill="#e8b860"/><circle cx="388" cy="1312" r="4" fill="#e8b860"/><circle cx="485" cy="1365" r="4" fill="#e8b860"/><circle cx="582" cy="1418" r="4" fill="#e8b860"/><circle cx="679" cy="1471" r="4" fill="#e8b860"/><circle cx="776" cy="1524" r="4" fill="#e8b860"/><circle cx="873" cy="1577" r="4" fill="#e8b860"/><circle cx="970" cy="1630" r="4" fill="#e8b860"/><circle cx="1067" cy="1683" r="4" fill="#e8b860"/><circle cx="84" cy="1736" r="4" fill="#e8b860"/><circle cx="181" cy="1789" r="4" fill="#e8b860"/><circle cx="278" cy="1842" r="4" fill="#e8b860"/><circle cx="375" cy="1895" r="4" fill="#e8b860"/><circle cx="472" cy="1148" r="4" fill="#e8b860"/><circle cx="569" cy="1201" r="4" fill="#e8b860"/><circle cx="666" cy="1254" r="4" fill="#e8b860"/><circle cx="763" cy="1307" r="4" fill="#e8b860"/><circle cx="860" cy="1360" r="4" fill="#e8b860"/><circle cx="957" cy="1413" r="4" fill="#e8b860"/><circle cx="1054" cy="1466" r="4" fill="#e8b860"/><circle cx="71" cy="1519" r="4" fill="#e8b860"/><circle cx="168" cy="1572" r="4" fill="#e8b860"/><circle cx="265" cy="1625" r="4" fill="#e8b860"/><circle cx="362" cy="1678" r="4" fill="#e8b860"/><circle cx="459" cy="1731" r="4" fill="#e8b860"/><circle cx="556" cy="1784" r="4" fill="#e8b860"/><circle cx="653" cy="1837" r="4" fill="#e8b860"/><circle cx="750" cy="1890" r="4" fill="#e8b860"/><circle cx="847" cy="1143" r="4" fill="#e8b860"/><circle cx="944" cy="1196" r="4" fill="#e8b860"/><circle cx="1041" cy="1249" r="4" fill="#e8b860"/><circle cx="58" cy="1302" r="4" fill="#e8b860"/><circle cx="155" cy="1355" r="4" fill="#e8b860"/><circle cx="252" cy="1408" r="4" fill="#e8b860"/><circle cx="349" cy="1461" r="4" fill="#e8b860"/><circle cx="446" cy="1514" r="4" fill="#e8b860"/><circle cx="543" cy="1567" r="4" fill="#e8b860"/><circle cx="640" cy="1620" r="4" fill="#e8b860"/><circle cx="737" cy="1673" r="4" fill="#e8b860"/><circle cx="834" cy="1726" r="4" fill="#e8b860"/><circle cx="931" cy="1779" r="4" fill="#e8b860"/><circle cx="1028" cy="1832" r="4" fill="#e8b860"/><circle cx="45" cy="1885" r="4" fill="#e8b860"/><circle cx="142" cy="1138" r="4" fill="#e8b860"/><circle cx="239" cy="1191" r="4" fill="#e8b860"/><circle cx="336" cy="1244" r="4" fill="#e8b860"/><circle cx="433" cy="1297" r="4" fill="#e8b860"/><circle cx="530" cy="1350" r="4" fill="#e8b860"/><circle cx="627" cy="1403" r="4" fill="#e8b860"/><circle cx="724" cy="1456" r="4" fill="#e8b860"/><circle cx="821" cy="1509" r="4" fill="#e8b860"/><circle cx="918" cy="1562" r="4" fill="#e8b860"/><circle cx="1015" cy="1615" r="4" fill="#e8b860"/><circle cx="32" cy="1668" r="4" fill="#e8b860"/><circle cx="129" cy="1721" r="4" fill="#e8b860"/><circle cx="226" cy="1774" r="4" fill="#e8b860"/><circle cx="323" cy="1827" r="4" fill="#e8b860"/><g transform="translate(90,260) scale(1.4)" fill="#fff"><circle cx="0" cy="0" r="28"/><circle cx="30" cy="-10" r="34"/><circle cx="62" cy="2" r="26"/><rect x="0" y="0" width="62" height="26"/></g><g transform="translate(720,340) scale(1.1)" fill="#fff"><circle cx="0" cy="0" r="28"/><circle cx="30" cy="-10" r="34"/><circle cx="62" cy="2" r="26"/><rect x="0" y="0" width="62" height="26"/></g><circle cx="880" cy="200" r="90" fill="#ffe14a"/><g transform="translate(70,1120) scale(1.4)" opacity="1" class="fs" id="fs0"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(230,1120) scale(1.7)" opacity="1" class="fs" id="fs1"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(390,1120) scale(2.0)" opacity="1" class="fs" id="fs2"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(550,1120) scale(1.4)" opacity="1" class="fs" id="fs3"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(710,1120) scale(1.7)" opacity="1" class="fs" id="fs4"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(870,1120) scale(2.0)" opacity="1" class="fs" id="fs5"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(100,1290) scale(1.4)" opacity="1" class="fs" id="fs6"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(260,1290) scale(1.7)" opacity="1" class="fs" id="fs7"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(420,1290) scale(2.0)" opacity="1" class="fs" id="fs8"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(580,1290) scale(1.4)" opacity="1" class="fs" id="fs9"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(740,1290) scale(1.7)" opacity="1" class="fs" id="fs10"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(900,1290) scale(2.0)" opacity="1" class="fs" id="fs11"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(130,1460) scale(1.4)" opacity="1" class="fs" id="fs12"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(290,1460) scale(1.7)" opacity="1" class="fs" id="fs13"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(450,1460) scale(2.0)" opacity="1" class="fs" id="fs14"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(610,1460) scale(1.4)" opacity="1" class="fs" id="fs15"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(770,1460) scale(1.7)" opacity="1" class="fs" id="fs16"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g><g transform="translate(930,1460) scale(2.0)" opacity="1" class="fs" id="fs17"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/><path d="M32 54 L18 26 M32 54 L27 18 M32 54 L37 18 M32 54 L46 26" stroke="#e8467c" stroke-width="2" fill="none"/></g></svg>
      <div id="s1a" class="big">STELL DIR VOR:</div>
      <div id="s1b" class="big"><span class="p">KEINE</span><br>MUSCHELN!</div>""",
"""      const K = at("L1", "KEINE");
      tl.fromTo("#s1a", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, .02);
      tl.to("#s1a", { opacity: 0, y: -60, duration: .12 }, K - .15);
      [...Array(18).keys()].forEach(i => tl.to("#fs" + i, { y: -1800 - (i % 4) * 200, x: (i % 2 ? 1 : -1) * (80 + i * 12), rotation: (i % 2 ? 1 : -1) * 260, duration: .9, ease: "power2.in" }, K + .05 + (i % 6) * .04));
      tl.fromTo("#s1b", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, K - .05);
      tl.fromTo("#s1b .p", { textShadow: "0 0 0px #ff3dbd" }, { textShadow: "0 0 80px #ff3dbd", duration: .12, yoyo: true, repeat: 3, ease: "none", immediateRender: false }, K + .3);
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s01-stage", { x, y, duration: .04, ease: "none" }, K + i * .04));""")

# s02 – Einsiedlerkrebse wohnen in Getränkedosen
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
    .art { position: absolute; inset: 0; width: 1080px; height: 1920px; }
    .H { top: 220px; } .B { top: 1520px; }
    #kk1 { font-size: 140px; } #kk2 { font-size: 80px; }""",
"""      <svg class="art" id="cn2" viewBox="0 0 1080 1920"><defs><linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd27a"/><stop offset=".5" stop-color="#ffb85c"/><stop offset="1" stop-color="#e8935a"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#g2)"/><rect y="1180" width="1080" height="740" fill="#e6c27a"/><circle cx="0" cy="1220" r="5" fill="#c79a4a"/><circle cx="131" cy="1291" r="5" fill="#c79a4a"/><circle cx="262" cy="1362" r="5" fill="#c79a4a"/><circle cx="393" cy="1433" r="5" fill="#c79a4a"/><circle cx="524" cy="1504" r="5" fill="#c79a4a"/><circle cx="655" cy="1575" r="5" fill="#c79a4a"/><circle cx="786" cy="1646" r="5" fill="#c79a4a"/><circle cx="917" cy="1717" r="5" fill="#c79a4a"/><circle cx="1048" cy="1788" r="5" fill="#c79a4a"/><circle cx="99" cy="1859" r="5" fill="#c79a4a"/><circle cx="230" cy="1270" r="5" fill="#c79a4a"/><circle cx="361" cy="1341" r="5" fill="#c79a4a"/><circle cx="492" cy="1412" r="5" fill="#c79a4a"/><circle cx="623" cy="1483" r="5" fill="#c79a4a"/><circle cx="754" cy="1554" r="5" fill="#c79a4a"/><circle cx="885" cy="1625" r="5" fill="#c79a4a"/><circle cx="1016" cy="1696" r="5" fill="#c79a4a"/><circle cx="67" cy="1767" r="5" fill="#c79a4a"/><circle cx="198" cy="1838" r="5" fill="#c79a4a"/><circle cx="329" cy="1249" r="5" fill="#c79a4a"/><circle cx="460" cy="1320" r="5" fill="#c79a4a"/><circle cx="591" cy="1391" r="5" fill="#c79a4a"/><circle cx="722" cy="1462" r="5" fill="#c79a4a"/><circle cx="853" cy="1533" r="5" fill="#c79a4a"/><circle cx="984" cy="1604" r="5" fill="#c79a4a"/><circle cx="35" cy="1675" r="5" fill="#c79a4a"/><circle cx="166" cy="1746" r="5" fill="#c79a4a"/><circle cx="297" cy="1817" r="5" fill="#c79a4a"/><circle cx="428" cy="1228" r="5" fill="#c79a4a"/><circle cx="559" cy="1299" r="5" fill="#c79a4a"/><circle cx="690" cy="1370" r="5" fill="#c79a4a"/><circle cx="821" cy="1441" r="5" fill="#c79a4a"/><circle cx="952" cy="1512" r="5" fill="#c79a4a"/><circle cx="3" cy="1583" r="5" fill="#c79a4a"/><circle cx="134" cy="1654" r="5" fill="#c79a4a"/><circle cx="265" cy="1725" r="5" fill="#c79a4a"/><circle cx="396" cy="1796" r="5" fill="#c79a4a"/><circle cx="527" cy="1867" r="5" fill="#c79a4a"/><circle cx="658" cy="1278" r="5" fill="#c79a4a"/><circle cx="789" cy="1349" r="5" fill="#c79a4a"/><circle cx="920" cy="1420" r="5" fill="#c79a4a"/><circle cx="1051" cy="1491" r="5" fill="#c79a4a"/><circle cx="102" cy="1562" r="5" fill="#c79a4a"/><circle cx="233" cy="1633" r="5" fill="#c79a4a"/><circle cx="364" cy="1704" r="5" fill="#c79a4a"/><circle cx="495" cy="1775" r="5" fill="#c79a4a"/><circle cx="626" cy="1846" r="5" fill="#c79a4a"/><circle cx="757" cy="1257" r="5" fill="#c79a4a"/><circle cx="888" cy="1328" r="5" fill="#c79a4a"/><circle cx="1019" cy="1399" r="5" fill="#c79a4a"/><g transform="translate(540,1150) scale(2.5)"><rect x="-60" y="-110" width="120" height="170" rx="18" fill="#e8433c" stroke="#2a1b12" stroke-width="6"/><rect x="-60" y="-110" width="120" height="22" rx="10" fill="#d8d8d8" stroke="#2a1b12" stroke-width="5"/><text x="0" y="-20" font-family="Lilita One" font-size="40" fill="#fff" text-anchor="middle" transform="rotate(-8)" textLength="96" lengthAdjust="spacingAndGlyphs">COLA</text><path d="M-40 40 Q-75 55 -95 40 M-40 52 Q-70 75 -92 70 M40 40 Q75 55 95 40 M40 52 Q70 75 92 70" stroke="#c7432c" stroke-width="10" fill="none" stroke-linecap="round"/><ellipse cx="-55" cy="20" rx="34" ry="24" fill="#e2553f" stroke="#8a2a1a" stroke-width="5"/><path d="M-30 -108 L-24 -140 M-8 -108 L0 -144" stroke="#8a2a1a" stroke-width="6"/><circle cx="-24" cy="-146" r="13" fill="#fff" stroke="#2a1b12" stroke-width="3"/><circle cx="0" cy="-150" r="13" fill="#fff" stroke="#2a1b12" stroke-width="3"/><circle cx="-22" cy="-144" r="5" fill="#111"/><circle cx="2" cy="-148" r="5" fill="#111"/></g><g transform="translate(170,1380) scale(1.2)"><rect x="-60" y="-110" width="120" height="170" rx="18" fill="#2f7fe0" stroke="#2a1b12" stroke-width="6"/><rect x="-60" y="-110" width="120" height="22" rx="10" fill="#d8d8d8" stroke="#2a1b12" stroke-width="5"/><text x="0" y="-20" font-family="Lilita One" font-size="40" fill="#fff" text-anchor="middle" transform="rotate(-8)" textLength="96" lengthAdjust="spacingAndGlyphs">LIMO</text><path d="M-40 40 Q-75 55 -95 40 M-40 52 Q-70 75 -92 70 M40 40 Q75 55 95 40 M40 52 Q70 75 92 70" stroke="#c7432c" stroke-width="10" fill="none" stroke-linecap="round"/><ellipse cx="-55" cy="20" rx="34" ry="24" fill="#e2553f" stroke="#8a2a1a" stroke-width="5"/><path d="M-30 -108 L-24 -140 M-8 -108 L0 -144" stroke="#8a2a1a" stroke-width="6"/><circle cx="-24" cy="-146" r="13" fill="#fff" stroke="#2a1b12" stroke-width="3"/><circle cx="0" cy="-150" r="13" fill="#fff" stroke="#2a1b12" stroke-width="3"/><circle cx="-22" cy="-144" r="5" fill="#111"/><circle cx="2" cy="-148" r="5" fill="#111"/></g><g transform="translate(910,1400) scale(1.1)"><rect x="-60" y="-110" width="120" height="170" rx="18" fill="#2fbf6a" stroke="#2a1b12" stroke-width="6"/><rect x="-60" y="-110" width="120" height="22" rx="10" fill="#d8d8d8" stroke="#2a1b12" stroke-width="5"/><text x="0" y="-20" font-family="Lilita One" font-size="40" fill="#fff" text-anchor="middle" transform="rotate(-8)" textLength="96" lengthAdjust="spacingAndGlyphs">SPRUDEL</text><path d="M-40 40 Q-75 55 -95 40 M-40 52 Q-70 75 -92 70 M40 40 Q75 55 95 40 M40 52 Q70 75 92 70" stroke="#c7432c" stroke-width="10" fill="none" stroke-linecap="round"/><ellipse cx="-55" cy="20" rx="34" ry="24" fill="#e2553f" stroke="#8a2a1a" stroke-width="5"/><path d="M-30 -108 L-24 -140 M-8 -108 L0 -144" stroke="#8a2a1a" stroke-width="6"/><circle cx="-24" cy="-146" r="13" fill="#fff" stroke="#2a1b12" stroke-width="3"/><circle cx="0" cy="-150" r="13" fill="#fff" stroke="#2a1b12" stroke-width="3"/><circle cx="-22" cy="-144" r="5" fill="#111"/><circle cx="2" cy="-148" r="5" fill="#111"/></g><g transform="translate(820,1080) rotate(12)"><rect x="-80" y="-60" width="160" height="90" rx="8" fill="#c9a46a" stroke="#6b4a26" stroke-width="6"/><text x="0" y="-18" font-family="Lilita One" font-size="32" fill="#2a1b12" text-anchor="middle">ZU</text><text x="0" y="14" font-family="Lilita One" font-size="30" fill="#2a1b12" text-anchor="middle" textLength="140" lengthAdjust="spacingAndGlyphs">VERMIETEN</text><rect x="-6" y="30" width="12" height="90" fill="#6b4a26"/></g></svg>
      <div id="kk1" class="big H"><span class="p">EINSIEDLER-<br>KREBSE</span></div>
      <div id="kk2" class="neo pk B">🥫 WOHNEN IN DOSEN!</div>""",
"""      const t = line("L2")[0], CD = at("L2", "Coladosen");
      tl.fromTo("#cn2", { scale: 1.3, y: 200 }, { scale: 1, y: 0, duration: .5, ease: "back.out(1.6)" }, t);
      tl.fromTo("#kk1", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#kk2", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, CD - .05);
      tl.fromTo("#kk2", { textShadow: "0 0 0px #ff3dbd" }, { textShadow: "0 0 80px #ff3dbd", duration: .12, yoyo: true, repeat: 3, ease: "none", immediateRender: false }, CD + .2);""")

# s03 – Handy: Muschel-Emoji wird gelöscht
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
    .art { position: absolute; inset: 0; width: 1080px; height: 1920px; }
    .H { top: 220px; } .B { top: 1520px; }
    #bg3 { position: absolute; inset: 0; background: radial-gradient(circle at 50% 40%, #7a3dff, #2a0e5a 70%); }
    #ph { position: absolute; left: 250px; top: 430px; width: 580px; height: 1060px; border-radius: 70px; background: #111; border: 14px solid #333; box-shadow: 0 30px 80px rgba(0,0,0,.5); overflow: hidden; }
    #ph .scr { position: absolute; inset: 16px; border-radius: 52px; background: #f2f2f7; overflow: hidden; }
    #ph .bar { height: 120px; background: #fff; border-bottom: 2px solid #ddd; display: flex; align-items: center; padding: 0 30px; font: 800 34px Inter, sans-serif; color: #111; }
    #ph .msg { margin: 30px; padding: 20px 26px; border-radius: 30px; background: #fff; font: 700 34px/1.25 Inter, sans-serif; color: #111; width: fit-content; max-width: 420px; }
    #ph .me { margin-left: auto; background: #3a8bff; color: #fff; }
    #kb { position: absolute; left: 0; right: 0; bottom: 0; height: 420px; background: #d1d4db; display: grid; grid-template-columns: repeat(5, 1fr); padding: 24px; gap: 14px; }
    #kb div { border-radius: 16px; background: #fff; display: grid; place-items: center; font-size: 56px; }
    #kb .sh { background: #ffe4ec; box-shadow: 0 0 0 5px #ff3dbd; }
    #trash { position: absolute; left: 720px; top: 330px; font-size: 140px; opacity: 0; }
    #flyS { position: absolute; width: 110px; height: 110px; left: 0; top: 0; opacity: 0; }
    #x3 { position: absolute; left: 430px; top: 1060px; font-size: 200px; opacity: 0; }
    #e3a { top: 220px; font-size: 120px; } #e3b { top: 1560px; font-size: 104px; }""",
"""      <div id="bg3"></div>
      <div id="ph"><div class="scr"><div class="bar">💬 Beste Freundin</div>
        <div class="msg">Strand morgen? 🏖️</div><div class="msg me">klar, ich bring die …</div>
        <div id="kb"><div>😂</div><div>🔥</div><div>🌊</div><div class="sh" id="key">🐚</div><div>🦀</div><div>😭</div><div>💀</div><div>🫠</div><div>🌴</div><div>☀️</div></div></div></div>
      <div id="trash">🗑️</div>
      <svg id="flyS" viewBox="0 0 64 64"><path d="M32 54 L6 44 Q2 34 10 32 Q8 22 17 23 Q19 13 27 18 Q32 9 37 18 Q45 13 47 23 Q56 22 54 32 Q62 34 58 44 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="2.5"/></svg>
      <div id="x3">❌</div>
      <div id="e3a" class="big"><span class="l">MUSCHEL-EMOJI?</span></div>
      <div id="e3b" class="neo pk">🗑️ GELÖSCHT!</div>""",
"""      const t = line("L3")[0], G = at("L3", "Gelöscht");
      tl.fromTo("#ph", { y: 600, rotation: 8 }, { y: 0, rotation: 0, duration: .4, ease: "back.out(1.6)" }, t - .1);
      tl.fromTo("#e3a", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" },  t - .05);
      tl.to("#key", { scale: 1.25, duration: .15, yoyo: true, repeat: 3 }, t + .5);
      tl.fromTo("#trash", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, G - .45);
      tl.fromTo("#flyS", { opacity: 1, x: 640, y: 1310, scale: .8, rotation: 0 }, { x: 750, y: 360, scale: .4, rotation: 360, duration: .45, ease: "power2.in" }, G - .4);
      tl.to("#flyS", { opacity: 0, duration: .05 }, G + .05);
      tl.to("#key", { opacity: .15, duration: .05 }, G - .4);
      tl.fromTo("#x3", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, G);
      tl.fromTo("#e3b", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" },  G - .05);
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s03-stage", { x, y, duration: .04, ease: "none" },  G + i * .04));""")

# s05 – Urlaub: Pfandflaschen statt Muscheln sammeln
scene("s05", COMMON7 + """
    #bg5 { position: absolute; inset: 0; }
    .pf { position: absolute; font: 900 46px Inter, sans-serif; color: #fff; background: #1fa34a; border: 5px solid #fff; border-radius: 22px; padding: 6px 16px; opacity: 0; }
    #p1 { font-size: 118px; } #p2 { font-size: 70px; }""",
"""      <svg class="art" id="bg5" viewBox="0 0 1080 1920"><defs><linearGradient id="g5s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fd8ff"/><stop offset=".55" stop-color="#bfeeff"/><stop offset="1" stop-color="#fff2c8"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#g5s)"/><circle cx="880" cy="560" r="90" fill="#ffd84a"/><rect y="1000" width="1080" height="200" fill="#2fb7e8"/><rect y="1180" width="1080" height="740" fill="#f2d38c"/>
        <g transform="translate(330,1330)"><circle cx="0" cy="-260" r="70" fill="#f1c09a" stroke="#2a1b12" stroke-width="6"/><path d="M-70 -280 Q0 -360 70 -280" fill="#5a3a1a"/><rect x="-75" y="-60" width="22" height="16" rx="4" fill="#111"/><rect x="-60" y="-200" width="120" height="200" rx="40" fill="#ff7a3d" stroke="#2a1b12" stroke-width="6"/><circle cx="-24" cy="-268" r="7" fill="#111"/><circle cx="24" cy="-268" r="7" fill="#111"/><path d="M-22 -236 Q0 -220 22 -236" stroke="#111" stroke-width="5" fill="none"/><path d="M-40 0 L-50 130 M40 0 L50 130" stroke="#f1c09a" stroke-width="26" stroke-linecap="round"/><path d="M60 -160 L150 -90" stroke="#f1c09a" stroke-width="24" stroke-linecap="round"/>
          <g transform="translate(160,-80)"><path d="M-80 0 L80 0 L60 170 L-60 170 Z" fill="#ff3dbd" stroke="#2a1b12" stroke-width="6"/><path d="M-70 0 Q0 -90 70 0" stroke="#2a1b12" stroke-width="6" fill="none"/>
            <g id="btl"><rect x="-55" y="-90" width="30" height="110" rx="10" fill="#9fe39f" stroke="#2a6a2a" stroke-width="4" transform="rotate(-14)"/><rect x="-12" y="-110" width="30" height="130" rx="10" fill="#b8ecff" stroke="#3a7a9a" stroke-width="4"/><rect x="30" y="-95" width="30" height="115" rx="10" fill="#8a5a2b" stroke="#4a2a0a" stroke-width="4" transform="rotate(12)"/></g></g></g>
        <g transform="translate(720,1520) rotate(-70)"><rect x="-22" y="-80" width="44" height="160" rx="14" fill="#b8ecff" stroke="#3a7a9a" stroke-width="5"/></g><g transform="translate(880,1700) rotate(20)"><rect x="-22" y="-80" width="44" height="160" rx="14" fill="#9fe39f" stroke="#2a6a2a" stroke-width="5"/></g><g transform="translate(170,1720) rotate(80)"><rect x="-22" y="-80" width="44" height="160" rx="14" fill="#8a5a2b" stroke="#4a2a0a" stroke-width="5"/></g></svg>
      <div class="pf" id="pf1" style="left:600px;top:1040px">+0,25 €</div><div class="pf" id="pf2" style="left:790px;top:1190px">+0,25 €</div><div class="pf" id="pf3" style="left:600px;top:1330px">+0,25 €</div>
      <div id="p1" class="big H"><span class="c">URLAUB AM</span><br><span class="l">STRAND:</span></div>
      <div id="p2" class="neo li B">🍾 PFANDFLASCHEN SAMMELN!</div>""",
"""      const t = line("L5")[0], P = at("L5", "Pfandflaschen");
      tl.fromTo("#p1", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#btl", { y: -260, opacity: 0 }, { y: 0, opacity: 1, duration: .35, ease: "bounce.out" }, P - .3);
      tl.fromTo(".pf", { opacity: 0, scale: .3, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: .22, ease: "back.out(3)", stagger: .15 }, P);
      tl.fromTo("#p2", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, P - .05);
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s05-stage", { x, y, duration: .04, ease: "none" }, P + i * .04));""")

# s06 – Muschelkette → Kronkorken-Kette
scene("s06", COMMON7 + """
    #bg6 { position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, #ffcf6a, #e0631f 80%); }
    #k1 { font-size: 130px; } #k2 { font-size: 70px; }
    #mk { opacity: 1; } #kk { opacity: 0; } #s06-stage .art { transform: translateY(-260px); }""",
"""      <div id="bg6"></div>
      <svg class="art" viewBox="0 0 1080 1920"><path d="M240 1920 Q240 1500 420 1440 L420 1240 Q540 1290 660 1240 L660 1440 Q840 1500 840 1920 Z" fill="#f1c09a" stroke="#2a1b12" stroke-width="8"/><circle cx="540" cy="1000" r="230" fill="#f1c09a" stroke="#2a1b12" stroke-width="8"/><path d="M310 960 Q330 720 540 740 Q760 720 770 960 Q700 840 540 850 Q380 840 310 960Z" fill="#2a1b12"/><circle cx="470" cy="1010" r="14" fill="#111"/><circle cx="610" cy="1010" r="14" fill="#111"/><path d="M490 1110 Q540 1140 590 1110" stroke="#111" stroke-width="8" fill="none" stroke-linecap="round"/><rect x="420" y="980" width="100" height="56" rx="20" fill="#111" opacity=".85"/><rect x="560" y="980" width="100" height="56" rx="20" fill="#111" opacity=".85"/><path d="M520 1004 L560 1004" stroke="#111" stroke-width="8"/>
        <path d="M420 1400 Q540 1560 660 1400" stroke="#c9a46a" stroke-width="6" fill="none"/></svg>
      <svg class="art" id="mk" viewBox="0 0 1080 1920"><g transform="translate(445,1440)"><path d="M0 18 L-22 10 Q-26 0 -18 -2 Q-18 -12 -8 -10 Q0 -20 8 -10 Q18 -12 18 -2 Q26 0 22 10 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="3"/></g><g transform="translate(490,1490)"><path d="M0 18 L-22 10 Q-26 0 -18 -2 Q-18 -12 -8 -10 Q0 -20 8 -10 Q18 -12 18 -2 Q26 0 22 10 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="3"/></g><g transform="translate(540,1505) scale(1.6)"><path d="M0 18 L-22 10 Q-26 0 -18 -2 Q-18 -12 -8 -10 Q0 -20 8 -10 Q18 -12 18 -2 Q26 0 22 10 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="3"/></g><g transform="translate(590,1490)"><path d="M0 18 L-22 10 Q-26 0 -18 -2 Q-18 -12 -8 -10 Q0 -20 8 -10 Q18 -12 18 -2 Q26 0 22 10 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="3"/></g><g transform="translate(635,1440)"><path d="M0 18 L-22 10 Q-26 0 -18 -2 Q-18 -12 -8 -10 Q0 -20 8 -10 Q18 -12 18 -2 Q26 0 22 10 Z" fill="#ffc7b2" stroke="#e8467c" stroke-width="3"/></g></svg>
      <svg class="art" id="kk" viewBox="0 0 1080 1920"><g fill="#d9d9d9" stroke="#777" stroke-width="5"><circle cx="445" cy="1440" r="26"/><circle cx="490" cy="1490" r="26"/><circle cx="590" cy="1490" r="26"/><circle cx="635" cy="1440" r="26"/></g><circle cx="540" cy="1510" r="40" fill="#e8433c" stroke="#8a1a1a" stroke-width="6"/><circle cx="540" cy="1510" r="22" fill="none" stroke="#fff" stroke-width="5"/><g stroke="#fff" stroke-width="6" stroke-linecap="round"><path d="M700 1400 L730 1370"/><path d="M380 1400 L350 1370"/><path d="M720 1470 L760 1470"/></g></svg>
      <div id="k1" class="big H"><span class="p">MUSCHEL-</span><br><span class="p">KETTE?</span></div>
      <div id="k2" class="neo pk B">🍺 JETZT AUS KRONKORKEN!</div>""",
"""      const t = line("L6")[0], K = at("L6", "Kronkorken");
      tl.fromTo("#k1", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.to("#mk", { opacity: 0, scale: 0, transformOrigin: "540px 1480px", duration: .2, ease: "back.in(2)" }, K - .25);
      tl.fromTo("#kk", { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, transformOrigin: "540px 1480px", duration: .3, ease: "back.out(2.5)" }, K - .05);
      tl.fromTo("#k2", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, K - .05);
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s06-stage", { x, y, duration: .04, ease: "none" }, K + i * .04));""")

# s04 – Möwen-Streik
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
    .art { position: absolute; inset: 0; width: 1080px; height: 1920px; }
    .H { top: 220px; } .B { top: 1520px; }
    #m1 { font-size: 170px; } #m2 { font-size: 130px; }""",
"""      <svg class="art" id="gl4" viewBox="0 0 1080 1920"><defs><linearGradient id="g4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9aa6b2"/><stop offset=".5" stop-color="#c3cbd3"/><stop offset="1" stop-color="#d8d2c0"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#g4)"/><rect y="1250" width="1080" height="670" fill="#d6c79e"/><g transform="translate(220,1350) scale(1.3)"><rect x="-6" y="-170" width="12" height="150" fill="#8a5a2b"/><rect x="-90" y="-250" width="180" height="100" rx="8" fill="#fff" stroke="#2a1b12" stroke-width="6"/><text x="0" y="-210" font-family="Lilita One" font-size="38" fill="#e8433c" text-anchor="middle" textLength="150" lengthAdjust="spacingAndGlyphs">KEINE</text><text x="0" y="-170" font-family="Lilita One" font-size="38" fill="#e8433c" text-anchor="middle" textLength="150" lengthAdjust="spacingAndGlyphs">MUSCHELN</text><ellipse cx="0" cy="20" rx="70" ry="50" fill="#fff" stroke="#9aa" stroke-width="5"/><circle cx="40" cy="-30" r="34" fill="#fff" stroke="#9aa" stroke-width="5"/><path d="M70 -30 L110 -22 L70 -16Z" fill="#ffb400" stroke="#a87a00" stroke-width="3"/><circle cx="48" cy="-38" r="6" fill="#111"/><path d="M36 -52 L58 -44" stroke="#111" stroke-width="5"/><path d="M-70 10 Q-110 -20 -120 30 Q-90 20 -60 40" fill="#c9d1d6" stroke="#9aa" stroke-width="4"/><path d="M-20 68 L-20 100 M20 68 L20 100" stroke="#ffb400" stroke-width="7"/></g><g transform="translate(560,1300) scale(1.6)"><rect x="-6" y="-170" width="12" height="150" fill="#8a5a2b"/><rect x="-90" y="-250" width="180" height="100" rx="8" fill="#fff" stroke="#2a1b12" stroke-width="6"/><text x="0" y="-210" font-family="Lilita One" font-size="38" fill="#e8433c" text-anchor="middle" textLength="120" lengthAdjust="spacingAndGlyphs">KEIN</text><text x="0" y="-170" font-family="Lilita One" font-size="38" fill="#e8433c" text-anchor="middle" textLength="150" lengthAdjust="spacingAndGlyphs">FRIEDEN!</text><ellipse cx="0" cy="20" rx="70" ry="50" fill="#fff" stroke="#9aa" stroke-width="5"/><circle cx="40" cy="-30" r="34" fill="#fff" stroke="#9aa" stroke-width="5"/><path d="M70 -30 L110 -22 L70 -16Z" fill="#ffb400" stroke="#a87a00" stroke-width="3"/><circle cx="48" cy="-38" r="6" fill="#111"/><path d="M36 -52 L58 -44" stroke="#111" stroke-width="5"/><path d="M-70 10 Q-110 -20 -120 30 Q-90 20 -60 40" fill="#c9d1d6" stroke="#9aa" stroke-width="4"/><path d="M-20 68 L-20 100 M20 68 L20 100" stroke="#ffb400" stroke-width="7"/></g><g transform="translate(900,1380) scale(1.2)"><rect x="-6" y="-170" width="12" height="150" fill="#8a5a2b"/><rect x="-90" y="-250" width="180" height="100" rx="8" fill="#fff" stroke="#2a1b12" stroke-width="6"/><text x="0" y="-186" font-family="Lilita One" font-size="44" fill="#e8433c" text-anchor="middle" textLength="150" lengthAdjust="spacingAndGlyphs">STREIK!!</text><ellipse cx="0" cy="20" rx="70" ry="50" fill="#fff" stroke="#9aa" stroke-width="5"/><circle cx="40" cy="-30" r="34" fill="#fff" stroke="#9aa" stroke-width="5"/><path d="M70 -30 L110 -22 L70 -16Z" fill="#ffb400" stroke="#a87a00" stroke-width="3"/><circle cx="48" cy="-38" r="6" fill="#111"/><path d="M36 -52 L58 -44" stroke="#111" stroke-width="5"/><path d="M-70 10 Q-110 -20 -120 30 Q-90 20 -60 40" fill="#c9d1d6" stroke="#9aa" stroke-width="4"/><path d="M-20 68 L-20 100 M20 68 L20 100" stroke="#ffb400" stroke-width="7"/></g><text x="100" y="800" font-size="70" fill="#2a1b12">💢</text><text x="880" y="760" font-size="70" fill="#2a1b12">💢</text><text x="470" y="700" font-size="70" fill="#2a1b12">📣</text></svg>
      <div id="m1" class="big H">DIE <span class="p">MÖWEN</span></div>
      <div id="m2" class="neo pk B">✊ STREIKEN!</div>""",
"""      const t = line("L4")[0], S = at("L4", "streiken");
      tl.fromTo("#m1", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.to("#gl4", { y: -18, duration: .14, yoyo: true, repeat: 7, ease: "sine.inOut" }, t + .2);
      tl.fromTo("#m2", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, S - .05);
      tl.fromTo("#m2", { textShadow: "0 0 0px #ff3dbd" }, { textShadow: "0 0 80px #ff3dbd", duration: .12, yoyo: true, repeat: 3, ease: "none", immediateRender: false }, S + .2);""")



# s07 – WLAN-Passwort war Muschel123 → kein Internet
scene("s07", COMMON7 + """
    #bg7w { position: absolute; inset: 0; background: radial-gradient(circle at 50% 45%, #2b3a6b, #0c1030 75%); }
    #rt { position: absolute; left: 150px; top: 820px; width: 700px; height: 520px; }
    #wf { position: absolute; left: 380px; top: 560px; width: 240px; height: 240px; }
    #wx { position: absolute; left: 395px; top: 545px; font-size: 220px; opacity: 0; }
    #w1 { font-size: 112px; } #w2 { font-size: 80px; }""",
"""      <div id="bg7w"></div>
      <svg id="wf" viewBox="0 0 100 100"><path d="M10 40 Q50 5 90 40" stroke="#3ff0ff" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M24 55 Q50 32 76 55" stroke="#3ff0ff" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M37 69 Q50 58 63 69" stroke="#3ff0ff" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="50" cy="82" r="7" fill="#3ff0ff"/></svg>
      <div id="wx">❌</div>
      <svg id="rt" viewBox="0 0 700 520"><rect x="140" y="20" width="16" height="170" rx="8" fill="#222"/><rect x="544" y="20" width="16" height="170" rx="8" fill="#222"/><rect x="60" y="180" width="580" height="200" rx="30" fill="#f4f4f4" stroke="#2a1b12" stroke-width="8"/><circle class="ld" cx="130" cy="330" r="12" fill="#2ee86a"/><circle class="ld" cx="175" cy="330" r="12" fill="#2ee86a"/><circle class="ld" cx="220" cy="330" r="12" fill="#2ee86a"/><g transform="rotate(-4 450 250)"><rect x="300" y="200" width="300" height="100" rx="6" fill="#fff59a" stroke="#c9b400" stroke-width="4"/><text x="450" y="238" font-family="Inter" font-weight="800" font-size="24" fill="#333" text-anchor="middle" textLength="250" lengthAdjust="spacingAndGlyphs">WLAN-PASSWORT:</text><text x="450" y="282" font-family="Lilita One" font-size="38" fill="#e8433c" text-anchor="middle" textLength="250" lengthAdjust="spacingAndGlyphs">Muschel123</text></g><path id="strk" d="M310 270 L590 220" stroke="#e8433c" stroke-width="12" stroke-linecap="round" stroke-dasharray="300" stroke-dashoffset="300"/><rect x="40" y="380" width="620" height="140" fill="#6b4a2b"/></svg>
      <div id="w1" class="big H"><span class="c">WLAN-PASSWORT:</span><br><span class="p">MUSCHEL123</span></div>
      <div id="w2" class="neo pk B">📵 KEIN INTERNET!</div>""",
"""      const t = line("L7")[0], K = line("L7b")[0];
      tl.fromTo("#rt", { y: 500 }, { y: 0, duration: .4, ease: "back.out(1.6)" }, t - .1);
      tl.fromTo("#w1", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#wf", { opacity: .3 }, { opacity: 1, duration: .2, yoyo: true, repeat: 5 }, t + .2);
      tl.to("#strk", { strokeDashoffset: 0, duration: .25, ease: "power2.in" }, K - .1);
      tl.to(".ld", { fill: "#ff2d2d", duration: .05 }, K);
      tl.to("#wf", { opacity: .25, filter: "grayscale(1)", duration: .1 }, K);
      tl.fromTo("#wx", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, K);
      tl.fromTo("#w2", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, K - .05);
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s07-stage", { x, y, duration: .04, ease: "none" }, K + i * .04));""")

# s10 – Statt Meeresrauschen: 47 Sprachnachrichten von Mama
scene("s10", COMMON7 + """
    #bg10 { position: absolute; inset: 0; background: radial-gradient(circle at 50% 40%, #ff7ab8, #5a0e3a 75%); }
    #ph10 { position: absolute; left: 250px; top: 470px; width: 580px; height: 1000px; border-radius: 70px; background: #111; border: 14px solid #333; box-shadow: 0 30px 80px rgba(0,0,0,.5); overflow: hidden; }
    #ph10 .scr { position: absolute; inset: 16px; border-radius: 52px; background: #ece5dd; overflow: hidden; }
    #ph10 .bar { height: 120px; background: #fff; border-bottom: 2px solid #ddd; display: flex; align-items: center; padding: 0 30px; font: 800 36px Inter, sans-serif; color: #111; }
    #ph10 .vm { margin: 18px 26px; padding: 18px 22px; border-radius: 26px; background: #fff; display: flex; align-items: center; gap: 14px; font: 700 30px Inter, sans-serif; color: #555; width: 400px; opacity: 0; }
    #ph10 .vm b { font-size: 34px; } #ph10 .vm i { flex: 1; height: 26px; background: repeating-linear-gradient(90deg, #7a7a7a 0 5px, transparent 5px 11px); border-radius: 6px; }
    #cnt { position: absolute; left: 700px; top: 400px; width: 170px; height: 170px; border-radius: 50%; background: #ff2d2d; color: #fff; font: 900 80px/170px Inter, sans-serif; text-align: center; border: 8px solid #fff; opacity: 0; }
    #o1 { font-size: 96px; } #o2 { font-size: 66px; }""",
"""      <div id="bg10"></div>
      <div id="ph10"><div class="scr"><div class="bar">👩 Mama</div>
        <div class="vm"><b>▶</b><i></i>3:47</div><div class="vm"><b>▶</b><i></i>5:12</div><div class="vm"><b>▶</b><i></i>2:58</div><div class="vm"><b>▶</b><i></i>8:03</div><div class="vm"><b>▶</b><i></i>4:31</div><div class="vm"><b>▶</b><i></i>6:66</div></div></div>
      <div id="cnt">47</div>
      <div id="o1" class="big H"><span class="c">STATT MEERES-<br>RAUSCHEN:</span></div>
      <div id="o2" class="neo pk B">🎙️ 47 SPRACHNACHRICHTEN VON MAMA!</div>""",
"""      const t = line("L10")[0], M = at("L10", "Sprachnachrichten");
      tl.fromTo("#ph10", { y: 600, rotation: -8 }, { y: 0, rotation: 0, duration: .4, ease: "back.out(1.6)" }, t - .1);
      tl.fromTo("#o1", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#ph10 .vm", { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: .18, ease: "back.out(2)", stagger: .12 }, M - .5);
      tl.fromTo("#cnt", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, M);
      tl.to("#cnt", { scale: 1.15, duration: .12, yoyo: true, repeat: 5 }, M + .3);
      tl.fromTo("#o2", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, M - .05);
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s10-stage", { x, y, duration: .04, ease: "none" }, M + i * .04));""")

# s08 – Ortsschild: MUSCHEL-TAL → TAL
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
    .art { position: absolute; inset: 0; width: 1080px; height: 1920px; }
    .H { top: 220px; } .B { top: 1520px; }
    #tp { position: absolute; left: 186px; top: 770px; width: 500px; height: 150px; background: #9a9a9a; border: 6px solid #555; transform: rotate(-4deg); opacity: 0; }
    #t1 { font-size: 104px; } #t2 { position: absolute; left: 60px; right: 190px; top: 1240px; text-align: center; font: 400 300px "Lilita One"; color: #ff3dbd; -webkit-text-stroke: 16px #0a0418; paint-order: stroke fill; opacity: 0; }""",
"""      <svg class="art" viewBox="0 0 1080 1920"><defs><linearGradient id="g6" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#87cdee"/><stop offset=".5" stop-color="#b7e2f5"/><stop offset="1" stop-color="#e2f2e6"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#g6)"/><path d="M0 1150 Q270 980 540 1100 Q810 1220 1080 1050 L1080 1920 L0 1920Z" fill="#7fb86a"/><path d="M0 1280 Q300 1180 600 1300 Q850 1390 1080 1260 L1080 1920 L0 1920Z" fill="#6aa257"/><rect x="520" y="900" width="40" height="560" fill="#9a9a9a" stroke="#555" stroke-width="4"/><g transform="translate(540,840)"><rect x="-380" y="-130" width="760" height="260" rx="18" fill="#ffd23f" stroke="#2a1b12" stroke-width="14"/><text id="sgT" x="0" y="60" font-family="Lilita One" font-size="128" fill="#2a1b12" text-anchor="middle" textLength="690" lengthAdjust="spacingAndGlyphs">MUSCHEL-TAL</text></g></svg>
      <div id="tp"></div>
      <div id="t1" class="big H">UND <span class="p">MUSCHEL-TAL</span><br>HEISST NUR<br>NOCH …</div>
      <div id="t2">TAL.</div>""",
"""      const t = line("L8")[0], T = line("L8b")[0];
      tl.fromTo("#t1", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, t - .05);
      tl.fromTo("#tp", { opacity: 0, y: -300, rotation: -30 }, { opacity: 1, y: 0, rotation: -4, duration: .3, ease: "power3.in" }, T - .3);
      tl.fromTo("#t2", { opacity: 0, scale: 3.4, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: .26, ease: "back.out(2.2)" }, T - .02);
      [[24,-14],[-26,12],[20,16],[-16,-12],[10,8],[0,0]].forEach(([x, y], i) => tl.to("#s08-stage", { x, y, duration: .04, ease: "none" }, T + i * .04));""", blur=False)

