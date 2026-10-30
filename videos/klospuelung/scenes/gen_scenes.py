#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Klospülung“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
from pathlib import Path

HEAD = '''<template>
  <style>
    /*__COMMON_CSS__*/
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .panel { position: absolute; border-radius: 24px; background: rgba(13,16,38,.94); text-align: center; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; }
    .cbox { top: 440px; } /* unter der großen Kapitel-Überschrift */
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

S['s01'] = ('''    #s01-news { left: 60px; top: 884px; width: 960px; height: 262px; border: 5px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.5); overflow: hidden; text-align: left; }
    #s01-news .bar { height: 66px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 30px; font-size: 36px; letter-spacing: .08em; }
    #s01-news .hl { padding: 12px 36px 0; font-size: 84px; line-height: 1.0; letter-spacing: -.015em; }
    #s01-news .hl em { font-style: normal; color: #ff4fb0; text-shadow: 0 0 26px rgba(255,79,176,.7); }
    #s01-count .num { font-size: 50px; }
    #s01-q { left: 240px; top: 600px; width: 600px; height: 420px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 150px; line-height: 1.05; padding-top: 40px; box-sizing: border-box; opacity: 0; box-shadow: 0 0 50px rgba(255,59,85,.45); }
    #s01-q small { display: block; font-size: 52px; color: #fff; letter-spacing: .04em; }''',
'''      <div id="s01-count" class="cbox p"><div class="lab">SPÜLUNGEN</div><div class="num">4.000.000.000</div></div>
''' + SVG + '''
      <div id="s01-news" class="panel"><div class="bar">● EILMELDUNG · LIVE</div><div class="hl">ALLE MENSCHEN<br><em>SPÜLEN!</em></div></div>
      <div id="s01-q" class="panel">?!<small>NICHT IM KLO</small></div>''',
'''      const sv = document.querySelector("#s01-svg");
      const glow = el("circle", { cx: 540, cy: 780, r: 230, fill: "#ff3b55", opacity: 0.25 }, sv);
      const wt = el("g", {}, sv);
      const tri = el("path", { d: "M540 590 L780 870 Q790 884 772 884 H308 Q290 884 300 870Z", fill: "#ffd43b", stroke: "#ff3b55", "stroke-width": 26, "stroke-linejoin": "round" }, wt);
      const ex = txt(wt, 540, 860, "!", 230, "#161a36");
      const sideL = miniToilet(sv, 190, 790, 2.1), sideR = miniToilet(sv, 890, 790, 2.1);
      gsap.set([sideL.g, sideR.g], { opacity: 1 });
      const mg = el("g", {}, sv), minis = [];
      for (let i = 0; i < 35; i++) minis.push(miniToilet(mg, 150 + (i % 7) * 130, 650 + Math.floor(i / 7) * 100, 1));
      const sp = at("L1", "spülen"), vier = at("L2", "Vier"), sek = at("L2", "Sekunde"), nicht = at("L2", "nicht");
      tl.to(tri, { attr: { fill: "#ff3b55", stroke: "#ffd43b" }, duration: 0.01, repeat: 13, yoyo: true, repeatDelay: 0.2 }, 0.2);
      tl.to(ex, { attr: { fill: "#ffffff" }, duration: 0.01, repeat: 13, yoyo: true, repeatDelay: 0.2 }, 0.2);
      tl.fromTo(glow, { attr: { opacity: 0.25 } }, { attr: { opacity: 0.6, r: 280 }, duration: 0.21, repeat: 13, yoyo: true }, 0.2);
      tl.fromTo(wt, { scale: 1.1, svgOrigin: "540 760" }, { scale: 1, duration: 0.4, ease: "expo.out" }, 0);
      tl.to(sideL.g, { rotation: 8, duration: 0.06, repeat: 15, yoyo: true, svgOrigin: "190 840" }, 0.3);
      tl.to(sideR.g, { rotation: -8, duration: 0.06, repeat: 15, yoyo: true, svgOrigin: "890 840" }, 0.3);
      tl.to("#s01-news", { opacity: 0, y: 160, duration: 0.3, ease: "power3.in" }, Math.max(sp - 0.6, 2.6));
      tl.to(wt, { scale: 1.2, svgOrigin: "540 760", duration: 0.12, yoyo: true, repeat: 3 }, sp);
      tl.to([wt, glow, sideL.g, sideR.g], { opacity: 0, scale: 0.3, svgOrigin: "540 760", duration: 0.3, ease: "power3.in" }, vier - 0.3);
      tl.fromTo("#s01-count", { scale: 1 }, { scale: 1.12, duration: 0.15, yoyo: true, repeat: 1 }, vier);
      minis.forEach((m, i) => tl.fromTo(m.g, { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, vier + i * 0.025));
      tl.to(minis.map((m) => m.w), { attr: { fill: "#cfe8ff" }, duration: 0.1, yoyo: true, repeat: 3 }, sek);
      tl.to(mg, { y: 10, duration: 0.05, yoyo: true, repeat: 7 }, sek);
      tl.to(minis.map((m) => m.g), { opacity: 0, filter: "blur(8px)", duration: 0.25 }, nicht - 0.75);
      tl.fromTo("#s01-q", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, nicht - 0.55);
      tl.to("#s01-q", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, nicht + 0.3);''' + OUT)

