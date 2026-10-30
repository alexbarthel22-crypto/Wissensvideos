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

S['s01'] = ('''    #s01-news { left: 60px; top: 952px; width: 960px; height: 196px; border: 5px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.5); overflow: hidden; text-align: left; }
    #s01-news .bar { height: 50px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 30px; font-size: 36px; letter-spacing: .08em; }
    #s01-news .hl { padding: 6px 36px 0; text-align: center; font-size: 68px; line-height: 1.0; letter-spacing: -.015em; }
    #s01-news .hl em { font-style: normal; color: #ff4fb0; text-shadow: 0 0 26px rgba(255,79,176,.7); }
    #s01-count .num { font-size: 50px; }
    #s01-q { left: 240px; top: 600px; width: 600px; height: 420px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 150px; line-height: 1.05; padding-top: 40px; box-sizing: border-box; opacity: 0; box-shadow: 0 0 50px rgba(255,59,85,.45); }
    #s01-q small { display: block; font-size: 52px; color: #fff; letter-spacing: .04em; }''',
'''      <div id="s01-count" class="cbox p" style="opacity:0"><div class="lab">SPÜLUNGEN</div><div class="num">4.000.000.000</div></div>
''' + SVG + '''
      <div id="s01-news" class="panel"><div class="bar">● EILMELDUNG · LIVE</div><div class="hl">ALLE SPÜLEN<br><em>GLEICHZEITIG!</em></div></div>
      <div id="s01-q" class="panel">?!<small>NICHT IM KLO</small></div>''',
'''      const sv = document.querySelector("#s01-svg");
      const glow = el("circle", { cx: 540, cy: 740, r: 290, fill: "#4da3ff", opacity: 0.25 }, sv);
      const T = toilet(sv, 540, 790, 1.1);
      const warn = (x) => { const g = el("g", {}, sv);
        const t = el("path", { d: `M${x} 560 L${x + 70} 665 H${x - 70}Z`, fill: "#ffd43b", stroke: "#ff3b55", "stroke-width": 12, "stroke-linejoin": "round" }, g);
        const e = txt(g, x, 655, "!", 70, "#161a36"); return { g, t, e }; };
      const W = [warn(110), warn(970)];
      const r = rng(4), drops = []; for (let i = 0; i < 8; i++) drops.push(drop(sv, 300 + r() * 480, 520 + r() * 120, 0.12 + r() * 0.08));
      const mg = el("g", {}, sv), minis = [];
      for (let i = 0; i < 35; i++) minis.push(miniToilet(mg, 150 + (i % 7) * 130, 650 + Math.floor(i / 7) * 100, 1));
      const sp = at("L1", "spülen"), vier = at("L2", "Vier"), sek = at("L2", "Sekunde"), nicht = at("L2", "nicht");
      tl.to(T.swirl, { rotation: -1100, svgOrigin: "0 0", duration: 6, ease: "power1.in" }, 0);
      tl.to(T.handle, { rotation: 28, svgOrigin: "46 -229", duration: 0.12, yoyo: true, repeat: 1 }, 0.15);
      tl.fromTo(glow, { attr: { opacity: 0.25 } }, { attr: { opacity: 0.5 }, duration: 0.35, repeat: 7, yoyo: true }, 0);
      drops.forEach((d, i) => tl.fromTo(d, { y: "-=30", opacity: 0.9 }, { y: "+=120", opacity: 0, duration: 1.1, ease: "power1.in", repeat: 2 }, 0.1 * i));
      W.forEach((w) => { tl.to(w.t, { attr: { fill: "#ff3b55", stroke: "#ffd43b" }, duration: 0.01, repeat: 13, yoyo: true, repeatDelay: 0.22 }, 0.2);
        tl.to(w.e, { attr: { fill: "#ffffff" }, duration: 0.01, repeat: 13, yoyo: true, repeatDelay: 0.22 }, 0.2); });
      tl.to("#s01-news", { opacity: 0, scale: 0.85, duration: 0.25, ease: "power3.in" }, 2.6);
      tl.to(T.handle, { rotation: 28, svgOrigin: "46 -229", duration: 0.12, yoyo: true, repeat: 1 }, sp);
      tl.to(glow, { attr: { r: 600, opacity: 0.8 }, duration: 0.2 }, sp + 0.05);
      tl.to(glow, { attr: { r: 290, opacity: 0.25 }, duration: 0.4 }, sp + 0.25);
      tl.to(T.g, { x: 548, duration: 0.04, repeat: 7, yoyo: true }, sp + 0.05);
      tl.to([glow, ...W.map((w) => w.g)], { opacity: 0, scale: 0.3, svgOrigin: "540 760", duration: 0.3, ease: "power3.in" }, vier - 0.3);
      tl.to(T.g, { opacity: 0, scale: 0.3, duration: 0.3, ease: "power3.in" }, vier - 0.3);
      tl.to("#s01-count", { opacity: 1, duration: 0.2 }, vier - 0.25);
      tl.fromTo("#s01-count", { scale: 1 }, { scale: 1.12, duration: 0.15, yoyo: true, repeat: 1 }, vier);
      minis.forEach((m, i) => tl.fromTo(m.g, { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, vier + i * 0.025));
      tl.to(minis.map((m) => m.w), { attr: { fill: "#cfe8ff" }, duration: 0.1, yoyo: true, repeat: 3 }, sek);
      tl.to(mg, { y: 10, duration: 0.05, yoyo: true, repeat: 7 }, sek);
      tl.to(minis.map((m) => m.g), { opacity: 0, filter: "blur(8px)", duration: 0.25 }, nicht - 0.75);
      tl.fromTo("#s01-q", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, nicht - 0.55);
      tl.to("#s01-q", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, nicht + 0.3);''' + OUT)

