// Stylised cinematic renderer for "Sternenfall". draw(t) paints one 1080x1920 frame.
const W = 1080, H = 1920;
let TL, CUE, SC, LINES, ctx, grain = [];

const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, x) => a + (b - a) * x;
const smooth = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const fract = x => x - Math.floor(x);
const rnd = (i, k = 0) => fract(Math.sin(i * 127.1 + k * 311.7 + 0.123) * 43758.5453);
const easeOut = x => 1 - Math.pow(1 - clamp(x), 3);
const easeInOut = x => smooth(0, 1, x);

// ---------- world data ----------
const STARS = [];
for (let i = 0; i < 520; i++) {
  STARS.push({ x: rnd(i, 1), y: Math.pow(rnd(i, 2), 1.25) * 0.8, s: 0.6 + Math.pow(rnd(i, 3), 6) * 4.5,
    ph: rnd(i, 4) * 6.28, sp: 0.6 + rnd(i, 5) * 2.5, hue: rnd(i, 6), off: rnd(i, 7) });
}
STARS[0] = { x: 0.5, y: 0.17, s: 4.5, ph: 0, sp: 0.8, hue: 0.1, off: 99, last: true };

const GLYPHS = [];
for (let g = 0; g < 48; g++) {
  const segs = [], n = 2 + Math.floor(rnd(g, 9) * 3);
  for (let k = 0; k < n; k++) {
    segs.push([rnd(g, k * 4) - 0.5, rnd(g, k * 4 + 1) - 0.5, rnd(g, k * 4 + 2) - 0.5, rnd(g, k * 4 + 3) - 0.5]);
  }
  GLYPHS.push(segs);
}

function buildings(seed, count, base, minH, maxH, spire) {
  const out = [];
  let x = -80;
  for (let i = 0; x < W + 200; i++) {
    const w = 50 + rnd(seed + i, 1) * 110, h = minH + Math.pow(rnd(seed + i, 2), 1.6) * (maxH - minH);
    const kind = rnd(seed + i, 3);
    const wins = [];
    for (let k = 0; k < Math.floor(h * w / 2600); k++) {
      wins.push([rnd(seed + i, 10 + k) * (w - 16) + 8, rnd(seed + i, 50 + k) * (h - 30) + 20, rnd(seed + i, 90 + k)]);
    }
    out.push({ x, w, h, kind: kind < spire ? 'spire' : kind < spire + 0.25 ? 'peak' : kind < spire + 0.35 ? 'dome' : 'flat', wins });
    x += w - 6 + rnd(seed + i, 4) * 20;
  }
  return { list: out, base };
}
const CITY = [buildings(100, 0, 1180, 120, 340, 0.12), buildings(300, 0, 1300, 90, 260, 0.08), buildings(500, 0, 1430, 60, 200, 0.05)];

// ---------- primitives ----------
function glow(x, y, r, color, a = 1) {
  const g = ctx.createRadialGradient(x, y, 0, x, y, r);
  g.addColorStop(0, color.replace('A', a));
  g.addColorStop(0.35, color.replace('A', a * 0.35));
  g.addColorStop(1, color.replace('A', 0));
  ctx.fillStyle = g;
  ctx.fillRect(x - r, y - r, 2 * r, 2 * r);
}

function vgrad(stops) {
  const g = ctx.createLinearGradient(0, 0, 0, H);
  stops.forEach(([o, c]) => g.addColorStop(o, c));
  ctx.fillStyle = g;
  ctx.fillRect(-200, -200, W + 400, H + 400);
}

function starAlpha(st, t) {
  let a = 0.55 + 0.45 * Math.sin(t * st.sp + st.ph);
  if (st.last) return 1;
  const out = CUE.erloeschen + st.off * 3.0;
  if (t > out) a *= clamp(1 - (t - out) / 0.25);
  return a;
}

function stars(t, o = {}) {
  const alpha = o.alpha ?? 1, yo = o.yo ?? 0, h = o.h ?? H, drift = o.drift ?? 0;
  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  for (const st of STARS) {
    if (st.last && o.noLast) continue;
    const a = starAlpha(st, t) * alpha;
    if (a <= 0.01) continue;
    const x = fract(st.x + drift * t * 0.002) * W, y = st.y * h + yo;
    const col = st.hue < 0.15 ? '255,210,170' : st.hue > 0.85 ? '170,200,255' : '235,240,255';
    ctx.fillStyle = `rgba(${col},${a})`;
    ctx.beginPath(); ctx.arc(x, y, st.s * (st.last ? 1 : 0.8), 0, 7); ctx.fill();
    if (st.s > 2.5) glow(x, y, st.s * 7, `rgba(${col},A)`, a * 0.35);
    // spark when a star dies
    const out = CUE.erloeschen + st.off * 3.0;
    if (!st.last && t > out && t < out + 0.5 && st.s > 1.2) glow(x, y, 30 * (1 - (t - out) / 0.5), 'rgba(200,120,255,A)', 0.6 * alpha);
  }
  ctx.restore();
}

function nebula(t, cols, alpha = 1) {
  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  cols.forEach((c, i) => {
    const x = W * (0.2 + 0.6 * rnd(i, 30)) + Math.sin(t * 0.05 + i) * 60;
    const y = H * (0.1 + 0.4 * rnd(i, 31)) + Math.cos(t * 0.04 + i) * 40;
    glow(x, y, 520 + 200 * rnd(i, 32), c, 0.22 * alpha);
  });
  ctx.restore();
}

function particles(t, n, o) {
  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) {
    const life = o.life ?? 8, tt = t + rnd(i, 40) * life, k = fract(tt / life);
    const x = (o.x0 ?? 0) + rnd(i, 41) * (o.w ?? W) + Math.sin(tt * 0.7 + i) * (o.sway ?? 30);
    const y = (o.y0 ?? H) + (o.dy ?? -H) * k;
    const a = Math.sin(k * Math.PI) * (o.a ?? 0.8) * (0.4 + 0.6 * rnd(i, 42));
    const r = (o.r ?? 2.5) * (0.5 + rnd(i, 43));
    ctx.fillStyle = (o.color ?? 'rgba(255,190,120,A)').replace('A', a);
    ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
    if (o.glowR) glow(x, y, o.glowR, o.color ?? 'rgba(255,190,120,A)', a * 0.25);
  }
  ctx.restore();
}

// Silhouette figure. (x,y) = feet, h = height in px. Returns hand position.
function figure(x, y, h, o = {}) {
  const s = h / 100, dir = o.dir ?? 1, wind = o.wind ?? 0;
  const t = o.t ?? 0;
  ctx.save();
  ctx.translate(x, y);
  if (o.rot) ctx.rotate(o.rot);
  ctx.scale(dir * s, s);
  if (o.rim) { ctx.shadowColor = o.rim; ctx.shadowBlur = o.rimBlur ?? 26; }
  ctx.fillStyle = o.color ?? '#05060b';
  const flap = Math.sin(t * 2.3) * 2 + wind;
  // body + cloak
  ctx.beginPath();
  ctx.moveTo(-3, -85);
  ctx.lineTo(-11, -80);
  ctx.bezierCurveTo(-15, -77, -15, -66, -13.5, -56);
  ctx.bezierCurveTo(-13, -40, -17 - flap * 0.5, -18, -24 - flap * 1.6, 0);
  ctx.lineTo(21 + flap * 0.4, 0);
  ctx.bezierCurveTo(16, -18, 12, -40, 11.5, -56);
  ctx.bezierCurveTo(11.5, -66, 13, -76, 10, -80);
  ctx.lineTo(3, -85);
  ctx.closePath(); ctx.fill();
  ctx.fillRect(-2.6, -90, 5.2, 7);
  // head
  ctx.beginPath(); ctx.ellipse(1.2, -92.5, 5.8, 7.2, 0.12, 0, 7); ctx.fill();
  if (o.hood) {
    ctx.beginPath();
    ctx.moveTo(-12, -80); ctx.bezierCurveTo(-12, -96, -6, -104, 2, -103);
    ctx.bezierCurveTo(9, -102, 11, -94, 10, -80); ctx.closePath(); ctx.fill();
  }
  if (o.hair) {
    ctx.beginPath();
    ctx.moveTo(3, -99);
    ctx.bezierCurveTo(-6, -102, -10, -94, -10, -86);
    ctx.bezierCurveTo(-12, -76, -15 - flap, -66, -18 - flap * 1.8, -56);
    ctx.lineTo(-11, -60);
    ctx.bezierCurveTo(-8, -70, -5, -80, -4, -88);
    ctx.closePath(); ctx.fill();
  }
  if (o.cape) {
    ctx.beginPath();
    ctx.moveTo(-8, -81); ctx.bezierCurveTo(-24 - flap, -60, -32 - flap * 2, -25, -38 - flap * 3, -2);
    ctx.lineTo(-18, -1); ctx.closePath(); ctx.fill();
  }
  // arm
  let hand = null;
  if (o.arm !== undefined) {
    const a = o.arm, sx = 6, sy = -77, len = o.armLen ?? 34;
    const ex = sx + Math.cos(a + 0.3) * len * 0.5, ey = sy + Math.sin(a + 0.3) * len * 0.5;
    const hx = ex + Math.cos(a - 0.2) * len * 0.5, hy = ey + Math.sin(a - 0.2) * len * 0.5;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = ctx.fillStyle; ctx.lineWidth = 5.2;
    ctx.beginPath(); ctx.moveTo(sx - 2, sy + 1); ctx.lineTo(ex, ey); ctx.lineTo(hx, hy); ctx.stroke();
    hand = [x + dir * hx * s, y + hy * s];
    if (o.sword !== undefined) {
      const b = o.sword;
      ctx.shadowBlur = 0;
      ctx.lineWidth = 2.6; ctx.strokeStyle = o.blade ?? '#c9d4e6';
      ctx.beginPath(); ctx.moveTo(hx, hy); ctx.lineTo(hx + Math.cos(b) * 62, hy + Math.sin(b) * 62); ctx.stroke();
      ctx.lineWidth = 3; ctx.strokeStyle = '#05060b';
      ctx.beginPath(); ctx.moveTo(hx - Math.sin(b) * 6, hy + Math.cos(b) * 6); ctx.lineTo(hx + Math.sin(b) * 6, hy - Math.cos(b) * 6); ctx.stroke();
    }
    if (o.staff) {
      ctx.lineWidth = 2.8; ctx.strokeStyle = '#05060b';
      ctx.beginPath(); ctx.moveTo(hx, hy + 30); ctx.lineTo(hx + 2, hy - 38); ctx.stroke();
      hand = [x + dir * (hx + 2) * s, y + (hy - 40) * s];
    }
  }
  ctx.restore();
  return hand;
}

function ground(y, color, rough = 18, seed = 1) {
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.moveTo(-200, H + 200); ctx.lineTo(-200, y);
  for (let x = -200; x <= W + 200; x += 40) ctx.lineTo(x, y + (rnd(seed, x) - 0.5) * rough + Math.sin(x * 0.004 + seed) * rough * 2);
  ctx.lineTo(W + 200, H + 200); ctx.closePath(); ctx.fill();
}

function city(t, o = {}) {
  const tints = o.tints ?? ['#1a2142', '#0f1430', '#070914'];
  CITY.forEach((layer, li) => {
    const par = (o.pan ?? 0) * (0.3 + li * 0.35);
    ctx.fillStyle = tints[li];
    for (const b of layer.list) {
      const x = b.x - par, top = layer.base - b.h;
      ctx.beginPath();
      ctx.moveTo(x, layer.base + 400); ctx.lineTo(x, top);
      if (b.kind === 'peak') ctx.lineTo(x + b.w / 2, top - b.w * 0.45);
      if (b.kind === 'spire') { ctx.lineTo(x + b.w * 0.4, top); ctx.lineTo(x + b.w / 2, top - b.h * 0.9); ctx.lineTo(x + b.w * 0.6, top); }
      if (b.kind === 'dome') ctx.arc(x + b.w / 2, top, b.w / 2, Math.PI, 0);
      ctx.lineTo(x + b.w, top); ctx.lineTo(x + b.w, layer.base + 400); ctx.closePath(); ctx.fill();
    }
    // lantern-lit windows
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (const b of layer.list) {
      const x = b.x - par, top = layer.base - b.h;
      for (const [wx, wy, r] of b.wins) {
        if (r > (o.lit ?? 0.55)) continue;
        const a = (0.55 + 0.45 * Math.sin(t * (1 + r * 3) + r * 40)) * (o.winA ?? 1) * (0.4 + li * 0.3);
        ctx.fillStyle = `rgba(255,${170 + r * 60},${90 + r * 40},${a})`;
        ctx.fillRect(x + wx, top + wy, 3 + li * 1.5, 4 + li * 2);
      }
    }
    ctx.restore();
  });
}

function upperCity(t, a = 1) {
  // the city of the mages on the hill, glowing violet spires
  ctx.fillStyle = '#121633';
  ctx.beginPath(); ctx.moveTo(380, 1200); ctx.bezierCurveTo(480, 980, 760, 960, 980, 1200); ctx.closePath(); ctx.fill();
  const sp = [[520, 330], [600, 470], [660, 400], [720, 560], [790, 420], [860, 300]];
  for (const [x, h] of sp) {
    const y = 1080 - Math.abs(x - 700) * 0.25;
    ctx.fillStyle = '#141838';
    ctx.beginPath(); ctx.moveTo(x - 16, y + 60); ctx.lineTo(x - 10, y - h + 60); ctx.lineTo(x, y - h - 20); ctx.lineTo(x + 10, y - h + 60); ctx.lineTo(x + 16, y + 60); ctx.closePath(); ctx.fill();
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(x, y - h - 20, 60 + 15 * Math.sin(t * 2 + x), 'rgba(160,110,255,A)', 0.7 * a);
    ctx.restore();
  }
}

function moon(x, y, r, a = 1) {
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  glow(x, y, r * 4, 'rgba(150,170,255,A)', 0.35 * a);
  ctx.restore();
  const g = ctx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r);
  g.addColorStop(0, `rgba(245,240,230,${a})`); g.addColorStop(1, `rgba(190,195,215,${a})`);
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
  ctx.fillStyle = `rgba(150,150,175,${0.25 * a})`;
  [[-0.3, -0.2, 0.18], [0.25, 0.1, 0.22], [-0.05, 0.4, 0.12], [0.35, -0.35, 0.1]].forEach(([dx, dy, rr]) => {
    ctx.beginPath(); ctx.arc(x + dx * r, y + dy * r, rr * r, 0, 7); ctx.fill();
  });
}

