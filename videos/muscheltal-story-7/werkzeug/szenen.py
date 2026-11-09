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

# s01 – Dönerbude + Strandbar
scene("s01", PILL + """
    #s01-n { top: 300px; font-size: 44px; background: #7b3fe0; }
    #s01-d { top: 410px; font-size: 64px; background: #e8433c; }
    #s01-s { top: 410px; font-size: 64px; background: #18b8c0; }
    .s01-ok { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 540px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-6deg); font-size: 50px; white-space: nowrap; }""",
"""      <div id="s01-n" class="pl">🏝️ NEU IN MUSCHEL-TAL</div>
      <div id="s01-d" class="pl">🥙 DÖNERBUDE</div>
      <div id="s01-dk" class="stamp s01-ok" data-layout-ignore>✅ GEBAUT!</div>
      <div id="s01-s" class="pl">🍹 STRANDBAR</div>
      <div id="s01-sk" class="stamp s01-ok" data-layout-ignore>✅ GEBAUT!</div>""",
"""      const dn = at("L1", "Dönerbude"), sb = at("L1", "Strandbar");
      tl.fromTo("#s01-n", { opacity: 0, y: -50 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, .05);
      tl.fromTo("#s01-d", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.6)" }, dn - .1);
      tl.fromTo("#s01-dk", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, dn + .3);
      tl.to(["#s01-d", "#s01-dk"], { opacity: 0, scale: .7, duration: .15 }, sb - .25);
      tl.fromTo("#s01-s", { opacity: 0, scale: .3, rotation: 8 }, { opacity: 1, scale: 1, rotation: 2, duration: .35, ease: "back.out(2.6)" }, sb - .1);
      tl.fromTo("#s01-sk", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(2)" }, sb + .35);""")

# s02 – Baustellen mit Zielen
BAUC = [("🏨", "Hotel Sandkorn", "800", 653 / 800), ("⚓", "Boots-Anlegestelle", "900", 653 / 900)]
CARDS = "".join(f'<div class="s02-c" id="s02-c{i}" style="top:{400 + i * 160}px"><div class="e">{e}</div><div class="m"><b>{n}</b><small>Fertig bei {z} Bewohnern</small><div class="bar"><i id="s02-b{i}"></i></div></div><div class="z">653<br><span>/ {z}</span></div></div>' for i, (e, n, z, p) in enumerate(BAUC))
scene("s02", PILL + """
    #s02-t { top: 290px; font-size: 48px; background: #ff6a1a; }
    .s02-c { position: absolute; left: 90px; width: 900px; height: 140px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.3);
      display: flex; align-items: center; gap: 20px; padding: 0 28px; font-family: "Inter", sans-serif; color: #23285a; }
    .s02-c .e { font-size: 72px; } .s02-c .m { flex: 1; } .s02-c b { font-size: 40px; font-weight: 900; display: block; line-height: 1.1; }
    .s02-c small { display: block; font-size: 28px; font-weight: 800; color: #6b6f8a; margin-top: 2px; }
    .s02-c .bar { height: 20px; border-radius: 10px; background: #e3e6f0; margin-top: 8px; overflow: hidden; } .s02-c .bar i { display: block; height: 100%; width: 0; background: #ff6a1a; border-radius: 10px; }
    .s02-c .z { font-size: 40px; font-weight: 900; color: #ff6a1a; text-align: center; line-height: 1; } .s02-c .z span { font-size: 26px; color: #6b6f8a; }""",
"""      <div id="s02-t" class="pl">🏗️ JETZT WIRD GEBAUT</div>
      """ + CARDS,
"""      const ws = [at("L2", "Hotel"), at("L2", "Anlegestelle")], pc = """ + str([round(x[3], 3) for x in BAUC]) + """;
      tl.fromTo("#s02-t", { opacity: 0, y: -50 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, .05);
      ws.forEach((w, i) => { tl.fromTo("#s02-c" + i, { opacity: 0, x: i ? 120 : -120 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, w - .2);
        tl.fromTo("#s02-b" + i, { width: "0%" }, { width: (pc[i] * 100).toFixed(1) + "%", duration: .8, ease: "power2.out" }, w + .1); });
      tl.to("#s02-c1", { scale: 1.06, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, at("L2", "900"));""")

# s03 – Inseln wechseln, Freunde markieren, Nachbarn
scene("s03", PILL + """
    #s03-w { top: 300px; font-size: 48px; background: #18b8c0; }
    #s03-m { top: 410px; font-size: 48px; background: #e8467c; }
    #s03-nb { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 530px; color: #2e9e5b; border-color: #2e9e5b; background: #fff; transform: rotate(-5deg); font-size: 58px; white-space: nowrap; }
    #s03-f { top: 690px; font-size: 38px; background: #fe2c55; }""",
"""      <div id="s03-w" class="pl">⛵ Zwischen den Inseln wechseln!</div>
      <div id="s03-m" class="pl">👯 Freunde markieren</div>
      <div id="s03-nb" class="stamp" data-layout-ignore>🏡 NACHBARN WERDEN!</div>
      <div id="s03-f" class="pl">➕ @muscheltal folgen = einziehen</div>""",
"""      const zw = at("L3", "zwischen"), ma = at("L3", "Freunde"), nb = at("L3", "Nachbarn");
      tl.fromTo("#s03-w", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, zw - .15);
      tl.fromTo("#s03-m", { opacity: 0, x: -120 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, ma - .15);
      tl.fromTo("#s03-nb", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .28, ease: "back.out(2)" }, nb - .05);
      tl.to("#s03-nb", { scale: 1.07, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, nb + .35);
      tl.fromTo("#s03-f", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, nb + .5);""", blur=False)
