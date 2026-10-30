#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Welt in Deutschland“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
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
NEWS = '''    #@@ID@@-news { left: 60px; top: 975px; width: 960px; height: 172px; border: 5px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.5); overflow: hidden; text-align: left; }
    #@@ID@@-news .bar { height: 44px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 30px; font-size: 32px; letter-spacing: .08em; }
    #@@ID@@-news .hl { padding: 4px 36px 0; text-align: center; font-size: 60px; line-height: 1.0; letter-spacing: -.015em; }
    #@@ID@@-news .hl em { font-style: normal; color: #ffd43b; text-shadow: 0 0 26px rgba(255,212,59,.7); }'''
BOX = '    .bx .num { font-size: 44px; }'
def box(sid, n, col, lab, num, nid=True):
    return f'      <div id="{sid}-box{n}" class="cbox {col} bx" style="opacity:0"><div class="lab">{lab}</div><div{" id=" + chr(34) + sid + "-n" + str(n) + chr(34) if nid else ""} class="num">{num}</div></div>\n'

S['s01'] = (NEWS + '\n' + BOX + '''
    #s01-q { left: 190px; top: 600px; width: 700px; height: 380px; border: 5px solid #39e27a; color: #39e27a; font-size: 130px; line-height: 1.05; padding-top: 40px; box-sizing: border-box; opacity: 0; box-shadow: 0 0 50px rgba(57,226,122,.45); }
    #s01-q small { display: block; font-size: 52px; color: #fff; letter-spacing: .04em; }''',
box('s01', 1, 'p', 'EINWOHNER DEUTSCHLAND', '84.000.000') + SVG + '''
      <div id="s01-news" class="panel"><div class="bar">● EILMELDUNG · LIVE</div><div class="hl">8 MILLIARDEN<br><em>IN DEUTSCHLAND!</em></div></div>
      <div id="s01-q" class="panel">?!<small>DER REST DER WELT</small></div>''',
'''      const sv = document.querySelector("#s01-svg");
      const glow = el("circle", { cx: 540, cy: 760, r: 260, fill: "#ff4fb0", opacity: 0.16 }, sv);
      const map = germany(sv, 540, 760, 400);
      const pts = dePoints(540, 760, 400, 260, 3), r = rng(5), dots = [];
      const COL = ["#ffd43b", "#4da3ff", "#39e27a", "#ff8a3d", "#ff4fb0", "#ffffff"];
      pts.forEach(([x, y], i) => { const a = r() * Math.PI * 2, d = 700 + r() * 300;
        dots.push({ e: el("circle", { cx: x, cy: y, r: 7, fill: COL[i % 6] }, sv), fx: Math.cos(a) * d, fy: Math.sin(a) * d }); });
      const first = dots.slice(0, 90), rest = dots.slice(90);
      gsap.set(rest.map((d) => d.e), { opacity: 0 });
      const de = at("L1", "Deutschland"), n82 = at("L2", "8,2"), ei = at("L2", "einem"), re = at("L2", "Rest");
      first.forEach((d, i) => tl.from(d.e, { x: d.fx, y: d.fy, duration: 1.4, ease: "power2.out" }, -0.6 + (i % 30) * 0.02));
      tl.fromTo(glow, { attr: { opacity: 0.16 } }, { attr: { opacity: 0.4 }, duration: 0.4, repeat: 5, yoyo: true }, 0);
      tl.to("#s01-news", { opacity: 0, scale: 0.85, duration: 0.25, ease: "power3.in" }, 2.6);
      tl.to(map, { scale: 1.08, svgOrigin: "540 760", duration: 0.15, yoyo: true, repeat: 1 }, de);
      tl.to("#s01-box1", { opacity: 1, duration: 0.2 }, n82 - 0.4);
      count(tl, "#s01-n1", 84000000, 8200000000, n82 - 0.3, 1.2, "", "", "power3.in");
      rest.forEach((d, i) => tl.fromTo(d.e, { opacity: 0, x: d.fx * 0.6, y: d.fy * 0.6 }, { opacity: 1, x: 0, y: 0, duration: 0.6, ease: "power2.out" }, n82 - 0.2 + (i % 40) * 0.02));
      tl.to(map, { attr: { fill: "#5a2346", stroke: "#ff3b55" }, duration: 0.4 }, n82 + 0.4);
      tl.to(sv, { x: 8, duration: 0.04, repeat: 9, yoyo: true }, ei);
      tl.to([map, glow, ...dots.map((d) => d.e)], { opacity: 0, filter: "blur(8px)", duration: 0.25 }, re - 0.75);
      tl.to("#s01-box1", { opacity: 0, duration: 0.2 }, re - 0.75);
      tl.fromTo("#s01-q", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, re - 0.55);
      tl.to("#s01-q", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, re + 0.3);''' + OUT)