function heart(x, y, r, t, o = {}) {
  const pulse = o.pulse ?? 0, col = o.col ?? '200,225,255', dark = o.dark ?? 0;
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  glow(x, y, r * (9 + pulse * 5), `rgba(${col},A)`, 0.45 + pulse * 0.3);
  // rays
  for (let i = 0; i < 12; i++) {
    const a = i / 12 * 6.283 + t * 0.15 * (i % 2 ? 1 : -1), L = r * (5 + 3 * Math.sin(t * 1.3 + i * 2) + pulse * 6);
    const g = ctx.createLinearGradient(x, y, x + Math.cos(a) * L, y + Math.sin(a) * L);
    g.addColorStop(0, `rgba(${col},${0.35 + pulse * 0.3})`); g.addColorStop(1, `rgba(${col},0)`);
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.moveTo(x + Math.cos(a + 1.57) * r * 0.25, y + Math.sin(a + 1.57) * r * 0.25);
    ctx.lineTo(x + Math.cos(a) * L, y + Math.sin(a) * L);
    ctx.lineTo(x + Math.cos(a - 1.57) * r * 0.25, y + Math.sin(a - 1.57) * r * 0.25); ctx.fill();
  }
  ctx.restore();
  // crystal
  ctx.save(); ctx.translate(x, y); ctx.rotate(t * 0.4);
  ctx.fillStyle = dark > 0.5 ? '#1a0630' : `rgba(240,248,255,1)`;
  ctx.beginPath();
  for (let i = 0; i < 16; i++) { const a = i / 16 * 6.283, rr = i % 2 ? r * 0.45 : r; ctx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr * 1.25); }
  ctx.closePath(); ctx.fill();
  if (dark > 0) { ctx.strokeStyle = `rgba(190,120,255,${dark})`; ctx.lineWidth = 3; ctx.stroke(); }
  ctx.restore();
}

function lightning(x0, y0, x1, y1, seed, width, color) {
  const pts = [[x0, y0], [x1, y1]];
  for (let it = 0; it < 6; it++) {
    for (let i = pts.length - 1; i > 0; i--) {
      const [ax, ay] = pts[i - 1], [bx, by] = pts[i], d = Math.hypot(bx - ax, by - ay);
      const k = (rnd(seed + i * 7, it) - 0.5) * d * 0.45;
      pts.splice(i, 0, [(ax + bx) / 2 + (ay - by) / d * k, (ay + by) / 2 + (bx - ax) / d * k]);
    }
  }
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.lineJoin = 'round';
  [[width * 6, 0.15], [width * 2.5, 0.4], [width, 1]].forEach(([w, a]) => {
    ctx.strokeStyle = color.replace('A', a); ctx.lineWidth = w;
    ctx.beginPath(); pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.stroke();
  });
  ctx.restore();
}

function runeRing(x, y, r, t, a, color, n = 24, dir = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  ctx.strokeStyle = color.replace('A', a); ctx.lineWidth = 2.5; ctx.shadowColor = color.replace('A', 1); ctx.shadowBlur = 14;
  ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.stroke();
  ctx.beginPath(); ctx.arc(x, y, r * 0.86, 0, 7); ctx.stroke();
  for (let i = 0; i < n; i++) {
    const ang = i / n * 6.283 + t * 0.25 * dir;
    ctx.save(); ctx.translate(x + Math.cos(ang) * r * 0.93, y + Math.sin(ang) * r * 0.93); ctx.rotate(ang + 1.57);
    const sz = r * 0.07;
    ctx.beginPath();
    for (const [a1, b1, a2, b2] of GLYPHS[(i * 7 + n) % GLYPHS.length]) { ctx.moveTo(a1 * sz, b1 * sz); ctx.lineTo(a2 * sz, b2 * sz); }
    ctx.stroke(); ctx.restore();
  }
  ctx.restore();
}

function ruins(t, o = {}) {
  const c = o.color ?? '#070812';
  ctx.fillStyle = c;
  // columns
  [[120, 760, 70], [300, 900, 60], [780, 820, 64], [960, 700, 76]].forEach(([x, h, w], i) => {
    const base = 1500;
    ctx.beginPath(); ctx.moveTo(x - w / 2, base); ctx.lineTo(x - w / 2, base - h);
    for (let k = 0; k <= 6; k++) ctx.lineTo(x - w / 2 + w * k / 6, base - h - rnd(i, k) * 50);
    ctx.lineTo(x + w / 2, base); ctx.fill();
    ctx.fillRect(x - w / 2 - 14, base - 30, w + 28, 30);
  });
  // broken arch
  ctx.lineWidth = 58; ctx.strokeStyle = c;
  ctx.beginPath(); ctx.arc(540, 820, 300, Math.PI * 1.02, Math.PI * 1.58); ctx.stroke();
  ctx.beginPath(); ctx.arc(540, 820, 300, Math.PI * 1.72, Math.PI * 1.98); ctx.stroke();
  ctx.lineWidth = 1;
  ground(1480, c, 26, 7);
  // rubble
  for (let i = 0; i < 14; i++) {
    const x = rnd(i, 60) * W, s = 20 + rnd(i, 61) * 50;
    ctx.save(); ctx.translate(x, 1500 + rnd(i, 62) * 120); ctx.rotate(rnd(i, 63));
    ctx.fillRect(-s / 2, -s / 2, s, s * 0.7); ctx.restore();
  }
}

function titleText(x, y, size, a, z = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(z, z);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  if (ctx.letterSpacing !== undefined) ctx.letterSpacing = Math.round(size / 11) + 'px';
  ctx.font = `700 ${size}px Cinzel`;
  const g = ctx.createLinearGradient(0, -size * 0.55, 0, size * 0.55);
  g.addColorStop(0, `rgba(255,240,200,${a})`); g.addColorStop(0.5, `rgba(228,178,92,${a})`); g.addColorStop(1, `rgba(150,96,40,${a})`);
  ctx.shadowColor = `rgba(255,170,80,${a * 0.85})`; ctx.shadowBlur = 45;
  ctx.fillStyle = g; ctx.fillText('STERNENFALL', 0, 0);
  ctx.restore();
}

function emblem(x, y, r, t, prog, a) {
  if (a <= 0 || prog <= 0) return;
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  ctx.strokeStyle = `rgba(255,205,130,${a})`; ctx.shadowColor = 'rgba(255,170,80,1)'; ctx.shadowBlur = 18; ctx.lineWidth = 3;
  const start = -Math.PI / 2;
  ctx.beginPath(); ctx.arc(x, y, r, start, start + prog * 6.2832); ctx.stroke();
  ctx.beginPath(); ctx.arc(x, y, r * 0.84, start + 3.14, start + 3.14 - prog * 6.2832, true); ctx.stroke();
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.arc(x, y, r * 1.08, start, start + prog * 6.2832); ctx.stroke();
  ctx.restore();
  runeRing(x, y, r * 0.92, t, a * smooth(0.3, 1, prog) * 0.8, 'rgba(255,215,150,A)', 30, 1);
  // eight-pointed star
  const sp = smooth(0.5, 1, prog);
  if (sp > 0) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(t * 0.1);
    ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = `rgba(255,215,150,${a * sp})`; ctx.lineWidth = 2.5;
    ctx.shadowColor = 'rgba(255,170,80,1)'; ctx.shadowBlur = 16;
    ctx.beginPath();
    for (let i = 0; i <= 16; i++) { const ang = i / 16 * 6.2832, rr = (i % 2 ? 0.28 : 0.72) * r * sp; ctx.lineTo(Math.cos(ang) * rr, Math.sin(ang) * rr); }
    ctx.stroke();
    ctx.restore();
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(x, y, r * 0.5, 'rgba(255,220,170,A)', 0.4 * a * sp); ctx.restore();
  }
}

function aurora(t, a) {
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  [['80,255,200', 380, 0.9], ['150,110,255', 520, 0.7], ['255,120,200', 640, 0.5]].forEach(([c, base, f], k) => {
    const g = ctx.createLinearGradient(0, base - 160, 0, base + 220);
    g.addColorStop(0, `rgba(${c},0)`); g.addColorStop(0.4, `rgba(${c},${0.22 * a})`); g.addColorStop(1, `rgba(${c},0)`);
    ctx.fillStyle = g;
    ctx.beginPath();
    for (let x = -100; x <= W + 100; x += 30) ctx.lineTo(x, base + Math.sin(x * 0.006 * f + t * 0.4 + k) * 90 + Math.sin(x * 0.017 + t * 0.7) * 25);
    for (let x = W + 100; x >= -100; x -= 30) ctx.lineTo(x, base + 260 + Math.sin(x * 0.005 + t * 0.3 + k * 2) * 60);
    ctx.fill();
  });
  ctx.restore();
}

function pinkMoon(x, y, r) {
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(x, y, r * 4, 'rgba(255,150,190,A)', 0.3); ctx.restore();
  const g = ctx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r);
  g.addColorStop(0, '#ffe2ee'); g.addColorStop(1, '#d98aab');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
}

function island(x, y, w, t, seed, depth) {
  y += Math.sin(t * 0.5 + seed) * 12 * depth;
  const dark = `rgb(${Math.round(lerp(70, 12, depth))},${Math.round(lerp(50, 14, depth))},${Math.round(lerp(110, 34, depth))})`;
  // waterfall
  const wx = x + w * (0.25 - 0.5 * rnd(seed, 1)), ww = w * 0.07;
  const g = ctx.createLinearGradient(0, y, 0, y + w * 2.2);
  g.addColorStop(0, `rgba(190,225,255,${0.75 * depth})`); g.addColorStop(1, 'rgba(190,225,255,0)');
  ctx.fillStyle = g; ctx.fillRect(wx - ww / 2, y, ww, w * 2.2);
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = `rgba(230,245,255,${0.35 * depth})`; ctx.lineWidth = 2;
  for (let k = 0; k < 4; k++) { const yy = y + fract(t * 0.6 + k / 4) * w * 1.8; ctx.beginPath(); ctx.moveTo(wx - ww * 0.4, yy); ctx.lineTo(wx + ww * 0.4, yy + 14); ctx.stroke(); }
  glow(wx, y + w * 1.6, w * 0.5, 'rgba(200,220,255,A)', 0.25 * depth);
  ctx.restore();
  // rock
  ctx.fillStyle = dark;
  ctx.beginPath(); ctx.moveTo(x - w / 2, y);
  for (let k = 0; k <= 8; k++) { const u = k / 8; ctx.lineTo(x - w / 2 + w * u, y + Math.sin(u * Math.PI) * w * (0.75 + 0.3 * rnd(seed, k)) + (rnd(seed, k + 9) - 0.5) * w * 0.12); }
  ctx.lineTo(x + w / 2, y); ctx.closePath(); ctx.fill();
  // grass top
  ctx.fillStyle = `rgb(${Math.round(lerp(60, 10, depth))},${Math.round(lerp(90, 30, depth))},${Math.round(lerp(120, 46, depth))})`;
  ctx.beginPath(); ctx.ellipse(x, y, w / 2, w * 0.07, 0, 0, 7); ctx.fill();
  // glowing trees
  for (let k = 0; k < 4; k++) {
    const tx = x - w * 0.35 + w * 0.7 * rnd(seed, 20 + k), th = w * (0.12 + 0.15 * rnd(seed, 30 + k));
    ctx.fillStyle = dark; ctx.fillRect(tx - 2, y - th, 4, th);
    ctx.beginPath(); ctx.arc(tx, y - th, th * 0.45, 0, 7); ctx.fill();
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(tx, y - th, th * 0.9, k % 2 ? 'rgba(120,255,210,A)' : 'rgba(255,190,240,A)', 0.35 * (0.7 + 0.3 * Math.sin(t * 2 + k + seed)));
    ctx.restore();
  }
}

function whale(x, y, s, t, depth, dir = 1) {
  y += Math.sin(t * 0.6 + x * 0.002) * 20;
  ctx.save(); ctx.translate(x, y); ctx.scale(dir * s, s); ctx.rotate(Math.sin(t * 0.6) * 0.04);
  ctx.fillStyle = `rgba(${Math.round(lerp(60, 10, depth))},${Math.round(lerp(60, 16, depth))},${Math.round(lerp(120, 44, depth))},1)`;
  ctx.shadowColor = 'rgba(140,200,255,0.6)'; ctx.shadowBlur = 25;
  const tail = Math.sin(t * 1.4) * 18;
  ctx.beginPath();
  ctx.moveTo(220, 0); ctx.bezierCurveTo(200, -70, 40, -95, -80, -55);
  ctx.bezierCurveTo(-160, -30, -220, -10, -270, tail * 0.5);
  ctx.lineTo(-330, -50 + tail); ctx.lineTo(-310, tail * 0.6); ctx.lineTo(-335, 45 + tail); ctx.lineTo(-268, 10 + tail * 0.5);
  ctx.bezierCurveTo(-200, 30, -80, 70, 40, 60); ctx.bezierCurveTo(140, 55, 215, 35, 220, 0); ctx.fill();
  ctx.beginPath(); ctx.moveTo(40, 40); ctx.quadraticCurveTo(10, 120 + tail, -40, 130 + tail); ctx.quadraticCurveTo(-10, 80, 0, 45); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.globalCompositeOperation = 'lighter';
  for (let k = 0; k < 12; k++) {
    const u = k / 11, px = lerp(180, -250, u), py = lerp(-30, -5, u) + Math.sin(u * 3) * -20;
    glow(px, py, 12, 'rgba(140,230,255,A)', 0.7 * (0.6 + 0.4 * Math.sin(t * 3 + k)));
  }
  glow(150, -10, 7, 'rgba(220,250,255,A)', 0.9);
  ctx.restore();
}

function clouds(t, y, a) {
  ctx.save();
  for (let k = 0; k < 9; k++) {
    const x = fract(rnd(k, 50) + t * 0.004 * (1 + rnd(k, 51))) * (W + 600) - 300, r = 260 + 160 * rnd(k, 52);
    const g = ctx.createRadialGradient(x, y + 60 * rnd(k, 53), 0, x, y + 60 * rnd(k, 53), r);
    g.addColorStop(0, `rgba(235,200,235,${0.28 * a})`); g.addColorStop(1, 'rgba(235,200,235,0)');
    ctx.fillStyle = g; ctx.fillRect(x - r, y - r, 2 * r, 2 * r);
  }
  ctx.restore();
}

const CAPTIONS = [
  { scene: 'welt', at: 0.8, dur: 6, title: 'VALDORIA', sub: 'Die Welt über den Wolken' },
  { scene: 'stadt', at: 0.6, dur: 7, title: 'AURELION', sub: 'Die Stadt der tausend Laternen · Jahr 1137 nach dem Sternenbund' },
  { scene: 'lichtkrone', at: 0.5, dur: 6, title: 'DIE LICHTKRONE', sub: 'Sitz des Ordens der Hohen Flamme' },
  { scene: 'seraphine_vor', at: 0.5, dur: 6, title: 'SERAPHINE', sub: 'Hohepriesterin des Ordens der Hohen Flamme' },
  { scene: 'lunara', at: 0.6, dur: 6.5, title: 'LUNARA', sub: '17 · Laternenanzünderin der Tiefen Äste' },
  { scene: 'kael_vor', at: 0.6, dur: 6, title: 'KAEL', sub: '21 · Lunaras Bruder · Hauptmann der Flammenwache' },
  { scene: 'ruinen', at: 0.5, dur: 6, title: 'DIE VERBOTENEN RUINEN', sub: 'Tempel der Ersten Sterne · Ursprung des großen Feuers' },
];

