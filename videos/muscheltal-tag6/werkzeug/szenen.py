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

BIG = """.big { position: absolute; left: 0; right: 0; width: fit-content; max-width: 980px; white-space: nowrap; margin: 0 auto; text-align: center; padding: 10px 26px 20px; border-radius: 36px; color: #fff; font-family: "Lilita One", sans-serif; line-height: 1; box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3); }"""
CMT = """.cmt { position: absolute; left: 140px; width: 800px; border-radius: 30px; padding: 8px; background: linear-gradient(135deg, #5fe0ff, #ff7ac0); box-shadow: 0 14px 30px rgba(0,0,0,.45); transform: rotate(-1.5deg); }
    .cmt img { display: block; width: 100%; border-radius: 23px; }"""


NS = (D.parent / "werkzeug" / "slot.txt").read_text().split(); WI = NS.index("sklmq3")

# s01 – Hook im Stil von Tag 1: pinke Balken, Wörter springen groß hervor, Sticker „GEBAUT!“
QL = [[("AUF", "Auf"), ("DIESER", "dieser")], [("INSEL", "Insel"), ("LEBEN", "leben")], [("MEHR", "mehr"), ("TIERE", "Tiere")], [("ALS", "als"), ("MENSCHEN!", "Menschen")]]
QW = [w for ln in QL for w in ln]
YW = ("MEHR", "TIERE", "MENSCHEN!")
SP = [(110, 560, 46), (900, 600, 34), (70, 960, 30), (930, 1010, 44), (180, 1230, 38), (820, 1200, 30)]
scene("s01", LILITA + "\n    " + PT + "\n" + FL + """
    #s01-ray { position: absolute; left: -460px; top: 300px; width: 2000px; height: 2000px; border-radius: 50%; background: repeating-conic-gradient(rgba(255,250,210,.28) 0 8deg, rgba(255,255,255,0) 8deg 20deg); -webkit-mask: radial-gradient(circle, #000 15%, transparent 60%); }
    #s01-hk { position: absolute; left: 40px; right: 40px; top: 640px; text-align: center; font-family: "Lilita One", sans-serif; }
    #s01-hk .ln { display: block; width: fit-content; margin: 0 auto 16px; padding: 4px 34px 14px; border-radius: 30px; background: #ff2e7e; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.35); font-size: 118px; line-height: 1.05; white-space: nowrap; transform-origin: 50% 60%; }
    #s01-hk span { position: relative; display: inline-block; margin: 0 .08em; color: #fff; -webkit-text-stroke: 8px #1a0f08; paint-order: stroke fill; transform-origin: 50% 65%; }
    #s01-gk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 420px; padding: 8px 30px 16px; border-radius: 26px; background: #e8101e; border: 8px solid #fff; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.3), 0 0 60px 20px rgba(255,20,30,.8); font-family: "Lilita One", sans-serif; font-size: 76px; line-height: 1; color: #fff; white-space: nowrap; transform: rotate(-4deg); }
    #s01-gk span { display: inline-block; }
    #s01-rv { position: absolute; inset: 0; box-shadow: inset 0 0 140px 50px rgba(255,10,20,.9); opacity: 0; }
    .s01-sp { position: absolute; color: #fff; text-shadow: 0 0 18px #fff, 0 0 30px #ffe14a; opacity: 0; line-height: 1; }""",
"""      <div id="s01-ray" data-layout-ignore></div>
      <div id="s01-fl" class="fl" data-layout-ignore></div>
      <div id="s01-rv" data-layout-ignore></div>
      <div id="s01-gk" data-layout-ignore><span id="s01-s1">🚨</span> STREUNER-ALARM! <span id="s01-s2">🚨</span></div>
      <div id="s01-hk">""" + "".join('<div class="ln" id="s01-l' + str(j) + '">' + "".join(f'<span id="s01-w{QW.index(w)}">{w[0]}</span>' for w in ln) + '</div>' for j, ln in enumerate(QL)) + """</div>
      """ + "".join(f'<div class="s01-sp" id="s01-sp{k}" data-layout-ignore style="left:{x}px;top:{y}px;font-size:{f}px">✦</div>' for k, (x, y, f) in enumerate(SP)) + drops("s01-p", 22, 5, 'sc', 540, 900, "🐾", 600, 820)[0],
"""      const sc = at("L1", "Menschen");
      tl.set(["#s01-ray"], { opacity: 1 }, 0);
      tl.fromTo("#s01-ray", { rotation: 0 }, { rotation: 40, duration: 4, ease: "none" }, 0);
      tl.fromTo("#s01-gk", { rotation: -6 }, { rotation: 2, duration: .07, yoyo: true, repeat: 33, ease: "none" }, 0);
      tl.fromTo("#s01-gk", { backgroundColor: "#e8101e", color: "#ffffff" }, { backgroundColor: "#ffffff", color: "#e8101e", duration: .01, yoyo: true, repeat: 15, repeatDelay: .14, ease: "none" }, .1);
      tl.fromTo(["#s01-s1", "#s01-s2"], { rotation: -25, scale: 1 }, { rotation: 25, scale: 1.25, duration: .12, yoyo: true, repeat: 19, ease: "sine.inOut" }, 0);
      tl.fromTo("#s01-rv", { opacity: .2 }, { opacity: 1, duration: .15, yoyo: true, repeat: 15, ease: "sine.inOut", immediateRender: false }, 0);
      tl.to("#s01-rv", { opacity: 0, duration: .3 }, 2.45);
      """ + "\n      ".join(
        f'tl.set("#s01-w{i}", {{ zIndex: 5 }}, at("L1", "{k}") - .03); tl.to("#s01-w{i}", {{ scale: {1.35 if len(w) > 7 else (1.38 if len(w) <= 5 else 1.5)}, rotation: {(-1)**i * 3}, duration: .1, ease: "back.out(3)" }}, at("L1", "{k}") - .03); tl.to("#s01-w{i}", {{ scale: 1, rotation: 0, duration: .22, ease: "power2.inOut" }}, at("L1", "{k}") + .17); tl.set("#s01-w{i}", {{ zIndex: 0 }}, at("L1", "{k}") + .4);'
        + (f' tl.to("#s01-w{i}", {{ color: "#ffe500", duration: .05 }}, at("L1", "{k}") - .02);' if w in YW else '')
        for i, (w, k) in enumerate(QW)) + """
      """ + "\n      ".join(f'tl.fromTo("#s01-sp{k}", {{ opacity: 0, scale: .2, rotation: 0 }}, {{ opacity: 1, scale: 1, rotation: 90, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {k * .2:.2f});' for k in range(len(SP))) + """
      tl.fromTo("#s01-fl", { opacity: .9 }, { opacity: 0, duration: .45, immediateRender: false }, sc);
      tl.to("#s01-l3", { scale: 1.12, duration: .12, yoyo: true, repeat: 1 }, sc);
      tl.to("#s01-gk", { scale: 1.25, duration: .12, yoyo: true, repeat: 1 }, sc + .05);
      tl.to("#s01-hk", { x: 12, duration: .04, yoyo: true, repeat: 5, ease: "none" }, sc);
""" + drops("s01-p", 22, 5, 'sc', 540, 900, "🐾", 600, 820)[1])