S['s02'] = ('''    #s02-box .num { font-size: 44px; }''',
'''      <div id="s02-box" class="cbox b" style="opacity:0"><div class="lab">WASSER</div><div id="s02-n" class="num">0 L</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s02-svg");
      const D = drop(sv, 540, 800, 1.6);
      const L6 = txt(sv, 540, 880, "6 L", 110, "#ffffff"); gsap.set(L6, { opacity: 0 });
      const fcl = el("clipPath", { id: "s02-clip" }, sv); el("rect", { x: 0, y: 0, width: 1080, height: 1130 }, fcl);
      const fg = el("g", { "clip-path": "url(#s02-clip)" }, sv);
      const F = flood(fg, 1180, "#2f7fe0"); const F2 = flood(fg, 1210, "#4da3ff");
      const fall = el("g", { opacity: 0, transform: "translate(0 50)" }, sv);
      el("path", { d: "M80 520 H1000 V600 H80Z", fill: "#2d6b4f" }, fall);
      el("path", { d: "M60 600 H1020 V640 H60Z", fill: "#3b4b6e" }, fall);
      const strands = [];
      for (let i = 0; i < 18; i++) strands.push(el("path", { d: `M${105 + i * 51} 640 V1060`, stroke: i % 2 ? "#cfe8ff" : "#4da3ff", "stroke-width": 52, "stroke-dasharray": `${220 + (i % 3) * 60} 26`, fill: "none" }, fall));
      const mist = []; for (let i = 0; i < 7; i++) mist.push(el("circle", { cx: 120 + i * 140, cy: 1020, r: 70, fill: "#e6f2ff", opacity: 0.85 }, fall));
      const sechs = at("L3", "sechs"), z = at("L3", "24"), l4 = line("L4")[0], nia = at("L4", "Niagarafälle"), ue = at("L4", "über");
      tl.fromTo(D, { opacity: 0, y: 300 }, { opacity: 1, y: 800, duration: 0.6, ease: "bounce.out" }, 0.05);
      tl.to("#s02-box", { opacity: 1, duration: 0.25 }, sechs - 0.3);
      count(tl, "#s02-n", 0, 6, sechs - 0.1, 0.5, "", " LITER");
      tl.fromTo(L6, { opacity: 0, scale: 0.4, svgOrigin: "540 850" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, sechs);
      tl.to([D, L6], { scale: 0.25, y: "+=200", opacity: 0, duration: 0.4, ease: "power3.in" }, z - 0.5);
      count(tl, "#s02-n", 6, 24000000000, z - 0.3, 1.4, "", " L", "power3.in");
      tl.fromTo(F, { y: 0 }, { y: -600, duration: 1.6, ease: "power2.inOut" }, z - 0.3);
      tl.fromTo(F2, { y: 0 }, { y: -580, duration: 1.7, ease: "power2.inOut" }, z - 0.2);
      tl.to([F, F2], { x: -135, duration: 0.6, repeat: 3, yoyo: true, ease: "sine.inOut" }, z);
      tl.to([F, F2], { y: 200, opacity: 0, duration: 0.4, ease: "power3.in" }, l4 - 0.1);
      tl.to(fall, { opacity: 1, duration: 0.35 }, nia - 0.4);
      tl.fromTo(strands, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -1300 }, duration: 3.5, ease: "none" }, nia - 0.4);
      tl.fromTo(mist, { scale: 0.8, svgOrigin: "540 1020" }, { scale: 1.15, duration: 0.5, repeat: 5, yoyo: true, stagger: 0.08 }, nia - 0.3);
      tl.to("#s02-box .lab", { textContent: "SO LANGE FÄLLT NIAGARA", duration: 0.01 }, ue - 0.2);
      tl.set("#s02-n", { textContent: "> 2 STUNDEN" }, ue - 0.2);
      tl.to("#s02-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, ue);''' + OUT)