S['s02'] = (BOX, box('s02', 1, 'b', 'FLÄCHE', '0 KM²') + box('s02', 2, 'r', 'PRO PERSON', '0 M²') + box('s02', 3, 'r', 'MENSCHEN PRO KM²', '0') + SVG,
'''      const sv = document.querySelector("#s02-svg");
      const map = germany(sv, 540, 830, 520, { fill: "#2e3670", stroke: "#4da3ff" });
      const room = el("g", { opacity: 0 }, sv);
      el("rect", { x: 240, y: 600, width: 600, height: 480, rx: 10, fill: "#262d63", stroke: "#dfe2f5", "stroke-width": 8 }, room);
      for (let k = 1; k < 6; k++) el("path", { d: `M${240 + k * 100} 600 V1080`, stroke: "#3a4280", "stroke-width": 3 }, room);
      for (let k = 1; k < 5; k++) el("path", { d: `M240 ${600 + k * 96} H840`, stroke: "#3a4280", "stroke-width": 3 }, room);
      const tree = el("g", { opacity: 0 }, room); el("rect", { x: 312, y: 760, width: 22, height: 70, fill: "#8a5a2b" }, tree); el("circle", { cx: 323, cy: 735, r: 55, fill: "#39e27a" }, tree);
      const lake = el("ellipse", { cx: 700, cy: 700, rx: 100, ry: 55, fill: "#4da3ff", opacity: 0 }, room);
      const road = el("g", { opacity: 0 }, room); el("rect", { x: 240, y: 940, width: 600, height: 80, fill: "#3b4b6e" }, road); el("path", { d: "M250 980 H830", stroke: "#ffd43b", "stroke-width": 6, "stroke-dasharray": "30 22" }, road);
      const me = mini(room, 560, 820, "#ff4fb0"); gsap.set(me, { opacity: 1, scale: 2.2, svgOrigin: "560 840" });
      const sky = el("g", { opacity: 0 }, sv), r = rng(12);
      for (let i = 0; i < 14; i++) { const w = 60 + r() * 30, h = 220 + r() * 300, x = 20 + i * 75; el("rect", { x, y: 1130 - h, width: w, height: h, fill: ["#3a4078", "#4f5a9a", "#2e3670"][i % 3] }, sky);
        for (let k = 0; k < Math.floor(h / 60); k++) el("rect", { x: x + 10, y: 1110 - h + 30 + k * 60, width: w - 20, height: 14, fill: "#ffd43b", opacity: 0.7 }, sky); }
      const qk = at("L3", "357.000"), n44 = at("L4", "44"), wa = at("L4", "Wald"), se = at("L4", "Seen"), au = at("L4", "Autobahn"), l4b = line("L4b")[0], ma = at("L4b", "Manhattan"), ue = at("L4b", "Überall");
      tl.fromTo(map, { opacity: 0, scale: 0.8, svgOrigin: "540 830" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 0.05);
      tl.to("#s02-box1", { opacity: 1, duration: 0.2 }, qk - 0.3);
      count(tl, "#s02-n1", 0, 357000, qk - 0.2, 1.2, "", " KM²", "power3.out");
      tl.to(map, { opacity: 0, scale: 3, svgOrigin: "540 830", duration: 0.4, ease: "power3.in" }, n44 - 0.6);
      tl.to("#s02-box1", { opacity: 0, duration: 0.15 }, n44 - 0.5);
      tl.to("#s02-box2", { opacity: 1, duration: 0.2 }, n44 - 0.4);
      count(tl, "#s02-n2", 0, 44, n44 - 0.3, 0.8, "", " M²", "power3.out");
      tl.fromTo(room, { opacity: 0, scale: 0.4, svgOrigin: "540 840" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, n44 - 0.3);
      tl.fromTo(tree, { opacity: 0, scale: 0.2, svgOrigin: "323 830" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, wa - 0.1);
      tl.to(lake, { opacity: 1, duration: 0.25 }, se - 0.1);
      tl.fromTo(road, { opacity: 0, x: -300 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, au - 0.1);
      tl.to(room, { opacity: 0, duration: 0.25 }, l4b - 0.3);
      tl.to("#s02-box2", { opacity: 0, duration: 0.15 }, l4b - 0.3);
      tl.to("#s02-box3", { opacity: 1, duration: 0.2 }, ma - 0.5);
      count(tl, "#s02-n3", 0, 22900, ma - 0.4, 1.0, "", "", "power3.out");
      tl.fromTo(sky, { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, ma - 0.3);
      tl.to(sky, { x: 8, duration: 0.04, repeat: 7, yoyo: true }, ue);''' + OUT)

