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
      #day { top: 250px; font-size: 230px; line-height: 1; color: #ffd43b; letter-spacing: -.03em; text-shadow: 0 0 60px rgba(255,212,59,.6), 0 10px 0 rgba(0,0,0,.55); }
      #h { top: 480px; font-size: 104px; line-height: 1; color: #fff; text-shadow: 0 8px 0 rgba(0,0,0,.6), 0 0 30px rgba(0,0,0,.5); }
      #h em { font-style: normal; color: #ff4fb0; text-shadow: 0 0 40px rgba(255,79,176,.85), 0 8px 0 rgba(0,0,0,.6); }
      .chip { padding: 12px 24px; border-radius: 16px; background: rgba(13,10,30,.92); border: 4px solid #ffd43b; color: #fff;
        font-family: "Inter", sans-serif; font-weight: 900; font-size: 44px; white-space: nowrap; box-shadow: 0 0 30px rgba(255,212,59,.4); }
      #q { left: 70px; width: 940px; top: 1470px; height: 150px; border-radius: 24px; background: #0b0e22; border: 5px solid #ff4fb0;
        box-shadow: 0 0 50px rgba(255,79,176,.5); text-align: center; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 62px; line-height: 140px; }
      #q span { color: #ff4fb0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="cover" data-start="0" data-duration="1" data-width="1080" data-height="1920" data-no-timeline>
      <svg id="bg" class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
      <svg id="sv" class="abs" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
      <div id="day" class="abs t">TAG 1</div>
      <div id="h" class="abs t">ICH GRÜNDE<br>EINE <em>SEKTE</em></div>
      <div class="abs chip" style="left:640px;top:820px;transform:rotate(4deg)">1 STUHL</div>
      <div class="abs chip" style="left:640px;top:930px;transform:rotate(-3deg);border-color:#ff4fb0">1 BAUM</div>
      <div class="abs chip" style="left:640px;top:1040px;transform:rotate(2deg);border-color:#39e27a">0 ANHÄNGER</div>
      <div id="q" class="abs">WIE SOLL SIE <span>HEISSEN</span>?</div>
    </div>
    <script>
      const NS = "http://www.w3.org/2000/svg";
      const el = (n, a, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
      const rng = (seed) => () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let x = Math.imul(seed ^ (seed >>> 15), 1 | seed);
        x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x; return ((x ^ (x >>> 14)) >>> 0) / 4294967296; };
@@JS@@
      const G = grundstueck(document.getElementById("bg"), "cg", { mood: "dusk", dy: 150, chairX: 760, treeX: 860 }); gsap.set(G.rays, { opacity: 0.7 });
      peter(document.getElementById("sv"), "cp", 320, 1450, 0.8);
      filmLook(document.getElementById("sv"), "cf");
    </script>
  </body>
</html>
'''
(here / "index.html").write_text(doc.replace("@@JS@@", js))