S['s02'] = ('''    #s02-box .num, #s02-box2 .num { font-size: 44px; }''',
'''      <div id="s02-box" class="cbox b" style="opacity:0"><div class="lab">WASSER</div><div id="s02-n" class="num">0 L</div></div>
      <div id="s02-box2" class="cbox y" style="opacity:0"><div class="lab">OLYMPIA-BECKEN</div><div id="s02-n2" class="num">0</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s02-svg");
      const D = drop(sv, 540, 800, 1.6);
      const L6 = txt(sv, 540, 880, "6 L", 110, "#ffffff"); gsap.set(L6, { opacity: 0 });
      const fcl = el("clipPath", { id: "s02-clip" }, sv); el("rect", { x: 0, y: 0, width: 1080, height: 1130 }, fcl);
      const fg = el("g", { "clip-path": "url(#s02-clip)" }, sv);
      const F = flood(fg, 1180, "#2f7fe0"); const F2 = flood(fg, 1210, "#4da3ff");
      const pools = [];
      for (let i = 0; i < 16; i++) { const x = 70 + (i % 4) * 240, y = 600 + Math.floor(i / 4) * 128, g = el("g", { opacity: 0 }, sv);
        el("rect", { x, y, width: 220, height: 110, rx: 10, fill: "#dfe5f5" }, g); el("rect", { x: x + 10, y: y + 10, width: 200, height: 90, rx: 6, fill: "#2f9be0" }, g);
        for (let k = 1; k < 4; k++) el("path", { d: `M${x + 14} ${y + 10 + k * 22.5} H${x + 206}`, stroke: "#ffffff", "stroke-width": 4, "stroke-dasharray": "10 8" }, g);
        pools.push(g); }
      const sechs = at("L3", "sechs"), z = at("L3", "24"), l4 = line("L4")[0], n96 = at("L4", "9.600"), sek = at("L4", "Sekunde");
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
      tl.to("#s02-box", { opacity: 0, duration: 0.2 }, n96 - 0.4);
      tl.to("#s02-box2", { opacity: 1, duration: 0.2 }, n96 - 0.3);
      count(tl, "#s02-n2", 0, 9600, n96 - 0.2, 1.2, "", "", "power2.out");
      pools.forEach((p, i) => tl.fromTo(p, { opacity: 0, scale: 0.3, svgOrigin: `${180 + (i % 4) * 240} ${655 + Math.floor(i / 4) * 128}` }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, n96 - 0.1 + i * 0.06));
      tl.to(pools, { y: 8, duration: 0.05, yoyo: true, repeat: 7 }, sek);
      tl.to("#s02-box2", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, sek);''' + OUT)

S['s03'] = ('''    #s03-box .num, #s03-box2 .num { font-size: 52px; }''',
'''      <div id="s03-box" class="cbox r" style="opacity:0"><div class="lab">WASSERDRUCK</div><div id="s03-n" class="num">4 BAR</div></div>
      <div id="s03-box2" class="cbox b" style="opacity:0"><div class="lab">DUSCHE</div><div id="s03-n2" class="num">38 °C</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s03-svg");
      const gg = el("g", {}, sv);
      el("circle", { cx: 540, cy: 800, r: 190, fill: "#141838", stroke: "#2e3670", "stroke-width": 10 }, gg);
      const arc = (a0, a1, c) => { const p = (a) => [540 + 150 * Math.cos(a * Math.PI / 180), 800 + 150 * Math.sin(a * Math.PI / 180)];
        const [x0, y0] = p(a0), [x1, y1] = p(a1); el("path", { d: `M${x0} ${y0} A150 150 0 0 1 ${x1} ${y1}`, stroke: c, "stroke-width": 26, fill: "none" }, gg); };
      arc(150, 210, "#ff3b55"); arc(212, 270, "#ffd43b"); arc(272, 390, "#39e27a");
      const needle = el("path", { d: "M764 800 L540 660 L776 800Z", fill: "#ffffff" }, gg);
      el("circle", { cx: 540, cy: 800, r: 20, fill: "#ffffff" }, gg);
      txt(gg, 540, 930, "DRUCK", 40, "#dfe2f5");
      gsap.set(needle, { rotation: 60, svgOrigin: "540 800" });
      const sh = el("g", { opacity: 0 }, sv);
      el("rect", { x: 520, y: 590, width: 40, height: 100, fill: "#8f9bc4" }, sh);
      el("path", { d: "M420 710 Q540 650 660 710Z", fill: "#c9cde6" }, sh);
      const P = person(sh, "s03p", 540, 900, 1, { three: false, arms: [150, -150], shirt: "#f2c9a5", pants: "#4da3ff" });
      const jets = []; for (let i = 0; i < 9; i++) jets.push(el("path", { d: `M${452 + i * 22} 720 V850`, stroke: "#4da3ff", "stroke-width": 7, "stroke-dasharray": "26 22", "stroke-linecap": "round" }, sh));
      const steam = []; for (let i = 0; i < 6; i++) steam.push(el("circle", { cx: 390 + i * 60, cy: 800 - (i % 2) * 60, r: 50, fill: "#e6eaf5", opacity: 0 }, sh));
      const gl = at("L5", "gleichzeitig"), br = at("L5", "bricht"), du = at("L6", "Dusche"), heiss = at("L7", "brühend");
      tl.fromTo(gg, { opacity: 0, scale: 0.5, svgOrigin: "540 800" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.2);
      tl.to("#s03-box", { opacity: 1, duration: 0.25 }, gl - 0.4);
      tl.to(needle, { rotation: 40, svgOrigin: "540 800", duration: 0.1, repeat: 5, yoyo: true }, gl);
      tl.to(needle, { rotation: -95, svgOrigin: "540 800", duration: 0.5, ease: "back.out(2)" }, br - 0.1);
      count(tl, "#s03-n", 4, 1, br - 0.1, 0.6, "", " BAR");
      tl.to(gg, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, br + 0.1);
      tl.to(gg, { opacity: 0, filter: "blur(8px)", duration: 0.25 }, du - 0.6);
      tl.to("#s03-box", { opacity: 0, duration: 0.2 }, du - 0.45);
      tl.to("#s03-box2", { opacity: 1, duration: 0.2 }, du - 0.3);
      tl.to(sh, { opacity: 1, duration: 0.3 }, du - 0.3);
      tl.fromTo(jets, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -480 }, duration: 4, ease: "none" }, du - 0.3);
      tl.to(jets, { attr: { stroke: "#ff3b55" }, duration: 0.15 }, heiss - 0.1);
      tl.to("#s03-box2", { borderColor: "#ff3b55", duration: 0.2 }, heiss);
      count(tl, "#s03-n2", 38, 60, heiss - 0.1, 0.5, "", " °C");
      tl.to(steam, { opacity: 0.8, y: -60, duration: 0.6, stagger: 0.05 }, heiss);
      tl.to(P.g, { y: 830, duration: 0.15, yoyo: true, repeat: 3, ease: "power2.out" }, heiss);
      tl.to("#s03p-mouth", { attr: { d: "M-16 -24 q16 -22 32 0" }, duration: 0.1 }, heiss);''' + OUT)