S['s03'] = ('''    .s03-l { position: absolute; width: 220px; text-align: center; font: 900 34px/1.1 Inter, sans-serif; color: #fff; }''',
SVG + '''
      <div class="s03-l" style="left:70px;top:1088px">BERLIN</div><div class="s03-l" style="left:310px;top:1088px">USA</div>
      <div class="s03-l" style="left:550px;top:1088px">HAMBURG</div><div class="s03-l" style="left:790px;top:1088px">TOKIO*</div>''',
'''      const sv = document.querySelector("#s03-svg");
      el("path", { d: "M60 1080 H1020", stroke: "#8f9bc4", "stroke-width": 6 }, sv);
      const B = [[180, "#ff4fb0", 480, 370], [420, "#4da3ff", 435, 335], [660, "#ff8a3d", 240, 185], [900, "#8f9bc4", 48, 37]];
      const bars = B.map(([x, c, h]) => el("rect", { x: x - 90, y: 1080, width: 180, height: 0, rx: 12, fill: c }, sv));
      const vals = B.map(([x, c, h, v]) => txt(sv, x, 1060 - h, `${v} MIO`, 44, "#ffffff", { opacity: 0 }));
      const crowns = [180, 660].map((x, i) => { const g = el("g", { opacity: 0 }, sv); const y = 1080 - B[i * 2][2] - 120;
        el("path", { d: `M${x - 50} ${y + 40} L${x - 50} ${y} L${x - 25} ${y + 20} L${x} ${y - 10} L${x + 25} ${y + 20} L${x + 50} ${y} L${x + 50} ${y + 40}Z`, fill: "#ffd43b" }, g); return g; });
      const tk = txt(sv, 900, 640, "*HEUTE", 30, "#8f9bc4", { opacity: 0 });
      const be = at("L5", "370"), us = at("L5", "USA"), hh = at("L6", "185"), gr = at("L6", "größten");
      const grow = (i, t) => { tl.to(bars[i], { attr: { y: 1080 - B[i][2], height: B[i][2] }, duration: 0.6, ease: "power3.out" }, t); tl.to(vals[i], { opacity: 1, duration: 0.2 }, t + 0.4); };
      grow(0, be - 0.3); grow(1, us - 0.3); grow(2, hh - 0.3); grow(3, gr - 0.3);
      tl.to(".s03-l", { opacity: 1, duration: 0.01 }, 0);
      tl.fromTo(".s03-l", { opacity: 0 }, { opacity: 1, duration: 0.3, stagger: 0.1 }, 0.1);
      tl.to(tk, { opacity: 1, duration: 0.2 }, gr);
      crowns.forEach((c, i) => tl.fromTo(c, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2.4)" }, gr + 0.2 + i * 0.15));''' + OUT)

