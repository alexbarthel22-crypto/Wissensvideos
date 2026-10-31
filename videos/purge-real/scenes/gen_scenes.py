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
    #s01-call b { display: block; margin-top: 40px; font: 700 110px/1 Oswald, sans-serif; color: #fff; } #s01-call i { display: block; margin-top: 16px; font: 700 40px Oswald, sans-serif; font-style: normal; color: #ff3b55; letter-spacing: .06em; }''',
SVG + '''
      <div id="s01-call" class="abs"><b>112</b><i>NICHT ERREICHBAR</i></div>''',
'''      const sv = document.querySelector("#s01-svg");
      night(sv, "s01-n", "#07091a", "#2a1630", [850, 660]);
      pines(sv, 1010, "#0f1424", 4);
      const H = [[20, 230, 250, "#3b3550", [1, 0]], [300, 200, 230, "#45405c", [0, 1]], [560, 240, 260, "#37324a", [1, 1]], [850, 220, 240, "#423b56", [0, 1]]].map(([x, w, h, c, lit]) => house(sv, x, 1150, w, h, c, { lit }));
      el("rect", { x: 0, y: 1150, width: 1080, height: 300, fill: "#141320" }, sv);
      const L = lamp(sv, 230, 1200);
      const pk = [pumpkin(sv, 130, 1175, 0.9), pumpkin(sv, 690, 1172, 0.8), pumpkin(sv, 960, 1176, 0.85)];
      const fg = fog(sv, 1110, 0.3, 6);
      const M = masked(sv, 560, 1360, 1.15, "#1d1f2b", true);
''' + RED + '''      const mo = at("L2", "Mord"), ni = at("L3", "nicht"), sz = at("L3", "schockierendste");
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.32, duration: 0.25, repeat: 7, yoyo: true, ease: "sine.inOut" }, 0);
      pk.forEach((k, i) => tl.fromTo(k.face, { opacity: 1 }, { opacity: 0.5, duration: 0.12, repeat: 9, yoyo: true }, 0.3 + i * 0.2));
      tl.to(fg, { x: 60, duration: 8, ease: "none" }, 0);
      tl.to(L.cone, { attr: { opacity: 0.04 }, duration: 0.06, repeat: 5, yoyo: true }, 1.5);
      tl.to(M.g, { scale: 1.45, y: 1450, duration: 0.5, ease: "power3.in" }, mo - 0.3);
      tl.fromTo(red, { opacity: 0.6 }, { opacity: 0, duration: 0.5 }, mo);
      tl.fromTo("#s01-call", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, ni - 0.4);
      tl.to("#s01-call", { x: 10, duration: 0.04, repeat: 7, yoyo: true }, ni + 0.2);
      tl.to("#s01-call", { opacity: 0, duration: 0.25 }, sz - 0.6);
      tl.to(M.mask, { scaleY: 0.92, svgOrigin: "0 -345", duration: 0.15, yoyo: true, repeat: 3 }, sz);''' + OUT)

