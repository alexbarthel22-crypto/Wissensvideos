#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Klospülung“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
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

S['s01'] = ('''    #s01-news { left: 60px; top: 884px; width: 960px; height: 262px; border: 5px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.5); overflow: hidden; text-align: left; }
    #s01-news .bar { height: 66px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 30px; font-size: 36px; letter-spacing: .08em; }
    #s01-news .hl { padding: 12px 36px 0; font-size: 84px; line-height: 1.0; letter-spacing: -.015em; }
    #s01-news .hl em { font-style: normal; color: #ff4fb0; text-shadow: 0 0 26px rgba(255,79,176,.7); }
    #s01-count .num { font-size: 50px; }
    #s01-q { left: 240px; top: 560px; width: 600px; height: 420px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 150px; line-height: 1.05; padding-top: 40px; box-sizing: border-box; opacity: 0; box-shadow: 0 0 50px rgba(255,59,85,.45); }
    #s01-q small { display: block; font-size: 52px; color: #fff; letter-spacing: .04em; }''',
'''      <div id="s01-count" class="cbox p"><div class="lab">SPÜLUNGEN</div><div class="num">4.000.000.000</div></div>
''' + SVG + '''
      <div id="s01-news" class="panel"><div class="bar">● EILMELDUNG · LIVE</div><div class="hl">4 MRD. SPÜLEN<br><em>GLEICHZEITIG!</em></div></div>
      <div id="s01-q" class="panel">?!<small>NICHT IM KLO</small></div>''',
'''      const sv = document.querySelector("#s01-svg");
      const glow = el("circle", { cx: 540, cy: 700, r: 300, fill: "#4da3ff", opacity: 0.2 }, sv);
      const T = toilet(sv, 540, 790, 0.86);
      const r = rng(4), drops = [];
      for (let i = 0; i < 10; i++) drops.push(drop(sv, 160 + r() * 760, 560 + r() * 260, 0.16 + r() * 0.1));
      const mg = el("g", {}, sv), minis = [];
      for (let i = 0; i < 35; i++) minis.push(miniToilet(mg, 150 + (i % 7) * 130, 600 + Math.floor(i / 7) * 112, 1));
      const ab = at("L1", "abziehen"), gl = at("L1", "gleichzeitig"), vier = at("L2", "Vier"), sek = at("L2", "Sekunde"), nicht = at("L2", "nicht");
      tl.to(T.swirl, { rotation: -900, svgOrigin: "0 0", duration: 5, ease: "power1.in" }, 0);
      tl.fromTo(glow, { attr: { opacity: 0.2 } }, { attr: { opacity: 0.45 }, duration: 0.35, repeat: 5, yoyo: true }, 0);
      drops.forEach((d, i) => tl.fromTo(d, { y: "-=40", opacity: 0.9 }, { y: "+=160", opacity: 0, duration: 1.2, ease: "power1.in", repeat: 1 }, 0.1 * i));
      tl.to("#s01-news", { opacity: 0, y: 160, duration: 0.3, ease: "power3.in" }, Math.max(gl - 0.1, 2.6));
      tl.to(T.g, { y: 760, scale: 1.05, duration: 0.4, ease: "expo.out" }, Math.max(gl + 0.2, 2.9));
      tl.to(T.handle, { rotation: 28, svgOrigin: "46 -229", duration: 0.12, yoyo: true, repeat: 1 }, ab);
      tl.to(glow, { attr: { r: 700, opacity: 0.8 }, duration: 0.2 }, ab + 0.05);
      tl.to(glow, { attr: { r: 300, opacity: 0.2 }, duration: 0.4 }, ab + 0.25);
      tl.to(T.g, { x: 548, duration: 0.04, repeat: 7, yoyo: true }, ab + 0.05);
      tl.to([T.g, glow], { opacity: 0, scale: 0.3, duration: 0.3, ease: "power3.in" }, vier - 0.3);
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
      const fall = el("g", { opacity: 0 }, sv);
      el("path", { d: "M80 520 H1000 V600 H80Z", fill: "#2d6b4f" }, fall);
      el("path", { d: "M60 600 H1020 V640 H60Z", fill: "#3b4b6e" }, fall);
      const strands = [];
      for (let i = 0; i < 18; i++) strands.push(el("path", { d: `M${105 + i * 51} 640 V1060`, stroke: i % 2 ? "#cfe8ff" : "#4da3ff", "stroke-width": 52, "stroke-dasharray": `${220 + (i % 3) * 60} 26`, fill: "none" }, fall));
      const mist = []; for (let i = 0; i < 7; i++) mist.push(el("circle", { cx: 120 + i * 140, cy: 1060, r: 70, fill: "#e6f2ff", opacity: 0.85 }, fall));
      const sechs = at("L3", "sechs"), z = at("L3", "24"), l4 = line("L4")[0], nia = at("L4", "Niagarafälle"), ue = at("L4", "über");
      tl.fromTo(D, { opacity: 0, y: 300 }, { opacity: 1, y: 800, duration: 0.6, ease: "bounce.out" }, 0.05);
      tl.to("#s02-box", { opacity: 1, duration: 0.25 }, sechs - 0.3);
      count(tl, "#s02-n", 0, 6, sechs - 0.1, 0.5, "", " LITER");
      tl.fromTo(L6, { opacity: 0, scale: 0.4, svgOrigin: "540 850" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, sechs);
      tl.to([D, L6], { scale: 0.25, y: "+=200", opacity: 0, duration: 0.4, ease: "power3.in" }, z - 0.5);
      count(tl, "#s02-n", 6, 24000000000, z - 0.3, 1.4, "", " L", "power3.in");
      tl.fromTo(F, { y: 0 }, { y: -660, duration: 1.6, ease: "power2.inOut" }, z - 0.3);
      tl.fromTo(F2, { y: 0 }, { y: -640, duration: 1.7, ease: "power2.inOut" }, z - 0.2);
      tl.to([F, F2], { x: -135, duration: 0.6, repeat: 3, yoyo: true, ease: "sine.inOut" }, z);
      tl.to([F, F2], { y: 200, opacity: 0, duration: 0.4, ease: "power3.in" }, l4 - 0.1);
      tl.to(fall, { opacity: 1, duration: 0.35 }, nia - 0.4);
      tl.fromTo(strands, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -1300 }, duration: 3.5, ease: "none" }, nia - 0.4);
      tl.fromTo(mist, { scale: 0.8, svgOrigin: "540 1060" }, { scale: 1.15, duration: 0.5, repeat: 5, yoyo: true, stagger: 0.08 }, nia - 0.3);
      tl.to("#s02-box .lab", { textContent: "SO LANGE FÄLLT NIAGARA", duration: 0.01 }, ue - 0.2);
      tl.set("#s02-n", { textContent: "> 2 STUNDEN" }, ue - 0.2);
      tl.to("#s02-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, ue);''' + OUT)

