#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Pokémon real“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
from pathlib import Path

HEAD = '''<template>
  <style>
    /*__COMMON_CSS__*/
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .panel { position: absolute; border-radius: 24px; background: rgba(13,16,38,.94); text-align: center; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; }
@@CSS@@
  </style>
  <div id="root" data-composition-id="@@ID@@" data-start="0" data-duration="__DUR__" data-width="1080" data-height="1920">
    <div id="@@ID@@-stage" class="clip stage" data-start="0" data-duration="__DUR__" data-track-index="0">
@@HTML@@
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

S['s01'] = ('''    #s01-news { left: 70px; top: 800px; width: 940px; height: 360px; border: 5px solid #ffd43b; box-shadow: 0 0 60px rgba(255,212,59,.45); overflow: hidden; text-align: left; }
    #s01-news .bar { height: 84px; background: #ffd43b; color: #161a36; display: flex; align-items: center; padding-left: 34px; font-size: 44px; letter-spacing: .06em; }
    #s01-news .hl { padding: 22px 40px 0; font-size: 96px; line-height: 1.02; letter-spacing: -.015em; }
    #s01-news .hl em { font-style: normal; color: #ff3b55; text-shadow: 0 0 26px rgba(255,59,85,.6); }
    #s01-q { left: 240px; top: 520px; width: 600px; height: 380px; border: 5px solid #2e3670; color: #ff3b55; font-size: 220px; line-height: 370px; opacity: 0; }''',
'''      <div id="s01-count" class="cbox y"><div class="lab">BEKANNTE ARTEN</div><div class="num">1.025</div></div>
''' + SVG + '''
      <div id="s01-news" class="panel"><div class="bar">WAS WÄRE, WENN …</div><div class="hl">POKÉMON <em>REAL</em> WÄREN?</div></div>
      <div id="s01-q" class="panel">?</div>''',
'''      const sv = document.querySelector("#s01-svg");
      const glow = el("circle", { cx: 540, cy: 720, r: 280, fill: "#ffd43b", opacity: 0.18 }, sv);
      const bolts = [zigzag(sv, 230, 500, 300, 820), zigzag(sv, 850, 500, 780, 820), zigzag(sv, 160, 740, 260, 980, "#4da3ff"), zigzag(sv, 920, 740, 820, 980, "#4da3ff")];
      const B = ball(sv, 540, 720, 210);
      const M = mouse(sv, 540, 700, 0.8); gsap.set(M, { opacity: 0, scale: 0.2 });
      const echt = at("L1", "echt"), l2 = line("L2")[0], nie = at("L2", "niemand");
      tl.fromTo(B.g, { scale: 1.08 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);
      bolts.forEach((b, i) => tl.fromTo(b, { opacity: 1 }, { opacity: 0.15, duration: 0.07, repeat: 7, yoyo: true, ease: "none" }, 0.02 + i * 0.05));
      tl.fromTo(glow, { attr: { opacity: 0.18 } }, { attr: { opacity: 0.4 }, duration: 0.3, repeat: 3, yoyo: true }, 0);
      tl.to("#s01-news", { opacity: 0, y: 140, duration: 0.3, ease: "power3.in" }, at("L1", "wirklich") - 0.2);
      tl.to(B.g, { rotation: 12, duration: 0.07, repeat: 7, yoyo: true, svgOrigin: "540 930" }, echt - 0.7);
      tl.to(B.top, { rotation: -35, svgOrigin: "-210 0", duration: 0.3, ease: "back.out(2)" }, echt);
      tl.to(glow, { attr: { r: 700, opacity: 0.9 }, duration: 0.18 }, echt);
      tl.to(glow, { attr: { r: 280, opacity: 0.2 }, duration: 0.4 }, echt + 0.18);
      tl.to(M, { opacity: 1, scale: 0.8, y: 610, duration: 0.45, ease: "back.out(1.8)" }, echt + 0.05);
      tl.to([B.g, M, ...bolts, glow], { opacity: 0, filter: "blur(8px)", duration: 0.2 }, nie - 0.25);
      tl.fromTo("#s01-count", { scale: 1 }, { scale: 1.12, duration: 0.15, yoyo: true, repeat: 1 }, l2);
      tl.fromTo("#s01-q", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, nie - 0.1);
      tl.to("#s01-q", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, nie + 0.3);''' + OUT)

