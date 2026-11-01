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

LAB = '''    .lab { position: absolute; padding: 10px 24px; border-radius: 18px; background: rgba(20,10,50,.82); border: 3px solid #8ff4ff; color: #fff; font: 900 52px Inter, sans-serif; opacity: 0; box-shadow: 0 0 30px rgba(143,244,255,.4); white-space: nowrap; }
    .lab.r { border-color: #ff6b8a; box-shadow: 0 0 30px rgba(255,107,138,.5); } .lab.g { border-color: #7dffb0; box-shadow: 0 0 30px rgba(125,255,176,.5); } .lab.y { border-color: #ffd84a; }'''
def popin(sel, t, d=0.25): return f'\n      tl.fromTo("{sel}", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(2.5)" }}, {t});'
def cut(a, b, t): return f'\n      tl.set({a}, {{ opacity: 0 }}, {t}); tl.set({b}, {{ opacity: 1 }}, {t});'

S['s01'] = (LAB + '''
    #s01-clk { left: 330px; top: 300px; width: 660px; height: 230px; border-radius: 40px; background: linear-gradient(#ff9a5a, #d8542e); padding: 16px; box-shadow: 0 0 60px rgba(255,120,60,.6); }
    #s01-clk .in { width: 100%; height: 100%; border-radius: 26px; background: #2a0e2e; text-align: center; font: 700 116px/198px "Space Mono", monospace; color: #ff8a4a; text-shadow: 0 0 24px rgba(255,138,74,.9); letter-spacing: -.02em; }''',
SVG + '''
      <div id="s01-clk" class="abs"><div class="in" id="s01-t">22:45:45</div></div>''',
'''      const sv = document.querySelector("#s01-svg"), A = el("g", {}, sv), Bz = el("g", { opacity: 0 }, sv); room(A, "s01a"); defsG(sv);
      el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "url(#s01-svgR)", opacity: 0.25 }, A);
      const P = sitter(A, 330, 1150, 2.4);
      room(Bz, "s01b", "#251a6e", "#7a2fa0"); const H = brainHead(Bz, 470, 900, 1.7);
      const ge = at("L2", "Gehirn"), l2 = line("L2")[0];
      for (let k = 1; k <= 7; k++) tl.set("#s01-t", { textContent: "22:45:" + (45 + k) }, k * 0.8);
      tl.fromTo(A, { scale: 1, svgOrigin: "540 900" }, { scale: 1.08, svgOrigin: "540 900", duration: ge, ease: "none" }, 0);
      tl.to(P.head, { rotation: 6, svgOrigin: "-10 -200", duration: 1.2, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0.5);
      tl.to("#s01-clk", { opacity: 0, duration: 0.15 }, ge - 0.25);''' + cut("A", "Bz", "ge - 0.25") + '''
      H.rings.forEach((r, i) => tl.fromTo(r, { scale: 0.6, opacity: 0, svgOrigin: "0 -40" }, { scale: 1.1, opacity: 0.9 - i * 0.12, svgOrigin: "0 -40", duration: 1.2, repeat: 2, ease: "power1.out", immediateRender: false }, ge - 0.25 + i * 0.12));
      tl.fromTo(H.br, { scale: 0.9, svgOrigin: "10 -50" }, { scale: 1.06, svgOrigin: "10 -50", duration: 0.4, yoyo: true, repeat: 5, immediateRender: false }, ge);''' + OUT)

