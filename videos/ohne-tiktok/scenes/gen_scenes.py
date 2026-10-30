#!/usr/bin/env python3
"""Erzeugt die Szenen s01–s08 für „Ohne TikTok“ (danach Szenen direkt editieren oder hier ändern und neu erzeugen)."""
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
CAM = '      const P = iso(540, 770, 80);\n'
FLAT = '''    .flat { position: absolute; border-radius: 26px; background: rgba(255,255,255,.94); box-shadow: 0 18px 50px rgba(0,0,0,.35); opacity: 0; text-align: center; color: #22283f; }'''

S['s01'] = ('''    #s01-title { left: 70px; right: 70px; top: 240px; text-align: center; color: #fff; font: 500 66px/1.18 "EB Garamond", "Liberation Serif", serif; text-shadow: 0 2px 16px rgba(0,0,0,.6); }
    #s01-title em { font-style: normal; color: #ff8fd0; }
    #s01-ic { left: 505px; top: 140px; width: 70px; height: 110px; border: 6px solid #fff; border-radius: 16px; box-shadow: 0 0 30px rgba(255,143,208,.8); }
    #s01-ic i { position: absolute; left: 22px; bottom: 8px; width: 14px; height: 6px; border-radius: 3px; background: #fff; }''',
SVG + '''
      <div id="s01-ic" class="abs"><i></i></div>
      <div id="s01-title" class="abs">Was wäre, wenn du nicht mehr stundenlang auf <em>TikTok</em> wärst?</div>''',
'''      const sv = document.querySelector("#s01-svg");
''' + CAM + '''      sky(sv, "s01-sky", "#1d2550", "#3a3f6e");
      room(P, sv, 6, 6, 4.2, { wall: "#e6ded2", floor: "#b98f6a" });
      const win = wallX(P, sv, 1.3, 3.3, 1.6, 3.4, "#28305e");
      el("polyline", { points: poly([P(0, 2.3, 1.6), P(0, 2.3, 3.4)]), stroke: "#f4efe6", "stroke-width": 8 }, sv);
      wallX(P, sv, 1.3, 3.3, 1.6, 3.4, "none", { stroke: "#f4efe6", "stroke-width": 10 });
      const beam = el("polygon", { points: poly([P(0, 1.3, 1.6), P(0, 3.3, 1.6), P(2.8, 4.9, 0), P(2.8, 2.9, 0)]), fill: "#fff1b8", opacity: 0 }, sv);
      box(P, sv, 5.0, 0.3, 0, 0.6, 0.6, 0.6, "#d77a4a"); box(P, sv, 4.9, 0.2, 0.6, 0.8, 0.8, 0.8, "#5fbf6a");
      box(P, sv, 2.0, 0.2, 0, 2.9, 1.9, 0.45, "#7b8fd6");
      box(P, sv, 4.35, 0.4, 0.45, 0.45, 1.5, 0.2, "#ffffff");
      const me = person(P, sv, 2.1, 0.95, 0.47, { pose: "lie", shirt: "#ff8fd0" });
      box(P, sv, 2.0, 0.2, 0.45, 1.9, 1.9, 0.14, "#e8a0b4");
      const ph = box(P, sv, 3.9, 1.0, 1.25, 0.12, 0.34, 0.55, "#1d1d24");
      const [gx, gy] = P(3.9, 1.17, 1.55);
      const glow = el("circle", { cx: gx, cy: gy, r: 70, fill: "#9dbcff", opacity: 0.55 }, sv);
      box(P, sv, 0.3, 4.3, 0, 1.3, 1.5, 1.0, "#a07a55"); box(P, sv, 0.5, 4.6, 1.0, 0.3, 0.3, 0.5, "#f2d06b");
      const night = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#0a1030", opacity: 0.42 }, sv);
      const l1e = line("L1")[1], lo = at("L2", "löschst"), fe = at("L2", "Fenster");
      tl.fromTo(glow, { attr: { fill: "#9dbcff" } }, { attr: { fill: "#ff8fd0" }, duration: 0.5, repeat: 7, yoyo: true }, 0);
      tl.fromTo(glow, { attr: { r: 60 } }, { attr: { r: 85 }, duration: 0.35, repeat: 11, yoyo: true }, 0);
      tl.to(["#s01-title", "#s01-ic"], { opacity: 0, y: -30, duration: 0.4, ease: "power2.in" }, l1e + 0.4);
      tl.to(glow, { opacity: 0, duration: 0.3 }, lo);
      tl.to(ph, { y: 40, rotation: 70, svgOrigin: `${gx} ${gy}`, duration: 0.5, ease: "bounce.out" }, lo + 0.1);
      tl.to(win, { attr: { fill: "#bfe3ff" }, duration: 0.5 }, fe - 0.3);
      tl.to(night, { opacity: 0, duration: 0.6 }, fe - 0.3);
      tl.to(beam, { opacity: 0.5, duration: 0.6 }, fe - 0.2);
      tl.to(me, { y: -14, duration: 0.15, yoyo: true, repeat: 3 }, fe);''' + OUT)