S['s02'] = ('', '''      <div id="s02-box" class="cbox r" style="opacity:0"><div class="lab">ESSEN PRO TAG</div><div id="s02-n" class="num">0 KG</div></div>
''' + SVG, '''      const sv = document.querySelector("#s02-svg");
      const R = blob(sv, 540, 760, 1.2);
      const Z = el("text", { x: 760, y: 520, fill: "#a9d2ff", "font-family": "Inter", "font-weight": 900, "font-size": 90 }, sv); Z.textContent = "Z z";
      const tiny = []; for (let i = 0; i < 48; i++) tiny.push(blob(sv, 150 + (i % 8) * 112, 520 + Math.floor(i / 8) * 105, 0.22));
      gsap.set(tiny, { opacity: 0 });
      const vier = at("L3", "400"), l4 = line("L4")[0], hn = at("L4", "Hungersnot");
      tl.fromTo(R, { opacity: 0, y: 820 }, { opacity: 1, y: 760, duration: 0.5, ease: "expo.out" }, 0.05);
      tl.fromTo(Z, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, repeat: 2, yoyo: true }, 0.4);
      tl.to("#s02-box", { opacity: 1, duration: 0.25 }, vier - 0.4);
      count(tl, "#s02-n", 0, 400, vier - 0.2, 0.7, "", " KG", "power3.out");
      tl.to([R, Z], { opacity: 0, scale: 0.4, duration: 0.3, ease: "power3.in" }, l4 - 0.1);
      tl.to(tiny, { opacity: 1, duration: 0.1, stagger: 0.02 }, l4);
      tl.to("#s02-box .lab", { textContent: "× 1 MILLION", duration: 0.01 }, l4);
      count(tl, "#s02-n", 400, 400000, l4 + 0.1, 0.9, "", " T", "power2.in");
      tl.to(tiny, { attr: { opacity: 1 }, x: "+=0", duration: 0.01 }, hn);
      tl.to("#s02-box", { scale: 1.12, duration: 0.15, yoyo: true, repeat: 1 }, hn);''' + OUT)

S['s03'] = ('''    #s03-farm { left: 140px; top: 470px; width: 800px; height: 120px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 70px; line-height: 108px; opacity: 0; }''',
'''      <div id="s03-box" class="cbox y" style="opacity:0"><div class="lab">LEISTUNG</div><div id="s03-n" class="num">0 %</div></div>
''' + SVG + '''
      <div id="s03-farm" class="panel">PIKACHU-FARM</div>''',
'''      const sv = document.querySelector("#s03-svg");
      const M = mouse(sv, 360, 820, 1.0);
      const bulb = el("g", {}, sv); el("circle", { cx: 820, cy: 640, r: 90, fill: "#3a3f6e" }, bulb); el("rect", { x: 780, y: 720, width: 80, height: 60, rx: 8, fill: "#8fa2ff" }, bulb);
      const lit = el("circle", { cx: 820, cy: 640, r: 90, fill: "#ffd43b", opacity: 0 }, sv);
      const bolt = zigzag(sv, 470, 740, 760, 660); gsap.set(bolt, { opacity: 0 });
      const minis = []; for (let i = 0; i < 18; i++) minis.push(mouse(sv, 190 + (i % 6) * 140, 700 + Math.floor(i / 6) * 150, 0.28));
      gsap.set(minis, { opacity: 0 });
      const prot = el("g", {}, sv), people = [];
      for (let i = 0; i < 3; i++) {
        const P = person(prot, "s03-p" + i, 250 + i * 290, 820, 0.85, { three: false, arms: [10, -160], shirt: ["#39e27a", "#4da3ff", "#ff4fb0"][i] });
        const sign = el("g", {}, P.a2); el("rect", { x: 10, y: 130, width: 150, height: 90, rx: 8, fill: "#f3f1ea" }, sign);
        const tx = el("text", { x: 85, y: 186, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 36, fill: "#ff3b55", transform: "rotate(180 85 175)" }, sign); tx.textContent = "FREI!";
        people.push(P.g);
      }
      gsap.set(people, { opacity: 0 });
      const kw = at("L5", "Kraftwerk"), farm = at("L6", "Pikachu-Farmen"), ts = at("L6", "Tierschützer"), st = at("L6", "Straße");
      tl.fromTo([M, bulb], { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.05);
      tl.to(bolt, { opacity: 1, duration: 0.05, repeat: 5, yoyo: true }, kw - 0.2);
      tl.to(lit, { opacity: 1, duration: 0.15 }, kw);
      tl.to("#s03-box", { opacity: 1, duration: 0.25 }, kw - 0.3);
      count(tl, "#s03-n", 0, 100, kw - 0.2, 0.5, "", " %");
      tl.to([M, bulb, lit, bolt], { opacity: 0, duration: 0.25 }, farm - 0.6);
      tl.to("#s03-farm", { opacity: 1, duration: 0.25 }, farm - 0.4);
      tl.to(minis, { opacity: 1, duration: 0.1, stagger: 0.03 }, farm - 0.3);
      tl.to([minis, "#s03-farm"], { opacity: 0.2, duration: 0.25 }, ts - 0.1);
      tl.to(people, { opacity: 1, duration: 0.25, stagger: 0.12 }, ts);
      people.forEach((p, i) => tl.to(p, { y: "-=24", duration: 0.15, yoyo: true, repeat: 3 }, st - 0.1 + i * 0.08));''' + OUT)