S['s03'] = ('''    #s03-box .num { font-size: 52px; }''',
'''      <div id="s03-box" class="cbox r" style="opacity:0"><div class="lab">WASSERDRUCK</div><div id="s03-n" class="num">4 BAR</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s03-svg");
      const bld = el("g", {}, sv), wins = [];
      el("rect", { x: 110, y: 540, width: 330, height: 600, rx: 10, fill: "#262d63" }, bld);
      for (let f = 0; f < 14; f++) { const row = []; for (let c = 0; c < 4; c++) row.push(el("rect", { x: 132 + c * 76, y: 1100 - f * 40, width: 56, height: 26, rx: 4, fill: "#ffd43b" }, bld)); wins.push(row); }
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
      el("rect", { x: 520, y: 548, width: 40, height: 100, fill: "#8f9bc4" }, sh);
      el("path", { d: "M420 670 Q540 610 660 670Z", fill: "#c9cde6" }, sh);
      const P = person(sh, "s03p", 540, 880, 1.15, { three: false, arms: [150, -150], shirt: "#f2c9a5", pants: "#4da3ff" });
      const jets = []; for (let i = 0; i < 9; i++) jets.push(el("path", { d: `M${452 + i * 22} 680 V820`, stroke: "#4da3ff", "stroke-width": 7, "stroke-dasharray": "26 22", "stroke-linecap": "round" }, sh));
      const steam = []; for (let i = 0; i < 6; i++) steam.push(el("circle", { cx: 390 + i * 60, cy: 780 - (i % 2) * 60, r: 50, fill: "#e6eaf5", opacity: 0 }, sh));
      const gl = at("L5", "gleichzeitig"), br = at("L5", "bricht"), zs = at("L6", "zehnten"), du = at("L6", "duscht"), heiss = at("L7", "brühend");
      tl.fromTo(bld, { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.fromTo(gg, { opacity: 0, scale: 0.5, svgOrigin: "770 800" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.2);
      tl.to("#s03-box", { opacity: 1, duration: 0.25 }, gl - 0.4);
      tl.to(needle, { rotation: 40, svgOrigin: "770 800", duration: 0.1, repeat: 5, yoyo: true }, gl);
      tl.to(needle, { rotation: -95, svgOrigin: "770 800", duration: 0.5, ease: "back.out(2)" }, br - 0.1);
      count(tl, "#s03-n", 4, 1, br - 0.1, 0.6, "", " BAR");
      tl.to(gg, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, br + 0.1);
      wins.forEach((row, f) => { if (f >= 9) tl.to(row, { attr: { fill: "#3a2140" }, duration: 0.15 }, zs + (13 - f) * 0.06); });
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
      tl.to(P.g, { y: 810, duration: 0.15, yoyo: true, repeat: 3, ease: "power2.out" }, heiss);
      tl.to("#s03p-mouth", { attr: { d: "M-16 -24 q16 -22 32 0" }, duration: 0.1 }, heiss);''' + OUT)