S['s02'] = ('',
SVG,
'''      const sv = document.querySelector("#s02-svg");
''' + CAM + '''      sky(sv, "s02-sky", "#bfe3ff", "#f6f1e6");
      room(P, sv, 6, 6, 4.2, { wall: "#f3ead8", floor: "#c9a982" });
      wallY(P, sv, 3.4, 5.4, 1.6, 3.3, "#cdeaff"); wallY(P, sv, 3.4, 5.4, 1.6, 3.3, "none", { stroke: "#fff", "stroke-width": 10 });
      box(P, sv, 0.2, 0.2, 0, 3.0, 0.8, 1.0, "#9fb7c9"); box(P, sv, 0.2, 0.2, 2.2, 3.0, 0.6, 0.9, "#b8cbd8");
      box(P, sv, 2.2, 2.0, 0, 1.9, 1.5, 0.9, "#b98a5e");
      box(P, sv, 2.7, 2.4, 0.9, 0.7, 0.7, 0.05, "#ffffff"); box(P, sv, 2.85, 2.55, 0.95, 0.35, 0.35, 0.1, "#e2a85a");
      const ghost = box(P, sv, 2.4, 3.0, 0.9, 0.3, 0.16, 0.03, "#ffffff", { opacity: 0 });
      box(P, sv, 4.45, 2.35, 0, 0.6, 0.6, 0.5, "#8a6a4a");
      const me = person(P, sv, 4.5, 2.4, 0, { pose: "sit", shirt: "#ff8fd0" });
      const hand = box(P, sv, 3.75, 2.6, 0.9, 0.3, 0.2, 0.1, "#f0c8a0");
      box(P, sv, 5.0, 2.35, 0.5, 0.12, 0.6, 0.95, "#8a6a4a");
      const [px, py] = P(4.6, 2.9, 0.65);
      const vib = el("g", { opacity: 0 }, sv);
      [24, 44, 64].forEach((r) => el("path", { d: `M${px + r} ${py - r * 0.8} q${r * 0.5} ${r * 0.8} 0 ${r * 1.6}`, stroke: "#ff5a5f", "stroke-width": 7, fill: "none", "stroke-linecap": "round" }, vib));
      const bz = txt(sv, px + 120, py - 30, "BZZZ", 40, "#ff5a5f", { opacity: 0, "font-weight": 900 });
      const [qx, qy] = P(2.55, 3.1, 1.1); const q = txt(sv, qx, qy, "?", 90, "#ff5a5f", { opacity: 0, "font-family": "EB Garamond" });
      const wi = at("L3", "wischt"), vi = at("L4", "vibriert"), ga = at("L4", "gar"), pv = at("L5", "Phantomvibration");
      tl.to(hand, { x: -26, y: -14, duration: 0.22, yoyo: true, repeat: 9, ease: "sine.inOut" }, wi - 0.1);
      tl.to(vib, { opacity: 1, duration: 0.05, repeat: 9, yoyo: true }, vi);
      tl.to(bz, { opacity: 1, x: 6, duration: 0.06, repeat: 9, yoyo: true }, vi);
      tl.to(me, { x: 4, duration: 0.05, repeat: 9, yoyo: true }, vi);
      tl.to([vib, bz], { opacity: 0, duration: 0.2 }, ga + 0.6);
      tl.to(ghost, { opacity: 0.6, duration: 0.2 }, ga);
      tl.fromTo(q, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, ga + 0.2);
      tl.to([vib, bz], { opacity: 1, duration: 0.05, repeat: 5, yoyo: true }, pv);''' + OUT)