S['s02'] = (LAB, SVG + '''
      <div id="s02-l1" class="lab g" style="left:520px;top:420px">„Hab noch Zeit“</div>''',
'''      const sv = document.querySelector("#s02-svg"), A = el("g", {}, sv), Bz = el("g", { opacity: 0 }, sv), Cz = el("g", { opacity: 0 }, sv); room(A, "s02a", "#2b1366", "#9a3a8a"); defsG(sv);
      const K = aclock(A, 760, 760, 150); const P = person(A, 360, 1380, 2.2);
      room(Bz, "s02b", "#1f1450", "#6a2f9a");
      el("rect", { x: 140, y: 1040, width: 800, height: 40, rx: 12, fill: "#3b2a8a" }, Bz); el("rect", { x: 330, y: 820, width: 420, height: 230, rx: 16, fill: "#22164f", stroke: "#8ff4ff", "stroke-width": 6 }, Bz);
      const P2 = person(Bz, 540, 1400, 2.0);
      const lines = []; for (let i = 0; i < 6; i++) lines.push(el("rect", { x: 160 + (i % 2) * 560, y: 900 + i * 40, width: 200, height: 10, rx: 5, fill: "#8ff4ff", opacity: 0 }, Bz));
      room(Cz, "s02c", "#3a0d3a", "#c02a5a"); const K2 = aclock(Cz, 540, 820, 230);
      const ze = at("L3", "Zeit"), sc = at("L3", "schnell"), l4 = line("L4")[0], pl = at("L4", "plötzlich");
      tl.to(P.head, { rotation: 18, svgOrigin: "0 -270", duration: 0.3 }, line("L3")[0] + 0.8);
      tl.to(K.m, { rotation: 30, svgOrigin: "760 760", duration: 2, ease: "none" }, 0.3);''' + popin("#s02-l1", "ze - 0.6") + '''
      tl.to("#s02-l1", { opacity: 0, duration: 0.15 }, sc - 0.6);''' + cut("A", "Bz", "sc - 0.6") + '''
      tl.to([P2.aL, P2.aR], { y: -8, duration: 0.06, yoyo: true, repeat: 40 }, sc - 0.5);
      tl.to(lines, { opacity: 0.9, x: -60, duration: 0.2, stagger: 0.05, yoyo: true, repeat: 9 }, sc - 0.4);''' + cut("Bz", "Cz", "pl - 0.3") + '''
      tl.fromTo(K2.m, { rotation: 0, svgOrigin: "540 820" }, { rotation: 1080, svgOrigin: "540 820", duration: 1.6, ease: "power2.in", immediateRender: false }, pl - 0.3);
      tl.fromTo(K2.h, { rotation: 0, svgOrigin: "540 820" }, { rotation: 90, svgOrigin: "540 820", duration: 1.6, ease: "power2.in", immediateRender: false }, pl - 0.3);
      tl.to(Cz, { x: 12, duration: 0.04, repeat: 9, yoyo: true }, pl + 1.2);''' + OUT)

S['s03'] = (LAB + '''
    #s03-sw { left: 300px; top: 560px; width: 480px; height: 480px; border-radius: 50%; background: #e9ecff; border: 22px solid #3b2a8a; text-align: center; font: 900 120px/436px "Space Mono", monospace; color: #22164f; opacity: 0; box-shadow: 0 0 60px rgba(143,244,255,.5); }''',
SVG + '''
      <div id="s03-sw" class="abs">00:00</div>
      <div id="s03-pf" class="lab r" style="left:280px;top:1260px">PUFFER: 0 MIN</div>''',
'''      const sv = document.querySelector("#s03-svg"), A = el("g", {}, sv), Bz = el("g", { opacity: 0 }, sv); room(A, "s03a", "#1e1650", "#5a2a8a"); defsG(sv);
      for (let i = 0; i < 4; i++) { el("rect", { x: 80 + i * 230, y: 1180, width: 190, height: 30, rx: 10, fill: "#4a3a9a" }, A); el("rect", { x: 90 + i * 230, y: 1040, width: 170, height: 150, rx: 14, fill: "#3b2a8a" }, A); }
      const P = person(A, 425, 1380, 1.9);
      const hg = el("g", {}, A); el("path", { d: "M700 560 H900 L820 700 L900 840 H700 L780 700Z", fill: "none", stroke: "#8ff4ff", "stroke-width": 10 }, hg);
      const sandT = el("path", { d: "M720 575 H880 L800 690Z", fill: "#ffd84a" }, hg), sandB = el("path", { d: "M800 830 L800 830 L800 830Z", fill: "#ff6b8a" }, hg);
      room(Bz, "s03b", "#2a1060", "#a02f7a");
      const ve = at("L5", "verschwendete"), l6 = line("L6")[0], se = at("L6", "Sekunde"), oh = at("L6", "Ohne");
      tl.to(P.head, { rotation: -14, svgOrigin: "0 -270", duration: 1.5, yoyo: true, repeat: 2, ease: "sine.inOut" }, 0.3);
      tl.to(sandT, { attr: { d: "M790 680 H810 L800 690Z" }, duration: ve - 0.3, ease: "none" }, 0.3);
      tl.to(sandB, { attr: { d: "M720 830 Q800 740 880 830Z" }, duration: ve - 0.3, ease: "none" }, 0.3);
      tl.fromTo(hg, { rotation: 0, svgOrigin: "800 700" }, { rotation: 180, svgOrigin: "800 700", duration: 0.5, immediateRender: false }, ve);''' + cut("A", "Bz", "l6 - 0.1") + '''
      tl.fromTo("#s03-sw", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, l6 - 0.1);
      tl.to("#s03-sw", { scale: 1.08, duration: 0.12, yoyo: true, repeat: 3 }, se);''' + popin("#s03-pf", "oh - 0.1") + OUT)

