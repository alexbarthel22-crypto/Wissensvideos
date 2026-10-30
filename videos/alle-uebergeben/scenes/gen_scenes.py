#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Alle übergeben sich“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
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
    #@@ID@@-news .bar { height: 44px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 30px; font-size: 36px; letter-spacing: .08em; }
    #@@ID@@-news .hl { padding: 4px 36px 0; text-align: center; font-size: 60px; line-height: 1.0; letter-spacing: -.015em; }
    #@@ID@@-news .hl em { font-style: normal; color: #9be27a; text-shadow: 0 0 26px rgba(155,226,122,.7); }'''

S['s01'] = (NEWS + '''
    #s01-count .num { font-size: 50px; }
    #s01-q { left: 240px; top: 600px; width: 600px; height: 420px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 150px; line-height: 1.05; padding-top: 40px; box-sizing: border-box; opacity: 0; box-shadow: 0 0 50px rgba(255,59,85,.45); }
    #s01-q small { display: block; font-size: 52px; color: #fff; letter-spacing: .04em; }''',
'''      <div id="s01-count" class="cbox p" style="opacity:0"><div class="lab">MÄGEN</div><div class="num">8.200.000.000</div></div>
''' + SVG + '''
      <div id="s01-news" class="panel"><div class="bar">● EILMELDUNG · LIVE</div><div class="hl">ALLE MÜSSEN SICH<br><em>ÜBERGEBEN!</em></div></div>
      <div id="s01-q" class="panel">?!<small>LEBENSGEFAHR</small></div>''',
'''      const sv = document.querySelector("#s01-svg");
      const glow = el("circle", { cx: 540, cy: 700, r: 260, fill: "#9be27a", opacity: 0.18 }, sv);
      const pud = el("ellipse", { cx: 540, cy: 962, rx: 190, ry: 26, fill: "#a8b83a" }, sv);
      const F = sick(sv, 540, 680, 1.3);
      gsap.set(F.puke, { opacity: 1 }); gsap.set(F.mouth, { attr: { rx: 46, ry: 34 } });
      const sp = []; for (let i = 0; i < 8; i++) sp.push(el("circle", { cx: 380 + i * 46, cy: 950, r: 10 + (i % 3) * 4, fill: "#c9d94a" }, sv));
      const warn = (x) => { const g = el("g", {}, sv);
        const t = el("path", { d: `M${x} 560 L${x + 70} 665 H${x - 70}Z`, fill: "#ffd43b", stroke: "#ff3b55", "stroke-width": 12, "stroke-linejoin": "round" }, g);
        const e = txt(g, x, 655, "!", 70, "#161a36"); return { g, t, e }; };
      const W = [warn(110), warn(970)];
      const mg = el("g", {}, sv), minis = [];
      for (let i = 0; i < 35; i++) { const m = sick(mg, 150 + (i % 7) * 130, 640 + Math.floor(i / 7) * 100, 0.3); gsap.set(m.g, { opacity: 0 }); minis.push(m); }
      const ub = at("L1", "übergeben"), n82 = at("L2", "8,2"), sek = at("L2", "Sekunde"), ri = at("L2", "richtig");
      tl.to(F.g, { x: 548, duration: 0.05, repeat: 21, yoyo: true }, 0.2);
      tl.fromTo(glow, { attr: { opacity: 0.18 } }, { attr: { opacity: 0.45 }, duration: 0.35, repeat: 7, yoyo: true }, 0);
      W.forEach((w) => { tl.to(w.t, { attr: { fill: "#ff3b55", stroke: "#ffd43b" }, duration: 0.01, repeat: 13, yoyo: true, repeatDelay: 0.22 }, 0.2);
        tl.to(w.e, { attr: { fill: "#ffffff" }, duration: 0.01, repeat: 13, yoyo: true, repeatDelay: 0.22 }, 0.2); });
      tl.to("#s01-news", { opacity: 0, scale: 0.85, duration: 0.25, ease: "power3.in" }, 2.6);
      tl.to(F.head, { attr: { fill: "#9fd35a" }, duration: 0.4 }, ub - 0.5);
      tl.fromTo(F.puke, { scaleY: 0.92, scaleX: 0.95, transformOrigin: "50% 0%" }, { scaleY: 1.06, scaleX: 1.08, duration: 0.18, yoyo: true, repeat: 15, ease: "sine.inOut" }, 0);
      sp.forEach((d, i) => tl.fromTo(d, { y: 0, x: 0, opacity: 1 }, { y: -60 - (i % 3) * 30, x: (i - 3.5) * 22, opacity: 0, duration: 0.45, ease: "power2.out", repeat: 5, repeatDelay: 0.05 }, 0.05 + i * 0.04));
      tl.fromTo(pud, { attr: { rx: 120 } }, { attr: { rx: 230 }, duration: 2.5, ease: "power1.out" }, 0);
      tl.to(F.puke, { scaleX: 1.35, scaleY: 1.12, transformOrigin: "50% 0%", duration: 0.2, yoyo: true, repeat: 3 }, ub);
      tl.to(F.g, { y: 668, duration: 0.12, yoyo: true, repeat: 3 }, ub);
      tl.to([F.g, glow, pud, ...sp, ...W.map((w) => w.g)], { opacity: 0, duration: 0.3 }, n82 - 0.35);
      tl.to("#s01-count", { opacity: 1, duration: 0.2 }, n82 - 0.25);
      tl.fromTo("#s01-count", { scale: 1 }, { scale: 1.12, duration: 0.15, yoyo: true, repeat: 1 }, n82);
      minis.forEach((m, i) => tl.fromTo(m.g, { opacity: 0, scale: 0.1 }, { opacity: 1, scale: 0.3, duration: 0.25, ease: "back.out(2)" }, n82 + i * 0.025));
      tl.to(minis.map((m) => m.cheeks).flat(), { scale: 1.4, transformOrigin: "50% 50%", duration: 0.1, yoyo: true, repeat: 3 }, sek);
      tl.to(mg, { y: 10, duration: 0.05, yoyo: true, repeat: 7 }, sek);
      tl.to(minis.map((m) => m.g), { opacity: 0, filter: "blur(8px)", duration: 0.25 }, ri - 0.85);
      tl.fromTo("#s01-q", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, ri - 0.6);
      tl.to("#s01-q", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, ri + 0.2);''' + OUT)