# s01b – Das ist Muschel-Tal: die Welt, in der ihr alles entscheidet
scene("s01b", LILITA + "\n    " + PILL + """
    #s1b-lg { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 300px; font-family: "Lilita One", sans-serif; font-size: 150px; line-height: 1; color: #fff; -webkit-text-stroke: 16px #1a0f08; paint-order: stroke fill; filter: drop-shadow(0 12px 0 rgba(0,0,0,.3)); }
    #s1b-lg b { font-weight: 400; color: #ffe14a; }
    #s1b-e { top: 480px; font-size: 50px; background: linear-gradient(100deg, #ff2e7e, #7b3fe0); }""",
"""      <div id="s1b-lg" data-layout-ignore>MUSCHEL-<b>TAL</b></div>
      <div id="s1b-e" class="pl">🗳️ Ihr entscheidet ALLES</div>""",
"""      const t0 = line("L1b")[0], mu = at("L1b", "Muschel-Tal"), en = at("L1b", "ihr");
      tl.fromTo("#s1b-lg", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(1.8)" }, mu - .15);
      tl.fromTo("#s1b-e", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, en - .2);
      tl.to("#s1b-e", { scale: 1.08, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut" }, en + .3);""")

# s02 – Live-Verlosung: Platz in der Strandvilla
def col(names): return '<div id="s02-col">' + "".join(f'<div class="s02-r" id="s02-r{i}">@{n}</div>' for i, n in enumerate(names)) + "</div>"
scene("s02", LILITA + "\n    " + PILL + "\n    " + CF_CSS.replace("top: 700px", "top: 640px") + """
    #s02-dim { position: absolute; inset: 0; background: rgba(10,12,40,.5); }
    #s02-lv { top: 290px; font-size: 50px; background: #e8262f; }
    #s02-v { top: 380px; font-size: 42px; background: #fff; color: #18a6b8; }
    #s02-box { position: absolute; left: 190px; width: 700px; top: 480px; height: 390px; border-radius: 34px; background: #fff; overflow: hidden; box-shadow: 0 0 0 7px #2a1b12, 0 0 0 14px #ffc93c, 0 0 0 19px #2a1b12, 0 18px 0 rgba(0,0,0,.35); }
    #s02-band { position: absolute; left: 0; right: 0; top: 130px; height: 130px; background: #fff3c4; border-top: 5px solid #ffc93c; border-bottom: 5px solid #ffc93c; }
    #s02-col { position: absolute; left: 0; right: 0; top: 0; }
    .s02-r { height: 130px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #23285a; white-space: nowrap; }
    #s02-sh { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,.95)); }
    #s02-fv { position: absolute; left: 60px; width: 960px; top: 905px; text-align: center; white-space: nowrap; font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; color: #fff; text-shadow: 0 2px 6px rgba(0,0,0,.6); }
    #s02-st { left: 0; right: 120px; margin: 0 auto; width: fit-content; top: 900px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 60px; white-space: nowrap; font-family: "Lilita One", sans-serif; }
    #s02-wn { top: 300px; font-size: 50px; background: #2e9e5b; }
    #s02-ml { top: 400px; font-size: 40px; background: #fff; color: #ff6a1a; }
    #s02-fr { top: 490px; font-size: 40px; background: #7b3fe0; }""",
f"""      <div id="s02-dim"></div>
      <div id="s02-lv" class="pl">🔴 LIVE-VERLOSUNG</div>
      <div id="s02-v" class="pl">🏖️ Ein Platz in der Strandvilla</div>
      <div id="s02-box"><div id="s02-band"></div>{col(NS)}<div id="s02-sh" data-layout-ignore></div></div>
      <div id="s02-fv">➕ Folgen & Bewohner werden = teilnehmen!</div>
      <div id="s02-cfw"></div>
      <div id="s02-st" class="stamp" data-layout-ignore>🏖️ GEWONNEN!</div>
      <div id="s02-wn" class="pl">🎉 @sklmq3 zieht in die Villa!</div>
      <div id="s02-ml" class="pl">👭 zu Emilia & Lea</div>
""",
f"""      const l2 = line("L2")[0], vi = at("L2", "Strandvilla"), TB = line("L2w")[0] - .25, gl = at("L2w", "Glückwunsch"), em = at("L2w", "Emilia"), H = 130, N = {len(NS)}, W = {WI};
      tl.fromTo("#s02-dim", {{ opacity: 0 }}, {{ opacity: 1, duration: .3 }}, l2);
      tl.fromTo("#s02-lv", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }}, l2);
      tl.to("#s02-lv", {{ opacity: .4, duration: .2, yoyo: true, repeat: 7, ease: "steps(1)" }}, l2 + .4);
      tl.fromTo("#s02-v", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }}, vi - .3);
      tl.fromTo("#s02-box", {{ opacity: 0, scale: .5 }}, {{ opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }}, vi + .1);
      tl.fromTo("#s02-fv", {{ opacity: 0 }}, {{ opacity: 1, duration: .3 }}, vi + .3);
      tl.to("#s02-fv", {{ opacity: 0, duration: .2 }}, TB);
      tl.set("#s02-col", {{ y: -(N - 3) * H }}, 0);
      tl.fromTo("#s02-col", {{ y: -(N - 3) * H }}, {{ y: -(W - 1) * H, duration: TB - (vi + .6), ease: "power3.out", immediateRender: false }}, vi + .6);
      tl.fromTo("#s02-col", {{ filter: "blur(5px)" }}, {{ filter: "blur(0px)", duration: (TB - vi - .6) * .8, ease: "power2.in", immediateRender: false }}, vi + .6);
      tl.to("#s02-r" + W, {{ color: "#2e9e5b", scale: 1.15, duration: .2, ease: "back.out(3)" }}, TB);
      tl.to("#s02-band", {{ backgroundColor: "#7dff9e", duration: .15, yoyo: true, repeat: 5 }}, TB);
      tl.fromTo("#s02-st", {{ opacity: 0, scale: 2.6 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, TB + .2);
      """ + CONF_JS.replace("SEED", "61").replace("BOX", "s02-cfw").replace("T0", "TB") + """
      tl.to(["#s02-box", "#s02-st", "#s02-lv", "#s02-v", "#s02-dim"], { opacity: 0, duration: .25 }, em - .5);
      tl.fromTo("#s02-wn", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, em - .45);
      tl.fromTo("#s02-ml", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, em - .1);""", blur=True)