S['s04'] = (LAB + '''
    .s04-b { position: absolute; bottom: 640px; width: 220px; border-radius: 18px 18px 0 0; }
    #s04-a { left: 220px; height: 0; background: linear-gradient(#7dffb0, #2aa86a); box-shadow: 0 0 40px rgba(125,255,176,.6); }
    #s04-b { left: 560px; height: 0; background: linear-gradient(#ff8a9a, #c42a4a); box-shadow: 0 0 40px rgba(255,107,138,.6); }''',
SVG + '''
      <div id="s04-a" class="s04-b"></div><div id="s04-b" class="s04-b"></div>
      <div id="s04-la" class="lab g" style="left:190px;top:1300px">34 TAGE</div><div id="s04-lb" class="lab r" style="left:530px;top:1300px">55 TAGE</div>
      <div id="s04-pa" class="lab" style="left:185px;top:330px;font-size:38px">GESCHÄTZT</div><div id="s04-pb" class="lab r" style="left:540px;top:330px;font-size:38px">ECHT</div>''',
'''      const sv = document.querySelector("#s04-svg"), A = el("g", {}, sv), Bz = el("g", { opacity: 0 }, sv); room(A, "s04a", "#1a1660", "#4a2a9a"); defsG(sv);
      const nodes = [], rn = rng(4); for (let i = 0; i < 9; i++) nodes.push([150 + rn() * 780, 450 + rn() * 900]);
      nodes.forEach(([x, y], i) => { const [x2, y2] = nodes[(i + 3) % 9]; glowLine(A, `M${x} ${y} Q${(x + x2) / 2 + 60} ${(y + y2) / 2 - 80} ${x2} ${y2}`, "#5ff0e0", 6); });
      const cells = nodes.map(([x, y]) => { const g = el("g", {}, A); el("circle", { cx: x, cy: y, r: 60, fill: U(sv, "R") }, g); el("circle", { cx: x, cy: y, r: 26, fill: U(sv, "B") }, g); return g; });
      room(Bz, "s04b", "#1e1450", "#5a2a8a"); el("rect", { x: 140, y: 1280, width: 800, height: 8, fill: "#8ff4ff" }, Bz);
      const pf = at("L7", "Planungsfehlschluss"), l8 = line("L8")[0], d34 = at("L8", "34"), d55 = at("L8", "55");
      A.querySelectorAll("path[stroke-dasharray]").forEach((p, i) => tl.to(p, { attr: { "stroke-dashoffset": 0 }, duration: 1.2, ease: "power1.out" }, 0.3 + i * 0.1));
      cells.forEach((c, i) => tl.fromTo(c, { scale: 0.6, opacity: 0.5, svgOrigin: `${nodes[i][0]} ${nodes[i][1]}` }, { scale: 1.1, opacity: 1, svgOrigin: `${nodes[i][0]} ${nodes[i][1]}`, duration: 0.5, yoyo: true, repeat: 3, immediateRender: false }, pf - 0.4 + i * 0.05));''' + cut("A", "Bz", "l8") + '''
      tl.to(["#s04-pa", "#s04-pb"], { opacity: 1, duration: 0.2 }, l8 + 0.2);
      tl.to("#s04-a", { height: 34 * 12, duration: 0.6, ease: "power2.out" }, d34 - 0.2);''' + popin("#s04-la", "d34") + '''
      tl.to("#s04-b", { height: 55 * 12, duration: 0.8, ease: "power2.out" }, d55 - 0.5);''' + popin("#s04-lb", "d55") + OUT)

