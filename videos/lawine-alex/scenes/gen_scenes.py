#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Lawine Alex“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
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

S['s01'] = ('''    #s01-t { left: 50px; right: 50px; top: 230px; text-align: center; color: #fff; font: 500 92px/1.08 "EB Garamond", serif; text-shadow: 0 3px 22px rgba(0,0,0,.7); }
    #s01-t em { font-style: normal; color: #9dd6ff; text-shadow: 0 0 40px rgba(157,214,255,.9), 0 3px 22px rgba(0,0,0,.6); } #s01-t b { font-weight: 600; color: #ff5a5f; text-shadow: 0 0 40px rgba(255,90,95,.9); }
    #s01-live { left: 0; right: 0; top: 160px; margin: 0 auto; width: fit-content; padding: 6px 18px; border-radius: 10px; background: #e0484f; color: #fff; font: 700 30px Inter, sans-serif; letter-spacing: .12em; }
    #s01-tag { left: 600px; top: 520px; padding: 8px 18px; border-radius: 12px; background: rgba(255,255,255,.95); color: #22283f; font: 600 40px "EB Garamond", serif; opacity: 0; }''',
SVG + '''
      <div id="s01-live" class="abs">● 1 ÜBERLEBENDER</div>
      <div id="s01-t" class="abs">Die ganze Welt unter <em>Schnee</em>.<br>Nur <b>du</b> überlebst.</div>
      <div id="s01-tag" class="abs">Alex · 24</div>''',
'''      const sv = document.querySelector("#s01-svg");
      sky(sv, "s01-s", "#1c2748", "#7d8fb5");
      const W = el("g", {}, sv);
      skyline(W, 1080, 3, ["#33405f", "#3b4a6c"], 8, 200, 420);
      const S2 = skyline(W, 1120, 5, ["#4e5b7e", "#5b6a8f"], 7, 260, 520);
      snowLayer(W, 960, "#dfe9f5");
      el("rect", { x: 470, y: 860, width: 140, height: 420, fill: "#3b4766" }, W); el("rect", { x: 462, y: 850, width: 156, height: 22, fill: "#f4f8fc" }, W);
      snowLayer(W, 1050, "#f2f7fc");
      const beam = el("path", { d: "M555 800 L760 700 L780 780Z", fill: "#fff6c8", opacity: 0.55 }, W);
      const A = alex(W, 540, 852, 1.1);
      const sf = snowfall(sv, 90, 7, -200, 1400);
      const al = at("L2", "Alex"), le = at("L2", "letzte"), l3 = line("L3")[0], al2 = at("L3", "alles");
      fall(tl, sf, C.__dur);
      tl.fromTo(W, { scale: 1, svgOrigin: "540 850" }, { scale: 1.35, svgOrigin: "540 850", duration: C.__dur, ease: "power1.inOut" }, 0);
      tl.fromTo("#s01-t em", { opacity: 1 }, { opacity: 0.45, duration: 0.08, repeat: 9, yoyo: true }, 0.2);
      tl.fromTo("#s01-t", { scale: 1.12 }, { scale: 1, duration: 0.6, ease: "power3.out" }, 0);
      tl.to("#s01-t b", { scale: 1.2, duration: 0.25, repeat: 7, yoyo: true, ease: "sine.inOut", display: "inline-block" }, 0.4);
      tl.fromTo("#s01-live", { opacity: 1 }, { opacity: 0.3, duration: 0.3, repeat: 13, yoyo: true }, 0);
      tl.fromTo(beam, { attr: { opacity: 0.55 } }, { attr: { opacity: 0.25 }, duration: 0.5, repeat: 9, yoyo: true }, 0);
      tl.to(["#s01-t", "#s01-live"], { opacity: 0, y: -30, duration: 0.35 }, al - 0.3);
      tl.fromTo("#s01-tag", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, al);
      tl.to(A, { y: 840, duration: 0.15, yoyo: true, repeat: 1 }, le);
      tl.to("#s01-tag", { opacity: 0, duration: 0.3 }, l3);''' + OUT)

