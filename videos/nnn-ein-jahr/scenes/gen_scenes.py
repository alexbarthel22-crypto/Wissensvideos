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

GEO = '{ hood: "#1d1f2b", arm: "#15161f", undercut: "#f0d060", noPhones: true, tee: "#ffffff", chain: true, can: true, label: "" }'
GEO0 = '{ hood: "#1d1f2b", arm: "#15161f", undercut: "#f0d060", noPhones: true, tee: "#ffffff", chain: true, label: "" }'
END = '''
      tl.fromTo("@@SEL@@", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, @@T@@);'''
def pop(sel, t): return END.replace("@@SEL@@", sel).replace("@@T@@", t)

S['s01'] = ('''    #s01-ad { left: 0; right: 0; top: 330px; margin: 0 auto; width: fit-content; padding: 12px 34px; border-radius: 18px; background: #e0202f; color: #fff; font: 900 54px Inter, sans-serif; letter-spacing: .04em; box-shadow: 0 0 60px rgba(224,32,47,1); }
    #s01-t { left: 0; width: 1080px; top: 450px; text-align: center; }
    #s01-t .a { font: 900 175px/0.92 Inter, sans-serif; color: #ff4fb0; text-shadow: 0 0 50px rgba(255,79,176,.95), 0 8px 30px rgba(0,0,0,.7); }
    #s01-t .b { position: relative; display: inline-block; font: 900 124px/1.02 Inter, sans-serif; color: #fff; text-shadow: 0 8px 30px rgba(0,0,0,.8); }
    #s01-t .b s { position: absolute; left: -10px; right: -10px; top: 58px; height: 15px; border-radius: 6px; background: #ff2d4b; }
    #s01-j { left: 640px; top: 660px; font: 700 120px "Caveat", "Comic Sans MS", cursive; color: #ffd43b; transform: rotate(-10deg); text-shadow: 0 0 30px rgba(255,212,59,.8), 0 6px 20px rgba(0,0,0,.8); }
    #s01-bd { left: 40px; top: 800px; width: 640px; height: 250px; border-radius: 18px; background: #0b1a3a; border: 8px solid #3a4a6e; box-shadow: 0 20px 60px rgba(0,0,0,.6); }
    #s01-bd .h { height: 50px; background: #1f3a7a; color: #fff; font: 700 28px/50px "Space Mono", monospace; padding-left: 22px; letter-spacing: .1em; }
    #s01-bd .r { position: absolute; left: 22px; right: 22px; font: 700 31px/56px "Space Mono", monospace; color: #ffd43b; white-space: nowrap; }
    #s01-bd .r i { font-style: normal; color: #ff3b55; }
    #s01-vl { left: 0; width: 1080px; top: 840px; text-align: center; font: 900 120px Inter, sans-serif; color: #ff2d4b; opacity: 0; transform: rotate(-6deg); text-shadow: 0 0 40px rgba(255,45,75,1), 0 0 90px rgba(255,45,75,.8); }
    #s01-big { left: 0; width: 760px; top: 790px; text-align: center; font: 900 180px/1 Inter, sans-serif; color: #ffd43b; opacity: 0; text-shadow: 0 0 60px rgba(255,212,59,.9); }
    #s01-big small { display: block; font: 900 56px Inter, sans-serif; color: #fff; letter-spacing: .2em; }
    #s01-tag { left: 560px; top: 700px; padding: 10px 22px; border-radius: 14px; background: rgba(255,255,255,.96); color: #22283f; font: 800 46px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    #s01-eb { left: 0; width: 760px; top: 720px; text-align: center; font: 900 110px Inter, sans-serif; color: #ff3b55; opacity: 0; text-shadow: 0 0 40px rgba(255,59,85,.9); }
    #s01-flash { left: 0; top: 0; width: 1080px; height: 1920px; background: #fff; opacity: 0; }''',
SVG + '''
      <div id="s01-ad" class="abs">📢 ACHTUNG, DURCHSAGE!</div>
      <div id="s01-t" class="abs" data-layout-allow-overlap><div class="a">NO NUT</div><div class="b">NOVEMBER<s></s></div></div>
      <div id="s01-j" class="abs" data-layout-allow-overlap>JAHR!</div>
      <div id="s01-bd" class="abs"><div class="h">ABFAHRT · GLEIS 1</div>
        <div class="r" style="top:66px">00:00  NO NUT NOVEMBER</div><div class="r" style="top:120px">DAUER  <i>+335 TAGE</i></div><div class="r" style="top:174px">STATUS <i id="s01-st">VERLÄNGERT</i></div></div>
      <div id="s01-vl" class="abs" data-layout-allow-overlap>VERLÄNGERT</div>
      <div id="s01-big" class="abs"><span id="s01-n">30</span><small>TAGE</small></div>
      <div id="s01-tag" class="abs">Georg · 18</div>
      <div id="s01-eb" class="abs">ERDBEBEN?!</div>
      <div id="s01-flash" class="abs"></div>''',
'''      const sv = document.querySelector("#s01-svg"); sky(sv, "s01g", "#1b2346", "#0b0f22");
      el("rect", { x: 0, y: 1130, width: 1080, height: 790, fill: "#4a4f63" }, sv); el("rect", { x: 0, y: 1130, width: 1080, height: 22, fill: "#ffd43b" }, sv);
      const G = finn(sv, 860, 1150, 2.1, ''' + GEO + ''');
      const cs = el("g", {}, sv); el("rect", { x: 950, y: 1060, width: 90, height: 80, rx: 10, fill: "#7a4ad6" }, cs);
      const ad = at("L0", "Achtung"), ve = at("L1b", "verlängert"), ja = at("L2", "Jahr"), d3 = at("L2", "365"), ka = at("L2", "Kronjuwelen"), l3 = line("L3")[0], ge = at("L3", "Georg"), be = at("L3b", "bebt");
      tl.to("#s01-ad", { scale: 1.08, duration: 0.18, yoyo: true, repeat: 13 }, 0);
      tl.to("#s01-ad", { backgroundColor: "#ff4b5a", boxShadow: "0 0 100px rgba(255,45,75,1)", duration: 0.18, yoyo: true, repeat: 13 }, 0);
      tl.fromTo("#s01-flash", { opacity: 0.6 }, { opacity: 0, duration: 0.3, immediateRender: false }, ad - 0.05);
      tl.to("#s01-st", { color: "#ff0018", textShadow: "0 0 18px rgba(255,0,24,1)", duration: 0.15, yoyo: true, repeat: 9 }, ve - 0.1);
      tl.fromTo("#s01-vl", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, ve - 0.1);
      tl.to("#s01-vl", { textShadow: "0 0 70px rgba(255,45,75,1), 0 0 140px rgba(255,45,75,1)", duration: 0.2, yoyo: true, repeat: 5 }, ve + 0.15);
      tl.to(["#s01-t", "#s01-bd", "#s01-j", "#s01-ad"], { x: 12, duration: 0.04, repeat: 9, yoyo: true }, ve);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, ve);
      tl.to(["#s01-bd", "#s01-vl", "#s01-ad"], { opacity: 0, duration: 0.25 }, ja - 0.3);
      tl.fromTo("#s01-big", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ja - 0.1);
      count(tl, "#s01-n", 30, 365, ja, d3 - ja + 0.4, "", "", "power2.in");
      tl.to("#s01-big", { scale: 1.12, duration: 0.15, yoyo: true, repeat: 3 }, d3 + 0.4);
      tl.to(sv, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, ka);
      tl.to(["#s01-big", "#s01-t", "#s01-j"], { opacity: 0, duration: 0.25 }, l3 - 0.25);''' + pop("#s01-tag", "ge") + '''
      armsUp(tl, G, ge + 0.3, 0.3, 160); tl.to(G.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, ge + 0.3);
      tl.to("#s01-tag", { opacity: 0, duration: 0.2 }, be - 0.4); armsDown(tl, G, be - 0.4);''' + pop("#s01-eb", "be - 0.05") + '''
      tl.to([sv, "#s01-eb"], { x: 16, y: 6, duration: 0.04, repeat: 15, yoyo: true }, be);''' + OUT)

