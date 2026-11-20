import json
import sys
from pathlib import Path
D = Path(sys.argv[1]); LOGO = Path(sys.argv[2]).read_text().strip()
SHELL = '<svg viewBox="0 0 64 64"><path d="M32 47 L8.8 40.8 Q5.0 34.0 12.7 32.7 Q11.6 25.0 19.2 26.7 Q21.0 19.1 27.5 23.4 Q32.0 17.0 36.5 23.4 Q43.0 19.1 44.8 26.7 Q52.4 25.0 51.3 32.7 Q59.0 34.0 55.2 40.8 Z" fill="#ffc7b2" stroke="#2a1b12" stroke-width="3" stroke-linejoin="round"/><path d="M32 45L13.9 33.6M32 45L20.0 27.9M32 45L27.8 24.9M32 45L36.2 24.9M32 45L44.0 27.9M32 45L50.1 33.6" stroke="#c43d6b" stroke-width="2" stroke-linecap="round"/></svg>'
LILITA = '@font-face { font-family: "Lilita One"; src: url("assets/fonts/LilitaOne-Regular.woff2") format("woff2"); font-weight: 400; }'

V1 = """
    .stk { background: rgba(255,255,255,.94) !important; border: 10px solid #e8467c; color: #e8467c !important; text-shadow: none !important; box-shadow: 0 9px 0 rgba(0,0,0,.25) !important;
      font-family: "Inter", sans-serif !important; font-weight: 900; font-size: 76px !important; padding: 6px 30px 12px !important; border-radius: 40px !important; line-height: 1.05 !important; max-width: 900px; }
    .stk small { color: #2a1b12 !important; font-size: 36px !important; text-shadow: none !important; font-weight: 800; }
    .stk.bl { border-color: #2f7fe0; color: #2f7fe0 !important; } .stk.gr { border-color: #2fbf6a; color: #1f9a52 !important; } .stk.go { border-color: #ffd23f; color: #2a1b12 !important; background: #ffd23f !important; }
    #h4 { border-color: #7b4fe0; color: #7b4fe0 !important; background: rgba(255,255,255,.94) !important; }
    .gl { background: #7b4fe0 !important; backdrop-filter: none !important; -webkit-backdrop-filter: none !important; border-radius: 22px !important; box-shadow: 0 9px 0 rgba(0,0,0,.28) !important; padding: 8px 28px 12px !important; }
    .gl small { font: 900 24px Inter, sans-serif !important; letter-spacing: .15em !important; opacity: .9; }
    .gl b { font-size: 54px !important; }
    .ch6, #tg2, #fr8 { font-family: "Inter", sans-serif !important; font-weight: 900 !important; font-size: 50px !important; box-shadow: 0 9px 0 rgba(0,0,0,.28) !important; }
    #f2 { font-size: 48px !important; }"""

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

