      // ---- Flache Grusel-Vektorwelt (Stil Referenz B2: dunkle Konturen, Nacht, Nebel) ----
      const NS = "http://www.w3.org/2000/svg", K = "#0b0c14";
      const el = (n, a, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
      const txt = (p, x, y, s, size, fill, a = {}) => { const t = el("text", Object.assign({ x, y, "text-anchor": "middle", "font-family": "Oswald", "font-weight": 700, "font-size": size, fill }, a), p); t.textContent = s; return t; };
      const O = (a) => Object.assign({ stroke: K, "stroke-width": 5, "stroke-linejoin": "round" }, a);
      function night(p, id, c1, c2, moon = [820, 640]) {
        const d = el("defs", {}, p), lg = el("linearGradient", { id, x1: 0, y1: 0, x2: 0, y2: 1 }, d);
        el("stop", { offset: 0, "stop-color": c1 }, lg); el("stop", { offset: 1, "stop-color": c2 }, lg);
        el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: `url(#${id})` }, p);
        const r = rng(id.length * 7); for (let i = 0; i < 40; i++) el("circle", { cx: r() * 1080, cy: r() * 900, r: 1 + r() * 2, fill: "#fff", opacity: 0.25 + r() * 0.4 }, p);
        if (moon) { el("circle", { cx: moon[0], cy: moon[1], r: 120, fill: "#f4e9c8", opacity: 0.12 }, p); el("circle", { cx: moon[0], cy: moon[1], r: 64, fill: "#efe6c8" }, p); }
      }
      function pines(p, y, col = "#121a2a", seed = 3) { const r = rng(seed), g = el("g", {}, p);
        for (let i = 0; i < 16; i++) { const x = i * 72 + r() * 30 - 20, h = 140 + r() * 90; el("path", { d: `M${x} ${y} L${x + 40} ${y - h} L${x + 80} ${y}Z`, fill: col }, g); } return g; }
      function house(p, x, by, w, h, col, o = {}) {
        const g = el("g", {}, p), wins = [];
        el("rect", O({ x, y: by - h, width: w, height: h, fill: col }), g);
        el("path", O({ d: `M${x - 18} ${by - h + 4} L${x + w / 2} ${by - h - w * 0.42} L${x + w + 18} ${by - h + 4}Z`, fill: o.roof || "#2a2236" }), g);
        const n = o.n || 2; for (let i = 0; i < n; i++) { const wx = x + (i + 0.5) * w / n - 26; wins.push(el("rect", O({ x: wx, y: by - h + 30, width: 52, height: 56, fill: o.lit && o.lit[i] ? "#ffcf6b" : "#1a2033", "stroke-width": 4 }), g)); }
        if (o.door !== false) el("rect", O({ x: x + w / 2 - 24, y: by - 92, width: 48, height: 92, fill: "#3a2a22", "stroke-width": 4 }), g);
        return { g, wins };
      }
      function lamp(p, x, by, on = true) { const g = el("g", {}, p);
        const cone = el("path", { d: `M${x + 40} ${by - 330} L${x - 70} ${by} L${x + 150} ${by}Z`, fill: "#ffe7a3", opacity: on ? 0.16 : 0 }, g);
        el("rect", O({ x: x - 7, y: by - 340, width: 14, height: 340, fill: "#2a2f40", "stroke-width": 4 }), g);
        el("path", O({ d: `M${x} ${by - 340} q20 -30 50 -10`, fill: "none", "stroke-width": 8, stroke: "#2a2f40" }), g);
        el("circle", { cx: x + 46, cy: by - 334, r: 14, fill: "#ffe7a3" }, g); return { g, cone }; }
      function fog(p, y, op = 0.35, seed = 5) { const r = rng(seed), g = el("g", {}, p);
        for (let i = 0; i < 9; i++) el("ellipse", { cx: r() * 1080, cy: y + r() * 80, rx: 220 + r() * 160, ry: 40 + r() * 30, fill: "#c9cfe6", opacity: op * (0.4 + r() * 0.6) }, g); return g; }
      // Maskierte Figur (Fußpunkt x, by)
      function masked(p, x, by, s = 1, coat = "#1d1f2b", tool = false) {
        const g = el("g", {}, p); gsap.set(g, { x, y: by, scale: s, transformOrigin: "0 0" });
        el("path", O({ d: "M-46 0 L-40 -150 L40 -150 L46 0Z", fill: "#14151d" }), g);
        el("path", O({ d: "M-70 -140 Q-74 -300 0 -310 Q74 -300 70 -140Z", fill: coat }), g);
        if (tool) el("path", O({ d: "M64 -200 L120 -60 M104 -90 l30 -12 l10 24 l-30 12Z", fill: "#8a8f9c", "stroke-width": 6 }), g);
        el("path", O({ d: "M-58 -300 Q-62 -400 0 -404 Q62 -400 58 -300 Q40 -290 0 -290 Q-40 -290 -58 -300Z", fill: "#2a2c38" }), g);
        const mask = el("g", {}, g);
        el("ellipse", O({ cx: 0, cy: -345, rx: 40, ry: 50, fill: "#ece6d6", "stroke-width": 4 }), mask);
        el("ellipse", { cx: -15, cy: -355, rx: 9, ry: 6, fill: K }, mask); el("ellipse", { cx: 15, cy: -355, rx: 9, ry: 6, fill: K }, mask);
        el("path", { d: "M-20 -322 Q0 -310 20 -322", stroke: "#c8102e", "stroke-width": 4, fill: "none" }, mask);
        [-14, -5, 5, 14].forEach((sx) => el("path", { d: `M${sx} -326 v8`, stroke: "#c8102e", "stroke-width": 3 }, mask));
        return { g, mask };
      }
      function pumpkin(p, x, y, s = 1) { const g = el("g", {}, p); gsap.set(g, { x, y, scale: s, transformOrigin: "0 0" });
        el("ellipse", O({ cx: 0, cy: 0, rx: 46, ry: 36, fill: "#e8761f", "stroke-width": 4 }), g); el("rect", O({ x: -5, y: -46, width: 10, height: 14, fill: "#3d6b1e", "stroke-width": 3 }), g);
        const face = el("path", { d: "M-24 -8 l8 -10 l8 10Z M8 -8 l8 -10 l8 10Z M-22 12 q22 14 44 0 l-6 -6 l-6 6 l-8 -6 l-8 6 l-8 -6Z", fill: "#ffd76b" }, g); return { g, face }; }
      function flames(p, x, y, s = 1) { const g = el("g", {}, p); gsap.set(g, { x, y, scale: s, transformOrigin: "0 0" });
        el("path", { d: "M-60 0 Q-70 -80 -30 -120 Q-20 -70 0 -150 Q30 -90 40 -130 Q80 -70 60 0Z", fill: "#ff5a1f" }, g);
        el("path", { d: "M-34 0 Q-40 -50 -12 -80 Q0 -40 12 -96 Q40 -50 34 0Z", fill: "#ffc53a" }, g); return g; }
      function plank(p, x, y, w, rot) { return el("rect", O({ x, y, width: w, height: 22, rx: 4, fill: "#a87a4a", "stroke-width": 4, transform: `rotate(${rot} ${x + w / 2} ${y + 11})` }), p); }
      function flatCard(p, x, y, w, h, fill = "#efe8d6") { return el("rect", O({ x, y, width: w, height: h, rx: 18, fill }), p); }