S['s02'] = (CHIP + '''
    #s02-v { left: 0; right: 0; margin: 0 auto; top: 470px; width: fit-content; padding: 14px 40px; border: 10px solid #ff2d4b; border-radius: 20px; color: #ff2d4b; background: rgba(255,255,255,.92); font: 900 86px Inter, sans-serif; letter-spacing: .06em; opacity: 0; transform: rotate(-7deg); }
    #s02-v small { display: block; font: 800 30px Inter, sans-serif; color: #22283f; letter-spacing: .1em; text-align: center; }''',
SVG + '''
      <div id="s02-v" class="abs" data-layout-allow-overlap>VERBOTEN<small>365 TAGE LANG</small></div>''',
'''      const sv = document.querySelector("#s02-svg"); sky(sv, "s02g", "#172048", "#0a0e26");
      el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#dfe8f4" }, sv);
      [[60, "#8a5a33"], [400, "#9a6a3d"], [740, "#8a5a33"]].forEach(([x, c]) => { const h = el("g", {}, sv); el("rect", { x, y: 760, width: 300, height: 300, fill: c }, h);
        el("path", { d: `M${x - 30} 770 L${x + 150} 640 L${x + 330} 770Z`, fill: "#eef4fb" }, h); el("rect", { x: x + 20, y: 840, width: 260, height: 90, fill: "#ffd78a" }, h); });
      const bulbs = []; for (let i = 0; i < 22; i++) bulbs.push(el("circle", { cx: 30 + i * 48, cy: 600 + Math.sin(i * 0.6) * 20, r: 9, fill: ["#ffd43b", "#ff4fb0", "#39e27a", "#4da3ff"][i % 4] }, sv));
      const sf = snowfall(sv, 60, 5, 300, 1200);
      const T = woman(sv, 330, 1150, 2.3, "#d0343f", "#5a3a22");
      const G = finn(sv, 720, 1150, 2.3, ''' + GEO0 + ''');
      const wurst = el("g", { opacity: 0 }, sv); el("rect", { x: 430, y: 880, width: 150, height: 40, rx: 20, fill: "#a0522d" }, wurst); el("rect", { x: 420, y: 895, width: 170, height: 22, rx: 11, fill: "#f2d6a2", opacity: 0.9 }, wurst);
      const sweat = [0, 1, 2].map((k) => el("circle", { cx: 690 + k * 30, cy: 760, r: 8, fill: "#9fd8ff", opacity: 0 }, sv));
      fall(tl, sf, C.__dur);
      tl.to(bulbs, { opacity: 0.4, duration: 0.3, yoyo: true, repeat: 15, stagger: 0.05 }, 0);
      const br = at("L5", "Bratwurst"), sc = at("L5", "schwitzt"), wu = at("L6", "Wurst"), vb = at("L6", "verboten");
      tl.to(T.aR, { rotation: -80, svgOrigin: "35 -126", duration: 0.3 }, br - 0.3);
      tl.fromTo(wurst, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, br - 0.1);
      tl.to(wurst, { x: 160, duration: 0.4 }, sc - 0.4);
      tl.to(sweat, { opacity: 1, y: 40, duration: 0.5, stagger: 0.15 }, sc);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, sc);
      tl.to(wurst, { scale: 1.6, svgOrigin: "665 900", duration: 0.3 }, wu - 0.1);
      tl.fromTo("#s02-v", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, vb - 0.15);
      tl.to(sv, { x: 10, duration: 0.04, repeat: 7, yoyo: true }, vb + 0.05);''' + OUT)

