#!/usr/bin/env python3
"""Erzeugt die Szenen s01, s02, s04–s09 für „Prophet Peter – Tag 1“ (hier ändern und neu erzeugen).

Figur und Kulisse kommen aus tools/characters/ (Serien-Bausteine, in jeder Folge gleich).
"""
from pathlib import Path

here = Path(__file__).parent
CHAR = here.parents[2] / "tools" / "characters"
SERIES_JS = (CHAR / "prophet-peter.js").read_text() + (CHAR / "grundstueck.js").read_text()

HEAD = '''<template>
  <style>
    /*__COMMON_CSS__*/
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .panel { position: absolute; border-radius: 24px; background: rgba(13,10,30,.9); text-align: center; color: #fff;
      font-family: "Inter", sans-serif; font-weight: 900; }
    .lbl { position: absolute; font-family: "Inter", sans-serif; font-weight: 900; color: #fff; text-align: center; white-space: nowrap;
      padding: 14px 30px; border-radius: 18px; background: rgba(13,10,30,.9); border: 4px solid #ffd43b; box-shadow: 0 0 34px rgba(255,212,59,.45); opacity: 0; }
    .lbl small { display: block; font-family: "Space Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .16em; color: #f4d27a; }
    .plate { position: absolute; font-family: "Inter", sans-serif; font-weight: 900; color: #fff; text-align: center; }
    /* Vordergrund 110 px tiefer = besser zentriert zwischen Kapitel-Marke und Untertiteln (Hintergrund/Filmlook bleiben) */
    .fgwrap { transform: translateY(110px); }
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
@@SERIES@@
      const tl = gsap.timeline({ paused: true });
      const bg = document.querySelector("#@@ID@@-bg"), sv = document.querySelector("#@@ID@@-svg"), fx = document.querySelector("#@@ID@@-fx");
      if (fx) filmLook(fx, "@@ID@@f");
@@JS@@
      window.__timelines["@@ID@@"] = tl;
    })();
  </script>
</template>
'''
OUT = '\n      tl.to("#@@ID@@-stage > *", { opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }, C.__dur - 0.18);'
BG = '      <svg id="@@ID@@-bg" class="full" viewBox="0 0 1080 1920"></svg>'
SVG = '      <svg id="@@ID@@-svg" class="full" viewBox="0 0 1080 1920"></svg>'
FX = '      <svg id="@@ID@@-fx" class="full" viewBox="0 0 1080 1920"></svg>'
S = {}