S['s04'] = ('''    #s04-card { left: 160px; top: 520px; width: 760px; height: 420px; border: 6px solid #4da3ff; box-shadow: 0 0 50px rgba(77,163,255,.4); opacity: 0; }
    #s04-card .t1 { margin-top: 140px; font-size: 72px; color: #4da3ff; }
    #s04-card .t2 { margin-top: 18px; font-family: "Space Mono", monospace; font-weight: 700; font-size: 34px; color: #dfe2f5; letter-spacing: .08em; }''',
SVG + '''
      <div id="s04-card" class="panel"><div class="t1">GLURAK-HAFTPFLICHT</div><div class="t2">AB 49 € IM MONAT</div></div>''',
'''      const sv = document.querySelector("#s04-svg");
      const H = el("g", {}, sv); el("rect", { x: 620, y: 700, width: 300, height: 260, fill: "#c9cde6" }, H); el("path", { d: "M600 710 L770 560 L940 710Z", fill: "#ff3b55" }, H);
      el("rect", { x: 740, y: 840, width: 60, height: 120, fill: "#6b4f2a" }, H); el("rect", { x: 650, y: 750, width: 60, height: 60, fill: "#4da3ff" }, H);
      const flames = []; for (let i = 0; i < 5; i++) flames.push(el("path", { d: `M${650 + i * 60} 720 q20 -80 30 -150 q20 70 30 150Z`, fill: i % 2 ? "#ffd43b" : "#ff8a3d", opacity: 0 }, sv));
      const D = dragon(sv, 300, 820, 1.0);
      const fire = el("path", { d: "M350 720 Q480 660 640 720 Q480 700 350 740Z", fill: "#ff8a3d", opacity: 0 }, sv);
      const sh = el("g", { opacity: 0 }, sv); el("path", { d: "M540 420 l120 40 v90 q0 90 -120 140 q-120 -50 -120 -140 v-90Z", fill: "#4da3ff" }, sh);
      el("path", { d: "M490 540 l40 40 l70 -80", stroke: "#fff", "stroke-width": 18, fill: "none", "stroke-linecap": "round" }, sh);
      const fk = at("L7", "fackelt"), hp = at("L7", "Glurak-Haftpflicht");
      tl.fromTo([H, D], { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.05);
      tl.to(fire, { opacity: 1, duration: 0.1 }, fk - 0.1);
      tl.to(flames, { opacity: 1, duration: 0.15, stagger: 0.06 }, fk);
      flames.forEach((f, i) => tl.to(f, { scaleY: 1.25, transformOrigin: "50% 100%", duration: 0.12, repeat: 5, yoyo: true }, fk + 0.2 + i * 0.03));
      tl.to([H, D, fire, ...flames], { opacity: 0.15, duration: 0.25 }, hp - 0.35);
      tl.to("#s04-card", { opacity: 1, duration: 0.3, ease: "back.out(1.6)" }, hp - 0.2);
      tl.fromTo(sh, { opacity: 0, scale: 0.5, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, hp - 0.1);''' + OUT)