S['s10'] = (CHIP + '''
    #s10-ph { left: 300px; top: 470px; width: 480px; height: 640px; border-radius: 50px; background: linear-gradient(170deg, #2b1f5c, #0b0d1c); border: 10px solid #3a3f5c; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,.5); opacity: 0; }
    .s10-a { position: absolute; width: 100px; height: 100px; border-radius: 24px; }
    #s10-sc { left: 190px; top: 210px; width: 100px; height: 100px; border-radius: 24px; background: #fffc00; }
    #s10-sl { position: absolute; left: 160px; top: 318px; width: 160px; text-align: center; font: 700 22px Inter, sans-serif; color: #fff; }
    #s10-dl { position: absolute; left: 40px; right: 40px; top: 360px; padding: 20px; border-radius: 22px; background: #f1eefa; text-align: center; color: #22283f; font: 800 30px Inter, sans-serif; opacity: 0; }
    #s10-dl b { display: block; margin-top: 14px; padding: 10px; border-radius: 14px; background: #ff3b55; color: #fff; }''',
SVG + '''
      <div id="s10-ph" class="abs"><div class="s10-a" style="left:50px;top:80px;background:#ff4fb0"></div><div class="s10-a" style="left:190px;top:80px;background:#4da3ff"></div><div class="s10-a" style="left:330px;top:80px;background:#39e27a"></div>
        <div id="s10-sc" class="abs"></div><div id="s10-sl">Snapchat</div><div class="s10-a" style="left:50px;top:210px;background:#ff8a3d"></div><div class="s10-a" style="left:330px;top:210px;background:#a06bff"></div>
        <div id="s10-dl">„Snapchat“ löschen?<b>App löschen</b></div></div>
      <div id="s10-cl" class="chip" style="left:140px;top:1000px"><b>02:00</b> · 5 neue Snaps</div>''',
'''      const sv = document.querySelector("#s10-svg"); sky(sv, "s10g", "#1d1640", "#0b0820");
      const G = finn(sv, 880, 1160, 1.9, ''' + GEO + ''');
      const shards = []; const rs = rng(23); for (let i = 0; i < 12; i++) shards.push(el("rect", { x: 530 + rs() * 60, y: 720 + rs() * 60, width: 16, height: 16, fill: "#fffc00", opacity: 0 }, sv));
      const lo = at("L6b", "löscht"), l6c = line("L6c")[0], zw = at("L6c", "zwei"), ri = at("L6c", "Risiko");
      tl.fromTo("#s10-ph", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4 }, 1.0);
      tl.to("#s10-sc", { rotation: 6, duration: 0.08, yoyo: true, repeat: 9 }, lo - 0.6);
      tl.fromTo("#s10-dl", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, lo - 0.1);
      tl.to("#s10-dl b", { scale: 0.92, duration: 0.1, yoyo: true, repeat: 1 }, lo + 0.5);
      tl.to(["#s10-sc", "#s10-sl", "#s10-dl"], { opacity: 0, duration: 0.15 }, lo + 0.7);
      shards.forEach((sh, i) => tl.fromTo(sh, { opacity: 1, x: 0, y: 0 }, { opacity: 0, x: (rs() - 0.5) * 400, y: 200 + rs() * 200, rotation: rs() * 360, duration: 0.8, ease: "power2.out", immediateRender: false }, lo + 0.7));''' + pop("#s10-cl", "zw - 0.1") + '''
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, ri);''' + OUT)