function captions(t) {
  for (const c of CAPTIONS) {
    const t0 = SC[c.scene].start + c.at, a = smooth(t0, t0 + 0.8, t) * (1 - smooth(t0 + c.dur - 0.8, t0 + c.dur, t));
    if (a <= 0) continue;
    ctx.save();
    const bg = ctx.createRadialGradient(540, 330, 40, 540, 330, 520);
    bg.addColorStop(0, `rgba(0,0,0,${0.55 * a})`); bg.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, 800);
    ctx.textAlign = 'center'; ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 14;
    const lw = 360 * easeOut((t - t0) / 1.2);
    ctx.fillStyle = `rgba(230,190,120,${a})`; ctx.fillRect(540 - lw, 236, lw * 2, 2);
    if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '12px';
    ctx.font = '700 58px Cinzel'; ctx.fillStyle = `rgba(255,232,190,${a})`; ctx.fillText(c.title, 540, 316);
    if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '1px';
    ctx.font = 'italic 600 40px "Cormorant Garamond"'; ctx.fillStyle = `rgba(240,230,215,${a})`;
    wrap(c.sub, 900).forEach((line, i) => ctx.fillText(line, 540, 380 + i * 46));
    ctx.fillStyle = `rgba(230,190,120,${a})`; ctx.fillRect(540 - lw, 380 + 46 * (wrap(c.sub, 900).length - 1) + 30, lw * 2, 2);
    ctx.restore();
  }
}

function treeColor(depth) {
  return `rgb(${Math.round(lerp(70, 7, depth))},${Math.round(lerp(55, 9, depth))},${Math.round(lerp(105, 24, depth))})`;
}

function giantTree(x, w, top, t, depth, seed, o = {}) {
  const c = o.color ?? treeColor(depth);
  ctx.fillStyle = c; ctx.strokeStyle = c; ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(x - w * 0.62, H + 400);
  ctx.bezierCurveTo(x - w * 0.5, top + (H - top) * 0.6, x - w * 0.42, top + 200, x - w * 0.3, top + 60);
  ctx.lineTo(x + w * 0.3, top + 60);
  ctx.bezierCurveTo(x + w * 0.42, top + 200, x + w * 0.5, top + (H - top) * 0.6, x + w * 0.62, H + 400);
  ctx.closePath(); ctx.fill();
  for (let k = 0; k < (o.branches ?? 4); k++) {
    const by = top + 140 + k * (o.branchGap ?? 170), side = (k + seed) % 2 ? 1 : -1, L = w * (1.1 + rnd(seed, k) * 0.9);
    ctx.lineWidth = w * 0.13 * (1 - k * 0.12);
    ctx.beginPath(); ctx.moveTo(x + side * w * 0.3, by + 40);
    ctx.quadraticCurveTo(x + side * L * 0.6, by - 10, x + side * L, by - 50 - 40 * rnd(seed, k + 5)); ctx.stroke();
    for (let j = 0; j < 5; j++) {
      ctx.beginPath();
      ctx.arc(x + side * L + (rnd(seed, k * 9 + j) - 0.5) * w * 0.7, by - 60 + (rnd(seed, k * 9 + j + 50) - 0.5) * w * 0.3, w * (0.16 + 0.12 * rnd(seed, k * 9 + j + 90)), 0, 7);
      ctx.fill();
    }
  }
  ctx.save();
  ctx.shadowColor = o.rim ?? 'rgba(170,150,255,0.55)'; ctx.shadowBlur = 18;
  for (let j = 0; j < 22; j++) {
    const a = rnd(seed, 200 + j) * Math.PI, r = w * (0.3 + 0.9 * rnd(seed, 220 + j));
    ctx.beginPath();
    ctx.arc(x + Math.cos(a) * r * 1.25, top - Math.sin(a) * r * 0.5, w * (0.22 + 0.2 * rnd(seed, 260 + j)), 0, 7); ctx.fill();
  }
  ctx.restore();
  if (o.lights) {
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (let j = 0; j < o.lights; j++) {
      const lx = x + (rnd(seed, 300 + j) - 0.5) * w * (o.lightW ?? 2.4), ly = top - 60 + rnd(seed, 320 + j) * (o.lightSpan ?? 500);
      const fl = 0.6 + 0.4 * Math.sin(t * (1 + rnd(seed, 340 + j) * 3) + j);
      glow(lx, ly, 10 + 14 * depth, 'rgba(255,190,110,A)', fl * 0.9 * (o.lightA ?? 1));
    }
    ctx.restore();
  }
}

function cloudSea(t, y, a = 1) {
  const g = ctx.createLinearGradient(0, y - 120, 0, H + 200);
  g.addColorStop(0, 'rgba(200,170,220,0)'); g.addColorStop(0.25, `rgba(190,160,215,${0.75 * a})`); g.addColorStop(1, `rgba(120,95,160,${a})`);
  ctx.fillStyle = g; ctx.fillRect(-300, y - 120, W + 600, H - y + 600);
  clouds(t, y, a); clouds(t + 40, y + 180, a);
}

function house(x, y, w, h, t, seed, lit = true) {
  ctx.fillRect(x - w / 2, y - h, w, h);
  ctx.beginPath(); ctx.moveTo(x - w / 2 - 6, y - h); ctx.lineTo(x, y - h - w * 0.55); ctx.lineTo(x + w / 2 + 6, y - h); ctx.fill();
  if (!lit) return;
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  const fl = 0.75 + 0.25 * Math.sin(t * 2 + seed * 7);
  ctx.fillStyle = `rgba(255,${180 + 40 * rnd(seed, 1)},110,${fl})`;
  ctx.fillRect(x - w * 0.2, y - h * 0.65, w * 0.16, h * 0.28);
  if (w > 50) ctx.fillRect(x + w * 0.08, y - h * 0.65, w * 0.16, h * 0.28);
  glow(x, y - h * 0.5, w * 0.9, 'rgba(255,170,90,A)', 0.25 * fl);
  ctx.restore();
}

function platform(x, y, w, t, seed, color) {
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.ellipse(x, y, w / 2, w * 0.07, 0, 0, 7); ctx.fill();
  ctx.fillRect(x - w / 2, y - 4, w, 14);
  const n = Math.max(2, Math.floor(w / 90));
  for (let k = 0; k < n; k++) {
    const hx = x - w / 2 + (k + 0.5) * w / n + (rnd(seed, k) - 0.5) * 20;
    if (Math.abs(hx - x) < w * 0.16) continue;
    ctx.fillStyle = color;
    house(hx, y, 44 + 30 * rnd(seed, k + 3), 40 + 34 * rnd(seed, k + 6), t, seed * 10 + k);
  }
}

function bridge(x1, y1, x2, y2, sag, t, seed, color, lanterns = 5) {
  ctx.strokeStyle = color; ctx.lineWidth = 3;
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 + sag;
  [0, -26].forEach(off => { ctx.beginPath(); ctx.moveTo(x1, y1 + off); ctx.quadraticCurveTo(mx, my + off, x2, y2 + off); ctx.stroke(); });
  ctx.lineWidth = 2;
  for (let k = 1; k < 24; k++) {
    const u = k / 24, bx = (1 - u) * (1 - u) * x1 + 2 * (1 - u) * u * mx + u * u * x2, by = (1 - u) * (1 - u) * y1 + 2 * (1 - u) * u * my + u * u * y2;
    ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(bx, by - 26); ctx.stroke();
  }
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  for (let k = 1; k <= lanterns; k++) {
    const u = k / (lanterns + 1), bx = (1 - u) * (1 - u) * x1 + 2 * (1 - u) * u * mx + u * u * x2, by = (1 - u) * (1 - u) * y1 + 2 * (1 - u) * u * my + u * u * y2;
    const fl = 0.75 + 0.25 * Math.sin(t * 7 + k * 3 + seed);
    glow(bx, by + 18, 46 * fl, 'rgba(255,170,80,A)', 0.8); glow(bx, by + 18, 8, 'rgba(255,235,190,A)', 1);
  }
  ctx.restore();
}

function flame(x, y, h, t, a = 1, col = ['255,120,40', '255,200,90', '255,250,220']) {
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  glow(x, y - h * 0.4, h * 1.6, `rgba(${col[0]},A)`, 0.5 * a);
  col.forEach((c, k) => {
    const s = 1 - k * 0.3;
    ctx.fillStyle = `rgba(${c},${0.75 * a})`;
    ctx.beginPath();
    const sway = Math.sin(t * 7 + k) * h * 0.06, sway2 = Math.sin(t * 11 + k * 2) * h * 0.04;
    ctx.moveTo(x - h * 0.28 * s, y);
    ctx.bezierCurveTo(x - h * 0.35 * s, y - h * 0.5 * s, x + sway - h * 0.1, y - h * 0.7 * s, x + sway + sway2, y - h * s);
    ctx.bezierCurveTo(x + sway + h * 0.12, y - h * 0.7 * s, x + h * 0.35 * s, y - h * 0.5 * s, x + h * 0.28 * s, y);
    ctx.closePath(); ctx.fill();
  });
  ctx.restore();
}

function palace(x, y, s, t, o = {}) {
  // the Light Crown: white-gold temple spires on top of the world tree, eternal flame, star beams
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const c = o.color ?? '#1a1630';
  ctx.fillStyle = c;
  ctx.beginPath(); ctx.ellipse(0, 0, 420, 60, 0, 0, 7); ctx.fill();
  [[-330, 260], [-240, 380], [-130, 300], [130, 300], [240, 380], [330, 260]].forEach(([px, h]) => {
    ctx.beginPath(); ctx.moveTo(px - 26, 0); ctx.lineTo(px - 20, -h); ctx.lineTo(px, -h - 70); ctx.lineTo(px + 20, -h); ctx.lineTo(px + 26, 0); ctx.fill();
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    ctx.fillStyle = 'rgba(255,215,150,0.5)'; ctx.fillRect(px - 2, -h + 20, 4, h - 40);
    glow(px, -h - 70, 40, 'rgba(255,220,160,A)', 0.8);
    ctx.restore();
  });
  ctx.fillStyle = c;
  ctx.beginPath(); ctx.arc(0, -40, 130, Math.PI, 0); ctx.fill();
  ctx.fillRect(-150, -40, 300, 40);
  ctx.restore();
  // star beams converging into the crystal above the flame
  const cx = x, cy = y - 360 * s;
  if (o.beams !== false) {
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (let k = 0; k < 9; k++) {
      const sx = (rnd(k, 500) * 1.4 - 0.2) * W, sy = -100 + rnd(k, 501) * 300;
      const g = ctx.createLinearGradient(sx, sy, cx, cy);
      g.addColorStop(0, 'rgba(200,220,255,0)'); g.addColorStop(1, `rgba(220,235,255,${0.35 * (0.6 + 0.4 * Math.sin(t * 2 + k))})`);
      ctx.strokeStyle = g; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(cx, cy); ctx.stroke();
    }
    glow(cx, cy, 90 * s, 'rgba(220,235,255,A)', 0.9);
    ctx.restore();
  }
  flame(x, y - 160 * s, 170 * s * (o.flare ?? 1), t, 1);
}

function bellTower(x, y, s, t, strikes, side) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = '#0d0a16';
  ctx.fillRect(-90, -520, 180, 560);
  ctx.beginPath(); ctx.moveTo(-110, -520); ctx.lineTo(0, -700); ctx.lineTo(110, -520); ctx.fill();
  ctx.fillStyle = '#2a0c10'; ctx.fillRect(-62, -480, 124, 200);
  // bell swings after each strike
  let last = -99;
  for (const st of strikes) if (t >= st) last = st;
  const since = t - last, ang = since < 3 ? Math.sin(since * 4.2) * 0.5 * Math.exp(-since * 0.8) * side : 0;
  ctx.save(); ctx.translate(0, -470); ctx.rotate(ang);
  ctx.fillStyle = '#c9a25a'; ctx.shadowColor = 'rgba(255,120,60,0.9)'; ctx.shadowBlur = 30;
  ctx.beginPath(); ctx.moveTo(-14, 10); ctx.bezierCurveTo(-30, 40, -34, 110, -58, 150); ctx.lineTo(58, 150); ctx.bezierCurveTo(34, 110, 30, 40, 14, 10); ctx.closePath(); ctx.fill();
  ctx.restore();
  // sound rings
  if (since < 1.6) {
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (let k = 0; k < 3; k++) {
      const r = (since - k * 0.18) * 520;
      if (r <= 0) continue;
      ctx.strokeStyle = `rgba(255,140,90,${clamp(1 - since / 1.6) * 0.6})`; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.arc(0, -380, r, 0, 7); ctx.stroke();
    }
    ctx.restore();
  }
  ctx.restore();
}

function pendant(x, y, r, t, o = {}) {
  const tremble = o.tremble ?? 0;
  ctx.save(); ctx.translate(x + Math.sin(t * 50) * tremble * 3, y);
  ctx.strokeStyle = '#b8934e'; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.moveTo(0, -r); ctx.lineTo(-r * 0.5, -r * 3); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0, -r); ctx.lineTo(r * 0.5, -r * 3); ctx.stroke();
  const g = ctx.createRadialGradient(-r * 0.3, -r * 0.3, r * 0.1, 0, 0, r);
  g.addColorStop(0, '#2a2650'); g.addColorStop(1, '#0c0a1e');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.fill();
  ctx.lineWidth = r * 0.09; ctx.strokeStyle = '#d7b169'; ctx.shadowColor = 'rgba(255,200,120,0.8)'; ctx.shadowBlur = 20;
  ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.stroke();
  ctx.shadowBlur = 0; ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(215,177,105,0.6)';
  ctx.beginPath(); ctx.arc(0, 0, r * 0.78, 0, 7); ctx.stroke();
  ctx.fillStyle = 'rgba(255,240,210,0.7)';
  for (let k = 0; k < 14; k++) { ctx.beginPath(); ctx.arc((rnd(k, 600) - 0.5) * r * 1.3, (rnd(k, 601) - 0.5) * r * 1.3, 1.5 + rnd(k, 602) * 2, 0, 7); ctx.fill(); }
  const ang = (o.angle ?? -0.9) + tremble * 0.25 * Math.sin(t * 37) + tremble * 0.15 * Math.sin(t * 23);
  ctx.rotate(ang + Math.PI / 2);
  ctx.fillStyle = '#ffe0a0'; ctx.shadowColor = 'rgba(255,210,140,1)'; ctx.shadowBlur = 24;
  ctx.beginPath(); ctx.moveTo(0, -r * 0.7); ctx.lineTo(r * 0.08, 0); ctx.lineTo(0, r * 0.35); ctx.lineTo(-r * 0.08, 0); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.arc(0, 0, r * 0.07, 0, 7); ctx.fill();
  ctx.restore();
}

