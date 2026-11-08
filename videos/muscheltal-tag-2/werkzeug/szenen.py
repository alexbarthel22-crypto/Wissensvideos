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

# s01 – Party: 0 -> 575 Bewohner, Hauptinsel voll
scene("s01", f"""    {CF_CSS}
    #s01-c {{ position: absolute; left: 0; right: 0; margin: 0 auto; top: 300px; width: fit-content; padding: 6px 40px 12px; border-radius: 40px; background: #fff; border: 7px solid #ff6a1a;
      font-family: "Inter", sans-serif; color: #0a78c2; font-weight: 900; font-size: 44px; display: flex; flex-direction: column; align-items: center; gap: 0; line-height: 1; box-shadow: 0 12px 0 rgba(0,40,80,.3); }}
    #s01-c b {{ font-size: 130px; color: #ff6a1a; line-height: 1; }}
    #s01-f {{ position: absolute; left: 0; right: 0; margin: 0 auto; top: 540px; width: fit-content; padding: 8px 28px 12px; border-radius: 999px; background: #fe2c55; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 42px; box-shadow: 0 8px 0 rgba(0,0,0,.25); white-space: nowrap; }}
    #s01-st {{ left: 0; right: 0; margin: 0 auto; width: fit-content; top: 640px; color: #e8433c; border-color: #e8433c; transform: rotate(-6deg); font-size: 60px; white-space: nowrap; }}
    .s01-em {{ position: absolute; width: 150px; height: 150px; border-radius: 50%; background: #fff; display: grid; place-items: center; font-size: 92px;
      box-shadow: 0 0 0 7px #ffc93c, 0 12px 24px rgba(0,40,80,.35); }}
    .s01-ring {{ position: absolute; width: 150px; height: 150px; border-radius: 50%; border: 8px solid #fff; opacity: 0; }}
    .s01-sp {{ position: absolute; width: 56px; height: 56px; }}""",
"""      <div id="s01-cfw"></div>
      <div id="s01-c"><b id="s01-n">0</b>BEWOHNER</div>
      <div id="s01-f">➕ Folge mir, um auch einzuziehen!</div>
      <div id="s01-st" class="stamp">HAUPT-INSEL VOLL!</div>
      <div class="s01-ring" style="left:30px;top:300px"></div><div class="s01-ring" style="left:890px;top:290px"></div>
      <div class="s01-em" id="s01-e1" style="left:30px;top:300px">🥳</div><div class="s01-em" id="s01-e2" style="left:890px;top:290px">🎉</div>
      <svg class="s01-sp" style="left:300px;top:265px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#fff"/></svg>
      <svg class="s01-sp" style="left:730px;top:420px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="#ffc93c"/></svg>""",
"""      const n = at("L1", "575"), vo = at("L2", "voll"), T0 = n;
      tl.set("#s01-c", { opacity: 1 }, 0);
      count(tl, "#s01-n", 0, 575, 0, at("L1", "575") + .1, "", "", "power1.in");
      tl.fromTo("#s01-c", { scale: 1 }, { scale: 1.18, duration: .15, yoyo: true, repeat: 3, ease: "sine.inOut" }, n);
      tl.fromTo("#s01-e1", { scale: 0, rotation: -120 }, { scale: 1, rotation: -12, duration: .6, ease: "elastic.out(1, .45)" }, n);
      tl.fromTo("#s01-e2", { scale: 0, rotation: 120 }, { scale: 1, rotation: 12, duration: .6, ease: "elastic.out(1, .45)" }, n + .12);
      tl.fromTo(".s01-ring", { opacity: .9, scale: .8 }, { opacity: 0, scale: 2.2, duration: .7, ease: "power2.out", stagger: .12, immediateRender: false }, n + .05);
      tl.fromTo(".s01-ring", { opacity: .7, scale: .8 }, { opacity: 0, scale: 2.0, duration: .7, ease: "power2.out", stagger: .12, immediateRender: false }, n + 1.1);
      tl.to("#s01-e1", { y: -22, rotation: 6, scale: 1.08, duration: .38, yoyo: true, repeat: 7, ease: "sine.inOut" }, n + .6);
      tl.to("#s01-e2", { y: -18, rotation: -6, scale: 1.08, duration: .42, yoyo: true, repeat: 7, ease: "sine.inOut" }, n + .7);
      tl.fromTo(".s01-sp", { scale: 0, rotation: 0, opacity: 0 }, { scale: 1.3, rotation: 180, opacity: 1, duration: .4, ease: "back.out(3)", stagger: .15, yoyo: true, repeat: 5 }, n + .2);
      tl.fromTo("#s01-f", { opacity: 0, y: -30, scale: .6 }, { opacity: 1, y: 0, scale: 1, duration: .35, ease: "back.out(2.6)" }, line("L1")[1] + .2);
      tl.to("#s01-f", { scale: 1.07, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, line("L1")[1] + .7);
      tl.fromTo("#s01-st", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, vo - .05);
      """ + CONF_JS.replace("SEED", "11").replace("BOX", "s01-cfw"))

