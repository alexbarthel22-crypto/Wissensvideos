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

# s01 – Eilmeldung: Wal im Pool
sp_h, sp_js = drops("s01-d", 16, 11, 'po + .05', 540, 760, "💦", 480, 600)
scene("s01", LILITA + "\n    " + PILL + "\n    " + PT + """
    #s01-bar { position: absolute; left: 0; right: 0; top: 250px; height: 120px; background: #e8262f; display: flex; align-items: center; gap: 24px; padding: 0 40px; box-shadow: 0 8px 0 rgba(0,0,0,.25); }
    #s01-bar b { font-family: "Lilita One", sans-serif; font-size: 78px; color: #fff; letter-spacing: .02em; }
    #s01-live { padding: 4px 16px 6px; border-radius: 10px; background: #fff; color: #e8262f; font-family: "Inter", sans-serif; font-weight: 900; font-size: 36px; }
    #s01-tk { position: absolute; left: 0; right: 0; top: 1060px; height: 70px; background: #111; overflow: hidden; }
    #s01-tt { position: absolute; left: 1080px; top: 10px; white-space: nowrap; font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; color: #ffd23f; }
    #s01-w { position: absolute; left: 470px; top: 590px; font-size: 280px; line-height: 1; }""",
f"""      <div id="s01-bar"><span id="s01-live">● LIVE</span><b>EILMELDUNG</b></div>
      <div id="s01-w" data-layout-ignore>🐳</div>
      {sp_h}
      <div id="s01-tk" data-layout-ignore><div id="s01-tt">+++ WAL IM POOL +++ LUISE SPRACHLOS +++ BADEMEISTER GESUCHT +++ WAL IM POOL +++ LUISE SPRACHLOS +++</div></div>""",
"""      const wa = at("L1", "Wal"), po = at("L1", "Pool");
      tl.set("#s01-bar", { opacity: 1 }, 0);
      tl.fromTo("#s01-bar", { x: -1100 }, { x: 0, duration: .25, ease: "power3.out" }, 0);
      tl.to("#s01-live", { opacity: .2, duration: .25, yoyo: true, repeat: 15, ease: "steps(1)" }, .3);
      tl.fromTo("#s01-tt", { x: 0 }, { x: -2600, duration: 6, ease: "none" }, .2);
      tl.fromTo("#s01-w", { y: -1100, rotation: -40, scale: .8 }, { y: 0, rotation: 8, scale: 1, duration: po - wa + .1, ease: "power2.in" }, wa - .1);
      tl.to("#s01-w", { scaleY: .7, scaleX: 1.25, duration: .08, yoyo: true, repeat: 1 }, po);
      tl.to("#s01-w", { rotation: -6, y: -14, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, po + .3);
      tl.to("#s01-stage", { x: 16, duration: .04, yoyo: true, repeat: 9, ease: "none" }, po);
""" + sp_js, blur=False)

# s02 – Spaß!
scene("s02", LILITA + "\n    " + PILL + """
    #s02-w { position: absolute; left: 470px; top: 590px; font-size: 280px; line-height: 1; }
    #s02-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 420px; color: #e8262f; border-color: #e8262f; background: #fff; transform: rotate(-6deg); font-size: 90px; white-space: nowrap; font-family: "Lilita One", sans-serif; }
    #s02-p { top: 950px; font-size: 44px; background: #7b3fe0; }""",
"""      <div id="s02-w" data-layout-ignore>🐳</div>
      <div id="s02-st" class="stamp" data-layout-ignore>😅 SPASS!</div>
      <div id="s02-p" class="pl">…aber IHR entscheidet, was passiert!</div>""",
"""      const ok = at("L2", "Okay"), sp = at("L2", "Spaß"), ih = at("L2", "ihr");
      tl.set("#s02-w", { opacity: 1, rotation: 8 }, 0);
      tl.to("#s02-w", { y: -1400, rotation: 200, scale: .4, duration: .6, ease: "back.in(1.6)" }, sp + .1);
      tl.fromTo("#s02-st", { opacity: 0, scale: 2.8 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, sp - .05);
      tl.to("#s02-st", { opacity: 0, duration: .2 }, ih - .5);
      tl.fromTo("#s02-p", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, ih - .3);
      tl.to("#s02-p", { scale: 1.07, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, ih + .2);""", blur=False)

