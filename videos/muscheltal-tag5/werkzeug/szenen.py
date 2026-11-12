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

LOCK = '<svg viewBox="0 0 64 64" width="110" height="110"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd84d"/><stop offset="1" stop-color="#ff8a00"/></linearGradient></defs><path d="M20 28 V20 a12 12 0 0 1 24 0 V28" fill="none" stroke="#2a1b12" stroke-width="6" stroke-linecap="round"/><rect x="12" y="27" width="40" height="30" rx="9" fill="url(#lg)" stroke="#2a1b12" stroke-width="4"/><circle cx="32" cy="40" r="4.5" fill="#2a1b12"/><rect x="30" y="42" width="4" height="8" rx="2" fill="#2a1b12"/><path d="M54 8 l2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2z" fill="#fff"/></svg>'
HW = [("ICH", "Ich", "<br>"), ("VERSCHENKE", "verschenke", "<br>"), ("EINE", "eine", ""), ("VILLA!", "VILLA", "")]

# s01 – Stil wie Tag 1 „Ich habe euch eine Insel gekauft“: pinke Balken, Schlüsselwörter werden gelb, Sticker „BESIEDELT!“
QL = [[("STELL", "Stell"), ("DIR", "dir"), ("VOR,", "vor")], [("DEINE", "deine"), ("FOLLOWER", "Follower")], [("WÜRDEN", "würden"), ("EINE", "eine")], [("INSEL", "Insel")], [("BESIEDELN!", "besiedeln")]]
QW = [w for ln in QL for w in ln]
YW = ("FOLLOWER", "INSEL", "BESIEDELN!")
SP = [(110, 560, 46), (900, 600, 34), (70, 960, 30), (930, 1010, 44), (180, 1330, 38), (820, 1290, 30)]
scene("s01", LILITA + "\n    " + PT + "\n" + FL + """
    #s01-ray { position: absolute; left: -460px; top: 300px; width: 2000px; height: 2000px; border-radius: 50%; background: repeating-conic-gradient(rgba(255,250,210,.28) 0 8deg, rgba(255,255,255,0) 8deg 20deg); -webkit-mask: radial-gradient(circle, #000 15%, transparent 60%); }
    #s01-hk { position: absolute; left: 40px; right: 40px; top: 620px; text-align: center; font-family: "Lilita One", sans-serif; }
    #s01-hk .ln { display: block; width: fit-content; margin: 0 auto 16px; padding: 4px 34px 14px; border-radius: 30px; background: #ff2e7e; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.35); font-size: 112px; line-height: 1.05; white-space: nowrap; transform-origin: 50% 60%; }
    #s01-hk span { display: inline-block; margin: 0 .08em; color: #fff; -webkit-text-stroke: 8px #1a0f08; paint-order: stroke fill; transform-origin: 50% 65%; }
    #s01-gk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 400px; padding: 6px 36px 14px; border-radius: 26px; background: #fff; border: 8px solid #ff2e7e; box-shadow: 0 0 0 5px #1a0f08, 0 12px 0 rgba(0,0,0,.3); font-family: "Lilita One", sans-serif; font-size: 96px; line-height: 1; color: #ff2e7e; transform: rotate(-6deg); }
    .s01-sp { position: absolute; color: #fff; text-shadow: 0 0 18px #fff, 0 0 30px #ffe14a; opacity: 0; line-height: 1; }
    #s01-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 820px; z-index: 6; padding: 14px 40px 22px; box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.35), 0 0 80px 20px rgba(255,255,255,.7); color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 120px; line-height: 1.05; text-align: center; white-space: nowrap; font-family: "Lilita One", sans-serif; }""",
"""      <div id="s01-ray" data-layout-ignore></div>
      <div id="s01-fl" class="fl" data-layout-ignore></div>
      <div id="s01-gk" data-layout-ignore>BESIEDELT!</div>
      <div id="s01-hk">""" + "".join('<div class="ln" id="s01-l' + str(j) + '">' + "".join(f'<span id="s01-w{QW.index(w)}">{w[0]}</span>' for w in ln) + '</div>' for j, ln in enumerate(QL)) + """</div>
      """ + "".join(f'<div class="s01-sp" id="s01-sp{k}" data-layout-ignore style="left:{x}px;top:{y}px;font-size:{f}px">✦</div>' for k, (x, y, f) in enumerate(SP)) + """
      <div id="s01-st" class="stamp" data-layout-ignore>✅ GENAU DAS<br>MACHE ICH!</div>""" + drops("s01-p", 22, 5, 'ge', 540, 900, "🏠", 600, 820)[0] + drops("s01-q2", 16, 9, 'ge + .2', 540, 900, "🐚", 520, 760)[0],
"""      const ge = at("L1b", "Genau"), be = at("L1", "besiedeln");
      tl.set(["#s01-ray"], { opacity: 1 }, 0);
      tl.fromTo("#s01-ray", { rotation: 0 }, { rotation: 40, duration: 4, ease: "none" }, 0);
      tl.fromTo("#s01-gk", { rotation: -6 }, { rotation: -2, duration: .5, yoyo: true, repeat: 7, ease: "sine.inOut" }, 0);
      """ + "\n      ".join(
        f'tl.to("#s01-w{i}", {{ scale: 1.22, duration: .09, yoyo: true, repeat: 1, ease: "power2.out" }}, at("L1", "{k}") - .02);'
        + (f' tl.to("#s01-w{i}", {{ color: "#ffe500", duration: .05 }}, at("L1", "{k}") - .02);' if w in YW else '')
        for i, (w, k) in enumerate(QW)) + """
      """ + "\n      ".join(f'tl.fromTo("#s01-sp{k}", {{ opacity: 0, scale: .2, rotation: 0 }}, {{ opacity: 1, scale: 1, rotation: 90, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {k * .23:.2f});' for k in range(len(SP))) + """
      tl.fromTo("#s01-fl", { opacity: .9 }, { opacity: 0, duration: .45, immediateRender: false }, be);
      tl.to("#s01-l4", { scale: 1.12, duration: .12, yoyo: true, repeat: 1 }, be);
      tl.to("#s01-gk", { scale: 1.25, duration: .12, yoyo: true, repeat: 1 }, be + .05);
      tl.to("#s01-hk", { x: 12, duration: .04, yoyo: true, repeat: 5, ease: "none" }, be);
      tl.to("#s01-hk", { opacity: 0, y: -40, duration: .2 }, ge - .15);
      tl.fromTo("#s01-fl", { opacity: .85 }, { opacity: 0, duration: .35, immediateRender: false }, ge);
      tl.fromTo("#s01-st", { opacity: 0, scale: .1, rotation: -20 }, { opacity: 1, scale: 1, rotation: -4, duration: .32, ease: "back.out(3.2)" }, ge - .05);
      tl.to("#s01-st", { scale: 1.08, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut" }, ge + .3);
""" + drops("s01-p", 22, 5, 'ge', 540, 900, "🏠", 600, 820)[1] + drops("s01-q2", 16, 9, 'ge + .2', 540, 900, "🐚", 520, 760)[1])

