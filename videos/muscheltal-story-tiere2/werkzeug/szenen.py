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
scene("s01", PILL + "\n" + FOLLOW + """
    #s01-flash { position: absolute; inset: 0; box-shadow: inset 0 0 220px 60px rgba(232,38,47,.85); opacity: 0; }
    #s01-t { top: 290px; font-size: 62px; background: #e8262f; }
    #s01-f { position: absolute; left: 90px; right: 90px; top: 410px; padding: 18px 26px 22px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.28); font-family: "Inter", sans-serif; font-weight: 900; font-size: 42px; color: #2a1b12; text-align: center; }
    #s01-f span { display: inline-block; margin: 10px 6px 0; padding: 4px 18px 8px; border-radius: 999px; background: #e8f3ff; color: #0a78c2; font-size: 36px; }
    #s01-btn { top: 640px; } #s01-hand { left: 690px; top: 690px; }
    #s01-r { top: 800px; font-size: 46px; background: #2e9e5b; }
    #s01-m { top: 900px; font-size: 40px; background: #7b3fe0; }
    #s01-k { position: absolute; left: 90px; right: 90px; top: 410px; padding: 20px 28px 24px; border-radius: 30px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.28); font-family: "Inter", sans-serif; font-weight: 900; color: #2a1b12; text-align: center; font-size: 40px; }
    #s01-k b { display: block; font-size: 96px; color: #2e9e5b; line-height: 1.05; }
    #s01-d { top: 640px; font-size: 56px; background: #e8467c; }""",
"""      <div id="s01-flash" data-layout-ignore></div>
      <div id="s01-t" class="pl">🚨 Die Tiere brauchen euch!</div>
      <div id="s01-f">👯 Lade deine Freunde ein<br><span>@deine_bff</span><span>@bester_freund</span></div>
      <div id="s01-btn" class="fbtn">+ Folgen<div id="s01-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s01-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s01-r" class="pl">🐾 Tiere gerettet!</div>
      <div id="s01-m" class="pl">💬 Markiere sie unter dem Video!</div>
      <div id="s01-k">🐚 Jeder neue Bewohner<b id="s01-kn">+5</b>Muscheln fürs Tierheim Pfotenkuss</div>""",
"""      const hi = at("L1", "Hilfe"), fr = at("L2", "Freunde"), fo = at("L2", "folgt"), re = at("L2", "rettet"), ma = at("L2", "Markiert"), l3 = line("L3")[0];
      tl.set("#s01-t", { opacity: 1 }, 0);
      tl.fromTo("#s01-t", { scale: 2.4 }, { scale: 1, duration: .3, ease: "back.out(2.2)" }, 0);
      tl.to("#s01-t", { opacity: .35, duration: .14, yoyo: true, repeat: 9, ease: "none" }, .4);
      tl.fromTo("#s01-flash", { opacity: 0 }, { opacity: 1, duration: .14, yoyo: true, repeat: 11, ease: "none" }, 0);
      tl.fromTo("#s01-f", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.4)" }, fr - .3);
      tl.fromTo("#s01-f span", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .25, stagger: .15 }, fr + .1);
      tl.fromTo("#s01-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .4);
      tl.fromTo("#s01-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .3);
      tl.to("#s01-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo);
      tl.to("#s01-btn2", { opacity: 1, duration: .05 }, fo + .1);
      tl.fromTo("#s01-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .1);
      tl.to("#s01-hand", { opacity: 0, duration: .2 }, fo + .5);
      tl.fromTo("#s01-r", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, re - .1);
      tl.fromTo("#s01-m", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ma - .2);
      tl.to("#s01-m", { scale: 1.08, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut" }, ma + .2);
      tl.to(["#s01-f", "#s01-btn", "#s01-r", "#s01-m"], { opacity: 0, y: -30, duration: .25 }, l3 - .3);
      tl.fromTo("#s01-k", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.4)" }, l3 - .1);
      tl.fromTo("#s01-k b", { scale: 1 }, { scale: 1.25, duration: .15, yoyo: true, repeat: 5, immediateRender: false }, at("L3", "Muscheln"));
      tl.to(["#s01-t", "#s01-k"], { opacity: 0, y: -30, duration: .3 }, line("L3")[1] + .3);""", blur=False)
