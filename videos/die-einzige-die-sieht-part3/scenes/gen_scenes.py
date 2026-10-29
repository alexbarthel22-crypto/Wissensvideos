#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s13 für „Die Einzige, die sieht – Part 3 (Finale)“ (hier ändern und neu erzeugen)."""
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

# ---------- Zusatz-Helfer (Sammler, Sendeturm, Globus) ----------
EXTRA_JS = '''
      function sammler(parent, id, x, y, s) {
        const p = person(parent, id, x, y, s, { shirt: "#0b0e22", hair: "#0b0e22", pants: "#0b0e22", skin: "#c9b49a" });
        el("path", { d: "M-70 0 L70 0 L95 230 L-95 230Z", fill: "#161a36" }, p.g);
        el("rect", { x: -70, y: -122, width: 140, height: 20, rx: 6, fill: "#05060f" }, p.g); el("rect", { x: -44, y: -170, width: 88, height: 54, rx: 10, fill: "#05060f" }, p.g);
        return p;
      }
      function tower(parent, x, y, s) {
        const g = el("g", {}, parent); gsap.set(g, { x, y, scale: s, transformOrigin: "0 0" });
        el("path", { d: "M-90 0 L-12 -520 L12 -520 L90 0", fill: "none", stroke: "#8fa2ff", "stroke-width": 12 }, g);
        for (let i = 1; i < 6; i++) { const yy = -i * 86, w = 90 - i * 15; el("path", { d: `M${-w} ${yy} L${w - 15} ${yy - 86} M${w} ${yy} L${-w + 15} ${yy - 86}`, stroke: "#5d6db8", "stroke-width": 6 }, g); }
        el("rect", { x: -40, y: -560, width: 80, height: 40, rx: 8, fill: "#8fa2ff" }, g);
        const lamp = el("circle", { cx: 0, cy: -580, r: 16, fill: "#ff3b55" }, g);
        return { g, lamp };
      }
      function globe(parent, x, y, r) {
        const g = el("g", {}, parent);
        const sea = el("circle", { cx: x, cy: y, r, fill: "#2b6fd1" }, g);
        [[-0.4, -0.3, 0.35, 0.25], [0.3, -0.1, 0.3, 0.4], [-0.1, 0.45, 0.25, 0.15]].forEach(([dx, dy, rx, ry]) => el("ellipse", { cx: x + dx * r, cy: y + dy * r, rx: rx * r, ry: ry * r, fill: "#39a06a" }, g));
        return { g, sea };
      }
'''

# ---------- s01 Hook: Spartakus ist einer von ihnen, Titel DAS FINALE ----------
S['s01'] = ('''    #s01-news { left: 60px; top: 690px; width: 960px; height: 420px; border: 5px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.45); overflow: hidden; text-align: left; }
    #s01-news .bar { height: 84px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 34px; font-size: 44px; letter-spacing: .06em; }
    #s01-news .hl { padding: 22px 40px 0; font-size: 84px; line-height: 1.04; letter-spacing: -.015em; }
    #s01-news .hl em { font-style: normal; color: #ff3b55; text-shadow: 0 0 26px rgba(255,59,85,.6); }
    #s01-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 40%, rgba(160,0,20,.75) 100%); opacity: 0; }
    #s01-dark { background: #05060f; opacity: 0; }
    #s01-title { left: 0; width: 1080px; top: 500px; height: 340px; overflow: hidden; text-align: center; opacity: 0; }
    #s01-title .k { margin-top: 20px; font-family: "Space Mono", monospace; font-weight: 700; font-size: 54px; letter-spacing: .3em; color: #ff4fb0; text-shadow: 0 0 26px rgba(255,79,176,.7); }
    #s01-title .t { margin-top: 18px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 124px; line-height: 1; color: #ffd43b; text-shadow: 0 0 50px rgba(255,212,59,.5), 0 8px 0 rgba(0,0,0,.5); }
    #s01-sweep { position: absolute; left: -300px; top: -40px; width: 200px; height: 420px; transform: skewX(-20deg);
      background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.45), rgba(255,255,255,0)); }
    .s01-bar { position: absolute; left: 0; width: 1080px; height: 150px; background: #000; }''',
SVG + '''
      <div id="s01-vig" class="full"></div>
      <div id="s01-news" class="panel"><div class="bar">● EILMELDUNG · FINALE</div><div class="hl">SPARTAKUS IST <em>EINER VON IHNEN</em></div></div>
      <div id="s01-dark" class="full"></div>
      <div id="s01-title" class="abs"><div class="k">PART 3</div><div class="t">DAS FINALE</div><div id="s01-sweep"></div></div>
      <div id="s01-bar1" class="s01-bar" style="top:0;transform:translateY(-150px)"></div><div id="s01-bar2" class="s01-bar" style="top:1770px;transform:translateY(150px)"></div>
      <svg id="s01-iris" class="full" viewBox="0 0 1080 1920"><circle id="s01-ir" cx="540" cy="760" r="2600" fill="none" stroke="#000" stroke-width="2400"/></svg>''',
'''      const F = face(sv, 540, 570, 130, { hair: "#2a2f55" }); F.g.style.filter = "drop-shadow(0 0 30px rgba(255,212,59,.6))";
      const glints = F.pup.map((p) => el("circle", { cx: +p.getAttribute("cx") + 5, cy: +p.getAttribute("cy") - 5, r: 5, fill: "#ffd43b" }, F.g));
      const sp = at("L1", "Spartakus"), ei = at("L1", "einer"), l2 = line("L2")[0], sc = at("L2", "schlimmer");
      tl.fromTo("#s01-news", { scale: 1.06 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);
      tl.to("#s01-news", { x: 8, duration: 0.04, repeat: 5, yoyo: true }, 0.9);
      tl.to(F.pup, { attr: { cx: (i) => [495, 585][i] - 14 }, duration: 0.3, repeat: 3, yoyo: true }, 1.2);
      tl.to("#s01-news", { opacity: 0, y: 160, duration: 0.3, ease: "power3.in" }, sp - 0.4);
      tl.to(F.g, { scale: 1.9, svgOrigin: "540 570", y: 200, duration: 0.6, ease: "expo.out" }, sp - 0.1);
      tl.fromTo("#s01-vig", { opacity: 0 }, { opacity: 1, duration: 0.12 }, ei);
      tl.fromTo(glints, { scale: 0.5 }, { scale: 2.4, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 3 }, ei);
      tl.to("#s01-dark", { opacity: 0.9, duration: 0.4 }, l2 - 0.1);
      tl.to(F.g, { opacity: 0, duration: 0.35 }, l2 - 0.1);
      tl.fromTo("#s01-bar1", { y: -150 }, { y: 0, duration: 0.5, ease: "power3.out" }, l2 - 0.1);
      tl.fromTo("#s01-bar2", { y: 150 }, { y: 0, duration: 0.5, ease: "power3.out" }, l2 - 0.1);
      tl.fromTo("#s01-title", { opacity: 0, scale: 1.4, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, l2 + 0.1);
      tl.fromTo("#s01-sweep", { x: 0 }, { x: 1700, duration: 0.9, ease: "power2.inOut" }, l2 + 0.6);
      tl.to("#s01-title .t", { color: "#ff3b55", duration: 0.05, repeat: 5, yoyo: true }, sc);
      tl.to("#s01-title", { x: 10, duration: 0.04, repeat: 7, yoyo: true }, sc);
      tl.to("#s01-ir", { attr: { r: 1200 }, duration: 0.45, ease: "power2.in" }, C.__dur - 0.5);''' + OUT.replace('#@@ID@@-stage > *', '#@@ID@@-stage > *:not(#s01-iris)'))