S['s04'] = ('''    #s04-box .num { font-size: 52px; }''',
'''      <div id="s04-box" class="cbox g" style="opacity:0"><div class="lab">KANAL-AUSLASTUNG</div><div id="s04-n" class="num">0 %</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s04-svg");
      const top = el("g", {}, sv);
      el("rect", { x: 0, y: 600, width: 1080, height: 540, fill: "#2a2140" }, top);
      el("rect", { x: 0, y: 580, width: 1080, height: 26, fill: "#3b4b6e" }, top);
      [[90, 70], [330, 90], [570, 80], [810, 95]].forEach(([x, h]) => { el("rect", { x, y: 580 - h, width: 180, height: h, fill: "#4a5590" }, top); el("path", { d: `M${x - 10} ${580 - h} L${x + 90} ${540 - h} L${x + 190} ${580 - h}Z`, fill: "#ff3b55" }, top); });
      const dps = [];
      [180, 420, 660, 900].forEach((x) => { el("rect", { x: x - 18, y: 606, width: 36, height: 170, fill: "#161a36" }, top);
        dps.push(el("path", { d: `M${x} 600 V780`, stroke: "#8a6a3c", "stroke-width": 22, "stroke-dasharray": "24 18", opacity: 0 }, top)); });
      el("rect", { x: 40, y: 770, width: 1000, height: 150, rx: 75, fill: "#161a36", stroke: "#4a5590", "stroke-width": 10 }, top);
      const wtr = el("rect", { x: 50, y: 880, width: 980, height: 30, rx: 15, fill: "#8a6a3c" }, top);
      const pl = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 560, width: 1080, height: 600, fill: "#16234a" }, pl);
      [280, 760].forEach((x) => { el("ellipse", { cx: x, cy: 760, rx: 200, ry: 60, fill: "#8f9bc4" }, pl); el("ellipse", { cx: x, cy: 740, rx: 180, ry: 44, fill: "#6b5a3a" }, pl); });
      const spill = [280, 760].map((x) => el("path", { d: `M${x - 186} 752 q-40 100 -14 210 h44 q-24 -100 14 -210Z M${x + 186} 752 q40 100 14 210 h-44 q24 -100 -14 -210Z`, fill: "#7a5c34", opacity: 0 }, pl));
      txt(pl, 540, 640, "KLÄRWERK", 48, "#dfe2f5");
      const river = el("rect", { x: 0, y: 960, width: 1080, height: 170, fill: "#2f7fe0" }, pl);
      const fishes = [fish(pl, 220, 1040, 1), fish(pl, 560, 1060, 0.9, "#ffd43b"), fish(pl, 870, 1030, 1)];
      const nt = at("L8", "normale"), alle = at("L8", "alle"), l9 = line("L9")[0], fl = at("L9", "Flüsse"), fi = at("L9", "Fische");
      tl.fromTo(top, { opacity: 0, y: 140 }, { opacity: 1, y: 60, duration: 0.45, ease: "expo.out" }, 0.05);
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

S['s05'] = ('''    #s05-box .num { font-size: 52px; }''',
'''      <div id="s05-box" class="cbox r" style="opacity:0"><div class="lab">WASSER IM KELLER</div><div id="s05-n" class="num">0 CM</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s05-svg");
      el("rect", { x: 0, y: 640, width: 1080, height: 500, fill: "#2a2140" }, sv);
      el("rect", { x: 0, y: 620, width: 1080, height: 24, fill: "#3b4b6e" }, sv);
      el("rect", { x: 180, y: 540, width: 720, height: 80, fill: "#4a5590" }, sv);
      el("rect", { x: 200, y: 660, width: 680, height: 330, rx: 8, fill: "#3a3f78" }, sv);
      txt(sv, 300, 710, "KELLER", 36, "#8f9bc4");
      el("rect", { x: 520, y: 990, width: 40, height: 70, fill: "#161a36" }, sv);
      el("rect", { x: 30, y: 1050, width: 1020, height: 70, rx: 35, fill: "#161a36", stroke: "#4a5590", "stroke-width": 8 }, sv);
      const sew = el("path", { d: "M60 1085 H1020", stroke: "#8a6a3c", "stroke-width": 36, "stroke-dasharray": "50 30" }, sv);
      const up = el("path", { d: "M540 1060 V1000 M516 1024 L540 996 L564 1024", stroke: "#ff3b55", "stroke-width": 10, fill: "none", opacity: 0 }, sv);
      const T = toilet(sv, 540, 900, 0.42, "#4da3ff");
      const fount = el("path", { d: "M540 860 C470 760 420 720 380 820 M540 860 C540 740 540 700 540 690 M540 860 C610 760 660 720 700 820", stroke: "#8a6a3c", "stroke-width": 28, "stroke-linecap": "round", fill: "none", opacity: 0 }, sv);
      const cl = el("clipPath", { id: "s05-clip" }, sv); el("rect", { x: 200, y: 660, width: 680, height: 330 }, cl);
      const fg = el("g", { "clip-path": "url(#s05-clip)" }, sv); const F = flood(fg, 1000, "#7a5c34");
      const q = txt(sv, 540, 760, "?", 140, "#ffd43b", { opacity: 0 });
      const iw = at("L10", "irgendwohin"), zu = at("L11", "zurück"), aus = at("L11", "Aus"), ob = at("L11", "oben");
      tl.fromTo(sew, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -600 }, duration: 3, ease: "power1.in" }, 0);
      tl.fromTo(q, { opacity: 0, scale: 0.4, svgOrigin: "540 720" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, iw - 0.1);
      tl.to(q, { opacity: 0, duration: 0.2 }, zu - 0.4);
      tl.to(sew, { attr: { "stroke-dashoffset": -200 }, duration: 0.6, ease: "power2.in" }, zu - 0.5);
      tl.to(up, { opacity: 1, duration: 0.1, repeat: 5, yoyo: true }, zu - 0.1);
      tl.to("#s05-box", { opacity: 1, duration: 0.25 }, zu - 0.2);
      tl.to(T.water, { attr: { fill: "#7a5c34" }, duration: 0.2 }, zu);
      tl.to(T.g, { x: 548, duration: 0.04, repeat: 9, yoyo: true }, zu + 0.1);
      tl.fromTo(fount, { opacity: 0, scale: 0.2, svgOrigin: "540 860" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, aus);
      tl.to(fount, { scaleY: 1.12, svgOrigin: "540 860", duration: 0.12, repeat: 9, yoyo: true }, aus + 0.35);
      tl.fromTo(F, { y: 0 }, { y: -160, duration: 2.2, ease: "power1.in" }, aus + 0.1);
      count(tl, "#s05-n", 0, 40, aus + 0.1, 2.2, "", " CM", "power1.in");
      tl.to("#s05-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, ob);''' + OUT)