S['s03'] = ('''    #s03-box .num { font-size: 52px; }''',
'''      <div id="s03-box" class="cbox r" style="opacity:0"><div class="lab">WASSERDRUCK</div><div id="s03-n" class="num">4 BAR</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s03-svg");
      const bld = el("g", {}, sv), wins = [];
      el("rect", { x: 110, y: 600, width: 330, height: 540, rx: 10, fill: "#262d63" }, bld);
      for (let f = 0; f < 13; f++) { const row = []; for (let c = 0; c < 4; c++) row.push(el("rect", { x: 132 + c * 76, y: 1100 - f * 40, width: 56, height: 26, rx: 4, fill: "#ffd43b" }, bld)); wins.push(row); }
      const ten = el("g", { opacity: 0 }, bld);
      el("path", { d: "M90 721 H460", stroke: "#ff3b55", "stroke-width": 8, "stroke-dasharray": "22 12" }, ten);
      txt(ten, 400, 706, "10.", 40, "#ff3b55");
      const gg = el("g", {}, sv);
      el("circle", { cx: 770, cy: 800, r: 190, fill: "#141838", stroke: "#2e3670", "stroke-width": 10 }, gg);
      const arc = (a0, a1, c) => { const p = (a) => [770 + 150 * Math.cos(a * Math.PI / 180), 800 + 150 * Math.sin(a * Math.PI / 180)];
        const [x0, y0] = p(a0), [x1, y1] = p(a1); el("path", { d: `M${x0} ${y0} A150 150 0 0 1 ${x1} ${y1}`, stroke: c, "stroke-width": 26, fill: "none" }, gg); };
      arc(150, 210, "#ff3b55"); arc(212, 270, "#ffd43b"); arc(272, 390, "#39e27a");
      const needle = el("path", { d: "M764 800 L770 660 L776 800Z", fill: "#ffffff" }, gg);
      el("circle", { cx: 770, cy: 800, r: 20, fill: "#ffffff" }, gg);
      txt(gg, 770, 930, "DRUCK", 40, "#dfe2f5");
      gsap.set(needle, { rotation: 60, svgOrigin: "770 800" });
      const sh = el("g", { opacity: 0 }, sv);
      el("rect", { x: 520, y: 590, width: 40, height: 100, fill: "#8f9bc4" }, sh);
      el("path", { d: "M420 710 Q540 650 660 710Z", fill: "#c9cde6" }, sh);
      const P = person(sh, "s03p", 540, 900, 1, { three: false, arms: [150, -150], shirt: "#f2c9a5", pants: "#4da3ff" });
      const jets = []; for (let i = 0; i < 9; i++) jets.push(el("path", { d: `M${452 + i * 22} 720 V850`, stroke: "#4da3ff", "stroke-width": 7, "stroke-dasharray": "26 22", "stroke-linecap": "round" }, sh));
      const steam = []; for (let i = 0; i < 6; i++) steam.push(el("circle", { cx: 390 + i * 60, cy: 800 - (i % 2) * 60, r: 50, fill: "#e6eaf5", opacity: 0 }, sh));
      const gl = at("L5", "gleichzeitig"), br = at("L5", "bricht"), zs = at("L6", "zehnten"), du = at("L6", "duscht"), heiss = at("L7", "brühend");
      tl.fromTo(bld, { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.fromTo(gg, { opacity: 0, scale: 0.5, svgOrigin: "770 800" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.2);
      tl.to("#s03-box", { opacity: 1, duration: 0.25 }, gl - 0.4);
      tl.to(needle, { rotation: 40, svgOrigin: "770 800", duration: 0.1, repeat: 5, yoyo: true }, gl);
      tl.to(needle, { rotation: -95, svgOrigin: "770 800", duration: 0.5, ease: "back.out(2)" }, br - 0.1);
      count(tl, "#s03-n", 4, 1, br - 0.1, 0.6, "", " BAR");
      tl.to(gg, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, br + 0.1);
      wins.forEach((row, f) => { if (f >= 9) tl.to(row, { attr: { fill: "#3a2140" }, duration: 0.15 }, zs + (12 - f) * 0.06); });
      tl.to(ten, { opacity: 1, duration: 0.2 }, zs);
      tl.to([bld, gg], { opacity: 0, filter: "blur(8px)", duration: 0.25 }, du - 0.6);
      tl.to("#s03-box .lab", { textContent: "DUSCHE", duration: 0.01 }, du - 0.35);
      tl.set("#s03-n", { textContent: "38 °C" }, du - 0.35);
      tl.to("#s03-box", { borderColor: "#4da3ff", duration: 0.01 }, du - 0.35);
      tl.to(sh, { opacity: 1, duration: 0.3 }, du - 0.3);
      tl.fromTo(jets, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -480 }, duration: 4, ease: "none" }, du - 0.3);
      tl.to(jets, { attr: { stroke: "#ff3b55" }, duration: 0.15 }, heiss - 0.1);
      tl.to("#s03-box", { borderColor: "#ff3b55", duration: 0.01 }, heiss);
      count(tl, "#s03-n", 38, 60, heiss - 0.1, 0.5, "", " °C");
      tl.to(steam, { opacity: 0.8, y: -60, duration: 0.6, stagger: 0.05 }, heiss);
      tl.to(P.g, { y: 830, duration: 0.15, yoyo: true, repeat: 3, ease: "power2.out" }, heiss);
      tl.to("#s03p-mouth", { attr: { d: "M-16 -24 q16 -22 32 0" }, duration: 0.1 }, heiss);''' + OUT)