# s02 – Hütten mit Namen, findest du deinen?
scene("s02", """    #s02-t { top: 300px; font-size: 52px; white-space: nowrap; max-width: none; }
    #s02-q { top: 430px; font-size: 44px; white-space: nowrap; max-width: none; }
    #s02-ok { left: 330px; top: 420px; color: #2e9e5b; border-color: #2e9e5b; transform: rotate(-6deg); font-size: 80px; }""",
"""      <div id="s02-t" class="bt or">500 HÜTTEN · 500 NAMEN</div>
      <div id="s02-q" class="bt pk">🔍 FINDEST DU DEINEN NAMEN?</div>
      <div id="s02-ok" class="stamp">ALLE DA ✓</div>""",
"""      const de = at("L3", "deinen"), al = at("L4", "Alle");
      tl.fromTo("#s02-t", { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: .4, ease: "back.out(2)" }, .05);
      tl.fromTo("#s02-q", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, de - .3);
      tl.to("#s02-q", { rotation: 2, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, de + .1);
      tl.to("#s02-q", { opacity: 0, scale: .6, duration: .15, ease: "power2.in" }, al - .2);
      tl.fromTo("#s02-ok", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, al - .05);""")

# s03 – Kokos-Küste besiedelt
scene("s03", """    #s03-t { top: 300px; font-size: 72px; white-space: nowrap; max-width: none; }
    #s03-c { position: absolute; left: 0; right: 0; margin: 0 auto; top: 450px; width: fit-content; padding: 4px 36px 10px; border-radius: 36px; background: #fff; border: 6px solid #ff6a1a;
      font-family: "Inter", sans-serif; color: #2a1b12; font-weight: 900; font-size: 40px; display: flex; align-items: baseline; gap: 14px; box-shadow: 0 10px 0 rgba(0,40,80,.3); }
    #s03-c b { font-size: 100px; color: #ff6a1a; line-height: 1; }
    #s03-h { position: absolute; left: 0; right: 0; margin: 0 auto; top: 600px; width: fit-content; padding: 8px 26px 12px; border-radius: 999px; background: #e8467c; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 40px; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); white-space: nowrap; }
    #s03-new { left: 90px; top: 440px; color: #e8433c; border-color: #e8433c; transform: rotate(10deg); font-size: 48px; }""",
"""      <div id="s03-t" class="bt or">🥥 KOKOS-KÜSTE</div>
      <div id="s03-new" class="stamp">NEU!</div>
      <div id="s03-c"><b id="s03-n">0</b>BEWOHNER</div>
      <div id="s03-h">➡️ Hier ziehen die nächsten Follower ein!</div>""",
"""      const ko = at("L5", "Kokos"), fu = at("L6", "75");
      tl.fromTo("#s03-t", { opacity: 0, scale: .3, rotation: -10 }, { opacity: 1, scale: 1, rotation: -2, duration: .45, ease: "back.out(2.6)" }, ko - .1);
      tl.fromTo("#s03-new", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, ko + .3);
      tl.fromTo("#s03-c", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, fu - .4);
      count(tl, "#s03-n", 0, 75, fu - .3, .8);
      tl.fromTo("#s03-h", { opacity: 0, y: 30, scale: .6 }, { opacity: 1, y: 0, scale: 1, duration: .4, ease: "back.out(2.6)" }, fu + .6);
      tl.to("#s03-h", { scale: 1.05, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, fu + 1.1);""")

# s04 – Muscheln
scene("s04", """    #s04-eq { top: 300px; font-size: 56px; white-space: nowrap; max-width: none; }
    #s04-c { position: absolute; left: 0; right: 0; margin: 0 auto; top: 440px; width: fit-content; padding: 6px 40px 12px; border-radius: 40px; background: #fff7d6; border: 7px solid #e0a020;
      font-family: "Inter", sans-serif; color: #7a4a00; font-weight: 900; font-size: 44px; display: flex; align-items: baseline; gap: 16px; box-shadow: 0 12px 0 rgba(120,70,0,.35); }
    #s04-c b { font-size: 120px; color: #e07a00; line-height: 1; }
    #s04-g { top: 640px; font-size: 64px; }""",
"""      <div id="s04-eq" class="bt or">1 BEWOHNER = 5 🐚</div>
      <div id="s04-c"><b id="s04-n">0</b>MUSCHELN 🐚</div>
      <div id="s04-g" class="bt gr">= 2 GEBÄUDE 🏗️</div>""",
"""      const fu = at("L7", "5"), mu = at("L7", "2.875"), zw = at("L8", "zwei");
      tl.fromTo("#s04-eq", { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: .4, ease: "back.out(2)" }, fu - .3);
      tl.fromTo("#s04-c", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, mu - .5);
      count(tl, "#s04-n", 0, 2875, mu - .3, 1.2);
      tl.fromTo("#s04-c", { scale: 1 }, { scale: 1.12, duration: .14, yoyo: true, repeat: 3 }, mu + .9);
      tl.fromTo("#s04-g", { opacity: 0, scale: 2, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.4)" }, zw - .1);""")

