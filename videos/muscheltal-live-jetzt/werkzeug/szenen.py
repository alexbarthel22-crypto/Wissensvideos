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


# s01 – Hook im Stil von Tag 1: pinke Balken, Wörter springen groß hervor, Sticker „GEBAUT!“
QL = [[("ICH", "Ich"), ("BIN", "bin")], [("GERADE", "gerade")], [("LIVE!", "LIVE")], [("KOMM", "komm"), ("REIN!", "rein")]]
QW = [w for ln in QL for w in ln]
YW = ("GERADE", "LIVE!", "REIN!")
SP = [(110, 560, 46), (900, 600, 34), (70, 960, 30), (930, 1010, 44), (180, 1230, 38), (820, 1200, 30)]
scene("s01", LILITA + "\n    " + PT + "\n" + FL + """
    #s01-ray { position: absolute; left: -460px; top: 300px; width: 2000px; height: 2000px; border-radius: 50%; background: repeating-conic-gradient(rgba(255,250,210,.28) 0 8deg, rgba(255,255,255,0) 8deg 20deg); -webkit-mask: radial-gradient(circle, #000 15%, transparent 60%); }
    #s01-hk { position: absolute; left: 40px; right: 40px; top: 560px; text-align: center; font-family: "Lilita One", sans-serif; }
    #s01-hk .ln { display: block; width: fit-content; margin: 0 auto 16px; padding: 4px 34px 14px; border-radius: 30px; background: #ff2e7e; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.35); font-size: 104px; line-height: 1.05; white-space: nowrap; transform-origin: 50% 60%; }
    #s01-hk span { position: relative; display: inline-block; margin: 0 .08em; color: #fff; -webkit-text-stroke: 8px #1a0f08; paint-order: stroke fill; transform-origin: 50% 65%; }
    #s01-gk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 420px; padding: 8px 30px 16px; border-radius: 26px; background: #2e9e5b; border: 8px solid #fff; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.3), 0 0 60px 20px rgba(80,230,140,.7); font-family: "Lilita One", sans-serif; font-size: 68px; line-height: 1; color: #fff; white-space: nowrap; transform: rotate(-4deg); }
    #s01-gk span { display: inline-block; }
    #s01-av { position: absolute; left: 0; right: 0; margin: 0 auto; top: 250px; width: 230px; height: 260px; }
    #s01-ring { position: absolute; left: 15px; top: 0; width: 200px; height: 200px; border-radius: 50%; background: conic-gradient(#ff1f4b, #ff6a1a, #ff1f4b, #ff2e7e, #ff1f4b); box-shadow: 0 0 40px 10px rgba(255,30,70,.7); }
    #s01-pic { position: absolute; left: 31px; top: 16px; width: 168px; height: 168px; border-radius: 50%; overflow: hidden; background: #fff; border: 6px solid #fff; }
    #s01-pic svg { width: 100%; height: 100%; }
    #s01-lb { position: absolute; left: 0; right: 0; margin: 0 auto; top: 176px; width: fit-content; padding: 2px 22px 6px; border-radius: 12px; background: #ff1f4b; border: 5px solid #fff; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; letter-spacing: .04em; }
    #s01-rv { position: absolute; inset: 0; box-shadow: inset 0 0 140px 50px rgba(255,10,20,.9); opacity: 0; }
    .s01-sp { position: absolute; color: #fff; text-shadow: 0 0 18px #fff, 0 0 30px #ffe14a; opacity: 0; line-height: 1; }""",
"""      <div id="s01-ray" data-layout-ignore></div>
      <div id="s01-fl" class="fl" data-layout-ignore></div>
      <div id="s01-rv" data-layout-ignore></div>
      <div id="s01-av" data-layout-ignore><div id="s01-ring"></div><div id="s01-pic">""" + LOGO + """</div><div id="s01-lb">LIVE</div></div>
      
      <div id="s01-hk">""" + "".join('<div class="ln" id="s01-l' + str(j) + '">' + "".join(f'<span id="s01-w{QW.index(w)}">{w[0]}</span>' for w in ln) + '</div>' for j, ln in enumerate(QL)) + """</div>
      """ + "".join(f'<div class="s01-sp" id="s01-sp{k}" data-layout-ignore style="left:{x}px;top:{y}px;font-size:{f}px">✦</div>' for k, (x, y, f) in enumerate(SP)) + drops("s01-p", 0, 5, 'sc', 540, 900, "🎉", 600, 820)[0],
"""      const sc = at("L1", "rein");
      tl.set(["#s01-ray"], { opacity: 1 }, 0);
      tl.fromTo("#s01-ray", { rotation: 0 }, { rotation: 40, duration: 4, ease: "none" }, 0);
      tl.fromTo("#s01-ring", { scale: 1, rotation: 0 }, { scale: 1.12, rotation: 40, duration: .3, yoyo: true, repeat: 9, ease: "sine.inOut" }, 0);
      tl.fromTo("#s01-lb", { scale: 1 }, { scale: 1.15, duration: .3, yoyo: true, repeat: 9, ease: "sine.inOut" }, 0);
      tl.fromTo("#s01-rv", { opacity: .45 }, { opacity: 1, duration: .14, yoyo: true, repeat: 17, ease: "sine.inOut", immediateRender: false }, 0);
      
      """ + "\n      ".join(
        f'tl.set("#s01-w{i}", {{ zIndex: 5 }}, at("L1", "{k}") - .03); tl.to("#s01-w{i}", {{ scale: 1.12, rotation: {(-1)**i * 3}, duration: .1, ease: "back.out(3)" }}, at("L1", "{k}") - .03); tl.to("#s01-w{i}", {{ scale: 1, rotation: 0, duration: .22, ease: "power2.inOut" }}, at("L1", "{k}") + .17); tl.set("#s01-w{i}", {{ zIndex: 0 }}, at("L1", "{k}") + .4);'
        + (f' tl.to("#s01-w{i}", {{ color: "#ffe500", duration: .05 }}, at("L1", "{k}") - .02);' if w in YW else '')
        for i, (w, k) in enumerate(QW)) + """
      """ + "\n      ".join(f'tl.fromTo("#s01-sp{k}", {{ opacity: 0, scale: .2, rotation: 0 }}, {{ opacity: 1, scale: 1, rotation: 90, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {k * .2:.2f});' for k in range(len(SP))) + """
      tl.fromTo("#s01-fl", { opacity: .9 }, { opacity: 0, duration: .45, immediateRender: false }, sc);
      tl.to("#s01-l3", { scale: 1.12, duration: .12, yoyo: true, repeat: 1 }, sc);
      
      tl.to("#s01-hk", { x: 12, duration: .04, yoyo: true, repeat: 5, ease: "none" }, sc);
""" + drops("s01-p", 0, 5, 'sc', 540, 900, "🎉", 600, 820)[1])