S['s03'] = (CHIP + '''
    #s03-th { left: 470px; top: 470px; width: 560px; height: 300px; border-radius: 150px; background: #fff; box-shadow: 0 16px 40px rgba(0,0,0,.4); opacity: 0; overflow: hidden; text-align: center; }
    #s03-th .z { position: absolute; left: 70px; right: 70px; top: 110px; height: 80px; background: #111; color: #fff; font: 900 50px/80px Inter, sans-serif; letter-spacing: .14em; }
    #s03-th .k { position: absolute; left: 0; right: 0; top: 34px; font: 800 30px Inter, sans-serif; color: #ff4fb0; letter-spacing: .2em; }''',
SVG + '''
      <div id="s03-th" class="abs"><div class="k">KOPFKINO</div><div class="z">ZENSIERT</div></div>''',
'''      const sv = document.querySelector("#s03-svg"); sky(sv, "s03g", "#ffb3d1", "#d96a9c");
      el("rect", { x: 0, y: 1100, width: 1080, height: 820, fill: "#8a4a62" }, sv);
      const pairs = [[160, 820], [420, 760], [700, 820]].map(([x, y], i) => { const g = el("g", { opacity: 0 }, sv);
        tiny(g, x - 26, y + 40, "#ff4fb0", 1.7); tiny(g, x + 26, y + 40, "#4da3ff", 1.7); txt(g, x, y - 40, "♥", 60, "#ff2d6b"); return g; });
      const bub = [0, 1, 2].map((k) => el("circle", { cx: 790 - k * 50, cy: 820 + k * 60, r: 14 - k * 3, fill: "#fff", opacity: 0 }, sv));
      const G = finn(sv, 640, 1180, 2.0, ''' + GEO + ''');
      const pa = at("L7", "Pärchen"), ge = at("L8", "geküsst"), gk = at("L8", "gekuschelt"), ko = at("L8b", "Kopfkino"), ho = at("L8b", "Hochtouren");
      pairs.forEach((p, i) => { tl.fromTo(p, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, pa - 0.2 + i * 0.15); });
      pairs.forEach((p, i) => tl.to(p, { scale: 1.08, svgOrigin: "540 860", duration: 0.25, yoyo: true, repeat: 5 }, ge + i * 0.1));
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -153 6 -149" }, duration: 0.2 }, pa);
      tl.to(bub, { opacity: 1, duration: 0.15, stagger: 0.12 }, ko - 0.5);
      tl.fromTo("#s03-th", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ko - 0.1);
      tl.fromTo("#s03-th .z", { scaleX: 0 }, { scaleX: 1, duration: 0.25 }, ko + 0.3);
      tl.to("#s03-th", { rotation: 3, duration: 0.06, repeat: 9, yoyo: true }, ho);''' + OUT)

S['s04'] = (CHIP + '''
    #s04-n { left: 0; width: 1080px; top: 470px; text-align: center; font: 900 220px/1 Inter, sans-serif; color: #39e27a; opacity: 0; text-shadow: 0 0 60px rgba(57,226,122,.9); }''',
SVG + '''
      <div id="s04-n" class="abs">1,3</div>''',
'''      const sv = document.querySelector("#s04-svg"); sky(sv, "s04g", "#d8dde8", "#b4bccb");
      el("rect", { x: 0, y: 1080, width: 1080, height: 840, fill: "#7d6a55" }, sv);
      for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) { const x = 140 + c * 270, y = 700 + r * 170; if (r === 1 && c === 1) continue;
        const g = el("g", {}, sv); el("rect", { x: x - 80, y, width: 160, height: 14, fill: "#c79a5b" }, g); tiny(g, x, y - 4, ["#4da3ff", "#ff6a3d", "#39e27a", "#ffd43b"][(r + c) % 4], 1.5); }
      const G = finn(sv, 410, 1190, 2.2, ''' + GEO + ''');
      el("rect", { x: 280, y: 1020, width: 260, height: 26, rx: 6, fill: "#c79a5b" }, sv);
      const cans = [0, 1, 2, 3, 4].map((k) => { const g = el("g", { opacity: 0 }, sv); el("rect", { x: 560 + k * 34, y: 960, width: 26, height: 60, rx: 4, fill: "#2a4fa8" }, g); el("rect", { x: 560 + k * 34, y: 960, width: 13, height: 60, fill: "#c9d2e0" }, g); return g; });
      const pap = []; const rp = rng(8); for (let i = 0; i < 10; i++) pap.push(el("rect", { x: 420, y: 990, width: 60, height: 80, fill: "#fff", stroke: "#cfd5e2", "stroke-width": 2, opacity: 0 }, sv));
      const en = at("L9", "Energy"), ma = at("L9", "Maschine"), l10 = line("L10")[0];
      tl.to(cans, { opacity: 1, duration: 0.12, stagger: 0.12 }, en - 0.2);
      tl.to(G.aR, { rotation: -40, svgOrigin: "37 -126", duration: 0.06, yoyo: true, repeat: 40 }, ma - 2.0);
      pap.forEach((p, i) => tl.fromTo(p, { opacity: 1, x: 0, y: 0, rotation: 0 }, { x: 300 + rp() * 300, y: -300 - rp() * 300, rotation: rp() * 360, svgOrigin: "450 1030", opacity: 0, duration: 0.8, ease: "power2.out", immediateRender: false }, ma - 1.2 + i * 0.15));
      tl.fromTo("#s04-n", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, l10 + 0.6);
      armsUp(tl, G, l10 + 0.7, 0.3, 160); tl.to(G.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, l10 + 0.7);''' + OUT)