# s04n – Nagelstudio kurz: Lisann links, Alina rechts
def side(cid, img, name, hand, col, left):
    return f"""<div id="{cid}" class="s4n-pn" style="left:{left}px;background:{col}"><img src="assets/img/{img}" alt=""><div class="nm">{name}</div><div class="hd" id="{cid}-hd">{hand}</div></div>"""
scene("s04n", LILITA + "\n    " + PILL + """
    #s4n-t { top: 290px; font-size: 54px; background: #e8467c; }
    .s4n-pn { position: absolute; top: 400px; width: 400px; height: 470px; border-radius: 32px; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); overflow: hidden; opacity: 0; }
    .s4n-pn img { position: absolute; left: 30px; top: 20px; width: 340px; height: 340px; border-radius: 24px; }
    .s4n-pn .nm { position: absolute; left: 0; right: 0; top: 368px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 32px; color: #fff; }
    .s4n-pn .hd { position: absolute; left: 0; right: 0; top: 412px; margin: 0 auto; width: fit-content; padding: 2px 14px 6px; border-radius: 14px; background: #fff; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 34px; opacity: 0; }
    #s4n-sx { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 900px; padding: 4px 20px 8px; border-radius: 18px; background: #e8262f; color: #fff; font-family: "Lilita One", sans-serif; font-size: 48px; box-shadow: 0 0 0 5px #2a1b12; transform: rotate(-6deg); opacity: 0; }""",
"""      <div id="s4n-t" class="pl">💅 NEU: Ocean Nails</div>
      """ + side("s4n-L", "av_lisann.png", "@lisann.lmp", "🤚 LINKE HÄNDE", "linear-gradient(160deg,#ff5e8a,#c2185b)", 90) + side("s4n-R", "av_alina.png", "@al1na.mai5", "✋ RECHTE HÄNDE", "linear-gradient(200deg,#5ea8ff,#3949ab)", 590) + """
      <div id="s4n-sx" data-layout-ignore>⏳ Bis der Streit beigelegt ist</div>""",
"""      const ng = at("L4n", "Nagelstudio"), sr = at("L4n", "Streit") - .3, li = at("L4n", "linken"), al = at("L4n", "rechten"), u1 = at("L4n", "lisann"), u2 = at("L4n", "al1na");
      tl.fromTo("#s4n-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, ng - .25);
      tl.fromTo("#s4n-L", { opacity: 1, x: -500, rotation: -8 }, { x: 0, rotation: -3, duration: .3, ease: "back.out(1.6)" }, u1 - .1);
      tl.fromTo("#s4n-R", { opacity: 1, x: 500, rotation: 8 }, { x: 0, rotation: 3, duration: .3, ease: "back.out(1.6)" }, u2 - .1);
      tl.fromTo("#s4n-sx", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, sr - .1);
      tl.to("#s4n-sx", { x: 10, duration: .05, yoyo: true, repeat: 5, ease: "none" }, sr + .15);
      tl.fromTo("#s4n-L-hd", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1.15, duration: .3, ease: "back.out(2.6)" }, li);
      tl.fromTo("#s4n-R-hd", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1.15, duration: .3, ease: "back.out(2.6)" }, al);
      tl.to(["#s4n-L", "#s4n-R", "#s4n-sx"], { opacity: 0, y: -40, duration: .3 }, line("L4n")[1] + .2);""")

