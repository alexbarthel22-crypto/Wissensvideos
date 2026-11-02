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

BIGT = '''    .bt { position: absolute; left: 0; width: 1080px; text-align: center; font: 900 120px/1 Inter, sans-serif; color: #fff; opacity: 0; text-shadow: 0 0 40px rgba(0,0,0,.5), 0 8px 0 rgba(0,0,0,.35); }
    .bt.r { color: #ff3b55; text-shadow: 0 0 40px rgba(255,59,85,.8); } .bt.y { color: #ffd43b; text-shadow: 0 0 40px rgba(255,212,59,.7); } .bt.g { color: #39e27a; text-shadow: 0 0 40px rgba(57,226,122,.7); }'''
def pop(sel, t, s=0.5): return f'\n      tl.fromTo("{sel}", {{ opacity: 0, scale: {s} }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }}, {t});'
def hide(sel, t): return f'\n      tl.to("{sel}", {{ opacity: 0, duration: 0.2 }}, {t});'

ME = '{ hood: "#2f6fe0", arm: "#2559b8", cap: "#ffd43b", label: "DU" }'

S['s01'] = ('''    #s01-bar { left: 0; right: 0; top: 300px; margin: 0 auto; width: fit-content; padding: 8px 28px; border-radius: 12px; background: #e0202f; color: #fff; font: 900 40px Inter, sans-serif; letter-spacing: .14em; box-shadow: 0 0 40px rgba(224,32,47,.9); }
    #s01-t { left: 30px; width: 1020px; top: 380px; text-align: center; color: #fff; font: 900 84px/1.04 Inter, sans-serif; text-shadow: 0 6px 0 rgba(0,0,0,.4), 0 0 30px rgba(0,0,0,.6); }
    #s01-t b { display: block; font-size: 150px; line-height: 1; color: #ff3b55; text-shadow: 0 0 60px rgba(255,59,85,.9), 0 8px 0 rgba(0,0,0,.4); }
    #s01-frame { left: 0; top: 0; width: 1080px; height: 1920px; box-shadow: inset 0 0 0 14px rgba(224,32,47,.9), inset 0 0 140px rgba(224,32,47,.6); }
    #s01-cnt { left: 240px; width: 600px; top: 1480px; text-align: center; font: 900 60px/1 "Space Mono", monospace; color: #ffd43b; text-shadow: 0 0 20px rgba(255,212,59,.8); }
    #s01-cnt small { display: block; margin-top: 8px; font: 800 28px Inter, sans-serif; color: #fff; letter-spacing: .14em; }
    #s01-du { left: 0; width: 1080px; top: 1370px; text-align: center; font: 900 64px Inter, sans-serif; color: #ffd43b; opacity: 0; text-shadow: 0 0 30px rgba(255,212,59,1); }
    #s01-flash { left: 0; top: 0; width: 1080px; height: 1920px; background: #fff; opacity: 0; }''',
SVG + '''
      <div id="s01-frame" class="abs"></div>
      <div id="s01-bar" class="abs">● EILMELDUNG · LIVE</div>
      <div id="s01-t" class="abs" data-layout-allow-overlap>WAS WÄRE, WENN<br>DU DER<b>LETZTE</b>FRUCHTBARE MANN WÄRST?</div>
      <div id="s01-cnt" class="abs"><span id="s01-n">4.100.000.000</span><small>FRUCHTBARE MÄNNER</small></div>
      <div id="s01-du" class="abs">★ DAS BIST DU ★</div>
      <div id="s01-flash" class="abs"></div>''',
'''      const sv = document.querySelector("#s01-svg"); sky(sv, "s01g", "#2a0d24", "#0b0716");
      const G = globe(sv, 540, 1080, 165, "s01w", 120, 3); G.dots.forEach((d) => gsap.set(d, { opacity: 1, attr: { fill: "#4da3ff" } }));
      const me = G.dots[57]; const ring = el("circle", { cx: me.getAttribute("cx"), cy: me.getAttribute("cy"), r: 22, fill: "none", stroke: "#ffd43b", "stroke-width": 5, opacity: 0 }, sv);
      const le = at("L1", "letzte"), l2 = line("L2")[0], un = at("L2", "unfruchtbar"), au = at("L2", "Außer"), l3 = line("L3")[0];
      tl.to("#s01-bar", { opacity: 0.35, duration: 0.25, yoyo: true, repeat: 17 }, 0);
      tl.to("#s01-frame", { opacity: 0.25, duration: 0.3, yoyo: true, repeat: 15 }, 0);
      tl.fromTo(G.g, { rotation: 0, svgOrigin: "540 1080" }, { rotation: 8, svgOrigin: "540 1080", duration: C.__dur, ease: "none" }, 0);
      tl.fromTo("#s01-flash", { opacity: 0.85 }, { opacity: 0, duration: 0.4, immediateRender: false }, le - 0.05);
      tl.fromTo("#s01-t b", { scale: 1.35 }, { scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }, le - 0.05);
      tl.to("#s01-t", { x: 12, duration: 0.04, repeat: 9, yoyo: true }, le);
      const off = G.dots.filter((d) => d !== me);
      tl.to(off, { attr: { fill: "#4a4f66" }, opacity: 0.6, duration: 0.1, stagger: { each: (au - un) / off.length, from: "random" } }, un - 0.3);
      count(tl, "#s01-n", 4100000000, 1, un - 0.3, au - un + 0.3, "", "", "power3.in");
      tl.to(me, { attr: { fill: "#ffd43b", r: 9 }, duration: 0.2 }, au - 0.1);
      tl.fromTo(ring, { opacity: 0, scale: 0.4, svgOrigin: `${me.getAttribute("cx")} ${me.getAttribute("cy")}` }, { opacity: 1, scale: 2, svgOrigin: `${me.getAttribute("cx")} ${me.getAttribute("cy")}`, duration: 0.6, repeat: 4, ease: "power1.out", immediateRender: false }, au);
      tl.fromTo("#s01-du", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, au);
      tl.to("#s01-cnt small", { textContent: "FRUCHTBARER MANN", duration: 0.01 }, au + 0.2);
      tl.to("#s01-t", { opacity: 0.3, duration: 0.3 }, l3);''' + OUT)

