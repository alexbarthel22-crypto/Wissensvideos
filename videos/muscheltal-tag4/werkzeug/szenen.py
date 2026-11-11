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

NS = (D.parent / "werkzeug" / "slot.txt").read_text().split(); WI = NS.index("lona.js")
BIG = """.big { position: absolute; left: 0; right: 0; width: fit-content; max-width: 980px; white-space: nowrap; margin: 0 auto; text-align: center; padding: 10px 26px 20px; border-radius: 36px; color: #fff; font-family: "Lilita One", sans-serif; line-height: 1; box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3); }"""
CMT = """.cmt { position: absolute; left: 140px; width: 800px; border-radius: 30px; padding: 8px; background: linear-gradient(135deg, #5fe0ff, #ff7ac0); box-shadow: 0 14px 30px rgba(0,0,0,.45); transform: rotate(-1.5deg); }
    .cmt img { display: block; width: 100%; border-radius: 23px; }"""

# s01 – Ich habe euch eine Insel gekauft (Wörter fliegen ins Gesicht), leere Insel, Stadt wächst
AW = [("ALLEINE", 'at("L1", "alleine")', "<br>"), ("AUF", 'at("L1", "auf")', ""), ("EINER", 'at("L1", "meiner")', "<br>"), ("INSEL!", 'at("L1", "meiner") + .3', "")]
HW = [("ICH", "Ich", ""), ("HABE", "habe", "<br>"), ("EUCH", "euch", ""), ("EINE", "eine", "<br>"), ("INSEL", "Insel", "<br>"), ("GEKAUFT!", "gekauft", "")]
scene("s01", LILITA + "\n    " + PILL + "\n    " + PT + "\n" + FL + """
    #s01-ray { position: absolute; left: -460px; top: -80px; width: 2000px; height: 2000px; border-radius: 50%; background: repeating-conic-gradient(rgba(255,240,150,.42) 0 9deg, rgba(255,255,255,0) 9deg 22deg); -webkit-mask: radial-gradient(circle, #000 20%, transparent 62%); }
    #s01-hk { position: absolute; left: 10px; right: 10px; top: 540px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 178px; white-space: nowrap; line-height: 1.02; color: #fff; -webkit-text-stroke: 14px #2a1b12; paint-order: stroke fill; filter: drop-shadow(0 12px 0 rgba(0,0,0,.35)); }
    #s01-hk span { display: inline-block; margin: 0 .08em; transform-origin: 50% 60%; }
    #s01-hk span.y { color: #ffe14a; }
    #s01-hk i, #s01-al i { font-style: normal; display: inline-block; transform-origin: 50% 60%; }
    #s01-sad { position: absolute; inset: -80px; background: radial-gradient(ellipse at 50% 55%, rgba(30,34,48,0) 35%, rgba(20,22,34,.6) 100%); }
    .s01-rn { position: absolute; width: 4px; height: 70px; border-radius: 2px; background: rgba(210,225,240,.55); }
    #s01-al { position: absolute; left: 20px; right: 20px; top: 360px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 150px; line-height: 1.02; color: #dfe6f2; -webkit-text-stroke: 14px #1b1e2c; paint-order: stroke fill; filter: drop-shadow(0 12px 0 rgba(0,0,0,.4)); white-space: nowrap; }
    #s01-al span { display: inline-block; margin: 0 .06em; transform-origin: 50% 60%; opacity: 0; }
    #s01-c { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 600px; padding: 10px 44px 18px; border-radius: 36px; background: #fff; box-shadow: 0 0 0 8px #2a1b12, 0 14px 0 rgba(0,0,0,.3); text-align: center; font-family: "Inter", sans-serif; font-weight: 900; color: #2a1b12; font-size: 44px; }
    #s01-c b { display: block; font-family: "Lilita One", sans-serif; font-weight: 400; font-size: 170px; line-height: 1; color: #2e9e5b; }
    .s01-rg { position: absolute; left: 340px; top: 560px; width: 400px; height: 400px; border-radius: 50%; border: 14px solid #ffe14a; opacity: 0; }""",
"""      <div id="s01-ray" data-layout-ignore></div>
      <div id="s01-sad" data-layout-ignore></div>""" + "".join(f'<div class="s01-rn" id="s01-rn{i}" data-layout-ignore></div>' for i in range(40)) + """
      <div id="s01-fl" class="fl" data-layout-ignore></div>
      <div id="s01-hk">""" + "".join(f'<span id="s01-w{i}" class="{"y" if w in ("INSEL","GEKAUFT!") else ""}"><i id="s01-wi{i}">{w}</i></span>{br}' for i, (w, _, br) in enumerate(HW)) + """</div>
      <div id="s01-al">""" + "".join(f'<span id="s01-a{i}"><i id="s01-ai{i}">{w}</i></span>{br}' for i, (w, _, br) in enumerate(AW)) + """</div>
      <div class="s01-rg" id="s01-rg0" data-layout-ignore></div><div class="s01-rg" id="s01-rg1" data-layout-ignore></div><div class="s01-rg" id="s01-rg2" data-layout-ignore></div>
      <div id="s01-c"><b id="s01-n">1</b>Bewohner 🏝️</div>""" + drops("s01-i", 18, 17, '0', 540, 700, "🌴", 560, 760)[0] + drops("s01-g", 22, 19, '.35', 540, 720, "🐚", 600, 820)[0] + drops("s01-p", 22, 5, 'je + .1', 540, 760, "🏠", 560, 820)[0] + drops("s01-q", 16, 9, 'le', 540, 760, "✨", 520, 760)[0],
"""      const al = at("L1", "Am"), je = at("L1", "jetzt"), le = at("L1", "Bewohner"), ga = at("L1", "gekauft");
      """ + "\n      ".join(f'tl.set("#s01-w{i}", {{ opacity: 1 }}, 0);' for i, (_, k, _) in enumerate(HW)) + """
      """ + "\n      ".join(f'tl.to("#s01-wi{i}", {{ scale: {1.3 if i >= 4 else 1.7}, color: "#ffffff", textShadow: "0 0 50px rgba(255,230,80,1)", duration: .1, yoyo: true, repeat: 1, ease: "power2.out" }}, {"0.02" if i == 0 else f"at(\"L1\", \"{k}\") - .02"});' for i, (_, k, _) in enumerate(HW)) + """
      tl.to("#s01-hk", { scale: 1.12, duration: .1, yoyo: true, repeat: 3 }, ga + .05);
      tl.fromTo("#s01-ray", { rotation: 0, opacity: 1 }, { rotation: 60, duration: al, ease: "none" }, 0);
      tl.to("#s01-ray", { opacity: 0, duration: .2 }, al - .15);
      tl.fromTo("#s01-fl", { opacity: 1 }, { opacity: 0, duration: .3, immediateRender: false }, 0);
      tl.fromTo("#s01-fl", { opacity: .8 }, { opacity: 0, duration: .3, immediateRender: false }, ga);
      ["Ich", "habe", "euch", "eine", "Insel"].forEach((w, i) => tl.to("#s01-hk", { x: i % 2 ? -14 : 14, y: i % 2 ? 10 : -10, duration: .05, yoyo: true, repeat: 3, ease: "none" }, i ? at("L1", w) : 0.02));
      tl.to("#s01-hk", { x: 24, y: -12, duration: .04, yoyo: true, repeat: 9, ease: "none" }, ga);
      tl.to("#s01-stage", { x: 14, duration: .04, yoyo: true, repeat: 5, ease: "none" }, at("L1", "gekauft") + .1);
      tl.to("#s01-hk", { opacity: 0, scale: .7, y: -80, duration: .25 }, al - .15);
      { const R = rng(3); for (let i = 0; i < 40; i++) { const x = R() * 1080, d = .5 + R() * .4, st = al - .3 + R() * (je - al);
        document.getElementById("s01-rn" + i).style.left = x + "px";
        tl.fromTo("#s01-rn" + i, { y: -100, opacity: .9 }, { y: 2000, duration: d, ease: "none" }, st); } }
      tl.set("#s01-sad", { opacity: 0 }, 0); tl.set("#s01-sad", { opacity: 1 }, al - .1);
      tl.to("#s01-sad", { opacity: 0, duration: .5 }, je);
      """ + "\n      ".join(f'tl.fromTo("#s01-a{i}", {{ opacity: 0, scale: 6, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: .2, ease: "power3.in" }}, {k} - .12); tl.to("#s01-ai{i}", {{ scale: 1.45, color: "#ff6b6b", duration: .1, yoyo: true, repeat: 1 }}, {k} + .1);' for i, (_, k, _) in enumerate(AW)) + """
      tl.to("#s01-al", { x: 14, duration: .04, yoyo: true, repeat: 5, ease: "none" }, at("L1", "alleine") + .1);
      tl.to("#s01-al", { opacity: 0, scale: .6, duration: .2 }, je - .15);
      tl.fromTo("#s01-fl", { opacity: .85 }, { opacity: 0, duration: .4, immediateRender: false }, je);
      [0, 1, 2].forEach(i => tl.fromTo("#s01-rg" + i, { opacity: .9, scale: .2 }, { opacity: 0, scale: 3, duration: .7, ease: "power2.out", immediateRender: false }, je + i * .25));
      tl.fromTo("#s01-c", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.4)" }, je);
      count(tl, "#s01-n", 1, 702, je + .05, le - je + .1, "", "", "power2.in");
      tl.fromTo("#s01-c", { scale: 1 }, { scale: 1.18, duration: .15, yoyo: true, repeat: 1, immediateRender: false }, le + .1);
      tl.fromTo("#s01-fl", { opacity: .7 }, { opacity: 0, duration: .35, immediateRender: false }, le + .1);
""" + drops("s01-i", 18, 17, '0', 540, 700, "🌴", 560, 760)[1] + drops("s01-g", 22, 19, '.35', 540, 720, "🐚", 600, 820)[1] + drops("s01-p", 22, 5, 'je + .1', 540, 760, "🏠", 560, 820)[1] + drops("s01-q", 16, 9, 'le', 540, 760, "✨", 520, 760)[1])

