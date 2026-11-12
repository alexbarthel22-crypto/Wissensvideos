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

# s01 – Ich verschenke eine Villa!
scene("s01", LILITA + "\n    " + PILL + "\n    " + PT + "\n" + FL + """
    #s01-ray { position: absolute; left: -460px; top: -80px; width: 2000px; height: 2000px; border-radius: 50%; background: repeating-conic-gradient(rgba(255,240,150,.42) 0 9deg, rgba(255,255,255,0) 9deg 22deg); -webkit-mask: radial-gradient(circle, #000 20%, transparent 62%); }
    #s01-hk { position: absolute; left: 10px; right: 10px; top: 470px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 160px; white-space: nowrap; line-height: 1.02; color: #fff; -webkit-text-stroke: 14px #2a1b12; paint-order: stroke fill; filter: drop-shadow(0 12px 0 rgba(0,0,0,.35)); }
    #s01-hk span { display: inline-block; margin: 0 .06em; transform-origin: 50% 60%; } #s01-hk span.y { color: #ffe14a; }
    #s01-hk i { font-style: normal; display: inline-block; transform-origin: 50% 60%; }
    #s01-t { top: 290px; font-size: 50px; background: #e8467c; }
    #s01-v { top: 400px; font-size: 44px; background: #fff; color: #18a6b8; }
    #s01-f { top: 900px; right: 120px; font-size: 42px; background: #7b3fe0; }""",
"""      <div id="s01-ray" data-layout-ignore></div>
      <div id="s01-fl" class="fl" data-layout-ignore></div>
      <div id="s01-hk">""" + "".join(f'<span id="s01-w{i}" class="{"y" if w == "VILLA!" else ""}"><i id="s01-wi{i}">{w}</i></span>{br}' for i, (w, _, br) in enumerate(HW)) + """</div>
      <div id="s01-t" class="pl">🎟️ Verlosung im nächsten Video!</div>
      <div id="s01-v" class="pl">🏖️ Ein Platz in der Strandvilla</div>
      <div id="s01-f" class="pl">👯 Freund markieren = er zieht mit ein!</div>""" + drops("s01-a", 18, 17, '0', 540, 700, "🎁", 560, 760)[0] + drops("s01-b", 22, 19, 'vi - .25', 540, 720, "🏖️", 600, 820)[0],
"""      const vi = at("L1", "VILLA"), l1b = line("L1b")[0], pl = at("L1b", "Platz"), fr = at("L1b", "Freund");
      """ + "\n      ".join(f'tl.set("#s01-w{i}", {{ opacity: 1 }}, 0); tl.to("#s01-wi{i}", {{ scale: {1.25 if i in (1, 3) else 1.6}, color: "#ffffff", textShadow: "0 0 50px rgba(255,230,80,1)", duration: .1, yoyo: true, repeat: 1, ease: "power2.out" }}, {"0.02" if i == 0 else f"at(\"L1\", \"{k}\") - .02"});' for i, (_, k, _) in enumerate(HW)) + """
      tl.fromTo("#s01-ray", { rotation: 0, opacity: 1 }, { rotation: 50, duration: l1b, ease: "none" }, 0);
      tl.fromTo("#s01-fl", { opacity: 1 }, { opacity: 0, duration: .3, immediateRender: false }, 0);
      tl.fromTo("#s01-fl", { opacity: .85 }, { opacity: 0, duration: .3, immediateRender: false }, vi);
      tl.to("#s01-hk", { x: 16, y: -10, duration: .05, yoyo: true, repeat: 5, ease: "none" }, 0.02);
      tl.to("#s01-hk", { x: 24, y: -12, duration: .04, yoyo: true, repeat: 9, ease: "none" }, vi);
      tl.to("#s01-hk", { scale: 1.12, duration: .1, yoyo: true, repeat: 3 }, vi + .05);
      tl.to(["#s01-hk", "#s01-ray"], { opacity: 0, scale: .7, duration: .25 }, l1b - .1);
      tl.fromTo("#s01-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, l1b);
      tl.fromTo("#s01-v", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, pl - .2);
      tl.fromTo("#s01-f", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fr - .2);
      tl.to("#s01-f", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, fr + .3);
""" + drops("s01-a", 18, 17, '0', 540, 700, "🎁", 560, 760)[1] + drops("s01-b", 22, 19, 'vi - .25', 540, 720, "🏖️", 600, 820)[1])

