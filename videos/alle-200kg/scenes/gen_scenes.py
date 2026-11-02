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

BIGT = '''    .bt { position: absolute; left: 0; width: 1080px; text-align: center; font: 900 120px/1 Inter, sans-serif; color: #fff; opacity: 0; text-shadow: 0 0 40px rgba(0,0,0,.5), 0 8px 0 rgba(0,0,0,.35); }
    .bt.r { color: #ff3b55; text-shadow: 0 0 40px rgba(255,59,85,.8); } .bt.y { color: #ffd43b; text-shadow: 0 0 40px rgba(255,212,59,.7); } .bt.g { color: #39e27a; text-shadow: 0 0 40px rgba(57,226,122,.7); }'''
def pop(sel, t, s=0.5): return f'\n      tl.fromTo("{sel}", {{ opacity: 0, scale: {s} }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }}, {t});'
def hide(sel, t): return f'\n      tl.to("{sel}", {{ opacity: 0, duration: 0.2 }}, {t});'

S['s01'] = ('''    #s01-bar { left: 0; right: 0; top: 300px; margin: 0 auto; width: fit-content; padding: 8px 28px; border-radius: 12px; background: #e0202f; color: #fff; font: 900 40px Inter, sans-serif; letter-spacing: .14em; box-shadow: 0 0 40px rgba(224,32,47,.9); }
    #s01-t { left: 30px; width: 1020px; top: 380px; text-align: center; color: #fff; font: 900 92px/1.02 Inter, sans-serif; text-shadow: 0 6px 0 rgba(0,0,0,.4), 0 0 30px rgba(0,0,0,.6); }
    #s01-t b { display: block; font-size: 230px; line-height: .95; color: #ff3b55; text-shadow: 0 0 60px rgba(255,59,85,.9), 0 8px 0 rgba(0,0,0,.4); }
    #s01-frame { left: 0; top: 0; width: 1080px; height: 1920px; box-shadow: inset 0 0 0 14px rgba(224,32,47,.9), inset 0 0 140px rgba(224,32,47,.6); }
    #s01-d { left: 380px; top: 1006px; width: 320px; height: 96px; border-radius: 14px; background: #10131f; text-align: center; font: 700 70px/96px "Space Mono", monospace; color: #ff3b55; text-shadow: 0 0 20px rgba(255,59,85,.9); }
    #s01-flash { left: 0; top: 0; width: 1080px; height: 1920px; background: #fff; opacity: 0; }''',
SVG + '''
      <div id="s01-frame" class="abs"></div>
      <div id="s01-bar" class="abs">● EILMELDUNG · LIVE</div>
      <div id="s01-t" class="abs" data-layout-allow-overlap>WAS WÄRE, WENN<br>JEDER MENSCH<b>200 KG</b>WIEGEN WÜRDE?</div>
      <div id="s01-d" class="abs">200 kg</div>
      <div id="s01-flash" class="abs"></div>''',
'''      const sv = document.querySelector("#s01-svg"); sky(sv, "s01g", "#2a0d24", "#0b0716");
      const sc = el("g", {}, sv); el("rect", { x: 260, y: 960, width: 560, height: 230, rx: 40, fill: "#e9ecf5" }, sc); el("rect", { x: 280, y: 980, width: 520, height: 190, rx: 30, fill: "#cfd5e2" }, sc);
      const cr = el("path", { d: "M560 1000 l-30 50 l40 30 l-30 60 M620 1010 l30 40 l-20 40", stroke: "#22283f", "stroke-width": 6, fill: "none", opacity: 0 }, sv);
      const crowd = []; for (let i = 0; i < 9; i++) crowd.push(fat(sv, 90 + i * 112, 1680 + (i % 2) * 30, 0.9 + (i % 3) * 0.08, COLS[i % 6]));
      gsap.set(crowd.map((c) => c.g), { opacity: 0 });
      const z = at("L1", "200"), l2 = line("L2")[0], zw = at("L2", "zweihundert"), l3 = line("L3")[0], er = at("L3", "Erde");
      tl.to("#s01-bar", { opacity: 0.35, duration: 0.25, yoyo: true, repeat: 15 }, 0);
      tl.to("#s01-frame", { opacity: 0.25, duration: 0.3, yoyo: true, repeat: 13 }, 0);
      tl.to("#s01-d", { opacity: 0.4, duration: 0.15, yoyo: true, repeat: 11 }, 0);
      tl.fromTo("#s01-flash", { opacity: 0.85 }, { opacity: 0, duration: 0.4, immediateRender: false }, z - 0.05);
      tl.fromTo("#s01-t b", { scale: 1.3 }, { scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }, z - 0.05);
      tl.to([sc, "#s01-d"], { y: 14, duration: 0.05, repeat: 9, yoyo: true }, z);
      tl.to(cr, { opacity: 1, duration: 0.05 }, z + 0.1);
      crowd.forEach((c, i) => tl.fromTo(c.g, { opacity: 0, y: 1820 }, { opacity: 1, y: 1680 + (i % 2) * 30, duration: 0.3, ease: "back.out(2)" }, l2 + 0.2 + i * 0.12));
      crowd.forEach((c, i) => tl.to(c.g, { y: "-=14", duration: 0.18, yoyo: true, repeat: 3 }, zw + (i % 3) * 0.06));
      tl.to(["#s01-t", "#s01-bar"], { opacity: 0.25, duration: 0.3 }, l3);
      tl.to(sv, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, er);''' + OUT)