# s01 – Ich verschenke eine Villa!
scene("s02v", LILITA + "\n    " + PILL + "\n    " + PT + "\n" + FL + """
    #s2v-ray { position: absolute; left: -460px; top: -80px; width: 2000px; height: 2000px; border-radius: 50%; background: repeating-conic-gradient(rgba(255,240,150,.42) 0 9deg, rgba(255,255,255,0) 9deg 22deg); -webkit-mask: radial-gradient(circle, #000 20%, transparent 62%); }
    #s2v-hk { position: absolute; left: 10px; right: 10px; top: 470px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 160px; white-space: nowrap; line-height: 1.02; color: #fff; -webkit-text-stroke: 14px #2a1b12; paint-order: stroke fill; filter: drop-shadow(0 12px 0 rgba(0,0,0,.35)); }
    #s2v-hk span { display: inline-block; margin: 0 .06em; transform-origin: 50% 60%; } #s2v-hk span.y { color: #ffe14a; }
    #s2v-hk i { font-style: normal; display: inline-block; transform-origin: 50% 60%; }
    #s2v-t { top: 290px; font-size: 50px; background: #e8467c; }
    #s2v-v { top: 400px; font-size: 44px; background: #fff; color: #18a6b8; }
    #s2v-e { top: 500px; font-size: 44px; background: #ff7a59; }
    #s2v-f { top: 900px; right: 120px; font-size: 42px; background: #7b3fe0; }""",
"""      <div id="s2v-ray" data-layout-ignore></div>
      <div id="s2v-fl" class="fl" data-layout-ignore></div>
      <div id="s2v-hk">""" + "".join(f'<span id="s2v-w{i}" class="{"y" if w == "VILLA!" else ""}"><i id="s2v-wi{i}">{w}</i></span>{br}' for i, (w, _, br) in enumerate(HW)) + """</div>
      <div id="s2v-t" class="pl">🎟️ Verlosung im nächsten Video!</div>
      <div id="s2v-v" class="pl">🏖️ Ein Platz in der Strandvilla</div>
      <div id="s2v-e" class="pl">👭 Bei Emilia & Lea</div>
      <div id="s2v-f" class="pl">👯 Freund markieren = er zieht mit ein!</div>""" + drops("s2v-a", 18, 17, 'line("L2v")[0]', 540, 700, "🎁", 560, 760)[0] + drops("s2v-b", 22, 19, 'vi - .25', 540, 720, "🏖️", 600, 820)[0],
"""      const vi = at("L2v", "VILLA"), l1b = line("L2vb")[0], pl = at("L2vb", "Platz"), fr = at("L2vb", "Freund");
      """ + "\n      ".join(f'tl.set("#s2v-w{i}", {{ opacity: 1 }}, 0); tl.to("#s2v-wi{i}", {{ scale: {1.25 if i in (1, 3) else 1.6}, color: "#ffffff", textShadow: "0 0 50px rgba(255,230,80,1)", duration: .1, yoyo: true, repeat: 1, ease: "power2.out" }}, {f"line(\"L2v\")[0] + .02" if i == 0 else f"at(\"L2v\", \"{k}\") - .02"});' for i, (_, k, _) in enumerate(HW)) + """
      tl.fromTo("#s2v-ray", { rotation: 0, opacity: 1 }, { rotation: 50, duration: l1b, ease: "none" }, 0);
      tl.fromTo("#s2v-fl", { opacity: 1 }, { opacity: 0, duration: .3, immediateRender: false }, 0);
      tl.fromTo("#s2v-fl", { opacity: .85 }, { opacity: 0, duration: .3, immediateRender: false }, vi);
      tl.to("#s2v-hk", { x: 16, y: -10, duration: .05, yoyo: true, repeat: 5, ease: "none" }, 0.02);
      tl.to("#s2v-hk", { x: 24, y: -12, duration: .04, yoyo: true, repeat: 9, ease: "none" }, vi);
      tl.to("#s2v-hk", { scale: 1.12, duration: .1, yoyo: true, repeat: 3 }, vi + .05);
      tl.to(["#s2v-hk", "#s2v-ray"], { opacity: 0, scale: .7, duration: .25 }, l1b - .1);
      tl.fromTo("#s2v-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, l1b);
      tl.fromTo("#s2v-v", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, pl - .2);
      tl.fromTo("#s2v-e", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, at("L2vb", "Emilia") - .15);
      tl.fromTo("#s2v-f", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fr - .2);
      tl.to("#s2v-f", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, fr + .3);
""" + drops("s2v-a", 18, 17, 'line("L2v")[0]', 540, 700, "🎁", 560, 760)[1] + drops("s2v-b", 22, 19, 'vi - .25', 540, 720, "🏖️", 600, 820)[1])

