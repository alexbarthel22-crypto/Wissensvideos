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
FOLLOW_CSS = """    .fbtn { position: absolute; left: 0; right: 0; margin: 0 auto; width: 420px; height: 120px; border-radius: 60px; background: #fe2c55; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; display: grid; place-items: center; box-shadow: 0 0 0 5px #2a1b12, 0 12px 0 rgba(0,0,0,.25); }
    .fbtn2 { position: absolute; inset: 0; border-radius: 60px; background: #fff; color: #0a78c2; display: grid; place-items: center; opacity: 0; }
    .fhand { position: absolute; font-size: 120px; }"""
def follow_js(p, t_tap):
    return f"""tl.fromTo("#{p}-btn", {{ opacity: 0, scale: .3 }}, {{ opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }}, {t_tap} - .9);
      tl.fromTo("#{p}-hand", {{ opacity: 0, x: 160, y: 160 }}, {{ opacity: 1, x: 0, y: 0, duration: .3, ease: "power3.out" }}, {t_tap} - .4);
      tl.to("#{p}-hand", {{ y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }}, {t_tap} - .05);
      tl.to("#{p}-btn2", {{ opacity: 1, duration: .05 }}, {t_tap} + .05);
      tl.fromTo("#{p}-btn", {{ scale: 1 }}, {{ scale: 1.15, duration: .12, yoyo: true, repeat: 1 }}, {t_tap} + .05);
      tl.to("#{p}-hand", {{ opacity: 0, duration: .25 }}, {t_tap} + .6);"""

# s01 – Hook: Geschenk + Haus
scene("s01", """    .s01-st { position: absolute; width: 190px; height: 190px; border-radius: 50%; background: #fff; display: grid; place-items: center; font-size: 120px;
      box-shadow: 0 0 0 7px #ffc93c, 0 0 0 12px #2a1b12, 0 14px 24px rgba(0,40,80,.35); }
    .s01-ring { position: absolute; width: 190px; height: 190px; border-radius: 50%; border: 8px solid #fff; opacity: 0; }""",
"""      <div class="s01-ring" style="left:180px;top:300px"></div><div class="s01-ring" style="left:710px;top:300px"></div>
      <div class="s01-st" id="s01-g" style="left:180px;top:300px">🎁</div><div class="s01-st" id="s01-h" style="left:710px;top:300px">🏠</div>""",
"""      const sc = at("L1", "schenke"), ha = at("L1", "Haus");
      tl.set(["#s01-g", "#s01-h"], { opacity: 1 }, 0);
      tl.fromTo("#s01-g", { rotation: -10 }, { rotation: 10, y: -16, duration: .35, yoyo: true, repeat: 9, ease: "sine.inOut" }, 0);
      tl.fromTo("#s01-h", { scale: 1 }, { scale: 1.25, rotation: 8, duration: .14, yoyo: true, repeat: 1, ease: "power2.out" }, ha - .02);
      tl.to("#s01-h", { y: -16, rotation: -6, duration: .38, yoyo: true, repeat: 7, ease: "sine.inOut" }, ha + .3);
      tl.fromTo(".s01-ring", { opacity: .9, scale: .8 }, { opacity: 0, scale: 2.2, duration: .7, ease: "power2.out", stagger: .12, immediateRender: false }, ha);""")

# s02 – Muschel-Tal Rundgang
scene("s02", STK + """
    #s02-t { top: 300px; font-size: 54px; background: #ff6a1a; }
    #s02-n { top: 430px; font-size: 46px; background: #e8467c; }""",
"""      <div id="s02-t" class="stk2">🌴 MUSCHEL-TAL</div>
      <div id="s02-n" class="stk2">🏠 Jede Hütte = ein @Name</div>""",
"""      tl.fromTo("#s02-t", { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: .45, ease: "back.out(2)" }, line("L2")[0]);
      tl.to("#s02-t", { rotation: 2, duration: .4, yoyo: true, repeat: 3, ease: "sine.inOut" }, line("L2")[0] + .6);
      tl.fromTo("#s02-n", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .4, ease: "back.out(2.6)" }, line("L3")[0] + .2);""")

# s03 – Folgen = einziehen
scene("s03", STK + "\n" + FOLLOW_CSS + """
    #s03-t { top: 300px; font-size: 52px; background: #ff6a1a; }
    #s03-btn { top: 470px; } #s03-hand { left: 690px; top: 520px; }
    #s03-at { top: 640px; font-size: 44px; background: #e8467c; }""",
"""      <div id="s03-t" class="stk2">FOLGEN = EINZIEHEN 🏝️</div>
      <div id="s03-btn" class="fbtn">+ Folgen<div id="s03-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s03-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s03-at" class="stk2">@muscheltal</div>""",
"""      const fo = at("L4", "folg");
      tl.fromTo("#s03-t", { opacity: 0, scale: 2, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.4)" }, line("L4")[0]);
      """ + follow_js("s03", "fo") + """
      tl.fromTo("#s03-at", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "power3.out" }, fo + .3);""")

