      // ===== Das geerbte Grundstück (Serien-Kulisse): riesig, verwahrlost, ein Stuhl unter einem kargen Baum, eine Ziege =====
      // Braucht: el(), lin(), rad(), GR(), gsap, rng(). Zeichnet in eine 1080×1920-SVG.
      // o.mood: "dusk" (Abendrot, Standard) | "night" | "day"; o.w: Breite der Welt (Standard 1080, für Kamerafahrten z. B. 3240);
      // o.chairX/o.treeX: Stuhl/Baum (Welt-x); o.goatX: Ziege (null = keine); o.dy: Höhenversatz (Standard -20, passend zum um 110 px abgesenkten Vordergrund)
      // Rückgabe: land (Vordergrund, für Schwenks x tweenen), far (Sonne/Strahlen, Parallaxe), tree, chair, leaf, goat, …
      function goatFig(parent, x, y, s = 1, flip = false) {
        const g = el("g", {}, parent); gsap.set(g, { x, y, scale: s, scaleX: flip ? -s : s, transformOrigin: "0 0" });
        el("ellipse", { cx: 0, cy: 4, rx: 90, ry: 14, fill: "#000", opacity: 0.3 }, g);
        [-46, -24, 30, 52].forEach((lx) => { el("rect", { x: lx - 7, y: -40, width: 14, height: 44, rx: 6, fill: "#d9d4c4" }, g); el("rect", { x: lx - 7, y: -4, width: 14, height: 8, rx: 3, fill: "#3a2a20" }, g); });
        el("ellipse", { cx: 0, cy: -62, rx: 74, ry: 36, fill: "#ebe6d6" }, g);
        el("ellipse", { cx: -8, cy: -50, rx: 60, ry: 18, fill: "#cfc8b4", opacity: 0.7 }, g);
        el("path", { d: "M-70 -76 q-16 -6 -22 6", stroke: "#ebe6d6", "stroke-width": 8, fill: "none", "stroke-linecap": "round" }, g);
        const head = el("g", {}, g);
        el("path", { d: "M56 -82 Q74 -70 82 -40", stroke: "#ebe6d6", "stroke-width": 26, fill: "none", "stroke-linecap": "round" }, head);
        el("ellipse", { cx: 88, cy: -26, rx: 20, ry: 30, fill: "#ebe6d6", transform: "rotate(-25 88 -26)" }, head);
        el("path", { d: "M80 -52 q-4 -26 -22 -32 M90 -52 q4 -28 -10 -40", stroke: "#8a7a5a", "stroke-width": 7, fill: "none", "stroke-linecap": "round" }, head);
        el("ellipse", { cx: 66, cy: -42, rx: 14, ry: 6, fill: "#d9d4c4", transform: "rotate(30 66 -42)" }, head);
        el("circle", { cx: 92, cy: -34, r: 3.5, fill: "#2a1a10" }, head);
        el("path", { d: "M100 -4 l4 18 l6 -16", fill: "#bdb6a0" }, head);
        gsap.set(head, { rotation: 0, svgOrigin: "60 -80" });
        return { g, head };
      }
      function grundstueck(sv, pre, o = {}) {
        const D = GR(sv), R = rng(o.seed || 7), mood = o.mood || "dusk", W = o.w || 1080, DY = o.dy ?? -20;
        const skyC = { dusk: [[0, "#1a1240"], [0.45, "#5b2a6e"], [0.75, "#d0604a"], [1, "#ffb15c"]],
          night: [[0, "#05060f"], [0.6, "#121634"], [1, "#2a2350"]], day: [[0, "#6d9cc8"], [0.7, "#c9d6d8"], [1, "#efe2c2"]] }[mood];
        const sky = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: lin(D, pre + "sky", skyC) }, sv);
        const far = el("g", {}, sv); gsap.set(far, { y: DY });
        const sunG = el("g", {}, far);
        el("circle", { cx: 760, cy: 960, r: 520, fill: rad(D, pre + "sunh", [[0, "#ffd08a", 0.75], [0.4, "#ff9a5a", 0.25], [1, "#ff9a5a", 0]]) }, sunG);
        el("circle", { cx: 760, cy: 960, r: 90, fill: "#ffe2a8", opacity: mood === "night" ? 0 : 0.95 }, sunG);
        if (mood === "night") gsap.set(sunG, { opacity: 0.25 });
        const rays = el("g", { opacity: 0.0 }, far);
        for (let i = 0; i < 9; i++) { const a = -150 + i * 15 + R() * 6; const r1 = 1700;
          el("path", { d: `M760 960 L${760 + r1 * Math.cos((a - 2.5) * Math.PI / 180)} ${960 + r1 * Math.sin((a - 2.5) * Math.PI / 180)} L${760 + r1 * Math.cos((a + 2.5) * Math.PI / 180)} ${960 + r1 * Math.sin((a + 2.5) * Math.PI / 180)}Z`,
            fill: lin(D, pre + "ray" + i, [[0, "#fff1c4", 0.5], [1, "#fff1c4", 0]], 0, 0, 1, 0) }, rays); }
        const land = el("g", {}, sv); gsap.set(land, { y: DY });
        // Hügel: gespiegelte Kacheln, damit die Kanten nahtlos sind
        for (let k = 0; k * 1080 < W; k++) {
          const t = el("g", { transform: k % 2 ? `translate(${(k + 1) * 1080} 0) scale(-1 1)` : `translate(${k * 1080} 0)` }, land);
          el("path", { d: "M0 1010 Q160 900 330 960 Q520 1020 700 930 Q900 850 1080 960 L1080 1920 L0 1920Z", fill: mood === "day" ? "#8a9a8c" : "#4a2a55", opacity: 0.8 }, t);
          el("path", { d: "M0 1060 Q240 990 470 1050 Q760 1110 1080 1060 L1080 1920 L0 1920Z", fill: mood === "day" ? "#6d7a5a" : "#2f1d3a" }, t);
        }
        el("rect", { x: 0, y: 1080, width: W, height: 1000, fill: lin(D, pre + "gr", mood === "day" ? [[0, "#8b7a4a"], [1, "#4a3f22"]] : [[0, "#5a3f34"], [0.5, "#33231f"], [1, "#160f12"]]) }, land);
        // Erdflecken, Pfützen (spiegeln den Himmel), Steine
        for (let i = 0; i < W / 220; i++) { const px = R() * W, py = 1150 + R() * 400;
          el("ellipse", { cx: px, cy: py, rx: 60 + R() * 90, ry: 10 + R() * 14, fill: "#2a1a14", opacity: 0.5 }, land);
          if (i % 3 === 0) el("ellipse", { cx: px + 40, cy: py + 30, rx: 50 + R() * 40, ry: 9, fill: mood === "day" ? "#9fb8d0" : "#b0607a", opacity: 0.45 }, land);
          el("ellipse", { cx: px - 50, cy: py - 8, rx: 10 + R() * 12, ry: 7 + R() * 6, fill: "#6a6060" }, land); }
        // kaputter Zaun hinten (über die ganze Breite, mit Lücken)
        const fence = el("g", { opacity: 0.85 }, land);
        for (let fx = 40; fx < W; fx += 90 + R() * 40) { if (R() < 0.25) continue; const rot = (R() - 0.5) * 34;
          el("rect", { x: fx, y: 1010, width: 16, height: 110, rx: 3, fill: "#2a1a18", transform: `rotate(${rot} ${fx + 8} 1120)` }, fence);
          if (R() < 0.6) el("path", { d: `M${fx + 8} ${1040 + R() * 8} Q${fx + 60} ${1052} ${fx + 110} ${1040 + R() * 10}`, stroke: "#2a1a18", "stroke-width": 5, fill: "none" }, fence); }
        // Baum: karg, krumm, ein einziges Blatt
        const tree = el("g", {}, land); const bark = lin(D, pre + "bark", [[0, "#3a2620"], [0.6, "#24160f"], [1, "#120a08"]], 0, 0, 1, 0);
        const TX = o.treeX ?? 610, TY = 1210;
        function br(x, y, len, ang, w, d) {
          const x2 = x + len * Math.cos(ang), y2 = y + len * Math.sin(ang), mx = (x + x2) / 2 + (R() - 0.5) * len * 0.25, my = (y + y2) / 2 + (R() - 0.5) * len * 0.2;
          el("path", { d: `M${x} ${y} Q${mx} ${my} ${x2} ${y2}`, stroke: bark, "stroke-width": w, fill: "none", "stroke-linecap": "round" }, tree);
          if (d > 0) { br(x2, y2, len * 0.72, ang - 0.45 - R() * 0.25, w * 0.66, d - 1); br(x2, y2, len * 0.68, ang + 0.35 + R() * 0.3, w * 0.62, d - 1); if (R() > 0.6) br(x2, y2, len * 0.5, ang + (R() - 0.5) * 0.4, w * 0.5, d - 2); }
          return [x2, y2];
        }
        el("path", { d: `M${TX - 46} ${TY} Q${TX - 20} ${TY - 120} ${TX - 18} ${TY - 260} L${TX + 18} ${TY - 260} Q${TX + 24} ${TY - 120} ${TX + 54} ${TY}Z`, fill: bark }, tree);
        br(TX, TY - 250, 170, -1.95, 30, 4); br(TX, TY - 250, 190, -1.15, 28, 4); br(TX, TY - 200, 120, -0.35, 16, 2);
        // abbrechender Ast (eigene Gruppe, Drehpunkt = Ansatz am Stamm): brk / brkBase
        const brk = el("g", {}, tree), BX = TX + 14, BY = TY - 330;
        el("path", { d: `M${BX} ${BY} Q${BX + 90} ${BY - 30} ${BX + 190} ${BY - 110}`, stroke: bark, "stroke-width": 18, fill: "none", "stroke-linecap": "round" }, brk);
        el("path", { d: `M${BX + 110} ${BY - 44} Q${BX + 140} ${BY - 100} ${BX + 150} ${BY - 150} M${BX + 160} ${BY - 86} Q${BX + 210} ${BY - 90} ${BX + 240} ${BY - 70}`, stroke: bark, "stroke-width": 9, fill: "none", "stroke-linecap": "round" }, brk);
        const leafX = TX + 150, leafY = TY - 520;
        const leaf = el("path", { d: `M${leafX} ${leafY} q16 -22 34 -6 q-12 24 -34 6Z`, fill: "#9a8a2a" }, land);
        // Stuhl (Holz, leicht schief) unter dem Baum
        const chair = el("g", {}, land); const cw = lin(D, pre + "chw", [[0, "#b98a52"], [1, "#6b4824"]], 0, 0, 1, 1);
        const CX = o.chairX ?? 500, CY = 1250;
        el("ellipse", { cx: CX + 40, cy: CY + 6, rx: 120, ry: 18, fill: "#000", opacity: 0.4 }, chair);
        el("rect", { x: CX - 70, y: CY - 210, width: 16, height: 210, rx: 4, fill: cw }, chair);
        el("rect", { x: CX + 54, y: CY - 210, width: 16, height: 210, rx: 4, fill: cw }, chair);
        el("rect", { x: CX - 70, y: CY - 210, width: 140, height: 20, rx: 6, fill: cw }, chair);
        el("rect", { x: CX - 70, y: CY - 160, width: 140, height: 14, rx: 6, fill: cw }, chair);
        el("path", { d: `M${CX - 76} ${CY - 100} L${CX + 76} ${CY - 100} L${CX + 108} ${CY - 74} L${CX - 44} ${CY - 74}Z`, fill: "#c89a60" }, chair);
        el("rect", { x: CX - 46, y: CY - 76, width: 14, height: 76, rx: 4, fill: "#6b4824" }, chair);
        el("rect", { x: CX + 92, y: CY - 76, width: 14, height: 80, rx: 4, fill: "#6b4824", transform: `rotate(-4 ${CX + 99} ${CY})` }, chair);
        // Gerümpel im Standardbild: Reifen, Müllsäcke, Rostfass
        const junk = el("g", {}, land);
        el("ellipse", { cx: 190, cy: 1230, rx: 70, ry: 26, fill: "#121212" }, junk); el("ellipse", { cx: 190, cy: 1226, rx: 34, ry: 11, fill: "#2b1d1a" }, junk);
        [[90, 1135, "#16181c"], [140, 1145, "#22252b"]].forEach(([bx, by, c]) => { el("path", { d: `M${bx - 34} ${by} Q${bx - 40} ${by - 50} ${bx} ${by - 62} Q${bx + 40} ${by - 50} ${bx + 34} ${by}Z`, fill: c }, junk); el("path", { d: `M${bx - 6} ${by - 62} l-8 -14 M${bx + 4} ${by - 62} l8 -14`, stroke: c, "stroke-width": 6 }, junk); });
        el("rect", { x: 300, y: 1060, width: 50, height: 70, rx: 6, fill: "#7a3a1a", transform: "rotate(12 325 1130)" }, junk);
        el("path", { d: "M300 1080 h50 M300 1110 h50", stroke: "#4a200c", "stroke-width": 5, transform: "rotate(12 325 1130)" }, junk);
        // Weitere Verwahrlosung, nur wenn die Welt breiter ist (Kamerafahrt): Autowrack, Schuppen-Ruine, Badewanne, Einkaufswagen, Reifenstapel, Schild
        if (W > 1300) {
          const A = (x) => x; // Welt-x
          const rustC = lin(D, pre + "rst", [[0, "#9a4a22"], [0.6, "#6a3014"], [1, "#3a1a0a"]], 0, 0, 1, 1);
          // Autowrack ohne Räder auf Steinen
          const car = el("g", {}, land); gsap.set(car, { x: A(1350), y: 1150 });
          el("path", { d: "M-170 0 L-170 -60 Q-160 -80 -120 -84 L-70 -140 L70 -140 L120 -84 Q170 -78 176 -50 L176 0Z", fill: rustC }, car);
          el("path", { d: "M-60 -128 L-24 -128 L-24 -88 L-100 -88Z M-12 -128 L60 -128 L104 -88 L-12 -88Z", fill: "#1a1418" }, car);
          el("path", { d: "M-40 -120 l20 22 M20 -122 l30 28", stroke: "#c9d6e8", "stroke-width": 3, opacity: 0.6 }, car);
          [-110, 110].forEach((wx) => { el("rect", { x: wx - 30, y: -6, width: 60, height: 26, rx: 4, fill: "#6a6060" }, car); });
          el("circle", { cx: -60, cy: -40, r: 9, fill: "#2a1008" }, car); el("circle", { cx: 40, cy: -30, r: 13, fill: "#2a1008" }, car);
          el("path", { d: "M-160 -20 q30 -40 20 -80 M150 -10 q10 -30 -10 -60", stroke: "#4a5a2a", "stroke-width": 6, fill: "none" }, car);
          // Schuppen-Ruine mit eingesacktem Dach
          const shed = el("g", {}, land); gsap.set(shed, { x: A(1880), y: 1110 });
          el("rect", { x: -160, y: -200, width: 320, height: 200, fill: "#5a3a26" }, shed);
          for (let i = -140; i < 160; i += 40) el("path", { d: `M${i} -200 V0`, stroke: "#3a2416", "stroke-width": 5 }, shed);
          el("path", { d: "M-190 -190 L-10 -260 L40 -170 L190 -230 L190 -200 L40 -140 L-10 -230 L-190 -160Z", fill: "#3a3a42" }, shed);
          el("rect", { x: -40, y: -120, width: 70, height: 120, fill: "#120c0a" }, shed);
          el("rect", { x: 30, y: -120, width: 60, height: 120, fill: "#6a4a30", transform: "rotate(18 30 0)" }, shed);
          el("rect", { x: 70, y: -170, width: 60, height: 44, fill: "#1a1418" }, shed); el("path", { d: "M70 -170 l60 44 M130 -170 l-30 22", stroke: "#c9d6e8", "stroke-width": 3, opacity: 0.6 }, shed);
          // Badewanne mit Brackwasser
          const tub = el("g", {}, land); gsap.set(tub, { x: A(2330), y: 1200 });
          el("path", { d: "M-110 -70 L110 -70 Q110 0 70 0 L-70 0 Q-110 0 -110 -70Z", fill: "#e6e2d8" }, tub);
          el("ellipse", { cx: 0, cy: -70, rx: 112, ry: 16, fill: "#4a5a3a" }, tub);
          [-80, 80].forEach((fx) => el("path", { d: `M${fx} 0 l-6 16 h16Z`, fill: "#c9a24a" }, tub));
          el("path", { d: "M-100 -60 q20 30 60 40", stroke: "#8a6a3a", "stroke-width": 4, fill: "none", opacity: 0.6 }, tub);
          // umgekippter Einkaufswagen
          const cart = el("g", {}, land); gsap.set(cart, { x: A(2700), y: 1180, rotation: -14 });
          el("path", { d: "M-80 -100 L80 -100 L60 -20 L-60 -20Z", fill: "none", stroke: "#a8b0bc", "stroke-width": 6 }, cart);
          for (let i = -60; i <= 60; i += 20) el("path", { d: `M${i} -100 L${i * 0.75} -20`, stroke: "#a8b0bc", "stroke-width": 3 }, cart);
          el("path", { d: "M-90 -84 L70 -84 M-70 -52 L66 -52", stroke: "#a8b0bc", "stroke-width": 3 }, cart);
          el("path", { d: "M80 -100 L110 -130", stroke: "#a8b0bc", "stroke-width": 6 }, cart);
          [-50, 50].forEach((wx) => el("circle", { cx: wx, cy: 0, r: 12, fill: "#22252b" }, cart));
          // Reifenstapel
          const tires = el("g", {}, land); gsap.set(tires, { x: A(3020), y: 1160 });
          [0, -34, -68].forEach((ty, i) => { el("ellipse", { cx: i * 6, cy: ty, rx: 70, ry: 24, fill: "#121212" }, tires); el("ellipse", { cx: i * 6, cy: ty - 4, rx: 34, ry: 10, fill: "#2b1d1a" }, tires); });
          // schiefes Schild „BETRETEN AUF EIGENE GEFAHR“
          const sign = el("g", {}, land); gsap.set(sign, { x: A(2120), y: 1150, rotation: 9 });
          el("rect", { x: -6, y: -150, width: 12, height: 150, fill: "#3a2416" }, sign);
          el("rect", { x: -130, y: -226, width: 260, height: 96, rx: 6, fill: "#e8d9a0" }, sign);
          const st = el("text", { x: 0, y: -186, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 30, fill: "#8a1a1a", "data-layout-ignore": "" }, sign); st.textContent = "BETRETEN AUF";
          const st2 = el("text", { x: 0, y: -146, "text-anchor": "middle", "font-family": "Inter", "font-weight": 900, "font-size": 30, fill: "#8a1a1a", "data-layout-ignore": "" }, sign); st2.textContent = "EIGENE GEFAHR";
          // Dornenbüsche
          [1150, 1620, 2520, 2900].forEach((bx) => { for (let i = 0; i < 9; i++) el("path", { d: `M${bx} 1130 q${(R() - 0.5) * 120} ${-40 - R() * 60} ${(R() - 0.5) * 160} ${-60 - R() * 70}`, stroke: "#3a3a1a", "stroke-width": 4, fill: "none" }, land); });
        }
        // Ziege, grast (Kopf unten); goat.head kauend animieren
        const goat = o.goatX === null ? null : goatFig(land, o.goatX ?? 880, 1150, o.goatS ?? 0.8, !!o.goatFlip);
        if (goat) gsap.set(goat.head, { rotation: 38 });
        // Unkraut über die ganze Breite
        const weeds = el("g", {}, land);
        for (let i = 0; i < 140 * W / 1080; i++) { const wx = R() * W, wy = 1110 + R() * R() * 800, h = 20 + R() * 60 * (wy / 1300), c = ["#4a5a2a", "#6b6a32", "#8a7a3a", "#3a4422"][i % 4];
          el("path", { d: `M${wx} ${wy} q${(R() - 0.5) * 20} ${-h * 0.6} ${(R() - 0.5) * 30} ${-h}`, stroke: c, "stroke-width": 3 + R() * 3, fill: "none", "stroke-linecap": "round" }, weeds); }
        const dust = el("g", {}, sv);
        const motes = Array.from({ length: 26 }, () => el("circle", { cx: 100 + R() * 880, cy: 500 + R() * 600, r: 2 + R() * 4, fill: "#ffe2a8", opacity: 0.25 + R() * 0.5 }, dust));
        return { sky, land, far, sunG, rays, tree, brk, brkBase: [BX, BY], leaf, chair, goat, weeds, dust, motes, fence, chairPos: [CX, CY], treePos: [TX, TY] };
      }
      // Ziege kaut (Kopf wippt, endlich)
      function chew(tl, G, t0, dur) { if (G.goat) tl.to(G.goat.head, { rotation: 30, duration: 0.22, yoyo: true, repeat: Math.max(1, 2 * Math.floor(dur / 0.44) - 1), ease: "sine.inOut" }, t0); }
      // Filmlook: Vignette + feines Korn (statisch) – als oberste Ebene einer Szene
      function filmLook(sv, pre, strength = 1) {
        const D = GR(sv);
        el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: rad(D, pre + "vig", [[0.55, "#000", 0], [1, "#000", 0.7 * strength]], 0.5, 0.42, 0.75), "pointer-events": "none" }, sv);
        const f = el("filter", { id: pre + "grain", x: 0, y: 0, width: "100%", height: "100%" }, D);
        el("feTurbulence", { type: "fractalNoise", baseFrequency: 0.9, numOctaves: 2, seed: 3, result: "n" }, f);
        el("feColorMatrix", { type: "saturate", values: 0 }, f);
        el("rect", { x: 0, y: 0, width: 1080, height: 1920, filter: `url(#${pre}grain)`, opacity: 0.07 * strength, style: "mix-blend-mode:overlay" }, sv);
      }
      // Staubteilchen schweben lassen (endlich, über die Szenendauer)
      function floatDust(tl, G, dur) { G.motes.forEach((m, i) => tl.to(m, { y: -60 - (i % 5) * 20, x: (i % 3 - 1) * 30, duration: dur, ease: "none" }, 0)); }
