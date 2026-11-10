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
scene("s01", PILL + """
    #s01-flash { position: absolute; inset: 0; box-shadow: inset 0 0 220px 60px rgba(232,38,47,.85); opacity: 0; }
    #s01-t { top: 290px; font-size: 64px; background: #e8262f; }
    #s01-h { top: 400px; font-size: 46px; background: #fff; color: #e8262f; }
    #s01-c { position: absolute; left: 70px; right: 70px; top: 500px; padding: 22px 30px 26px; border-radius: 34px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    #s01-c .row { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 40px; }
    #s01-c .row b { font-size: 76px; color: #e8262f; line-height: 1; } #s01-c .row span { font-size: 36px; color: #6b6f8a; }
    #s01-c .bar { height: 34px; border-radius: 17px; background: #ece4d8; margin-top: 14px; overflow: hidden; } #s01-c .bar i { display: block; height: 100%; width: 25.25%; border-radius: 17px; background: linear-gradient(90deg, #e8262f, #ff8a3a); }
    #s01-c .rest { margin-top: 10px; font-weight: 900; font-size: 32px; color: #2a1b12; text-align: center; }
    #s01-m { top: 790px; font-size: 48px; background: #7b3fe0; }""",
"""      <div id="s01-flash" data-layout-ignore></div>
      <div id="s01-t" class="pl">🚨 NEUES VIDEO</div>
      <div id="s01-h" class="pl">Wir brauchen eure Hilfe!</div>
      <div id="s01-c"><div class="row"><div>🐚 Inselkasse</div><div><b>505</b><span> / 2.000</span></div></div><div class="bar"><i></i></div><div class="rest">🐶🐱 Für das Tierheim Pfotenkuss</div></div>
      <div id="s01-m" class="pl">👉 Mehr im neuesten Video!</div>""",
"""      const hi = at("L1", "Hilfe"), ti = at("L2", "Tiere"), me = at("L2", "Mehr");
      tl.set("#s01-t", { opacity: 1 }, 0);
      tl.to("#s01-t", { opacity: .35, duration: .14, yoyo: true, repeat: 11, ease: "none" }, .1);
      tl.fromTo("#s01-flash", { opacity: 0 }, { opacity: 1, duration: .14, yoyo: true, repeat: 11, ease: "none" }, 0);
      tl.fromTo("#s01-h", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, hi - .4);
      tl.fromTo("#s01-c", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, ti - .3);
      tl.to("#s01-c .bar i", { opacity: .3, duration: .14, yoyo: true, repeat: 9, ease: "none" }, ti + .2);
      tl.fromTo("#s01-m", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, me - .2);
      tl.to("#s01-m", { scale: 1.08, x: 14, duration: .25, yoyo: true, repeat: 11, ease: "sine.inOut" }, me + .3);""", blur=False)
