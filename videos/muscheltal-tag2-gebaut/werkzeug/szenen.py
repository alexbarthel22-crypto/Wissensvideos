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


NAMES = (D.parent / "werkzeug" / "slot_names.txt").read_text().split()
WIN = NAMES.index("prvt.lott1")
PILL = """.pl { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; padding: 8px 28px 12px; border-radius: 999px; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); white-space: nowrap; }"""

# s01 – Hook + 653 Bewohner, Kokos-Küste 148
scene("s01", LILITA + "\n    " + PILL + """
    #s01-c { position: absolute; left: 0; right: 0; margin: 0 auto; top: 300px; width: fit-content; padding: 6px 40px 12px; border-radius: 40px; background: #fff; border: 7px solid #ff6a1a;
      font-family: "Inter", sans-serif; color: #0a78c2; font-weight: 900; font-size: 44px; display: flex; flex-direction: column; align-items: center; line-height: 1; box-shadow: 0 12px 0 rgba(0,40,80,.3); }
    #s01-c b { font-size: 130px; color: #ff6a1a; line-height: 1; }
    #s01-p { top: 300px; left: 760px; right: auto; margin: 0; font-size: 46px; background: #2e9e5b; transform: rotate(8deg); }
    #s01-k { top: 560px; font-size: 46px; background: #18b8c0; }
    #s01-ray { position: absolute; left: -660px; top: 140px; width: 2400px; height: 2400px; border-radius: 50%;
      background: repeating-conic-gradient(from 0deg, rgba(255,255,255,.16) 0deg 5deg, rgba(255,255,255,0) 5deg 15deg);
      -webkit-mask-image: radial-gradient(circle, #000 0%, #000 30%, transparent 62%); mask-image: radial-gradient(circle, #000 0%, #000 30%, transparent 62%); }
    #s01-tint { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,60,120,0) 35%, rgba(10,60,120,.45) 100%); }
    #s01-fl { position: absolute; inset: 0; background: #fff; opacity: 0; }
    #s01-stk { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 300px; padding: 4px 30px 10px; border-radius: 22px; background: #fff; color: #ff2e7e;
      font-family: "Lilita One", sans-serif; font-size: 64px; border: 5px solid #ff2e7e; box-shadow: 0 8px 0 rgba(0,0,0,.2); transform: rotate(-6deg); }
    #s01-hk { position: absolute; left: 0; right: 0; top: 430px; text-align: center; }
    .hk-l { display: table; margin: 16px auto 0; background: #ff2e7e; border-radius: 34px; padding: 4px 34px 14px; font-family: "Lilita One", sans-serif; font-size: 112px; line-height: 1.05; color: #fff; box-shadow: 0 9px 0 rgba(0,0,0,.25); }
    .hk-w { display: inline-block; margin: 0 .1em; transform-origin: 50% 60%; }
    .hk-sp { position: absolute; width: 70px; height: 70px; }""",
"""      <div id="s01-ray"></div><div id="s01-tint"></div>
      <div id="s01-stk">EINGEZOGEN!</div>
      <div id="s01-hk"><div class="hk-l"><span class="hk-w" id="hw0">DU</span><span class="hk-w" id="hw1">WOHNST</span></div><div class="hk-l"><span class="hk-w" id="hw2">AB</span><span class="hk-w" id="hw3">JETZT</span></div><div class="hk-l"><span class="hk-w" id="hw4">AUF</span><span class="hk-w" id="hw5">MEINER</span></div><div class="hk-l"><span class="hk-w" id="hw6">INSEL!</span></div></div>
      <svg class="hk-sp" style="left:90px;top:520px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#fff"/></svg>
      <svg class="hk-sp" style="left:900px;top:640px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#ffd23f"/></svg>
      <svg class="hk-sp" style="left:140px;top:880px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#ffd23f"/></svg>
      <svg class="hk-sp" style="left:850px;top:930px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#fff"/></svg>
      <div id="s01-fl"></div>
      <div id="s01-c"><b id="s01-n">575</b>BEWOHNER</div>
      <div id="s01-p" class="pl">+78</div>
      <div id="s01-k" class="pl">🥥 Kokos-Küste: 148</div>""",
"""      const hkw = ["Du", "wohnst", "ab", "jetzt", "auf", "meiner", "Insel"], hEnd = line("L1")[1], ins = at("L1", "Insel");
      tl.set(["#s01-hk", "#s01-stk", "#s01-ray", "#s01-tint"], { opacity: 1 }, 0);
      tl.fromTo("#s01-ray", { rotation: 0 }, { rotation: 24, duration: hEnd + .3, ease: "none" }, 0);
      tl.fromTo("#s01-stk", { scale: 1 }, { scale: 1.08, rotation: -3, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, 0);
      hkw.forEach((w, i) => { const t0 = Math.max(0, at("L1", w) - .03); tl.fromTo("#hw" + i, { scale: 1 }, { scale: .45, duration: .05, ease: "power2.in", immediateRender: false }, t0); tl.to("#hw" + i, { scale: 1.35, duration: .12, ease: "power2.out" }, t0 + .05); tl.to("#hw" + i, { scale: 1, duration: .2, ease: "back.out(3)" }, t0 + .17); });
      tl.to("#hw3", { color: "#ffd23f", duration: .05 }, at("L1", "jetzt"));
      tl.to("#hw6", { color: "#ffd23f", duration: .05 }, ins);
      tl.fromTo(".hk-sp", { scale: 0, rotation: 0, opacity: 0 }, { scale: 1.2, rotation: 180, opacity: 1, duration: .35, ease: "back.out(3)", stagger: .12, yoyo: true, repeat: 3 }, .05);
      tl.fromTo("#s01-fl", { opacity: 0 }, { opacity: .75, duration: .08, yoyo: true, repeat: 1, ease: "power2.out" }, ins + .25);
      tl.to(["#s01-hk", "#s01-stk", "#s01-ray", "#s01-tint", ".hk-sp"], { opacity: 0, duration: .2 }, hEnd + .05);
      const l2 = line("L2")[0], be = at("L2", "653"), ko = at("L2", "Kokos");
      tl.fromTo("#s01-c", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, l2 - .1);
      count(tl, "#s01-n", 575, 653, l2 + .1, be - l2 + .3);
      tl.fromTo("#s01-c", { scale: 1 }, { scale: 1.15, duration: .15, yoyo: true, repeat: 3, ease: "sine.inOut" }, be + .4);
      tl.fromTo("#s01-p", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, be + .45);
      tl.fromTo("#s01-k", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, ko - .1);""")

