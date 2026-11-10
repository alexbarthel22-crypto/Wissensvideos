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

# s01 – Stell dir vor: Es regnet Red Bull
r_h, r_js = rain("s01-c", 150, 4, '0', 'C.__dur + .3')
b1_h, b1_js = drops("s01-b", 14, 21, 'rb', 540, 480, "⚡", 520, 700)
scene("s01", LILITA + "\n    " + PILL + "\n    " + CAN + "\n    " + PT + "\n" + FL + """
    #s01-a { top: 290px; font-size: 76px; padding: 10px 40px 16px; background: #7b3fe0; z-index: 5; }
    #s01-h { z-index: 5; position: absolute; left: 70px; right: 70px; top: 440px; padding: 14px 20px 26px; border-radius: 40px; background: #1f3f95; color: #fff; font-family: "Lilita One", sans-serif; font-size: 160px; line-height: .95; text-align: center; box-shadow: 0 0 0 9px #2a1b12, 0 18px 0 rgba(0,0,0,.3), 0 0 80px 20px rgba(255,204,0,.6); transform: rotate(-3deg); }
    #s01-h b { color: #ffcc00; font-weight: 400; }""",
f"""      <div id="s01-fl" class="fl" data-layout-ignore></div>
      <div id="s01-a" class="pl">🤯 Stell dir vor …</div>{b1_h}
      <div id="s01-h">🌊 RED BULL<br><b>TSUNAMI!</b></div>
      {r_h}""",
"""      const re = at("L1", "RED"), rb = at("L1", "TSUNAMI");
      tl.set("#s01-a", { opacity: 1 }, 0);
      tl.fromTo("#s01-a", { scale: 3 }, { scale: 1, duration: .35, ease: "back.out(2.2)" }, 0);
      tl.fromTo("#s01-h", { opacity: 0, scale: 4.5, rotation: 12 }, { opacity: 1, scale: 1, rotation: -3, duration: .3, ease: "back.out(1.6)" }, re - .05);
      tl.to("#s01-h", { scale: 1.1, duration: .14, yoyo: true, repeat: 11, ease: "sine.inOut" }, re + .3);
      tl.fromTo("#s01-fl", { opacity: .9 }, { opacity: 0, duration: .35, immediateRender: false }, rb);
      tl.to("#s01-stage", { x: 18, duration: .04, yoyo: true, repeat: 9, ease: "none" }, rb);
      tl.to("#s01-a", { rotation: 4, duration: .1, yoyo: true, repeat: 7 }, .3);
""" + r_js + b1_js, blur=False)

