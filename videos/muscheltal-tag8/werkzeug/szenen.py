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
QL = [[("NUR", "Nur"), ("NOCH", "noch"), ("50", "50")], [("FOLLOWER –", "Follower")], [("DANN", "dann"), ("RETTEN", "retten"), ("WIR", "wir")], [("HUNDERTE", "hunderte")], [("TIERE!", "Tiere")]]
QW = [w for ln in QL for w in ln]
YW = ("50", "HUNDERTE", "TIERE!")
SP = [(110, 560, 46), (900, 600, 34), (70, 960, 30), (930, 1010, 44), (180, 1230, 38), (820, 1200, 30)]
scene("s01", LILITA + "\n    " + PT + "\n" + FL + """
    #s01-ray { position: absolute; left: -460px; top: 300px; width: 2000px; height: 2000px; border-radius: 50%; background: repeating-conic-gradient(rgba(255,250,210,.28) 0 8deg, rgba(255,255,255,0) 8deg 20deg); -webkit-mask: radial-gradient(circle, #000 15%, transparent 60%); }
    #s01-hk { position: absolute; left: 40px; right: 40px; top: 600px; text-align: center; font-family: "Lilita One", sans-serif; }
    #s01-hk .ln { display: block; width: fit-content; margin: 0 auto 16px; padding: 4px 34px 14px; border-radius: 30px; background: #ff2e7e; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.35); font-size: 104px; line-height: 1.05; white-space: nowrap; transform-origin: 50% 60%; }
    #s01-hk span { position: relative; display: inline-block; margin: 0 .08em; color: #fff; -webkit-text-stroke: 8px #1a0f08; paint-order: stroke fill; transform-origin: 50% 65%; }
    #s01-gk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 420px; padding: 8px 30px 16px; border-radius: 26px; background: #2e9e5b; border: 8px solid #fff; box-shadow: 0 0 0 6px #1a0f08, 0 12px 0 rgba(0,0,0,.3), 0 0 60px 20px rgba(80,230,140,.7); font-family: "Lilita One", sans-serif; font-size: 68px; line-height: 1; color: #fff; white-space: nowrap; transform: rotate(-4deg); }
    #s01-gk span { display: inline-block; }
    #s01-rv { position: absolute; inset: 0; box-shadow: inset 0 0 140px 50px rgba(255,10,20,.9); opacity: 0; }
    .s01-sp { position: absolute; color: #fff; text-shadow: 0 0 18px #fff, 0 0 30px #ffe14a; opacity: 0; line-height: 1; }""",
"""      <div id="s01-ray" data-layout-ignore></div>
      <div id="s01-fl" class="fl" data-layout-ignore></div>
      <div id="s01-rv" data-layout-ignore></div>
      
      <div id="s01-hk">""" + "".join('<div class="ln" id="s01-l' + str(j) + '">' + "".join(f'<span id="s01-w{QW.index(w)}">{w[0]}</span>' for w in ln) + '</div>' for j, ln in enumerate(QL)) + """</div>
      """ + "".join(f'<div class="s01-sp" id="s01-sp{k}" data-layout-ignore style="left:{x}px;top:{y}px;font-size:{f}px">✦</div>' for k, (x, y, f) in enumerate(SP)) + drops("s01-p", 22, 5, 'sc', 540, 900, "🐾", 600, 820)[0],
"""      const sc = at("L1", "Tiere");
      tl.set(["#s01-ray"], { opacity: 1 }, 0);
      tl.fromTo("#s01-ray", { rotation: 0 }, { rotation: 40, duration: 4, ease: "none" }, 0);
      tl.fromTo("#s01-rv", { opacity: .45 }, { opacity: 1, duration: .14, yoyo: true, repeat: 17, ease: "sine.inOut", immediateRender: false }, 0);
      
      """ + "\n      ".join(
        f'tl.set("#s01-w{i}", {{ zIndex: 5 }}, at("L1", "{k}") - .03); tl.to("#s01-w{i}", {{ scale: {1.35 if len(w) > 7 else (1.38 if len(w) <= 5 else 1.5)}, rotation: {(-1)**i * 3}, duration: .1, ease: "back.out(3)" }}, at("L1", "{k}") - .03); tl.to("#s01-w{i}", {{ scale: 1, rotation: 0, duration: .22, ease: "power2.inOut" }}, at("L1", "{k}") + .17); tl.set("#s01-w{i}", {{ zIndex: 0 }}, at("L1", "{k}") + .4);'
        + (f' tl.to("#s01-w{i}", {{ color: "#ffe500", duration: .05 }}, at("L1", "{k}") - .02);' if w in YW else '')
        for i, (w, k) in enumerate(QW)) + """
      """ + "\n      ".join(f'tl.fromTo("#s01-sp{k}", {{ opacity: 0, scale: .2, rotation: 0 }}, {{ opacity: 1, scale: 1, rotation: 90, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }}, {k * .2:.2f});' for k in range(len(SP))) + """
      tl.fromTo("#s01-fl", { opacity: .9 }, { opacity: 0, duration: .45, immediateRender: false }, sc);
      tl.to("#s01-l4", { scale: 1.12, duration: .12, yoyo: true, repeat: 1 }, sc);
      
      tl.to("#s01-hk", { x: 12, duration: .04, yoyo: true, repeat: 5, ease: "none" }, sc);
""" + drops("s01-p", 22, 5, 'sc', 540, 900, "🐾", 600, 820)[1])