# s04 – Kokos-Küste: nächster Bewohner, Häuser frei, 75 Bewohner
scene("s04", STK + """
    #s04-t { top: 300px; font-size: 64px; background: #ff6a1a; }
    #s04-f { top: 430px; font-size: 46px; background: #2e9e5b; }
    #s04-c { position: absolute; left: 0; right: 0; margin: 0 auto; top: 560px; width: fit-content; padding: 4px 36px 10px; border-radius: 36px; background: #fff; border: 6px solid #ff6a1a;
      font-family: "Inter", sans-serif; color: #2a1b12; font-weight: 900; font-size: 40px; display: flex; align-items: baseline; gap: 14px; box-shadow: 0 10px 0 rgba(0,40,80,.3); }
    #s04-c b { font-size: 100px; color: #ff6a1a; line-height: 1; }""",
"""      <div id="s04-t" class="stk2">🥥 KOKOS-KÜSTE</div>
      <div id="s04-f" class="stk2">✅ Hier sind noch Häuser frei!</div>
      <div id="s04-c"><b id="s04-n">0</b>BEWOHNER</div>""",
"""      const ko = at("L5", "Kokos"), fr = at("L5", "frei"), fu = at("L6", "75");
      tl.fromTo("#s04-t", { opacity: 0, scale: .3, rotation: -10 }, { opacity: 1, scale: 1, rotation: -2, duration: .45, ease: "back.out(2.6)" }, ko - .1);
      tl.fromTo("#s04-f", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, fr - .3);
      tl.to("#s04-f", { scale: 1.06, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, fr + .2);
      tl.fromTo("#s04-c", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, fu - .5);
      count(tl, "#s04-n", 0, 75, fu - .4, .9);""")

# s05 – Nächstes Video: Gebäude + Berufe, folgen
scene("s05", STK + "\n" + FOLLOW_CSS + """
    #s05-t { top: 300px; font-size: 52px; background: #e8467c; }
    .s05-k { position: absolute; top: 420px; width: 400px; height: 250px; border-radius: 34px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 14px 0 rgba(0,0,0,.35); overflow: hidden; text-align: center; font-family: "Inter", sans-serif; }
    .s05-k .e { height: 160px; display: grid; place-items: center; font-size: 110px; background: linear-gradient(180deg, #bfefff, #fff); }
    .s05-k .l { height: 90px; display: grid; place-items: center; font-weight: 900; font-size: 38px; color: #fff; }
    #s05-btn { top: 760px; } #s05-hand { left: 690px; top: 810px; }""",
"""      <div id="s05-t" class="stk2">🎬 IM NÄCHSTEN VIDEO</div>
      <div class="s05-k" id="s05-k1" style="left:90px"><div class="e">🏗️</div><div class="l" style="background:#ff6a1a">ERSTE GEBÄUDE</div></div>
      <div class="s05-k" id="s05-k2" style="left:590px"><div class="e">👷</div><div class="l" style="background:#2e9e5b">BERUFE</div></div>
      <div id="s05-btn" class="fbtn">+ Folgen<div id="s05-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s05-hand" class="fhand" data-layout-ignore>👆</div>""",
"""      const ge = at("L7", "Gebäude"), be = at("L7", "Berufe"), fo = at("L8", "folgen");
      tl.fromTo("#s05-t", { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: .4, ease: "back.out(2)" }, line("L7")[0]);
      tl.fromTo("#s05-k1", { opacity: 0, scale: 0, rotation: -14 }, { opacity: 1, scale: 1, rotation: -3, duration: .45, ease: "back.out(2.2)" }, ge - .1);
      tl.fromTo("#s05-k2", { opacity: 0, scale: 0, rotation: 14 }, { opacity: 1, scale: 1, rotation: 3, duration: .45, ease: "back.out(2.2)" }, be - .1);
      tl.to(["#s05-k1", "#s05-k2"], { y: -14, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut", stagger: .15 }, be + .5);
      """ + follow_js("s05", "fo"))

# s06 – Was fehlt dir? Kommentieren + Nachbarn markieren
scene("s06", STK + """
    #s06-t { top: 300px; font-size: 52px; background: #ff6a1a; }
    #s06-sheet { top: 440px; }""",
f"""      <div id="s06-t" class="stk2">💬 WAS FEHLT DIR NOCH?</div>
      <div id="s06-sheet" class="tk"><div class="tk-h">Kommentare<b>×</b></div>
        {tk("s06-c1", "#ff6a1a", "?", "dein.name", "ein Kino 🍿 @bestie zieh neben mich!", "1.204")}
        {tk("s06-c2", "#2e9e5b", "?", "dein.nachbar", "Freibad!! 🏊 @mein.bruder du auch", "873")}
      </div>""",
"""      const l0 = line("L9")[0], ko = at("L9", "Kommentare"), na = at("L9", "Nachbar");
      tl.fromTo("#s06-t", { opacity: 0, scale: 2, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.4)" }, l0);
      tl.fromTo("#s06-sheet", { opacity: 0, y: 500 }, { opacity: 1, y: 0, duration: .45, ease: "power4.out" }, ko - .3);
      tl.fromTo(["#s06-c1", "#s06-c2"], { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: .3, ease: "power3.out", stagger: .25 }, ko);
      tkLike(tl, "#s06-c1", ko + .5, 1204, 1391, 1.4, 3); tkLike(tl, "#s06-c2", na, 873, 960, 1.2, 5);
      tl.to("#s06-sheet", { rotation: 1.2, duration: .22, yoyo: true, repeat: 5, ease: "sine.inOut" }, na);""", blur=False)