# s02 – Dönerbude
scene("s02", PILL + """
    #s02-t { top: 300px; font-size: 62px; background: #e8433c; }
    #s02-w { left: 20px; top: 385px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-10deg); font-size: 36px; }
    .s02-n { font-size: 40px; background: #fff; color: #e8433c; }
    #s02-g { top: 720px; font-size: 46px; background: #ff6a1a; }""",
"""      <div id="s02-t" class="pl">🥙 DÖNERBUDE</div>
      <div id="s02-w" class="stamp">GEWONNEN!</div>
      <div id="s02-n1" class="pl s02-n" style="top:430px">⭐ @lotta.fsthff</div>
      <div id="s02-n2" class="pl s02-n" style="top:520px">@alana_wbr</div>
      <div id="s02-n3" class="pl s02-n" style="top:610px">@em1lia.brn</div>
      <div id="s02-g" class="pl">😋 Döner für alle!</div>""",
"""      const dn = at("L3", "Dönerbude"), dr = at("L3", "drei");
      tl.fromTo("#s02-t", { opacity: 0, scale: .3, rotation: -10 }, { opacity: 1, scale: 1, rotation: -2, duration: .45, ease: "back.out(2.6)" }, dn - .15);
      tl.fromTo("#s02-w", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, dn + .45);
      tl.fromTo(["#s02-n1", "#s02-n2", "#s02-n3"], { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)", stagger: .18 }, dr - .35);
      const dg = at("L3b", "Döner");
      tl.fromTo("#s02-g", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, dg - .15);
      tl.to("#s02-g", { rotation: 3, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, dg + .3);""")

