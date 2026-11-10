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


NA = (D.parent / "werkzeug" / "slot_a.txt").read_text().split(); NB = (D.parent / "werkzeug" / "slot_b.txt").read_text().split()
WA, WB = NA.index("emiliamarie155"), NB.index("lea.3818730")
PILL = """.pl { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; padding: 8px 28px 12px; border-radius: 999px; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); white-space: nowrap; }"""
FOLLOW = """    .fbtn { position: absolute; left: 0; right: 0; margin: 0 auto; width: 420px; height: 120px; border-radius: 60px; background: #fe2c55; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; display: grid; place-items: center; box-shadow: 0 0 0 5px #2a1b12, 0 12px 0 rgba(0,0,0,.25); }
    .fbtn2 { position: absolute; inset: 0; border-radius: 60px; background: #fff; color: #0a78c2; display: grid; place-items: center; opacity: 0; }
    .fhand { position: absolute; font-size: 120px; }"""
KASSE = """    .ks { position: absolute; left: 70px; right: 70px; padding: 18px 28px 22px; border-radius: 32px; background: #fff; box-shadow: 0 0 0 6px #2a1b12, 0 12px 0 rgba(0,0,0,.3); font-family: "Inter", sans-serif; color: #2a1b12; }
    .ks .row { display: flex; align-items: baseline; justify-content: space-between; font-weight: 900; font-size: 38px; }
    .ks .row b { font-size: 70px; color: #e8262f; line-height: 1; } .ks .row span { font-size: 34px; color: #6b6f8a; }
    .ks .bar { height: 30px; border-radius: 15px; background: #ece4d8; margin-top: 12px; overflow: hidden; } .ks .bar i { display: block; height: 100%; width: 0; border-radius: 15px; background: linear-gradient(90deg, #e8262f, #ff8a3a); }"""
KHTML = lambda p: f'<div id="{p}-ks" class="ks"><div class="row"><div>🐾 Tierheim Pfotenkuss</div><div><b id="{p}-kn">505</b><span> / 2.000 🐚</span></div></div><div class="bar"><i id="{p}-kb"></i></div></div>'

# s01 – Hilfe! Tiere, Kasse, 299 Follower
scene("s01", LILITA + "\n    " + PILL + "\n" + KASSE + """
    #s01-h { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 300px; padding: 4px 50px 16px; border-radius: 30px; background: #e8262f; color: #fff; font-family: "Lilita One", sans-serif; font-size: 170px; line-height: 1; box-shadow: 0 0 0 7px #2a1b12, 0 14px 0 rgba(0,0,0,.3); transform: rotate(-4deg); }
    #s01-ks { top: 330px; }
    #s01-f { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; top: 540px; padding: 6px 34px 12px; border-radius: 30px; background: #fff; border: 6px solid #e8262f; font-family: "Inter", sans-serif; font-weight: 900; color: #2a1b12; font-size: 40px; text-align: center; box-shadow: 0 10px 0 rgba(0,0,0,.25); }
    #s01-f b { display: block; font-size: 96px; color: #e8262f; line-height: 1; }
    .s01-e { position: absolute; width: 130px; height: 130px; border-radius: 50%; background: #fff; display: grid; place-items: center; font-size: 80px; box-shadow: 0 0 0 6px #ffc93c, 0 0 0 11px #2a1b12, 0 10px 18px rgba(0,0,0,.3); }""",
f"""      <div id="s01-h">🆘 HILFE!</div>
      <div class="s01-e" id="s01-e1" style="left:60px;top:560px">🥺</div><div class="s01-e" id="s01-e2" style="left:890px;top:600px">🐶</div><div class="s01-e" id="s01-e3" style="left:110px;top:760px">🐱</div>
      {KHTML("s01")}
      <div id="s01-f">Es fehlen nur noch<b>299</b>Follower!</div>""",
"""      const hu = at("L1", "Hunde"), ko = at("L2", "kostet"), ka = at("L2", "Kasse"), fe = at("L3", "fehlen"), st = at("L3", "Straße");
      tl.fromTo("#s01-h", { opacity: 0, scale: 3.2 }, { opacity: 1, scale: 1, duration: .16, ease: "power4.in" }, 0);
      tl.to("#s01-h", { x: 10, duration: .05, yoyo: true, repeat: 7 }, .18);
      tl.to("#s01-h", { scale: 1.08, duration: .2, yoyo: true, repeat: 5, ease: "sine.inOut" }, .7);
      [["#s01-e1", 0], ["#s01-e2", .15], ["#s01-e3", .3]].forEach(([e, d]) => { tl.fromTo(e, { scale: 0, rotation: -40 }, { scale: 1, rotation: 0, duration: .45, ease: "elastic.out(1, .5)" }, hu - .2 + d); tl.to(e, { y: -14, duration: .35, yoyo: true, repeat: 5, ease: "sine.inOut" }, hu + .4 + d); });
      tl.to(["#s01-h", ".s01-e"], { opacity: 0, scale: .6, duration: .2 }, ko - .45);
      tl.fromTo("#s01-ks", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }, ko - .3);
      tl.fromTo("#s01-kb", { width: "0%" }, { width: "25.25%", duration: .8, ease: "power2.out" }, ka);
      tl.to("#s01-kb", { opacity: .35, duration: .2, yoyo: true, repeat: 7 }, ka + .8);
      tl.fromTo("#s01-f", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, fe - .1);
      tl.to("#s01-f", { scale: 1.07, duration: .22, yoyo: true, repeat: 7, ease: "sine.inOut" }, st);""")

