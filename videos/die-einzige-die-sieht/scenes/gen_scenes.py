#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s13 für „Die Einzige, die sieht“ (hier ändern und neu erzeugen)."""
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

# ---------- s01 Hook: Eilmeldung, leuchtendes Auge, Menge ----------
S['s01'] = ('''    #s01-news { left: 60px; top: 690px; width: 960px; height: 420px; border: 5px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.45); overflow: hidden; text-align: left; }
    #s01-news .bar { height: 84px; background: #ff3b55; color: #fff; display: flex; align-items: center; padding-left: 34px; font-size: 44px; letter-spacing: .06em; }
    #s01-news .hl { padding: 22px 40px 0; font-size: 84px; line-height: 1.04; letter-spacing: -.015em; }
    #s01-news .hl em { font-style: normal; color: #ffd43b; text-shadow: 0 0 26px rgba(255,212,59,.6); }
    #s01-dark { background: #05060f; opacity: 0; }''',
'''      <div id="s01-dark" class="full"></div>
''' + SVG + '''
      <div id="s01-news" class="panel"><div class="bar">● EILMELDUNG · LIVE</div><div class="hl">8 MILLIARDEN MENSCHEN ÜBER NACHT <em>BLIND</em></div></div>''',
'''      const E = bigEye(sv, 540, 560, 0.9);
      const crowd = el("g", {}, sv), r = rng(3), ms = [];
      for (let row = 0; row < 4; row++) for (let i = 0; i < 9; i++) {
        const x = 90 + i * 112 + (row % 2) * 50 + (r() - 0.5) * 20, y = 820 + row * 78;
        const hero = row === 1 && i === 4;
        ms.push(mini(crowd, hero ? 540 : x, y, hero ? "#ff4fb0" : ["#3a4280", "#47508f", "#2f366e"][(i + row) % 3], hero));
      }
      const beam = el("path", { d: "M540 1130 L380 520 L700 520Z", fill: "#ffd43b", opacity: 0 }, sv);
      const q = el("text", { x: 540, y: 820, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 260, fill: "#ff3b55", opacity: 0 }, sv); q.textContent = "?";
      const ein = at("L1", "einzige"), acht = at("L2", "Acht"), erb = at("L2", "erblindet"), l3 = line("L3")[0], unm = at("L3", "unmöglich");
      tl.fromTo(E.g, { filter: "drop-shadow(0 0 20px rgba(255,212,59,.5))" }, { filter: "drop-shadow(0 0 60px rgba(255,212,59,.9))", duration: 0.35, repeat: 5, yoyo: true }, 0);
      tl.fromTo("#s01-news", { scale: 1.06 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);
      tl.to("#s01-news", { x: 8, duration: 0.04, repeat: 5, yoyo: true }, 0.9);
      tl.to("#s01-news", { opacity: 0, y: 160, duration: 0.3, ease: "power3.in" }, acht - 0.4);
      tl.to(E.g, { scale: 1.1, duration: 0.6, ease: "expo.out" }, ein - 0.1);
      tl.to(E.iris, { x: -80, duration: 0.3, ease: "power2.inOut" }, ein + 0.6);
      tl.to(E.iris, { x: 80, duration: 0.4, ease: "power2.inOut" }, ein + 1.0);
      tl.to(E.iris, { x: 0, duration: 0.3, ease: "power2.inOut" }, ein + 1.5);
      tl.to(E.g, { y: 600, scale: 0.85, duration: 0.45, ease: "power3.inOut" }, acht - 0.35);
      ms.forEach((m, i) => tl.fromTo(m, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, acht - 0.1 + (i % 9) * 0.03 + Math.floor(i / 9) * 0.06));
      tl.to(ms.filter((_, i) => i !== 13), { opacity: 0.45, duration: 0.3 }, erb);
      tl.fromTo(ms[13], { scale: 1 }, { scale: 1.35, svgOrigin: "540 880", duration: 0.25, yoyo: true, repeat: 1 }, erb);
      tl.to("#s01-dark", { opacity: 0.85, duration: 0.5 }, l3 - 0.1);
      tl.to([crowd, E.g], { opacity: 0, duration: 0.4 }, l3 - 0.1);
      tl.to(beam, { opacity: 0.35, duration: 0.2 }, l3 + 0.5);
      tl.fromTo(beam, { rotation: -25 }, { rotation: 25, svgOrigin: "540 1130", duration: 1.4, ease: "sine.inOut" }, l3 + 0.5);
      tl.to(beam, { opacity: 0, duration: 0.2 }, unm - 0.2);
      tl.fromTo(q, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.4)" }, unm - 0.1);
      tl.to(q, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, unm + 0.3);''' + OUT)


# ---------- s02 Schlafzimmer: Sina wacht auf ----------
S['s02'] = ('''    #s02-name { left: 640px; top: 450px; width: 360px; height: 120px; border: 4px solid #ff4fb0; box-shadow: 0 0 30px rgba(255,79,176,.4); opacity: 0; }
    #s02-name .a { margin-top: 12px; font-size: 52px; color: #ff4fb0; } #s02-name .b { font-size: 30px; color: #dfe2f5; letter-spacing: .14em; font-family: "Space Mono", monospace; }''',
SVG + '''
      <div id="s02-name" class="panel"><div class="a">SINA</div><div class="b">27 JAHRE</div></div>''',
'''      const win = el("g", {}, sv);
      el("rect", { x: 110, y: 480, width: 280, height: 320, rx: 14, fill: "#6d55a8" }, win);
      const glass = el("rect", { x: 130, y: 500, width: 240, height: 280, rx: 8, fill: "#9db4ff" }, win);
      el("path", { d: "M250 500 V780 M130 640 H370", stroke: "#6d55a8", "stroke-width": 12 }, win);
      const red = el("rect", { x: 130, y: 500, width: 240, height: 280, rx: 8, fill: "#ff3b55", opacity: 0 }, win);
      const P = person(sv, "s02-p", 600, 760, 1.15, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0", closed: true, arms: [10, -10] });
      el("rect", { x: 300, y: 905, width: 640, height: 150, rx: 30, fill: "#4a3f9a" }, sv);
      el("rect", { x: 300, y: 905, width: 640, height: 40, rx: 20, fill: "#5d52b8" }, sv);
      el("rect", { x: 940, y: 960, width: 110, height: 140, rx: 12, fill: "#6b3f1d" }, sv);
      const clk = el("g", {}, sv);
      el("circle", { cx: 995, cy: 905, r: 52, fill: "#ff3b55" }, clk); el("circle", { cx: 995, cy: 905, r: 40, fill: "#f3f1ea" }, clk);
      el("path", { d: "M995 905 V875 M995 905 L1015 912", stroke: "#161a36", "stroke-width": 6, "stroke-linecap": "round" }, clk);
      const rings = ["#39e27a", "#ffd43b", "#4da3ff", "#ff4fb0"].map((c, i) => el("circle", { cx: 600, cy: 693, r: 60, fill: "none", stroke: c, "stroke-width": 12, opacity: 0 }, sv));
      const ex = el("text", { x: 690, y: 600, "font-family": "Inter", "font-weight": 900, "font-size": 120, fill: "#ff3b55", opacity: 0 }, sv); ex.textContent = "!";
      const sina = at("L4", "Sina"), wk = at("L4", "27"), auf = at("L4", "Augen"), sch = at("L4", "scharf"), schr = at("L6", "Schreie");
      tl.fromTo(P.g, { opacity: 0, y: 820 }, { opacity: 1, y: 760, duration: 0.5, ease: "expo.out" }, 0.05);
      tl.fromTo("#s02-name", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)" }, sina);
      tl.to(clk, { rotation: 10, svgOrigin: "995 950", duration: 0.05, repeat: 15, yoyo: true }, wk);
      tl.to("#s02-name", { opacity: 0, duration: 0.2 }, auf - 0.3);
      tl.to(P.lids, { opacity: 0, duration: 0.05 }, auf);
      tl.to(P.eyes, { opacity: 1, duration: 0.05 }, auf);
      tl.fromTo(P.eyes, { scaleY: 0.2, svgOrigin: "0 -56" }, { scaleY: 1, svgOrigin: "0 -56", duration: 0.25, ease: "back.out(3)" }, auf);
      [sch, sch + 0.2, sch + 0.4, sch + 0.6].forEach((t, i) => tl.set(rings[i], { opacity: 1 }, t).to(rings[i], { attr: { r: 380 }, opacity: 0, duration: 0.7, ease: "power2.out" }, t));
      tl.to(glass, { fill: "#ffe9a8", duration: 0.4 }, sch);
      tl.to(red, { opacity: 0.8, duration: 0.08, repeat: 5, yoyo: true }, schr);
      tl.to(P.g, { x: 610, duration: 0.04, repeat: 7, yoyo: true }, schr);
      tl.to(P.mouth, { attr: { d: "M-10 -30 q10 -10 20 0 q-10 10 -20 0" }, duration: 0.1 }, schr);
      tl.fromTo(ex, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, svgOrigin: "710 560", duration: 0.3, ease: "back.out(3)" }, schr);''' + OUT)