# s02 – Folgen = eigenes Haus mit Namen
scene("s02", LILITA + "\n    " + PILL + "\n" + FOLLOW + "\n    " + PT + """
    #s02-t { top: 290px; font-size: 52px; background: #2e9e5b; }
    #s02-fr { position: absolute; left: 375px; top: 500px; width: 330px; height: 440px; border-radius: 34px; border: 9px dashed #ffe14a; box-shadow: 0 0 34px 6px rgba(255,225,74,.7); }
    #s02-tag { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 640px; padding: 8px 26px 12px; border-radius: 22px; background: #ffe14a; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 64px; box-shadow: 0 0 0 6px #2a1b12; transform: rotate(-6deg); }
    #s02-btn { top: 400px; } #s02-hand { left: 690px; top: 450px; }
    #s02-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1035px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 60px; white-space: nowrap; font-family: "Lilita One", sans-serif; }""",
"""      <div id="s02-t" class="pl">🏝️ Folgen = eigenes Haus</div>
      <div id="s02-fr" data-layout-ignore></div>
      <div id="s02-tag" data-layout-ignore>🔑 FREI</div>
      <div id="s02-btn" class="fbtn">+ Folgen<div id="s02-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s02-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s02-st" class="stamp" data-layout-ignore>🏠 MIT DEINEM NAMEN!</div>""" + drops("s02-p", 14, 13, 'fo + .2', 540, 720, "🎉", 480, 700)[0],
"""      const fo = at("L2", "folgt"), na = at("L2", "Namen");
      tl.fromTo("#s02-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, line("L2")[0] - .1);
      tl.fromTo(["#s02-fr", "#s02-tag"], { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, line("L2")[0]);
      tl.fromTo("#s02-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .45);
      tl.fromTo("#s02-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .35);
      tl.to("#s02-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo - .05);
      tl.to("#s02-btn2", { opacity: 1, duration: .05 }, fo + .05);
      tl.fromTo("#s02-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .05);
      tl.to("#s02-hand", { opacity: 0, duration: .2 }, fo + .5);
      tl.to("#s02-tag", { opacity: 0, scale: .3, duration: .2 }, fo + .1);
      tl.to("#s02-fr", { borderColor: "#2e9e5b", borderStyle: "solid", boxShadow: "0 0 50px 14px rgba(46,158,91,.9)", duration: .2 }, fo + .15);
      tl.fromTo("#s02-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, na - .3);
""" + drops("s02-p", 14, 13, 'fo + .2', 540, 720, "🎉", 480, 700)[1])

# s03 – Nagelstudio Ocean Nails
scene("s03", LILITA + "\n    " + PILL + """
    #s03-t { top: 290px; font-size: 50px; background: #7b3fe0; }
    #s03-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 400px; color: #e8467c; border-color: #e8467c; background: #fff; transform: rotate(-4deg); font-size: 66px; white-space: nowrap; font-family: "Lilita One", sans-serif; }
    .s03-n { top: 1000px; font-size: 36px; background: #fff; color: #2a1b12; right: auto; margin: 0; }
    #s03-sx { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 400px; padding: 6px 30px 12px; border-radius: 22px; background: #e8262f; color: #fff; font-family: "Lilita One", sans-serif; font-size: 70px; box-shadow: 0 0 0 6px #2a1b12; transform: rotate(3deg); }
    #s03-hs { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 520px; font-size: 130px; }""",
"""      <div id="s03-t" class="pl">💡 Euer Top-Kommentar</div>
      <div id="s03-st" class="stamp" data-layout-ignore>💅 OCEAN NAILS – GEBAUT!</div>
      <div id="s03-sx" data-layout-ignore>⚡ STREIT?</div>
      <div id="s03-hs" data-layout-ignore>🤝</div>
      <div id="s03-l" class="pl s03-n" style="left:60px">⭐🤚 @lisann.lmp – links</div>
      <div id="s03-r" class="pl s03-n" style="left:540px">⭐✋ @al1na.mai5 – rechts</div>""",
"""      const ng = at("L3", "Nagelstudio"), hi = at("L3", "hier"), li = at("L4", "Lisann"), al = at("L4", "Alina"), sr = at("L4", "Streit"), lk = at("L4", "linken"), re = at("L4", "rechten");
      tl.fromTo("#s03-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, ng - .3);
      tl.fromTo("#s03-st", { opacity: 0, scale: 2.8 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, hi - .05);
      tl.to(["#s03-t", "#s03-st"], { opacity: 0, duration: .2 }, li - .2);
      tl.fromTo("#s03-sx", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, sr - .1);
      tl.to("#s03-sx", { x: 14, duration: .05, yoyo: true, repeat: 7, ease: "none" }, sr + .15);
      tl.to("#s03-sx", { opacity: 0, scale: .4, duration: .2 }, lk - .4);
      tl.fromTo("#s03-hs", { opacity: 0, scale: .2, rotation: -30 }, { opacity: 1, scale: 1, rotation: 0, duration: .35, ease: "back.out(3)" }, lk - .3);
      tl.fromTo("#s03-l", { opacity: 0, x: -120 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, li - .1);
      tl.fromTo("#s03-r", { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, al - .1);
      tl.to("#s03-l", { scale: 1.2, backgroundColor: "#ffd23f", duration: .14, yoyo: true, repeat: 1 }, lk);
      tl.to("#s03-r", { scale: 1.2, backgroundColor: "#ffd23f", duration: .14, yoyo: true, repeat: 1 }, re);""")

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
    #s05-h .f { margin-top: 8px; font-weight: 900; font-size: 32px; color: #2e9e5b; }
    #s05-sp { top: 290px; font-size: 64px; background: linear-gradient(135deg, #ff5ecf, #7b5cff); transform: rotate(-2deg); }
    #s05-lk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 470px; padding: 14px 40px 18px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 7px #2a1b12; font-family: "Inter", sans-serif; font-weight: 900; font-size: 42px; color: #2a1b12; text-align: center; }""",
