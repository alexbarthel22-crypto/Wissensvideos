#!/usr/bin/env python3
"""TikTok-Profilbild: Prophet Peter als Heiliger (1080×1080, wichtig = Kreismitte). Rendern: python3 gen_profilbild.py && node shot.cjs"""
from pathlib import Path
here = Path(__file__).parent; CH = here.parents[1] / "tools" / "characters"
js = (CH / "prophet-peter.js").read_text()
doc = '''<!doctype html><html lang="de"><head><meta charset="UTF-8"><script src="gsap.min.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1080px; height: 1080px; overflow: hidden; background: #1a0f2e; }
  .abs { position: absolute; }
  #bg { left: 0; top: 0; width: 1080px; height: 1080px;
    background: radial-gradient(circle at 50% 42%, #ffe9b0 0%, #f2b54a 14%, #c8662e 30%, #6a2a86 58%, #2a1046 85%, #12061f 100%); }
  #rays { left: -540px; top: -540px; width: 2160px; height: 2160px;
    background: repeating-conic-gradient(from 0deg at 50% 45.5%, rgba(255,250,220,.34) 0deg 4deg, rgba(255,250,220,0) 4deg 12deg);
    -webkit-mask-image: radial-gradient(circle at 50% 45.5%, #000 8%, transparent 42%); }
  #ring { left: 290px; top: 135px; width: 500px; height: 500px; border-radius: 50%;
    border: 22px solid #fff1a8; box-shadow: 0 0 40px 8px rgba(255,200,60,1), 0 0 90px 20px rgba(255,170,40,.7), inset 0 0 40px rgba(255,200,80,.9); }
  #ring2 { left: 260px; top: 105px; width: 560px; height: 560px; border-radius: 50%; border: 3px solid rgba(255,240,190,.7); }
  .sp { position: absolute; width: 12px; height: 12px; border-radius: 50%; background: #fffbe6; box-shadow: 0 0 16px 6px rgba(255,225,140,.9); }
  #vig { left: 0; top: 0; width: 1080px; height: 1080px; background: radial-gradient(circle at 50% 48%, rgba(0,0,0,0) 52%, rgba(10,4,20,.55) 72%); }
</style></head><body>
<div id="bg" class="abs"></div><div id="rays" class="abs"></div><div id="ring2" class="abs"></div>
<svg id="sv" class="abs" style="left:0;top:0" width="1080" height="1080" viewBox="0 0 1080 1080"></svg>
<div id="ring" class="abs"></div>
<div id="sps"></div><div id="vig" class="abs"></div>
<script>
const NS = "http://www.w3.org/2000/svg";
const el = (n, a, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
@@JS@@
const sv = document.getElementById("sv");
// Brustbild: Kopf in der Kreismitte, segnende Hand, Discokugel funkelt
const P = peter(sv, "pp", 540, 1600, 1.55, { arms: [14, -150] });
P.g.style.filter = "drop-shadow(0 0 40px rgba(255,230,150,.7))";
gsap.set(P.halo, { opacity: 0 });              // statt Neonring: goldener Heiligenschein (HTML hinter dem Kopf)
gsap.set(P.mouth, { attr: { d: "M-24 -588 Q0 -566 24 -588 Q0 -580 -24 -588Z" } }); // leichtes Lächeln/offen
// goldener Heiligenschein hinter den Kopf: Kopfmitte liegt bei (540, 1600 - 700*1.55)
const hy = 1600 - 760 * 1.55;
const ring = document.getElementById("ring"), ring2 = document.getElementById("ring2");
ring.style.top = (hy - 250) + "px"; ring2.style.top = (hy - 280) + "px"; document.getElementById("rays").style.top = (hy - 1080) + "px";
document.body.insertBefore(ring, sv);
const sps = document.getElementById("sps"); let seed = 5; const R = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
for (let i = 0; i < 40; i++) { const d = document.createElement("div"); d.className = "sp"; const a = R() * 6.283, r = 300 + R() * 220;
  Object.assign(d.style, { left: 540 + r * Math.cos(a) + "px", top: hy + r * Math.sin(a) * 0.95 + "px", transform: `scale(${0.3 + R() * 0.9})`, opacity: 0.5 + R() * 0.5 }); sps.appendChild(d); }
</script></body></html>'''
(here / "index.html").write_text(doc.replace("@@JS@@", js))
