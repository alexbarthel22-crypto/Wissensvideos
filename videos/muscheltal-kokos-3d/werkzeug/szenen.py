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

PATHS = [("M330,1212 A280,268 0 1,1 750,1212", 1.0), ("M447,1244 L447,974 A93,95 0 0,1 633,974 L633,1244", .55), ("M767,870 A40,40 0 1,1 687,870 A40,40 0 1,1 767,870", .25),
         ("M540,716 C490,640 430,650 395,700", .2), ("M540,716 C590,640 650,650 685,700", .2), ("M200,1246 L880,1246", .3)]
SVG = '<svg id="s01-svg" width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0">' + "".join(
    f'<path id="s01-p{i}" d="{d}" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>' for i, (d, w) in enumerate(PATHS)) + "</svg>"
scene("s01", LILITA + "\n    " + PILL + """
    #s01-svg path { filter: drop-shadow(0 0 4px rgba(0,0,0,.45)); }
    #s01-pen { position: absolute; left: 0; top: 0; font-size: 110px; }
    #s01-hk { position: absolute; left: 0; right: 0; top: 280px; text-align: center; }
    .hk-l { display: table; margin: 14px auto 0; background: #ff2e7e; border-radius: 30px; padding: 2px 34px 12px; font-family: "Lilita One", sans-serif; font-size: 104px; line-height: 1.05; color: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 9px 0 rgba(0,0,0,.25); }
    .hk-w { display: inline-block; margin: 0 .08em; transform-origin: 50% 60%; position: relative; }
    #s01-stk { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 600px; color: #e8433c; border-color: #e8433c; background: #fff; transform: rotate(-6deg); font-size: 60px; white-space: nowrap; }
    #s01-d { top: 300px; font-size: 56px; background: #2e9e5b; }
    #s01-fl { position: absolute; inset: 0; background: #fff; opacity: 0; }""",
SVG + """
      <div id="s01-pen" data-layout-ignore>✏️</div>
      <div id="s01-hk"><div class="hk-l"><span class="hk-w" id="hw0">EINWOHNER</span></div><div class="hk-l"><span class="hk-w" id="hw1">FÜR</span><span class="hk-w" id="hw2">MEINE</span><span class="hk-w" id="hw3">INSEL</span></div></div>
      <div id="s01-stk" class="stamp" data-layout-ignore>🔎 GESUCHT!</div>
      <div id="s01-d" class="pl">🏠 Das könnte DEIN Haus sein!</div>
      <div id="s01-fl"></div>""",
"""      const ps = [...document.querySelectorAll("#s01-svg path")], WT = """ + str([w for _, w in PATHS]) + """, sum = WT.reduce((a, b) => a + b, 0);
      const T0 = .12, T1 = at("L2", "Das") - .15; let tt = T0;
      const pen = document.getElementById("s01-pen");
      ps.forEach((p, i) => { const len = p.getTotalLength(), d = (T1 - T0) * WT[i] / sum; p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
        const o = { v: 0 }; tl.to(o, { v: 1, duration: d, ease: "none", onUpdate: () => { p.style.strokeDashoffset = len * (1 - o.v); const pt = p.getPointAtLength(len * o.v); pen.style.transform = `translate(${pt.x - 8}px, ${pt.y - 102}px)`; } }, tt);
        tt += d; });
      tl.set(pen, { opacity: 1 }, 0); tl.to(pen, { opacity: 0, duration: .2 }, T1);
      tl.fromTo("#s01-fl", { opacity: 0 }, { opacity: .7, duration: .07, yoyo: true, repeat: 1, immediateRender: false }, T1 + .05);
      tl.to("#s01-svg", { opacity: 0, duration: .25 }, T1 + .05);
      const hk = ["Einwohner", "für", "meine", "Insel"];
      tl.set("#s01-hk", { opacity: 1 }, 0);
      hk.forEach((w, i) => { const t0 = Math.max(0, at("L1", w) - .03); tl.set("#hw" + i, { zIndex: 5 }, t0); tl.fromTo("#hw" + i, { scale: 1 }, { scale: .5, duration: .05, immediateRender: false }, t0); tl.to("#hw" + i, { scale: [1.3, 1.6, 1.6, 1.6][i], duration: .12, ease: "power2.out" }, t0 + .05); tl.to("#hw" + i, { scale: 1, duration: .2, ease: "back.out(2.5)" }, t0 + .17); });
      tl.to("#hw3", { color: "#ffd23f", duration: .05 }, at("L1", "Insel"));
      tl.fromTo("#s01-stk", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .16, ease: "power4.in" }, at("L1", "gesucht") - .1);
      tl.to(["#s01-hk", "#s01-stk"], { opacity: 0, y: -40, duration: .2 }, T1 - .05);
      tl.fromTo("#s01-d", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, T1 + .1);
      tl.to("#s01-d", { scale: 1.07, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, at("L2", "dein"));""", blur=False)