S['s02'] = ('''    .s02b .num { font-size: 44px; }''',
'''      <div id="s02-box" class="cbox g s02b" style="opacity:0"><div class="lab">PRO PERSON</div><div class="num">0,5 LITER</div></div>
      <div id="s02-box2" class="cbox g s02b" style="opacity:0"><div class="lab">ZUSAMMEN</div><div id="s02-n2" class="num">0 L</div></div>
      <div id="s02-box3" class="cbox y s02b" style="opacity:0"><div class="lab">DOSEN À 0,33 L</div><div id="s02-n3" class="num">0</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s02-svg");
      const cup = el("g", {}, sv);
      el("path", { d: "M400 640 H680 L650 980 H430Z", fill: "#dfe5f5", opacity: 0.35 }, cup);
      const liq = el("path", { d: "M418 800 H662 L650 970 H430Z", fill: "#c9d94a" }, cup);
      txt(cup, 540, 900, "½ L", 90, "#161a36");
      const fcl = el("clipPath", { id: "s02-clip" }, sv); el("rect", { x: 0, y: 0, width: 1080, height: 1130 }, fcl);
      const fg = el("g", { "clip-path": "url(#s02-clip)" }, sv);
      const Fl = flood(fg, 1180, "#a8b83a"); const F2 = flood(fg, 1210, "#c9d94a");
      const pools = [];
      for (let i = 0; i < 12; i++) { const x = 115 + (i % 6) * 170, y = 600 + Math.floor(i / 6) * 250, g = el("g", { opacity: 0 }, sv);
        el("rect", { x: x - 55, y, width: 110, height: 200, rx: 18, fill: "#1d1d24" }, g);
        el("ellipse", { cx: x, cy: y + 4, rx: 50, ry: 12, fill: "#c9cde6" }, g);
        el("rect", { x: x - 55, y: y + 70, width: 110, height: 64, fill: "#f3e3c3" }, g);
        txt(g, x, y + 114, "ZERO", 28, "#1d1d24");
        el("rect", { x: x - 55, y: y + 186, width: 110, height: 14, rx: 7, fill: "#8f9bc4" }, g);
        pools.push(g); }
      const ha = at("L3", "halber"), v4 = at("L3", "4"), l4 = line("L4")[0], n16 = at("L4", "12");
      tl.fromTo(cup, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.to("#s02-box", { opacity: 1, duration: 0.25 }, ha - 0.3);
      tl.fromTo(liq, { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.6, ease: "power2.out" }, ha - 0.2);
      tl.to(cup, { opacity: 0, y: 120, scale: 0.5, svgOrigin: "540 900", duration: 0.35, ease: "power3.in" }, v4 - 0.5);
      tl.to("#s02-box", { opacity: 0, duration: 0.15 }, v4 - 0.45);
      tl.to("#s02-box2", { opacity: 1, duration: 0.2 }, v4 - 0.35);
      count(tl, "#s02-n2", 0, 4000000000, v4 - 0.3, 1.3, "", " L", "power3.in");
      tl.fromTo(Fl, { y: 0 }, { y: -600, duration: 1.6, ease: "power2.inOut" }, v4 - 0.3);
      tl.fromTo(F2, { y: 0 }, { y: -580, duration: 1.7, ease: "power2.inOut" }, v4 - 0.2);
      tl.to([Fl, F2], { x: -135, duration: 0.6, repeat: 3, yoyo: true, ease: "sine.inOut" }, v4);
      tl.to([Fl, F2], { y: 200, opacity: 0, duration: 0.4, ease: "power3.in" }, l4 - 0.1);
      tl.to("#s02-box2", { opacity: 0, duration: 0.15 }, n16 - 0.45);
      tl.to("#s02-box3", { opacity: 1, duration: 0.2 }, n16 - 0.35);
      count(tl, "#s02-n3", 0, 12000000000, n16 - 0.3, 1.3, "", "", "power3.out");
      pools.forEach((p, i) => tl.fromTo(p, { opacity: 0, y: -300 }, { opacity: 1, y: 0, duration: 0.35, ease: "bounce.out" }, n16 - 0.2 + i * 0.07));
      tl.to(pools, { rotation: 6, svgOrigin: "540 1050", duration: 0.12, yoyo: true, repeat: 5 }, at("L4", "Zero"));''' + OUT)

