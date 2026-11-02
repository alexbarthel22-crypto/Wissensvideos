import json
#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Alle Männer NNN“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
from pathlib import Path

HEAD = '''<template>
  <style>
    /*__COMMON_CSS__*/
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .panel { position: absolute; border-radius: 24px; background: rgba(13,16,38,.94); text-align: center; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; }
    .vig { position: absolute; left: 0; right: 0; top: 1040px; height: 880px; background: linear-gradient(rgba(10,12,30,0), rgba(10,12,30,.5) 45%, rgba(10,12,30,.55)); pointer-events: none; }
@@CSS@@
  </style>
  <div id="root" data-composition-id="@@ID@@" data-start="0" data-duration="__DUR__" data-width="1080" data-height="1920">
@@MEDIA@@
    <div id="@@ID@@-stage" class="clip stage" data-start="0" data-duration="__DUR__" data-track-index="0">
@@HTML@@
      <div class="vig"></div>
    </div>
  </div>
  <script>
    (() => {
      /*__CUE_HELPERS__*/
/*__COMMON_JS__*/
      const tl = gsap.timeline({ paused: true });
@@JS@@
      window.__timelines["@@ID@@"] = tl;
    })();
  </script>
</template>
'''
OUT = '\n      tl.to("#@@ID@@-stage > *", { opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }, C.__dur - 0.18);'
SVG = '      <svg id="@@ID@@-svg" class="full" viewBox="0 0 1080 1920"></svg>'
S = {}
FLAT = '''    .flat { position: absolute; border-radius: 26px; background: rgba(255,255,255,.94); box-shadow: 0 18px 50px rgba(0,0,0,.35); opacity: 0; text-align: center; color: #22283f; }'''
BIG = '''    .big { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; color: #fff; opacity: 0; text-shadow: 0 2px 18px rgba(0,0,0,.6); }
    .big b { display: block; font: 600 150px/1 "EB Garamond", serif; color: #1f5fb8; text-shadow: 0 0 30px rgba(255,255,255,.9); } .big i { color: #1d2b4a; text-shadow: 0 0 12px rgba(255,255,255,.9); } .big i { display: block; margin-top: 6px; font: 600 28px Inter, sans-serif; font-style: normal; letter-spacing: .18em; }'''
FLAT2 = FLAT + '''
    .fc { position: absolute; border-radius: 24px; background: rgba(255,255,255,.94); box-shadow: 0 18px 50px rgba(0,0,0,.35); opacity: 0; text-align: center; color: #22283f; padding: 22px 30px; font: 500 46px/1.15 "EB Garamond", serif; }
    .fc b { color: #e0484f; }'''
COLS = '["#5b6a8f", "#6f7da3", "#4e5b7e", "#7c88ad"]'

CARD = '''    .cd { position: absolute; left: 140px; width: 800px; height: 130px; border-radius: 24px; background: rgba(255,255,255,.95); box-shadow: 0 18px 50px rgba(0,0,0,.4);
      color: #22283f; font: 900 64px/130px Inter, sans-serif; text-align: center; opacity: 0; }
    #s02-stage .cd { height: 100px; font: 900 56px/100px Inter, sans-serif; }
    #s02-stage .cd s { top: 46px; }
    .cd s { position: absolute; left: 60px; right: 60px; top: 62px; height: 10px; border-radius: 5px; background: #ff3b55; transform: scaleX(0); transform-origin: 0 50%; }
    .bdg { position: absolute; left: 190px; width: 700px; height: 92px; border-radius: 46px; background: rgba(12,40,30,.92); border: 4px solid #39e27a; color: #fff;
      font: 800 46px/84px Inter, sans-serif; text-align: center; opacity: 0; box-shadow: 0 0 34px rgba(57,226,122,.45); }
    .bdg { height: 84px; font: 800 42px/76px Inter, sans-serif; }
    .bdg b { color: #39e27a; }'''

CHIP = '''    .chip { position: absolute; padding: 12px 26px; border-radius: 22px; background: rgba(255,255,255,.96); color: #22283f; font: 900 52px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); white-space: nowrap; }
    .chip b { color: #e0484f; } .chip i { font-style: normal; color: #1fa65a; }'''
NIGHT = 'sky(sv, "@@ID@@g", "#241c48", "#0e0b22");'

LAB = '''    .shv { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
    .sh { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; opacity: 0; }
    .lab { position: absolute; padding: 10px 26px; border-radius: 18px; background: rgba(20,10,50,.85); border: 3px solid #8ff4ff; color: #fff; font: 900 56px Inter, sans-serif; opacity: 0; box-shadow: 0 0 30px rgba(143,244,255,.4); white-space: nowrap; }
    .lab.r { border-color: #ff6b8a; box-shadow: 0 0 30px rgba(255,107,138,.5); } .lab.g { border-color: #7dffb0; box-shadow: 0 0 30px rgba(125,255,176,.5); } .lab.y { border-color: #ffd84a; }'''