# s01 – Hook im Stil von Video 1: Strahlen, Glühen, Funkeln, Stempel „PASSIERT!“ und „KEINER?!“, Blitz + Konfetti
scene("s01", """
    #s01-rays { position: absolute; left: -260px; top: 160px; width: 1600px; height: 1600px; border-radius: 50%;
      background: repeating-conic-gradient(from 0deg, rgba(255,255,255,.20) 0deg 9deg, rgba(255,255,255,0) 9deg 22deg);
      -webkit-mask: radial-gradient(circle, #000 0%, #000 35%, transparent 70%); mask: radial-gradient(circle, #000 0%, #000 35%, transparent 70%); }
    #s01-glow { position: absolute; left: 140px; top: 560px; width: 800px; height: 520px; border-radius: 50%; background: radial-gradient(closest-side, rgba(255,214,90,.55), rgba(255,214,90,0)); }
    #s01-flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
    .stamp { position: absolute; padding: 6px 30px; border: 10px solid; border-radius: 40px; background: rgba(255,255,255,.94); font-family: "Inter", sans-serif; font-weight: 900; font-size: 84px; opacity: 0; }
    #st1 { left: 290px; top: 300px; color: #e8467c; border-color: #e8467c; transform: rotate(-9deg); font-size: 96px; }
    #st2 { left: 330px; top: 300px; color: #7b4fe0; border-color: #7b4fe0; transform: rotate(7deg); font-size: 92px; }
    .s01-cf { position: absolute; left: 530px; top: 820px; width: 18px; height: 28px; border-radius: 4px; }
    .s01-sp { position: absolute; width: 70px; height: 70px; }""",
"""      <div id="s01-glow"></div><div id="s01-rays"></div><div id="s01-cfw"></div>
      <svg class="s01-sp" style="left:120px;top:520px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#fff"/></svg>
      <svg class="s01-sp" style="left:860px;top:600px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#ffd23f"/></svg>
      <svg class="s01-sp" style="left:170px;top:1060px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#ffd23f"/></svg>
      <svg class="s01-sp" style="left:820px;top:1000px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#fff"/></svg>
      <div id="st1" class="stamp">PASSIERT!</div>
      <div id="st2" class="stamp">KEINER?! 😳</div>
      <div id="s01-flash"></div>""",
"""      const P = at("L1", "passiert"), K = at("L1b", "keiner"), cols = ["#ffd23f", "#e8467c", "#2fb3a0", "#fff", "#7b4fe0", "#ff7a59"], box = document.getElementById("s01-cfw");
      let sd = 21; const R = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
      tl.fromTo("#s01-rays", { rotation: 0, opacity: .75 }, { rotation: 75, opacity: .35, duration: C.__dur, ease: "none" }, 0);
      tl.fromTo("#s01-glow", { scale: .9, opacity: .8 }, { scale: 1.15, opacity: .4, duration: .45, yoyo: true, repeat: 5, ease: "sine.inOut" }, 0);
      tl.fromTo(".s01-sp", { scale: .2, opacity: 0, rotation: 0 }, { scale: 1.4, opacity: 1, rotation: 90, duration: .35, ease: "back.out(3)", stagger: .12, yoyo: true, repeat: 5 }, 0);
      tl.fromTo("#s01-flash", { opacity: .75 }, { opacity: 0, duration: .35, ease: "power2.out", immediateRender: false }, P);
      tl.fromTo("#st1", { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: .32, ease: "elastic.out(1.2, .4)" }, P - .03);
      tl.fromTo("#st1", { x: 0 }, { x: 12, duration: .04, yoyo: true, repeat: 7, ease: "none" }, P + .2);
      tl.to("#st1", { opacity: 0, scale: .6, rotation: 10, duration: .25, ease: "back.in(2)" }, K - .3);
      tl.fromTo("#st2", { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: .32, ease: "elastic.out(1.2, .4)" }, K - .03);
      tl.fromTo("#st2", { x: 0 }, { x: 12, duration: .04, yoyo: true, repeat: 7, ease: "none" }, K + .2);
      for (let k = 0; k < 46; k++) { const d = document.createElement("div"); d.className = "s01-cf"; d.style.background = cols[k % cols.length]; box.appendChild(d);
        const a = R() * Math.PI * 2, v = 380 + R() * 520, dx = Math.cos(a) * v, dy = Math.sin(a) * v * .8 - 260;
        tl.fromTo(d, { opacity: 0, x: 0, y: 0, rotation: 0, scale: .6 }, { opacity: 1, x: dx * .7, y: dy * .7, rotation: (R() - .5) * 720, scale: 1, duration: .45, ease: "power3.out" }, P + .02);
        tl.to(d, { x: dx, y: dy + 520, rotation: "+=" + Math.round((R() - .5) * 540), opacity: 0, duration: 1.1, ease: "power1.in" }, P + .47); }""")