"""      <div id="s05-c"><b id="s05-n">0</b>Bewohner 🏝️</div>
      <div id="s05-h"><div class="r"><div>🏨 Hotel Sandkorn</div><div><b id="s05-hn">716</b> / 800</div></div><div class="bar"><i id="s05-hb"></i></div><div class="f">Nur noch 84 Bewohner bis zur Eröffnung!</div></div>
      <div id="s05-sp" class="big">🤫 SPOILER</div>
      <div id="s05-lk">""" + LOCK + """<br>Die ersten 1.000 bekommen<br>Vorteile im Spiel!</div>""",
"""      const be = at("L6", "Bewohner"), vi = at("L6", "84"), ho = at("L6", "Hotel"), l7 = line("L7")[0], vo = at("L7", "Vorteile");
      tl.fromTo("#s05-c", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.4)" }, line("L6")[0]);
      count(tl, "#s05-n", 0, 716, line("L6")[0] + .1, be - line("L6")[0], "", "", "power2.out");
      tl.fromTo("#s05-h", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, vi - .3);
      tl.fromTo("#s05-hb", { width: "0%" }, { width: "89.5%", duration: .9, ease: "power2.out" }, vi - .1);
      tl.to("#s05-hb", { opacity: .4, duration: .15, yoyo: true, repeat: 7, ease: "none" }, ho);
      tl.to(["#s05-c", "#s05-h"], { opacity: 0, y: -30, duration: .25 }, l7 - .2);
      tl.fromTo("#s05-sp", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, l7 - .05);
      tl.fromTo("#s05-lk", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, l7 + .3);
      tl.to("#s05-lk svg", { rotation: 12, duration: .1, yoyo: true, repeat: 7 }, vo);""")

# s06 – Ideen + Freunde + Folgen
scene("s06", LILITA + "\n    " + PILL + "\n    " + BIG + "\n" + FOLLOW + """
    #s06-h { top: 290px; font-size: 76px; background: #fe2c55; transform: rotate(-2deg); }
    #s06-g { top: 470px; font-size: 42px; background: #e8262f; }
    #s06-ar { position: absolute; left: 850px; top: 1230px; font-size: 110px; filter: drop-shadow(0 6px 0 rgba(0,0,0,.35)); }
    #s06-cb { position: absolute; left: 640px; top: 1085px; padding: 4px 18px 8px; border-radius: 999px; background: #fff; color: #fe2c55; font-family: "Inter", sans-serif; font-weight: 900; font-size: 30px; box-shadow: 0 0 0 4px #2a1b12; }
    #s06-t { top: 290px; font-size: 50px; background: #e8467c; }
    #s06-nb { top: 560px; font-size: 34px; background: #2e9e5b; }
    #s06-btn { top: 400px; } #s06-hand { left: 690px; top: 450px; }""",
"""      <div id="s06-h" class="big">💬 WAS BAUEN WIR<br>ALS NÄCHSTES?</div>
      <div id="s06-g" class="pl">❤️ Meiste Likes = nächstes Video!</div>
      <div id="s06-cb" data-layout-ignore>Hier kommentieren</div>
      <div id="s06-ar" data-layout-ignore>👉</div>
      <div id="s06-t" class="pl">👯 Markiert eure Freunde!</div>
      <div id="s06-nb" class="pl">🤝 Nachbarn: @melie_js & @lisann.lmp</div>
      <div id="s06-btn" class="fbtn">+ Folgen<div id="s06-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s06-hand" class="fhand" data-layout-ignore>👆</div>""",
"""      const wa = line("L8")[0], me = at("L8", "meisten"), l9 = line("L9")[0], fr = at("L9", "Freunde"), fo = at("L9", "folgt");
      tl.fromTo("#s06-h", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, wa);
      tl.fromTo("#s06-g", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, me - .2);
      tl.fromTo(["#s06-ar", "#s06-cb"], { opacity: 0 }, { opacity: 1, duration: .25 }, wa + .3);
      tl.to("#s06-ar", { x: 40, duration: .3, yoyo: true, repeat: 7, ease: "sine.inOut" }, wa + .5);
      tl.to(["#s06-h", "#s06-g", "#s06-ar", "#s06-cb"], { opacity: 0, duration: .2 }, l9 - .2);
      tl.fromTo("#s06-t", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, fr - .3);
      tl.fromTo("#s06-nb", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, fr);
      tl.fromTo("#s06-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .4);
      tl.fromTo("#s06-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .2);
      tl.to("#s06-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .1);
      tl.to("#s06-btn2", { opacity: 1, duration: .05 }, fo + .2);
      tl.fromTo("#s06-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .2);
      tl.to("#s06-hand", { opacity: 0, duration: .25 }, fo + .7);""", blur=False)