S['s03'] = ('''    #s03-box .num { font-size: 52px; }''',
'''      <div id="s03-box" class="cbox r" style="opacity:0"><div class="lab">AM STEUER</div><div class="num">MILLIONEN</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s03-svg");
      const road = el("g", {}, sv);
      el("path", { d: "M440 580 H640 L1040 1130 H40Z", fill: "#2a2f55" }, road);
      const dash = el("path", { d: "M540 590 V1130", stroke: "#ffd43b", "stroke-width": 10, "stroke-dasharray": "50 40" }, road);
      const COL = ["#ff4fb0", "#4da3ff", "#39e27a", "#ffd43b", "#ff8a3d"];
      const cars = [[400, 700, 0.55], [680, 760, 0.65], [300, 880, 0.85], [760, 940, 0.95], [520, 1050, 1.1]].map(([x, y, s], i) => car(road, x, y, s, COL[i]));
      const eyes = el("g", { opacity: 0 }, sv);
      [380, 700].forEach((x) => { el("ellipse", { cx: x, cy: 780, rx: 120, ry: 80, fill: "#ffffff" }, eyes); el("circle", { cx: x, cy: 780, r: 44, fill: "#161a36" }, eyes); });
      const lids = [380, 700].map((x) => el("rect", { x: x - 125, y: 690, width: 250, height: 0, fill: "#b9e07a" }, eyes));
      const booms = [[330, 860], [720, 920], [520, 1010]].map(([x, y]) => { const b = el("path", { d: (() => { const p = []; for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2, r = i % 2 ? 50 : 110; p.push(`${x + r * Math.cos(a)},${y + r * Math.sin(a)}`); } return "M" + p.join(" L") + "Z"; })(), fill: "#ffd43b", opacity: 0 }, sv); return b; });
      const mi = at("L5", "Millionen"), au = at("L6", "Augen"), zu = at("L6", "zu"), mk = at("L6", "Massenunfälle");
      tl.fromTo(road, { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.05);
      tl.fromTo(dash, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": 900 }, duration: 5, ease: "none" }, 0.05);
      cars.forEach((c, i) => tl.to(c, { y: `+=${10 + i * 4}`, duration: 0.3, yoyo: true, repeat: 7, ease: "sine.inOut" }, 0.1 + i * 0.1));
      tl.to("#s03-box", { opacity: 1, duration: 0.25 }, mi - 0.3);
      tl.to(road, { opacity: 0.25, duration: 0.2 }, au - 0.3);
      tl.fromTo(eyes, { opacity: 0, scale: 0.6, svgOrigin: "540 780" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, au - 0.25);
      tl.to(lids, { attr: { height: 180 }, duration: 0.3, ease: "power2.in" }, zu - 0.1);
      tl.to(eyes, { opacity: 0, duration: 0.2 }, mk - 0.5);
      tl.to(road, { opacity: 1, duration: 0.2 }, mk - 0.5);
      cars.forEach((c, i) => tl.to(c, { rotation: [25, -30, 40, -20, 15][i], x: `+=${[60, -80, 90, -70, 30][i]}`, duration: 0.3, ease: "power3.in" }, mk - 0.3 + i * 0.05));
      booms.forEach((b, i) => tl.fromTo(b, { opacity: 0, scale: 0.2, svgOrigin: "540 950" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, mk + i * 0.12));
      tl.to(road, { x: 10, duration: 0.04, repeat: 9, yoyo: true }, mk);''' + OUT)