# s01b – Das ist Muschel-Tal: die Welt, in der ihr alles entscheidet
scene("s01b", LILITA + "\n    " + PILL + """
    #s1b-lg { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 300px; font-family: "Lilita One", sans-serif; font-size: 150px; line-height: 1; color: #fff; -webkit-text-stroke: 16px #1a0f08; paint-order: stroke fill; filter: drop-shadow(0 12px 0 rgba(0,0,0,.3)); }
    #s1b-lg b { font-weight: 400; color: #ffe14a; }
    #s1b-e { top: 480px; font-size: 50px; background: linear-gradient(100deg, #ff2e7e, #7b3fe0); }""",
"""      <div id="s1b-lg" data-layout-ignore>MUSCHEL-<b>TAL</b></div>
      <div id="s1b-e" class="pl">🏠 Folgen = Hütte mit deinem @Namen</div>""",
"""      const t0 = line("L1b")[0], mu = at("L1b", "Muschel-Tal"), en = at("L1b", "Hütte");
      tl.fromTo("#s1b-lg", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(1.8)" }, mu - .15);
      tl.fromTo("#s1b-e", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, en - .2);
      tl.to("#s1b-e", { scale: 1.08, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut" }, en + .3);""")


SLOT_CSS = """    .sl-dim { position: absolute; inset: 0; background: rgba(10,12,40,.5); }
    .sl-box { position: absolute; left: 190px; width: 700px; top: 480px; height: 390px; border-radius: 34px; background: #fff; overflow: hidden; box-shadow: 0 0 0 7px #2a1b12, 0 0 0 14px #ffc93c, 0 0 0 19px #2a1b12, 0 18px 0 rgba(0,0,0,.35); }
    .sl-band { position: absolute; left: 0; right: 0; top: 130px; height: 130px; background: #fff3c4; border-top: 5px solid #ffc93c; border-bottom: 5px solid #ffc93c; }
    .sl-col { position: absolute; left: 0; right: 0; top: 0; }
    .sl-r { height: 130px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #23285a; white-space: nowrap; }
    .sl-sh { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,.95)); }
    .sl-fv { position: absolute; left: 60px; width: 960px; top: 905px; text-align: center; white-space: nowrap; font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; color: #fff; text-shadow: 0 2px 6px rgba(0,0,0,.6); }"""
def names(f): return (D.parent / "werkzeug" / f).read_text().split()
def slot_col(cid, ns): return f'<div class="sl-col" id="{cid}">' + "".join(f'<div class="sl-r" id="{cid}-{i}">@{n}</div>' for i, n in enumerate(ns)) + "</div>"
def slot_js(cid, band, ns, w, t0, tb):
    W = ns.index(w)
    return f"""      {{ const T0 = {t0}, TB = {tb}, H = 130, W = {W}, T1 = TB - 1.1;
      tl.set("#{cid}", {{ y: 0 }}, 0);
      tl.fromTo("#{cid}", {{ y: 0 }}, {{ y: -(W - 9) * H, duration: T1 - T0, ease: "none", immediateRender: false }}, T0);
      tl.fromTo("#{cid}", {{ y: -(W - 9) * H }}, {{ y: -(W - 1) * H, duration: 1.1, ease: "power3.out", immediateRender: false }}, T1);
      tl.fromTo("#{cid}", {{ filter: "blur(5px)" }}, {{ filter: "blur(0px)", duration: 1.0, ease: "power2.in", immediateRender: false }}, T1);
      tl.to("#{cid}-" + W, {{ color: "#2e9e5b", scale: 1.15, duration: .2, ease: "back.out(3)" }}, TB);
      tl.to("#{band}", {{ backgroundColor: "#7dff9e", duration: .15, yoyo: true, repeat: 5 }}, TB); }}
"""