S['s05'] = (CHIP, SVG + '''
      <div id="s05-sp" class="chip" style="left:120px;top:500px;background:#ffd43b">SPERRZONE ⚠</div>''',
'''      const sv = document.querySelector("#s05-svg"); sky(sv, "s05g", "#5fc0ff", "#bfe9ff");
      const sun = el("circle", { cx: 880, cy: 520, r: 80, fill: "#ffd43b" }, sv);
      const sea = el("g", {}, sv); el("rect", { x: 0, y: 760, width: 1080, height: 160, fill: "#2fa8e8" }, sea);
      const waves = []; for (let k = 0; k < 3; k++) waves.push(el("path", { d: `M0 ${790 + k * 40} q60 -14 120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0`, stroke: "#bfe9ff", "stroke-width": 5, fill: "none", opacity: 0.7 }, sea));
      el("rect", { x: 0, y: 900, width: 1080, height: 1020, fill: "#f2dca6" }, sv);
      [[140, "#ff4fb0"], [760, "#39e27a"]].forEach(([x, c]) => { el("rect", { x: x + 46, y: 760, width: 8, height: 260, fill: "#8a6a44" }, sv); el("path", { d: `M${x - 70} 790 Q${x + 50} 680 ${x + 170} 790Z`, fill: c }, sv);
        const t = el("rect", { x: x - 40, y: 1010, width: 180, height: 60, rx: 10, fill: c, opacity: 0.6 }, sv); });
      const G = finn(sv, 540, 1150, 2.3, { swim: true, undercut: "#f0d060", noPhones: true, chain: true, can: true, label: "" });
      const mound = el("path", { d: "M260 1300 Q540 720 820 1300Z", fill: "#dcbd78", opacity: 0 }, sv);
      const l13 = line("L13")[0], bu = at("L13", "buddelt"), hu = at("L13", "Hüfte"), lu = at("L14", "Lust");
      waves.forEach((w) => tl.to(w, { x: -120, duration: 2, repeat: Math.ceil(C.__dur / 2), ease: "none" }, 0));
      tl.to(sun, { scale: 1.1, svgOrigin: "880 520", duration: 0.8, yoyo: true, repeat: 8 }, 0);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.2 }, 1.5);
      tl.fromTo(mound, { opacity: 0, attr: { d: "M420 1170 Q540 1150 660 1170Z" } }, { opacity: 1, attr: { d: "M240 1300 Q540 700 840 1300Z" }, duration: hu - bu + 0.4, ease: "power1.out" }, bu - 0.1);
      tl.to(G.g, { y: 1170, duration: hu - bu + 0.4 }, bu - 0.1);''' + pop("#s05-sp", "lu - 0.1") + '''
      tl.to(G.mouth, { attr: { d: "M-8 -153 Q0 -144 8 -153" }, duration: 0.15 }, lu + 0.3);''' + OUT)

S['s06'] = (CHIP + '''
    #s06-h { left: 0; width: 1080px; top: 470px; text-align: center; font: 900 96px Inter, sans-serif; color: #fff; opacity: 0; text-shadow: 0 0 40px rgba(255,79,176,.9); }
    #s06-sp { left: 380px; top: 500px; width: 520px; padding: 18px 26px; border-radius: 28px 28px 28px 6px; background: #fff; color: #22283f; font: 700 38px/1.25 Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }''',
SVG + '''
      <div id="s06-h" class="abs">72 STUNDEN</div>
      <div id="s06-sp" class="abs">Wollen wir mal kurz … <b style="color:#ff4fb0">aufs Klo?</b> 😉</div>
      <div id="s06-kr" class="chip" style="left:200px;top:470px;background:#ff3b55;color:#fff">SEHR KRITISCH</div>''',
'''      const sv = document.querySelector("#s06-svg"); sky(sv, "s06g", "#12082a", "#05030f");
      const beams = [0, 1, 2, 3, 4].map((k) => el("path", { d: `M${140 + k * 200} 380 L${40 + k * 200} 1140 L${240 + k * 200} 1140Z`, fill: ["#ff4fb0", "#4da3ff", "#39e27a", "#ffd43b", "#a06bff"][k], opacity: 0.18 }, sv));
      el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#120a24" }, sv);
      const dixi = el("g", { opacity: 0 }, sv); el("rect", { x: 820, y: 760, width: 190, height: 380, rx: 14, fill: "#2f6fe0" }, dixi); el("rect", { x: 800, y: 740, width: 230, height: 30, rx: 10, fill: "#2559b8" }, dixi); el("rect", { x: 840, y: 800, width: 50, height: 16, rx: 4, fill: "#39e27a" }, dixi);
      const crowd = []; for (let i = 0; i < 16; i++) crowd.push(tiny(sv, 40 + i * 68, 1180 + (i % 2) * 20, "#2a1f4f", 1.8));
      const G = finn(sv, 400, 1150, 2.3, ''' + GEO + ''');
      const Sd = woman(sv, 700, 1150, 2.3, "#111111", "#e0b050"); txt(Sd.g, 0, -100, "SECURITY", 9, "#ffd43b", { "data-layout-allow-overlap": "" });
      const heart = txt(sv, 700, 760, "♥", 70, "#ff4fb0", { opacity: 0 });
      const dr = at("L15", "drei"), l16 = line("L16")[0], kl = at("L16", "Klo"), l16b = line("L16b")[0], fl = at("L16b", "flüchtet");
      beams.forEach((b, i) => tl.to(b, { opacity: 0.4, duration: 0.25, yoyo: true, repeat: Math.floor(C.__dur / 0.5), ease: "none" }, i * 0.1));
      crowd.forEach((c, i) => tl.to(c, { y: -14, duration: 0.25, yoyo: true, repeat: Math.floor(C.__dur / 0.5) }, (i % 3) * 0.08));
      const n = Math.floor((l16 - 0.6) / 0.5); for (let k = 0; k < n; k++) { const t = 0.6 + k * 0.5; armsUp(tl, G, t, 0.2, k % 2 ? 160 : 90); tl.to(G.g, { y: 1130, duration: 0.2, yoyo: true, repeat: 1 }, t); }
      tl.fromTo("#s06-h", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3 }, dr - 0.1);
      tl.to("#s06-h", { opacity: 0, duration: 0.2 }, l16 - 0.2); armsDown(tl, G, l16);
      tl.fromTo(Sd.g, { x: 1000 }, { x: 650, duration: 0.4 }, l16);
      tl.to(heart, { opacity: 1, y: -30, duration: 0.3 }, l16 + 0.6);
      tl.to(dixi, { opacity: 1, duration: 0.3 }, kl - 0.5);
      tl.fromTo("#s06-sp", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, kl - 0.6);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -156 6 -149" }, duration: 0.15 }, kl);
      tl.to("#s06-sp", { opacity: 0, duration: 0.2 }, l16b - 0.1);''' + pop("#s06-kr", "l16b") + '''
      tl.to(G.g, { x: -200, duration: 0.5, ease: "power2.in" }, fl);''' + OUT)