# s03 – Strandbar, nachts Party
scene("s03", PILL + """
    #s03-t { top: 300px; font-size: 62px; background: #18b8c0; }
    .s03-n { font-size: 40px; background: #fff; color: #0a8a90; }
    #s03-p { top: 640px; font-size: 52px; background: #7b3fe0; }""",
"""      <div id="s03-t" class="pl">🍹 STRANDBAR</div>
      <div id="s03-n1" class="pl s03-n" style="top:430px">⭐ @paulepfpgfn</div>
      <div id="s03-n2" class="pl s03-n" style="top:520px">@khmr.496</div>
      <div id="s03-p" class="pl">🎉 Jede Nacht Party!</div>""",
"""      const sb = at("L4", "Strandbar"), na = at("L4b", "nachts"), zw = at("L4", "zwei");
      tl.fromTo("#s03-t", { opacity: 0, scale: .3, rotation: 10 }, { opacity: 1, scale: 1, rotation: 2, duration: .45, ease: "back.out(2.6)" }, sb - .15);
      tl.fromTo(["#s03-n1", "#s03-n2"], { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)", stagger: .2 }, zw - .3);
      tl.fromTo("#s03-p", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, na);
      tl.to("#s03-p", { rotation: 3, scale: 1.06, duration: .2, yoyo: true, repeat: 7, ease: "sine.inOut" }, na + .4);""")

# s04 – Bürgermeisterin
scene("s04", PILL + """
    #s04-t { top: 300px; font-size: 56px; background: #7b3fe0; }
    #s04-n { top: 410px; font-size: 46px; background: #fff; color: #7b3fe0; }
    #s04-sheet { top: 500px; }
    #s04-gl { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 530px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 54px; white-space: nowrap; }
    """ + CF_CSS.replace("top: 700px", "top: 600px") + """""",
f"""      <div id="s04-t" class="pl">🎖️ BÜRGERMEISTERIN</div>
      <div id="s04-n" class="pl">@lillygyqcf0</div>
      <div id="s04-gl" class="stamp" data-layout-ignore>🎉 HERZLICHEN GLÜCKWUNSCH!</div>
      <div id="s04-cfw"></div>
      <div id="s04-sheet" class="tk"><div class="tk-h">Kommentare<b>×</b></div>
        {tk("s04-k1", "#ff6a1a", "?", "dein.name", "Jeden Freitag Strandparty! 🎉", "1.204")}
        {tk("s04-k2", "#2e9e5b", "?", "dein.nachbar", "Gratis Döner am Sonntag 🥙", "873")}
      </div>""",
"""      const bm = at("L5", "Bürgermeisterin");
      tl.fromTo("#s04-t", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: .4, ease: "back.out(2)" }, bm - .15);
      tl.fromTo("#s04-n", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, bm + .35);
      const T0 = at("L5", "Herzlichen");
      tl.fromTo("#s04-gl", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, T0 - .05);
      tl.to("#s04-gl", { scale: 1.06, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, T0 + .4);
      const l5b = line("L5b")[0], vo = at("L5b", "Vorschläge");
      tl.to("#s04-gl", { opacity: 0, scale: .7, duration: .2 }, l5b - .1);
      tl.fromTo("#s04-sheet", { opacity: 0, y: 500 }, { opacity: 1, y: 0, duration: .45, ease: "power4.out" }, l5b + .1);
      tl.fromTo(["#s04-k1", "#s04-k2"], { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: .3, ease: "power3.out", stagger: .25 }, l5b + .35);
      tkLike(tl, "#s04-k1", vo, 1204, 1388, 1.2, 3);
      tl.to("#s04-sheet", { rotation: 1.2, duration: .22, yoyo: true, repeat: 3, ease: "sine.inOut" }, vo);
      """ + CONF_JS.replace("SEED", "31").replace("BOX", "s04-cfw"))

