#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s15 für „Die Einzige, die sieht – Part 2“ (hier ändern und neu erzeugen)."""
from pathlib import Path

HEAD = '''<template>
  <style>
    /*__COMMON_CSS__*/
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .panel { position: absolute; border-radius: 24px; background: rgba(13,16,38,.94); text-align: center; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; }
    .bub { position: absolute; border-radius: 26px; background: #f3f1ea; color: #161a36; font-family: "Inter", sans-serif;
      font-weight: 900; text-align: center; padding: 22px 26px; font-size: 40px; line-height: 1.1; opacity: 0; }
    .rule { position: absolute; left: 0; width: 1080px; top: 440px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900;
      font-size: 120px; color: #ffd43b; text-shadow: 0 0 40px rgba(255,212,59,.5), 0 8px 0 rgba(0,0,0,.5); opacity: 0; }
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
      const sv = document.querySelector("#@@ID@@-svg");
@@JS@@
      window.__timelines["@@ID@@"] = tl;
    })();
  </script>
</template>
'''
OUT = '\n      tl.to("#@@ID@@-stage > *", { opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }, C.__dur - 0.18);'
SVG = '      <svg id="@@ID@@-svg" class="full" viewBox="0 0 1080 1920"></svg>'
S = {}

# ---------- s01 Hook: Eilmeldung, jemand hinter Sina, Story-Start (Kinobalken, Titel, Iris) ----------
S['s01'] = ('''    #s01-news { left: 60px; top: 690px; width: 960px; height: 420px; border: 5px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.45); overflow: hidden; text-align: left; }
    #s01-news .bar { height: 84px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 34px; font-size: 44px; letter-spacing: .06em; }
    #s01-news .hl { padding: 22px 40px 0; font-size: 84px; line-height: 1.04; letter-spacing: -.015em; }
    #s01-news .hl em { font-style: normal; color: #ff3b55; text-shadow: 0 0 26px rgba(255,59,85,.6); }
    #s01-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 40%, rgba(160,0,20,.75) 100%); opacity: 0; }
    #s01-dark { background: #05060f; opacity: 0; }
    #s01-title { left: 0; width: 1080px; top: 470px; height: 400px; overflow: hidden; text-align: center; opacity: 0; }
    #s01-title .k { margin-top: 20px; font-family: "Space Mono", monospace; font-weight: 700; font-size: 54px; letter-spacing: .3em; color: #ff4fb0; text-shadow: 0 0 26px rgba(255,79,176,.7); }
    #s01-title .t { margin-top: 18px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 116px; line-height: 1; color: #fff; text-shadow: 0 0 40px rgba(255,255,255,.3), 0 8px 0 rgba(0,0,0,.5); }
    #s01-sweep { position: absolute; left: -300px; top: -40px; width: 200px; height: 480px; transform: skewX(-20deg);
      background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.45), rgba(255,255,255,0)); }
    .s01-bar { position: absolute; left: 0; width: 1080px; height: 150px; background: #000; }''',
SVG + '''
      <div id="s01-vig" class="full"></div>
      <div id="s01-news" class="panel"><div class="bar">● EILMELDUNG · PART 2</div><div class="hl">JEMAND STEHT <em>HINTER</em> SINA</div></div>
      <div id="s01-dark" class="full"></div>
      <div id="s01-title" class="abs"><div class="k">PART 2</div><div class="t">DIE EINZIGE,<br>DIE SIEHT</div><div id="s01-sweep"></div></div>
      <div id="s01-bar1" class="s01-bar" style="top:0;transform:translateY(-150px)"></div><div id="s01-bar2" class="s01-bar" style="top:1770px;transform:translateY(150px)"></div>
      <svg id="s01-iris" class="full" viewBox="0 0 1080 1920"><circle id="s01-ir" cx="540" cy="760" r="2600" fill="none" stroke="#000" stroke-width="2400"/></svg>''',
'''      const fig = el("g", {}, sv);
      const H = person(fig, "s01-h", 440, 600, 1.4, { skin: "#020309", shirt: "#020309", hair: "#020309", pants: "#020309" });
      gsap.set([H.eyes, H.mouth], { opacity: 0 }); gsap.set(H.g, { opacity: 0 }); H.g.style.filter = "drop-shadow(0 0 22px rgba(255,59,85,.9))";
      const glint = el("g", { opacity: 0 }, fig);
      el("circle", { cx: 418, cy: 522, r: 6, fill: "#ff3b55" }, glint); el("circle", { cx: 462, cy: 522, r: 6, fill: "#ff3b55" }, glint);
      const P = person(fig, "s01-p", 600, 640, 1.2, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      P.g.style.filter = "drop-shadow(0 0 24px rgba(255,79,176,.6))";
      const l2 = line("L2")[0], je = at("L2", "jemand"), hi = at("L2", "hinter"), l3 = line("L3")[0], ni = at("L3", "niemals");
      tl.fromTo("#s01-news", { scale: 1.06 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);
      tl.to("#s01-news", { x: 8, duration: 0.04, repeat: 5, yoyo: true }, 0.9);
      tl.to(P.eyes, { x: -6, duration: 0.25, repeat: 3, yoyo: true }, 1.4);
      tl.to("#s01-news", { opacity: 0, y: 160, duration: 0.3, ease: "power3.in" }, l2 - 0.35);
      tl.to(fig, { y: 120, duration: 0.5, ease: "power3.out" }, l2 - 0.1);
      tl.to(H.g, { opacity: 1, duration: 0.15 }, je - 0.05);
      tl.to(glint, { opacity: 1, duration: 0.1 }, hi);
      tl.fromTo("#s01-vig", { opacity: 0 }, { opacity: 1, duration: 0.12 }, je);
      tl.to(P.eyes, { scale: 1.4, svgOrigin: "0 -56", duration: 0.12 }, hi);
      tl.to(P.g, { x: 610, duration: 0.04, repeat: 5, yoyo: true }, je);
      tl.to("#s01-dark", { opacity: 0.88, duration: 0.4 }, l3 - 0.1);
      tl.to(fig, { opacity: 0, duration: 0.35 }, l3 - 0.1);
      tl.fromTo("#s01-bar1", { y: -150 }, { y: 0, duration: 0.5, ease: "power3.out" }, l3 - 0.1);
      tl.fromTo("#s01-bar2", { y: 150 }, { y: 0, duration: 0.5, ease: "power3.out" }, l3 - 0.1);
      tl.fromTo("#s01-title", { opacity: 0, scale: 1.4, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, l3 + 0.1);
      tl.fromTo("#s01-sweep", { x: 0 }, { x: 1700, duration: 0.9, ease: "power2.inOut" }, l3 + 0.6);
      tl.to("#s01-title .t", { color: "#ff3b55", duration: 0.05, repeat: 5, yoyo: true }, ni);
      tl.to("#s01-title", { x: 10, duration: 0.04, repeat: 7, yoyo: true }, ni);
      tl.to("#s01-ir", { attr: { r: 1200 }, duration: 0.45, ease: "power2.in" }, C.__dur - 0.5);''' + OUT.replace('#@@ID@@-stage > *', '#@@ID@@-stage > *:not(#s01-iris)'))