# s03 – verrückte Ideen
ch_h, ch_js = drops("s03-c", 14, 7, 'sc', 540, 700, "🍫", 420, 800)
scene("s03", LILITA + "\n    " + PILL + "\n    " + PT + """
    #s03-q { top: 290px; font-size: 48px; background: #7b3fe0; }
    .s03-g { position: absolute; left: 0; right: 0; margin: 0 auto; text-align: center; top: 560px; font-size: 300px; line-height: 1; opacity: 0; }
    .s03-l { top: 960px; font-size: 42px; }
    #s03-pz { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 880px; padding: 4px 22px 8px; border-radius: 12px; background: #1d4ed8; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; box-shadow: 0 0 0 4px #2a1b12; opacity: 0; }
    #s03-si { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 520px; font-size: 90px; opacity: 0; }
    #s03-cr { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 450px; font-size: 130px; opacity: 0; }
    #s03-gl { position: absolute; left: 290px; top: 480px; width: 500px; height: 500px; border-radius: 50%; background: radial-gradient(circle, rgba(255,215,90,.85), rgba(255,215,90,0) 65%); opacity: 0; }""",
f"""      <div id="s03-q" class="pl">💡 Eure verrückteste Idee?</div>
      <div id="s03-gl" data-layout-ignore></div>
      <div id="s03-g1" class="s03-g" data-layout-ignore>🌋</div>{ch_h}
      <div id="s03-g2" class="s03-g" data-layout-ignore>🐧</div><div id="s03-si" data-layout-ignore>🚨</div><div id="s03-pz" data-layout-ignore>POLIZEI</div>
      <div id="s03-g3" class="s03-g" data-layout-ignore>🗿</div><div id="s03-cr" data-layout-ignore>👑</div>
      <div id="s03-l1" class="pl s03-l" style="background:#e8262f">Schoko-Vulkan</div>
      <div id="s03-l2" class="pl s03-l" style="background:#1d4ed8">Pinguin-Polizist</div>
      <div id="s03-l3" class="pl s03-l" style="background:#d4a017">Bürgermeisterin-Statue</div>""",
"""      const vu = at("L3", "Vulkan"), sc = at("L3", "Schokolade"), pi = at("L3", "Pinguin"), bu = at("L3", "Bürgermeisterin"), rs = at("L3", "Riesen-Statue");
      tl.fromTo("#s03-q", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, line("L3")[0] - .2);
      tl.fromTo("#s03-g1", { opacity: 0, y: 500 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(1.8)" }, vu - .2);
      tl.fromTo("#s03-l1", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .25 }, vu);
      tl.to("#s03-g1", { x: 12, duration: .05, yoyo: true, repeat: 9, ease: "none" }, sc - .3);
      tl.to(["#s03-g1", "#s03-l1"], { opacity: 0, scale: .5, duration: .2 }, pi - .3);
      tl.fromTo("#s03-g2", { opacity: 1, x: 900, rotation: 20 }, { x: 0, rotation: 0, duration: .45, ease: "back.out(1.6)" }, pi - .2);
      tl.to("#s03-g2", { rotation: 10, duration: .15, yoyo: true, repeat: 7, ease: "sine.inOut" }, pi + .3);
      tl.fromTo(["#s03-pz", "#s03-si"], { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2.6)" }, pi + .25);
      tl.to("#s03-si", { opacity: .2, duration: .12, yoyo: true, repeat: 9, ease: "steps(1)" }, pi + .5);
      tl.fromTo("#s03-l2", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .25 }, pi + .1);
      tl.to(["#s03-g2", "#s03-pz", "#s03-si", "#s03-l2"], { opacity: 0, scale: .5, duration: .2 }, bu - .2);
      tl.fromTo("#s03-g3", { opacity: 1, y: 700, scale: .6 }, { y: 0, scale: 1.15, duration: .6, ease: "power2.out" }, rs - .5);
      tl.fromTo("#s03-cr", { opacity: 0, y: -400 }, { opacity: 1, y: 0, duration: .3, ease: "bounce.out" }, rs + .15);
      tl.fromTo("#s03-gl", { opacity: 0, scale: .5 }, { opacity: 1, scale: 1.1, duration: .4 }, rs);
      tl.fromTo("#s03-l3", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .25 }, bu);
""" + ch_js)