S['s02'] = (BIGT, SVG + '''
      <div id="s02-n" class="bt y" style="top:470px">400 MIO. T</div><div id="s02-m" class="bt r" style="top:470px">1,6 MRD. T</div><div id="s02-x" class="bt r" style="top:600px;font-size:90px">× 74</div>''',
'''      const sv = document.querySelector("#s02-svg"); sky(sv, "s02g", "#1d2146", "#0c0e24");
      const B = el("g", {}, sv); el("rect", { x: 530, y: 760, width: 20, height: 420, fill: "#9aa3c0" }, B); el("path", { d: "M440 1180 H640 L600 1140 H480Z", fill: "#9aa3c0" }, B);
      const beam = el("g", {}, B); el("rect", { x: 160, y: 750, width: 760, height: 16, rx: 8, fill: "#cfd5e2" }, beam);
      const pl = el("g", {}, beam); el("line", { x1: 220, y1: 758, x2: 220, y2: 900, stroke: "#9aa3c0", "stroke-width": 4 }, pl); el("path", { d: "M120 900 H320 Q300 940 220 940 Q140 940 120 900Z", fill: "#cfd5e2" }, pl);
      const pr = el("g", {}, beam); el("line", { x1: 860, y1: 758, x2: 860, y2: 900, stroke: "#9aa3c0", "stroke-width": 4 }, pr); el("path", { d: "M760 900 H960 Q940 940 860 940 Q780 940 760 900Z", fill: "#cfd5e2" }, pr);
      const hum = [0, 1, 2].map((k) => fat(pl, 160 + k * 60, 900, 0.55, COLS[k]));
      const ani = txt(pr, 860, 890, "🐘🦁🦌", 54, "#fff");
      txt(sv, 220, 1000, "MENSCHEN", 34, "#fff"); txt(sv, 860, 1000, "WILDE TIERE", 30, "#fff");
      const l4 = line("L4")[0], vi = at("L4", "400"), mi = at("L5", "Milliarden"), si = at("L6", "siebzigmal"), al = at("L6", "Alle");
      tl.fromTo(B, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4 }, 0.8);''' + pop("#s02-n", "vi - 0.1") + hide("#s02-n", "mi - 0.3") + pop("#s02-m", "mi - 0.2") + '''

      tl.fromTo(beam, { rotation: 0, svgOrigin: "540 758" }, { rotation: -14, svgOrigin: "540 758", duration: 0.8, ease: "bounce.out", immediateRender: false }, si - 0.2);

      pl.setAttribute("data-o", "220 758"); pr.setAttribute("data-o", "860 758");
''' + pop("#s02-x", "si") + '''
      tl.to(ani, { scale: 1.2, svgOrigin: "860 870", duration: 0.2, yoyo: true, repeat: 3 }, al);''' + OUT)