S['s02'] = (BIGT, SVG + '''
      <div id="s02-ok" class="bt g" style="top:470px;font-size:96px">✓ PERFEKT</div>''',
'''      const sv = document.querySelector("#s02-svg"), W = el("g", {}, sv);
      const R = bedroom(W, "s02g", { w1: "#3a2f6e", w2: "#221a48" });
      const F = finn(W, 420, 1150, 2.2, ''' + ME + ''');
      const P = phone(W, 650, 830, 110, "#39e27a"); gsap.set(P.g, { opacity: 0 });
      const cars = el("g", { opacity: 0 }, sv); [120, 600].forEach((x) => { el("rect", { x, y: 560, width: 360, height: 100, rx: 26, fill: "#111" }, cars); el("rect", { x: x + 60, y: 510, width: 220, height: 70, rx: 18, fill: "#1a1a1a" }, cars); el("circle", { cx: x + 80, cy: 665, r: 26, fill: "#333" }, cars); el("circle", { cx: x + 280, cy: 665, r: 26, fill: "#333" }, cars); });
      const ar = at("L4", "Arzt"), pe = at("L4", "perfekt"), l5 = line("L5")[0], re = at("L5", "Regierungsautos");
      tl.fromTo(P.g, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3 }, ar - 0.2);
      tl.to(P.g, { rotation: 6, svgOrigin: "650 830", duration: 0.05, repeat: 9, yoyo: true }, ar);
      tl.to(F.aR, { rotation: -70, svgOrigin: "37 -126", duration: 0.25 }, ar + 0.4);''' + pop("#s02-ok", "pe - 0.1") + '''
      tl.to(F.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, pe);''' + hide("#s02-ok", "l5 - 0.2") + '''
      tl.to([R.win, R.poster], { opacity: 0, duration: 0.2 }, re - 0.4);
      tl.fromTo(cars, { opacity: 0, x: -400 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, re - 0.3);
      tl.to(F.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, re);''' + OUT)