# ---------- s01 Hook: TAG 1 – ICH GRÜNDE EINE SEKTE (alles ab Frame 0 lesbar, jedes gesprochene Wort leuchtet groß auf) ----------
S['s01'] = ('''    #s01-title { left: 0; width: 1080px; top: 50px; text-align: center; }
    #s01-heaven { left: 0; top: 0; width: 1080px; height: 1920px; opacity: .9;
      background: repeating-conic-gradient(from 180deg at 50% -4%, rgba(255,236,170,.30) 0deg 3deg, rgba(255,236,170,0) 3deg 9deg);
      -webkit-mask-image: radial-gradient(ellipse 80% 70% at 50% 0%, #000 30%, transparent 80%); mask-image: radial-gradient(ellipse 80% 70% at 50% 0%, #000 30%, transparent 80%); }
    #s01-glow { left: -100px; top: 150px; width: 1280px; height: 1100px; background: radial-gradient(ellipse 50% 45% at 50% 45%, rgba(255,226,140,.55), rgba(255,180,90,.18) 55%, rgba(255,180,90,0) 75%); }
    #s01-ring { left: 190px; top: 20px; width: 700px; height: 700px; border-radius: 50%; border: 6px solid rgba(255,230,150,.7); box-shadow: 0 0 60px rgba(255,214,110,.8), inset 0 0 60px rgba(255,214,110,.5); }
    .s01-sp { position: absolute; width: 10px; height: 10px; border-radius: 50%; background: #fff6d0; box-shadow: 0 0 14px 4px rgba(255,220,120,.9); }
    /* Wörter auf farbigen Kästen, damit der Text vor dem hellen Himmel auffällt */
    #s01-title .k, #s01-title .d, #s01-title .h { font-family: "Inter", sans-serif; font-weight: 900; letter-spacing: -.02em; }
    #s01-title .k { font-size: 96px; line-height: 1.2; margin-bottom: 14px; }
    #s01-title .d { font-size: 170px; line-height: 1.1; }
    #s01-title .h { margin-top: 22px; font-size: 118px; line-height: 1.32; }
    .s01-w { position: relative; display: inline-block; margin: 0 6px; padding: 2px 24px 8px; border-radius: 22px; transform-origin: 50% 55%;
      background: rgba(28,10,58,.9); border: 5px solid rgba(255,214,110,.85); color: #fff;
      box-shadow: 0 0 34px rgba(255,200,90,.45), 0 12px 0 rgba(0,0,0,.35); text-shadow: 0 6px 0 rgba(0,0,0,.45); }
    #s01-title .d .s01-w { color: #ffd43b; text-shadow: 0 0 40px rgba(255,212,59,.6), 0 8px 0 rgba(0,0,0,.5); }
    .s01-kn { background: #c8102e !important; border-color: #ffb3bf !important; color: #fff; box-shadow: 0 0 50px rgba(255,40,70,.8), 0 12px 0 rgba(0,0,0,.35) !important; }
    #s01-w6 { background: #ff4fb0; border-color: #ffd1ec; box-shadow: 0 0 50px rgba(255,79,176,.75), 0 12px 0 rgba(0,0,0,.35); }
    #s01-flash { background: #ffffff; opacity: 0; mix-blend-mode: overlay; }
    .s01-bar { position: absolute; left: 0; width: 1080px; height: 120px; background: #000; }''',
BG + '''
      <svg id="s01-vis" class="full noshift" viewBox="0 0 1080 1920"></svg>
''' + SVG + '''
      <div id="s01-heaven" class="abs noshift"></div>
      <div id="s01-glow" class="abs"></div><div id="s01-ring" class="abs"></div><div id="s01-sps" class="abs" style="left:0;top:0"></div>
      <div id="s01-flash" class="full noshift"></div>
      <div id="s01-title" class="abs"><div class="k"><span id="s01-k1" class="s01-w s01-kn">AUF</span> <span id="s01-k2" class="s01-w s01-kn">DIE</span> <span id="s01-k3" class="s01-w s01-kn">KNIE!</span></div><div class="d"><span id="s01-w1" class="s01-w">TAG</span> <span id="s01-w2" class="s01-w">1</span></div>
        <div class="h"><span id="s01-w3" class="s01-w">ICH</span> <span id="s01-w4" class="s01-w">GRÜNDE</span><br><span id="s01-w5" class="s01-w">EINE</span> <span id="s01-w6" class="s01-w">SEKTE</span></div></div>
      <div class="s01-bar noshift" style="top:0"></div><div class="s01-bar noshift" style="top:1800px"></div>
''' + FX,
'''      const G = grundstueck(bg, "s01g", { mood: "dusk", goatX: 440, goatS: 0.6 }); gsap.set(G.rays, { opacity: 0.55 });
      floatDust(tl, G, C.__dur); chew(tl, G, 0, C.__dur - 0.3);
      // Visionen schon ab Frame 0 angedeutet: goldene, gestrichelte Geister-Umrisse von Tempel, Gärten und Pilgerstraße über dem Grundstück
      const vis = document.querySelector("#s01-vis"), vg = el("g", { transform: "translate(745 1190) scale(0.72) translate(-540 -920)", opacity: 0.8 }, vis);
      vg.style.filter = "drop-shadow(0 0 12px rgba(255,212,59,.95))";
      const vd = (d, c = "#ffe08a", w = 9) => el("path", { d, stroke: c, "stroke-width": w, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-dasharray": "16 12" }, vg);
      const ghosts = [vd("M300 900 L780 900 L780 920 L300 920Z"), vd("M330 880 L750 880"), vd("M340 880 L340 720 M410 880 L410 720 M480 880 L480 720 M600 880 L600 720 M670 880 L670 720 M740 880 L740 720"),
        vd("M320 720 L760 720 L540 640Z"), vd("M430 650 Q540 470 650 650"), vd("M540 520 L540 470 M520 490 L560 490"), vd("M505 690 q35 -22 70 0 q-35 22 -70 0Z", "#ff8fd0", 6),
        vd("M470 925 L250 1120"), vd("M610 925 L830 1120")];
      [[150, 980], [930, 990], [80, 1050], [1000, 1050]].forEach(([x, y]) => { ghosts.push(vd(`M${x} ${y} l0 -40`, "#7dffb0")); ghosts.push(vd(`M${x - 30} ${y - 40} a30 30 0 1 1 60 0 a30 30 0 1 1 -60 0`, "#7dffb0")); });
      tl.fromTo(ghosts, { strokeDashoffset: 0 }, { strokeDashoffset: -112, duration: C.__dur, ease: "none" }, 0);
      tl.fromTo(vg, { opacity: 0.65 }, { opacity: 0.95, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0);
      // Chor auf Frame 0: Licht pulsiert, Titel ruckt kurz
      tl.fromTo(G.rays, { opacity: 1 }, { opacity: 0.55, duration: 0.8, ease: "power2.out", immediateRender: false }, 0.02);
      tl.fromTo("#s01-title", { scale: 1.04 }, { scale: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, 0.02);
      tl.fromTo(bg, { scale: 1.1, transformOrigin: "60% 55%" }, { scale: 1.0, duration: C.__dur, ease: "none" }, 0);
      // jedes gesprochene Wort wird groß (eigener Kasten springt nach vorn), danach zurück auf Normalgröße, leuchtend
      gsap.set(".s01-w", { filter: "brightness(0.85)" });
      [["#s01-k1", "auf", "#ff3b55"], ["#s01-k2", "die", "#ff3b55"], ["#s01-k3", "knie", "#ff3b55"], ["#s01-w1", "tag", "#ffd43b"], ["#s01-w2", "eins", "#ffd43b"], ["#s01-w3", "ich", "#ffd36e"], ["#s01-w4", "gründe", "#ffd36e"], ["#s01-w5", "eine", "#ffd36e"], ["#s01-w6", "sekte", "#ff4fb0"]].forEach(([sel, w, c], i) => {
        const ORD = ["auf", "die", "knie", "tag", "eins", "ich", "gründe", "eine", "sekte"], t = at("L1", w), nx = i < 8 ? at("L1", ORD[i + 1]) : C.__dur - 0.3;
        tl.set(sel, { zIndex: 5 }, t - 0.04);
        tl.to(sel, { scale: 1.32, filter: `brightness(1.25) drop-shadow(0 0 30px ${c})`, duration: 0.09, ease: "power2.out" }, t - 0.04);
        tl.to(sel, { scale: 1.0, filter: `brightness(1.08) drop-shadow(0 0 14px ${c})`, duration: 0.22, ease: "power2.out" }, Math.max(t + 0.08, nx - 0.2));
        tl.set(sel, { zIndex: 1 }, Math.max(t + 0.3, nx));
      });
      // Himmelslicht: Strahlen drehen langsam, Ring + Glühen atmen, Lichtfunken steigen auf
      tl.fromTo("#s01-heaven", { rotation: -4, transformOrigin: "50% 0%" }, { rotation: 4, duration: C.__dur, ease: "none" }, 0);
      tl.fromTo("#s01-ring", { scale: 0.92, opacity: 0.5 }, { scale: 1.06, opacity: 1, duration: C.__dur, ease: "sine.inOut" }, 0);
      tl.fromTo("#s01-glow", { opacity: 0.75 }, { opacity: 1, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0);
      const RS = rng(91), spc = document.querySelector("#s01-sps");
      for (let i = 0; i < 34; i++) { const d = document.createElement("div"); d.className = "s01-sp"; const x = 80 + RS() * 900, y = 300 + RS() * 900;
        Object.assign(d.style, { left: x + "px", top: y + "px", transform: `scale(${0.4 + RS()})` }); spc.appendChild(d);
        tl.fromTo(d, { opacity: 0, y: 0 }, { opacity: 0.4 + RS() * 0.6, y: -120 - RS() * 160, duration: C.__dur, ease: "none" }, 0); }
      // Prophet Peter steht ab Frame 0 links im Bild (segnend)
      const P = peter(sv, "s01p", 205, 1225, 0.53, { arms: [14, -120] });
      P.g.style.filter = "drop-shadow(0 0 30px rgba(255,220,130,.55))";
      talk(tl, P, line("L1")[0], line("L1")[1]);
      tl.fromTo(P.spark, { scale: 0.5, svgOrigin: "-187 -850" }, { scale: 1.6, duration: 0.2, yoyo: true, repeat: 5 }, 0.1);
      tl.to(P.armL, { rotation: -150, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0.4);
      // „Auf die Knie!“: Bild bebt
      tl.to(["#s01-title", bg], { x: 10, duration: 0.04, repeat: 7, yoyo: true }, at("L1", "knie"));
      const se = at("L1", "sekte");
      tl.fromTo("#s01-flash", { opacity: 0.7 }, { opacity: 0, duration: 0.4, ease: "power2.out", immediateRender: false }, se);
      tl.to("#s01-title", { x: 12, duration: 0.04, repeat: 5, yoyo: true }, se);''' + OUT)

