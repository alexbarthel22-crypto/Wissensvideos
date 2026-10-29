#!/usr/bin/env python3
"""Erzeugt die Szenen-Vorlagen s01–s11 für „Drei Arme“ (einmalig; danach Szenen direkt editieren)."""
from pathlib import Path

HEAD = '''<template>
  <style>
    /*__COMMON_CSS__*/
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
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
OUT = '      tl.to("#@@ID@@-stage > *", { opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }, C.__dur - 0.18);'
S = {}

S['s01'] = ('''    #s01-news { position: absolute; left: 70px; top: 700px; width: 940px; height: 400px; border-radius: 24px;
      background: rgba(14,10,30,.94); border: 5px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.55); overflow: hidden; }
    #s01-news .bar { height: 88px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 34px;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; letter-spacing: .06em; }
    #s01-news .dot { width: 24px; height: 24px; border-radius: 50%; background: #fff; margin-right: 18px; }
    #s01-news .hl { padding: 26px 40px 0; color: #fff; font-family: "Inter", sans-serif; font-weight: 900; font-size: 92px; line-height: 1.02; letter-spacing: -.015em; }
    #s01-news .hl em { font-style: normal; color: #ff4fb0; text-shadow: 0 0 26px rgba(255,79,176,.6); }
    #s01-q { position: absolute; left: 240px; top: 520px; width: 600px; height: 380px; border-radius: 30px; opacity: 0;
      background: #0b0e22; border: 5px solid #2e3670; text-align: center; color: #ff3b55; font-family: "Inter", sans-serif;
      font-weight: 900; font-size: 220px; line-height: 370px; text-shadow: 0 0 30px rgba(255,59,85,.5); }''',
'''      <div id="s01-count" class="cbox"><div class="lab">MENSCHEN MIT 3 ARMEN</div><div class="num" style="color:#ff4fb0">8.200.000.000</div></div>
      <svg id="s01-svg" class="full" viewBox="0 0 1080 1920"><g id="s01-crowd"></g><g id="s01-hero"></g></svg>
      <div id="s01-news"><div class="bar"><span class="dot"></span>WAS WÄRE, WENN …</div>
        <div class="hl">JEDER MENSCH <em>3&nbsp;ARME</em> HÄTTE?</div></div>
      <div id="s01-q">?</div>''',
'''      const crowd = document.querySelector("#s01-crowd"), cols = ["#4da3ff", "#ff4fb0", "#39e27a", "#ffd43b", "#8fa2ff"], minis = [];
      for (let r = 0; r < 5; r++) for (let i = 0; i < 9; i++) minis.push(mini(crowd, 110 + i * 108 + (r % 2) * 54, 460 + r * 128, cols[(i + r) % 5]));
      gsap.set(minis, { opacity: 1 });
      const P = person(document.querySelector("#s01-hero"), "s01-p", 540, 640, 1.5, { arms: [10, -10, 0], shirt: "#ff4fb0" });
      gsap.set(P.g, { opacity: 0 }); gsap.set(P.a3, { scale: 0, svgOrigin: "0 46" }); gsap.set(P.eyes, { scaleY: 0.15, svgOrigin: "0 -56" });
      const du = at("L1", "du"), drit = at("L1", "dritten"), acht = at("L2", "acht"), l2b = line("L2b")[0], verr = at("L2b", "verrückter");
      tl.fromTo("#s01-news", { scale: 1.04 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);
      tl.fromTo("#s01-news .dot", { opacity: 1 }, { opacity: 0.2, duration: 0.25, repeat: 3, yoyo: true, ease: "none" }, 0.1);
      minis.forEach((m, i) => tl.fromTo(m, { y: 0 }, { y: -10, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0.05 + (i % 9) * 0.03));
      tl.to(["#s01-news", "#s01-crowd", "#s01-count"], { opacity: 0, y: 60, duration: 0.3, ease: "power3.in" }, du - 0.3);
      tl.to(P.g, { opacity: 1, duration: 0.3 }, du - 0.1);
      tl.to(P.eyes, { scaleY: 1, duration: 0.15, svgOrigin: "0 -56" }, drit - 0.6);
      tl.to(P.a3, { scale: 1, rotation: -128, duration: 0.45, ease: "back.out(2.4)", svgOrigin: "0 46" }, drit);
      tl.to(P.eyes, { scale: 1.35, duration: 0.15, svgOrigin: "0 -56" }, drit + 0.1);
      wave(tl, P.a3, -128, -105, drit + 0.5, 2);
      tl.to(P.g, { opacity: 0, duration: 0.25 }, acht - 0.2);
      tl.to(["#s01-crowd", "#s01-count"], { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, acht - 0.1);
      tl.fromTo("#s01-count", { scale: 1 }, { scale: 1.1, duration: 0.15, yoyo: true, repeat: 1 }, acht + 0.3);
      tl.to(["#s01-crowd", "#s01-count"], { opacity: 0, filter: "blur(8px)", duration: 0.2 }, l2b - 0.15);
      tl.fromTo("#s01-q", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, l2b);
      tl.to("#s01-q", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, verr);
''' + OUT)

S['s02'] = ('''    #s02-x { position: absolute; left: 290px; top: 520px; width: 500px; height: 500px; opacity: 0; }''',
'''      <svg id="s02-svg" class="full" viewBox="0 0 1080 1920">
        <g id="s02-shirt"><path d="M380 470 L460 440 Q540 480 620 440 L700 470 L800 560 L740 630 L700 600 L700 1010 L380 1010 L380 600 L340 630 L280 560Z" fill="#4da3ff" />
          <path d="M460 440 Q540 500 620 440" fill="none" stroke="#2f73c4" stroke-width="10" /></g>
        <circle id="s02-hole" cx="540" cy="700" r="0" fill="#0e1124" />
        <g id="s02-sc"><circle cx="0" cy="0" r="26" fill="none" stroke="#dfe3f5" stroke-width="10" /><circle cx="0" cy="70" r="26" fill="none" stroke="#dfe3f5" stroke-width="10" />
          <path d="M20 14 L140 60 M20 56 L140 10" stroke="#dfe3f5" stroke-width="14" stroke-linecap="round" /></g>
        <g id="s02-arm"><rect x="528" y="560" width="24" height="140" rx="12" fill="#f2c9a5" /><circle cx="540" cy="556" r="16" fill="#f2c9a5" /></g>
      </svg>
      <svg id="s02-x" viewBox="0 0 500 500"><g stroke="#ff3b55" stroke-width="40" stroke-linecap="round"><line x1="60" y1="60" x2="440" y2="440" /><line x1="440" y1="60" x2="60" y2="440" /></g></svg>
      <div id="s02-box" class="cbox y" style="opacity:0"><div class="lab">NEUE LÖCHER</div><div id="s02-n" class="num">0</div></div>''',
'''      const kein = at("L3", "kein"), l4 = line("L4")[0], loch = at("L4", "Loch");
      gsap.set("#s02-sc", { x: 900, y: 1000, rotation: -20 }); gsap.set("#s02-arm", { scaleY: 0, svgOrigin: "540 700" });
      tl.fromTo("#s02-shirt", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.fromTo("#s02-x", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "expo.out" }, kein);
      tl.to("#s02-x", { opacity: 0, duration: 0.2 }, l4 - 0.1);
      tl.to("#s02-box", { opacity: 1, duration: 0.25 }, l4);
      count(tl, "#s02-n", 0, 8200000000, l4, loch - l4 + 0.4, "", "", "power2.in");
      tl.to("#s02-sc", { x: 560, y: 650, rotation: 0, duration: 0.5, ease: "power3.out" }, loch - 0.6);
      tl.to("#s02-sc", { rotation: 12, duration: 0.08, repeat: 5, yoyo: true }, loch - 0.1);
      tl.to("#s02-hole", { attr: { r: 30 }, duration: 0.2, ease: "back.out(2)" }, loch + 0.1);
      tl.to("#s02-sc", { opacity: 0, x: 900, duration: 0.3, ease: "power2.in" }, loch + 0.4);
      tl.to("#s02-arm", { scaleY: 1, duration: 0.35, ease: "back.out(2.2)", svgOrigin: "540 700" }, loch + 0.5);
''' + OUT)

S['s03'] = ('', '''      <svg id="s03-svg" class="full" viewBox="0 0 1080 1920"><g id="s03-hero"></g></svg>
      <div id="s03-box" class="cbox g" style="opacity:0"><div class="lab">MULTITASKING</div><div id="s03-n" class="num">100 %</div></div>''',
'''      const P = person(document.querySelector("#s03-hero"), "s03-p", 540, 640, 1.45, { arms: [70, -60, -132], items: ["cup", "phone", "bread"], shirt: "#ffd43b" });
      const items = [P.a1, P.a2, P.a3].map((a) => a.lastChild);
      gsap.set(items, { opacity: 0, scale: 0, transformOrigin: "50% 50%" });
      tl.fromTo(P.g, { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.05);
      ["Kaffee", "Handy", "Brötchen"].forEach((w, i) => tl.to(items[i], { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)" }, at("L5", w) - 0.05));
      const g = at("L5", "gleichzeitig");
      tl.to("#s03-box", { opacity: 1, duration: 0.25 }, g - 0.1);
      count(tl, "#s03-n", 100, 300, g, 0.6, "", " %", "power3.out");
      [P.a1, P.a2, P.a3].forEach((a, i) => wave(tl, a, 0, [55, -45, -115][i], g + 0.1 + i * 0.05, 2, 0.15));
''' + OUT)

NET = ''.join(f'<line x1="{x}" y1="520" x2="{x}" y2="1080" />' for x in range(170, 970, 60)) + \
      ''.join(f'<line x1="110" y1="{y}" x2="970" y2="{y}" />' for y in range(580, 1080, 60))
S['s04'] = ('', '''      <svg id="s04-svg" class="full" viewBox="0 0 1080 1920">
        <g stroke="#2e3670" stroke-width="3">''' + NET + '''</g>
        <g id="s04-goal" fill="none" stroke="#dfe3f5" stroke-width="16"><path d="M110 1080 L110 520 L970 520 L970 1080" /></g>
        <rect x="0" y="1080" width="1080" height="60" fill="#1d6b3a" />
        <g id="s04-hero"></g><g id="s04-balls"></g></svg>
      <div id="s04-box" class="cbox g" style="opacity:0"><div class="lab">GEHALTEN</div><div id="s04-n" class="num">0 %</div></div>''',
'''      const P = person(document.querySelector("#s04-hero"), "s04-p", 540, 760, 1.25, { arms: [100, -95, -140], shirt: "#39e27a" });
      const bg = document.querySelector("#s04-balls"), balls = [];
      const tgt = [[260, 640], [820, 640], [540, 470], [300, 900], [780, 880]];
      tgt.forEach(() => { const b = el("g", {}, bg); el("circle", { cx: 0, cy: 0, r: 34, fill: "#fff" }, b); el("path", { d: "M-12 -10 l12 -8 l12 8 l-4 14 h-16z", fill: "#161a36" }, b); balls.push(b); });
      gsap.set(balls, { opacity: 0 });
      const fast = at("L6", "fast");
      tl.fromTo(["#s04-goal", P.g], { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "expo.out" }, 0.05);
      const t0 = line("L6")[0] + 0.3, step = (fast - t0) / tgt.length;
      balls.forEach((b, i) => {
        const t = t0 + i * step, [x, y] = tgt[i];
        tl.fromTo(b, { x: 540, y: 1700, scale: 1.8, opacity: 1 }, { x, y, scale: 1, duration: 0.35, ease: "power2.out" }, t);
        tl.to(b, { x: x + (x < 540 ? -200 : 200), y: y - 260, opacity: 0, duration: 0.3, ease: "power2.out" }, t + 0.35);
        tl.to([P.a1, P.a2, P.a3][i % 3], { rotation: "+=12", duration: 0.08, yoyo: true, repeat: 1 }, t + 0.3);
      });
      tl.to("#s04-box", { opacity: 1, duration: 0.25 }, fast - 0.3);
      count(tl, "#s04-n", 0, 97, fast - 0.2, 0.7, "", " %", "power3.out");
''' + OUT)

S['s05'] = ('', '''      <svg id="s05-svg" class="full" viewBox="0 0 1080 1920">
        <rect x="160" y="1000" width="760" height="40" rx="10" fill="#6b4f2a" />
        <rect x="200" y="960" width="200" height="40" rx="6" fill="#d9b07a" /><ellipse cx="760" cy="960" rx="120" ry="34" fill="#2c3470" />
        <g id="s05-hero"></g></svg>
      <div id="s05-box" class="cbox b" style="opacity:0"><div class="lab">OP-DAUER</div><div id="s05-n" class="num">180 MIN</div></div>''',
'''      const P = person(document.querySelector("#s05-hero"), "s05-p", 540, 600, 1.35, { arms: [40, -40, -128], items: ["knife", "spoon", "salt"], shirt: "#ffffff", hair: "#222" });
      tl.fromTo(P.g, { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.05);
      [["schneiden", P.a1, 40, 70], ["rühren", P.a2, -40, -70], ["würzen", P.a3, -128, -105]].forEach(([w, a, f, t]) => wave(tl, a, f, t, at("L8", w) - 0.05, 2, 0.12));
      const ch = at("L8", "Chirurgen"), sch = at("L8", "schneller");
      tl.to("#s05-box", { opacity: 1, duration: 0.25 }, ch - 0.1);
      count(tl, "#s05-n", 180, 120, sch - 0.2, 0.7, "", " MIN", "power3.out");
      tl.to("#s05-box", { borderColor: "#39e27a", duration: 0.2 }, sch + 0.4);
''' + OUT)

S['s06'] = ('', '''      <svg id="s06-svg" class="full" viewBox="0 0 1080 1920"><g id="s06-seats"></g><g id="s06-hero"></g></svg>
      <div id="s06-box" class="cbox y" style="opacity:0"><div class="lab">SITZBREITE</div><div id="s06-n" class="num">45 CM</div></div>''',
'''      const Sg = document.querySelector("#s06-seats"), seats = [];
      for (let i = 0; i < 3; i++) { const g = el("g", {}, Sg); el("rect", { x: -90, y: 0, width: 180, height: 220, rx: 30, fill: ["#4da3ff", "#ff4fb0", "#39e27a"][i] }, g);
        el("rect", { x: -100, y: 200, width: 200, height: 70, rx: 20, fill: "#2c3470" }, g); gsap.set(g, { x: 240 + i * 300, y: 640 }); seats.push(g); }
      const P = person(document.querySelector("#s06-hero"), "s06-p", 540, 560, 1.1, { arms: [60, -60, -120], shirt: "#ff4fb0" });
      gsap.set(P.g, { opacity: 0 });
      const br = at("L9", "breiter"), pl = at("L10", "Platz");
      seats.forEach((s, i) => tl.fromTo(s, { opacity: 0, y: 700 }, { opacity: 1, y: 640, duration: 0.35, ease: "back.out(1.8)" }, 0.1 + i * 0.25));
      tl.to("#s06-box", { opacity: 1, duration: 0.25 }, br - 0.3);
      seats.forEach((s, i) => tl.to(s, { scaleX: 1.3, x: 200 + i * 340, duration: 0.45, ease: "back.out(1.6)" }, br));
      count(tl, "#s06-n", 45, 60, br, 0.45, "", " CM");
      tl.to(seats, { opacity: 0.25, duration: 0.25 }, line("L10")[0] - 0.1);
      tl.to(P.g, { opacity: 1, duration: 0.25 }, line("L10")[0]);
      wave(tl, P.a3, -120, -95, pl - 0.1, 2, 0.12);
''' + OUT)

S['s07'] = ('''    #s07-pack { position: absolute; left: 240px; top: 480px; width: 600px; height: 560px; border-radius: 30px;
      background: #1d2350; border: 6px solid #39e27a; box-shadow: 0 0 40px rgba(57,226,122,.35); }
    #s07-pack .t { position: absolute; left: 0; width: 100%; top: 30px; text-align: center; color: #39e27a;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 76px; }''',
'''      <div id="s07-pack"><div class="t">3ER-PACK</div><svg id="s07-g" class="abs" style="left:0;top:150px;width:600px;height:380px" viewBox="0 0 600 380"></svg></div>
      <svg id="s07-conf" class="full" viewBox="0 0 1080 1920"></svg>
      <div id="s07-box" class="cbox g" style="opacity:0"><div class="lab">HANDSCHUH-VERKÄUFE</div><div id="s07-n" class="num">+0 %</div></div>''',
'''      const G = document.querySelector("#s07-g"), gl = [];
      for (let i = 0; i < 3; i++) { const g = el("g", {}, G); const h = el("g", { transform: `translate(${120 + i * 180} 200) scale(3.2)` }, g); ITEMS.glove(h); gl.push(g); }
      const cf = document.querySelector("#s07-conf"), r = rng(7), conf = [];
      for (let i = 0; i < 60; i++) conf.push(el("rect", { x: 540, y: 760, width: 16, height: 26, rx: 4, fill: ["#ffd43b", "#ff4fb0", "#39e27a", "#4da3ff"][i % 4], opacity: 0 }, cf));
      tl.fromTo("#s07-pack", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, 0.05);
      tl.fromTo(gl, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.12, ease: "back.out(2)" }, at("L11", "Dreierpack") - 0.2);
      const mb = at("L11", "Modebranche"), j = at("L11", "jubelt");
      tl.to("#s07-box", { opacity: 1, duration: 0.25 }, mb - 0.1);
      count(tl, "#s07-n", 0, 50, mb, j - mb + 0.3, "+", " %", "power2.out");
      conf.forEach((c) => tl.fromTo(c, { opacity: 1, x: 0, y: 0, rotation: 0 }, { x: (r() - 0.5) * 1000, y: (r() - 0.7) * 900, rotation: r() * 720, opacity: 0, duration: 1.2, ease: "power2.out" }, j));
''' + OUT)

S['s08'] = ('''    #s08-paper { position: absolute; left: 140px; top: 440px; width: 800px; height: 360px; border-radius: 16px; background: #f3f1ea; }''',
'''      <div id="s08-paper"></div>
      <svg id="s08-svg" class="full" viewBox="0 0 1080 1920">
        <g id="s08-lines" fill="none" stroke-width="10" stroke-linecap="round">
          <path id="s08-l0" d="M200 530 q40 -30 80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0" stroke="#4da3ff" />
          <path id="s08-l1" d="M200 620 q40 -30 80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0" stroke="#ff4fb0" />
          <path id="s08-l2" d="M200 710 q40 -30 80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0" stroke="#39e27a" /></g>
        <g id="s08-pens"></g><g id="s08-piano"></g></svg>''',
'''      const L = [0, 1, 2].map((i) => document.querySelector("#s08-l" + i)), len = L[0].getTotalLength();
      L.forEach((p) => gsap.set(p, { attr: { "stroke-dasharray": len, "stroke-dashoffset": len } }));
      const pens = [0, 1, 2].map(() => { const g = el("g", {}, document.querySelector("#s08-pens")); const h = el("g", { transform: "rotate(200) scale(1.6)" }, g); ITEMS.pen(h); return g; });
      const pi = document.querySelector("#s08-piano"), keys = [];
      for (let i = 0; i < 16; i++) keys.push(el("rect", { x: 100 + i * 55, y: 880, width: 50, height: 220, rx: 6, fill: "#fff", opacity: i < 10 ? 1 : 0 }, pi));
      for (let i = 0; i < 15; i++) if (i % 7 !== 2 && i % 7 !== 6) el("rect", { x: 138 + i * 55, y: 880, width: 30, height: 130, rx: 4, fill: "#161a36", opacity: 0, class: i < 9 ? "s08-bk" : "s08-bkx" }, pi);
      const dr = at("L12", "dreihändig"), kl = at("L12", "Klaviere"), ta = at("L12", "Tasten");
      gsap.set(pi, { opacity: 0 });
      tl.fromTo(["#s08-paper", "#s08-lines", "#s08-pens"], { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 0.05);
      L.forEach((p, i) => {
        tl.to(p, { attr: { "stroke-dashoffset": 0 }, duration: 1.4, ease: "none" }, dr - 0.2 + i * 0.05);
        tl.fromTo(pens[i], { x: 200, y: 460 + i * 90 }, { x: 760, y: 460 + i * 90, duration: 1.4, ease: "none" }, dr - 0.2 + i * 0.05);
      });
      tl.fromTo(pi, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, kl - 0.1);
      tl.to(".s08-bk", { opacity: 1, duration: 0.01 }, kl - 0.1);
      tl.to(keys.slice(10), { opacity: 1, duration: 0.15, stagger: 0.06, ease: "back.out(2)" }, ta - 0.1);
      tl.to(".s08-bkx", { opacity: 1, duration: 0.15, stagger: 0.06 }, ta);
      tl.to(keys.slice(10), { attr: { fill: "#ff9fd2" }, duration: 0.2 }, ta + 0.4);
''' + OUT)

S['s09'] = ('', '''      <svg id="s09-svg" class="full" viewBox="0 0 1080 1920">
        <ellipse cx="540" cy="900" rx="380" ry="120" fill="#dfe3f5" /><ellipse cx="540" cy="890" rx="300" ry="86" fill="#c9cde6" />
        <g id="s09-food"></g></svg>
      <div id="s09-box" class="cbox r" style="opacity:0"><div class="lab">KALORIEN PRO TAG</div><div id="s09-n" class="num">2.000</div></div>''',
'''      const F = document.querySelector("#s09-food"), food = [];
      const burger = (x, y, s) => { const g = el("g", {}, F); const h = el("g", { transform: `translate(${x} ${y}) scale(${s})` }, g);
        el("path", { d: "M-80 0 q80 -90 160 0z", fill: "#e0a35a" }, h); el("rect", { x: -84, y: 0, width: 168, height: 18, rx: 8, fill: "#39e27a" }, h);
        el("rect", { x: -86, y: 16, width: 172, height: 26, rx: 12, fill: "#7a3b1a" }, h); el("rect", { x: -80, y: 40, width: 160, height: 26, rx: 10, fill: "#e0a35a" }, h); return g; };
      food.push(burger(400, 820, 1), burger(680, 820, 1), burger(540, 760, 1.15));
      gsap.set(food, { opacity: 0, y: -60 });
      const mu = at("L13", "Muskeln"), hu = at("L13", "Hunger"), de = at("L13", "deutlich");
      tl.to(food.slice(0, 2), { opacity: 1, y: 0, duration: 0.35, stagger: 0.15, ease: "bounce.out" }, mu - 0.1);
      tl.to("#s09-box", { opacity: 1, duration: 0.25 }, hu - 0.2);
      tl.to(food[2], { opacity: 1, y: 0, duration: 0.4, ease: "bounce.out" }, de - 0.1);
      count(tl, "#s09-n", 2000, 2300, de - 0.1, 0.7, "", "", "power3.out");
''' + OUT)

S['s10'] = ('''    #s10-case { position: absolute; left: 330px; top: 430px; width: 420px; height: 640px; border-radius: 12px;
      border: 6px solid #a9d2ff; background: rgba(77,163,255,.08); box-shadow: 0 0 40px rgba(77,163,255,.3); }
    #s10-plate { position: absolute; left: 240px; top: 1080px; width: 600px; height: 70px; border-radius: 10px; background: #b8944a;
      color: #1a1205; text-align: center; line-height: 70px; font-family: "Space Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: .06em; }''',
'''      <svg id="s10-svg" class="full" viewBox="0 0 1080 1920"><g id="s10-in"></g><g id="s10-out"></g></svg>
      <div id="s10-case"></div>
      <div id="s10-plate">MENSCH · 2026 · NUR 2 ARME</div>''',
'''      const P = person(document.querySelector("#s10-in"), "s10-p", 540, 640, 1.2, { three: false, arms: [8, -8], shirt: "#8fa2ff" });
      const V1 = person(document.querySelector("#s10-out"), "s10-v1", 160, 860, 0.9, { arms: [20, -30, -132], shirt: "#ff4fb0", hair: "#e8c26a" });
      const V2 = person(document.querySelector("#s10-out"), "s10-v2", 920, 860, 0.9, { arms: [40, -20, -135], shirt: "#39e27a", hair: "#222" });
      const nur = at("L14", "nur"), fr = at("L14", "fragt");
      tl.fromTo(["#s10-case", "#s10-in"], { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }, 0.05);
      tl.fromTo("#s10-plate", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.5);
      tl.fromTo([V1.g, V2.g], { opacity: 0 }, { opacity: 1, duration: 0.3, stagger: 0.15 }, fr - 0.2);
      wave(tl, V1.a3, -132, -110, fr + 0.2, 2);
      tl.fromTo("#s10-plate", { scale: 1 }, { scale: 1.12, duration: 0.18, yoyo: true, repeat: 1 }, nur);
      wave(tl, V2.a3, -135, -110, nur + 0.3, 2);
''' + OUT)

S['s11'] = ('''    .s11-c { position: absolute; top: 980px; height: 120px; border-radius: 24px; text-align: center; line-height: 120px;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; color: #0b0e22; }
    #s11-c1 { left: 60px; width: 300px; background: #39e27a; } #s11-c2 { left: 390px; width: 300px; background: #ffd43b; } #s11-c3 { left: 720px; width: 300px; background: #ff4fb0; }''',
'''      <svg id="s11-svg" class="full" viewBox="0 0 1080 1920"><g id="s11-hero"></g></svg>
      <div id="s11-c1" class="s11-c">ZOCKEN?</div><div id="s11-c2" class="s11-c">KOCHEN?</div><div id="s11-c3" class="s11-c">???</div>''',
'''      const P = person(document.querySelector("#s11-hero"), "s11-p", 540, 560, 1.3, { arms: [140, -150, -95], shirt: "#ff4fb0" });
      const du = at("L15", "du?"), dr = at("L15", "dritten");
      tl.fromTo(P.g, { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "expo.out" }, 0.05);
      wave(tl, P.a1, 140, 160, du, 3); wave(tl, P.a2, -150, -165, du + 0.1, 3); wave(tl, P.a3, -95, -75, du + 0.05, 3);
      tl.fromTo(".s11-c", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, stagger: 0.12, ease: "back.out(1.8)" }, dr);
''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    out = HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid)
    (here / f"{sid}.html").write_text(out)
print(sorted(S))