S['s04'] = ('''    #s04-box .num { font-size: 52px; }''',
'''      <div id="s04-box" class="cbox g" style="opacity:0"><div class="lab">KANAL-AUSLASTUNG</div><div id="s04-n" class="num">0 %</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s04-svg");
      const top = el("g", {}, sv);
      el("rect", { x: 0, y: 600, width: 1080, height: 540, fill: "#2a2140" }, top);
      el("rect", { x: 0, y: 580, width: 1080, height: 26, fill: "#3b4b6e" }, top);
      [[90, 50], [330, 60], [570, 55], [810, 60]].forEach(([x, h]) => { el("rect", { x, y: 580 - h, width: 180, height: h, fill: "#4a5590" }, top); el("path", { d: `M${x - 10} ${580 - h} L${x + 90} ${540 - h} L${x + 190} ${580 - h}Z`, fill: "#ff3b55" }, top); });
      const dps = [];
      [180, 420, 660, 900].forEach((x) => { el("rect", { x: x - 18, y: 606, width: 36, height: 170, fill: "#161a36" }, top);
        dps.push(el("path", { d: `M${x} 600 V780`, stroke: "#8a6a3c", "stroke-width": 22, "stroke-dasharray": "24 18", opacity: 0 }, top)); });
      el("rect", { x: 40, y: 770, width: 1000, height: 150, rx: 75, fill: "#161a36", stroke: "#4a5590", "stroke-width": 10 }, top);
      const wtr = el("rect", { x: 50, y: 880, width: 980, height: 30, rx: 15, fill: "#8a6a3c" }, top);
      const pl = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 590, width: 1080, height: 560, fill: "#16234a" }, pl);
      [280, 760].forEach((x) => { el("ellipse", { cx: x, cy: 760, rx: 200, ry: 60, fill: "#8f9bc4" }, pl); el("ellipse", { cx: x, cy: 740, rx: 180, ry: 44, fill: "#6b5a3a" }, pl); });
      const spill = [280, 760].map((x) => el("path", { d: `M${x - 186} 752 q-40 100 -14 210 h44 q-24 -100 14 -210Z M${x + 186} 752 q40 100 14 210 h-44 q24 -100 -14 -210Z`, fill: "#7a5c34", opacity: 0 }, pl));
      txt(pl, 540, 640, "KLÄRWERK", 48, "#dfe2f5");
      const river = el("rect", { x: 0, y: 960, width: 1080, height: 170, fill: "#2f7fe0" }, pl);
      const fishes = [fish(pl, 220, 1040, 1), fish(pl, 560, 1060, 0.9, "#ffd43b"), fish(pl, 870, 1030, 1)];
      const nt = at("L8", "normale"), alle = at("L8", "alle"), l9 = line("L9")[0], fl = at("L9", "Flüsse"), fi = at("L9", "Fische");
      tl.fromTo(top, { opacity: 0, y: 190 }, { opacity: 1, y: 110, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.to("#s04-box", { opacity: 1, duration: 0.25 }, nt - 0.4);
      count(tl, "#s04-n", 0, 30, nt - 0.2, 0.5, "", " %");
      tl.to(dps, { opacity: 1, duration: 0.2, stagger: 0.08 }, alle - 0.4);
      tl.fromTo(dps, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -400 }, duration: 2.5, ease: "none" }, alle - 0.4);
      tl.to(wtr, { attr: { y: 780, height: 130 }, duration: 0.8, ease: "power2.in" }, alle - 0.2);
      count(tl, "#s04-n", 30, 100, alle - 0.2, 0.8, "", " %", "power2.in");
      tl.to("#s04-box", { borderColor: "#ff3b55", duration: 0.01 }, alle + 0.6);
      tl.set("#s04-n", { textContent: "ÜBERLAST!" }, alle + 0.7);
      tl.to(top, { x: 10, duration: 0.04, repeat: 9, yoyo: true }, alle + 0.6);
      tl.to(top, { opacity: 0, filter: "blur(8px)", duration: 0.25 }, l9 - 0.35);
      tl.to(pl, { opacity: 1, duration: 0.3 }, l9 - 0.2);
      tl.to(spill, { opacity: 1, duration: 0.4, stagger: 0.15 }, l9 + 0.2);
      tl.to(river, { attr: { fill: "#6b5a3a" }, duration: 0.8 }, fl - 0.2);
      fishes.forEach((f, i) => { tl.to(f.g, { rotation: 180, y: 975, duration: 0.5, ease: "back.out(2)" }, fi + i * 0.15); tl.to(f.g, { attr: { opacity: 0.8 }, duration: 0.2 }, fi + i * 0.15); });
      tl.set(fishes.map((f) => f.eye), { attr: { r: 0 } }, fi);
      fishes.forEach((f, i) => txt(pl, [220, 560, 870][i], 1002, "✕", 34, "#ff3b55", { opacity: 0, class: "s04-x" }));
      tl.to(".s04-x", { opacity: 1, duration: 0.15, stagger: 0.15 }, fi + 0.3);''' + OUT)