# ---------- s02 Prophet Peter erscheint ----------
S['s02'] = ('''    #s02-beam { left: 290px; top: 0; width: 500px; height: 1200px; opacity: 0;
      background: linear-gradient(180deg, rgba(255,240,200,.75), rgba(255,240,200,.05)); clip-path: polygon(38% 0, 62% 0, 100% 100%, 0 100%); filter: blur(6px); }
    #s02-plate { left: 120px; width: 780px; top: 960px; height: 170px; border-radius: 22px; background: rgba(13,10,30,.92); border: 4px solid #ffd43b;
      box-shadow: 0 0 40px rgba(255,212,59,.45); opacity: 0; }
    #s02-plate .n { margin-top: 18px; font-size: 76px; line-height: 1; color: #ffd43b; text-shadow: 0 0 26px rgba(255,212,59,.6); letter-spacing: -.01em; }
    #s02-plate .r { margin-top: 12px; font-family: "Space Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .14em; color: #fff; }
    #s02-plate .r span { opacity: 0; }''',
BG + '''
      <div id="s02-beam" class="abs"></div>
''' + SVG + '''
      <div id="s02-plate" class="plate"><div class="n">PROPHET PETER</div><div class="r"><span id="s02-r1">GRÜNDER</span> <span id="s02-r2">· ERLEUCHTET ·</span> <span id="s02-r3">ANFÜHRER</span></div></div>
''' + FX,
'''      const G = grundstueck(bg, "s02g", { mood: "dusk" }); gsap.set(G.rays, { opacity: 0.35 }); gsap.set(bg, { filter: "blur(5px) brightness(.7)" });
      const P = peter(sv, "s02p", 540, 1090, 0.7);
      floatDust(tl, G, C.__dur);
      const l3 = line("L3"), l4 = line("L4"), pr = at("L3", "prophet"), gr = at("L4", "gründer"), er = at("L4", "erleuchteter"), an = at("L4", "anführer");
      tl.fromTo("#s02-beam", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
      tl.fromTo(P.g, { opacity: 0, y: 1150, filter: "brightness(3) blur(10px)" }, { opacity: 1, y: 1090, filter: "brightness(1) blur(0px)", duration: 0.7, ease: "expo.out" }, 0.05);
      tl.fromTo(P.halo, { scale: 0.2, opacity: 0, svgOrigin: "0 -790" }, { scale: 1, opacity: 1, duration: 0.6, ease: "back.out(2)" }, pr - 0.1);
      tl.fromTo("#s02-plate", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, pr);
      tl.fromTo(P.glint, { x: -30, opacity: 0 }, { x: 20, opacity: 1, duration: 0.35, yoyo: true, repeat: 1 }, pr + 0.4);
      talk(tl, P, l3[0], l3[1]); talk(tl, P, l4[0], l4[1]);
      [["#s02-r1", gr], ["#s02-r2", er], ["#s02-r3", an]].forEach(([s, t]) => tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.15 }, t - 0.05));
      tl.to(P.armL, { rotation: -150, duration: 0.45, ease: "back.out(1.8)" }, an - 0.2);
      tl.fromTo(P.spark, { scale: 0.4, svgOrigin: "-187 -850" }, { scale: 1.6, duration: 0.25, yoyo: true, repeat: 3 }, an);
      tl.to("#s02-r3", { color: "#ff4fb0", textShadow: "0 0 20px rgba(255,79,176,.8)", duration: 0.2 }, an);''' + OUT)

# ---------- s04 Das Erbe: Testament, dann verschlossenes Tor mit Schild ----------
S['s04'] = ('''    #s04-doc { left: 150px; top: 410px; width: 720px; height: 660px; border-radius: 10px; padding: 46px 54px;
      background: linear-gradient(160deg, #f6ecd2 0%, #e9d9b0 60%, #d8c08a 100%); box-shadow: 0 30px 60px rgba(0,0,0,.6); color: #3a2a18; text-align: left; }
    #s04-doc .t { font-family: "Inter", sans-serif; font-weight: 900; font-size: 64px; letter-spacing: .12em; text-align: center; color: #5a1a1a; }
    #s04-doc .p { margin-top: 30px; font-family: Georgia, serif; font-style: italic; font-size: 40px; line-height: 1.35; }
    #s04-doc .p b { font-style: normal; color: #8a1a1a; }
    #s04-doc .sig { position: absolute; left: 60px; bottom: 50px; font-family: Georgia, serif; font-style: italic; font-size: 42px; color: #22305a; }
    #s04-seal { position: absolute; right: 60px; bottom: 36px; width: 130px; height: 130px; border-radius: 50%; background: radial-gradient(circle at 40% 35%, #e0454f, #8a1020);
      box-shadow: 0 6px 0 rgba(0,0,0,.3); color: #ffd2d2; font-family: "Inter", sans-serif; font-weight: 900; font-size: 50px; line-height: 130px; text-align: center; }
    #s04-stamp { left: 210px; top: 640px; width: 600px; height: 150px; border: 10px solid #39e27a; border-radius: 20px; color: #39e27a; font-family: "Inter", sans-serif; font-weight: 900;
      font-size: 110px; line-height: 130px; text-align: center; opacity: 0; transform: rotate(-12deg); text-shadow: 0 0 30px rgba(57,226,122,.6); box-shadow: 0 0 30px rgba(57,226,122,.5), inset 0 0 30px rgba(57,226,122,.4); background: rgba(5,20,10,.55); }
    #s04-sign { left: 330px; top: 420px; width: 480px; height: 170px; border-radius: 12px; background: linear-gradient(180deg, #8a5a2b, #5e3b1a);
      border: 6px solid #3b2410; color: #ffd43b; font-family: "Inter", sans-serif; font-weight: 900; font-size: 46px; line-height: 1.05; text-align: center; padding-top: 24px; opacity: 0;
      box-shadow: 0 20px 40px rgba(0,0,0,.5); }
    #s04-sign small { display: block; font-size: 30px; color: #f3e2c0; letter-spacing: .1em; }''',
BG + '''
      <svg id="s04-holy" class="full noshift" viewBox="0 0 1080 1920"></svg>
''' + SVG + '''
      <div id="s04-doc" class="abs"><div class="t">TESTAMENT</div><div class="p">„… vermache ich meinem Neffen <b>Peter</b> mein gesamtes <b>Grundstück</b>.<br>Mach was draus, Junge.“</div>
        <div class="sig">Onkel Heinz</div><div id="s04-seal">H</div></div>
      <div id="s04-stamp" class="abs" data-layout-ignore>GEERBT</div>
      <div id="s04-sign" class="abs"><small>ZUKÜNFTIGES</small>HEILIGTUM</div>
''' + FX,
'''      const G = grundstueck(bg, "s04g", { mood: "dusk", goatX: 880, goatS: 0.6 }); gsap.set(bg, { filter: "blur(8px) brightness(.55)" });
      // Heiligenschein um Baum + Stuhl: goldener Ring, Glühen, Lichtkegel von oben (Bild-Koordinaten, nicht verschoben)
      const H = document.querySelector("#s04-holy"), HD = GR(H), holy = el("g", { opacity: 0 }, H);
      el("ellipse", { cx: 570, cy: 930, rx: 380, ry: 400, fill: rad(HD, "s04hg", [[0, "#ffe9a8", 0.55], [0.55, "#ffcf6a", 0.22], [1, "#ffcf6a", 0]]) }, holy);
      el("path", { d: "M470 0 L670 0 L860 1240 L280 1240Z", fill: lin(HD, "s04beam", [[0, "#fff4cf", 0.55], [1, "#fff4cf", 0]]) }, holy);
      const ring = el("ellipse", { cx: 570, cy: 860, rx: 330, ry: 330, fill: "none", stroke: "#ffe08a", "stroke-width": 16 }, holy);
      ring.style.filter = "drop-shadow(0 0 22px rgba(255,210,90,1)) drop-shadow(0 0 50px rgba(255,180,60,.8))";
      const sp = Array.from({ length: 18 }, (_, i) => el("circle", { cx: 570 + 330 * Math.cos(i / 18 * 6.283), cy: 860 + 330 * Math.sin(i / 18 * 6.283), r: 7, fill: "#fffbe6" }, holy));
      const P = peter(sv, "s04p", 165, 1120, 0.55, { halo: false });
      const ve = at("L7", "vererbt"), l8 = line("L8"), he = at("L8", "heiligtum");
      tl.fromTo("#s04-doc", { y: -700, rotation: -18 }, { y: 0, rotation: -3, duration: 0.4, ease: "back.out(1.4)" }, 0);
      tl.fromTo("#s04-stamp", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, ve - 0.15);
      tl.to("#s04-doc", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, ve + 0.06);
      tl.to(["#s04-doc", "#s04-stamp"], { y: 1300, rotation: 10, opacity: 0, duration: 0.35, ease: "power3.in" }, l8[0] - 0.3);
      tl.to(bg, { filter: "blur(0px) brightness(.85)", duration: 0.4 }, l8[0] - 0.2);
      tl.fromTo(holy, { opacity: 0 }, { opacity: 1, duration: 0.4 }, l8[0] - 0.1);
      tl.fromTo(ring, { scale: 0.6, svgOrigin: "570 860" }, { scale: 1, duration: 0.5, ease: "back.out(1.8)" }, l8[0] - 0.1);
      tl.fromTo(sp, { opacity: 0 }, { opacity: 1, duration: 0.15, stagger: 0.02 }, l8[0] + 0.2);
      tl.fromTo(P.g, { opacity: 0, x: 40 }, { opacity: 1, x: 165, duration: 0.4, ease: "expo.out" }, l8[0]);
      tl.to(P.armL, { rotation: -100, duration: 0.35, ease: "back.out(1.6)" }, l8[0] + 0.1);
      talk(tl, P, l8[0], l8[1]);
      tl.fromTo("#s04-sign", { opacity: 0, y: -400, rotation: -20 }, { opacity: 1, y: 0, rotation: -4, duration: 0.4, ease: "bounce.out" }, he - 0.3);''' + OUT)