# s04 – Kein Witz: Ideen werden echt (Luises Pool)
scene("s04", PILL + """
    #s04-t { top: 290px; font-size: 46px; background: #2e9e5b; }
    #s04-c { position: absolute; left: 160px; width: 760px; top: 395px; border-radius: 30px; padding: 8px; background: linear-gradient(135deg, #5fe0ff, #ff7ac0); box-shadow: 0 14px 30px rgba(0,0,0,.45); transform: rotate(-1.5deg); }
    #s04-c img { display: block; width: 100%; border-radius: 23px; }
    #s04-r { position: absolute; left: 400px; top: 620px; width: 280px; height: 280px; border-radius: 50%; border: 12px solid #ffd23f; box-shadow: 0 0 40px 10px rgba(255,210,63,.9); opacity: 0; }
    #s04-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 930px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-5deg); font-size: 60px; white-space: nowrap; }""",
"""      <div id="s04-t" class="pl">🙌 Kein Witz: Eure Ideen werden echt!</div>
      <div id="s04-c"><img src="assets/img/luise_comment.jpg" alt=""></div>
      <div id="s04-r" data-layout-ignore></div>
      <div id="s04-st" class="stamp" data-layout-ignore>🏊 GEBAUT! (ohne Wal)</div>""",
"""      const ec = at("L4", "echt"), lu = at("L4", "Luise"), be = at("L4", "bekommen");
      tl.fromTo("#s04-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, line("L4")[0]);
      tl.fromTo("#s04-c", { opacity: 0, y: -40, scale: .85 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2)" }, lu - .2);
      tl.fromTo("#s04-r", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .14, yoyo: true, repeat: 9, ease: "none" }, at("L4", "Pool") - .1);
      tl.fromTo("#s04-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, be);""")

# s05 – Kommentiert!
scene("s05", LILITA + "\n    " + PILL + """
    #s05-h { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 290px; padding: 6px 40px 16px; border-radius: 30px; background: #fe2c55; color: #fff; font-family: "Lilita One", sans-serif; font-size: 84px; line-height: 1; white-space: nowrap; box-shadow: 0 0 0 7px #2a1b12, 0 14px 0 rgba(0,0,0,.3); transform: rotate(-3deg); }
    #s05-cm { position: absolute; left: 90px; right: 210px; top: 430px; padding: 22px 26px 26px; border-radius: 30px; background: #1f1f1f; box-shadow: 0 0 0 5px #000, 0 14px 26px rgba(0,0,0,.45); font-family: "Inter", sans-serif; color: #fff; display: flex; gap: 20px; }
    #s05-cm .av { width: 74px; height: 74px; border-radius: 50%; flex: none; background: linear-gradient(135deg, #ffd23f, #e8467c); display: grid; place-items: center; font-size: 40px; }
    #s05-cm .nm { font-size: 26px; color: #a8a8a8; font-weight: 600; } #s05-cm .tx { font-size: 36px; font-weight: 600; margin-top: 4px; min-height: 92px; line-height: 1.25; }
    #s05-cm .cu { display: inline-block; width: 4px; height: 38px; background: #fe2c55; vertical-align: -6px; margin-left: 3px; }
    #s05-g { top: 700px; font-size: 44px; background: #2e9e5b; }
    #s05-ar { position: absolute; left: 850px; top: 1230px; font-size: 110px; filter: drop-shadow(0 6px 0 rgba(0,0,0,.35)); }
    #s05-cb { position: absolute; left: 640px; top: 1085px; padding: 4px 18px 8px; border-radius: 999px; background: #fff; color: #fe2c55; font-family: "Inter", sans-serif; font-weight: 900; font-size: 30px; box-shadow: 0 0 0 4px #2a1b12; }""",
"""      <div id="s05-h">💬 KOMMENTIERT JETZT!</div>
      <div id="s05-cm"><div class="av">🐚</div><div><div class="nm">Du</div><div class="tx"><span id="s05-ty"></span><span class="cu" id="s05-cu"></span></div></div></div>
      <div id="s05-g" class="pl">🍀 Mit Glück im nächsten Video!</div>
      <div id="s05-cb" data-layout-ignore>Hier kommentieren</div>
      <div id="s05-ar" data-layout-ignore>👉</div>""",
"""      const ko = at("L5", "Kommentiert"), ne = at("L5", "nächsten");
      tl.fromTo("#s05-h", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, ko - .2);
      tl.to("#s05-h", { scale: 1.08, duration: .18, yoyo: true, repeat: 11, ease: "sine.inOut" }, ko + .2);
      tl.fromTo("#s05-cm", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ko + .2);
      const TXT = "Bitte wirklich einen Wal in Luises Pool 🐳😂", ty = document.getElementById("s05-ty"), o = { n: 0 };
      tl.to(o, { n: Array.from(TXT).length, duration: 1.8, ease: "none", onUpdate: () => { ty.textContent = Array.from(TXT).slice(0, Math.round(o.n)).join(""); } }, ko + .5);
      tl.to("#s05-cu", { opacity: 0, duration: .25, yoyo: true, repeat: 13, ease: "steps(1)" }, ko + .5);
      tl.fromTo("#s05-g", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, ne - .6);
      tl.fromTo(["#s05-ar", "#s05-cb"], { opacity: 0 }, { opacity: 1, duration: .25 }, ko + .3);
      tl.to("#s05-ar", { x: 40, duration: .3, yoyo: true, repeat: 11, ease: "sine.inOut" }, ko + .5);""")