S['s02'] = (BIG, SVG + '''
      <div id="s02-big" class="big"><b>40 m</b><i>SCHNEE IN UNTER 1 MINUTE</i></div>''',
'''      const sv = document.querySelector("#s02-svg");
      sky(sv, "s02-s", "#9cc4e8", "#e4eef7");
      const W = el("g", {}, sv);
      skyline(W, 1150, 3, ["#8090b4", "#8a9abd"], 8, 260, 480);
      const back = skyline(W, 1200, 5, ''' + COLS + ''', 7, 300, 560);
      el("rect", { x: 470, y: 760, width: 140, height: 460, fill: "#55627f" }, W); el("rect", { x: 462, y: 750, width: 156, height: 20, fill: "#7c88ad" }, W);
      el("rect", { x: 0, y: 1200, width: 1080, height: 400, fill: "#4a4f60" }, W);
      const cars = []; for (let i = 0; i < 6; i++) cars.push(el("rect", { x: 60 + i * 170, y: 1180, width: 90, height: 34, rx: 10, fill: ["#e8484f", "#4da3ff", "#ffd56b"][i % 3] }, W));
      const A = alex(W, 540, 752, 0.9);
      const wave = el("path", { d: "M-1400 1300 Q-900 600 -500 760 Q-300 820 -200 740 L-200 1600 L-1400 1600Z", fill: "#f4f8fc" }, sv);
      const fill = el("rect", { x: 0, y: 1600, width: 1080, height: 1500, fill: "#eef4fb" }, sv);
      const mist = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#ffffff", opacity: 0 }, sv);
      const gr = at("L4", "Grollen"), ww = at("L4", "weiße"), da = at("L5", "Dach"), aw = at("L5", "alles"), l5b = line("L5b")[0], vm = at("L5b", "vierzig");
      cars.forEach((c, i) => tl.to(c, { x: (i % 2 ? -1 : 1) * 200, duration: 3, ease: "none" }, 0));
      tl.to(W, { x: 8, duration: 0.05, repeat: 19, yoyo: true }, gr);
      tl.to(wave, { x: 2600, duration: 2.6, ease: "power1.in" }, ww - 0.2);
      tl.to(fill, { attr: { y: 770 }, duration: 2.2, ease: "power2.inOut" }, ww + 0.3);
      tl.to(mist, { opacity: 0.45, duration: 0.6, yoyo: true, repeat: 1 }, ww + 0.8);
      tl.to(W, { scale: 1.25, svgOrigin: "540 760", duration: 1.5, ease: "power2.inOut" }, da - 0.4);
      tl.to(A, { y: 742, duration: 0.15, yoyo: true, repeat: 3 }, aw);
      tl.fromTo("#s02-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, vm - 0.2);''' + OUT)

