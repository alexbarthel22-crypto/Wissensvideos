      // ---- Isometrische Low-Poly-Helfer (Stil Referenz A: Klötzchen-Welt, weiche Farben) ----
      const NS = "http://www.w3.org/2000/svg";
      const el = (n, a, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
      const txt = (p, x, y, s, size, fill, a = {}) => { const t = el("text", Object.assign({ x, y, "text-anchor": "middle", "font-family": "Inter", "font-weight": 800, "font-size": size, fill }, a), p); t.textContent = s; return t; };
      const shade = (hex, f) => { const n = parseInt(hex.slice(1), 16); const c = [n >> 16, (n >> 8) & 255, n & 255].map((v) => Math.max(0, Math.min(255, Math.round(f > 1 ? v + (255 - v) * (f - 1) : v * f))));
        return "#" + c.map((v) => v.toString(16).padStart(2, "0")).join(""); };
      // Kamera: Ursprung (ox, oy), Einheit u
      const iso = (ox, oy, u) => (x, y, z = 0) => [ox + (x - y) * u * 0.866, oy + (x + y) * u * 0.5 - z * u];
      const poly = (pts) => pts.map((p) => p.map((v) => v.toFixed(1)).join(",")).join(" ");
      function box(P, p, x, y, z, w, d, h, col, a = {}) {
        const g = el("g", a, p);
        el("polygon", { points: poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]), fill: shade(col, 0.78) }, g);
        el("polygon", { points: poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)]), fill: col }, g);
        el("polygon", { points: poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]), fill: shade(col, 1.18) }, g);
        return g;
      }
      // Fläche auf der hinteren Wand (y = 0) bzw. linken Wand (x = 0)
      const wallY = (P, p, x0, x1, z0, z1, fill, a = {}) => el("polygon", Object.assign({ points: poly([P(x0, 0, z0), P(x1, 0, z0), P(x1, 0, z1), P(x0, 0, z1)]), fill }, a), p);
      const wallX = (P, p, y0, y1, z0, z1, fill, a = {}) => el("polygon", Object.assign({ points: poly([P(0, y0, z0), P(0, y1, z0), P(0, y1, z1), P(0, y0, z1)]), fill }, a), p);
      function room(P, p, W, D, H, o = {}) {
        const g = el("g", {}, p);
        box(P, g, 0, 0, -0.25, W, D, 0.25, o.floor || "#c9a982");
        for (let k = 1; k < W; k++) el("polyline", { points: poly([P(k, 0, 0), P(k, D, 0)]), stroke: shade(o.floor || "#c9a982", 0.9), "stroke-width": 2, fill: "none" }, g);
        wallY(P, g, 0, W, 0, H, o.wall || "#ece6dc"); wallX(P, g, 0, D, 0, H, shade(o.wall || "#ece6dc", 0.9));
        el("polyline", { points: poly([P(0, D, 0), P(0, 0, 0), P(W, 0, 0)]), stroke: shade(o.wall || "#ece6dc", 0.75), "stroke-width": 6, fill: "none" }, g);
        return g;
      }
      // Klötzchen-Figur; Ursprung = Fußpunkt (x, y, z). o.pose: "stand" | "sit" | "lie"
      function person(P, p, x, y, z, o = {}) {
        const g = el("g", {}, p), skin = o.skin || "#f0c8a0", shirt = o.shirt || "#e85d5d", pants = o.pants || "#3d4a7a", hair = o.hair || "#4a3020";
        if (o.pose === "lie") {
          box(P, g, x, y, z, 1.0, 0.45, 0.3, pants); box(P, g, x + 1.0, y, z, 0.9, 0.5, 0.36, shirt);
          box(P, g, x + 1.9, y + 0.05, z, 0.45, 0.4, 0.4, skin); box(P, g, x + 2.25, y + 0.05, z, 0.12, 0.4, 0.42, hair);
        } else if (o.pose === "sit") {
          box(P, g, x - 0.25, y, z, 0.25, 0.5, 0.5, pants); box(P, g, x, y, z + 0.5, 0.45, 0.5, 0.28, pants);
          box(P, g, x, y + 0.02, z + 0.78, 0.38, 0.46, 0.75, shirt); box(P, g, x + 0.02, y + 0.06, z + 1.53, 0.36, 0.36, 0.38, skin);
          box(P, g, x + 0.02, y + 0.06, z + 1.85, 0.36, 0.36, 0.1, hair);
        } else {
          box(P, g, x, y, z, 0.36, 0.42, 0.75, pants); box(P, g, x - 0.02, y - 0.02, z + 0.75, 0.4, 0.46, 0.75, shirt);
          box(P, g, x + 0.02, y + 0.03, z + 1.5, 0.34, 0.38, 0.38, skin); box(P, g, x + 0.02, y + 0.03, z + 1.82, 0.34, 0.38, 0.1, hair);
        }
        return g;
      }
      function sky(p, id, c1, c2) {
        const d = el("defs", {}, p), lg = el("linearGradient", { id, x1: 0, y1: 0, x2: 0, y2: 1 }, d);
        el("stop", { offset: 0, "stop-color": c1 }, lg); el("stop", { offset: 1, "stop-color": c2 }, lg);
        return el("rect", { x: 0, y: 0, width: 1080, height: 1920, fill: `url(#${id})` }, p);
      }