S['s02'] = ('''    #s02-st { left: 230px; top: 760px; width: 620px; height: 150px; border: 10px solid #ff3b55; border-radius: 18px; color: #ff3b55; font: 700 90px/130px Oswald, sans-serif; text-align: center; opacity: 0; background: rgba(10,10,16,.6); }''',
SVG + '''
      <div id="s02-st" class="abs">AUSVERKAUFT</div>''',
'''      const sv = document.querySelector("#s02-svg");
      night(sv, "s02-n", "#151a2c", "#2a2236", null);
      const shop = el("g", {}, sv);
      el("rect", O({ x: 80, y: 560, width: 920, height: 760, fill: "#2c2f3e" }), shop);
      [700, 900, 1100].forEach((y) => el("rect", O({ x: 110, y, width: 860, height: 20, fill: "#8a8f9c", "stroke-width": 4 }), shop));
      const items = []; const r = rng(2);
      [680, 880, 1080].forEach((y) => { for (let i = 0; i < 9; i++) items.push(el("rect", O({ x: 130 + i * 92, y: y - 70, width: 70, height: 70, rx: 6, fill: ["#ffd43b", "#ff8a3d", "#7fd0ff", "#a87a4a"][i % 4], "stroke-width": 4 }), shop)); });
      el("rect", O({ x: 360, y: 590, width: 360, height: 70, rx: 10, fill: "#ffd43b" }), shop); txt(shop, 540, 642, "BAUMARKT", 46, K);
      const st = el("g", { opacity: 0 }, sv);
      const A = house(st, 120, 1250, 380, 420, "#4a4258", { lit: [0, 0], n: 2 }), B = house(st, 600, 1250, 360, 400, "#3e3a4e", { lit: [1, 1], n: 2 });
      el("rect", { x: 0, y: 1250, width: 1080, height: 200, fill: "#141320" }, st);
      const planks = []; A.wins.forEach((w) => { const x = +w.getAttribute("x"), y = +w.getAttribute("y"); planks.push(plank(st, x - 14, y + 4, 80, -14), plank(st, x - 14, y + 30, 80, 12)); });
      const shut = el("rect", O({ x: A.wins[0].getAttribute("x") - 0, y: 0, width: 0, height: 0, fill: "none" }), st);
      const crack = B.wins.map((w) => { const x = +w.getAttribute("x"), y = +w.getAttribute("y"); return el("path", { d: `M${x + 26} ${y + 28} l-18 -20 M${x + 26} ${y + 28} l20 -22 M${x + 26} ${y + 28} l-14 26 M${x + 26} ${y + 28} l22 16`, stroke: "#fff", "stroke-width": 3, opacity: 0 }, st); });
      const ok = txt(st, 310, 760, "✓", 120, "#39e27a", { opacity: 0 }), no = txt(st, 780, 760, "✕", 120, "#ff3b55", { opacity: 0 });
      const le = at("L4", "leergekauft"), we = at("L4", "weg"), l5 = line("L5")[0], ve = at("L5", "verbarrikadiert"), sc = at("L5", "schutzlos");
      items.forEach((it, i) => tl.to(it, { opacity: 0, y: -40, duration: 0.18 }, le - 0.6 + (i % 27) * 0.03));
      tl.fromTo("#s02-st", { opacity: 0, scale: 2.2, rotation: -8 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.25, ease: "power4.in" }, we - 0.15);
      tl.to(["#s02-st", shop], { opacity: 0, duration: 0.25 }, l5 - 0.3);
      tl.to(st, { opacity: 1, duration: 0.3 }, l5 - 0.2);
      planks.forEach((pl, i) => tl.fromTo(pl, { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: 0.2, ease: "back.out(2)" }, ve - 0.2 + i * 0.12));
      tl.to(ok, { opacity: 1, duration: 0.2 }, ve + 0.5);
      tl.to(crack, { opacity: 1, duration: 0.1 }, sc - 0.2);
      tl.to(no, { opacity: 1, duration: 0.2 }, sc);
      tl.to(B.g, { x: 6, duration: 0.04, repeat: 7, yoyo: true }, sc);''' + OUT)