S['s07'] = ('''    #s07-l { left: 110px; top: 470px; width: 860px; height: 620px; border-radius: 14px; background: #f6efdc; box-shadow: 0 24px 60px rgba(0,0,0,.5); color: #3a2a1a; opacity: 0; padding: 36px 46px; font: 600 40px/1.3 "EB Garamond", serif; }
    #s07-l h3 { font: 700 30px Inter, sans-serif; letter-spacing: .14em; color: #7a5a2a; margin: 0 0 14px; } #s07-l b { color: #b0262f; } #s07-l u { text-decoration: none; color: #1f7a3a; font-weight: 700; }
    #s07-l .seal { position: absolute; right: 46px; bottom: 34px; width: 110px; height: 110px; border-radius: 50%; background: #b0262f; color: #f6efdc; font: 900 52px/110px "EB Garamond", serif; text-align: center; }''',
SVG + '''
      <div id="s07-l" class="abs"><h3>KLOSTER ST. BENNO · BAYERN</h3>Lieber Georg,<br><span id="s07-a">mit Stolz haben wir gehört, dass du seit fast einem Jahr</span> <b id="s07-b">nicht mehr den Pilz gepflückt hast.</b><br><br><u id="s07-c">Wir hätten da eine Stelle frei.</u><div class="seal">✝</div></div>''',
'''      const sv = document.querySelector("#s07-svg"); sky(sv, "s07g", "#f2c27a", "#c9783a");
      el("rect", { x: 0, y: 1100, width: 1080, height: 820, fill: "#6b8a3a" }, sv);
      const leaves = []; const rl = rng(19); for (let i = 0; i < 26; i++) leaves.push(el("ellipse", { cx: rl() * 1080, cy: 300 + rl() * 400, rx: 14, ry: 8, fill: ["#e0702a", "#c9431f", "#ffb03a"][i % 3] }, sv));
      const G = finn(sv, 880, 1180, 1.9, ''' + GEO + ''');
      leaves.forEach((l, i) => tl.to(l, { y: 900, x: (i % 2 ? 60 : -60), rotation: 360, svgOrigin: `${l.getAttribute("cx")} ${l.getAttribute("cy")}`, duration: 5 + (i % 4), ease: "none" }, 0));
      const br = at("L17", "Brief"), l18 = line("L18")[0], pi = at("L18", "Pilz"), st = at("L18c", "Stelle");
      tl.fromTo("#s07-l", { opacity: 0, scale: 0.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.6)" }, br - 0.2);
      tl.fromTo(["#s07-a", "#s07-b", "#s07-c"], { opacity: 0.15 }, { opacity: 0.15, duration: 0.01 }, 0);
      tl.to("#s07-a", { opacity: 1, duration: 0.3 }, l18 + 0.3); tl.to("#s07-b", { opacity: 1, duration: 0.3 }, pi - 0.6);
      tl.fromTo("#s07-b", { color: "#b0262f" }, { color: "#ff0018", duration: 0.2, yoyo: true, repeat: 5, immediateRender: false }, pi);
      tl.to("#s07-c", { opacity: 1, duration: 0.3 }, st - 0.4);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -156 6 -149" }, duration: 0.15 }, pi); tl.to(G.head, { y: -10, duration: 0.15, yoyo: true, repeat: 1 }, st);''' + OUT)

