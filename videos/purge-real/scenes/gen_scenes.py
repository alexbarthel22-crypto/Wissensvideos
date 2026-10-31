#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Purge real“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
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
RED = '      const red = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#c8102e", opacity: 0 }, sv);\n'

S['s01'] = ('''    #s01-call { left: 290px; top: 640px; width: 500px; height: 300px; border-radius: 30px; background: #12131c; border: 5px solid #ff3b55; text-align: center; opacity: 0; box-shadow: 0 0 60px rgba(255,59,85,.45); }
    #s01-call b { display: block; margin-top: 40px; font: 700 110px/1 Oswald, sans-serif; color: #fff; } #s01-call i { display: block; margin-top: 16px; font: 700 40px Oswald, sans-serif; font-style: normal; color: #ff3b55; letter-spacing: .06em; }
    #s01-tv { left: 140px; top: 600px; width: 800px; height: 560px; border-radius: 30px; background: #1a1c26; border: 6px solid #0b0c14; opacity: 0; }
    #s01-tv .scr { position: absolute; left: 34px; top: 34px; right: 34px; bottom: 90px; border-radius: 14px; background: #2a0d14; text-align: center; overflow: hidden; }
    #s01-tv .scr b { display: block; margin-top: 40px; font: 700 40px Oswald, sans-serif; color: #ff3b55; letter-spacing: .1em; }
    #s01-tv .scr i { display: block; margin-top: 10px; font: 700 120px/1 Oswald, sans-serif; font-style: normal; color: #fff; }
    #s01-tv .tk { position: absolute; left: 0; right: 0; bottom: 0; height: 64px; background: #ff3b55; color: #fff; font: 700 36px/64px Oswald, sans-serif; white-space: nowrap; }''',
SVG + '''
      <div id="s01-tv" class="abs"><div class="scr"><b>NOTFALL-DURCHSAGE</b><i id="s01-cd">12:00:00</i><div class="tk"><span id="s01-tk">ALLE VERBRECHEN LEGAL · 12 STUNDEN · KEINE RETTUNGSDIENSTE · ALLE VERBRECHEN LEGAL ·</span></div></div></div>
      <div id="s01-call" class="abs"><b>112</b><i>NICHT ERREICHBAR</i></div>''',
'''      const sv = document.querySelector("#s01-svg");
      night(sv, "s01-n", "#07091a", "#2a1630", [850, 660]);
      const A = el("g", {}, sv);
      pines(A, 1010, "#0f1424", 4);
      [[20, 230, 250, "#3b3550", [1, 0]], [300, 200, 230, "#45405c", [0, 1]], [560, 240, 260, "#37324a", [1, 1]], [850, 220, 240, "#423b56", [0, 1]]].forEach(([x, w, h, c, lit]) => house(A, x, 1150, w, h, c, { lit }));
      el("rect", { x: -200, y: 1150, width: 1480, height: 400, fill: "#141320" }, A);
      const L = lamp(A, 230, 1200);
      const pk = [pumpkin(A, 130, 1175, 0.9), pumpkin(A, 690, 1172, 0.8), pumpkin(A, 960, 1176, 0.85)];
      const fg = fog(A, 1110, 0.3, 6);
      const M = masked(A, 900, 1360, 1.15, "#1d1f2b", true);
      const CU = el("g", { opacity: 0 }, sv); el("rect", { x: 0, y: 500, width: 1080, height: 1000, fill: "#0b0c14" }, CU);
      const MC = masked(CU, 540, 2050, 3.6, "#1d1f2b");
      const D = el("g", { opacity: 0 }, sv), icons = [];
      [["#2f5bd6", "POLIZEI"], ["#d63a2f", "FEUERWEHR"], ["#ece6d6", "NOTARZT"]].forEach(([c, l], i) => { const g = el("g", { opacity: 0 }, D), x = 190 + i * 350, y = 860;
        el("rect", O({ x: x - 130, y: y - 60, width: 260, height: 130, rx: 24, fill: c }), g); el("rect", O({ x: x - 50, y: y - 100, width: 100, height: 46, rx: 10, fill: c }), g);
        [x - 80, x + 80].forEach((wx) => el("circle", O({ cx: wx, cy: y + 72, r: 30, fill: "#22232e" }), g));
        el("rect", { x: x - 40, y: y - 116, width: 80, height: 18, rx: 6, fill: i === 0 ? "#4da3ff" : "#ff3b55" }, g);
        txt(g, x, y + 160, l, 44, "#fff"); const xx = txt(g, x, y + 50, "✕", 230, "#ff3b55", { opacity: 0 }); icons.push({ g, xx }); });
      const Q = txt(sv, 540, 1000, "?", 420, "#ff3b55", { opacity: 0 });
''' + RED + '''      const l2 = line("L2")[0], ve = at("L2", "Verbrechen"), mo = at("L2", "Mord"), l3 = line("L3")[0], po = at("L3", "Polizei"), fe = at("L3", "Feuerwehr"), no = at("L3", "Notarzt"), ni = at("L3", "nicht"), ue = at("L3", "Und"), sz = at("L3", "schockierendste");
      // Einstellung 1: Straße, Kamera fährt langsam ran, Figur läuft ins Bild
      tl.fromTo(A, { scale: 1 }, { scale: 1.15, svgOrigin: "540 1100", duration: l2, ease: "none" }, 0);
      tl.to(M.g, { x: 560, duration: 2.6, ease: "power1.out" }, 0.2);
      tl.to(M.g, { y: 1352, duration: 0.3, repeat: 7, yoyo: true, ease: "sine.inOut" }, 0.2);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.32, duration: 0.25, repeat: 7, yoyo: true, ease: "sine.inOut" }, 0);
      pk.forEach((k, i) => tl.fromTo(k.face, { opacity: 1 }, { opacity: 0.5, duration: 0.12, repeat: 9, yoyo: true }, 0.3 + i * 0.2));
      tl.to(fg, { x: 80, duration: 6, ease: "none" }, 0);
      tl.to(L.cone, { attr: { opacity: 0.04 }, duration: 0.06, repeat: 5, yoyo: true }, 1.5);
      tl.to(M.mask, { rotation: -8, svgOrigin: "0 -345", duration: 0.4, yoyo: true, repeat: 1 }, 2.9);
      // Einstellung 2: Fernseher mit Notfall-Durchsage
      tl.set(A, { opacity: 0 }, l2 - 0.05); tl.set("#s01-tv", { opacity: 1 }, l2 - 0.05);
      tl.fromTo("#s01-tv", { scale: 1.25 }, { scale: 1, duration: 0.5, ease: "power3.out" }, l2 - 0.05);
      tl.fromTo("#s01-tk", { x: 900 }, { x: -1400, duration: 4, ease: "none" }, l2);
      tl.to("#s01-tv .scr", { backgroundColor: "#5a0d1c", duration: 0.12, repeat: 5, yoyo: true }, ve);
      // Einstellung 3: Nahaufnahme Maske
      tl.set("#s01-tv", { opacity: 0 }, mo - 0.25); tl.set(CU, { opacity: 1 }, mo - 0.25);
      tl.fromTo(CU, { scale: 1.2 }, { scale: 1, svgOrigin: "540 900", duration: 0.4, ease: "power3.out" }, mo - 0.25);
      tl.fromTo(red, { opacity: 0.7 }, { opacity: 0, duration: 0.5 }, mo);
      tl.to(MC.g, { x: 552, duration: 0.04, repeat: 9, yoyo: true }, mo);
      // Einstellung 4: Polizei, Feuerwehr, Notarzt durchgestrichen
      tl.set(CU, { opacity: 0 }, l3 - 0.1); tl.set(D, { opacity: 1 }, l3 - 0.1);
      [po, fe, no].forEach((t, i) => { tl.fromTo(icons[i].g, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, t - 0.15);
        tl.fromTo(icons[i].xx, { opacity: 0, scale: 2, svgOrigin: `${190 + i * 350} 860` }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }, t + 0.25); });
      // Einstellung 5: Notruf tot
      tl.to(D, { opacity: 0, duration: 0.2 }, ni + 0.25);
      tl.fromTo("#s01-call", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ni + 0.1);
      tl.to("#s01-call", { x: 10, duration: 0.04, repeat: 7, yoyo: true }, ni + 0.2);
      // Einstellung 6: dunkle Straße, Frage
      tl.set("#s01-call", { opacity: 0 }, ue - 0.1); tl.set(A, { opacity: 1, scale: 1.4 }, ue - 0.1); tl.set(M.g, { opacity: 0 }, ue - 0.1);
      tl.to(A, { scale: 1.2, duration: 2, ease: "power1.out" }, ue - 0.1);
      tl.fromTo(Q, { opacity: 0, scale: 0.4, svgOrigin: "540 900" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, sz - 0.1);''' + OUT)