S['s04'] = ('''    .s04b .num { font-size: 50px; }
    #s04-ap { left: 330px; top: 900px; width: 420px; height: 90px; border-radius: 45px; background: #39e27a; color: #0b0e22; text-align: center; font: 900 46px/90px Inter, sans-serif; opacity: 0; }''',
'''      <div id="s04-box" class="cbox b s04b" style="opacity:0"><div class="lab">FLUGZEUGE IN DER LUFT</div><div id="s04-n" class="num">0</div></div>
      <div id="s04-box2" class="cbox y s04b" style="opacity:0"><div class="lab">MENSCHEN AN BORD</div><div id="s04-n2" class="num">0</div></div>
''' + SVG + '''
      <div id="s04-ap" class="abs">AUTOPILOT ✓</div>''',
'''      const sv = document.querySelector("#s04-svg");
      const sky = el("g", {}, sv);
      const r = rng(8); for (let i = 0; i < 6; i++) el("ellipse", { cx: 100 + r() * 880, cy: 620 + r() * 420, rx: 90, ry: 30, fill: "#2e3670", opacity: 0.8 }, sky);
      const P = plane(sky, 560, 760, 1.25);
      const rw = el("g", { opacity: 0 }, sv); el("path", { d: "M380 1130 L500 990 H580 L700 1130Z", fill: "#3b4b6e" }, rw); el("path", { d: "M540 1000 V1130", stroke: "#fff", "stroke-width": 6, "stroke-dasharray": "20 16" }, rw);
      const bag = el("g", { opacity: 0 }, sv); el("rect", { x: 140, y: 880, width: 120, height: 150, rx: 10, fill: "#f3f1ea" }, bag); txt(bag, 200, 970, "🤢", 1, "#fff");
      el("path", { d: "M140 900 l20 -20 l20 20 l20 -20 l20 20 l20 -20 l20 20", stroke: "#f3f1ea", "stroke-width": 8, fill: "none" }, bag);
      const iss = el("g", { opacity: 0 }, sv);
      el("rect", { x: 140, y: 740, width: 260, height: 90, fill: "#4da3ff" }, iss); el("rect", { x: 680, y: 740, width: 260, height: 90, fill: "#4da3ff" }, iss);
      for (let k = 1; k < 4; k++) { el("path", { d: `M${140 + k * 65} 740 V830`, stroke: "#1b2150", "stroke-width": 4 }, iss); el("path", { d: `M${680 + k * 65} 740 V830`, stroke: "#1b2150", "stroke-width": 4 }, iss); }
      el("rect", { x: 400, y: 772, width: 280, height: 26, fill: "#8f9bc4" }, iss);
      el("rect", { x: 450, y: 700, width: 180, height: 170, rx: 30, fill: "#dfe5f5" }, iss);
      el("circle", { cx: 540, cy: 785, r: 40, fill: "#1b2150" }, iss);
      const blobs = []; for (let i = 0; i < 9; i++) blobs.push(blob(sv, 200 + (i % 3) * 330 + r() * 60, 640 + Math.floor(i / 3) * 170 + r() * 40, 22 + r() * 12));
      gsap.set(blobs, { opacity: 0 });
      const zt = at("L7", "10.000"), mil = at("L7", "Million"), ap = at("L8", "Autopilot"), la = at("L8", "landet"), ra = at("L8b", "Raumstation"), qu = at("L8b", "quer");
      tl.fromTo(P, { x: -300 }, { x: 560, duration: 0.8, ease: "power3.out" }, 0.05);
      tl.to(P, { y: 745, duration: 0.6, yoyo: true, repeat: 5, ease: "sine.inOut" }, 0.9);
      tl.to("#s04-box", { opacity: 1, duration: 0.25 }, zt - 0.3);
      count(tl, "#s04-n", 0, 10000, zt - 0.2, 0.9, "", "", "power3.out");
      tl.to("#s04-box", { opacity: 0, duration: 0.15 }, mil - 0.45);
      tl.to("#s04-box2", { opacity: 1, duration: 0.2 }, mil - 0.35);
      count(tl, "#s04-n2", 0, 1000000, mil - 0.3, 0.9, "", "", "power3.out");
      tl.fromTo(bag, { opacity: 0, scale: 0.5, svgOrigin: "200 950" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, mil);
      tl.fromTo("#s04-ap", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ap - 0.1);
      tl.to("#s04-ap", { opacity: 0, duration: 0.2 }, la - 0.4);
      tl.to(bag, { opacity: 0, duration: 0.2 }, la - 0.4);
      tl.to(rw, { opacity: 1, duration: 0.3 }, la - 0.3);
      tl.to(P, { rotation: 14, svgOrigin: "560 760", y: 860, duration: 0.6, ease: "power2.in" }, la - 0.2);
      tl.to(P, { rotation: 8, svgOrigin: "560 760", duration: 0.08, yoyo: true, repeat: 9 }, la + 0.4);
      tl.to([sky, rw], { opacity: 0, duration: 0.25 }, ra - 0.4);
      tl.to("#s04-box2", { opacity: 0, duration: 0.2 }, ra - 0.4);
      tl.fromTo(iss, { opacity: 0, scale: 0.7, svgOrigin: "540 785" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, ra - 0.2);
      tl.to(iss, { rotation: 6, svgOrigin: "540 785", duration: 3, ease: "sine.inOut" }, ra);
      blobs.forEach((b, i) => { tl.to(b, { opacity: 1, duration: 0.2 }, qu - 0.2 + i * 0.06); tl.to(b, { x: (i % 2 ? 1 : -1) * (40 + i * 8), y: (i % 3 - 1) * 50, rotation: 120, svgOrigin: `${200 + (i % 3) * 330} ${640 + Math.floor(i / 3) * 170}`, duration: 2, ease: "sine.inOut" }, qu - 0.2 + i * 0.06); });''' + OUT)