# s02 – Matcha-Brunnen
b2_h, b2_js = drops("s02-b", 12, 31, 'gr', 540, 900, "🎉", 520, 700)
scene("s02", LILITA + "\n    " + PILL + "\n    " + PT + "\n" + FL + """
    #s02-t { top: 300px; font-size: 54px; background: #3f9b3a; }
    #s02-bs { position: absolute; left: 240px; top: 930px; width: 600px; height: 170px; border-radius: 50%; background: radial-gradient(ellipse at 50% 40%, #b9e87a, #5fae2e 60%, #3c7d1c); box-shadow: 0 0 0 10px #f2e6c8, 0 0 0 16px #2a1b12, 0 0 60px 20px rgba(140,220,90,.8); }
    #s02-cup { position: absolute; left: 0; right: 0; margin: 0 auto; text-align: center; top: 600px; font-size: 380px; line-height: 1; filter: drop-shadow(0 0 40px rgba(140,220,90,.9)); }
    .s02-d { position: absolute; left: 520px; top: 640px; width: 40px; height: 40px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #d8f5b0, #6fbf3a 60%, #3f8a1f); box-shadow: 0 0 0 3px #2a1b12; opacity: 0; }
    #s02-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 1080px; color: #3f9b3a; border-color: #3f9b3a; background: #fff; transform: rotate(-5deg); font-size: 64px; white-space: nowrap; font-family: "Lilita One", sans-serif; }""",
"""      <div id="s02-t" class="pl">🍵 Matcha-Brunnen am Muschelplatz</div>
      <div id="s02-bs" data-layout-ignore></div><div id="s02-cup" data-layout-ignore>🍵</div>""" + "".join(f'<div class="s02-d" id="s02-d{i}" data-layout-ignore></div>' for i in range(26)) + """
      <div id="s02-st" class="stamp" data-layout-ignore>GRATIS FÜR ALLE!</div><div id="s02-fl" class="fl" data-layout-ignore></div>""" + b2_h,
"""      const ma = at("L2", "Matcha-Brunnen"), gr = at("L2", "gratis");
      tl.fromTo("#s02-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, ma - .4);
      tl.fromTo(["#s02-bs", "#s02-cup"], { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .4, ease: "back.out(1.8)" }, ma - .2);
      tl.to("#s02-stage > *", { opacity: 0, duration: .15 }, line("L2")[1] + .15);
      { const R = rng(9); for (let i = 0; i < 26; i++) { const t = ma + .2 + (i % 13) * .2, dx = (R() - .5) * 500, up = 380 + R() * 260;
        tl.fromTo("#s02-d" + i, { opacity: 1, x: 0, y: 0, scale: .6 }, { x: dx * .5, y: -up, scale: 1, duration: .45, ease: "power2.out" }, t);
        tl.to("#s02-d" + i, { x: dx, y: 260, opacity: 0, duration: .7, ease: "power2.in" }, t + .45); } }
      tl.fromTo("#s02-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, gr - .05);
      tl.set("#s02-fl", { backgroundColor: "#9be36b" }, 0); tl.fromTo("#s02-fl", { opacity: .8 }, { opacity: 0, duration: .35, immediateRender: false }, ma);
      tl.to("#s02-stage", { x: 14, duration: .04, yoyo: true, repeat: 7, ease: "none" }, gr);
""" + b2_js, blur=False)

# s03 – Dubai-Schoko, Akku, keine Schule
scene("s03", LILITA + "\n    " + PILL + "\n" + FL + """
    .s03-c { position: absolute; left: 110px; right: 230px; height: 150px; border-radius: 34px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.28); display: flex; align-items: center; gap: 24px; padding: 0 28px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 42px; color: #2a1b12; }
    .s03-c i { font-style: normal; font-size: 84px; }
    .s03-c { height: 130px !important; font-size: 40px !important; }
    #s03-c1 { top: 290px; transform: rotate(-2deg); background: linear-gradient(90deg, #c8e6a0, #fff 60%); }
    #s03-cm { top: 445px; transform: rotate(1.5deg); background: linear-gradient(90deg, #b3202f, #e8565f 60%, #ff9a8a); color: #fff; }
    #s03-c2 { top: 600px; transform: rotate(-1.5deg); }
    #s03-bt { width: 170px; height: 64px; border-radius: 12px; box-shadow: 0 0 0 5px #2a1b12; position: relative; overflow: hidden; background: #eee; flex: none; }
    #s03-bt i { position: absolute; left: 0; top: 0; bottom: 0; width: 8%; background: #e8262f; font-size: 0; }
    #s03-bp { font-size: 46px; }
    #s03-c3 { top: 755px; transform: rotate(1.5deg); }
    #s03-no { left: 520px; top: 765px; color: #e8262f; border-color: #e8262f; background: #fff; transform: rotate(-8deg); font-size: 50px; white-space: nowrap; font-family: "Lilita One", sans-serif; }
    #s03-fe { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 925px; padding: 6px 40px 16px; border-radius: 30px; background: #ffcc00; color: #2a1b12; font-family: "Lilita One", sans-serif; font-size: 80px; line-height: 1; white-space: nowrap; box-shadow: 0 0 0 7px #2a1b12, 0 14px 0 rgba(0,0,0,.3); transform: rotate(-2deg); }""",
"""      <div id="s03-fl" class="fl" data-layout-ignore></div>
      <div id="s03-c1" class="s03-c"><i>🍫</i>Dubai-Schoko überall</div>
      <div id="s03-cm" class="s03-c"><i>🌊</i>Das Meer = Glühwein 🍷</div>
      <div id="s03-c2" class="s03-c"><i>🔋</i><div id="s03-bt"><i id="s03-bi"></i></div><span id="s03-bp">8 %</span></div>
      <div id="s03-c3" class="s03-c"><i>🏫</i>Schule?</div>
      <div id="s03-no" class="stamp" data-layout-ignore>❌ GIBT'S NICHT</div>
      <div id="s03-fe">🏖️ NUR FERIEN!</div>""",
"""      const me = at("L3", "Meer"), du = at("L3", "Dubai-Schokolade"), ak = at("L3", "Akku"), im = at("L3", "immer"), sc = at("L3", "Schule"), ni = at("L3", "nicht"), fe = at("L3", "Ferien");
      [["#s03-c1", du], ["#s03-cm", me], ["#s03-c2", ak], ["#s03-c3", sc]].forEach(([e, t], i) => { tl.fromTo(e, { opacity: 0, scale: .3, x: i % 2 ? 200 : -200 }, { opacity: 1, scale: 1, x: 0, duration: .28, ease: "back.out(2.6)" }, t - .2);
        tl.fromTo(e + " i", { scale: 1.8, rotation: -30 }, { scale: 1, rotation: 0, duration: .4, ease: "elastic.out(1, .4)", immediateRender: false }, t);
        tl.fromTo("#s03-fl", { opacity: .55 }, { opacity: 0, duration: .25, immediateRender: false }, t); });
      tl.to("#s03-stage", { x: 14, duration: .04, yoyo: true, repeat: 7, ease: "none" }, ni);
      tl.to("#s03-bi", { width: "100%", backgroundColor: "#2e9e5b", duration: .6, ease: "power2.out" }, im - .1);
      count(tl, "#s03-bp", 8, 100, im - .1, .6, "", " %");
      tl.fromTo("#s03-no", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, ni - .05);
      tl.fromTo("#s03-fe", { opacity: 0, scale: .3, rotation: -10 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.6)" }, fe - .2);
      tl.to("#s03-fe", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, fe + .3);""")

