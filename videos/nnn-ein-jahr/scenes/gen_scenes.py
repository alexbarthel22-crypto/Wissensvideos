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

GEO = '{ hood: "#e8a83a", arm: "#c98c22", hair: "#e0b050", glasses: true, label: "G" }'

S['s01'] = ('''    #s01-t { left: 0; width: 1080px; top: 220px; text-align: center; }
    #s01-t .a { font: 900 150px/0.95 Inter, sans-serif; color: #ff4fb0; text-shadow: 0 0 50px rgba(255,79,176,.95), 0 8px 30px rgba(0,0,0,.7); }
    #s01-t .b { position: relative; display: inline-block; font: 900 110px/1.05 Inter, sans-serif; color: #fff; text-shadow: 0 8px 30px rgba(0,0,0,.8); }
    #s01-t .b s { position: absolute; left: -10px; right: -10px; top: 52px; height: 14px; border-radius: 7px; background: #ff2d4b; }
    #s01-j { left: 600px; top: 410px; font: 700 120px "Caveat", "Comic Sans MS", cursive; color: #ffd43b; transform: rotate(-10deg); text-shadow: 0 0 30px rgba(255,212,59,.8), 0 6px 20px rgba(0,0,0,.8); }
    #s01-bd { left: 40px; top: 560px; width: 680px; height: 290px; border-radius: 18px; background: #0b1a3a; border: 8px solid #3a4a6e; box-shadow: 0 20px 60px rgba(0,0,0,.6); font-family: "Space Mono", monospace; }
    #s01-bd .h { height: 56px; background: #1f3a7a; color: #fff; font: 700 30px/56px "Space Mono", monospace; padding-left: 24px; letter-spacing: .1em; }
    #s01-bd .r { position: absolute; left: 22px; right: 22px; font: 700 33px/60px "Space Mono", monospace; color: #ffd43b; white-space: nowrap; }
    #s01-bd .r i { font-style: normal; color: #ff3b55; }
    #s01-big { left: 0; width: 1080px; top: 610px; text-align: center; font: 900 190px/1 Inter, sans-serif; color: #ffd43b; opacity: 0; text-shadow: 0 0 60px rgba(255,212,59,.9); }
    #s01-big small { display: block; font: 900 60px Inter, sans-serif; color: #fff; letter-spacing: .2em; }
    #s01-tag { left: 560px; top: 600px; padding: 10px 22px; border-radius: 14px; background: rgba(255,255,255,.96); color: #22283f; font: 800 46px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    #s01-ok { left: 0; width: 760px; top: 600px; text-align: center; font: 900 120px Inter, sans-serif; color: #ffd43b; opacity: 0; text-shadow: 0 0 40px rgba(255,212,59,.9); }
    #s01-ok small { display: block; font: 900 110px Inter, sans-serif; color: #ff3b55; }
    #s01-flash { left: 0; top: 0; width: 1080px; height: 1920px; background: #fff; opacity: 0; }''',
SVG + '''
      <div id="s01-t" class="abs" data-layout-allow-overlap><div class="a">NO NUT</div><div class="b">NOVEMBER<s></s></div></div>
      <div id="s01-j" class="abs" data-layout-allow-overlap>JAHR!</div>
      <div id="s01-bd" class="abs"><div class="h">ABFAHRT · GLEIS 1</div>
        <div class="r" style="top:80px">00:00  NO NUT NOVEMBER</div>
        <div class="r" style="top:140px">DAUER  <i>+335 TAGE</i></div>
        <div class="r" style="top:200px">STATUS <i>VERLÄNGERT</i></div></div>
      <div id="s01-big" class="abs"><span id="s01-n">30</span><small>TAGE</small></div>
      <div id="s01-tag" class="abs">Georg · 18</div>
      <div id="s01-ok" class="abs">OKTOBER<small>???</small></div>
      <div id="s01-flash" class="abs"></div>''',
'''      const sv = document.querySelector("#s01-svg"); sky(sv, "s01g", "#1b2346", "#0b0f22");
      el("rect", { x: 0, y: 1130, width: 1080, height: 790, fill: "#4a4f63" }, sv); el("rect", { x: 0, y: 1130, width: 1080, height: 22, fill: "#ffd43b" }, sv);
      for (let k = 0; k < 2; k++) el("rect", { x: 100 + k * 760, y: 380, width: 30, height: 760, fill: "#2f3550" }, sv);
      const G = finn(sv, 860, 1150, 2.1, ''' + GEO + ''');
      const cs = el("g", {}, sv); el("rect", { x: 950, y: 1060, width: 90, height: 80, rx: 10, fill: "#7a4ad6" }, cs); el("rect", { x: 980, y: 1040, width: 30, height: 24, rx: 6, fill: "none", stroke: "#5a3ab0", "stroke-width": 6 }, cs);
      const ve = at("L1", "verlängert"), l2 = line("L2")[0], ja = at("L2", "Jahr"), d3 = at("L2", "365"), ka = at("L2", "Kronjuwelen"), l3 = line("L3")[0], ge = at("L3", "Georg"), ok = at("L3b", "Oktober"), ni = at("L3b", "niemand");
      tl.fromTo("#s01-j", { scale: 1.3 }, { scale: 1, duration: 0.5, ease: "back.out(2)" }, 0);
      tl.to("#s01-bd .r i", { opacity: 0.3, duration: 0.25, yoyo: true, repeat: 7 }, 0.2);
      tl.fromTo("#s01-flash", { opacity: 0.85 }, { opacity: 0, duration: 0.4, immediateRender: false }, ve - 0.05);
      tl.to(["#s01-t", "#s01-bd", "#s01-j"], { x: 12, duration: 0.04, repeat: 9, yoyo: true }, ve);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, ve);
      tl.to("#s01-bd", { opacity: 0, duration: 0.25 }, ja - 0.3);
      tl.fromTo("#s01-big", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ja - 0.1);
      count(tl, "#s01-n", 30, 365, ja, d3 - ja + 0.4, "", "", "power2.in");
      tl.to("#s01-big", { scale: 1.12, duration: 0.15, yoyo: true, repeat: 3 }, d3 + 0.4);
      tl.to(sv, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, ka);
      tl.to(["#s01-big", "#s01-t", "#s01-j"], { opacity: 0, duration: 0.25 }, l3 - 0.25);
      tl.fromTo("#s01-tag", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ge);
      armsUp(tl, G, ge + 0.3, 0.3, 160); tl.to(G.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, ge + 0.3);
      tl.to("#s01-tag", { opacity: 0, duration: 0.2 }, ok - 0.3); armsDown(tl, G, ok - 0.3);
      tl.fromTo("#s01-ok", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }, ok - 0.1);
      tl.to("#s01-ok small", { x: 10, duration: 0.05, repeat: 9, yoyo: true }, ni);''' + OUT)

