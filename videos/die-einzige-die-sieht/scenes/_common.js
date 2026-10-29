      // ---- Gemeinsame Zeichenhelfer (flacher Stil wie Referenz) ----
      const NS = "http://www.w3.org/2000/svg";
      const el = (n, a, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
      // Arm als Gruppe, dreht um die Schulter (sx, sy); 0° = hängt nach unten
      function arm(g, sx, sy, deg, skin, sleeve) {
        const a = el("g", {}, g);
        el("rect", { x: sx - 12, y: sy - 4, width: 24, height: 60, rx: 12, fill: sleeve }, a);
        el("rect", { x: sx - 10, y: sy + 40, width: 20, height: 56, rx: 10, fill: skin }, a);
        el("circle", { cx: sx, cy: sy + 100, r: 14, fill: skin }, a);
        gsap.set(a, { rotation: deg, svgOrigin: `${sx} ${sy}` });
        return a;
      }
      // Figur: Ursprung = Mitte des Oberkörpers oben. o.long = lange Haare, o.blind = trübe Augen, o.closed = Augen zu
      function person(parent, id, x, y, s = 1, o = {}) {
        const skin = o.skin || "#f2c9a5", shirt = o.shirt || "#4da3ff", hair = o.hair || "#5b3a26", pants = o.pants || "#2a3170";
        const g = el("g", { id }, parent);
        gsap.set(g, { x, y, scale: s, transformOrigin: "0 0" });
        const ang = o.arms || [12, -12];
        el("rect", { x: -34, y: 118, width: 28, height: 110, rx: 12, fill: pants }, g);
        el("rect", { x: 6, y: 118, width: 28, height: 110, rx: 12, fill: pants }, g);
        el("rect", { x: -40, y: 222, width: 36, height: 16, rx: 8, fill: "#1a1f45" }, g);
        el("rect", { x: 4, y: 222, width: 36, height: 16, rx: 8, fill: "#1a1f45" }, g);
        const a1 = arm(g, -52, 18, ang[0], skin, shirt), a2 = arm(g, 52, 18, ang[1], skin, shirt);
        el("rect", { x: -56, y: 0, width: 112, height: 132, rx: 40, fill: shirt }, g);
        if (o.long) el("path", { d: "M-52 -60 C-56 -128 56 -128 52 -60 L60 34 Q30 48 0 30 Q-30 48 -60 34Z", fill: hair }, g);
        el("rect", { x: -12, y: -18, width: 24, height: 22, fill: skin }, g);
        el("circle", { cx: 0, cy: -58, r: 46, fill: skin }, g);
        el("path", { d: o.long ? "M-48 -54 C-52 -122 52 -122 48 -54 C40 -92 -10 -98 -48 -54Z" : "M-46 -60 C-46 -118 46 -118 46 -60 C30 -84 -20 -88 -46 -60Z", fill: hair }, g);
        const eyes = el("g", {}, g);
        if (o.blind) { [-16, 16].forEach((cx) => { el("circle", { cx, cy: -56, r: 9, fill: "#e4e8f6" }, eyes); el("circle", { cx, cy: -56, r: 5, fill: "#b4bbd6" }, eyes); }); }
        else { el("circle", { cx: -16, cy: -56, r: 7, fill: "#161a36" }, eyes); el("circle", { cx: 16, cy: -56, r: 7, fill: "#161a36" }, eyes); }
        const lids = el("path", { d: "M-24 -56 q8 6 16 0 M8 -56 q8 6 16 0", fill: "none", stroke: "#161a36", "stroke-width": 4, "stroke-linecap": "round", opacity: o.closed ? 1 : 0 }, g);
        if (o.closed) gsap.set(eyes, { opacity: 0 });
        const mouth = el("path", { d: o.sad ? "M-14 -26 q14 -10 28 0" : "M-12 -30 q12 8 24 0", fill: "none", stroke: "#8a3b2a", "stroke-width": 5, "stroke-linecap": "round" }, g);
        return { g, a1, a2, eyes, lids, mouth };
      }
      // kleine Figur (Menge), Arme tastend nach vorn/außen
      function mini(parent, x, y, c, glow) {
        const g = el("g", { opacity: 0 }, parent);
        if (glow) g.style.filter = "drop-shadow(0 0 18px rgba(255,212,59,.9))";
        el("path", { d: `M${x - 14} ${y + 22} l-22 -14 M${x + 14} ${y + 22} l22 -14`, stroke: glow ? "#f2c9a5" : "#9aa1c4", "stroke-width": 7, "stroke-linecap": "round" }, g);
        el("circle", { cx: x, cy: y, r: 14, fill: glow ? "#f2c9a5" : "#9aa1c4" }, g);
        el("rect", { x: x - 15, y: y + 15, width: 30, height: 42, rx: 11, fill: c }, g);
        return g;
      }
      // großes Auge (Mandelform), Pupille separat beweglich
      function bigEye(parent, cx, cy, s = 1) {
        const g = el("g", {}, parent); gsap.set(g, { x: cx, y: cy, scale: s, transformOrigin: "0 0" });
        const glow = null; g.style.filter = "drop-shadow(0 0 40px rgba(255,212,59,.6))";
        el("path", { d: "M-240 0 Q0 -175 240 0 Q0 175 -240 0Z", fill: "#f3f1ea" }, g);
        const iris = el("g", {}, g);
        el("circle", { cx: 0, cy: 0, r: 86, fill: "#4da3ff" }, iris);
        el("circle", { cx: 0, cy: 0, r: 60, fill: "#2b6fd1" }, iris);
        el("circle", { cx: 0, cy: 0, r: 38, fill: "#0b0e22" }, iris);
        el("circle", { cx: 26, cy: -26, r: 16, fill: "#fff" }, iris);
        el("path", { d: "M-240 0 Q0 -175 240 0", fill: "none", stroke: "#161a36", "stroke-width": 14, "stroke-linecap": "round" }, g);
        return { g, iris, glow };
      }
      function radio(parent, x, y, s = 1) {
        const g = el("g", {}, parent); gsap.set(g, { x, y, scale: s, transformOrigin: "0 0" });
        el("path", { d: "M180 -150 L260 -300", stroke: "#c9cde6", "stroke-width": 10, "stroke-linecap": "round" }, g);
        el("rect", { x: -300, y: -160, width: 600, height: 320, rx: 40, fill: "#8a5a2b" }, g);
        el("rect", { x: -280, y: -140, width: 560, height: 280, rx: 28, fill: "#a86b2c" }, g);
        el("circle", { cx: -140, cy: 0, r: 110, fill: "#5e3b1a" }, g);
        for (let i = -3; i <= 3; i++) el("rect", { x: -230, y: i * 26 - 4, width: 180, height: 8, rx: 4, fill: "#8a5a2b" }, g);
        el("rect", { x: 20, y: -100, width: 240, height: 90, rx: 12, fill: "#ffe9a8" }, g);
        for (let i = 0; i < 9; i++) el("rect", { x: 40 + i * 24, y: -84, width: 4, height: i % 2 ? 20 : 34, fill: "#8a5a2b" }, g);
        const needle = el("rect", { x: 90, y: -96, width: 6, height: 82, fill: "#ff3b55" }, g);
        el("circle", { cx: 80, cy: 70, r: 38, fill: "#5e3b1a" }, g); el("circle", { cx: 200, cy: 70, r: 38, fill: "#5e3b1a" }, g);
        return { g, needle };
      }
      function car(parent, x, y, c, rot = 0) {
        const g = el("g", {}, parent); gsap.set(g, { x, y, rotation: rot, transformOrigin: "0 0" });
        el("rect", { x: -130, y: -40, width: 260, height: 70, rx: 22, fill: c }, g);
        el("path", { d: "M-70 -40 L-40 -90 L50 -90 L80 -40Z", fill: c }, g);
        el("path", { d: "M-56 -44 L-34 -80 L0 -80 L0 -44Z M10 -44 L10 -80 L44 -80 L64 -44Z", fill: "#a9d2ff" }, g);
        el("circle", { cx: -70, cy: 34, r: 26, fill: "#161a36" }, g); el("circle", { cx: 70, cy: 34, r: 26, fill: "#161a36" }, g);
        const blink = el("g", { opacity: 0 }, g);
        el("circle", { cx: -124, cy: -10, r: 12, fill: "#ffb020" }, blink); el("circle", { cx: 124, cy: -10, r: 12, fill: "#ffb020" }, blink);
        return { g, blink };
      }