# s05 – Wünsche: 4 Karten, 2 werden gekauft -> Abstimmung
scene("s05", WC_CSS + """
    #s05-t { top: 300px; font-size: 52px; white-space: nowrap; max-width: none; }
    #s05-hier { position: absolute; left: 0; right: 0; margin: 0 auto; top: 760px; width: fit-content; padding: 8px 30px 12px; border-radius: 999px; background: #ff6a1a; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); white-space: nowrap; }
    #s05-hier::after { content: ""; position: absolute; left: 50%; bottom: -26px; margin-left: -18px; border: 18px solid transparent; border-top-color: #ff6a1a; border-bottom: 0; }
    #s05-ring { position: absolute; left: 340px; top: 860px; width: 400px; height: 220px; border-radius: 30px; border: 8px dashed #ff6a1a; }
    #s05-v { top: 1020px; font-size: 50px; white-space: nowrap; max-width: none; }""",
f"""      <div id="s05-t" class="bt pk">EURE WÜNSCHE VON GESTERN:</div>

      <div id="s05-hier">🏗️ HIER WIRD GEBAUT!</div>
      {cards("s05-k", [("🍹", "STRANDBAR", "#ff7a00"), ("🥙", "DÖNERBUDE", "#e8433c"), ("🥐", "BÄCKEREI", "#c98a2a"), ("🏥", "KRANKENHAUS", "#0098ff")], 420)}
      <div id="s05-v" class="bt pk">👇 STIMMT AB: 2 GEWINNEN!</div>""",
"""      const ws = [at("L9", "Strandbar"), at("L9", "Dönerbude"), at("L9", "Bäckerei"), at("L9", "Krankenhaus")], ab = at("L10", "Stimmt");
      tl.fromTo("#s05-hier", { opacity: 0, y: -40, scale: .5 }, { opacity: 1, y: 0, scale: 1, duration: .4, ease: "back.out(2.6)" }, line("L9")[0] + .3);
      tl.to("#s05-hier", { y: -14, duration: .25, yoyo: true, repeat: 3, ease: "sine.inOut" }, line("L9")[0] + .7);
      tl.to("#s05-hier", { opacity: 0, duration: .25 }, ws[0] - .3);
      tl.fromTo("#s05-t", { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, line("L9")[0] - .1);
      ws.forEach((t, i) => { tl.fromTo("#s05-k" + i, { opacity: 0, scale: 0, rotation: (i % 2 ? 14 : -14) }, { opacity: 1, scale: 1, rotation: (i % 2 ? 3 : -3), duration: .45, ease: "back.out(2.2)" }, t - .08);
        tl.to("#s05-k" + i, { y: -14, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut" }, t + .5); });
      tl.to(["#s05-k0", "#s05-k1", "#s05-k2", "#s05-k3"], { scale: 1.06, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut", stagger: .1 }, line("L10")[0]);
      tl.fromTo("#s05-v", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, ab - .1);
      tl.to("#s05-v", { rotation: 2, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, ab + .3);""")