S['s05'] = (LAB, SVG + '''
      <div id="s05-l1" class="lab y" style="left:150px;top:1250px">1 STUNDE</div><div id="s05-l2" class="lab g" style="left:560px;top:1250px">= 10 MIN</div>''',
'''      const sv = document.querySelector("#s05-svg"), A = el("g", {}, sv), Bz = el("g", { opacity: 0 }, sv); room(A, "s05a", "#141048", "#3a2a9a"); defsG(sv);
      const sw = []; for (let i = 0; i < 5; i++) sw.push(el("ellipse", { cx: 540, cy: 800, rx: 200 + i * 70, ry: 120 + i * 40, fill: "none", stroke: ["#8ff4ff", "#ff9ad6", "#7dffb0"][i % 3], "stroke-width": 5, opacity: 0.6 }, A));
      el("rect", { x: 180, y: 1120, width: 720, height: 36, rx: 12, fill: "#3b2a8a" }, A); const P = person(A, 540, 1300, 2.0);
      room(Bz, "s05b", "#1e1450", "#6a2f9a"); const K = aclock(Bz, 540, 820, 260);
      const fl = at("L9", "Flow"), ze = at("L9", "Zeitgefühl"), l10 = line("L10")[0], mi = at("L10", "Minuten");
      sw.forEach((e, i) => tl.fromTo(e, { rotation: 0, svgOrigin: "540 800" }, { rotation: i % 2 ? -360 : 360, svgOrigin: "540 800", duration: 6, ease: "none", immediateRender: false }, 0));
      tl.fromTo(sw, { opacity: 0 }, { opacity: 0.7, duration: 0.4, stagger: 0.1 }, fl - 0.2);''' + cut("A", "Bz", "l10 - 0.1") + '''
      tl.fromTo(K.m, { rotation: 0, svgOrigin: "540 820" }, { rotation: 360, svgOrigin: "540 820", duration: 0.8, ease: "power1.inOut", immediateRender: false }, l10);''' + popin("#s05-l1", "l10 + 0.2") + popin("#s05-l2", "mi - 0.2") + OUT)

S['s06'] = (LAB + '''
    #s06-n { left: 240px; top: 600px; width: 600px; text-align: center; font: 900 260px/1 "Space Mono", monospace; color: #fff; text-shadow: 0 0 40px rgba(143,244,255,.8); }
    #s06-u { left: 240px; top: 880px; width: 600px; text-align: center; font: 900 50px Inter, sans-serif; color: #8ff4ff; letter-spacing: .2em; }''',
SVG + '''
      <div id="s06-n" class="abs">0</div><div id="s06-u" class="abs">SEKUNDEN</div>
      <div id="s06-l" class="lab" style="left:300px;top:380px">1 MINUTE?</div>''',
'''      const sv = document.querySelector("#s06-svg"); room(sv, "s06a", "#2a0d50", "#8a2a7a");
      const ring = el("circle", { cx: 540, cy: 760, r: 330, fill: "none", stroke: "#8ff4ff", "stroke-width": 16, "stroke-dasharray": 2074, "stroke-dashoffset": 2074, transform: "rotate(-90 540 760)" }, sv);
      const s7 = at("L11", "77"), l11 = line("L11")[0];''' + popin("#s06-l", "l11 + 0.3") + '''
      count(tl, "#s06-n", 0, 60, l11 + 0.4, s7 - l11 - 1.4, "", "", "none");
      tl.to(ring, { attr: { "stroke-dashoffset": 0 }, duration: s7 - l11 - 1.4, ease: "none" }, l11 + 0.4);
      count(tl, "#s06-n", 60, 77, s7 - 1.0, 1.0, "", "", "none");
      tl.to("#s06-n", { color: "#ff6b8a", textShadow: "0 0 50px rgba(255,107,138,1)", duration: 0.2 }, s7 - 1.0);
      tl.to(ring, { attr: { stroke: "#ff6b8a" }, duration: 0.2 }, s7 - 1.0);
      tl.to("#s06-n", { scale: 1.15, duration: 0.15, yoyo: true, repeat: 3 }, s7);''' + OUT)