# ---------- s02 Die Hand gehört Spartakus ----------
S['s02'] = ('''    #s02-name { left: 640px; top: 450px; width: 380px; height: 120px; border: 4px solid #4da3ff; box-shadow: 0 0 30px rgba(77,163,255,.4); opacity: 0; }
    #s02-name .a { margin-top: 12px; font-size: 48px; color: #4da3ff; } #s02-name .b { font-size: 30px; color: #dfe2f5; letter-spacing: .14em; font-family: "Space Mono", monospace; }
    #s02-b { left: 70px; top: 430px; width: 560px; }''',
SVG + '''
      <svg class="full" viewBox="0 0 1080 1920"><circle id="s02-ir" cx="540" cy="760" r="1200" fill="none" stroke="#000" stroke-width="2400"/></svg>
      <div id="s02-name" class="panel"><div class="a">SPARTAKUS</div><div class="b">NACHBAR</div></div>
      <div id="s02-b" class="bub">„ICH WEISS, DASS DU SIEHST. DU STOLPERST NIE.“</div>''',
'''      tl.fromTo("#s02-ir", { attr: { r: 1200 } }, { attr: { r: 2600 }, duration: 0.6, ease: "power2.out" }, 0);
      const bg = el("rect", { x: 0, y: 400, width: 1080, height: 740, fill: "#0b0d20" }, sv);
      el("rect", { x: 0, y: 1060, width: 1080, height: 80, fill: "#151833" }, sv);
      el("rect", { x: 760, y: 490, width: 260, height: 570, rx: 6, fill: "#6b3f1d" }, sv);
      const S2 = person(sv, "s02-s", 300, 700, 1.3, { blind: true, shades: true, shirt: "#39a06a", hair: "#2a2f55", arms: [12, -60] });
      const sil = el("g", {}, sv);
      const H = person(sil, "s02-h", 300, 700, 1.3, { skin: "#020309", shirt: "#020309", hair: "#020309", pants: "#020309", arms: [12, -60] });
      gsap.set([H.eyes, H.mouth], { opacity: 0 });
      const P = person(sv, "s02-p", 470, 770, 1.1, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      gsap.set(P.eyes, { scale: 1.4, svgOrigin: "0 -56" });
      const hand = el("ellipse", { cx: 480, cy: 736, rx: 46, ry: 34, fill: "#020309" }, sv);
      const sp = at("L4", "Spartakus"), l5 = line("L5")[0], ni = at("L5", "nie");
      tl.to(bg, { fill: "#1c2250", duration: 0.4 }, sp - 0.2);
      tl.to(sil, { opacity: 0, duration: 0.4 }, sp - 0.2);
      tl.to(hand, { attr: { cx: 420, cy: 800 }, fill: "#f2c9a5", opacity: 0, duration: 0.4 }, sp);
      tl.fromTo("#s02-name", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)" }, sp);
      tl.to(P.g, { x: 620, duration: 0.4, ease: "power2.out" }, sp + 0.1);
      tl.to("#s02-name", { opacity: 0, duration: 0.2 }, l5 - 0.2);
      tl.fromTo("#s02-b", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, l5 + 0.3);
      tl.to(P.mouth, { attr: { d: "M-10 -30 q10 -12 20 0 q-10 12 -20 0" }, duration: 0.1 }, ni);
      tl.to(P.g, { x: 630, duration: 0.04, repeat: 5, yoyo: true }, ni);''' + OUT)

# ---------- s03 Der Sammler, Flucht über den Balkon ----------
S['s03'] = ('''    #s03-lab { left: 240px; top: 440px; width: 600px; height: 100px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 58px; line-height: 90px; box-shadow: 0 0 40px rgba(255,59,85,.5); opacity: 0; }
    #s03-late { left: 300px; top: 450px; width: 480px; height: 96px; border: 5px solid #39e27a; color: #39e27a; font-size: 52px; line-height: 86px; box-shadow: 0 0 40px rgba(57,226,122,.45); opacity: 0; }''',
SVG + '''
      <div id="s03-lab" class="panel">DER SAMMLER</div><div id="s03-late" class="panel">ZU SPÄT!</div>''',
'''      const A = el("g", {}, sv);
      el("rect", { x: 300, y: 560, width: 480, height: 570, rx: 10, fill: "#3a2614" }, A);
      const door = el("rect", { x: 330, y: 590, width: 420, height: 540, rx: 6, fill: "#7a4b22" }, A);
      el("circle", { cx: 700, cy: 860, r: 18, fill: "#ffd43b" }, A);
      const pg = el("circle", { cx: 540, cy: 700, r: 70, fill: "#ffd43b", opacity: 0.6 }, A);
      el("circle", { cx: 540, cy: 700, r: 26, fill: "#f3f1ea" }, A);
      const pu = el("circle", { cx: 540, cy: 700, r: 11, fill: "#161a36" }, A);
      const key = el("g", { opacity: 0 }, A);
      el("rect", { x: 690, y: 896, width: 70, height: 10, rx: 4, fill: "#ffd43b" }, key);
      el("circle", { cx: 774, cy: 901, r: 22, fill: "none", stroke: "#ffd43b", "stroke-width": 10 }, key);
      const B = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#141838" }, B);
      el("circle", { cx: 900, cy: 520, r: 50, fill: "#f3f1ea", opacity: 0.8 }, B);
      const win = el("rect", { x: 80, y: 600, width: 260, height: 380, rx: 8, fill: "#10142f" }, B);
      el("rect", { x: 0, y: 980, width: 1080, height: 26, fill: "#3a3f7a" }, B);
      for (let i = 0; i < 22; i++) el("rect", { x: 10 + i * 50, y: 880, width: 10, height: 100, fill: "#3a3f7a" }, B);
      el("rect", { x: 0, y: 872, width: 1080, height: 16, rx: 6, fill: "#3a3f7a" }, B);
      const run = el("g", {}, B);
      const P = person(run, "s03-p", 480, 700, 0.9, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0", arms: [40, -40] });
      const Sp = person(run, "s03-s", 640, 690, 0.95, { shades: true, blind: true, shirt: "#39a06a", hair: "#2a2f55", arms: [40, -40] });
      const beam = el("path", { d: "M210 760 L1100 560 L1100 980Z", fill: "#ffe680", opacity: 0 }, B);
      const debris = [0, 1, 2, 3, 4, 5].map((i) => el("rect", { x: 200, y: 760, width: 26, height: 12, rx: 3, fill: "#a86b2c", opacity: 0 }, B));
      const sa = at("L6", "sammelt"), l7 = line("L7")[0], ba = at("L7", "Balkon"), sp = at("L29", "splittert"), li = at("L29", "Lichtkegel"), zs = at("L29", "zu");
      tl.fromTo(A, { opacity: 0, scale: 0.94, svgOrigin: "540 840" }, { opacity: 1, scale: 1, svgOrigin: "540 840", duration: 0.4, ease: "expo.out" }, 0.05);
      tl.to(pg, { attr: { r: 110 }, opacity: 0.9, duration: 0.4, repeat: 5, yoyo: true }, 0.4);
      tl.to(pu, { attr: { cx: 552 }, duration: 0.3, repeat: 3, yoyo: true }, 1.0);
      tl.fromTo("#s03-lab", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, sa - 0.1);
      tl.to("#s03-lab", { opacity: 0, duration: 0.2 }, l7 - 0.15);
      tl.fromTo(key, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, l7);
      tl.to(key, { scaleY: -1, svgOrigin: "700 901", duration: 0.25 }, l7 + 0.5);
      tl.to(door, { x: 6, duration: 0.04, repeat: 5, yoyo: true }, l7 + 0.5);
      tl.to(A, { opacity: 0, duration: 0.2 }, ba - 0.6);
      tl.to(B, { opacity: 1, duration: 0.2 }, ba - 0.6);
      tl.to(run, { x: 700, duration: 1.4, ease: "power2.in" }, ba - 0.3);
      tl.to([P.g, Sp.g], { y: "-=14", duration: 0.12, repeat: 9, yoyo: true }, ba - 0.3);
      tl.to(win, { fill: "#ffd43b", duration: 0.05 }, sp - 0.05);
      debris.forEach((d, i) => tl.fromTo(d, { opacity: 1, x: 0, y: 0, rotation: 0 }, { x: 80 + i * 60, y: -120 + i * 50, rotation: 200 + i * 40, opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, sp));
      tl.to(B, { x: 12, duration: 0.04, repeat: 5, yoyo: true }, sp);
      tl.to(beam, { opacity: 0.45, duration: 0.15 }, li - 0.1);
      tl.fromTo(beam, { rotation: -10 }, { rotation: 12, svgOrigin: "210 760", duration: 1.6, ease: "sine.inOut" }, li - 0.1);
      tl.fromTo("#s03-late", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, zs);''' + OUT)