function stoneTree(x, base, h, seed, c) {
  ctx.fillStyle = c; ctx.strokeStyle = c; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x - h * 0.08, base); ctx.lineTo(x - h * 0.04, base - h); ctx.lineTo(x + h * 0.03, base - h * 1.02); ctx.lineTo(x + h * 0.08, base); ctx.fill();
  for (let k = 0; k < 4; k++) {
    const by = base - h * (0.45 + k * 0.14), side = (k + seed) % 2 ? 1 : -1, L = h * (0.25 + 0.2 * rnd(seed, k));
    ctx.lineWidth = h * 0.025;
    ctx.beginPath(); ctx.moveTo(x, by); ctx.lineTo(x + side * L, by - L * 0.6); ctx.lineTo(x + side * L * 1.2, by - L * 0.5); ctx.stroke();
  }
}

function whaleBones(x, y, s, c) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.strokeStyle = c; ctx.lineCap = 'round'; ctx.lineWidth = 10;
  ctx.beginPath(); ctx.moveTo(-260, -20); ctx.quadraticCurveTo(0, -60, 240, -10); ctx.stroke();
  for (let k = 0; k < 9; k++) {
    const px = -200 + k * 50, py = -40 + Math.abs(k - 4) * 3;
    ctx.lineWidth = 7;
    ctx.beginPath(); ctx.moveTo(px, py); ctx.quadraticCurveTo(px + 30, py - 120 + k * 4, px + 70, py - 10); ctx.stroke();
  }
  ctx.lineWidth = 14; ctx.beginPath(); ctx.moveTo(240, -10); ctx.quadraticCurveTo(300, -40, 330, 10); ctx.stroke();
  ctx.restore();
}

function followButton(x, y, a, t) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha = a;
  const pulse = 1 + 0.04 * Math.sin(t * 5);
  ctx.translate(x, y); ctx.scale(pulse, pulse);
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  for (let k = 0; k < 2; k++) {
    const p = fract(t * 0.6 + k * 0.5);
    ctx.strokeStyle = `rgba(255,200,120,${(1 - p) * 0.6})`; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.roundRect(-230 - p * 40, -60 - p * 20, 460 + p * 80, 120 + p * 40, 60 + p * 20); ctx.stroke();
  }
  ctx.restore();
  const g = ctx.createLinearGradient(0, -60, 0, 60);
  g.addColorStop(0, '#f6d38f'); g.addColorStop(1, '#c48a3c');
  ctx.fillStyle = g; ctx.shadowColor = 'rgba(255,170,80,0.8)'; ctx.shadowBlur = 30;
  ctx.beginPath(); ctx.roundRect(-230, -60, 460, 120, 60); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.fillStyle = '#1a0f05'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '6px';
  ctx.font = '700 46px Cinzel'; ctx.fillText('+ FOLGEN', 0, 4);
  ctx.restore();
}

function memoryHaze(a) {
  if (a <= 0) return;
  const g = ctx.createRadialGradient(W / 2, H / 2, H * 0.2, W / 2, H / 2, H * 0.7);
  g.addColorStop(0, 'rgba(255,220,170,0)'); g.addColorStop(1, `rgba(255,220,170,${0.35 * a})`);
  ctx.fillStyle = g; ctx.fillRect(-200, -200, W + 400, H + 400);
}

function crossfade(k, drawA, drawB) {
  if (k < 1) drawA();
  if (k > 0) { ctx.save(); ctx.globalAlpha = k; drawB(); ctx.restore(); }
}

// ---------- scene helpers ----------
const local = (id, t) => t - SC[id].start;
const lineOf = (scene, idx) => LINES.filter(l => l.scene === scene)[idx];
function speaking(who, t) {
  const l = LINES.find(l => l.who === who && t >= l.start && t <= l.end);
  return l ? Math.sin(clamp((t - l.start) / (l.end - l.start)) * Math.PI) : 0;
}

function camera(z, px = 0, py = 0) {
  ctx.translate(W / 2 + px, H / 2 + py); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
}