# s02 – Hütten + Passanten: 790, Hier könntest DU wohnen, Folgen
scene("s02", GL + """
    .stk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; max-width: 1000px; top: 250px; padding: 14px 44px 26px; border-radius: 40px; font-family: "Lilita One", sans-serif; text-align: center; line-height: .95; color: #ffe14a; opacity: 0;
      background: linear-gradient(160deg, #ff3d7f, #ff7a2a); box-shadow: 0 0 0 9px #fff, 0 0 0 16px #2a1b12, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(255,90,60,.6); text-shadow: 0 7px 0 #8a1035; font-size: 120px; }
    .stk small { display: block; font-size: 52px; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.3); }
    .stk.bl { background: linear-gradient(160deg, #1f8ff0, #36d1dc); text-shadow: 0 7px 0 #0b3d7a; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0b2340, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(60,180,255,.7); }
    .stk.gr { background: linear-gradient(160deg, #22b36a, #8be04e); text-shadow: 0 7px 0 #0d5a2e; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0d3a20, 0 24px 0 rgba(0,0,0,.28); }
    .stk.go { background: linear-gradient(160deg, #ffd23f, #ff9a1a); color: #fff; text-shadow: 0 7px 0 #8a4a00; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #4a2a00, 0 24px 0 rgba(0,0,0,.28), 0 0 90px rgba(255,200,60,.8); }
    #n2 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 240px; text-align: center; font-family: "Lilita One", sans-serif; opacity: 0; }
    #n2 b { display: block; font-weight: 400; font-size: 270px; line-height: .9; color: #ffe14a; text-shadow: 0 6px 0 #ff9a1a, 0 12px 0 #e8601a, 0 18px 0 #8a3510, 0 26px 40px rgba(0,0,0,.5); }
    #n2 small { display: inline-block; margin-top: 8px; font-size: 54px; color: #fff; background: #2a1b12; padding: 4px 30px 10px; border-radius: 30px; }
    #dk2 { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 30%, rgba(20,10,40,.55) 0%, rgba(10,5,30,.8) 70%); opacity: 0; }
    #ry2 { position: absolute; left: 540px; top: 360px; width: 1500px; height: 1500px; margin: -750px; border-radius: 50%; opacity: 0;
      background: repeating-conic-gradient(rgba(255,225,74,.7) 0deg 8deg, rgba(255,225,74,0) 8deg 20deg); -webkit-mask: radial-gradient(circle, #000 12%, transparent 62%); mask: radial-gradient(circle, #000 12%, transparent 62%); }
    #gl2 { position: absolute; left: 540px; top: 340px; width: 700px; height: 700px; margin: -350px; border-radius: 50%; background: radial-gradient(circle, rgba(255,230,120,.75), rgba(255,200,60,0) 65%); opacity: 0; }
    .rg2 { position: absolute; left: 540px; top: 340px; width: 300px; height: 300px; margin: -150px; border-radius: 50%; border: 18px solid #ffe14a; opacity: 0; }
    .sp2 { position: absolute; font-size: 72px; opacity: 0; }
    .pt2 { position: absolute; font-size: 80px; line-height: 1; width: 80px; height: 80px; opacity: 0; }
    #tg2 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 680px; padding: 10px 34px 16px; border-radius: 34px; background: linear-gradient(160deg,#ff3d7f,#ff7ac0); color: #fff; font: 400 64px "Lilita One", sans-serif; box-shadow: 0 0 0 7px #fff, 0 12px 0 rgba(0,0,0,.3); opacity: 0; }
    #h2 { top: 250px; } #h2 small { font-size: 56px; }
    #f2 { position: absolute; left: 0; right: 0; margin: 0 auto; top: 620px; width: 440px; height: 112px; border-radius: 56px; background: #fe2c55; color: #fff; font: 800 54px/112px Inter, sans-serif; text-align: center; opacity: 0; box-shadow: 0 14px 30px rgba(0,0,0,.35); }""",
"""      <div id="dk2"></div><div id="ry2"></div><div id="gl2"></div><div class="rg2" id="rg0"></div><div class="rg2" id="rg1"></div><div class="rg2" id="rg2"></div>
      <div id="n2"><b id="n2n">0</b><small>BEWOHNER 🏠</small></div>
      <div id="tg2">1 Hütte = 1 echter Follower 💖</div>
      <div class="sp2" id="sq0" style="left:150px;top:230px">✨</div><div class="sp2" id="sq1" style="left:860px;top:250px">⭐</div><div class="sp2" id="sq2" style="left:110px;top:470px">⭐</div><div class="sp2" id="sq3" style="left:880px;top:480px">✨</div>
      """ + "".join(f'<div class="pt2" id="pq{i}" style="left:500px;top:300px">{e}</div>' for i, e in enumerate("🏠👥🎉🏠💖✨🏠👥🎉🏠💖✨🏠👥")) + """
      <div id="h2" class="stk"><small>Hier könntest auch</small>DU wohnen! 🏡</div>
      <div id="f2">+ Folgen</div>""",
"""      const t = line("L2")[0], H = line("L2b")[0], F = at("L2b", "Folg");
      tl.fromTo("#n2", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .45, ease: "back.out(2.4)" }, at("L2", "790") - .1);
      count(tl, "#n2n", 0, 790, at("L2", "790"), 1.1, "", "", "power2.out");
      const N = at("L2", "790"), E = N + 1.1, J = at("L2", "jede");
      tl.fromTo("#dk2", { opacity: 0 }, { opacity: 1, duration: .35 }, N - .15);
      tl.fromTo("#ry2", { opacity: 0, scale: .4, rotation: 0 }, { opacity: 1, scale: 1, rotation: 70, duration: 5, ease: "power1.out" }, N - .1);
      tl.fromTo("#gl2", { opacity: 0, scale: .5 }, { opacity: 1, scale: 1.2, duration: .5, ease: "power2.out" }, N);
      tl.to("#gl2", { opacity: .55, scale: 1, duration: .35, yoyo: true, repeat: 7, ease: "sine.inOut" }, N + .5);
      ["#rg0", "#rg1", "#rg2"].forEach((q, i) => tl.fromTo(q, { opacity: 1, scale: .3 }, { opacity: 0, scale: 4.5, duration: .9, ease: "power3.out", immediateRender: false }, E + i * .15));
      tl.fromTo("#n2 b", { scale: 1 }, { scale: 1.25, duration: .14, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 60%" }, E);
      tl.fromTo("#n2 b", { textShadow: "0 6px 0 #ff9a1a, 0 12px 0 #e8601a, 0 18px 0 #8a3510, 0 0 0 rgba(255,230,120,0)" }, { textShadow: "0 6px 0 #ff9a1a, 0 12px 0 #e8601a, 0 18px 0 #8a3510, 0 0 80px rgba(255,230,120,1)", duration: .3, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false }, E + .1);
      [...Array(14).keys()].forEach(i => { const a = i / 14 * 6.283, r = 300 + (i % 3) * 120; tl.fromTo("#pq" + i, { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: Math.cos(a) * r, y: Math.sin(a) * r * .8, scale: 1.3, rotation: (i % 2 ? 1 : -1) * 180, opacity: 0, duration: 1.3, ease: "power3.out", immediateRender: false }, E + (i % 3) * .04); });
      ["#sq0", "#sq1", "#sq2", "#sq3"].forEach((q, i) => tl.fromTo(q, { opacity: 0, scale: .2, rotation: 0 }, { opacity: 1, scale: 1.3, rotation: 120, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, E + .1 + i * .12));
      tl.fromTo("#tg2", { opacity: 0, scale: .4, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: .4, ease: "back.out(2.5)" }, J - .1);
      [[10,-6,-2],[-10,4,2],[6,4,-1],[0,0,0]].forEach(([x, y, r], i) => tl.to("#tg2", { x, y, rotation: r, duration: .05, ease: "none" }, J + .35 + i * .05));
      tl.to(["#dk2", "#ry2", "#gl2", "#tg2"], { opacity: 0, duration: .25 }, H - .25);
      tl.to("#n2", { opacity: 0, scale: .8, duration: .2, ease: "power2.in" }, H - .2);
      tl.fromTo("#h2", { opacity: 0, scale: 2.2, rotation: -10 }, { opacity: 1, scale: 1, rotation: -3, duration: .3, ease: "back.out(3)" }, H);
      [[12,-8,-1],[-14,6,-6],[10,8,-2],[-8,-6,-5],[0,0,-3]].forEach(([x, y, r], i) => tl.to("#h2", { x, y, rotation: r, duration: .05, ease: "none" }, H + .3 + i * .05));
      tl.fromTo("#f2", { opacity: 0, scale: .5 }, { opacity: 1, scale: 1, duration: .4, ease: "back.out(2.5)" }, F);
      tl.to("#f2", { scale: 1.08, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, F + .45);""")

