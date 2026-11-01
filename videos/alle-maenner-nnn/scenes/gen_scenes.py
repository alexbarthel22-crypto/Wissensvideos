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

S['s01'] = ('''    #s01-bar { left: 0; right: 0; top: 232px; margin: 0 auto; width: fit-content; padding: 8px 26px; border-radius: 12px; background: #e0202f; color: #fff; font: 900 38px Inter, sans-serif; letter-spacing: .14em; box-shadow: 0 0 40px rgba(224,32,47,.9); }
    #s01-t { left: 0; width: 1080px; top: 310px; text-align: center; }
    #s01-t .a { font: 900 116px/1 Inter, sans-serif; color: #ff4fb0; text-shadow: 0 0 50px rgba(255,79,176,.95), 0 8px 30px rgba(0,0,0,.7); }
    #s01-t .b { font: 900 60px/1.1 Inter, sans-serif; color: #fff; text-shadow: 0 6px 24px rgba(0,0,0,.8); }
    #s01-cnt { left: 230px; width: 620px; top: 545px; height: 112px; border: 4px solid #ffd43b; border-radius: 18px; background: rgba(10,8,24,.9); text-align: center; box-shadow: 0 0 40px rgba(255,212,59,.45); }
    #s01-cnt .n { font: 900 64px/76px Inter, sans-serif; color: #ffd43b; } #s01-cnt .l { font: 700 24px "Space Mono", monospace; color: #fff; letter-spacing: .2em; }
    #s01-stamp { left: 120px; top: 820px; width: 840px; padding: 8px 0; border: 12px solid #ff2d4b; border-radius: 22px; color: #ff2d4b; background: rgba(10,6,20,.6); text-align: center; font: 900 74px/1.1 Inter, sans-serif; opacity: 0; transform: rotate(-8deg); text-shadow: 0 0 30px rgba(255,45,75,.8); box-shadow: 0 0 40px rgba(255,45,75,.6); }
    #s01-flash { left: 0; top: 0; width: 1080px; height: 1920px; background: #fff; opacity: 0; }
    #s01-frame { left: 0; top: 0; width: 1080px; height: 1920px; box-shadow: inset 0 0 0 14px rgba(224,32,47,.9), inset 0 0 140px rgba(224,32,47,.6); }
    #s01-cal { left: 340px; top: 600px; width: 400px; height: 400px; border-radius: 30px; background: #fff; box-shadow: 0 0 70px rgba(57,226,122,.8); opacity: 0; text-align: center; overflow: hidden; }
    #s01-cal .h { height: 100px; background: #39b86b; color: #fff; font: 900 56px/100px Inter, sans-serif; letter-spacing: .12em; }
    #s01-cal .n { font: 900 230px/290px Inter, sans-serif; color: #22283f; }
    #s01-q { left: 0; width: 1080px; top: 1000px; text-align: center; font: 900 120px Inter, sans-serif; color: #ff3b55; opacity: 0; text-shadow: 0 0 40px rgba(255,59,85,.9); }''',
SVG + '''
      <div id="s01-frame" class="abs"></div>
      <div id="s01-bar" class="abs">● EILMELDUNG · LIVE</div>
      <div id="s01-t" class="abs" data-layout-allow-overlap><div class="a">ALLE MÄNNER</div><div class="b">MACHEN NO NUT NOVEMBER</div></div>
      <div id="s01-cnt" class="abs"><div class="n">4.100.000.000</div><div class="l">TEILNEHMER WELTWEIT</div></div>
      <div id="s01-stamp" class="abs" data-layout-allow-overlap>KEIN SACK-SILVESTER</div>
      <div id="s01-cal" class="abs"><div class="h">DEZEMBER</div><div class="n">1</div></div>
      <div id="s01-q" class="abs">???</div>
      <div id="s01-flash" class="abs"></div>''',
'''      const sv = document.querySelector("#s01-svg"); sky(sv, "s01g", "#2a0d24", "#0b0716");
      const G = globe(sv, 540, 940, 220, "s01w", 110, 3);
      const ring = el("g", { "data-layout-allow-overlap": "" }, sv), rr = rng(11), men = [];
      for (let i = 0; i < 26; i++) { const a = (i / 26) * Math.PI * 2; men.push(tiny(ring, 540 + Math.cos(a) * 300, 960 + Math.sin(a) * 300 * 0.9, ["#ff4fb0", "#4da3ff", "#ffd43b", "#39e27a", "#ff6a3d"][i % 5], 1.3, { opacity: 0 })); }
      const al = at("L1", "Alle"), nn = at("L1", "nonutnovember"), vi = at("L2", "vier"), dr = at("L2", "Dreißig"), sa = at("L2", "Sack"), l3 = line("L3")[0], de = at("L3", "Dezember"), ke = at("L3", "keiner");
      tl.to("#s01-bar", { opacity: 0.35, duration: 0.25, yoyo: true, repeat: 15 }, 0);
      tl.to("#s01-frame", { opacity: 0.2, duration: 0.3, yoyo: true, repeat: 11 }, 0);
      tl.fromTo(G.g, { rotation: 0, svgOrigin: "540 940" }, { rotation: 10, svgOrigin: "540 940", duration: C.__dur, ease: "none" }, 0);
      tl.fromTo("#s01-flash", { opacity: 0.85 }, { opacity: 0, duration: 0.4, immediateRender: false }, al - 0.05);
      tl.to(["#s01-t", "#s01-cnt"], { x: 12, duration: 0.04, repeat: 9, yoyo: true }, al);
      tl.fromTo("#s01-t .a", { scale: 1.25 }, { scale: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, al - 0.05);
      tl.to(G.dots, { opacity: 1, attr: { fill: "#ff4fb0" }, duration: 0.15, stagger: { each: 0.012, from: "random" } }, al);
      tl.to(men, { opacity: 1, duration: 0.15, stagger: 0.04 }, nn - 0.3);
      tl.fromTo("#s01-cnt", { scale: 1 }, { scale: 1.15, duration: 0.18, yoyo: true, repeat: 3, immediateRender: false }, vi - 0.05);
      tl.to(men, { y: -16, duration: 0.15, yoyo: true, repeat: 3, stagger: 0.01 }, dr);
      tl.fromTo("#s01-stamp", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, sa - 0.1);
      tl.to(sv, { x: 14, duration: 0.04, repeat: 9, yoyo: true }, sa + 0.1);
      tl.to(["#s01-stamp", G.g, ring, "#s01-cnt", "#s01-t", "#s01-bar"], { opacity: 0, duration: 0.3 }, l3 - 0.2);
      tl.fromTo("#s01-cal", { opacity: 0, scale: 0.4, rotation: -12 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.45, ease: "back.out(1.8)" }, de - 0.15);
      tl.fromTo("#s01-q", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power3.out" }, ke);
      tl.to("#s01-q", { x: 10, duration: 0.05, repeat: 7, yoyo: true }, ke + 0.25);''' + OUT)