# ---------- s04 Mann in Unterhose geht zur Arbeit ----------
S['s04'] = ('''    .stamp { position: absolute; left: 190px; top: 470px; width: 700px; height: 130px; border: 7px solid #39e27a; border-radius: 20px; color: #39e27a;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 72px; line-height: 116px; text-align: center; background: rgba(8,30,18,.85);
      box-shadow: 0 0 50px rgba(57,226,122,.5); opacity: 0; }''',
SVG + '''
      <div id="s04-st" class="stamp">SIEHT JA KEINER</div>''',
'''      [[40, 640, 200, 420], [260, 580, 220, 480], [500, 660, 180, 400], [700, 600, 200, 460], [920, 650, 160, 410]].forEach(([x, y, w, h], i) => {
        el("rect", { x, y, width: w, height: h, fill: ["#232a5a", "#2b3368", "#1f2550"][i % 3] }, sv);
        for (let r = 0; r < 4; r++) for (let c = 0; c < 2; c++) el("rect", { x: x + 30 + c * (w / 2 - 10), y: y + 40 + r * 80, width: 40, height: 44, rx: 4, fill: "#ffe9a8", opacity: 0.25 }, sv); });
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#3a3f5c" }, sv);
      const M = person(sv, "s04-m", -150, 800, 1.0, { blind: true, shirt: "#e5e9f7", hair: "#5b3a26", pants: "#f2c9a5", arms: [10, -25] });
      el("path", { d: "M-34 112 h68 v40 h-68Z", fill: "#ff4fb0" }, M.g);
      [-18, 2, 22].forEach((x) => el("path", { d: `M${x} 126 q-6 -8 0 -10 q6 2 0 10 q6 -8 0 -10`, fill: "#fff" }, M.g));
      el("path", { d: "M0 6 l-10 20 l10 60 l10 -60Z", fill: "#ff3b55" }, M.g);
      const bc = el("g", {}, M.a2); el("rect", { x: 30, y: 116, width: 70, height: 50, rx: 8, fill: "#6b3f1d" }, bc); el("rect", { x: 52, y: 106, width: 26, height: 12, rx: 4, fill: "none", stroke: "#6b3f1d", "stroke-width": 5 }, bc);
      const ex = el("text", { x: 0, y: 640, "font-family": "Inter", "font-weight": 900, "font-size": 120, fill: "#ff3b55", opacity: 0 }, sv); ex.textContent = "!";
      const un = at("L9", "Unterhose"), si = at("L9", "Sieht");
      tl.fromTo(M.g, { x: 80 }, { x: 900, duration: C.__dur, ease: "none" }, 0);
      tl.to(M.g, { y: 810, duration: 0.2, repeat: Math.floor(C.__dur / 0.2) - 1, yoyo: true }, 0);
      ex.setAttribute("x", 60 + 820 * un / C.__dur);
      tl.fromTo(ex, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, transformOrigin: "50% 100%", duration: 0.2, ease: "back.out(3)" }, un);
      tl.to(ex, { opacity: 0, duration: 0.2 }, si - 0.2);
      tl.fromTo("#s04-st", { opacity: 0, scale: 2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.25, ease: "power4.out" }, si - 0.05);''' + OUT)

# ---------- s05 Oma strickt einen 40-Meter-Schal ----------
S['s05'] = ('',
'''      <div id="s05-box" class="cbox p"><div class="lab">SCHAL</div><div id="s05-n" class="num">0 M</div></div>
''' + SVG,
'''      el("rect", { x: 140, y: 760, width: 300, height: 320, rx: 40, fill: "#6d55a8" }, sv);
      el("rect", { x: 100, y: 860, width: 80, height: 220, rx: 30, fill: "#5d4598" }, sv); el("rect", { x: 400, y: 860, width: 80, height: 220, rx: 30, fill: "#5d4598" }, sv);
      const O = person(sv, "s05-o", 290, 790, 1.0, { blind: true, shirt: "#ff8fb0", hair: "#d8dbe8", pants: "#5d4598", arms: [-40, 40] });
      el("circle", { cx: 0, cy: -118, r: 22, fill: "#d8dbe8" }, O.g);
      const scarf = el("path", { d: "M300 960 C420 1000 520 900 620 960 S780 1060 860 960 S980 820 860 760 S600 700 520 620 S700 470 880 520 S1060 640 1040 760", stroke: "#ff3b55", "stroke-width": 34, fill: "none", "stroke-linecap": "round", "stroke-dasharray": "2400", "stroke-dashoffset": "2400" }, sv);
      const stripes = el("path", { d: "M300 960 C420 1000 520 900 620 960 S780 1060 860 960 S980 820 860 760 S600 700 520 620 S700 470 880 520 S1060 640 1040 760", stroke: "#ffd43b", "stroke-width": 34, fill: "none", "stroke-dasharray": "20 40", opacity: 0 }, sv);
      const ndl = [el("path", { d: "M250 900 l60 -60", stroke: "#c9cde6", "stroke-width": 7 }, sv), el("path", { d: "M330 900 l-60 -60", stroke: "#c9cde6", "stroke-width": 7 }, sv)];
      const vi = at("L33", "vierzig");
      tl.to(ndl, { rotation: 15, svgOrigin: "290 880", duration: 0.1, repeat: Math.floor(C.__dur / 0.1) - 3, yoyo: true }, 0);
      tl.to(scarf, { attr: { "stroke-dashoffset": 0 }, duration: vi + 0.4, ease: "power1.in" }, 0.1);
      tl.to(stripes, { opacity: 0.6, duration: 0.3 }, vi);
      count(tl, "#s05-n", 0, 40, 0.2, vi + 0.3, "", " M", "power2.in");
      tl.to("#s05-box", { scale: 1.15, duration: 0.12, yoyo: true, repeat: 1 }, vi + 0.3);''' + OUT)