# s02 – Folgen = eigenes Haus mit Namen
scene("s03h", LILITA + "\n    " + PILL + "\n" + FOLLOW + "\n    " + PT + """
    #s3h-t { top: 290px; font-size: 52px; background: #2e9e5b; }
    #s3h-fr { position: absolute; left: 375px; top: 500px; width: 330px; height: 440px; border-radius: 34px; border: 9px dashed #ffe14a; box-shadow: 0 0 34px 6px rgba(255,225,74,.7); }
    #s3h-tag { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 640px; padding: 8px 26px 12px; border-radius: 22px; background: #ffe14a; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 64px; box-shadow: 0 0 0 6px #2a1b12; transform: rotate(-6deg); }
    #s3h-btn { top: 400px; } #s3h-hand { left: 690px; top: 450px; }
    #s3h-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1035px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 60px; white-space: nowrap; font-family: "Lilita One", sans-serif; }""",
"""      <div id="s3h-t" class="pl">🏝️ Folgen = eigenes Haus</div>
      <div id="s3h-fr" data-layout-ignore></div>
      <div id="s3h-tag" data-layout-ignore>🔑 FREI</div>
      <div id="s3h-btn" class="fbtn">+ Folgen<div id="s3h-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s3h-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s3h-st" class="stamp" data-layout-ignore>🏠 MIT DEINEM NAMEN!</div>""" + drops("s3h-p", 14, 13, 'fo + .2', 540, 720, "🎉", 480, 700)[0],
"""      const fo = at("L3h", "folgt"), na = at("L3h", "Namen");
      tl.fromTo("#s3h-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, line("L3h")[0] - .1);
      tl.fromTo(["#s3h-fr", "#s3h-tag"], { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, line("L3h")[0]);
      tl.fromTo("#s3h-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .45);
      tl.fromTo("#s3h-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .35);
      tl.to("#s3h-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo - .05);
      tl.to("#s3h-btn2", { opacity: 1, duration: .05 }, fo + .05);
      tl.fromTo("#s3h-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .05);
      tl.to("#s3h-hand", { opacity: 0, duration: .2 }, fo + .5);
      tl.to("#s3h-tag", { opacity: 0, scale: .3, duration: .2 }, fo + .1);
      tl.to("#s3h-fr", { borderColor: "#2e9e5b", borderStyle: "solid", boxShadow: "0 0 50px 14px rgba(46,158,91,.9)", duration: .2 }, fo + .15);
      tl.fromTo("#s3h-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, na - .3);
""" + drops("s3h-p", 14, 13, 'fo + .2', 540, 720, "🎉", 480, 700)[1])