S['s03'] = (FLAT + '''
    #s03-bt { left: 700px; top: 520px; width: 330px; height: 520px; padding-top: 24px; box-sizing: border-box; font: 800 30px/1.35 Inter, sans-serif; }
    #s03-bt .cap { width: 120px; height: 60px; margin: 0 auto 14px; border-radius: 12px; background: #4da3ff; }
    #s03-bt .lb { margin: 0 24px; padding: 18px 10px; border-radius: 16px; background: #e9f3ff; font-size: 26px; text-align: left; color: #44506e; }
    #s03-bt b { display: block; font-size: 34px; color: #22283f; text-align: center; margin-bottom: 8px; }
    #s03-two { left: 760px; top: 860px; width: 240px; height: 160px; text-align: center; font: 500 150px/160px "EB Garamond", serif; color: #ffd56b; text-shadow: 0 3px 18px rgba(0,0,0,.5); opacity: 0; }''',
SVG + '''
      <div id="s03-bt" class="flat"><div class="cap"></div><b>DESINFEKTION</b><div class="lb">Ethanol 70 %, Aqua, Glycerin, Wasserstoffperoxid, Hautpflege-Komplex …</div></div>
      <div id="s03-two" class="abs">2×</div>''',
'''      const sv = document.querySelector("#s03-svg");
''' + CAM + '''      sky(sv, "s03-sky", "#dfe9f2", "#f4f1ea");
      room(P, sv, 6, 6, 4.2, { wall: "#e3eef0", floor: "#b8c3c9" });
      const [cx, cy] = P(3.2, 0, 3.2); const clk = el("g", {}, sv);
      el("ellipse", { cx, cy, rx: 46, ry: 52, fill: "#fff", stroke: "#22283f", "stroke-width": 6 }, clk);
      const hm = el("path", { d: `M${cx} ${cy} V${cy - 36}`, stroke: "#22283f", "stroke-width": 6, "stroke-linecap": "round" }, clk);
      el("path", { d: `M${cx} ${cy} H${cx + 24}`, stroke: "#22283f", "stroke-width": 7, "stroke-linecap": "round" }, clk);
      wallY(P, sv, 0.8, 2.3, 2.0, 3.0, "#ffffff"); txt(sv, P(1.55, 0, 2.5)[0], P(1.55, 0, 2.5)[1] + 4, "BITTE WARTEN", 18, "#44506e", { "font-size": 28 });
      [0.9, 2.1, 3.3, 4.5].forEach((x, i) => { box(P, sv, x, 0.4, 0, 0.75, 0.75, 0.5, "#4f7fc9"); box(P, sv, x, 0.3, 0.5, 0.75, 0.12, 0.8, "#4f7fc9");
        if (i === 2) { person(P, sv, x + 0.5, 0.45, 0, { pose: "sit", shirt: "#ff8fd0" }); } });
      box(P, sv, 3.0, 2.2, 0, 1.4, 0.9, 0.45, "#c9a982");
      const btl = box(P, sv, 3.4, 1.0, 1.4, 0.18, 0.18, 0.4, "#4da3ff");
      const l7 = line("L7")[0], de = at("L7", "Desinfektionsmittel"), zw = at("L8", "Zweimal");
      tl.to(hm, { rotation: 300, svgOrigin: `${cx} ${cy}`, duration: 5, ease: "none" }, 0);
      tl.to(btl, { y: -10, duration: 0.3, yoyo: true, repeat: 3 }, l7 - 0.2);
      tl.fromTo("#s03-bt", { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, de - 0.4);
      tl.fromTo("#s03-two", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, zw - 0.05);''' + OUT)