# s03 – Wal
scene("s03", GL + """
    .stk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; max-width: 1000px; top: 250px; padding: 14px 44px 26px; border-radius: 40px; font-family: "Lilita One", sans-serif; text-align: center; line-height: .95; color: #ffe14a; opacity: 0;
      background: linear-gradient(160deg, #ff3d7f, #ff7a2a); box-shadow: 0 0 0 9px #fff, 0 0 0 16px #2a1b12, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(255,90,60,.6); text-shadow: 0 7px 0 #8a1035; font-size: 120px; }
    .stk small { display: block; font-size: 52px; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.3); }
    .stk.bl { background: linear-gradient(160deg, #1f8ff0, #36d1dc); text-shadow: 0 7px 0 #0b3d7a; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0b2340, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(60,180,255,.7); }
    .stk.gr { background: linear-gradient(160deg, #22b36a, #8be04e); text-shadow: 0 7px 0 #0d5a2e; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0d3a20, 0 24px 0 rgba(0,0,0,.28); }
    .stk.go { background: linear-gradient(160deg, #ffd23f, #ff9a1a); color: #fff; text-shadow: 0 7px 0 #8a4a00; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #4a2a00, 0 24px 0 rgba(0,0,0,.28), 0 0 90px rgba(255,200,60,.8); }
    #e3 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 600px; display: flex; gap: 22px; align-items: center; padding: 18px 34px 20px 20px; border-radius: 36px; background: #fff; box-shadow: 0 0 0 7px #ffd23f, 0 18px 40px rgba(0,0,0,.35); opacity: 0; }
    #e3 i { width: 96px; height: 96px; border-radius: 50%; background: linear-gradient(135deg,#36d1dc,#1f8ff0); display: grid; place-items: center; font-style: normal; font-size: 58px; }
    #e3 small { display: block; font: 800 28px Inter, sans-serif; color: #c08a00; letter-spacing: .2em; } #e3 b { font: 400 66px "Lilita One", sans-serif; color: #2a1b12; }""",
"""      <div id="w3" class="stk bl"><small>vor der Küste</small>🐋 WAL-ALARM!</div>""",
"""      const W = at("L3", "WAL");
      tl.fromTo("#w3", { opacity: 0, scale: 2.2, rotation: -10 }, { opacity: 1, scale: 1, rotation: -3, duration: .3, ease: "back.out(3)" }, W - .05);
      [[12,-8,-1],[-14,6,-6],[10,8,-2],[-8,-6,-5],[0,0,-3]].forEach(([x, y, r], i) => tl.to("#w3", { x, y, rotation: r, duration: .05, ease: "none" }, W + .3 + i * .05));""")