S['s02'] = ('''    #s02-st { left: 230px; top: 760px; width: 620px; height: 150px; border: 10px solid #ff3b55; border-radius: 18px; color: #ff3b55; font: 700 90px/130px Oswald, sans-serif; text-align: center; opacity: 0; background: rgba(10,10,16,.6); }''',
SVG + '''
      <div id="s02-st" class="abs">AUSVERKAUFT</div>''',
'''      const sv = document.querySelector("#s02-svg");
      night(sv, "s02-n", "#151a2c", "#2a2236", null);
      const shop = el("g", {}, sv);
      el("rect", O({ x: 80, y: 560, width: 920, height: 760, fill: "#2c2f3e" }), shop);
      [700, 900, 1100].forEach((y) => el("rect", O({ x: 110, y, width: 860, height: 20, fill: "#8a8f9c", "stroke-width": 4 }), shop));
      const items = [];
      [680, 880, 1080].forEach((y) => { for (let i = 0; i < 9; i++) items.push(el("rect", O({ x: 130 + i * 92, y: y - 70, width: 70, height: 70, rx: 6, fill: ["#ffd43b", "#ff8a3d", "#7fd0ff", "#a87a4a"][i % 4], "stroke-width": 4 }), shop)); });
      el("rect", O({ x: 360, y: 590, width: 360, height: 70, rx: 10, fill: "#ffd43b" }), shop); txt(shop, 540, 642, "BAUMARKT", 46, K);
      const big = (draw) => { const g = el("g", { opacity: 0 }, sv); el("rect", { x: 0, y: 500, width: 1080, height: 1000, fill: "#1a1c28" }, g); draw(g); return g; };
      const lock = big((g) => { el("path", O({ d: "M440 820 V720 Q540 600 640 720 V820", fill: "none", "stroke-width": 34, stroke: "#8a8f9c" }), g); el("rect", O({ x: 400, y: 810, width: 280, height: 240, rx: 30, fill: "#ffd43b" }), g); el("circle", { cx: 540, cy: 920, r: 26, fill: K }, g); });
      const grid = big((g) => { for (let k = 0; k < 7; k++) { el("path", O({ d: `M${300 + k * 80} 640 V1180`, stroke: "#8a8f9c", "stroke-width": 18 }), g); el("path", O({ d: `M260 ${680 + k * 80} H820`, stroke: "#8a8f9c", "stroke-width": 18 }), g); } });
      const wood = big((g) => { for (let k = 0; k < 4; k++) plank(g, 200, 700 + k * 110, 680, k % 2 ? 4 : -4); const h = el("g", {}, g); el("rect", O({ x: 720, y: 560, width: 40, height: 260, rx: 10, fill: "#8a5a3a", transform: "rotate(30 740 690)" }), h); el("rect", O({ x: 650, y: 540, width: 170, height: 70, rx: 14, fill: "#8a8f9c", transform: "rotate(30 740 690)" }), h); g.hammer = h; });
      const st = el("g", { opacity: 0 }, sv);
      const A = house(st, 120, 1250, 380, 420, "#4a4258", { lit: [0, 0], n: 2 }), B = house(st, 600, 1250, 360, 400, "#3e3a4e", { lit: [1, 1], n: 2 });
      el("rect", { x: 0, y: 1250, width: 1080, height: 200, fill: "#141320" }, st);
      const planks = []; A.wins.forEach((w) => { const x = +w.getAttribute("x"), y = +w.getAttribute("y"); planks.push(plank(st, x - 14, y + 4, 80, -14), plank(st, x - 14, y + 30, 80, 12)); });
      const crack = B.wins.map((w) => { const x = +w.getAttribute("x"), y = +w.getAttribute("y"); return el("path", { d: `M${x + 26} ${y + 28} l-18 -20 M${x + 26} ${y + 28} l20 -22 M${x + 26} ${y + 28} l-14 26 M${x + 26} ${y + 28} l22 16`, stroke: "#fff", "stroke-width": 3, opacity: 0 }, st); });
      const ok = txt(st, 310, 760, "✓", 120, "#39e27a", { opacity: 0 }), no = txt(st, 780, 760, "✕", 120, "#ff3b55", { opacity: 0 });
      const le = at("L4", "leergekauft"), sl = at("L4", "Schlösser"), gi = at("L4", "Gitter"), sp = at("L4", "Sperrholz"), we = at("L4", "weg"), l5 = line("L5")[0], ve = at("L5", "verbarrikadiert"), sc = at("L5", "schutzlos");
      tl.fromTo(shop, { scale: 1.2 }, { scale: 1, svgOrigin: "540 940", duration: 1.2, ease: "power2.out" }, 0);
      items.forEach((it, i) => tl.to(it, { opacity: 0, y: -40, duration: 0.18 }, le - 0.6 + (i % 27) * 0.03));
      [[lock, sl], [grid, gi], [wood, sp]].forEach(([g, t], i, arr) => { tl.set(g, { opacity: 1 }, t - 0.1); tl.fromTo(g, { scale: 1.3 }, { scale: 1, svgOrigin: "540 900", duration: 0.35, ease: "power3.out" }, t - 0.1);
        tl.set(g, { opacity: 0 }, i < 2 ? arr[i + 1][1] - 0.1 : we - 0.1); });
      tl.to(wood.hammer, { rotation: -40, svgOrigin: "740 800", duration: 0.12, yoyo: true, repeat: 5 }, sp);
      tl.fromTo("#s02-st", { opacity: 0, scale: 2.2, rotation: -8 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.25, ease: "power4.in" }, we - 0.15);
      tl.to(["#s02-st", shop], { opacity: 0, duration: 0.2 }, l5 - 0.25);
      tl.to(st, { opacity: 1, duration: 0.2 }, l5 - 0.15);
      tl.fromTo(st, { scale: 1.25 }, { scale: 1, svgOrigin: "540 1100", duration: 1.0, ease: "power2.out" }, l5 - 0.15);
      planks.forEach((pl, i) => tl.fromTo(pl, { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: 0.2, ease: "back.out(2)" }, ve - 0.2 + i * 0.12));
      tl.to(ok, { opacity: 1, duration: 0.2 }, ve + 0.5);
      tl.to(st, { x: -160, duration: 0.6, ease: "power2.inOut" }, sc - 0.6);
      tl.to(crack, { opacity: 1, duration: 0.1 }, sc - 0.2);
      tl.to(no, { opacity: 1, duration: 0.2 }, sc);
      tl.to(B.g, { x: 6, duration: 0.04, repeat: 7, yoyo: true }, sc);''' + OUT)