S['s06'] = ('''    #s06-box .num { font-size: 50px; }
    .s06-c { position: absolute; top: 600px; width: 290px; height: 330px; border-radius: 24px; background: rgba(20,24,56,.92); border: 4px solid #2e3670; }
    .s06-c b { position: absolute; left: 0; right: 0; bottom: 22px; text-align: center; font: 900 36px Inter, sans-serif; color: #fff; }
    #s06-c1 { left: 60px; } #s06-c2 { left: 395px; } #s06-c3 { left: 730px; }
    #s06-doc { left: 300px; top: 560px; width: 480px; height: 560px; background: #eef2fb; border-radius: 18px; opacity: 0; }
    #s06-doc h3 { margin: 40px 0 26px; text-align: center; font: 900 46px Inter, sans-serif; color: #161a36; }
    #s06-doc i { display: block; margin: 0 50px 24px; height: 18px; border-radius: 9px; background: #c3cbe4; }
    #s06-st { left: 320px; top: 760px; width: 440px; height: 140px; border: 10px solid #ff3b55; border-radius: 18px; color: #ff3b55; font: 900 70px/120px Inter, sans-serif; text-align: center; opacity: 0; }
    #s06-v { left: 610px; top: 620px; width: 400px; height: 420px; border-radius: 24px; background: rgba(20,24,56,.3); border: 5px solid #ffd43b; box-shadow: 0 0 40px rgba(255,212,59,.4); opacity: 0; text-align: center; }
    #s06-v b { position: absolute; left: 0; right: 0; bottom: 26px; font: 900 40px/1.05 Inter, sans-serif; color: #ffd43b; }''',
'''      <div id="s06-box" class="cbox r" style="opacity:0"><div class="lab">SCHÄDEN</div><div id="s06-n" class="num">0 €</div></div>
      <div id="s06-c1" class="s06-c abs"><b>PUMPEN</b></div><div id="s06-c2" class="s06-c abs"><b>ROHRE</b></div><div id="s06-c3" class="s06-c abs"><b>KELLER</b></div>
''' + SVG + '''
      <div id="s06-doc" class="abs"><h3>VERSICHERUNG</h3><i></i><i></i><i style="width:60%"></i><i></i><i></i><i style="width:50%"></i></div>
      <div id="s06-st" class="abs">ABGELEHNT</div>
      <div id="s06-v" class="abs"><b>RÜCKSTAU-<br>KLAPPE?</b></div>''',
'''      const sv = document.querySelector("#s06-svg");
      const ic = el("g", {}, sv);
      const pump = el("g", { opacity: 0 }, ic); el("circle", { cx: 205, cy: 740, r: 90, fill: "#4a5590" }, pump);
      const blades = el("g", {}, pump); [0, 120, 240].forEach((a) => el("path", { d: "M205 740 L205 670 Q240 690 215 740Z", fill: "#cfe8ff", transform: `rotate(${a} 205 740)` }, blades));
      el("circle", { cx: 205, cy: 740, r: 16, fill: "#161a36" }, pump);
      const pipe = el("g", { opacity: 0 }, ic);
      el("rect", { x: 430, y: 710, width: 100, height: 60, rx: 10, fill: "#8f9bc4", transform: "rotate(-12 480 740)" }, pipe);
      el("rect", { x: 560, y: 720, width: 100, height: 60, rx: 10, fill: "#8f9bc4", transform: "rotate(14 610 750)" }, pipe);
      const spr = el("path", { d: "M545 735 l-20 -90 M545 735 l10 -100 M545 735 l40 -80", stroke: "#4da3ff", "stroke-width": 12, "stroke-linecap": "round" }, pipe);
      const kel = el("g", { opacity: 0 }, ic); el("rect", { x: 780, y: 650, width: 190, height: 170, rx: 8, fill: "#3a3f78" }, kel);
      el("path", { d: "M765 655 L875 590 L985 655Z", fill: "#ff3b55" }, kel);
      const kf = el("rect", { x: 780, y: 780, width: 190, height: 40, fill: "#7a5c34" }, kel);
      const r = rng(9), coins = [], cg = el("g", { "data-layout-allow-overlap": "" }, sv); for (let i = 0; i < 16; i++) coins.push(txt(cg, 100 + r() * 880, 560, "€", 70 + r() * 40, "#ffd43b", { opacity: 0 }));
      const vl = el("g", { opacity: 0 }, sv);
      el("rect", { x: 650, y: 760, width: 320, height: 70, rx: 14, fill: "#8f9bc4" }, vl);
      const flap = el("rect", { x: 800, y: 742, width: 18, height: 106, rx: 6, fill: "#ffd43b" }, vl);
      const ms = at("L12", "Milliardenschäden"), pu = at("L12", "Pumpen"), ro = at("L12", "Rohre"), ke = at("L12", "geflutete"), l13 = line("L13")[0], kc = at("L13", "keinen"), rk = at("L13", "Rückstauklappe");
      tl.to("#s06-box", { opacity: 1, duration: 0.25 }, ms - 0.3);
      count(tl, "#s06-n", 0, 999000000, ms - 0.2, 0.9, "", " €", "power2.in");
      tl.set("#s06-n", { textContent: "MILLIARDEN €" }, ms + 0.75);
      coins.forEach((c, i) => tl.set(c, { opacity: 1 }, ms + i * 0.04).to(c, { y: 560 + (i % 4) * 40, rotation: (i % 2 ? 1 : -1) * 200, svgOrigin: `${c.getAttribute("x")} 560`, duration: 1.0, ease: "power1.in" }, ms + i * 0.04).to(c, { opacity: 0, duration: 0.2 }, ms + 1 + i * 0.04));
      [["#s06-c1", pump, pu], ["#s06-c2", pipe, ro], ["#s06-c3", kel, ke]].forEach(([c, g, t]) => {
        tl.fromTo(c, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, t - 0.15);
        tl.fromTo(g, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, t - 0.15); });
      tl.to(blades, { rotation: 720, svgOrigin: "205 740", duration: 1.2, ease: "power2.out" }, pu);
      tl.to(blades, { x: 6, duration: 0.04, repeat: 7, yoyo: true }, pu + 1.2);
      tl.fromTo(spr, { opacity: 1 }, { opacity: 0.3, duration: 0.08, repeat: 9, yoyo: true }, ro);
      tl.fromTo(kf, { attr: { y: 820, height: 0 } }, { attr: { y: 720, height: 100 }, duration: 0.9 }, ke);
      tl.to([".s06-c", ic], { opacity: 0, filter: "blur(8px)", duration: 0.25 }, l13 - 0.3);
      tl.fromTo("#s06-doc", { opacity: 0, y: 60, rotation: -4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(1.8)" }, l13 - 0.1);
      tl.fromTo("#s06-st", { opacity: 0, scale: 2.4, rotation: -14 }, { opacity: 1, scale: 1, rotation: -14, duration: 0.25, ease: "power4.in" }, kc - 0.2);
      tl.to("#s06-doc", { x: 8, duration: 0.04, repeat: 5, yoyo: true }, kc + 0.05);
      tl.to(["#s06-doc", "#s06-st"], { x: -240, scale: 0.75, duration: 0.4, ease: "power3.inOut" }, rk - 0.4);
      tl.to("#s06-v", { opacity: 1, duration: 0.3 }, rk - 0.2);
      tl.to(vl, { opacity: 1, duration: 0.3 }, rk - 0.2);
      tl.to(flap, { rotation: 70, svgOrigin: "809 742", duration: 0.25, repeat: 3, yoyo: true }, rk + 0.2);''' + OUT)