S['s05'] = ('', '''      <div id="s05-box" class="cbox g" style="opacity:0"><div class="lab">LASTWAGEN NÖTIG</div><div id="s05-n" class="num">100 %</div></div>
''' + SVG, '''      const sv = document.querySelector("#s05-svg");
      const O = el("g", {}, sv);
      [[260, 1000, 90], [380, 900, 100], [520, 840, 110], [660, 760, 105], [760, 640, 95], [800, 520, 120]].forEach(([x, y, r]) => el("ellipse", { cx: x, cy: y, rx: r, ry: r * 0.8, fill: "#8a8fa8", stroke: "#5b607a", "stroke-width": 8 }, O));
      el("circle", { cx: 770, cy: 500, r: 12, fill: "#161a36" }, O);
      const B = ball(sv, 300, 640, 70); gsap.set(B.g, { opacity: 0 });
      const T = el("g", { opacity: 0 }, sv); el("rect", { x: 300, y: 700, width: 360, height: 200, rx: 12, fill: "#c9cde6" }, T); el("rect", { x: 660, y: 760, width: 140, height: 140, rx: 12, fill: "#4da3ff" }, T);
      el("circle", { cx: 380, cy: 910, r: 40, fill: "#161a36" }, T); el("circle", { cx: 720, cy: 910, r: 40, fill: "#161a36" }, T);
      const X = el("g", { opacity: 0, stroke: "#ff3b55", "stroke-width": 30, "stroke-linecap": "round" }, sv); el("line", { x1: 280, y1: 640, x2: 820, y2: 980 }, X); el("line", { x1: 820, y1: 640, x2: 280, y2: 980 }, X);
      const pb = at("L8", "Pokéball"), tg = at("L8", "Taschengröße"), l9 = line("L9")[0], ke = at("L9", "keine");
      tl.fromTo(O, { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.05);
      tl.to(B.g, { opacity: 1, duration: 0.25 }, pb);
      tl.to(B.top, { rotation: -50, svgOrigin: "-70 0", duration: 0.2 }, tg - 0.5);
      tl.to(O, { scale: 0.02, svgOrigin: "300 640", opacity: 0, duration: 0.5, ease: "power3.in" }, tg - 0.4);
      tl.to(B.top, { rotation: 0, svgOrigin: "-70 0", duration: 0.15 }, tg + 0.1);
      tl.to(B.g, { scale: 0.5, x: 540, y: 1060, duration: 0.4, ease: "power2.inOut" }, l9 - 0.2);
      tl.to(T, { opacity: 1, duration: 0.3 }, l9);
      tl.to("#s05-box", { opacity: 1, duration: 0.25 }, l9 + 0.2);
      tl.to(X, { opacity: 1, duration: 0.15 }, ke);
      count(tl, "#s05-n", 100, 0, ke, 0.6, "", " %", "power3.out");''' + OUT)

S['s06'] = ('''    #s06-sec { left: 250px; top: 460px; width: 580px; height: 90px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 52px; line-height: 80px; letter-spacing: .1em; opacity: 0; }''',
SVG + '''
      <div id="s06-sec" class="panel">STRENG GEHEIM</div>''',
'''      const sv = document.querySelector("#s06-svg");
      const aura = el("circle", { cx: 540, cy: 800, r: 220, fill: "#b06bff", opacity: 0 }, sv);
      const leg = el("g", { opacity: 0 }, sv); el("path", { d: "M540 600 q-120 60 -110 200 q10 120 110 140 q100 -20 110 -140 q10 -140 -110 -200Z", fill: "#e9d6ff" }, leg);
      el("path", { d: "M560 940 q160 40 180 -120", stroke: "#e9d6ff", "stroke-width": 30, fill: "none", "stroke-linecap": "round" }, leg);
      el("circle", { cx: 510, cy: 700, r: 10, fill: "#7a2fd0" }, leg); el("circle", { cx: 570, cy: 700, r: 10, fill: "#7a2fd0" }, leg);
      const warn = el("g", { opacity: 0 }, sv); el("path", { d: "M540 1000 l60 100 h-120Z", fill: "#ffd43b" }, warn); el("text", { x: 540, y: 1090, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 60, fill: "#161a36" }, warn).textContent = "!";
      const door = el("g", {}, sv); el("circle", { cx: 0, cy: 0, r: 330, fill: "#3a3f6e", stroke: "#8a8fa8", "stroke-width": 24 }, door);
      for (let i = 0; i < 6; i++) el("rect", { x: -12, y: -300, width: 24, height: 120, fill: "#8a8fa8", transform: `rotate(${i * 60})` }, door);
      el("circle", { cx: 0, cy: 0, r: 90, fill: "#5b607a" }, door);
      gsap.set(door, { x: 1500, y: 800 });
      const lg = at("L10", "Legendäre"), aw = at("L10", "Atomwaffen"), vs = at("L10", "verstecken");
      tl.to([aura, leg], { opacity: 1, duration: 0.4 }, lg - 0.1);
      tl.to(aura, { attr: { r: 300, opacity: 0.35 }, duration: 0.5, repeat: 3, yoyo: true }, lg + 0.2);
      tl.to(warn, { opacity: 1, duration: 0.2 }, aw - 0.1);
      tl.to("#s06-sec", { opacity: 1, duration: 0.25 }, aw + 0.3);
      tl.to(door, { x: 540, rotation: -180, duration: 0.6, ease: "power3.inOut" }, vs - 0.3);''' + OUT)