S['s04'] = ('''    #s04-c { left: 600px; top: 600px; width: 400px; height: 200px; border-radius: 22px; background: rgba(10,10,16,.85); border: 4px solid #ff3b55; text-align: center; color: #fff; opacity: 0; }
    #s04-c b { display: block; margin-top: 22px; font: 700 96px/1 Oswald, sans-serif; } #s04-c i { display: block; margin-top: 8px; font: 700 30px Oswald, sans-serif; font-style: normal; color: #ff3b55; letter-spacing: .05em; }''',
SVG + '''
      <div id="s04-c" class="abs"><b id="s04-n">0</b><i>EINSÄTZE · 12 STD.</i></div>''',
'''      const sv = document.querySelector("#s04-svg");
      night(sv, "s04-n2", "#0a0c1c", "#301424", [200, 640]);
      const amb = el("g", {}, sv);
      el("rect", O({ x: 120, y: 900, width: 520, height: 230, rx: 26, fill: "#ece6d6" }), amb); el("rect", O({ x: 520, y: 940, width: 120, height: 90, rx: 12, fill: "#9bb7d6" }), amb);
      el("rect", { x: 120, y: 1010, width: 400, height: 30, fill: "#ff3b55" }, amb); el("path", { d: "M300 940 v50 M275 965 h50", stroke: "#ff3b55", "stroke-width": 14 }, amb);
      const bl = el("rect", O({ x: 260, y: 870, width: 80, height: 30, rx: 8, fill: "#4da3ff" }), amb);
      [210, 560].forEach((x) => el("circle", O({ cx: x, cy: 1130, r: 46, fill: "#22232e" }), amb));
      const xx = txt(sv, 380, 1090, "✕", 300, "#ff3b55", { opacity: 0 });
      const ecg = el("g", { opacity: 0 }, sv); flatCard(ecg, 140, 620, 800, 300, "#0e1a14");
      const line1 = el("path", { d: "M170 780 h120 l20 -60 l25 120 l20 -60 h120 l20 -60 l25 120 l20 -60 h300", stroke: "#39e27a", "stroke-width": 8, fill: "none" }, ecg);
      const st2 = el("g", { opacity: 0 }, sv);
      const hs = [house(st2, 60, 1300, 300, 300, "#4a4258", { lit: [1, 0] }), house(st2, 400, 1300, 300, 320, "#3e3a4e", { lit: [0, 1] }), house(st2, 740, 1300, 300, 290, "#45405c", { lit: [1, 1] })];
      const fl = [flames(st2, 210, 1010, 1.4), flames(st2, 550, 990, 1.5), flames(st2, 890, 1020, 1.4)]; gsap.set(fl, { opacity: 0 });
      const glow = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#ff5a1f", opacity: 0 }, sv);
      const l9 = line("L9")[0], n2 = at("L9", "20.000"), ke = at("L10", "keinen"), he = at("L10", "Herzinfarkt"), kb = at("L10", "Küchenbrand"), fr = at("L10", "frisst");
      tl.fromTo(amb, { opacity: 0, x: -300 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.1);
      tl.to(bl, { attr: { fill: "#ff3b55" }, duration: 0.15, repeat: 15, yoyo: true }, 0.2);
      tl.to("#s04-c", { opacity: 1, duration: 0.25 }, n2 - 0.4);
      count(tl, "#s04-n", 0, 20000, n2 - 0.3, 0.9, "", "", "power3.out");
      count(tl, "#s04-n", 20000, 0, ke - 0.3, 0.5, "", "", "power3.in");
      tl.fromTo(xx, { opacity: 0, scale: 2, svgOrigin: "380 1000" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, ke);
      tl.to([amb, xx, "#s04-c"], { opacity: 0, duration: 0.25 }, he - 0.4);
      tl.to(ecg, { opacity: 1, duration: 0.2 }, he - 0.3);
      tl.to(line1, { attr: { d: "M170 780 h120 l20 -60 l25 120 l20 -60 h120 l10 -20 l10 30 h500" }, duration: 0.5 }, he + 0.3);
      tl.to(line1, { attr: { stroke: "#ff3b55" }, duration: 0.2 }, he + 0.6);
      tl.to(ecg, { opacity: 0, duration: 0.2 }, kb - 0.4);
      tl.to(st2, { opacity: 1, duration: 0.3 }, kb - 0.3);
      fl.forEach((f, i) => { tl.fromTo(f, { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1.4, duration: 0.35, ease: "back.out(2)" }, kb + 0.2 + i * 0.5); tl.to(f, { scaleY: 1.6, duration: 0.15, yoyo: true, repeat: 9 }, kb + 0.6 + i * 0.5); });
      tl.to(glow, { opacity: 0.22, duration: 0.6 }, fr);''' + OUT)