# s02 – größte Insel auf TikTok, ihr entscheidet
scene("s02", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s02-h { top: 290px; font-size: 76px; background: #18a6b8; transform: rotate(-2deg); }
    #s02-e { top: 460px; font-size: 48px; background: #7b3fe0; }
    #s02-ihr { position: absolute; left: 0; right: 0; top: 560px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 300px; line-height: 1; color: #ffe14a; -webkit-text-stroke: 18px #2a1b12; paint-order: stroke fill; filter: drop-shadow(0 16px 0 rgba(0,0,0,.35)); opacity: 0; }""",
"""      <div id="s02-h" class="big">🏆 DIE GRÖSSTE<br>INSEL-WELT AUF TIKTOK</div>
      <div id="s02-ihr" data-layout-ignore>IHR!</div>
      <div id="s02-e" class="pl">👑 Hier entscheidet ihr!</div>""",
"""      const gr = at("L2", "größte"), ih = at("L2", "ihr");
      tl.fromTo("#s02-h", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(1.8)" }, gr - .25);
      tl.fromTo("#s02-e", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, ih - .2);
      tl.to("#s02-e", { scale: 1.1, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut" }, ih + .2);
      tl.fromTo("#s02-ihr", { opacity: 0, scale: 8, filter: "blur(14px) drop-shadow(0 16px 0 rgba(0,0,0,.35))" }, { opacity: 1, scale: 1, filter: "blur(0px) drop-shadow(0 16px 0 rgba(0,0,0,.35))", duration: .22, ease: "power3.in" }, ih - .12);
      tl.to("#s02-stage", { x: 16, duration: .04, yoyo: true, repeat: 7, ease: "none" }, ih + .1);
      tl.to("#s02-ihr", { scale: 1.12, duration: .15, yoyo: true, repeat: 3 }, ih + .15);
      tl.to("#s02-ihr", { opacity: 0, scale: .6, duration: .25 }, ih + .95);""")

# s0a – So einfach: folgen = eigene Hütte
scene("s0a", LILITA + "\n    " + PILL + "\n" + FOLLOW + "\n    " + PT + """
    #s0a-t { top: 290px; font-size: 54px; background: #2e9e5b; }
    #s0a-fr { position: absolute; left: 375px; top: 500px; width: 330px; height: 440px; border-radius: 34px; border: 9px dashed #ffe14a; box-shadow: 0 0 34px 6px rgba(255,225,74,.7); }
    #s0a-tag { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 640px; padding: 8px 26px 12px; border-radius: 22px; background: #ffe14a; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 64px; box-shadow: 0 0 0 6px #2a1b12; transform: rotate(-6deg); }
    #s0a-nm { display: none; top: 1090px; right: 120px; font-size: 34px; background: #7b3fe0; }
    #s0a-btn { top: 400px; } #s0a-hand { left: 690px; top: 450px; }
    #s0a-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1035px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 60px; white-space: nowrap; font-family: "Lilita One", sans-serif; }""",
"""      <div id="s0a-t" class="pl">✨ So einfach geht's</div>
      <div id="s0a-fr" data-layout-ignore></div>
      <div id="s0a-tag" data-layout-ignore>🔑 FREI</div>
      <div id="s0a-btn" class="fbtn">+ Folgen<div id="s0a-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s0a-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s0a-st" class="stamp" data-layout-ignore>🏠 DEINE HÜTTE!</div>
      <div id="s0a-nm" class="pl" data-layout-ignore>🏷️ mit deinem @Namen!</div>""" + drops("s0a-p", 14, 13, 'fo + .2', 540, 720, "🎉", 480, 700)[0],
"""      const ei = at("L2b", "einfach"), fo = at("L2b", "Folg"), hu = at("L2b", "Hütte");
      tl.fromTo("#s0a-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, ei - .3);
      tl.fromTo(["#s0a-fr", "#s0a-tag"], { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, line("L2b")[0]);
      tl.to("#s0a-fr", { boxShadow: "0 0 60px 18px rgba(255,225,74,1)", duration: .3, yoyo: true, repeat: 3 }, ei);
      tl.fromTo("#s0a-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .45);
      tl.fromTo("#s0a-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .35);
      tl.to("#s0a-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo - .05);
      tl.to("#s0a-btn2", { opacity: 1, duration: .05 }, fo + .05);
      tl.fromTo("#s0a-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .05);
      tl.to("#s0a-hand", { opacity: 0, duration: .2 }, fo + .5);
      tl.to("#s0a-tag", { opacity: 0, scale: .3, duration: .2 }, fo + .1);
      tl.to("#s0a-fr", { borderColor: "#2e9e5b", borderStyle: "solid", boxShadow: "0 0 50px 14px rgba(46,158,91,.9)", duration: .2 }, fo + .15);
      tl.fromTo("#s0a-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, hu - .2);
      tl.fromTo("#s0a-nm", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, at("L2b", "Namen") - .25);
""" + drops("s0a-p", 14, 13, 'fo + .2', 540, 720, "🎉", 480, 700)[1])

# s0b – Ihr wolltet … alles gebaut
scene("s0b", LILITA + "\n    " + PILL + """
    .s02-b { top: 300px; font-size: 52px; }
    #s02-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 430px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-5deg); font-size: 70px; white-space: nowrap; font-family: "Lilita One", sans-serif; }""",
"""      <div id="s02-b0" class="pl s02-b" style="background:#e8262f">🥙 Dönerbude</div>
      <div id="s02-b1" class="pl s02-b" style="background:#18a6b8">🍹 Strandbar</div>
      <div id="s02-b2" class="pl s02-b" style="background:#7b3fe0">🫐 Açaí-Stand</div>
      <div id="s02-b3" class="pl s02-b" style="background:#e2560c">🔧 Moped-Werkstatt</div>
      <div id="s02-b4" class="pl s02-b" style="background:#2e9e5b">🏖️ Strandvilla</div>
      <div id="s02-st" class="stamp" data-layout-ignore>✅ ALLES GEBAUT!</div>""",
"""      const al = at("L3", "alles");
      ["Dönerbude", "Strandbar", "Açaí-Stand", "Moped-Werkstatt", "Strandvilla"].forEach((w, i) => { const t = at("L3", w);
        tl.fromTo("#s02-b" + i, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .22, ease: "back.out(2)" }, t - .25);
        if (i < 4) tl.to("#s02-b" + i, { opacity: 0, duration: .12 }, at("L3", ["Strandbar", "Açaí-Stand", "Moped-Werkstatt", "Strandvilla"][i]) - .3); });
      tl.to("#s02-b4", { opacity: 0, duration: .12 }, al - .2);
      tl.fromTo("#s02-st", { opacity: 0, scale: 2.8 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, al - .05);""")

# s03 – Bäckerei, Live-Verlosung, Spoiler
def col(names, w): return '<div id="s03-col">' + "".join(f'<div class="s03-r" id="s03-r{i}">@{n}</div>' for i, n in enumerate(names)) + "</div>"
scene("s03", LILITA + "\n    " + PILL + "\n    " + BIG + "\n    " + CMT + "\n    " + CF_CSS.replace("top: 700px", "top: 640px") + """
    #s03-t { top: 290px; font-size: 56px; background: #e2560c; }
    #s03-v { top: 390px; font-size: 40px; background: #fff; color: #e2560c; }
    #s03-fc { top: 470px; left: 160px; width: 760px; }
    #s03-fc .av { width: 70px; height: 70px; border-radius: 50%; background: url(assets/img/fab_avatar.png) center/cover; flex: none; }
    #s03-fc .nm { font-size: 24px; color: #a8a8a8; font-weight: 600; } #s03-fc .tx { font-size: 28px; line-height: 1.28; margin-top: 2px; }
    #s03-gw { top: 1000px; right: 120px; font-size: 42px; background: #2e9e5b; }
    #s03-dim { position: absolute; inset: 0; background: rgba(10,12,40,.55); }
    #s03-lv { top: 290px; font-size: 50px; background: #e8262f; }
    #s03-box { position: absolute; left: 190px; width: 700px; top: 450px; height: 390px; border-radius: 34px; background: #fff; overflow: hidden; box-shadow: 0 0 0 7px #2a1b12, 0 0 0 14px #ffc93c, 0 0 0 19px #2a1b12, 0 18px 0 rgba(0,0,0,.35); }
    #s03-fv { position: absolute; left: 60px; width: 840px; top: 870px; text-align: center; white-space: nowrap; font-family: "Inter", sans-serif; font-weight: 800; font-size: 30px; color: #fff; text-shadow: 0 2px 6px rgba(0,0,0,.6); }
    #s03-band { position: absolute; left: 0; right: 0; top: 130px; height: 130px; background: #fff3c4; border-top: 5px solid #ffc93c; border-bottom: 5px solid #ffc93c; }
    #s03-col { position: absolute; left: 0; right: 0; top: 0; }
    .s03-r { height: 130px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #23285a; white-space: nowrap; }
    #s03-sh { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,.95)); }
    #s03-st { left: 0; right: 120px; margin: 0 auto; width: fit-content; top: 880px; color: #e2560c; border-color: #e2560c; background: #fff; transform: rotate(-4deg); font-size: 56px; white-space: nowrap; }
    #s03-wn { top: 300px; font-size: 52px; background: #2e9e5b; }
    #s03-sp { top: 290px; font-size: 76px; background: linear-gradient(135deg, #ff5ecf, #7b5cff); transform: rotate(-2deg); }
    #s03-lk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 520px; padding: 14px 40px 18px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 7px #2a1b12; font-family: "Inter", sans-serif; font-weight: 900; font-size: 44px; color: #2a1b12; text-align: center; }
    #s03-lk b { display: block; line-height: 1; }""",
f"""      <div id="s03-t" class="pl">🥐 NEU: Fabiennes Bäckerei!</div>
      <div id="s03-v" class="pl">✅ Ihr habt abgestimmt</div>
      <div id="s03-gw" class="pl">🎉 Glückwunsch, Fabienne!</div>
      <div id="s03-fc" class="cmt"><img src="assets/img/fab_comment.jpg" alt=""></div>
      <div id="s03-dim"></div>
      <div id="s03-lv" class="pl">🔴 LIVE: Job in der Bäckerei!</div>
      <div id="s03-box"><div id="s03-band"></div>{col(NS, WI)}<div id="s03-sh" data-layout-ignore></div></div>
      <div id="s03-fv">➕ Folgen, um bei der nächsten Verlosung teilzunehmen</div>
      <div id="s03-cfw"></div>
      <div id="s03-st" class="stamp" data-layout-ignore>🥐 NEU IM TEAM!</div>
      <div id="s03-wn" class="pl">🎉 @lona.js arbeitet in der Bäckerei!</div>
      <div id="s03-sp" class="big"><svg viewBox="0 0 64 64" width="90" height="90" style="vertical-align:-18px"><defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff5ecf"/><stop offset="1" stop-color="#7b5cff"/></linearGradient></defs><path d="M4 32 C14 14 50 14 60 32 C50 50 14 50 4 32 Z" fill="#fff" stroke="url(#sg)" stroke-width="5"/><circle cx="32" cy="32" r="12" fill="url(#sg)"/><circle cx="36" cy="27" r="4" fill="#fff"/><path d="M50 6 l2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2z" fill="#ffe14a"/></svg> SPOILER</div>
      <div id="s03-lk"><b><svg viewBox="0 0 64 64" width="120" height="120"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd84d"/><stop offset="1" stop-color="#ff8a00"/></linearGradient></defs><path d="M20 28 V20 a12 12 0 0 1 24 0 V28" fill="none" stroke="#2a1b12" stroke-width="6" stroke-linecap="round"/><rect x="12" y="27" width="40" height="30" rx="9" fill="url(#lg)" stroke="#2a1b12" stroke-width="4"/><circle cx="32" cy="40" r="4.5" fill="#2a1b12"/><rect x="30" y="42" width="4" height="8" rx="2" fill="#2a1b12"/><path d="M54 8 l2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2z" fill="#fff"/></svg></b>Job = Vorteil beim Spiel<br>bei 1.000 Followern!</div>""",
f"""      const fa = at("L4", "Fabienne"), ab = at("L4", "abgestimmt"), l5 = line("L5")[0], ba = at("L5", "Bäckerei"), TB = line("L6")[0] - .4, gl = at("L6", "Glückwunsch"), l7 = line("L7")[0], vo = at("L7", "Vorteil"), H = 130, N = {len(NS)}, W = {WI};
      tl.fromTo("#s03-t", {{ opacity: 0, scale: 2.6 }}, {{ opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }}, line("L4")[0]);
      tl.fromTo("#s03-v", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .25 }}, ab - .2);
      tl.fromTo("#s03-fc", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }}, fa - .2);
      tl.fromTo("#s03-gw", {{ opacity: 0, scale: .3 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }}, at("L4", "Glückwunsch") - .15);
      tl.to(["#s03-t", "#s03-v", "#s03-fc", "#s03-gw"], {{ opacity: 0, duration: .2 }}, l5 - .2);
      tl.fromTo("#s03-dim", {{ opacity: 0 }}, {{ opacity: 1, duration: .3 }}, l5);
      tl.fromTo("#s03-lv", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }}, l5);
      tl.to("#s03-lv", {{ opacity: .4, duration: .2, yoyo: true, repeat: 7, ease: "steps(1)" }}, l5 + .4);
      tl.fromTo("#s03-box", {{ opacity: 0, scale: .5 }}, {{ opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }}, ba - .3);
      tl.fromTo("#s03-fv", {{ opacity: 0 }}, {{ opacity: 1, duration: .3 }}, ba);
      tl.to("#s03-fv", {{ opacity: 0, duration: .2 }}, TB);
      tl.set("#s03-col", {{ y: -(N - 3) * H }}, 0);
      tl.fromTo("#s03-col", {{ y: -(N - 3) * H }}, {{ y: -(W - 1) * H, duration: TB - (ba + .7), ease: "power3.out", immediateRender: false }}, ba + .7);
      tl.fromTo("#s03-col", {{ filter: "blur(5px)" }}, {{ filter: "blur(0px)", duration: (TB - ba - .7) * .8, ease: "power2.in", immediateRender: false }}, ba + .7);
      tl.to("#s03-r" + W, {{ color: "#e2560c", scale: 1.15, duration: .2, ease: "back.out(3)" }}, TB);
      tl.to("#s03-band", {{ backgroundColor: "#ffd23f", duration: .15, yoyo: true, repeat: 5 }}, TB);
      tl.fromTo("#s03-st", {{ opacity: 0, scale: 2.6 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, TB + .2);
      """ + CONF_JS.replace("SEED", "44").replace("BOX", "s03-cfw").replace("T0", "TB") + """
      tl.to(["#s03-box", "#s03-st", "#s03-lv"], { opacity: 0, duration: .25 }, gl + 1.0);
      tl.fromTo("#s03-wn", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, gl + 1.1);
      tl.to(["#s03-wn", "#s03-dim"], { opacity: 0, duration: .25 }, l7 - .2);
      tl.fromTo("#s03-sp", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, l7 - .05);
      tl.fromTo("#s03-lk", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, at("L7", "Job") - .2);
      tl.fromTo("#s03-lk b", { rotation: 0 }, { rotation: 12, duration: .1, yoyo: true, repeat: 7, immediateRender: false }, vo);""", blur=False)

# s04 – Neu seit gestern: Bewohner, Kasse, Villa
scene("s04", PILL + """
    #s04-n { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 290px; padding: 10px 40px 16px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 7px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; font-weight: 900; font-size: 44px; color: #2a1b12; }
    #s04-n b { color: #2e9e5b; font-size: 80px; }
    #s04-k { position: absolute; left: 70px; right: 70px; top: 300px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s04-k .row { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 38px; }
    #s04-k .row b { font-size: 70px; color: #e2560c; line-height: 1; } #s04-k .row span { font-size: 34px; color: #6b6f8a; }
    #s04-k .bar { height: 30px; border-radius: 15px; background: #ece4d8; margin-top: 12px; overflow: hidden; } #s04-k .bar i { display: block; height: 100%; width: 0; border-radius: 15px; background: linear-gradient(90deg, #ff6a1a, #ffb21a); }
    #s04-v { top: 300px; font-size: 46px; background: #18a6b8; }
    #s04-w1 { top: 400px; font-size: 44px; background: #fff; color: #2a1b12; } #s04-w2 { top: 490px; font-size: 44px; background: #fff; color: #2a1b12; }""",
"""      <div id="s04-k"><div class="row"><div>🐚 Inselkasse</div><div><b id="s04-kn">0</b><span> / 2.000</span></div></div><div class="bar"><i id="s04-kb"></i></div><div class="row" style="font-size:30px;margin-top:8px"><div>🐾 fürs Tierheim Pfotenkuss</div></div></div>
      <div id="s04-v" class="pl">🏖️ Eingezogen in die Strandvilla</div>
      <div id="s04-w1" class="pl">🎉 @emiliamarie155</div>
      <div id="s04-w2" class="pl">🎉 @lea.3818730</div>""",
"""      const ka = at("L8", "Inselkasse"), em = at("L8", "Emilia");
      tl.fromTo("#s04-k", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ka - .3);
      count(tl, "#s04-kn", 0, 635, ka, 1.0);
      tl.fromTo("#s04-kb", { width: "0%" }, { width: "31.75%", duration: 1.0, ease: "power2.out" }, ka);
      tl.to("#s04-k", { opacity: 0, y: -30, duration: .25 }, em - .5);
      tl.fromTo("#s04-v", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, em - .3);
      tl.fromTo(["#s04-w1", "#s04-w2"], { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)", stagger: .2 }, em - .1);""")

# s05 – Abstimmung: Yacht für Marie
scene("s05", PILL + "\n    " + CMT + """
    #s05-t { top: 290px; font-size: 52px; background: #1f6fb8; }
    #s05-c { top: 400px; }
    #s05-y { position: absolute; left: 90px; top: 640px; width: 560px; height: 300px; }
    #s05-q { top: 960px; right: 120px; font-size: 40px; background: #e8467c; }
    #s05-vv { position: absolute; left: 110px; right: 230px; top: 1050px; display: flex; gap: 24px; }
    #s05-vv div { flex: 1; text-align: center; padding: 14px 0 18px; border-radius: 26px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); }""",
"""      <div id="s05-t" class="pl">🛥️ Private Yacht für @marie18034?</div>
      <div id="s05-c" class="cmt"><img src="assets/img/marie_comment.jpg" alt=""></div>
      <svg id="s05-y" viewBox="0 0 600 320" data-layout-ignore><g fill="none" stroke="#2a1b12" stroke-linejoin="round" stroke-linecap="round">
 <ellipse cx="300" cy="268" rx="290" ry="26" fill="#bfeefa" stroke="none" opacity=".7"/><path d="M40 262 q30 -12 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0" stroke="#fff" stroke-width="7" opacity=".9"/>
 <path d="M30 168 H500 Q570 168 552 196 L486 252 H82 Q48 252 30 168 Z" fill="#ffffff" stroke-width="6"/>
 <path d="M44 214 H528 L506 232 H70 Z" fill="#1f3f95" stroke="none"/><path d="M38 196 H544" stroke="#c9d6e6" stroke-width="4"/>
 <g fill="#123a4a" stroke="none"><circle cx="150" cy="190" r="6"/><circle cx="180" cy="190" r="6"/><circle cx="210" cy="190" r="6"/><circle cx="380" cy="190" r="6"/><circle cx="410" cy="190" r="6"/></g>
 <path d="M110 168 L130 112 H420 Q470 112 488 168 Z" fill="#f4f7fb" stroke-width="6"/>
 <path d="M150 158 L162 124 H300 V158 Z M314 158 V124 H412 Q440 124 456 158 Z" fill="#1d5f7a" stroke-width="4"/>
 <path d="M176 154 L186 128 H210 L200 154Z M330 154 V128 H352 V154Z" fill="#7fd6f0" stroke="none" opacity=".7"/>
 <path d="M190 112 L206 74 H360 Q392 74 404 112 Z" fill="#ffffff" stroke-width="6"/>
 <path d="M220 104 L230 82 H350 Q370 82 378 104 Z" fill="#1d5f7a" stroke-width="4"/>
 <path d="M250 74 V48 M250 48 H300 M300 48 V74" stroke-width="6"/><circle cx="275" cy="40" r="10" fill="#e9eef5" stroke-width="4"/>
 <path d="M96 168 V120" stroke-width="5"/><path d="M96 120 L130 130 L96 140 Z" fill="#e8467c" stroke-width="3"/>
 <path d="M96 122 Q170 70 250 50 Q330 40 420 70 Q470 90 520 140" stroke="#2a1b12" stroke-width="2.5"/>
 <g stroke="#2a1b12" stroke-width="2"><circle cx="130" cy="100" r="7" fill="#ffe14a"/><circle cx="170" cy="78" r="7" fill="#ff5ecf"/><circle cx="215" cy="60" r="7" fill="#5fe0ff"/><circle cx="330" cy="46" r="7" fill="#ffe14a"/><circle cx="380" cy="56" r="7" fill="#ff5ecf"/><circle cx="430" cy="74" r="7" fill="#5fe0ff"/><circle cx="480" cy="104" r="7" fill="#ffe14a"/></g>
 <g stroke-width="3"><circle cx="440" cy="98" r="9" fill="#f2c39a"/><path d="M440 108 V130 M430 116 L450 116 M428 100 L418 86 M452 100 L462 86" stroke-width="5"/><circle cx="160" cy="96" r="9" fill="#8a5a3c"/><path d="M160 106 V128 M150 112 L140 98 M170 112 L180 98" stroke-width="5"/></g>
 <text x="300" y="246" font-family="Lilita One" font-size="22" fill="#fff" stroke="none" text-anchor="middle">MARIE · MUSCHEL-TAL</text></g></svg>
      <div id="s05-q" class="pl">🎉 Mit Partys an Bord!</div>
      <div id="s05-vv"><div style="background:#2e9e5b">✅ JA</div><div style="background:#e8262f">❌ NEIN</div></div>""",
"""      const ma = at("L9", "Marie"), pa = at("L9", "Partys"), so = at("L9", "Soll"), st = at("L9", "Stimmt");
      tl.fromTo("#s05-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, ma - .2);
      tl.fromTo("#s05-c", { opacity: 0, y: -40, scale: .85 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2)" }, ma);
      tl.fromTo("#s05-y", { opacity: 0, x: -700 }, { opacity: 1, x: 0, duration: .6, ease: "power2.out" }, at("L9", "Yacht") - .2);
      tl.to("#s05-y", { y: -10, rotation: -2, duration: .6, yoyo: true, repeat: 7, ease: "sine.inOut" }, at("L9", "Yacht") + .4);
      tl.fromTo("#s05-q", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, pa - .2);
      tl.fromTo("#s05-vv div", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)", stagger: .12 }, so - .1);
      tl.to("#s05-vv div", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut", stagger: .1 }, st);""")

# s06 – Ihr entscheidet, keine Grenzen
scene("s06", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s06-h { top: 290px; font-size: 80px; background: #fe2c55; transform: rotate(-2deg); }
    #s06-cm { position: absolute; left: 90px; right: 210px; top: 480px; padding: 22px 26px 26px; border-radius: 30px; background: #1f1f1f; box-shadow: 0 0 0 5px #000, 0 14px 26px rgba(0,0,0,.45); font-family: "Inter", sans-serif; color: #fff; display: flex; gap: 20px; }
    #s06-cm .av { width: 74px; height: 74px; border-radius: 50%; flex: none; background: linear-gradient(135deg, #ffd23f, #e8467c); display: grid; place-items: center; font-size: 40px; }
    #s06-cm .nm { font-size: 26px; color: #a8a8a8; font-weight: 600; } #s06-cm .tx { font-size: 34px; font-weight: 600; margin-top: 4px; min-height: 86px; line-height: 1.25; }
    #s06-cm .cu { display: inline-block; width: 4px; height: 36px; background: #fe2c55; vertical-align: -6px; margin-left: 3px; }
    #s06-lk { margin-left: auto; text-align: center; font-weight: 800; font-size: 24px; color: #a8a8a8; flex: none; position: relative; }
    #s06-lk span { display: block; font-size: 42px; } #s06-h1 { position: absolute; left: 0; right: 0; top: 0; opacity: 0; }
    #s06-g { top: 800px; font-size: 42px; background: #e8262f; }
    #s06-ar { position: absolute; left: 850px; top: 1230px; font-size: 110px; filter: drop-shadow(0 6px 0 rgba(0,0,0,.35)); }
    #s06-cb { position: absolute; left: 640px; top: 1085px; padding: 4px 18px 8px; border-radius: 999px; background: #fff; color: #fe2c55; font-family: "Inter", sans-serif; font-weight: 900; font-size: 30px; box-shadow: 0 0 0 4px #2a1b12; }""",
"""      <div id="s06-h" class="big">🚀 ES GIBT KEINE<br>GRENZEN!</div>
      <div id="s06-cm"><div class="av">🐚</div><div><div class="nm">Du</div><div class="tx"><span id="s06-ty"></span><span class="cu" id="s06-cu"></span></div></div><div id="s06-lk"><span id="s06-h0">🤍</span><span id="s06-h1">❤️</span><b id="s06-ln">0</b></div></div>
      <div id="s06-g" class="pl">❤️ Meiste Likes = morgen im Video!</div>
      <div id="s06-cb" data-layout-ignore>Hier kommentieren</div>
      <div id="s06-ar" data-layout-ignore>👉</div>""",
"""      const ke = at("L10", "keine"), ve = at("L10", "verrückteste"), me = at("L10", "meisten"), mo = at("L10", "morgen");
      tl.fromTo("#s06-h", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, ke - .2);
      tl.to("#s06-h", { scale: 1.06, duration: .18, yoyo: true, repeat: 7, ease: "sine.inOut" }, ke + .3);
      tl.fromTo("#s06-cm", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ve - .3);
      const TXT = "Es gibt einen Matcha-Brunnen und jeden Tag regnet es Red Bull 🍵⚡", ty = document.getElementById("s06-ty"), o = { n: 0 };
      tl.to(o, { n: Array.from(TXT).length, duration: 2.2, ease: "none", onUpdate: () => { ty.textContent = Array.from(TXT).slice(0, Math.round(o.n)).join(""); } }, ve);
      tl.to("#s06-cu", { opacity: 0, duration: .25, yoyo: true, repeat: 13, ease: "steps(1)" }, ve);
      tl.set("#s06-h1", { opacity: 1 }, me);
      tl.fromTo("#s06-h1", { scale: 2.2 }, { scale: 1, duration: .35, ease: "back.out(3)", immediateRender: false }, me);
      count(tl, "#s06-ln", 0, 12480, me, 1.4, "", "", "power2.in");
      tl.fromTo("#s06-g", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, me - .2);
      tl.to("#s06-g", { scale: 1.07, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, mo);
      tl.fromTo(["#s06-ar", "#s06-cb"], { opacity: 0 }, { opacity: 1, duration: .25 }, ve);
      tl.to("#s06-ar", { x: 40, duration: .3, yoyo: true, repeat: 11, ease: "sine.inOut" }, ve + .2);""")

# s07 – Freunde markieren, folgen
scene("s07", PILL + "\n" + FOLLOW + """
    #s07-t { top: 290px; font-size: 50px; background: #e8467c; }
    #s07-box { position: absolute; left: 352px; top: 700px; width: 278px; height: 560px; border-radius: 40px; border: 9px solid #ffd23f; box-shadow: 0 0 30px 8px rgba(255,210,63,.85); opacity: 0; }
    #s07-hs { position: absolute; left: 215px; top: 930px; width: 130px; height: 130px; border-radius: 50%; background: #fff; display: grid; place-items: center; font-size: 78px; box-shadow: 0 0 0 7px #ffd23f, 0 0 0 12px #2a1b12; opacity: 0; }
    #s07-fr { position: absolute; left: 315px; top: 905px; width: 520px; height: 230px; border-radius: 36px; border: 9px solid #ffd23f; box-shadow: 0 0 30px 8px rgba(255,210,63,.85); opacity: 0; }
    #s07-hs2 { position: absolute; left: 515px; top: 845px; width: 120px; height: 120px; border-radius: 50%; background: #fff; display: grid; place-items: center; font-size: 72px; box-shadow: 0 0 0 7px #ffd23f, 0 0 0 12px #2a1b12; opacity: 0; }
    #s07-nb { top: 560px; font-size: 34px; background: #2e9e5b; }
    #s07-btn { top: 400px; } #s07-hand { left: 690px; top: 450px; }""",
"""      <div id="s07-t" class="pl">👯 Markiert eure Freunde!</div>
      <div id="s07-fr" data-layout-ignore></div><div id="s07-hs2" data-layout-ignore>🤝</div>
      <div id="s07-nb" class="pl">🤝 Nachbarn: @melie_js & @lisann.lmp</div>
      <div id="s07-btn" class="fbtn">+ Folgen<div id="s07-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s07-hand" class="fhand" data-layout-ignore>👆</div>""",
"""      const fr = at("L11", "Freunde"), fo = at("L11", "folgt");
      tl.fromTo("#s07-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, fr - .3);
      tl.fromTo("#s07-nb", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, fr);
      tl.fromTo("#s07-fr", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, fr);
      tl.fromTo("#s07-hs2", { opacity: 0, scale: .2, rotation: -30 }, { opacity: 1, scale: 1, rotation: 0, duration: .35, ease: "back.out(3)" }, fr + .1);
      tl.to("#s07-hs2", { scale: 1.12, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, fr + .5);
      tl.fromTo("#s07-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .4);
      tl.fromTo("#s07-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .2);
      tl.to("#s07-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .1);
      tl.to("#s07-btn2", { opacity: 1, duration: .05 }, fo + .2);
      tl.fromTo("#s07-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .2);
      tl.to("#s07-hand", { opacity: 0, duration: .25 }, fo + .7);""", blur=False)