# ---------- s02 Der Sammler: das Signal um drei Uhr nachts ----------
S['s02'] = ('''    #s02-chip { left: 540px; top: 450px; width: 480px; white-space: nowrap; height: 96px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 48px; line-height: 86px; box-shadow: 0 0 40px rgba(255,59,85,.5); opacity: 0; }''',
SVG + '''
      <svg class="full" viewBox="0 0 1080 1920"><circle id="s02-ir" cx="540" cy="760" r="1200" fill="none" stroke="#000" stroke-width="2400"/></svg>
      <div id="s02-chip" class="panel">03:00 · SIGNAL</div>''',
'''      tl.fromTo("#s02-ir", { attr: { r: 1200 } }, { attr: { r: 2600 }, duration: 0.6, ease: "power2.out" }, 0);
      el("rect", { x: 0, y: 1060, width: 1080, height: 70, fill: "#2a2f55" }, sv);
      const T = tower(sv, 780, 1060, 1.0);
      const rings = [0, 1, 2, 3].map((i) => el("circle", { cx: 780, cy: 480, r: 30, fill: "none", stroke: "#ff3b55", "stroke-width": 8, opacity: 0 }, sv));
      const SM = sammler(sv, "s02-m", 290, 760, 1.25);
      const eyes = [], r = rng(9);
      for (let i = 0; i < 10; i++) { const e = bigEye(sv, 90 + (i % 5) * 225 + (r() - 0.5) * 40, 470 + Math.floor(i / 5) * 120, 0.18); gsap.set(e.g, { opacity: 0 }); eyes.push(e.g); }
      const si = at("L4", "Signal"), dr = at("L4", "Drei"), wi = at("L4", "wir");
      tl.fromTo(SM.g, { opacity: 0, x: 200 }, { opacity: 1, x: 290, duration: 0.5, ease: "expo.out" }, 0.1);
      tl.to(SM.mouth, { attr: { d: "M-16 -34 q16 14 32 0" }, duration: 0.2 }, 0.6);
      tl.to(T.lamp, { opacity: 0.2, duration: 0.2, repeat: 9, yoyo: true }, 0.3);
      rings.forEach((g, i) => tl.fromTo(g, { opacity: 1, attr: { r: 30 } }, { opacity: 0, attr: { r: 520 }, duration: 1.2, ease: "power1.out", immediateRender: false }, si - 0.1 + i * 0.3));
      tl.fromTo("#s02-chip", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, dr - 0.1);
      tl.to("#s02-chip", { opacity: 0, duration: 0.2 }, wi - 1.0);
      eyes.forEach((e, i) => tl.to(e, { opacity: 1, duration: 0.15 }, wi - 0.6 + i * 0.05));''' + OUT)

# ---------- s03 Du bist ein Fehler – dein Blut ist das Gegenmittel ----------
S['s03'] = ('''    #s03-st { left: 290px; top: 470px; width: 500px; height: 130px; border: 7px solid #ff3b55; border-radius: 20px; color: #ff3b55; font-size: 86px; line-height: 116px; box-shadow: 0 0 50px rgba(255,59,85,.5); opacity: 0; }
    #s03-lab { left: 300px; top: 450px; width: 480px; height: 96px; border: 5px solid #39e27a; color: #39e27a; font-size: 50px; line-height: 86px; box-shadow: 0 0 40px rgba(57,226,122,.5); opacity: 0; }''',
SVG + '''
      <div id="s03-st" class="panel">FEHLER</div><div id="s03-lab" class="panel">GEGENMITTEL</div>''',
'''      const P = person(sv, "s03-p", 540, 760, 1.15, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const drop = el("g", { opacity: 0 }, sv);
      el("circle", { cx: 540, cy: 800, r: 110, fill: "#39e27a", opacity: 0.25 }, drop);
      el("path", { d: "M540 690 C600 780 620 820 620 850 A80 80 0 0 1 460 850 C460 820 480 780 540 690Z", fill: "#ff3b55" }, drop);
      el("ellipse", { cx: 512, cy: 840, rx: 14, ry: 26, fill: "#fff", opacity: 0.5 }, drop);
      const G = globe(sv, 540, 800, 220); gsap.set(G.g, { opacity: 0 });
      const ey = [bigEye(sv, 470, 760, 0.14), bigEye(sv, 610, 800, 0.14), bigEye(sv, 540, 900, 0.14)]; gsap.set(ey.map((e) => e.g), { opacity: 0 });
      const X = el("path", { d: "M330 590 L750 1010 M750 590 L330 1010", stroke: "#ff3b55", "stroke-width": 26, "stroke-linecap": "round", opacity: 0 }, sv);
      const fe = at("L5", "Fehler"), l6 = line("L6")[0], ge = at("L6", "Gegenmittel"), wi = at("L6", "Welt"), l7 = line("L7")[0], ni = at("L7", "Nie");
      tl.fromTo(P.g, { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.1);
      tl.fromTo("#s03-st", { opacity: 0, scale: 2, rotation: -12 }, { opacity: 1, scale: 1, rotation: -5, duration: 0.25, ease: "power4.out" }, fe - 0.05);
      tl.to(P.g, { x: 548, duration: 0.04, repeat: 5, yoyo: true }, fe);
      tl.to(["#s03-st", P.g], { opacity: 0, duration: 0.2 }, l6 - 0.1);
      tl.fromTo(drop, { opacity: 0, scale: 0.4, svgOrigin: "540 820" }, { opacity: 1, scale: 1, svgOrigin: "540 820", duration: 0.4, ease: "back.out(2)" }, l6);
      tl.fromTo("#s03-lab", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, ge - 0.05);
      tl.to(drop, { opacity: 0, scale: 0.3, svgOrigin: "540 820", duration: 0.25 }, wi - 0.6);
      tl.to("#s03-lab", { opacity: 0, duration: 0.2 }, wi - 0.6);
      tl.fromTo(G.g, { opacity: 0, scale: 0.6, svgOrigin: "540 800" }, { opacity: 1, scale: 1, svgOrigin: "540 800", duration: 0.4, ease: "back.out(1.8)" }, wi - 0.5);
      tl.to(ey.map((e) => e.g), { opacity: 1, duration: 0.2, stagger: 0.1 }, wi);
      tl.to(G.g, { filter: "grayscale(1) brightness(0.5)", duration: 0.4 }, l7 + 0.2);
      tl.to(ey.map((e) => e.g), { opacity: 0, duration: 0.2 }, l7 + 0.2);
      tl.fromTo(X, { opacity: 0, scale: 1.5, svgOrigin: "540 800" }, { opacity: 1, scale: 1, svgOrigin: "540 800", duration: 0.2, ease: "power4.out" }, ni - 0.05);''' + OUT)