S['s03'] = (BIGT + '''
    #s03-sign { left: 300px; top: 440px; width: 480px; padding: 12px 0; border-radius: 14px; background: #10131f; border: 4px solid #9aa3c0; text-align: center; color: #fff; font: 800 38px/1.2 Inter, sans-serif; }
    #s03-ov { left: 0; right: 0; margin: 0 auto; top: 560px; width: fit-content; padding: 10px 30px; border-radius: 14px; background: #e0202f; color: #fff; font: 900 64px Inter, sans-serif; letter-spacing: .08em; opacity: 0; box-shadow: 0 0 40px rgba(224,32,47,.9); }''',
SVG + '''
      <div id="s03-sign" class="abs" data-layout-allow-overlap>MAX. 630 KG · 8 PERSONEN</div><div id="s03-ov" class="abs">⚠ ÜBERLAST</div>''',
'''      const sv = document.querySelector("#s03-svg"); sky(sv, "s03g", "#3a3f5c", "#1e2236");
      el("rect", { x: 140, y: 520, width: 800, height: 700, rx: 10, fill: "#c9ced9" }, sv); el("rect", { x: 160, y: 540, width: 760, height: 660, fill: "#e6e9f0" }, sv);
      for (let k = 0; k < 6; k++) el("line", { x1: 160 + k * 152, y1: 540, x2: 160 + k * 152, y2: 1200, stroke: "#d3d7e0", "stroke-width": 3 }, sv);
      const thin = []; for (let k = 0; k < 8; k++) thin.push(tiny(sv, 220 + (k % 4) * 180 + (k > 3 ? 90 : 0), 1060 + (k > 3 ? 110 : 0), COLS[k % 6], 2.2, { opacity: 0 }));
      const big = [0, 1, 2].map((k) => fat(sv, 300 + k * 240, 1190, 1.6, COLS[k + 1])); big.forEach((b) => gsap.set(b.g, { opacity: 0 }));
      const four = fat(sv, 1000, 1190, 1.6, COLS[4]); gsap.set(four.g, { opacity: 0 });
      const ac = at("L8", "acht"), l9 = line("L9")[0], dr = at("L9", "drei"), tr = at("L9", "Treppe");
      tl.fromTo("#s03-sign", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 1.8);
      tl.to(thin, { opacity: 1, duration: 0.12, stagger: 0.08 }, ac - 0.2);
      tl.to(thin, { opacity: 0, duration: 0.2 }, l9 - 0.1);
      big.forEach((b, i) => tl.fromTo(b.g, { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1.6, duration: 0.3, ease: "back.out(2)" }, dr - 0.2 + i * 0.12));
      tl.fromTo(four.g, { opacity: 1, x: 1180 }, { x: 960, duration: 0.3, immediateRender: false }, dr + 0.5);''' + pop("#s03-ov", "dr + 0.7") + '''
      tl.to("#s03-ov", { opacity: 0.4, duration: 0.15, yoyo: true, repeat: 7 }, dr + 1.0);
      tl.to(four.g, { x: 1200, duration: 0.4, ease: "power2.in" }, tr - 0.2);''' + OUT)

S['s04'] = (BIGT, SVG + '''
      <div id="s04-a" class="bt y" style="top:470px">× 3</div><div id="s04-b" class="bt r" style="top:470px">600 KG</div>''',
'''      const sv = document.querySelector("#s04-svg"); sky(sv, "s04g", "#2a2a55", "#151530");
      const st = el("g", {}, sv); for (let k = 0; k < 7; k++) el("rect", { x: 100 + k * 130, y: 1180 - k * 80, width: 1080, height: 80, fill: k % 2 ? "#5a5f8f" : "#6a6f9f" }, st);
      const F = fat(sv, 230, 1180, 1.7, "#ff6a3d");
      const knee = el("circle", { cx: 0, cy: 0, r: 34, fill: "none", stroke: "#ff3b55", "stroke-width": 8, opacity: 0 }, sv);
      const dr = at("L10", "Dreifache"), l11 = line("L11")[0], sx = at("L11", "600"), pr = at("L11", "Pro");
      for (let k = 0; k < 4; k++) tl.to(F.g, { x: 230 + (k + 1) * 130, y: 1180 - (k + 1) * 80, duration: 0.5, ease: "power1.inOut" }, 0.8 + k * 1.6);
      for (let k = 0; k < 4; k++) tl.to(F.g, { rotation: 4, svgOrigin: "0 0", duration: 0.25, yoyo: true, repeat: 1 }, 0.8 + k * 1.6);
      tl.set(knee, { attr: { cx: 230 + 2 * 130 + 18, cy: 1180 - 2 * 80 - 50 } }, 0);''' + pop("#s04-a", "dr - 0.1") + '''
      tl.to(F.body, { attr: { fill: "#ff3b55" }, duration: 0.3, yoyo: true, repeat: 9 }, dr);''' + hide("#s04-a", "sx - 0.3") + pop("#s04-b", "sx - 0.1") + '''
      tl.to(sv, { y: 8, duration: 0.04, repeat: 7, yoyo: true }, pr);''' + OUT)