S['s02'] = (CHIP + '''
    #s02-v { left: 0; right: 0; margin: 0 auto; top: 470px; width: fit-content; padding: 14px 40px; border: 10px solid #ff2d4b; border-radius: 20px; color: #ff2d4b; background: rgba(255,255,255,.92); font: 900 86px Inter, sans-serif; letter-spacing: .06em; opacity: 0; transform: rotate(-7deg); }
    #s02-v small { display: block; font: 800 30px Inter, sans-serif; color: #22283f; letter-spacing: .1em; text-align: center; }''',
SVG + '''
      <div id="s02-v" class="abs" data-layout-allow-overlap>VERBOTEN<small>BIS 1. NOVEMBER</small></div>''',
'''      const sv = document.querySelector("#s02-svg"); sky(sv, "s02g", "#172048", "#0a0e26");
      el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#dfe8f4" }, sv);
      [[60, "#8a5a33"], [400, "#9a6a3d"], [740, "#8a5a33"]].forEach(([x, c]) => { const h = el("g", {}, sv); el("rect", { x, y: 760, width: 300, height: 300, fill: c }, h);
        el("path", { d: `M${x - 30} 770 L${x + 150} 640 L${x + 330} 770Z`, fill: "#eef4fb" }, h); el("rect", { x: x + 20, y: 840, width: 260, height: 90, fill: "#ffd78a" }, h); });
      const bulbs = []; for (let i = 0; i < 22; i++) bulbs.push(el("circle", { cx: 30 + i * 48, cy: 600 + Math.sin(i * 0.6) * 20, r: 9, fill: ["#ffd43b", "#ff4fb0", "#39e27a", "#4da3ff"][i % 4] }, sv));
      const sf = snowfall(sv, 60, 5, 300, 1200);
      const T = woman(sv, 330, 1150, 2.3, "#d0343f", "#5a3a22");
      const G = finn(sv, 720, 1150, 2.3, ''' + GEO + ''');
      const wurst = el("g", { opacity: 0 }, sv); el("rect", { x: 430, y: 880, width: 150, height: 40, rx: 20, fill: "#a0522d" }, wurst); el("rect", { x: 420, y: 895, width: 170, height: 22, rx: 11, fill: "#f2d6a2", opacity: 0.9 }, wurst);
      const sweat = [0, 1, 2].map((k) => el("circle", { cx: 690 + k * 30, cy: 760, r: 8, fill: "#9fd8ff", opacity: 0 }, sv));
      fall(tl, sf, C.__dur);
      tl.to(bulbs, { opacity: 0.4, duration: 0.3, yoyo: true, repeat: 15, stagger: 0.05 }, 0);
      const br = at("L5", "Bratwurst"), sc = at("L5", "schwitzt"), wu = at("L6", "Wurst"), vb = at("L6", "verboten");
      tl.to(T.aR, { rotation: -80, svgOrigin: "35 -126", duration: 0.3 }, br - 0.3);
      tl.fromTo(wurst, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, br - 0.1);
      tl.to(wurst, { x: 160, duration: 0.4 }, sc - 0.4);
      tl.to(sweat, { opacity: 1, y: 40, duration: 0.5, stagger: 0.15 }, sc);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, sc);
      tl.to(wurst, { scale: 1.6, svgOrigin: "665 900", duration: 0.3 }, wu - 0.1);
      tl.fromTo("#s02-v", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, vb - 0.15);
      tl.to(sv, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, vb + 0.05);''' + OUT)