S['s02'] = (CHIP + '''
    #s02-sign { left: 120px; top: 600px; width: 420px; height: 90px; border-radius: 16px; background: #120f26; border: 5px solid #39e27a; color: #39e27a; text-align: center; font: 900 58px/80px Inter, sans-serif; letter-spacing: .12em; text-shadow: 0 0 20px rgba(57,226,122,.9); box-shadow: 0 0 30px rgba(57,226,122,.5); }''',
SVG + '''
      <div id="s02-sign" class="abs">FITNESS</div>
      <div id="s02-br" class="chip" style="left:620px;top:470px">BRRR!</div>''',
'''      const sv = document.querySelector("#s02-svg"); sky(sv, "s02g", "#3b4f8f", "#1a2246");
      const gym = el("g", {}, sv); el("rect", { x: 80, y: 560, width: 500, height: 560, fill: "#4a3f7a" }, gym); el("rect", { x: 260, y: 900, width: 140, height: 220, fill: "#1b1636" }, gym);
      for (let k = 0; k < 2; k++) el("rect", { x: 120 + k * 280, y: 730, width: 140, height: 120, fill: "#ffe7a3", opacity: 0.8 }, gym);
      el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#2a2c3e" }, sv);
      const q = [], rq = rng(2); for (let i = 0; i < 26; i++) { const x = 360 + i * 30 + (i > 12 ? 0 : 0), y = 1120 + (i % 2) * 10 + Math.floor(i / 13) * 0;
        q.push(tiny(sv, 420 + (i % 13) * 52, 1125 + Math.floor(i / 13) * 70, ["#ff4fb0", "#4da3ff", "#ffd43b", "#39e27a", "#ff6a3d"][i % 5], 1.5, { opacity: 0 })); }
      const blk = el("g", { opacity: 0 }, sv); el("rect", { x: 140, y: 440, width: 800, height: 680, fill: "#5b5f8f" }, blk);
      const wins = []; for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) { const x = 190 + c * 250, y = 480 + r * 210, g = el("g", {}, blk);
        el("rect", { x, y, width: 200, height: 170, fill: "#cfe8ff" }, g); tiny(g, x + 100, y + 160, "#f2cba5", 2);
        const dr = []; for (let k = 0; k < 6; k++) dr.push(el("line", { x1: x + 40 + k * 24, y1: y + 10, x2: x + 40 + k * 24, y2: y + 40, stroke: "#2b7cff", "stroke-width": 5, "stroke-linecap": "round" }, g));
        wins.push({ g, dr }); }
      const st = at("L5", "Schlangen"), l6 = line("L6")[0], ka = at("L6", "kalt");
      tl.fromTo(gym, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4 }, 0.6);
      tl.fromTo("#s02-sign", { opacity: 0 }, { opacity: 1, duration: 0.1, repeat: 5, yoyo: true }, 0.8); tl.set("#s02-sign", { opacity: 1 }, 1.4);
      tl.to(q, { opacity: 1, duration: 0.12, stagger: 0.05 }, st - 0.4);
      q.forEach((m, i) => tl.to(m, { y: -8, duration: 0.18, yoyo: true, repeat: 5 }, st + 0.6 + (i % 4) * 0.05));
      tl.to([gym, "#s02-sign", ...q], { opacity: 0, duration: 0.3 }, l6 - 0.2);
      tl.fromTo(blk, { opacity: 0, scale: 0.9, svgOrigin: "540 780" }, { opacity: 1, scale: 1, svgOrigin: "540 780", duration: 0.4 }, l6);
      wins.forEach((w, i) => w.dr.forEach((d, k) => tl.fromTo(d, { y: -10, opacity: 0 }, { y: 120, opacity: 1, duration: 0.45, repeat: 5, ease: "none", immediateRender: false }, ka + (i % 3) * 0.06 + k * 0.05)));
      wins.forEach((w, i) => tl.to(w.g, { x: 4, duration: 0.05, repeat: 30, yoyo: true }, ka + 0.2 + i * 0.02));
      tl.fromTo("#s02-br", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, ka + 0.3);''' + OUT)