# s02 – Açaí-Stand
scene("s02", PILL + """
    #s02-t { top: 300px; font-size: 58px; background: #7b3fe0; }
    #s02-l { top: 410px; font-size: 38px; background: #fff; color: #7b3fe0; }
    .s02-n { font-size: 38px; background: #fff; color: #2a1b12; }""",
"""      <div id="s02-t" class="pl">🫐 AÇAÍ-STAND</div>
      <div id="s02-l" class="pl">eröffnet von Bürgermeisterin Lilly 🎖️</div>
      <div id="s02-n0" class="pl s02-n" style="top:520px">⭐ Filipa · @vidafilipa</div>
      <div id="s02-n1" class="pl s02-n" style="top:610px">Marina · @marina.cgnn</div>
      <div id="s02-n2" class="pl s02-n" style="top:700px">Johanna · @borbie20</div>
      <div id="s02-n3" class="pl s02-n" style="top:790px">@lp_art18</div>""",
"""      const ac = at("L4", "Açaí-Stand"), li = at("L4", "Lilly"), ns = [at("L4", "Filipa"), at("L4", "Marina"), at("L4", "Johanna"), at("L4", "lp_art18")];
      tl.fromTo("#s02-t", { opacity: 0, scale: .3, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: .4, ease: "back.out(2.6)" }, ac - .15);
      tl.fromTo("#s02-l", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, li - .2);
      ns.forEach((t, i) => tl.fromTo("#s02-n" + i, { opacity: 0, x: i % 2 ? 120 : -120 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, t - .15));""")

# s03 – Moped-Werkstatt
scene("s03", PILL + """
    #s03-t { top: 300px; font-size: 58px; background: #e2560c; }
    .s03-n { font-size: 42px; background: #fff; color: #2a1b12; }""",
"""      <div id="s03-t" class="pl">🔧 MOPED-WERKSTATT</div>
      <div id="s03-n0" class="pl s03-n" style="top:420px">⭐ @bruecke.2803</div>
      <div id="s03-n1" class="pl s03-n" style="top:515px">@anti.teamtoxic</div>""",
"""      const mo = at("L5", "Moped-Werkstatt"), a = at("L5", "bruecke.2803"), b = at("L5", "anti.teamtoxic");
      tl.fromTo("#s03-t", { opacity: 0, scale: .3, rotation: 8 }, { opacity: 1, scale: 1, rotation: 2, duration: .4, ease: "back.out(2.6)" }, mo - .15);
      tl.fromTo("#s03-n0", { opacity: 0, x: -120 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, a - .15);
      tl.fromTo("#s03-n1", { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: .3, ease: "back.out(2)" }, b - .15);""")

