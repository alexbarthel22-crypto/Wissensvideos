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

ME = '{ hood: "#2f6fe0", arm: "#2559b8", cap: "#ffd43b", label: "DU" }'
def one(c): return '{ one: true, hood: "%s", arm: "%s", label: "" }' % (c, c)
def walk(f, t0, n, step=0.28):  # zwei Beine im Wechsel
    return f'\n      for (let k = 0; k < {n}; k++) {{ tl.to({f}.lL, {{ rotation: k % 2 ? -18 : 18, svgOrigin: "-10 -60", duration: {step} }}, {t0} + k * {step}); tl.to({f}.lR, {{ rotation: k % 2 ? 18 : -18, svgOrigin: "10 -60", duration: {step} }}, {t0} + k * {step}); }}'
def hopjs(sel, t0, n, h=40, d=0.22):
    return f'\n      tl.to({sel}, {{ y: "-={h}", duration: {d}, yoyo: true, repeat: {2 * n - 1}, ease: "power1.out" }}, {t0});'

S['s01'] = ('''    #s01-bar { left: 0; right: 0; top: 300px; margin: 0 auto; width: fit-content; padding: 8px 28px; border-radius: 12px; background: #e0202f; color: #fff; font: 900 40px Inter, sans-serif; letter-spacing: .14em; box-shadow: 0 0 40px rgba(224,32,47,.9); }
    #s01-t { left: 30px; width: 1020px; top: 380px; text-align: center; color: #fff; font: 900 84px/1.04 Inter, sans-serif; text-shadow: 0 6px 0 rgba(0,0,0,.4), 0 0 30px rgba(0,0,0,.6); }
    #s01-t b { display: block; font-size: 150px; line-height: 1; color: #ff3b55; text-shadow: 0 0 60px rgba(255,59,85,.9), 0 8px 0 rgba(0,0,0,.4); }
    #s01-frame { left: 0; top: 0; width: 1080px; height: 1920px; box-shadow: inset 0 0 0 14px rgba(224,32,47,.9), inset 0 0 140px rgba(224,32,47,.6); }
    #s01-du { left: 0; width: 1080px; top: 1480px; text-align: center; font: 900 60px Inter, sans-serif; color: #ffd43b; opacity: 0; text-shadow: 0 0 30px rgba(255,212,59,1); }
    #s01-flash { left: 0; top: 0; width: 1080px; height: 1920px; background: #fff; opacity: 0; }''',
SVG + '''
      <div id="s01-frame" class="abs"></div>
      <div id="s01-bar" class="abs">● EILMELDUNG · LIVE</div>
      <div id="s01-t" class="abs" data-layout-allow-overlap>WAS WÄRE, WENN<br>DU DER EINZIGE<br>MENSCH MIT<b>2 BEINEN</b>WÄRST?</div>
      <div id="s01-du" class="abs">★ DAS BIST DU ★</div>
      <div id="s01-flash" class="abs"></div>''',
'''      const sv = document.querySelector("#s01-svg"); sky(sv, "s01g", "#2a0d24", "#0b0716");
      el("rect", { x: 0, y: 1290, width: 1080, height: 630, fill: "#1a0f22" }, sv);
      const crowd = []; for (let i = 0; i < 11; i++) { if (i === 5) continue; crowd.push(hop(sv, 60 + i * 96, 1250 + (i % 2) * 24, COLS[i % 6], 2.0)); }
      const F = finn(sv, 540, 1290, 1.9, ''' + ME + ''');
      const glow = el("ellipse", { cx: 540, cy: 1290, rx: 110, ry: 24, fill: "#ffd43b", opacity: 0 }, sv);
      const zw = at("L1", "zwei"), l2 = line("L2")[0], ei = at("L2", "ein"), l3 = line("L3")[0];
      tl.to("#s01-bar", { opacity: 0.35, duration: 0.25, yoyo: true, repeat: 15 }, 0);
      tl.to("#s01-frame", { opacity: 0.25, duration: 0.3, yoyo: true, repeat: 13 }, 0);''' + hopjs("crowd", "0.2", 20, 34, 0.2) + walk("F", "0.2", 14, 0.3) + '''
      tl.fromTo("#s01-flash", { opacity: 0.85 }, { opacity: 0, duration: 0.4, immediateRender: false }, zw - 0.05);
      tl.fromTo("#s01-t b", { scale: 1.35 }, { scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }, zw - 0.05);
      tl.to("#s01-t", { x: 12, duration: 0.04, repeat: 9, yoyo: true }, zw);
      tl.to(glow, { opacity: 0.6, duration: 0.3 }, zw);''' + pop("#s01-du", "ei") + '''
      tl.to("#s01-t", { opacity: 0.3, duration: 0.3 }, l3);''' + OUT)