S['s03'] = (CHIP, SVG + '''
      <div id="s03-ek" class="chip" style="left:600px;top:500px;color:#2b7cff">EISKALT ❄</div>''',
'''      const sv = document.querySelector("#s03-svg"); sky(sv, "s03g", "#ffb3d1", "#d96a9c");
      el("rect", { x: 0, y: 1100, width: 1080, height: 820, fill: "#8a4a62" }, sv);
      const pairs = [[180, 760], [540, 700], [900, 760]].map(([x, y], i) => { const g = el("g", { opacity: 0 }, sv);
        el("ellipse", { cx: x, cy: y + 70, rx: 90, ry: 18, fill: "#fff" }, g); tiny(g, x - 40, y + 40, "#ff4fb0", 1.6); tiny(g, x + 40, y + 40, "#4da3ff", 1.6);
        txt(g, x, y - 30, "♥", 56, "#ff2d6b"); return g; });
      el("ellipse", { cx: 540, cy: 1080, rx: 160, ry: 26, fill: "#fff" }, sv);
      const G = finn(sv, 540, 1180, 2.2, ''' + GEO + ''');
      const gl = el("g", { opacity: 0 }, sv); el("path", { d: "M600 960 L700 960 L690 1070 L610 1070Z", fill: "#9fd8ff", stroke: "#e8f6ff", "stroke-width": 5 }, gl);
      el("rect", { x: 620, y: 990, width: 26, height: 26, rx: 4, fill: "#fff", opacity: 0.8 }, gl); el("rect", { x: 652, y: 1010, width: 26, height: 26, rx: 4, fill: "#fff", opacity: 0.8 }, gl);
      const frost = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#bfe6ff", opacity: 0 }, sv);
      const pa = at("L7", "Pärchen"), ei = at("L8", "Eistee"), ek = at("L8", "Eiskalt"), si = at("L8", "Sicherheit");
      pairs.forEach((p, i) => { tl.fromTo(p, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, pa - 0.2 + i * 0.15); tl.to(p, { y: -10, duration: 0.4, yoyo: true, repeat: 7 }, pa + 0.4 + i * 0.1); });
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -153 6 -149" }, duration: 0.2 }, pa);
      tl.fromTo(gl, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, ei - 0.1);
      tl.fromTo("#s03-ek", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, ek - 0.05);
      tl.to(frost, { opacity: 0.35, duration: 0.4 }, ek);
      tl.to(G.g, { x: 548, duration: 0.04, repeat: 30, yoyo: true }, ek + 0.1);''' + OUT)