# ---------- s04 Wachen packen Sina, Spartakus reißt den Hauptschalter runter ----------
S['s04'] = ('''    #s04-b { left: 470px; top: 440px; width: 540px; background: #ffd43b; }
    #s04-black { background: #000; opacity: 0; }''',
SVG + '''
      <div id="s04-b" class="bub">„AUGEN ZU, SINA.“</div><div id="s04-black" class="full"></div>''',
'''      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#141838" }, sv);
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#2a2f55" }, sv);
      const lamps = [180, 540, 900].map((x) => el("circle", { cx: x, cy: 450, r: 26, fill: "#ffe9a8" }, sv));
      const box = el("g", {}, sv);
      el("rect", { x: 900, y: 600, width: 140, height: 220, rx: 12, fill: "#5d6db8" }, box);
      el("path", { d: "M935 640 l20 -30 l-6 24 l20 -2 l-24 34 l6 -24Z", fill: "#ffd43b" }, box);
      const lever = el("rect", { x: 962, y: 680, width: 16, height: 100, rx: 8, fill: "#ff3b55" }, box);
      el("circle", { cx: 970, cy: 780, r: 16, fill: "#c9cde6" }, box);
      const G1 = person(sv, "s04-g1", 180, 760, 1.05, { shirt: "#0b0e22", hair: "#0b0e22", pants: "#0b0e22", arms: [12, -70] });
      const P = person(sv, "s04-p", 340, 770, 1.0, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0", arms: [20, -20] });
      const G2 = person(sv, "s04-g2", 500, 760, 1.05, { shirt: "#0b0e22", hair: "#0b0e22", pants: "#0b0e22", arms: [70, -12] });
      const Sp = person(sv, "s04-s", 780, 750, 1.05, { shirt: "#39a06a", hair: "#2a2f55", arms: [12, -12] });
      const sparks = [0, 1, 2, 3, 4].map((i) => el("circle", { cx: 970, cy: 700, r: 6, fill: "#ffd43b", opacity: 0 }, sv));
      const pa = at("L8", "packen"), sw = at("L8", "schaut"), l9 = line("L9")[0], az = at("L9", "Augen"), ha = at("L10", "Hauptschalter"), ru = at("L10", "runter");
      tl.fromTo([G1.g, G2.g], { opacity: 0 }, { opacity: 1, duration: 0.3 }, pa - 0.3);
      tl.to(P.g, { y: 760, duration: 0.05, repeat: 5, yoyo: true }, pa);
      tl.to(Sp.eyes, { x: 9, duration: 0.25 }, sw);
      tl.to(Sp.mouth, { attr: { d: "M-12 -26 q12 -10 24 0" }, duration: 0.2 }, sw);
      tl.fromTo("#s04-b", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, l9 + 0.2);
      tl.to(P.lids, { opacity: 1, duration: 0.05 }, az + 0.6);
      tl.to(P.eyes, { opacity: 0, duration: 0.05 }, az + 0.6);
      tl.to("#s04-b", { opacity: 0, duration: 0.2 }, ha - 0.6);
      tl.to(Sp.g, { x: 860, duration: 0.3, ease: "power3.out" }, ha - 0.6);
      tl.to(Sp.a2, { rotation: -150, duration: 0.25 }, ha - 0.4);
      tl.to(Sp.a2, { rotation: -60, duration: 0.15, ease: "power4.in" }, ru - 0.1);
      tl.to(lever, { rotation: 180, svgOrigin: "970 780", duration: 0.15, ease: "power4.in" }, ru - 0.1);
      sparks.forEach((s, i) => tl.fromTo(s, { opacity: 1, x: 0, y: 0 }, { opacity: 0, x: (i - 2) * 50, y: -60 + i * 20, duration: 0.4, immediateRender: false }, ru + 0.05));
      tl.to(lamps, { fill: "#2a2f55", duration: 0.05, stagger: 0.06 }, ru);
      tl.to("#s04-black", { opacity: 1, duration: 0.05 }, ru + 0.25);''')