# s05 – Verlosung Palast-Leitung: Spielautomat
ROWS = "".join(f'<div class="s05-r{" s05-win" if i == WIN else ""}">@{n}</div>' for i, n in enumerate(NAMES))
scene("s05", PILL + "\n    " + CF_CSS.replace("top: 700px", "top: 660px") + """
    #s05-dim { position: absolute; inset: 0; background: rgba(10,12,40,.55); }
    #s05-t { top: 300px; font-size: 50px; background: #ff6a1a; }
    #s05-box { position: absolute; left: 110px; top: 450px; width: 860px; height: 390px; border-radius: 40px; background: #fff; overflow: hidden;
      box-shadow: 0 0 0 8px #2a1b12, 0 0 0 16px #ffc93c, 0 0 0 22px #2a1b12, 0 22px 0 rgba(0,0,0,.35); }
    #s05-band { position: absolute; left: 0; right: 0; top: 130px; height: 130px; background: #fff3c4; border-top: 5px solid #ffc93c; border-bottom: 5px solid #ffc93c; }
    #s05-col { position: absolute; left: 0; right: 0; top: 0; }
    .s05-r { height: 130px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 64px; color: #23285a; white-space: nowrap; }
    #s05-shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,.95)); }
    .s05-arr { position: absolute; top: 605px; font-size: 80px; color: #ffc93c; -webkit-text-stroke: 4px #2a1b12; }
    #s05-pl { top: 300px; font-size: 46px; background: #ffb81c; color: #2a1b12; }
    #s05-pb { top: 400px; font-size: 42px; background: #7b3fe0; }
    #s05-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 890px; color: #e8433c; border-color: #e8433c; transform: rotate(-5deg); font-size: 64px; white-space: nowrap; background: #fff; }""",
f"""      <div id="s05-dim"></div>
      <div id="s05-t" class="pl">👑 VERLOSUNG: PALAST-LEITUNG</div>
      <div id="s05-box"><div id="s05-band"></div><div id="s05-col" data-layout-ignore>{ROWS}</div><div id="s05-shade" data-layout-ignore></div></div>
      <div class="s05-arr" style="left:30px">▶</div><div class="s05-arr" style="left:985px">◀</div>
      <div id="s05-cfw"></div>
      <div id="s05-st" class="stamp" data-layout-ignore>👑 PALAST-LEITUNG!</div>
      <div id="s05-pl" class="pl">👑 Palast-Leitung: @prvt.lott1</div>
      <div id="s05-pb" class="pl">🏰 zusammen im Palast</div>""",
f"""      const s0 = at("L6", "Palast-Leitung") + .7, T0 = line("L7")[0] - .45, H = 130, NR = {len(NAMES)}, W = {WIN};
      tl.fromTo("#s05-dim", {{ opacity: 0 }}, {{ opacity: 1, duration: .4 }}, line("L6")[0]);
      tl.fromTo("#s05-t", {{ opacity: 0, scale: .3 }}, {{ opacity: 1, scale: 1, duration: .4, ease: "back.out(2.6)" }}, line("L6")[0] + .1);
      tl.fromTo(["#s05-box", ".s05-arr"], {{ opacity: 0, scale: .5 }}, {{ opacity: 1, scale: 1, duration: .4, ease: "back.out(2)" }}, at("L6", "Wer") - .2);
      tl.set("#s05-col", {{ y: -(NR - 3) * H }}, 0);
      tl.fromTo("#s05-col", {{ y: -(NR - 3) * H }}, {{ y: -(W - 1) * H, duration: T0 - s0, ease: "power3.out", immediateRender: false }}, s0);
      tl.fromTo("#s05-col", {{ filter: "blur(5px)" }}, {{ filter: "blur(0px)", duration: (T0 - s0) * .8, ease: "power2.in", immediateRender: false }}, s0);
      tl.to(".s05-arr", {{ x: (i) => i ? -14 : 14, duration: .15, yoyo: true, repeat: 13, ease: "sine.inOut" }}, s0);
      tl.to(".s05-win", {{ color: "#e8433c", scale: 1.18, duration: .2, ease: "back.out(3)" }}, T0);
      tl.to(".s05-win", {{ scale: 1.08, duration: .25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, T0 + .25);
      tl.to("#s05-band", {{ backgroundColor: "#ffd23f", duration: .15, yoyo: true, repeat: 9 }}, T0);
      tl.fromTo("#s05-st", {{ opacity: 0, scale: 2.6 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, T0 + .25);
      """ + CONF_JS.replace("SEED", "21").replace("BOX", "s05-cfw") + """
      tl.to("#s05-t", { opacity: 0, duration: .2 }, T0);
      const wo = at("L7", "wohnst");
      tl.to(["#s05-box", ".s05-arr", "#s05-st"], { opacity: 0, scale: .8, duration: .25, ease: "power2.in" }, wo - .1);
      tl.to("#s05-dim", { opacity: 0, duration: .3 }, wo - .1);
      tl.fromTo("#s05-pl", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, wo + .1);
      tl.fromTo("#s05-pb", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, at("L7", "Bürgermeisterin") - .1);""", blur=False)