S['s05'] = ('''    #s05-st { left: 300px; top: 640px; width: 480px; height: 150px; border: 10px solid #ff3b55; border-radius: 18px; color: #ff3b55; font: 700 100px/130px Oswald, sans-serif; text-align: center; opacity: 0; background: rgba(10,10,16,.6); }
    #s05-card { left: 330px; top: 560px; width: 420px; height: 600px; border-radius: 26px; background: linear-gradient(135deg, #ffd43b, #ff8fd0 45%, #7fd0ff); border: 8px solid #0b0c14; opacity: 0; box-shadow: 0 0 80px rgba(255,212,59,.5); }
    #s05-card .art { position: absolute; left: 30px; top: 80px; right: 30px; height: 300px; border-radius: 14px; background: #1a1c28; border: 5px solid #0b0c14; }
    #s05-card .nm { position: absolute; left: 30px; top: 22px; font: 700 40px Oswald, sans-serif; color: #0b0c14; } #s05-card .st { position: absolute; right: 30px; top: 18px; font: 700 46px Oswald, sans-serif; color: #0b0c14; }
    #s05-card .tx { position: absolute; left: 30px; right: 30px; top: 400px; height: 150px; border-radius: 12px; background: rgba(255,255,255,.7); }
    #s05-price { left: 640px; top: 1050px; width: 330px; height: 120px; border-radius: 18px; background: #ff3b55; color: #fff; text-align: center; font: 700 70px/120px Oswald, sans-serif; opacity: 0; transform: rotate(-8deg); }
    #s05-lt { left: 190px; top: 620px; width: 700px; height: 480px; border-radius: 16px; background: #efe8d6; border: 5px solid #0b0c14; opacity: 0; text-align: center; color: #22283f; }
    #s05-lt b { display: block; margin-top: 40px; font: 700 54px Oswald, sans-serif; } #s05-lt p { margin: 20px 60px; font: 500 34px/1.4 "EB Garamond", serif; }''',
SVG + '''
      <div id="s05-card" class="abs"><div class="nm">NACHTFALKE</div><div class="st">★★★</div><div class="art"></div><div class="tx"></div></div>
      <div id="s05-price" class="abs">2.500 €</div>
      <div id="s05-lt" class="abs"><b>VERSICHERUNG</b><p>Schaden während der Säuberung: keine Leistung.</p></div>
      <div id="s05-st" class="abs" data-layout-allow-overlap>LEGAL</div>''',
'''      const sv = document.querySelector("#s05-svg");
      night(sv, "s05-n", "#08091a", "#24122a", [180, 660]);
      const W = el("g", {}, sv);
      pines(W, 1050, "#0f1424", 8);
      el("rect", { x: -200, y: 1180, width: 1480, height: 300, fill: "#141320" }, W);
      const fg = fog(W, 1150, 0.28, 11);
      const gang = [[160, 1360, 0.95, "#1d1f2b"], [330, 1330, 0.85, "#2a1c26"], [470, 1380, 1.05, "#1a2230"], [60, 1340, 0.8, "#231d2b"]].map(([x, y, s, c], i) => masked(W, x, y, s, c, i === 2));
      const row = el("g", { opacity: 0 }, sv); el("rect", { x: 0, y: 500, width: 3300, height: 1000, fill: "#0f1020" }, row);
      const glass = [], shards = [];
      [["JUWELIER", "#ffd43b"], ["BANK", "#7fd0ff"], ["KARTEN-SHOP", "#ff8fd0"]].forEach(([n, c], i) => { const x = 140 + i * 1080;
        el("rect", O({ x, y: 620, width: 800, height: 640, fill: "#2c2f3e" }), row); el("rect", O({ x: x + 60, y: 650, width: 680, height: 90, rx: 10, fill: c }), row); txt(row, x + 400, 718, n, 60, K);
        if (i === 2) for (let k = 0; k < 6; k++) el("rect", O({ x: x + 110 + k * 100, y: 880, width: 80, height: 115, rx: 8, fill: ["#ffd43b", "#ff8fd0", "#7fd0ff"][k % 3], "stroke-width": 3 }), row);
        if (i === 0) for (let k = 0; k < 5; k++) el("path", O({ d: `M${x + 150 + k * 120} 960 l30 -40 l30 40 l-30 30Z`, fill: "#bfe7ff", "stroke-width": 3 }), row);
        if (i === 1) txt(row, x + 400, 1000, "€ € €", 120, "#39e27a");
        glass.push(el("rect", O({ x: x + 60, y: 780, width: 680, height: 420, fill: "#7fd0ff", opacity: 0.55 }), row));
        const r = rng(i + 3); for (let k = 0; k < 9; k++) shards.push([i, el("path", { d: `M${x + 120 + r() * 560} ${820 + r() * 340} l${20 + r() * 30} ${-10 - r() * 20} l-10 ${30 + r() * 20}Z`, fill: "#e6f6ff", opacity: 0 }, row)]); });
''' + RED + '''      const ba = at("L11", "Banden"), ra = at("L11", "Rachegelüsten"), zu = at("L11", "zuschauen"), l12 = line("L12")[0], ju = at("L12", "Juweliere"), bk = at("L12", "Banken"), sk = at("L12", "Sammelkartenläden"), l12b = line("L12b")[0], te = at("L12b", "tausende"), l12c = line("L12c")[0], le = at("L12c", "legal");
      tl.fromTo(W, { scale: 1.3 }, { scale: 1, svgOrigin: "540 1250", duration: 1.5, ease: "power2.out" }, 0);
      gang.forEach((m, i) => tl.fromTo(m.g, { x: `-=${300}`, opacity: 0 }, { x: `+=${300}`, opacity: 1, duration: 1.2, ease: "power2.out" }, ba - 0.4 + i * 0.25));
      tl.to(gang.map((m) => m.g), { y: "-=10", duration: 0.3, yoyo: true, repeat: 9, stagger: 0.1 }, ba + 1.0);
      tl.to(fg, { x: -80, duration: 8, ease: "none" }, 0);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.25, duration: 0.2, repeat: 3, yoyo: true }, ra);
      tl.to(W, { scale: 1.6, svgOrigin: "300 1100", duration: 0.8, ease: "power2.in" }, zu);
      tl.set(W, { opacity: 0 }, l12 - 0.1); tl.set(row, { opacity: 1 }, l12 - 0.1);
      [ju, bk, sk].forEach((t, i) => { tl.to(row, { x: -1080 * i, duration: i ? 0.35 : 0.01, ease: "power3.inOut" }, t - (i ? 0.45 : 0.1));
        tl.to(glass[i], { opacity: 0, duration: 0.05 }, t);
        shards.filter((s) => s[0] === i).forEach(([_, sh], k) => tl.fromTo(sh, { opacity: 1, x: 0, y: 0 }, { x: (k % 2 ? 1 : -1) * (40 + k * 12), y: 220 + k * 10, rotation: 140, opacity: 0, svgOrigin: `${540 + 1080 * i} 1000`, duration: 0.7, ease: "power2.in" }, t));
        tl.fromTo(red, { opacity: 0.35 }, { opacity: 0, duration: 0.3 }, t); });
      tl.set(row, { opacity: 0 }, l12b - 0.1);
      tl.fromTo("#s05-card", { opacity: 0, rotationY: 90, scale: 0.7 }, { opacity: 1, rotationY: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, l12b - 0.1);
      tl.to("#s05-card", { rotation: 4, duration: 0.8, yoyo: true, repeat: 3, ease: "sine.inOut" }, l12b + 0.4);
      tl.fromTo("#s05-price", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, te - 0.1);
      tl.to(["#s05-card", "#s05-price"], { opacity: 0, duration: 0.2 }, l12c - 0.2);
      tl.fromTo("#s05-lt", { opacity: 0, y: 60, rotation: -3 }, { opacity: 1, y: 0, rotation: -3, duration: 0.35, ease: "back.out(1.8)" }, l12c - 0.1);
      tl.fromTo("#s05-st", { opacity: 0, scale: 2.4, rotation: -10 }, { opacity: 1, scale: 1, rotation: -10, duration: 0.25, ease: "power4.in" }, at("L12c", "Zahlt"));
      tl.to("#s05-st", { x: 8, duration: 0.04, repeat: 7, yoyo: true }, le);''' + OUT)