# ---------- s06 Supermarkt: 20 Flaschen "Milch" = Waschmittel ----------
S['s06'] = ('''    #s06-lab { left: 560px; top: 470px; width: 460px; height: 100px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 50px; line-height: 90px; box-shadow: 0 0 40px rgba(255,59,85,.5); opacity: 0; }''',
SVG + '''
      <div id="s06-lab" class="panel">WASCHMITTEL!</div>''',
'''      [600, 760, 920].forEach((y) => el("rect", { x: 560, y, width: 480, height: 18, fill: "#8fa2ff" }, sv));
      for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) el("rect", { x: 580 + c * 76, y: 500 + r * 160 + 30, width: 50, height: 70, rx: 10, fill: ["#ffd43b", "#39e27a", "#ff8a3d"][(r + c) % 3] }, sv);
      const F = person(sv, "s06-f", 200, 780, 1.0, { blind: true, shirt: "#ffd43b", hair: "#b06b3a", long: true, arms: [12, -70] });
      const cart = el("g", {}, sv);
      el("path", { d: "M300 900 h260 l-30 130 h-200Z", fill: "none", stroke: "#c9cde6", "stroke-width": 10, "stroke-linejoin": "round" }, cart);
      [340, 510].forEach((x) => el("circle", { cx: x, cy: 1060, r: 18, fill: "#c9cde6" }, cart));
      const bot = [], labs = [];
      for (let i = 0; i < 10; i++) { const x = 320 + (i % 5) * 46, y = 830 - Math.floor(i / 5) * 60;
        const b = el("g", { opacity: 0 }, cart); el("rect", { x, y, width: 38, height: 70, rx: 10, fill: "#f3f1ea" }, b); el("rect", { x: x + 10, y: y - 14, width: 18, height: 16, rx: 4, fill: "#4da3ff" }, b);
        labs.push(el("rect", { x: x + 4, y: y + 24, width: 30, height: 22, rx: 4, fill: "#4da3ff" }, b)); bot.push(b); }
      const zw = at("L10", "zwanzig"), wa = at("L10", "Waschmittel");
      bot.forEach((b, i) => tl.fromTo(b, { opacity: 0, y: -200 }, { opacity: 1, y: 0, duration: 0.25, ease: "bounce.out" }, zw - 0.3 + i * 0.1));
      tl.to(labs, { fill: "#ff3b55", duration: 0.05 }, wa);
      tl.fromTo("#s06-lab", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, wa);
      tl.to(cart, { x: 8, duration: 0.04, repeat: 5, yoyo: true }, wa);''' + OUT)

# ---------- s07 Friseur nach Gefühl: Igel ----------
S['s07'] = ('''    .stamp { position: absolute; left: 190px; top: 470px; width: 700px; height: 130px; border: 7px solid #39e27a; border-radius: 20px; color: #39e27a;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 72px; line-height: 116px; text-align: center; background: rgba(8,30,18,.85);
      box-shadow: 0 0 50px rgba(57,226,122,.5); opacity: 0; }''',
SVG + '''
      <div id="s07-st" class="stamp">SIEHT JA KEINER</div>''',
'''      el("rect", { x: 160, y: 470, width: 360, height: 300, rx: 20, fill: "#a9d2ff", opacity: 0.25 }, sv);
      el("rect", { x: 380, y: 920, width: 280, height: 40, rx: 12, fill: "#2a2f55" }, sv);
      el("rect", { x: 500, y: 960, width: 40, height: 140, fill: "#2a2f55" }, sv);
      const K = person(sv, "s07-k", 520, 760, 1.05, { shirt: "#e5e9f7", hair: "#5b3a26" });
      el("path", { d: "M-70 10 L70 10 L100 200 L-100 200Z", fill: "#e5e9f7" }, K.g);
      const spikes = el("g", {}, K.g);
      for (let i = 0; i < 11; i++) { const a = -80 + i * 16; el("path", { d: `M0 -60 L${Math.sin(a * Math.PI / 180) * 110} ${-60 - Math.cos(a * Math.PI / 180) * 110} L${Math.sin((a + 8) * Math.PI / 180) * 40} ${-60 - Math.cos((a + 8) * Math.PI / 180) * 40}Z`, fill: "#5b3a26" }, spikes); }
      gsap.set(spikes, { scale: 0, svgOrigin: "0 -60" });
      const Fr = person(sv, "s07-fr", 820, 770, 1.0, { blind: true, shirt: "#2a2f55", hair: "#161a36", arms: [12, 120] });
      const sc = el("g", {}, sv);
      el("path", { d: "M680 690 l70 30 M680 730 l70 -30", stroke: "#c9cde6", "stroke-width": 8, "stroke-linecap": "round" }, sc);
      el("circle", { cx: 674, cy: 686, r: 10, fill: "none", stroke: "#c9cde6", "stroke-width": 5 }, sc); el("circle", { cx: 674, cy: 734, r: 10, fill: "none", stroke: "#c9cde6", "stroke-width": 5 }, sc);
      const hairs = [0, 1, 2, 3, 4, 5].map((i) => el("rect", { x: 560 + i * 20, y: 650, width: 8, height: 22, rx: 3, fill: "#5b3a26", opacity: 0 }, sv));
      const sch = at("L11", "schneidet"), ig = at("L11", "Igel"), si = at("L11", 12);
      tl.to(sc, { rotation: 14, svgOrigin: "715 710", duration: 0.08, repeat: 25, yoyo: true }, sch - 0.2);
      tl.to(sc, { x: -60, y: -30, duration: 0.6, repeat: 2, yoyo: true, ease: "sine.inOut" }, sch);
      hairs.forEach((h, i) => tl.fromTo(h, { opacity: 1, y: 0 }, { opacity: 0, y: 300, rotation: 80, duration: 0.8, ease: "power1.in", immediateRender: false }, sch + i * 0.2));
      tl.to(spikes, { scale: 1, svgOrigin: "0 -60", duration: 0.3, ease: "back.out(3)" }, ig - 0.15);
      tl.to(K.mouth, { attr: { d: "M-12 -32 q12 12 24 0" }, duration: 0.1 }, ig);
      tl.fromTo("#s07-st", { opacity: 0, scale: 2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.25, ease: "power4.out" }, si - 0.05);''' + OUT)