# s03 – Eure Wünsche: Kommentar-Screenshot + fertiger Laden
WU = [("L3a", "c_sophia.jpg", "🛟 Rettungsschwimmerin @soph_221144".replace("Rettungsschwimmerin ", ""), "#e8262f", "Rettungsschwimmerin"),
      ("L3b", "c_charlie.jpg", "🍕 Porto Pizza · @charlie._.pink", "#2e9e5b", "Porto"),
      ("L3c", "c_amelie.jpg", "🧋 Boba Beach · @_amiesspamm", "#d4469c", "Boba"),
      ("L3d", "c_jule.jpg", "🍦 @ju1e_smt & @vanessa_k1n", "#18a6b8", "Kunterbunt"),
      ("L3e", "c_mia.jpg", "🛒 @mia_04_ & @leonie27628", "#2a6bff", "Meerkauf"),
      ("L3f", "c_baeckerin.jpg", "🥐 Neu in der Bäckerei: @_privat_033", "#ff6a1a", "neue")]
scene("s03", LILITA + "\n    " + PILL + "\n    " + CMT + """
    .s03-d { max-width: 1000px; }
    #s03-t { top: 260px; font-size: 46px; background: #7b3fe0; }
    .s03-c { top: 360px; }
    .s03-d { top: 560px; font-size: 44px; }""",
"""      <div id="s03-t" class="pl">💬 Ihr habt kommentiert – ich hab's gebaut!</div>
      """ + "\n      ".join(f'<div id="s03-c{i}" class="cmt s03-c"><img src="assets/img/{img}" alt=""></div><div id="s03-d{i}" class="pl s03-d" style="background:{col}">✅ {lab}</div>' for i, (lid, img, lab, col, kw) in enumerate(WU)),
"""      tl.fromTo("#s03-t", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, line("L3a")[0] - .25);
      """ + "\n      ".join(
        f'tl.fromTo("#s03-c{i}", {{ opacity: 0, x: {-700 if i % 2 else 700}, rotation: {-6 if i % 2 else 6} }}, {{ opacity: 1, x: 0, rotation: -1.5, duration: .3, ease: "back.out(1.6)" }}, line("{lid}")[0] - .2);'
        f' tl.fromTo("#s03-d{i}", {{ opacity: 0, scale: .3 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }}, at("{lid}", "{kw}") - .1);'
        f' tl.to("#s03-d{i}", {{ scale: 1.08, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut" }}, at("{lid}", "{kw}") + .3);'
        + (f' tl.to(["#s03-c{i}", "#s03-d{i}"], {{ opacity: 0, y: -30, duration: .2 }}, line("{WU[i+1][0]}")[0] - .3);' if i < len(WU) - 1 else '')
        for i, (lid, img, lab, col, kw) in enumerate(WU)))