S['s04'] = ('''    #s04-ring { left: 760px; top: 520px; width: 230px; height: 230px; opacity: 0; }''',
SVG + '''
      <svg id="s04-ring" class="abs" viewBox="0 0 230 230"><circle cx="115" cy="115" r="96" fill="rgba(13,16,38,.55)" stroke="#ffffff33" stroke-width="16"/>
        <circle id="s04-arc" cx="115" cy="115" r="96" fill="none" stroke="#ff5a5f" stroke-width="16" stroke-dasharray="603" stroke-dashoffset="0" transform="rotate(-90 115 115)" stroke-linecap="round"/>
        <text x="115" y="132" text-anchor="middle" font-family="EB Garamond" font-size="58" fill="#fff">47 s</text></svg>''',
'''      const sv = document.querySelector("#s04-svg");
''' + CAM + '''      sky(sv, "s04-sky", "#2c3352", "#4a5172");
      const lift = el("g", {}, sv);
      room(P, lift, 6, 6, 4.2, { wall: "#c4cad4", floor: "#8a909c" });
      wallY(P, lift, 3.6, 4.4, 1.6, 2.6, "#e8ecf2"); [0, 1, 2].forEach((k) => { const [bx, by] = P(4.0, 0, 1.8 + k * 0.28); el("circle", { cx: bx, cy: by, r: 8, fill: k === 1 ? "#ffd56b" : "#9aa2b0" }, lift); });
      const a = person(P, lift, 2.0, 2.2, 0, { shirt: "#ff8fd0" }), b = person(P, lift, 3.3, 3.0, 0, { shirt: "#6aa8e8", hair: "#c9a050" });
      const [ax, ay] = P(2.2, 2.4, 2.4), [bx2, by2] = P(3.5, 3.2, 2.4);
      const ex = [txt(lift, ax, ay - 20, "!", 64, "#ff5a5f", { opacity: 0, "font-weight": 900 }), txt(lift, bx2, by2 - 20, "!", 64, "#ff5a5f", { opacity: 0, "font-weight": 900 })];
      const sweat = el("path", { d: `M${ax + 30} ${ay + 20} q10 16 0 22 q-10 -6 0 -22Z`, fill: "#9dd6ff", opacity: 0 }, lift);
      const liv = el("g", { opacity: 0 }, sv);
      room(P, liv, 6, 6, 4.2, { wall: "#efe3d3", floor: "#b98f6a" });
      wallX(P, liv, 1.6, 4.2, 1.2, 2.7, "#22283f"); const scr = wallX(P, liv, 1.75, 4.05, 1.3, 2.6, "#3a4166");
      box(P, liv, 1.0, 2.0, 0, 0.9, 1.2, 0.35, "#a07a55");
      const ph = box(P, liv, 1.3, 2.4, 0.35, 0.3, 0.16, 0.03, "#1d1d24");
      box(P, liv, 3.4, 1.4, 0, 1.0, 3.2, 0.45, "#6a7fc9"); person(P, liv, 3.6, 2.6, 0.45, { pose: "sit", shirt: "#ff8fd0" });
      box(P, liv, 4.3, 1.4, 0.45, 0.25, 3.2, 0.7, "#5a6db5");
      const re = at("L9", "reden"), au = at("L9", "Augenkontakt"), l10 = line("L10")[0], n47 = at("L10", "47"), l11 = line("L11")[0], fi = at("L11", "Film"), oh = at("L11", "ohne");
      tl.to(lift, { x: 4, duration: 0.05, repeat: 3, yoyo: true }, 0.1);
      tl.to(ex, { opacity: 1, duration: 0.1 }, au - 0.1);
      tl.to(sweat, { opacity: 1, y: 30, duration: 0.6 }, au);
      tl.to([a, b], { y: -8, duration: 0.08, repeat: 5, yoyo: true }, au);
      tl.to(lift, { opacity: 0, duration: 0.3 }, l10 - 0.3);
      tl.to(liv, { opacity: 1, duration: 0.3 }, l10 - 0.2);
      tl.fromTo("#s04-ring", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, n47 - 0.3);
      tl.to("#s04-arc", { attr: { "stroke-dashoffset": 603 }, duration: 2.2, ease: "none" }, n47);
      tl.to("#s04-ring", { opacity: 0, duration: 0.3 }, l11 - 0.2);
      tl.to(scr, { attr: { fill: "#ffb36b" }, duration: 0.4 }, fi - 0.2);
      tl.to(scr, { attr: { fill: "#8fd0ff" }, duration: 0.8, repeat: 3, yoyo: true }, fi + 0.2);
      tl.to(ph, { y: -260, x: -120, rotation: -200, opacity: 0, svgOrigin: `${P(1.45, 2.48, 0.36).join(" ")}`, duration: 0.7, ease: "power2.in" }, oh);''' + OUT)

