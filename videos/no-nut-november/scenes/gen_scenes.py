#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „No Nut November“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
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
    .cd s { position: absolute; left: 60px; right: 60px; top: 62px; height: 10px; border-radius: 5px; background: #ff3b55; transform: scaleX(0); transform-origin: 0 50%; }
    .bdg { position: absolute; left: 190px; width: 700px; height: 92px; border-radius: 46px; background: rgba(12,40,30,.92); border: 4px solid #39e27a; color: #fff;
      font: 800 46px/84px Inter, sans-serif; text-align: center; opacity: 0; box-shadow: 0 0 34px rgba(57,226,122,.45); }
    .bdg b { color: #39e27a; }'''

S['s01'] = ('''    #s01-t { left: 0; width: 1080px; top: 250px; text-align: center; }
    #s01-t .a { font: 900 190px/0.92 Inter, sans-serif; color: #ff4fb0; letter-spacing: -.02em; text-shadow: 0 0 50px rgba(255,79,176,.95), 0 8px 30px rgba(0,0,0,.7); }
    #s01-t .b { font: 900 136px/1 Inter, sans-serif; color: #fff; text-shadow: 0 0 30px rgba(255,255,255,.35), 0 8px 30px rgba(0,0,0,.8); }
    #s01-chip { left: 0; right: 0; top: 575px; margin: 0 auto; width: fit-content; padding: 10px 26px; border-radius: 14px; background: #ff3b55; color: #fff; font: 800 38px Inter, sans-serif; letter-spacing: .1em; box-shadow: 0 0 40px rgba(255,59,85,.7); }
    #s01-tag { left: 640px; top: 640px; padding: 10px 22px; border-radius: 14px; background: rgba(255,255,255,.96); color: #22283f; font: 800 46px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    #s01-cal { left: 340px; top: 430px; width: 400px; height: 400px; border-radius: 30px; background: #fff; box-shadow: 0 0 70px rgba(57,226,122,.8); opacity: 0; text-align: center; overflow: hidden; }
    #s01-cal .h { height: 100px; background: #39b86b; color: #fff; font: 900 56px/100px Inter, sans-serif; letter-spacing: .12em; }
    #s01-cal .n { font: 900 230px/290px Inter, sans-serif; color: #22283f; }
    #s01-q { left: 0; width: 1080px; top: 800px; text-align: center; font: 900 140px Inter, sans-serif; color: #ff3b55; opacity: 0; text-shadow: 0 0 40px rgba(255,59,85,.9); }''',
SVG + '''
      <div id="s01-t" class="abs"><div class="a">NO NUT</div><div class="b">NOVEMBER</div></div>
      <div id="s01-chip" class="abs">30 TAGE · KEINE AUSNAHME</div>
      <div id="s01-tag" class="abs">Finn · 18</div>
      <div id="s01-cal" class="abs"><div class="h">DEZEMBER</div><div class="n">1</div></div>
      <div id="s01-q" class="abs">???</div>''',
'''      const sv = document.querySelector("#s01-svg"), W = el("g", {}, sv);
      const R = bedroom(W, "s01g", { w1: "#241c48", w2: "#120e28" });
      gsap.set([R.poster, R.win], { opacity: 0 });
      const F = finn(W, 540, 1130, 2.6);
      const fi = at("L2", "Finn"), l3 = line("L3")[0], de = at("L3", "Dezember"), ke = at("L3", "keiner");
      tl.fromTo(W, { scale: 1, svgOrigin: "540 1000" }, { scale: 1.08, svgOrigin: "540 1000", duration: C.__dur, ease: "none" }, 0);
      tl.fromTo("#s01-t", { scale: 1.12 }, { scale: 1, duration: 0.6, ease: "power3.out" }, 0);
      tl.fromTo("#s01-t .a", { textShadow: "0 0 50px rgba(255,79,176,.95), 0 8px 30px rgba(0,0,0,.7)" }, { textShadow: "0 0 90px rgba(255,79,176,1), 0 8px 30px rgba(0,0,0,.7)", duration: 0.5, yoyo: true, repeat: 5 }, 0.3);
      tl.to(["#s01-t", "#s01-chip"], { opacity: 0, y: -40, duration: 0.3 }, fi - 0.3);
      tl.to([R.poster, R.win], { opacity: 1, duration: 0.4 }, fi - 0.2);
      tl.fromTo("#s01-tag", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, fi);
      armsUp(tl, F, fi + 0.4, 0.3, 160);
      tl.to(F.g, { y: 1110, duration: 0.18, yoyo: true, repeat: 1 }, fi + 0.4);
      tl.to("#s01-tag", { opacity: 0, duration: 0.25 }, l3 - 0.3); armsDown(tl, F, l3 - 0.3);
      tl.fromTo("#s01-cal", { opacity: 0, scale: 0.4, rotation: -12 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.45, ease: "back.out(1.8)" }, de - 0.15);
      tl.fromTo("#s01-q", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power3.out" }, ke);
      tl.to("#s01-q", { x: 10, duration: 0.05, repeat: 7, yoyo: true }, ke + 0.25);''' + OUT)

S['s02'] = (CARD + '''
    #s02-big { left: 0; width: 1080px; top: 560px; text-align: center; font: 900 220px/1 Inter, sans-serif; color: #ffd43b; text-shadow: 0 0 60px rgba(255,212,59,.7); opacity: 0; }
    #s02-sub { left: 0; width: 1080px; top: 800px; text-align: center; font: 700 44px Inter, sans-serif; color: #fff; letter-spacing: .14em; opacity: 0; }''',
SVG + '''
      <div id="s02-c1" class="cd" style="top:540px">ALLEIN<s></s></div><div id="s02-c2" class="cd" style="top:710px">ZU ZWEIT<s></s></div><div id="s02-c3" class="cd" style="top:880px">GAR NICHT<s></s></div>
      <div id="s02-big" class="abs">2011</div><div id="s02-sub" class="abs">ALS INTERNET-WITZ</div>''',
'''      const sv = document.querySelector("#s02-svg"); sky(sv, "s02g", "#2a1f4f", "#120e28");
      const cal = el("g", {}, sv), cells = [];
      el("rect", { x: 130, y: 560, width: 820, height: 560, rx: 26, fill: "#f4f1fb" }, cal); el("rect", { x: 130, y: 560, width: 820, height: 86, rx: 26, fill: "#ff4fb0" }, cal);
      el("rect", { x: 130, y: 610, width: 820, height: 36, fill: "#ff4fb0" }, cal); txt(cal, 540, 620, "NOVEMBER", 50, "#fff");
      for (let d = 0; d < 30; d++) { const c = d % 7, r = Math.floor(d / 7), x = 150 + c * 112, y = 662 + r * 88;
        const g = el("g", {}, cal); const b = el("rect", { x, y, width: 104, height: 80, rx: 12, fill: "#e4def3" }, g); txt(g, x + 52, y + 54, String(d + 1), 36, "#4a4170");
        cells.push(b); }
      const ban = el("g", { opacity: 0 }, sv); el("circle", { cx: 540, cy: 840, r: 250, fill: "none", stroke: "#ff3b55", "stroke-width": 40 }, ban); el("line", { x1: 363, y1: 663, x2: 717, y2: 1017, stroke: "#ff3b55", "stroke-width": 40 }, ban);
      const ppl = el("g", {}, sv), rp = rng(5), crowd = [];
      for (let i = 0; i < 84; i++) { const c = i % 12, r = Math.floor(i / 12), x = 120 + c * 76 + (r % 2) * 30, y = 990 + r * 28 + rp() * 8, col = ["#ff4fb0", "#4da3ff", "#39e27a", "#ffd43b", "#1fb5a5"][i % 5];
        const g = el("g", { opacity: 0 }, ppl); el("circle", { cx: x, cy: y - 34, r: 13, fill: "#f2cba5" }, g); el("rect", { x: x - 15, y: y - 20, width: 30, height: 36, rx: 10, fill: col }, g); crowd.push(g); }
      const ga = at("L4", "ganzen"), kh = at("L4", "kein"), al = at("L5", "allein"), zw = at("L5", "zweit"), ga2 = at("L5", "gar"), l6 = line("L6")[0], wi = at("L6", "Internet"), mi = at("L6", "Millionen");
      tl.fromTo(cal, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 0.4);
      tl.to(cells, { attr: { fill: "#ff9fd4" }, duration: 0.15, stagger: 0.035 }, ga - 0.1);
      tl.fromTo(ban, { opacity: 0, scale: 1.6, svgOrigin: "540 840" }, { opacity: 1, scale: 1, svgOrigin: "540 840", duration: 0.3, ease: "power3.out" }, kh);
      tl.to([cal, ban], { opacity: 0.12, duration: 0.3 }, al - 0.35);
      [["#s02-c1", al], ["#s02-c2", zw], ["#s02-c3", ga2]].forEach(([id, t]) => { tl.fromTo(id, { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.25, ease: "back.out(2)" }, t - 0.15);
        tl.to(id + " s", { scaleX: 1, duration: 0.2 }, t + 0.25); });
      tl.to("#s02-c3", { scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }, ga2 + 0.3);
      tl.to(["#s02-c1", "#s02-c2", "#s02-c3"], { opacity: 0, duration: 0.25 }, l6 - 0.3); tl.to([cal, ban], { opacity: 0, duration: 0.25 }, l6 - 0.3);
      tl.fromTo("#s02-big", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }, l6 + 0.4);
      tl.fromTo("#s02-sub", { opacity: 0 }, { opacity: 1, duration: 0.3 }, wi - 0.1);
      tl.to("#s02-sub", { opacity: 0, duration: 0.2 }, mi - 0.3); tl.to("#s02-big", { y: -200, scale: 0.7, duration: 0.4, ease: "power2.inOut" }, mi - 0.3);
      tl.to(crowd, { opacity: 1, duration: 0.12, stagger: { each: 0.012, from: "random" } }, mi - 0.1);''' + OUT)

S['s03'] = ('''    #s03-easy { left: 610px; top: 560px; padding: 12px 26px; border-radius: 30px 30px 30px 6px; background: #fff; color: #22283f; font: 900 60px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    #s03-easy b { color: #39b86b; }''',
SVG + '''
      <div id="s03-easy" class="abs">„<b>easy</b>“</div>''',
'''      const sv = document.querySelector("#s03-svg"), W = el("g", {}, sv);
      const R = bedroom(W, "s03g", { w1: "#3a2f6e", w2: "#221a48" });
      const halo = el("ellipse", { cx: 540, cy: 0, rx: 80, ry: 20, fill: "none", stroke: "#ffd43b", "stroke-width": 10, opacity: 0 }, W);
      const glow = el("circle", { cx: 540, cy: 860, r: 260, fill: "#ffd43b", opacity: 0 }, W);
      const F = finn(W, 540, 1130, 2.6);
      gsap.set(halo, { attr: { cy: 1130 - 192 * 2.6 } });
      const P = phone(W, 260, 760, 170, "#1b1f3a"), apps = [], ra = rng(3);
      for (let i = 0; i < 9; i++) { const c = i % 3, r = Math.floor(i / 3); apps.push(el("rect", { x: 197 + c * 44, y: 610 + r * 52, width: 36, height: 36, rx: 9, fill: ["#ff4fb0", "#4da3ff", "#ffd43b", "#39e27a", "#ff7a3b", "#a06bff"][i % 6] }, P.g)); }
      const clock = el("g", { opacity: 0 }, W); el("circle", { cx: 880, cy: 905, r: 40, fill: "#ff3b55" }, clock); el("circle", { cx: 880, cy: 905, r: 30, fill: "#fff" }, clock);
      el("line", { x1: 880, y1: 905, x2: 880, y2: 885, stroke: "#22283f", "stroke-width": 5 }, clock); el("line", { x1: 880, y1: 905, x2: 895, y2: 912, stroke: "#22283f", "stroke-width": 4 }, clock);
      el("circle", { cx: 852, cy: 868, r: 12, fill: "#ff3b55" }, clock); el("circle", { cx: 908, cy: 868, r: 12, fill: "#ff3b55" }, clock);
      const ea = at("L7", "easy"), ap = at("L8", "Apps"), we = at("L8", "Wecker"), mo = at("L8", "Mönch");
      tl.fromTo(W, { scale: 1.05, svgOrigin: "540 900" }, { scale: 1, svgOrigin: "540 900", duration: C.__dur, ease: "none" }, 0);
      tl.fromTo("#s03-easy", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)" }, ea - 0.05);
      tl.to(F.mouth, { attr: { d: "M-9 -151 Q0 -141 9 -151" }, duration: 0.2 }, ea);
      tl.to("#s03-easy", { opacity: 0, duration: 0.2 }, ap - 0.5);
      tl.fromTo(P.g, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3 }, ap - 0.45);
      apps.forEach((a, i) => tl.to(a, { y: -260 - ra() * 200, x: (ra() - 0.5) * 300, rotation: (ra() - 0.5) * 120, svgOrigin: "260 700", opacity: 0, duration: 0.45, ease: "power2.in" }, ap + i * 0.05));
      tl.to(P.g, { opacity: 0, duration: 0.25 }, we - 0.2);
      tl.fromTo(clock, { opacity: 0, scale: 0.4, svgOrigin: "880 905" }, { opacity: 1, scale: 1, svgOrigin: "880 905", duration: 0.25, ease: "back.out(2)" }, we - 0.1);
      tl.to(clock, { x: 5, duration: 0.04, repeat: 11, yoyo: true }, we + 0.15);
      tl.to(glow, { opacity: 0.28, duration: 0.5 }, mo - 0.1);
      tl.fromTo(halo, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, mo - 0.1);
      tl.to(halo, { y: -8, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }, mo + 0.3);''' + OUT)

S['s04'] = ('''    #s04-pk { left: 400px; top: 470px; width: 280px; text-align: center; font: 900 76px Inter, sans-serif; color: #ffd43b; text-shadow: 0 0 40px rgba(255,212,59,.8); opacity: 0; }''',
SVG + '''
      <div id="s04-pk" class="abs">145 %</div>''',
'''      const sv = document.querySelector("#s04-svg"); sky(sv, "s04g", "#10224a", "#0a1230");
      const G = el("g", {}, sv), X = (d) => 150 + (d - 1) * (800 / 13), Y = (v) => 1060 - (v - 90) * 6.4;
      for (let v = 100; v <= 150; v += 25) el("line", { x1: 130, y1: Y(v), x2: 970, y2: Y(v), stroke: "#2f4a8a", "stroke-width": 2, "stroke-dasharray": v === 100 ? "" : "10 10" }, G);
      txt(G, 92, Y(100) + 10, "100 %", 28, "#8fb3ff"); txt(G, 92, Y(150) + 10, "150 %", 28, "#8fb3ff");
      for (let d = 1; d <= 14; d += 1) txt(G, X(d), 1110, String(d), 28, d === 7 ? "#ffd43b" : "#8fb3ff");
      txt(G, 540, 1150, "TAG IM NOVEMBER", 28, "#8fb3ff", { "letter-spacing": "4" });
      const up = [[1, 100], [2, 102], [3, 104], [4, 107], [5, 112], [6, 122], [7, 145.7]], dn = [[7, 145.7], [8, 101], [9, 99], [10, 101], [11, 100], [12, 99], [13, 101], [14, 100]];
      const pth = (a) => "M" + a.map(([d, v]) => `${X(d).toFixed(1)} ${Y(v).toFixed(1)}`).join(" L");
      const pu = el("path", { d: pth(up), stroke: "#ffd43b", "stroke-width": 12, fill: "none", "stroke-linejoin": "round", "stroke-linecap": "round", "stroke-dasharray": 2000, "stroke-dashoffset": 2000 }, G);
      const pd = el("path", { d: pth(dn), stroke: "#ff3b55", "stroke-width": 12, fill: "none", "stroke-linejoin": "round", "stroke-linecap": "round", "stroke-dasharray": 2000, "stroke-dashoffset": 2000 }, G);
      const dot = el("circle", { cx: X(7), cy: Y(145.7), r: 20, fill: "#ffd43b", opacity: 0 }, G);
      const glow = el("circle", { cx: 860, cy: 960, r: 170, fill: "#ffd43b", opacity: 0 }, sv);
      const F = finn(sv, 860, 1060, 1.5); gsap.set(F.g, { opacity: 0 });
      const st = at("L10", "steigt"), pc = at("L10", "Prozent"), l11 = line("L11")[0], gl = at("L11", "Gladiator"), ha = at("L12", "Haken"), we = at("L12", "wieder");
      tl.fromTo(G, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 1.0);
      tl.to(pu, { attr: { "stroke-dashoffset": 0 }, duration: pc - st + 0.3, ease: "power2.in" }, st - 0.2);
      tl.fromTo(dot, { opacity: 0, scale: 0, svgOrigin: `${X(7)} ${Y(145.7)}` }, { opacity: 1, scale: 1, svgOrigin: `${X(7)} ${Y(145.7)}`, duration: 0.3, ease: "back.out(3)" }, pc - 0.4);
      tl.fromTo("#s04-pk", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3 }, pc - 0.4);
      gsap.set("#s04-pk", { left: X(7) - 140, top: Y(145.7) - 120 });
      tl.fromTo(F.g, { opacity: 0 }, { opacity: 1, duration: 0.3 }, l11 - 0.1);
      armsUp(tl, F, gl - 0.1, 0.25, 160); tl.to(glow, { opacity: 0.35, duration: 0.3 }, gl - 0.1);
      tl.to(F.g, { scale: 1.75, duration: 0.3, ease: "back.out(2)" }, gl - 0.1);
      tl.to(sv, { x: 6, duration: 0.04, repeat: 5, yoyo: true }, gl);
      tl.to(pd, { attr: { "stroke-dashoffset": 0 }, duration: 1.4, ease: "power1.out" }, we - 0.3);
      tl.to(glow, { opacity: 0, duration: 0.4 }, we - 0.2); armsDown(tl, F, we - 0.1, 0.4); tl.to(F.g, { scale: 1.5, duration: 0.4 }, we - 0.1);
      tl.to("#s04-pk", { color: "#9aa3c0", textShadow: "0 0 0 rgba(0,0,0,0)", duration: 0.4 }, we);''' + OUT)

S['s05'] = ('''    #s05-fyp { left: 330px; top: 470px; width: 420px; height: 640px; border-radius: 50px; background: #0b0d1c; border: 10px solid #3a3f5c; overflow: hidden; opacity: 0; box-shadow: 0 0 80px rgba(77,163,255,.5); }
    #s05-fyp .h { margin-top: 30px; text-align: center; color: #fff; font: 800 34px Inter, sans-serif; }
    #s05-fyp .h u { text-decoration: none; border-bottom: 4px solid #fff; padding-bottom: 4px; }
    #s05-fyp .f { position: absolute; left: 30px; right: 30px; top: 110px; bottom: 30px; border-radius: 24px; background: linear-gradient(160deg, #ff4fb0, #6b3bff); filter: blur(14px); }
    #s05-fyp .e { position: absolute; left: 0; right: 0; top: 230px; text-align: center; font: 900 120px Inter, sans-serif; color: #fff; text-shadow: 0 0 30px rgba(0,0,0,.6); }''',
SVG + '''
      <div id="s05-fyp" class="abs"><div class="h"><u>Für dich</u></div><div class="f"></div><div class="e">?!</div></div>''',
'''      const sv = document.querySelector("#s05-svg"), W = el("g", {}, sv);
      const R = bedroom(W, "s05g", { w1: "#1a1436", w2: "#0b0920", floor: "#1c1630" });
      // Finn liegt im Bett, Handy leuchtet
      const lie = el("g", {}, W); el("circle", { cx: 120, cy: 870, r: 34, fill: "#f2cba5" }, lie); el("path", { d: "M86 866 Q90 830 124 834 Q150 838 154 862 Q130 850 86 866Z", fill: "#6b4423" }, lie);
      el("rect", { x: 140, y: 862, width: 330, height: 110, rx: 40, fill: "#5865c8" }, lie);
      const ph = phone(lie, 190, 800, 46, "#9fd0ff"); gsap.set(ph.g, { rotation: -20, svgOrigin: "190 800" });
      const faceGlow = el("circle", { cx: 150, cy: 830, r: 120, fill: "#4da3ff", opacity: 0.25 }, lie);
      const red = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#c4123a", opacity: 0 }, sv);
      // stehender Finn (Strategie)
      const F = finn(W, 560, 1130, 2.5); gsap.set(F.g, { opacity: 0 });
      const big = phone(W, 900, 760, 140, "#4da3ff"); gsap.set(big.g, { opacity: 0 });
      const shower = el("g", { opacity: 0 }, W); el("rect", { x: 520, y: 420, width: 16, height: 120, fill: "#b9c3d9" }, shower); el("path", { d: "M470 540 H600 L580 580 H490Z", fill: "#cfd8ea" }, shower);
      const drops = [], rd = rng(9); for (let i = 0; i < 40; i++) { const dx = 490 + rd() * 100; drops.push(el("line", { x1: dx, y1: 590 + rd() * 40, x2: dx, y2: 625 + rd() * 40, stroke: "#9fd8ff", "stroke-width": 5, "stroke-linecap": "round", opacity: 0 }, W)); }
      const blue = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#2b7cff", opacity: 0 }, sv);
      const sweat = [el("circle", { cx: 610, cy: 680, r: 9, fill: "#9fd8ff", opacity: 0 }, W), el("circle", { cx: 470, cy: 700, r: 8, fill: "#9fd8ff", opacity: 0 }, W)];
      const na = at("L14", "Nachts"), l14b = at("L14", "Handy"), fu = at("L14", "Für"), ve = at("L14", "verdächtig"), l15 = line("L15")[0], ha = at("L15", "Handy"), l16 = line("L16")[0], ka = at("L17", "kalt"), wi = at("L17", "wirklich"), ex = at("L17", "extrem");
      tl.fromTo(W, { scale: 1.25, svgOrigin: "200 880" }, { scale: 1.1, svgOrigin: "200 880", duration: l15, ease: "none" }, 0);
      tl.to(faceGlow, { opacity: 0.45, duration: 0.3, yoyo: true, repeat: 9 }, 0.5);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.22, duration: 0.45, yoyo: true, repeat: 7, ease: "sine.inOut" }, na - 0.1);
      tl.fromTo("#s05-fyp", { opacity: 0, scale: 0.6, y: 120 }, { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(1.6)" }, fu - 0.35);
      tl.fromTo("#s05-fyp .e", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(3)" }, ve);
      tl.to("#s05-fyp", { rotation: 3, duration: 0.06, repeat: 7, yoyo: true }, ve + 0.2);
      tl.to("#s05-fyp", { x: 900, rotation: 40, opacity: 0, duration: 0.55, ease: "power2.in" }, ha);
      tl.set(lie, { opacity: 0 }, l16 - 0.05); tl.set(W, { scale: 1, svgOrigin: "540 900" }, l16 - 0.05); tl.set(F.g, { opacity: 1 }, l16 - 0.05);
      tl.set(red, { opacity: 0 }, l15);
      // Hampelmann
      for (let k = 0; k < 4; k++) { const t = l16 + k * 0.42; armsUp(tl, F, t, 0.2, 165); armsDown(tl, F, t + 0.21, 0.2); tl.to(F.g, { y: 1095, duration: 0.2, yoyo: true, repeat: 1 }, t); }
      tl.to(sweat, { opacity: 1, y: 40, duration: 0.5, stagger: 0.2 }, l16 + 0.6);
      tl.to(sweat, { opacity: 0, duration: 0.2 }, ka - 0.3);
      tl.fromTo(shower, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.3 }, ka - 0.25);
      drops.forEach((d, i) => tl.fromTo(d, { opacity: 0.9, y: 0 }, { y: 520, opacity: 0.9, duration: 0.5, repeat: 6, ease: "none", immediateRender: false }, ka + (i % 10) * 0.05));
      tl.to(blue, { opacity: 0.25, duration: 0.3 }, ka);
      tl.to(F.g, { x: 568, duration: 0.04, repeat: 40, yoyo: true }, ka + 0.2);
      tl.to(F.mouth, { attr: { d: "M-8 -149 L-4 -152 L0 -149 L4 -152 L8 -149" }, duration: 0.1 }, ka + 0.2);''' + OUT)

S['s06'] = ('''    #s06-board { left: 120px; top: 560px; width: 840px; height: 540px; border-radius: 30px; background: #f6f3ea; box-shadow: 0 24px 60px rgba(0,0,0,.45); opacity: 0; }
    #s06-board .h { height: 96px; border-radius: 30px 30px 0 0; background: #4da3ff; color: #fff; font: 900 50px/96px Inter, sans-serif; text-align: center; letter-spacing: .1em; }
    .s06-r { position: absolute; left: 50px; right: 50px; height: 120px; border-bottom: 3px dashed #d3cdbd; font: 800 56px/120px Inter, sans-serif; color: #22283f; opacity: 0; }
    .s06-r i { position: absolute; right: 10px; top: 14px; width: 92px; height: 92px; border-radius: 50%; background: #ff3b55; color: #fff; font: 900 64px/92px Inter, sans-serif; text-align: center; font-style: normal; opacity: 0; }
    #s06-ok { left: 140px; top: 540px; width: 800px; height: 520px; border-radius: 34px; background: rgba(10,40,28,.95); border: 6px solid #39e27a; box-shadow: 0 0 70px rgba(57,226,122,.5); text-align: center; color: #fff; opacity: 0; }
    #s06-ok .t { margin-top: 220px; font: 900 84px/1.05 Inter, sans-serif; } #s06-ok .t b { color: #39e27a; }''',
'''      <div id="s06-board" class="abs"><div class="h">MYTHEN-CHECK</div>
        <div id="s06-r1" class="s06-r" style="top:110px">Superkräfte<i>✕</i></div><div id="s06-r2" class="s06-r" style="top:230px">Mehr Bart<i>✕</i></div><div id="s06-r3" class="s06-r" style="top:350px;border:0">Magische Aura<i>✕</i></div></div>
      <div id="s06-ok" class="abs"><svg width="160" height="160" viewBox="0 0 160 160" style="position:absolute;left:320px;top:40px"><circle cx="80" cy="80" r="76" fill="#39e27a"/><rect x="66" y="30" width="28" height="100" rx="6" fill="#fff"/><rect x="30" y="66" width="100" height="28" rx="6" fill="#fff"/></svg>
        <div class="t"><b>normal</b><br>und <b>gesund</b></div></div>''',
'''      const st6 = document.querySelector("#s06-stage"), sv6 = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st6.insertBefore(sv6, st6.firstChild); sky(sv6, "s06g", "#16305e", "#0c1a3a");
      const w = (i) => at("L19", i), l20 = line("L20")[0], no = at("L20", "normal");
      tl.fromTo("#s06-board", { opacity: 0, y: 80, rotation: -3 }, { opacity: 1, y: 0, rotation: -1, duration: 0.5, ease: "back.out(1.6)" }, 1.2);
      [["#s06-r1", 0, 1], ["#s06-r2", 2, 4], ["#s06-r3", 5, 7]].forEach(([id, a, b]) => { tl.fromTo(id, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.25 }, w(a) - 0.1);
        tl.fromTo(id + " i", { opacity: 0, scale: 2.2, rotation: -30 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.22, ease: "power3.out" }, w(b) - 0.05);
        tl.to("#s06-board", { x: 8, duration: 0.04, repeat: 3, yoyo: true }, w(b) + 0.1); });
      tl.to("#s06-board", { opacity: 0, y: -60, duration: 0.3 }, l20 - 0.3);
      tl.fromTo("#s06-ok", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, no - 0.4);''' + OUT)

S['s07'] = (CARD + '''
    #s07-cal { left: 400px; top: 560px; width: 420px; height: 420px; border-radius: 32px; background: #fff; box-shadow: 0 0 80px rgba(57,226,122,.8); opacity: 0; text-align: center; overflow: hidden; }
    #s07-cal .h { height: 104px; background: #39b86b; color: #fff; font: 900 56px/104px Inter, sans-serif; letter-spacing: .12em; }
    #s07-cal .n { font: 900 240px/300px Inter, sans-serif; color: #22283f; }
    #s07-dz { left: 0; width: 1080px; top: 470px; text-align: center; font: 900 150px/1 Inter, sans-serif; color: #ffd43b; text-shadow: 0 0 60px rgba(255,212,59,.8); opacity: 0; }''',
SVG + '''
      <div id="s07-cal" class="abs"><div class="h">DEZEMBER</div><div class="n">1</div></div>
      <div id="s07-b1" class="bdg" style="top:440px"><b>✓</b> Impulse im Griff</div><div id="s07-b2" class="bdg" style="top:550px"><b>✓</b> Sport &amp; früher schlafen</div><div id="s07-b3" class="bdg" style="top:660px"><b>✓</b> Weniger Handy</div>
      <div id="s07-dz" class="abs">30 / 30</div>''',
'''      const sv = document.querySelector("#s07-svg"), W = el("g", {}, sv);
      const R = bedroom(W, "s07g", { w1: "#3b2f75", w2: "#241b50" });
      const glow = el("circle", { cx: 560, cy: 880, r: 300, fill: "#39e27a", opacity: 0 }, W);
      gsap.set([R.poster, R.win], { opacity: 0.35 });
      const F = finn(W, 560, 1130, 2.1);
      const cf = el("g", { "data-layout-allow-overlap": "" }, sv), rc = rng(12), conf = [];
      for (let i = 0; i < 70; i++) conf.push(el("rect", { x: 540, y: 700, width: 14, height: 22, rx: 3, fill: ["#ff4fb0", "#ffd43b", "#39e27a", "#4da3ff", "#fff"][i % 5], opacity: 0 }, cf));
      const spot = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#000", opacity: 0 }, sv);
      const de = at("L21", "Dezember"), ge = at("L21", "geschafft"), l22 = line("L22")[0], im = at("L23", "Impulse"), gw = at("L24", "Gewohnheiten"), wn = at("L24", "weniger"), l25 = line("L25")[0], dr = at("L26", "dreißig"), al = at("L26", "alles");
      tl.fromTo("#s07-cal", { opacity: 0, rotationX: 90, y: -60 }, { opacity: 1, rotationX: 0, y: 0, duration: 0.5, ease: "back.out(1.6)" }, de - 0.2);
      armsUp(tl, F, ge - 0.05, 0.25, 160); tl.to(glow, { opacity: 0.3, duration: 0.3 }, ge);
      tl.to(F.mouth, { attr: { d: "M-9 -151 Q0 -140 9 -151" }, duration: 0.2 }, ge);
      for (let k = 0; k < 3; k++) tl.to(F.g, { y: 1100, duration: 0.16, yoyo: true, repeat: 1 }, ge + k * 0.34);
      conf.forEach((c, i) => { const a = rc() * Math.PI * 2, d = 250 + rc() * 380;
        tl.fromTo(c, { opacity: 1, x: 0, y: 0, rotation: 0 }, { x: Math.cos(a) * d, y: Math.sin(a) * d * 0.7 + 380, rotation: rc() * 720, svgOrigin: "547 711", duration: 1.6, ease: "power2.out", immediateRender: false }, ge);
        tl.to(c, { opacity: 0, duration: 0.3 }, ge + 1.4); });
      tl.to("#s07-cal", { opacity: 0, scale: 0.6, duration: 0.3 }, l22 - 0.1); armsDown(tl, F, l22);
      [["#s07-b1", im], ["#s07-b2", gw], ["#s07-b3", wn]].forEach(([id, t]) => tl.fromTo(id, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, t - 0.15));
      tl.to(["#s07-b1", "#s07-b2", "#s07-b3"], { opacity: 0, y: -30, duration: 0.3 }, l25 - 0.3);
      tl.to(spot, { opacity: 0.55, duration: 0.6 }, l25); tl.to(glow, { opacity: 0, duration: 0.4 }, l25);
      tl.fromTo("#s07-dz", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, dr - 0.1);
      armsUp(tl, F, al - 0.05, 0.25, 160); tl.to(glow, { opacity: 0.4, duration: 0.2 }, al); tl.to(spot, { opacity: 0.2, duration: 0.3 }, al);
      tl.to("#s07-dz", { scale: 1.12, duration: 0.2, yoyo: true, repeat: 1 }, al);''' + OUT)

S['s08'] = ('''    #s08-t { left: 0; width: 1080px; top: 440px; text-align: center; color: #fff; font: 900 120px/1 Inter, sans-serif; text-shadow: 0 0 40px rgba(255,79,176,.6); opacity: 0; }
    #s08-t small { display: block; margin-top: 20px; font: 800 44px Inter, sans-serif; color: #ff8fd0; letter-spacing: .2em; }
    .s08-b { position: absolute; top: 760px; width: 420px; height: 150px; border-radius: 30px; text-align: center; color: #fff; font: 900 60px/150px Inter, sans-serif; opacity: 0; }
    #s08-y { left: 70px; background: #1fa65a; box-shadow: 0 0 50px rgba(57,226,122,.6); } #s08-n { left: 590px; background: #d32a45; box-shadow: 0 0 50px rgba(255,59,85,.6); }''',
'''      <div id="s08-t" class="abs">Bist du dabei?<small>START: 1. NOVEMBER</small></div>
      <div id="s08-y" class="s08-b">DABEI</div><div id="s08-n" class="s08-b">TAG 1 RAUS</div>''',
'''      const st8 = document.querySelector("#s08-stage"), sv8 = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st8.insertBefore(sv8, st8.firstChild); sky(sv8, "s08g", "#2a1f4f", "#0f0b22");
      const da = at("L27", "Dabei"), ta = at("L27", "Tag");
      tl.fromTo("#s08-t", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.1);
      tl.fromTo("#s08-y", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, da - 0.1);
      tl.fromTo("#s08-n", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, ta - 0.1);
      tl.to(["#s08-y", "#s08-n"], { scale: 1.06, duration: 0.35, yoyo: true, repeat: 9, ease: "sine.inOut", stagger: 0.35 }, ta + 0.4);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
