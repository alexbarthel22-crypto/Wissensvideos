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


STK = """.stk2 { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; padding: 8px 30px 12px; border-radius: 999px; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); white-space: nowrap; }"""

scene("s01", STK + """
    #s01-t { top: 300px; font-size: 46px; background: #ff6a1a; }""",
"""      <div id="s01-t" class="stk2">🔥 KOKOS-KÜSTE · ABENDS</div>""",
"""      tl.fromTo("#s01-t", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: .5, ease: "back.out(2)" }, .2);
      tl.to("#s01-t", { rotation: 1.5, duration: .6, yoyo: true, repeat: 2, ease: "sine.inOut" }, .8);""")

scene("s02", STK + """
    #s02-t { top: 300px; font-size: 46px; background: #e8467c; }
    #s02-k { position: absolute; left: 0; right: 0; margin: 0 auto; top: 400px; width: 520px; height: 300px; border-radius: 34px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 14px 0 rgba(0,0,0,.35); overflow: hidden; text-align: center; font-family: "Inter", sans-serif; }
    #s02-k .e { height: 200px; display: grid; place-items: center; font-size: 130px; background: linear-gradient(180deg, #bfefff, #fff); }
    #s02-k .l { height: 100px; display: grid; place-items: center; font-weight: 900; font-size: 42px; color: #fff; background: #ff6a1a; }""",
"""      <div id="s02-t" class="stk2">⏰ MORGEN</div>
      <div id="s02-k"><div class="e">🏗️</div><div class="l">ERSTE GEBÄUDE!</div></div>""",
"""      const mo = at("L2", "morgen"), ge = at("L2", "Gebäude");
      tl.fromTo("#s02-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .4, ease: "back.out(2.6)" }, mo - .1);
      tl.fromTo("#s02-k", { opacity: 0, scale: 0, rotation: -12 }, { opacity: 1, scale: 1, rotation: -2, duration: .5, ease: "back.out(2.2)" }, ge - .2);
      tl.to("#s02-k", { y: -14, rotation: 2, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut" }, ge + .4);""")

scene("s03", STK + """
    #s03-btn { position: absolute; left: 0; right: 0; margin: 0 auto; top: 360px; width: 420px; height: 120px; border-radius: 60px; background: #fe2c55; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; display: grid; place-items: center; box-shadow: 0 0 0 5px #2a1b12, 0 12px 0 rgba(0,0,0,.25); }
    #s03-btn2 { position: absolute; inset: 0; border-radius: 60px; background: #fff; color: #0a78c2; display: grid; place-items: center; opacity: 0; }
    #s03-hand { position: absolute; left: 690px; top: 410px; font-size: 120px; }
    #s03-at { top: 530px; font-size: 44px; background: #ff6a1a; }
    #s03-a { top: 640px; font-size: 40px; background: #e8467c; }
    #s03-w { top: 740px; font-size: 44px; background: #2e9e5b; }""",
"""      <div id="s03-btn">+ Folgen<div id="s03-btn2">✓ Gefolgt</div></div>
      <div id="s03-hand" data-layout-ignore>👆</div>
      <div id="s03-at" class="stk2">@muscheltal</div>
      <div id="s03-a" class="stk2">👯 Ladet eure Freunde ein!</div>
      <div id="s03-w" class="stk2">🌍 DIE GRÖSSTE WELT AUF TIKTOK!</div>""",
"""      const fo = at("L3", "folgen"), an = at("L3", "Freunde");
      tl.fromTo("#s03-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, fo - .7);
      tl.fromTo("#s03-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .3, ease: "power3.out" }, fo - .4);
      tl.to("#s03-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo - .05);
      tl.to("#s03-btn2", { opacity: 1, duration: .05 }, fo + .05);
      tl.fromTo("#s03-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1 }, fo + .05);
      tl.to("#s03-hand", { opacity: 0, duration: .25 }, fo + .6);
      tl.fromTo("#s03-at", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "power3.out" }, fo + .3);
      tl.fromTo("#s03-a", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, an - .1);
      tl.to("#s03-btn", { scale: 1.06, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, fo + .6);
      const gr = at("L4", "größte");
      tl.fromTo("#s03-w", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .45, ease: "back.out(2.6)" }, gr - .15);
      tl.to("#s03-w", { scale: 1.07, rotation: 2, duration: .25, yoyo: true, repeat: 5, ease: "sine.inOut" }, gr + .35);""", blur=False)