# s04 – Schildkröten-Wanderung
scene("s04", GL + """
    .stk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; max-width: 1000px; top: 250px; padding: 14px 44px 26px; border-radius: 40px; font-family: "Lilita One", sans-serif; text-align: center; line-height: .95; color: #ffe14a; opacity: 0;
      background: linear-gradient(160deg, #ff3d7f, #ff7a2a); box-shadow: 0 0 0 9px #fff, 0 0 0 16px #2a1b12, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(255,90,60,.6); text-shadow: 0 7px 0 #8a1035; font-size: 120px; }
    .stk small { display: block; font-size: 52px; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.3); }
    .stk.bl { background: linear-gradient(160deg, #1f8ff0, #36d1dc); text-shadow: 0 7px 0 #0b3d7a; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0b2340, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(60,180,255,.7); }
    .stk.gr { background: linear-gradient(160deg, #22b36a, #8be04e); text-shadow: 0 7px 0 #0d5a2e; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0d3a20, 0 24px 0 rgba(0,0,0,.28); }
    .stk.go { background: linear-gradient(160deg, #ffd23f, #ff9a1a); color: #fff; text-shadow: 0 7px 0 #8a4a00; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #4a2a00, 0 24px 0 rgba(0,0,0,.28), 0 0 90px rgba(255,200,60,.8); }""",
"""      <div id="t4" class="stk gr"><small>am Strand</small>🐢 Schildkröten-<br>Wanderung!</div>
      <div id="h4" class="stk" style="background:linear-gradient(160deg,#7b3dff,#ff3d7f);text-shadow:0 7px 0 #3a1070;font-size:96px"><small>🐋 + 🐢 merkt euch das …</small>WICHTIG<br>FÜRS SPIEL? 🤫</div>""",
"""      tl.fromTo("#t4", { opacity: 0, scale: 2.2, rotation: -10 }, { opacity: 1, scale: 1, rotation: -3, duration: .3, ease: "back.out(3)" }, at("L4", "Schildkröten") - .1);
      tl.to("#t4", { y: -10, duration: .5, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L4", "Schildkröten") + .4);
      tl.to("#t4", { opacity: 0, scale: .8, duration: .2 }, line("L4b")[0] - .2);
      tl.fromTo("#h4", { opacity: 0, scale: 2.2, rotation: -10 }, { opacity: 1, scale: 1, rotation: -3, duration: .3, ease: "back.out(3)" }, line("L4b")[0]);
      tl.to("#h4", { scale: 1.06, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L4b", "wichtig"));""")

# s05 – Freiluftkino
scene("s05", GL + """
    #k5 { top: 250px; } #k5 b { font-size: 84px; }
    .pc { position: absolute; font-size: 80px; opacity: 0; }""",
"""      <div id="k5" class="gl"><small>Fr &amp; Sa · 20–22 Uhr</small><b>🎬 Freiluftkino</b></div>
      <div class="pc" id="pc0" style="left:120px;top:560px">🍿</div><div class="pc" id="pc1" style="left:860px;top:600px">🍿</div><div class="pc" id="pc2" style="left:200px;top:1450px">🎞️</div><div class="pc" id="pc3" style="left:820px;top:1480px">🥤</div>""",
"""      const t = line("L5")[0], P = at("L5", "Popcorn");
      tl.fromTo("#k5", { opacity: 0, y: 30, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .45, ease: "power3.out" }, t - .1);
      ["#pc0", "#pc1", "#pc2", "#pc3"].forEach((q, i) => { tl.fromTo(q, { opacity: 0, scale: .3, rotation: -20 }, { opacity: 1, scale: 1, rotation: 0, duration: .35, ease: "back.out(2.5)" }, P - .1 + i * .12); tl.to(q, { y: -18, duration: .45, yoyo: true, repeat: 3, ease: "sine.inOut" }, P + .4 + i * .12); });""")

