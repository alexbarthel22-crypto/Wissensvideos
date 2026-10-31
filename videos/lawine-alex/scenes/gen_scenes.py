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

S['s01'] = ('''    #s01-t { left: 20px; right: 20px; top: 360px; text-align: center; color: #fff; font: 600 150px/0.96 "EB Garamond", serif; text-shadow: 0 0 6px rgba(0,0,0,.9), 0 6px 34px rgba(0,0,0,.9); }
    #s01-t em { font-style: normal; color: #9dd6ff; text-shadow: 0 0 50px rgba(157,214,255,1), 0 6px 30px rgba(0,0,0,.7); }
    #s01-t small { display: block; margin-top: 24px; font-size: 84px; } #s01-t b { display: block; font-size: 128px; color: #ff4b52; text-shadow: 0 0 60px rgba(255,75,82,1), 0 6px 30px rgba(0,0,0,.7); }
    #s01-frame { left: 0; top: 0; width: 1080px; height: 1920px; box-shadow: inset 0 0 0 16px rgba(224,72,79,.9), inset 0 0 120px rgba(224,72,79,.6); opacity: 0; }
    #s01-warn { left: 455px; top: 110px; width: 170px; height: 153px; filter: drop-shadow(0 0 24px rgba(255,212,59,.8)); }
    #s01-live { left: 0; right: 0; top: 290px; margin: 0 auto; width: fit-content; padding: 8px 22px; border-radius: 12px; background: #e0484f; color: #fff; font: 800 34px Inter, sans-serif; letter-spacing: .12em; box-shadow: 0 0 40px rgba(224,72,79,.8); }
    .s01-w { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; font: 700 140px/1 "EB Garamond", serif; color: #fff; opacity: 0; text-shadow: 0 0 50px rgba(255,75,82,.9), 0 6px 30px rgba(0,0,0,.8); }
    #s01-tag { left: 600px; top: 860px; padding: 10px 22px; border-radius: 14px; background: rgba(255,255,255,.96); color: #22283f; font: 600 48px "EB Garamond", serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }''',
SVG + '''
      <div id="s01-frame" class="abs"></div>
      <svg id="s01-warn" class="abs" viewBox="0 0 200 180"><path id="s01-tri" d="M100 10 L190 168 H10Z" fill="#ffd43b" stroke="#e0484f" stroke-width="14" stroke-linejoin="round"/><rect x="91" y="62" width="18" height="62" rx="9" fill="#141a32"/><circle cx="100" cy="144" r="11" fill="#141a32"/></svg>
      <div id="s01-live" class="abs">● 1 ÜBERLEBENDER WELTWEIT</div>
      <div id="s01-t" class="abs">Die ganze <em>Welt</em><br>unter Schnee.<small>Du bist der</small><b>letzte Mensch.</b></div>
      <div id="s01-tag" class="abs">Alex · 30</div>''',
'''      const sv = document.querySelector("#s01-svg");
      sky(sv, "s01-s", "#141d3a", "#6f82ab");
      const W = el("g", {}, sv);
      skyline(W, 1280, 3, ["#2c3858", "#344263"], 8, 260, 480);
      skyline(W, 1320, 5, ["#45537a", "#516089"], 7, 320, 580);
      snowLayer(W, 1180, "#dfe9f5");
      el("rect", { x: 450, y: 1150, width: 180, height: 420, fill: "#36425f" }, W); el("rect", { x: 440, y: 1140, width: 200, height: 24, fill: "#f4f8fc" }, W);
      snowLayer(W, 1260, "#f2f7fc");
      const beam = el("path", { d: "M570 1010 L860 880 L880 980Z", fill: "#fff6c8", opacity: 0.6 }, W);
      const A = alex(W, 540, 1142, 1.05);
      const sf = snowfall(sv, 120, 7, -300, 1500);
      const burst = []; const r = rng(17); for (let i = 0; i < 26; i++) burst.push(el("circle", { cx: 540, cy: 660, r: 6 + r() * 10, fill: "#ffffff", opacity: 0 }, sv));
      const flash = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#ffffff", opacity: 0 }, sv);
      const l1b = line("L1y")[0], du = at("L1y", 3), al = at("L2", "Alex"), le = at("L2", "letzte"), l3 = line("L3")[0];
      fall(tl, sf, C.__dur);
      tl.fromTo(flash, { opacity: 1 }, { opacity: 0, duration: 0.5, ease: "power2.out" }, 0);
      tl.fromTo("#s01-t", { scale: 1.6, filter: "blur(10px)" }, { scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }, 0);
      tl.to("#s01-t", { x: 12, duration: 0.04, repeat: 9, yoyo: true }, 0.45);
      burst.forEach((b, i) => { const a = i / 26 * Math.PI * 2; tl.fromTo(b, { opacity: 1, x: 0, y: 0 }, { x: Math.cos(a) * (500 + (i % 4) * 120), y: Math.sin(a) * (600 + (i % 3) * 140), opacity: 0, scale: 3, duration: 1.1, ease: "power2.out" }, 0.05); });
      tl.to("#s01-t em", { opacity: 0.35, duration: 0.07, repeat: 11, yoyo: true }, 0.6);
      tl.fromTo("#s01-t b", { scale: 1 }, { scale: 1.1, duration: 0.22, repeat: 9, yoyo: true, ease: "sine.inOut" }, 0.6);
      tl.fromTo("#s01-live", { opacity: 1 }, { opacity: 0.25, duration: 0.25, repeat: 21, yoyo: true }, 0);
      tl.fromTo(W, { scale: 1, svgOrigin: "540 1140" }, { scale: 1.12, svgOrigin: "540 1140", duration: l1b, ease: "power1.inOut" }, 0);
      tl.fromTo("#s01-tri", { attr: { fill: "#ffd43b" } }, { attr: { fill: "#e0484f" }, duration: 0.01, repeat: 23, yoyo: true, repeatDelay: 0.2 }, 0.05);
      tl.fromTo("#s01-warn", { scale: 1 }, { scale: 1.15, duration: 0.2, repeat: 23, yoyo: true, ease: "sine.inOut" }, 0.05);
      tl.fromTo("#s01-frame", { opacity: 0 }, { opacity: 1, duration: 0.2, repeat: 23, yoyo: true, ease: "sine.inOut" }, 0.05);
      tl.to(W, { x: 8, duration: 0.05, repeat: 11, yoyo: true }, 0.1);
      tl.to("#s01-t b", { scale: 1.25, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, du);
      tl.fromTo(flash, { opacity: 0.6 }, { opacity: 0, duration: 0.4 }, du); tl.to(W, { x: 12, duration: 0.04, repeat: 7, yoyo: true }, du);
      tl.to(["#s01-t", "#s01-live", "#s01-warn"], { opacity: 0, scale: 0.9, duration: 0.25 }, al - 0.35);
      tl.to("#s01-frame", { opacity: 0, duration: 0.3 }, al - 0.3);
      tl.to(W, { scale: 1.6, svgOrigin: "540 1100", duration: 1.0, ease: "power3.inOut" }, al - 0.4);
      tl.fromTo("#s01-tag", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, al);
      tl.to(A, { y: 1130, duration: 0.15, yoyo: true, repeat: 1 }, le);
      tl.fromTo(beam, { attr: { opacity: 0.6 } }, { attr: { opacity: 0.25 }, duration: 0.5, repeat: 11, yoyo: true }, 0);
      tl.to("#s01-tag", { opacity: 0, duration: 0.3 }, l3);
      tl.to(W, { scale: 1.25, svgOrigin: "540 1100", duration: 1.6, ease: "power2.inOut" }, l3);''' + OUT)