# ---------- s08 Mann ruft seinen Hund, drei fremde kommen ----------
S['s08'] = ('',
SVG,
'''      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#3a3f5c" }, sv);
      const M = person(sv, "s08-m", 260, 800, 1.0, { blind: true, shirt: "#ff8a3d", hair: "#2a2f55", arms: [12, -130] });
      const notes = [0, 1, 2].map((i) => el("text", { x: 330 + i * 40, y: 600 - i * 30, "font-family": "Inter", "font-weight": 900, "font-size": 50, fill: "#ffd43b", opacity: 0 }, sv));
      notes.forEach((n) => (n.textContent = "♪"));
      const D = [["#a86b2c", 600, 980], ["#f3f1ea", 760, 960], ["#2a2f55", 920, 990]].map(([c, x, y], i) => { const d = dog(sv, x + 500, y, c, 0.8); return { d, x, y }; });
      const leashes = D.map((o, i) => el("path", { d: `M350 830 L${o.x + 60 - 120} ${o.y - 20}`, stroke: "#ff3b55", "stroke-width": 5, opacity: 0 }, sv));
      const hearts = [0, 1, 2].map((i) => el("text", { x: 220 + i * 70, y: 640, "font-size": 60, fill: "#ff4fb0", opacity: 0 }, sv));
      hearts.forEach((h) => (h.textContent = "♥"));
      const ru = at("L30", "ruft"), dr = at("L30", "Drei"), al = at("L30", "alle");
      notes.forEach((n, i) => tl.fromTo(n, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, repeat: 1, yoyo: true }, ru + i * 0.15));
      D.forEach((o, i) => { tl.to(o.d.g, { x: o.x - 120, duration: 0.45, ease: "power3.out" }, dr - 0.1 + i * 0.15);
        tl.to(o.d.tail, { rotation: 25, svgOrigin: "-70 -10", duration: 0.1, repeat: 13, yoyo: true }, dr + i * 0.15); });
      tl.to(leashes, { opacity: 1, duration: 0.15, stagger: 0.1 }, al - 0.1);
      hearts.forEach((h, i) => tl.fromTo(h, { opacity: 0, y: 0 }, { opacity: 1, y: -60, duration: 0.6, ease: "power2.out" }, al + i * 0.12));''' + OUT)

# ---------- s09 Park: erstes Date mit einer Mülltonne ----------
S['s09'] = ('''    #s09-lab { left: 560px; top: 470px; width: 440px; height: 100px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 50px; line-height: 90px; box-shadow: 0 0 40px rgba(255,59,85,.5); opacity: 0; }
    #s09-box { opacity: 0; }''',
'''      <div id="s09-box" class="cbox p"><div class="lab">DATE LÄUFT SEIT</div><div id="s09-n" class="num">0 MIN</div></div>
''' + SVG + '''
      <div id="s09-lab" class="panel">MÜLLTONNE</div>''',
'''      el("circle", { cx: 160, cy: 560, r: 110, fill: "#2f7a4a" }, sv); el("rect", { x: 145, y: 640, width: 30, height: 200, fill: "#6b3f1d" }, sv);
      el("rect", { x: 200, y: 880, width: 460, height: 30, rx: 10, fill: "#a86b2c" }, sv);
      el("rect", { x: 200, y: 820, width: 460, height: 22, rx: 8, fill: "#a86b2c" }, sv);
      [230, 610].forEach((x) => el("rect", { x, y: 910, width: 22, height: 130, fill: "#6b3f1d" }, sv));
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#2a5a3a" }, sv);
      const M = person(sv, "s09-m", 360, 700, 1.0, { blind: true, shirt: "#4da3ff", hair: "#e0a35a", arms: [12, -120] });
      el("rect", { x: -34, y: 118, width: 68, height: 40, rx: 14, fill: "#2a3170" }, M.g);
      const fl = el("g", {}, M.a2); el("rect", { x: 49, y: 110, width: 6, height: 60, fill: "#39e27a" }, fl); el("circle", { cx: 52, cy: 108, r: 18, fill: "#ff4fb0" }, fl);
      const bin = el("g", {}, sv);
      el("rect", { x: 560, y: 790, width: 170, height: 250, rx: 16, fill: "#2f7a4a" }, bin);
      const lid = el("rect", { x: 548, y: 770, width: 194, height: 34, rx: 10, fill: "#256a3e" }, bin);
      el("path", { d: "M600 840 v160 M645 840 v160 M690 840 v160", stroke: "#256a3e", "stroke-width": 8 }, bin);
      const hearts = [0, 1, 2, 3].map((i) => el("text", { x: 420 + i * 50, y: 640, "font-size": 56, fill: "#ff4fb0", opacity: 0 }, sv));
      hearts.forEach((h) => (h.textContent = "♥"));
      const da = at("L12", "Date"), st = at("L12", "Stunde"), mu = at("L12", "Mülltonne");
      tl.to(M.mouth, { attr: { d: "M-12 -32 q12 12 24 0" }, duration: 0.1 }, 0.3);
      hearts.forEach((h, i) => tl.fromTo(h, { opacity: 0, y: 0 }, { opacity: 1, y: -90, duration: 0.8, ease: "power1.out" }, da - 0.2 + i * 0.15));
      tl.fromTo("#s09-box", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, st - 0.6);
      count(tl, "#s09-n", 0, 60, st - 0.5, 0.8, "", " MIN", "power2.out");
      tl.to(lid, { rotation: -25, svgOrigin: "548 787", duration: 0.12, repeat: 3, yoyo: true }, mu - 0.1);
      tl.fromTo("#s09-lab", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, mu);''' + OUT)

# ---------- s10 Kino: Spartakus fängt die Tasse ohne hinzusehen ----------
S['s10'] = ('''    #s10-b { left: 60px; top: 440px; width: 420px; background: #ff4fb0; color: #fff; }''',
SVG + '''
      <div id="s10-b" class="bub">GLÜCK …?</div>''',
'''      const scr = el("rect", { x: 140, y: 440, width: 800, height: 260, rx: 10, fill: "#4da3ff", opacity: 0.18 }, sv);
      for (let r = 0; r < 2; r++) for (let c = 0; c < 7; c++) el("rect", { x: 90 + c * 130 + r * 40, y: 960 + r * 70, width: 110, height: 60, rx: 14, fill: "#8a1f35" }, sv);
      const P = person(sv, "s10-p", 300, 760, 1.0, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const Sp = person(sv, "s10-s", 720, 750, 1.05, { blind: true, shades: true, shirt: "#39a06a", hair: "#2a2f55", arms: [12, -12] });
      el("rect", { x: 830, y: 880, width: 140, height: 16, rx: 6, fill: "#6b3f1d" }, sv); el("rect", { x: 890, y: 896, width: 18, height: 140, fill: "#6b3f1d" }, sv);
      const cup = el("g", {}, sv);
      el("rect", { x: 900, y: 836, width: 40, height: 44, rx: 6, fill: "#f3f1ea" }, cup);
      el("path", { d: "M940 846 q14 0 14 12 q0 12 -14 12", stroke: "#f3f1ea", "stroke-width": 5, fill: "none" }, cup);
      const ring = el("circle", { cx: 860, cy: 960, r: 90, fill: "none", stroke: "#ffd43b", "stroke-width": 8, opacity: 0 }, sv);
      const fa = at("L14", "fällt"), fn = at("L14", "fängt"), oh = at("L14", "Ohne"), gl = at("L15", "Glück");
      tl.fromTo(scr, { attr: { opacity: 0.1 } }, { attr: { opacity: 0.3 }, duration: 0.6, repeat: 5, yoyo: true }, 0);
      tl.fromTo([P.g, Sp.g], { opacity: 0 }, { opacity: 1, duration: 0.4, stagger: 0.15 }, 0.1);
      tl.to(cup, { x: -30, rotation: -70, svgOrigin: "920 880", duration: 0.25, ease: "power1.in" }, fa - 0.1);
      tl.to(cup, { y: 90, duration: 0.3, ease: "power2.in" }, fa + 0.15);
      tl.to(Sp.a2, { rotation: -55, duration: 0.12, ease: "power4.out" }, fn - 0.15);
      tl.set(cup, { x: -60, y: -20, rotation: 0 }, fn - 0.03);
      tl.fromTo(ring, { opacity: 1, attr: { r: 40 } }, { opacity: 0, attr: { r: 160 }, duration: 0.5, immediateRender: false }, fn);
      tl.to(Sp.g, { x: 726, duration: 0.03, repeat: 3, yoyo: true }, fn);
      tl.to(P.eyes, { x: 7, duration: 0.15 }, oh - 0.2);
      tl.to(P.mouth, { attr: { d: "M-10 -30 q10 -12 20 0 q-10 12 -20 0" }, duration: 0.1 }, oh);
      tl.fromTo("#s10-b", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, gl - 0.1);''' + OUT)

