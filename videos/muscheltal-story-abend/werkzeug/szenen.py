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
scene("s01", LILITA + "\n    " + PILL + "\n    " + CF_CSS.replace("top: 700px", "top: 760px") + """
    #s01-sun { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(90,40,140,.6) 0%, rgba(230,90,110,.45) 30%, rgba(255,150,80,.32) 60%, rgba(120,50,110,.5) 100%); mix-blend-mode: multiply; }
    #s01-glow { position: absolute; left: 540px; top: -280px; width: 900px; height: 900px; border-radius: 50%; background: radial-gradient(circle, rgba(255,225,150,.9) 0%, rgba(255,160,80,.5) 25%, rgba(255,120,60,0) 62%); mix-blend-mode: screen; }
    #s01-a { top: 280px; font-size: 54px; background: linear-gradient(90deg, #7b3fe0, #ff7a59); }
    #s01-cm { position: absolute; left: 90px; right: 90px; top: 420px; padding: 22px 26px 26px; border-radius: 30px; background: #1f1f1f; box-shadow: 0 0 0 6px #ffd23f, 0 0 40px 10px rgba(255,210,63,.6); font-family: "Inter", sans-serif; color: #fff; display: flex; gap: 18px; }
    #s01-cm .av { width: 74px; height: 74px; border-radius: 50%; flex: none; background: linear-gradient(135deg, #ffd23f, #e8467c); display: grid; place-items: center; font-size: 40px; }
    #s01-cm .nm { font-size: 26px; color: #ffd23f; font-weight: 800; } #s01-cm .tx { font-size: 38px; font-weight: 600; margin-top: 6px; }
    #s01-lk { margin-left: auto; text-align: center; font-weight: 800; font-size: 26px; color: #ff5c7a; flex: none; } #s01-lk span { display: block; font-size: 46px; }
    #s01-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 700px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-4deg); font-size: 66px; white-space: nowrap; font-family: "Lilita One", sans-serif; }
    #s01-eg { top: 860px; font-size: 52px; background: #e8262f; }""",
"""      <div id="s01-sun" data-layout-ignore></div><div id="s01-glow" data-layout-ignore></div>
      <div id="s01-a" class="pl">🌅 Abend auf der Haupt-Insel</div>
      <div id="s01-cm"><div class="av">👑</div><div><div class="nm">Top-Kommentar</div><div class="tx">Deine Idee – egal, was es ist 🤯</div></div><div id="s01-lk"><span>❤️</span><b id="s01-ln">0</b></div></div>
      <div id="s01-st" class="stamp" data-layout-ignore>🎬 MORGEN IM VIDEO!</div>
      <div id="s01-eg" class="pl">🤯 Egal, was es ist!</div>
      <div id="s01-cfw"></div>""",
"""      const to = at("L2", "Top-Kommentar"), mo = at("L2", "morgen"), eg = at("L2", "egal");
      tl.set(["#s01-a", "#s01-sun", "#s01-glow"], { opacity: 1 }, 0);
      tl.fromTo("#s01-glow", { scale: .95 }, { scale: 1.06, duration: 2.5, yoyo: true, repeat: 4, ease: "sine.inOut" }, 0);
      tl.fromTo("#s01-a", { scale: .6, y: 20 }, { scale: 1, y: 0, duration: .5, ease: "back.out(2)" }, 0);
      tl.fromTo("#s01-cm", { opacity: 0, y: 40, scale: .9 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2)" }, to - .25);
      count(tl, "#s01-ln", 0, 9999, to, 2.0, "", "", "power2.in");
      tl.fromTo("#s01-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, mo - .05);
      tl.fromTo("#s01-eg", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, eg - .15);
      tl.to("#s01-eg", { scale: 1.1, duration: .2, yoyo: true, repeat: 9, ease: "sine.inOut" }, eg + .3);
      """ + CONF_JS.replace("SEED", "27").replace("BOX", "s01-cfw").replace("T0", "eg + .4") + """""", blur=False)