# ---------- s05 Totale Dunkelheit: alle blind, Blinde sind Profis ----------
S['s05'] = ('''    #s05-bg { background: #000; }''',
'''      <div id="s05-bg" class="full"></div>
''' + SVG,
'''      const guards = [], qs = [];
      [[220, 700], [540, 660], [860, 720]].forEach(([x, y], i) => { const g = el("g", { opacity: 0 }, sv);
        el("circle", { cx: x - 14, cy: y, r: 8, fill: "#f3f1ea" }, g); el("circle", { cx: x + 14, cy: y, r: 8, fill: "#f3f1ea" }, g);
        const q = el("text", { x, y: y - 40, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 70, fill: "#ff3b55", opacity: 0 }, sv); q.textContent = "?";
        guards.push(g); qs.push(q); });
      const pros = [], r = rng(4);
      for (let i = 0; i < 8; i++) { const g = mini(sv, 120 + i * 120, 960 + (i % 2) * 40, "#0b0e22"); g.style.filter = "drop-shadow(0 0 10px rgba(57,226,122,.9))"; pros.push(g); }
      const da = at("L11", "Dunkelheit"), al = at("L11", "alle"), l12 = line("L12")[0], pr = at("L12", "Profis");
      guards.forEach((g, i) => { tl.to(g, { opacity: 1, duration: 0.1 }, da + i * 0.15); tl.to(g, { x: (i % 2 ? 1 : -1) * 30, duration: 0.25, repeat: 7, yoyo: true, ease: "sine.inOut" }, da + 0.2 + i * 0.1); });
      qs.forEach((q, i) => tl.fromTo(q, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, transformOrigin: "50% 100%", duration: 0.25, ease: "back.out(3)" }, al + i * 0.12));
      pros.forEach((p, i) => { tl.to(p, { opacity: 1, duration: 0.2 }, l12 + i * 0.06); tl.to(p, { x: 140, duration: 2.5, ease: "none" }, l12); });
      tl.to(pros, { y: -10, duration: 0.2, repeat: 9, yoyo: true }, l12);
      tl.to(pros, { scale: 1.15, transformOrigin: "50% 100%", duration: 0.15, yoyo: true, repeat: 1 }, pr);''' + OUT)

# ---------- s06 Chaos im Dunkeln: Säule, Getränkeautomat, Handschellen für den Chef ----------
S['s06'] = ('''    #s06-bg { background: #05060f; }
    #s06-b { left: 90px; top: 440px; width: 520px; background: #4da3ff; color: #fff; }''',
'''      <div id="s06-bg" class="full"></div>
''' + SVG + '''
      <div id="s06-b" class="bub">„OH, ENTSCHULDIGUNG!“</div>''',
'''      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#14172e" }, sv);
      const pil = el("rect", { x: 120, y: 470, width: 110, height: 570, fill: "#2a2f55" }, sv);
      const G1 = person(sv, "s06-g1", 380, 780, 1.0, { blind: true, shirt: "#1c2250", hair: "#0b0e22", pants: "#1c2250", arms: [80, -80] });
      const stars = [0, 1, 2].map((i) => el("text", { x: 250 + i * 40, y: 640 - i * 20, "font-size": 50, fill: "#ffd43b", opacity: 0 }, sv)); stars.forEach((s) => (s.textContent = "★"));
      const vm = el("g", {}, sv);
      el("rect", { x: 760, y: 560, width: 220, height: 480, rx: 14, fill: "#ff3b55" }, vm);
      el("rect", { x: 785, y: 590, width: 120, height: 300, rx: 8, fill: "#a9d2ff" }, vm);
      for (let i = 0; i < 4; i++) el("rect", { x: 800, y: 610 + i * 70, width: 90, height: 40, rx: 6, fill: ["#ffd43b", "#39e27a", "#ff8a3d", "#4da3ff"][i] }, vm);
      el("rect", { x: 920, y: 620, width: 36, height: 80, rx: 6, fill: "#0b0e22" }, vm);
      const G2 = person(sv, "s06-g2", 640, 790, 1.0, { blind: true, shirt: "#1c2250", hair: "#0b0e22", pants: "#1c2250", arms: [12, -12] });
      const S2 = el("g", { opacity: 0 }, sv);
      const SM = sammler(S2, "s06-m", 360, 760, 1.15);
      const GG = person(S2, "s06-g3", 640, 790, 1.0, { blind: true, shirt: "#1c2250", hair: "#0b0e22", pants: "#1c2250", arms: [12, -100] });
      const cuffs = el("g", { opacity: 0 }, S2);
      el("circle", { cx: 450, cy: 900, r: 22, fill: "none", stroke: "#c9cde6", "stroke-width": 8 }, cuffs); el("circle", { cx: 500, cy: 900, r: 22, fill: "none", stroke: "#c9cde6", "stroke-width": 8 }, cuffs);
      el("path", { d: "M472 900 h6", stroke: "#c9cde6", "stroke-width": 8 }, cuffs);
      const sa = at("L13", "Säulen"), en = at("L13", "entschuldigt"), l14 = line("L14")[0], ch = at("L14", "Chef"), hs = at("L14", "Handschellen");
      tl.to(G1.g, { x: 250, duration: sa - 0.2, ease: "none" }, 0.1);
      tl.to(G1.g, { x: 290, rotation: 8, svgOrigin: "0 238", duration: 0.15, ease: "power4.out" }, sa);
      stars.forEach((s, i) => tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.15, repeat: 3, yoyo: true }, sa + i * 0.08));
      tl.to(G2.g, { rotation: 25, svgOrigin: "0 238", duration: 0.3, yoyo: true, repeat: 1 }, en);
      tl.fromTo("#s06-b", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, en);
      tl.to(["#s06-b", G1.g, G2.g, vm, pil, ...stars], { opacity: 0, duration: 0.25 }, l14 - 0.15);
      tl.to(S2, { opacity: 1, duration: 0.25 }, l14 - 0.1);
      tl.to(SM.mouth, { attr: { d: "M-14 -26 q14 -10 28 0" }, duration: 0.15 }, ch);
      tl.fromTo(cuffs, { opacity: 0, scale: 1.6, svgOrigin: "475 900" }, { opacity: 1, scale: 1, svgOrigin: "475 900", duration: 0.2, ease: "back.out(3)" }, hs);
      tl.to(S2, { x: 6, duration: 0.04, repeat: 5, yoyo: true }, hs + 0.1);''' + OUT)