S['s05'] = ('''    #s05-box .num { font-size: 52px; }''',
'''      <div id="s05-box" class="cbox y" style="opacity:0"><div class="lab">OPERATIONEN · JETZT</div><div id="s05-n" class="num">0</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s05-svg");
      const room = el("g", {}, sv);
      const lamp = el("g", {}, room); el("path", { d: "M540 560 V610", stroke: "#8f9bc4", "stroke-width": 10 }, lamp);
      el("path", { d: "M420 660 Q540 580 660 660Z", fill: "#dfe5f5" }, lamp); const beam = el("path", { d: "M440 660 L300 960 H780 L640 660Z", fill: "#fff7c0", opacity: 0.18 }, lamp);
      el("rect", { x: 200, y: 940, width: 680, height: 40, rx: 12, fill: "#8f9bc4" }, room); el("rect", { x: 520, y: 980, width: 40, height: 120, fill: "#6b7399" }, room);
      el("rect", { x: 300, y: 890, width: 460, height: 60, rx: 30, fill: "#4da3ff" }, room); el("circle", { cx: 260, cy: 905, r: 46, fill: "#f2c9a5" }, room);
      const mon = el("g", {}, room); el("rect", { x: 820, y: 700, width: 200, height: 150, rx: 14, fill: "#141838", stroke: "#8f9bc4", "stroke-width": 6 }, mon);
      const ecg = el("path", { d: "M835 780 h40 l12 -30 l14 60 l12 -30 h40 l12 -30 l14 60 l12 -30 h15", stroke: "#39e27a", "stroke-width": 6, fill: "none" }, mon);
      const S1 = sick(room, 640, 760, 0.62, "#f2c9a5");
      el("rect", { x: -62, y: 34, width: 124, height: 50, rx: 14, fill: "#39b3a0" }, S1.g); // Mundschutz
      gsap.set(S1.g, { opacity: 1 });
      const alarm = el("rect", { x: 0, y: 560, width: 1080, height: 570, fill: "#ff3b55", opacity: 0 }, sv);
      const n7 = at("L9", "70.000"), ch = at("L10", "Chirurgen"), wu = at("L10", "Wunden"), na = at("L10", "Narkose"), er = at("L10", "ersticken");
      tl.fromTo(room, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.fromTo(beam, { attr: { opacity: 0.12 } }, { attr: { opacity: 0.3 }, duration: 0.5, repeat: 5, yoyo: true }, 0.3);
      tl.to("#s05-box", { opacity: 1, duration: 0.25 }, n7 - 0.3);
      count(tl, "#s05-n", 0, 70000, n7 - 0.2, 1.0, "", "", "power3.out");
      tl.to(S1.head, { attr: { fill: "#b9e07a" }, duration: 0.4 }, ch - 0.2);
      tl.to(S1.cheeks, { scale: 1.4, transformOrigin: "50% 50%", duration: 0.15, yoyo: true, repeat: 5 }, ch);
      tl.to(S1.g, { x: 648, duration: 0.05, repeat: 11, yoyo: true }, ch + 0.1);
      tl.fromTo(alarm, { attr: { opacity: 0 } }, { attr: { opacity: 0.18 }, duration: 0.15, repeat: 5, yoyo: true }, wu);
      tl.to(ecg, { attr: { stroke: "#ffd43b" }, duration: 0.2 }, na);
      tl.to(ecg, { attr: { stroke: "#ff3b55", d: "M835 780 h40 l6 -50 l8 90 l8 -60 l8 50 l8 -70 l8 60 l8 -40 h70" }, duration: 0.2 }, er - 0.1);
      tl.to(mon, { x: 8, duration: 0.04, repeat: 9, yoyo: true }, er);
      tl.to("#s05-box", { borderColor: "#ff3b55", duration: 0.2 }, er);''' + OUT)