# s06 – Golden Pearl (neues Gebäude, nur „Minispiele“ und „Feiern“ – keine Glücksspiel-Wörter)
scene("s06", GL + """
    #dk6 { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 42%, rgba(40,20,70,.45), rgba(8,4,24,.88)); opacity: 0; }
    #gp { position: absolute; left: 140px; top: 330px; width: 800px; height: 760px; opacity: 0; }
    #gp .fa { position: absolute; left: 60px; right: 60px; bottom: 0; height: 430px; border-radius: 30px 30px 10px 10px; background: linear-gradient(180deg, #fff3c4, #f4c64a 45%, #c98a12); box-shadow: 0 0 0 8px #6b3f00, 0 0 120px rgba(255,210,80,.6); }
    #gp .ro { position: absolute; left: 20px; right: 20px; bottom: 420px; height: 70px; border-radius: 20px; background: linear-gradient(180deg,#ffe58a,#d69a18); box-shadow: 0 0 0 8px #6b3f00; }
    #gp .pe { position: absolute; left: 50%; bottom: 470px; width: 230px; height: 230px; margin-left: -115px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #ffffff, #f3eefc 35%, #d9cdee 65%, #a99ac8); box-shadow: 0 0 0 10px #ffd23f, 0 0 0 18px #6b3f00, 0 0 120px 30px rgba(255,255,255,.55); }
    #gp .sh { position: absolute; left: 50%; bottom: 455px; width: 320px; height: 120px; margin-left: -160px; border-radius: 160px 160px 20px 20px; background: #f4c64a; box-shadow: 0 0 0 8px #6b3f00; }
    #gp .sg { position: absolute; left: 90px; right: 90px; bottom: 300px; padding: 14px 0 20px; border-radius: 24px; background: #2a0e3a; text-align: center; font: 400 92px/1 "Lilita One", sans-serif; color: #ffe14a; text-shadow: 0 0 18px #ff9af0, 0 0 40px #ff3d7f; box-shadow: 0 0 0 6px #6b3f00, inset 0 0 30px rgba(255,61,127,.5); }
    #gp .dr { position: absolute; left: 50%; bottom: 0; width: 170px; height: 220px; margin-left: -85px; border-radius: 85px 85px 0 0; background: linear-gradient(180deg,#ff3d7f,#8a1035); box-shadow: 0 0 0 8px #6b3f00; }
    #gp .w { position: absolute; bottom: 70px; width: 110px; height: 150px; border-radius: 55px 55px 8px 8px; background: linear-gradient(180deg,#7fd0ff,#2a6fb0); box-shadow: 0 0 0 6px #6b3f00; }
    #gp .st { position: absolute; font-size: 64px; opacity: 0; }
    #nw6 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 250px; padding: 8px 40px 14px; border-radius: 30px; background: #ffd23f; color: #2a1b12; font: 400 80px "Lilita One", sans-serif; transform: rotate(-3deg); box-shadow: 0 0 0 8px #2a1b12, 0 12px 0 rgba(0,0,0,.3); opacity: 0; }
    .ch6 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; padding: 12px 40px 18px; border-radius: 40px; font: 400 70px "Lilita One", sans-serif; color: #fff; opacity: 0; box-shadow: 0 0 0 7px #fff, 0 14px 0 rgba(0,0,0,.3); }
    #c60 { top: 240px; background: linear-gradient(160deg,#22b36a,#8be04e); } #c61 { top: 365px; background: linear-gradient(160deg,#7b3dff,#ff3d7f); }""",
"""      <div id="nw6">✨ NEU AUF DER INSEL</div>
      <div id="c60" class="ch6">🎯 jede Menge Minispiele</div>
      <div id="c61" class="ch6">🎉 nachts: Party!</div>""",
"""      const t = line("L6")[0], G = at("L6", "Golden"), M = at("L6b", "jede"), N = at("L6b", "nachts");
      tl.fromTo("#nw6", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, t);
      tl.to("#nw6", { opacity: 0, duration: .2 }, M - .3);
      tl.fromTo("#c60", { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: .4, ease: "back.out(2)" }, M - .1);
      tl.fromTo("#c61", { opacity: 0, x: 200 }, { opacity: 1, x: 0, duration: .4, ease: "back.out(2)" }, N - .1);""")