S['s02'] = (BIGT, SVG + '''
      <div id="s02-a" class="bt r" style="top:470px;font-size:90px">😮‍💨 PUH …</div>''',
'''      const sv = document.querySelector("#s02-svg"); sky(sv, "s02g", "#ffb36b", "#e46a4e");
      el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#6e6a7a" }, sv); for (let k = 0; k < 6; k++) el("rect", { x: k * 200 + 40, y: 1240, width: 120, height: 14, fill: "#fff", opacity: 0.6 }, sv);
      const bus = el("g", {}, sv); el("rect", { x: 760, y: 880, width: 300, height: 260, rx: 30, fill: "#ffd43b" }, bus); el("rect", { x: 790, y: 920, width: 240, height: 90, rx: 12, fill: "#cfe8ff" }, bus);
      const F = finn(sv, 220, 1180, 1.9, ''' + ME + ''');
      const others = [0, 1, 2].map((i) => finn(sv, 420 + i * 120, 1190, 1.7, ''' + one('#ff4fb0') + '''));
      const sweat = others.map((o, i) => el("circle", { cx: 440 + i * 120, cy: 880, r: 9, fill: "#9fd8ff", opacity: 0 }, sv));
      const hu = at("L4", "hüpfen"), at_ = at("L5", "Atem");''' + walk("F", "0.6", 30, 0.3) + '''
      tl.to(F.g, { x: 620, duration: 9, ease: "none" }, 0.6);
      others.forEach((o, i) => { tl.to(o.g, { y: 1150, duration: 0.2, yoyo: true, repeat: 23, ease: "power1.out" }, hu - 0.3 + i * 0.07); tl.to(o.g, { x: "+=120", duration: 5, ease: "none" }, hu - 0.3); });
      tl.to(sweat, { opacity: 1, y: 40, duration: 0.6, stagger: 0.2 }, at_ - 1);''' + pop("#s02-a", "at_ - 0.1") + OUT)

S['s03'] = (BIGT, SVG, '''      const sv = document.querySelector("#s03-svg"); sky(sv, "s03g", "#3b4f8f", "#1a2246");
      const city = skyline(sv, 1000, 31, ["#2a3a6a", "#33437a", "#24345a"], 9, 220, 480);
      el("rect", { x: 0, y: 1000, width: 1080, height: 920, fill: "#2a2c3e" }, sv);
      const esc_ = el("g", {}, sv); el("path", { d: "M120 1180 L520 820 L600 820 L200 1180Z", fill: "#9aa3c0" }, esc_); for (let k = 0; k < 8; k++) el("line", { x1: 160 + k * 50, y1: 1144 - k * 45, x2: 240 + k * 50, y2: 1144 - k * 45, stroke: "#5a628a", "stroke-width": 6 }, esc_);
      const belt = el("g", {}, sv); el("rect", { x: 600, y: 1120, width: 460, height: 40, rx: 20, fill: "#9aa3c0" }, belt);
      const rails = el("g", { opacity: 0 }, sv); for (let k = 0; k < 5; k++) el("rect", { x: 90 + k * 200, y: 1050, width: 140, height: 14, rx: 7, fill: "#ffd43b" }, rails);
      const r1 = finn(sv, 260, 1060, 1.3, ''' + one('#39e27a') + '''), r2 = finn(sv, 700, 1120, 1.4, ''' + one('#4da3ff') + ''');
      const ro = at("L6", "Rolltreppen"), la = at("L6", "Laufbänder"), ha = at("L7", "Haltegriffe");
      tl.to(r1.g, { x: 470, y: 860, duration: 3, ease: "none" }, ro - 0.4);
      tl.to(r2.g, { x: 980, duration: 3, ease: "none" }, la - 0.3);
      tl.fromTo(rails, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, ha - 0.1);''' + OUT)