# ---------- s07 Hundert blinde Hände führen Sina hinaus ----------
S['s07'] = ('''    #s07-bg { background: #05060f; }
    #s07-exit { left: 760px; top: 450px; width: 260px; height: 90px; border-radius: 12px; background: #39e27a; color: #0b0e22; font-size: 48px; line-height: 90px; box-shadow: 0 0 50px rgba(57,226,122,.7); opacity: 0; }''',
'''      <div id="s07-bg" class="full"></div>
''' + SVG + '''
      <div id="s07-exit" class="panel">AUSGANG →</div>''',
'''      const P = person(sv, "s07-p", 300, 760, 1.0, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0", closed: true });
      const hands = [], r = rng(12);
      for (let i = 0; i < 14; i++) { const left = i % 2 === 0, y = 560 + Math.floor(i / 2) * 70, x = left ? -60 : 1140;
        const h = el("g", {}, sv); gsap.set(h, { x, y });
        el("rect", { x: left ? -400 : 0, y: -14, width: 400, height: 28, rx: 14, fill: ["#f2c9a5", "#d9a77f", "#b9835a"][i % 3] }, h);
        el("circle", { cx: left ? 10 : -10, cy: 0, r: 26, fill: ["#f2c9a5", "#d9a77f", "#b9835a"][i % 3] }, h);
        hands.push({ h, left }); }
      const gr = at("L15", "greifen"), fe = at("L15", "festzuhalten"), fu = at("L15", "führen"), hi = at("L15", "hinaus");
      hands.forEach(({ h, left }, i) => tl.to(h, { x: left ? 220 + (i % 4) * 20 : 860 - (i % 4) * 20, duration: 0.4, ease: "power3.out" }, gr - 0.2 + i * 0.05));
      tl.to(P.g, { y: 754, duration: 0.05, repeat: 5, yoyo: true }, fe);
      tl.fromTo("#s07-exit", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, fu - 0.1);
      tl.to(P.g, { x: 820, duration: hi - fu + 0.8, ease: "power1.inOut" }, fu);
      hands.forEach(({ h }, i) => tl.to(h, { x: "+=320", duration: hi - fu + 0.8, ease: "power1.inOut" }, fu + (i % 3) * 0.05));''' + OUT)

# ---------- s08 Draußen: Sendeturm – Spartakus hat das Signal gebaut ----------
S['s08'] = ('''    #s08-lab { left: 560px; top: 440px; width: 440px; height: 96px; border: 5px solid #ffd43b; color: #ffd43b; font-size: 50px; line-height: 86px; box-shadow: 0 0 40px rgba(255,212,59,.5); opacity: 0; }
    #s08-st { left: 140px; top: 460px; width: 800px; height: 130px; border: 7px solid #ff3b55; border-radius: 20px; color: #ff3b55; font-size: 68px; line-height: 116px; box-shadow: 0 0 50px rgba(255,59,85,.5); opacity: 0; }
    #s08-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 40%, rgba(160,0,20,.7) 100%); opacity: 0; }''',
SVG + '''
      <div id="s08-vig" class="full"></div>
      <div id="s08-lab" class="panel">SENDETURM</div><div id="s08-st" class="panel">ER HAT ES GEBAUT</div>''',
'''      const sky = el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#2a2350" }, sv);
      el("circle", { cx: 540, cy: 960, r: 150, fill: "#ff8a3d", opacity: 0.35 }, sv);
      [[0, 840, 220], [200, 800, 180], [700, 820, 200], [880, 850, 200]].forEach(([x, y, w]) => el("rect", { x, y, width: w, height: 1130 - y, fill: "#1c2250" }, sv));
      const T = tower(sv, 780, 1000, 0.8);
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#2a2f55" }, sv);
      const P = person(sv, "s08-p", 260, 780, 1.0, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const Sp = person(sv, "s08-s", 470, 770, 1.05, { shirt: "#39a06a", hair: "#2a2f55", arms: [12, -130] });
      const tear = el("ellipse", { cx: 488, cy: 712, rx: 6, ry: 10, fill: "#4da3ff", opacity: 0 }, sv);
      const se = at("L16", "Sendeturm"), um = at("L16", "umkehren"), l17 = line("L17")[0], ge = at("L17", "gebaut"), l33 = line("L33")[0], gi = at("L33", "geirrt");
      tl.to(sky, { fill: "#3a2d5c", duration: 3 }, 0);
      tl.to(T.lamp, { opacity: 0.2, duration: 0.25, repeat: 21, yoyo: true }, 0.2);
      tl.fromTo([P.g, Sp.g], { opacity: 0, x: "-=120" }, { opacity: 1, x: "+=120", duration: 0.5, ease: "expo.out" }, 0.1);
      tl.fromTo("#s08-lab", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, se - 0.05);
      tl.to(T.g, { scale: 0.86, svgOrigin: "780 1000", duration: 0.2, yoyo: true, repeat: 1 }, um);
      tl.to("#s08-lab", { opacity: 0, duration: 0.2 }, l17 - 0.1);
      tl.to(Sp.a2, { rotation: -12, duration: 0.3 }, l17);
      tl.to(P.eyes, { x: 7, duration: 0.2 }, l17);
      tl.fromTo("#s08-st", { opacity: 0, scale: 2, rotation: -10 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.25, ease: "power4.out" }, ge - 0.05);
      tl.to("#s08-vig", { opacity: 1, duration: 0.1 }, ge);
      tl.to(P.mouth, { attr: { d: "M-10 -30 q10 -12 20 0 q-10 12 -20 0" }, duration: 0.1 }, ge);
      tl.to(["#s08-st", "#s08-vig"], { opacity: 0, duration: 0.3 }, l33 + 0.9);
      tl.to(Sp.mouth, { attr: { d: "M-12 -26 q12 -10 24 0" }, duration: 0.2 }, l33);
      tl.to(Sp.eyes, { y: 6, duration: 0.3 }, l33);
      tl.fromTo(tear, { opacity: 1, attr: { cy: 712 } }, { opacity: 0, attr: { cy: 770 }, duration: 0.8, repeat: 1, immediateRender: false }, gi - 0.6);''' + OUT)