# ---------- s03 Straße: Mann im Bademantel, Hund will zur Metzgerei ----------
S['s03'] = ('''    #s03-box .num { font-size: 44px; }
    #s03-sign { left: 700px; top: 560px; width: 340px; height: 84px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 44px; line-height: 74px;
      box-shadow: 0 0 40px rgba(255,59,85,.5); opacity: 0; }''',
'''      <div id="s03-box" class="cbox r"><div class="lab">ERBLINDET</div><div id="s03-n" class="num">0</div></div>
''' + SVG + '''
      <div id="s03-sign" class="panel">METZGEREI</div>''',
'''      const city = el("g", {}, sv);
      [[40, 600, 200, 400], [260, 540, 220, 460], [500, 620, 180, 380]].forEach(([x, y, w, h], i) => {
        el("rect", { x, y, width: w, height: h, fill: ["#232a5a", "#2b3368", "#1f2550"][i] }, city);
        for (let r = 0; r < 4; r++) for (let c = 0; c < 2; c++) el("rect", { x: x + 30 + c * (w / 2 - 10), y: y + 40 + r * 80, width: 40, height: 44, rx: 4, fill: "#151a3d" }, city); });
      const shop = el("g", {}, sv);
      el("rect", { x: 720, y: 660, width: 300, height: 340, fill: "#3a3f7a" }, shop);
      for (let i = 0; i < 6; i++) el("rect", { x: 720 + i * 50, y: 660, width: 50, height: 60, fill: i % 2 ? "#f3f1ea" : "#ff3b55" }, shop);
      el("rect", { x: 750, y: 760, width: 240, height: 150, rx: 10, fill: "#a9d2ff" }, shop);
      const saus = [0, 1, 2, 3].map((i) => el("rect", { x: 768 + i * 56, y: 780, width: 34, height: 110, rx: 17, fill: "#e46a7a" }, shop));
      el("rect", { x: 0, y: 1000, width: 1080, height: 130, fill: "#3a3f5c" }, sv);
      const pair = el("g", {}, sv);
      const M = person(pair, "s03-m", 300, 712, 1.0, { blind: true, shirt: "#e5e9f7", hair: "#8a8fa8", pants: "#c9cde6", arms: [12, -60] });
      el("path", { d: "M-40 70 h80", stroke: "#9aa1c4", "stroke-width": 8 }, M.g);
      const dog = el("g", {}, pair); gsap.set(dog, { x: 600, y: 930 });
      const tail = el("path", { d: "M-70 -10 q-40 -30 -30 -70", stroke: "#a86b2c", "stroke-width": 14, fill: "none", "stroke-linecap": "round" }, dog);
      el("ellipse", { cx: 0, cy: 0, rx: 80, ry: 40, fill: "#a86b2c" }, dog);
      [-50, -25, 30, 55].forEach((x) => el("rect", { x: x - 8, y: 20, width: 16, height: 54, rx: 8, fill: "#8a5a2b" }, dog));
      el("circle", { cx: 84, cy: -36, r: 36, fill: "#a86b2c" }, dog);
      el("ellipse", { cx: 118, cy: -26, rx: 22, ry: 15, fill: "#c98a4a" }, dog);
      el("circle", { cx: 136, cy: -30, r: 7, fill: "#161a36" }, dog);
      el("circle", { cx: 92, cy: -44, r: 6, fill: "#161a36" }, dog);
      el("path", { d: "M62 -62 q-14 30 6 44Z", fill: "#6b3f1d" }, dog);
      el("rect", { x: 60, y: -16, width: 40, height: 10, rx: 5, fill: "#ff3b55" }, dog);
      el("path", { d: "M439 780 Q560 850 680 920", stroke: "#ff3b55", "stroke-width": 6, fill: "none" }, pair);
      const nose = el("g", { opacity: 0 }, sv);
      [0, 1, 2].forEach((i) => el("path", { d: `M${760 + i * 26} ${860 - i * 22} q14 -14 0 -28`, stroke: "#ffd43b", "stroke-width": 7, fill: "none", "stroke-linecap": "round" }, nose));
      const ma = at("L8", "Mann"), hu = at("L8", "Hund"), zi = at("L8", "Ziel"), me = at("L8", "Metzgerei");
      tl.from(city, { y: 40, opacity: 0, duration: 0.5, ease: "expo.out" }, 0);
      count(tl, "#s03-n", 0, 8199999999, 0.1, me - 0.2, "", "", "power2.out");
      tl.fromTo(pair, { x: -400 }, { x: 0, duration: 0.8, ease: "power2.out" }, ma - 0.2);
      tl.to(M.g, { y: 718, duration: 0.15, repeat: 7, yoyo: true }, ma - 0.2);
      tl.to(tail, { rotation: 25, svgOrigin: "-70 -10", duration: 0.1, repeat: 15, yoyo: true }, hu);
      tl.fromTo(dog, { rotation: 0 }, { rotation: -6, svgOrigin: "0 40", duration: 0.12, repeat: 7, yoyo: true }, hu);
      tl.to(nose, { opacity: 1, duration: 0.15, repeat: 5, yoyo: true }, zi - 0.1);
      tl.fromTo("#s03-sign", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, me - 0.1);
      tl.to(saus, { y: -10, duration: 0.12, repeat: 5, yoyo: true, stagger: 0.05 }, me);
      tl.to(pair, { x: 260, duration: 0.6, ease: "power3.in" }, me + 0.1);
      tl.to(M.g, { rotation: 12, svgOrigin: "0 238", duration: 0.3 }, me + 0.1);''' + OUT)

# ---------- s04 Radio: die Meldung ----------
S['s04'] = ('''    .s04-st { position: absolute; left: 120px; top: 470px; width: 840px; height: 180px; border: 7px solid #ff3b55; border-radius: 20px;
      color: #ff3b55; font-family: "Inter", sans-serif; font-weight: 900; font-size: 96px; line-height: 166px; text-align: center;
      background: rgba(13,16,38,.92); box-shadow: 0 0 50px rgba(255,59,85,.45); opacity: 0; }''',
SVG + '''
      <div id="s04-a" class="s04-st" style="background:#ff3b55;color:#fff">EILMELDUNG</div><div id="s04-b" class="s04-st">WELTWEIT</div><div id="s04-c" class="s04-st">ALLE</div>
      <div id="s04-d" class="s04-st">ERBLINDET</div><div id="s04-e" class="s04-st" style="font-size:80px">OHNE AUSNAHME</div><div id="s04-f" class="s04-st" style="font-size:64px;color:#ffd43b;border-color:#ffd43b">BLEIBEN SIE ZU HAUSE</div>''',
'''      const R = radio(sv, 540, 900, 1.05);
      const waves = [0, 1, 2].map((i) => el("path", { d: `M${880 + i * 40} ${760 - i * 30} q40 60 0 120`, fill: "none", stroke: "#ffd43b", "stroke-width": 10, "stroke-linecap": "round", opacity: 0 }, sv));
      const T = [["#s04-a", at("L10", "Eilmeldung")], ["#s04-b", at("L10", "weltweit")], ["#s04-d", at("L10", "erblindet")], ["#s04-e", at("L10", "Ausnahme")], ["#s04-f", at("L10", "Bleiben")]];
      tl.fromTo(R.g, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1.05, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.to(R.needle, { x: 120, duration: 0.6, ease: "power2.inOut" }, 0.1);
      waves.forEach((w, i) => tl.fromTo(w, { opacity: 0 }, { opacity: 1, duration: 0.3, repeat: 15, yoyo: true }, 0.4 + i * 0.12));
      T.forEach(([s, t], i) => {
        tl.fromTo(s, { opacity: 0, scale: 1.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: [-4, 3, 4, -3, 2][i], duration: 0.22, ease: "power4.out" }, t - 0.05);
        if (i < T.length - 1) tl.to(s, { opacity: 0, duration: 0.12 }, T[i + 1][1] - 0.08); });
      tl.to(R.g, { x: "+=8", duration: 0.04, repeat: 5, yoyo: true }, T[3][1]);''' + OUT)