# ---------- s05 Das Grundstück: Totale über alle 2 Hektar, dann Zoom auf Schrott, Ziege, Stuhl, Baum (Ast bricht) ----------
S['s05'] = ('''    #s05-box { left: 240px; width: 600px; }
    #s05-box2 { left: 240px; width: 600px; top: 410px; }
    .s05-l { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 600px; font-size: 48px; border-color: #ff4fb0; box-shadow: 0 0 34px rgba(255,79,176,.5); }''',
BG + '\n' + SVG + '''
      <div id="s05-box" class="cbox y" style="opacity:0"><div class="lab">FLÄCHE</div><div class="num" id="s05-n">0 m²</div></div>
      <div id="s05-box2" class="cbox r" style="opacity:0"><div class="lab">AUSSTATTUNG</div><div class="num">1 STUHL</div></div>
      <div id="s05-junk" class="lbl s05-l"><small>INKLUSIVE</small>SCHROTT &amp; RUINEN</div>
      <div id="s05-goat" class="lbl s05-l"><small>BEWOHNERIN</small>DIE ZIEGE</div>
''' + FX,
'''      const G = grundstueck(bg, "s05g", { mood: "day", w: 3240, chairX: 470, treeX: 600, goatX: 1150, goatS: 1.0, seed: 11 });
      floatDust(tl, G, C.__dur);
      const tw = el("g", {}, sv); for (let i = 0; i < 14; i++) el("circle", { cx: (i % 4) * 9 - 14, cy: Math.floor(i / 4) * 9 - 14, r: 34 - (i % 5) * 3, fill: "none", stroke: "#8a7040", "stroke-width": 3, opacity: 0.8 }, tw);
      gsap.set(tw, { x: -120, y: 1030 });
      const ha = at("L9", "hektar"), wi = at("L9", "wildnis"), zi = at("L9b", "ziege"), wo = at("L9b", "wohnt"), st = at("L9b", "stuhl"), es = at("L9b", "und"), l10 = line("L10")[0], ba = at("L10", "baum");
      // Kamera: Welt-Punkt (wx, wy) mit Zoom s an Bild-Punkt (sx, sy)
      const cam = (s, wx, wy, sx, sy) => ({ s, x: sx - s * wx, y: sy - s * wy });
      const CAM = cam(0.333, 1620, 1080, 540, 980);                        // Totale: die ganzen 2 Hektar
      const apply = () => G.land.setAttribute("transform", `translate(${CAM.x} ${CAM.y}) scale(${CAM.s})`);
      apply();
      const move = (c, t, d = 0.6, ease = "power3.inOut") => tl.to(CAM, { ...c, duration: d, ease, onUpdate: apply }, t);
      move(cam(0.36, 1620, 1080, 540, 980), 0, Math.max(0.4, wi - 0.4), "none");
      move(cam(0.85, 2050, 1080, 540, 1000), wi - 0.3);                        // Schrott: Schuppen, Schild, Badewanne
      move(cam(1.15, 1180, 1120, 540, 1040), zi - 0.35);                       // die Ziege
      move(cam(1.35, 530, 1150, 560, 1060), es - 0.2, 0.7);                    // der einzige Stuhl
      move(cam(1.0, 600, 1000, 560, 920), l10 - 0.15, 0.5);                    // der karge Baum
      tl.fromTo("#s05-box", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, ha - 0.1);
      count(tl, "#s05-n", 0, 20000, ha - 0.05, 0.7, "", " m²");
      tl.fromTo("#s05-junk", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, wi + 0.15);
      tl.to("#s05-junk", { opacity: 0, duration: 0.15 }, zi - 0.3);
      tl.fromTo("#s05-goat", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, zi);
      tl.to(G.goat.head, { rotation: -8, duration: 0.25, ease: "back.out(2)" }, wo - 0.05);
      tl.to(G.goat.head, { rotation: -14, duration: 0.07, yoyo: true, repeat: 7 }, wo + 0.2);
      tl.to(G.goat.head, { rotation: 36, duration: 0.3 }, wo + 0.9);
      tl.to("#s05-goat", { opacity: 0, duration: 0.2 }, es - 0.2);
      tl.fromTo("#s05-box2", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, st - 0.05);
      tl.to("#s05-box2", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, st + 0.25);
      tl.to(tw, { x: 1200, rotation: 720, duration: 2.2, ease: "none" }, l10 - 0.1);
      // Ast bricht demonstrativ ab: knackt, knickt, fällt zu Boden, prallt ab
      const [bx, by] = G.brkBase, crk = ba + 0.12;
      tl.to(G.brk, { rotation: 8, svgOrigin: `${bx} ${by}`, duration: 0.04, yoyo: true, repeat: 1 }, crk - 0.1);
      tl.to(G.brk, { rotation: 30, svgOrigin: `${bx} ${by}`, duration: 0.12, ease: "power2.in" }, crk);
      tl.to(G.brk, { y: 1235 - by + 40, x: 40, rotation: 96, svgOrigin: `${bx} ${by}`, duration: 0.38, ease: "power2.in" }, crk + 0.12);
      tl.to(G.brk, { y: 1235 - by + 20, rotation: 92, svgOrigin: `${bx} ${by}`, duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out" }, crk + 0.5);
      tl.to(G.tree, { rotation: -1.5, svgOrigin: "600 1210", duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }, crk);''' + OUT)