S['s05'] = ('''    #s05-box .num { font-size: 52px; }
    #s05-med { left: 700px; top: 600px; width: 300px; height: 150px; border-radius: 22px; background: rgba(20,24,56,.94); border: 5px solid #ffd43b; opacity: 0;
      text-align: center; font: 900 40px/1.1 Inter, sans-serif; color: #ffd43b; padding-top: 22px; box-sizing: border-box; box-shadow: 0 0 40px rgba(255,212,59,.4); }''',
'''      <div id="s05-box" class="cbox r" style="opacity:0"><div class="lab">ABWASSER-PEGEL</div><div id="s05-n" class="num">0 CM</div></div>
''' + SVG + '''
      <div id="s05-med" class="abs">OLYMPIA<br>2024</div>''',
'''      const sv = document.querySelector("#s05-svg");
      const city = el("g", {}, sv);
      el("circle", { cx: 880, cy: 660, r: 50, fill: "#f4d27a", opacity: 0.8 }, city);
      const tw = el("g", {}, city);
      el("path", { d: "M540 600 L556 700 L590 860 L640 1060 H596 Q568 960 540 960 Q512 960 484 1060 H440 L490 860 L524 700Z", fill: "#c9a46a" }, tw);
      el("rect", { x: 486, y: 850, width: 108, height: 18, fill: "#8a6a3c" }, tw); el("rect", { x: 515, y: 700, width: 50, height: 14, fill: "#8a6a3c" }, tw);
      el("path", { d: "M540 600 V560", stroke: "#c9a46a", "stroke-width": 8 }, tw);
      const lights = []; for (let i = 0; i < 10; i++) lights.push(el("circle", { cx: 500 + (i % 5) * 20, cy: 760 + Math.floor(i / 5) * 140 + (i % 2) * 20, r: 5, fill: "#fff3c0" }, tw));
      [[40, 760, 300, 300], [790, 780, 250, 280]].forEach(([x, y, w, h]) => { el("rect", { x, y, width: w, height: h, fill: "#3a4078" }, city);
        el("path", { d: `M${x - 10} ${y} L${x + 20} ${y - 50} H${x + w - 20} L${x + w + 10} ${y}Z`, fill: "#4f5a9a" }, city);
        for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) el("rect", { x: x + 22 + c * (w - 40) / 4, y: y + 30 + r * 64, width: 34, height: 44, rx: 4, fill: "#ffd43b", opacity: 0.85 }, city); });
      el("rect", { x: 0, y: 1060, width: 1080, height: 70, fill: "#2a2f55" }, city);
      const covers = [200, 540, 880].map((x) => el("ellipse", { cx: x, cy: 1092, rx: 70, ry: 18, fill: "#8f9bc4", stroke: "#161a36", "stroke-width": 6 }, city));
      const jets = [200, 540, 880].map((x) => el("path", { d: `M${x - 30} 1100 Q${x} 860 ${x + 30} 1100Z`, fill: "#7a5c34", opacity: 0 }, city));
      const cl = el("clipPath", { id: "s05-clip" }, sv); el("rect", { x: 0, y: 0, width: 1080, height: 1130 }, cl);
      const fg = el("g", { "clip-path": "url(#s05-clip)" }, sv); const F = flood(fg, 1140, "#7a5c34");
      const lab = txt(sv, 540, 1010, "SEINE", 64, "#ffd43b", { opacity: 0 });
      const gd = at("L10", "Gullydeckel"), fs = at("L10", "flutet"), se = at("L11", "Seine"), kl = at("L11", "Kloake"), ol = at("L11", "Olympischen");
      tl.fromTo(city, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.fromTo(lights, { opacity: 1 }, { opacity: 0.2, duration: 0.15, repeat: 9, yoyo: true, stagger: 0.05 }, 0.3);
      covers.forEach((c, i) => { tl.to(c, { y: -360 - i * 40, rotation: 300 + i * 90, svgOrigin: `${[200, 540, 880][i]} 1092`, duration: 0.6, ease: "power2.out" }, gd + i * 0.08);
        tl.to(c, { y: 0, opacity: 0, duration: 0.4, ease: "power2.in" }, gd + 0.6 + i * 0.08); });
      tl.fromTo(jets, { opacity: 0, scaleY: 0.1, svgOrigin: "540 1100" }, { opacity: 1, scaleY: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.08 }, gd + 0.02);
      tl.to(jets, { scaleY: 1.15, svgOrigin: "540 1100", duration: 0.12, repeat: 9, yoyo: true }, gd + 0.35);
      tl.to("#s05-box", { opacity: 1, duration: 0.25 }, fs - 0.3);
      tl.to(F, { y: -150, duration: 1.6, ease: "power1.inOut" }, fs - 0.2);
      tl.to(F, { x: -135, duration: 0.6, repeat: 5, yoyo: true, ease: "sine.inOut" }, fs);
      count(tl, "#s05-n", 0, 20, fs - 0.2, 1.6, "", " CM", "power1.inOut");
      tl.fromTo(lab, { opacity: 0, scale: 0.4, svgOrigin: "540 990" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, se - 0.1);
      tl.to("#s05-box .lab", { textContent: "SEINE · KEIME", duration: 0.01 }, kl - 0.2);
      tl.set("#s05-n", { textContent: "ALARM!" }, kl - 0.2);
      tl.to("#s05-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, kl);
      tl.fromTo("#s05-med", { opacity: 0, y: 60, rotation: 8 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, ol - 0.2);''' + OUT)