S['s06'] = ('''    #s06-box .num { font-size: 44px; }''',
'''      <div id="s06-box" class="cbox b" style="opacity:0"><div class="lab">SCHLAFEN GERADE</div><div id="s06-n" class="num">0</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s06-svg");
      const moon = el("circle", { cx: 880, cy: 640, r: 60, fill: "#f4d27a" }, sv); el("circle", { cx: 905, cy: 625, r: 52, fill: "#121634" }, sv);
      const bed = el("g", {}, sv);
      el("rect", { x: 140, y: 900, width: 800, height: 90, rx: 20, fill: "#6b5aa8" }, bed); el("rect", { x: 140, y: 820, width: 40, height: 260, rx: 10, fill: "#4a3f7a" }, bed);
      el("rect", { x: 900, y: 860, width: 40, height: 220, rx: 10, fill: "#4a3f7a" }, bed); el("rect", { x: 190, y: 860, width: 170, height: 50, rx: 25, fill: "#eef2fb" }, bed);
      const sl = el("g", {}, bed);
      el("rect", { x: 330, y: 850, width: 520, height: 70, rx: 35, fill: "#4da3ff" }, sl);
      const hd = el("circle", { cx: 300, cy: 840, r: 52, fill: "#b9e07a" }, sl);
      el("path", { d: "M280 830 h-16 M330 830 h-16", stroke: "#161a36", "stroke-width": 6, "stroke-linecap": "round" }, sl);
      const zz = txt(sv, 380, 760, "Z z z", 64, "#a9d2ff");
      const danger = el("circle", { cx: 300, cy: 840, r: 90, fill: "none", stroke: "#ff3b55", "stroke-width": 12, opacity: 0 }, sv);
      const ok = el("g", { opacity: 0 }, sv); el("circle", { cx: 780, cy: 700, r: 70, fill: "#39e27a" }, ok);
      el("path", { d: "M745 702 L772 730 L820 678", stroke: "#0b0e22", "stroke-width": 18, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, ok);
      const dr = at("L11", "Drittel"), ru = at("L12", "Rücken"), ei = at("L12", "einatmen"), st = at("L12b", "Stabile");
      tl.fromTo(bed, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.fromTo(zz, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, repeat: 5, yoyo: true }, 0.3);
      tl.to("#s06-box", { opacity: 1, duration: 0.25 }, dr - 0.3);
      count(tl, "#s06-n", 0, 2700000000, dr - 0.2, 1.2, "", "", "power3.out");
      tl.to(danger, { opacity: 1, duration: 0.15, yoyo: true, repeat: 5 }, ru);
      tl.to(hd, { attr: { fill: "#9fd35a" }, duration: 0.3 }, ru);
      tl.to(sv, { x: 8, duration: 0.04, repeat: 9, yoyo: true }, ei);
      tl.to("#s06-box", { borderColor: "#ff3b55", duration: 0.2 }, ei);
      tl.to(danger, { opacity: 0, duration: 0.2 }, st - 0.4);
      tl.to(sl, { rotation: -8, svgOrigin: "590 885", y: -10, duration: 0.4, ease: "back.out(2)" }, st - 0.3);
      tl.fromTo(ok, { opacity: 0, scale: 0.3, svgOrigin: "780 700" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }, st);
      tl.to("#s06-box", { borderColor: "#39e27a", duration: 0.2 }, st);''' + OUT)

S['s07'] = ('''    #s07-box .num { font-size: 42px; }''',
'''      <div id="s07-box" class="cbox r" style="opacity:0"><div class="lab">ZWEITE WELLE</div><div class="num">KETTENREAKTION</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s07-svg");
      const fs = [0, 1, 2, 3, 4].map((i) => sick(sv, 140 + i * 200, 820 + (i % 2) * 40, 0.62, "#f2c9a5"));
      const waves = [0, 1, 2, 3].map((i) => el("path", { d: `M${200 + i * 200} 770 q20 -20 40 0 t40 0`, stroke: "#9be27a", "stroke-width": 10, fill: "none", "stroke-linecap": "round", opacity: 0 }, sv));
      const zw = at("L13", "zweite"), si = at("L13", "sieht"), se = at("L13", "selbst"), re = at("L13", "Reflex");
      fs.forEach((f, i) => tl.fromTo(f.g, { opacity: 0, y: "+=40" }, { opacity: 1, y: "-=40", duration: 0.3, ease: "back.out(2)" }, 0.05 + i * 0.06));
      tl.to(fs[0].head, { attr: { fill: "#9fd35a" }, duration: 0.2 }, zw - 0.2);
      tl.to("#s07-box", { opacity: 1, duration: 0.25 }, zw);
      fs.slice(1).forEach((f, i) => { const t = si + i * ((se - si) / 4);
        tl.to(waves[i], { opacity: 1, duration: 0.1 }, t - 0.15); tl.to(waves[i], { x: 30, duration: 0.3 }, t - 0.15); tl.to(waves[i], { opacity: 0, duration: 0.1 }, t + 0.2);
        tl.to(f.head, { attr: { fill: "#9fd35a" }, duration: 0.2 }, t);
        tl.to(f.cheeks, { scale: 1.4, transformOrigin: "50% 50%", duration: 0.12, yoyo: true, repeat: 3 }, t); });
      tl.to(fs.map((f) => f.g), { y: "-=20", duration: 0.12, yoyo: true, repeat: 3, stagger: 0.05 }, re);''' + OUT)