# s06 – Bürgermeister*in gesucht, Top-Kommentar gewinnt
scene("s06", """    #s06-t { top: 300px; font-size: 52px; white-space: nowrap; max-width: none; }
    #s06-cr { position: absolute; left: 0; right: 0; top: 420px; text-align: center; font-size: 170px; }
    #s06-sheet { top: 660px; }
    .vlos { position: absolute; left: 140px; width: 800px; top: 560px; background: #fff7d6; border: 7px solid #e0a020; border-radius: 34px; text-align: center; padding: 18px 20px 24px;
      font-family: "Inter", sans-serif; box-shadow: 0 0 0 6px #fff3b0, 0 14px 0 rgba(120,70,0,.35); }
    .vl1 { display: inline-block; background: #e8467c; color: #fff; font-weight: 900; font-size: 38px; padding: 4px 22px 8px; border-radius: 999px; }
    .vl2 { font-family: "Inter", sans-serif; font-weight: 900; font-size: 84px; color: #e07a00; line-height: 1.05; margin-top: 8px; }
    .vl3 { font-weight: 800; font-size: 30px; color: #7a4a00; }
    #s06-p { top: 690px; font-size: 54px; white-space: nowrap; max-width: none; }""",
f"""      <div id="s06-t" class="bt or">BÜRGERMEISTER*IN · 1 WOCHE</div>
      <div id="s06-cr">👑</div>
      <div id="s06-sheet" class="tk"><div class="tk-h">Top-Kommentar gewinnt<b>×</b></div>
        {tk("s06-c1", "#8a3ffc", "?", "dein.name", "ich will bürgermeister*in werden 👑", "1.204")}
      </div>
      <div id="s06-p" class="bt or">🏰 WOHNT IM MUSCHELPALAST</div>
      <div id="s06-v" class="vlos"><div class="vl1">🎟️ VERLOSUNG</div><div class="vl2">PALAST-LEITUNG</div><div class="vl3">1 Woche im Palast wohnen · unter allen Followern</div></div>""",
"""      const l0 = line("L11")[0], tp = at("L12", "Top");
      tl.fromTo("#s06-t", { opacity: 0, scale: 2, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .35, ease: "back.out(2.4)" }, l0);
      tl.fromTo("#s06-cr", { opacity: 0, y: -200, rotation: -30 }, { opacity: 1, y: 0, rotation: 0, duration: .5, ease: "bounce.out" }, l0 + .3);
      tl.to("#s06-cr", { rotation: 8, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, l0 + .9);
      tl.fromTo("#s06-sheet", { opacity: 0, y: 500 }, { opacity: 1, y: 0, duration: .45, ease: "power4.out" }, tp - .4);
      tkLike(tl, "#s06-c1", tp + .2, 1204, 1388, 1.2, 3);
      const mp = at("L12", "Muschelpalast");
      tl.to("#s06-sheet", { opacity: 0, y: 300, duration: .3, ease: "power2.in" }, mp - .35);
      tl.fromTo("#s06-p", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .4, ease: "back.out(2.6)" }, mp - .05);
      const vb = line("L12b")[0], pl = at("L12b", "Palast-Leitung");
      tl.to(["#s06-p", "#s06-cr"], { opacity: 0, y: -60, duration: .3, ease: "power2.in" }, vb - .1);
      tl.fromTo("#s06-v", { opacity: 0, scale: .3, rotation: 8 }, { opacity: 1, scale: 1, rotation: -2, duration: .45, ease: "back.out(2.2)" }, vb + .1);
      tl.to("#s06-v", { scale: 1.06, duration: .18, yoyo: true, repeat: 3, ease: "sine.inOut" }, pl);""")

# s07 – Überraschung bei 1.000, folgen
scene("s07", """    #s07-t { top: 300px; font-size: 56px; white-space: nowrap; max-width: none; }
    #s07-g { position: absolute; left: 0; right: 0; top: 440px; text-align: center; font-size: 200px; }
    #s07-btn { position: absolute; left: 0; right: 0; margin: 0 auto; top: 720px; width: 420px; height: 120px; border-radius: 60px; background: #fe2c55; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; display: grid; place-items: center; box-shadow: 0 12px 0 rgba(0,0,0,.25); }
    #s07-btn2 { position: absolute; inset: 0; border-radius: 60px; background: #fff; color: #0a78c2; display: grid; place-items: center; opacity: 0; }
    #s07-hand { position: absolute; left: 690px; top: 770px; font-size: 120px; }
    #s07-at { top: 880px; font-size: 44px; }""",
"""      <div id="s07-t" class="bt pk">BEI 1.000 BEWOHNERN …</div>
      <div id="s07-g">🎁</div>
      <div id="s07-btn">+ Folgen<div id="s07-btn2">✓ Gefolgt</div></div>
      <div id="s07-hand" data-layout-ignore>👆</div>
      <div id="s07-at" class="bt or">@muscheltal</div>""",
"""      const l0 = line("L13")[0], ue = at("L13", "Überraschung"), fo = at("L14", "Folg");
      tl.fromTo("#s07-t", { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: .4, ease: "back.out(2)" }, l0);
      tl.fromTo("#s07-g", { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: .45, ease: "back.out(2.6)" }, l0 + .3);
      tl.to("#s07-g", { rotation: 10, duration: .08, yoyo: true, repeat: 13, ease: "none" }, ue - .1);
      tl.fromTo("#s07-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, line("L14")[0] - .1);
      tl.fromTo("#s07-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .3, ease: "power3.out" }, fo - .4);
      tl.to("#s07-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo - .05);
      tl.to("#s07-btn2", { opacity: 1, duration: .05 }, fo + .05);
      tl.fromTo("#s07-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1 }, fo + .05);
      tl.to("#s07-hand", { opacity: 0, duration: .25 }, fo + .6);
      tl.fromTo("#s07-at", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: .3, ease: "power3.out" }, fo + .3);
      tl.to("#s07-btn", { scale: 1.06, duration: .3, yoyo: true, repeat: 5, ease: "sine.inOut" }, fo + .5);""", blur=False)