# s06 – Strandvilla: nächstes Video
scene("s06", PILL + """
    #s06-t { top: 300px; font-size: 58px; background: #18b8c0; }
    #s06-n { top: 420px; font-size: 44px; background: #e8467c; }
    #s06-sp { top: 300px; font-size: 48px; background: #18b8c0; }
    #s06-nb { top: 300px; font-size: 42px; background: #2e9e5b; }
    #s06-hs { position: absolute; left: 215px; top: 880px; width: 130px; height: 130px; border-radius: 50%; background: #fff; display: grid; place-items: center; font-size: 84px; box-shadow: 0 0 0 7px #ffc93c, 0 0 0 12px #2a1b12, 0 12px 20px rgba(0,0,0,.3); }
    #s06-z { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 530px; color: #e8433c; border-color: #e8433c; transform: rotate(-4deg); font-size: 56px; white-space: nowrap; background: #fff; }""",
"""      <div id="s06-t" class="pl">🏖️ STRANDVILLA</div>
      <div id="s06-n" class="pl">🎬 Nächstes Video: Verlosung</div>
      <div id="s06-z" class="stamp">2 GEWINNER 🎁</div>
      <div id="s06-sp" class="pl">🏊 Pool für @sophia_e065!</div>
      <div id="s06-nb" class="pl">🏡 @anton.van11 + @laura.ngynn</div>
      <div id="s06-hs" data-layout-ignore>🤝</div>""",
"""      const sv = at("L8", "Strandvilla"), zw = at("L8", "zwei");
      tl.fromTo("#s06-n", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, .05);
      tl.fromTo("#s06-t", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .45, ease: "back.out(2.6)" }, sv - .15);
      tl.fromTo("#s06-z", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, zw - .05);
      const sp = line("L8b")[0], kd = at("L8b", "kriegst");
      tl.to(["#s06-t", "#s06-n", "#s06-z"], { opacity: 0, y: -20, duration: .2 }, sp - .1);
      tl.fromTo("#s06-sp", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, sp + .1);
      tl.to("#s06-sp", { scale: 1.1, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut" }, kd);
      const nb = line("L8c")[0], na = at("L8c", "Nachbarn");
      tl.to("#s06-sp", { opacity: 0, y: -20, duration: .2 }, nb - .1);
      tl.fromTo("#s06-nb", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, nb + .1);
      tl.fromTo("#s06-hs", { opacity: 0, scale: 0, rotation: -40 }, { opacity: 1, scale: 1, rotation: 0, duration: .5, ease: "elastic.out(1, .5)" }, na - .2);
      tl.to("#s06-hs", { scale: 1.15, rotation: 8, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, na + .35);""")