S['s07'] = ('''    #s07-box .num { font-size: 44px; }''',
'''      <div id="s07-box" class="cbox r" style="opacity:0"><div class="lab">OHNE SICHERE TOILETTE</div><div id="s07-n" class="num">0</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s07-svg");
      const ppl = [], xs = [];
      for (let i = 0; i < 50; i++) { const x = 200 + (i % 10) * 76, y = 640 + Math.floor(i / 10) * 100; const g = el("g", { opacity: 0 }, sv);
        const h = el("circle", { cx: x, cy: y, r: 17, fill: "#dfe2f5" }, g); const b = el("rect", { x: x - 24, y: y + 21, width: 48, height: 40, rx: 18, fill: "#dfe2f5" }, g); ppl.push({ g, h, b }); }
      const r = rng(5), idx = [...Array(50).keys()].sort(() => r() - 0.5), red = idx.slice(0, 22), none = red.slice(0, 3);
      none.forEach((i) => xs.push(txt(sv, 200 + (i % 10) * 76, 640 + Math.floor(i / 10) * 100 + 36, "✕", 80, "#ffd43b", { opacity: 0 })));
      const mt = el("g", { opacity: 0 }, sv); const T = toilet(mt, 540, 870, 0.75);
      el("circle", { cx: 540, cy: 780, r: 250, fill: "none", stroke: "#ff3b55", "stroke-width": 30 }, mt);
      el("path", { d: "M363 957 L717 603", stroke: "#ff3b55", "stroke-width": 30 }, mt);
      const ec = at("L14", "echte"), d35 = at("L14", "3,5"), kt = at("L14", "keine"), m419 = at("L15", "419"), gk = at("L15", "gar"), hw = at("L15", "halbe"), mi = at("L15", "mitspülen");
      ppl.forEach((p, i) => tl.fromTo(p.g, { opacity: 0, scale: 0.3, svgOrigin: `${200 + (i % 10) * 76} ${660 + Math.floor(i / 10) * 100}` }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }, 0.05 + i * 0.02));
      tl.to(sv, { x: 8, duration: 0.04, repeat: 5, yoyo: true }, ec);
      tl.to("#s07-box", { opacity: 1, duration: 0.25 }, d35 - 0.3);
      count(tl, "#s07-n", 0, 3500000000, d35 - 0.2, 1.2, "", "", "power3.out");
      red.forEach((i, k) => tl.to([ppl[i].h, ppl[i].b], { attr: { fill: "#ff3b55" }, duration: 0.12 }, d35 + k * 0.05));
      tl.to("#s07-box .lab", { textContent: "GAR KEINE TOILETTE", duration: 0.01 }, m419 - 0.2);
      count(tl, "#s07-n", 0, 419000000, m419 - 0.1, 1.0, "", "", "power3.out");
      tl.to(xs, { opacity: 1, duration: 0.15, stagger: 0.08 }, gk - 0.1);
      tl.to(red.map((i) => ppl[i].g), { opacity: 0.4, duration: 0.15, yoyo: true, repeat: 3 }, hw);
      tl.to([...ppl.map((p) => p.g), ...xs], { opacity: 0.15, duration: 0.3 }, mi - 0.6);
      tl.fromTo(mt, { opacity: 0, scale: 0.5, svgOrigin: "540 780" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, mi - 0.4);''' + OUT)