S['s08'] = ('''    #s08-box .num, #s08-box2 .num { font-size: 50px; }
    #s08-st { left: 260px; top: 760px; width: 560px; height: 140px; border: 10px solid #ff3b55; border-radius: 18px; color: #ff3b55; font: 900 70px/120px Inter, sans-serif; text-align: center; opacity: 0; background: rgba(13,16,38,.7); }''',
'''      <div id="s08-box" class="cbox r" style="opacity:0"><div class="lab">MAHLZEIT DER WELT</div><div class="num">MILLIARDEN €</div></div>
      <div id="s08-box2" class="cbox g" style="opacity:0"><div class="lab">REINIGUNGSFIRMEN</div><div class="num">+ REKORD</div></div>
''' + SVG + '''
      <div id="s08-st" class="abs">AUSVERKAUFT</div>''',
'''      const sv = document.querySelector("#s08-svg");
      const plate = el("g", {}, sv); el("ellipse", { cx: 540, cy: 860, rx: 260, ry: 80, fill: "#eef2fb" }, plate); el("ellipse", { cx: 540, cy: 850, rx: 190, ry: 52, fill: "#dfe5f5" }, plate);
      const food = [el("circle", { cx: 470, cy: 820, r: 40, fill: "#ff8a3d" }, plate), el("rect", { x: 520, y: 790, width: 110, height: 50, rx: 18, fill: "#c9611f" }, plate), el("circle", { cx: 600, cy: 835, r: 26, fill: "#39e27a" }, plate)];
      const r = rng(9), cg = el("g", { "data-layout-allow-overlap": "" }, sv), coins = []; for (let i = 0; i < 14; i++) coins.push(txt(cg, 120 + r() * 840, 600, "€", 70 + r() * 40, "#ffd43b", { opacity: 0 }));
      const shelf = el("g", { opacity: 0 }, sv);
      [700, 900].forEach((y) => el("rect", { x: 140, y, width: 800, height: 18, rx: 6, fill: "#8f9bc4" }, shelf));
      const bottles = []; for (let i = 0; i < 6; i++) { const b = el("g", {}, shelf); const x = 200 + i * 130;
        el("rect", { x: x - 30, y: 600, width: 60, height: 100, rx: 12, fill: ["#4da3ff", "#ff4fb0", "#39e27a"][i % 3] }, b); el("rect", { x: x - 12, y: 570, width: 30, height: 30, fill: "#dfe5f5" }, b); bottles.push(b); }
      const mop = el("g", { opacity: 0 }, sv); el("path", { d: "M540 600 L600 1000", stroke: "#c9a46a", "stroke-width": 16 }, mop); el("path", { d: "M540 990 h130 l-20 70 h-90Z", fill: "#dfe5f5" }, mop);
      const mi = at("L14", "Milliarden"), dr = at("L14", "draußen"), l15 = line("L15")[0], au = at("L15", "ausverkauft"), ge = at("L15", "Geschäft");
      tl.fromTo(plate, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.to("#s08-box", { opacity: 1, duration: 0.25 }, mi - 0.3);
      coins.forEach((c, i) => tl.set(c, { opacity: 1 }, mi + i * 0.04).to(c, { y: 500 + (i % 4) * 30, rotation: (i % 2 ? 1 : -1) * 200, svgOrigin: `${c.getAttribute("x")} 600`, duration: 1.0, ease: "power1.in" }, mi + i * 0.04).to(c, { opacity: 0, duration: 0.2 }, mi + 1 + i * 0.04));
      food.forEach((f, i) => tl.to(f, { y: -400, x: (i - 1) * 200, rotation: 200, opacity: 0, duration: 0.6, ease: "power2.in" }, dr - 0.2 + i * 0.08));
      tl.to(plate, { opacity: 0, duration: 0.25 }, l15 - 0.3);
      tl.to("#s08-box", { opacity: 0, duration: 0.2 }, l15 - 0.3);
      tl.to(shelf, { opacity: 1, duration: 0.3 }, l15 - 0.1);
      bottles.forEach((b, i) => tl.to(b, { y: -500, opacity: 0, duration: 0.35, ease: "power2.in" }, au - 0.6 + i * 0.07));
      tl.fromTo("#s08-st", { opacity: 0, scale: 2.4, rotation: -10 }, { opacity: 1, scale: 1, rotation: -10, duration: 0.25, ease: "power4.in" }, au);
      tl.to(["#s08-st", shelf], { opacity: 0, duration: 0.2 }, ge - 0.5);
      tl.to("#s08-box2", { opacity: 1, duration: 0.25 }, ge - 0.3);
      tl.fromTo(mop, { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.8)" }, ge - 0.3);
      tl.to(mop, { rotation: 12, svgOrigin: "540 600", duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }, ge + 0.1);''' + OUT)

S['s09'] = ('''    .s09-k { position: absolute; left: 90px; width: 900px; border-radius: 28px; background: rgba(13,16,38,.94); text-align: center; opacity: 0; }
    .s09-k .n { font: 900 150px/1 Inter, sans-serif; letter-spacing: -.02em; }
    .s09-k .t { margin-top: 12px; font: 700 36px/1.2 "Space Mono", monospace; letter-spacing: .1em; color: #dfe2f5; }
    #s09-k1 { top: 600px; height: 340px; padding-top: 50px; box-sizing: border-box; border: 5px solid #ff3b55; box-shadow: 0 0 50px rgba(255,59,85,.35); }
    #s09-k1 .n { color: #ff3b55; }
    #s09-k2 { top: 600px; height: 400px; padding-top: 46px; box-sizing: border-box; border: 6px solid #4da3ff; box-shadow: 0 0 60px rgba(77,163,255,.45); }
    #s09-k2 .n { color: #4da3ff; } #s09-k2 .ph { margin-top: 14px; font: 900 64px Inter, sans-serif; color: #ffd43b; }''',
'''      <div id="s09-k1" class="s09-k"><div id="s09-n1" class="n">0 M</div><div class="t">SO WEIT FLIEGT ES</div></div>
      <div id="s09-k2" class="s09-k"><div id="s09-n2" class="n">0 L</div><div class="t">MAGENSÄURE PRO TAG</div><div class="ph">pH 1 – WIE SALZSÄURE</div></div>
''' + SVG,
'''      const sv = document.querySelector("#s09-svg");
      const arr = el("path", { d: "M160 1040 H920 M880 1010 L920 1040 L880 1070", stroke: "#ff3b55", "stroke-width": 12, fill: "none", "stroke-linecap": "round", "stroke-dasharray": 900, "stroke-dashoffset": 900 }, sv);
      const m3 = at("L16", "3"), l17 = line("L17")[0], z2 = at("L17", "2"), me = at("L17", "Metall");
      tl.fromTo("#s09-k1", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 0.1);
      count(tl, "#s09-n1", 0, 3, m3 - 0.4, 0.6, "", " METER", "power3.out");
      tl.to(arr, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "power2.out" }, m3 - 0.3);
      tl.to("#s09-k1", { scale: 1.08, duration: 0.12, yoyo: true, repeat: 1 }, m3 + 0.3);
      tl.to(["#s09-k1", arr], { opacity: 0, y: -60, filter: "blur(8px)", duration: 0.25 }, l17 - 0.2);
      tl.fromTo("#s09-k2", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, l17);
      count(tl, "#s09-n2", 0, 2, z2 - 0.4, 0.6, "", " LITER", "power3.out");
      tl.to("#s09-k2", { x: 10, duration: 0.04, repeat: 7, yoyo: true }, me);''' + OUT)