# s07 – Bauprojekte mit Zielen, Anlegestelle wichtig, Aufruf
BAUC = [("🏨", "Hotel Sandkorn", "800"), ("⚓", "Boots-Anlegestelle", "900")]
PCT = [653 / 800, 653 / 900]
CARDS = "".join(f'<div class="s07-c" id="s07-c{i}" style="top:{290 + i * 160}px"><div class="e">{e}</div><div class="m"><b>{n}</b><small>Fertig bei {z} Bewohnern</small><div class="bar"><i id="s07-b{i}"></i></div></div><div class="z">653<br><span>/ {z}</span></div></div>' for i, (e, n, z) in enumerate(BAUC))
scene("s07", PILL + """
    .s07-c { position: absolute; left: 90px; width: 900px; height: 140px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.3);
      display: flex; align-items: center; gap: 20px; padding: 0 28px; font-family: "Inter", sans-serif; color: #23285a; }
    .s07-c .e { font-size: 72px; } .s07-c .m { flex: 1; } .s07-c b { font-size: 40px; font-weight: 900; display: block; line-height: 1.1; }
    .s07-c small { display: block; font-size: 28px; font-weight: 800; color: #6b6f8a; margin-top: 2px; }
    .s07-c .bar { height: 20px; border-radius: 10px; background: #e3e6f0; margin-top: 8px; overflow: hidden; } .s07-c .bar i { display: block; height: 100%; width: 0; background: #ff6a1a; border-radius: 10px; }
    .s07-c .z { font-size: 40px; font-weight: 900; color: #ff6a1a; text-align: center; line-height: 1; } .s07-c .z span { font-size: 26px; color: #6b6f8a; }
    #s07-w { top: 640px; font-size: 44px; background: #18b8c0; }
    .fbtn { position: absolute; left: 0; right: 0; margin: 0 auto; top: 330px; width: 420px; height: 120px; border-radius: 60px; background: #fe2c55; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; display: grid; place-items: center; box-shadow: 0 0 0 5px #2a1b12, 0 12px 0 rgba(0,0,0,.25); }
    .fbtn2 { position: absolute; inset: 0; border-radius: 60px; background: #fff; color: #0a78c2; display: grid; place-items: center; opacity: 0; }
    #s07-hand { position: absolute; left: 690px; top: 380px; font-size: 120px; }
    #s07-m { top: 500px; font-size: 44px; background: #e8467c; }""",
CARDS + """
      <div id="s07-w" class="pl">⛵ Zwischen den Inseln wechseln!</div>
      <div id="s07-btn" class="fbtn">+ Folgen<div id="s07-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s07-hand" data-layout-ignore>👆</div>
      <div id="s07-m" class="pl">👯 Freunde markieren!</div>""",
"""      const ws = [at("L9", "Hotel"), at("L9", "Anlegestelle")], pc = """ + str([round(x, 3) for x in PCT]) + """, l10 = line("L10")[0], fo = at("L10", "folgen"), fr = at("L10", "Freunde"), zw = at("L9b", "zwischen"), l9b = line("L9b")[0];
      ws.forEach((w, i) => { tl.fromTo("#s07-c" + i, { opacity: 0, x: i % 2 ? 120 : -120 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, w - .2);
        tl.fromTo("#s07-b" + i, { width: "0%" }, { width: (pc[i] * 100).toFixed(1) + "%", duration: .8, ease: "power2.out" }, w + .1); });
      tl.to(["#s07-c0"], { opacity: .45, duration: .25 }, l9b);
      tl.to("#s07-c1", { scale: 1.07, boxShadow: "0 0 0 8px #18b8c0, 0 12px 0 rgba(0,0,0,.3)", duration: .3, ease: "back.out(2)" }, l9b);
      tl.fromTo("#s07-w", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, zw - .2);
      tl.to("#s07-w", { scale: 1.06, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, zw + .3);
      tl.to([".s07-c", "#s07-w"], { opacity: 0, y: -30, duration: .2 }, l10 - .25);
      tl.fromTo("#s07-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, l10);
      tl.fromTo("#s07-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .2);
      tl.to("#s07-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo + .1);
      tl.to("#s07-btn2", { opacity: 1, duration: .05 }, fo + .2);
      tl.fromTo("#s07-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1 }, fo + .2);
      tl.to("#s07-hand", { opacity: 0, duration: .25 }, fo + .7);
      tl.fromTo("#s07-m", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, fr - .15);
      tl.to("#s07-m", { scale: 1.06, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, fr + .4);""", blur=False)