S['s03'] = ('''    #s03-np { left: 140px; top: 580px; width: 800px; height: 560px; background: #e8dfc8; border: 5px solid #0b0c14; border-radius: 10px; opacity: 0; transform: rotate(-3deg); color: #1a1a1a; text-align: center; box-shadow: 0 30px 70px rgba(0,0,0,.5); }
    #s03-np h3 { margin: 30px 30px 10px; padding-bottom: 12px; border-bottom: 4px double #1a1a1a; font: 700 64px/1 "EB Garamond", serif; }
    #s03-np h4 { margin: 14px 40px; font: 700 70px/1.05 Oswald, sans-serif; }
    #s03-np p { margin: 0 50px; font: 500 30px/1.3 "EB Garamond", serif; color: #444; }
    #s03-np small { position: absolute; left: 0; right: 0; bottom: 14px; font: 500 22px Inter, sans-serif; color: #777; }
    .s03-i { position: absolute; top: 1160px; width: 260px; height: 190px; border-radius: 20px; background: rgba(10,10,16,.85); border: 4px solid #ff3b55; text-align: center; opacity: 0; color: #fff; }
    .s03-i b { display: block; margin-top: 18px; font: 700 80px/1 Oswald, sans-serif; color: #ff3b55; } .s03-i i { display: block; margin-top: 10px; font: 700 30px Oswald, sans-serif; font-style: normal; }''',
SVG + '''
      <div id="s03-np" class="abs"><h3>Montreal · 1969</h3><h4>POLIZEI STREIKT<br>16 STUNDEN</h4><p>Plünderungen, Überfälle und Brände in der Innenstadt.</p><small data-layout-ignore>vereinfachte Darstellung</small></div>
      <div id="s03-i1" class="s03-i" style="left:60px"><b>$</b><i>BANKÜBERFÄLLE</i></div><div id="s03-i2" class="s03-i" style="left:410px"><b>100+</b><i>GESCHÄFTE</i></div><div id="s03-i3" class="s03-i" style="left:760px"><b>2</b><i>TOTE</i></div>''',
'''      const sv = document.querySelector("#s03-svg");
      night(sv, "s03-n", "#1c1a24", "#2e2430", null);
      const r = rng(9); for (let i = 0; i < 30; i++) el("circle", { cx: r() * 1080, cy: 500 + r() * 900, r: 2 + r() * 3, fill: "#ffb36b", opacity: 0.3 + r() * 0.4 }, sv);
      const n69 = at("L6", "1969"), st = at("L6", "streikt"), ba = at("L7", "Banküberfälle"), hu = at("L7", "100"), to = at("L7", "Tote");
      tl.fromTo("#s03-np", { opacity: 0, scale: 1.4, rotation: 8 }, { opacity: 1, scale: 1, rotation: -3, duration: 0.5, ease: "power3.out" }, Math.min(n69 - 0.3, at("L6", "Montreal") - 0.2));
      tl.to("#s03-np", { y: -150, scale: 0.8, duration: 0.4, ease: "power2.inOut" }, ba - 0.6);
      [["#s03-i1", ba], ["#s03-i2", hu], ["#s03-i3", to]].forEach(([id, t]) => tl.fromTo(id, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, t - 0.15));
      tl.to("#s03-i3", { x: 8, duration: 0.04, repeat: 7, yoyo: true }, to + 0.2);''' + OUT)

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

S['s05'] = ('''    #s05-st { left: 300px; top: 640px; width: 480px; height: 150px; border: 10px solid #ff3b55; border-radius: 18px; color: #ff3b55; font: 700 100px/130px Oswald, sans-serif; text-align: center; opacity: 0; background: rgba(10,10,16,.6); }''',
SVG + '''
      <div id="s05-st" class="abs">LEGAL</div>''',
'''      const sv = document.querySelector("#s05-svg");
      night(sv, "s05-n", "#08091a", "#24122a", [180, 660]);
      pines(sv, 1050, "#0f1424", 8);
      const shop = el("g", {}, sv); el("rect", O({ x: 560, y: 760, width: 460, height: 420, fill: "#2c2f3e" }), shop);
      el("rect", O({ x: 600, y: 790, width: 380, height: 60, rx: 8, fill: "#ffd43b" }), shop); txt(shop, 790, 836, "JUWELIER", 44, K);
      const win = el("rect", O({ x: 600, y: 880, width: 380, height: 220, fill: "#7fd0ff", opacity: 0.85 }), shop);
      const shards = []; const r = rng(4); for (let i = 0; i < 10; i++) shards.push(el("path", { d: `M${650 + r() * 280} ${900 + r() * 180} l${20 + r() * 30} ${-10 - r() * 20} l${-10} ${30 + r() * 20}Z`, fill: "#bfe7ff", opacity: 0 }, sv));
      el("rect", { x: 0, y: 1180, width: 1080, height: 260, fill: "#141320" }, sv);
      const fg = fog(sv, 1150, 0.28, 11);
      const gang = [[160, 1360, 0.95, "#1d1f2b"], [330, 1330, 0.85, "#2a1c26"], [470, 1380, 1.05, "#1a2230"], [60, 1340, 0.8, "#231d2b"]].map(([x, y, s, c], i) => masked(sv, x, y, s, c, i === 2));
''' + RED + '''      const ba = at("L11", "Banden"), ra = at("L11", "Rachegelüsten"), zu = at("L11", "zuschauen"), l12 = line("L12")[0], ge = at("L12", "geplündert"), ni = at("L12", "nichts"), le = at("L12", "legal");
      gang.forEach((m, i) => tl.fromTo(m.g, { x: `-=${300}`, opacity: 0 }, { x: `+=${300}`, opacity: 1, duration: 1.2, ease: "power2.out" }, ba - 0.4 + i * 0.25));
      tl.to(gang.map((m) => m.g), { y: "-=10", duration: 0.3, yoyo: true, repeat: 9, stagger: 0.1 }, ba + 1.0);
      tl.to(fg, { x: -80, duration: 8, ease: "none" }, 0);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.25, duration: 0.2, repeat: 3, yoyo: true }, ra);
      tl.to(win, { opacity: 0, duration: 0.05 }, ge - 0.1);
      shards.forEach((s, i) => tl.fromTo(s, { opacity: 1, x: 0, y: 0 }, { x: (i % 2 ? 1 : -1) * (40 + i * 10), y: 160 + i * 8, rotation: 120, opacity: 0, svgOrigin: "790 990", duration: 0.7, ease: "power2.in" }, ge - 0.1));
      tl.fromTo("#s05-st", { opacity: 0, scale: 2.4, rotation: -10 }, { opacity: 1, scale: 1, rotation: -10, duration: 0.25, ease: "power4.in" }, at("L12", "Zahlt"));''' + OUT)