# s02 – Streuner + Tierheim: 750 / 800
scene("s02", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s2-s { top: 280px; font-size: 54px; background: #e8262f; }
    #s2-h { position: absolute; left: 70px; right: 70px; top: 280px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s2-h .r { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 42px; } #s2-h .r b { font-size: 66px; color: #2e9e5b; }
    #s2-h .bar { height: 30px; border-radius: 15px; background: #ece4d8; margin-top: 10px; overflow: hidden; } #s2-h .bar i { display: block; height: 100%; width: 0; border-radius: 15px; background: linear-gradient(90deg, #2e9e5b, #8be06a); }
    #s2-h .f { margin-top: 8px; font-weight: 900; font-size: 34px; color: #e2560c; }
    #s2-ff { top: 560px; font-size: 54px; background: linear-gradient(100deg, #ff6a1a, #ff2e7e); }""",
"""      <div id="s2-s" class="pl">🐱🐶 Streuner überall!</div>
      <div id="s2-h"><div class="r"><div>🐾 Tierheim Pfotenkuss</div><div><b id="s2-n">0</b> / 800</div></div><div class="bar"><i id="s2-b"></i></div><div class="f">Bei 800 Bewohnern wird gebaut</div></div>
      <div id="s2-ff" class="pl">🔥 Nur noch 50!</div>""",
"""      const t2 = line("L2")[0], t2b = line("L2b")[0], wi = at("L2b", "750"), fu = at("L2b", "50");
      tl.fromTo("#s2-s", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, t2);
      tl.to("#s2-s", { x: 10, duration: .05, yoyo: true, repeat: 7, ease: "none" }, t2 + .4);
      tl.to("#s2-s", { opacity: 0, y: -30, duration: .2 }, t2b - .25);
      tl.fromTo("#s2-h", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, t2b - .1);
      count(tl, "#s2-n", 0, 750, t2b + .2, wi - t2b + .2, "", "", "power2.out");
      tl.fromTo("#s2-b", { width: "0%" }, { width: "93.75%", duration: wi - t2b + .2, ease: "power2.out" }, t2b + .2);
      tl.fromTo("#s2-ff", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fu - .2);
      tl.to("#s2-ff", { scale: 1.1, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, fu + .2);""")

# s03 – Drei Live-Verlosungen: Boba Beach, Coast & Cotton, Coco Bay
JB = [("L3a", "L3aw", "🧋 Boba Beach", "Bubble-Tea-Bude am Steg", "hanna.013", "#d4469c"), ("L3b", "L3bw", "👗 Coast & Cotton", "Modeboutique · Kokos-Küste", "pxlinx.022", "#7b3fe0"), ("L3c", "L3cw", "🍹 Coco Bay", "Beach-Bar am Südstrand", "haylie.aeriana", "#ff6a1a")]
NSS = [names(f"slot_{i}.txt") for i in range(3)]
scene("s03", LILITA + "\n    " + PILL + "\n    " + CF_CSS.replace("top: 700px", "top: 640px") + "\n" + SLOT_CSS + """
    #s3-lv { top: 280px; font-size: 52px; background: #e8262f; }
    .s3-o { top: 280px; font-size: 58px; font-family: "Lilita One", sans-serif; font-weight: 400; }
    .s3-d { top: 385px; font-size: 40px; background: #fff; color: #2a1b12; }
    .s3-w { top: 900px; font-size: 48px; background: #2e9e5b; }""",
"""      <div id="s3-dim" class="sl-dim"></div>
      <div id="s3-lv" class="pl">🔴 LIVE: 3 Jobs zu gewinnen!</div>
      """ + "\n      ".join(f'<div id="s3-o{i}" class="pl s3-o" style="background:{c}">{o}</div><div id="s3-d{i}" class="pl s3-d">{t}</div>' for i, (a, w, o, t, n, c) in enumerate(JB)) + """
      <div id="s3-box" class="sl-box"><div id="s3-band" class="sl-band"></div>""" + "".join(slot_col(f"s3-c{i}", NSS[i]) for i in range(3)) + """<div class="sl-sh" data-layout-ignore></div></div>
      """ + "".join(f'<div id="s3-cf{i}"></div>' for i in range(3)) + "\n      " + "\n      ".join(f'<div id="s3-w{i}" class="pl s3-w">🎉 @{n} arbeitet jetzt hier!</div>' for i, (a, w, o, t, n, c) in enumerate(JB)),
"""      const t3 = line("L3")[0];
      tl.fromTo("#s3-lv", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, t3);
      tl.to("#s3-lv", { opacity: 0, duration: .2 }, line("L3a")[0] - .3);
      tl.set(["#s3-c1", "#s3-c2"], { opacity: 0 }, 0);
""" + "".join(f"""      tl.fromTo("#s3-o{i}", {{ opacity: 0, scale: 2.2 }}, {{ opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }}, line("{a}")[0] - .1);
      tl.fromTo("#s3-d{i}", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }}, line("{a}")[0] + .4);
      tl.fromTo("#s3-dim", {{ opacity: {0 if i == 0 else .0} }}, {{ opacity: 1, duration: .25, immediateRender: false }}, line("{a}")[1] + .05);
      tl.fromTo("#s3-box", {{ opacity: 0, scale: .5 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)", immediateRender: false }}, line("{a}")[1] + .05);
      tl.set(["#s3-c0", "#s3-c1", "#s3-c2"], {{ opacity: 0 }}, line("{a}")[1]); tl.set("#s3-c{i}", {{ opacity: 1 }}, line("{a}")[1]); tl.set("#s3-band", {{ backgroundColor: "#fff3c4" }}, line("{a}")[1]);
""" + slot_js(f"s3-c{i}", "s3-band", NSS[i], n, f'line("{a}")[1] + .2', f'line("{w}")[0] - .25') + "      { " + CONF_JS.replace("SEED", str(81 + i)).replace("BOX", f"s3-cf{i}").replace("T0", f'(line("{w}")[0] - .25)') + " }\n" + f"""      tl.to(["#s3-box", "#s3-dim"], {{ opacity: 0, duration: .25 }}, line("{w}")[1] + .2);
      tl.fromTo("#s3-w{i}", {{ opacity: 0, scale: .4 }}, {{ opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }}, line("{w}")[1] + .2);
      tl.to(["#s3-w{i}", "#s3-o{i}", "#s3-d{i}"], {{ opacity: 0, duration: .2 }}, {f'line("{JB[i+1][0]}")[0] - .3' if i < 2 else f'line("{w}")[1] + 2.0'});
""" for i, (a, w, o, t, n, c) in enumerate(JB)))

# s04 – Die LIVE-Insel: eigene Insel, getrennt von Muschel-Tal
scene("s04", LILITA + "\n    " + PILL + "\n    " + BIG + """
    #s4-b { top: 270px; font-size: 88px; background: #e8101e; transform: rotate(-2deg); box-shadow: 0 0 0 8px #2a1b12, 0 16px 0 rgba(0,0,0,.3), 0 0 50px 14px rgba(255,20,30,.6); }
    #s4-dot { display: inline-block; width: 44px; height: 44px; border-radius: 50%; background: #fff; margin-right: 16px; vertical-align: 6px; }
    #s4-e { top: 430px; font-size: 46px; background: #fff; color: #2a1b12; }
    #s4-g { top: 520px; font-size: 44px; background: #7b3fe0; }""",
"""      <div id="s4-b" class="big"><span id="s4-dot"></span>LIVE-INSEL</div>
      <div id="s4-e" class="pl">🏝️ Eine eigene Insel</div>
      <div id="s4-g" class="pl">↔️ Getrennt von der Muschel-Tal-Region</div>""",
"""      const t4 = line("L4")[0], ei = at("L4", "eigenen"), ge = at("L4", "getrennt");
      tl.fromTo("#s4-b", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(1.8)" }, t4 - .05);
      tl.to("#s4-dot", { opacity: .15, duration: .25, yoyo: true, repeat: 13, ease: "steps(1)" }, t4 + .3);
      tl.fromTo("#s4-e", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, ei - .2);
      tl.fromTo("#s4-g", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, ge - .2);""")

# s05 – Folg mir: der 800. sein
scene("s05", LILITA + "\n    " + PILL + "\n" + FOLLOW + """
    #s5-btn { top: 280px; } #s5-hand { left: 690px; top: 330px; }
    #s5-t { top: 430px; font-size: 64px; background: linear-gradient(135deg, #2e9e5b, #8be06a); font-family: "Lilita One", sans-serif; font-weight: 400; transform: rotate(-2deg); }
    #s5-h { top: 560px; font-size: 44px; background: #fff; color: #2e9e5b; }""",
"""      <div id="s5-btn" class="fbtn">+ Folgen<div id="s5-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s5-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s5-t" class="pl">🐾 Sei der 800. Bewohner!</div>
      <div id="s5-h" class="pl">🏠 Tierheim eröffnen – Tiere retten</div>""",
"""      const t5 = line("L5")[0], fo = at("L5", "Folg"), du = at("L5", "du"), ti = at("L5", "Tierheim");
      tl.fromTo("#s5-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, t5 - .15);
      tl.fromTo("#s5-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, t5);
      tl.to("#s5-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .2);
      tl.to("#s5-btn2", { opacity: 1, duration: .05 }, fo + .3);
      tl.to("#s5-hand", { opacity: 0, duration: .2 }, fo + .7);
      tl.fromTo("#s5-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, du - .2);
      tl.to("#s5-t", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, du + .3);
      tl.fromTo("#s5-h", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .28, ease: "back.out(2)" }, ti - .3);""", blur=False)