# ---------- s11 Plakate mit Sinas Gesicht, ein Mann schaut zurück ----------
S['s11'] = ('''    #s11-q { position: absolute; left: 0; width: 1080px; top: 520px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 300px;
      color: #ff3b55; text-shadow: 0 0 60px rgba(255,59,85,.7); opacity: 0; }
    #s11-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 40%, rgba(160,0,20,.75) 100%); opacity: 0; }''',
SVG + '''
      <div id="s11-q" class="abs">?</div><div id="s11-vig" class="full"></div>''',
'''      const wall = el("g", {}, sv);
      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#2b2440" }, wall);
      for (let r = 0; r < 9; r++) el("path", { d: `M0 ${440 + r * 76} h1080`, stroke: "#3a3158", "stroke-width": 4 }, wall);
      const posters = [[110, 500, -5], [410, 470, 3], [710, 510, -2]].map(([x, y, rot], i) => {
        const g = el("g", { opacity: 0 }, wall); gsap.set(g, { rotation: rot, svgOrigin: `${x + 130} ${y + 180}` });
        el("rect", { x, y, width: 260, height: 360, rx: 8, fill: "#f3f1ea" }, g);
        el("rect", { x, y, width: 260, height: 64, fill: "#ff3b55" }, g);
        el("text", { x: x + 130, y: y + 46, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 38, fill: "#fff" }, g).textContent = "GESUCHT";
        el("path", { d: `M${x + 70} ${y + 250} C${x + 64} ${y + 120} ${x + 196} ${y + 120} ${x + 190} ${y + 250}Z`, fill: "#4a2c1d" }, g);
        el("circle", { cx: x + 130, cy: y + 180, r: 48, fill: "#f2c9a5" }, g);
        el("path", { d: `M${x + 82} ${y + 172} C${x + 82} ${y + 112} ${x + 178} ${y + 112} ${x + 178} ${y + 172} C${x + 160} ${y + 140} ${x + 110} ${y + 136} ${x + 82} ${y + 172}Z`, fill: "#4a2c1d" }, g);
        el("rect", { x: x + 70, y: y + 250, width: 120, height: 40, rx: 14, fill: "#ff4fb0" }, g);
        el("text", { x: x + 130, y: y + 336, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 36, fill: "#161a36" }, g).textContent = "SINA";
        return g; });
      const F = face(sv, 540, 790, 230, { blind: true, hair: "#161a36", skin: "#d9a77f" }); gsap.set(F.g, { opacity: 0 });
      const pl = at("L16", "Plakate"), ge = at("L16", "Gesicht"), l17 = line("L17")[0], fw = at("L17", "Für"), l31 = line("L31")[0], zu = at("L31", "zurück"), ta = at("L31", "tastet");
      posters.forEach((p, i) => tl.fromTo(p, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, pl - 0.1 + i * 0.2));
      tl.to(posters, { y: -6, duration: 0.05, repeat: 5, yoyo: true }, ge);
      tl.to(wall, { opacity: 0.25, duration: 0.3 }, fw - 0.3);
      tl.fromTo("#s11-q", { opacity: 0, scale: 0.4 }, { opacity: 0.95, scale: 1, duration: 0.35, ease: "back.out(2.4)" }, fw);
      tl.to("#s11-q", { opacity: 0, duration: 0.2 }, l31 - 0.2);
      tl.to(wall, { opacity: 0, duration: 0.2 }, l31 - 0.2);
      tl.fromTo(F.g, { opacity: 0, scale: 0.9, svgOrigin: "540 790" }, { opacity: 1, scale: 1, svgOrigin: "540 790", duration: 0.4 }, l31);
      tl.to(F.cloud, { opacity: 0, duration: 0.08 }, zu - 0.15);
      tl.to(F.pup, { opacity: 1, duration: 0.08 }, zu - 0.15);
      tl.fromTo(F.g, { scale: 1 }, { scale: 1.3, svgOrigin: "540 790", duration: 0.3, ease: "power4.out" }, zu - 0.15);
      tl.to("#s11-vig", { opacity: 1, duration: 0.12 }, zu - 0.15);
      tl.to(F.cloud, { opacity: 1, duration: 0.2 }, ta - 0.1);
      tl.to(F.pup, { opacity: 0, duration: 0.2 }, ta - 0.1);
      tl.to("#s11-vig", { opacity: 0, duration: 0.4 }, ta);
      tl.to(F.g, { x: -400, opacity: 0, duration: 1.0, ease: "power1.in" }, ta + 0.2);''' + OUT)