S['s03'] = (BIG + '''
    #s03-ch { left: 140px; top: 760px; width: 800px; height: 380px; opacity: 0; }''' + FLAT2, SVG + '''
      <div id="s03-big" class="big"><b>90 %</b><i>ÜBERLEBEN DIE ERSTEN 15 MINUTEN</i></div>
      <svg id="s03-ch" class="abs" viewBox="0 0 800 380"><rect x="0" y="0" width="800" height="380" rx="24" fill="rgba(13,16,38,.75)"/>
        <path d="M80 320 H740 M80 320 V40" stroke="#fff" stroke-opacity=".5" stroke-width="4" fill="none"/>
        <path id="s03-cv" d="M80 70 L280 80 Q380 100 430 220 Q520 300 740 305" stroke="#ff5a5f" stroke-width="10" fill="none" stroke-dasharray="900" stroke-dashoffset="900" stroke-linecap="round"/>
        <text x="80" y="360" font-family="Inter" font-size="28" fill="#fff">0</text><text x="400" y="360" font-family="Inter" font-size="28" fill="#fff">35 MIN</text><text x="690" y="360" font-family="Inter" font-size="28" fill="#fff">2 STD</text></svg>
      <div id="s03-ph" class="fc" style="left:290px;top:640px;width:500px">📵<br><b>KEIN NETZ</b></div>''',
'''      const sv = document.querySelector("#s03-svg");
      sky(sv, "s03-s", "#a9c2dc", "#eef3f8");
      const P = iso(540, 820, 70), w = el("g", {}, sv);
      box(P, w, -1, -1, -0.4, 8, 8, 0.4, "#f2f7fc");
      for (let k = 0; k < 7; k++) box(P, w, 0.5 + (k % 3) * 1.6, 3.6 + Math.floor(k / 3) * 1.2, 0, 0.9, 0.9, 0.35 + (k % 2) * 0.2, "#e6eef7");
      const hole = el("ellipse", { cx: P(3, 3, 0)[0], cy: P(3, 3, 0)[1], rx: 30, ry: 16, fill: "#b9c9dc" }, w);
      const me = person(P, w, 3.4, 3.2, 0, { shirt: "#e8484f", pants: "#2a3060" });
      const chunks = []; const r = rng(4); for (let i = 0; i < 12; i++) chunks.push(el("circle", { cx: P(3, 3, 0)[0], cy: P(3, 3, 0)[1], r: 6 + r() * 6, fill: "#ffffff" }, w));
      const sf = snowfall(sv, 60, 9, -200, 1300);
      const br = at("L6", "Bleib"), l7 = line("L7")[0], n90 = at("L7", "90"), ra = at("L7", "rapide"), l8 = line("L8")[0], kv = at("L8", "keine"), l8b = line("L8b")[0], kn = at("L8b", "Kein");
      fall(tl, sf, C.__dur);
      tl.to(me, { y: -6, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }, br);
      tl.fromTo("#s03-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, n90 - 0.3);
      tl.to(w, { opacity: 0.25, duration: 0.3 }, n90);
      tl.to("#s03-ch", { opacity: 1, duration: 0.3 }, n90 + 0.2);
      tl.to("#s03-cv", { attr: { "stroke-dashoffset": 0 }, duration: 2.0, ease: "power1.inOut" }, n90 + 0.3);
      tl.to(["#s03-big", "#s03-ch"], { opacity: 0, duration: 0.3 }, l8 - 0.3);
      tl.to(w, { opacity: 1, duration: 0.3 }, l8 - 0.3);
      chunks.forEach((c, i) => tl.fromTo(c, { x: 0, y: 0, opacity: 1 }, { x: (i % 2 ? 1 : -1) * (40 + i * 8), y: -80 - (i % 3) * 30, opacity: 0, duration: 0.5, ease: "power2.out", repeat: 3 }, l8 + i * 0.05));
      tl.to(hole, { attr: { rx: 60, ry: 32 }, duration: 2 }, l8);
      tl.to(me, { y: 8, duration: 0.15, yoyo: true, repeat: 11 }, l8);
      tl.fromTo("#s03-ph", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, kn - 0.2);''' + OUT)