S['s04'] = ('''    #s04-box .num { font-size: 52px; }''',
'''      <div id="s04-box" class="cbox g" style="opacity:0"><div class="lab">KANAL-AUSLASTUNG</div><div id="s04-n" class="num">0 %</div></div>
      <div id="s04-box2" class="cbox r" style="opacity:0"><div class="lab">TRINKWASSER</div><div class="num">IN GEFAHR</div></div>
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
      tl.to(".s04-x", { opacity: 1, duration: 0.15, stagger: 0.15 }, fi + 0.3);
      const gl = el("g", { opacity: 0 }, sv);
      el("path", { d: "M400 620 L680 620 L650 940 L430 940Z", fill: "#dfe5f5", opacity: 0.35 }, gl);
      const liq = el("path", { d: "M412 720 L668 720 L650 930 L432 930Z", fill: "#7a5c34" }, gl);
      txt(gl, 540, 860, "✕", 180, "#ff3b55");
      const ki = at("L9b", "kippt"), mm = at("L9b", "Millionen");
      tl.to(river, { attr: { fill: "#4a3d2a" }, duration: 0.5 }, ki - 0.1);
      tl.to(fishes.map((f) => f.g), { opacity: 0.35, duration: 0.4 }, ki);
      tl.to("#s04-box", { opacity: 0, duration: 0.2 }, mm - 0.4);
      tl.to("#s04-box2", { opacity: 1, duration: 0.2 }, mm - 0.3);
      tl.to(pl.querySelectorAll("ellipse, path"), { opacity: 0.15, duration: 0.3 }, mm - 0.4);
      tl.fromTo(gl, { opacity: 0, scale: 0.5, svgOrigin: "540 800" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, mm - 0.2);
      tl.to(gl, { rotation: 6, svgOrigin: "540 940", duration: 0.08, yoyo: true, repeat: 5 }, mm + 0.4);''' + OUT)