S['s04'] = (CHIP + '''
    #s04-n { left: 0; width: 1080px; top: 470px; text-align: center; font: 900 220px/1 Inter, sans-serif; color: #39e27a; opacity: 0; text-shadow: 0 0 60px rgba(57,226,122,.9); }''',
SVG + '''
      <div id="s04-n" class="abs">1,3</div>
      <div id="s04-dt" class="chip" style="left:120px;top:540px;background:#ff3b55;color:#fff">DROGENTEST?</div>''',
'''      const sv = document.querySelector("#s04-svg"); sky(sv, "s04g", "#d8dde8", "#b4bccb");
      el("rect", { x: 0, y: 1080, width: 1080, height: 840, fill: "#7d6a55" }, sv);
      const desks = []; for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) { const x = 140 + c * 270, y = 700 + r * 170; if (r === 1 && c === 1) continue;
        const g = el("g", {}, sv); el("rect", { x: x - 80, y, width: 160, height: 14, fill: "#c79a5b" }, g); tiny(g, x, y - 4, ["#4da3ff", "#ff6a3d", "#39e27a", "#ffd43b"][(r + c) % 4], 1.5); desks.push(g); }
      const G = finn(sv, 410, 1190, 2.2, ''' + GEO + ''');
      el("rect", { x: 280, y: 1020, width: 260, height: 26, rx: 6, fill: "#c79a5b" }, sv);
      const pap = []; const rp = rng(8); for (let i = 0; i < 10; i++) pap.push(el("rect", { x: 420, y: 990, width: 60, height: 80, fill: "#fff", stroke: "#cfd5e2", "stroke-width": 2, opacity: 0 }, sv));
      const par = el("g", { opacity: 0 }, sv); const Mo = woman(par, 700, 1180, 2.1, "#3aa37a"); const Fa = finn(par, 900, 1180, 2.2, { hood: "#4a5a7a", arm: "#3a4a6a", hair: "#7a7a7a", label: "" });
      const ma = at("L9", "Maschine"), l10 = line("L10")[0], dr = at("L11", "Drogen"), l11 = line("L11")[0];
      tl.to(G.aR, { rotation: -40, svgOrigin: "37 -126", duration: 0.06, yoyo: true, repeat: 40 }, 1.0);
      pap.forEach((p, i) => tl.fromTo(p, { opacity: 1, x: 0, y: 0, rotation: 0 }, { x: 300 + rp() * 300, y: -300 - rp() * 300, rotation: rp() * 360, svgOrigin: "450 1030", opacity: 0, duration: 0.8, ease: "power2.out", immediateRender: false }, ma - 1.2 + i * 0.15));
      tl.fromTo("#s04-n", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, l10 + 0.6);
      armsUp(tl, G, l10 + 0.7, 0.3, 160);
      tl.to("#s04-n", { opacity: 0, y: -60, duration: 0.25 }, l11 - 0.2); tl.to(desks, { opacity: 0, duration: 0.3 }, l11 - 0.2);
      tl.fromTo(par, { opacity: 0, x: 200 }, { opacity: 1, x: 0, duration: 0.35 }, l11 - 0.1);
      tl.fromTo("#s04-dt", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, dr - 0.1);
      armsDown(tl, G, dr); tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, dr);''' + OUT)