S['s11'] = (CHIP, SVG + '''
      <div id="s11-gr" class="chip" style="left:120px;top:470px">Greta 💉</div>
      <div id="s11-mo" class="chip" style="left:600px;top:470px">Georg: <b>Mönch</b></div>''',
'''      const sv = document.querySelector("#s11-svg"); sky(sv, "s11g", "#2a1240", "#0c0518");
      el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#1a0c2a" }, sv);
      const pk = [[90, 1110], [990, 1110]].map(([x, y]) => { const g = el("g", {}, sv); el("ellipse", { cx: x, cy: y, rx: 70, ry: 56, fill: "#ff8a1f" }, g);
        el("path", { d: `M${x - 30} ${y - 12} l12 -16 l12 16Z M${x + 6} ${y - 12} l12 -16 l12 16Z M${x - 26} ${y + 16} q26 16 52 0`, fill: "#3a1a00" }, g); return g; });
      const lights = []; for (let i = 0; i < 20; i++) lights.push(el("circle", { cx: 30 + i * 54, cy: 420 + Math.sin(i * 0.7) * 16, r: 9, fill: ["#ff8a1f", "#a06bff", "#39e27a"][i % 3] }, sv));
      const Gr = woman(sv, 330, 1150, 2.3, "#f4f4f8", "#f0d060");
      el("rect", { x: -6, y: -118, width: 12, height: 34, fill: "#e0202f" }, Gr.g); el("rect", { x: -17, y: -107, width: 34, height: 12, fill: "#e0202f" }, Gr.g);
      el("path", { d: "M-16 -184 H16 L12 -196 H-12Z", fill: "#fff", stroke: "#e0202f", "stroke-width": 2 }, Gr.head); el("rect", { x: -3, y: -194, width: 6, height: 8, fill: "#e0202f" }, Gr.head);
      const G = finn(sv, 760, 1150, 2.3, ''' + GEO0 + ''');
      const robe = el("g", { opacity: 0 }, G.g); el("path", { d: "M-40 -138 Q0 -150 40 -138 L48 0 H-48Z", fill: "#7a5230" }, robe); el("rect", { x: -44, y: -72, width: 88, height: 8, fill: "#e8d29a" }, robe);
      el("path", { d: "M-26 -176 Q0 -206 26 -176 L26 -150 Q0 -164 -26 -150Z", fill: "#6a4424" }, robe);
      const gr = at("L19", "Greta"), kr = at("L19", "Krankenschwester"), mo = at("L19b", "Mönch");
      tl.to(lights, { opacity: 0.4, duration: 0.3, yoyo: true, repeat: 12, stagger: 0.05 }, 0);''' + pop("#s11-gr", "gr - 0.1") + '''
      tl.to(Gr.g, { rotation: -6, svgOrigin: "0 0", duration: 0.25, yoyo: true, repeat: 3 }, kr);
      tl.to(G.mouth, { attr: { d: "M-6 -149 Q0 -156 6 -149" }, duration: 0.15 }, kr); tl.to(G.head, { y: -12, duration: 0.15, yoyo: true, repeat: 1 }, kr + 0.2);
      tl.to(robe, { opacity: 1, duration: 0.2 }, mo - 0.3);''' + pop("#s11-mo", "mo - 0.1") + '''
      tl.to(G.mouth, { attr: { d: "M-6 -150 H6" }, duration: 0.15 }, mo);''' + OUT)

