      // ---- Gemeinsame Zeichenhelfer (flacher Stil wie Referenz) ----
      const NS = "http://www.w3.org/2000/svg";
      const el = (n, a, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
      // Gegenstände für die Hände (Koordinaten relativ zur Hand)
      const ITEMS = {
        cup: (g) => { el("rect", { x: -16, y: -6, width: 32, height: 38, rx: 6, fill: "#fff" }, g); el("rect", { x: -12, y: -2, width: 24, height: 8, fill: "#6b3f1d" }, g);
                      el("path", { d: "M16 4 q16 0 16 12 q0 12 -16 12", fill: "none", stroke: "#fff", "stroke-width": 6 }, g); },
        phone: (g) => { el("rect", { x: -15, y: -8, width: 30, height: 54, rx: 6, fill: "#1b2150", stroke: "#8fa2ff", "stroke-width": 3 }, g);
                        el("rect", { x: -10, y: -2, width: 20, height: 34, rx: 3, fill: "#4da3ff" }, g); },
        bread: (g) => { el("ellipse", { cx: 0, cy: 10, rx: 30, ry: 20, fill: "#e0a35a" }, g); el("path", { d: "M-14 2 l8 10 M0 0 l8 10 M14 2 l8 10", stroke: "#a86b2c", "stroke-width": 4 }, g); },
        knife: (g) => { el("rect", { x: -4, y: -4, width: 8, height: 26, rx: 3, fill: "#6b3f1d" }, g); el("path", { d: "M-5 22 L5 22 L3 70 L-6 64Z", fill: "#dfe3f5" }, g); },
        spoon: (g) => { el("rect", { x: -3, y: -4, width: 6, height: 50, rx: 3, fill: "#c9cde6" }, g); el("ellipse", { cx: 0, cy: 54, rx: 11, ry: 15, fill: "#c9cde6" }, g); },
        salt: (g) => { el("rect", { x: -12, y: -6, width: 24, height: 40, rx: 6, fill: "#fff" }, g); el("rect", { x: -12, y: -10, width: 24, height: 10, rx: 4, fill: "#8fa2ff" }, g); },
        pen: (g) => { el("rect", { x: -4, y: -6, width: 8, height: 46, rx: 3, fill: "#ffd43b" }, g); el("path", { d: "M-4 40 L4 40 L0 52Z", fill: "#333" }, g); },
        glove: (g) => { el("path", { d: "M-16 30 L-16 0 q0 -8 6 -8 L-10 -22 q4 -6 8 0 L-2 -26 q4 -6 8 0 L6 -20 q4 -6 8 0 L14 0 q8 -6 10 2 L16 30Z", fill: "#39e27a" }, g); },
      };
      // Arm als Gruppe, dreht um die Schulter (sx, sy); 0° = hängt nach unten
      function arm(g, id, sx, sy, deg, skin, sleeve, item) {
        const a = el("g", { id }, g);
        el("rect", { x: sx - 12, y: sy - 4, width: 24, height: 60, rx: 12, fill: sleeve }, a);
        el("rect", { x: sx - 10, y: sy + 40, width: 20, height: 56, rx: 10, fill: skin }, a);
        el("circle", { cx: sx, cy: sy + 100, r: 14, fill: skin }, a);
        if (item) { const h = el("g", { transform: `translate(${sx} ${sy + 104}) rotate(180)` }, a); ITEMS[item](h); }
        gsap.set(a, { rotation: deg, svgOrigin: `${sx} ${sy}` });
        return a;
      }
      // Figur: Ursprung = Mitte des Oberkörpers oben. o.arms = [Winkel links, rechts, dritter], o.items = [..3]
      function person(parent, id, x, y, s = 1, o = {}) {
        const skin = o.skin || "#f2c9a5", shirt = o.shirt || "#4da3ff", hair = o.hair || "#5b3a26", pants = o.pants || "#2a3170";
        const g = el("g", { id }, parent);
        gsap.set(g, { x, y, scale: s, transformOrigin: "0 0" });
        const ang = o.arms || [12, -12, -150], it = o.items || [];
        el("rect", { x: -34, y: 118, width: 28, height: 110, rx: 12, fill: pants }, g);
        el("rect", { x: 6, y: 118, width: 28, height: 110, rx: 12, fill: pants }, g);
        el("rect", { x: -40, y: 222, width: 36, height: 16, rx: 8, fill: "#1a1f45" }, g);
        el("rect", { x: 4, y: 222, width: 36, height: 16, rx: 8, fill: "#1a1f45" }, g);
        const back = [arm(g, id + "-a1", -52, 18, ang[0], skin, shirt, it[0]), arm(g, id + "-a2", 52, 18, ang[1], skin, shirt, it[1])];
        el("rect", { x: -56, y: 0, width: 112, height: 132, rx: 40, fill: shirt }, g);
        const third = o.three === false ? null : arm(g, id + "-a3", 0, 46, ang[2], skin, o.shirt3 || shirt, it[2]);
        el("rect", { x: -12, y: -18, width: 24, height: 22, fill: skin }, g);
        el("circle", { cx: 0, cy: -58, r: 46, fill: skin }, g);
        el("path", { d: "M-46 -60 C-46 -118 46 -118 46 -60 C30 -84 -20 -88 -46 -60Z", fill: hair }, g);
        const eyes = el("g", { id: id + "-eyes" }, g);
        el("circle", { cx: -16, cy: -56, r: 6, fill: "#161a36" }, eyes); el("circle", { cx: 16, cy: -56, r: 6, fill: "#161a36" }, eyes);
        el("path", { id: id + "-mouth", d: o.sad ? "M-14 -26 q14 -10 28 0" : "M-14 -32 q14 14 28 0", fill: "none", stroke: "#8a3b2a", "stroke-width": 5, "stroke-linecap": "round" }, g);
        return { g, a1: back[0], a2: back[1], a3: third, eyes };
      }
      // kleine Figur (Menge): Kopf, Körper, drei Arme als Striche
      function mini(parent, x, y, c) {
        const g = el("g", { opacity: 0 }, parent);
        el("circle", { cx: x, cy: y, r: 12, fill: "#f2c9a5" }, g);
        el("rect", { x: x - 14, y: y + 14, width: 28, height: 40, rx: 10, fill: c }, g);
        el("path", { d: `M${x - 14} ${y + 22} l-14 22 M${x + 14} ${y + 22} l14 22 M${x} ${y + 30} l10 -26`, stroke: "#f2c9a5", "stroke-width": 6, "stroke-linecap": "round" }, g);
        return g;
      }
      // Arm winken lassen (endlich viele Wiederholungen)
      const wave = (tl, a, from, to, t, n = 3, d = 0.18) => tl.to(a, { rotation: to, duration: d, repeat: n * 2 - 1, yoyo: true, ease: "sine.inOut" }, t);