S['s06'] = ('''    #s06-box .num { font-size: 44px; }''',
'''      <div id="s06-box" class="cbox b" style="opacity:0"><div class="lab">MENSCHEN AM MEER</div><div id="s06-n" class="num">0</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s06-svg");
      const beach = el("g", {}, sv);
      const sea = el("rect", { x: 0, y: 700, width: 1080, height: 300, fill: "#2f7fe0" }, beach);
      const wave = el("path", { d: "M-40 700 q65 -22 135 0 t135 0 t135 0 t135 0 t135 0 t135 0 t135 0 t135 0 t135 0 V740 H-40Z", fill: "#4da3ff" }, beach);
      el("rect", { x: 0, y: 990, width: 1080, height: 140, fill: "#e8c77a" }, beach);
      el("circle", { cx: 860, cy: 630, r: 56, fill: "#ffd43b" }, beach);
      const r = rng(11), crowd = el("g", { "data-layout-allow-overlap": "" }, beach), ppl = [];
      const COL = ["#ff4fb0", "#4da3ff", "#39e27a", "#ffd43b", "#ff8a3d"];
      for (let i = 0; i < 60; i++) ppl.push(mini(crowd, 40 + r() * 1000, 900 + r() * 150, COL[i % 5]));
      const algae = []; for (let i = 0; i < 14; i++) algae.push(el("circle", { cx: 60 + i * 74, cy: 760 + (i % 3) * 70, r: 60, fill: "#39e27a", opacity: 0 }, beach));
      const road = el("g", { opacity: 0 }, sv);
      el("path", { d: "M440 580 H640 L1000 1130 H80Z", fill: "#2a2f55" }, road);
      el("path", { d: "M540 600 V1130", stroke: "#ffd43b", "stroke-width": 8, "stroke-dasharray": "40 30" }, road);
      const cars = []; for (let k = 0; k < 18; k++) { const row = Math.floor(k / 3), t = row / 5, y = 620 + t * 460, w = 50 + t * 90, x = 540 + ((k % 3) - 1) * (110 + t * 220) - w / 2;
        const c = el("g", {}, road); el("rect", { x, y, width: w, height: w * 0.6, rx: 10, fill: COL[k % 5] }, c); el("rect", { x: x + w * 0.1, y: y + w * 0.6 - 6, width: w * 0.8, height: 8, fill: "#ff3b55" }, c); cars.push(c); }
      const me = at("L12", "Meer"), vm = at("L12", "Vier"), l13 = line("L13")[0], st = at("L13", "Stau"), l14 = line("L14")[0], t8 = at("L14", "800.000"), al = at("L14", "Algen");
      tl.fromTo(beach, { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.05);
      tl.to(wave, { x: -135, duration: 0.8, repeat: 9, yoyo: true, ease: "sine.inOut" }, 0.1);
      tl.to("#s06-box", { opacity: 1, duration: 0.25 }, vm - 0.3);
      count(tl, "#s06-n", 0, 4000000000, vm - 0.2, 1.2, "", "", "power3.out");
      ppl.forEach((p, i) => tl.to(p, { opacity: 1, duration: 0.15 }, vm + i * 0.02));
      ppl.forEach((p, i) => tl.to(p, { y: -150 - (i % 4) * 25, duration: 0.6, ease: "power2.inOut" }, me - 0.2 + (i % 10) * 0.03));
      tl.to(beach, { opacity: 0, duration: 0.25 }, l13 - 0.3);
      tl.to(road, { opacity: 1, duration: 0.3 }, l13 - 0.1);
      cars.forEach((c, i) => tl.fromTo(c, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }, l13 + i * 0.05));
      tl.to("#s06-box .lab", { textContent: "STAU ZUM STRAND", duration: 0.01 }, st - 0.2);
      tl.set("#s06-n", { textContent: "ENDLOS" }, st - 0.2);
      tl.to("#s06-box", { borderColor: "#ff3b55", scale: 1.12, duration: 0.12, yoyo: true, repeat: 1 }, st);
      tl.to(road, { x: 6, duration: 0.05, repeat: 7, yoyo: true }, st + 0.1);
      tl.to(road, { opacity: 0, duration: 0.25 }, l14 - 0.3);
      tl.to(beach, { opacity: 1, duration: 0.3 }, l14 - 0.1);
      tl.to("#s06-box .lab", { textContent: "AUF EINEN SCHLAG", duration: 0.01 }, t8 - 0.3);
      count(tl, "#s06-n", 0, 800000, t8 - 0.2, 0.8, "", " T", "power3.out");
      tl.to([sea, wave], { attr: { fill: "#6b6a3a" }, duration: 1.0 }, t8);
      algae.forEach((a, i) => tl.fromTo(a, { opacity: 0, scale: 0.1, svgOrigin: `${60 + i * 74} ${760 + (i % 3) * 70}` }, { opacity: 0.9, scale: 1, duration: 0.4, ease: "back.out(2)" }, al - 0.1 + i * 0.05));''' + OUT)