// ---------- scenes ----------
const SCENES = {
  kalt(t) {
    const lt = local('kalt', t), d = SC.kalt.end - SC.kalt.start;
    camera(1.15 - 0.12 * lt / d, 0, 120 - 160 * lt / d);
    vgrad([[0, '#010208'], [0.6, '#060b1f'], [1, '#0d1430']]);
    nebula(t, ['rgba(110,60,200,A)', 'rgba(40,120,200,A)', 'rgba(200,80,140,A)'], smooth(0, 3, lt));
    stars(t, { alpha: smooth(0, 2.5, lt), drift: 1 });
    // "Das ist eine Lüge": the sky shivers red
    const lie = lineOf('kalt', 1);
    const red = smooth(lie.start - 0.1, lie.start + 0.3, t) * (1 - smooth(lie.end + 0.2, lie.end + 1.2, t));
    if (red > 0) { ctx.fillStyle = `rgba(120,0,20,${red * 0.25})`; ctx.fillRect(-200, -200, W + 400, H + 400); }
    // cage constellations appear on "Gefängnisse"
    const cage = smooth(lineOf('kalt', 2).start, lineOf('kalt', 2).start + 2, t);
    if (cage > 0) {
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      ctx.strokeStyle = `rgba(180,200,255,${cage * 0.45})`; ctx.lineWidth = 1.5;
      [[270, 520], [780, 380], [540, 900], [300, 1180], [820, 1080]].forEach(([cx, cy], k) => {
        const n = 6, r = 90 + 30 * rnd(k, 5);
        ctx.beginPath();
        for (let i = 0; i <= n; i++) { const a = i / n * 6.283 + k; ctx.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r * 0.8); }
        for (let i = 0; i < n; i += 2) { const a = i / n * 6.283 + k; ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r * 0.8); }
        ctx.stroke();
        glow(cx, cy, 40, 'rgba(220,230,255,A)', cage * (0.6 + 0.4 * Math.sin(t * 3 + k)));
      });
      ctx.restore();
    }
    // the star that is about to fall
    const fall = smooth(d - 3.5, d, lt);
    if (fall > 0) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(540 + Math.sin(t * 40) * 3 * fall, 900, 160 * fall, 'rgba(230,240,255,A)', fall); ctx.restore(); }
  },

  intro(t) {
    const lt = local('intro', t), hit = CUE.title_hit - SC.intro.start, d = SC.intro.end - SC.intro.start;
    vgrad([[0, '#000003'], [1, '#04030c']]);
    // warp flight through the stars
    const speed = 0.15 + 2.2 * smooth(0.5, hit, lt) - 1.8 * smooth(hit, hit + 1.5, lt);
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.lineCap = 'round';
    for (let i = 0; i < 360; i++) {
      const ang = rnd(i, 11) * 6.283, z0 = rnd(i, 12);
      const z = fract(z0 - lt * 0.08 - smooth(0, d, lt) * speed * 0.35);
      const r = 30 / (z + 0.05), r2 = 30 / (z + 0.05 + 0.02 * speed);
      const a = clamp((1 - z) * 1.4) * smooth(0, 1.2, lt);
      ctx.strokeStyle = `rgba(${200 + 55 * rnd(i, 13)},${210 + 40 * rnd(i, 14)},255,${a})`;
      ctx.lineWidth = 1 + (1 - z) * 2.5;
      ctx.beginPath(); ctx.moveTo(540 + Math.cos(ang) * r, 900 + Math.sin(ang) * r); ctx.lineTo(540 + Math.cos(ang) * r2, 900 + Math.sin(ang) * r2); ctx.stroke();
    }
    ctx.restore();
    nebula(t, ['rgba(110,60,200,A)', 'rgba(200,120,60,A)'], smooth(1, 4, lt) * 0.8);
    // emblem draws itself with the leitmotif
    const draw = easeInOut(clamp((lt - 3.0) / 7.5));
    emblem(540, 900, 300 + 40 * smooth(hit, hit + 2, lt), t, draw, smooth(2.6, 3.4, lt) * (1 - 0.55 * smooth(hit, hit + 0.6, lt)));
    // a falling star dives into the emblem and ignites the title
    if (lt > hit - 1.2 && lt < hit + 0.1) {
      const p = clamp((lt - (hit - 1.2)) / 1.2), k = p * p;
      const x = lerp(1000, 540, k), y = lerp(-60, 900, k);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let i = 0; i < 24; i++) { const q = clamp(p - i * 0.02) ** 2; glow(lerp(1000, 540, q), lerp(-60, 900, q), 40 - i, 'rgba(255,220,170,A)', 0.5 * (1 - i / 24)); }
      glow(x, y, 160, 'rgba(255,230,190,A)', 0.9); ctx.restore();
    }
    const ta = smooth(hit, hit + 0.25, lt);
    if (ta > 0) {
      ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(540, 900, 700, 'rgba(255,180,90,A)', 0.35 * ta * (1 - 0.5 * smooth(hit, d, lt))); ctx.restore();
      titleText(540, 900, 112, ta, 1.12 - 0.12 * easeOut((lt - hit) / 3.5));
      ctx.save(); ctx.textAlign = 'center';
      ctx.font = 'italic 600 50px "Cormorant Garamond"'; ctx.fillStyle = `rgba(240,228,210,${smooth(hit + 0.9, hit + 1.8, lt)})`;
      ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 12;
      ctx.fillText(TL.tagline, 540, 1060);
      ctx.restore();
    }
    particles(t, 60, { y0: 1700, dy: -1400, a: 0.6 * ta, color: 'rgba(255,190,120,A)', r: 2, life: 4 });
  },

  welt(t) {
    const lt = local('welt', t), d = SC.welt.end - SC.welt.start;
    const L = i => lineOf('welt', i);
    camera(1.08 - 0.06 * easeInOut(lt / d), 0, 260 - 420 * easeInOut(lt / d));
    vgrad([[0, '#05021a'], [0.3, '#1b0f4c'], [0.5, '#3b2b7a'], [0.66, '#7a4c8f'], [0.76, '#c58aa0'], [1, '#2a1c48']]);
    stars(t, { alpha: 0.95, h: 1000 });
    aurora(t, 1);
    moon(820, 330, 150);
    pinkMoon(220, 230, 55);
    // star dust drifting down - stronger when it is explained
    const dust = 0.35 + 0.65 * smooth(L(3).start - 0.5, L(3).start + 1, t);
    particles(t, 140, { y0: -100, dy: 1800, a: dust, color: 'rgba(255,225,170,A)', r: 2, life: 11, sway: 25, glowR: 7 });
    // far giant trees rising out of the clouds
    giantTree(130, 120, 820, t, 0.35, 11, { lights: 10, lightA: 0.6 });
    giantTree(960, 140, 760, t, 0.4, 12, { lights: 12, lightA: 0.6 });
    island(560, 700, 150, t, 3, 0.5);
    const wx = lerp(-350, 1350, (lt + 2) / (d + 6));
    whale(wx, 620, 0.6, t, 0.6);
    // whale song carries the islands
    const song = smooth(L(4).start - 0.3, L(4).start + 0.8, t);
    if (song > 0) {
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let k = 0; k < 4; k++) {
        const p = fract(t * 0.35 + k / 4);
        ctx.strokeStyle = `rgba(150,230,255,${(1 - p) * 0.45 * song})`; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(wx, 620, 60 + p * 600, 0, 7); ctx.stroke();
      }
      ctx.restore();
    }
    giantTree(420, 230, 980, t, 0.65, 13, { lights: 16, lightA: 0.8 });
    island(880, 1000, 230, t, 4, 0.75);
    whale(lerp(1400, -400, (lt + 1) / (d + 4)), 1080, 1.0, t, 0.9, -1);
    const sea = 0.85 + 0.15 * smooth(L(2).start, L(2).start + 1, t);
    cloudSea(t, 1380, sea);
    particles(t, 50, { y0: 1900, dy: -900, a: 0.5, color: 'rgba(255,220,240,A)', r: 2.4, life: 9, sway: 80 });
  },

  _treeCity(t, o = {}) {
    vgrad([[0, '#04031a'], [0.4, '#121a48'], [0.62, '#2a2e66'], [0.75, '#5a4a86'], [1, '#2a2048']]);
    stars(t, { alpha: 0.9, h: 1100 });
    aurora(t, 0.5);
    moon(840, 300, 120);
    pinkMoon(170, 210, 40);
    palace(540, -260, 0.9, t, { beams: o.beams ?? true });
    whale(lerp(-300, 1400, fract(t / 60)), 760, 0.45, t, 0.55);
    giantTree(540, 200, 520, t, 0.45, 21, { lights: 26, lightA: 0.8, lightSpan: 900 });
    cloudSea(t, 1560, 0.9);
    const c = treeColor(0.8);
    giantTree(150, 190, 360, t, 0.8, 22, { lights: 14, lightSpan: 1100, branches: 3 });
    giantTree(950, 210, 400, t, 0.8, 23, { lights: 14, lightSpan: 1100, branches: 3 });
    platform(160, 820, 470, t, 1, c); platform(940, 900, 480, t, 2, c);
    platform(160, 1230, 500, t, 3, c); platform(940, 1320, 520, t, 4, c);
    bridge(330, 800, 770, 880, 70, t, 1, c, 5);
    bridge(350, 1215, 760, 1300, 80, t, 2, c, 5);
    if (o.lightsOn) {
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let k = 0; k < 60; k++) {
        const on = smooth(o.lightsOn + rnd(k, 700) * 3, o.lightsOn + rnd(k, 700) * 3 + 0.3, t);
        if (on > 0) glow(rnd(k, 701) * W, 500 + rnd(k, 702) * 1000, 26, 'rgba(255,200,120,A)', on * 0.8);
      }
      ctx.restore();
    }
  },

  stadt(t) {
    const lt = local('stadt', t), d = SC.stadt.end - SC.stadt.start, up = lineOf('stadt', 2);
    const tilt = easeInOut(clamp((t - up.start + 0.6) / (up.end - up.start + 0.6)));
    camera(1.04 + 0.04 * lt / d, -30 + 60 * lt / d, 700 * tilt);
    this._treeCity(t);
    particles(t, 50, { y0: 1900, dy: -1300, a: 0.6, color: 'rgba(255,190,110,A)', r: 2, life: 9, glowR: 8 });
  },

  _palaceView(t, flare = 1) {
    vgrad([[0, '#05031c'], [0.45, '#1a1448'], [0.7, '#3b2a5c'], [1, '#120c24']]);
    stars(t, { alpha: 1, h: 1000 });
    aurora(t, 0.4);
    giantTree(540, 420, 1420, t, 0.85, 31, { branches: 0, lights: 0 });
    palace(540, 1260, 1.25, t, { flare });
    for (let k = 0; k < 10; k++) {
      const x = 90 + k * 100, y = 1450 + Math.abs(k - 4.5) * 10;
      figure(x, y, 170, { hood: true, t: t + k, dir: x < 540 ? 1 : -1, color: '#0a0812', rim: 'rgba(255,200,130,0.7)', rimBlur: 14, arm: -1.25, armLen: 30, staff: true });
    }
    particles(t, 50, { y0: 1500, dy: -1300, a: 0.6, color: 'rgba(255,210,150,A)', r: 2, life: 7 });
  },

  _lowerView(t) {
    vgrad([[0, '#020309'], [0.5, '#0a0d1e'], [1, '#05050a']]);
    const c = treeColor(0.95);
    giantTree(260, 360, 200, t, 0.95, 41, { lights: 6, lightSpan: 1500, branches: 2, lightA: 0.6 });
    giantTree(860, 300, 300, t, 0.95, 42, { lights: 5, lightSpan: 1400, branches: 2, lightA: 0.6 });
    platform(260, 1250, 380, t, 7, c); platform(860, 1480, 360, t, 8, c);
    bridge(420, 1240, 700, 1460, 90, t, 3, c, 3);
    // dim pool of light from above - the Light Crown far up
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    const g = ctx.createLinearGradient(0, 0, 0, 700);
    g.addColorStop(0, 'rgba(255,210,150,0.25)'); g.addColorStop(1, 'rgba(255,210,150,0)');
    ctx.fillStyle = g; ctx.fillRect(380, 0, 320, 700);
    ctx.restore();
    particles(t, 30, { y0: -50, dy: 1600, a: 0.4, color: 'rgba(255,220,170,A)', r: 1.6, life: 14 });
  },

  _fireView(t, k) {
    vgrad([[0, '#1a0204'], [0.5, '#5a0d08'], [0.75, '#b8360f'], [1, '#2a0603']]);
    for (let i = 0; i < 7; i++) {
      const x = 80 + i * 150, h = 500 + 300 * rnd(i, 800);
      giantTree(x, 80 + 40 * rnd(i, 801), 1500 - h, t, 1, 50 + i, { color: '#120202', branches: 2 });
      flame(x + (rnd(i, 802) - 0.5) * 120, 1500 - h * 0.4, 260 + 100 * rnd(i, 803), t + i, 0.9);
    }
    ground(1500, '#0a0101', 20, 3);
    particles(t, 160, { y0: 1700, dy: -1900, a: 0.9, color: 'rgba(255,140,60,A)', r: 2.6, life: 4, sway: 90, glowR: 8 });
  },

  lichtkrone(t) {
    const L = i => lineOf('lichtkrone', i), lt = local('lichtkrone', t);
    const low = smooth(L(1).start - 0.6, L(1).start + 0.4, t) * (1 - smooth(L(2).start - 0.6, L(2).start + 0.2, t));
    const fire = smooth(L(3).start + 2.0, L(3).start + 3.0, t);
    ctx.save(); camera(1.05 + 0.04 * lt / 20, 0, 0);
    if (fire < 1) {
      crossfade(low, () => this._palaceView(t), () => this._lowerView(t));
    }
    if (fire > 0) { ctx.save(); ctx.globalAlpha = fire; this._fireView(t, fire); ctx.restore(); }
    ctx.restore();
    // the law as an inscription
    const law = smooth(L(2).start, L(2).start + 0.8, t) * (1 - smooth(L(3).start + 1.6, L(3).start + 2.4, t));
    if (law > 0) {
      ctx.save(); ctx.textAlign = 'center';
      const bg = ctx.createRadialGradient(540, 560, 40, 540, 560, 560);
      bg.addColorStop(0, `rgba(0,0,0,${0.6 * law})`); bg.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = bg; ctx.fillRect(0, 100, W, 900);
      ctx.shadowColor = 'rgba(255,150,60,0.9)'; ctx.shadowBlur = 24;
      if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '8px';
      ctx.font = '700 44px Cinzel'; ctx.fillStyle = `rgba(255,214,150,${law})`;
      ctx.fillText('DAS ERSTE GESETZ', 540, 430);
      if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '1px';
      ctx.font = 'italic 600 52px "Cormorant Garamond"'; ctx.fillStyle = `rgba(250,240,225,${law})`;
      ctx.fillText('Jeder Stern, der fällt, gehört dem Orden.', 540, 530);
      ctx.fillText('Wer ein Sternenherz berührt, stirbt.', 540, 600);
      ctx.restore();
    }
  },

  seraphine_vor(t) {
    const L = i => lineOf('seraphine_vor', i), lt = local('seraphine_vor', t);
    const mem = smooth(L(2).start - 0.3, L(2).start + 0.9, t) * (1 - smooth(L(2).end - 2.2, L(2).end - 0.6, t));
    const speak = speaking('SERAPHINE_HALLE', t);
    const A = () => {
      ctx.save(); camera(1.0 + 0.08 * lt / 22, 0, 60);
      vgrad([[0, '#06030f'], [0.5, '#2a0d1c'], [0.8, '#5a1a22'], [1, '#10050a']]);
      stars(t, { alpha: 0.5, h: 900 });
      palace(540, 1100, 1.0, t, { beams: false, flare: 1 + speak * 0.6 });
      ctx.fillStyle = '#0c0610'; ctx.fillRect(-200, 1240, W + 400, 60);
      for (let k = 0; k < 12; k++) ctx.fillRect(-180 + k * 110, 1150, 14, 100);
      const hand = figure(540, 1250, 720, { hood: true, cape: true, t, dir: -1, rim: 'rgba(255,90,60,0.95)', rimBlur: 40, arm: lerp(-1.3, -1.75, speak), armLen: 36, staff: true });
      flame(hand[0], hand[1] + 10, 80 + 70 * speak, t, 1);
      for (let k = 0; k < 26; k++) {
        const x = (k + 0.5) * W / 26 + (rnd(k, 900) - 0.5) * 20, y = 1640 + rnd(k, 901) * 140;
        ctx.fillStyle = '#050207'; ctx.beginPath(); ctx.arc(x, y, 30, 0, 7); ctx.fill(); ctx.fillRect(x - 36, y + 20, 72, 300);
        if (k % 4 === 1) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(x + 30, y - 20, 40, 'rgba(255,170,90,A)', 0.7); ctx.restore(); }
      }
      ctx.restore();
    };
    const B = () => {
      ctx.save(); camera(1.05, 0, 0);
      vgrad([[0, '#2a1a10'], [0.55, '#7a4a28'], [0.8, '#c08850'], [1, '#3a2414']]);
      stars(t, { alpha: 0.4, h: 800 });
      ground(1500, '#1a0f08', 10, 8);
      figure(430, 1500, 560, { hair: true, t, color: '#1a0f08', rim: 'rgba(255,220,160,0.9)', rimBlur: 30, arm: -0.2, armLen: 30 });
      const h2 = figure(650, 1500, 580, { hair: true, t, dir: -1, color: '#1a0f08', rim: 'rgba(255,220,160,0.9)', rimBlur: 30, arm: -0.25, armLen: 30 });
      ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(540, 1170, 70, 'rgba(255,240,200,A)', 0.9); ctx.restore();
      memoryHaze(1);
      ctx.restore();
    };
    crossfade(mem, A, B);
  },

  _branchScene(t, o = {}) {
    vgrad([[0, '#04031a'], [0.4, '#141c4c'], [0.65, '#2e2e66'], [0.8, '#5e4a88'], [1, '#2a2048']]);
    stars(t, { alpha: 0.9, h: 1100 });
    moon(820, 330, 110);
    giantTree(860, 220, 500, t, 0.55, 61, { lights: 18, lightSpan: 900, lightA: 0.8 });
    giantTree(200, 180, 620, t, 0.5, 62, { lights: 14, lightSpan: 900, lightA: 0.7 });
    cloudSea(t, 1500, 0.9);
    // the big branch Lunara walks on
    const c = treeColor(0.98);
    ctx.fillStyle = c;
    ctx.beginPath(); ctx.moveTo(-200, 1640); ctx.quadraticCurveTo(500, 1560, 1300, 1420); ctx.lineTo(1300, 1560); ctx.quadraticCurveTo(500, 1700, -200, 1800); ctx.closePath(); ctx.fill();
    ctx.fillRect(-200, 1780, W + 400, 400);
    const lanterns = 7, lit = o.lit ?? lanterns;
    for (let i = 0; i < lanterns; i++) {
      const u = (i + 0.5) / lanterns, x = lerp(-100, 1250, u), y = (1 - u) * (1 - u) * 1640 + 2 * (1 - u) * u * 1560 + u * u * 1420;
      ctx.strokeStyle = c; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y + 60); ctx.stroke();
      ctx.fillStyle = c; ctx.fillRect(x - 10, y + 60, 20, 28);
      const on = clamp(lit - i);
      if (on > 0) {
        const fl = 0.8 + 0.2 * Math.sin(t * 9 + i * 3);
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        glow(x, y + 74, 90 * fl, 'rgba(255,170,80,A)', 0.8 * on); glow(x, y + 74, 16, 'rgba(255,230,180,A)', on);
        ctx.restore();
      }
    }
  },

  lunara(t) {
    const L = i => lineOf('lunara', i), lt = local('lunara', t);
    const close = smooth(L(5).start - 0.6, L(5).start + 0.6, t);
    const A = () => {
      const push = smooth(L(2).start, L(4).end, t);
      ctx.save(); camera(1.0 + 0.35 * push, -120 * push, -260 * push);
      const lit = lerp(1, 7, clamp((t - SC.lunara.start) / (L(0).end - SC.lunara.start + 1)));
      this._branchScene(t, { lit });
      const look = smooth(L(4).start - 0.8, L(4).start, t);
      const hand = figure(380, 1610, 500, { hair: true, t, arm: lerp(-0.9, -1.4, look), armLen: 36, rim: 'rgba(255,170,90,0.85)', rimBlur: 30 });
      ctx.strokeStyle = '#04050a'; ctx.lineWidth = 6;
      ctx.beginPath(); ctx.moveTo(hand[0] - 30, hand[1] + 80); ctx.lineTo(hand[0] + 60, hand[1] - 170); ctx.stroke();
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      glow(hand[0] + 60, hand[1] - 175, 60, 'rgba(255,180,90,A)', 0.9);
      const dust = smooth(L(1).start, L(1).start + 1, t);
      if (dust > 0) { glow(330, 1330, 70, 'rgba(255,230,160,A)', 0.8 * dust); glow(330, 1330, 14, 'rgba(255,250,230,A)', dust); }
      ctx.restore();
      particles(t, 50, { y0: 1800, dy: -1200, a: 0.6, color: 'rgba(255,190,110,A)', r: 2, life: 9, glowR: 8 });
      ctx.restore();
    };
    const B = () => {
      ctx.save(); camera(1.0 + 0.06 * clamp((t - L(5).start) / 8), 0, 0);
      vgrad([[0, '#03021a'], [0.6, '#151446'], [1, '#08061a']]);
      stars(t, { alpha: 1 });
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let k = 0; k < 12; k++) glow(rnd(k, 950) * W, rnd(k, 951) * H, 120 + 80 * rnd(k, 952), 'rgba(255,190,120,A)', 0.12);
      glow(STARS[0].x * W + 160, STARS[0].y * H - 60, 90, 'rgba(255,230,190,A)', 0.8 + 0.2 * Math.sin(t * 3));
      ctx.restore();
      pendant(540, 1000, 220, t, { angle: Math.atan2(STARS[0].y * H - 60 - 1000, STARS[0].x * W + 160 - 540) });
      ctx.restore();
    };
    crossfade(close, A, B);
  },

  kael_vor(t) {
    const L = i => lineOf('kael_vor', i);
    const leave = smooth(L(2).start - 0.5, L(2).start + 0.5, t);
    const now = smooth(L(4).start - 0.5, L(4).start + 0.5, t);
    const A = () => {
      ctx.save(); camera(1.05, 0, 0);
      vgrad([[0, '#3a2414'], [0.5, '#8a5a30'], [0.75, '#d69a58'], [1, '#2a1a0e']]);
      ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(540, 1150, 500, 'rgba(255,200,130,A)', 0.5); ctx.restore();
      cloudSea(t, 1520, 0.5);
      ctx.fillStyle = '#1a0f08';
      ctx.beginPath(); ctx.moveTo(-200, 1560); ctx.quadraticCurveTo(540, 1500, 1300, 1560); ctx.lineTo(1300, 2200); ctx.lineTo(-200, 2200); ctx.fill();
      const k = figure(470, 1540, 600, { t, color: '#1a0f08', rim: 'rgba(255,220,160,0.9)', rimBlur: 30, arm: -0.6, armLen: 36 });
      figure(660, 1545, 330, { hair: true, t, dir: -1, color: '#1a0f08', rim: 'rgba(255,220,160,0.9)', rimBlur: 24, arm: -1.2, armLen: 30 });
      memoryHaze(1);
      ctx.restore();
    };
    const B = () => {
      ctx.save(); camera(1.0, 0, 0);
      vgrad([[0, '#2a2030'], [0.5, '#5a4050'], [0.8, '#a07060'], [1, '#20141a']]);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      glow(900, 160, 500, 'rgba(255,230,190,A)', 0.7);
      ctx.restore();
      // the glowing stair up to the Light Crown
      for (let k = 0; k < 18; k++) {
        const u = k / 17, x = lerp(250, 900, u), y = lerp(1600, 260, u);
        ctx.fillStyle = `rgba(255,${220 - 60 * u},${170 - 70 * u},${0.25 + 0.5 * u})`; ctx.fillRect(x - 70, y, 140, 10);
      }
      const p = clamp((t - L(2).start) / (L(3).end - L(2).start));
      const u = 0.12 + 0.55 * easeInOut(p), turn = speaking('KAEL_ERINNERUNG', t) > 0.05;
      figure(lerp(250, 900, u), lerp(1600, 260, u), lerp(560, 260, u), { t, color: '#1a0f12', rim: 'rgba(255,220,180,0.9)', rimBlur: 24, dir: turn ? -1 : 1 });
      figure(160, 1720, 330, { hair: true, t, color: '#1a0f12', rim: 'rgba(255,210,170,0.8)', rimBlur: 20, arm: -0.7, armLen: 32 });
      memoryHaze(1);
      ctx.restore();
    };
    const C = () => {
      ctx.save(); camera(1.0 + 0.05 * clamp((t - L(4).start) / 8), 0, 0);
      this._ridge(t, 0.6);
      this._order(t, { skip: 6 });
      figure(540, 1780, 860, { dir: -1, t, cape: true, rim: 'rgba(255,110,70,0.9)', rimBlur: 34, arm: 1.25, armLen: 34, sword: 1.5 });
      particles(t, 40, { y0: 1500, dy: -1100, a: 0.5, color: 'rgba(255,140,70,A)', r: 2, life: 6 });
      ctx.restore();
    };
    if (now < 1) crossfade(leave, A, B);
    if (now > 0) { ctx.save(); ctx.globalAlpha = now; C(); ctx.restore(); }
  },

  fall(t) {
    const lt = local('fall', t), d = SC.fall.end - SC.fall.start;
    const imp = CUE.impact, st = CUE.streak;
    const city = smooth(st - 1.2, st - 0.3, t);
    const P = () => {
      ctx.save();
      vgrad([[0, '#03021a'], [1, '#08061a']]);
      stars(t, { alpha: 1 });
      pendant(540, 1000, 240, t, { angle: -1.2, tremble: smooth(SC.fall.start, SC.fall.start + 3, t) });
      ctx.restore();
    };
    const V = () => {
      ctx.save(); camera(1.0, 0, 0);
      this._branchScene(t);
      const p = clamp((t - st) / (imp - st));
      const ix = 640, iy = 1530;
      if (t >= st && t < imp + 0.1) {
        const k = Math.pow(p, 1.6), x = lerp(60, ix, k), y = lerp(80, iy, k);
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < 40; i++) { const q = Math.pow(clamp(p - i * 0.012), 1.6); glow(lerp(60, ix, q), lerp(80, iy, q), 50 - i, 'rgba(200,225,255,A)', (1 - i / 40) * 0.5); }
        glow(x, y, 260 * (0.5 + p), 'rgba(210,230,255,A)', 0.8); glow(x, y, 30, 'rgba(255,255,255,A)', 1);
        ctx.restore();
      }
      if (t > imp) {
        const a = Math.exp(-(t - imp) * 0.3);
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        const g = ctx.createLinearGradient(0, 0, 0, iy);
        g.addColorStop(0, 'rgba(180,210,255,0)'); g.addColorStop(1, `rgba(200,225,255,${0.7 * a})`);
        ctx.fillStyle = g; ctx.fillRect(ix - 30 - 20 * a, 0, 60 + 40 * a, iy);
        glow(ix, iy, 500, 'rgba(190,215,255,A)', 0.7 * a);
        const r = (t - imp) * 900;
        ctx.strokeStyle = `rgba(220,235,255,${clamp(1 - (t - imp) / 1.4) * 0.8})`; ctx.lineWidth = 6;
        ctx.beginPath(); ctx.ellipse(ix, iy, r, r * 0.25, 0, 0, 7); ctx.stroke();
        ctx.restore();
      }
      const lit = smooth(imp - 0.3, imp + 0.2, t);
      figure(330, 1610, 480, { hair: true, t, arm: -0.4, rim: `rgba(200,220,255,${0.3 + 0.7 * lit})`, rimBlur: 40 });
      ctx.restore();
    };
    crossfade(city, P, V);
  },

  ruinen(t) {
    const lt = local('ruinen', t), d = SC.ruinen.end - SC.ruinen.start;
    camera(1.0 + 0.1 * lt / d, 0, -20 * lt / d);
    vgrad([[0, '#02030c'], [0.5, '#0b1330'], [0.8, '#1a2650'], [1, '#05060c']]);
    stars(t, { alpha: 0.6, h: 1100 });
    const voice = speaking('STERN', t);
    const hx = 600, hy = 1150 + Math.sin(t * 1.1) * 14;
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(hx, hy, 900, 'rgba(120,160,255,A)', 0.4 + voice * 0.25);
    ctx.restore();
    [[80, 900, 1], [250, 700, 2], [880, 820, 3], [1010, 640, 4]].forEach(([x, h, s]) => stoneTree(x, 1500, h, s, '#0c0e1a'));
    ruins(t);
    whaleBones(830, 1570, 1.1, '#2a3048');
    whaleBones(160, 1640, 0.7, '#1e2236');
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    ctx.fillStyle = 'rgba(160,200,255,0.25)'; ctx.beginPath(); ctx.ellipse(hx, 1490, 220, 40, 0, 0, 7); ctx.fill();
    ctx.restore();
    for (let i = 0; i < 10; i++) {
      const a = t * (0.2 + rnd(i, 70) * 0.3) + i, r = 120 + rnd(i, 71) * 160;
      const x = hx + Math.cos(a) * r, y = hy + Math.sin(a) * r * 0.35 - 20, s = 8 + rnd(i, 72) * 18;
      ctx.fillStyle = '#05060c'; ctx.save(); ctx.translate(x, y); ctx.rotate(a * 2);
      ctx.shadowColor = 'rgba(170,200,255,0.9)'; ctx.shadowBlur = 12; ctx.fillRect(-s / 2, -s / 2, s, s * 0.8); ctx.restore();
    }
    heart(hx, hy, 34, t, { pulse: voice });
    particles(t, 70, { y0: 1500, dy: -900, x0: 250, w: 700, a: 0.8, color: 'rgba(190,215,255,A)', r: 2, life: 7, sway: 50 });
    const enter = lineOf('ruinen', 3);
    const walk = easeInOut(clamp((t - enter.start) / 8));
    const ex = lerp(-120, 300, walk);
    figure(ex, 1640, 470, { hair: true, t, wind: 2, rim: `rgba(170,205,255,${0.8 + voice * 0.2})`, rimBlur: 36, arm: lerp(0.9, 0.2, smooth(lineOf('ruinen', 8).start, lineOf('ruinen', 8).end, t)) });
    ctx.fillStyle = '#020306'; ctx.fillRect(-200, 1640, W + 400, 500);
  },

  glocken(t) {
    const L = i => lineOf('glocken', i), lt = local('glocken', t);
    const strikes = [];
    for (let k = 0; k < 20; k++) strikes.push(CUE.glocke + k * 1.5);
    const city = smooth(L(2).start - 0.5, L(2).start + 0.5, t);
    const A = () => {
      ctx.save(); camera(1.0 + 0.05 * lt / 10, 0, 0);
      vgrad([[0, '#0a0206'], [0.5, '#3a0a10'], [0.8, '#6a1a18'], [1, '#14040a']]);
      stars(t, { alpha: 0.5, h: 900 });
      palace(540, 1450, 1.0, t, { beams: false, flare: 1.5 });
      bellTower(220, 1480, 1.2, t, strikes.filter((_, k) => k % 2 === 0), 1);
      bellTower(860, 1480, 1.2, t, strikes.filter((_, k) => k % 2 === 1), -1);
      ctx.fillStyle = '#080206'; ctx.fillRect(-200, 1480, W + 400, 600);
      ctx.restore();
    };
    const B = () => {
      ctx.save(); camera(1.0, 0, 120);
      this._treeCity(t, { beams: false, lightsOn: L(2).start });
      // torches of the Flame Guard spiralling down the great trunk
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let k = 0; k < 24; k++) {
        const u = fract((t - L(2).start) * 0.08 + k / 24);
        const y = lerp(300, 1500, u), x = 540 + Math.sin(u * 18 + k * 0.2) * 130;
        glow(x, y, 36, 'rgba(255,120,50,A)', 0.9 * smooth(L(2).start, L(2).start + 1, t)); glow(x, y, 8, 'rgba(255,230,180,A)', 1);
      }
      ctx.restore();
      ctx.fillStyle = `rgba(120,10,10,${0.18 + 0.1 * Math.sin(t * 6)})`; ctx.fillRect(-300, -300, W + 600, H + 600);
      ctx.restore();
    };
    crossfade(city, A, B);
  },

  outro(t) {
    const lt = local('outro', t), d = SC.outro.end - SC.outro.start, hit = CUE.outro_hit;
    const dawn = smooth(hit - 0.2, hit + 2.5, t);
    ctx.save(); camera(1.05 + 0.08 * lt / d, 0, 0);
    vgrad([[0, '#020108'], [0.45, `rgb(${18 + 50 * dawn},${10 + 30 * dawn},${40 + 30 * dawn})`], [0.7, `rgb(${60 + 150 * dawn},${30 + 90 * dawn},${70 + 40 * dawn})`], [1, '#160c22']]);
    stars(t, { alpha: 1 });
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(STARS[0].x * W, STARS[0].y * H, 220, 'rgba(255,205,140,A)', 0.6);
    glow(540, 1350, 900, 'rgba(255,190,120,A)', 0.5 * dawn);
    ctx.restore();
    whale(lerp(1300, -300, lt / (d + 4)), 900, 0.7, t, 0.8, -1);
    cloudSea(t, 1380, 0.9);
    // Lunara sitting on the end of a branch, looking out
    const c = '#05030a';
    ctx.fillStyle = c;
    ctx.beginPath(); ctx.moveTo(-200, 1500); ctx.quadraticCurveTo(300, 1460, 640, 1420); ctx.lineTo(650, 1450); ctx.quadraticCurveTo(300, 1520, -200, 1620); ctx.fill();
    ctx.shadowColor = 'rgba(255,190,130,0.9)'; ctx.shadowBlur = 26;
    ctx.beginPath(); ctx.ellipse(540, 1310, 26, 32, 0, 0, 7); ctx.fill();
    ctx.beginPath(); ctx.moveTo(520, 1342); ctx.bezierCurveTo(470, 1380, 480, 1430, 500, 1440); ctx.lineTo(590, 1440); ctx.bezierCurveTo(600, 1400, 580, 1360, 560, 1342); ctx.fill();
    ctx.beginPath(); ctx.moveTo(500, 1300); ctx.bezierCurveTo(470, 1340, 450, 1380, 430 - Math.sin(t * 2) * 8, 1410); ctx.lineTo(500, 1350); ctx.fill();
    ctx.lineCap = 'round'; ctx.lineWidth = 16; ctx.strokeStyle = c;
    ctx.beginPath(); ctx.moveTo(560, 1440); ctx.lineTo(600, 1500 + Math.sin(t * 1.5) * 6); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(580, 1440); ctx.lineTo(625, 1495 + Math.sin(t * 1.5 + 1) * 6); ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(575, 1400, 40, 'rgba(255,215,150,A)', 0.8); ctx.restore();
    particles(t, 60, { y0: 1900, dy: -1700, a: 0.6, color: 'rgba(255,210,150,A)', r: 2, life: 8 });
    ctx.restore();
    // call to action, then the end card
    const cta = LINES.find(l => l.scene === 'outro');
    const fa = smooth(cta.start + 1.5, cta.start + 2.3, t);
    followButton(540, 980, fa, t);
    ctx.save(); ctx.textAlign = 'center'; ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 14;
    ctx.font = 'italic 600 46px "Cormorant Garamond"'; ctx.fillStyle = `rgba(245,235,220,${fa})`;
    ctx.fillText('… und sieh die nächste Folge als Erstes', 540, 1110);
    ctx.restore();
    const card = smooth(hit - 0.1, hit + 0.8, t);
    if (card > 0) {
      titleText(540, 470, 100, card, 1.05 - 0.05 * easeOut((t - hit) / 3));
      ctx.save(); ctx.textAlign = 'center'; ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 14;
      if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '6px';
      ctx.font = '400 36px Cinzel'; ctx.fillStyle = `rgba(230,205,165,${smooth(hit + 0.6, hit + 1.4, t)})`;
      ctx.fillText('FOLGE 2 · DIE STADT OHNE STERNE', 540, 600);
      if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '0px';
      ctx.font = 'italic 600 54px "Cormorant Garamond"'; ctx.fillStyle = `rgba(245,235,220,${smooth(hit + 1.2, hit + 2.0, t)})`;
      ctx.fillText('Fortsetzung folgt …', 540, 700);
      ctx.restore();
    }
  },

  bund(t) {
    const lt = local('bund', t), d = SC.bund.end - SC.bund.start, touch = CUE.touch;
    const pre = clamp((t - SC.bund.start) / (touch - SC.bund.start)), post = t - touch;
    camera(1.0 + 0.15 * easeInOut(pre), 0, 0);
    vgrad([[0, '#02030a'], [1, '#0b1028']]);
    const hx = 540, hy = 820;
    const after = post > 0 ? Math.exp(-post * 0.5) : 0;
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(hx, hy, 1100, 'rgba(110,150,255,A)', 0.35 + pre * 0.3 + after * 0.4);
    ctx.restore();
    heart(hx, hy, 70 + pre * 20, t, { pulse: pre * 0.6 + after });
    // reaching hand
    const reach = easeInOut(pre);
    const hy2 = lerp(2100, hy + 115, reach);
    ctx.save(); ctx.translate(540 + 20 * (1 - reach), hy2);
    ctx.fillStyle = '#04050b'; ctx.shadowColor = 'rgba(190,215,255,0.95)'; ctx.shadowBlur = 40 + 40 * pre;
    ctx.beginPath(); ctx.moveTo(-70, 900); ctx.bezierCurveTo(-70, 400, -80, 180, -62, 60); ctx.lineTo(62, 60); ctx.bezierCurveTo(78, 180, 70, 400, 70, 900); ctx.fill();
    ctx.beginPath(); ctx.ellipse(0, 20, 70, 85, 0, 0, 7); ctx.fill();
    [[-50, -70, -0.18, 95], [-18, -95, -0.05, 120], [16, -98, 0.05, 125], [48, -80, 0.16, 105]].forEach(([fx, fy, a, L]) => {
      ctx.save(); ctx.translate(fx, fy + 60); ctx.rotate(a); ctx.beginPath(); ctx.roundRect(-13, -L + 30, 26, L, 13); ctx.fill(); ctx.restore();
    });
    ctx.beginPath(); ctx.ellipse(-82, 30, 20, 60, -0.6, 0, 7); ctx.fill();
    ctx.restore();
    if (post > 0) {
      // runes crawling up the arm, rings expanding, silver lightning
      const e = easeOut(post / 1.4);
      runeRing(hx, hy, 220 + 260 * e, t, clamp(1.4 - post * 0.12), 'rgba(200,225,255,A)', 28, 1);
      runeRing(hx, hy, 160 + 120 * e, t, clamp(1.4 - post * 0.12), 'rgba(255,230,180,A)', 18, -1);
      runeRing(hx, hy, 420 + 380 * e, t, clamp(0.9 - post * 0.12), 'rgba(170,200,255,A)', 40, 1);
      if (post < 3) {
        for (let k = 0; k < 6; k++) {
          const a = k / 6 * 6.283 + Math.floor(t * 12) * 0.3;
          lightning(hx, hy, hx + Math.cos(a) * 700, hy + Math.sin(a) * 700, Math.floor(t * 15) + k * 31, 3, 'rgba(210,230,255,A)');
        }
      }
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let k = 0; k < 7; k++) {
        const y = hy + 160 + k * 120, x = 540 + Math.sin(k * 2.1) * 30;
        ctx.save(); ctx.translate(x, y); ctx.strokeStyle = `rgba(210,230,255,${clamp(post * 2 - k * 0.3) * 0.9})`; ctx.lineWidth = 3;
        ctx.beginPath(); for (const [a1, b1, a2, b2] of GLYPHS[k + 5]) { ctx.moveTo(a1 * 40, b1 * 40); ctx.lineTo(a2 * 40, b2 * 40); } ctx.stroke(); ctx.restore();
      }
      ctx.restore();
      particles(t, 120, { y0: 1700, dy: -1800, a: after, color: 'rgba(210,230,255,A)', r: 2.5, life: 3, sway: 120 });
    } else {
      particles(t, 50, { y0: 1400, dy: -900, a: 0.6, color: 'rgba(190,215,255,A)', r: 2, life: 6 });
    }
  },

  _order(t, o = {}) {
    // the Order on the ridge: hooded figures, torches, Seraphine in the middle
    const rise = o.rise ?? 1, pos = [];
    for (let i = 0; i < 9; i++) {
      if (i === 4) continue;
      const x = 120 + i * 105 + (rnd(i, 80) - 0.5) * 30, y = 1250 + Math.abs(i - 4) * 8 + (1 - rise) * 120;
      if (o.skip === i) continue;
      figure(x, y, 190 + rnd(i, 81) * 20, { hood: true, t: t + i, dir: x < 540 ? 1 : -1, rim: 'rgba(255,120,60,0.6)', rimBlur: 14, arm: -1.2, armLen: 30, staff: true, color: '#050509' });
      pos.push([x, y - 200]);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      const fl = 0.8 + 0.25 * Math.sin(t * 13 + i * 5) + 0.1 * Math.sin(t * 29 + i);
      const tx = x + (x < 540 ? 1 : -1) * 20, ty = y - 220;
      glow(tx, ty, 80 * fl, 'rgba(255,130,50,A)', 0.7 * rise); glow(tx, ty, 14, 'rgba(255,220,150,A)', rise);
      ctx.restore();
    }
    const sx = 540, sy = 1270 + (1 - rise) * 120, raise = o.raise ?? 0;
    const sh = figure(sx, sy, 250, { hood: true, t, cape: true, rim: 'rgba(255,90,60,0.85)', rimBlur: 18, arm: lerp(-1.35, -1.9, raise), armLen: 36, staff: true, dir: -1 });
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(sh[0], sh[1], 120 + 80 * raise + 20 * Math.sin(t * 6), 'rgba(255,110,60,A)', 0.9 * rise);
    glow(sh[0], sh[1], 22, 'rgba(255,230,200,A)', rise);
    ctx.restore();
    return sh;
  },

  _ridge(t, red = 0.5) {
    vgrad([[0, '#05030a'], [0.45, `rgb(${30 + 40 * red},12,30)`], [0.62, `rgb(${70 + 60 * red},30,40)`], [0.7, '#2a1424'], [1, '#05050a']]);
    stars(t, { alpha: 0.5, h: 1000 });
    ctx.save(); ctx.globalAlpha = 0.85; ruins(t, { color: '#0b0812' }); ctx.restore();
    ctx.fillStyle = '#0a070f';
    ctx.beginPath(); ctx.moveTo(-200, 1290);
    for (let x = -200; x <= W + 200; x += 60) ctx.lineTo(x, 1260 + Math.sin(x * 0.01) * 14 + rnd(3, x) * 10);
    ctx.lineTo(W + 200, 2200); ctx.lineTo(-200, 2200); ctx.fill();
  },

  _elaraFg(t, o = {}) {
    // Elara foreground left, glowing hand
    const corrupt = o.corrupt ?? 0;
    const hand = figure(o.x ?? 300, 1760, o.h ?? 640, { hair: true, t, wind: 3, rim: corrupt > 0.5 ? 'rgba(170,80,255,0.9)' : 'rgba(170,205,255,0.9)', rimBlur: 34, arm: o.arm ?? 0.25, armLen: 32 });
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    const p = 0.8 + 0.2 * Math.sin(t * 3);
    glow(hand[0], hand[1], 170 * p, corrupt > 0.5 ? 'rgba(150,60,255,A)' : 'rgba(190,220,255,A)', 0.9);
    glow(hand[0], hand[1], 26, 'rgba(255,255,255,A)', 0.9);
    ctx.restore();
    return hand;
  },

  orden(t) {
    const lt = local('orden', t), d = SC.orden.end - SC.orden.start;
    camera(1.0 + 0.08 * lt / d, 0, 0);
    this._ridge(t, 0.4 + 0.4 * smooth(lineOf('orden', 5).start, lineOf('orden', 5).end, t));
    const rise = easeOut(clamp((t - SC.orden.start - 0.3) / 3));
    this._order(t, { rise });
    particles(t, 50, { y0: 1400, dy: -1100, a: 0.6, color: 'rgba(255,140,70,A)', r: 2, life: 6, sway: 60 });
    this._elaraFg(t, { arm: 0.3 });
    // "Es hat sie getötet" - slow red pulse
    const k = smooth(lineOf('orden', 5).start - 0.2, lineOf('orden', 5).start + 0.4, t) * (1 - smooth(lineOf('orden', 6).start, lineOf('orden', 6).end, t));
    if (k > 0) { ctx.fillStyle = `rgba(140,10,20,${k * 0.18})`; ctx.fillRect(-200, -200, W + 400, H + 400); }
  },

  _kaelPos(t) {
    const walkL = lineOf('kael', 1);
    const w = easeInOut(clamp((t - walkL.start) / (walkL.end - walkL.start)));
    return { x: lerp(750, 760, w), y: lerp(1262, 1760, w), h: lerp(192, 600, w) };
  },

  kael(t) {
    const lt = local('kael', t), d = SC.kael.end - SC.kael.start;
    camera(1.0 + 0.06 * lt / d, 0, 0);
    this._ridge(t, 0.5);
    const kp = this._kaelPos(t);
    const blur = smooth(lineOf('kael', 1).start, lineOf('kael', 1).end, t);
    ctx.save(); ctx.filter = `blur(${blur * 5}px)`; ctx.globalAlpha = 1 - blur * 0.35; this._order(t, { skip: 6 }); ctx.restore();
    particles(t, 40, { y0: 1500, dy: -1100, a: 0.5, color: 'rgba(255,140,70,A)', r: 2, life: 6 });
    this._elaraFg(t, { arm: 0.3 });
    figure(kp.x, kp.y, kp.h, { dir: -1, t, cape: true, rim: 'rgba(255,110,70,0.85)', rimBlur: 28, arm: -0.35, armLen: 34, sword: -0.25 });
    // eye-line light between the two on "Ich kann es trotzdem nicht"
    const k = smooth(lineOf('kael', 7).start, lineOf('kael', 7).end, t);
    if (k > 0) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(540, 1200, 600, 'rgba(255,200,150,A)', 0.15 * k); ctx.restore(); }
  },

  angriff(t) {
    const lt = local('angriff', t), d = SC.angriff.end - SC.angriff.start;
    const B = CUE.bolt, F = CUE.fallen;
    const shake = t > F ? 0 : 0;
    camera(1.06 + 0.04 * smooth(B, F, t), shake, 0);
    this._ridge(t, 0.7);
    const sh = this._order(t, { skip: 6, raise: smooth(SC.angriff.start + 1, B, t) });
    particles(t, 40, { y0: 1500, dy: -1100, a: 0.5, color: 'rgba(255,140,70,A)', r: 2, life: 6 });
    const hand = this._elaraFg(t, { arm: lerp(0.3, -0.9, smooth(B, F, t)) });
    // Kael lowers his sword, then leaps in front of her
    const lower = smooth(SC.angriff.start, SC.angriff.start + 1.4, t);
    const leap = easeInOut(clamp((t - B - 0.15) / (F - B - 0.2)));
    const kx = lerp(760, 470, leap), fallRot = t > F ? easeOut((t - F) / 1.1) * 1.45 : 0;
    figure(kx, 1760, 600, { dir: -1, t, cape: true, rim: 'rgba(255,110,70,0.85)', rimBlur: 28, arm: lerp(-0.35, 1.3, lower), armLen: 34, sword: lerp(-0.25, 1.45, lower), rot: -fallRot * 0.9 });
    // fireball from Seraphine's staff
    if (t >= B && t < F + 0.05) {
      const p = clamp((t - B) / (F - B));
      const x = lerp(sh[0], 520, p * p), y = lerp(sh[1], 1440, p * p), r = lerp(20, 110, p);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let i = 1; i < 14; i++) { const q = clamp(p - i * 0.03); glow(lerp(sh[0], 520, q * q), lerp(sh[1], 1440, q * q), r * (1 - i / 16), 'rgba(255,110,40,A)', 0.4); }
      glow(x, y, r * 3, 'rgba(255,120,50,A)', 0.9); glow(x, y, r * 0.6, 'rgba(255,240,200,A)', 1);
      ctx.restore();
      lightning(sh[0], sh[1], x, y, Math.floor(t * 20), 2, 'rgba(255,150,80,A)');
    }
    if (t > F) {
      const k = Math.exp(-(t - F) * 1.4);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      glow(520, 1440, 900, 'rgba(255,120,60,A)', k); glow(520, 1440, 200, 'rgba(255,240,220,A)', k);
      ctx.restore();
      particles(t, 90, { y0: 1600, dy: -1400, x0: 200, w: 650, a: k, color: 'rgba(255,160,80,A)', r: 3, life: 2.5, sway: 150 });
    }
  },

  abschied(t) {
    const lt = local('abschied', t), d = SC.abschied.end - SC.abschied.start;
    camera(1.0 + 0.14 * lt / d, 0, -60 * lt / d);
    vgrad([[0, '#04050c'], [0.5, '#141a33'], [0.72, '#2c2a40'], [1, '#06060c']]);
    stars(t, { alpha: 0.55, h: 1000 });
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(560, 1240, 760, 'rgba(255,190,140,A)', 0.3);
    glow(560, 1240, 300, 'rgba(255,220,190,A)', 0.25);
    ctx.restore();
    ground(1560, '#05050a', 10, 4);
    particles(t, 110, { y0: -50, dy: 1900, a: 0.55, color: 'rgba(210,225,255,A)', r: 2.2, life: 14, sway: 40 });
    const c = '#05050a';
    // Kael lying across her lap (head right)
    ctx.fillStyle = c; ctx.shadowColor = 'rgba(255,170,120,0.7)'; ctx.shadowBlur = 24;
    ctx.beginPath(); ctx.moveTo(200, 1580); ctx.bezierCurveTo(240, 1510, 420, 1480, 610, 1470);
    ctx.bezierCurveTo(680, 1462, 720, 1440, 740, 1430); ctx.lineTo(760, 1480); ctx.bezierCurveTo(600, 1540, 380, 1560, 200, 1580); ctx.fill();
    ctx.beginPath(); ctx.ellipse(780, 1420, 36, 42, 0.5, 0, 7); ctx.fill();
    // Elara kneeling, bent over him
    ctx.beginPath(); ctx.moveTo(420, 1580); ctx.bezierCurveTo(430, 1440, 470, 1300, 560, 1230);
    ctx.bezierCurveTo(620, 1185, 690, 1190, 720, 1240); ctx.bezierCurveTo(720, 1300, 700, 1400, 700, 1480); ctx.lineTo(760, 1590); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.ellipse(735, 1268, 40, 48, 0.9, 0, 7); ctx.fill();
    ctx.beginPath(); ctx.moveTo(570, 1225); ctx.bezierCurveTo(480, 1260, 440, 1380, 400, 1470); ctx.lineTo(440, 1470); ctx.bezierCurveTo(480, 1380, 540, 1290, 600, 1240); ctx.fill();
    // his hand rises to her face and falls
    const armL = lineOf('abschied', 3);
    const fallK = smooth(armL.end - 0.2, armL.end + 0.6, t), up = smooth(SC.abschied.start + 0.5, SC.abschied.start + 3, t);
    const ang = lerp(lerp(-0.2, -1.75, up), 0.95, fallK);
    ctx.lineCap = 'round'; ctx.lineWidth = 22; ctx.strokeStyle = c;
    ctx.beginPath(); ctx.moveTo(690, 1460); ctx.lineTo(690 + Math.cos(ang) * 150, 1460 + Math.sin(ang) * 150); ctx.stroke();
    ctx.shadowBlur = 0;
    // her glowing hand on his chest
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(600, 1475, 140 + 20 * Math.sin(t * 2.5), 'rgba(190,220,255,A)', 0.8); glow(600, 1475, 18, 'rgba(255,255,255,A)', 0.9);
    ctx.restore();
    ctx.fillStyle = '#030306'; ctx.fillRect(-200, 1620, W + 400, 600);
  },

  erwachen(t) {
    const lt = local('erwachen', t), d = SC.erwachen.end - SC.erwachen.start;
    const black = smooth(CUE.schwarz - 0.5, CUE.schwarz + 1.5, t);
    camera(1.05 + 0.1 * lt / d, 0, 30);
    vgrad([[0, '#020104'], [0.5, `rgb(${16 + 30 * black},6,${24 + 10 * black})`], [0.72, `rgb(${40 + 60 * black},16,40)`], [1, '#040208']]);
    stars(t, { alpha: 1, h: 1200 });
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(540, 860, 900, 'rgba(140,60,255,A)', 0.25 * black);
    ctx.restore();
    ground(1660, '#040307', 16, 9);
    // the Order recoils in the distance
    for (let i = 0; i < 6; i++) {
      const x = 90 + i * 180 + (i > 2 ? 40 : -40), back = smooth(CUE.schwarz, CUE.schwarz + 2, t) * 60;
      figure(x + (x < 540 ? -back : back), 1670, 150, { hood: true, t: t + i, dir: x < 540 ? 1 : -1, color: '#060409', rim: 'rgba(160,80,255,0.4)', rimBlur: 10 });
    }
    // Elara, low angle, hand raised with the star heart
    const hand = figure(540, 1880, 980, { hair: true, t, wind: 6 * black, rim: `rgba(${lerp(170, 160, black)},${lerp(205, 70, black)},255,0.95)`, rimBlur: 50, arm: -0.75, armLen: 36 });
    // dark tendrils
    if (black > 0) {
      ctx.save(); ctx.lineCap = 'round';
      for (let k = 0; k < 14; k++) {
        const a = k / 14 * 6.283 + Math.sin(t * 0.7 + k) * 0.4, L = 500 * black * (0.6 + rnd(k, 90) * 0.6);
        ctx.strokeStyle = `rgba(120,40,220,${0.35 * black})`; ctx.lineWidth = 20 * (1 - k / 20);
        ctx.shadowColor = 'rgba(150,60,255,1)'; ctx.shadowBlur = 30;
        ctx.beginPath(); ctx.moveTo(hand[0], hand[1]);
        ctx.bezierCurveTo(hand[0] + Math.cos(a + 0.8) * L * 0.4, hand[1] + Math.sin(a + 0.8) * L * 0.4, hand[0] + Math.cos(a - 0.5 + Math.sin(t + k)) * L * 0.7, hand[1] + Math.sin(a - 0.5) * L * 0.7, hand[0] + Math.cos(a) * L, hand[1] + Math.sin(a) * L);
        ctx.stroke();
      }
      ctx.restore();
    }
    heart(hand[0], hand[1], 30, t, { pulse: 0.3 + 0.4 * black, col: black > 0.5 ? '170,90,255' : '200,225,255', dark: black });
    runeRing(hand[0], hand[1], 180, t, 0.8 * black, 'rgba(170,90,255,A)', 22, -1);
    particles(t, 70, { y0: 1900, dy: -1900, a: 0.6, color: black > 0.5 ? 'rgba(170,90,255,A)' : 'rgba(190,215,255,A)', r: 2.5, life: 5, sway: 80 });
  },

  letzter(t) {
    const lt = local('letzter', t), d = SC.letzter.end - SC.letzter.start;
    camera(1.0 + 0.35 * easeInOut(lt / d), 0, 330 * easeInOut(lt / d));
    vgrad([[0, '#000000'], [0.7, '#05040a'], [1, '#09070f']]);
    stars(t, { alpha: 1 });
    const mom = LINES.find(l => l.who === 'MUTTER');
    const m = smooth(mom.start - 1.5, mom.start + 1, t), sp = speaking('MUTTER', t);
    const x = STARS[0].x * W, y = STARS[0].y * H, sis = smooth(CUE.schwester, CUE.schwester + 0.5, t);
    const col = sis > 0.5 ? 'rgba(170,80,255,A)' : 'rgba(255,205,140,A)';
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(x, y, 150 + 450 * m + 60 * sp, col, (0.5 + 0.3 * m) * (sis > 0 && sis < 1 ? 0.5 + 0.5 * Math.sin(t * 40) : 1));
    glow(x, y, 20 + 30 * m, 'rgba(255,245,225,A)', 1);
    ctx.restore();
    if (sis > 0) {
      for (let k = 0; k < 9; k++) {
        const a = k / 9 * 6.283 + rnd(k, 3), L = 380 * sis * (0.5 + rnd(k, 4));
        lightning(x, y, x + Math.cos(a) * L, y + Math.sin(a) * L, 900 + k * 13, 1.6, 'rgba(190,110,255,A)');
      }
    }
    if (m > 0 && sis < 1) {
      // faint golden outline of a woman inside the star
      ctx.save(); ctx.globalAlpha = (0.35 * m + 0.15 * sp) * (1 - sis); ctx.globalCompositeOperation = 'lighter';
      figure(x, y + 150, 300, { hair: true, t, color: 'rgba(255,200,130,0.25)', rim: 'rgba(255,200,120,1)', rimBlur: 30, arm: -1.2 });
      ctx.restore();
    }
    ground(1700, '#050409', 8, 2);
    figure(540, 1712, 250, { hair: true, t, rim: 'rgba(255,200,140,0.6)', rimBlur: 16, arm: -1.2, armLen: 30 });
  },

  ende(t) {
    // Elara: half human, half star - veins of starlight, one glowing eye
    const lt = local('ende', t), d = SC.ende.end - SC.ende.start;
    camera(1.0 + 0.25 * easeInOut(lt / d), 60 * easeInOut(lt / d), 200 * easeInOut(lt / d));
    vgrad([[0, '#010003'], [0.6, '#12061e'], [1, '#05020a']]);
    stars(t, { alpha: 1 });
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(STARS[0].x * W, STARS[0].y * H, 200, 'rgba(170,90,255,A)', 0.5); ctx.restore();
    ground(1700, '#040208', 12, 5);
    const x = 540, y = 1720, h = 900, s2 = h / 100;
    const hand = figure(x, y, h, { hair: true, t, wind: 4, rim: 'rgba(160,80,255,0.9)', rimBlur: 40, arm: 0.55, armLen: 34 });
    heart(hand[0], hand[1], 22, t, { pulse: 0.4, col: '170,90,255', dark: 1 });
    const v = smooth(0.4, d - 1.2, lt);
    if (v > 0) {
      const pts = [[x + 2 * s2, y - 60 * s2], [x - 6 * s2, y - 30 * s2], [x + 8 * s2, y - 76 * s2], [x - 4 * s2, y - 80 * s2]];
      pts.forEach(([px, py], k) => {
        const qx = lerp(hand[0], px, v), qy = lerp(hand[1], py, v);
        lightning(hand[0], hand[1], qx, qy, 400 + k * 17 + Math.floor(t * 3), 1.0, 'rgba(255,215,150,A)');
      });
    }
    const eye = smooth(lineOf('ende', 1).start + 0.6, lineOf('ende', 1).end, t);
    if (eye > 0) {
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      glow(x + 4 * s2, y - 93.5 * s2, 60 * eye, 'rgba(255,210,140,A)', eye); glow(x + 4 * s2, y - 93.5 * s2, 8, 'rgba(255,250,230,A)', eye);
      ctx.restore();
    }
    particles(t, 80, { y0: 1900, dy: -1900, a: 0.6, color: 'rgba(200,140,255,A)', r: 2.2, life: 5 });
  },

  sting(t) {
    const lt = local('sting', t), d = SC.sting.end - SC.sting.start;
    vgrad([[0, '#000000'], [1, '#050002']]);
    const a = smooth(0.3, 2.5, lt);
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(540, 820, 700, 'rgba(160,20,20,A)', 0.35 * a); ctx.restore();
    // Seraphine's hooded head, close, from the dark
    ctx.save(); ctx.translate(560, 1500); const z = 1 + 0.06 * lt; ctx.scale(z, z);
    ctx.fillStyle = '#030001'; ctx.shadowColor = `rgba(255,60,40,${0.9 * a})`; ctx.shadowBlur = 50;
    ctx.beginPath(); ctx.moveTo(-430, 500); ctx.bezierCurveTo(-400, 100, -330, -420, -60, -640);
    ctx.bezierCurveTo(10, -700, 120, -690, 190, -620); ctx.bezierCurveTo(380, -420, 420, 100, 450, 500); ctx.closePath(); ctx.fill();
    ctx.shadowBlur = 0;
    ctx.globalCompositeOperation = 'lighter';
    [-70, 70].forEach(ex => glow(ex, -260, 40, 'rgba(255,90,60,A)', 0.5 * smooth(1.2, 2.2, lt)));
    ctx.restore();
  },

  abspann(t) {
    const lt = local('abspann', t), hit = CUE.end_hit - SC.abspann.start;
    vgrad([[0, '#010103'], [1, '#05040c']]);
    stars(t, { alpha: 0.35, noLast: true, drift: 1 });
    emblem(540, 860, 330, t, easeInOut(clamp(lt / hit)), 0.5);
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(540, 860, 520, 'rgba(255,190,110,A)', 0.2 + 0.2 * smooth(hit, hit + 0.3, lt)); ctx.restore();
    titleText(540, 860, 104, smooth(0.2, 1.2, lt), 1.06 - 0.06 * easeOut(lt / 5));
    ctx.save(); ctx.textAlign = 'center'; ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 12;
    ctx.font = 'italic 600 66px "Cormorant Garamond"'; ctx.fillStyle = `rgba(240,230,215,${smooth(hit, hit + 0.6, lt)})`;
    ctx.fillText('Fortsetzung folgt …', 540, 1300);
    if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '6px';
    ctx.font = '400 34px Cinzel'; ctx.fillStyle = `rgba(210,185,150,${smooth(hit + 0.8, hit + 1.6, lt)})`;
    ctx.fillText('FOLGE 2 · DIE STADT OHNE STERNE', 540, 1390);
    ctx.restore();
    particles(t, 50, { y0: 1700, dy: -1300, a: 0.5, color: 'rgba(255,190,120,A)', r: 2, life: 6 });
  },
};