# ---------- s12 Spartakus telefoniert, Tür von außen abgeschlossen ----------
S['s12'] = ('''    #s12-b { left: 420px; top: 430px; width: 600px; background: #ff3b55; color: #fff; }
    #s12-lab { left: 200px; top: 450px; width: 680px; height: 100px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 52px; line-height: 90px; box-shadow: 0 0 40px rgba(255,59,85,.5); opacity: 0; }''',
SVG + '''
      <div id="s12-b" class="bub">„ICH HABE SIE. 6 UHR. BAHNHOF.“</div><div id="s12-lab" class="panel">VON AUSSEN ZU!</div>''',
'''      const A = el("g", {}, sv);
      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#0b0d20" }, A);
      el("rect", { x: 620, y: 560, width: 300, height: 360, rx: 8, fill: "#1c2250" }, A);
      el("circle", { cx: 860, cy: 620, r: 34, fill: "#f3f1ea", opacity: 0.7 }, A);
      const Sp = person(A, "s12-s", 760, 760, 1.05, { blind: true, shades: true, shirt: "#39a06a", hair: "#2a2f55", arms: [12, -150] });
      const ph = el("rect", { x: 800, y: 640, width: 26, height: 48, rx: 6, fill: "#4da3ff" }, A);
      const glow = el("circle", { cx: 812, cy: 664, r: 60, fill: "#4da3ff", opacity: 0.25 }, A);
      el("rect", { x: 80, y: 520, width: 200, height: 600, fill: "#3a2614" }, A);
      el("rect", { x: 280, y: 520, width: 40, height: 600, fill: "#05060f" }, A);
      const P = person(A, "s12-p", 300, 780, 1.0, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" }); gsap.set(P.g, { x: 250 });
      const B = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#0b0d20" }, B);
      const door = el("g", {}, B);
      el("rect", { x: 330, y: 560, width: 420, height: 560, rx: 6, fill: "#7a4b22" }, door);
      const handle = el("rect", { x: 660, y: 830, width: 70, height: 18, rx: 8, fill: "#ffd43b" }, door);
      const lock = el("g", { opacity: 0 }, B);
      el("rect", { x: 500, y: 760, width: 80, height: 70, rx: 12, fill: "#ff3b55" }, lock);
      el("path", { d: "M515 760 v-26 q25 -40 50 0 v26", stroke: "#ff3b55", "stroke-width": 12, fill: "none" }, lock);
      const te = at("L18", "telefoniert"), ha = at("L19", "habe"), l32 = line("L32")[0], ab = at("L32", "abgeschlossen"), au = at("L32", "außen");
      tl.fromTo(glow, { attr: { r: 50 } }, { attr: { r: 80 }, duration: 0.5, repeat: 9, yoyo: true }, 0);
      tl.to(P.g, { x: 290, duration: 0.6, ease: "power2.out" }, te - 0.4);
      tl.to(P.eyes, { x: 7, duration: 0.2 }, te);
      tl.fromTo("#s12-b", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ha - 0.4);
      tl.to(P.mouth, { attr: { d: "M-10 -30 q10 -12 20 0 q-10 12 -20 0" }, duration: 0.1 }, ha);
      tl.to(P.g, { x: 296, duration: 0.04, repeat: 5, yoyo: true }, ha);
      tl.to("#s12-b", { opacity: 0, duration: 0.2 }, l32 - 0.2);
      tl.to(A, { opacity: 0, duration: 0.2 }, l32 - 0.2);
      tl.to(B, { opacity: 1, duration: 0.2 }, l32 - 0.2);
      tl.to(handle, { rotation: 25, svgOrigin: "668 839", duration: 0.08, repeat: 9, yoyo: true }, ab - 0.4);
      tl.to(door, { x: 6, duration: 0.04, repeat: 7, yoyo: true }, ab);
      tl.fromTo(lock, { opacity: 0, scale: 1.8, svgOrigin: "540 780" }, { opacity: 1, scale: 1, svgOrigin: "540 780", duration: 0.25, ease: "power4.out" }, au - 0.1);
      tl.fromTo("#s12-lab", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, au);''' + OUT)

# ---------- s13 Bahnhof: hundert Menschen drehen gleichzeitig den Kopf ----------
S['s13'] = ('''    #s13-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 35%, rgba(160,0,20,.8) 100%); opacity: 0; }''',
SVG + '''
      <div id="s13-vig" class="full"></div>''',
'''      const st = el("g", {}, sv);
      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#141838" }, st);
      el("rect", { x: 0, y: 1000, width: 1080, height: 40, fill: "#c9cde6" }, st);
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#2a2f55" }, st);
      el("rect", { x: 330, y: 450, width: 420, height: 90, rx: 10, fill: "#0b0e22", stroke: "#ffd43b", "stroke-width": 4 }, st);
      el("text", { x: 540, y: 510, "text-anchor": "middle", "font-family": "Space Mono", "font-weight": 700, "font-size": 40, fill: "#ffd43b" }, st).textContent = "GLEIS 1 · 06:00";
      const crowd = el("g", {}, st), ms = [], r = rng(5);
      for (let row = 0; row < 3; row++) for (let i = 0; i < 11; i++) ms.push(mini(crowd, 60 + i * 96 + (row % 2) * 40 + (r() - 0.5) * 20, 640 + row * 90, ["#3a4280", "#47508f", "#2f366e"][(i + row) % 3]));
      const pair = el("g", {}, st);
      const P = person(pair, "s13-p", 360, 760, 0.95, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const Sp = person(pair, "s13-s", 520, 750, 1.0, { blind: true, shades: true, shirt: "#39a06a", hair: "#2a2f55" });
      gsap.set(pair, { x: -500 });
      const fc = el("g", { opacity: 0 }, sv), F = [];
      [[200, 640], [540, 600], [880, 640], [370, 900], [710, 900]].forEach(([x, y], i) => F.push(face(fc, x, y, 120, { blind: true, hair: ["#161a36", "#5b3a26", "#e0a35a", "#2a2f55", "#8a5a2b"][i], skin: ["#f2c9a5", "#d9a77f", "#f2c9a5", "#b9835a", "#f2c9a5"][i] })));
      const l20 = line("L20")[0], ra = at("L20", "raus"), vo = at("L21", "voll"), sti = at("L21", "still"), l22 = line("L22")[0], gl = at("L22", "gleichzeitig"), zu = at("L22", "Zu");
      tl.to(pair, { x: 0, duration: 1.4, ease: "power2.out" }, l20);
      tl.to(P.g, { y: 766, duration: 0.15, repeat: 7, yoyo: true }, l20);
      ms.forEach((m, i) => tl.fromTo(m, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }, vo - 0.4 + (i % 11) * 0.03 + Math.floor(i / 11) * 0.08));
      tl.to(P.eyes, { x: -6, duration: 0.2, repeat: 3, yoyo: true }, sti);
      tl.to(st, { opacity: 0, duration: 0.3 }, l22 - 0.2);
      tl.to(fc, { opacity: 1, duration: 0.3 }, l22 - 0.1);
      F.forEach((f, i) => { tl.to(f.cloud, { opacity: 0, duration: 0.05 }, zu - 0.1); tl.to(f.pup, { opacity: 1, duration: 0.05 }, zu - 0.1); });
      tl.fromTo(fc, { scale: 1 }, { scale: 1.12, svgOrigin: "540 760", duration: 0.25, ease: "power4.out" }, zu - 0.1);
      tl.to("#s13-vig", { opacity: 1, duration: 0.1 }, zu - 0.1);
      tl.to("#s13-vig", { opacity: 0.5, duration: 0.4, repeat: 5, yoyo: true }, zu + 0.2);''' + OUT)