S['s04'] = (BOX + '''
    #s04-rent { left: 290px; top: 640px; width: 500px; height: 300px; text-align: center; font: 900 220px/300px Inter, sans-serif; color: #ff3b55; opacity: 0; text-shadow: 0 0 50px rgba(255,59,85,.6); }''',
box('s04', 1, 'b', 'WOHNUNGEN HEUTE', '0') + box('s04', 2, 'r', 'GEBRAUCHT', '0') + box('s04', 3, 'r', 'MIETE', '↑ ↑ ↑', False) + SVG + '''
      <div id="s04-rent" class="abs">€</div>''',
'''      const sv = document.querySelector("#s04-svg");
      const blds = [], r = rng(4);
      for (let i = 0; i < 24; i++) { const g = el("g", { opacity: 0 }, sv), x = 70 + (i % 8) * 120, y = 640 + Math.floor(i / 8) * 150;
        el("rect", { x, y, width: 100, height: 130, rx: 6, fill: ["#4f5a9a", "#3a4078", "#5b6bb0"][i % 3] }, g);
        for (let k = 0; k < 6; k++) el("rect", { x: x + 12 + (k % 3) * 28, y: y + 14 + Math.floor(k / 3) * 50, width: 18, height: 30, fill: "#ffd43b", opacity: 0.8 }, g); blds.push(g); }
      const room = el("g", { opacity: 0 }, sv); el("rect", { x: 240, y: 620, width: 600, height: 440, rx: 12, fill: "#262d63", stroke: "#dfe2f5", "stroke-width": 8 }, room);
      const COL = ["#ff4fb0", "#4da3ff", "#39e27a", "#ffd43b", "#ff8a3d"], ppl = [];
      for (let i = 0; i < 10; i++) { const m = mini(room, 300 + (i % 5) * 120, 720 + Math.floor(i / 5) * 160, COL[i % 5]); gsap.set(m, { scale: 1.8, svgOrigin: `${300 + (i % 5) * 120} 740` }); ppl.push(m); }
      const n43 = at("L7", "43"), n4 = at("L7", "Milliarden") - 0.25, l8 = line("L8")[0], ex = at("L8", "explodieren"), ze = at("L8", "zehn");
      tl.to("#s04-box1", { opacity: 1, duration: 0.2 }, n43 - 0.3);
      count(tl, "#s04-n1", 0, 43000000, n43 - 0.2, 1.0, "", "", "power3.out");
      blds.slice(0, 3).forEach((b, i) => tl.fromTo(b, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, n43 + i * 0.1));
      tl.to("#s04-box1", { opacity: 0, duration: 0.15 }, n4 - 0.45);
      tl.to("#s04-box2", { opacity: 1, duration: 0.2 }, n4 - 0.35);
      count(tl, "#s04-n2", 0, 3900000000, n4 - 0.3, 1.2, "", "", "power3.in");
      blds.slice(3).forEach((b, i) => tl.fromTo(b, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }, n4 - 0.2 + i * 0.04));
      tl.to(blds, { opacity: 0, duration: 0.25 }, l8 - 0.3);
      tl.to("#s04-box2", { opacity: 0, duration: 0.15 }, l8 - 0.3);
      tl.to("#s04-box3", { opacity: 1, duration: 0.2 }, ex - 0.3);
      tl.fromTo("#s04-rent", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1.3, duration: 0.4, ease: "back.out(2.4)" }, ex - 0.2);
      tl.to("#s04-rent", { opacity: 0, duration: 0.2 }, ze - 0.6);
      tl.to(room, { opacity: 1, duration: 0.2 }, ze - 0.5);
      ppl.forEach((p, i) => tl.fromTo(p, { opacity: 0 }, { opacity: 1, duration: 0.15 }, ze - 0.4 + i * 0.06));
      tl.to(ppl, { y: -12, duration: 0.15, yoyo: true, repeat: 5, stagger: 0.03 }, ze + 0.4);''' + OUT)

S['s05'] = (BOX, box('s05', 1, 'r', 'SATT WERDEN', '1 VON 100', False) + SVG,
'''      const sv = document.querySelector("#s05-svg");
      const field = el("g", {}, sv);
      for (let k = 0; k < 6; k++) el("rect", { x: 60, y: 590 + k * 22, width: 960, height: 14, rx: 7, fill: k % 2 ? "#e0b84a" : "#c9a43a" }, field);
      const ppl = [];
      for (let i = 0; i < 100; i++) { const x = 104 + (i % 20) * 46, y = 760 + Math.floor(i / 20) * 64; const g = el("g", { opacity: 0 }, sv);
        el("circle", { cx: x, cy: y, r: 9, fill: "#8f9bc4" }, g); el("rect", { x: x - 11, y: y + 10, width: 22, height: 14, rx: 6, fill: "#8f9bc4" }, g); ppl.push(g); }
      const one = ppl[44];
      const ship = el("g", { opacity: 0 }, sv); el("path", { d: "M300 900 H780 L720 990 H360Z", fill: "#ff3b55" }, ship);
      [[380, 840], [460, 840], [540, 840], [620, 840], [420, 790], [500, 790]].forEach(([x, y], i) => el("rect", { x, y, width: 76, height: 48, fill: ["#4da3ff", "#ffd43b", "#39e27a"][i % 3] }, ship));
      const xx = txt(sv, 540, 960, "✕", 260, "#ff3b55", { opacity: 0 });
      const plate = el("g", { opacity: 0 }, sv); el("ellipse", { cx: 540, cy: 860, rx: 230, ry: 70, fill: "#eef2fb" }, plate); el("ellipse", { cx: 540, cy: 852, rx: 165, ry: 46, fill: "#dfe5f5" }, plate);
      const er = at("L9", "ernähren"), ei = at("L9", "einen"), l10 = line("L10")[0], im = at("L10", "Importe"), hu = at("L10", "Hungersnot");
      tl.fromTo(field, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.4 }, 0.05);
      ppl.forEach((p, i) => tl.to(p, { opacity: 1, duration: 0.1 }, er - 0.5 + i * 0.01));
      tl.to("#s05-box1", { opacity: 1, duration: 0.2 }, ei - 0.3);
      tl.to(one.querySelectorAll("circle, rect"), { attr: { fill: "#39e27a" }, duration: 0.2 }, ei);
      tl.to(one, { scale: 1.8, svgOrigin: `${104 + 4 * 46} 912`, duration: 0.3, ease: "back.out(2)" }, ei);
      tl.to(ppl.filter((p) => p !== one), { opacity: 0.35, duration: 0.3 }, ei + 0.2);
      tl.to([field, ...ppl], { opacity: 0, duration: 0.25 }, l10 - 0.3);
      tl.to("#s05-box1", { opacity: 0, duration: 0.2 }, l10 - 0.3);
      tl.fromTo(ship, { opacity: 0, x: -600 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, l10 - 0.2);
      tl.fromTo(xx, { opacity: 0, scale: 2, svgOrigin: "540 880" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, im);
      tl.to([ship, xx], { opacity: 0, duration: 0.2 }, hu - 0.4);
      tl.fromTo(plate, { opacity: 0, scale: 0.5, svgOrigin: "540 860" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, hu - 0.3);
      tl.to(plate, { x: 8, duration: 0.04, repeat: 9, yoyo: true }, hu + 0.2);''' + OUT)