S['s05'] = (CHIP, SVG + '''
      <div id="s05-sw" class="chip" style="left:640px;top:480px">⏱ <i>2:00</i></div>''',
'''      const sv = document.querySelector("#s05-svg"); sky(sv, "s05g", "#5fc0ff", "#9fdcff");
      const sun = el("circle", { cx: 880, cy: 520, r: 80, fill: "#ffd43b" }, sv);
      el("rect", { x: 0, y: 760, width: 1080, height: 160, fill: "#f2e3c2" }, sv);
      const towels = [[120, "#ff4fb0"], [420, "#ffd43b"], [740, "#39e27a"]].map(([x, c]) => { const g = el("g", {}, sv); el("rect", { x, y: 790, width: 200, height: 70, rx: 10, fill: c }, g); el("ellipse", { cx: x + 100, cy: 800, rx: 70, ry: 18, fill: "#f2cba5" }, g); return g; });
      const pool = el("g", {}, sv); el("rect", { x: 0, y: 920, width: 1080, height: 1000, fill: "#2fa8e8" }, pool);
      const waves = []; for (let k = 0; k < 5; k++) waves.push(el("path", { d: `M0 ${960 + k * 50} q60 -14 120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0`, stroke: "#bfe9ff", "stroke-width": 5, fill: "none", opacity: 0.6 }, pool));
      const G = finn(sv, 540, 1180, 2.2, ''' + GEO + ''');
      const water = el("rect", { x: 0, y: 1000, width: 1080, height: 920, fill: "#2fa8e8", opacity: 0.85 }, sv);
      const bub = []; for (let i = 0; i < 10; i++) bub.push(el("circle", { cx: 520 + (i % 3) * 20, cy: 1000, r: 6 + (i % 3) * 3, fill: "none", stroke: "#e8f8ff", "stroke-width": 3, opacity: 0 }, sv));
      const un = at("L13", "unter"), zw = at("L14", "zwei");
      waves.forEach((w, i) => tl.to(w, { x: -120, duration: 2, repeat: Math.ceil(C.__dur / 2), ease: "none" }, 0));
      tl.to(sun, { scale: 1.1, svgOrigin: "880 520", duration: 0.8, yoyo: true, repeat: 8 }, 0);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.2 }, 1.5);
      tl.to(G.g, { y: 1600, duration: 0.6, ease: "power2.in" }, un - 0.1);
      bub.forEach((b, i) => tl.fromTo(b, { opacity: 0.9, y: 0 }, { opacity: 0, y: -260, duration: 0.9, repeat: 4, ease: "power1.out", immediateRender: false }, un + 0.4 + i * 0.18));
      tl.fromTo("#s05-sw", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, zw - 0.1);''' + OUT)

S['s06'] = (CHIP + '''
    #s06-h { left: 0; width: 1080px; top: 470px; text-align: center; font: 900 96px Inter, sans-serif; color: #fff; opacity: 0; text-shadow: 0 0 40px rgba(255,79,176,.9); }''',
SVG + '''
      <div id="s06-h" class="abs">72 STUNDEN</div>
      <div id="s06-rb" class="chip" style="left:560px;top:600px"><b>ROBOTER?</b></div>''',
'''      const sv = document.querySelector("#s06-svg"); sky(sv, "s06g", "#12082a", "#05030f");
      const beams = [0, 1, 2, 3, 4].map((k) => el("path", { d: `M${140 + k * 200} 380 L${40 + k * 200} 1140 L${240 + k * 200} 1140Z`, fill: ["#ff4fb0", "#4da3ff", "#39e27a", "#ffd43b", "#a06bff"][k], opacity: 0.18 }, sv));
      el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#120a24" }, sv);
      const crowd = []; for (let i = 0; i < 16; i++) crowd.push(tiny(sv, 40 + i * 68, 1180 + (i % 2) * 20, "#2a1f4f", 1.8));
      const G = finn(sv, 400, 1150, 2.3, ''' + GEO + ''');
      const Sec = finn(sv, 820, 1150, 2.8, { hood: "#111", arm: "#000", hair: "#222", label: "SECURITY" });
      const dr = at("L15", "drei"), l16 = line("L16")[0], ro = at("L16", "Roboter");
      beams.forEach((b, i) => tl.to(b, { opacity: 0.4, duration: 0.25, yoyo: true, repeat: Math.floor(C.__dur / 0.5), ease: "none" }, i * 0.1));
      crowd.forEach((c, i) => tl.to(c, { y: -14, duration: 0.25, yoyo: true, repeat: Math.floor(C.__dur / 0.5) }, (i % 3) * 0.08));
      const n = Math.floor((ro - 0.6) / 0.5); for (let k = 0; k < n; k++) { const t = 0.6 + k * 0.5; armsUp(tl, G, t, 0.2, k % 2 ? 160 : 90); tl.to(G.g, { y: 1130, duration: 0.2, yoyo: true, repeat: 1 }, t); }
      tl.fromTo("#s06-h", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3 }, dr - 0.1);
      tl.to("#s06-h", { opacity: 0, duration: 0.2 }, l16 - 0.2);
      tl.to(Sec.head, { rotation: 12, svgOrigin: "0 -150", duration: 0.3 }, ro - 0.4);
      tl.fromTo("#s06-rb", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, ro - 0.1);
      for (let k = 0; k < 6; k++) tl.to(G.aL, { rotation: k % 2 ? 90 : 0, svgOrigin: "-37 -126", duration: 0.05 }, ro + k * 0.2);''' + OUT)