# s04 – Yacht für Marie
scene("s04", LILITA + "\n    " + PILL + """
    #s04-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 300px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 76px; white-space: nowrap; font-family: "Lilita One", sans-serif; }
    #s04-n { top: 440px; font-size: 44px; background: #1f6fb8; }
    #s04-p { top: 1030px; right: 120px; font-size: 40px; background: #e8467c; }""",
"""      <div id="s04-st" class="stamp" data-layout-ignore>✅ JA – YACHT!</div>
      <div id="s04-n" class="pl">🛥️ White Pearl · @marie18034</div>
      <div id="s04-p" class="pl">🎉 Jeden Tag Party an Bord!</div>""",
"""      const ma = at("L5", "Marie"), ya = at("L5", "Yacht"), je = at("L5", "jeden");
      tl.fromTo("#s04-st", { opacity: 0, scale: 2.8 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, ma - .1);
      tl.fromTo("#s04-n", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ya - .1);
      tl.fromTo("#s04-p", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, je - .2);
      tl.to("#s04-p", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, je + .3);""")

# s05 – 716 Bewohner, Hotel, Spoiler
scene("s05", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s05-c { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 290px; padding: 8px 40px 14px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 7px #2a1b12, 0 12px 0 rgba(0,0,0,.3); text-align: center; font-family: "Inter", sans-serif; font-weight: 900; color: #2a1b12; font-size: 40px; }
    #s05-c b { display: block; font-family: "Lilita One", sans-serif; font-weight: 400; font-size: 120px; line-height: 1; color: #2e9e5b; }
    #s05-h { position: absolute; left: 70px; right: 70px; top: 540px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s05-h .r { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 40px; } #s05-h .r b { font-size: 66px; color: #e2560c; }
    #s05-h .bar { height: 30px; border-radius: 15px; background: #ece4d8; margin-top: 10px; overflow: hidden; } #s05-h .bar i { display: block; height: 100%; width: 0; border-radius: 15px; background: linear-gradient(90deg, #ff6a1a, #ffb21a); }
    #s05-h .f { margin-top: 8px; font-weight: 900; font-size: 32px; color: #2e9e5b; }""",
"""      <div id="s05-c"><b id="s05-n">0</b>Bewohner 🏝️</div>
      <div id="s05-h"><div class="r"><div>🏗️ Nächster Bau</div><div><b id="s05-hn">716</b> / 800</div></div><div class="bar"><i id="s05-hb"></i></div><div class="f">Nur noch 84 Bewohner – dann wird gebaut!</div></div>""",
"""      const be = at("L6", "Bewohner"), vi = at("L6", "84"), ho = at("L6", "gebaut");
      tl.fromTo("#s05-c", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.4)" }, line("L6")[0]);
      count(tl, "#s05-n", 0, 716, line("L6")[0] + .1, be - line("L6")[0], "", "", "power2.out");
      tl.fromTo("#s05-h", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, vi - .3);
      tl.fromTo("#s05-hb", { width: "0%" }, { width: "89.5%", duration: .9, ease: "power2.out" }, vi - .1);
      tl.to("#s05-hb", { opacity: .4, duration: .15, yoyo: true, repeat: 7, ease: "none" }, ho);""")



# s05b – Zuletzt gebaut: Fabiennes Bäckerei
scene("s05b", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s5b-t { top: 290px; font-size: 52px; background: #2e9e5b; }
    #s5b-b { top: 400px; font-size: 84px; background: linear-gradient(135deg, #ffb21a, #ff6a1a); transform: rotate(-2deg); }
    #s5b-u { top: 560px; font-size: 40px; background: #fff; color: #e2560c; }""",
"""      <div id="s5b-t" class="pl">✅ Zuletzt gebaut</div>
      <div id="s5b-b" class="big">🥐 Fabiennes Bäckerei</div>
      <div id="s5b-u" class="pl">@fabienne3692</div>""",
"""      const t0 = line("L6b")[0], fa = at("L6b", "Fabiennes");
      tl.fromTo("#s5b-t", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: .25, ease: "back.out(2)" }, t0);
      tl.fromTo("#s5b-b", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, fa - .2);
      tl.fromTo("#s5b-u", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2.6)" }, fa + .25);""")

# s05g – Bei 1.000 Followern wird Muschel-Tal zum Spiel
scene("s05g", LILITA + "\n    " + PILL + "\n    " + BIG + "\n" + FL + """
    #s5g-t { top: 230px; font-size: 92px; background: linear-gradient(100deg, #ff3d7f, #7b3fe0 55%, #2fb3ff); transform: rotate(-2deg); box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3), 0 0 60px 12px rgba(123,63,224,.6); }
    #s5g-b { position: absolute; left: 90px; right: 90px; top: 420px; padding: 14px 26px 18px; border-radius: 28px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 10px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s5g-b .r { display: flex; justify-content: space-between; align-items: baseline; font-weight: 900; font-size: 38px; } #s5g-b .r b { font-size: 50px; color: #7b3fe0; }
    #s5g-b .bar { height: 28px; border-radius: 14px; background: #ece4d8; margin-top: 8px; overflow: hidden; } #s5g-b .bar i { display: block; height: 100%; width: 0; border-radius: 14px; background: linear-gradient(90deg, #ff3d7f, #7b3fe0, #2fb3ff); }
    #s5g-du { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 735px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 70px; color: #fff; -webkit-text-stroke: 10px #2a1b12; paint-order: stroke fill; }
    #s5g-du div { font-size: 90px; line-height: .9; -webkit-text-stroke: 0; }
    #s5g-hud { position: absolute; inset: 0; }
    #s5g-js { position: absolute; left: 70px; top: 1300px; width: 230px; height: 230px; border-radius: 50%; background: rgba(255,255,255,.28); box-shadow: inset 0 0 0 6px rgba(255,255,255,.75), 0 0 0 4px rgba(42,27,18,.5); }
    #s5g-jk { position: absolute; left: 60px; top: 60px; width: 110px; height: 110px; border-radius: 50%; background: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 8px 0 rgba(0,0,0,.3); }
    #s5g-ch { position: absolute; left: 60px; top: 560px; display: flex; flex-direction: column; gap: 18px; }
    .s5g-c { padding: 8px 26px 12px; border-radius: 999px; background: #fff; color: #2a1b12; font-family: "Inter", sans-serif; font-weight: 900; font-size: 44px; box-shadow: 0 0 0 5px #2a1b12, 0 8px 0 rgba(0,0,0,.3); width: fit-content; }
    #s5g-v { top: 600px; font-size: 64px; background: linear-gradient(135deg, #ffb21a, #ff6a1a); }""",
"""      <div id="s5g-fl" class="fl" data-layout-ignore></div>
      <div id="s5g-t" class="big">🎮 BALD SPIELBAR!</div>
      <div id="s5g-b"><div class="r"><div>Bei 1.000 Followern</div><div><b id="s5g-n">716</b> / 1.000</div></div><div class="bar"><i id="s5g-bi"></i></div></div>
      <div id="s5g-du" data-layout-ignore>DU<div>👇</div></div>
            <div id="s5g-ch"><div id="s5g-c0" class="s5g-c">🕹️ Spiel dich selbst</div><div id="s5g-c1" class="s5g-c">🏝️ Lauf über die Inseln</div><div id="s5g-c2" class="s5g-c">🗺️ Erkunde die Welt</div></div>
      <div id="s5g-v" class="big">⭐ Die ersten 1.000: VORTEILE!</div>""",
"""      const t0 = line("L7g")[0], sp = at("L7g", "Spiel"), sl = at("L7g", "spielst"), la = at("L7g", "läufst"), er = at("L7g", "erkundest"), di = at("L7g", "ersten"), vo = at("L7g", "Vorteile");
      tl.fromTo("#s5g-b", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, t0 + .4);
      tl.fromTo("#s5g-bi", { width: "0%" }, { width: "71.6%", duration: .9, ease: "power2.out" }, t0 + .6);
      tl.fromTo("#s5g-fl", { opacity: .8 }, { opacity: 0, duration: .3, immediateRender: false }, sp);
      tl.fromTo("#s5g-t", { opacity: 0, scale: 3.5 }, { opacity: 1, scale: 1, duration: .25, ease: "power3.in" }, sp - .25);
      tl.to("#s5g-t", { scale: 1.07, duration: .25, yoyo: true, repeat: 9, ease: "sine.inOut" }, sp + .1);
      tl.fromTo("#s5g-du", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2.5)" }, sl - .1);
      tl.to("#s5g-du div", { y: 18, duration: .25, yoyo: true, repeat: 11, ease: "sine.inOut" }, sl + .2);
            [[0, sl], [1, la], [2, er]].forEach(([i, t]) => tl.fromTo("#s5g-c" + i, { opacity: 0, x: -400 }, { opacity: 1, x: 0, duration: .28, ease: "back.out(1.8)" }, t - .1));
      tl.to("#s5g-du", { opacity: 0, duration: .2 }, la + .15);
      tl.to(["#s5g-ch"], { opacity: 0, duration: .2 }, di - .25);
      tl.fromTo("#s5g-v", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, di - .15);
      tl.to("#s5g-v", { scale: 1.1, duration: .12, yoyo: true, repeat: 1 }, vo);""")

# s06 – Abstimmung der Bürgermeisterin: Hotel oder Tierheim
scene("s06", LILITA + "\n    " + PILL + """
    #s06-h { top: 280px; font-size: 46px; background: #7b3fe0; }
    .s06-a { position: absolute; top: 470px; width: 430px; padding: 18px 14px 22px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); text-align: center; font-family: "Inter", sans-serif; font-weight: 900; color: #2a1b12; font-size: 38px; line-height: 1.15; }
    .s06-a i { display: block; font-style: normal; font-size: 110px; line-height: 1.1; }
    #s06-vs { position: absolute; left: 0; right: 0; top: 590px; margin: 0 auto; width: fit-content; font-family: "Lilita One", sans-serif; font-size: 110px; color: #ffe14a; -webkit-text-stroke: 12px #2a1b12; paint-order: stroke fill; }
    #s06-8 { top: 365px; font-size: 40px; background: #ff6a1a; transform: rotate(-1.5deg); }
    #s06-c { top: 840px; font-size: 44px; background: #fe2c55; }
    #s06-ar { position: absolute; left: 850px; top: 1230px; font-size: 110px; filter: drop-shadow(0 6px 0 rgba(0,0,0,.35)); }
    #s06-cb { position: absolute; left: 640px; top: 1085px; padding: 4px 18px 8px; border-radius: 999px; background: #fff; color: #fe2c55; font-family: "Inter", sans-serif; font-weight: 900; font-size: 30px; box-shadow: 0 0 0 4px #2a1b12; }""",
"""      <div id="s06-h" class="pl">🗳️ Abstimmung von Bürgermeisterin Lilly</div>
      <div id="s06-8" class="pl">Bei 800 Bewohnern bauen wir zuerst …</div>
            <div id="s06-o1"><div class="s06-a" style="left:50px"><i>🏨</i>Hotel<br>Sandkorn</div></div>
      <div id="s06-o2"><div class="s06-a" style="left:600px"><i>🐾</i>Tierheim<br>Pfotenkuss</div></div>
      <div id="s06-vs" data-layout-ignore>VS</div>
      <div id="s06-c" class="pl">💬 Stimmt in den Kommentaren ab!</div>
      <div id="s06-cb" data-layout-ignore>Hier abstimmen</div>
      <div id="s06-ar" data-layout-ignore>👉</div>""",
"""      const ab = at("L10", "Abstimmung"), ac = at("L10", "800"), ho = at("L10", "Hotel"), ti = at("L10", "Tierheim"), st = at("L10", "Stimmt");
      tl.fromTo("#s06-h", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, ab - .3);
      tl.fromTo("#s06-8", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2.2)" }, ac - .2);
      tl.fromTo("#s06-o1", { opacity: 0, x: -500 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(1.6)" }, ho - .2);
      tl.fromTo("#s06-o2", { opacity: 0, x: 500 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(1.6)" }, ti - .2);
      tl.fromTo("#s06-vs", { opacity: 0, scale: 4 }, { opacity: 1, scale: 1, duration: .22, ease: "power3.in" }, ti + .15);
      tl.to("#s06-o1", { scale: 1.06, duration: .2, yoyo: true, repeat: 1 }, ho + .1);
      tl.to("#s06-o2", { scale: 1.06, duration: .2, yoyo: true, repeat: 1 }, ti + .1);
      tl.fromTo("#s06-c", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, st - .2);
      tl.to("#s06-c", { scale: 1.08, duration: .2, yoyo: true, repeat: 7, ease: "sine.inOut" }, st + .3);
      tl.fromTo(["#s06-ar", "#s06-cb"], { opacity: 0 }, { opacity: 1, duration: .25 }, st);
      tl.to("#s06-ar", { x: 40, duration: .3, yoyo: true, repeat: 7, ease: "sine.inOut" }, st + .2);""", blur=False)