S['s05'] = (FLAT + '''
    #s05-bub { left: 560px; top: 520px; width: 440px; height: 190px; padding: 24px 26px; box-sizing: border-box; font: 500 40px/1.15 "EB Garamond", serif; color: #22283f; }''',
SVG + '''
      <div id="s05-bub" class="flat">„Kennst du schon den neuen Trend?“</div>''',
'''      const sv = document.querySelector("#s05-svg");
''' + CAM + '''      sky(sv, "s05-sky", "#ffe2c4", "#f6efe6");
      room(P, sv, 6, 6, 4.2, { wall: "#f1e4d4", floor: "#b98f6a" });
      const cal = []; for (let k = 0; k < 4; k++) cal.push(wallY(P, sv, 0.8, 1.9, 1.9, 3.1, k % 2 ? "#ffffff" : "#fff6e0", { stroke: "#d9cbb4", "stroke-width": 3 }));
      const [cx, cy] = P(1.35, 0, 2.6); const ct = txt(sv, cx, cy, "MAI", 30, "#ff5a5f");
      box(P, sv, 2.0, 0.6, 0, 3.4, 1.0, 0.5, "#8fa36a"); box(P, sv, 2.0, 0.4, 0.5, 3.4, 0.25, 0.8, "#7d915a");
      const me = person(P, sv, 2.8, 2.4, 0, { shirt: "#ff8fd0" });
      const oma = person(P, sv, 4.0, 2.9, 0, { shirt: "#9a7bd6", hair: "#e3e3e3", skin: "#f2cfaf" });
      const ph = box(P, sv, 3.85, 2.85, 1.25, 0.08, 0.26, 0.42, "#1d1d24");
      const [gx, gy] = P(3.85, 2.98, 1.46); const glow = el("circle", { cx: gx, cy: gy, r: 40, fill: "#ff8fd0", opacity: 0 }, sv);
      const [qx, qy] = P(3.0, 2.6, 2.4); const q = txt(sv, qx, qy, "?", 80, "#22283f", { opacity: 0, "font-family": "EB Garamond" });
      const dr = at("L12", "drei"), om = at("L13", "Oma");
      cal.slice(1).forEach((c, i) => tl.to(c, { y: -200, x: 80 + i * 40, rotation: 30, opacity: 0, svgOrigin: `${cx} ${cy}`, duration: 0.5, ease: "power2.in" }, dr - 0.2 + i * 0.25));
      tl.to(ct, { opacity: 0, duration: 0.1 }, dr - 0.2); tl.set(ct, { textContent: "JUNI" }, dr + 0.6); tl.to(ct, { opacity: 1, duration: 0.2 }, dr + 0.6);
      tl.to(glow, { opacity: 0.7, duration: 0.2 }, om - 0.6);
      tl.to(oma, { y: -26, duration: 0.18, yoyo: true, repeat: 5, ease: "power2.out" }, om - 0.1);
      tl.fromTo("#s05-bub", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, line("L12")[0] + 0.2);
      tl.fromTo(q, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, om + 0.4);''' + OUT)