# ---------- s05 Tom an der Tür, Durchsage, Lüge ----------
S['s05'] = ('''    #s05-b1 { left: 70px; top: 440px; width: 480px; }
    #s05-b2 { left: 560px; top: 440px; width: 440px; background: #ff4fb0; color: #fff; }
    #s05-alert { left: 70px; top: 430px; width: 940px; height: 260px; border: 6px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.5); overflow: hidden; opacity: 0; }
    #s05-alert .bar { height: 70px; background: #ff3b55; font-size: 38px; line-height: 70px; letter-spacing: .08em; }
    #s05-alert .t { margin-top: 26px; font-size: 56px; line-height: 1.12; } #s05-alert em { font-style: normal; color: #ff3b55; }''',
SVG + '''
      <div id="s05-b1" class="bub">„SINA? KANNST DU WAS SEHEN?“</div>
      <div id="s05-b2" class="bub">„NEIN. ICH SEHE NICHTS.“</div>
      <div id="s05-alert" class="panel"><div class="bar">DURCHSAGE · RADIO</div><div class="t">SEHENDE MENSCHEN<br>WERDEN <em>ABGEHOLT</em></div></div>''',
'''      el("rect", { x: 110, y: 560, width: 380, height: 540, rx: 10, fill: "#5e3b1a" }, sv);
      el("rect", { x: 130, y: 580, width: 340, height: 520, fill: "#0b0e22" }, sv);
      const door = el("rect", { x: 130, y: 580, width: 340, height: 520, fill: "#8a5a2b" }, sv);
      const T = person(sv, "s05-t", 300, 780, 1.1, { blind: true, shirt: "#4da3ff", hair: "#2a2f55", arms: [70, -70] });
      gsap.set(T.g, { opacity: 0 });
      const P = person(sv, "s05-p", 790, 780, 1.1, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const sweat = el("path", { d: "M850 650 q-14 22 0 30 q14 -8 0 -30Z", fill: "#a9d2ff", opacity: 0 }, sv);
      const kl = at("L12", "klopft"), tom = at("L12", "Alex"), sn = at("L12", "Sina"), ja = at("L13", "Da"), du = at("L13", "Durchsage"), ab = at("L14", "abgeholt"), l15 = line("L15")[0], nein = at("L15", "Nein");
      tl.fromTo(P.g, { opacity: 0, x: 860 }, { opacity: 1, x: 790, duration: 0.4, ease: "expo.out" }, 0.05);
      tl.to(door, { x: 6, duration: 0.05, repeat: 5, yoyo: true }, kl);
      tl.to(door, { scaleX: 0.08, svgOrigin: "130 840", duration: 0.4, ease: "power2.inOut" }, tom - 0.35);
      tl.fromTo(T.g, { opacity: 0, x: 260 }, { opacity: 1, x: 300, duration: 0.4, ease: "power2.out" }, tom - 0.15);
      tl.fromTo("#s05-b1", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, sn - 0.05);
      tl.to(P.mouth, { attr: { d: "M-12 -32 q12 14 24 0" }, duration: 0.15 }, ja - 0.1);
      tl.to("#s05-b1", { opacity: 0, duration: 0.2 }, du - 0.2);
      tl.fromTo("#s05-alert", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, du);
      tl.to("#s05-alert", { x: 10, duration: 0.04, repeat: 7, yoyo: true }, ab);
      tl.to(P.mouth, { attr: { d: "M-12 -26 q12 -10 24 0" }, duration: 0.15 }, ab);
      tl.to(P.eyes, { y: 5, duration: 0.2 }, ab);
      tl.to(sweat, { opacity: 1, y: 30, duration: 0.6 }, ab + 0.1);
      tl.to("#s05-alert", { opacity: 0, duration: 0.25 }, l15 - 0.1);
      tl.fromTo("#s05-b2", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, nein - 0.05);''' + OUT)


# ---------- s06 Warum: wertvoll, Banden, Labor, kein Zurück ----------
S['s06'] = ('''    .s06-lab { left: 260px; width: 560px; height: 96px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 52px; line-height: 86px;
      box-shadow: 0 0 40px rgba(255,59,85,.5); opacity: 0; }
    #s06-val { top: 450px; border-color: #ffd43b; color: #ffd43b; box-shadow: 0 0 40px rgba(255,212,59,.5); }
    #s06-gang { top: 450px; } #s06-lab2 { top: 450px; } #s06-back { top: 1010px; left: 200px; width: 680px; }''',
SVG + '''
      <div id="s06-val" class="panel s06-lab">UNBEZAHLBAR</div><div id="s06-gang" class="panel s06-lab">BANDEN</div>
      <div id="s06-lab2" class="panel s06-lab">LABOR</div><div id="s06-back" class="panel s06-lab">KEIN ZURÜCK</div>''',
'''      const E = bigEye(sv, 540, 780, 1.0);
      const sp = [[300, 640], [800, 620], [820, 930], [270, 920]].map(([x, y]) => el("path", { d: `M${x} ${y - 30} l9 21 l21 9 l-21 9 l-9 21 l-9 -21 l-21 -9 l21 -9Z`, fill: "#ffd43b", opacity: 0 }, sv));
      const gang = el("g", { opacity: 0 }, sv), G = [];
      [[300, 1.0], [540, 1.1], [780, 1.0]].forEach(([x, s], i) => { const p = person(gang, "s06-g" + i, x, 720 - (s - 1) * 60, s, { blind: true, shirt: "#2a2f55", hair: "#161a36", pants: "#161a36", arms: [16, -16] });
        el("rect", { x: -48, y: -96, width: 96, height: 30, rx: 10, fill: "#161a36" }, p.g); G.push(p); });
      const bag = el("g", { opacity: 0 }, sv);
      el("circle", { cx: 880, cy: 900, r: 70, fill: "#8a5a2b" }, bag); el("path", { d: "M850 836 l30 -30 l30 30Z", fill: "#6b3f1d" }, bag);
      const lab = el("g", { opacity: 0 }, sv);
      el("rect", { x: 380, y: 600, width: 320, height: 420, rx: 40, fill: "#a9d2ff", opacity: 0.35 }, lab);
      el("rect", { x: 360, y: 580, width: 360, height: 40, rx: 12, fill: "#c9cde6" }, lab);
      el("rect", { x: 360, y: 1010, width: 360, height: 40, rx: 12, fill: "#c9cde6" }, lab);
      const bub = [0, 1, 2, 3].map((i) => el("circle", { cx: 450 + i * 60, cy: 980, r: 10 + (i % 2) * 6, fill: "#e5e9f7", opacity: 0.7 }, lab));
      const E2 = bigEye(lab, 540, 800, 0.5);
      const van = el("g", { opacity: 0 }, sv);
      el("rect", { x: 260, y: 700, width: 480, height: 240, rx: 30, fill: "#e5e9f7" }, van);
      el("path", { d: "M740 740 L840 790 L840 940 L740 940Z", fill: "#e5e9f7" }, van);
      el("path", { d: "M746 752 L828 794 L828 850 L746 850Z", fill: "#161a36" }, van);
      el("rect", { x: 260, y: 840, width: 580, height: 22, fill: "#ff3b55" }, van);
      [360, 760].forEach((x) => el("circle", { cx: x, cy: 950, r: 46, fill: "#161a36" }, van));
      const we = at("L16", "Wertvollste"), l17 = line("L17")[0], ba = at("L17", "Banden"), ra = at("L17", "Raubzüge"), l18 = line("L18")[0], lb = at("L18", "Labor"), l19 = line("L19")[0], ni = at("L19", "nicht");
      tl.fromTo(E.g, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.05);
      tl.fromTo("#s06-val", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, we - 0.05);
      sp.forEach((s, i) => tl.fromTo(s, { opacity: 0, scale: 0.3, svgOrigin: s.getAttribute("d").slice(1).split(" ").slice(0, 2).join(" ") }, { opacity: 1, scale: 1.3, duration: 0.25, repeat: 3, yoyo: true }, we + i * 0.08));
      tl.to([E.g, "#s06-val"], { opacity: 0, duration: 0.2 }, l17 - 0.15);
      tl.fromTo(gang, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, l17 - 0.05);
      tl.fromTo("#s06-gang", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, ba);
      G.forEach((p, i) => tl.to(p.a2, { rotation: -100, duration: 0.25, ease: "back.out(2)" }, ba + 0.3 + i * 0.1));
      tl.fromTo(bag, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.3, ease: "bounce.out" }, ra - 0.2);
      tl.to([gang, bag, "#s06-gang"], { opacity: 0, duration: 0.2 }, l18 - 0.15);
      tl.fromTo(lab, { opacity: 0, scale: 0.8, svgOrigin: "540 800" }, { opacity: 1, scale: 1, svgOrigin: "540 800", duration: 0.35, ease: "back.out(1.8)" }, l18);
      tl.to(bub, { attr: { cy: 640 }, opacity: 0, duration: 1.2, stagger: 0.15, ease: "power1.in" }, l18 + 0.2);
      tl.fromTo("#s06-lab2", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, lb - 0.05);
      tl.to(E2.iris, { x: -50, duration: 0.25, repeat: 3, yoyo: true }, lb);
      tl.to([lab, "#s06-lab2"], { opacity: 0, duration: 0.2 }, l19 - 0.15);
      tl.fromTo(van, { opacity: 0 }, { opacity: 1, duration: 0.2 }, l19);
      tl.to(van, { x: 900, duration: 0.8, ease: "power2.in" }, ni);
      tl.fromTo("#s06-back", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, ni);''' + OUT)