# s04 – LIVE-Insel: wir bauen weiter, 87 Häuser, Krankenhaus, Rangliste, Profilbild
scene("s04", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s4-b { top: 270px; font-size: 88px; background: #e8101e; transform: rotate(-2deg); box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3), 0 0 50px 14px rgba(255,20,30,.6); }
    #s4-dot { display: inline-block; width: 44px; height: 44px; border-radius: 50%; background: #fff; margin-right: 16px; vertical-align: 6px; }
    #s4-e { top: 430px; font-size: 46px; background: #fff; color: #2a1b12; }
    #s4-pa { position: absolute; left: 928px; top: 950px; width: 130px; height: 150px; }
    #s4-ring { position: absolute; left: 5px; top: 0; width: 120px; height: 120px; border-radius: 50%; background: conic-gradient(#ff1f4b, #ff6a1a, #ff1f4b, #ff2e7e, #ff1f4b); box-shadow: 0 0 40px 10px rgba(255,30,70,.8); }
    #s4-pic { position: absolute; left: 15px; top: 10px; width: 100px; height: 100px; border-radius: 50%; overflow: hidden; background: #fff; border: 4px solid #fff; }
    #s4-pic svg { width: 100%; height: 100%; }
    #s4-lb { position: absolute; left: 0; right: 0; margin: 0 auto; top: 108px; width: fit-content; padding: 1px 12px 4px; border-radius: 8px; background: #ff1f4b; border: 3px solid #fff; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 24px; }
    #s4-ph { left: auto; right: 12px; margin: 0; top: 1124px; font-size: 26px; padding: 5px 13px 8px; background: #ff1f4b; box-shadow: 0 0 0 5px #fff, 0 10px 0 rgba(0,0,0,.25); }
    #s4-z { top: 290px; font-size: 38px; background: #fff; color: #2a1b12; }
    #s4-l { top: 380px; font-size: 48px; background: #e8467c; }
    #s4-r { position: absolute; left: 90px; right: 90px; top: 290px; padding: 16px 26px 20px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s4-r .rh { font-family: "Lilita One", sans-serif; font-size: 50px; text-align: center; color: #e2560c; margin-bottom: 6px; }
    #s4-r .rr { display: flex; align-items: center; gap: 16px; font-weight: 900; font-size: 40px; padding: 6px 0; border-top: 3px solid #f1e6d6; }
    #s4-r .rr b { font-size: 50px; } #s4-r .rr span { flex: 1; } #s4-r .rr i { font-style: normal; font-size: 30px; color: #7b3fe0; }
    #s4-h { top: 290px; font-size: 34px; background: #e8467c; }""",
"""      <div id="s4-b" class="big"><span id="s4-dot"></span>LIVE-INSEL</div>
      <div id="s4-e" class="pl">🏗️ Wir bauen gerade weiter!</div>
      <div id="s4-z" class="pl">🏠 87 Häuser · 🏫 Schule · 🎬 Kino · 🐠 Aquarium</div>
      <div id="s4-l" class="pl">🏥 Als Nächstes: Krankenhaus!</div>
      <div id="s4-h" class="pl">🏠 Dein eigenes Haus – jeder ❤️ lässt es wachsen!</div>
      <div id="s4-pa" data-layout-ignore><div id="s4-ring"></div><div id="s4-pic">""" + LOGO + """</div><div id="s4-lb">LIVE</div></div>
      <div id="s4-ph" class="pl">👆 Tippen!</div>
      <div id="s4-r"><div class="rh">🏆 Größte Häuser im LIVE</div>
        <div class="rr"><b>🥇</b><span>@anna_hahnlbichler</span><i>Stufe 26</i></div>
        <div class="rr"><b>🥈</b><span>@ju1e_smt</span><i>Stufe 23</i></div>
        <div class="rr"><b>🥉</b><span>@_marydoesart_</span><i>Stufe 22</i></div></div>""",
"""      const t4 = line("L4")[0], ei = at("L4", "weiter");
      tl.fromTo("#s4-b", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, t4 - .05);
      tl.to("#s4-dot", { opacity: .15, duration: .25, yoyo: true, repeat: 13, ease: "steps(1)" }, t4 + .3);
      tl.fromTo("#s4-e", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, ei - .2);
      const tb = line("L4b")[0], li = at("L4b", "Krankenhaus"), tc = line("L4c")[0];
      tl.to(["#s4-b", "#s4-e"], { opacity: 0, y: -30, duration: .2 }, tb - .25);
      tl.fromTo("#s4-z", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, at("L4b", "87") - .2);
      tl.fromTo("#s4-l", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, li - .4);
      tl.to(["#s4-z", "#s4-l"], { opacity: 0, y: -30, duration: .2 }, tc - .25);
      tl.fromTo("#s4-r", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, tc - .1);
      const te = line("L4e")[0], td = line("L4d")[0];
      tl.to("#s4-r", { opacity: 0, y: -30, duration: .2 }, te - .25);
      tl.fromTo("#s4-h", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, at("L4e", "eigenes") - .2);
      tl.to("#s4-h", { opacity: 0, y: -30, duration: .2 }, td - .25);
      tl.fromTo("#s4-pa", { opacity: 0, scale: .2 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, at("L4d", "rechts") - .2);
      tl.fromTo("#s4-ring", { scale: 1, rotation: 0 }, { scale: 1.15, rotation: 40, duration: .3, yoyo: true, repeat: 9, ease: "sine.inOut" }, at("L4d", "rechts"));
      tl.fromTo("#s4-ph", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, at("L4d", "Profilbild") - .1);
      tl.to("#s4-ph", { y: -12, duration: .25, yoyo: true, repeat: 7, ease: "sine.inOut" }, at("L4d", "Profilbild") + .3);
      tl.fromTo("#s4-r .rr", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: .25, stagger: .45, ease: "back.out(2)" }, at("L4c", "Anna") - .15);""")