# ---------- s09 Turmspitze: Sammler hält Spartakus über die Kante ----------
S['s09'] = ('''    #s09-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 35%, rgba(160,0,20,.8) 100%); opacity: 0; }''',
SVG + '''
      <div id="s09-vig" class="full"></div>''',
'''      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#1a1f45" }, sv);
      const r = rng(2); for (let i = 0; i < 26; i++) el("rect", { x: r() * 1080, y: 980 + r() * 130, width: 8, height: 8, fill: "#ffe9a8", opacity: 0.6 }, sv);
      el("rect", { x: 0, y: 960, width: 780, height: 24, fill: "#5d6db8" }, sv);
      for (let i = 0; i < 16; i++) el("rect", { x: 10 + i * 48, y: 880, width: 8, height: 80, fill: "#5d6db8" }, sv);
      el("rect", { x: 0, y: 874, width: 780, height: 12, rx: 5, fill: "#5d6db8" }, sv);
      const mach = el("g", {}, sv);
      el("rect", { x: 380, y: 640, width: 220, height: 320, rx: 16, fill: "#2a2f55", stroke: "#8fa2ff", "stroke-width": 6 }, mach);
      const scr = el("rect", { x: 405, y: 670, width: 170, height: 100, rx: 8, fill: "#39e27a", opacity: 0.6 }, mach);
      el("rect", { x: 440, y: 800, width: 100, height: 120, rx: 14, fill: "#0b0e22", stroke: "#ffd43b", "stroke-width": 4 }, mach);
      el("path", { d: "M470 900 v-60 M490 900 v-74 M510 900 v-66 M530 900 v-50", stroke: "#ffd43b", "stroke-width": 8, "stroke-linecap": "round", opacity: 0.6 }, mach);
      const P = person(sv, "s09-p", 190, 720, 0.95, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const SM = sammler(sv, "s09-m", 740, 700, 1.15);
      gsap.set(SM.a1, { rotation: 70, svgOrigin: "-52 18" });
      const Sp = person(sv, "s09-s", 900, 720, 1.0, { shirt: "#39a06a", hair: "#2a2f55", arms: [150, -150] });
      gsap.set(Sp.g, { rotation: 18, svgOrigin: "900 900" });
      const beams = [0, 1].map((i) => el("path", { d: `M${120 + i * 200} 1130 L${60 + i * 200} 980 L${180 + i * 200} 980Z`, fill: "#ffe680", opacity: 0 }, sv));
      const sa = at("L18", "Sammler"), ka = at("L19", "Kante"), fa = at("L19", "fällt"), l34 = line("L34")[0], tr = at("L34", "Treppe");
      tl.to(scr, { opacity: 0.25, duration: 0.3, repeat: 25, yoyo: true }, 0);
      tl.fromTo([P.g, mach], { opacity: 0 }, { opacity: 1, duration: 0.4, stagger: 0.2 }, 0.1);
      tl.fromTo([SM.g, Sp.g], { opacity: 0 }, { opacity: 1, duration: 0.3 }, sa - 0.2);
      tl.to(Sp.g, { rotation: 32, svgOrigin: "900 900", duration: 0.4, ease: "power2.inOut" }, ka - 0.2);
      tl.to(Sp.g, { rotation: 26, svgOrigin: "900 900", duration: 0.2, repeat: 5, yoyo: true }, ka + 0.3);
      tl.to("#s09-vig", { opacity: 1, duration: 0.15 }, fa - 0.1);
      tl.to(P.g, { x: 210, duration: 0.3 }, fa - 0.6);
      tl.to(P.g, { x: 190, duration: 0.15 }, fa);
      tl.to(beams, { opacity: 0.5, duration: 0.2, stagger: 0.2 }, l34);
      tl.to(beams, { y: -60, duration: 0.5, repeat: 3, yoyo: true }, l34);
      tl.to("#s09-vig", { opacity: 0.5, duration: 0.4, repeat: 5, yoyo: true }, tr);''' + OUT)

# ---------- s10 Die Wahl: Hand auf die Maschine, weißes Licht, der Sammler erblindet ----------
S['s10'] = ('''    .s10-c { position: absolute; top: 560px; width: 440px; height: 260px; border-radius: 24px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; opacity: 0; }
    .s10-c .n { margin-top: 56px; font-size: 64px; line-height: 1; } .s10-c .w { margin-top: 20px; font-family: "Space Mono", monospace; font-size: 32px; letter-spacing: .1em; }
    #s10-a { left: 50px; background: #39a06a; color: #fff; box-shadow: 0 0 40px rgba(57,160,106,.6); } #s10-b { left: 590px; background: #2b6fd1; color: #fff; box-shadow: 0 0 40px rgba(77,163,255,.6); }
    #s10-or { position: absolute; left: 490px; top: 640px; width: 100px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 56px; color: #ffd43b; opacity: 0; }
    #s10-white { background: #fff; opacity: 0; }
    #s10-st { left: 240px; top: 470px; width: 600px; height: 120px; border: 7px solid #ff3b55; border-radius: 20px; color: #ff3b55; font-size: 72px; line-height: 106px; box-shadow: 0 0 50px rgba(255,59,85,.5); opacity: 0; }''',
SVG + '''
      <div id="s10-a" class="s10-c"><div class="n">SPARTAKUS</div><div class="w">1 MENSCH</div></div><div id="s10-or">?</div>
      <div id="s10-b" class="s10-c"><div class="n">8 MRD.</div><div class="w">DIE GANZE WELT</div></div>
      <div id="s10-white" class="full"></div><div id="s10-st" class="panel">FÜR IMMER</div>''',
'''      const hand = el("g", { opacity: 0 }, sv);
      el("rect", { x: 330, y: 560, width: 420, height: 520, rx: 30, fill: "#2a2f55", stroke: "#ffd43b", "stroke-width": 8 }, hand);
      const glow = el("rect", { x: 330, y: 560, width: 420, height: 520, rx: 30, fill: "#ffd43b", opacity: 0 }, hand);
      el("rect", { x: 420, y: 760, width: 240, height: 260, rx: 90, fill: "#f2c9a5" }, hand);
      [-84, -30, 24, 78].forEach((fx, k) => el("rect", { x: 540 + fx - 22, y: 600 + Math.abs(k - 1.5) * 26, width: 44, height: 200, rx: 22, fill: "#f2c9a5" }, hand));
      const SM = el("g", { opacity: 0 }, sv);
      const F = face(SM, 540, 800, 240, { hair: "#05060f", skin: "#c9b49a" });
      el("rect", { x: 300, y: 560, width: 480, height: 50, rx: 12, fill: "#05060f" }, SM); el("rect", { x: 380, y: 450, width: 320, height: 130, rx: 20, fill: "#05060f" }, SM);
      const l20 = line("L20")[0], ei = at("L20", "eine"), sp = at("L20", "Spartakus"), ac = at("L20", "acht"), l21 = line("L21")[0], ma = at("L21", "Maschine"),
            we = at("L22", "Weißes"), l23 = line("L23")[0], au = at("L23", "Augen"), im = at("L23", "immer");
      tl.fromTo("#s10-a", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)" }, sp - 0.1);
      tl.fromTo("#s10-or", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, sp + 0.4);
      tl.fromTo("#s10-b", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)" }, ac - 0.1);
      tl.to(".s10-c", { scale: 1.06, duration: 0.3, yoyo: true, repeat: 3, stagger: 0.15 }, ac + 0.4);
      tl.to([".s10-c", "#s10-or"], { opacity: 0, duration: 0.2 }, l21 - 0.15);
      tl.fromTo(hand, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, l21);
      tl.to(glow, { opacity: 0.8, duration: 0.3 }, ma);
      tl.to(hand, { x: 8, duration: 0.04, repeat: 7, yoyo: true }, ma);
      tl.fromTo("#s10-white", { opacity: 0 }, { opacity: 1, duration: 0.15 }, we - 0.05);
      tl.to(hand, { opacity: 0, duration: 0.01 }, we + 0.1);
      tl.to("#s10-white", { opacity: 0, duration: 0.8 }, l23 - 0.1);
      tl.to(SM, { opacity: 1, duration: 0.3 }, l23);
      tl.to(F.cloud, { opacity: 1, duration: 0.4 }, au - 0.1);
      tl.to(F.pup, { opacity: 0, duration: 0.4 }, au - 0.1);
      tl.to(SM, { x: 10, duration: 0.04, repeat: 9, yoyo: true }, au);
      tl.fromTo("#s10-st", { opacity: 0, scale: 2, rotation: -10 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.25, ease: "power4.out" }, im - 0.1);''' + OUT)

