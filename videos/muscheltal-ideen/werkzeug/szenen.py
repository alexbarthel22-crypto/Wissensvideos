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

# s01 – Ihr seid gefragt!
scene("s01", LILITA + "\n    " + PILL + """
    #s01-h { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 300px; padding: 6px 44px 18px; border-radius: 30px; background: #ffd23f; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 90px; line-height: 1; white-space: nowrap; box-shadow: 0 0 0 7px #2a1b12, 0 14px 0 rgba(0,0,0,.3); transform: rotate(-3deg); }
    #s01-q { top: 440px; font-size: 46px; background: #7b3fe0; }
    #s01-b { position: absolute; left: 470px; top: 600px; font-size: 150px; filter: drop-shadow(0 0 30px rgba(255,230,120,.95)); }
    .s01-x { position: absolute; font-family: "Lilita One", sans-serif; font-size: 120px; color: #fff; -webkit-text-stroke: 8px #2a1b12; paint-order: stroke fill; }""",
"""      <div id="s01-h">📣 IHR SEID GEFRAGT!</div>
      <div id="s01-q" class="pl">Eure verrückteste Idee für Muschel-Tal?</div>
      <div id="s01-b" data-layout-ignore>💡</div>
      <div class="s01-x" id="s01-x1" style="left:250px;top:640px" data-layout-ignore>?</div><div class="s01-x" id="s01-x2" style="left:760px;top:610px" data-layout-ignore>?</div>""",
"""      const ve = at("L1", "verrückteste");
      tl.set("#s01-h", { opacity: 1 }, 0);
      tl.fromTo("#s01-h", { scale: 1.25 }, { scale: 1, duration: .35, ease: "back.out(3)" }, 0);
      tl.to("#s01-h", { scale: 1.07, duration: .2, yoyo: true, repeat: 7, ease: "sine.inOut" }, .4);
      tl.fromTo("#s01-q", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ve - .3);
      tl.fromTo("#s01-b", { opacity: 0, scale: .2 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(3)" }, ve);
      tl.to("#s01-b", { filter: "drop-shadow(0 0 60px rgba(255,230,120,1))", scale: 1.1, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, ve + .4);
      [["#s01-x1", 0], ["#s01-x2", .15]].forEach(([e, d]) => { tl.fromTo(e, { opacity: 0, scale: 0, rotation: -30 }, { opacity: 1, scale: 1, rotation: 10, duration: .35, ease: "back.out(3)" }, ve + .2 + d);
        tl.to(e, { y: -20, rotation: -10, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, ve + .6 + d); });""", blur=True)

# s02 – Beispiele
scene("s02", PILL + """
    .s02-c { position: absolute; left: 110px; right: 230px; height: 150px; border-radius: 34px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.28); display: flex; align-items: center; gap: 26px; padding: 0 30px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 44px; color: #2a1b12; }
    .s02-c i { font-style: normal; font-size: 90px; }
    #s02-c1 { top: 300px; transform: rotate(-2deg); } #s02-c2 { top: 490px; transform: rotate(2deg); } #s02-c3 { top: 680px; transform: rotate(-1.5deg); }""",
"""      <div id="s02-c1" class="s02-c"><i>🎢</i>Achterbahn über die Insel</div>
      <div id="s02-c2" class="s02-c"><i>🌋</i>Vulkan aus Schokolade</div>
      <div id="s02-c3" class="s02-c"><i>🐠</i>Unterwasser-Kino</div>""",
"""      [["Achterbahn", 1], ["Vulkan", 2], ["Unterwasser-Kino", 3]].forEach(([w, i]) => { const t = at("L2", w);
        tl.fromTo("#s02-c" + i, { opacity: 0, scale: .3, x: i % 2 ? -200 : 200 }, { opacity: 1, scale: 1, x: 0, duration: .35, ease: "back.out(2.4)" }, t - .2);
        tl.to("#s02-c" + i + " i", { rotation: 360, duration: .6, ease: "power2.out" }, t); });""")

# s03 – Ideen werden echt (Luises Pool)
scene("s03", PILL + """
    #s03-t { top: 290px; font-size: 50px; background: #2e9e5b; }
    #s03-c { position: absolute; left: 160px; width: 760px; top: 395px; border-radius: 30px; padding: 8px; background: linear-gradient(135deg, #5fe0ff, #ff7ac0); box-shadow: 0 14px 30px rgba(0,0,0,.45); transform: rotate(-1.5deg); }
    #s03-c img { display: block; width: 100%; border-radius: 23px; }
    #s03-r { position: absolute; left: 400px; top: 620px; width: 280px; height: 280px; border-radius: 50%; border: 12px solid #ffd23f; box-shadow: 0 0 40px 10px rgba(255,210,63,.9); opacity: 0; }
    #s03-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 930px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-5deg); font-size: 60px; white-space: nowrap; }
    #s03-f { top: 930px; font-size: 40px; background: #e2560c; }""",
"""      <div id="s03-t" class="pl">✅ Eure Ideen werden echt!</div>
      <div id="s03-c"><img src="assets/img/luise_comment.jpg" alt=""></div>
      <div id="s03-r" data-layout-ignore></div>
      <div id="s03-st" class="stamp" data-layout-ignore>🏊 GEBAUT!</div>
      <div id="s03-f" class="pl">🥐 Bäckerei für @fabienne3692?</div>""",
"""      const ec = at("L3", "echt"), lu = at("L3", "Luise"), ha = at("L3", "hat"), fa = at("L3", "Fabienne");
      tl.fromTo("#s03-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, ec - .4);
      tl.fromTo("#s03-c", { opacity: 0, y: -40, scale: .85 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2)" }, lu - .2);
      tl.fromTo("#s03-r", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .14, yoyo: true, repeat: 9, ease: "none" }, at("L3", "Pool") - .1);
      tl.fromTo("#s03-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, ha);
      tl.to("#s03-st", { opacity: 0, duration: .2 }, fa - .3);
      tl.fromTo("#s03-f", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, fa - .1);""")