S['s06'] = (BOX, box('s06', 1, 'r', 'WASSER', '– 50 %', False) + box('s06', 2, 'y', 'STROMBEDARF', '× 0') + SVG,
'''      const sv = document.querySelector("#s06-svg");
      const tanks = el("g", {}, sv);
      [[300, "BEDARF"], [780, "VORHANDEN"]].forEach(([x, l]) => { el("rect", { x: x - 150, y: 620, width: 300, height: 420, rx: 20, fill: "none", stroke: "#dfe2f5", "stroke-width": 8 }, tanks); txt(tanks, x, 1092, l, 40, "#dfe2f5"); });
      const w1 = el("rect", { x: 156, y: 1036, width: 288, height: 0, rx: 12, fill: "#4da3ff" }, tanks);
      const w2 = el("rect", { x: 636, y: 1036, width: 288, height: 0, rx: 12, fill: "#4da3ff" }, tanks);
      const miss = el("rect", { x: 636, y: 628, width: 288, height: 204, fill: "#ff3b55", opacity: 0 }, tanks);
      const pw = el("g", { opacity: 0 }, sv), cells = [];
      for (let i = 0; i < 60; i++) cells.push(el("rect", { x: 120 + (i % 10) * 86, y: 640 + Math.floor(i / 10) * 70, width: 70, height: 54, rx: 8, fill: "#2e3670" }, pw));
      const bolt = el("path", { d: "M560 560 L470 760 H540 L500 900 L640 680 H570 L620 560Z", fill: "#ffd43b", opacity: 0 }, sv);
      const de = at("L11", "Deutscher"), ha = at("L11", "Hälfte"), l12 = line("L12")[0], sm = at("L12", "sechzigmal");
      tl.fromTo(tanks, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4 }, 0.05);
      tl.to(w1, { attr: { y: 628, height: 408 }, duration: 1.0, ease: "power2.out" }, de - 0.6);
      tl.to(w2, { attr: { y: 832, height: 204 }, duration: 1.0, ease: "power2.out" }, de - 0.4);
      tl.to("#s06-box1", { opacity: 1, duration: 0.2 }, ha - 0.3);
      tl.to(miss, { opacity: 0.7, duration: 0.15, yoyo: true, repeat: 5 }, ha);
      tl.to(tanks, { opacity: 0, duration: 0.25 }, l12 - 0.3);
      tl.to("#s06-box1", { opacity: 0, duration: 0.15 }, l12 - 0.3);
      tl.to("#s06-box2", { opacity: 1, duration: 0.2 }, l12 - 0.2);
      tl.to(pw, { opacity: 1, duration: 0.2 }, l12 - 0.1);
      tl.to(cells[0], { attr: { fill: "#ffd43b" }, duration: 0.1 }, l12);
      count(tl, "#s06-n2", 1, 60, sm - 0.2, 1.2, "× ", "", "power2.in");
      cells.slice(1).forEach((c, i) => tl.to(c, { attr: { fill: "#ffd43b" }, duration: 0.05 }, sm - 0.2 + i * 0.02));
      tl.fromTo(bolt, { opacity: 0, scale: 0.4, svgOrigin: "545 730" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, sm + 1.0);''' + OUT)