S['s07'] = ('''    #s07-l { left: 140px; top: 470px; width: 800px; height: 560px; border-radius: 14px; background: #f6efdc; box-shadow: 0 24px 60px rgba(0,0,0,.5); color: #3a2a1a; opacity: 0; padding: 40px 50px; font: 600 40px/1.35 "EB Garamond", serif; }
    #s07-l h3 { font: 700 34px Inter, sans-serif; letter-spacing: .14em; color: #7a5a2a; margin: 0 0 16px; } #s07-l b { color: #b0262f; font-size: 56px; }
    #s07-l .seal { position: absolute; right: 50px; bottom: 40px; width: 120px; height: 120px; border-radius: 50%; background: #b0262f; color: #f6efdc; font: 900 56px/120px "EB Garamond", serif; text-align: center; }
    #s07-ok { left: 140px; top: 520px; width: 800px; height: 480px; border-radius: 34px; background: rgba(10,40,28,.95); border: 6px solid #39e27a; box-shadow: 0 0 70px rgba(57,226,122,.5); text-align: center; color: #fff; opacity: 0; }
    #s07-ok .t { margin-top: 200px; font: 900 62px/1.1 Inter, sans-serif; } #s07-ok .t b { color: #39e27a; }''',
SVG + '''
      <div id="s07-l" class="abs"><h3>KLOSTER ST. BENNO · BAYERN</h3>Lieber Georg,<br><b>wir haben von dir gehört.</b><br>Wir hätten da eine Stelle frei.<div class="seal">✝</div></div>
      <div id="s07-ok" class="abs"><svg width="150" height="150" viewBox="0 0 160 160" style="position:absolute;left:325px;top:34px"><circle cx="80" cy="80" r="76" fill="#39e27a"/><rect x="66" y="30" width="28" height="100" rx="6" fill="#fff"/><rect x="30" y="66" width="100" height="28" rx="6" fill="#fff"/></svg>
        <div class="t">Wurst pellen =<br><b>normal &amp; gesund</b></div></div>''',
'''      const sv = document.querySelector("#s07-svg"); sky(sv, "s07g", "#f2c27a", "#c9783a");
      el("rect", { x: 0, y: 1100, width: 1080, height: 820, fill: "#6b8a3a" }, sv);
      const leaves = []; const rl = rng(19); for (let i = 0; i < 26; i++) leaves.push(el("ellipse", { cx: rl() * 1080, cy: 300 + rl() * 400, rx: 14, ry: 8, fill: ["#e0702a", "#c9431f", "#ffb03a"][i % 3] }, sv));
      const mbox = el("g", {}, sv); el("rect", { x: 150, y: 840, width: 40, height: 260, fill: "#5a4a3a" }, mbox); el("rect", { x: 90, y: 760, width: 160, height: 110, rx: 20, fill: "#ffd43b" }, mbox);
      const env = el("g", { opacity: 0 }, sv); el("rect", { x: 300, y: 820, width: 180, height: 120, rx: 8, fill: "#f6efdc", stroke: "#c9b98a", "stroke-width": 4 }, env); el("path", { d: "M300 820 L390 890 L480 820", fill: "none", stroke: "#c9b98a", "stroke-width": 4 }, env);
      const G = finn(sv, 700, 1150, 2.3, ''' + GEO + ''');
      leaves.forEach((l, i) => tl.to(l, { y: 900, x: (i % 2 ? 60 : -60), rotation: 360, svgOrigin: `${l.getAttribute("cx")} ${l.getAttribute("cy")}`, duration: 5 + (i % 4), ease: "none" }, 0));
      const br = at("L17", "Brief"), l18 = line("L18")[0], wi = at("L18", "Wir"), l19 = line("L19")[0], no = at("L19", "normal");
      tl.fromTo(env, { opacity: 0, x: -400, rotation: -30, svgOrigin: "390 880" }, { opacity: 1, x: 0, rotation: 0, svgOrigin: "390 880", duration: 0.5, ease: "back.out(1.5)" }, br - 0.3);
      tl.to(env, { opacity: 0, duration: 0.2 }, l18); tl.fromTo("#s07-l", { opacity: 0, scale: 0.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.6)" }, l18);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -156 6 -149" }, duration: 0.15 }, wi); tl.to(G.head, { y: -10, duration: 0.15, yoyo: true, repeat: 1 }, wi);
      tl.fromTo("#s07-l b", { color: "#b0262f" }, { color: "#ff0018", duration: 0.2, yoyo: true, repeat: 5 }, wi);
      tl.to("#s07-l", { opacity: 0, y: -60, duration: 0.3 }, l19 - 0.2);
      tl.fromTo("#s07-ok", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, no - 0.4);''' + OUT)