S['s04'] = (BIG + FLAT2 + '''
    .s04-w { left: 340px; width: 660px; padding: 14px 20px; }''', SVG + '''
      <div id="s04-big" class="big"><b>25×</b><i>SCHNELLER AUSGEKÜHLT · NASSE KLEIDUNG</i></div>
      <div id="s04-w1" class="fc s04-w" style="top:580px"><b>Zittern</b></div><div id="s04-w2" class="fc s04-w" style="top:700px"><b>Verwirrung</b></div><div id="s04-w3" class="fc s04-w" style="top:820px"><b>Blaue Lippen</b></div>''',
'''      const sv = document.querySelector("#s04-svg");
      sky(sv, "s04-s", "#8ea6c4", "#dfe7f0");
      const P = iso(540, 900, 110), w = el("g", {}, sv);
      box(P, w, -2, -2, -0.3, 7, 7, 0.3, "#f2f7fc");
      const me = person(P, w, 1.2, 1.2, 0, { shirt: "#e8484f", pants: "#2a3060" });
      const l2 = box(P, w, 1.14, 1.14, 0.7, 0.52, 0.58, 0.82, "#5a7bd6", { opacity: 0 }), l3 = box(P, w, 1.1, 1.1, 0.72, 0.6, 0.66, 0.82, "#3d4a7a", { opacity: 0 });
      const wind = []; for (let i = 0; i < 6; i++) wind.push(el("path", { d: `M${-200} ${620 + i * 90} q200 -30 400 0 t400 0`, stroke: "#ffffff", "stroke-width": 6, fill: "none", opacity: 0.6, "stroke-linecap": "round" }, sv));
      const sf = snowfall(sv, 70, 11, -200, 1300);
      const n25 = at("L9", "25"), l10 = line("L10")[0], sc = at("L10", "Schicht"), wi = at("L10", "Wind"), l10b = line("L10b")[0], zi = at("L10b", "Zittern"), ve = at("L10b", "Verwirrung"), bl = at("L10b", "blaue"), le = at("L10b", "lebensgefährlich");
      fall(tl, sf, C.__dur);
      wind.forEach((wl, i) => tl.fromTo(wl, { x: 0 }, { x: 1300, duration: 1.6, repeat: 3, ease: "none" }, i * 0.2));
      tl.to(me, { x: 4, duration: 0.05, repeat: 21, yoyo: true }, 0.2);
      tl.fromTo("#s04-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, n25 - 0.3);
      tl.to("#s04-big", { opacity: 0, duration: 0.3 }, l10 - 0.2);
      tl.to(l2, { opacity: 1, duration: 0.2 }, sc); tl.to(l3, { opacity: 1, duration: 0.2 }, sc + 0.5);
      tl.to(wind, { opacity: 0, duration: 0.4 }, wi);
      tl.to(w, { opacity: 0.3, duration: 0.3 }, l10b);
      [["#s04-w1", zi], ["#s04-w2", ve], ["#s04-w3", bl]].forEach(([id, t]) => tl.fromTo(id, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, t - 0.1));
      tl.to([".s04-w"], { x: 8, duration: 0.04, repeat: 7, yoyo: true }, le);''' + OUT)