# ---------- s14 Der Sammler, Spartakus nimmt die Sonnenbrille ab, "Du bist die Letzte" ----------
S['s14'] = ('''    #s14-b { left: 440px; top: 430px; width: 580px; background: #0b0e22; color: #fff; border: 4px solid #ff3b55; }
    #s14-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 35%, rgba(160,0,20,.8) 100%); opacity: 0; }
    #s14-w { position: absolute; left: 0; width: 1080px; top: 470px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 150px;
      color: #ff3b55; text-shadow: 0 0 50px rgba(255,59,85,.7), 0 10px 0 rgba(0,0,0,.6); opacity: 0; }
    #s14-black { background: #000; opacity: 0; }''',
SVG + '''
      <div id="s14-vig" class="full"></div>
      <div id="s14-b" class="bub">„GUTE ARBEIT, SPARTAKUS.“</div>
      <div id="s14-w">DIE LETZTE.</div>
      <div id="s14-black" class="full"></div>''',
'''      const A = el("g", {}, sv);
      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#141838" }, A);
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#2a2f55" }, A);
      for (let i = 0; i < 12; i++) mini(A, 40 + i * 92, 980, "#2f366e").setAttribute("opacity", "0.6");
      const P = person(A, "s14-p", 220, 760, 1.0, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const Sp = person(A, "s14-s", 420, 750, 1.05, { blind: true, shades: true, shirt: "#39a06a", hair: "#2a2f55" });
      const Sm = el("g", {}, A); gsap.set(Sm, { x: 400 });
      const SM = person(Sm, "s14-m", 780, 690, 1.3, { shirt: "#0b0e22", hair: "#0b0e22", pants: "#0b0e22", skin: "#c9b49a" });
      el("path", { d: "M-70 0 L70 0 L95 230 L-95 230Z", fill: "#161a36" }, SM.g);
      el("rect", { x: -70, y: -122, width: 140, height: 20, rx: 6, fill: "#05060f" }, SM.g); el("rect", { x: -44, y: -170, width: 88, height: 54, rx: 10, fill: "#05060f" }, SM.g);
      el("path", { d: "M-16 -34 q16 14 32 0", stroke: "#8a3b2a", "stroke-width": 5, fill: "none" }, SM.g);
      const CU = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#0b0d20" }, CU);
      const F = face(CU, 540, 800, 260, { hair: "#2a2f55" });
      const sh = el("g", {}, CU);
      el("rect", { x: 380, y: 780, width: 140, height: 90, rx: 30, fill: "#05060f" }, sh); el("rect", { x: 560, y: 780, width: 140, height: 90, rx: 30, fill: "#05060f" }, sh);
      el("rect", { x: 510, y: 805, width: 60, height: 16, fill: "#05060f" }, sh);
      const shine = [el("circle", { cx: 438, cy: 818, r: 10, fill: "#ffd43b", opacity: 0 }, CU), el("circle", { cx: 618, cy: 818, r: 10, fill: "#ffd43b", opacity: 0 }, CU)];
      const sa = at("L23", "Sammler"), gu = at("L23", "Gute"), l24 = line("L24")[0], so = at("L24", "Sonnenbrille"), kl = at("L24", "klar"),
            l25 = line("L25")[0], ga = at("L25", "ganze"), l26 = line("L26")[0], le = at("L26", "Letzte");
      tl.to(Sm, { x: 0, duration: 0.9, ease: "power3.out" }, sa - 0.6);
      tl.to(P.eyes, { x: 7, duration: 0.2 }, sa);
      tl.fromTo("#s14-b", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, gu - 0.05);
      tl.to("#s14-b", { opacity: 0, duration: 0.2 }, l24 - 0.1);
      tl.to(A, { opacity: 0, duration: 0.25 }, l24);
      tl.to(CU, { opacity: 1, duration: 0.25 }, l24);
      tl.fromTo(CU, { scale: 1 }, { scale: 1.08, svgOrigin: "540 820", duration: 3.5, ease: "none" }, l24);
      tl.to(sh, { y: -260, rotation: -12, svgOrigin: "540 820", opacity: 0, duration: 0.9, ease: "power2.inOut" }, so - 0.2);
      tl.to(shine, { opacity: 1, duration: 0.1 }, kl);
      tl.fromTo(shine, { scale: 0.5 }, { scale: 2.2, svgOrigin: "540 818", duration: 0.25, yoyo: true, repeat: 1 }, kl);
      tl.to("#s14-vig", { opacity: 1, duration: 0.1 }, ga);
      tl.to(CU, { x: 12, duration: 0.04, repeat: 7, yoyo: true }, ga);
      tl.to("#s14-vig", { opacity: 0.5, duration: 0.45, repeat: 7, yoyo: true }, ga + 0.2);
      tl.to(CU, { opacity: 0.2, duration: 0.3 }, l26);
      tl.fromTo("#s14-w", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.out" }, le - 0.05);
      tl.to("#s14-w", { x: 12, duration: 0.04, repeat: 5, yoyo: true }, le + 0.15);
      tl.to("#s14-black", { opacity: 1, duration: 0.05 }, le + 0.9);
      tl.set("#s14-w", { opacity: 0 }, le + 0.9);''')

# ---------- s15 Ende: Wem traust du? + Folgen für Part 3 (letzte Szene, kein Blur-Out) ----------
S['s15'] = ('''    #s15-bg { background: #000; }
    .s15-btn { position: absolute; top: 640px; width: 420px; height: 150px; border-radius: 26px; font-family: "Inter", sans-serif; font-weight: 900;
      font-size: 52px; line-height: 150px; text-align: center; opacity: 0; }
    #s15-a { left: 80px; background: #39e27a; color: #0b0e22; box-shadow: 0 0 40px rgba(57,226,122,.45); } #s15-c { left: 580px; background: #ff3b55; color: #fff; box-shadow: 0 0 40px rgba(255,59,85,.45); }
    #s15-cta { left: 90px; top: 470px; width: 900px; height: 600px; border: 6px solid #ff4fb0; box-shadow: 0 0 70px rgba(255,79,176,.5); opacity: 0; }
    #s15-cta .a { margin-top: 300px; font-size: 54px; line-height: 1.1; color: #fff; }
    #s15-btn { position: absolute; left: 290px; top: 440px; width: 320px; height: 100px; border-radius: 50px; background: #ff4fb0; color: #fff; font-size: 54px; line-height: 100px; }
    #s15-p3 { position: absolute; left: 620px; top: 36px; width: 240px; height: 76px; border-radius: 14px; background: #ffd43b; color: #0b0e22; font-size: 44px; line-height: 76px; transform: rotate(6deg); }''',
'''      <div id="s15-bg" class="full"></div>
      <div id="s15-a" class="s15-btn">SPARTAKUS</div><div id="s15-c" class="s15-btn">NIEMANDEM</div>
      <div id="s15-cta" class="panel"><div id="s15-p3">PART 3</div><div class="a">WENN DU DAS<br>SEHEN KANNST …</div><div id="s15-btn">+ FOLGEN</div></div>
''' + SVG,
'''      const E = bigEye(sv, 540, 640, 0.75); gsap.set(E.g, { opacity: 0 });
      const du = at("L27", "du"), l28 = line("L28")[0], se = at("L28", "sehen"), fo = at("L28", "folge"), pa = at("L28", "Part");
      tl.fromTo(".s15-btn", { opacity: 0, y: 80, rotation: (i) => [-6, 6][i] }, { opacity: 1, y: 0, rotation: 0, duration: 0.4, stagger: 0.12, ease: "back.out(2)" }, du);
      tl.to(".s15-btn", { opacity: 0, duration: 0.25 }, l28 - 0.2);
      tl.fromTo("#s15-cta", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, l28);
      tl.to(E.g, { opacity: 1, duration: 0.3 }, l28 + 0.1);
      tl.to(E.iris, { x: -60, duration: 0.3, yoyo: true, repeat: 1 }, se);
      tl.fromTo("#s15-btn", { scale: 1 }, { scale: 1.15, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }, fo);
      tl.fromTo("#s15-p3", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(3)" }, pa);''')


here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