S['s06'] = ('''    .s06-k { position: absolute; top: 640px; width: 470px; border-radius: 24px; background: rgba(12,12,20,.9); text-align: center; opacity: 0; color: #fff; padding: 26px 22px 30px; box-sizing: border-box; }
    .s06-k h3 { font: 700 52px Oswald, sans-serif; letter-spacing: .04em; margin-bottom: 18px; }
    .s06-k p { font: 700 44px/1.25 Oswald, sans-serif; margin-top: 14px; } .s06-k small { display: block; font: 500 30px/1.25 Inter, sans-serif; color: #b9bdcc; margin-top: 4px; }
    #s06-k1 { left: 40px; border: 5px solid #39e27a; } #s06-k1 h3 { color: #39e27a; } #s06-k2 { left: 570px; border: 5px solid #ff3b55; } #s06-k2 h3 { color: #ff3b55; }
    #s06-w { left: 140px; top: 760px; width: 800px; border-radius: 26px; background: rgba(12,12,20,.9); border: 5px solid #ffd43b; text-align: center; color: #ffd43b; opacity: 0; font: 700 70px/1.25 Oswald, sans-serif; padding: 40px 20px; box-sizing: border-box; }''',
SVG + '''
      <div id="s06-k1" class="s06-k"><h3>IM FILM</h3><p>Kriminalität ↓<small>das ganze Jahr ruhig</small></p><p>Arbeitslosigkeit ↓<small>„Ventil“ für Wut</small></p></div>
      <div id="s06-k2" class="s06-k"><h3>IN WAHRHEIT</h3><p>Gewalt → mehr Gewalt<small>Rache am nächsten Tag</small></p><p>Traumata<small>für Millionen</small></p></div>
      <div id="s06-w" class="abs">🛡 SICHERHEITSFIRMEN<br>WAFFENHÄNDLER ↑</div>''',
'''      const sv = document.querySelector("#s06-svg");
      night(sv, "s06-n", "#0c0f1e", "#1c1626", null);
      const im = at("L13", "Im"), wa = at("L14", "Wahrheit"), ra = at("L14", "Rache"), l15 = line("L15")[0], si = at("L15", "Sicherheitsfirmen");
      tl.fromTo("#s06-k1", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, im - 0.1);
      tl.fromTo("#s06-k1 p", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.5 }, im + 0.4);
      tl.fromTo("#s06-k2", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, wa - 0.2);
      tl.fromTo("#s06-k2 p", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.8 }, wa + 0.3);
      tl.to("#s06-k1", { opacity: 0.35, scale: 0.95, duration: 0.3 }, wa);
      tl.to("#s06-k2", { scale: 1.05, duration: 0.3 }, wa);
      tl.to("#s06-k2", { x: 8, duration: 0.04, repeat: 7, yoyo: true }, ra);
      tl.to([".s06-k"], { opacity: 0, duration: 0.25 }, l15 - 0.3);
      tl.fromTo("#s06-w", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, si - 0.2);''' + OUT)