// ---------- overlays ----------
const SPEAKER_COL = { LUNARA: '#a8c8ff', KAEL_ERINNERUNG: '#ffc09a', SERAPHINE_HALLE: '#ff6f6f', KAEL: '#ff9b78', SERAPHINE: '#ff6f6f', STERN: '#d9e6ff', STERN_DUNKEL: '#c08cff', MUTTER: '#ffd59a' };

function wrap(text, maxW) {
  const words = text.split(' '), out = [];
  let cur = '';
  for (const w of words) {
    const test = cur ? cur + ' ' + w : w;
    if (ctx.measureText(test).width > maxW && cur) { out.push(cur); cur = w; } else cur = test;
  }
  if (cur) out.push(cur);
  return out;
}

function subtitles(t) {
  const l = LINES.find(l => t >= l.start - 0.12 && t <= l.end + 0.35);
  if (!l) return;
  const a = smooth(l.start - 0.12, l.start + 0.08, t) * (1 - smooth(l.end + 0.1, l.end + 0.35, t));
  const narr = l.who === 'ICH';
  ctx.save();
  ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  ctx.font = narr ? 'italic 500 58px "Cormorant Garamond"' : '600 60px "Cormorant Garamond"';
  const lines = wrap(l.text, 900);
  const lh = 68, y0 = 1460 - (lines.length - 1) * lh / 2;
  const band = ctx.createLinearGradient(0, y0 - 190, 0, y0 + lines.length * lh + 80);
  band.addColorStop(0, 'rgba(0,0,0,0)'); band.addColorStop(0.35, `rgba(0,0,0,${0.5 * a})`);
  band.addColorStop(0.75, `rgba(0,0,0,${0.5 * a})`); band.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = band; ctx.fillRect(0, y0 - 190, W, lines.length * lh + 270);
  ctx.shadowColor = 'rgba(0,0,0,0.95)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 2;
  if (!narr) {
    if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '5px';
    ctx.font = '700 34px Cinzel'; ctx.fillStyle = (SPEAKER_COL[l.who] ?? '#fff') + Math.round(a * 255).toString(16).padStart(2, '0');
    ctx.fillText(l.label.toUpperCase(), 540, y0 - 72);
    if (ctx.letterSpacing !== undefined) ctx.letterSpacing = '0px';
    ctx.font = '600 60px "Cormorant Garamond"';
  }
  ctx.fillStyle = narr ? `rgba(235,228,214,${a})` : `rgba(255,255,255,${a})`;
  lines.forEach((s, i) => { ctx.fillText(s, 540, y0 + i * lh); ctx.fillText(s, 540, y0 + i * lh); });
  ctx.restore();
}