# ---------- s07 Regel 1: niemals ausweichen ----------
S['s07'] = ('''    #s07-lab { left: 300px; top: 470px; width: 480px; height: 96px; border: 5px solid #ff3b55; color: #ff3b55; font-size: 52px; line-height: 86px;
      box-shadow: 0 0 40px rgba(255,59,85,.5); opacity: 0; }
    #s07-bum { left: 380px; top: 560px; width: 320px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 96px; color: #ffd43b;
      text-shadow: 0 0 30px rgba(255,212,59,.5), 0 6px 0 rgba(0,0,0,.5); opacity: 0; }''',
'''      <div id="s07-rule" class="rule">REGEL 1</div>
''' + SVG + '''
      <div id="s07-bum" class="abs">BUMM!</div><div id="s07-lab" class="panel">VERDÄCHTIG</div>''',
'''      el("rect", { x: 0, y: 1040, width: 1080, height: 90, fill: "#2a2f55" }, sv);
      const A = person(sv, "s07-a", 160, 790, 1.0, { blind: true, shirt: "#39a06a", hair: "#161a36", arms: [80, -80] });
      const B = person(sv, "s07-b", 920, 790, 1.0, { blind: true, shirt: "#4da3ff", hair: "#e0a35a", arms: [80, -80] });
      const P = person(sv, "s07-p", 160, 790, 1.0, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" }); gsap.set(P.g, { opacity: 0 });
      const trail = el("path", { d: "M300 900 Q540 640 780 900", stroke: "#ffd43b", "stroke-width": 7, "stroke-dasharray": "18 14", fill: "none", opacity: 0 }, sv);
      const ring = el("circle", { cx: 0, cy: 0, r: 150, fill: "none", stroke: "#ff3b55", "stroke-width": 10, opacity: 0 }, sv);
      const rg = at("L20", "Regel"), l21 = line("L21")[0], ine = at("L21", "ineinander"), au = at("L21", "ausweicht"), ve = at("L21", "verrät");
      tl.fromTo("#s07-rule", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, rg - 0.05);
      tl.to("#s07-rule", { opacity: 0, y: -40, duration: 0.25 }, l21 - 0.2);
      tl.to(A.g, { x: 470, duration: ine - 0.4, ease: "none" }, 0.2);
      tl.to(B.g, { x: 610, duration: ine - 0.4, ease: "none" }, 0.2);
      tl.to(A.g, { x: 420, rotation: -10, duration: 0.2, ease: "power3.out" }, ine - 0.2);
      tl.to(B.g, { x: 660, rotation: 10, duration: 0.2, ease: "power3.out" }, ine - 0.2);
      tl.fromTo("#s07-bum", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(3)" }, ine - 0.2);
      tl.to(["#s07-bum", A.g], { opacity: 0, duration: 0.2 }, au - 0.5);
      tl.set(B.g, { x: 920, rotation: 0 }, au - 0.5);
      tl.to(B.g, { x: 600, duration: 1.2, ease: "none" }, au - 0.45);
      tl.fromTo(P.g, { opacity: 0, x: 120 }, { opacity: 1, x: 300, duration: 0.3 }, au - 0.5);
      tl.to(trail, { opacity: 1, duration: 0.15 }, au - 0.1);
      tl.to(P.g, { keyframes: [{ x: 540, y: 650, duration: 0.3 }, { x: 780, y: 790, duration: 0.3 }], ease: "sine.inOut" }, au - 0.1);
      tl.set(ring, { attr: { cx: 780, cy: 760 } }, ve - 0.1);
      tl.fromTo(ring, { opacity: 0, scale: 2, svgOrigin: "780 760" }, { opacity: 1, scale: 1, svgOrigin: "780 760", duration: 0.3, ease: "power4.out" }, ve - 0.1);
      tl.fromTo("#s07-lab", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)" }, ve);
      tl.to(P.mouth, { attr: { d: "M-12 -26 q12 -10 24 0" }, duration: 0.1 }, ve);''' + OUT)

# ---------- s08 Regel 2: kein Licht ----------
S['s08'] = ('''    #s08-lab { left: 560px; top: 520px; width: 380px; height: 90px; border: 4px solid #ff3b55; color: #ff3b55; font-size: 46px; line-height: 82px; opacity: 0; box-shadow: 0 0 40px rgba(255,59,85,.5); }''',
'''      <div id="s08-rule" class="rule">REGEL 2</div>
''' + SVG + '''
      <div id="s08-lab" class="panel">GEFUNDEN</div>''',
'''      el("circle", { cx: 900, cy: 620, r: 60, fill: "#f3f1ea", opacity: 0.85 }, sv);
      const blds = [[60, 700, 220, 430], [300, 620, 240, 510], [560, 740, 200, 390], [780, 680, 240, 450]], wins = [];
      blds.forEach(([x, y, w, h]) => { el("rect", { x, y, width: w, height: h, fill: "#1c2250" }, sv);
        for (let r = 0; r < 5; r++) for (let c = 0; c < 3; c++) { if (y + 40 + r * 80 > 1100) continue;
          wins.push(el("rect", { x: x + 22 + c * (w - 44 - 40) / 2, y: y + 40 + r * 80, width: 40, height: 50, rx: 4, fill: "#10142f" }, sv)); } });
      const lit = wins[22], lx = +lit.getAttribute("x") + 20, ly = +lit.getAttribute("y") + 25;
      const halo = el("circle", { cx: lx, cy: ly, r: 70, fill: "#ffd43b", opacity: 0 }, sv);
      const tgt = el("g", { opacity: 0 }, sv);
      el("circle", { cx: lx, cy: ly, r: 90, fill: "none", stroke: "#ff3b55", "stroke-width": 8 }, tgt);
      el("path", { d: `M${lx - 130} ${ly} h80 M${lx + 50} ${ly} h80 M${lx} ${ly - 130} v80 M${lx} ${ly + 50} v80`, stroke: "#ff3b55", "stroke-width": 8 }, tgt);
      const rg = at("L22", "Regel"), kl = at("L22", "Kein"), he = at("L23", "helles"), wo = at("L23", "wo");
      tl.fromTo("#s08-rule", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, rg - 0.05);
      tl.to("#s08-rule", { opacity: 0, y: -40, duration: 0.25 }, line("L22")[1]);
      tl.to(wins, { fill: "#ffd43b", duration: 0.05 }, 0.1);
      tl.to(wins, { fill: "#10142f", duration: 0.05, stagger: { each: 0.02, from: "random" } }, kl);
      tl.to(lit, { fill: "#ffd43b", duration: 0.05 }, he);
      tl.to(halo, { opacity: 0.4, duration: 0.3 }, he);
      tl.fromTo(tgt, { opacity: 0, scale: 2.5, svgOrigin: `${lx} ${ly}` }, { opacity: 1, scale: 1, svgOrigin: `${lx} ${ly}`, duration: 0.4, ease: "power4.out" }, wo - 0.3);
      tl.fromTo("#s08-lab", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.25, ease: "back.out(2)" }, wo + 0.1);
      tl.to(tgt, { opacity: 0.3, duration: 0.12, repeat: 5, yoyo: true }, wo + 0.3);''' + OUT)