S['s10'] = ('''    .s10-b { position: absolute; top: 950px; width: 450px; height: 150px; border-radius: 26px; text-align: center; font: 900 50px/150px Inter, sans-serif; color: #0b0e22; }
    #s10-tag { left: 560px; top: 560px; width: 470px; height: 96px; border-radius: 48px; background: #ff4fb0; color: #fff; text-align: center; font: 900 46px/96px Inter, sans-serif; opacity: 0; box-shadow: 0 0 40px rgba(255,79,176,.6); }
    #s10-b1 { left: 50px; background: #9be27a; box-shadow: 0 0 40px rgba(77,163,255,.5); } #s10-b2 { left: 580px; background: #4da3ff; box-shadow: 0 0 40px rgba(77,163,255,.5); }
    #s10-f { left: 290px; top: 950px; width: 500px; height: 150px; border-radius: 75px; background: #ff3b55; box-shadow: 0 0 50px rgba(255,59,85,.6); opacity: 0;
      text-align: center; font: 900 64px/150px Inter, sans-serif; color: #fff; }''',
SVG + '''
      <div id="s10-b1" class="s10-b">JA, LEIDER</div><div id="s10-b2" class="s10-b">ZUM GLÜCK NIE</div>
      <div id="s10-tag" class="abs">@ DER SCHULDIGE</div>
      <div id="s10-f" class="abs">+ FOLGEN</div>''',
'''      const sv = document.querySelector("#s10-svg");
      const glow = el("circle", { cx: 540, cy: 760, r: 250, fill: "#9be27a", opacity: 0.2 }, sv);
      const F = sick(sv, 540, 750, 1.25, "#f2c9a5");
      const du = at("L18", "du?"), fl = at("L18", "angekotzt"), bu = at("L18", "angekotzt") + 0.35, ko = at("L18", "Kommentare"), mk = at("L18", "markiere"), l19 = line("L19")[0], fo = at("L19", "folg"), sc = at("L19", "schlecht");
      tl.fromTo(F.g, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1.25, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.to(F.g, { rotation: 5, svgOrigin: "540 900", duration: 0.08, repeat: 5, yoyo: true }, du - 0.1);
      tl.fromTo("#s10-b1", { opacity: 0, y: 80, rotation: -6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, fl - 0.15);
      tl.fromTo("#s10-b2", { opacity: 0, y: 80, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(2)" }, bu - 0.15);
      tl.to(".s10-b", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 3, stagger: 0.3, ease: "sine.inOut" }, ko - 0.3);
      tl.fromTo("#s10-tag", { opacity: 0, scale: 0.4, rotation: -8 }, { opacity: 1, scale: 1, rotation: 4, duration: 0.4, ease: "back.out(2.4)" }, mk - 0.1);
      tl.to("#s10-tag", { y: -20, duration: 0.4, yoyo: true, repeat: 7, ease: "sine.inOut" }, mk + 0.4);
      tl.to(".s10-b", { opacity: 0, y: 60, duration: 0.25, ease: "power3.in" }, l19 - 0.2);
      tl.fromTo("#s10-f", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, fo - 0.1);
      tl.to("#s10-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);
      tl.to(F.head, { attr: { fill: "#9fd35a" }, duration: 0.8 }, fo);
      tl.to(F.cheeks, { scale: 1.45, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 11, ease: "sine.inOut" }, sc - 0.6);
      tl.to(F.g, { x: 548, duration: 0.05, repeat: 25, yoyo: true }, sc - 0.4);
      tl.fromTo(glow, { attr: { opacity: 0.2 } }, { attr: { opacity: 0.55 }, duration: 0.3, repeat: 9, yoyo: true }, sc - 0.4);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
