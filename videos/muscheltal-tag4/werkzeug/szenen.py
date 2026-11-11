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
BIG = """.big { position: absolute; left: 60px; right: 60px; margin: 0 auto; text-align: center; padding: 10px 26px 20px; border-radius: 36px; color: #fff; font-family: "Lilita One", sans-serif; line-height: 1; box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3); }"""
CMT = """.cmt { position: absolute; left: 140px; width: 800px; border-radius: 30px; padding: 8px; background: linear-gradient(135deg, #5fe0ff, #ff7ac0); box-shadow: 0 14px 30px rgba(0,0,0,.45); transform: rotate(-1.5deg); }
    .cmt img { display: block; width: 100%; border-radius: 23px; }"""

# s01 – Ich habe euch eine Insel gekauft
scene("s01", LILITA + "\n    " + PILL + "\n    " + BIG + "\n    " + PT + "\n" + FL + """
    #s01-h { top: 280px; font-size: 86px; background: #e8467c; transform: rotate(-2deg); }
    #s01-h b { color: #ffe14a; font-weight: 400; }
    #s01-al { top: 640px; font-size: 46px; background: #23285a; }
    #s01-c { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 640px; padding: 10px 44px 18px; border-radius: 36px; background: #fff; box-shadow: 0 0 0 8px #2a1b12, 0 14px 0 rgba(0,0,0,.3); text-align: center; font-family: "Inter", sans-serif; font-weight: 900; color: #2a1b12; font-size: 44px; }
    #s01-c b { display: block; font-family: "Lilita One", sans-serif; font-weight: 400; font-size: 170px; line-height: 1; color: #2e9e5b; }""",
"""      <div id="s01-fl" class="fl" data-layout-ignore></div>
      <div id="s01-h" class="big">ICH HABE EUCH EINE <b>INSEL GEKAUFT!</b></div>
      <div id="s01-al" class="pl">🏠 Am Anfang: nur ich – ganz allein</div>
      <div id="s01-c"><b id="s01-n">1</b>Bewohner 🏝️</div>""" + drops("s01-p", 14, 5, 'le', 540, 760, "🎉", 520, 760)[0],
"""      const al = at("L1", "ganz"), je = at("L1", "jetzt"), le = at("L1", "Leute");
      tl.set("#s01-h", { opacity: 1 }, 0);
      tl.fromTo("#s01-h", { scale: 1.6 }, { scale: 1, duration: .35, ease: "back.out(2.4)" }, 0);
      tl.to("#s01-h", { scale: 1.05, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, .5);
      tl.fromTo("#s01-al", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, al - .3);
      tl.to("#s01-al", { opacity: 0, duration: .2 }, je - .2);
      tl.fromTo("#s01-c", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.4)" }, je - .1);
      count(tl, "#s01-n", 1, 702, je, le - je + .1, "", "", "power2.in");
      tl.fromTo("#s01-c", { scale: 1 }, { scale: 1.18, duration: .15, yoyo: true, repeat: 1, immediateRender: false }, le + .1);
      tl.fromTo("#s01-fl", { opacity: .8 }, { opacity: 0, duration: .35, immediateRender: false }, le + .1);
""" + drops("s01-p", 14, 5, 'le', 540, 760, "🎉", 520, 760)[1])