S['s03'] = (BIGT, SVG + '''
      <div id="s03-a" class="bt r" style="top:470px;font-size:84px">✈️ ❌   🏍️ ❌   🛒 ❌</div>''',
'''      const sv = document.querySelector("#s03-svg"); sky(sv, "s03g", "#1d2146", "#0c0e24"); el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#2a2c3e" }, sv);
      const F = finn(sv, 540, 1180, 2.1, ''' + ME + ''');
      const guards = [160, 300, 780, 920].map((x, i) => { const g = finn(sv, x, 1200 - (i % 2) * 20, 2.0, { hood: "#111", arm: "#000", cap: "#111", label: "" }); el("rect", { x: -14, y: -170, width: 28, height: 8, rx: 3, fill: "#000" }, g.head); gsap.set(g.g, { opacity: 0 }); return g; });
      const wv = at("L6", "wertvollste"), bo = at("L6", "Bodyguards"), l7 = line("L7")[0], fl = at("L7", "fliegen");
      tl.to(F.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, wv);
      guards.forEach((g, i) => tl.fromTo(g.g, { opacity: 0, x: (i < 2 ? -200 : 1280) }, { opacity: 1, x: [160, 300, 780, 920][i], duration: 0.4, ease: "power3.out" }, bo - 0.2 + i * 0.12));''' + pop("#s03-a", "fl - 0.1") + OUT)

S['s04'] = (BIGT + '''
    #s04-n { left: 0; width: 1080px; top: 640px; text-align: center; font: 900 120px/1 Inter, sans-serif; color: #ffd43b; opacity: 0; text-shadow: 0 0 40px rgba(255,212,59,.7); }
    #s04-n small { display: block; font: 800 38px Inter, sans-serif; color: #fff; letter-spacing: .14em; margin-top: 8px; }''',
SVG + '''
      <div id="s04-n" class="abs"><span id="s04-v">0</span><small id="s04-l">BABYS PRO JAHR</small></div>''',
'''      const sv = document.querySelector("#s04-svg"); sky(sv, "s04g", "#1d3a5a", "#0d1e33");
      el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#16263c" }, sv);
      const lab = el("g", {}, sv); el("rect", { x: 140, y: 880, width: 800, height: 40, rx: 10, fill: "#cfd8ea" }, lab);
      const tubes = []; for (let i = 0; i < 9; i++) { const g = el("g", { opacity: 0 }, lab); el("rect", { x: 180 + i * 84, y: 720, width: 40, height: 160, rx: 20, fill: "#fff", stroke: "#9aa3b5", "stroke-width": 4 }, g); el("rect", { x: 186 + i * 84, y: 800, width: 28, height: 74, rx: 14, fill: COLS[i % 6], opacity: 0.8 }, g); tubes.push(g); }
      const babies = []; for (let i = 0; i < 18; i++) babies.push(el("circle", { cx: 120 + (i % 9) * 105, cy: 940 + Math.floor(i / 9) * 90, r: 30, fill: "#f2cba5", opacity: 0 }, sv));
      const dct = woman(sv, 900, 1180, 1.8, "#ffffff", "#6b4423"); gsap.set(dct.g, { opacity: 0 });
      const l8 = line("L8")[0], m1 = at("L8", "130"), l9 = line("L9")[0], hu = at("L9", "hundert"), ge = at("L9", "genug"), l10 = line("L10")[0], uh = at("L10", "Uhr");
      tl.to("#s04-n", { opacity: 1, duration: 0.3 }, l8 + 0.2);
      count(tl, "#s04-v", 0, 130000000, l8 + 0.3, m1 - l8, "", "", "power2.out");
      tl.to(babies, { opacity: 1, duration: 0.1, stagger: 0.06 }, m1 - 0.6);
      tl.to(babies, { opacity: 0, duration: 0.2 }, l9 - 0.1);
      tl.set("#s04-l", { textContent: "SPERMIEN PRO TAG" }, l9); count(tl, "#s04-v", 0, 100000000, hu - 0.4, 0.8, "", "+", "power2.out");
      tl.to("#s04-v", { color: "#39e27a", duration: 0.2 }, ge);
      tl.to("#s04-n", { opacity: 0, duration: 0.2 }, l10 - 0.2);
      tl.to(tubes, { opacity: 1, duration: 0.15, stagger: 0.12 }, l10);
      tl.fromTo(dct.g, { opacity: 0 }, { opacity: 1, duration: 0.3 }, l10 + 0.3);
      tubes.forEach((t, i) => tl.to(t, { y: -16, duration: 0.25, yoyo: true, repeat: 3 }, uh - 0.5 + i * 0.05));''' + OUT)