S['s08'] = ('''    .s08-b { position: absolute; top: 940px; width: 450px; height: 150px; border-radius: 26px; text-align: center; font: 900 48px/150px Inter, sans-serif; color: #0b0e22; }
    #s08-b1 { left: 50px; background: #ff4fb0; box-shadow: 0 0 40px rgba(255,79,176,.5); } #s08-b2 { left: 580px; background: #39e27a; box-shadow: 0 0 40px rgba(57,226,122,.5); }''',
SVG + '''
      <div id="s08-b1" class="s08-b">MITSPÜLEN</div><div id="s08-b2" class="s08-b">KELLER SICHERN</div>''',
'''      const sv = document.querySelector("#s08-svg");
      const glow = el("circle", { cx: 540, cy: 700, r: 260, fill: "#ff4fb0", opacity: 0.2 }, sv);
      const T = toilet(sv, 540, 790, 0.8);
      const du = at("L16", "du?"), mi = at("L16", "mitspülen"), ks = at("L16", "vorher"), ko = at("L16", "Kommentare");
      tl.fromTo(T.g, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 0.8, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.to(T.swirl, { rotation: -1080, svgOrigin: "0 0", duration: 8, ease: "none" }, 0.1);
      tl.to(T.g, { rotation: 6, svgOrigin: "540 920", duration: 0.08, repeat: 5, yoyo: true }, du - 0.1);
      tl.fromTo("#s08-b1", { opacity: 0, y: 80, rotation: -6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, mi - 0.15);
      tl.fromTo("#s08-b2", { opacity: 0, y: 80, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, ks - 0.15);
      tl.to(".s08-b", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 7, stagger: 0.3, ease: "sine.inOut" }, ko - 0.3);
      tl.fromTo(glow, { attr: { opacity: 0.2 } }, { attr: { opacity: 0.45 }, duration: 0.4, repeat: 7, yoyo: true }, ko - 0.3);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