def popin(sel, t, d=0.25): return f'\n      tl.fromTo("{sel}", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.5)" }}, {t});'

MEDIA = {}
SHOTJ = json.loads((Path(__file__).parent.parent / "shots.json").read_text())


def scene(sid, shots, extra_css="", extra_html="", extra_js="", outro=True):
    """Animierte Einstellungen (Gemini-Omni-Clips) als Video-Clips mit harten Schnitten wie in der Referenz."""
    MEDIA[sid] = "\n".join(f'    <video id="{sid}-v{k}" class="clip shv" data-start="{v["start"]:.3f}" data-duration="{v["dur"]:.3f}" data-track-index="{1 + k % 2}" src="{v["src"]}" muted playsinline></video>'
                     for k, v in enumerate(SHOTJ[sid]))
    return (LAB + extra_css, extra_html, extra_js + (OUT if outro else ""))

S['s01'] = scene("s01", [])
S['s02'] = scene("s02", [], extra_html='\n      <div id="s02-a" class="lab y" style="left:90px;top:330px">← LINKS</div><div id="s02-b" class="lab y" style="left:560px;top:330px">RECHTS →</div>',
  extra_js=popin("#s02-a", 'at("L3", "links") - 0.1') + popin("#s02-b", 'at("L3", "rechts") - 0.1') + '\n      tl.set(["#s02-a", "#s02-b"], { opacity: 0 }, line("L4")[0] - 0.05);')
S['s03'] = scene("s03", [], extra_html='\n      <div id="s03-a" class="lab" style="left:150px;top:330px">„SIDEWALK SHUFFLE“</div>', extra_js=popin("#s03-a", 'at("L5", "Sidewalk") - 0.1') + '\n      tl.set("#s03-a", { opacity: 0 }, line("L6")[0] - 0.05);')
S['s04'] = scene("s04", [], extra_html='\n      <div id="s04-a" class="lab r" style="left:260px;top:1330px;font-size:80px">&lt; 1 METER</div>', extra_js=popin("#s04-a", 'at("L7", "Meter") - 0.1') + '\n      tl.set("#s04-a", { opacity: 0 }, line("L8")[0] - 0.05);')
S['s05'] = scene("s05", [], extra_html='\n      <div id="s05-a" class="lab g" style="left:90px;top:330px">BLICK = RICHTUNG</div><div id="s05-b" class="lab r" style="left:180px;top:1330px">KEIN SIGNAL</div>',
  extra_js=popin("#s05-a", 'at("L9", "wohin") - 0.1') + '\n      tl.set("#s05-a", { opacity: 0 }, line("L10")[0] - 0.05);' + popin("#s05-b", 'at("L10", "kein") - 0.1'))
S['s06'] = scene("s06", [], extra_css='\n    #s06-c { left: 0; width: 1080px; top: 380px; text-align: center; font: 900 190px/1 Inter, sans-serif; color: #ff5a6e; opacity: 0; transform: rotate(-8deg); text-shadow: 6px 6px 0 #1a0d33, -6px -6px 0 #1a0d33, 0 0 50px rgba(255,90,110,.9); }',
  extra_html='\n      <div id="s06-c" class="abs">CRASH!</div>',
  extra_js='\n      tl.fromTo("#s06-c", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, at("L11", "Crash") - 0.1);\n      tl.to("#s06-c", { opacity: 0, duration: 0.2 }, line("L12")[0] - 0.2);')
S['s07'] = scene("s07", [], extra_html='\n      <div id="s07-a" class="lab g" style="left:120px;top:330px">BLICK AUF DEN WEG</div>', extra_js=popin("#s07-a", 'at("L13", "genau") - 0.1') + '\n      tl.set("#s07-a", { opacity: 0 }, line("L14")[0] - 0.05);')
S['s08'] = scene("s08", [], outro=False,
  extra_css='''
    #s08-f { left: 290px; top: 1320px; width: 500px; height: 124px; border-radius: 62px; background: #ff3b5c; color: #fff; text-align: center; font: 900 60px/124px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 50px rgba(255,59,92,.7); }''',
  extra_html='\n      <div id="s08-f" class="abs">+ Folgen</div>',
  extra_js='''
      const fo = at("L16", "folg");
      tl.fromTo("#s08-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s08-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 11, ease: "sine.inOut" }, fo + 0.4);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@MEDIA@@", MEDIA.get(sid, "")).replace("@@ID@@", sid))
print(sorted(S))