S['s03'] = ('''    #s03-win { left: 110px; top: 470px; width: 860px; height: 560px; border-radius: 22px; background: #f4f2fa; tbox-shadow: 0 24px 60px rgba(0,0,0,.5); overflow: hidden; opacity: 0; }
    #s03-win .bar { height: 64px; background: #dcd8e8; } #s03-win .url { position: absolute; left: 150px; top: 12px; width: 560px; height: 40px; border-radius: 20px; background: #fff; font: 700 26px/40px Inter, sans-serif; color: #5a5f7a; padding-left: 20px; }
    #s03-win .url b { background: #22283f; color: #22283f; border-radius: 4px; }
    #s03-k { left: 0; width: 1080px; top: 1040px; text-align: center; font: 900 96px Inter, sans-serif; color: #4da3ff; opacity: 0; text-shadow: 0 0 30px rgba(77,163,255,.8); }''',
SVG + '''
      <div id="s03-win" class="abs"><div class="bar"></div><div class="url">www.<b>geheim123</b>.com</div><svg id="s03-ch" width="860" height="496" viewBox="0 0 860 496" style="position:absolute;left:0;top:64px"></svg></div>
      <div id="s03-k" class="abs">???</div>''',
'''      const sv = document.querySelector("#s03-svg"); sky(sv, "s03g", "#1d2146", "#0c0e24");
      const ch = document.querySelector("#s03-ch"); for (let v = 0; v < 4; v++) el("line", { x1: 50, y1: 60 + v * 110, x2: 820, y2: 60 + v * 110, stroke: "#d8d4e6", "stroke-width": 2 }, ch);
      const ln = el("path", { d: "M50 120 L180 100 L300 110 L420 90 L470 300 L560 330 L680 320 L810 340", stroke: "#ff3b55", "stroke-width": 12, fill: "none", "stroke-linejoin": "round", "stroke-linecap": "round", "stroke-dasharray": 1300, "stroke-dashoffset": 1300 }, ch);
      txt(ch, 640, 300, "−50 %", 64, "#ff3b55", { opacity: 0, id: "s03-m" });
      const tbox = el("g", { opacity: 0 }, sv); el("rect", { x: 380, y: 640, width: 320, height: 200, rx: 18, fill: "#8ad0ff" }, tbox); el("rect", { x: 380, y: 640, width: 320, height: 60, rx: 18, fill: "#5fb3f0" }, tbox);
      el("path", { d: "M490 640 Q540 560 590 640Z", fill: "#fff" }, tbox); txt(tbox, 540, 790, "TASCHENTÜCHER", 32, "#1d3c66");
      const arr = el("g", { opacity: 0 }, sv); el("path", { d: "M800 600 V820 L760 780 M800 820 L840 780", stroke: "#ff3b55", "stroke-width": 18, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, arr);
      const ha = at("L8", "Hälfte"), l9 = line("L9")[0], si = at("L9", "sinken"), ko = at("L9b", "Komischerweise");
      tl.fromTo("#s03-win", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 0.9);
      tl.to(ln, { attr: { "stroke-dashoffset": 0 }, duration: 1.4, ease: "power1.in" }, ha - 1.0);
      tl.to("#s03-m", { opacity: 1, duration: 0.2 }, ha + 0.3);
      tl.to("#s03-win", { opacity: 0, y: -60, duration: 0.3 }, l9 - 0.2);
      tl.fromTo(tbox, { opacity: 0, scale: 0.6, svgOrigin: "540 740" }, { opacity: 1, scale: 1, svgOrigin: "540 740", duration: 0.35, ease: "back.out(2)" }, l9);
      tl.fromTo(arr, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.3 }, si - 0.1);
      tl.fromTo("#s03-k", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25 }, ko - 0.05);
      tl.to(tbox, { rotation: -6, svgOrigin: "540 740", duration: 0.12, yoyo: true, repeat: 3 }, ko);''' + OUT)

S['s04'] = (CHIP + '''
    #s04-ph { left: 560px; top: 440px; width: 440px; height: 640px; border-radius: 48px; background: #f1eefa; border: 10px solid #22283f; overflow: hidden; opacity: 0; box-shadow: 0 20px 60px rgba(0,0,0,.5); }
    #s04-ph .hd { height: 80px; background: #b77cff; color: #fff; font: 800 34px/80px Inter, sans-serif; padding-left: 28px; }
    .s04-m { position: absolute; left: 22px; right: 22px; padding: 16px 20px; border-radius: 22px 22px 22px 6px; background: #fff; color: #22283f; font: 600 30px/1.25 Inter, sans-serif; opacity: 0; box-shadow: 0 4px 12px rgba(0,0,0,.12); }
    .s04-m small { display: block; margin-top: 6px; font: 600 20px Inter, sans-serif; color: #8a8fa8; } .s04-m u { text-decoration: none; background: #ffd43b; border-radius: 4px; }''',
SVG + '''
      <div id="s04-ph" class="abs"><div class="hd">Jonas</div>
        <div id="s04-m1" class="s04-m" style="top:110px">hey :)<small>vor 1 Sek.</small></div>
        <div id="s04-m2" class="s04-m" style="top:240px">Hallo Lena<u>,</u> wie war dein Tag<u>?</u> Ich hoffe<u>,</u> gut<u>.</u><small>vor 1 Sek.</small></div></div>
      <div id="s04-hw" class="chip" style="left:640px;top:520px"><i>✓</i> Hausaufgaben</div>
      <div id="s04-pf" class="chip" style="left:560px;top:440px;background:#c9f5d8">PARFÜM <b>9000</b></div>''',
'''      const sv = document.querySelector("#s04-svg"), W = el("g", {}, sv);
      const R = bedroom(W, "s04g", { w1: "#4a2f66", w2: "#2a1a44", floor: "#2e1f45" }); R.poster.remove();
      const Lg = lena(W, 300, 1130, 2.4);
      const J = finn(W, 790, 1130, 2.3, { hood: "#3aa37a", arm: "#2f8a65", cap: "#22283f", label: "" }); gsap.set(J.g, { opacity: 0 });
      const cloud = []; const rc = rng(6); for (let i = 0; i < 9; i++) cloud.push(el("circle", { cx: 700 + rc() * 220, cy: 720 + rc() * 260, r: 30 + rc() * 30, fill: "#8ff0b0", opacity: 0 }, W));
      const se = at("L11", "Sekunden"), sa = at("L12", "Sätzen"), sz = at("L12", "Satzzeichen"), l13 = line("L13")[0], ha = at("L13", "Hausaufgaben"), l13b = line("L13b")[0], vi = at("L13b", "Viel");
      tl.fromTo(Lg.g, { opacity: 0, x: 200 }, { opacity: 1, x: 300, duration: 0.4 }, 0.8);
      tl.fromTo("#s04-ph", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35 }, line("L11")[0]);
      tl.fromTo("#s04-m1", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2 }, se - 0.15);
      tl.to(Lg.mouth, { attr: { d: "M-6 -150 Q0 -156 6 -150" }, duration: 0.15 }, se);
      tl.fromTo("#s04-m2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2 }, sa - 0.3);
      tl.fromTo("#s04-m2 u", { backgroundColor: "rgba(255,212,59,0)" }, { backgroundColor: "rgba(255,212,59,1)", duration: 0.2 }, sz - 0.1);
      tl.to("#s04-ph", { opacity: 0, x: 300, duration: 0.3 }, l13 - 0.2);
      tl.to(Lg.mouth, { attr: { d: "M-6 -152 Q0 -147 6 -152" }, duration: 0.15 }, l13);
      tl.fromTo(J.g, { opacity: 0, x: 900 }, { opacity: 1, x: 790, duration: 0.35 }, l13 - 0.05);
      tl.fromTo("#s04-hw", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)" }, ha - 0.1);
      armsUp(tl, J, ha, 0.25, 150);
      tl.to("#s04-hw", { opacity: 0, duration: 0.2 }, l13b - 0.2); armsDown(tl, J, l13b - 0.2);
      tl.to(cloud, { opacity: 0.55, scale: 1.3, svgOrigin: "800 860", duration: 0.6, stagger: 0.05 }, l13b + 0.3);
      tl.fromTo("#s04-pf", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)" }, vi - 0.1);
      tl.to(Lg.aR, { rotation: -150, svgOrigin: "35 -126", duration: 0.25 }, vi); tl.to(Lg.g, { x: 250, rotation: -6, svgOrigin: "0 0", duration: 0.3 }, vi);
      tl.to(Lg.mouth, { attr: { d: "M-6 -149 Q0 -153 6 -149" }, duration: 0.15 }, vi);''' + OUT)