# ---------- s06 Die Vision: goldene Linien zeichnen Tempel, Gärten, Pilgerstraße; dann Weltreligion ----------
S['s06'] = ('''    #s06-box { left: 190px; width: 700px; opacity: 0; }
    #s06-box .num { font-size: 52px; }
    #s06-world { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 980px; font-size: 76px; border-color: #ff4fb0; box-shadow: 0 0 40px rgba(255,79,176,.6); }
    #s06-zero { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 600px; padding: 10px 36px; border: 10px solid #ff3b55; border-radius: 22px; background: rgba(40,4,14,.9);
      color: #ff3b55; font-family: "Inter", sans-serif; font-weight: 900; font-size: 104px; line-height: 1.05; text-align: center; white-space: nowrap; opacity: 0;
      text-shadow: 0 0 30px rgba(255,59,85,.7); box-shadow: 0 0 60px rgba(255,59,85,.6); transform: rotate(-6deg); }
    #s06-zero small { display: block; font-family: "Space Mono", monospace; font-weight: 700; font-size: 32px; letter-spacing: .16em; color: #ffb3bf; }''',
BG + '\n' + SVG + '''
      <div id="s06-box" class="cbox p"><div class="lab">ANHÄNGER</div><div class="num" id="s06-n">1</div></div>
      <div id="s06-world" class="lbl"><small>ZIEL</small>WELTRELIGION</div>
      <div id="s06-zero" class="abs"><small>AKTUELLER STAND</small>0 ANHÄNGER</div>
''' + FX,
'''      const G = grundstueck(bg, "s06g", { mood: "dusk", goatX: 880, goatS: 0.5 }); gsap.set(G.rays, { opacity: 0.4 });
      floatDust(tl, G, C.__dur);
      const D = GR(sv), gold = "#ffd43b";
      const vis = el("g", {}, sv); vis.style.filter = "drop-shadow(0 0 14px rgba(255,212,59,.9))";
      const draw = (d, w = 6, c = gold) => { const p = el("path", { d, stroke: c, "stroke-width": w, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, vis); return p; };
      // Tempel mit Kuppel und Säulen
      const temple = [draw("M300 900 L780 900 L780 920 L300 920Z"), draw("M330 880 L750 880"), draw("M340 880 L340 720 M410 880 L410 720 M480 880 L480 720 M600 880 L600 720 M670 880 L670 720 M740 880 L740 720"),
        draw("M320 720 L760 720 L540 640Z"), draw("M430 650 Q540 470 650 650"), draw("M540 520 L540 470 M520 490 L560 490")];
      const eye = draw("M505 690 q35 -22 70 0 q-35 22 -70 0Z", 5, "#ff4fb0");
      // Gärten
      const gardens = []; [[150, 980], [230, 1020], [860, 990], [930, 1030], [110, 1050]].forEach(([x, y]) => { gardens.push(draw(`M${x} ${y} l0 -40`, 6, "#39e27a")); gardens.push(draw(`M${x - 30} ${y - 40} a30 30 0 1 1 60 0 a30 30 0 1 1 -60 0`, 6, "#39e27a")); });
      // Pilgerstraße in Perspektive mit kleinen Pilgern
      const road = [draw("M470 925 L250 1120", 6), draw("M610 925 L830 1120", 6), draw("M540 935 L540 960 M540 990 L540 1025 M540 1060 L540 1110", 6)];
      const pil = []; for (let i = 0; i < 6; i++) { const p = el("g", { opacity: 0 }, vis); el("circle", { cx: 0, cy: -16, r: 8, fill: "#fff1c4" }, p); el("rect", { x: -9, y: -8, width: 18, height: 24, rx: 7, fill: "#fff1c4" }, p); pil.push(p); }
      const all = [...temple, eye, ...gardens, ...road];
      all.forEach((p) => { const L = p.getTotalLength(); gsap.set(p, { strokeDasharray: L, strokeDashoffset: L }); });
      const P = peter(sv, "s06p", 150, 1120, 0.42, { halo: true });
      const mehr = at("L11", "mehr"), te = at("L11", "tempel"), ga = at("L11", "gärten"), pi = at("L11", "pilgerstraße"), l12 = line("L12")[0], wr = at("L12", "weltreligion");
      talk(tl, P, line("L11")[0], line("L11")[1]);
      tl.fromTo(P.glint, { x: -30, opacity: 0 }, { x: 20, opacity: 1, duration: 0.3, yoyo: true, repeat: 1 }, mehr - 0.1);
      tl.to(G.rays, { opacity: 0.9, duration: 0.5 }, mehr);
      tl.to(temple, { strokeDashoffset: 0, duration: 0.7, stagger: 0.08, ease: "power2.inOut" }, te - 0.25);
      tl.to(eye, { strokeDashoffset: 0, duration: 0.4 }, te + 0.4);
      tl.to(gardens, { strokeDashoffset: 0, duration: 0.45, stagger: 0.04, ease: "power2.out" }, ga - 0.15);
      tl.to(road, { strokeDashoffset: 0, duration: 0.5, stagger: 0.06, ease: "power2.out" }, pi - 0.2);
      pil.forEach((p, i) => { const s = i % 2 ? 1 : -1, k = (i >> 1) / 3; tl.fromTo(p, { opacity: 0, x: 540 + s * 30, y: 950, scale: 0.6 }, { opacity: 1, x: 540 + s * (90 + 180 * k), y: 1000 + 100 * k, scale: 1 + k, duration: 0.8, ease: "power1.out" }, pi + i * 0.08); });
      // Weltreligion: alles wird zur Weltkugel, Pins überall
      tl.to([vis, P.g], { opacity: 0, scale: 0.5, svgOrigin: "540 800", duration: 0.4, ease: "power3.in" }, l12 - 0.2);
      const globe = el("g", { opacity: 0 }, sv), gl = rad(D, "s06glb", [[0, "#5fb0ff"], [0.6, "#2b6fd1"], [1, "#0d2a66"]], 0.38, 0.35, 0.7);
      el("circle", { cx: 540, cy: 720, r: 230, fill: gl }, globe); globe.style.filter = "drop-shadow(0 0 40px rgba(255,79,176,.6))";
      [[-0.4, -0.3, 0.35, 0.22], [0.3, -0.1, 0.28, 0.38], [-0.1, 0.45, 0.25, 0.14], [-0.55, 0.2, 0.15, 0.2]].forEach(([dx, dy, rx, ry]) => el("ellipse", { cx: 540 + dx * 230, cy: 720 + dy * 230, rx: rx * 230, ry: ry * 230, fill: "#3fa06a" }, globe));
      const R = rng(61), pins = Array.from({ length: 34 }, () => { const a = R() * 6.28, r = Math.sqrt(R()) * 210; const p = el("circle", { cx: 540 + r * Math.cos(a), cy: 720 + r * Math.sin(a), r: 8, fill: "#ff4fb0", opacity: 0 }, globe); return p; });
      tl.fromTo(globe, { opacity: 0, scale: 0.3, svgOrigin: "540 720" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, l12);
      tl.to(pins, { opacity: 1, duration: 0.05, stagger: 0.035 }, l12 + 0.3);
      tl.fromTo("#s06-box", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3 }, l12 + 0.1);
      // Zähler rast bis in die Millionen … und stürzt bei „null Anhänger“ auf 0 ab (ein Tween, damit Vor-/Zurückspulen stimmt)
      const zs = at("L12b", "null"), t0 = l12 + 0.3, t1 = zs + 0.25, pc = (zs - 0.05 - t0) / (t1 - t0), nEl = document.querySelector("#s06-n"), cnt = { p: 0 };
      nEl.textContent = "1";
      tl.to(cnt, { p: 1, duration: t1 - t0, ease: "none", onUpdate: () => { const p = cnt.p;
        const v = p <= pc ? 1 + 4870000 * Math.pow(p / pc, 3) : 4870000 * Math.pow(1 - (p - pc) / (1 - pc), 4); nEl.textContent = fmt(v); } }, t0);
      const l12b = line("L12b")[0];
      tl.to("#s06-box", { borderColor: "#ff3b55", boxShadow: "0 0 50px rgba(255,59,85,.8)", duration: 0.15 }, zs);
      tl.to("#s06-box", { x: 12, duration: 0.04, repeat: 7, yoyo: true }, zs + 0.2);
      tl.to(pins, { opacity: 0, duration: 0.05, stagger: { each: 0.01, from: "random" } }, l12b);
      tl.to(globe, { filter: "grayscale(1) brightness(.6)", duration: 0.4 }, l12b);
      tl.to("#s06-world", { opacity: 0.25, filter: "grayscale(1)", duration: 0.3 }, l12b);
      tl.fromTo("#s06-zero", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.in" }, zs - 0.05);
      tl.to("#s06-zero", { x: 10, duration: 0.04, repeat: 5, yoyo: true }, zs + 0.22);
      tl.fromTo("#s06-world", { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }, wr);''' + OUT)