S['s08'] = ('''    #s08-c { left: 240px; top: 470px; width: 600px; height: 200px; border-radius: 26px; background: #07060f; border: 5px solid #2a2440; text-align: center; font: 700 150px/200px "Space Mono", monospace; color: #ff8a3d; text-shadow: 0 0 26px rgba(255,138,61,.9); }
    #s08-d { left: 0; width: 1080px; top: 470px; text-align: center; opacity: 0; }
    #s08-d .a { display: inline-block; padding: 10px 30px; border-radius: 16px; background: #39b86b; color: #fff; font: 900 80px Inter, sans-serif; }
    #s08-st { left: 90px; top: 700px; width: 900px; padding: 10px 0; border: 12px solid #ff2d4b; border-radius: 22px; color: #ff4fb0; background: rgba(10,6,20,.8); text-align: center; font: 900 82px/1.05 Inter, sans-serif; opacity: 0; transform: rotate(-7deg); box-shadow: 0 0 50px rgba(255,79,176,.7); }
    #s08-st small { display: block; color: #fff; font-size: 56px; }''',
SVG + '''
      <div id="s08-c" class="abs">00:<span id="s08-t">1</span><span id="s08-n">0</span></div>
      <div id="s08-d" class="abs"><div class="a">1. NOVEMBER</div></div>
      <div id="s08-st" class="abs" data-layout-allow-overlap>NO NUT NOVEMBER<small>TAG 1 · SCHON WIEDER</small></div>''',
'''      const sv = document.querySelector("#s08-svg"); sky(sv, "s08g", "#2a1240", "#0c0518");
      el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#1a0c2a" }, sv);
      const pk = [[120, 1110], [960, 1110], [260, 1150], [820, 1150]].map(([x, y]) => { const g = el("g", {}, sv); el("ellipse", { cx: x, cy: y, rx: 70, ry: 56, fill: "#ff8a1f" }, g);
        el("rect", { x: x - 6, y: y - 70, width: 12, height: 20, fill: "#4a7a2a" }, g); el("path", { d: `M${x - 30} ${y - 12} l12 -16 l12 16Z M${x + 6} ${y - 12} l12 -16 l12 16Z M${x - 26} ${y + 16} q26 16 52 0`, fill: "#3a1a00" }, g); return g; });
      const ghosts = [[200, 900], [880, 900]].map(([x, y]) => { const g = el("g", {}, sv); el("path", { d: `M${x - 50} ${y + 140} V${y} q50 -70 100 0 V${y + 140} l-17 -20 l-17 20 l-16 -20 l-17 20 l-16 -20Z`, fill: "#f4f4f8" }, g);
        el("circle", { cx: x - 18, cy: y + 10, r: 8, fill: "#111" }, g); el("circle", { cx: x + 18, cy: y + 10, r: 8, fill: "#111" }, g); return g; });
      const G = finn(sv, 540, 1150, 2.4, ''' + GEO + ''');
      const flash = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#fff", opacity: 0 }, sv);
      const ze = at("L20", "zehn"), dr = at("L21", "drei"), zw = at("L21", "zwei"), ei = at("L21", "eins"), mi = at("L22", "Mitternacht"), er = at("L22", "erste"), l23 = line("L23")[0], sw = at("L23", "schon");
      tl.fromTo("#s08-c", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 1.7);
      ghosts.forEach((g, i) => tl.to(g, { y: -20, duration: 0.6, yoyo: true, repeat: Math.floor(C.__dur / 1.2) }, i * 0.3));
      tl.set("#s08-t", { textContent: "0" }, ze + (dr - ze) / 7); for (let k = 9; k >= 4; k--) tl.set("#s08-n", { textContent: String(k) }, ze + (10 - k) * (dr - ze) / 7);
      [[dr, "3"], [zw, "2"], [ei, "1"]].forEach(([t, v]) => { tl.set("#s08-n", { textContent: v }, t); tl.fromTo("#s08-c", { scale: 1.12 }, { scale: 1, duration: 0.3, immediateRender: false }, t); });
      tl.to(G.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, dr); armsUp(tl, G, ei, 0.3, 150);
      tl.set("#s08-n", { textContent: "0" }, mi - 0.05); tl.set("#s08-c", { color: "#39e27a", textShadow: "0 0 30px rgba(57,226,122,1)" }, mi - 0.05);
      tl.fromTo(flash, { opacity: 0.8 }, { opacity: 0, duration: 0.4, immediateRender: false }, mi - 0.05);
      tl.to("#s08-c", { opacity: 0, duration: 0.2 }, er - 0.3);
      tl.fromTo("#s08-d", { opacity: 0, rotationX: 90 }, { opacity: 1, rotationX: 0, duration: 0.4, ease: "back.out(1.6)" }, er - 0.1);
      armsDown(tl, G, er); tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -156 6 -149" }, duration: 0.15 }, er);
      tl.fromTo("#s08-st", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, sw - 0.2);
      tl.to(sv, { x: 12, duration: 0.04, repeat: 9, yoyo: true }, sw);
      tl.to(G.g, { rotation: -90, svgOrigin: "0 0", y: 1120, duration: 0.5, ease: "bounce.out" }, sw + 0.3);''' + OUT)