S['s05'] = (CHIP, SVG + '''
      <div id="s05-hup" class="chip" style="left:600px;top:520px"><b>HUP! HUP!</b></div>
      <div id="s05-vs" class="chip" style="left:430px;top:470px;font-size:70px">1 <b>vs</b> 1</div>''',
'''      const sv = document.querySelector("#s05-svg"); sky(sv, "s05g", "#5fa8ff", "#2a5fb8");
      const pitch = el("g", {}, sv); el("rect", { x: 0, y: 700, width: 1080, height: 1220, fill: "#3aa35a" }, pitch);
      for (let k = 0; k < 6; k++) el("rect", { x: k * 180, y: 700, width: 90, height: 1220, fill: "#349652" }, pitch);
      el("rect", { x: 380, y: 560, width: 320, height: 150, fill: "none", stroke: "#fff", "stroke-width": 10 }, pitch);
      const pl = [[320, 1060, "#ff6a3d"], [560, 1080, "#4da3ff"], [780, 1050, "#ff6a3d"]].map(([x, y, c]) => finn(pitch, x, y, 1.7, { hood: c, arm: shade(c, 0.85), label: "" }));
      const cards = [["#ffd43b", 380], ["#ff3b55", 540], ["#ffd43b", 700], ["#ff3b55", 460], ["#ffd43b", 620]].map(([c, x], i) => el("rect", { x, y: 520, width: 60, height: 86, rx: 8, fill: c, opacity: 0, transform: `rotate(${(i - 2) * 9} ${x + 30} 563)` }, pitch));
      const road = el("g", { opacity: 0 }, sv); el("rect", { x: 0, y: 760, width: 1080, height: 1160, fill: "#3a3d4f" }, road);
      for (let k = 0; k < 6; k++) el("rect", { x: 40 + k * 190, y: 930, width: 110, height: 16, fill: "#ffd43b" }, road);
      const cars = [[120, 860, "#ff3b55"], [430, 860, "#4da3ff"], [740, 860, "#ffd43b"], [260, 1040, "#39e27a"], [600, 1040, "#ff6a3d"]].map(([x, y, c]) => { const g = el("g", {}, road);
        el("rect", { x, y, width: 220, height: 70, rx: 18, fill: c }, g); el("rect", { x: x + 40, y: y - 40, width: 130, height: 50, rx: 14, fill: shade(c, 0.8) }, g);
        el("circle", { cx: x + 50, cy: y + 72, r: 20, fill: "#111" }, g); el("circle", { cx: x + 170, cy: y + 72, r: 20, fill: "#111" }, g); return g; });
      const fight = el("g", { opacity: 0 }, sv); el("rect", { x: 0, y: 1100, width: 1080, height: 820, fill: "#2f6a3a" }, fight);
      const bear = el("g", {}, fight); el("ellipse", { cx: 800, cy: 900, rx: 150, ry: 200, fill: "#6b4423" }, bear); el("circle", { cx: 800, cy: 660, r: 100, fill: "#7a4f2a" }, bear);
      el("circle", { cx: 730, cy: 580, r: 34, fill: "#6b4423" }, bear); el("circle", { cx: 870, cy: 580, r: 34, fill: "#6b4423" }, bear); el("ellipse", { cx: 800, cy: 690, rx: 44, ry: 32, fill: "#c9a07a" }, bear);
      el("circle", { cx: 770, cy: 640, r: 9, fill: "#111" }, bear); el("circle", { cx: 830, cy: 640, r: 9, fill: "#111" }, bear); el("circle", { cx: 800, cy: 676, r: 12, fill: "#111" }, bear);
      const M = finn(fight, 300, 1120, 2.3, { hood: "#ff3b55", arm: "#d02a45", label: "" });
      const fo = at("L15", "Fouls"), hu = at("L15", "Hupen"), l15b = at("L15", 5), l16 = line("L16")[0], ba = at("L16", "Bären");
      tl.fromTo(pitch, { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.6);
      pl.forEach((p, i) => tl.to(p.g, { x: `+=${(i - 1) * 40}`, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut" }, 1));
      cards.forEach((c, i) => tl.fromTo(c, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.2, ease: "back.out(3)" }, fo - 0.2 + i * 0.12));
      tl.to(pitch, { opacity: 0, duration: 0.3 }, l15b - 0.3);
      tl.fromTo(road, { opacity: 0 }, { opacity: 1, duration: 0.3 }, l15b - 0.1);
      cars.forEach((c, i) => tl.to(c, { x: 8, duration: 0.05, repeat: 9, yoyo: true }, hu + i * 0.08));
      tl.fromTo("#s05-hup", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(3)" }, hu - 0.05);
      tl.to(["#s05-hup", road], { opacity: 0, duration: 0.3 }, l16 - 0.2);
      tl.fromTo(fight, { opacity: 0 }, { opacity: 1, duration: 0.3 }, l16);
      armsUp(tl, M, ba - 0.2, 0.25, 160); tl.to(M.g, { scale: 2.6, duration: 0.3, ease: "back.out(2)" }, ba - 0.2);
      tl.fromTo("#s05-vs", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power3.out" }, ba);
      tl.to(bear, { scale: 1.08, svgOrigin: "800 1100", duration: 0.2, yoyo: true, repeat: 3 }, ba + 0.4);''' + OUT)