S['s07'] = ('''    #s07-box .num { font-size: 50px; }
    .s07-c { position: absolute; top: 620px; width: 290px; height: 330px; border-radius: 24px; background: rgba(20,24,56,.92); border: 4px solid #ff3b55; box-shadow: 0 0 30px rgba(255,59,85,.3); }
    .s07-c b { position: absolute; left: 0; right: 0; bottom: 22px; text-align: center; font: 900 34px Inter, sans-serif; color: #fff; }
    #s07-c1 { left: 60px; } #s07-c2 { left: 395px; } #s07-c3 { left: 730px; }''',
'''      <div id="s07-box" class="cbox r" style="opacity:0"><div class="lab">TOURISMUS</div><div id="s07-n" class="num">0 €</div></div>
      <div id="s07-c1" class="s07-c abs"><b>BADEVERBOT</b></div><div id="s07-c2" class="s07-c abs"><b>FISCHFANG</b></div><div id="s07-c3" class="s07-c abs"><b>URLAUB</b></div>
''' + SVG,
'''      const sv = document.querySelector("#s07-svg");
      const ic = el("g", {}, sv);
      const g1 = el("g", { opacity: 0 }, ic); el("circle", { cx: 205, cy: 760, r: 95, fill: "#fff", stroke: "#ff3b55", "stroke-width": 18 }, g1);
      el("circle", { cx: 175, cy: 735, r: 16, fill: "#161a36" }, g1); el("path", { d: "M150 790 q25 -20 50 0 t50 0", stroke: "#4da3ff", "stroke-width": 10, fill: "none" }, g1);
      el("path", { d: "M160 760 l50 -20", stroke: "#161a36", "stroke-width": 12, "stroke-linecap": "round" }, g1);
      el("path", { d: "M138 693 L272 827", stroke: "#ff3b55", "stroke-width": 18 }, g1);
      const g2 = el("g", {}, ic); const F = fish(g2, 540, 760, 1.6, "#ff8a3d"); gsap.set(g2, { opacity: 0 });
      const x2 = txt(g2, 540, 800, "✕", 150, "#ff3b55");
      const g3 = el("g", { opacity: 0 }, ic); el("rect", { x: 805, y: 700, width: 150, height: 120, rx: 16, fill: "#ff8a3d" }, g3);
      el("path", { d: "M845 700 v-26 h70 v26", stroke: "#ff8a3d", "stroke-width": 12, fill: "none" }, g3); el("rect", { x: 805, y: 748, width: 150, height: 14, fill: "#c9611f" }, g3);
      const x3 = txt(g3, 880, 810, "✕", 150, "#ff3b55");
      const ch = el("g", { opacity: 0 }, sv);
      el("path", { d: "M160 620 V1060 H940", stroke: "#8f9bc4", "stroke-width": 8, fill: "none" }, ch);
      const ln = el("path", { d: "M180 680 L360 700 L480 690 L560 900 L700 960 L900 1030", stroke: "#ff3b55", "stroke-width": 16, fill: "none", "stroke-linejoin": "round", "stroke-dasharray": 1000, "stroke-dashoffset": 1000 }, ch);
      const r = rng(9), cg = el("g", { "data-layout-allow-overlap": "" }, sv), coins = []; for (let i = 0; i < 14; i++) coins.push(txt(cg, 120 + r() * 840, 600, "€", 70 + r() * 40, "#ffd43b", { opacity: 0 }));
      const bv = at("L15", "Badeverbot"), ff = at("L15", "Fischfang"), ur = at("L15", "Urlaub"), l16 = line("L16")[0], mv = at("L16", "Milliarden");
      [["#s07-c1", g1, bv], ["#s07-c2", g2, ff], ["#s07-c3", g3, ur]].forEach(([c, g, t]) => {
        tl.fromTo(c, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, t - 0.15);
        tl.fromTo(g, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, t - 0.15); });
      tl.fromTo([x2, x3], { opacity: 0 }, { opacity: 1, duration: 0.1 }, ff + 0.3);
      tl.set(x3, { opacity: 0 }, ff + 0.3); tl.to(x3, { opacity: 1, duration: 0.1 }, ur + 0.3);
      tl.to(F.g, { rotation: 180, svgOrigin: "540 760", duration: 0.4 }, ff + 0.3);
      tl.to([".s07-c", ic], { opacity: 0, filter: "blur(8px)", duration: 0.25 }, l16 - 0.3);
      tl.to(ch, { opacity: 1, duration: 0.3 }, l16 - 0.1);
      tl.to(ln, { attr: { "stroke-dashoffset": 0 }, duration: 1.4, ease: "power2.in" }, l16);
      tl.to("#s07-box", { opacity: 1, duration: 0.25 }, mv - 0.4);
      count(tl, "#s07-n", 0, 999000000, mv - 0.3, 0.8, "– ", " €", "power2.in");
      tl.set("#s07-n", { textContent: "– MILLIARDEN €" }, mv + 0.55);
      tl.to("#s07-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, mv + 0.55);
      coins.forEach((c, i) => tl.set(c, { opacity: 1 }, mv + i * 0.04).to(c, { y: 500 + (i % 4) * 30, rotation: (i % 2 ? 1 : -1) * 200, svgOrigin: `${c.getAttribute("x")} 600`, duration: 1.0, ease: "power1.in" }, mv + i * 0.04).to(c, { opacity: 0, duration: 0.2 }, mv + 1 + i * 0.04));''' + OUT)