S['s05'] = (BIGT + '''
    #s05-live { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 470px; padding: 8px 22px; border-radius: 12px; background: #e0202f; color: #fff; font: 900 40px Inter, sans-serif; letter-spacing: .1em; opacity: 0; }''',
SVG + '''
      <div id="s05-live" class="abs">● 8 MRD. ZUSCHAUER</div>''',
'''      const sv = document.querySelector("#s05-svg"); sky(sv, "s05g", "#e8eef6", "#c9d3e0"); el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#b8c2d0" }, sv);
      const door = el("g", {}, sv); el("rect", { x: 300, y: 560, width: 480, height: 600, rx: 10, fill: "#8a96aa" }, door); el("rect", { x: 330, y: 590, width: 420, height: 570, fill: "#6b7a90" }, door);
      el("rect", { x: 400, y: 640, width: 280, height: 60, rx: 8, fill: "#e0202f" }, door); txt(door, 540, 683, "BESETZT", 40, "#fff");
      el("circle", { cx: 710, cy: 880, r: 16, fill: "#ffd43b" }, door);
      const cup = el("g", { opacity: 0 }, sv); el("path", { d: "M120 960 H220 L208 1100 H132Z", fill: "#fff", stroke: "#9aa3b5", "stroke-width": 4 }, cup); el("rect", { x: 112, y: 944, width: 116, height: 20, rx: 6, fill: "#4da3ff" }, cup);
      const guard = woman(sv, 900, 1180, 2.0, "#ffffff", "#3a2a1a");
      const be = at("L11", "Becher"), au = at("L11", "Aufsicht"), l12 = line("L12")[0], ma = at("L12", "machst");
      tl.fromTo(cup, { opacity: 0, y: 40, scale: 0.6, svgOrigin: "170 1020" }, { opacity: 1, y: 0, scale: 1, svgOrigin: "170 1020", duration: 0.3, ease: "back.out(2)" }, be - 0.1);
      tl.to(guard.head, { rotation: -12, svgOrigin: "0 -150", duration: 0.3 }, au - 0.1);
      tl.to(guard.mouth, { attr: { d: "M-6 -149 H6" }, duration: 0.1 }, au);''' + pop("#s05-live", "l12 + 0.3") + '''
      tl.to("#s05-live", { opacity: 0.4, duration: 0.2, yoyo: true, repeat: 7 }, l12 + 0.6);
      tl.to(door, { x: 6, duration: 0.05, repeat: 9, yoyo: true }, ma);''' + OUT)

S['s06'] = (BIGT, SVG + '''
      <div id="s06-f" class="bt y" style="top:470px;font-size:96px"><span id="s06-v">0</span></div>''',
'''      const sv = document.querySelector("#s06-svg"); sky(sv, "s06g", "#2a1158", "#a4307f");
      const bb = el("g", {}, sv); for (let i = 0; i < 3; i++) { el("rect", { x: 80 + i * 320, y: 640, width: 280, height: 400, rx: 20, fill: "#111" }, bb); }
      const faces = [0, 1, 2].map((i) => finn(sv, 220 + i * 320, 1020, 1.6, ''' + ME + '''));
      const flashes = []; const rf = rng(9); for (let i = 0; i < 16; i++) flashes.push(el("circle", { cx: 60 + rf() * 960, cy: 1250 + rf() * 400, r: 26, fill: "#fff", opacity: 0 }, sv));
      const crowd = []; for (let i = 0; i < 14; i++) crowd.push(tiny(sv, 40 + i * 76, 1700 + (i % 2) * 30, COLS[i % 6], 2.2));
      const ac = at("L13", "Acht"), l14 = line("L14")[0], mi = at("L14", "Milliarde");
      flashes.forEach((f, i) => tl.fromTo(f, { opacity: 0 }, { opacity: 0.9, duration: 0.06, yoyo: true, repeat: 1, immediateRender: false }, 0.6 + i * 0.35));
      crowd.forEach((c, i) => tl.to(c, { y: -18, duration: 0.2, yoyo: true, repeat: 7 }, ac + (i % 3) * 0.07));
      tl.to("#s06-f", { opacity: 1, duration: 0.2 }, l14);
      count(tl, "#s06-v", 0, 1000000000, l14 + 0.2, mi - l14 + 0.3, "", " FOLLOWER", "power2.in");''' + OUT)