# ---------- s07 Die Kollekte: 1 Follower = 1 Euro = 1 Ziegelstein ----------
S['s07'] = ('''    #s07-box { left: 290px; width: 500px; }
    #s07-law { left: 120px; width: 780px; top: 420px; height: 210px; border-radius: 18px; padding-top: 22px;
      background: linear-gradient(180deg, #f6ecd2, #dcc58f); color: #3a2a18; box-shadow: 0 20px 50px rgba(0,0,0,.55); opacity: 0; }
    #s07-law .k { font-family: "Space Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .16em; color: #8a1a1a; }
    #s07-law .x { margin-top: 12px; font-size: 52px; line-height: 1.05; color: #2a1a10; }
    #s07-law .x em { font-style: normal; color: #c2185b; }
    #s07-fol { left: 120px; top: 700px; width: 250px; height: 92px; border-radius: 46px; background: #ff4fb0; color: #fff; font-size: 46px; line-height: 92px;
      box-shadow: 0 0 40px rgba(255,79,176,.7); opacity: 0; }''',
BG + '\n' + SVG + '''
      <div id="s07-box" class="cbox y" style="opacity:0"><div class="lab">KOLLEKTE</div><div class="num" id="s07-n">0 €</div></div>
      <div id="s07-law" class="plate"><div class="k">HEILIGES GESETZ · § 1</div><div class="x"><em>1 FOLLOWER = 1 ANHÄNGER</em><br>+ 1 € IN DIE KOLLEKTE</div></div>
      <div id="s07-fol" class="plate">+ FOLGEN</div>
      <svg id="s07-top" class="full" viewBox="0 0 1080 1920"></svg>
''' + FX,
'''      const G = grundstueck(bg, "s07g", { mood: "dusk" }); gsap.set(bg, { filter: "blur(6px) brightness(.6)" });
      const D = GR(sv);
      // Klingelbeutel: Samtbeutel an langem Stab mit Glöckchen
      const bag = el("g", {}, sv), vel = rad(D, "s07vel", [[0, "#c2185b"], [0.7, "#7a0c3a"], [1, "#3a0418"]], 0.4, 0.3, 0.8);
      el("rect", { x: 0, y: 870, width: 520, height: 22, rx: 11, fill: lin(D, "s07st", [[0, "#a0703f"], [1, "#4f3116"]]) }, bag);
      el("path", { d: "M560 860 Q500 960 560 1060 Q680 1110 800 1060 Q860 960 800 860Z", fill: vel }, bag);
      el("ellipse", { cx: 680, cy: 860, rx: 122, ry: 30, fill: "#2a0210" }, bag);
      el("path", { d: "M558 860 A122 30 0 0 0 802 860", stroke: lin(D, "s07gd", [[0, "#fff2b0"], [1, "#d99a1e"]], 0, 0, 1, 0), "stroke-width": 14, fill: "none" }, bag);
      el("circle", { cx: 680, cy: 1076, r: 16, fill: "#ffd43b" }, bag);
      const top = document.querySelector("#s07-top"), coin = el("g", { opacity: 0 }, top); gsap.set(coin, { transformOrigin: "50% 50%" }); coin.style.filter = "drop-shadow(0 0 16px rgba(255,212,59,.9))";
      el("circle", { cx: 0, cy: 0, r: 46, fill: "#ffd43b" }, coin); el("circle", { cx: 0, cy: 0, r: 36, fill: "none", stroke: "#c48416", "stroke-width": 5 }, coin);
      const ct = el("text", { x: 0, y: 17, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 48, fill: "#9a6510" }, coin); ct.textContent = "€";
      const ge = at("L13", "heiliges"), fo = at("L13", "follower"), eu = at("L13", "euro");
      tl.fromTo(bag, { opacity: 0, x: -400 }, { opacity: 1, x: 0, duration: 0.6, ease: "expo.out" }, 0);
      tl.fromTo("#s07-law", { opacity: 0, y: -60, rotationX: 80 }, { opacity: 1, y: 0, rotationX: 0, duration: 0.45, ease: "back.out(1.6)" }, ge - 0.1);
      tl.fromTo("#s07-fol", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, fo - 0.05);
      tl.to("#s07-fol", { scale: 0.9, duration: 0.1, yoyo: true, repeat: 1 }, fo + 0.35);
      tl.fromTo("#s07-box", { opacity: 0 }, { opacity: 1, duration: 0.25 }, fo);
      // Münze fällt sichtbar von oben senkrecht in den Klingelbeutel und dreht sich dabei
      tl.fromTo(coin, { opacity: 1, x: 680, y: 150, scale: 1.5 }, { y: 850, scale: 1.1, duration: 0.8, ease: "power2.in", immediateRender: false }, eu - 0.7);
      tl.fromTo(coin, { scaleX: 1.4 }, { scaleX: -1.4, duration: 0.16, repeat: 4, yoyo: true, ease: "sine.inOut", immediateRender: false }, eu - 0.7);
      tl.to(coin, { opacity: 0, duration: 0.06 }, eu + 0.1);
      const burst = Array.from({ length: 10 }, () => el("circle", { cx: 680, cy: 860, r: 7, fill: "#ffd43b", opacity: 0 }, top));
      burst.forEach((b, i) => { const a = -Math.PI * (0.1 + 0.8 * i / 9); tl.fromTo(b, { opacity: 1, x: 0, y: 0 }, { opacity: 0, x: Math.cos(a) * 110, y: Math.sin(a) * 110, duration: 0.45, ease: "power2.out", immediateRender: false }, eu + 0.1); });
      tl.to(bag, { y: 14, duration: 0.08, yoyo: true, repeat: 3 }, eu + 0.1);
      count(tl, "#s07-n", 0, 1, eu + 0.1, 0.2, "", " €", "none");
      tl.fromTo("#s07-box", { scale: 1.25 }, { scale: 1, duration: 0.35, ease: "back.out(3)", immediateRender: false }, eu + 0.1);''' + OUT)