S['s09'] = ('''    #s09-t { left: 0; width: 1080px; top: 440px; text-align: center; color: #fff; font: 900 104px/1 Inter, sans-serif; text-shadow: 0 0 40px rgba(255,79,176,.6); opacity: 0; }
    #s09-t small { display: block; margin-top: 20px; font: 800 40px Inter, sans-serif; color: #ff8fd0; letter-spacing: .2em; }
    .s09-b { position: absolute; top: 760px; width: 440px; height: 150px; border-radius: 30px; text-align: center; color: #fff; font: 900 60px/150px Inter, sans-serif; opacity: 0; }
    #s09-y { left: 60px; background: #1fa65a; box-shadow: 0 0 50px rgba(57,226,122,.6); } #s09-n { left: 580px; background: #d32a45; box-shadow: 0 0 50px rgba(255,59,85,.6); }''',
'''      <div id="s09-t" class="abs">Und du?<small>1 JAHR ODER 1 MONAT</small></div>
      <div id="s09-y" class="s09-b">365 TAGE</div><div id="s09-n" class="s09-b">KEINE CHANCE</div>''',
'''      const st = document.querySelector("#s09-stage"), sv = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st.insertBefore(sv, st.firstChild); sky(sv, "s09g", "#2a1f4f", "#0f0b22");
      const a = at("L24", "365"), b = at("L24", "keine");
      tl.fromTo("#s09-t", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.1);
      tl.fromTo("#s09-y", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, a - 0.1);
      tl.fromTo("#s09-n", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, b - 0.1);
      tl.to(["#s09-y", "#s09-n"], { scale: 1.06, duration: 0.35, yoyo: true, repeat: 9, ease: "sine.inOut", stagger: 0.35 }, b + 0.4);''')
here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