# s04 – Ihr entscheidet – kommentiert!
scene("s04", LILITA + "\n    " + PILL + """
    #s04-h { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 290px; padding: 6px 40px 16px; border-radius: 30px; background: #fe2c55; color: #fff; font-family: "Lilita One", sans-serif; font-size: 84px; line-height: 1; white-space: nowrap; box-shadow: 0 0 0 7px #2a1b12, 0 14px 0 rgba(0,0,0,.3); transform: rotate(-3deg); }
    #s04-q { top: 420px; font-size: 44px; background: #7b3fe0; }
    #s04-cm { position: absolute; left: 90px; right: 210px; top: 530px; padding: 22px 26px 26px; border-radius: 30px; background: #1f1f1f; box-shadow: 0 0 0 5px #000, 0 14px 26px rgba(0,0,0,.45); font-family: "Inter", sans-serif; color: #fff; display: flex; gap: 20px; }
    #s04-cm .av { width: 74px; height: 74px; border-radius: 50%; flex: none; background: linear-gradient(135deg, #ffd23f, #e8467c); display: grid; place-items: center; font-size: 40px; }
    #s04-cm .nm { font-size: 26px; color: #a8a8a8; font-weight: 600; } #s04-cm .tx { font-size: 36px; font-weight: 600; margin-top: 4px; min-height: 92px; line-height: 1.25; }
    #s04-cm .cu { display: inline-block; width: 4px; height: 38px; background: #fe2c55; vertical-align: -6px; margin-left: 3px; }
    #s04-g { top: 820px; font-size: 42px; background: #e8262f; }
    #s04-lk { margin-left: auto; text-align: center; font-family: "Inter", sans-serif; font-weight: 800; font-size: 26px; color: #a8a8a8; flex: none; }
    #s04-lk span { display: block; font-size: 44px; } #s04-lk { position: relative; } #s04-h1 { position: absolute; left: 0; right: 0; top: 0; opacity: 0; }
    #s04-ar { position: absolute; left: 850px; top: 1230px; font-size: 110px; filter: drop-shadow(0 6px 0 rgba(0,0,0,.35)); }
    #s04-cb { position: absolute; left: 640px; top: 1085px; padding: 4px 18px 8px; border-radius: 999px; background: #fff; color: #fe2c55; font-family: "Inter", sans-serif; font-weight: 900; font-size: 30px; box-shadow: 0 0 0 4px #2a1b12; }""",
"""      <div id="s04-h">👑 IHR ENTSCHEIDET!</div>
      <div id="s04-q" class="pl">Eure verrückteste Idee? 👇</div>
      <div id="s04-cm"><div class="av">🐚</div><div><div class="nm">Du</div><div class="tx"><span id="s04-ty"></span><span class="cu" id="s04-cu"></span></div></div><div id="s04-lk"><span id="s04-h0">🤍</span><span id="s04-h1">❤️</span><b id="s04-ln">0</b></div></div>
      <div id="s04-g" class="pl">❤️ Meiste Likes = nächstes Video!</div>
      <div id="s04-cb" data-layout-ignore>Hier kommentieren</div>
      <div id="s04-ar" data-layout-ignore>👉</div>""",
"""      const mi = at("L4", "meisten"), ih = at("L4", "Ihr"), ve = at("L4", "verrückteste"), sr = at("L4", "Schreibt’s"), ne = at("L4", "nächste");
      tl.fromTo("#s04-h", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, ih - .1);
      tl.fromTo("#s04-q", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ve - .3);
      tl.fromTo("#s04-cm", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, sr - .3);
      const TXT = "Matcha-Brunnen + Red-Bull-Regen pls 🙏💚", ty = document.getElementById("s04-ty"), o = { n: 0 };
      tl.to(o, { n: Array.from(TXT).length, duration: 1.6, ease: "none", onUpdate: () => { ty.textContent = Array.from(TXT).slice(0, Math.round(o.n)).join(""); } }, sr);
      tl.to("#s04-cu", { opacity: 0, duration: .25, yoyo: true, repeat: 11, ease: "steps(1)" }, sr);
      tl.fromTo("#s04-g", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, mi - .2);
      tl.set("#s04-h1", { opacity: 1 }, mi);
      tl.fromTo("#s04-h1", { scale: 2.2 }, { scale: 1, duration: .35, ease: "back.out(3)", immediateRender: false }, mi);
      count(tl, "#s04-ln", 0, 12480, mi, 1.4, "", "", "power2.in");
      tl.to("#s04-g", { scale: 1.07, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, ne);
      tl.fromTo(["#s04-ar", "#s04-cb"], { opacity: 0 }, { opacity: 1, duration: .25 }, sr);
      tl.to("#s04-ar", { x: 40, duration: .3, yoyo: true, repeat: 11, ease: "sine.inOut" }, sr + .2);""")