S['s05'] = (BIGT + '''
    #s05-tk { left: 220px; top: 470px; width: 640px; padding: 16px 0; border-radius: 20px; background: #fff; text-align: center; color: #22283f; font: 900 60px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    #s05-tk s { color: #8a8fa8; } #s05-tk b { color: #e0202f; }''',
SVG + '''
      <div id="s05-tk" class="abs">TICKET: <s>99 €</s> <b>199 €+</b></div>''',
'''      const sv = document.querySelector("#s05-svg"); sky(sv, "s05g", "#5fa8ff", "#2a5fb8");
      const P = el("g", {}, sv); el("path", { d: "M540 380 Q700 440 720 620 V1500 Q720 1600 540 1650 Q360 1600 360 1500 V620 Q380 440 540 380Z", fill: "#eef2fa" }, P);
      el("path", { d: "M360 900 L60 1120 V1180 L360 1060Z M720 900 L1020 1120 V1180 L720 1060Z", fill: "#cfd8ea" }, P);
      const seats = []; for (let r = 0; r < 15; r++) for (let c = 0; c < 6; c++) seats.push(el("rect", { x: 392 + c * 50 + (c > 2 ? 16 : 0), y: 640 + r * 56, width: 40, height: 44, rx: 8, fill: "#4da3ff" }, P));
      const l12 = line("L12")[0], lu = at("L12", "Luxus"), ac = at("L13", "achtzig"), mi = at("L13", "mindestens");
      tl.fromTo(P, { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "power2.out" }, 0.6);
      const off = seats.filter((_, i) => i % 9 >= 4);
      tl.to(off, { attr: { fill: "#ff3b55" }, duration: 0.1, stagger: { each: 0.015, from: "random" } }, ac - 0.6);
      tl.to(P, { scale: 0.92, svgOrigin: "540 1000", duration: 0.3 }, mi - 0.6);''' + pop("#s05-tk", "mi - 0.2") + OUT)