S['s05'] = ('''    .tl { position: absolute; font: 600 44px "EB Garamond", serif; text-shadow: 0 2px 10px rgba(0,0,0,.6); opacity: 0; }''', SVG + '''
      <div id="s05-in" class="tl" style="left:470px;top:860px;color:#6be3a0;font-size:60px">0 °C</div><div id="s05-out" class="tl" style="left:760px;top:600px;color:#9dbcff">−20 °C</div>
      <div id="s05-co" class="tl" style="left:640px;top:760px;color:#ff5a5f;font-size:60px">CO ✕</div>''',
'''      const sv = document.querySelector("#s05-svg");
      sky(sv, "s05-s", "#2a3150", "#8a90ad");
      const W = el("g", {}, sv);
      const sk = skyline(W, 1150, 13, ''' + COLS + ''', 8, 300, 560);
      snowLayer(W, 1010, "#dfe9f5");
      const tls = []; [180, 540, 900].forEach((x) => { el("rect", { x: x - 12, y: 900, width: 24, height: 120, fill: "#2a2f40" }, W); tls.push(el("circle", { cx: x, cy: 900, r: 16, fill: "#39e27a" }, W)); });
      const cave = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#e8f0f8" }, cave);
      el("path", { d: "M160 1180 Q160 760 540 740 Q920 760 920 1180Z", fill: "#3a4566" }, cave);
      el("path", { d: "M200 1180 Q210 800 540 785 Q870 800 880 1180Z", fill: "#56628a" }, cave);
      const cand = el("g", {}, cave); el("rect", { x: 620, y: 1110, width: 26, height: 60, fill: "#f4f0e6" }, cand); const fl = el("ellipse", { cx: 633, cy: 1098, rx: 10, ry: 18, fill: "#ffcf6b" }, cand);
      const glow = el("circle", { cx: 633, cy: 1100, r: 120, fill: "#ffcf6b", opacity: 0.18 }, cave);
      alex(cave, 440, 1180, 1.4);
      const hole = el("path", { d: "M540 740 V600", stroke: "#e8f0f8", "stroke-width": 26, opacity: 0 }, cave);
      const air = []; for (let i = 0; i < 4; i++) air.push(el("circle", { cx: 540, cy: 720, r: 10 + i * 4, fill: "#ffffff", opacity: 0 }, cave));
      const dark = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#060814", opacity: 0 }, sv);
      const am = at("L11", "Ampeln"), he = at("L11", "Heizungen"), l12 = line("L12")[0], nu = at("L12", "null"), mz = at("L12", "minus"), l12b = line("L12b")[0], lu = at("L12b", "Luftloch"), ko = at("L12b", "Kohlenmonoxid");
      const wins = sk.out.flatMap((b) => b.wins).filter((w) => +w.getAttribute("opacity") > 0.5);
      wins.forEach((w, i) => tl.to(w, { attr: { opacity: 0.08 }, duration: 0.05 }, 0.6 + (i % 40) * 0.05 + Math.floor(i / 40) * 0.3));
      tl.to(tls, { attr: { fill: "#2a2f40" }, duration: 0.05, stagger: 0.15 }, am);
      tl.to(dark, { opacity: 0.45, duration: 1.2 }, he);
      tl.set(W, { opacity: 0 }, l12 - 0.1); tl.set(dark, { opacity: 0 }, l12 - 0.1); tl.set(cave, { opacity: 1 }, l12 - 0.1);
      tl.fromTo(cave, { scale: 1.2, svgOrigin: "540 1000" }, { scale: 1, svgOrigin: "540 1000", duration: 0.6, ease: "power3.out", immediateRender: false }, l12 - 0.1);
      tl.to(fl, { attr: { ry: 22 }, duration: 0.15, yoyo: true, repeat: 30 }, l12);
      tl.fromTo("#s05-in", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3 }, nu - 0.1);
      tl.fromTo("#s05-out", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3 }, mz - 0.1);
      tl.to(hole, { opacity: 1, duration: 0.3 }, lu - 0.1);
      air.forEach((a, i) => tl.fromTo(a, { opacity: 0.8, y: 0 }, { opacity: 0, y: -120, duration: 0.8, repeat: 2 }, lu + i * 0.2));
      tl.fromTo("#s05-co", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ko - 0.1);''' + OUT)