S['s07'] = ('''    #s07-n { left: 0; width: 1080px; top: 640px; text-align: center; font: 700 170px/1 Oswald, sans-serif; color: #ff3b55; text-shadow: 0 0 50px rgba(255,59,85,.6), 0 8px 0 rgba(0,0,0,.6); opacity: 0; }''',
SVG + '''
      <div id="s07-n" class="abs">0</div>''',
'''      const sv = document.querySelector("#s07-svg");
      night(sv, "s07-n2", "#3a1420", "#e8743a", [540, 1020]);
      const smoke = []; const r = rng(3); for (let i = 0; i < 6; i++) smoke.push(el("ellipse", { cx: 120 + i * 170, cy: 900, rx: 70, ry: 140, fill: "#2a2228", opacity: 0.55 }, sv));
      const city = el("g", {}, sv); for (let i = 0; i < 9; i++) { const h = 200 + r() * 260; el("rect", O({ x: i * 125 - 10, y: 1250 - h, width: 120, height: h, fill: "#1c1418" }), city); }
      el("rect", { x: 0, y: 1250, width: 1080, height: 200, fill: "#140e12" }, sv);
      const crowd = el("g", { opacity: 0 }, sv); const ms = [];
      for (let i = 0; i < 40; i++) { const x = 90 + (i % 10) * 100, y = 980 + Math.floor(i / 10) * 90; const g = el("g", {}, crowd);
        el("ellipse", O({ cx: x, cy: y, rx: 26, ry: 32, fill: "#ece6d6", "stroke-width": 3 }), g); el("ellipse", { cx: x - 9, cy: y - 6, rx: 5, ry: 4, fill: K }, g); el("ellipse", { cx: x + 9, cy: y - 6, rx: 5, ry: 4, fill: K }, g);
        el("path", { d: `M${x - 12} ${y + 12} q12 8 24 0`, stroke: "#c8102e", "stroke-width": 3, fill: "none" }, g); ms.push(g); }
      const he = at("L16", "heult"), br = at("L16", "brennen"), l17 = line("L17")[0], ep = at("L17", "ein"), n84 = at("L17", "840.000");
      smoke.forEach((s, i) => tl.to(s, { attr: { cy: 760, ry: 200 }, duration: 5, ease: "none" }, i * 0.2));
      tl.to(city, { x: 6, duration: 0.05, repeat: 5, yoyo: true }, br);
      tl.to(crowd, { opacity: 1, duration: 0.01 }, ep - 0.2);
      ms.forEach((m, i) => tl.fromTo(m, { opacity: 0, scale: 0.3, svgOrigin: `${90 + (i % 10) * 100} ${980 + Math.floor(i / 10) * 90}` }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }, ep - 0.2 + i * 0.04));
      tl.to("#s07-n", { opacity: 1, duration: 0.2 }, n84 - 0.6);
      count(tl, "#s07-n", 0, 840000, n84 - 0.5, 1.2, "", "", "power3.out");
      tl.to("#s07-n", { scale: 1.1, duration: 0.15, yoyo: true, repeat: 3 }, n84 + 0.8);''' + OUT)