S['s06'] = (BIGT + '''
    .s06-tag { position: absolute; top: 470px; width: 220px; height: 150px; border-radius: 18px; background: #fff; color: #22283f; text-align: center; font: 900 76px/150px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }''',
SVG + '''
      <div id="s06-k" class="bt r" style="top:470px;font-size:170px;transform:rotate(-8deg)">KNACK!</div>
      <div id="s06-m" class="s06-tag" style="left:250px"><s>M</s></div><div id="s06-x" class="s06-tag" style="left:560px;width:280px;color:#e0202f">XXXL</div>''',
'''      const sv = document.querySelector("#s06-svg"); sky(sv, "s06g", "#3a2f6e", "#221a48"); el("rect", { x: 0, y: 1180, width: 1080, height: 740, fill: "#2a2142" }, sv);
      const ch = el("g", {}, sv); el("rect", { x: 400, y: 1000, width: 280, height: 30, rx: 8, fill: "#c79a5b" }, ch); el("rect", { x: 640, y: 760, width: 30, height: 260, rx: 8, fill: "#c79a5b" }, ch);
      const legs = [[410, "L"], [650, "R"]].map(([x]) => el("rect", { x, y: 1030, width: 22, height: 150, fill: "#a87d44" }, ch));
      const F = fat(sv, 540, 1010, 1.6, "#4da3ff");
      const kn = at("L14", "Knack"), l15 = line("L15")[0], gr = at("L15", "Größe");
      tl.fromTo(F.g, { y: 800, opacity: 0 }, { y: 1010, opacity: 1, duration: 0.4, ease: "power2.in" }, 0.8);
      tl.to(legs[0], { rotation: -40, svgOrigin: "421 1030", duration: 0.2 }, kn - 0.05); tl.to(legs[1], { rotation: 40, svgOrigin: "661 1030", duration: 0.2 }, kn - 0.05);
      tl.to(ch, { y: 120, duration: 0.25, ease: "power3.in" }, kn - 0.05); tl.to(F.g, { y: 1150, duration: 0.25, ease: "power3.in" }, kn - 0.05);
      tl.to(F.mouth, { attr: { d: "M-7 -142 Q0 -150 7 -142" }, duration: 0.1 }, kn);''' + pop("#s06-k", "kn - 0.05", 2.2) + '''
      tl.to(sv, { x: 12, duration: 0.04, repeat: 9, yoyo: true }, kn + 0.1);''' + hide("#s06-k", "l15 - 0.3") + pop("#s06-m", "l15") + pop("#s06-x", "gr - 0.2") + '''
      tl.to("#s06-x", { scale: 1.12, duration: 0.2, yoyo: true, repeat: 3 }, gr + 0.2);''' + OUT)

S['s07'] = (BIGT + '''
    #s07-k { left: 0; width: 1080px; top: 470px; text-align: center; font: 900 130px/1 Inter, sans-serif; color: #ffd43b; opacity: 0; text-shadow: 0 0 40px rgba(255,212,59,.7); }
    #s07-k small { display: block; font: 800 40px Inter, sans-serif; color: #fff; letter-spacing: .2em; }''',
SVG + '''
      <div id="s07-k" class="abs"><span id="s07-v">2.000</span><small>KALORIEN PRO TAG</small></div>
      <div id="s07-l" class="bt r" style="top:470px;font-size:110px;transform:rotate(-6deg)">LEER!</div>''',
'''      const sv = document.querySelector("#s07-svg"), A = el("g", {}, sv); sky(A, "s07a", "#ffb36b", "#d9573e");
      el("ellipse", { cx: 540, cy: 1060, rx: 360, ry: 90, fill: "#fff" }, A); el("ellipse", { cx: 540, cy: 1050, rx: 300, ry: 70, fill: "#eef2fa" }, A);
      const food = ["🍔", "🍕", "🍝", "🍟", "🍗", "🍰", "🌭", "🥨"].map((e, i) => txt(A, 340 + (i % 4) * 130, 1040 - Math.floor(i / 4) * 110, e, 110, "#fff", { opacity: 0 }));
      const Bz = el("g", { opacity: 0 }, sv); sky(Bz, "s07b", "#f2f0ea", "#d8d4c8");
      for (let r = 0; r < 3; r++) el("rect", { x: 80, y: 700 + r * 170, width: 920, height: 18, fill: "#9aa3b5" }, Bz);
      const boxes = []; for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) boxes.push(el("rect", { x: 100 + c * 150, y: 600 + r * 170, width: 130, height: 100, rx: 10, fill: COLS[(r + c) % 6] }, Bz));
      const l16 = line("L16")[0], ka = at("L16", "3.500"), l17 = line("L17")[0], le = at("L17", "leer");
      tl.fromTo("#s07-k", { opacity: 0 }, { opacity: 1, duration: 0.3 }, l16 + 0.3);
      count(tl, "#s07-v", 2000, 3500, ka - 0.8, 1.0, "", "", "power2.in");
      tl.to(food, { opacity: 1, duration: 0.15, stagger: 0.15 }, ka - 0.6);
      tl.to("#s07-k", { opacity: 0, duration: 0.2 }, l17 - 0.2); tl.to(A, { opacity: 0, duration: 0.3 }, l17 - 0.1); tl.to(Bz, { opacity: 1, duration: 0.3 }, l17 - 0.1);
      tl.to(boxes, { opacity: 0, y: -40, duration: 0.15, stagger: { each: 0.06, from: "random" } }, l17 + 0.6);''' + pop("#s07-l", "le - 0.1", 2) + OUT)