S['s07'] = (BOX, box('s07', 1, 'r', 'STRASSENNETZ', '× 0') + SVG,
'''      const sv = document.querySelector("#s07-svg");
      const road = el("g", {}, sv);
      el("path", { d: "M440 580 H640 L1040 1130 H40Z", fill: "#2a2f55" }, road);
      el("path", { d: "M540 590 V1130", stroke: "#ffd43b", "stroke-width": 8, "stroke-dasharray": "50 40" }, road);
      const COL = ["#ff4fb0", "#4da3ff", "#39e27a", "#ffd43b", "#ff8a3d"], cars = [];
      for (let row = 0; row < 7; row++) { const t = row / 6, y = 640 + t * 430, s = 0.3 + t * 0.6, half = 100 + t * 400, n = 2 + Math.round(t * 3);
        for (let k = 0; k < n; k++) cars.push(car(road, 540 - half + (k + 0.5) * (2 * half / n), y, s, COL[(row + k) % 5])); }
      gsap.set(cars, { opacity: 0 });
      const st = at("L13", "Straßennetz"), ac = at("L13", "achtmal"), sb = at("L13", "Stoßstange");
      tl.fromTo(road, { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.05);
      cars.forEach((c, i) => tl.to(c, { opacity: 1, duration: 0.12 }, st - 0.6 + i * 0.03));
      tl.to("#s07-box1", { opacity: 1, duration: 0.2 }, ac - 0.4);
      count(tl, "#s07-n1", 0, 8, ac - 0.3, 0.8, "× ", " VOLL", "power2.out");
      tl.to(cars, { y: "-=8", duration: 0.1, yoyo: true, repeat: 7, stagger: 0.01 }, sb);
      tl.to(road, { x: 6, duration: 0.05, repeat: 9, yoyo: true }, sb + 0.2);''' + OUT)

S['s08'] = (BOX + '''
    .s08-a { position: absolute; top: 640px; width: 380px; height: 380px; border-radius: 28px; background: rgba(13,16,38,.94); text-align: center; opacity: 0; }
    .s08-a .n { margin-top: 70px; font: 900 170px/1 Inter, sans-serif; } .s08-a .t { margin-top: 26px; font: 700 34px "Space Mono", monospace; letter-spacing: .1em; color: #dfe2f5; }
    #s08-a1 { left: 70px; border: 6px solid #ffd43b; } #s08-a1 .n { color: #ffd43b; } #s08-a2 { left: 630px; border: 6px solid #39e27a; } #s08-a2 .n { color: #39e27a; }''',
box('s08', 1, 'r', 'SPRECHEN DEUTSCH', '1 VON 60', False) + SVG + '''
      <div id="s08-a1" class="s08-a"><div class="n">45</div><div class="t">HEUTE</div></div><div id="s08-a2" class="s08-a"><div class="n">31</div><div class="t">DANN</div></div>''',
'''      const sv = document.querySelector("#s08-svg");
      const ppl = [], W = ["HELLO", "HOLA", "OLÁ", "BONJOUR", "CIAO", "MERHABA"];
      for (let i = 0; i < 60; i++) { const x = 130 + (i % 10) * 91, y = 640 + Math.floor(i / 10) * 70; const g = el("g", { opacity: 0 }, sv);
        el("circle", { cx: x, cy: y, r: 12, fill: "#8f9bc4" }, g); el("rect", { x: x - 15, y: y + 14, width: 30, height: 20, rx: 8, fill: "#8f9bc4" }, g); ppl.push(g); }
      const de = ppl[34];
      const bub = el("g", { opacity: 0 }, sv); el("rect", { x: 380, y: 740, width: 230, height: 70, rx: 20, fill: "#ffd43b" }, bub); txt(bub, 495, 790, "HALLO!", 40, "#161a36");
      const others = W.map((w, i) => { const g = el("g", { opacity: 0 }, sv); const x = 120 + (i % 3) * 330, y = i < 3 ? 1000 : 1080;
        el("rect", { x: x - 10, y: y - 40, width: 230, height: 56, rx: 16, fill: "#2e3670" }, g); txt(g, x + 105, y - 2, w, 32, "#dfe2f5"); return g; });
      const arr = txt(sv, 540, 870, "→", 140, "#ffffff", { opacity: 0 });
      const ei = at("L14", "einer"), mi = at("L14", "Minderheit"), l15 = line("L15")[0], n45 = at("L15", "45"), n31 = at("L15", "31"), re = at("L15", "Rentenproblem");
      ppl.forEach((p, i) => tl.to(p, { opacity: 1, duration: 0.1 }, 0.1 + i * 0.012));
      tl.to("#s08-box1", { opacity: 1, duration: 0.2 }, ei - 0.3);
      tl.to(de.querySelectorAll("circle, rect"), { attr: { fill: "#ffd43b" }, duration: 0.2 }, ei);
      tl.fromTo(bub, { opacity: 0, scale: 0.4, svgOrigin: "495 810" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, ei + 0.2);
      tl.to(ppl.filter((p) => p !== de), { opacity: 0.3, duration: 0.3 }, mi - 0.3);
      others.forEach((o, i) => tl.fromTo(o, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }, mi - 0.2 + i * 0.08));
      tl.to([...ppl, bub, ...others], { opacity: 0, duration: 0.25 }, l15 - 0.3);
      tl.to("#s08-box1", { opacity: 0, duration: 0.2 }, l15 - 0.3);
      tl.fromTo("#s08-a1", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, n45 - 0.2);
      tl.to(arr, { opacity: 1, duration: 0.2 }, n31 - 0.3);
      tl.fromTo("#s08-a2", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, n31 - 0.2);
      tl.to("#s08-a2", { scale: 1.1, duration: 0.15, yoyo: true, repeat: 3 }, re);''' + OUT)