S['s06'] = (BIG + FLAT2, SVG + '''
      <div id="s06-big" class="big"><b>4.000</b><i>KALORIEN AM TAG IN DER KÄLTE</i></div>''',
'''      const sv = document.querySelector("#s06-svg");
      sky(sv, "s06-s", "#b8cde2", "#eef3f8");
      const P = iso(540, 820, 90), k = el("g", {}, sv);
      box(P, k, -1, -1, -0.3, 7, 7, 0.3, "#e6eef7");
      box(P, k, 1.5, 1.5, 0, 1.6, 1.6, 0.35, "#4a4f60");
      box(P, k, 1.8, 1.8, 0.35, 1.0, 1.0, 0.55, "#8a8f9c"); const snow = box(P, k, 1.85, 1.85, 0.9, 0.9, 0.9, 0.25, "#ffffff");
      const fl = el("ellipse", { cx: P(2.3, 2.3, 0.35)[0], cy: P(2.3, 2.3, 0.35)[1] + 10, rx: 60, ry: 18, fill: "#4da3ff", opacity: 0 }, k);
      const steam = []; for (let i = 0; i < 4; i++) steam.push(el("circle", { cx: P(2.3, 2.3, 1.2)[0] + (i - 1.5) * 26, cy: P(2.3, 2.3, 1.2)[1], r: 22, fill: "#ffffff", opacity: 0 }, k));
      const sb = el("g", { opacity: 0 }, sv); el("circle", { cx: 300, cy: 760, r: 80, fill: "#ffffff" }, sb); txt(sb, 300, 800, "✕", 160, "#e0484f");
      const fr = el("g", { opacity: 0 }, sv);
      el("rect", { x: 120, y: 600, width: 840, height: 560, rx: 20, fill: "#2c3550" }, fr);
      [760, 920, 1080].forEach((y) => el("rect", { x: 140, y, width: 800, height: 12, fill: "#9aa6c4" }, fr));
      for (let i = 0; i < 18; i++) el("rect", { x: 160 + (i % 6) * 128, y: 680 + Math.floor(i / 6) * 160, width: 100, height: 70, rx: 10, fill: ["#e8484f", "#ffd56b", "#6be3a0", "#ff8fd0", "#9dbcff", "#ffffff"][i % 6] }, fr);
      el("rect", { x: 120, y: 600, width: 840, height: 560, rx: 20, fill: "#dff1ff", opacity: 0.35 }, fr);
      const is = at("L13", "Iss"), l14 = line("L14")[0], ke = at("L14", "Kerze"), l15 = line("L15")[0], ge = at("L15", "Gefrierschrank"), l15b = line("L15b")[0], n4 = at("L15b", "4.000");
      tl.fromTo(sb, { opacity: 0, scale: 0.5, svgOrigin: "300 760" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, is);
      tl.to(sb, { opacity: 0, duration: 0.2 }, l14 - 0.2);
      tl.to(fl, { opacity: 1, duration: 0.2 }, ke - 0.2);
      tl.to(snow, { scaleY: 0.2, svgOrigin: `${P(2.3, 2.3, 0.9).join(" ")}`, opacity: 0.4, duration: 2.5 }, ke);
      steam.forEach((s, i) => tl.fromTo(s, { opacity: 0.8, y: 0 }, { opacity: 0, y: -160, duration: 1.2, repeat: 2 }, ke + i * 0.25));
      tl.to(k, { opacity: 0, duration: 0.3 }, l15 - 0.2);
      tl.fromTo(fr, { opacity: 0, scale: 0.85, svgOrigin: "540 880" }, { opacity: 1, scale: 1, svgOrigin: "540 880", duration: 0.45, ease: "back.out(1.6)" }, l15 - 0.1);
      tl.to(fr, { opacity: 0.25, duration: 0.3 }, l15b - 0.1);
      tl.fromTo("#s06-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, n4 - 0.3);''' + OUT)