# s05 – Folg mir
r2_h, r2_js = rain("s05-c", 90, 8, '0', 'C.__dur')
scene("s05", PILL + "\n" + FOLLOW + "\n    " + CAN + """
    #s05-t { top: 300px; font-size: 50px; background: #18a6b8; }
    #s05-btn { top: 430px; } #s05-hand { left: 690px; top: 480px; }
    #s05-r { top: 600px; font-size: 42px; background: #2e9e5b; }""",
f"""      <div id="s05-t" class="pl">🏝️ Folg mir & zieh nach Muschel-Tal!</div>
      <div id="s05-btn" class="fbtn">+ Folgen<div id="s05-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s05-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s05-r" class="pl">🏡 Deine Hütte wartet – mit deinem @Namen!</div>
      {r2_h}""",
"""      const fo = at("L5", "Folg"), rb = at("L5", "Muschel-Tal"), da = at("L5", "Hütte");
      tl.fromTo("#s05-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, fo - .4);
      tl.fromTo("#s05-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .3);
      tl.fromTo("#s05-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .1);
      tl.to("#s05-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .2);
      tl.to("#s05-btn2", { opacity: 1, duration: .05 }, fo + .3);
      tl.fromTo("#s05-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .3);
      tl.to("#s05-hand", { opacity: 0, duration: .25 }, fo + .8);
      tl.fromTo("#s05-r", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, da - .3);
""" + r2_js, blur=False)