S['s12'] = (CHIP + '''
    #s12-b { left: 140px; top: 470px; width: 800px; height: 200px; border-radius: 12px; background: #2f5a46; border: 14px solid #8a6a44; color: #f2f7ee; font: 700 70px/170px "Caveat", "Comic Sans MS", cursive; text-align: center; }''',
SVG + '''
      <div id="s12-b" class="abs">Mathe · 8:00 Uhr</div>''',
'''      const sv = document.querySelector("#s12-svg"); sky(sv, "s12g", "#e6dcc6", "#c9b996");
      el("rect", { x: 0, y: 1100, width: 1080, height: 820, fill: "#8d7556" }, sv);
      const T = woman(sv, 900, 1080, 2.0, "#8b5bd6");
      const tears = [0, 1, 2, 3].map((k) => el("ellipse", { cx: 900 + (k % 2 ? 16 : -16) * 2, cy: 1080 - 150 * 2, rx: 6, ry: 10, fill: "#7cc8ff", opacity: 0 }, sv));
      const boys = [[200, "#ff6a3d"], [420, "#4da3ff"], [640, "#39e27a"]].map(([x, c]) => { const f = finn(sv, x, 1190, 1.8, { hood: c, arm: shade(c, 0.85), label: "" });
        el("rect", { x: x - 110, y: 1030, width: 220, height: 24, rx: 6, fill: "#c79a5b" }, sv); el("rect", { x: x - 100, y: 1054, width: 200, height: 140, fill: "#a87d44" }, sv); return f; });
      const wa = at("L16b", "wach"), me = at("L16c", "melden"), we = at("L16c", "weint");
      tl.fromTo("#s12-b", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.6);
      boys.forEach((b, i) => { tl.to(b.head, { y: -6, duration: 0.15, yoyo: true, repeat: 1 }, wa + i * 0.1); tl.to(b.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, wa); });
      boys.forEach((b, i) => tl.to(b.aR, { rotation: -170, svgOrigin: "37 -126", duration: 0.25, ease: "back.out(2)" }, me + i * 0.12));
      tl.to(T.mouth, { attr: { d: "M-6 -147 Q0 -153 6 -147" }, duration: 0.15 }, we);
      tears.forEach((t, k) => tl.fromTo(t, { opacity: 1, y: 0 }, { opacity: 0, y: 140, duration: 0.6, repeat: 2, ease: "power1.in", immediateRender: false }, we + k * 0.15));
      tl.to(T.g, { y: 1074, duration: 0.15, yoyo: true, repeat: 7 }, we);''' + OUT)

S['s06'] = ('''    #s06-n { left: 0; width: 1080px; top: 470px; text-align: center; font: 900 110px Inter, sans-serif; color: #fff; text-shadow: 0 0 40px rgba(255,59,85,.6); }
    #s06-l { left: 0; width: 1080px; top: 600px; text-align: center; font: 700 30px "Space Mono", monospace; color: #ffb3bf; letter-spacing: .2em; }''',
SVG + '''
      <div id="s06-n" class="abs">4.100.000.000</div><div id="s06-l" class="abs">MÄNNER NOCH DABEI</div>''',
'''      const sv = document.querySelector("#s06-svg"); sky(sv, "s06g", "#1a1030", "#090614");
      const G = globe(sv, 540, 930, 230, "s06w", 140, 9); G.dots.forEach((d) => gsap.set(d, { opacity: 1, attr: { fill: "#39e27a" } }));
      const moon = el("g", { opacity: 0 }, sv); el("circle", { cx: 880, cy: 700, r: 60, fill: "#fff6c9" }, moon); el("circle", { cx: 905, cy: 688, r: 54, fill: "#1a1030" }, moon);
      const red = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#c4123a", opacity: 0 }, sv);
      const l18 = line("L18")[0], ta = at("L18", "Tausende"), na = at("L18", "nachts"), ha = at("L19", "Hälfte");
      count(tl, "#s06-n", 4100000000, 2050000000, ta - 0.2, ha - ta + 0.4, "", "", "power1.inOut");
      const half = G.dots.filter((_, i) => i % 2 === 0);
      tl.to(half, { attr: { fill: "#ff3b55" }, duration: 0.1, stagger: { each: (ha - ta) / half.length, from: "random" } }, ta);
      tl.fromTo(moon, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3 }, na - 0.1);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.22, duration: 0.3, yoyo: true, repeat: 5 }, ha - 0.1);
      tl.to("#s06-n", { color: "#ff3b55", scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 }, ha);''' + OUT)