S['s08'] = ('''    #s08-c { left: 240px; top: 470px; width: 600px; height: 200px; border-radius: 26px; background: #07060f; border: 5px solid #2a2440; text-align: center; font: 700 150px/200px "Space Mono", monospace; color: #ff8a3d; text-shadow: 0 0 26px rgba(255,138,61,.9); opacity: 0; }
    #s08-eq { left: 0; right: 0; margin: 0 auto; top: 470px; width: fit-content; padding: 14px 36px; border: 10px solid #ff2d4b; border-radius: 20px; color: #fff; background: #e0202f; font: 900 70px/1.05 Inter, sans-serif; text-align: center; opacity: 0; box-shadow: 0 0 60px rgba(255,45,75,1); }
    #s08-eq small { display: block; font-size: 44px; color: #ffd43b; }''',
SVG + '''
      <div id="s08-c" class="abs">00:<span id="s08-t">1</span><span id="s08-n">0</span></div>
      <div id="s08-eq" class="abs" data-layout-allow-overlap>⚠ ERDBEBEN<small>STÄRKE 9,0</small></div>''',
'''      const sv = document.querySelector("#s08-svg"); sky(sv, "s08g", "#0d1030", "#05060f");
      const stars = []; const rs = rng(31); for (let i = 0; i < 30; i++) stars.push(el("circle", { cx: rs() * 1080, cy: 300 + rs() * 400, r: 2 + rs() * 2, fill: "#fff", opacity: 0.6 }, sv));
      el("rect", { x: 0, y: 1120, width: 1080, height: 800, fill: "#1a2a1a" }, sv);
      const H = el("g", {}, sv); el("rect", { x: 260, y: 760, width: 560, height: 360, fill: "#c9b38a" }, H); el("path", { d: "M220 770 L540 560 L860 770Z", fill: "#8a3a2a" }, H);
      const wins = [[320, 820], [620, 820], [320, 960], [620, 960]].map(([x, y]) => el("rect", { x, y, width: 140, height: 100, fill: "#ffd78a" }, H)); el("rect", { x: 480, y: 980, width: 120, height: 140, fill: "#5a3a22" }, H);
      const tiles = []; for (let i = 0; i < 10; i++) tiles.push(el("rect", { x: 300 + i * 50, y: 700 - Math.abs(i - 4.5) * 26, width: 40, height: 18, fill: "#a04a3a" }, sv));
      const cracks = el("path", { d: "M380 770 l30 60 l-20 40 l40 70 M720 790 l-30 50 l25 50 l-20 60", stroke: "#3a2a1a", "stroke-width": 6, fill: "none", opacity: 0 }, sv);
      const seis = el("path", { d: "M40 1520 H1040", stroke: "#39e27a", "stroke-width": 5, fill: "none", opacity: 0 }, sv);
      let d = "M40 1520"; const rq = rng(5); for (let x = 60; x <= 1040; x += 20) d += ` L${x} ${1520 + (rq() - 0.5) * (x > 300 ? 180 : 20)}`;
      const ze = at("L20", "zehn"), dr = at("L21", "Drei"), zw = at("L21", "zwei"), ei = at("L21", "eins"), mi = at("L22", "Mitternacht"), ju = at("L22", "Jürgen"), l23 = line("L23")[0], be = at("L23", "bebt"), sk = at("L23", "Stärke");
      tl.to("#s08-c", { opacity: 1, duration: 0.3 }, 1.7);
      tl.set("#s08-t", { textContent: "0" }, ze + (dr - ze) / 7); for (let k = 9; k >= 4; k--) tl.set("#s08-n", { textContent: String(k) }, ze + (10 - k) * (dr - ze) / 7);
      [[dr, "3"], [zw, "2"], [ei, "1"]].forEach(([t, v]) => { tl.set("#s08-n", { textContent: v }, t); tl.fromTo("#s08-c", { scale: 1.12 }, { scale: 1, duration: 0.3, immediateRender: false }, t); });
      tl.set("#s08-n", { textContent: "0" }, mi - 0.05); tl.set("#s08-c", { color: "#39e27a", textShadow: "0 0 30px rgba(57,226,122,1)" }, mi - 0.05);
      tl.to(wins.slice(0, 2), { attr: { fill: "#ffffff" }, duration: 0.1, yoyo: true, repeat: 7 }, ju - 0.2);
      tl.to(H, { x: 4, duration: 0.05, repeat: 11, yoyo: true }, ju);
      tl.to("#s08-c", { opacity: 0, duration: 0.2 }, l23 - 0.3);
      tl.to([H, tiles], { x: 26, y: 8, duration: 0.035, repeat: Math.floor((C.__dur - be) / 0.035) - 6, yoyo: true }, be - 0.1);
      tl.to(stars, { y: 14, duration: 0.05, repeat: 30, yoyo: true }, be);
      tiles.forEach((t, i) => tl.to(t, { y: 300 + i * 20, x: (i - 4.5) * 40, rotation: 200, svgOrigin: `${320 + i * 50} 700`, opacity: 0, duration: 1.2, ease: "power2.in" }, be + 0.3 + i * 0.08));
      tl.to(cracks, { opacity: 1, duration: 0.1 }, be + 0.2);
      tl.to(seis, { opacity: 1, attr: { d }, duration: 0.3 }, be);
      tl.fromTo("#s08-eq", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, sk - 0.15);''' + OUT)

S['s09'] = ('''    #s09-t { left: 0; width: 1080px; top: 440px; text-align: center; color: #fff; font: 900 90px/1.05 Inter, sans-serif; text-shadow: 0 0 40px rgba(255,79,176,.6); opacity: 0; }
    #s09-t small { display: block; margin-top: 20px; font: 800 44px Inter, sans-serif; color: #ff8fd0; letter-spacing: .1em; }
    .s09-b { position: absolute; top: 760px; width: 440px; height: 150px; border-radius: 30px; text-align: center; color: #fff; font: 900 56px/150px Inter, sans-serif; opacity: 0; }
    #s09-f { left: 290px; top: 960px; width: 500px; height: 120px; border-radius: 60px; background: #ff3b5c; color: #fff; text-align: center; font: 900 58px/120px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 40px rgba(255,59,92,.6); }
    #s09-y { left: 60px; background: #1fa65a; box-shadow: 0 0 50px rgba(57,226,122,.6); } #s09-n { left: 580px; background: #d32a45; box-shadow: 0 0 50px rgba(255,59,85,.6); }''',
'''      <div id="s09-t" class="abs">Würdest du<br>1 Jahr aushalten?<small>Wenn nein: wie lange?</small></div>
      <div id="s09-y" class="s09-b">JA, 365 TAGE</div><div id="s09-n" class="s09-b">NEIN, NUR …</div>
      <div id="s09-f" class="abs">+ Folgen</div>''',
'''      const st = document.querySelector("#s09-stage"), sv = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st.insertBefore(sv, st.firstChild); sky(sv, "s09g", "#2a1f4f", "#0f0b22");
      const a = at("L24", "Jahr"), b = at("L24", "wie");
      tl.fromTo("#s09-t", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.1);
      tl.fromTo("#s09-y", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, a - 0.1);
      tl.fromTo("#s09-n", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, b - 0.1);
      tl.to(["#s09-y", "#s09-n"], { scale: 1.06, duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut", stagger: 0.35 }, b + 0.4);
      const fo = at("L25", "folg");
      tl.fromTo("#s09-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s09-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 11, ease: "sine.inOut" }, fo + 0.4);''')

here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