S['s09'] = (BOX + '''
    .s09-c { position: absolute; top: 640px; width: 300px; height: 420px; border-radius: 24px; background: rgba(20,24,56,.92); border: 4px solid #39e27a; overflow: hidden; opacity: 0; }
    .s09-c b { position: absolute; left: 0; right: 0; bottom: 18px; text-align: center; font: 900 38px Inter, sans-serif; color: #fff; }
    #s09-c1 { left: 60px; } #s09-c2 { left: 390px; } #s09-c3 { left: 720px; }''',
box('s09', 1, 'y', 'ANTEIL LANDFLÄCHE', '0,24 %', False) + '''      <div id="s09-c1" class="s09-c"><b>PARIS</b></div><div id="s09-c2" class="s09-c"><b>NEW YORK</b></div><div id="s09-c3" class="s09-c"><b>TOKIO</b></div>
''' + SVG,
'''      const sv = document.querySelector("#s09-svg");
      const globe = el("g", {}, sv);
      el("circle", { cx: 540, cy: 830, r: 250, fill: "#2f7fe0" }, globe);
      [["M380 700 q60 -60 140 -20 q40 60 -20 110 q-80 30 -120 -20Z"], ["M560 640 q80 -20 140 40 q30 80 -40 100 q-60 -10 -100 -60Z"], ["M420 900 q60 -30 100 20 q10 90 -60 110 q-60 -40 -40 -130Z"], ["M600 880 q90 -10 130 60 q-20 70 -100 60 q-50 -50 -30 -120Z"]].forEach(([d]) => el("path", { d, fill: "#39e27a" }, globe));
      const dot = el("circle", { cx: 548, cy: 690, r: 9, fill: "#ff3b55" }, sv);
      const ring = el("circle", { cx: 548, cy: 690, r: 30, fill: "none", stroke: "#ff3b55", "stroke-width": 6 }, sv);
      const cards = [];
      [210, 540, 870].forEach((cx, i) => { const g = el("g", { opacity: 0 }, sv);
        for (let k = 0; k < 4; k++) { const h = 140 + ((k * 53 + i * 31) % 160); el("rect", { x: cx - 120 + k * 62, y: 1000 - h, width: 52, height: h, fill: "#4f5a9a" }, g); }
        const vine = el("path", { d: `M${cx - 130} 1000 q40 -120 0 -220 q-30 -60 40 -100 M${cx + 120} 1000 q-50 -90 0 -180 q40 -50 -10 -110`, stroke: "#39e27a", "stroke-width": 14, fill: "none", "stroke-linecap": "round", "stroke-dasharray": 700, "stroke-dashoffset": 700 }, g);
        const deer = el("path", { d: `M${cx - 30} 990 v-40 h60 v40 M${cx - 34} 950 h68 v-30 h-68Z M${cx + 34} 920 l20 -30 M${cx + 50} 900 l14 -16 M${cx + 50} 900 l20 4`, stroke: "#ffd43b", "stroke-width": 10, fill: "none", "stroke-linecap": "round", opacity: 0 }, g);
        cards.push({ g, vine, deer }); });
      const vi = at("L16", "Viertel"), ga = at("L17", "ganze"), me = at("L17", "menschenleer"), wa = at("L17", "Wälder"), wt = at("L17", "Wildtiere");
      tl.fromTo(globe, { opacity: 0, scale: 0.6, svgOrigin: "540 830" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, 0.05);
      tl.fromTo(ring, { attr: { r: 20 }, opacity: 1 }, { attr: { r: 90 }, opacity: 0, duration: 0.8, repeat: 5 }, 0.3);
      tl.to("#s09-box1", { opacity: 1, duration: 0.2 }, vi - 0.3);
      tl.to(dot, { attr: { r: 16 }, duration: 0.15, yoyo: true, repeat: 3 }, vi);
      tl.to(globe.querySelectorAll("path"), { attr: { fill: "#1fbf5a" }, duration: 0.6 }, ga);
      tl.to([globe, dot, ring], { opacity: 0, duration: 0.25 }, me + 0.4);
      tl.to("#s09-box1", { opacity: 0, duration: 0.2 }, me + 0.4);
      ["#s09-c1", "#s09-c2", "#s09-c3"].forEach((c, i) => { tl.fromTo(c, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, me + 0.5 + i * 0.1); tl.to(cards[i].g, { opacity: 1, duration: 0.3 }, me + 0.5 + i * 0.1); });
      cards.forEach((c, i) => { tl.to(c.g.querySelectorAll("rect"), { rotation: (i % 2 ? 6 : -6), svgOrigin: `${[210, 540, 870][i]} 1000`, duration: 1.2 }, wa - 0.8);
        tl.to(c.vine, { attr: { "stroke-dashoffset": 0 }, duration: 1.2, ease: "power2.out" }, wa - 0.2 + i * 0.1);
        tl.fromTo(c.deer, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(2)" }, wt + i * 0.25); });''' + OUT)