function overlays(t, frame) {
  // vignette
  const g = ctx.createRadialGradient(W / 2, H / 2, H * 0.25, W / 2, H / 2, H * 0.75);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.6)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  // flashes
  const flash = (c, col, dur, amp = 1) => { if (t >= c && t < c + dur) { ctx.fillStyle = col.replace('A', amp * Math.pow(1 - (t - c) / dur, 2)); ctx.fillRect(0, 0, W, H); } };
  flash(CUE.impact, 'rgba(235,242,255,A)', 1.0);
  flash(CUE.touch, 'rgba(225,235,255,A)', 0.9);
  flash(CUE.fallen, 'rgba(255,190,140,A)', 1.1, 0.9);
  flash(CUE.schwarz, 'rgba(120,40,200,A)', 0.8, 0.6);
  flash(CUE.title_hit, 'rgba(255,225,180,A)', 0.8, 0.85);
  flash(CUE.schwester, 'rgba(150,60,255,A)', 0.6, 0.5);
  flash(CUE.outro_hit, 'rgba(255,225,180,A)', 0.7, 0.5);
  flash(lineOf('orden', 2).start + 0.2, 'rgba(255,70,40,A)', 0.5, 0.35);
  // dip to black between scenes
  for (const s of TL.scenes.slice(1)) {
    const dd = Math.abs(t - s.start);
    if (dd < 0.4 && !['fall', 'angriff', 'intro', 'glocken'].includes(s.id)) { ctx.fillStyle = `rgba(0,0,0,${1 - smooth(0, 0.4, dd)})`; ctx.fillRect(0, 0, W, H); }
  }
  const fi = 1 - smooth(0, 0.8, t);
  if (fi > 0) { ctx.fillStyle = `rgba(0,0,0,${fi})`; ctx.fillRect(0, 0, W, H); }
  const fo = smooth(TL.duration - 0.8, TL.duration, t);
  if (fo > 0) { ctx.fillStyle = `rgba(0,0,0,${fo})`; ctx.fillRect(0, 0, W, H); }
  captions(t);
  subtitles(t);
  // film grain
  ctx.globalAlpha = 0.07; ctx.globalCompositeOperation = 'overlay';
  ctx.drawImage(grain[frame % grain.length], 0, 0, W, H);
  ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
}