scene("s02", PILL + """
    #s02-t { top: 300px; font-size: 58px; background: #e2560c; }
    #s02-n { top: 420px; font-size: 48px; background: #fff; color: #2a1b12; }""",
"""      <div id="s02-t" class="pl">🏠 1 FOLLOWER = 1 HÜTTE</div>
      <div id="s02-n" class="pl">✍️ mit <span style="color:#e8467c">deinem @Namen</span></div>""",
"""      tl.fromTo("#s02-t", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.6)" }, at("L3", "Jeder") - .1);
      tl.fromTo("#s02-n", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, at("L3", "Namen") - .25);
      tl.to("#s02-n", { scale: 1.07, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L3", "Namen") + .2);""")

scene("s03", PILL + """
    #s03-t { top: 300px; font-size: 54px; background: #e8433c; }
    #s03-c { position: absolute; left: 0; right: 0; margin: 0 auto; top: 410px; width: fit-content; padding: 4px 36px 10px; border-radius: 36px; background: #fff; border: 6px solid #ff6a1a;
      font-family: "Inter", sans-serif; color: #2a1b12; font-weight: 900; font-size: 38px; display: flex; align-items: baseline; gap: 14px; box-shadow: 0 10px 0 rgba(0,40,80,.3); }
    #s03-c b { font-size: 92px; color: #e2560c; line-height: 1; }""",
"""      <div id="s03-t" class="pl">🔥 SCHON EINGEZOGEN</div>
      <div id="s03-c"><b id="s03-n">0</b>BEWOHNER</div>""",
"""      const he = at("L4", "heute");
      tl.fromTo("#s03-t", { opacity: 0, y: -50 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, he - .2);
      tl.fromTo("#s03-c", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, he);
      count(tl, "#s03-n", 0, 653, he + .1, 1.4, "", "", "power3.in");
      tl.fromTo("#s03-c", { scale: 1 }, { scale: 1.3, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, he + 1.5);""")

scene("s04", PILL + """
    #s04-t { top: 300px; font-size: 52px; background: #7b3fe0; }
    #s04-sheet { top: 420px; }""",
f"""      <div id="s04-t" class="pl">👯 WER WOHNT NEBEN DIR?</div>
      <div id="s04-sheet" class="tk"><div class="tk-h">Kommentare<b>×</b></div>
        {tk("s04-c1", "#e8467c", "?", "dein.name", "@dein.bestie zieh neben mich! 🏡", "1.204")}
      </div>""",
"""      const ne = at("L5", "neben"), ma = at("L5", "Markier");
      tl.fromTo("#s04-t", { opacity: 0, scale: .3, rotation: 8 }, { opacity: 1, scale: 1, rotation: 2, duration: .35, ease: "back.out(2.6)" }, ne - .2);
      tl.fromTo("#s04-sheet", { opacity: 0, y: 400 }, { opacity: 1, y: 0, duration: .45, ease: "power4.out" }, ma - .3);
      tl.fromTo("#s04-c1", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: .3, ease: "power3.out" }, ma);
      tkLike(tl, "#s04-c1", ma + .4, 1204, 1388, 1.2, 3);""")

scene("s05", PILL + "\n" + FOLLOW + """
    #s05-btn { top: 330px; } #s05-hand { left: 690px; top: 380px; }
    #s05-h { top: 480px; font-size: 64px; background: #fe2c55; }
    #s05-g { top: 600px; font-size: 44px; background: #2e9e5b; }""",
"""      <div id="s05-btn" class="fbtn">+ Folgen<div id="s05-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s05-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s05-h" class="pl">@muscheltal</div>
      <div id="s05-g" class="pl">🏠 Folgen = einziehen!</div>""",
"""      const fo = at("L6", "Folg"), ei = at("L6", "ein");
      tl.fromTo("#s05-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .5);
      tl.fromTo("#s05-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .3);
      tl.to("#s05-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo);
      tl.to("#s05-btn2", { opacity: 1, duration: .05 }, fo + .1);
      tl.fromTo("#s05-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .1);
      tl.to("#s05-hand", { opacity: 0, duration: .25 }, fo + .6);
      tl.fromTo("#s05-h", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, fo + .3);
      tl.fromTo("#s05-g", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, ei - .3);
      tl.to("#s05-g", { scale: 1.08, duration: .25, yoyo: true, repeat: 7, ease: "sine.inOut" }, ei + .2);""", blur=False)