S['s10'] = ('''    .s10-b { position: absolute; top: 950px; width: 450px; height: 150px; border-radius: 26px; text-align: center; font: 900 50px/150px Inter, sans-serif; color: #0b0e22; }
    #s10-b1 { left: 50px; background: #ff4fb0; box-shadow: 0 0 40px rgba(255,79,176,.5); } #s10-b2 { left: 580px; background: #39e27a; box-shadow: 0 0 40px rgba(57,226,122,.5); }
    #s10-f { left: 290px; top: 950px; width: 500px; height: 150px; border-radius: 75px; background: #ff3b55; box-shadow: 0 0 50px rgba(255,59,85,.6); opacity: 0;
      text-align: center; font: 900 64px/150px Inter, sans-serif; color: #fff; }''',
SVG + '''
      <div id="s10-b1" class="s10-b">BERLIN</div><div id="s10-b2" class="s10-b">AUFS LAND</div>
      <div id="s10-f" class="abs">+ FOLGEN</div>''',
'''      const sv = document.querySelector("#s10-svg");
      const map = germany(sv, 540, 760, 380);
      const pr = deProj(540, 760, 380), [bx, by] = pr(...CITY.Berlin);
      const bd = el("circle", { cx: bx, cy: by, r: 16, fill: "#ff4fb0" }, sv);
      const house = el("g", { opacity: 0 }, sv); el("rect", { x: 420, y: 700, width: 240, height: 200, fill: "#4f5a9a" }, house);
      el("path", { d: "M400 710 L540 590 L680 710Z", fill: "#ff3b55" }, house); const door = el("rect", { x: 510, y: 800, width: 60, height: 100, fill: "#ffd43b" }, house);
      const mover = el("g", { opacity: 0 }, sv); const mv = mini(mover, 820, 840, "#4da3ff"); gsap.set(mv, { opacity: 1, scale: 2.4, svgOrigin: "820 860" });
      el("rect", { x: 760, y: 870, width: 70, height: 56, fill: "#c9a46a", stroke: "#8a5a2b", "stroke-width": 4 }, mover);
      const du = at("L18", "du?"), be = at("L18", "Berlin"), la = at("L18", "Land?"), ko = at("L18", "Kommentare"), l19 = line("L19")[0], fo = at("L19", "folg"), ab = at("L19", "Abend"), ein = at("L19", "ein.");
      tl.fromTo(map, { opacity: 0, scale: 0.7, svgOrigin: "540 760" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.fromTo(bd, { attr: { r: 10 } }, { attr: { r: 30 }, duration: 0.3, yoyo: true, repeat: 5 }, be - 0.1);
      tl.fromTo("#s10-b1", { opacity: 0, y: 80, rotation: -6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, be - 0.15);
      tl.fromTo("#s10-b2", { opacity: 0, y: 80, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, la - 0.15);
      tl.to(".s10-b", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 3, stagger: 0.3, ease: "sine.inOut" }, ko - 0.3);
      tl.to(".s10-b", { opacity: 0, y: 60, duration: 0.25, ease: "power3.in" }, l19 - 0.2);
      tl.fromTo("#s10-f", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, fo - 0.1);
      tl.to("#s10-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);
      tl.to([map, bd], { opacity: 0, duration: 0.25 }, ab - 0.6);
      tl.to(house, { opacity: 1, duration: 0.3 }, ab - 0.5);
      tl.fromTo(mover, { opacity: 0, x: 300 }, { opacity: 1, x: 0, duration: 0.6, ease: "power2.out" }, ab - 0.3);
      tl.to(mover, { x: -260, duration: 1.0, ease: "power1.inOut" }, ein + 0.2);
      tl.to(door, { attr: { fill: "#161a36" }, duration: 0.2 }, ein);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