S['s07'] = (LAB, SVG + '''
      <div id="s07-a" class="lab g" style="left:470px;top:400px">10 MIN</div><div id="s07-b" class="lab r" style="left:300px;top:1250px;font-size:80px">25 MIN</div>''',
'''      const sv = document.querySelector("#s07-svg"), A = el("g", {}, sv), Bz = el("g", { opacity: 0 }, sv); room(A, "s07a", "#251a6e", "#7a2fa0"); defsG(sv);
      const H = brainHead(A, 380, 980, 1.5);
      const r1 = glowLine(A, "M560 640 Q700 520 860 600", "#7dffb0", 10);
      room(Bz, "s07b", "#1a1240", "#4a2a7a");
      for (let i = 0; i < 6; i++) el("rect", { x: 0, y: 500 + i * 140, width: 1080, height: 10, fill: "#3b2a8a" }, Bz);
      for (let i = 0; i < 6; i++) el("rect", { x: 80 + i * 180, y: 420, width: 10, height: 860, fill: "#3b2a8a" }, Bz);
      const r2 = glowLine(Bz, "M120 1200 L120 920 L470 920 L470 640 L300 640 L300 500 L760 500 L760 780 L940 780", "#ff6b8a", 12);
      const pin = el("circle", { cx: 940, cy: 780, r: 26, fill: "#ffd84a" }, Bz);
      const si = at("L12", "simuliert"), ze = at("L12", "zehn"), l13 = line("L13")[0], fz = at("L13", "fünfundzwanzig");
      H.rings.forEach((r, i) => tl.fromTo(r, { scale: 0.6, opacity: 0, svgOrigin: "0 -40" }, { scale: 1.1, opacity: 0.8 - i * 0.1, svgOrigin: "0 -40", duration: 1.1, repeat: 3, immediateRender: false }, 0.3 + i * 0.1));
      tl.to(r1.l, { attr: { "stroke-dashoffset": 2700 }, duration: 0.6 }, si);''' + popin("#s07-a", "ze - 0.1") + '''
      tl.to("#s07-a", { opacity: 0, duration: 0.15 }, l13 - 0.2);''' + cut("A", "Bz", "l13 - 0.2") + '''
      tl.to(r2.l, { attr: { "stroke-dashoffset": 0 }, duration: fz - l13 + 0.2, ease: "none" }, l13 - 0.2);''' + popin("#s07-b", "fz") + OUT)

S['s10'] = (LAB, SVG + '''
      <div id="s10-a" class="lab g" style="left:140px;top:420px">DUSCHEN: 3 MIN</div><div id="s10-b" class="lab g" style="left:140px;top:540px">ANZIEHEN: 1 MIN</div>
      <div id="s10-c" class="lab r" style="left:240px;top:1250px;font-size:84px">20 MIN</div>
      <div id="s10-d" class="lab y" style="left:330px;top:400px;font-size:90px">+5 MIN</div>''',
'''      const sv = document.querySelector("#s10-svg"), A = el("g", {}, sv), Bz = el("g", { opacity: 0 }, sv); room(A, "s10a", "#123a6e", "#4a2a9a"); defsG(sv);
      el("rect", { x: 520, y: 640, width: 24, height: 120, fill: "#c9d4ff" }, A); el("path", { d: "M460 760 H610 L590 800 H480Z", fill: "#e9ecff" }, A);
      const drops = []; for (let i = 0; i < 18; i++) drops.push(el("line", { x1: 480 + (i % 6) * 22, y1: 820, x2: 480 + (i % 6) * 22, y2: 850, stroke: "#8ff4ff", "stroke-width": 6, "stroke-linecap": "round" }, A));
      const P = person(A, 535, 1400, 1.8);
      const K = aclock(A, 870, 1000, 110);
      room(Bz, "s10b", "#2a1060", "#a02f7a");
      el("rect", { x: 380, y: 620, width: 320, height: 760, rx: 12, fill: "#3b2a8a", stroke: "#8ff4ff", "stroke-width": 8 }, Bz); el("circle", { cx: 660, cy: 1000, r: 14, fill: "#ffd84a" }, Bz);
      const crowd = []; for (let i = 0; i < 5; i++) crowd.push(person(Bz, 120 + i * 50 + (i > 2 ? 620 : 0), 1450, 0.9));
      const P2 = person(Bz, 540, 1420, 1.5); gsap.set(P2.g, { opacity: 0 });
      const an = at("L13b", "Anziehen"), l13c = line("L13c")[0], zw = at("L13c", "zwanzig"), l13d = line("L13d")[0], fu = at("L13d", "fünf");
      drops.forEach((d, i) => tl.fromTo(d, { y: 0, opacity: 1 }, { y: 420, opacity: 0.3, duration: 0.5, repeat: Math.ceil(l13d / 0.5), ease: "none", immediateRender: false }, (i % 6) * 0.08));''' + popin("#s10-a", "line('L13b')[0] + 0.9") + popin("#s10-b", "an - 0.1") + '''
      tl.fromTo(K.m, { rotation: 0, svgOrigin: "870 1000" }, { rotation: 1440, svgOrigin: "870 1000", duration: 1.6, ease: "power2.in", immediateRender: false }, l13c);''' + popin("#s10-c", "zw - 0.1") + '''
      tl.to(["#s10-a", "#s10-b", "#s10-c"], { opacity: 0, duration: 0.15 }, l13d - 0.2);''' + cut("A", "Bz", "l13d - 0.2") + '''
      crowd.forEach((c, i) => tl.to(c.head, { rotation: i < 3 ? 14 : -14, svgOrigin: "0 -270", duration: 0.3 }, fu - 0.6));
      tl.fromTo(P2.g, { opacity: 0, y: 1500 }, { opacity: 1, y: 1420, duration: 0.4 }, fu - 0.5);''' + popin("#s10-d", "fu") + OUT)