S['s08'] = ('''    .s08-b { position: absolute; top: 950px; width: 450px; height: 150px; border-radius: 26px; text-align: center; font: 900 50px/150px Inter, sans-serif; color: #0b0e22; }
    #s08-b1 { left: 50px; background: #ff4fb0; box-shadow: 0 0 40px rgba(255,79,176,.5); } #s08-b2 { left: 580px; background: #39e27a; box-shadow: 0 0 40px rgba(57,226,122,.5); }
    #s08-f { left: 290px; top: 950px; width: 500px; height: 150px; border-radius: 75px; background: #ff3b55; box-shadow: 0 0 50px rgba(255,59,85,.6); opacity: 0;
      text-align: center; font: 900 64px/150px Inter, sans-serif; color: #fff; }''',
SVG + '''
      <div id="s08-b1" class="s08-b">JEDES MAL</div><div id="s08-b2" class="s08-b">SELTENER</div>
      <div id="s08-f" class="abs">+ FOLGEN</div>''',
'''      const sv = document.querySelector("#s08-svg");
      const boom = el("path", { d: (() => { const p = []; for (let i = 0; i < 24; i++) { const a = i / 24 * Math.PI * 2, r = i % 2 ? 170 : 290; p.push(`${540 + r * Math.cos(a)},${760 + r * Math.sin(a)}`); } return "M" + p.join(" L") + "Z"; })(), fill: "#ffd43b", opacity: 0 }, sv);
      const boom2 = el("circle", { cx: 540, cy: 760, r: 150, fill: "#ff8a3d", opacity: 0 }, sv);
      const glow = el("circle", { cx: 540, cy: 740, r: 250, fill: "#ff4fb0", opacity: 0.2 }, sv);
      const T = toilet(sv, 540, 830, 0.8);
      const du = at("L17", "du?"), na = at("L17", "nach"), se = at("L17", "seltener"), ko = at("L17", "Kommentare"), l18 = line("L18")[0], fo = at("L18", "folg"), ex = at("L18", "explodiert"), ab = at("L18", "Abend");
      tl.fromTo(T.g, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 0.8, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.to(T.swirl, { rotation: -1440, svgOrigin: "0 0", duration: 10, ease: "none" }, 0.1);
      tl.to(T.g, { rotation: 6, svgOrigin: "540 960", duration: 0.08, repeat: 5, yoyo: true }, du - 0.1);
      tl.fromTo("#s08-b1", { opacity: 0, y: 80, rotation: -6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, na - 0.15);
      tl.fromTo("#s08-b2", { opacity: 0, y: 80, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, se - 0.15);
      tl.to(".s08-b", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 3, stagger: 0.3, ease: "sine.inOut" }, ko - 0.3);
      tl.to(".s08-b", { opacity: 0, y: 60, duration: 0.25, ease: "power3.in" }, l18 - 0.2);
      tl.fromTo("#s08-f", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, fo - 0.1);
      tl.to("#s08-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);
      tl.to(T.g, { x: 10, duration: 0.04, repeat: 15, yoyo: true }, ex - 0.6);
      tl.to(T.water, { attr: { fill: "#ff3b55" }, duration: 0.2 }, ex - 0.3);
      tl.fromTo(boom, { opacity: 0, scale: 0.2, svgOrigin: "540 760" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, ex);
      tl.fromTo(boom2, { opacity: 0, scale: 0.2, svgOrigin: "540 760" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, ex + 0.05);
      tl.to(glow, { opacity: 0, duration: 0.2 }, ex);
      tl.to([boom, boom2], { rotation: 15, svgOrigin: "540 760", duration: 0.3, yoyo: true, repeat: 5 }, ex + 0.3);
      tl.to(T.g, { y: -30, duration: 0.15, yoyo: true, repeat: 5, ease: "power2.out" }, ab);''')


here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
