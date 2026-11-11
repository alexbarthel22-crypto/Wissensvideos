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
scene("s01", LILITA + "\n    " + PILL + """
    #s01-h { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 280px; padding: 6px 36px 14px; border-radius: 30px; background: #e8467c; color: #fff; font-family: "Lilita One", sans-serif; font-size: 72px; line-height: 1; white-space: nowrap; box-shadow: 0 0 0 7px #2a1b12, 0 12px 0 rgba(0,0,0,.3); transform: rotate(-2deg); }
    #s01-cm { position: absolute; left: 90px; right: 210px; top: 420px; padding: 20px 24px 24px; border-radius: 28px; background: #1f1f1f; box-shadow: 0 0 0 5px #000, 0 12px 24px rgba(0,0,0,.45); font-family: "Inter", sans-serif; color: #fff; display: flex; gap: 18px; }
    #s01-cm .av { width: 70px; height: 70px; border-radius: 50%; flex: none; background: linear-gradient(135deg, #ffd23f, #e8467c); display: grid; place-items: center; font-size: 38px; }
    #s01-cm .nm { font-size: 24px; color: #a8a8a8; font-weight: 600; } #s01-cm .tx { font-size: 36px; font-weight: 600; margin-top: 4px; min-height: 46px; }
    #s01-cm .cu { display: inline-block; width: 4px; height: 36px; background: #fe2c55; vertical-align: -6px; margin-left: 3px; }
    #s01-v { top: 600px; font-size: 38px; background: #7b3fe0; }
    #s01-n { position: absolute; left: 90px; right: 210px; top: 420px; padding: 18px 24px 22px; border-radius: 28px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.28); font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; color: #2a1b12; text-align: center; }
    #s01-n span { display: inline-block; margin: 10px 6px 0; padding: 4px 18px 8px; border-radius: 999px; background: #e8f3ff; color: #0a78c2; font-size: 36px; }""",
"""      <div id="s01-h">🏠 Wo ist dein Haus?</div>
      <div id="s01-cm"><div class="av">🐚</div><div><div class="nm">Du</div><div class="tx"><span id="s01-ty"></span><span class="cu" id="s01-cu"></span></div></div></div>
      <div id="s01-v" class="pl">💬 Unter meinem neuen Video von heute</div>
      <div id="s01-n">👯 Gleich Nachbarn markieren<br><span>@beste_freundin</span><span>@bester_freund</span></div>""",
"""      const ha = at("L1", "Haus"), ko = at("L1", "Kommentiere"), ze = at("L1", "zeige"), l2 = line("L2")[0], ma = at("L2", "Markiere");
      tl.set("#s01-h", { opacity: 1 }, 0);
      tl.fromTo("#s01-h", { scale: 2.2 }, { scale: 1, duration: .3, ease: "back.out(2.2)" }, 0);
      tl.to("#s01-h", { scale: 1.08, duration: .15, yoyo: true, repeat: 1 }, ha);
      tl.fromTo("#s01-cm", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ko - .3);
      const TXT = "Wo ist mein Haus? 🏠", ty = document.getElementById("s01-ty"), o = { n: 0 };
      tl.to(o, { n: Array.from(TXT).length, duration: .9, ease: "none", onUpdate: () => { ty.textContent = Array.from(TXT).slice(0, Math.round(o.n)).join(""); } }, ko);
      tl.to("#s01-cu", { opacity: 0, duration: .25, yoyo: true, repeat: 7, ease: "steps(1)" }, ko);
      tl.fromTo("#s01-v", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, ko + .3);
      tl.to(["#s01-cm", "#s01-v"], { opacity: 0, y: -30, duration: .25 }, l2 - .25);
      tl.fromTo("#s01-n", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.4)" }, l2 - .1);
      tl.fromTo("#s01-n span", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .25, stagger: .15 }, ma);
      tl.to("#s01-n span", { scale: 1.1, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut", stagger: .1 }, ma + .4);""", blur=False)
