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
scene("s01", PILL + "\n    " + CF_CSS.replace("top: 700px", "top: 900px") + """
    #s01-t { top: 280px; font-size: 54px; background: #e8467c; }
    .s01-st { position: absolute; left: 90px; right: 210px; height: 104px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 10px 0 rgba(0,0,0,.28); display: flex; align-items: center; gap: 22px; padding: 0 22px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 38px; color: #2a1b12; }
    .s01-st b { flex: none; width: 70px; height: 70px; border-radius: 50%; display: grid; place-items: center; color: #fff; font-size: 42px; box-shadow: 0 0 0 4px #2a1b12; }
    #s01-s1 { top: 400px; } #s01-s2 { top: 530px; } #s01-s3 { top: 660px; }
    #s01-h { position: absolute; left: 110px; top: 850px; font-size: 110px; filter: drop-shadow(0 6px 0 rgba(0,0,0,.3)); }""",
"""      <div id="s01-t" class="pl">👯 Beste Freunde = Nachbarn!</div>
      <div id="s01-s1" class="s01-st"><b style="background:#7b3fe0">1</b>💬 Unter dem Video markieren</div>
      <div id="s01-s2" class="s01-st"><b style="background:#fe2c55">2</b>➕ Sie folgt mir</div>
      <div id="s01-s3" class="s01-st"><b style="background:#2e9e5b">3</b>🏡 Morgen seid ihr Nachbarn!</div>
      <div id="s01-h" data-layout-ignore>💞</div>
      <div id="s01-cfw"></div>""",
"""      const be = at("L1", "besten"), e1 = at("L2", "eins"), e2 = at("L2", "zwei"), e3 = at("L2", "drei"), na = at("L2", "Nachbarn");
      tl.fromTo("#s01-t", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.6)" }, Math.max(0, be - .3));
      [[e1, 1], [e2, 2], [e3, 3]].forEach(([t, i]) => {
        tl.fromTo("#s01-s" + i, { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, t - .35);
        tl.fromTo("#s01-s" + i, { scale: 1 }, { scale: 1.08, duration: .15, yoyo: true, repeat: 1, immediateRender: false }, t + .1); });
      tl.fromTo("#s01-h", { opacity: 0, scale: .2 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(3)" }, na - .1);
      tl.to("#s01-h", { scale: 1.15, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, na + .3);
      """ + CONF_JS.replace("SEED", "21").replace("BOX", "s01-cfw").replace("T0", "na") + """""", blur=False)