S['s07'] = ('', SVG, '''      const sv = document.querySelector("#s07-svg");
      const M = mouse(sv, 540, 780, 0.95);
      const bars = el("g", { opacity: 0 }, sv); for (let i = 0; i < 7; i++) el("rect", { x: 300 + i * 80, y: 470, width: 20, height: 640, rx: 8, fill: "#8a8fa8" }, bars);
      el("rect", { x: 280, y: 450, width: 520, height: 30, rx: 10, fill: "#8a8fa8" }, bars); el("rect", { x: 280, y: 1100, width: 520, height: 30, rx: 10, fill: "#8a8fa8" }, bars);
      const D = dragon(sv, 820, 820, 0.8); gsap.set(D, { opacity: 0 });
      const H = person(sv, "s07-h", 540, 640, 1.4, { three: false, arms: [8, -8], shirt: "#161a36", sad: false }); gsap.set(H.g, { opacity: 0 });
      const red = el("circle", { cx: 540, cy: 700, r: 360, fill: "#ff3b55", opacity: 0 }, sv); sv.insertBefore(red, sv.firstChild);
      const se = at("L12", "sperren"), ka = at("L12", "kämpfen"), wir = at("L12", "wir"), bo = at("L12", "Bösen");
      tl.fromTo(M, { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.05);
      tl.fromTo(bars, { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: 0.3, ease: "bounce.out" }, se);
      tl.to(bars, { opacity: 0, duration: 0.2 }, ka - 0.3);
      tl.to(M, { x: 260, duration: 0.3 }, ka - 0.3);
      tl.to(D, { opacity: 1, duration: 0.25 }, ka - 0.3);
      tl.to(M, { x: 420, duration: 0.12, yoyo: true, repeat: 3 }, ka);
      tl.to(D, { x: 680, duration: 0.12, yoyo: true, repeat: 3 }, ka);
      tl.to([M, D], { opacity: 0, duration: 0.2 }, wir - 0.25);
      tl.to(H.g, { opacity: 1, duration: 0.25 }, wir - 0.1);
      tl.to(red, { opacity: 0.35, duration: 0.3 }, bo - 0.1);''' + OUT)

S['s08'] = ('''    .s08-c { position: absolute; top: 960px; width: 300px; height: 120px; border-radius: 24px; text-align: center; line-height: 120px;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 50px; color: #0b0e22; }
    #s08-c1 { left: 60px; background: #ffd43b; } #s08-c2 { left: 390px; background: #ff8a3d; } #s08-c3 { left: 720px; background: #39e27a; }''',
SVG + '''
      <div id="s08-c1" class="s08-c">PIKACHU?</div><div id="s08-c2" class="s08-c">GLURAK?</div><div id="s08-c3" class="s08-c">RELAXO?</div>''',
'''      const sv = document.querySelector("#s08-svg");
      const B = ball(sv, 540, 680, 200);
      const du = at("L13", "du?");
      tl.fromTo(B.g, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.to(B.g, { rotation: 10, svgOrigin: "540 880", duration: 0.08, repeat: 5, yoyo: true }, du - 0.2);
      tl.fromTo(".s08-c", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, stagger: 0.12, ease: "back.out(1.8)" }, du);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