# s04 – Pool für Luise
scene("s04", PILL + """
    #s04-t { top: 300px; font-size: 52px; background: #18a6b8; }""",
"""      <div id="s04-t" class="pl">🏊 Pool für @luisedbr.11!</div>""",
"""      const po = at("L6", "Pool"), kr = at("L6", "kriegst");
      tl.fromTo("#s04-t", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, po - .2);
      tl.to("#s04-t", { scale: 1.1, duration: .18, yoyo: true, repeat: 5, ease: "sine.inOut" }, kr);""")

# s05 – Villa: Doppel-Spielautomat
def col(names, w, cid): return f'<div class="s05-col" id="{cid}">' + "".join(f'<div class="s05-r{" s05-win" if i == w else ""}" id="{cid}-{i}">@{n}</div>' for i, n in enumerate(names)) + "</div>"
scene("s05", PILL + "\n    " + CF_CSS.replace("top: 700px", "top: 640px") + """
    #s05-dim { position: absolute; inset: 0; background: rgba(10,12,40,.55); }
    #s05-t { top: 300px; font-size: 48px; background: #18a6b8; }
    .s05-box { position: absolute; top: 450px; width: 470px; height: 390px; border-radius: 34px; background: #fff; overflow: hidden;
      box-shadow: 0 0 0 7px #2a1b12, 0 0 0 14px #ffc93c, 0 0 0 19px #2a1b12, 0 18px 0 rgba(0,0,0,.35); }
    #s05-ba { left: 55px; } #s05-bb { left: 555px; }
    .s05-band { position: absolute; left: 0; right: 0; top: 130px; height: 130px; background: #fff3c4; border-top: 5px solid #ffc93c; border-bottom: 5px solid #ffc93c; }
    .s05-col { position: absolute; left: 0; right: 0; top: 0; }
    .s05-r { height: 130px; display: grid; place-items: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 38px; color: #23285a; white-space: nowrap; }
    .s05-sh { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,.95)); }
    #s05-fv { position: absolute; left: 55px; width: 970px; top: 875px; text-align: center; white-space: nowrap; font-family: "Inter", sans-serif; font-weight: 800; font-size: 30px; color: #fff; text-shadow: 0 2px 6px rgba(0,0,0,.6); }
    #s05-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 880px; color: #e8433c; border-color: #e8433c; transform: rotate(-4deg); font-size: 56px; white-space: nowrap; background: #fff; }
    #s05-nb { top: 300px; font-size: 44px; background: #2e9e5b; }
    #s05-w1 { top: 400px; font-size: 44px; background: #fff; color: #2a1b12; } #s05-w2 { top: 490px; font-size: 44px; background: #fff; color: #2a1b12; }""",
f"""      <div id="s05-dim"></div>
      <div id="s05-t" class="pl">🏖️ VERLOSUNG: STRANDVILLA</div>
      <div class="s05-box" id="s05-ba"><div class="s05-band" id="s05-bda"></div>{col(NA, WA, "s05-ca")}<div class="s05-sh" data-layout-ignore></div></div>
      <div class="s05-box" id="s05-bb"><div class="s05-band" id="s05-bdb"></div>{col(NB, WB, "s05-cb")}<div class="s05-sh" data-layout-ignore></div></div>
      <div id="s05-fv">➕ Folgen, um bei der nächsten Verlosung teilzunehmen</div>
      <div id="s05-cfw"></div>
      <div id="s05-st" class="stamp" data-layout-ignore>🏖️ VILLA-BEWOHNER!</div>
      <div id="s05-nb" class="pl">🏡 Neue Bewohner der Strandvilla</div>
      <div id="s05-w1" class="pl">🎉 @emiliamarie155</div>
      <div id="s05-w2" class="pl">🎉 @lea.3818730</div>""",
f"""      const s0 = at("L7", "zwei") + .5, TB = line("L8")[0] - .4, TA = TB - .75, H = 130, NA = {len(NA)}, NB = {len(NB)}, WA = {WA}, WB = {WB}, T0 = TB, gl = at("L8", "Glückwunsch");
      tl.fromTo("#s05-dim", {{ opacity: 0 }}, {{ opacity: 1, duration: .4 }}, line("L7")[0]);
      tl.fromTo("#s05-t", {{ opacity: 0, scale: .3 }}, {{ opacity: 1, scale: 1, duration: .4, ease: "back.out(2.6)" }}, line("L7")[0] + .1);
      tl.fromTo(".s05-box", {{ opacity: 0, scale: .5 }}, {{ opacity: 1, scale: 1, duration: .4, ease: "back.out(2)", stagger: .1 }}, at("L7", "lose") - .3);
      tl.fromTo("#s05-fv", {{ opacity: 0 }}, {{ opacity: 1, duration: .3 }}, at("L7", "lose"));
      tl.set("#s05-ca", {{ y: -(NA - 3) * H }}, 0); tl.set("#s05-cb", {{ y: -(NB - 3) * H }}, 0);
      tl.fromTo("#s05-ca", {{ y: -(NA - 3) * H }}, {{ y: -(WA - 1) * H, duration: TA - s0, ease: "power3.out", immediateRender: false }}, s0);
      tl.fromTo("#s05-cb", {{ y: -(NB - 3) * H }}, {{ y: -(WB - 1) * H, duration: TB - s0, ease: "power3.out", immediateRender: false }}, s0);
      tl.fromTo(".s05-col", {{ filter: "blur(5px)" }}, {{ filter: "blur(0px)", duration: (TA - s0) * .8, ease: "power2.in", immediateRender: false }}, s0);
      tl.to("#s05-ca-" + WA, {{ color: "#e8433c", scale: 1.15, duration: .2, ease: "back.out(3)" }}, TA);
      tl.to("#s05-bda", {{ backgroundColor: "#ffd23f", duration: .15, yoyo: true, repeat: 5 }}, TA);
      tl.to("#s05-cb-" + WB, {{ color: "#e8433c", scale: 1.15, duration: .2, ease: "back.out(3)" }}, TB);
      tl.to("#s05-bdb", {{ backgroundColor: "#ffd23f", duration: .15, yoyo: true, repeat: 5 }}, TB);
      tl.to("#s05-fv", {{ opacity: 0, duration: .2 }}, TB);
      tl.fromTo("#s05-st", {{ opacity: 0, scale: 2.6 }}, {{ opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }}, TB + .2);
      """ + CONF_JS.replace("SEED", "33").replace("BOX", "s05-cfw") + f"""
      tl.to("#s05-t", {{ opacity: 0, duration: .2 }}, TB);
      const di = at("L8", "Villa");
      tl.to([".s05-box", "#s05-st", "#s05-dim"], {{ opacity: 0, duration: .25 }}, di - .3);
      tl.fromTo("#s05-nb", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: .35, ease: "back.out(2)" }}, di - .1);
      tl.fromTo(["#s05-w1", "#s05-w2"], {{ opacity: 0, scale: .4 }}, {{ opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)", stagger: .15 }}, di + .1);""", blur=False)

