#!/usr/bin/env python3
"""Cover für Prophet Peter – Tag 1 (Figur/Kulisse aus tools/characters)."""
from pathlib import Path
here = Path(__file__).parent; CH = here.parents[2] / "tools" / "characters"
js = (CH / "prophet-peter.js").read_text() + (CH / "grundstueck.js").read_text()
doc = '''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0a0c1d; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; }
      .abs { position: absolute; }
      .t { left: 0; width: 1080px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; white-space: nowrap; }
      #heaven { left: 0; top: 0; width: 1080px; height: 1920px; opacity: .95;
        background: repeating-conic-gradient(from 180deg at 50% -4%, rgba(255,236,170,.32) 0deg 3deg, rgba(255,236,170,0) 3deg 9deg);
        -webkit-mask-image: radial-gradient(ellipse 85% 60% at 50% 0%, #000 30%, transparent 80%); }
      #glow { left: -100px; top: 120px; width: 1280px; height: 900px; background: radial-gradient(ellipse 50% 45% at 50% 45%, rgba(255,226,140,.55), rgba(255,180,90,.15) 55%, rgba(255,180,90,0) 75%); }
      #warte { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 245px; padding: 4px 40px 12px; border-radius: 26px; background: #c8102e; border: 6px solid #ffb3bf;
        color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 120px; line-height: 1.1; box-shadow: 0 0 60px rgba(255,40,70,.85), 0 12px 0 rgba(0,0,0,.35); transform: rotate(-3deg); }
      #day { top: 420px; font-size: 200px; line-height: 1; color: #ffd43b; letter-spacing: -.03em; text-shadow: 0 0 70px rgba(255,212,59,.75), 0 10px 0 rgba(0,0,0,.55); }
      #h { top: 625px; font-size: 116px; line-height: 1.02; color: #fff; text-shadow: 0 8px 0 rgba(0,0,0,.6), 0 0 34px rgba(255,236,170,.6); }
      #h em { font-style: normal; color: #ff4fb0; text-shadow: 0 0 44px rgba(255,79,176,.9), 0 8px 0 rgba(0,0,0,.6); }
      #zero { left: 560px; top: 930px; padding: 12px 26px; border: 9px solid #ff3b55; border-radius: 22px; background: rgba(40,4,14,.92); transform: rotate(-7deg);
        font-family: "Inter", sans-serif; font-weight: 900; color: #ff3b55; text-align: center; box-shadow: 0 0 60px rgba(255,59,85,.65); text-shadow: 0 0 26px rgba(255,59,85,.7); }
      #zero b { display: block; font-size: 150px; line-height: .95; }
      #zero small { display: block; font-family: "Space Mono", monospace; font-weight: 700; font-size: 36px; letter-spacing: .14em; color: #ffb3bf; }
      #q { left: 70px; width: 940px; top: 1480px; height: 150px; border-radius: 24px; background: #0b0e22; border: 6px solid #ffd43b;
        box-shadow: 0 0 50px rgba(255,212,59,.5); text-align: center; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 64px; line-height: 138px; }
      #q span { color: #ffd43b; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-width="1080" data-height="1920" data-no-timeline>
      <svg id="bg" class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
      <div id="heaven" class="abs"></div><div id="glow" class="abs"></div>
      <svg id="sv" class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
      <div id="warte" class="abs">WARTE!</div>
      <div id="day" class="abs t">TAG 1</div>
      <div id="h" class="abs t">ICH GRÜNDE<br>EINE <em>SEKTE</em></div>
      <div id="zero" class="abs"><small>ANHÄNGER</small><b>0</b></div>
      <div id="q" class="abs">WERDE MEIN <span>1. ANHÄNGER</span>!</div>
      <svg id="fx" class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
    </div>
    <script>
      const NS = "http://www.w3.org/2000/svg";
      const el = (n, a, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
      const rng = (seed) => () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let x = Math.imul(seed ^ (seed >>> 15), 1 | seed);
        x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x; return ((x ^ (x >>> 14)) >>> 0) / 4294967296; };
@@JS@@
      const G = grundstueck(document.getElementById("bg"), "cg", { mood: "dusk", dy: 200, chairX: 790, treeX: 900, goatX: 640, goatS: 0.8, goatFlip: true }); gsap.set(G.rays, { opacity: 0.7 });
      const P = peter(document.getElementById("sv"), "cp", 290, 1460, 0.6, { arms: [14, -135] });
      P.g.style.filter = "drop-shadow(0 0 40px rgba(255,220,130,.55))";
      filmLook(document.getElementById("fx"), "cf", 0.8);
    </script>
  </body>
</html>
'''
(here / "index.html").write_text(doc.replace("@@JS@@", js))