S['s08'] = (BIGT, SVG + '''
      <div id="s08-g" class="bt y" style="top:470px;font-size:110px">TOOOR!</div>''',
'''      const sv = document.querySelector("#s08-svg"); sky(sv, "s08g", "#1a2a5a", "#0d1530");
      const T = el("g", {}, sv); for (let r = 0; r < 5; r++) el("rect", { x: 0, y: 760 + r * 110, width: 1080, height: 24, fill: "#4a5a8a" }, T);
      const fans = []; for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) fans.push(fat(T, 90 + c * 180 + (r % 2) * 60, 760 + r * 110, 0.7, COLS[(r * 6 + c) % 6]));
      const cracks = el("path", { d: "M120 1100 l60 40 l-30 50 l70 40 M700 1000 l-40 60 l50 30 l-30 70 M450 900 l30 50 l-40 40", stroke: "#fff", "stroke-width": 7, fill: "none", opacity: 0 }, sv);
      const red = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "#c4123a", opacity: 0 }, sv);
      const sp = at("L19", "springen");
      fans.forEach((f, i) => tl.to(f.g, { y: "-=6", duration: 0.3, yoyo: true, repeat: 7, ease: "sine.inOut" }, 0.5 + (i % 5) * 0.1));''' + pop("#s08-g", "sp - 0.4") + '''
      fans.forEach((f, i) => { tl.to(f.g, { y: "-=60", duration: 0.18, yoyo: true, repeat: 5, ease: "power2.out" }, sp + (i % 4) * 0.03); armsUpFat(f, sp); });
      tl.to(cracks, { opacity: 1, duration: 0.05 }, sp + 0.4);
      tl.fromTo(red, { opacity: 0 }, { opacity: 0.35, duration: 0.15, yoyo: true, repeat: 7, immediateRender: false }, sp + 0.4);
      tl.to(T, { x: 14, y: 10, duration: 0.04, repeat: 25, yoyo: true }, sp + 0.4);
      function armsUpFat(f, t) { tl.to(f.aL, { rotation: 140, svgOrigin: "-50 -110", duration: 0.2 }, t); tl.to(f.aR, { rotation: -140, svgOrigin: "50 -110", duration: 0.2 }, t); }''' + OUT)

S['s09'] = (BIGT + '''
    #s09-bmi { left: 140px; top: 1000px; width: 800px; height: 40px; border-radius: 20px; background: linear-gradient(90deg, #39e27a, #ffd43b 40%, #ff6a3d 60%, #e0202f); }
    #s09-mk { left: 900px; top: 975px; width: 16px; height: 90px; border-radius: 8px; background: #fff; box-shadow: 0 0 20px #fff; opacity: 0; }
    #s09-life { left: 140px; top: 1110px; width: 800px; height: 40px; border-radius: 20px; background: #39e27a; transform-origin: 0 50%; opacity: 0; }''',
SVG + '''
      <div id="s09-bmi" class="abs"></div><div id="s09-mk" class="abs"></div><div id="s09-life" class="abs"></div>
      <div id="s09-a" class="bt r" style="top:470px;font-size:96px">BMI 65</div><div id="s09-b" class="bt r" style="top:470px;font-size:96px">− 10 JAHRE</div>''',
'''      const sv = document.querySelector("#s09-svg"); sky(sv, "s09g", "#3a0d2a", "#150818");
      const H = el("path", { d: "M540 900 C 380 780, 400 640, 470 640 C 510 640, 540 670, 540 700 C 540 670, 570 640, 610 640 C 680 640, 700 780, 540 900Z", fill: "#ff3b55" }, sv);
      const l20 = line("L20")[0], ad = at("L20", "Adipositas"), l21 = line("L21")[0], ze = at("L21", "zehn");
      for (let k = 0; k < 14; k++) tl.fromTo(H, { scale: 1, svgOrigin: "540 770" }, { scale: 1.18, svgOrigin: "540 770", duration: 0.12, yoyo: true, repeat: 1, immediateRender: false }, 0.5 + k * (k < 5 ? 0.8 : 0.45));
      tl.fromTo("#s09-mk", { opacity: 0, x: -700 }, { opacity: 1, x: 0, duration: 0.8, ease: "power2.out" }, ad - 0.5);''' + pop("#s09-a", "ad - 0.1") + hide("#s09-a", "l21 - 0.2") + '''
      tl.fromTo("#s09-life", { opacity: 0, scaleX: 1 }, { opacity: 1, scaleX: 1, duration: 0.3 }, l21);
      tl.to("#s09-life", { scaleX: 0.86, backgroundColor: "#ff6a3d", duration: 0.8, ease: "power2.inOut" }, ze - 0.2);''' + pop("#s09-b", "ze - 0.1") + OUT)