S['s08'] = (LAB + '''
    #s08-bar { left: 140px; top: 820px; width: 560px; height: 90px; border-radius: 16px; background: linear-gradient(90deg, #8ff4ff, #6d63e8); box-shadow: 0 0 40px rgba(143,244,255,.5); opacity: 0; }
    #s08-pz { left: 700px; top: 820px; width: 0; height: 90px; border-radius: 0 16px 16px 0; background: #7dffb0; box-shadow: 0 0 40px rgba(125,255,176,.7); }''',
SVG + '''
      <div id="s08-bar" class="abs"></div><div id="s08-pz" class="abs"></div>
      <div id="s08-l" class="lab g" style="left:470px;top:950px">+33 % PUFFER</div>''',
'''      const sv = document.querySelector("#s08-svg"), A = el("g", {}, sv), Bz = el("g", { opacity: 0 }, sv); room(A, "s08a", "#2a1158", "#8a2b8f"); defsG(sv);
      const H = brainHead(A, 470, 920, 1.6); const q = txt(A, 480, 900, "?", 240, "#fff", { opacity: 0 });
      room(Bz, "s08b", "#16305e", "#3a2a9a");
      const ni = at("L14", "nicht"), l15 = line("L15")[0], dr = at("L15", "Drittel"), im = at("L15", "Immer");
      tl.to(q, { opacity: 1, duration: 0.2 }, ni - 0.2); tl.to(H.br, { opacity: 0.4, duration: 0.3 }, ni - 0.2);''' + cut("A", "Bz", "l15 - 0.1") + '''
      tl.fromTo("#s08-bar", { opacity: 0, scaleX: 0, transformOrigin: "0 50%" }, { opacity: 1, scaleX: 1, duration: 0.4 }, l15);
      tl.to("#s08-pz", { width: 190, duration: 0.5, ease: "back.out(1.5)" }, dr - 0.2);''' + popin("#s08-l", "dr + 0.2") + '''
      tl.to("#s08-pz", { boxShadow: "0 0 70px rgba(125,255,176,1)", duration: 0.2, yoyo: true, repeat: 3 }, im);''' + OUT)

S['s09'] = (LAB + '''
    #s09-f { left: 290px; top: 1310px; width: 500px; height: 124px; border-radius: 62px; background: #ff3b5c; color: #fff; text-align: center; font: 900 60px/124px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 50px rgba(255,59,92,.7); }''',
SVG + '''
      <div id="s09-f" class="abs">+ Folgen</div>''',
'''      const sv = document.querySelector("#s09-svg"), A = el("g", {}, sv); room(A, "s09a", "#2a1158", "#a4307f"); defsG(sv);
      const H = brainHead(A, 470, 760, 1.5);
      const P = person(A, 760, 1040, 1.4);
      const fr = at("L16", "Frage"), ho = at("L16", "hochintelligent"), fo = at("L16", "folgst");
      H.rings.forEach((r, i) => tl.fromTo(r, { scale: 0.6, opacity: 0, svgOrigin: "0 -40" }, { scale: 1.1, opacity: 0.8 - i * 0.1, svgOrigin: "0 -40", duration: 1.1, repeat: 5, immediateRender: false }, 0.2 + i * 0.1));
      tl.to(P.aR, { rotation: -60, svgOrigin: "52 -236", duration: 0.3 }, fo - 0.2);
      tl.fromTo("#s09-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s09-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 11, ease: "sine.inOut" }, fo + 0.4);''')
here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
