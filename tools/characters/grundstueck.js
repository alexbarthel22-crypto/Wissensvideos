      // ===== Das geerbte Grundstück (Serien-Kulisse): verwahrlost, ein Stuhl unter einem kargen Baum =====
      // Braucht: el(), lin(), rad(), gsap, rng(). Zeichnet in eine 1080×1920-SVG. o.mood: "dusk" (Abendrot, Standard) | "night" | "day"
      function grundstueck(sv, pre, o = {}) {
        const D = GR(sv), R = rng(o.seed || 7), mood = o.mood || "dusk";
        const skyC = { dusk: [[0, "#1a1240"], [0.45, "#5b2a6e"], [0.75, "#d0604a"], [1, "#ffb15c"]],
          night: [[0, "#05060f"], [0.6, "#121634"], [1, "#2a2350"]], day: [[0, "#6d9cc8"], [0.7, "#c9d6d8"], [1, "#efe2c2"]] }[mood];
        const sky = el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: lin(D, pre + "sky", skyC) }, sv);
        const land = el("g", {}, sv); gsap.set(land, { y: o.dy ?? -130 });
        const sunG = el("g", {}, land);
        el("circle", { cx: 760, cy: 960, r: 520, fill: rad(D, pre + "sunh", [[0, "#ffd08a", 0.75], [0.4, "#ff9a5a", 0.25], [1, "#ff9a5a", 0]]) }, sunG);
        el("circle", { cx: 760, cy: 960, r: 90, fill: "#ffe2a8", opacity: mood === "night" ? 0 : 0.95 }, sunG);
        if (mood === "night") gsap.set(sunG, { opacity: 0.25 });
        // Lichtstrahlen (Gottesstrahlen)
        const rays = el("g", { opacity: 0.0 }, land);
        for (let i = 0; i < 9; i++) { const a = -150 + i * 15 + R() * 6; const r1 = 1700;
          el("path", { d: `M760 960 L${760 + r1 * Math.cos((a - 2.5) * Math.PI / 180)} ${960 + r1 * Math.sin((a - 2.5) * Math.PI / 180)} L${760 + r1 * Math.cos((a + 2.5) * Math.PI / 180)} ${960 + r1 * Math.sin((a + 2.5) * Math.PI / 180)}Z`,
            fill: lin(D, pre + "ray" + i, [[0, "#fff1c4", 0.5], [1, "#fff1c4", 0]], 0, 0, 1, 0) }, rays); }
        // Hügel in Lufperspektive
        el("path", { d: "M0 1010 Q160 900 330 960 Q520 1020 700 930 Q900 850 1080 960 L1080 1920 L0 1920Z", fill: mood === "day" ? "#8a9a8c" : "#4a2a55", opacity: 0.8 }, land);
        el("path", { d: "M0 1060 Q240 990 470 1050 Q760 1110 1080 1020 L1080 1920 L0 1920Z", fill: mood === "day" ? "#6d7a5a" : "#2f1d3a" }, land);
        // Boden: trockene Wiese, Erde
        el("rect", { x: 0, y: 1080, width: 1080, height: 1000, fill: lin(D, pre + "gr", mood === "day" ? [[0, "#8b7a4a"], [1, "#4a3f22"]] : [[0, "#5a3f34"], [0.5, "#33231f"], [1, "#160f12"]]) }, land);
        // kaputter Zaun hinten
        const fence = el("g", { opacity: 0.85 }, land);
        [[40, 0], [130, 6], [230, -14], [330, 4], [690, 10], [800, -8], [900, 18], [1010, 3]].forEach(([fx, rot]) => {
          el("rect", { x: fx, y: 1010, width: 16, height: 110, rx: 3, fill: "#2a1a18", transform: `rotate(${rot} ${fx + 8} 1120)` }, fence); });
        el("path", { d: "M40 1040 Q190 1052 340 1036 M690 1046 Q850 1030 1020 1050", stroke: "#2a1a18", "stroke-width": 5, fill: "none" }, fence);
        el("path", { d: "M40 1074 Q120 1090 250 1078", stroke: "#2a1a18", "stroke-width": 5, fill: "none" }, fence);
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
        // Gerümpel: alter Reifen, Unkraut
        el("ellipse", { cx: 190, cy: 1230, rx: 70, ry: 26, fill: "#121212" }, land); el("ellipse", { cx: 190, cy: 1226, rx: 34, ry: 11, fill: "#2b1d1a" }, land);
        const weeds = el("g", {}, land);
        for (let i = 0; i < 140; i++) { const wx = R() * 1080, wy = 1110 + R() * R() * 800, h = 20 + R() * 60 * (wy / 1300), c = ["#4a5a2a", "#6b6a32", "#8a7a3a", "#3a4422"][i % 4];
          el("path", { d: `M${wx} ${wy} q${(R() - 0.5) * 20} ${-h * 0.6} ${(R() - 0.5) * 30} ${-h}`, stroke: c, "stroke-width": 3 + R() * 3, fill: "none", "stroke-linecap": "round" }, weeds); }
        // Staub im Gegenlicht
        const dust = el("g", {}, land);
        const motes = Array.from({ length: 26 }, () => el("circle", { cx: 300 + R() * 700, cy: 500 + R() * 700, r: 2 + R() * 4, fill: "#ffe2a8", opacity: 0.25 + R() * 0.5 }, dust));
        return { sky, land, sunG, rays, tree, leaf, chair, weeds, dust, motes, fence, chairPos: [CX, CY], treePos: [TX, TY] };
      }
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