S['s07'] = ('', SVG,
'''      const sv = document.querySelector("#s07-svg");
      sky(sv, "s07-s", "#05070f", "#141a2e");
      const roof = el("g", {}, sv);
      el("rect", { x: 0, y: 1000, width: 1080, height: 600, fill: "#cfd9e6" }, roof);
      const rad = el("g", {}, roof); el("rect", { x: 300, y: 900, width: 160, height: 100, rx: 14, fill: "#2a2f40" }, rad); el("path", { d: "M440 900 L500 790", stroke: "#8a8f9c", "stroke-width": 8 }, rad);
      const waves = [1, 2, 3].map((i) => el("path", { d: `M${500 + i * 30} ${790 - i * 10} q${20 + i * 10} ${20 + i * 10} 0 ${40 + i * 20}`, stroke: "#9dbcff", "stroke-width": 6, fill: "none", opacity: 0 }, rad));
      const beam = el("path", { d: "M640 940 L1080 600 L1080 780Z", fill: "#fff6c8", opacity: 0 }, roof);
      alex(roof, 600, 1000, 1.3);
      const yard = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#9eacbf" }, yard);
      el("path", { d: "M640 1240 Q640 1040 860 1030 Q1080 1040 1080 1240Z", fill: "#e6eef7" }, yard); el("path", { d: "M780 1240 Q780 1150 860 1145 Q940 1150 940 1240Z", fill: "#0b0f1c" }, yard);
      const prints = []; for (let i = 0; i < 9; i++) { const x = 120 + i * 78, y = 760 + i * 52 + (i % 2 ? 22 : -22);
        prints.push(el("ellipse", { cx: x, cy: y, rx: 18, ry: 30, fill: "#6d7f98", opacity: 0, transform: `rotate(-40 ${x} ${y})` }, yard)); }
      const dark = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#000", opacity: 0 }, sv);
      const red = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#8a0f1c", opacity: 0 }, sv);
      const ra = at("L16", "Radio"), li = at("L16", "Licht"), l17 = line("L17")[0], st = at("L17", "Stille"), l18 = line("L18")[0], fu = at("L18", "Fußspuren"), l19 = line("L19")[0], hoe = at("L19", "Höhle"), l20 = line("L20")[0], ni = at("L20", "nicht");
      waves.forEach((w, i) => tl.fromTo(w, { opacity: 0 }, { opacity: 1, duration: 0.2, repeat: 7, yoyo: true }, ra + i * 0.12));
      tl.to(beam, { opacity: 0.5, duration: 0.1, repeat: 9, yoyo: true }, li);
      tl.to(dark, { opacity: 0.85, duration: 0.8 }, st - 0.3);
      tl.set(roof, { opacity: 0 }, l18 - 0.1); tl.to(dark, { opacity: 0.35, duration: 0.6 }, l18 - 0.1); tl.set(yard, { opacity: 1 }, l18 - 0.1);
      tl.fromTo(yard, { scale: 1.3, svgOrigin: "540 1000" }, { scale: 1, svgOrigin: "540 1000", duration: 3, ease: "power1.out", immediateRender: false }, l18 - 0.1);
      prints.forEach((p, i) => tl.to(p, { opacity: 1, duration: 0.15 }, fu + i * ((hoe - fu) / 9)));
      tl.to(yard, { scale: 1.25, svgOrigin: "860 1200", duration: 2.4, ease: "power2.in" }, hoe);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.55, duration: 0.15, repeat: 3, yoyo: true }, ni);
      tl.to(dark, { opacity: 1, duration: 0.6 }, C.__dur - 0.6);''')

S['s08'] = ('''    #s08-t { left: 0; width: 1080px; top: 620px; text-align: center; color: #fff; font: 500 170px/1 "EB Garamond", serif; text-shadow: 0 0 40px rgba(255,90,95,.6); opacity: 0; }
    #s08-s { left: 0; width: 1080px; top: 820px; text-align: center; color: #ff8fd0; font: 600 34px Inter, sans-serif; letter-spacing: .3em; opacity: 0; }
    #s08-f { left: 330px; top: 960px; width: 420px; height: 110px; border-radius: 55px; background: #ff3b5c; color: #fff; text-align: center; font: 800 52px/110px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 40px rgba(255,59,92,.5); }''',
'''      <div id="s08-t" class="abs">Teil 2?</div><div id="s08-s" class="abs">WER STEHT DA DRAUSSEN</div><div id="s08-f" class="abs">+ Folgen</div>''',
'''      const fo = at("L21", "folg"), l22 = line("L22")[0];
      tl.fromTo("#s08-t", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }, 0.1);
      tl.fromTo("#s08-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s08-f", { scale: 1.06, duration: 0.3, yoyo: true, repeat: 13, ease: "sine.inOut" }, fo + 0.4);
      tl.fromTo("#s08-s", { opacity: 0 }, { opacity: 1, duration: 0.5 }, l22);
      tl.to("#s08-t", { opacity: 0.6, duration: 0.08, repeat: 5, yoyo: true }, l22 + 0.5);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