S['s05'] = ('''    #s05-box .num, #s05-box2 .num { font-size: 52px; }''',
'''      <div id="s05-box" class="cbox r" style="opacity:0"><div class="lab">ABWASSER-PEGEL</div><div id="s05-n" class="num">0 CM</div></div>
      <div id="s05-box2" class="cbox r" style="opacity:0"><div class="lab">GESUNDHEIT</div><div class="num">GEFAHR!</div></div>
''' + SVG,
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
      const r = rng(21), rain = el("g", { "data-layout-allow-overlap": "" }, sv), rd = [];
      for (let i = 0; i < 26; i++) { const d = drop(rain, 60 + r() * 960, 560 + r() * 80, 0.14 + r() * 0.08, "#7a5c34"); gsap.set(d, { opacity: 0 }); rd.push(d); }
      const cl = el("clipPath", { id: "s05-clip" }, sv); el("rect", { x: 0, y: 0, width: 1080, height: 1130 }, cl);
      const fg = el("g", { "clip-path": "url(#s05-clip)" }, sv); const F = flood(fg, 1140, "#7a5c34");
      const germ = (x, y, s) => { const g = el("g", { opacity: 0 }, sv); gsap.set(g, { x, y, scale: s, transformOrigin: "0 0" });
        for (let k = 0; k < 8; k++) el("path", { d: "M0 0 L0 -70", stroke: "#39e27a", "stroke-width": 10, "stroke-linecap": "round", transform: `rotate(${k * 45})` }, g);
        el("ellipse", { cx: 0, cy: 0, rx: 58, ry: 44, fill: "#39e27a" }, g); el("circle", { cx: -18, cy: -8, r: 9, fill: "#161a36" }, g); el("circle", { cx: 18, cy: -8, r: 9, fill: "#161a36" }, g);
        el("path", { d: "M-18 18 q18 -12 36 0", stroke: "#161a36", "stroke-width": 6, fill: "none" }, g); return g; };
      const germs = [germ(200, 700, 0.9), germ(540, 640, 1.2), germ(870, 720, 0.8), germ(360, 900, 0.7), germ(740, 920, 0.75)];
      const stink = []; for (let i = 0; i < 5; i++) stink.push(el("path", { d: `M${140 + i * 200} 1000 q30 -40 0 -80 t0 -80 t0 -80`, stroke: "#9be27a", "stroke-width": 12, fill: "none", "stroke-linecap": "round", opacity: 0 }, sv));
      const gd = at("L10", "Gullydeckel"), rg = at("L10", "regnet"), fk = at("L10", "Fäkalien"), l11 = line("L11")[0], ke = at("L11", "Keime"), du = at("L11", "Durchfall"), sti = at("L11", "stinkt");
      tl.fromTo(city, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.fromTo(lights, { opacity: 1 }, { opacity: 0.2, duration: 0.15, repeat: 9, yoyo: true, stagger: 0.05 }, 0.3);
      covers.forEach((c, i) => { tl.to(c, { y: -360 - i * 40, rotation: 300 + i * 90, svgOrigin: `${[200, 540, 880][i]} 1092`, duration: 0.6, ease: "power2.out" }, gd + i * 0.08);
        tl.to(c, { y: 0, opacity: 0, duration: 0.4, ease: "power2.in" }, gd + 0.6 + i * 0.08); });
      tl.fromTo(jets, { opacity: 0, scaleY: 0.1, svgOrigin: "540 1100" }, { opacity: 1, scaleY: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.08 }, gd + 0.02);
      tl.to(jets, { scaleY: 1.15, svgOrigin: "540 1100", duration: 0.12, repeat: 9, yoyo: true }, gd + 0.35);
      rd.forEach((d, i) => tl.set(d, { opacity: 1 }, rg - 0.1 + i * 0.03).to(d, { y: "+=480", duration: 0.7, ease: "power1.in" }, rg - 0.1 + i * 0.03).to(d, { opacity: 0, duration: 0.1 }, rg + 0.6 + i * 0.03));
      tl.to("#s05-box", { opacity: 1, duration: 0.25 }, fk - 0.3);
      tl.to(F, { y: -150, duration: 1.6, ease: "power1.inOut" }, fk - 0.2);
      tl.to(F, { x: -135, duration: 0.6, repeat: 7, yoyo: true, ease: "sine.inOut" }, fk);
      count(tl, "#s05-n", 0, 20, fk - 0.2, 1.6, "", " CM", "power1.inOut");
      germs.forEach((g, i) => tl.fromTo(g, { opacity: 0, scale: 0.1 }, { opacity: 1, scale: [0.9, 1.2, 0.8, 0.7, 0.75][i], duration: 0.35, ease: "back.out(2.4)" }, ke - 0.1 + i * 0.1));
      tl.to(germs, { rotation: 15, duration: 0.25, yoyo: true, repeat: 7 }, ke + 0.6);
      tl.to("#s05-box", { opacity: 0, duration: 0.15 }, du - 0.6);
      tl.fromTo("#s05-box2", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, du - 0.3);
      tl.to(germs, { opacity: 0.25, duration: 0.3 }, sti - 0.4);
      tl.fromTo(stink, { opacity: 0, y: 40 }, { opacity: 0.9, y: 0, duration: 0.5, stagger: 0.08 }, sti - 0.2);
      tl.to(stink, { x: 14, duration: 0.3, yoyo: true, repeat: 5 }, sti + 0.4);''' + OUT)

S['s06'] = ('''    #s06-box .num, #s06-box2 .num { font-size: 44px; }''',
'''      <div id="s06-box" class="cbox b" style="opacity:0"><div class="lab">OHNE SPÜLUNG</div><div id="s06-n" class="num">0</div></div>
      <div id="s06-box2" class="cbox r" style="opacity:0"><div class="lab">FÄKALIEN</div><div id="s06-n2" class="num">0 T</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s06-svg");
      const beach = el("g", {}, sv);
      const sea = el("rect", { x: 0, y: 700, width: 1080, height: 300, fill: "#2f7fe0" }, beach);
      const wave = el("path", { d: "M-40 700 q65 -22 135 0 t135 0 t135 0 t135 0 t135 0 t135 0 t135 0 t135 0 t135 0 V740 H-40Z", fill: "#4da3ff" }, beach);
      el("rect", { x: 0, y: 990, width: 1080, height: 140, fill: "#e8c77a" }, beach);
      const sun = el("circle", { cx: 860, cy: 630, r: 56, fill: "#ffd43b" }, beach);
      const r = rng(11), crowd = el("g", { "data-layout-allow-overlap": "" }, beach), ppl = [];
      const COL = ["#ff4fb0", "#4da3ff", "#39e27a", "#ffd43b", "#ff8a3d"];
      for (let i = 0; i < 60; i++) ppl.push(mini(crowd, 40 + r() * 1000, 900 + r() * 150, COL[i % 5]));
      const whales = [], wg = el("g", { opacity: 0 }, sv);
      for (let i = 0; i < 5; i++) { const g = el("g", {}, wg); const x = 130 + i * 205, y = 800 + (i % 2) * 70;
        el("path", { d: `M${x - 85} ${y} Q${x - 40} ${y - 50} ${x + 50} ${y - 20} L${x + 90} ${y - 50} L${x + 80} ${y} L${x + 95} ${y + 40} L${x + 50} ${y + 15} Q${x - 40} ${y + 45} ${x - 85} ${y}Z`, fill: "#5b7bd6" }, g);
        el("circle", { cx: x - 55, cy: y - 8, r: 6, fill: "#161a36" }, g); whales.push(g); }
      const wl = txt(sv, 540, 660, "= ÜBER 5.000 BLAUWALE", 54, "#ffd43b", { opacity: 0 });
      const vm = at("L12", "vier"), ks = at("L12", "keine"), fl = at("L12b", "Flüsse"), me = at("L12b", "Meer"), t8 = at("L14", "800.000"), bw = at("L14", "schwer");
      tl.fromTo(beach, { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.05);
      tl.to(wave, { x: -135, duration: 0.8, repeat: 13, yoyo: true, ease: "sine.inOut" }, 0.1);
      tl.to("#s06-box", { opacity: 1, duration: 0.25 }, vm - 0.3);
      count(tl, "#s06-n", 0, 4000000000, vm - 0.2, 1.2, "", "", "power3.out");
      ppl.forEach((p, i) => tl.to(p, { opacity: 1, duration: 0.15 }, vm + i * 0.02));
      tl.to("#s06-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, ks);
      ppl.forEach((p, i) => tl.to(p, { y: -150 - (i % 4) * 25, duration: 0.6, ease: "power2.inOut" }, me - 0.3 + (i % 10) * 0.03));
      tl.to("#s06-box", { opacity: 0, duration: 0.2 }, t8 - 0.4);
      tl.to("#s06-box2", { opacity: 1, duration: 0.2 }, t8 - 0.3);
      count(tl, "#s06-n2", 0, 800000, t8 - 0.2, 0.8, "", " T", "power3.out");
      tl.to([sea, wave], { attr: { fill: "#6b5a3a" }, duration: 1.0 }, t8);
      tl.to(crowd, { opacity: 0.3, duration: 0.4 }, bw - 0.6);
      tl.to(sun, { opacity: 0, duration: 0.3 }, bw - 0.4);
      tl.to(wg, { opacity: 1, duration: 0.2 }, bw - 0.4);
      whales.forEach((w, i) => tl.fromTo(w, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, bw - 0.4 + i * 0.1));
      tl.fromTo(wl, { opacity: 0, scale: 0.5, svgOrigin: "540 640" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, bw);
      const l14b = line("L14b")[0], mm = at("L14b", "Millionstel"), l14c = line("L14c")[0], fu = at("L14c", "Flut"), fk = at("L14c", "Fäkalien"), br = at("L14c", "Brunnenwasser");
      const sand = beach.querySelector('rect[fill="#e8c77a"]');
      const ruler = el("g", { opacity: 0 }, sv);
      el("rect", { x: 900, y: 560, width: 90, height: 420, rx: 12, fill: "#dfe5f5" }, ruler);
      for (let k = 0; k < 9; k++) el("path", { d: `M900 ${590 + k * 45} h${k % 2 ? 26 : 46}`, stroke: "#161a36", "stroke-width": 6 }, ruler);
      const tick = el("path", { d: "M870 770 l-34 -18 v36Z", fill: "#39e27a" }, ruler);
      const tiny = txt(sv, 450, 640, "+ 0,000005 MM", 70, "#39e27a", { opacity: 0 });
      const wv = el("path", { d: "M1180 990 q-120 -260 -320 -200 q-160 50 -260 -10 q-140 -80 -300 30 q-120 80 -320 40 V1130 H1180Z", fill: "#6b5a3a", opacity: 0 }, sv);
      const well = el("g", { opacity: 0 }, sv);
      el("rect", { x: 440, y: 860, width: 200, height: 110, rx: 10, fill: "#8f9bc4" }, well);
      el("path", { d: "M420 860 L540 780 L660 860Z", fill: "#ff8a3d" }, well);
      el("ellipse", { cx: 540, cy: 860, rx: 90, ry: 18, fill: "#6b5a3a" }, well);
      txt(well, 540, 960, "✕", 120, "#ff3b55");
      tl.to([wg, wl, crowd], { opacity: 0, duration: 0.25 }, l14b - 0.3);
      tl.to("#s06-box2", { opacity: 0, duration: 0.2 }, l14b - 0.2);
      tl.fromTo(ruler, { opacity: 0, x: 100 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.8)" }, l14b);
      tl.to(tick, { y: -4, duration: 0.6, ease: "power2.out" }, mm);
      tl.fromTo(tiny, { opacity: 0, scale: 0.5, svgOrigin: "450 620" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, mm);
      tl.to([ruler, tiny], { opacity: 0, duration: 0.25 }, l14c - 0.2);
      tl.fromTo(wv, { opacity: 1, x: 1200 }, { x: 0, duration: 1.2, ease: "power2.out" }, fu - 0.1);
      tl.to(sand, { attr: { fill: "#8a6a3c" }, duration: 0.6 }, fk - 0.2);
      tl.to(wv, { y: -40, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut" }, fu + 1.1);
      tl.fromTo(well, { opacity: 0, scale: 0.4, svgOrigin: "540 920" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }, br - 0.3);
      tl.to(well, { x: 8, duration: 0.04, repeat: 7, yoyo: true }, br + 0.2);''' + OUT)

S['s07'] = ('''    .s07-c { position: absolute; top: 620px; width: 290px; height: 330px; border-radius: 24px; background: rgba(20,24,56,.92); border: 4px solid #ff3b55; box-shadow: 0 0 30px rgba(255,59,85,.3); }
    .s07-c b { position: absolute; left: 0; right: 0; bottom: 22px; text-align: center; font: 900 34px Inter, sans-serif; color: #fff; }
    #s07-c1 { left: 60px; } #s07-c2 { left: 395px; } #s07-c3 { left: 730px; }''',
'''      <div id="s07-c1" class="s07-c abs"><b>BADEVERBOT</b></div><div id="s07-c2" class="s07-c abs"><b>FISCHFANG</b></div><div id="s07-c3" class="s07-c abs"><b>URLAUB</b></div>
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
      const bv = at("L15", "Badeverbot"), ff = at("L15", "Fischfang"), ur = at("L15", "Urlaub");
      [["#s07-c1", g1, bv], ["#s07-c2", g2, ff], ["#s07-c3", g3, ur]].forEach(([c, g, t]) => {
        tl.fromTo(c, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, t - 0.15);
        tl.fromTo(g, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, t - 0.15); });
      tl.fromTo([x2, x3], { opacity: 0 }, { opacity: 1, duration: 0.1 }, ff + 0.3);
      tl.set(x3, { opacity: 0 }, ff + 0.3); tl.to(x3, { opacity: 1, duration: 0.1 }, ur + 0.3);
      tl.to(F.g, { rotation: 180, svgOrigin: "540 760", duration: 0.4 }, ff + 0.3);''' + OUT)

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
      tl.to(T.g, { rotation: 6, svgOrigin: "540 950", duration: 0.08, repeat: 5, yoyo: true }, du - 0.1);
      tl.fromTo("#s08-b1", { opacity: 0, y: 80, rotation: -6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, na - 0.15);
      tl.fromTo("#s08-b2", { opacity: 0, y: 80, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, se - 0.15);
      tl.to(".s08-b", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 3, stagger: 0.3, ease: "sine.inOut" }, ko - 0.3);
      tl.to(".s08-b", { opacity: 0, y: 60, duration: 0.25, ease: "power3.in" }, l18 - 0.2);
      tl.fromTo("#s08-f", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, fo - 0.1);
      tl.to("#s08-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);
      tl.to(T.g, { x: 550, duration: 0.04, repeat: 15, yoyo: true }, ex - 0.6);
      tl.to(T.water, { attr: { fill: "#ff3b55" }, duration: 0.2 }, ex - 0.3);
      tl.fromTo(boom, { opacity: 0, scale: 0.2, svgOrigin: "540 760" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, ex);
      tl.fromTo(boom2, { opacity: 0, scale: 0.2, svgOrigin: "540 760" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, ex + 0.05);
      tl.to(glow, { opacity: 0, duration: 0.2 }, ex);
      tl.to([boom, boom2], { rotation: 15, svgOrigin: "540 760", duration: 0.3, yoyo: true, repeat: 5 }, ex + 0.3);
      tl.to(T.g, { y: 800, duration: 0.15, yoyo: true, repeat: 3, ease: "power2.out" }, ab);
      const en = at("L18", "entleerst");
      tl.to(T.g, { x: 552, duration: 0.04, repeat: 11, yoyo: true }, en);
      tl.to([boom, boom2], { scale: 1.2, svgOrigin: "540 760", duration: 0.15, yoyo: true, repeat: 3 }, en);''')


S['s03b'] = ('''    #s03b-box .num { font-size: 52px; }''',
'''      <div id="s03b-box" class="cbox b" style="opacity:0"><div class="lab">DUSCHE</div><div id="s03b-n" class="num">38 °C</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s03b-svg");
      const sys = el("g", {}, sv);
      const boiler = el("g", {}, sys); el("rect", { x: 830, y: 600, width: 200, height: 170, rx: 24, fill: "#c9cde6" }, boiler);
      txt(boiler, 930, 700, "BOILER", 40, "#161a36"); el("circle", { cx: 930, cy: 740, r: 12, fill: "#ff3b55" }, boiler);
      const cp = el("rect", { x: 40, y: 800, width: 470, height: 50, rx: 25, fill: "#4da3ff" }, sys);
      const hp = el("rect", { x: 570, y: 800, width: 360, height: 50, rx: 25, fill: "#ff3b55" }, sys);
      el("rect", { x: 905, y: 760, width: 50, height: 70, fill: "#ff3b55" }, sys);
      const cf = el("path", { d: "M60 825 H500", stroke: "#cfe8ff", "stroke-width": 10, "stroke-dasharray": "30 26" }, sys);
      const hf = el("path", { d: "M920 825 H580", stroke: "#ffd0d6", "stroke-width": 10, "stroke-dasharray": "30 26" }, sys);
      const out = el("rect", { x: 515, y: 600, width: 50, height: 230, fill: "#a56bff" }, sys);
      const mix = el("circle", { cx: 540, cy: 825, r: 64, fill: "#2e3670", stroke: "#dfe2f5", "stroke-width": 8 }, sys);
      txt(sys, 540, 838, "MIX", 36, "#ffffff");
      el("path", { d: "M440 600 Q540 540 640 600Z", fill: "#c9cde6" }, sys);
      const jets = []; for (let i = 0; i < 7; i++) jets.push(el("path", { d: `M${474 + i * 22} 610 V720`, stroke: "#a56bff", "stroke-width": 7, "stroke-dasharray": "22 18", "stroke-linecap": "round" }, sys));
      const kl = txt(sys, 250, 920, "KALT", 52, "#4da3ff"), hl = txt(sys, 760, 920, "HEISS", 52, "#ff3b55");
      const xc = txt(sys, 270, 850, "✕", 150, "#ffd43b", { opacity: 0 });
      const steam = []; for (let i = 0; i < 5; i++) steam.push(el("circle", { cx: 440 + i * 50, cy: 720 - (i % 2) * 40, r: 40, fill: "#e6eaf5", opacity: 0 }, sys));
      const mi = at("L7b", "mischt"), ka = at("L7b", "kaltes"), he = at("L7b", "heißes"), kw = at("L7c", "kalte"), hb = at("L7c", "heißes"), g60 = at("L7c", "60");
      tl.fromTo(sys, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.to("#s03b-box", { opacity: 1, duration: 0.25 }, 0.3);
      tl.fromTo([cf, hf], { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -560 }, duration: 4, ease: "none" }, 0.1);
      tl.fromTo(jets, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -400 }, duration: 8, ease: "none" }, 0.1);
      tl.to(mix, { scale: 1.2, svgOrigin: "540 825", duration: 0.15, yoyo: true, repeat: 3 }, mi);
      tl.fromTo(kl, { scale: 1 }, { scale: 1.3, svgOrigin: "250 905", duration: 0.15, yoyo: true, repeat: 1 }, ka);
      tl.fromTo(hl, { scale: 1 }, { scale: 1.3, svgOrigin: "760 905", duration: 0.15, yoyo: true, repeat: 1 }, he);
      tl.to(cp, { attr: { fill: "#2a3170" }, duration: 0.3 }, kw);
      tl.to(cf, { opacity: 0, duration: 0.3 }, kw);
      tl.fromTo(xc, { opacity: 0, scale: 2, svgOrigin: "270 800" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, kw);
      tl.to(sys, { x: 8, duration: 0.04, repeat: 5, yoyo: true }, kw);
      tl.to([out, ...jets], { attr: { fill: "#ff3b55", stroke: "#ff3b55" }, duration: 0.4 }, hb - 0.2);
      tl.to(hf, { attr: { "stroke-dashoffset": -1400 }, duration: 2, ease: "none" }, hb);
      tl.to("#s03b-box", { borderColor: "#ff3b55", duration: 0.2 }, g60 - 0.3);
      count(tl, "#s03b-n", 38, 60, g60 - 0.3, 0.6, "", " °C");
      tl.to(steam, { opacity: 0.8, y: -60, duration: 0.6, stagger: 0.05 }, g60);
      tl.to("#s03b-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, g60 + 0.3);''' + OUT)


S['s07b'] = ('''    #s07b-box .num { font-size: 50px; }
    .s07b-p { position: absolute; top: 600px; width: 450px; height: 470px; border-radius: 26px; background: rgba(20,24,56,.94); text-align: center; opacity: 0; }
    .s07b-p b { position: absolute; left: 0; right: 0; top: 290px; font: 900 40px/1.1 Inter, sans-serif; color: #fff; }
    #s07b-p1 { left: 50px; border: 5px solid #39e27a; } #s07b-p2 { left: 580px; border: 5px solid #ff3b55; box-shadow: 0 0 40px rgba(255,59,85,.4); }''',
'''      <div id="s07b-box" class="cbox r" style="opacity:0"><div class="lab">TOTE PRO JAHR · HEUTE</div><div id="s07b-n" class="num">0</div></div>
      <div id="s07b-p1" class="s07b-p"><b>DURCHS<br>SPÜLEN</b></div><div id="s07b-p2" class="s07b-p"><b>DRECKIGES<br>WASSER</b></div>
''' + SVG,
'''      const sv = document.querySelector("#s07b-svg");
      const q = txt(sv, 540, 900, "?", 300, "#ff3b55", { opacity: 0 });
      const ok = el("g", { opacity: 0 }, sv); el("circle", { cx: 275, cy: 770, r: 100, fill: "#39e27a" }, ok);
      el("path", { d: "M225 772 L262 810 L330 735", stroke: "#0b0e22", "stroke-width": 24, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, ok);
      const kaum = txt(sv, 275, 1052, "KAUM", 50, "#39e27a", { opacity: 0 });
      const sk = el("g", { opacity: 0 }, sv);
      el("circle", { cx: 805, cy: 750, r: 95, fill: "#f3f1ea" }, sk); el("rect", { x: 750, y: 800, width: 110, height: 70, rx: 18, fill: "#f3f1ea" }, sk);
      el("circle", { cx: 770, cy: 750, r: 26, fill: "#161a36" }, sk); el("circle", { cx: 840, cy: 750, r: 26, fill: "#161a36" }, sk);
      el("path", { d: "M805 785 l-14 26 h28Z", fill: "#161a36" }, sk);
      [775, 805, 835].forEach((x) => el("rect", { x: x - 6, y: 835, width: 12, height: 30, fill: "#161a36" }, sk));
      const up = txt(sv, 805, 1052, "▲ MEHR", 56, "#ff3b55", { opacity: 0 });
      const st = at("L16b", "Sterben"), l16c = line("L16c")[0], ka = at("L16c", "kaum"), n5 = at("L16c", "500.000"), dm = at("L16d", "deutlich");
      tl.fromTo(q, { opacity: 0, scale: 0.4, svgOrigin: "540 800" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, st - 0.2);
      tl.to(q, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, st + 0.2);
      tl.to(q, { opacity: 0, duration: 0.2 }, l16c - 0.2);
      tl.fromTo("#s07b-p1", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, l16c - 0.05);
      tl.fromTo(ok, { opacity: 0, scale: 0.3, svgOrigin: "275 770" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }, ka - 0.1);
      tl.to(kaum, { opacity: 1, duration: 0.2 }, ka);
      tl.fromTo("#s07b-p2", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, n5 - 1.2);
      tl.fromTo(sk, { opacity: 0, scale: 0.3, svgOrigin: "805 790" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }, n5 - 0.9);
      tl.to("#s07b-box", { opacity: 1, duration: 0.25 }, n5 - 0.3);
      count(tl, "#s07b-n", 0, 500000, n5 - 0.2, 1.0, "", "", "power3.out");
      tl.fromTo(up, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, dm - 0.1);
      tl.to(sk, { x: 8, duration: 0.04, repeat: 7, yoyo: true }, dm);
      tl.to("#s07b-box", { scale: 1.14, duration: 0.12, yoyo: true, repeat: 1 }, dm);''' + OUT)


S['s07c'] = ('''    .s07c-k { position: absolute; left: 90px; width: 900px; border-radius: 28px; background: rgba(13,16,38,.94); text-align: center; opacity: 0; }
    .s07c-k .n { font: 900 150px/1 Inter, sans-serif; letter-spacing: -.02em; }
    .s07c-k .t { margin-top: 12px; font: 700 36px/1.2 "Space Mono", monospace; letter-spacing: .1em; color: #dfe2f5; }
    #s07c-k1 { top: 600px; height: 340px; padding-top: 50px; box-sizing: border-box; border: 5px solid #ffd43b; box-shadow: 0 0 50px rgba(255,212,59,.35); }
    #s07c-k1 .n { color: #ffd43b; }
    #s07c-k2 { top: 590px; height: 420px; padding-top: 46px; box-sizing: border-box; border: 6px solid #ff4fb0; box-shadow: 0 0 60px rgba(255,79,176,.5); overflow: hidden; }
    #s07c-k2 .n { color: #ff4fb0; font-size: 140px; }
    #s07c-k2 .z { position: absolute; left: 0; top: 330px; white-space: nowrap; font: 900 56px/1 Inter, sans-serif; color: #39e27a; opacity: .8; }''',
'''      <div id="s07c-k1" class="s07c-k"><div id="s07c-n1" class="n">0</div><div class="t">SPÜLUNGEN PRO LEBEN</div></div>
      <div id="s07c-q" class="abs" style="left:340px;top:600px;width:400px;height:400px;border-radius:50%;background:rgba(13,16,38,.94);border:6px solid #ff4fb0;box-shadow:0 0 60px rgba(255,79,176,.5);text-align:center;font:900 300px/390px Inter,sans-serif;color:#ff4fb0;opacity:0">?</div>
      <div id="s07c-k2" class="s07c-k"><div class="n">0,000…%</div><div class="t">17 MILLIARDEN NULLEN</div><div id="s07c-z" class="z">0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000</div></div>''',
'''      const n14 = at("L16e", "140.000"), l16f = line("L16f")[0], pr = at("L16f", "null"), nu = at("L16f", "Nullen");
      tl.fromTo("#s07c-k1", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 0.1);
      count(tl, "#s07c-n1", 0, 140000, n14 - 0.6, 1.0, "", "", "power3.out");
      tl.to("#s07c-k1", { scale: 1.08, duration: 0.12, yoyo: true, repeat: 1 }, n14 + 0.4);
      tl.to("#s07c-k1", { opacity: 0, y: -60, filter: "blur(8px)", duration: 0.25 }, l16f - 0.2);
      tl.fromTo("#s07c-q", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }, l16f);
      tl.to("#s07c-q", { rotation: 12, duration: 0.15, yoyo: true, repeat: 5 }, l16f + 0.5);
      tl.to("#s07c-q", { opacity: 0, scale: 0.5, duration: 0.2 }, pr - 0.4);
      tl.fromTo("#s07c-k2", { opacity: 0, scale: 0.4, rotation: -6 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2.4)" }, pr - 0.25);
      tl.to("#s07c-k2", { x: 10, duration: 0.04, repeat: 7, yoyo: true }, pr + 0.3);
      tl.fromTo("#s07c-z", { x: 0 }, { x: -1500, duration: 4, ease: "none" }, pr - 0.2);
      tl.to("#s07c-k2", { scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }, nu);''' + OUT)

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