S['s02'] = (BIG + '''
    #s02-ph { left: 300px; top: 560px; width: 480px; height: 760px; border-radius: 60px; background: #111522; border: 10px solid #2a2f40; opacity: 0; text-align: center; color: #fff; box-shadow: 0 30px 70px rgba(0,0,0,.5); }
    #s02-ph .av { width: 150px; height: 150px; margin: 90px auto 20px; border-radius: 50%; background: #ff8fd0; font: 600 80px/150px "EB Garamond", serif; color: #fff; }
    #s02-ph b { display: block; font: 600 60px "EB Garamond", serif; } #s02-ph i { display: block; margin-top: 18px; font: 700 34px Inter, sans-serif; font-style: normal; color: #ff5a5f; }
    #s02-ph .bt { position: absolute; left: 0; right: 0; bottom: 70px; display: flex; justify-content: space-around; }
    #s02-ph .bt span { width: 120px; height: 120px; border-radius: 50%; font: 700 60px/120px Inter, sans-serif; }
    .s02-c { position: absolute; font: 600 48px "EB Garamond", serif; color: #fff; opacity: 0; text-shadow: 0 2px 12px rgba(0,0,0,.8); }''',
SVG + '''
      <div id="s02-ph" class="abs"><div class="av">E</div><b>Ex 💔</b><i>47 verpasste Anrufe</i><div class="bt"><span style="background:#e0484f">✕</span><span style="background:#39b36a">✆</span></div></div>
      <div id="s02-c1" class="s02-c" style="left:640px;top:690px">Tokio</div><div id="s02-c2" class="s02-c" style="left:330px;top:940px">New York</div><div id="s02-c3" class="s02-c" style="left:470px;top:640px">Berlin</div>''',
'''      const sv = document.querySelector("#s02-svg");
      sky(sv, "s02-s", "#9cc4e8", "#e4eef7");
      const W = el("g", {}, sv);
      skyline(W, 1150, 3, ["#8090b4", "#8a9abd"], 8, 260, 480);
      skyline(W, 1200, 5, ''' + COLS + ''', 7, 300, 560);
      el("rect", { x: 450, y: 760, width: 180, height: 460, fill: "#55627f" }, W); el("rect", { x: 440, y: 750, width: 200, height: 20, fill: "#7c88ad" }, W);
      const vent = el("rect", { x: 580, y: 700, width: 50, height: 50, rx: 6, fill: "#9aa6c4" }, W);
      el("rect", { x: 0, y: 1200, width: 1080, height: 400, fill: "#4a4f60" }, W);
      const cars = []; for (let i = 0; i < 6; i++) cars.push(el("rect", { x: 60 + i * 170, y: 1180, width: 90, height: 34, rx: 10, fill: ["#e8484f", "#4da3ff", "#ffd56b"][i % 3] }, W));
      const A = alex(W, 520, 752, 1.0);
      const wave = el("path", { d: "M-1400 1300 Q-900 600 -500 760 Q-300 820 -200 740 L-200 1600 L-1400 1600Z", fill: "#f4f8fc" }, sv);
      const fill = el("rect", { x: 0, y: 1600, width: 1080, height: 1500, fill: "#eef4fb" }, sv);
      const mist = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#ffffff", opacity: 0 }, sv);
      const globe = el("g", { opacity: 0 }, sv);
      const sfg = [];  el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#0b1022" }, globe);
      el("circle", { cx: 540, cy: 800, r: 300, fill: "#2f6fb8" }, globe);
      [["M380 650 q60 -60 140 -20 q40 60 -20 110 q-80 30 -120 -20Z"], ["M560 600 q80 -20 140 40 q30 80 -40 100 q-60 -10 -100 -60Z"], ["M420 860 q60 -30 100 20 q10 90 -60 110 q-60 -40 -40 -130Z"], ["M600 860 q90 -10 130 60 q-20 70 -100 60 q-50 -50 -30 -120Z"]].forEach(([d]) => el("path", { d, fill: "#4caf6a", class: "s02-land" }, globe));
      const ice = el("circle", { cx: 540, cy: 800, r: 300, fill: "#f2f7fc", opacity: 0 }, globe);
      const dots = [[760, 715], [420, 920], [560, 665]].map(([x, y]) => el("circle", { cx: x, cy: y, r: 14, fill: "#ff4b52", opacity: 0 }, globe));
      const gr = at("L4", "Grollen"), ww = at("L4", "weiße"), l5 = line("L5")[0], da = at("L5", "Dach"), l5x = line("L5x")[0], tx = at("L5x", "toxischen"), l5b = line("L5b")[0], aw = at("L5b", "alles"), vm = at("L5b", "vierzig"), l5c = line("L5c")[0], to = at("L5c", "Tokio"), ny = at("L5c", "New"), be = at("L5c", "Berlin"), ue = at("L5c", "Überall");
      cars.forEach((c, i) => tl.to(c, { x: (i % 2 ? -1 : 1) * 200, duration: 3, ease: "none" }, 0));
      tl.to(W, { x: 8, duration: 0.05, repeat: 19, yoyo: true }, gr);
      tl.to(wave, { x: 2600, duration: 2.6, ease: "power1.in" }, ww - 0.2);
      tl.to(fill, { attr: { y: 770 }, duration: 2.2, ease: "power2.inOut" }, ww + 0.3);
      tl.to(mist, { opacity: 0.45, duration: 0.6, yoyo: true, repeat: 1 }, ww + 0.8);
      tl.to(W, { scale: 1.7, svgOrigin: "540 740", duration: 1.0, ease: "power2.inOut" }, da - 0.4);
      tl.to(A, { x: 590, duration: 0.5, ease: "power2.inOut" }, da + 0.2);
      tl.set("#s02-ph", { opacity: 1 }, l5x - 0.1);
      tl.fromTo("#s02-ph", { scale: 1.3, rotation: -6 }, { scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)", immediateRender: false }, l5x - 0.1);
      tl.to("#s02-ph", { x: 10, duration: 0.05, repeat: 15, yoyo: true }, tx - 0.2);
      tl.set("#s02-ph", { opacity: 0 }, l5b - 0.1);
      tl.to(W, { scale: 1, svgOrigin: "540 740", duration: 0.6, ease: "power2.out" }, l5b - 0.1);
      tl.to(A, { y: 742, duration: 0.15, yoyo: true, repeat: 3 }, aw);
      tl.fromTo("#s02-big", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, vm - 0.2);
      tl.set("#s02-big", { opacity: 0 }, l5c - 0.1);
      tl.set(globe, { opacity: 1 }, l5c - 0.1);
      tl.fromTo(globe, { scale: 1.3, svgOrigin: "540 800" }, { scale: 1, svgOrigin: "540 800", duration: 0.8, ease: "power3.out", immediateRender: false }, l5c - 0.1);
      [to, ny, be].forEach((t, i) => { tl.to(dots[i], { opacity: 1, duration: 0.1 }, t - 0.05); tl.fromTo("#s02-c" + (i + 1), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2 }, t - 0.05); });
      tl.to(ice, { opacity: 1, duration: 0.8 }, ue - 0.2);
      tl.to(dots, { attr: { fill: "#9aa6c4" }, duration: 0.6 }, ue);
      const sfa = snowfall(sv, 60, 41, -300, 1500); gsap.set(sfa.g, { opacity: 0 }); fall(tl, sfa, C.__dur); tl.to(sfa.g, { opacity: 0.85, duration: 0.8 }, ww + 1.2);''' + OUT)

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
      const me = person(P, w, 3.4, 3.2, 0, { shirt: "#e8484f", pants: "#22284d", big: true });
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
      const me = person(P, w, 1.2, 1.2, 0, { shirt: "#e8484f", pants: "#22284d", big: true });
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
      el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#8293b3" }, cave); const sfc = snowfall(cave, 60, 33, -300, 1400); fall(tl, sfc, C.__dur);
      el("path", { d: "M160 1180 Q160 760 540 740 Q920 760 920 1180Z", fill: "#3a4566" }, cave);
      el("path", { d: "M200 1180 Q210 800 540 785 Q870 800 880 1180Z", fill: "#56628a" }, cave);
      const cand = el("g", {}, cave); el("rect", { x: 620, y: 1110, width: 26, height: 60, fill: "#f4f0e6" }, cand); const fl = el("ellipse", { cx: 633, cy: 1098, rx: 10, ry: 18, fill: "#ffcf6b" }, cand);
      const glow = el("circle", { cx: 633, cy: 1100, r: 120, fill: "#ffcf6b", opacity: 0.18 }, cave);
      alex(cave, 440, 1180, 1.4);
      const hole = el("path", { d: "M540 740 V600", stroke: "#e8f0f8", "stroke-width": 26, opacity: 0 }, cave);
      const air = []; for (let i = 0; i < 4; i++) air.push(el("circle", { cx: 540, cy: 720, r: 10 + i * 4, fill: "#ffffff", opacity: 0 }, cave));
      const sfw = snowfall(W, 60, 31, -300, 1400); fall(tl, sfw, C.__dur);
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
      const sfk = snowfall(sv, 55, 51, -300, 1400); fall(tl, sfk, C.__dur);
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
      el("rect", { x: 0, y: 1000, width: 1080, height: 920, fill: "#cfd9e6" }, roof);
      const rad = el("g", {}, roof); el("rect", { x: 260, y: 900, width: 160, height: 100, rx: 14, fill: "#2a2f40" }, rad); el("path", { d: "M400 900 L460 790", stroke: "#8a8f9c", "stroke-width": 8 }, rad);
      const waves = [1, 2, 3].map((i) => el("path", { d: `M${460 + i * 30} ${790 - i * 10} q${20 + i * 10} ${20 + i * 10} 0 ${40 + i * 20}`, stroke: "#9dbcff", "stroke-width": 6, fill: "none", opacity: 0 }, rad));
      const beam = el("path", { d: "M660 880 L1080 560 L1080 740Z", fill: "#fff6c8", opacity: 0 }, roof);
      alex(roof, 600, 1000, 1.4);
      const yard = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#7f8ca0" }, yard);
      el("rect", { x: 0, y: 0, width: 1080, height: 600, fill: "#0b0f1c" }, yard);
      el("path", { d: "M620 1260 Q620 1020 860 1010 Q1100 1020 1100 1260Z", fill: "#dfe7f1" }, yard); const hole = el("path", { d: "M770 1260 Q770 1150 860 1145 Q950 1150 950 1260Z", fill: "#05070f" }, yard);
      const SOLE = "M-20 -58 Q-24 -74 -10 -80 Q8 -84 19 -70 Q27 -55 23 -32 Q19 -12 15 2 Q10 12 -9 11 Q-22 5 -22 -12 Q-24 -32 -20 -58Z", HEEL = "M-17 22 Q-19 48 0 52 Q19 48 17 22 Q0 15 -17 22Z";
      const prints = [], rp = rng(77);
      for (let i = 0; i < 6; i++) { const x = 70 + i * 150, y = 640 + i * 112 + (i % 2 ? 46 : -46), m = i % 2 ? -1 : 1;
        const g = el("g", { opacity: 0 }, yard), inner = el("g", { transform: `translate(${x} ${y}) rotate(128) scale(${m} 1)` }, g);
        const parts = [el("path", { d: SOLE, fill: "#4c576b" }, inner), el("path", { d: HEEL, fill: "#4c576b" }, inner)];
        const tread = el("g", { opacity: 0.3 }, inner); for (let k = 0; k < 5; k++) el("rect", { x: -15, y: -64 + k * 14, width: 30, height: 3, rx: 1.5, fill: "#2a0306" }, tread);
        const spl = []; for (let k = 0; k < 7; k++) { const a = rp() * Math.PI * 2, d = 48 + rp() * 40; spl.push(el("circle", { cx: Math.cos(a) * d * 0.55, cy: Math.sin(a) * d - 10, r: 2 + rp() * 6, fill: "#7a0b14", opacity: 0 }, inner)); }
        const drip = el("path", { d: `M0 54 q${6 * m} 30 0 ${56 + rp() * 30}`, stroke: "#7a0b14", "stroke-width": 5, fill: "none", "stroke-linecap": "round", opacity: 0 }, inner);
        prints.push({ g, x, y, parts, tread, spl, drip }); }
      const sf = snowfall(sv, 70, 21, -300, 1500);
      const shadow = el("path", { d: "M860 1145 Q850 900 870 860 Q900 820 930 860 Q960 900 950 1145Z", fill: "#000", opacity: 0 }, yard);
      const dark = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#000", opacity: 0 }, sv);
      const red = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#8a0f1c", opacity: 0 }, sv);
      const ra = at("L16", "Radio"), li = at("L16", "Licht"), l17 = line("L17")[0], st = at("L17", "Stille"), l18 = line("L18")[0], fu = at("L18", "Fußspuren"), ri = at("L18b", "Riesig"), dg = at("L18b", "Doppelt"), ro = at("L19", "rot"), bl = at("L19", "Blut"), l19b = line("L19b")[0], hoe = at("L19b", "Höhle"), l20 = line("L20")[0], l20b = line("L20b")[0];
      fall(tl, sf, C.__dur);
      waves.forEach((w, i) => tl.fromTo(w, { opacity: 0 }, { opacity: 1, duration: 0.2, repeat: 7, yoyo: true }, ra + i * 0.12));
      tl.to(beam, { opacity: 0.5, duration: 0.1, repeat: 9, yoyo: true }, li);
      tl.to(dark, { opacity: 0.85, duration: 0.8 }, st - 0.3);
      tl.set(roof, { opacity: 0 }, l18 - 0.1); tl.to(dark, { opacity: 0.25, duration: 0.6 }, l18 - 0.1); tl.set(yard, { opacity: 1 }, l18 - 0.1);
      tl.fromTo(yard, { scale: 1.35, svgOrigin: "300 900" }, { scale: 1.1, svgOrigin: "300 900", duration: 3, ease: "power1.out", immediateRender: false }, l18 - 0.1);
      prints.forEach((p, i) => tl.to(p.g, { opacity: 1, duration: 0.12 }, fu + i * 0.3));
      prints.forEach((p, i) => tl.to(p.g, { scale: 1.45, svgOrigin: `${p.x} ${p.y}`, duration: 0.35, ease: "back.out(2)" }, ri + i * 0.05));
      tl.to(yard, { x: 8, duration: 0.04, repeat: 7, yoyo: true }, dg);
      prints.forEach((p, i) => { tl.to(p.parts, { attr: { fill: "#6e0911" }, duration: 0.25 }, ro + i * 0.08); tl.to(p.tread, { opacity: 0.5, duration: 0.25 }, ro + i * 0.08);
        tl.to(p.spl, { opacity: 0.9, duration: 0.15, stagger: 0.02 }, bl - 0.1 + i * 0.06); tl.to(p.drip, { opacity: 0.85, duration: 0.3 }, bl + i * 0.06); });
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.6, duration: 0.12, repeat: 3, yoyo: true }, bl);
      tl.to(yard, { scale: 1.6, svgOrigin: "860 1200", duration: 2.2, ease: "power2.in" }, l19b);
      tl.to(dark, { opacity: 0.55, duration: 1.2 }, l20);
      tl.to(shadow, { opacity: 0.85, duration: 1.4, ease: "power1.in" }, l20b - 0.5);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.7, duration: 0.1, repeat: 5, yoyo: true }, l20b);
      tl.to(dark, { opacity: 1, duration: 0.5 }, C.__dur - 0.5);''')

S['s08'] = ('''    #s08-t { left: 0; width: 1080px; top: 620px; text-align: center; color: #fff; font: 500 170px/1 "EB Garamond", serif; text-shadow: 0 0 40px rgba(255,90,95,.6); opacity: 0; }
    #s08-s { left: 0; width: 1080px; top: 820px; text-align: center; color: #ff8fd0; font: 600 34px Inter, sans-serif; letter-spacing: .3em; opacity: 0; }
    #s08-f { left: 330px; top: 960px; width: 420px; height: 110px; border-radius: 55px; background: #ff3b5c; color: #fff; text-align: center; font: 800 52px/110px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 40px rgba(255,59,92,.5); }''',