# s06 – Folg mir, sonst zieht der Pinguin ein
scene("s06", PILL + "\n" + FOLLOW + """
    #s06-btn { top: 330px; } #s06-hand { left: 690px; top: 380px; }
    #s06-hu { top: 900px; font-size: 44px; background: #fff; color: #2a1b12; }
    #s06-p { position: absolute; left: 0; right: 0; margin: 0 auto; text-align: center; top: 600px; font-size: 230px; line-height: 1; }
    #s06-sb { position: absolute; left: 600px; top: 540px; padding: 8px 22px 12px; border-radius: 26px; background: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 44px; color: #2a1b12; box-shadow: 0 0 0 4px #2a1b12; }""",
"""      <div id="s06-btn" class="fbtn">+ Folgen<div id="s06-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s06-hu" class="pl">🏡 @DEIN_NAME</div>
      <div id="s06-p" data-layout-ignore>🐧</div>
      <div id="s06-sb" data-layout-ignore>MEINS! 😎</div>
      <div id="s06-hand" class="fhand" data-layout-ignore>👆</div>""",
"""      const fo = at("L6", "folg"), pi = at("L6", "Pinguin"), hu = at("L6", "Hütte"), cl = hu + 1.0;
      tl.fromTo("#s06-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .3);
      tl.fromTo("#s06-hu", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, fo);
      tl.fromTo("#s06-p", { opacity: 1, x: 800 }, { x: 0, duration: .8, ease: "power1.out" }, pi - .2);
      tl.to("#s06-p", { rotation: 12, duration: .1, yoyo: true, repeat: 7, ease: "none" }, pi - .2);
      tl.fromTo("#s06-sb", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, hu);
      tl.fromTo("#s06-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, cl - .4);
      tl.to("#s06-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, cl - .1);
      tl.to("#s06-btn2", { opacity: 1, duration: .05 }, cl);
      tl.fromTo("#s06-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, cl);
      tl.to(["#s06-p", "#s06-sb"], { y: -1300, x: 500, rotation: 540, duration: .7, ease: "power2.in" }, cl + .15);
      tl.to("#s06-hu", { backgroundColor: "#ffd23f", scale: 1.12, duration: .2, yoyo: true, repeat: 3 }, cl + .3);""", blur=False)