# ---------- s11 Morgen: alle sehen wieder (Rückblicke: Unterhose, Schal, Mülltonne) ----------
S['s11'] = ('''    #s11-box .num { font-size: 44px; }
    #s11-box { opacity: 0; }''',
'''      <div id="s11-box" class="cbox g"><div class="lab">SEHEN WIEDER</div><div id="s11-n" class="num">0</div></div>
''' + SVG,
'''      const sky = el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#2a2350" }, sv);
      const sun = el("circle", { cx: 540, cy: 1060, r: 130, fill: "#ffd43b", opacity: 0.8 }, sv);
      const A = el("g", {}, sv), eyes = [];
      for (let i = 0; i < 12; i++) { const e = bigEye(A, 140 + (i % 4) * 270, 560 + Math.floor(i / 4) * 170, 0.32); gsap.set(e.g, { scaleY: 0.05, transformOrigin: "50% 50%" }); eyes.push(e.g); }
      const B = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#3a3f5c" }, B);
      const M = person(B, "s11-m", 260, 790, 1.0, { shirt: "#e5e9f7", hair: "#5b3a26", pants: "#f2c9a5", arms: [10, -25] });
      el("path", { d: "M-34 112 h68 v40 h-68Z", fill: "#ff4fb0" }, M.g);
      gsap.set(M.eyes, { y: 6 });
      const blush = el("g", { opacity: 0 }, M.g); el("circle", { cx: -28, cy: -40, r: 10, fill: "#ff4fb0", opacity: 0.6 }, blush); el("circle", { cx: 28, cy: -40, r: 10, fill: "#ff4fb0", opacity: 0.6 }, blush);
      const O = person(B, "s11-o", 760, 800, 0.95, { shirt: "#ff8fb0", hair: "#d8dbe8", pants: "#5d4598", arms: [-40, 40] });
      el("circle", { cx: 0, cy: -118, r: 22, fill: "#d8dbe8" }, O.g);
      const scarf = el("path", { d: "M760 920 C880 960 980 880 1040 980 S900 1100 700 1060 S480 960 560 900", stroke: "#ff3b55", "stroke-width": 30, fill: "none", "stroke-linecap": "round", opacity: 0 }, B);
      const C2 = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#2a5a3a" }, C2);
      el("rect", { x: 380, y: 760, width: 210, height: 280, rx: 18, fill: "#2f7a4a" }, C2);
      el("rect", { x: 366, y: 740, width: 238, height: 36, rx: 10, fill: "#256a3e" }, C2);
      el("rect", { x: 600, y: 700, width: 6, height: 70, fill: "#39e27a" }, C2); el("circle", { cx: 603, cy: 696, r: 20, fill: "#ff4fb0" }, C2);
      const hrt = el("text", { x: 640, y: 690, "font-size": 70, fill: "#ff4fb0", opacity: 0 }, C2); hrt.textContent = "♥";
      const se = at("L24", "sehen"), l25 = line("L25")[0], un = at("L25", "Unterhose", 0), vi = at("L25", "vierzig"), l26 = line("L26")[0], zw = at("L26", "zweites");
      tl.to(sky, { fill: "#4a6fb8", duration: 3 }, 0);
      tl.to(sun, { attr: { cy: 990 }, duration: 3 }, 0);
      eyes.forEach((e, i) => tl.to(e, { scaleY: 1, transformOrigin: "50% 50%", duration: 0.25, ease: "back.out(2)" }, 0.5 + i * 0.12));
      tl.to("#s11-box", { opacity: 1, duration: 0.3 }, 0.4);
      count(tl, "#s11-n", 0, 8199999999, 0.5, se - 0.3, "", "", "power2.out");
      tl.to(A, { opacity: 0, duration: 0.25 }, l25 - 0.2);
      tl.to(B, { opacity: 1, duration: 0.25 }, l25 - 0.1);
      tl.to(blush, { opacity: 1, duration: 0.2 }, un + 0.6);
      tl.to(M.mouth, { attr: { d: "M-10 -30 q10 -12 20 0 q-10 12 -20 0" }, duration: 0.1 }, un + 0.6);
      tl.to(scarf, { opacity: 1, duration: 0.2 }, vi - 0.2);
      tl.to(O.mouth, { attr: { d: "M-12 -32 q12 14 24 0" }, duration: 0.1 }, vi);
      tl.to(B, { opacity: 0, duration: 0.25 }, l26 - 0.2);
      tl.to(C2, { opacity: 1, duration: 0.25 }, l26 - 0.1);
      tl.fromTo(hrt, { opacity: 0, y: 0 }, { opacity: 1, y: -50, duration: 0.6 }, zw - 0.1);''' + OUT)