S['s07'] = (BIGT, SVG + '''
      <div id="s07-l" class="bt r" style="top:470px;font-size:88px">10.000 💌 / TAG</div>''',
'''      const sv = document.querySelector("#s07-svg"); sky(sv, "s07g", "#ffb3d1", "#d96a9c"); el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#8a4a62" }, sv);
      const W1 = woman(sv, 220, 1180, 2.0, "#e0202f", "#3a2a1a"), W2 = woman(sv, 420, 1180, 2.0, "#a06bff", "#e0b050");
      const signs = [[220, "😡"], [420, "😤"]].map(([x, e]) => txt(sv, x, 700, e, 110, "#fff", { opacity: 0 }));
      const F = finn(sv, 820, 1180, 2.1, ''' + ME + ''');
      const env = []; const re = rng(6); for (let i = 0; i < 26; i++) env.push(txt(sv, 820 + (re() - 0.5) * 300, 300, "💌", 70, "#fff", { opacity: 0 }));
      const wu = at("L15", "wütend"), l16 = line("L16")[0], li = at("L16", "Liebesbriefe");
      tl.to(signs, { opacity: 1, y: -20, duration: 0.25, stagger: 0.15 }, wu - 0.1);
      tl.to([W1.g, W2.g], { x: "+=10", duration: 0.05, repeat: 7, yoyo: true }, wu);
      tl.to(signs, { opacity: 0, duration: 0.2 }, l16 - 0.2);
      env.forEach((e, i) => tl.fromTo(e, { opacity: 1, y: 0 }, { y: 700 + re() * 300, rotation: (re() - 0.5) * 90, svgOrigin: "820 300", duration: 1.2, ease: "power1.in", immediateRender: false }, li - 0.4 + i * 0.05));
      tl.to(F.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, li);''' + pop("#s07-l", "li - 0.1") + OUT)

S['s08'] = (BIGT, SVG + '''
      <div id="s08-n" class="bt r" style="top:470px;font-size:92px">⚠ INZUCHT</div>''',
'''      const sv = document.querySelector("#s08-svg"); sky(sv, "s08g", "#1a0a1a", "#050308");
      const red = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#c4123a", opacity: 0 }, sv);
      const F = finn(sv, 540, 640, 1.2, ''' + ME + ''');
      const kids = [], lines_ = []; const rk = rng(2);
      for (let i = 0; i < 30; i++) { const x = 80 + (i % 10) * 102, y = 790 + Math.floor(i / 10) * 125;
        lines_.push(el("line", { x1: 540, y1: 650, x2: x, y2: y - 40, stroke: "#ffd43b", "stroke-width": 2, opacity: 0 }, sv));
        kids.push(tiny(sv, x, y, COLS[i % 6], 1.6, { opacity: 0 })); }
      const web = el("g", { opacity: 0 }, sv); for (let i = 0; i < 40; i++) { const a = kids[Math.floor(rk() * 30)], b = kids[Math.floor(rk() * 30)]; }
      for (let i = 0; i < 45; i++) { const ia = Math.floor(rk() * 30), ib = Math.floor(rk() * 30); el("line", { x1: 80 + (ia % 10) * 102, y1: 770 + Math.floor(ia / 10) * 125, x2: 80 + (ib % 10) * 102, y2: 770 + Math.floor(ib / 10) * 125, stroke: "#ff3b55", "stroke-width": 3, opacity: 0.7 }, web); }
      const ve = at("L17", "verstörende"), di = at("L18", "dein"), ha = at("L19", "Halbgeschwister"), je = at("L19", "jeder"), in_ = at("L20", "Inzucht");
      tl.to(F.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, ve);
      tl.to(kids, { opacity: 1, duration: 0.1, stagger: 0.04 }, di - 0.3);
      tl.to(lines_, { opacity: 0.8, duration: 0.1, stagger: 0.03 }, di);
      tl.to(lines_, { opacity: 0, duration: 0.3 }, je - 0.3);
      tl.to(web, { opacity: 1, duration: 0.5 }, je - 0.2);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.3, duration: 0.3, yoyo: true, repeat: 5, immediateRender: false }, in_ - 0.1);''' + pop("#s08-n", "in_ - 0.1") + '''
      tl.to(sv, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, in_);''' + OUT)