S['s08'] = ('''    .s08-b { position: absolute; top: 1150px; width: 450px; height: 140px; border-radius: 22px; text-align: center; font: 700 56px/140px Oswald, sans-serif; color: #0b0c14; opacity: 0; }
    #s08-b1 { left: 50px; background: #39e27a; } #s08-b2 { left: 580px; background: #ff3b55; color: #fff; }
    #s08-f { left: 330px; top: 1170px; width: 420px; height: 120px; border-radius: 60px; background: #ff3b55; color: #fff; text-align: center; font: 700 60px/120px Oswald, sans-serif; opacity: 0; box-shadow: 0 0 50px rgba(255,59,85,.6); }''',
SVG + '''
      <div id="s08-b1" class="s08-b">VERSCHANZEN</div><div id="s08-b2" class="s08-b">TEILNEHMEN</div>
      <div id="s08-f" class="abs">+ FOLGEN</div>''',
'''      const sv = document.querySelector("#s08-svg");
      night(sv, "s08-n", "#06071a", "#200f22", null);
      const room = el("g", {}, sv);
      el("rect", { x: 0, y: 520, width: 1080, height: 1400, fill: "#3a2a22" }, room);
      for (let k = 0; k < 20; k++) el("path", { d: `M0 ${540 + k * 70} H1080`, stroke: "#2a1d18", "stroke-width": 5 }, room);
      const wf = el("rect", O({ x: 300, y: 600, width: 480, height: 440, fill: "#0d1428" }), room);
      el("circle", { cx: 680, cy: 700, r: 40, fill: "#efe6c8" }, room);
      const wcl = el("clipPath", { id: "s08-wc" }, sv); el("rect", { x: 300, y: 600, width: 480, height: 440 }, wcl);
      const wg = el("g", { "clip-path": "url(#s08-wc)" }, room); const M = masked(wg, 470, 1130, 0.9, "#1d1f2b"); gsap.set(M.g, { opacity: 0 });
      el("path", O({ d: "M540 600 V1040 M300 820 H780", fill: "none", stroke: "#a87a4a", "stroke-width": 16 }), room);
      el("rect", O({ x: 280, y: 580, width: 520, height: 480, fill: "none", stroke: "#a87a4a", "stroke-width": 20 }), room);
      const beam = el("path", { d: "M470 790 L300 1040 H640Z", fill: "#fff7c0", opacity: 0 }, room);
''' + RED + '''      const du = at("L18", "du?"), ei = at("L18", "verschanzen"), ra = at("L18", "teilnehmen"), ko = at("L18", "Kommentare"), l19 = line("L19")[0], fo = at("L19", "folg"), si = at("L19", "Sirene");
      tl.fromTo(M.g, { opacity: 0, x: 380 }, { opacity: 1, x: 470, duration: 1.2, ease: "power2.out" }, du);
      tl.to(beam, { opacity: 0.35, duration: 0.2, repeat: 3, yoyo: true }, du + 1.0);
      tl.fromTo("#s08-b2", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, ra - 0.15);
      tl.fromTo("#s08-b1", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, ei - 0.15);
      tl.to(".s08-b", { opacity: 0, y: 40, duration: 0.25 }, l19 - 0.2);
      tl.fromTo("#s08-f", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, fo - 0.1);
      tl.to("#s08-f", { scale: 1.07, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.35, duration: 0.25, repeat: 9, yoyo: true, ease: "sine.inOut" }, si - 0.2);
      tl.to(M.mask, { scale: 1.12, svgOrigin: "0 -345", duration: 0.3, yoyo: true, repeat: 3 }, si);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
