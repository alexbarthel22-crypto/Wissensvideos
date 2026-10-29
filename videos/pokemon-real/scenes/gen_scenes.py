#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Pokémon real“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
from pathlib import Path

HEAD = '''<template>
  <style>
    /*__COMMON_CSS__*/
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .panel { position: absolute; border-radius: 24px; background: rgba(13,16,38,.94); text-align: center; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; }
    .cbox { top: 398px; } /* unter der großen Kapitel-Überschrift */
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

S['s01'] = ('''    #s01-news { left: 70px; top: 700px; width: 940px; height: 360px; border: 5px solid #ffd43b; box-shadow: 0 0 60px rgba(255,212,59,.45); overflow: hidden; text-align: left; }
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
      const echt = at("L1", "Alltag"), l2 = line("L2")[0], nie = at("L2", "komplett");
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
      const R = blob(sv, 540, 820, 1.2);
      const Z = el("text", { x: 770, y: 640, fill: "#a9d2ff", "font-family": "Inter", "font-weight": 900, "font-size": 90 }, sv); Z.textContent = "Z z";
      const fr = el("g", { opacity: 0 }, sv);
      el("rect", { x: 600, y: 560, width: 320, height: 520, rx: 26, fill: "#dfe6f5" }, fr);
      el("rect", { x: 622, y: 582, width: 276, height: 476, rx: 14, fill: "#9fb3d9" }, fr);
      [740, 900].forEach((y) => el("rect", { x: 622, y, width: 276, height: 10, fill: "#dfe6f5" }, fr));
      el("rect", { x: 920, y: 580, width: 34, height: 480, rx: 10, fill: "#c9cde6" }, fr);
      const FOOD = ["#ff3b55", "#ffd43b", "#39e27a", "#ff8a3d", "#ff4fb0", "#4da3ff", "#ffd43b", "#ff3b55", "#39e27a"];
      const foods = FOOD.map((c, i) => { const x = 670 + (i % 3) * 90, y = 700 + Math.floor(i / 3) * 160;
        return i % 2 ? el("rect", { x: x - 30, y: y - 50, width: 60, height: 50, rx: 10, fill: c }, fr) : el("circle", { cx: x, cy: y - 28, r: 30, fill: c }, fr); });
      const pz = el("g", {}, sv), boxes = [];
      for (let i = 0; i < 8; i++) { const b = el("g", { opacity: 0 }, pz); const y = 1050 - i * 54;
        el("rect", { x: 340, y, width: 400, height: 46, rx: 6, fill: "#e0a458", stroke: "#8a5a2b", "stroke-width": 5 }, b);
        el("text", { x: 540, y: y + 34, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 30, fill: "#8a3b2a" }, b).textContent = "PIZZA";
        boxes.push(b); }
      const r = rng(7), coins = [], cg = el("g", { "data-layout-allow-overlap": "" }, sv);
      for (let i = 0; i < 16; i++) { const c = el("text", { x: 120 + r() * 840, y: 620, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 70 + r() * 40, fill: "#ffd43b", opacity: 0 }, cg); c.textContent = "€"; coins.push(c); }
      const vier = at("L3", "400"), l4 = line("L4")[0], sek = at("L4", "Sekunden"), bote = at("L4", "Pizzabote"), mil = at("L4", "Millionär");
      tl.fromTo(R, { opacity: 0, y: 880 }, { opacity: 1, y: 820, duration: 0.5, ease: "expo.out" }, 0.05);
      tl.fromTo(Z, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, repeat: 2, yoyo: true }, 0.4);
      tl.to("#s02-box", { opacity: 1, duration: 0.25 }, vier - 0.4);
      count(tl, "#s02-n", 0, 400, vier - 0.2, 0.7, "", " KG", "power3.out");
      tl.to(R, { scale: 1.32, duration: 0.14, yoyo: true, repeat: 3 }, vier + 0.4);
      tl.to(Z, { opacity: 0, duration: 0.2 }, l4 - 0.3);
      tl.to(R, { x: 300, y: 860, scale: 0.85, duration: 0.4, ease: "power3.inOut" }, l4 - 0.2);
      tl.fromTo(fr, { opacity: 0, x: 200 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.6)" }, l4 - 0.1);
      tl.to("#s02-box .lab", { textContent: "KÜHLSCHRANK", duration: 0.01 }, l4);
      tl.set("#s02-n", { textContent: "100 %" }, l4);
      foods.forEach((f, i) => tl.to(f, { x: 300 - (670 + (i % 3) * 90), y: 760 - (700 + Math.floor(i / 3) * 160), scale: 0.2, opacity: 0, duration: 0.22, ease: "power2.in" }, sek - 0.3 + i * 0.07));
      tl.to(R, { scaleY: 0.78, duration: 0.08, yoyo: true, repeat: 9 }, sek - 0.3);
      count(tl, "#s02-n", 100, 0, sek - 0.3, 0.7, "", " %", "none");
      tl.to([R, fr], { opacity: 0, scale: 0.5, duration: 0.25, ease: "power3.in" }, bote - 0.3);
      boxes.forEach((b, i) => tl.fromTo(b, { opacity: 0, y: -700 }, { opacity: 1, y: 0, duration: 0.3, ease: "bounce.out" }, bote - 0.05 + i * 0.07));
      tl.to("#s02-box .lab", { textContent: "TRINKGELD", duration: 0.01 }, mil - 0.3);
      count(tl, "#s02-n", 0, 1000000, mil - 0.3, 0.8, "", " €", "power2.in");
      coins.forEach((c, i) => tl.set(c, { opacity: 1 }, mil - 0.2 + i * 0.05).to(c, { y: 560 + (i % 4) * 30, rotation: (i % 2 ? 1 : -1) * 200, duration: 1.1, ease: "power1.in" }, mil - 0.2 + i * 0.05));
      tl.to(pz, { rotation: 4, svgOrigin: "540 1100", duration: 0.12, yoyo: true, repeat: 5 }, mil);''' + OUT)

S['s03'] = ('', '''      <div id="s03-box" class="cbox g" style="opacity:0"><div class="lab">AKKU</div><div id="s03-n" class="num">1 %</div></div>
''' + SVG, '''      const sv = document.querySelector("#s03-svg");
      const ph = el("g", { opacity: 0 }, sv);
      el("rect", { x: 640, y: 560, width: 270, height: 500, rx: 40, fill: "#161a36", stroke: "#8fa2ff", "stroke-width": 8 }, ph);
      el("rect", { x: 664, y: 600, width: 222, height: 420, rx: 16, fill: "#232a5a" }, ph);
      el("rect", { x: 745, y: 690, width: 60, height: 22, rx: 6, fill: "#fff" }, ph);
      el("rect", { x: 705, y: 710, width: 140, height: 240, rx: 16, fill: "none", stroke: "#fff", "stroke-width": 9 }, ph);
      const bar = el("rect", { x: 718, y: 922, width: 114, height: 16, rx: 8, fill: "#ff3b55" }, ph);
      const M = mouse(sv, 330, 830, 0.95); gsap.set(M, { opacity: 0 });
      const fea = el("path", { d: "M420 640 q60 -40 90 -120 q-10 80 -70 140Z", fill: "#f3f1ea", stroke: "#c9cde6", "stroke-width": 4, opacity: 0 }, sv);
      const bolts = [zigzag(sv, 430, 760, 650, 760), zigzag(sv, 430, 860, 650, 900, "#4da3ff")]; gsap.set(bolts, { opacity: 0 });
      const ha = el("text", { x: 180, y: 620, fill: "#ffd43b", "font-family": "Inter", "font-weight": 900, "font-size": 64, opacity: 0 }, sv); ha.textContent = "HIHI!";
      const P = person(sv, "s03-p", 540, 760, 1.35, { three: false, arms: [24, -24], shirt: "#ff4fb0" }); gsap.set(P.g, { opacity: 0 });
      const spikes = el("g", {}, P.g);
      for (let i = 0; i < 7; i++) { const x = -48 + i * 16; el("polyline", { points: `${x},-96 ${x * 1.5 - 8},-150 ${x * 1.6 + 8},-180 ${x * 2.2},-235`, fill: "none", stroke: "#5b3a26", "stroke-width": 14, "stroke-linecap": "round", "stroke-linejoin": "round" }, spikes); }
      gsap.set(spikes, { scaleY: 0, transformOrigin: "50% 100%" });
      const sparks = [zigzag(sv, 300, 560, 360, 660), zigzag(sv, 780, 560, 720, 660), zigzag(sv, 260, 760, 330, 820, "#4da3ff"), zigzag(sv, 820, 760, 750, 820, "#4da3ff")]; gsap.set(sparks, { opacity: 0 });
      const kz = at("L5", "kitzeln"), hu = at("L5", "hundert"), l6 = line("L6")[0], hr = at("L6", "Haare"), sk = at("L6", "senkrecht");
      tl.fromTo(ph, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, 0.05);
      tl.to(bar, { opacity: 0.2, duration: 0.15, yoyo: true, repeat: 5 }, 0.3);
      tl.to("#s03-box", { opacity: 1, duration: 0.25 }, 0.4);
      tl.fromTo(M, { opacity: 0, x: 150 }, { opacity: 1, x: 330, duration: 0.35, ease: "back.out(1.6)" }, at("L5", "Pikachu") - 0.3);
      tl.to(fea, { opacity: 1, duration: 0.1 }, kz - 0.2);
      tl.to(fea, { rotation: 25, svgOrigin: "460 600", duration: 0.08, yoyo: true, repeat: 9 }, kz - 0.1);
      tl.to(M, { rotation: 8, svgOrigin: "330 930", duration: 0.07, yoyo: true, repeat: 11 }, kz);
      tl.to(ha, { opacity: 1, duration: 0.1 }, kz + 0.1);
      tl.to(bolts, { opacity: 1, duration: 0.05, repeat: 9, yoyo: true }, kz + 0.1);
      tl.to(bar, { opacity: 1, attr: { y: 722, height: 216 }, fill: "#39e27a", duration: 0.55, ease: "power2.out" }, hu - 0.35);
      count(tl, "#s03-n", 1, 100, hu - 0.35, 0.55, "", " %", "power2.out");
      tl.to("#s03-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, hu + 0.2);
      tl.to([ph, M, fea, ha, ...bolts, "#s03-box"], { opacity: 0, duration: 0.22 }, l6 - 0.2);
      tl.fromTo(P.g, { opacity: 0, scale: 1.0 }, { opacity: 1, scale: 1.35, duration: 0.3, ease: "back.out(1.8)" }, l6);
      tl.to(spikes, { scaleY: 1, duration: 0.25, ease: "back.out(3)" }, hr);
      tl.to(sparks, { opacity: 1, duration: 0.05, repeat: 11, yoyo: true }, hr + 0.1);
      tl.to(P.g, { x: 560, duration: 0.05, yoyo: true, repeat: 15 }, sk - 0.2);
      tl.to(spikes, { scaleY: 1.15, duration: 0.1, yoyo: true, repeat: 7 }, sk);''' + OUT)

S['s04'] = ('''    #s04-card { left: 140px; top: 540px; width: 800px; height: 420px; border: 6px solid #4da3ff; box-shadow: 0 0 50px rgba(77,163,255,.4); opacity: 0; }
    #s04-card .t1 { margin-top: 120px; font-size: 76px; color: #4da3ff; line-height: 1.05; }
    #s04-card .t2 { margin-top: 22px; font-family: "Space Mono", monospace; font-weight: 700; font-size: 40px; color: #dfe2f5; letter-spacing: .08em; }''',
SVG + '''
      <div id="s04-card" class="panel"><div class="t1">GLURAK-HAFTPFLICHT</div><div class="t2">AB 49 € IM MONAT</div></div>''',
'''      const sv = document.querySelector("#s04-svg");
      const G = el("g", {}, sv);
      el("path", { d: "M600 880 h300 q-10 90 -150 90 q-140 0 -150 -90Z", fill: "#3a3f6e" }, G);
      el("rect", { x: 640, y: 960, width: 16, height: 120, fill: "#8a8fa8" }, G); el("rect", { x: 844, y: 960, width: 16, height: 120, fill: "#8a8fa8" }, G);
      el("rect", { x: 590, y: 868, width: 320, height: 14, rx: 7, fill: "#c9cde6" }, G);
      const wu = [0, 1, 2].map((i) => el("rect", { x: 615 + i * 95, y: 830, width: 80, height: 34, rx: 17, fill: "#ff9aa8" }, G));
      const H = el("g", { opacity: 0 }, sv); el("rect", { x: 620, y: 700, width: 300, height: 260, fill: "#c9cde6" }, H); el("path", { d: "M600 710 L770 560 L940 710Z", fill: "#ff3b55" }, H);
      el("rect", { x: 740, y: 840, width: 60, height: 120, fill: "#6b4f2a" }, H); el("rect", { x: 650, y: 750, width: 60, height: 60, fill: "#4da3ff" }, H);
      const flames = []; for (let i = 0; i < 5; i++) flames.push(el("path", { d: `M${650 + i * 60} 720 q20 -80 30 -150 q20 70 30 150Z`, fill: i % 2 ? "#ffd43b" : "#ff8a3d", opacity: 0 }, sv));
      const D = dragon(sv, 300, 840, 1.0);
      const fire = el("path", { d: "M350 740 Q480 680 640 780 Q480 720 350 760Z", fill: "#ff8a3d", opacity: 0 }, sv);
      const sh = el("g", { opacity: 0 }, sv); el("path", { d: "M540 400 l120 40 v90 q0 90 -120 140 q-120 -50 -120 -140 v-90Z", fill: "#4da3ff" }, sh);
      el("path", { d: "M490 520 l40 40 l70 -80", stroke: "#fff", "stroke-width": 18, fill: "none", "stroke-linecap": "round" }, sh);
      const gr = at("L7", "grillt"), sek = at("L7", "Sekunden"), le = at("L7", "Leider"), nb = at("L7", "Nachbarhaus"), wk = at("L8", "Willkommen"), hp = at("L8", "Glurak-Haftpflicht");
      tl.fromTo([G, D], { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.05);
      tl.to(fire, { opacity: 1, duration: 0.1 }, gr);
      tl.to(fire, { scaleX: 1.15, transformOrigin: "0% 50%", duration: 0.1, yoyo: true, repeat: 7 }, gr + 0.1);
      tl.to(wu, { fill: "#7a3b1a", duration: 0.5, stagger: 0.1 }, sek - 0.3);
      tl.to(wu, { y: -40, duration: 0.15, yoyo: true, repeat: 1, stagger: 0.08 }, sek + 0.2);
      tl.to([G, fire], { opacity: 0, duration: 0.25 }, le - 0.1);
      tl.to(H, { opacity: 1, duration: 0.25 }, le);
      tl.to(D, { rotation: -10, svgOrigin: "300 840", duration: 0.2 }, nb - 0.3);
      tl.set(fire, { scaleX: 1, attr: { d: "M350 720 Q480 660 640 720 Q480 700 350 740Z" } }, nb - 0.2);
      tl.to(fire, { opacity: 1, duration: 0.1 }, nb - 0.15);
      tl.to(flames, { opacity: 1, duration: 0.15, stagger: 0.06 }, nb);
      flames.forEach((f, i) => tl.to(f, { scaleY: 1.3, transformOrigin: "50% 100%", duration: 0.12, repeat: 7, yoyo: true }, nb + 0.2 + i * 0.03));
      tl.to([H, D, fire, ...flames], { opacity: 0.12, duration: 0.25 }, wk - 0.25);
      tl.fromTo("#s04-card", { opacity: 0, scale: 0.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }, wk);
      tl.fromTo(sh, { opacity: 0, scale: 0.5, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, hp - 0.1);
      tl.to("#s04-card", { rotation: 2, duration: 0.15, yoyo: true, repeat: 3 }, hp + 0.3);''' + OUT)

S['s05'] = ('', '''      <div id="s05-box" class="cbox g" style="opacity:0"><div class="lab">UMZUGSWAGEN NÖTIG</div><div id="s05-n" class="num">100 %</div></div>
''' + SVG, '''      const sv = document.querySelector("#s05-svg");
      const O = el("g", {}, sv);
      [[260, 1000, 90], [380, 900, 100], [520, 840, 110], [660, 760, 105], [760, 640, 95], [800, 520, 120]].forEach(([x, y, r]) => el("ellipse", { cx: x, cy: y, rx: r, ry: r * 0.8, fill: "#8a8fa8", stroke: "#5b607a", "stroke-width": 8 }, O));
      el("circle", { cx: 770, cy: 500, r: 12, fill: "#161a36" }, O);
      const B = ball(sv, 300, 640, 70); gsap.set(B.g, { opacity: 0 });
      const T = el("g", { opacity: 0 }, sv); el("rect", { x: 300, y: 700, width: 360, height: 200, rx: 12, fill: "#c9cde6" }, T); el("rect", { x: 660, y: 760, width: 140, height: 140, rx: 12, fill: "#4da3ff" }, T);
      el("circle", { cx: 380, cy: 910, r: 40, fill: "#161a36" }, T); el("circle", { cx: 720, cy: 910, r: 40, fill: "#161a36" }, T);
      const X = el("g", { opacity: 0, stroke: "#ff3b55", "stroke-width": 30, "stroke-linecap": "round" }, sv); el("line", { x1: 280, y1: 640, x2: 820, y2: 980 }, X); el("line", { x1: 820, y1: 640, x2: 280, y2: 980 }, X);
      const pb = at("L9", "Pokéball"), tg = at("L9", "Taschengröße"), l9 = line("L10")[0], ke = at("L10", "Hosentasche");
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

S['s06'] = ('''    #s06-boss { left: 770px; top: 500px; width: 140px; height: 120px; color: #ff3b55; font-size: 120px; line-height: 120px; background: none; opacity: 0; }''',
'''      <div id="s06-box" class="cbox g" style="opacity:0"><div class="lab">STAU</div><div id="s06-n" class="num">45 MIN</div></div>
''' + SVG + '''
      <div id="s06-boss" class="panel">!</div>''',
'''      const sv = document.querySelector("#s06-svg");
      const A = el("g", {}, sv); gsap.set(A, { x: 250, y: 860, scale: 0.9, transformOrigin: "0 0" });
      el("path", { d: "M60 60 q120 -10 110 -120 q-40 70 -110 80Z", fill: "#e8b32a" }, A);
      el("ellipse", { cx: 0, cy: 40, rx: 90, ry: 110, fill: "#e8b32a" }, A);
      el("ellipse", { cx: 0, cy: 50, rx: 66, ry: 64, fill: "#8a5a2b" }, A);
      el("path", { d: "M-60 -150 l-20 -90 l60 60Z M60 -150 l20 -90 l-60 60Z", fill: "#e8b32a" }, A);
      el("circle", { cx: 0, cy: -110, r: 78, fill: "#e8b32a" }, A);
      el("path", { d: "M-44 -118 q14 8 28 0 M16 -118 q14 8 28 0", stroke: "#161a36", "stroke-width": 7, fill: "none", "stroke-linecap": "round" }, A);
      const office = el("g", { opacity: 0 }, sv);
      el("rect", { x: 740, y: 950, width: 310, height: 70, rx: 8, fill: "#8a5a2b" }, office);
      el("rect", { x: 770, y: 1020, width: 20, height: 80, fill: "#6b4f2a" }, office); el("rect", { x: 1000, y: 1020, width: 20, height: 80, fill: "#6b4f2a" }, office);
      el("rect", { x: 940, y: 860, width: 100, height: 84, rx: 10, fill: "#161a36", stroke: "#8fa2ff", "stroke-width": 6 }, office);
      el("text", { x: 895, y: 1000, "text-anchor": "middle", "font-family": "Space Mono", "font-weight": 700, "font-size": 40, fill: "#ffe0a3" }, office).textContent = "BÜRO";
      const B = person(office, "s06-b", 840, 740, 1.0, { three: false, arms: [14, -14], shirt: "#3a3f6e", hair: "#8a8fa8" });
      const P = person(sv, "s06-p", 560, 760, 1.05, { three: false, arms: [16, -16], shirt: "#7fd1ff", pants: "#7fd1ff" });
      const str = el("g", {}, P.g); for (let i = 0; i < 4; i++) el("rect", { x: -56, y: 14 + i * 30, width: 112, height: 10, fill: "#fff", opacity: 0.8 }, str);
      for (let i = 0; i < 3; i++) el("rect", { x: -34 + (i % 2) * 40, y: 140 + i * 26, width: 28, height: 8, fill: "#fff", opacity: 0.8 }, P.g);
      const cap = el("path", { d: "M-46 -84 q46 -70 92 0 q20 -10 40 10 l-10 20Z", fill: "#ff4fb0" }, P.g);
      const blush = [el("circle", { cx: -28, cy: -36, r: 12, fill: "#ff3b55", opacity: 0 }, P.g), el("circle", { cx: 28, cy: -36, r: 12, fill: "#ff3b55", opacity: 0 }, P.g)];
      const fl1 = el("circle", { cx: 560, cy: 800, r: 20, fill: "#fff", opacity: 0 }, sv), fl2 = el("circle", { cx: 600, cy: 800, r: 20, fill: "#e9d6ff", opacity: 0 }, sv);
      const tp = at("L11", "teleportiert"), bu = at("L11", "Büro"), stau = at("L11", "Stau"), l12 = line("L12")[0], sa = at("L12", "Schlafanzug");
      tl.fromTo([A, P.g], { opacity: 0 }, { opacity: 1, duration: 0.35, stagger: 0.1 }, 0.05);
      tl.to(A, { y: 840, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0.4);
      tl.to("#s06-box", { opacity: 1, duration: 0.25 }, tp - 0.4);
      tl.to(fl1, { attr: { r: 300 }, opacity: 1, duration: 0.15 }, tp + 0.1);
      tl.set(P.g, { opacity: 0 }, tp + 0.25);
      tl.to(fl1, { opacity: 0, duration: 0.3 }, tp + 0.25);
      tl.to(A, { x: 180, scale: 0.7, duration: 0.3 }, tp + 0.25);
      tl.to(office, { opacity: 1, duration: 0.3 }, bu - 0.35);
      tl.set(P.g, { x: 600, scale: 1.05, opacity: 1 }, bu - 0.05);
      tl.fromTo(fl2, { attr: { r: 20 }, opacity: 1 }, { attr: { r: 260 }, opacity: 0, duration: 0.35 }, bu - 0.1);
      count(tl, "#s06-n", 45, 0, stau - 0.3, 0.6, "", " MIN", "power3.out");
      tl.to("#s06-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, stau + 0.25);
      tl.to("#s06-box", { opacity: 0, duration: 0.2 }, l12 - 0.1);
      tl.to(P.g, { scale: 1.25, x: 580, duration: 0.3, ease: "back.out(2)" }, sa - 0.3);
      tl.to(blush, { opacity: 0.8, duration: 0.2 }, sa);
      tl.to(str, { opacity: 0.3, duration: 0.1, yoyo: true, repeat: 5 }, sa);
      tl.fromTo("#s06-boss", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, sa - 0.05);
      tl.to(B.g, { x: 852, duration: 0.05, yoyo: true, repeat: 11 }, sa);
      tl.to(cap, { rotation: 20, svgOrigin: "0 -84", duration: 0.12, yoyo: true, repeat: 5 }, sa + 0.1);''' + OUT)

S['s07'] = ('''    .s07-c { position: absolute; top: 930px; width: 300px; height: 150px; border-radius: 24px; text-align: center;
      font-family: "Inter", sans-serif; font-weight: 900; color: #0b0e22; }
    .s07-c .n { margin-top: 18px; font-size: 52px; line-height: 1; } .s07-c .w { margin-top: 12px; font-size: 32px; letter-spacing: .04em; color: #2a2f55; }
    .s07-c .n, .s07-c .w { background: inherit; }
    #s07-c1 { left: 60px; background: #ffd43b; } #s07-c2 { left: 390px; background: #ff8a3d; } #s07-c3 { left: 720px; background: #39e27a; }''',
SVG + '''
      <div id="s07-c1" class="s07-c"><div class="n">PIKACHU</div><div class="w">ALS …?</div></div><div id="s07-c2" class="s07-c"><div class="n">GLURAK</div><div class="w">ALS …?</div></div><div id="s07-c3" class="s07-c"><div class="n">ABRA</div><div class="w">ALS …?</div></div>''',
'''      const sv = document.querySelector("#s07-svg");
      const B = ball(sv, 540, 680, 200);
      const du = at("L13", "du?"), wo = at("L13", "wofür?");
      tl.fromTo(B.g, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.to(B.g, { rotation: 10, svgOrigin: "540 880", duration: 0.08, repeat: 5, yoyo: true }, du - 0.2);
      tl.fromTo(".s07-c", { opacity: 0, y: 80, rotation: (i) => [-8, 6, -6][i] }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, stagger: 0.12, ease: "back.out(2)" }, du + 0.3);
      tl.to(".s07-c", { y: -16, duration: 0.3, yoyo: true, repeat: 11, stagger: 0.1, ease: "sine.inOut" }, du + 1.0);
      tl.to(".s07-c .w", { scale: 1.25, duration: 0.15, yoyo: true, repeat: 1, stagger: 0.08 }, wo - 0.1);
      tl.to(B.g, { rotation: -10, svgOrigin: "540 880", duration: 0.08, repeat: 5, yoyo: true }, wo);''')


here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