# ---------- s09 Regel 3: tasten, Scherbe ----------
S['s09'] = ('''    #s09-burst { opacity: 0; }''',
'''      <div id="s09-rule" class="rule">REGEL 3</div>
''' + SVG,
'''      el("rect", { x: 0, y: 1060, width: 1080, height: 70, fill: "#2a2f55" }, sv);
      const shard = el("path", { d: "M640 1066 L690 990 L720 1066Z", fill: "#a9d2ff" }, sv);
      const spark = el("path", { d: "M690 960 l8 -24 l8 24 l24 8 l-24 8 l-8 24 l-8 -24 l-24 -8Z", fill: "#fff", opacity: 0 }, sv);
      const P = person(sv, "s09-p", 330, 828, 1.0, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0", arms: [80, -80] });
      const sight = el("path", { d: "M350 770 L680 1000", stroke: "#ffd43b", "stroke-width": 6, "stroke-dasharray": "16 14", fill: "none", opacity: 0 }, sv);
      const burst = el("path", { d: "M680 1050 l20 -70 l20 60 l50 -40 l-20 60 l60 10 l-60 20", fill: "#ff3b55", opacity: 0 }, sv);
      const rg = at("L24", "Regel"), ta = at("L24", "Tasten"), sc = at("L25", "Scherbe"), si = at("L25", "siehst"), l22 = line("L26")[0], ab = at("L26", "absichtlich");
      tl.fromTo("#s09-rule", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, rg - 0.05);
      tl.to("#s09-rule", { opacity: 0, y: -40, duration: 0.25 }, ta + 0.6);
      tl.fromTo(P.g, { opacity: 0, x: 200 }, { opacity: 1, x: 330, duration: 0.5, ease: "expo.out" }, 0.1);
      tl.to(P.a1, { rotation: 95, duration: 0.3, repeat: 3, yoyo: true, ease: "sine.inOut" }, ta);
      tl.to(P.a2, { rotation: -65, duration: 0.3, repeat: 3, yoyo: true, ease: "sine.inOut" }, ta + 0.15);
      tl.to(spark, { opacity: 1, scale: 1.4, svgOrigin: "698 968", duration: 0.2, repeat: 3, yoyo: true }, sc);
      tl.to(P.eyes, { x: 6, y: 5, duration: 0.15 }, si - 0.4);
      tl.to(sight, { opacity: 1, duration: 0.2 }, si - 0.3);
      tl.to(sight, { opacity: 0, duration: 0.15 }, l22);
      tl.to(P.eyes, { x: 0, y: 0, duration: 0.15 }, l22);
      tl.to(P.g, { x: 640, duration: 0.7, ease: "power1.inOut" }, l22);
      tl.fromTo(burst, { opacity: 0, scale: 0.4, svgOrigin: "700 1050" }, { opacity: 1, scale: 1, svgOrigin: "700 1050", duration: 0.2, ease: "back.out(3)" }, ab + 0.05);
      tl.to(P.mouth, { attr: { d: "M-12 -26 q12 -10 24 0" }, duration: 0.1 }, ab + 0.05);
      tl.to(P.g, { y: 836, duration: 0.05, repeat: 5, yoyo: true }, ab + 0.1);''' + OUT)


# ---------- s10 Kreuzung: Kind, Lastwagen, Stopp, Köpfe drehen sich ----------
S['s10'] = ('''    #s10-b { left: 60px; top: 430px; width: 340px; background: #ff3b55; color: #fff; font-size: 64px; }''',
SVG + '''
      <div id="s10-b" class="bub">STOPP!</div>''',
'''      const scene = el("g", {}, sv);
      el("rect", { x: 0, y: 840, width: 1080, height: 260, fill: "#3a3f5c" }, scene);
      for (let i = 0; i < 9; i++) el("rect", { x: 20 + i * 130, y: 962, width: 80, height: 14, rx: 4, fill: "#c9cde6" }, scene);
      const P = person(scene, "s10-p", 180, 600, 0.95, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const K = person(scene, "s10-k", 640, 640, 0.6, { shirt: "#ffd43b", hair: "#e0a35a" });
      const tr = el("g", {}, scene); gsap.set(tr, { x: 1300 });
      el("rect", { x: 0, y: 760, width: 460, height: 260, rx: 18, fill: "#e5e9f7" }, tr);
      el("rect", { x: -190, y: 820, width: 190, height: 200, rx: 26, fill: "#ff3b55" }, tr);
      el("rect", { x: -170, y: 840, width: 110, height: 80, rx: 10, fill: "#a9d2ff" }, tr);
      el("circle", { cx: -200, cy: 950, r: 22, fill: "#ffd43b" }, tr);
      [-110, 120, 380].forEach((x) => el("circle", { cx: x, cy: 1030, r: 44, fill: "#161a36" }, tr));
      const shout = [0, 1, 2].map((i) => el("path", { d: `M${260 + i * 34} ${470 + i * 4} q30 60 0 120`, fill: "none", stroke: "#ff3b55", "stroke-width": 10, "stroke-linecap": "round", opacity: 0 }, scene));
      const heads = el("g", { opacity: 0 }, sv), faces = [];
      [[300, 600], [540, 560], [780, 600], [420, 860], [660, 860], [900, 860]].forEach(([x, y], i) => {
        el("circle", { cx: x, cy: y, r: 100, fill: ["#f2c9a5", "#d9a77f", "#f2c9a5", "#b9835a", "#f2c9a5", "#d9a77f"][i] }, heads);
        el("path", { d: `M${x - 100} ${y - 10} C${x - 100} ${y - 130} ${x + 100} ${y - 130} ${x + 100} ${y - 10} C${x + 60} ${y - 70} ${x - 40} ${y - 76} ${x - 100} ${y - 10}Z`, fill: ["#2a2f55", "#5b3a26", "#e0a35a", "#161a36", "#8a5a2b", "#2a2f55"][i] }, heads);
        const f = el("g", {}, heads);
        [-34, 34].forEach((dx) => { el("circle", { cx: x + dx, cy: y + 10, r: 18, fill: "#e4e8f6" }, f); el("circle", { cx: x + dx, cy: y + 10, r: 10, fill: "#b4bbd6" }, f); });
        el("path", { d: `M${x - 20} ${y + 56} h40`, stroke: "#8a3b2a", "stroke-width": 7, "stroke-linecap": "round" }, f);
        faces.push(f); });
      const sina2 = el("g", { opacity: 0 }, sv);
      el("circle", { cx: 120, cy: 1000, r: 120, fill: "#ff4fb0", opacity: 0.25 }, sina2);
      const ki = at("L27", "Kind"), st = at("L27", "Straße"), lw = at("L28", "Lastwagen"), sch = at("L29", "schreit"), sp = at("L29", "Stopp"),
            l26 = line("L30")[0], sti = at("L30", "Stille"), l27 = line("L31")[0], dr = at("L31", "drehen");
      tl.fromTo(scene, { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.05);
      tl.fromTo(K.g, { x: 760, y: 600 }, { x: 640, y: 690, duration: st - ki + 0.4, ease: "none" }, ki);
      tl.to(K.g, { y: "+=8", duration: 0.15, repeat: 9, yoyo: true }, ki);
      tl.to(tr, { x: 1060, duration: 0.6, ease: "power2.out" }, lw - 0.2);
      tl.to(tr, { x: 1090, duration: 0.05, repeat: 9, yoyo: true }, lw + 0.4);
      tl.to(P.mouth, { attr: { d: "M-14 -36 q14 26 28 0Z" }, duration: 0.1 }, sch);
      tl.to(P.a2, { rotation: -150, duration: 0.2, ease: "back.out(2)" }, sch);
      shout.forEach((s, i) => tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.12, repeat: 5, yoyo: true }, sp + i * 0.06));
      tl.fromTo("#s10-b", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, sp - 0.05);
      tl.to("#s10-b", { opacity: 0, duration: 0.2 }, l26);
      tl.to(tr, { x: -900, duration: 0.6, ease: "power2.in" }, l26 + 0.2);
      tl.to(K.g, { x: 650, duration: 0.04, repeat: 5, yoyo: true }, l26 + 0.6);
      tl.to(scene, { opacity: 0, duration: 0.35 }, sti - 0.15);
      tl.fromTo(heads, { opacity: 0, scale: 1.1, svgOrigin: "600 730" }, { opacity: 1, scale: 1, svgOrigin: "600 730", duration: 0.5, ease: "expo.out" }, sti + 0.3);
      faces.forEach((f, i) => tl.to(f, { x: -38, y: 10, duration: 0.7, ease: "power2.inOut" }, dr + (i * 0.12)));
      tl.to(heads, { x: -20, duration: 1.2, ease: "power1.inOut" }, dr + 0.6);''' + OUT)