S['s04'] = (BIGT, SVG + '''
      <div id="s04-a" class="bt y" style="top:470px;font-size:110px">🥇 PLATZ 1</div><div id="s04-b" class="bt g" style="top:470px;font-size:110px">⚽ TOOOR!</div>''',
'''      const sv = document.querySelector("#s04-svg"); sky(sv, "s04g", "#5fa8ff", "#2a5fb8");
      el("rect", { x: 0, y: 1000, width: 1080, height: 920, fill: "#c4483a" }, sv); for (let k = 0; k < 4; k++) el("rect", { x: 0, y: 1040 + k * 70, width: 1080, height: 6, fill: "#fff", opacity: 0.8 }, sv);
      el("rect", { x: 960, y: 980, width: 10, height: 300, fill: "#fff" }, sv);
      const F = finn(sv, 120, 1110, 1.6, ''' + ME + ''');
      const rs = [0, 1, 2].map((i) => finn(sv, 120, 1180 + i * 70, 1.3, ''' + one('#a06bff') + '''));
      const sc = at("L8", "schnellste"), l9 = line("L9")[0], l10 = line("L10")[0], sch = at("L10", "schießen");''' + walk("F", "l9 - 1", 16, 0.14) + '''
      tl.to(F.g, { x: 900, duration: 2.4, ease: "power1.in" }, l9 - 1);
      rs.forEach((r, i) => { tl.to(r.g, { x: 320 + i * 40, duration: 2.4, ease: "none" }, l9 - 1); tl.to(r.g, { y: "-=30", duration: 0.2, yoyo: true, repeat: 11 }, l9 - 1); });''' + pop("#s04-a", "l9 + 1.2") + hide("#s04-a", "l10 - 0.2") + '''
      const ball = el("circle", { cx: 980, cy: 1080, r: 22, fill: "#fff", stroke: "#111", "stroke-width": 4, opacity: 0 }, sv);
      tl.set(ball, { opacity: 1 }, sch - 0.3); tl.fromTo(ball, { x: 0, y: 0 }, { x: -600, y: -400, duration: 0.5, ease: "power2.out", immediateRender: false }, sch);''' + pop("#s04-b", "sch + 0.3") + OUT)

S['s05'] = (BIGT + '''
    .s05-tag { position: absolute; top: 1090px; padding: 14px 26px; border-radius: 16px; background: #fff; color: #22283f; font: 900 52px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }''',
SVG + '''
      <div id="s05-a" class="s05-tag" style="left:120px">1 SCHUH · 89 €</div><div id="s05-b" class="s05-tag" style="left:560px;background:#e0202f;color:#fff">DU: 178 €</div>''',
'''      const sv = document.querySelector("#s05-svg"); sky(sv, "s05g", "#f2f0ea", "#d8d4c8");
      for (let r = 0; r < 3; r++) el("rect", { x: 80, y: 760 + r * 150, width: 920, height: 16, fill: "#9aa3b5" }, sv);
      const shoes = []; for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) { const x = 130 + c * 180, y = 760 + r * 150; const g = el("g", {}, sv); el("path", { d: `M${x} ${y} h80 q30 0 30 -24 v-10 h-60 l-20 -20 h-30Z`, fill: COLS[(r + c) % 6] }, g); el("rect", { x, y: y - 6, width: 110, height: 6, fill: "#fff" }, g); shoes.push(g); }
      const ei = at("L11", "einzeln"), zw = at("L11", "zwei"), do_ = at("L11", "doppelt");
      shoes.forEach((s, i) => tl.fromTo(s, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.2 }, 0.5 + i * 0.05));''' + pop("#s05-a", "ei - 0.1") + pop("#s05-b", "do_ - 0.1") + '''
      tl.to("#s05-b", { scale: 1.1, duration: 0.15, yoyo: true, repeat: 5 }, do_ + 0.2);''' + OUT)