function shakeAt(t) {
  let s = 0;
  [[CUE.impact, 1.3, 22], [CUE.touch, 1.0, 16], [CUE.fallen, 1.2, 24], [CUE.schwarz, 0.8, 12], [CUE.title_hit, 0.9, 18], [CUE.schwester, 0.8, 14], [SC.sting.start - 0.05, 0.5, 10], [lineOf('orden', 2).start + 0.2, 0.7, 12], [CUE.outro_hit, 0.8, 12]].forEach(([c, d, a]) => {
    if (t >= c && t < c + d) s += a * Math.pow(1 - (t - c) / d, 2);
  });
  return s;
}

window.setup = (timeline) => {
  TL = timeline; CUE = TL.cues; LINES = TL.lines;
  SC = Object.fromEntries(TL.scenes.map(s => [s.id, s]));
  const cv = document.getElementById('c');
  ctx = cv.getContext('2d');
  for (let i = 0; i < 6; i++) {
    const g = document.createElement('canvas'); g.width = 540; g.height = 960;
    const gc = g.getContext('2d'), img = gc.createImageData(540, 960);
    for (let p = 0; p < img.data.length; p += 4) { const v = Math.random() * 255; img.data[p] = img.data[p + 1] = img.data[p + 2] = v; img.data[p + 3] = 255; }
    gc.putImageData(img, 0, 0); grain.push(g);
  }
};

window.draw = (t, frame = 0) => {
  const scene = TL.scenes.find(s => t >= s.start && t < s.end) ?? TL.scenes[TL.scenes.length - 1];
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
  ctx.save();
  const s = shakeAt(t);
  if (s) ctx.translate(Math.sin(t * 71) * s, Math.cos(t * 53) * s);
  SCENES[scene.id](t);
  ctx.restore();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  overlays(t, frame);
};