# ---------- s11 Belohnung ----------
S['s11'] = ('''    #s11-post { left: 260px; top: 450px; width: 560px; height: 620px; border: 6px solid #ff3b55; box-shadow: 0 0 60px rgba(255,59,85,.45); overflow: hidden; opacity: 0; background: #f3f1ea; color: #161a36; }
    #s11-post .bar { height: 96px; background: #ff3b55; color: #fff; font-size: 64px; line-height: 96px; letter-spacing: .06em; }
    #s11-post .sil { margin: 28px auto 0; width: 200px; height: 200px; border-radius: 100px; background: #2a2f55; color: #ffd43b; font-size: 150px; line-height: 200px; }
    #s11-post .t { margin-top: 22px; font-size: 44px; line-height: 1.1; }
    #s11-post .rw { margin: 22px 34px 0; padding: 16px 0; border-radius: 16px; background: #ffd43b; font-size: 40px; line-height: 1.1; }
    #s11-box { opacity: 0; }''',
'''      <div id="s11-box" class="cbox y"><div class="lab">BELOHNUNG</div><div id="s11-n" class="num">0 TAGE KINO</div></div>
''' + SVG + '''
      <div id="s11-post" class="panel"><div class="bar">GESUCHT</div><div class="sil">?</div><div class="t">FRAU, DIE<br>SEHEN KANN</div><div class="rw">1 JAHR GRATIS KINO</div></div>''',
'''      const van = el("g", {}, sv); gsap.set(van, { x: -700 });
      el("rect", { x: 280, y: 820, width: 520, height: 220, rx: 30, fill: "#e5e9f7" }, van);
      el("path", { d: "M800 860 L900 900 L900 1040 L800 1040Z", fill: "#e5e9f7" }, van);
      el("path", { d: "M806 872 L888 906 L888 960 L806 960Z", fill: "#a9d2ff" }, van);
      el("rect", { x: 280, y: 940, width: 620, height: 20, fill: "#ff3b55" }, van);
      [380, 790].forEach((x) => el("circle", { cx: x, cy: 1050, r: 46, fill: "#161a36" }, van));
      el("rect", { x: 500, y: 780, width: 30, height: 44, fill: "#8fa2ff" }, van);
      el("path", { d: "M470 790 L560 740 L560 830Z", fill: "#c9cde6" }, van);
      const waves = [0, 1, 2].map((i) => el("path", { d: `M${600 + i * 40} ${720 - i * 20} q40 60 0 130`, fill: "none", stroke: "#ffd43b", "stroke-width": 10, "stroke-linecap": "round", opacity: 0 }, sv));
      const T = person(sv, "s11-t", 860, 780, 1.0, { blind: true, shirt: "#4da3ff", hair: "#2a2f55", arms: [12, -150] });
      gsap.set(T.g, { opacity: 0 });
      const ear = el("circle", { cx: 906, cy: 722, r: 34, fill: "none", stroke: "#4da3ff", "stroke-width": 6, opacity: 0 }, sv);
      const du = at("L32", "Durchsage"), na = at("L33", "Namen"), es = at("L33", "Jahr"), ja = at("L33", "Kino"), l30 = line("L34")[0], tom = at("L34", "Alex"), ge = at("L34", "ganz");
      tl.to(van, { x: 0, duration: 0.8, ease: "power3.out" }, 0.05);
      waves.forEach((w, i) => tl.fromTo(w, { opacity: 0 }, { opacity: 1, duration: 0.2, repeat: 9, yoyo: true }, du + i * 0.1));
      tl.to(van, { opacity: 0, y: 60, duration: 0.3 }, na - 0.6);
      tl.to(waves, { opacity: 0, duration: 0.1 }, na - 0.6);
      tl.fromTo("#s11-post", { opacity: 0, scale: 0.5, rotation: -8 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.8)" }, na - 0.4);
      tl.to("#s11-box", { opacity: 1, duration: 0.25 }, es - 0.3);
      count(tl, "#s11-n", 0, 365, es - 0.2, ja - es + 0.2, "", " TAGE KINO", "power2.out");
      tl.fromTo("#s11-post .rw", { scale: 1 }, { scale: 1.12, duration: 0.15, yoyo: true, repeat: 1 }, ja);
      tl.to("#s11-post", { x: -150, scale: 0.75, duration: 0.4, ease: "power3.inOut" }, l30 - 0.1);
      tl.fromTo(T.g, { opacity: 0, x: 1000 }, { opacity: 1, x: 860, duration: 0.4, ease: "expo.out" }, tom - 0.2);
      tl.fromTo(ear, { opacity: 0, attr: { r: 34 } }, { opacity: 1, attr: { r: 80 }, duration: 0.4, repeat: 3, ease: "power1.out" }, ge - 0.1);''' + OUT)


# ---------- s12 Nacht acht: Taschenlampe ----------
S['s12'] = ('',
SVG,
'''      el("circle", { cx: 920, cy: 500, r: 50, fill: "#f3f1ea", opacity: 0.8 }, sv);
      el("rect", { x: 170, y: 470, width: 740, height: 660, fill: "#1c2250" }, sv);
      const W = [];
      for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        const x = 220 + c * 230, y = 510 + r * 190;
        W.push([x + 80, y + 70]);
        el("rect", { x, y, width: 160, height: 140, rx: 8, fill: "#10142f" }, sv);
      }
      const sw = W[4];
      const glow = el("rect", { x: sw[0] - 80, y: sw[1] - 70, width: 160, height: 140, rx: 8, fill: "#ffd43b", opacity: 0 }, sv);
      el("path", { d: `M${sw[0] - 80} ${sw[1] - 70} h50 q-10 70 0 140 h-50Z M${sw[0] + 80} ${sw[1] - 70} h-50 q10 70 0 140 h50Z`, fill: "#7a5bd0" }, sv);
      const face = el("g", {}, sv);
      el("circle", { cx: sw[0], cy: sw[1] + 20, r: 34, fill: "#f2c9a5" }, face);
      el("path", { d: `M${sw[0] - 36} ${sw[1] + 20} C${sw[0] - 38} ${sw[1] - 30} ${sw[0] + 38} ${sw[1] - 30} ${sw[0] + 36} ${sw[1] + 20} C${sw[0] + 20} ${sw[1] - 6} ${sw[0] - 20} ${sw[1] - 6} ${sw[0] - 36} ${sw[1] + 20}Z`, fill: "#4a2c1d" }, face);
      const ey = el("g", {}, face);
      el("circle", { cx: sw[0] - 12, cy: sw[1] + 20, r: 5, fill: "#161a36" }, ey); el("circle", { cx: sw[0] + 12, cy: sw[1] + 20, r: 5, fill: "#161a36" }, ey);
      const O = [540, 1150];
      const ang = (p) => Math.atan2(p[0] - O[0], O[1] - p[1]) * 180 / Math.PI;
      const beam = el("path", { d: `M${O[0]} ${O[1]} L${O[0] - 70} ${O[1] - 760} L${O[0] + 70} ${O[1] - 760}Z`, fill: "#ffd43b", opacity: 0 }, sv);
      const spot = el("ellipse", { cx: O[0], cy: O[1] - 760, rx: 90, ry: 70, fill: "#fff3b0", opacity: 0 }, sv);
      const bm = el("g", {}, sv); bm.appendChild(beam); bm.appendChild(spot);
      const q = el("text", { x: 540, y: 900, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 300, fill: "#ff3b55", opacity: 0 }, sv); q.textContent = "?";
      const t0 = at("L35", "Nacht"), lk = at("L36", "Lichtkegel"), l33 = at("L36", "Taschenlampe"), wb = at("L37", "wer"), bl = at("L37", "Blinder"), l35 = line("L38")[0], ih = at("L38", "ihrem");
      const aim = (p) => { const dy = O[1] - p[1]; return { rotation: ang(p), scaleY: Math.hypot(p[0] - O[0], dy) / 760, svgOrigin: `${O[0]} ${O[1]}` }; };
      tl.to(ey, { x: -6, duration: 0.3, repeat: 3, yoyo: true }, t0 + 0.6);
      tl.set(bm, aim(W[6]), 0);
      tl.to([beam], { opacity: 0.5, fill: "#ffe680", duration: 0.25 }, lk - 0.1);
      tl.to(spot, { opacity: 0.6, duration: 0.25 }, lk - 0.1);
      [W[6], W[7], W[3], W[2], W[1], W[0]].forEach((p, i) => tl.to(bm, { ...aim(p), duration: 0.6, ease: "power1.inOut" }, l33 + i * 0.7));
      tl.to(bm, { opacity: 0.35, duration: 0.2 }, wb - 0.1);
      tl.fromTo(q, { opacity: 0, scale: 0.4 }, { opacity: 0.9, scale: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.4)" }, wb);
      tl.to(q, { opacity: 0, duration: 0.25 }, bl + 0.6);
      tl.to(bm, { opacity: 1, duration: 0.2 }, bl + 0.6);
      tl.to(bm, { ...aim(sw), duration: 0.5, ease: "power3.out" }, ih - 0.45);
      tl.to(glow, { opacity: 0.85, duration: 0.15 }, ih);
      tl.to(ey, { scale: 1.6, svgOrigin: `${sw[0]} ${sw[1] + 20}`, duration: 0.15 }, ih);''' + OUT)