'''      <div id="s08-t" class="abs">Teil 2?</div><div id="s08-s" class="abs">WER IST IN DER HÖHLE?</div><div id="s08-f" class="abs">+ Folgen</div>''',
'''      // Schneesturm hinter dem Text: dicht, schräg, gedämpft
      const st8 = document.querySelector("#s08-stage"), sv8 = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st8.insertBefore(sv8, st8.firstChild);
      const storm = el("g", { opacity: 0.42, "data-layout-allow-overlap": "" }, sv8), rs = rng(88);
      for (let i = 0; i < 18; i++) { const y0 = rs() * 1920, ln = el("path", { d: `M-200 ${y0} l260 ${60 + rs() * 40}`, stroke: "#dfe9f5", "stroke-width": 2 + rs() * 3, opacity: 0.35, "stroke-linecap": "round" }, storm);
        tl.fromTo(ln, { x: -300 }, { x: 1500, duration: 0.9 + rs() * 0.6, repeat: Math.ceil(C.__dur / 0.9), ease: "none" }, rs() * 0.8); }
      for (let i = 0; i < 160; i++) { const f = el("circle", { cx: rs() * 1300 - 200, cy: rs() * 1920 - 400, r: 2 + rs() * 5, fill: "#ffffff", opacity: 0.4 + rs() * 0.5 }, storm), d = 1.6 + rs() * 1.4;
        tl.fromTo(f, { x: 0, y: 0 }, { x: 520, y: 900, duration: d, repeat: Math.ceil(C.__dur / d), ease: "none" }, -rs() * d); }
      const fo = at("L21", "folg"), l22 = line("L22")[0];
      tl.fromTo("#s08-t", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }, 0.1);
      tl.fromTo("#s08-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s08-f", { scale: 1.06, duration: 0.3, yoyo: true, repeat: 13, ease: "sine.inOut" }, fo + 0.4);
      tl.fromTo("#s08-s", { opacity: 0 }, { opacity: 1, duration: 0.5 }, l22);
      tl.fromTo("#s08-t", { opacity: 1 }, { opacity: 0.55, duration: 0.08, repeat: 7, yoyo: true, immediateRender: false }, l22 + 0.5);
      tl.set("#s08-t", { opacity: 1 }, l22 + 1.2);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