# s04 – Tierheim kommt zuerst
scene("s04", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s04-t { top: 280px; font-size: 50px; background: #2e9e5b; }
    #s04-h { position: absolute; left: 70px; right: 70px; top: 390px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s04-h .r { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 42px; } #s04-h .r b { font-size: 66px; color: #2e9e5b; }
    #s04-h .bar { height: 30px; border-radius: 15px; background: #ece4d8; margin-top: 10px; overflow: hidden; } #s04-h .bar i { display: block; height: 100%; width: 0; border-radius: 15px; background: linear-gradient(90deg, #2e9e5b, #8be06a); }
    #s04-h .f { margin-top: 8px; font-weight: 900; font-size: 34px; color: #e2560c; }""",
"""      <div id="s04-t" class="pl">🎯 Unser großes Ziel</div>
      <div id="s04-h"><div class="r"><div>🐾 Tierheim Pfotenkuss</div><div><b id="s04-n">0</b> / 800</div></div><div class="bar"><i id="s04-b"></i></div><div class="f">Bei 800 Bewohnern wird gebaut – nur noch 79!</div></div>""",
"""      const t0 = line("L4")[0], ti = at("L4", "Tierheim"), wi = at("L4", "800"), sv = at("L4", "79");
      tl.fromTo("#s04-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, t0);
      tl.fromTo("#s04-h", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ti - .2);
      count(tl, "#s04-n", 600, 721, wi, .9, "", "", "power2.out");
      tl.fromTo("#s04-b", { width: "0%" }, { width: "90.1%", duration: 1, ease: "power2.out" }, wi);
      tl.to("#s04-b", { opacity: .4, duration: .15, yoyo: true, repeat: 7, ease: "none" }, sv);""")

# s06 – Teaser: nächste Verlosung auf Maries Party-Yacht
scene("s06", LILITA + "\n    " + PILL + "\n    " + BIG + "\n    " + PT + """
    #s06-t { top: 270px; font-size: 48px; background: #7b3fe0; }
    #s06-b { top: 380px; font-size: 66px; background: linear-gradient(135deg, #ff3d7f, #ff9a3d); transform: rotate(-2deg); }
    #s06-y { top: 560px; font-size: 46px; background: #fff; color: #18a6b8; }""",
"""      <div id="s06-t" class="pl">🎟️ Im nächsten Video:</div>
      <div id="s06-b" class="big">2 PLÄTZE ZU GEWINNEN!</div>
      <div id="s06-y" class="pl">🛥️ auf Maries Party-Yacht @marie18034</div>""" + drops("s06-p", 18, 23, 'at("L6", "Party") - .1', 540, 700, "🎉", 560, 760)[0],
"""      const t0 = line("L6")[0], zw = at("L6", "zwei"), pa = at("L6", "Party");
      tl.fromTo("#s06-t", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: .25, ease: "back.out(2)" }, t0);
      tl.fromTo("#s06-b", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, zw - .15);
      tl.to("#s06-b", { scale: 1.08, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, zw + .3);
      tl.fromTo("#s06-y", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, pa - .25);
""" + drops("s06-p", 18, 23, 'at("L6", "Party") - .1', 540, 700, "🎉", 560, 760)[1])

# s05 – Folgen-Aufruf, dann Hütte mit deinem Namen
scene("s05", LILITA + "\n    " + PILL + "\n" + FOLLOW + "\n    " + PT + """
    #s05-t { top: 290px; font-size: 52px; background: #2e9e5b; }
    #s05-btn { top: 400px; } #s05-hand { left: 690px; top: 450px; }
    #s05-fr { position: absolute; left: 360px; top: 680px; width: 360px; height: 450px; border-radius: 34px; border: 9px dashed #ffe14a; box-shadow: 0 0 34px 6px rgba(255,225,74,.7); }
    #s05-nm { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1046px; padding: 4px 26px 8px; border-radius: 999px; overflow: hidden; background: linear-gradient(180deg, #fff9d6, #ffd84a 55%, #ffb21a); border: 4px solid #1a0f08; box-shadow: 0 0 26px 8px rgba(255,220,80,.95), 0 6px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #2a1b12; white-space: nowrap; opacity: 0; }
    #s05-gl { position: absolute; top: -20px; bottom: -20px; left: -120px; width: 70px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.95), rgba(255,255,255,0)); transform: skewX(-20deg); }
    #s05-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 400px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 60px; white-space: nowrap; font-family: "Lilita One", sans-serif; }""",
"""      <div id="s05-t" class="pl">🏝️ Folgen = eigene Hütte</div>
      <div id="s05-btn" class="fbtn">+ Folgen<div id="s05-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s05-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s05-fr" data-layout-ignore></div>
      <div id="s05-nm" data-layout-ignore>@dein_name<i id="s05-gl"></i></div>
      <div id="s05-st" class="stamp" data-layout-ignore>🏠 MIT DEINEM NAMEN!</div>""" + drops("s05-p", 14, 13, 'hu', 540, 820, "🎉", 480, 700)[0],
"""      const t0 = line("L5")[0], fo = at("L5", "folge"), hu = at("L5", "Hütte"), na = at("L5", "Namen");
      tl.fromTo("#s05-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, t0 - .1);
      tl.fromTo("#s05-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, t0);
      tl.fromTo("#s05-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, t0 + .1);
      tl.to("#s05-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .05);
      tl.to("#s05-btn2", { opacity: 1, duration: .05 }, fo + .15);
      tl.fromTo("#s05-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .15);
      tl.to("#s05-hand", { opacity: 0, duration: .2 }, fo + .5);
      tl.fromTo("#s05-nm", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, hu - .1);
      tl.fromTo("#s05-gl", { x: 0 }, { x: 520, duration: .6, repeat: 3, repeatDelay: .25, ease: "power1.inOut", immediateRender: false }, hu + .2);
      tl.to("#s05-nm", { boxShadow: "0 0 50px 18px rgba(255,230,90,1), 0 6px 0 rgba(0,0,0,.3)", duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, hu + .2);
      tl.fromTo("#s05-fr", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, hu - .2);
      tl.to("#s05-fr", { borderColor: "#2e9e5b", borderStyle: "solid", boxShadow: "0 0 50px 14px rgba(46,158,91,.9)", duration: .2 }, na - .1);
      tl.to(["#s05-btn", "#s05-t"], { opacity: 0, duration: .2 }, na - .35);
      tl.fromTo("#s05-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, na - .2);
""" + drops("s05-p", 14, 13, 'hu', 540, 820, "🎉", 480, 700)[1], blur=False)