# ---------- s13 Tür: Schritte, drei Schläge, Blick durch den Spion ----------
S['s13'] = ('''    .s13-k { position: absolute; font-family: "Inter", sans-serif; font-weight: 900; font-size: 64px; color: #ffd43b; text-shadow: 0 0 24px rgba(255,212,59,.5); opacity: 0; }
    #s13-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 40%, rgba(160,0,20,.75) 100%); opacity: 0; }''',
SVG + '''
      <div id="s13-k1" class="s13-k" style="left:90px;top:560px">KLOPF</div><div id="s13-k2" class="s13-k" style="left:800px;top:700px">KLOPF</div><div id="s13-k3" class="s13-k" style="left:100px;top:860px">KLOPF</div>
      <div id="s13-vig" class="full"></div>''',
'''      const room = el("g", {}, sv);
      el("rect", { x: 300, y: 450, width: 480, height: 680, rx: 10, fill: "#3a2614" }, room);
      const door = el("g", {}, room);
      el("rect", { x: 330, y: 480, width: 420, height: 640, rx: 6, fill: "#7a4b22" }, door);
      el("rect", { x: 370, y: 540, width: 340, height: 220, rx: 10, fill: "#6b3f1d" }, door);
      el("rect", { x: 370, y: 800, width: 340, height: 260, rx: 10, fill: "#6b3f1d" }, door);
      el("circle", { cx: 700, cy: 820, r: 18, fill: "#ffd43b" }, door);
      el("circle", { cx: 540, cy: 620, r: 22, fill: "#161a36" }, door);
      const strip = el("rect", { x: 330, y: 1112, width: 420, height: 12, fill: "#ffd43b", opacity: 0.15 }, room);
      const feet = el("g", { opacity: 0 }, room);
      el("rect", { x: 450, y: 1112, width: 60, height: 12, fill: "#0b0e22" }, feet); el("rect", { x: 570, y: 1112, width: 60, height: 12, fill: "#0b0e22" }, feet);
      // Blick durch den Spion: runder Fischaugen-Ausschnitt
      const defs = el("defs", {}, sv); const cp = el("clipPath", { id: "s13-clip" }, defs); el("circle", { cx: 540, cy: 780, r: 340 }, cp);
      const pv = el("g", { opacity: 0 }, sv);
      el("rect", { x: 0, y: 400, width: 1080, height: 760, fill: "#05060f" }, pv);
      const inner = el("g", { "clip-path": "url(#s13-clip)" }, pv);
      el("rect", { x: 200, y: 440, width: 680, height: 680, fill: "#1a1530" }, inner);
      el("ellipse", { cx: 540, cy: 1110, rx: 300, ry: 160, fill: "#ffd43b", opacity: 0.35 }, inner);
      const face = el("g", {}, inner);
      el("rect", { x: 380, y: 900, width: 320, height: 260, rx: 90, fill: "#2a2f55" }, face);
      el("circle", { cx: 540, cy: 760, r: 170, fill: "#d9a77f" }, face);
      el("path", { d: "M370 740 C360 560 720 560 710 740 C680 640 420 640 370 740Z", fill: "#161a36" }, face);
      el("ellipse", { cx: 540, cy: 900, rx: 150, ry: 50, fill: "#ffd43b", opacity: 0.25 }, face);
      const eyesW = el("g", {}, face), pups = [];
      [470, 610].forEach((x) => { el("ellipse", { cx: x, cy: 750, rx: 44, ry: 30, fill: "#f3f1ea" }, eyesW); pups.push(el("circle", { cx: x - 14, cy: 752, r: 17, fill: "#0b0e22" }, eyesW)); });
      el("path", { d: "M500 850 q40 10 80 0", stroke: "#6b3f1d", "stroke-width": 8, fill: "none", "stroke-linecap": "round" }, face);
      el("circle", { cx: 540, cy: 780, r: 350, fill: "none", stroke: "#0b0e22", "stroke-width": 30 }, pv);
      el("circle", { cx: 540, cy: 780, r: 336, fill: "none", stroke: "#3a3f7a", "stroke-width": 6 }, pv);
      const sr = at("L39", "Schritte"), la = at("L39", "Langsam"), dr = at("L40", "drei"), l41 = line("L41")[0], ts = at("L41", "Türspion"),
            l42 = line("L42")[0], we = at("L42", "weit"), di = at("L42", "direkt"), l43 = line("L43")[0], si = at("L43", "siehst");
      tl.fromTo(room, { opacity: 0, scale: 0.92, svgOrigin: "540 800" }, { opacity: 1, scale: 1, svgOrigin: "540 800", duration: 0.5, ease: "expo.out" }, 0.05);
      tl.to(strip, { opacity: 0.85, duration: 0.8 }, sr);
      tl.to(feet, { opacity: 0.5, duration: 0.2 }, la);
      tl.to(feet, { opacity: 1, duration: 0.6 }, la + 0.3);
      tl.to(room, { scale: 1.04, svgOrigin: "540 800", duration: dr - sr, ease: "none" }, sr);
      [0, 0.45, 0.9].forEach((d, i) => {
        tl.to(door, { x: 7, duration: 0.04, repeat: 3, yoyo: true }, dr + d);
        tl.fromTo(`#s13-k${i + 1}`, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.18, ease: "back.out(3)" }, dr + d); });
      tl.to(".s13-k", { opacity: 0, duration: 0.25 }, l41 - 0.1);
      tl.to(room, { scale: 3.2, svgOrigin: "540 620", duration: 0.6, ease: "power2.in" }, ts - 0.4);
      tl.to(room, { opacity: 0, duration: 0.15 }, ts + 0.1);
      tl.fromTo(pv, { opacity: 0 }, { opacity: 1, duration: 0.25 }, ts + 0.05);
      tl.fromTo(face, { y: 40, scale: 0.9, svgOrigin: "540 780" }, { y: 0, scale: 1, svgOrigin: "540 780", duration: 1.2, ease: "power2.out" }, ts + 0.1);
      tl.to(eyesW, { scaleY: 1.4, svgOrigin: "540 750", duration: 0.2, ease: "back.out(3)" }, we);
      tl.to(pups, { attr: { cx: (i) => [470, 610][i] }, duration: 0.3, ease: "power3.out" }, di - 0.1);
      tl.to(face, { scale: 1.45, svgOrigin: "540 750", duration: 0.35, ease: "power4.out" }, di);
      tl.to("#s13-vig", { opacity: 1, duration: 0.15 }, di);
      tl.to("#s13-vig", { opacity: 0.4, duration: 0.5, repeat: 5, yoyo: true }, di + 0.2);
      tl.to(face, { scale: 1.7, svgOrigin: "540 750", duration: si - l43, ease: "none" }, l43);
      tl.to(pv, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, si);''' + OUT)