# s06 – Fabienne-Kommentar (Original-Layout) + Abstimmung
scene("s06", PILL + """
    #s06-c { position: absolute; left: 50px; right: 50px; top: 290px; padding: 30px 30px 34px; border-radius: 34px; background: #1f1f1f; box-shadow: 0 0 0 5px #000, 0 16px 30px rgba(0,0,0,.45); font-family: "Inter", sans-serif; color: #fff; display: flex; gap: 26px; }
    #s06-c .av { width: 104px; height: 104px; border-radius: 50%; background: url(assets/img/fab_avatar.png) center/cover; flex: none; }
    #s06-c .nm { font-size: 34px; color: #a8a8a8; font-weight: 600; } #s06-c .tx { font-size: 38px; line-height: 1.32; margin-top: 6px; font-weight: 500; }
    #s06-c .ph { width: 300px; height: 340px; border-radius: 12px; margin-top: 18px; background: url(assets/img/fab_dog.jpg) center/cover; }
    #s06-c .mt { font-size: 28px; color: #8a8a8a; margin-top: 14px; font-weight: 600; }
    #s06-v { position: absolute; left: 90px; right: 90px; top: 960px; display: flex; gap: 24px; }
    #s06-v div { flex: 1; text-align: center; padding: 14px 0 18px; border-radius: 26px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; color: #fff; box-shadow: 0 0 0 5px #2a1b12, 0 10px 0 rgba(0,0,0,.25); }
    #s06-q { top: 870px; font-size: 40px; background: #e2560c; }""",
"""      <div id="s06-c"><div class="av"></div><div><div class="nm">Fabienne</div><div class="tx">Wir brauchen noch eine Bäckerei wo ich dann drüber wohne und dort backe.Kann sehr gut Cookies und Zimtschnecken backen.</div><div class="ph"></div><div class="mt">@fabienne3692 · Antworten</div></div></div>
      <div id="s06-q" class="pl">🥐 Soll Fabienne eine Bäckerei eröffnen?</div>
      <div id="s06-v"><div style="background:#2e9e5b">✅ JA</div><div style="background:#e8262f">❌ NEIN</div></div>""",
"""      const fa = at("L9", "Fabienne"), so = at("L9", "Soll"), stm = at("L9", "Stimmt");
      tl.fromTo("#s06-c", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: .45, ease: "power4.out" }, fa - .2);
      tl.fromTo("#s06-q", { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, so - .15);
      tl.fromTo("#s06-v div", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)", stagger: .12 }, stm - .2);
      tl.to("#s06-v div", { scale: 1.08, duration: .22, yoyo: true, repeat: 5, ease: "sine.inOut", stagger: .1 }, stm + .3);""", blur=False)