# ---------- s12 Nur Sina sieht nichts mehr – "Sieht ja keiner." ----------
S['s12'] = ('''    .stamp { position: absolute; left: 190px; top: 470px; width: 700px; height: 130px; border: 7px solid #39e27a; border-radius: 20px; color: #39e27a;
      font-family: "Inter", sans-serif; font-weight: 900; font-size: 72px; line-height: 116px; text-align: center; background: rgba(8,30,18,.85);
      box-shadow: 0 0 50px rgba(57,226,122,.5); opacity: 0; }''',
SVG + '''
      <div id="s12-st" class="stamp">SIEHT JA KEINER</div>''',
'''      el("rect", { x: 0, y: 420, width: 1080, height: 710, fill: "#3a4f8f" }, sv);
      el("circle", { cx: 860, cy: 560, r: 90, fill: "#ffd43b", opacity: 0.85 }, sv);
      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#2a5a3a" }, sv);
      el("rect", { x: 220, y: 900, width: 640, height: 28, rx: 10, fill: "#a86b2c" }, sv);
      el("rect", { x: 220, y: 840, width: 640, height: 22, rx: 8, fill: "#a86b2c" }, sv);
      [250, 830].forEach((x) => el("rect", { x, y: 928, width: 22, height: 112, fill: "#6b3f1d" }, sv));
      const P = person(sv, "s12-p", 430, 720, 1.05, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0", arms: [12, -40] });
      const cl = el("g", { opacity: 0 }, P.g);
      [-16, 16].forEach((cx) => { el("circle", { cx, cy: -56, r: 9, fill: "#e4e8f6" }, cl); el("circle", { cx, cy: -56, r: 5, fill: "#b4bbd6" }, cl); });
      const Sp = person(sv, "s12-s", 650, 710, 1.1, { shirt: "#39a06a", hair: "#2a2f55", arms: [40, -12] });
      const tears = [el("ellipse", { cx: 414, cy: 662, rx: 6, ry: 10, fill: "#4da3ff", opacity: 0 }, sv), el("ellipse", { cx: 448, cy: 662, rx: 6, ry: 10, fill: "#4da3ff", opacity: 0 }, sv)];
      const hrt = el("text", { x: 520, y: 640, "font-size": 70, fill: "#ff4fb0", opacity: 0 }, sv); hrt.textContent = "♥";
      const ni = at("L27", "nichts"), si = at("L28", "Sina"), ge = at("L28", "genommen"), l29 = line("L29")[0], we = at("L29", "weinst"), l30 = line("L30")[0], la = at("L30", "lächelt"), sj = at("L30", "Sieht");
      tl.fromTo([P.g, Sp.g], { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0.1);
      tl.to(P.eyes, { opacity: 0, duration: 0.6 }, ge - 0.3);
      tl.to(cl, { opacity: 1, duration: 0.6 }, ge - 0.3);
      tl.to(Sp.a1, { rotation: 55, duration: 0.5, ease: "power2.inOut" }, l29);
      tl.to(P.a2, { rotation: -60, duration: 0.5, ease: "power2.inOut" }, l29);
      tears.forEach((t, i) => tl.fromTo(t, { opacity: 1, attr: { cy: 662 } }, { opacity: 0, attr: { cy: 720 }, duration: 0.9, repeat: 1, immediateRender: false }, we - 0.3 + i * 0.3));
      tl.to(P.mouth, { attr: { d: "M-14 -32 q14 16 28 0" }, duration: 0.2 }, la);
      tl.fromTo("#s12-st", { opacity: 0, scale: 2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.25, ease: "power4.out" }, sj - 0.05);
      tl.fromTo(hrt, { opacity: 0, y: 0 }, { opacity: 1, y: -60, duration: 0.8 }, sj + 0.3);''' + OUT)

# ---------- s13 Ende: Wie hat dir das Finale gefallen? + Folgen (letzte Szene, kein Blur-Out) ----------
S['s13'] = ('''    #s13-bg { background: #000; }
    #s13-cta { left: 90px; top: 470px; width: 900px; height: 600px; border: 6px solid #ff4fb0; box-shadow: 0 0 70px rgba(255,79,176,.5); opacity: 0; }
    #s13-cta .a { margin-top: 300px; font-size: 54px; line-height: 1.1; color: #fff; }
    #s13-btn { position: absolute; left: 290px; top: 440px; width: 320px; height: 100px; border-radius: 50px; background: #ff4fb0; color: #fff; font-size: 54px; line-height: 100px; }
    #s13-tag { position: absolute; left: 500px; top: 36px; width: 360px; height: 76px; white-space: nowrap; border-radius: 14px; background: #ffd43b; color: #0b0e22; font-size: 36px; line-height: 76px; transform: rotate(6deg); }
    .s13-s { position: absolute; top: 640px; width: 150px; text-align: center; font-size: 120px; color: #ffd43b; text-shadow: 0 0 30px rgba(255,212,59,.6); opacity: 0; }''',
'''      <div id="s13-bg" class="full"></div>
      <div class="s13-s" style="left:165px">★</div><div class="s13-s" style="left:315px">★</div><div class="s13-s" style="left:465px">★</div><div class="s13-s" style="left:615px">★</div><div class="s13-s" style="left:765px">★</div>
      <div id="s13-cta" class="panel"><div id="s13-tag">NÄCHSTE STORY</div><div class="a">DANKE FÜRS<br>MITFIEBERN!</div><div id="s13-btn">+ FOLGEN</div></div>
''' + SVG,
'''      const E = bigEye(sv, 540, 640, 0.75); gsap.set(E.g, { opacity: 0 });
      const fi = at("L31", "Finale"), l32 = line("L32")[0], fo = at("L32", "folge");
      tl.fromTo(".s13-s", { opacity: 0, scale: 0.3, rotation: -40 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.35, stagger: 0.12, ease: "back.out(3)" }, fi - 0.1);
      tl.to(".s13-s", { opacity: 0, duration: 0.25 }, l32 - 0.25);
      tl.fromTo("#s13-cta", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, l32 - 0.1);
      tl.to(E.g, { opacity: 1, duration: 0.3 }, l32);
      tl.fromTo("#s13-btn", { scale: 1 }, { scale: 1.15, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }, fo);''')

HEAD = HEAD.replace("/*__COMMON_JS__*/", "/*__COMMON_JS__*/" + EXTRA_JS)


here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