S['s07'] = (CHIP + '''
    #s07-sock { left: 540px; top: 470px; width: 470px; text-align: center; padding: 14px 0; border-radius: 22px; background: rgba(255,255,255,.96); color: #22283f; font: 800 34px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    #s07-sock b { display: block; font: 900 84px Inter, sans-serif; color: #1fa65a; }''',
SVG + '''
      <div id="s07-cl" class="chip" style="left:560px;top:480px"><i>✓</i> freiwillig</div>
      <div id="s07-sock" class="abs">SOCKEN IM WÄSCHEKORB<b id="s07-sn">27</b></div>''',
'''      const sv = document.querySelector("#s07-svg"), W = el("g", {}, sv);
      const R = bedroom(W, "s07g", { w1: "#3b5b8f", w2: "#24385e", floor: "#3a3350" });
      const mess = [], rm = rng(14); for (let i = 0; i < 12; i++) mess.push(el("rect", { x: 120 + rm() * 820, y: 1120 + rm() * 120, width: 60 + rm() * 40, height: 26, rx: 8, fill: ["#ff6a3d", "#4da3ff", "#ffd43b", "#39e27a", "#fff"][i % 5], transform: `rotate(${(rm() - 0.5) * 60} ${540} ${1180})` }, W));
      const Mo = woman(W, 820, 1150, 2.3, "#3aa37a");
      const S = finn(W, 360, 1150, 2.3, { label: "" });
      const sparkle = [0, 1, 2, 3, 4].map((k) => txt(W, 200 + k * 170, 900 - (k % 2) * 80, "✦", 60, "#ffd43b", { opacity: 0 }));
      const bask = el("g", { opacity: 0 }, sv); el("path", { d: "M380 820 H700 L670 1060 H410Z", fill: "#c9a46b" }, bask); for (let k = 0; k < 5; k++) el("line", { x1: 400 + k * 60, y1: 830, x2: 420 + k * 50, y2: 1050, stroke: "#a8834c", "stroke-width": 6 }, bask);
      const socks = [0, 1, 2].map((k) => el("path", { d: `M${470 + k * 60} 800 v50 q0 20 24 20 h20 v-20 h-10 v-50z`, fill: "#fff", stroke: "#22283f", "stroke-width": 3 }, bask));
      const fr = at("L21", "Freiwillig"), au = at("L21", "auf"), l22 = line("L22")[0], so = at("L22", "Socken");
      tl.to(Mo.mouth, { attr: { d: "M-6 -147 Q0 -153 6 -147" }, duration: 0.2 }, 1.2);
      tl.to(Mo.head, { rotation: 8, svgOrigin: "0 -150", duration: 0.3, yoyo: true, repeat: 3 }, 1.3);
      mess.forEach((m, i) => tl.to(m, { x: 360 - (+m.getAttribute("x")), y: 980 - (+m.getAttribute("y")), opacity: 0, duration: 0.3, ease: "power2.in" }, au - 0.6 + i * 0.07));
      for (let k = 0; k < 4; k++) tl.to(S.g, { x: 330 + (k % 2) * 60, duration: 0.2 }, au - 0.6 + k * 0.22);
      tl.to(sparkle, { opacity: 1, scale: 1.3, duration: 0.2, stagger: 0.06, yoyo: true, repeat: 1 }, fr - 0.2);
      tl.fromTo("#s07-cl", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }, fr - 0.1);
      tl.to(["#s07-cl", S.g], { opacity: 0, duration: 0.25 }, l22 - 0.2);
      tl.fromTo(bask, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3 }, l22);
      tl.fromTo("#s07-sock", { opacity: 0 }, { opacity: 1, duration: 0.3 }, l22 + 0.1);
      count(tl, "#s07-sn", 27, 3, so - 0.8, 0.9, "", "", "power2.in");
      tl.to(socks.slice(1), { opacity: 0, y: -40, duration: 0.25, stagger: 0.15 }, so - 0.5);
      tl.to(Mo.mouth, { attr: { d: "M-5 -149 Q0 -152 5 -149" }, duration: 0.2 }, so);''' + OUT)

NAMES = ["Ben", "Jonas", "Luca", "Noah", "Elias", "Paul", "Leon", "Finn", "Emil", "Tim", "Max"]
S['s08'] = (CHIP + '''
    #s08-ch { left: 330px; top: 440px; width: 720px; height: 660px; border-radius: 34px; background: #f1eefa; box-shadow: 0 20px 60px rgba(0,0,0,.5); overflow: hidden; opacity: 0; }
    #s08-ch .hd { height: 84px; background: #ff4fb0; color: #fff; font: 900 38px/84px Inter, sans-serif; text-align: center; }
    #s08-ch .q { margin: 20px 30px 10px; font: 800 34px Inter, sans-serif; color: #22283f; }
    .s08-n { position: absolute; width: 320px; height: 70px; border-radius: 16px; background: #fff; color: #22283f; font: 800 34px/70px Inter, sans-serif; padding-left: 24px; box-shadow: 0 3px 10px rgba(0,0,0,.08); }
    .s08-n i { position: absolute; right: 18px; top: 0; font-style: normal; color: #ff3b55; opacity: 0; font-size: 40px; }''',
SVG + '''
      <div id="s08-ch" class="abs"><div class="hd">Klasse 11b</div><div class="q">Wer hält am längsten durch?</div>
''' + "\n".join(f'        <div id="s08-n{i}" class="s08-n" style="left:{25 + (i % 2) * 345}px;top:{150 + (i // 2) * 82}px">{n}<i>✕</i></div>' for i, n in enumerate(NAMES)) + '''</div>
      <div id="s08-h" class="chip" style="left:620px;top:470px;color:#ff4fb0">♥</div>''',
'''      const sv = document.querySelector("#s08-svg"); sky(sv, "s08g", "#4a2f66", "#1f1236");
      const Lg = lena(sv, 820, 1150, 2.3); gsap.set(Lg.g, { opacity: 0 });
      const l23 = line("L23")[0], we = at("L23", "Wette"), l24 = line("L24")[0], el_ = at("L25", "Elf"), zw = at("L25", "Zwei"), jo = at("L26", "Jonas"), be = at("L26", "beeindruckt");
      tl.fromTo("#s08-ch", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4 }, l24 - 0.4);
      const out = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10].filter((i) => i !== 0);
      out.forEach((i, k) => { tl.to(`#s08-n${i} i`, { opacity: 1, duration: 0.1 }, el_ + k * ((zw - el_) / out.length)); tl.to(`#s08-n${i}`, { opacity: 0.4, duration: 0.15 }, el_ + k * ((zw - el_) / out.length)); });
      tl.to(["#s08-n0", "#s08-n1"], { backgroundColor: "#c9f5d8", duration: 0.2 }, zw);
      tl.to("#s08-n1", { scale: 1.12, backgroundColor: "#ffd43b", duration: 0.25, ease: "back.out(2)" }, jo - 0.1);
      tl.to("#s08-ch", { x: -300, scale: 0.85, duration: 0.35 }, jo);
      tl.fromTo(Lg.g, { opacity: 0, x: 1000 }, { opacity: 1, x: 820, duration: 0.35 }, jo);
      tl.to(Lg.mouth, { attr: { d: "M-7 -153 Q0 -144 7 -153" }, duration: 0.15 }, be);
      tl.fromTo("#s08-h", { opacity: 0, scale: 0.3, y: 40 }, { opacity: 1, scale: 1.3, y: 0, duration: 0.3, ease: "back.out(3)" }, be - 0.05);
      tl.to("#s08-h", { scale: 1.5, duration: 0.25, yoyo: true, repeat: 3 }, be + 0.3);''' + OUT)