S['s10'] = (BIGT + '''
    #s10-c { left: 140px; top: 470px; width: 800px; text-align: center; color: #fff; font: 800 40px/1.3 Inter, sans-serif; opacity: 0; }
    #s10-c b { color: #39e27a; font-size: 54px; }''',
SVG + '''
      <div id="s10-ok" class="bt g" style="top:470px">✓ NICHTS</div>
      <div id="s10-c" class="abs">ERDE: <b>6 TRILLIARDEN T</b><br>MENSCHEN: 1,6 MILLIARDEN T</div>''',
'''      const sv = document.querySelector("#s10-svg"); sky(sv, "s10g", "#0d1030", "#05060f");
      const st = []; const rs = rng(4); for (let i = 0; i < 40; i++) st.push(el("circle", { cx: rs() * 1080, cy: rs() * 1920, r: 1 + rs() * 2.5, fill: "#fff", opacity: 0.6 }, sv));
      const G = globe(sv, 540, 960, 260, "s10w", 60, 5); G.dots.forEach((d) => gsap.set(d, { opacity: 1 }));
      const ni = at("L22", "nichts"), l23 = line("L23")[0];
      tl.fromTo(G.g, { rotation: 0, svgOrigin: "540 960" }, { rotation: 20, svgOrigin: "540 960", duration: C.__dur, ease: "none" }, 0);''' + pop("#s10-ok", "ni - 0.1") + hide("#s10-ok", "l23 - 0.2") + pop("#s10-c", "l23") + OUT)

S['s11'] = ('''    #s11-t { left: 0; width: 1080px; top: 440px; text-align: center; color: #fff; font: 900 92px/1.05 Inter, sans-serif; text-shadow: 0 0 40px rgba(255,79,176,.6); opacity: 0; }
    .s11-b { position: absolute; left: 240px; width: 600px; height: 120px; border-radius: 30px; text-align: center; color: #fff; font: 900 58px/120px Inter, sans-serif; opacity: 0; }
    #s11-f { left: 290px; top: 1100px; width: 500px; height: 110px; border-radius: 55px; background: #ff3b5c; color: #fff; text-align: center; font: 900 56px/110px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 50px rgba(255,59,92,.7); }''',
'''      <div id="s11-t" class="abs">Was nervt dich<br>am meisten?</div>
      <div id="s11-a" class="s11-b" style="top:680px;background:#4da3ff">🛗 AUFZUG</div><div id="s11-b" class="s11-b" style="top:820px;background:#ff6a3d">✈️ FLUGZEUG</div><div id="s11-c" class="s11-b" style="top:960px;background:#a06bff">🪑 STUHL</div>
      <div id="s11-f" class="abs">+ Folgen</div>''',
'''      const st = document.querySelector("#s11-stage"), sv = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st.insertBefore(sv, st.firstChild); sky(sv, "s11g", "#2a1f4f", "#0f0b22");
      const a = at("L24", "Aufzug"), b = at("L24", "Flugzeug"), c = at("L24", "Stuhl"), fo = at("L25", "folg");
      tl.fromTo("#s11-t", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.1);
      [["#s11-a", a], ["#s11-b", b], ["#s11-c", c]].forEach(([id, t]) => tl.fromTo(id, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, t - 0.1));
      tl.fromTo("#s11-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s11-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);''')
here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