# s07 – Live-Verlosung: Besitzer Kokos-Club → @kerem90025; nächste: Inhaber Golden Pearl
NAMES = ["limone233", "martha_smile", "anna_hahnlbichler", "hennah.ac", "jujo7624", "notrufhamburg.09077294", "the_real_sigma69420", "the_real_sigma69420", "el1naa_13", "mariee.24.03", "_amiesspamm", "..angrylittleprincess", "schneider56sn", "acelya.sahin2"]
scene("s07", GL + """
    .stk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; max-width: 1000px; top: 250px; padding: 14px 44px 26px; border-radius: 40px; font-family: "Lilita One", sans-serif; text-align: center; line-height: .95; color: #ffe14a; opacity: 0;
      background: linear-gradient(160deg, #ff3d7f, #ff7a2a); box-shadow: 0 0 0 9px #fff, 0 0 0 16px #2a1b12, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(255,90,60,.6); text-shadow: 0 7px 0 #8a1035; font-size: 120px; }
    .stk small { display: block; font-size: 52px; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.3); }
    .stk.bl { background: linear-gradient(160deg, #1f8ff0, #36d1dc); text-shadow: 0 7px 0 #0b3d7a; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0b2340, 0 24px 0 rgba(0,0,0,.28), 0 0 80px rgba(60,180,255,.7); }
    .stk.gr { background: linear-gradient(160deg, #22b36a, #8be04e); text-shadow: 0 7px 0 #0d5a2e; color: #fff; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #0d3a20, 0 24px 0 rgba(0,0,0,.28); }
    .stk.go { background: linear-gradient(160deg, #ffd23f, #ff9a1a); color: #fff; text-shadow: 0 7px 0 #8a4a00; box-shadow: 0 0 0 9px #fff, 0 0 0 16px #4a2a00, 0 24px 0 rgba(0,0,0,.28), 0 0 90px rgba(255,200,60,.8); }
    #l7 { top: 250px; } #l7 b { font-size: 70px; }
    #rl { position: absolute; left: 90px; right: 90px; top: 560px; height: 170px; border-radius: 40px; overflow: hidden; background: #fff; box-shadow: 0 0 0 9px #ffd23f, 0 0 0 16px #2a1b12, 0 20px 40px rgba(0,0,0,.4); opacity: 0; }
    #rl .r { position: absolute; left: 0; right: 0; top: 0; }
    #rl .r div { height: 170px; font: 400 76px/170px "Lilita One", sans-serif; color: #2a1b12; text-align: center; white-space: nowrap; }
    #wn { top: 520px; font-size: 104px; }
    #nx { top: 790px; } #nx b { font-size: 60px; }
    .pt { position: absolute; font-size: 84px; line-height: 1; width: 84px; height: 84px; opacity: 0; }""",
"""      <div id="l7" class="gl"><small>🔴 Live-Verlosung</small><b>Besitzer vom Kokos-Club</b></div>
      <div id="rl"><div class="r">""" + "".join(f"<div>@{n}</div>" for n in NAMES) + """<div>@kerem90025</div></div></div>
      <div id="wn" class="stk go"><small>🎁 Du gewinnst den Kokos-Club!</small>@kerem90025</div>
      <div id="nx" class="gl"><small>Nächste Folge · unter allen Followern</small><b>👑 Inhaber vom Golden Pearl</b></div>
      """ + "".join(f'<div class="pt" id="pc{i}" style="left:498px;top:620px">{e}</div>' for i, e in enumerate("🎉💖✨🥳🎊⭐🎉💖✨🥳🎊⭐")) + """""",
"""      const t = line("L7")[0], S = line("L7b")[0], W = line("L7c")[0], X = at("L7d", "Und");
      tl.fromTo("#l7", { opacity: 0, y: 30, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .45, ease: "power3.out" }, t - .1);
      tl.fromTo("#rl", { opacity: 0, scale: .7 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }, S - .4);
      tl.fromTo("#rl .r", { y: 0 }, { y: -170 * """ + str(len(NAMES)) + """, duration: W - S + .35, ease: "power3.inOut" }, S - .3);
      tl.to("#rl", { opacity: 0, scale: 1.2, duration: .2 }, W + .1);
      tl.fromTo("#wn", { opacity: 0, scale: 2.4, rotation: -10 }, { opacity: 1, scale: 1, rotation: -3, duration: .35, ease: "back.out(3)" }, W + .1);
      [[12,-8,-1],[-14,6,-6],[10,8,-2],[-8,-6,-5],[0,0,-3]].forEach(([x, y, r], i) => tl.to("#wn", { x, y, rotation: r, duration: .05, ease: "none" }, W + .1 + .3 + i * .05));
      [...Array(12).keys()].forEach(i => { const a = i / 12 * 6.283, r = 300 + (i % 3) * 120; tl.fromTo("#pc" + i, { x: 0, y: 0, scale: .3, opacity: 1, rotation: 0 }, { x: Math.cos(a) * r, y: Math.sin(a) * r * .9, scale: 1.3, rotation: 200, opacity: 0, duration: 1.3, ease: "power3.out", immediateRender: false }, W + .15 + (i % 3) * .04); });
      tl.to("#l7", { opacity: 0, duration: .2 }, X - .2);
      tl.fromTo("#nx", { opacity: 0, y: 30, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .45, ease: "power3.out" }, X);
      tl.to("#nx", { scale: 1.05, duration: .35, yoyo: true, repeat: 3, ease: "sine.inOut" }, X + .7);""")