# ---------- s14 Schlüssel im Schloss, jemand hinter ihr ----------
S['s14'] = ('''    #s14-vig { background: radial-gradient(ellipse 60% 45% at 50% 42%, rgba(0,0,0,0) 35%, rgba(160,0,20,.8) 100%); opacity: 0; }
    #s14-black { background: #000; opacity: 0; }
    .s14-w { position: absolute; left: 0; width: 1080px; top: 395px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 170px;
      color: #ff3b55; text-shadow: 0 0 50px rgba(255,59,85,.7), 0 10px 0 rgba(0,0,0,.6); opacity: 0; }''',
SVG + '''
      <div id="s14-vig" class="full"></div>
      <div id="s14-w1" class="s14-w">PSST.</div><div id="s14-w2" class="s14-w">MACH.</div><div id="s14-w3" class="s14-w">NICHT.</div><div id="s14-w4" class="s14-w">AUF.</div>
      <div id="s14-black" class="full"></div>''',
'''      el("rect", { x: 0, y: 400, width: 1080, height: 740, fill: "#0b0d20" }, sv);
      el("rect", { x: 0, y: 1060, width: 1080, height: 80, fill: "#151833" }, sv);
      el("rect", { x: 740, y: 470, width: 300, height: 600, rx: 8, fill: "#3a2614" }, sv);
      el("rect", { x: 760, y: 490, width: 260, height: 570, rx: 6, fill: "#6b3f1d" }, sv);
      el("rect", { x: 760, y: 1056, width: 260, height: 8, fill: "#ffd43b", opacity: 0.8 }, sv);
      el("circle", { cx: 800, cy: 790, r: 16, fill: "#ffd43b" }, sv);
      el("rect", { x: 794, y: 816, width: 12, height: 26, rx: 4, fill: "#161a36" }, sv);
      const key = el("g", { opacity: 0 }, sv);
      el("rect", { x: 796, y: 824, width: 70, height: 10, rx: 4, fill: "#ffd43b" }, key);
      el("circle", { cx: 880, cy: 829, r: 22, fill: "none", stroke: "#ffd43b", "stroke-width": 10 }, key);
      const H = person(sv, "s14-h", 250, 700, 1.3, { skin: "#020309", shirt: "#020309", hair: "#020309", pants: "#020309" });
      gsap.set(H.eyes, { opacity: 0 }); gsap.set(H.mouth, { opacity: 0 }); gsap.set(H.g, { opacity: 0 });
      const glint = el("g", { opacity: 0 }, sv);
      el("circle", { cx: 232, cy: 628, r: 5, fill: "#f3f1ea" }, glint); el("circle", { cx: 268, cy: 628, r: 5, fill: "#f3f1ea" }, glint);
      const P = person(sv, "s14-p", 560, 770, 1.1, { long: true, hair: "#4a2c1d", shirt: "#ff4fb0" });
      const hand = el("ellipse", { cx: 330, cy: 760, rx: 46, ry: 34, fill: "#020309", opacity: 0 }, sv);
      const sch = at("L44", "Schlüssel"), slo = at("L44", "Schloss"), zu = at("L45", "zurück"), je = at("L45", "jemanden"), l46 = line("L46")[0],
            ha = at("L47", "Hand"), mu = at("L47", "Mund"), w1 = at("L48", "Psst"), w2 = at("L48", "Mach"), w3 = at("L48", "Nicht"), w4 = at("L48", "Auf");
      tl.fromTo(P.g, { opacity: 0, x: 600 }, { opacity: 1, x: 560, duration: 0.4, ease: "expo.out" }, 0.05);
      tl.to(P.eyes, { x: 8, duration: 0.2 }, 0.3);
      tl.fromTo(key, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, sch - 0.1);
      tl.to(key, { scaleY: -1, svgOrigin: "800 829", duration: 0.25, ease: "power2.inOut" }, slo);
      tl.to(P.g, { x: 572, duration: 0.04, repeat: 5, yoyo: true }, slo);
      tl.to(P.g, { x: 330, duration: je - zu + 0.2, ease: "power1.inOut" }, zu - 0.2);
      tl.set(H.g, { opacity: 1 }, je - 0.05);
      tl.to(P.g, { x: 345, duration: 0.05, repeat: 3, yoyo: true }, je);
      tl.fromTo("#s14-vig", { opacity: 0 }, { opacity: 1, duration: 0.12 }, je);
      tl.to(P.mouth, { attr: { d: "M-10 -30 q10 -12 20 0 q-10 12 -20 0" }, duration: 0.1 }, je);
      tl.to(P.eyes, { x: -6, scale: 1.4, svgOrigin: "0 -56", duration: 0.15 }, je + 0.2);
      tl.to(glint, { opacity: 1, duration: 0.1 }, l46);
      tl.to("#s14-vig", { opacity: 0.5, duration: 0.45, repeat: 9, yoyo: true }, je + 0.3);
      tl.set(hand, { opacity: 1 }, ha);
      tl.fromTo(hand, { attr: { cx: 250, cy: 790 } }, { attr: { cx: 340, cy: 734 }, duration: mu - ha, ease: "power2.out" }, ha);
      tl.to(H.g, { x: 270, duration: mu - ha }, ha);
      [["#s14-w1", w1], ["#s14-w2", w2], ["#s14-w3", w3], ["#s14-w4", w4]].forEach(([s, t], i, a) => {
        tl.fromTo(s, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.15, ease: "power4.out" }, t - 0.05);
        tl.to("#s14-svg", { x: 12, duration: 0.04, repeat: 3, yoyo: true }, t - 0.05);
        if (i < 3) tl.set(s, { opacity: 0 }, a[i + 1][1] - 0.06); });
      tl.to("#s14-black", { opacity: 1, duration: 0.05 }, w4 + 0.55);
      tl.set("#s14-w4", { opacity: 0 }, w4 + 0.55);''')

# ---------- s15 Ende: Wer steht hinter ihr? + Folgen für Part 2 (letzte Szene, kein Blur-Out) ----------
S['s15'] = ('''    #s15-bg { background: #000; }
    #s15-q { position: absolute; left: 0; width: 1080px; top: 470px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 300px;
      color: #ff3b55; text-shadow: 0 0 60px rgba(255,59,85,.7); opacity: 0; }
    #s15-cta { left: 90px; top: 470px; width: 900px; height: 600px; border: 6px solid #ff4fb0; box-shadow: 0 0 70px rgba(255,79,176,.5); opacity: 0; }
    #s15-cta .a { margin-top: 300px; font-size: 54px; line-height: 1.1; color: #fff; }
    #s15-btn { position: absolute; left: 290px; top: 440px; width: 320px; height: 100px; border-radius: 50px; background: #ff4fb0; color: #fff;
      font-size: 54px; line-height: 100px; }
    #s15-p2 { position: absolute; left: 620px; top: 36px; width: 240px; height: 76px; border-radius: 14px; background: #ffd43b; color: #0b0e22;
      font-size: 44px; line-height: 76px; transform: rotate(6deg); }''',
'''      <div id="s15-bg" class="full"></div>
      <div id="s15-cta" class="panel"><div id="s15-p2">PART 2</div><div class="a">WENN DU DAS<br>SEHEN KANNST …</div><div id="s15-btn">+ FOLGEN</div></div>
''' + SVG + '''
      <div id="s15-q" class="abs">?</div>''',
'''      const sil = el("g", { opacity: 0 }, sv);
      const H = person(sil, "s15-h", 540, 760, 1.4, { skin: "#05060f", shirt: "#05060f", hair: "#05060f", pants: "#05060f" });
      gsap.set([H.eyes, H.mouth], { opacity: 0 });
      sil.style.filter = "drop-shadow(0 0 18px rgba(255,59,85,.8))";
      const E = bigEye(sv, 540, 640, 0.75); gsap.set(E.g, { opacity: 0 });
      const hi = at("L49", "hinter"), l50 = line("L50")[0], se = at("L50", "sehen"), fo = at("L50", "folge"), pa = at("L50", "Part");
      tl.fromTo(sil, { opacity: 0 }, { opacity: 1, duration: 0.6 }, 0.1);
      tl.fromTo("#s15-q", { opacity: 0, scale: 0.5 }, { opacity: 0.9, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, hi);
      tl.to([sil, "#s15-q"], { opacity: 0, duration: 0.25 }, l50 - 0.2);
      tl.fromTo("#s15-cta", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, l50);
      tl.to(E.g, { opacity: 1, duration: 0.3 }, l50 + 0.1);
      tl.to(E.iris, { x: -60, duration: 0.3, yoyo: true, repeat: 1 }, se);
      tl.fromTo("#s15-btn", { scale: 1 }, { scale: 1.15, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }, fo);
      tl.fromTo("#s15-p2", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(3)" }, pa);''')


here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