# s04 – Kommentiert jetzt!
scene("s04", LILITA + "\n    " + PILL + """
    #s04-h { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 290px; padding: 6px 40px 16px; border-radius: 30px; background: #fe2c55; color: #fff; font-family: "Lilita One", sans-serif; font-size: 84px; line-height: 1; white-space: nowrap; box-shadow: 0 0 0 7px #2a1b12, 0 14px 0 rgba(0,0,0,.3); transform: rotate(-3deg); }
    #s04-cm { position: absolute; left: 90px; right: 210px; top: 430px; padding: 22px 26px 26px; border-radius: 30px; background: #1f1f1f; box-shadow: 0 0 0 5px #000, 0 14px 26px rgba(0,0,0,.45); font-family: "Inter", sans-serif; color: #fff; display: flex; gap: 20px; }
    #s04-cm .av { width: 74px; height: 74px; border-radius: 50%; flex: none; background: linear-gradient(135deg, #ffd23f, #e8467c); display: grid; place-items: center; font-size: 40px; }
    #s04-cm .nm { font-size: 26px; color: #a8a8a8; font-weight: 600; } #s04-cm .tx { font-size: 36px; font-weight: 600; margin-top: 4px; min-height: 92px; line-height: 1.25; }
    #s04-cm .cu { display: inline-block; width: 4px; height: 38px; background: #fe2c55; vertical-align: -6px; margin-left: 3px; }
    #s04-g { top: 760px; font-size: 44px; background: #2e9e5b; }
    #s04-ar { position: absolute; left: 850px; top: 1230px; font-size: 110px; filter: drop-shadow(0 6px 0 rgba(0,0,0,.35)); }
    #s04-cb { position: absolute; left: 640px; top: 1085px; padding: 4px 18px 8px; border-radius: 999px; background: #fff; color: #fe2c55; font-family: "Inter", sans-serif; font-weight: 900; font-size: 30px; box-shadow: 0 0 0 4px #2a1b12; }""",
"""      <div id="s04-h">💬 KOMMENTIERT JETZT!</div>
      <div id="s04-cm"><div class="av">🐚</div><div><div class="nm">Du</div><div class="tx"><span id="s04-ty"></span><span class="cu" id="s04-cu"></span></div></div></div>
      <div id="s04-g" class="pl">🍀 Mit Glück im nächsten Video!</div>
      <div id="s04-cb" data-layout-ignore>Hier kommentieren</div>
      <div id="s04-ar" data-layout-ignore>👉</div>""",
"""      const ko = at("L4", "Kommentiert"), id = at("L4", "Idee"), gl = at("L4", "Glück");
      tl.fromTo("#s04-h", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, ko - .2);
      tl.to("#s04-h", { scale: 1.08, duration: .18, yoyo: true, repeat: 13, ease: "sine.inOut" }, ko + .2);
      tl.fromTo("#s04-cm", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, id - .4);
      const TXT = "Eine Riesen-Wasserrutsche vom Palast direkt ins Meer! 🌊", ty = document.getElementById("s04-ty"), o = { n: 0 };
      tl.to(o, { n: TXT.length, duration: 2.2, ease: "none", onUpdate: () => { ty.textContent = Array.from(TXT).slice(0, Math.round(o.n)).join(""); } }, id - .1);
      tl.to("#s04-cu", { opacity: 0, duration: .25, yoyo: true, repeat: 15, ease: "steps(1)" }, id);
      tl.fromTo("#s04-g", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, gl - .2);
      tl.to("#s04-g", { scale: 1.08, duration: .22, yoyo: true, repeat: 7, ease: "sine.inOut" }, gl + .3);
      tl.fromTo(["#s04-ar", "#s04-cb"], { opacity: 0 }, { opacity: 1, duration: .25 }, ko + .3);
      tl.to("#s04-ar", { x: 40, duration: .3, yoyo: true, repeat: 15, ease: "sine.inOut" }, ko + .5);""")

# s05 – Folg mir
scene("s05", PILL + "\n" + FOLLOW + """
    #s05-t { top: 300px; font-size: 50px; background: #18a6b8; }
    #s05-btn { top: 430px; } #s05-hand { left: 690px; top: 480px; }
    #s05-r { top: 600px; font-size: 42px; background: #2e9e5b; }""",
"""      <div id="s05-t" class="pl">🏝️ Folgen = einziehen!</div>
      <div id="s05-btn" class="fbtn">+ Folgen<div id="s05-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s05-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s05-r" class="pl">🏡 Deine Hütte mit deinem @Namen</div>""",
"""      const fo = at("L5", "folg"), ei = at("L5", "einzuziehen");
      tl.fromTo("#s05-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, fo - .4);
      tl.fromTo("#s05-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .3);
      tl.fromTo("#s05-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .1);
      tl.to("#s05-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .2);
      tl.to("#s05-btn2", { opacity: 1, duration: .05 }, fo + .3);
      tl.fromTo("#s05-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .3);
      tl.to("#s05-hand", { opacity: 0, duration: .25 }, fo + .8);
      tl.fromTo("#s05-r", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ei - .2);
      tl.to("#s05-r", { scale: 1.07, duration: .25, yoyo: true, repeat: 7, ease: "sine.inOut" }, ei + .3);""", blur=False)