# ---------- s08 Die Ränge: Pyramide, Platz 1 frei, unten Rasenmähen ----------
S['s08'] = ('''    .s08-r { position: absolute; left: 0; right: 0; margin: 0 auto; height: 112px; border-radius: 16px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900;
      color: #fff; font-size: 50px; line-height: 112px; opacity: 0; box-shadow: 0 10px 30px rgba(0,0,0,.45); white-space: nowrap; }
    .s08-r small { font-family: "Space Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .1em; margin-left: 14px; opacity: .85; }
    #s08-r1 { top: 420px; width: 600px; background: linear-gradient(180deg, #ffe27a, #d99a1e); color: #2a1a00; box-shadow: 0 0 60px rgba(255,212,59,.7); }
    #s08-r2 { top: 552px; width: 660px; background: linear-gradient(180deg, #e6e9f5, #9aa1c4); color: #161a36; }
    #s08-r3 { top: 684px; width: 740px; background: linear-gradient(180deg, #e0985a, #a0582a); }
    #s08-r4 { top: 816px; width: 800px; background: linear-gradient(180deg, #4a3a8a, #2e2462); }
    #s08-arr { left: 40px; top: 430px; width: 60px; height: 520px; opacity: 0; }''',
BG + '''
      <div id="s08-r1" class="s08-r">HOHEPRIESTER</div>
      <div id="s08-r2" class="s08-r">ERZDIAKON</div>
      <div id="s08-r3" class="s08-r">TEMPELWÄCHTER</div>
      <div id="s08-r4" class="s08-r">ANHÄNGER</div>
      <svg id="s08-arr" class="abs" viewBox="0 0 60 520"><path d="M30 510 L30 30" stroke="#39e27a" stroke-width="12" stroke-linecap="round"/><path d="M6 50 L30 10 L54 50" stroke="#39e27a" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
''' + SVG + '\n' + FX,
'''      const G = grundstueck(bg, "s08g", { mood: "dusk" }); gsap.set(bg, { filter: "blur(7px) brightness(.5)" });
      const ho = at("L15", "hohen"), er = at("L15", "rang");
      tl.fromTo([".s08-r#s08-r4", "#s08-r3", "#s08-r2", "#s08-r1"], { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, stagger: 0.12, ease: "back.out(2)" }, 0.05);
      tl.fromTo("#s08-arr", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, ho - 0.3);
      tl.fromTo("#s08-r1", { scale: 1 }, { scale: 1.12, duration: 0.2, yoyo: true, repeat: 1 }, er);
      tl.to("#s08-r1", { boxShadow: "0 0 90px rgba(255,212,59,1)", duration: 0.25, yoyo: true, repeat: 3 }, er);''' + OUT)

# ---------- s09 Der Name: Wie soll die Sekte heißen? ----------
S['s09'] = ('''    #s09-q { background: rgba(13,10,30,.9); left: 90px; width: 820px; top: 400px; height: 300px; border: 6px solid #ff4fb0; box-shadow: 0 0 60px rgba(255,79,176,.55); opacity: 0; }
    #s09-q .k { margin-top: 22px; font-family: "Space Mono", monospace; font-weight: 700; font-size: 32px; letter-spacing: .16em; color: #f4d27a; }
    #s09-q .n { margin-top: 12px; font-size: 80px; line-height: 1.08; color: #fff; }
    #s09-q .n span { color: #ff4fb0; }
    #s09-cur { display: inline-block; width: 8px; height: 76px; background: #ff4fb0; vertical-align: -6px; margin-left: 6px; }''',
BG + '\n' + SVG + '''
      <div id="s09-q" class="plate"><div class="k">TAG 1 · ABSTIMMUNG</div><div class="n">„SEKTE DER<br><span id="s09-name">________</span><span id="s09-cur"></span>“</div></div>
''' + FX,
'''      const G = grundstueck(bg, "s09g", { mood: "dusk", chairX: 690, treeX: 800, goatX: 560, goatS: 0.6, goatFlip: true }); gsap.set(G.rays, { opacity: 0.6 });
      floatDust(tl, G, C.__dur); chew(tl, G, 0, C.__dur - 0.3);
      const P = peter(sv, "s09p", 300, 1120, 0.44);
      const na = at("L17", "name"), he = at("L17", "heißen");
      talk(tl, P, line("L17")[0], line("L17")[1]);
      tl.fromTo(P.g, { opacity: 0, x: 180 }, { opacity: 1, x: 300, duration: 0.5, ease: "expo.out" }, 0);
      tl.fromTo("#s09-q", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, na - 0.2);
      tl.fromTo("#s09-cur", { opacity: 1 }, { opacity: 0, duration: 0.25, repeat: 9, yoyo: true, ease: "steps(1)" }, na);
      tl.fromTo("#s09-name", { color: "#ff4fb0" }, { color: "#ffd43b", duration: 0.12, repeat: 5, yoyo: true }, he);
      tl.to(P.armL, { rotation: -60, duration: 0.4, ease: "back.out(1.8)" }, he - 0.2);''' + OUT)