# s08 – Spiel-Tests, Start bei 1.000, Vorteile, Freunde einladen
scene("s08", GL + """
    #g8 { top: 240px; } #g8 b { font-size: 76px; }
    #pb { position: absolute; left: 110px; right: 110px; top: 480px; opacity: 0; font-family: "Lilita One", sans-serif; }
    #pb .tr { height: 70px; border-radius: 35px; background: rgba(0,0,0,.45); box-shadow: 0 0 0 6px #fff; overflow: hidden; }
    #pb .fi { height: 100%; width: 0; border-radius: 35px; background: linear-gradient(90deg,#ffd23f,#ff7a2a); }
    #pb .lb { display: flex; justify-content: space-between; margin-top: 10px; font-size: 48px; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.45); }
    .ck { position: absolute; left: 150px; padding: 10px 34px 16px 24px; border-radius: 34px; background: #fff; font: 400 62px "Lilita One", sans-serif; color: #2a1b12; opacity: 0; box-shadow: 0 0 0 6px #22b36a, 0 12px 0 rgba(0,0,0,.25); }
    .ck i { font-style: normal; color: #22b36a; margin-right: 12px; }
    #fr8 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 240px; padding: 14px 40px 20px; border-radius: 36px; background: linear-gradient(160deg,#ff3d7f,#ff7ac0); color: #fff; font: 400 64px/1.05 "Lilita One", sans-serif; text-align: center; box-shadow: 0 0 0 8px #fff, 0 0 0 14px #2a1b12; opacity: 0; }
    #fr8 span { color: #ffe14a; }""",
"""      <div id="g8" class="gl"><small>🧪 Tests laufen</small><b>🎮 Das Spiel Muschel-Tal</b></div>
      <div id="pb"><div class="tr"><div class="fi"></div></div><div class="lb"><span>790</span><span>Start bei 1.000 🚀</span></div></div>
      <div class="ck" id="ck0" style="top:640px"><i>✔</i>🌍 Welt erkunden</div>
      <div class="ck" id="ck1" style="top:770px"><i>✔</i>🐚 Muscheln sammeln</div>
      <div class="ck" id="ck2" style="top:900px"><i>✔</i>🛍️ Sachen kaufen</div>
      <div class="ck" id="ck3" style="top:1030px"><i>✔</i>👯 Freunde finden</div>
      <div id="fr8">📣 Sag's deinen Freunden!<br><span>Sei unter den ersten 1.000</span></div>""",
"""      const t = line("L8")[0], B = line("L8b")[0], F = line("L8c")[0];
      tl.fromTo("#g8", { opacity: 0, y: 30, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .45, ease: "power3.out" }, t - .1);
      tl.fromTo("#pb", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .35 }, B - .1);
      tl.fromTo("#pb .fi", { width: "0%" }, { width: "79%", duration: 1.2, ease: "power2.out" }, B + .1);
      [["Welt", 0], ["Muscheln", 1], ["Sachen", 2], ["Freunde", 3]].forEach(([w, i]) => tl.fromTo("#ck" + i, { opacity: 0, x: -120, scale: .8 }, { opacity: 1, x: 0, scale: 1, duration: .35, ease: "back.out(2.2)" }, at("L8b", w) - .1));
      tl.to("#g8", { opacity: 0, duration: .2 }, F - .25);
      tl.fromTo("#fr8", { opacity: 0, scale: .5 }, { opacity: 1, scale: 1, duration: .4, ease: "back.out(2.4)" }, F - .05);
      tl.to("#fr8", { scale: 1.05, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, F + .5);""")

# s07 – Folg mir
scene("s09", GL + """
    #t7 { top: 250px; } #t7 b { font-size: 76px; }
    #f7 { position: absolute; left: 0; right: 0; margin: 0 auto; top: 520px; width: 440px; height: 112px; border-radius: 56px; background: #fe2c55; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 50px; display: grid; place-items: center; box-shadow: 0 18px 40px rgba(254,44,85,.45); }""",
"""      <div id="t7" class="gl"><small>Deine Hütte wartet</small><b>@muscheltal</b></div>
      <div id="f7">+ Folgen</div>""",
"""      const t = line("L9")[0], fo = at("L9", "Folg");
      tl.fromTo("#t7", { opacity: 0, y: 40, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: .6, ease: "power3.out" }, t - .2);
      tl.fromTo("#f7", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .45, ease: "back.out(2)" }, fo);
      tl.to("#f7", { scale: 1.06, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, fo + .5);""", blur=False)