S['s06'] = (FLAT + '''
    .s06-b { padding: 10px 22px; font: 500 40px "EB Garamond", serif; border-radius: 20px; }''',
SVG + '''
      <div id="s06-b1" class="flat s06-b" style="left:600px;top:520px">¡Hola!</div><div id="s06-b2" class="flat s06-b" style="left:760px;top:610px">Bonjour</div><div id="s06-b3" class="flat s06-b" style="left:620px;top:700px">Ciao</div>''',
'''      const sv = document.querySelector("#s06-svg");
''' + CAM + '''      sky(sv, "s06-sky", "#2c3360", "#5b4a7a");
      room(P, sv, 6, 6, 4.2, { wall: "#e9dfd0", floor: "#a8825e" });
      wallX(P, sv, 1.3, 3.3, 1.6, 3.4, "#1f2550"); wallX(P, sv, 1.3, 3.3, 1.6, 3.4, "none", { stroke: "#f4efe6", "stroke-width": 10 });
      box(P, sv, 1.8, 0.4, 0, 2.6, 1.2, 1.0, "#a07a55");
      box(P, sv, 2.0, 0.6, 1.0, 0.25, 0.25, 0.55, "#f2d06b");
      const lamp = el("circle", { cx: P(2.12, 0.72, 1.6)[0], cy: P(2.12, 0.72, 1.6)[1], r: 90, fill: "#ffe9a8", opacity: 0.35 }, sv);
      const COL = ["#e85d5d", "#4da3ff", "#6be3a0", "#ffd56b", "#ff8fd0", "#9a7bd6"], books = [];
      for (let k = 0; k < 12; k++) books.push(box(P, sv, 3.3 + (k % 2) * 0.05, 0.7, 1.0 + k * 0.16, 0.8, 0.55, 0.15, COL[k % 6], { opacity: 0 }));
      box(P, sv, 2.4, 2.0, 0, 0.6, 0.6, 0.5, "#8a6a4a");
      person(P, sv, 2.5, 2.05, 0, { pose: "sit", shirt: "#ff8fd0" });
      box(P, sv, 3.0, 2.0, 0.5, 0.12, 0.6, 0.95, "#8a6a4a");
      const n578 = at("L14", "578"), sp = at("L15", "Sprache"), bu = at("L15", "Bücher");
      tl.fromTo(lamp, { attr: { opacity: 0.25 } }, { attr: { opacity: 0.45 }, duration: 0.6, repeat: 7, yoyo: true }, 0);
      books.slice(0, 3).forEach((b, i) => tl.to(b, { opacity: 1, duration: 0.15 }, n578 + i * 0.2));
      ["#s06-b1", "#s06-b2", "#s06-b3"].forEach((b, i) => tl.fromTo(b, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, sp - 0.1 + i * 0.18));
      tl.to(["#s06-b1", "#s06-b2", "#s06-b3"], { opacity: 0, duration: 0.25 }, bu - 0.6);
      books.slice(3).forEach((b, i) => tl.fromTo(b, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.2, ease: "bounce.out" }, bu - 0.4 + i * 0.07));''' + OUT)