# ---------- s10 Aufruf: Kommentar mit „Prophet Peter“, Frage: Was kaufen wir morgen? (letzte Szene, kein Blur-Out) ----------
S['s10'] = ('''    #s10-cm { left: 90px; width: 820px; top: 400px; height: 190px; border-radius: 26px; background: rgba(250,248,242,.97); box-shadow: 0 20px 50px rgba(0,0,0,.5); opacity: 0; text-align: left; }
    #s10-cm .av { position: absolute; left: 28px; top: 30px; width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(135deg, #ff4fb0, #ffd43b); }
    #s10-cm .u { position: absolute; left: 134px; top: 26px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 30px; color: #7a7f99; }
    #s10-cm .t { position: absolute; left: 134px; top: 70px; right: 110px; font-family: "Inter", sans-serif; font-weight: 900; font-size: 42px; line-height: 1.12; color: #161a36; }
    #s10-cm .t b { color: #c2185b; }
    #s10-cm .h { position: absolute; right: 26px; top: 46px; width: 70px; text-align: center; font-family: "Inter", sans-serif; font-weight: 900; font-size: 30px; color: #ff3b55; }
    #s10-cm .h i { display: block; font-style: normal; font-size: 46px; line-height: 1; }
    #s10-q { left: 90px; width: 820px; top: 630px; height: 250px; border: 6px solid #ffd43b; box-shadow: 0 0 60px rgba(255,212,59,.45); background: rgba(13,10,30,.92); opacity: 0; }
    #s10-q .k { margin-top: 22px; font-family: "Space Mono", monospace; font-weight: 700; font-size: 32px; letter-spacing: .14em; color: #f4d27a; }
    #s10-q .n { margin-top: 10px; font-size: 70px; line-height: 1.05; color: #fff; }
    #s10-q .n em { font-style: normal; color: #ffd43b; }
    #s10-st { left: 0; right: 0; margin: 0 auto; width: fit-content; top: 596px; padding: 8px 18px; border-radius: 12px; background: #39e27a; color: #0b0e22; font-family: "Inter", sans-serif; font-weight: 900; font-size: 32px; transform: rotate(-3deg); opacity: 0; white-space: nowrap; }
    #s10-f { left: 90px; top: 920px; width: 820px; height: 110px; border-radius: 55px; background: #ff4fb0; color: #fff; font-size: 46px; line-height: 110px; opacity: 0;
      box-shadow: 0 0 50px rgba(255,79,176,.65); }''',
BG + '\n' + SVG + '''
      <div id="s10-cm" class="abs"><div class="av"></div><div class="u">@dein_name · gerade eben</div><div class="t"><b id="s10-pp">Prophet Peter</b>, kauf uns eine Hüpfburg!</div><div class="h"><i>♥</i><span id="s10-likes">0</span></div></div>
      <div id="s10-q" class="plate"><div class="k">VON DER 1. KOLLEKTE</div><div class="n">WAS KAUFEN WIR<br><em>MORGEN?</em></div></div>
      <div id="s10-st" class="abs">TOP-KOMMENTAR ENTSCHEIDET</div>
      <div id="s10-f" class="plate">+ FOLGEN = 1 € IN DIE KOLLEKTE</div>
''' + FX,
'''      const G = grundstueck(bg, "s10g", { mood: "dusk", chairX: 690, treeX: 800, goatX: 470, goatS: 0.6 }); gsap.set(G.rays, { opacity: 0.6 }); gsap.set(bg, { filter: "blur(3px) brightness(.8)" });
      floatDust(tl, G, C.__dur); chew(tl, G, 0, 3);
      const ko = at("L18", "kommentare"), pp = at("L18", "prophet"), l19 = line("L19")[0], mo = at("L19", "morgen"), ko2 = at("L19", "kollekte"), tk = at("L19", "topkommentar"), en = at("L19", "entscheidet");
      tl.fromTo("#s10-cm", { opacity: 0, y: 60, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)" }, ko - 0.2);
      tl.fromTo("#s10-pp", { color: "#161a36" }, { color: "#c2185b", duration: 0.2 }, pp - 0.05);
      tl.fromTo("#s10-pp", { textShadow: "0 0 0px rgba(255,79,176,0)" }, { textShadow: "0 0 18px rgba(255,79,176,.8)", duration: 0.2, yoyo: true, repeat: 3 }, pp);
      count(tl, "#s10-likes", 0, 999, ko + 0.2, C.__dur - ko - 0.4, "", "", "power1.in");
      tl.fromTo("#s10-cm .h i", { scale: 1 }, { scale: 1.4, duration: 0.15, yoyo: true, repeat: 3 }, pp + 0.3);
      tl.fromTo("#s10-q", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, l19 - 0.1);
      tl.fromTo("#s10-q .n em", { scale: 1 }, { scale: 1.15, duration: 0.2, yoyo: true, repeat: 1 }, mo);
      tl.fromTo("#s10-f", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, ko2 - 0.1);
      tl.fromTo("#s10-st", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.in" }, tk - 0.1);
      tl.to("#s10-f", { scale: 1.05, duration: 0.3, yoyo: true, repeat: 7, ease: "sine.inOut" }, en + 0.3);''')

def wrap_fg(html):
    # Hintergrund, Filmlook und .noshift-Ebenen bleiben stehen; alles andere kommt in einen um 110 px abgesenkten Container
    lines = html.split("\n")
    bg = [l for l in lines if 'id="@@ID@@-bg"' in l or "noshift" in l]
    fx = [l for l in lines if 'id="@@ID@@-fx"' in l]
    fg = [l for l in lines if l not in bg and l not in fx and l.strip()]
    return "\n".join(bg + ['      <div id="@@ID@@-fg" class="full fgwrap">'] + fg + ["      </div>"] + fx)


for sid, (css, html, js) in S.items():
    (here / f"{sid}.html").write_text(HEAD.replace("@@SERIES@@", SERIES_JS).replace("@@CSS@@", css).replace("@@HTML@@", wrap_fg(html)).replace("@@JS@@", js).replace("@@ID@@", sid))
print(sorted(S))