S['s06'] = ('''    .s06-k { position: absolute; top: 600px; width: 450px; height: 640px; border-radius: 24px; background: rgba(12,12,20,.88); text-align: center; opacity: 0; color: #fff; }
    .s06-k h3 { margin-top: 30px; font: 700 52px Oswald, sans-serif; letter-spacing: .04em; } .s06-k p { margin: 30px 26px 0; font: 700 40px/1.35 Oswald, sans-serif; }
    #s06-k1 { left: 50px; border: 5px solid #39e27a; } #s06-k1 h3 { color: #39e27a; } #s06-k2 { left: 580px; border: 5px solid #ff3b55; } #s06-k2 h3 { color: #ff3b55; }
    #s06-w { left: 140px; top: 760px; width: 800px; height: 300px; border-radius: 26px; background: rgba(12,12,20,.9); border: 5px solid #ffd43b; text-align: center; color: #ffd43b; opacity: 0; font: 700 70px/1.25 Oswald, sans-serif; padding-top: 50px; box-sizing: border-box; }''',
SVG + '''
      <div id="s06-k1" class="s06-k"><h3>IM FILM</h3><p>KRIMINALITÄT ↓<br>ARBEITSLOSIGKEIT ↓</p></div>
      <div id="s06-k2" class="s06-k"><h3>IN WAHRHEIT</h3><p id="s06-p2">GEWALT →<br>MEHR GEWALT<br>RACHE ↻</p></div>
      <div id="s06-w" class="abs">🛡 SICHERHEITSFIRMEN<br>WAFFENHÄNDLER ↑</div>''',
'''      const sv = document.querySelector("#s06-svg");
      night(sv, "s06-n", "#0c0f1e", "#1c1626", null);
      const im = at("L13", "Im"), wa = at("L14", "Wahrheit"), ra = at("L14", "Rache"), l15 = line("L15")[0], si = at("L15", "Sicherheitsfirmen");
      tl.fromTo("#s06-k1", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, im - 0.1);
      tl.fromTo("#s06-k2", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, wa - 0.2);
      tl.to("#s06-k1", { opacity: 0.35, duration: 0.3 }, wa);
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
      <div id="s08-b1" class="s08-b">EINSCHLIESSEN</div><div id="s08-b2" class="s08-b">RAUSGEHEN</div>
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
''' + RED + '''      const du = at("L18", "du?"), ei = at("L18", "einschließen"), ra = at("L18", "rausgehen"), ko = at("L18", "Kommentare"), l19 = line("L19")[0], fo = at("L19", "folg"), si = at("L19", "Sirene");
      tl.fromTo(M.g, { opacity: 0, x: 380 }, { opacity: 1, x: 470, duration: 1.2, ease: "power2.out" }, du);
      tl.to(beam, { opacity: 0.35, duration: 0.2, repeat: 3, yoyo: true }, du + 1.0);
      tl.fromTo("#s08-b1", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, ei - 0.15);
      tl.fromTo("#s08-b2", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, ra - 0.15);
      tl.to(".s08-b", { opacity: 0, y: 40, duration: 0.25 }, l19 - 0.2);
      tl.fromTo("#s08-f", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, fo - 0.1);
      tl.to("#s08-f", { scale: 1.07, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.35, duration: 0.25, repeat: 9, yoyo: true, ease: "sine.inOut" }, si - 0.2);
      tl.to(M.mask, { scale: 1.12, svgOrigin: "0 -345", duration: 0.3, yoyo: true, repeat: 3 }, si);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