S['s09'] = (CARD + '''
    #s09-ok { left: 140px; top: 540px; width: 800px; height: 480px; border-radius: 34px; background: rgba(10,40,28,.95); border: 6px solid #39e27a; box-shadow: 0 0 70px rgba(57,226,122,.5); text-align: center; color: #fff; opacity: 0; }
    #s09-ok .t { margin-top: 200px; font: 900 64px/1.1 Inter, sans-serif; } #s09-ok .t b { color: #39e27a; }
    .s09-c { position: absolute; padding: 16px 34px; border-radius: 24px; background: #ffd43b; color: #22283f; font: 900 56px Inter, sans-serif; opacity: 0; }''',
SVG + '''
      <div id="s09-c1" class="cd" style="top:600px">SUPERKRÄFTE<s></s></div>
      <div id="s09-ok" class="abs"><svg width="150" height="150" viewBox="0 0 160 160" style="position:absolute;left:325px;top:34px"><circle cx="80" cy="80" r="76" fill="#39e27a"/><rect x="66" y="30" width="28" height="100" rx="6" fill="#fff"/><rect x="30" y="66" width="100" height="28" rx="6" fill="#fff"/></svg>
        <div class="t">Balken hobeln =<br><b>normal &amp; gesund</b></div></div>
      <div id="s09-a" class="s09-c" style="left:150px;top:1040px;transform:rotate(-3deg)">SPASS</div><div id="s09-b" class="s09-c" style="left:470px;top:1040px;transform:rotate(2deg)">DISZIPLIN-TEST</div>''',
'''      const sv = document.querySelector("#s09-svg"); sky(sv, "s09g", "#16305e", "#0c1a3a");
      const su = at("L27", "Superkräfte"), l28 = line("L28")[0], ba = at("L28", "Balken"), sp = at("L29", "Spaß"), di = at("L29", "Disziplin");
      tl.fromTo("#s09-c1", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.25, ease: "back.out(2)" }, su - 0.2);
      tl.to("#s09-c1 s", { scaleX: 1, duration: 0.25 }, su + 0.6);
      tl.to("#s09-c1", { opacity: 0, duration: 0.25 }, l28 - 0.2);
      tl.fromTo("#s09-ok", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, ba - 0.2);
      tl.to("#s09-ok", { y: -60, duration: 0.3 }, sp - 0.3);
      tl.fromTo("#s09-a", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, sp - 0.1);
      tl.fromTo("#s09-b", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, di - 0.1);''' + OUT)

S['s13'] = (CHIP + '''
    #s13-sp { left: 470px; top: 470px; width: 520px; padding: 18px 26px; border-radius: 28px 28px 6px 28px; background: #fff; color: #22283f; font: 700 38px/1.25 Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }''',
SVG + '''
      <div id="s13-sp" class="abs">… und dann hat sie mit <b style="color:#ff4fb0">„haha“</b> geantwortet. Was heißt das?</div>''',
'''      const sv = document.querySelector("#s13-svg"); sky(sv, "s13g", "#5a5560", "#3a3640");
      const wall = el("g", {}, sv); for (let r = 0; r < 12; r++) for (let c = 0; c < 6; c++) el("rect", { x: c * 190 - (r % 2) * 95, y: 420 + r * 60, width: 180, height: 52, rx: 4, fill: "#6e6872" }, wall);
      const marks = [], g = el("g", {}, sv); for (let i = 0; i < 29; i++) { const grp = Math.floor(i / 5), k = i % 5, x = 140 + (grp % 3) * 260 + k * 34, y = 470 + Math.floor(grp / 3) * 200;
        marks.push(k === 4 ? el("line", { x1: x - 150, y1: y + 120, x2: x + 10, y2: y + 20, stroke: "#f2efe6", "stroke-width": 10, "stroke-linecap": "round", opacity: 0 }, g) : el("line", { x1: x, y1: y, x2: x, y2: y + 140, stroke: "#f2efe6", "stroke-width": 10, "stroke-linecap": "round", opacity: 0 }, g)); }
      const P = finn(sv, 540, 1180, 2.1, { hood: "#ff8a3d", arm: "#e06e2a", label: "29" });
      const kit = el("g", { opacity: 0 }, sv); sky(kit, "s13k", "#e9e4d6", "#cfc8b4"); el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#a68f6c" }, kit);
      const fr = el("g", {}, kit); el("rect", { x: 120, y: 520, width: 300, height: 600, rx: 26, fill: "#f4f6fa", stroke: "#c4cad6", "stroke-width": 6 }, fr); el("line", { x1: 120, y1: 760, x2: 420, y2: 760, stroke: "#c4cad6", "stroke-width": 6 }, fr);
      el("rect", { x: 380, y: 600, width: 16, height: 100, rx: 8, fill: "#9aa3b5" }, fr); el("rect", { x: 380, y: 800, width: 16, height: 120, rx: 8, fill: "#9aa3b5" }, fr);
      const K = finn(kit, 640, 1180, 2.2, { hood: "#4da3ff", arm: "#2f7fd6", label: "" });
      const l29b = line("L29b")[0], ge = at("L29b", "Gefängnis"), l29c = line("L29c")[0], ku = at("L29c", "Kühlschrank"), gf = at("L29c", "Gefühlen");
      tl.to(marks, { opacity: 1, duration: 0.06, stagger: (ge - l29b) / 29 }, l29b);
      tl.to(P.mouth, { attr: { d: "M-6 -148 Q0 -153 6 -148" }, duration: 0.2 }, ge);
      tl.to(P.g, { y: 1190, duration: 0.4, yoyo: true, repeat: 1 }, ge);
      tl.to([wall, g, P.g], { opacity: 0, duration: 0.25 }, l29c - 0.2); tl.to(kit, { opacity: 1, duration: 0.3 }, l29c - 0.1);
      tl.to(K.head, { rotation: -10, svgOrigin: "0 -150", duration: 0.3 }, ku - 0.1);
      tl.fromTo("#s13-sp", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ku);
      tl.to(fr, { x: 5, duration: 0.05, repeat: 5, yoyo: true }, gf);''' + OUT)