S['s09'] = (BIGT, SVG + '''
      <div id="s09-a" class="bt g" style="top:470px;font-size:92px">❄️ SAMENBANK</div><div id="s09-b" class="bt g" style="top:470px;font-size:92px">🧬 LABOR</div>''',
'''      const sv = document.querySelector("#s09-svg"); sky(sv, "s09g", "#0d2a4a", "#061526");
      const tanks = []; for (let i = 0; i < 5; i++) { const g = el("g", {}, sv); const x = 120 + i * 180; el("rect", { x, y: 780, width: 120, height: 360, rx: 30, fill: "#cfd8ea" }, g); el("rect", { x: x + 10, y: 760, width: 100, height: 40, rx: 14, fill: "#9aa3b5" }, g);
        const fog = el("ellipse", { cx: x + 60, cy: 760, rx: 70, ry: 26, fill: "#e8f6ff", opacity: 0.6 }, g); tanks.push(fog); }
      const dna = el("g", { opacity: 0 }, sv); for (let i = 0; i < 18; i++) { const y = 700 + i * 30, dx = Math.sin(i * 0.6) * 120; el("circle", { cx: 540 + dx, cy: y, r: 12, fill: "#39e27a" }, dna); el("circle", { cx: 540 - dx, cy: y, r: 12, fill: "#4da3ff" }, dna); el("line", { x1: 540 + dx, y1: y, x2: 540 - dx, y2: y, stroke: "#fff", "stroke-width": 3, opacity: 0.5 }, dna); }
      const sa = at("L21", "Samenbanken"), l22 = line("L22")[0], la = at("L22", "Labor");
      tanks.forEach((f, i) => tl.to(f, { attr: { ry: 40 }, opacity: 0.9, duration: 0.8, yoyo: true, repeat: 5 }, 0.3 + i * 0.15));''' + pop("#s09-a", "sa - 0.1") + hide("#s09-a", "l22 - 0.2") + '''
      tl.to(tanks.map((t) => t.parentNode), { opacity: 0.2, duration: 0.3 }, l22);
      tl.fromTo(dna, { opacity: 0, rotation: -20, svgOrigin: "540 960" }, { opacity: 1, rotation: 20, svgOrigin: "540 960", duration: 3, ease: "none" }, l22);''' + pop("#s09-b", "la - 0.1") + OUT)

S['s10'] = ('''    #s10-t { left: 0; width: 1080px; top: 440px; text-align: center; color: #fff; font: 900 96px/1.05 Inter, sans-serif; text-shadow: 0 0 40px rgba(255,79,176,.6); opacity: 0; }
    .s10-b { position: absolute; top: 760px; width: 470px; height: 150px; border-radius: 30px; text-align: center; color: #fff; white-space: nowrap; font: 900 50px/150px Inter, sans-serif; opacity: 0; }
    #s10-y { left: 50px; background: #1fa65a; box-shadow: 0 0 50px rgba(57,226,122,.6); } #s10-n { left: 560px; background: #d32a45; box-shadow: 0 0 50px rgba(255,59,85,.6); }
    #s10-f { left: 290px; top: 960px; width: 500px; height: 110px; border-radius: 55px; background: #ff3b5c; color: #fff; text-align: center; font: 900 56px/110px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 50px rgba(255,59,92,.7); }''',
'''      <div id="s10-t" class="abs">Und du?</div>
      <div id="s10-y" class="s10-b">😎 GENIESSEN</div><div id="s10-n" class="s10-b">🫣 VERSTECKEN</div>
      <div id="s10-f" class="abs">+ Folgen</div>''',
'''      const st = document.querySelector("#s10-stage"), sv = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st.insertBefore(sv, st.firstChild); sky(sv, "s10g", "#2a1f4f", "#0f0b22");
      const a = at("L23", "genießen"), b = at("L23", "verstecken"), fo = at("L24", "folg");
      tl.fromTo("#s10-t", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.1);
      tl.fromTo("#s10-y", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, a - 0.1);
      tl.fromTo("#s10-n", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, b - 0.1);
      tl.fromTo("#s10-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s10-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);''')
here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