# s02 – größte Insel auf TikTok, ihr entscheidet, alles gebaut
scene("s02", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s02-h { top: 290px; font-size: 76px; background: #18a6b8; transform: rotate(-2deg); }
    #s02-e { top: 460px; font-size: 48px; background: #7b3fe0; }
    .s02-b { top: 300px; font-size: 52px; }
    #s02-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 430px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-5deg); font-size: 70px; white-space: nowrap; font-family: "Lilita One", sans-serif; }""",
"""      <div id="s02-h" class="big">🏆 DIE GRÖSSTE INSEL AUF TIKTOK</div>
      <div id="s02-e" class="pl">👑 Hier entscheidet ihr!</div>
      <div id="s02-b0" class="pl s02-b" style="background:#e8262f">🥙 Dönerbude</div>
      <div id="s02-b1" class="pl s02-b" style="background:#18a6b8">🍹 Strandbar</div>
      <div id="s02-b2" class="pl s02-b" style="background:#7b3fe0">🫐 Açaí-Stand</div>
      <div id="s02-b3" class="pl s02-b" style="background:#e2560c">🔧 Moped-Werkstatt</div>
      <div id="s02-b4" class="pl s02-b" style="background:#2e9e5b">🏖️ Strandvilla</div>
      <div id="s02-st" class="stamp" data-layout-ignore>✅ ALLES GEBAUT!</div>""",
"""      const gr = at("L2", "größte"), ih = at("L2", "ihr"), l3 = line("L3")[0], al = at("L3", "alles");
      tl.fromTo("#s02-h", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(1.8)" }, gr - .25);
      tl.fromTo("#s02-e", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, ih - .2);
      tl.to("#s02-e", { scale: 1.1, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut" }, ih + .2);
      tl.to(["#s02-h", "#s02-e"], { opacity: 0, y: -30, duration: .2 }, l3 - .2);
      ["Dönerbude", "Strandbar", "Açaí-Stand", "Moped-Werkstatt", "Strandvilla"].forEach((w, i) => { const t = at("L3", w);
        tl.fromTo("#s02-b" + i, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .22, ease: "back.out(2)" }, t - .25);
        if (i < 4) tl.to("#s02-b" + i, { opacity: 0, duration: .12 }, at("L3", ["Strandbar", "Açaí-Stand", "Moped-Werkstatt", "Strandvilla"][i]) - .3); });
      tl.to("#s02-b4", { opacity: 0, duration: .12 }, al - .2);
      tl.fromTo("#s02-st", { opacity: 0, scale: 2.8 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, al - .05);""")

# s03 – Bäckerei, Live-Verlosung, Spoiler
def col(names, w): return '<div id="s03-col">' + "".join(f'<div class="s03-r" id="s03-r{i}">@{n}</div>' for i, n in enumerate(names)) + "</div>"
scene("s03", LILITA + "\n    " + PILL + "\n    " + BIG + "\n    " + CF_CSS.replace("top: 700px", "top: 640px") + """
    #s03-t { top: 290px; font-size: 56px; background: #e2560c; }
    #s03-v { top: 390px; font-size: 40px; background: #fff; color: #e2560c; }
    #s03-fc { position: absolute; left: 150px; right: 150px; top: 470px; padding: 18px 22px 20px; border-radius: 28px; background: #1f1f1f; box-shadow: 0 0 0 4px #000, 0 12px 24px rgba(0,0,0,.4); display: flex; gap: 18px; font-family: "Inter", sans-serif; color: #fff; }
    #s03-fc .av { width: 70px; height: 70px; border-radius: 50%; background: url(assets/img/fab_avatar.png) center/cover; flex: none; }
    #s03-fc .nm { font-size: 24px; color: #a8a8a8; font-weight: 600; } #s03-fc .tx { font-size: 28px; line-height: 1.28; margin-top: 2px; }
    #s03-dim { position: absolute; inset: 0; background: rgba(10,12,40,.55); }
    #s03-lv { top: 290px; font-size: 50px; background: #e8262f; }
    #s03-box { position: absolute; left: 190px; width: 700px; top: 450px; height: 390px; border-radius: 34px; background: #fff; overflow: hidden; box-shadow: 0 0 0 7px #2a1b12, 0 0 0 14px #ffc93c, 0 0 0 19px #2a1b12, 0 18px 0 rgba(0,0,0,.35); }
    #s03-band { position: absolute; left: 0; right: 0; top: 130px; height: 130px; background: #fff3c4; border-top: 5px solid #ffc93c; border-bottom: 5px solid #ffc93c; }
    #s03-col { position: absolute; left: 0; right: 0; top: 0; }
    .s03-r { height: 130px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #23285a; white-space: nowrap; }
    #s03-sh { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,.95)); }
    #s03-st { left: 0; right: 120px; margin: 0 auto; width: fit-content; top: 880px; color: #e2560c; border-color: #e2560c; background: #fff; transform: rotate(-4deg); font-size: 56px; white-space: nowrap; }
    #s03-wn { top: 300px; font-size: 52px; background: #2e9e5b; }
    #s03-sp { top: 290px; font-size: 76px; background: #7b3fe0; transform: rotate(-2deg); }
    #s03-lk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 520px; padding: 14px 40px 18px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 7px #2a1b12; font-family: "Inter", sans-serif; font-weight: 900; font-size: 44px; color: #2a1b12; text-align: center; }
    #s03-lk b { display: block; font-size: 120px; line-height: 1.1; }""",
f"""      <div id="s03-t" class="pl">🥐 NEU: Fabiennes Bäckerei!</div>
      <div id="s03-v" class="pl">✅ Ihr habt abgestimmt</div>
      <div id="s03-fc"><div class="av"></div><div><div class="nm">Fabienne</div><div class="tx">Kann sehr gut Cookies und Zimtschnecken backen.</div></div></div>
      <div id="s03-dim"></div>
      <div id="s03-lv" class="pl">🔴 LIVE: Job in der Bäckerei!</div>
      <div id="s03-box"><div id="s03-band"></div>{col(NS, WI)}<div id="s03-sh" data-layout-ignore></div></div>
      <div id="s03-cfw"></div>
      <div id="s03-st" class="stamp" data-layout-ignore>🥐 NEU IM TEAM!</div>
      <div id="s03-wn" class="pl">🎉 @lona.js arbeitet in der Bäckerei!</div>
      <div id="s03-sp" class="big">🤫 SPOILER</div>
      <div id="s03-lk"><b>🔒</b>Job = Vorteil beim Spiel<br>bei 1.000 Followern!</div>""",
f"""      const fa = at("L4", "Fabienne"), ab = at("L4", "abgestimmt"), l5 = line("L5")[0], ba = at("L5", "Bäckerei"), TB = line("L6")[0] - .4, gl = at("L6", "Glückwunsch"), l7 = line("L7")[0], vo = at("L7", "Vorteil"), H = 130, N = {len(NS)}, W = {WI};
      tl.fromTo("#s03-t", {{ opacity: 0, scale: 2.6 }}, {{ opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }}, line("L4")[0]);
      tl.fromTo("#s03-v", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .25 }}, ab - .2);
      tl.fromTo("#s03-fc", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }}, fa - .2);
      tl.to(["#s03-t", "#s03-v", "#s03-fc"], {{ opacity: 0, duration: .2 }}, l5 - .2);
      tl.fromTo("#s03-dim", {{ opacity: 0 }}, {{ opacity: 1, duration: .3 }}, l5);
      tl.fromTo("#s03-lv", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }}, l5);
      tl.to("#s03-lv", {{ opacity: .4, duration: .2, yoyo: true, repeat: 7, ease: "steps(1)" }}, l5 + .4);
      tl.fromTo("#s03-box", {{ opacity: 0, scale: .5 }}, {{ opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }}, ba - .3);
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
    #s04-k { position: absolute; left: 70px; right: 70px; top: 450px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s04-k .row { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 38px; }
    #s04-k .row b { font-size: 70px; color: #e2560c; line-height: 1; } #s04-k .row span { font-size: 34px; color: #6b6f8a; }
    #s04-k .bar { height: 30px; border-radius: 15px; background: #ece4d8; margin-top: 12px; overflow: hidden; } #s04-k .bar i { display: block; height: 100%; width: 0; border-radius: 15px; background: linear-gradient(90deg, #ff6a1a, #ffb21a); }
    #s04-v { top: 300px; font-size: 46px; background: #18a6b8; }
    #s04-w1 { top: 400px; font-size: 44px; background: #fff; color: #2a1b12; } #s04-w2 { top: 490px; font-size: 44px; background: #fff; color: #2a1b12; }""",
"""      <div id="s04-n">🏝️ <b id="s04-nn">+0</b> neue Bewohner</div>
      <div id="s04-k"><div class="row"><div>🐚 Inselkasse</div><div><b id="s04-kn">0</b><span> / 2.000</span></div></div><div class="bar"><i id="s04-kb"></i></div><div class="row" style="font-size:30px;margin-top:8px"><div>🐾 fürs Tierheim Pfotenkuss</div></div></div>
      <div id="s04-v" class="pl">🏖️ Eingezogen in die Strandvilla</div>
      <div id="s04-w1" class="pl">🎉 @emiliamarie155</div>
      <div id="s04-w2" class="pl">🎉 @lea.3818730</div>""",
"""      const ne = at("L8", "29"), ka = at("L8", "Inselkasse"), em = at("L8", "Emilia");
      tl.fromTo("#s04-n", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, ne - .3);
      count(tl, "#s04-nn", 0, 29, ne - .1, .6, "+", "");
      tl.fromTo("#s04-k", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ka - .3);
      count(tl, "#s04-kn", 0, 635, ka, 1.0);
      tl.fromTo("#s04-kb", { width: "0%" }, { width: "31.75%", duration: 1.0, ease: "power2.out" }, ka);
      tl.to(["#s04-n", "#s04-k"], { opacity: 0, y: -30, duration: .25 }, em - .5);
      tl.fromTo("#s04-v", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, em - .3);
      tl.fromTo(["#s04-w1", "#s04-w2"], { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)", stagger: .2 }, em - .1);""")

# s05 – Abstimmung: Yacht für Marie
scene("s05", PILL + "\n    " + CMT + """
    #s05-t { top: 290px; font-size: 52px; background: #1f6fb8; }
    #s05-c { top: 400px; }
    #s05-y { position: absolute; left: 0; right: 0; margin: 0 auto; text-align: center; top: 640px; font-size: 220px; line-height: 1; }
    #s05-q { top: 880px; right: 120px; font-size: 40px; background: #e8467c; }
    #s05-vv { position: absolute; left: 110px; right: 230px; top: 980px; display: flex; gap: 24px; }
    #s05-vv div { flex: 1; text-align: center; padding: 14px 0 18px; border-radius: 26px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); }""",
"""      <div id="s05-t" class="pl">🛥️ Private Yacht für Marie?</div>
      <div id="s05-c" class="cmt"><img src="assets/img/marie_comment.jpg" alt=""></div>
      <div id="s05-y" data-layout-ignore>🛥️</div>
      <div id="s05-q" class="pl">🎉 Mit Partys an Bord!</div>
      <div id="s05-vv"><div style="background:#2e9e5b">✅ JA</div><div style="background:#e8262f">❌ NEIN</div></div>""",
"""      const ma = at("L9", "Marie"), pa = at("L9", "Partys"), so = at("L9", "Soll"), st = at("L9", "Stimmt");
      tl.fromTo("#s05-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, ma - .2);
      tl.fromTo("#s05-c", { opacity: 0, y: -40, scale: .85 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2)" }, ma);
      tl.fromTo("#s05-y", { opacity: 0, x: -700 }, { opacity: 1, x: 0, duration: .6, ease: "power2.out" }, at("L9", "Yacht") - .2);
      tl.to("#s05-y", { y: -14, rotation: -4, duration: .5, yoyo: true, repeat: 7, ease: "sine.inOut" }, at("L9", "Yacht") + .4);
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
"""      <div id="s06-h" class="big">🚀 ES GIBT KEINE GRENZEN!</div>
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
    #s07-btn { top: 400px; } #s07-hand { left: 690px; top: 450px; }""",
"""      <div id="s07-t" class="pl">👯 Markiert eure Freunde!</div>
      <div id="s07-btn" class="fbtn">+ Folgen<div id="s07-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s07-hand" class="fhand" data-layout-ignore>👆</div>""",
"""      const fr = at("L11", "Freunde"), fo = at("L11", "folgt");
      tl.fromTo("#s07-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, fr - .3);
      tl.fromTo("#s07-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .4);
      tl.fromTo("#s07-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .2);
      tl.to("#s07-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .1);
      tl.to("#s07-btn2", { opacity: 1, duration: .05 }, fo + .2);
      tl.fromTo("#s07-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .2);
      tl.to("#s07-hand", { opacity: 0, duration: .25 }, fo + .7);""", blur=False)