# s07 – Welches Tier? + Folgen
scene("s07", PILL + "\n" + FOLLOW + "\n" + KASSE + """
    #s07-q { top: 300px; font-size: 44px; background: #7b3fe0; }
    #s07-ks { top: 410px; }
    #s07-btn { top: 640px; } #s07-hand { left: 690px; top: 690px; }
    #s07-r { top: 790px; font-size: 42px; background: #2e9e5b; }""",
f"""      <div id="s07-q" class="pl">🐶🐱 Welches Tier willst du adoptieren?</div>
      {KHTML("s07")}
      <div id="s07-btn" class="fbtn">+ Folgen<div id="s07-btn2" class="fbtn2">✓ Gefolgt</div></div>
      <div id="s07-hand" class="fhand" data-layout-ignore>👆</div>
      <div id="s07-r" class="pl">🐚 +5 Muscheln für die Tiere</div>""",
"""      const ti = at("L10", "Tier"), fo = at("L10", "Folgt"), re = at("L10", "rettet");
      tl.fromTo("#s07-q", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2.6)" }, ti - .2);
      tl.fromTo("#s07-ks", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, ti + .3);
      tl.set("#s07-kb", { width: "25.25%" }, 0);
      tl.fromTo("#s07-btn", { opacity: 0, scale: .3 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2.6)" }, fo - .5);
      tl.fromTo("#s07-hand", { opacity: 0, x: 160, y: 160 }, { opacity: 1, x: 0, y: 0, duration: .25, ease: "power3.out" }, fo - .3);
      tl.to("#s07-hand", { y: -26, scale: .9, duration: .1, yoyo: true, repeat: 1 }, fo);
      tl.to("#s07-btn2", { opacity: 1, duration: .05 }, fo + .1);
      tl.fromTo("#s07-btn", { scale: 1 }, { scale: 1.15, duration: .12, yoyo: true, repeat: 1, immediateRender: false }, fo + .1);
      tl.to("#s07-hand", { opacity: 0, duration: .25 }, fo + .6);
      count(tl, "#s07-kn", 505, 510, fo + .2, .4);
      tl.to("#s07-kb", { width: "25.5%", duration: .4 }, fo + .2);
      tl.fromTo("#s07-r", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: "back.out(2)" }, fo + .3);
      tl.to("#s07-r", { scale: 1.08, duration: .22, yoyo: true, repeat: 5, ease: "sine.inOut" }, re);""", blur=False)