S['s10'] = (CHIP + '''
    #s10-so { left: 0; right: 0; margin: 0 auto; top: 470px; width: fit-content; padding: 12px 34px; border-radius: 16px; background: #ff3b55; color: #fff; font: 900 64px Inter, sans-serif; letter-spacing: .08em; opacity: 0; transform: rotate(-6deg); box-shadow: 0 0 40px rgba(255,59,85,.7); }
    #s10-ss { left: 0; width: 1080px; top: 480px; text-align: center; font: 900 110px/1 Inter, sans-serif; color: #ffd43b; text-shadow: 0 0 60px rgba(255,212,59,.9); opacity: 0; }''',
SVG + '''
      <div id="s10-ss" class="abs">SACK-<br>SILVESTER</div>
      <div id="s10-so" class="abs">AUSVERKAUFT</div>
      <div id="s10-h" class="chip" style="left:470px;top:560px;color:#ff4fb0;font-size:90px">♥</div>''',
'''      const sv = document.querySelector("#s10-svg"); sky(sv, "s10g", "#140f30", "#05030f");
      const city = skyline(sv, 1130, 31, ["#2a2a55", "#33336a", "#24244a"], 10, 200, 520);
      el("rect", { x: 0, y: 1130, width: 1080, height: 790, fill: "#0e0c22" }, sv);
      const fw = [], rf = rng(17); for (let i = 0; i < 12; i++) fw.push(burst(sv, 100 + rf() * 880, 480 + rf() * 420, ["#ff4fb0", "#ffd43b", "#39e27a", "#4da3ff", "#ff6a3d"][i % 5], 14, 60 + rf() * 60));
      const shop = el("g", { opacity: 0 }, sv); sky(shop, "s10s", "#f2f0ea", "#d8d4c8");
      for (let r = 0; r < 3; r++) { el("rect", { x: 80, y: 600 + r * 180, width: 920, height: 20, fill: "#9aa3b5" }, shop); }
      const boxes = []; for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) boxes.push(el("rect", { x: 100 + c * 150, y: 500 + r * 180, width: 130, height: 100, rx: 10, fill: "#8ad0ff" }, shop));
      const date = el("g", { opacity: 0 }, sv); sky(date, "s10d", "#ff9ec9", "#b5528a");
      const Lg = lena(date, 400, 1150, 2.4), J = finn(date, 700, 1150, 2.4, { hood: "#3aa37a", arm: "#2f8a65", cap: "#22283f", label: "" });
      const mi = at("L30", "Mitternacht"), gl = at("L31", "gleichzeitig"), sa = at("L31", "Sack"), l32 = line("L32")[0], le = at("L32", "leer"), l33 = line("L33")[0], da = at("L33", "Date"), jo = at("L33", "Jonas");
      city.out.forEach((b, i) => tl.to(b.wins, { opacity: 0.12, duration: 0.05, stagger: 0.01 }, mi - 0.3));
      fw.forEach((f, i) => { const t = gl - 0.2 + (i % 6) * 0.25 + Math.floor(i / 6) * 0.9;
        tl.fromTo(f.g, { opacity: 1, scale: 0.1, svgOrigin: `${f.rays[0].getAttribute("x1")} ${f.rays[0].getAttribute("y1")}` }, { opacity: 1, scale: 1, svgOrigin: `${f.rays[0].getAttribute("x1")} ${f.rays[0].getAttribute("y1")}`, duration: 0.45, ease: "power3.out", immediateRender: false }, t);
        tl.to(f.g, { opacity: 0, duration: 0.4 }, t + 0.5); });
      tl.fromTo("#s10-ss", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.in" }, sa - 0.15);
      tl.to(sv, { x: 10, duration: 0.04, repeat: 9, yoyo: true }, sa + 0.1);
      tl.to("#s10-ss", { opacity: 0, duration: 0.25 }, l32 - 0.2);
      tl.to(shop, { opacity: 1, duration: 0.3 }, l32 - 0.1);
      tl.to(boxes, { opacity: 0, y: -30, duration: 0.15, stagger: { each: 0.03, from: "random" } }, l32 + 0.2);
      tl.fromTo("#s10-so", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, le - 0.1);
      tl.to("#s10-so", { opacity: 0, duration: 0.2 }, l33 - 0.2); tl.to(date, { opacity: 1, duration: 0.3 }, l33 - 0.1);
      tl.to(Lg.mouth, { attr: { d: "M-7 -153 Q0 -144 7 -153" }, duration: 0.15 }, da); tl.to(J.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, jo);
      tl.fromTo("#s10-h", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, da - 0.05);
      tl.to("#s10-h", { scale: 1.25, duration: 0.25, yoyo: true, repeat: 5 }, da + 0.3);
      tl.to(Lg.g, { x: 450, duration: 0.4 }, jo); tl.to(J.g, { x: 650, duration: 0.4 }, jo);''' + OUT)

S['s11'] = ('''    #s11-t { left: 0; width: 1080px; top: 440px; text-align: center; color: #fff; font: 900 104px/1 Inter, sans-serif; text-shadow: 0 0 40px rgba(255,79,176,.6); opacity: 0; }
    #s11-t small { display: block; margin-top: 20px; font: 800 40px Inter, sans-serif; color: #ff8fd0; letter-spacing: .2em; }
    .s11-b { position: absolute; top: 760px; width: 440px; height: 150px; border-radius: 30px; text-align: center; color: #fff; font: 900 56px/150px Inter, sans-serif; opacity: 0; }
    #s11-y { left: 60px; background: #1fa65a; box-shadow: 0 0 50px rgba(57,226,122,.6); } #s11-n { left: 580px; background: #d63d9a; box-shadow: 0 0 50px rgba(255,79,176,.6); }''',
'''      <div id="s11-t" class="abs">Und du?<small>HEUTE IST TAG 1</small></div>
      <div id="s11-y" class="s11-b">ICH MACH MIT</div><div id="s11-n" class="s11-b">TEAM LENA</div>''',
'''      const st = document.querySelector("#s11-stage"), sv = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st.insertBefore(sv, st.firstChild); sky(sv, "s11g", "#2a1f4f", "#0f0b22");
      const ic = at("L34", "Ich"), te = at("L34", "Team");
      tl.fromTo("#s11-t", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.1);
      tl.fromTo("#s11-y", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, ic - 0.1);
      tl.fromTo("#s11-n", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, te - 0.1);
      tl.to(["#s11-y", "#s11-n"], { scale: 1.06, duration: 0.35, yoyo: true, repeat: 9, ease: "sine.inOut", stagger: 0.35 }, te + 0.4);''')
here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