S['s06'] = (BIGT, SVG + '''
      <div id="s06-a" class="bt y" style="top:470px;font-size:96px">✨ WUNDER</div>''',
'''      const sv = document.querySelector("#s06-svg"); sky(sv, "s06g", "#d8f0ff", "#9fd0f0"); el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#e6eef8" }, sv);
      const F = finn(sv, 540, 1180, 2.0, ''' + ME + ''');
      const docs = [200, 360, 720, 880].map((x, i) => { const w = woman(sv, x, 1190 - (i % 2) * 20, 1.7, "#ffffff", ["#6b4423", "#e0b050", "#3a2a1a", "#8a4b2a"][i]); return w; });
      const flash = []; for (let i = 0; i < 8; i++) flash.push(el("circle", { cx: 150 + i * 110, cy: 700 + (i % 2) * 80, r: 22, fill: "#fff", opacity: 0 }, sv));
      const un = at("L12", "untersuchen"), wu = at("L13", "Wunder");
      docs.forEach((d, i) => tl.fromTo(d.g, { opacity: 0, x: (i < 2 ? -200 : 1280) }, { opacity: 1, x: [200, 360, 720, 880][i], duration: 0.4, ease: "power3.out" }, un - 0.6 + i * 0.1));
      flash.forEach((f, i) => tl.fromTo(f, { opacity: 0 }, { opacity: 0.9, duration: 0.06, yoyo: true, repeat: 1, immediateRender: false }, un + i * 0.3));
      tl.to(F.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, un);''' + pop("#s06-a", "wu - 0.1") + OUT)

S['s07'] = (BIGT + '''
    .s07-c { position: absolute; padding: 12px 26px; border-radius: 18px; background: rgba(255,255,255,.96); color: #22283f; font: 900 48px Inter, sans-serif; opacity: 0; box-shadow: 0 16px 40px rgba(0,0,0,.4); }
    .s07-c b { color: #e0202f; }''',
SVG + '''
            <div id="s07-a" class="s07-c" style="left:80px;top:440px">👖 <b>1</b> Hosenbein</div><div id="s07-b" class="s07-c" style="left:560px;top:440px">🚲 <b>1</b> Pedal</div><div id="s07-c" class="s07-c" style="left:300px;top:560px">🚗 <b>1</b> Fußpedal</div>''',
'''      const sv = document.querySelector("#s07-svg"); sky(sv, "s07g", "#1a0a1a", "#050308"); el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#2a1a2a" }, sv);
      const F = finn(sv, 400, 1180, 2.0, ''' + ME + ''');
      const ch = el("g", { opacity: 0 }, sv); el("rect", { x: 650, y: 1020, width: 110, height: 22, rx: 6, fill: "#c79a5b" }, ch); el("rect", { x: 700, y: 1042, width: 12, height: 138, fill: "#a87d44" }, ch); el("rect", { x: 740, y: 860, width: 20, height: 170, rx: 6, fill: "#c79a5b" }, ch);
      const ha = at("L14", "Haken"), l15 = line("L15")[0], ho = at("L15", "Hosenbein"), pe = at("L15", "Pedal"), fu = at("L15", "Fußpedal"), l16 = line("L16")[0], sc = at("L16", "schmal");''' + pop("#s07-a", "ho - 0.2") + pop("#s07-b", "pe - 0.2") + pop("#s07-c", "fu - 0.2") + '''
      tl.to(["#s07-a", "#s07-b", "#s07-c"], { opacity: 0, duration: 0.2 }, l16 - 0.2);
      tl.to(ch, { opacity: 1, duration: 0.3 }, l16);
      tl.to(F.g, { x: 705, y: 1020, duration: 0.5 }, sc - 0.6);
      tl.to(F.g, { rotation: 14, svgOrigin: "0 0", duration: 0.08, yoyo: true, repeat: 7 }, sc - 0.1);
      tl.to(F.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, sc);''' + OUT)

S['s08'] = (BIGT, SVG, '''      const sv = document.querySelector("#s08-svg"); sky(sv, "s08g", "#3a3f5c", "#1e2236"); el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#2a2c3e" }, sv);
      const F = finn(sv, 540, 1180, 2.1, ''' + ME + ''');
      const ring = []; [[150, 1170], [290, 1200], [790, 1200], [930, 1170], [200, 1060], [880, 1060]].forEach(([x, y], i) => ring.push(finn(sv, x, y, 1.5 - (i > 3 ? 0.3 : 0), ''' + one('#9aa3c0') + ''')));
      const arrows = ring.map((r, i) => txt(sv, [150, 290, 790, 930, 200, 880][i], [820, 860, 860, 820, 780, 780][i], "👉", 60, "#fff", { opacity: 0 }));
      const ze = at("L17", "zeigen"), st = at("L17", "starren"), an = at("L18", "anders");
      tl.to(arrows, { opacity: 1, duration: 0.15, stagger: 0.08 }, ze - 0.1);
      ring.forEach((r) => tl.to(r.head, { rotation: 0, duration: 0.01 }, 0));
      tl.to(F.mouth, { attr: { d: "M-6 -149 Q0 -155 6 -149" }, duration: 0.15 }, st);
      tl.to(F.g, { scale: 1.9, duration: 0.6 }, an - 0.3);
      tl.to(sv, { scale: 1.12, svgOrigin: "540 900", duration: 1.5, ease: "power1.inOut" }, an - 0.4);''' + OUT)