S['s07'] = ('',
SVG,
'''      const sv = document.querySelector("#s07-svg");
      sky(sv, "s07-sky", "#a9d6ff", "#e8f4ff");
      const Q = iso(300, 880, 46), w = el("g", { "data-layout-allow-overlap": "" }, sv);
      box(Q, w, -4, -3, -0.3, 40, 8, 0.3, "#8ccf7e");
      box(Q, w, -4, 0, 0, 40, 2, 0.04, "#6e7488");
      for (let k = 0; k < 20; k++) box(Q, w, -3 + k * 2, 0.9, 0.04, 1.0, 0.2, 0.02, "#ffffff");
      const cards = [];
      for (let k = 0; k < 14; k++) { const g = el("g", {}, w); const x = 1 + k * 2.4, y = -1.2;
        box(Q, g, x, y, 0, 0.12, 0.9, 1.5, ["#ff8fd0", "#4da3ff", "#ffd56b", "#6be3a0"][k % 4]);
        const [cx, cy] = Q(x + 0.12, y + 0.45, 0.75); el("path", { d: `M${cx - 10} ${cy - 16} L${cx + 14} ${cy} L${cx - 10} ${cy + 16}Z`, fill: "#fff" }, g); cards.push(g); }
      [2, 4, 6, 8, 10].forEach((km, i) => { const x = 3 + i * 7; box(Q, w, x, 2.4, 0, 0.15, 0.15, 1.2, "#ffffff"); const [tx, ty] = Q(x, 2.6, 1.5); txt(w, tx, ty, km + " KM", 30, "#22283f"); });
      const th = el("g", {}, w);
      box(Q, th, -2.6, 0.4, 0, 1.0, 1.1, 1.3, "#f0c8a0"); box(Q, th, -2.5, 0.5, 1.3, 0.8, 0.9, 0.6, "#f0c8a0"); box(Q, th, -2.45, 0.55, 1.9, 0.7, 0.8, 0.08, "#ffd9dd");
      const vi = at("L16", "100.000"), l17 = line("L17")[0], zl = at("L17", "Zehn-Kilometer-Lauf");
      cards.forEach((c, i) => tl.fromTo(c, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }, vi - 0.4 + i * 0.06));
      tl.to(w, { x: -1150, y: -665, duration: (C.__dur - l17) + 0.2, ease: "power1.inOut" }, l17 - 0.2);
      tl.to(th, { x: 1150, y: 665, duration: (C.__dur - l17) + 0.2, ease: "power1.inOut" }, l17 - 0.2);
      tl.to(th, { y: "-=14", duration: 0.2, yoyo: true, repeat: 11 }, l17);''' + OUT)

S['s08'] = ('''    #s08-phone { left: 250px; top: 430px; width: 580px; height: 760px; border: 22px solid #15161c; border-radius: 70px; box-shadow: 0 0 0 4px #3a3c48, 0 30px 80px rgba(0,0,0,.5); opacity: 0; }
    #s08-f { left: 340px; top: 1060px; width: 400px; height: 110px; border-radius: 55px; background: #ff3b5c; color: #fff; text-align: center; font: 800 52px/110px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 40px rgba(255,59,92,.5); }''',
SVG + '''
      <div id="s08-phone" class="abs"></div>
      <div id="s08-f" class="abs">+ Folgen</div>''',
'''      const sv = document.querySelector("#s08-svg");
''' + CAM + '''      sky(sv, "s08-sky", "#ff9a6b", "#ffd9a0");
      const sun = el("circle", { cx: 780, cy: 520, r: 110, fill: "#fff1b8", opacity: 0.9 }, sv);
      const w = el("g", {}, sv);
      box(P, w, -1, -1, -0.3, 8, 8, 0.3, "#7cc77f");
      box(P, w, 2.5, -1, 0, 1.2, 8, 0.03, "#e6d2a8");
      box(P, w, 0.6, 1.0, 0, 0.5, 0.5, 1.6, "#8a5a3a"); box(P, w, 0.0, 0.4, 1.6, 1.7, 1.7, 1.5, "#4aa35a");
      box(P, w, 4.2, 2.0, 0, 0.9, 2.6, 0.45, "#a07a55"); box(P, w, 4.95, 2.0, 0.45, 0.15, 2.6, 0.7, "#8a6a4a");
      person(P, w, 4.3, 2.6, 0.0, { pose: "sit", shirt: "#ff8fd0" }); person(P, w, 4.3, 3.6, 0.0, { pose: "sit", shirt: "#6aa8e8", hair: "#c9a050" });
      const l18 = line("L18")[0], ti = at("L19", "TikTok"), fo = at("L20", "folg");
      tl.to(sun, { attr: { cy: 560 }, duration: 6, ease: "none" }, 0);
      tl.to([w, sun], { scale: 0.62, svgOrigin: "540 800", duration: 0.6, ease: "power3.inOut" }, ti - 0.5);
      tl.fromTo("#s08-phone", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.inOut" }, ti - 0.5);
      tl.fromTo("#s08-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s08-f", { scale: 1.06, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