S['s09'] = (BIGT + '''
    #s09-q { left: 90px; width: 900px; top: 470px; text-align: center; color: #fff; font: 900 74px/1.15 Inter, sans-serif; opacity: 0; text-shadow: 0 0 40px rgba(57,226,122,.5); }
    #s09-q b { color: #39e27a; }''',
SVG + '''
      <div id="s09-q" class="abs">„NORMAL“ =<br><b>WAS DIE MEISTEN HABEN</b></div>''',
'''      const sv = document.querySelector("#s09-svg"); sky(sv, "s09g", "#16305e", "#0c1a3a"); el("rect", { x: 0, y: 1150, width: 1080, height: 770, fill: "#14243f" }, sv);
      const ppl = []; const types = ["w", "one", "w", "one", "w", "one", "w"];
      for (let i = 0; i < 7; i++) { const x = 90 + i * 150; ppl.push(i === 3 ? finn(sv, x, 1180, 1.6, ''' + ME + ''') : finn(sv, x, 1180, 1.5, { hood: COLS[i % 6], arm: COLS[i % 6], label: "", one: i % 2 === 0 })); }
      const chair = el("g", { opacity: 0 }, sv); el("circle", { cx: 870, cy: 1150, r: 40, fill: "none", stroke: "#cfd8ea", "stroke-width": 8 }, chair);
      const no = at("L19", "Normal"), l20 = line("L20")[0], ge = at("L20", "genau");''' + pop("#s09-q", "no - 0.1") + '''
      tl.to(ppl.map((p) => p.g), { y: 1170, duration: 0.6, yoyo: true, repeat: 5, stagger: 0.1, ease: "sine.inOut" }, 0.3);
      tl.to("#s09-q", { opacity: 0.25, duration: 0.3 }, l20 + 0.5);
      tl.to(sv, { filter: "saturate(1.4)", duration: 0.6 }, ge);''' + OUT)

S['s10'] = ('''    #s10-t { left: 0; width: 1080px; top: 440px; text-align: center; color: #fff; font: 900 96px/1.05 Inter, sans-serif; text-shadow: 0 0 40px rgba(255,79,176,.6); opacity: 0; }
    .s10-b { position: absolute; top: 760px; width: 470px; height: 150px; border-radius: 30px; text-align: center; color: #fff; white-space: nowrap; font: 900 46px/150px Inter, sans-serif; opacity: 0; }
    #s10-y { left: 50px; background: #1fa65a; box-shadow: 0 0 50px rgba(57,226,122,.6); } #s10-n { left: 560px; background: #d32a45; box-shadow: 0 0 50px rgba(255,59,85,.6); }
    #s10-f { left: 290px; top: 960px; width: 500px; height: 110px; border-radius: 55px; background: #ff3b5c; color: #fff; text-align: center; font: 900 56px/110px Inter, sans-serif; opacity: 0; box-shadow: 0 10px 50px rgba(255,59,92,.7); }''',
'''      <div id="s10-t" class="abs">Und du?</div>
      <div id="s10-y" class="s10-b">🦵🦵 DER EINZIGE</div><div id="s10-n" class="s10-b">🦵 WIE ALLE</div>
      <div id="s10-f" class="abs">+ Folgen</div>''',
'''      const st = document.querySelector("#s10-stage"), sv = el("svg", { class: "full", viewBox: "0 0 1080 1920" }); st.insertBefore(sv, st.firstChild); sky(sv, "s10g", "#2a1f4f", "#0f0b22");
      const a = at("L21", "Einzige"), b = at("L21", "lieber"), fo = at("L22", "folg");
      tl.fromTo("#s10-t", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.1);
      tl.fromTo("#s10-y", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, a - 0.1);
      tl.fromTo("#s10-n", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, b - 0.1);
      tl.fromTo("#s10-f", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, fo - 0.1);
      tl.to("#s10-f", { scale: 1.08, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, fo + 0.4);''')
here = Path(__file__).parent
for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@CSS@@", css).replace("@@HTML@@", html).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
