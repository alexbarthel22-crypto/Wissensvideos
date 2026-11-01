// Einheitliches Thumbnail (1080x1920) für jede Sternenfall-Folge.
// Usage: NODE_PATH=$(npm root -g) node branding/thumbnail.js story/folge01.json  -> branding/thumbs/folge01.png
// Gleiches Layout für alle Folgen: Serientitel oben, Bildmitte mit kleinen Story-Elementen,
// "FOLGE N" als Goldband, Folgentitel darunter. Alles im mittleren 3:4-Bereich (TikTok-Profilraster).
// Welche Elemente erscheinen, steht im Folgen-JSON unter "thumbnail": {"elements": [...]}.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const storyPath = path.resolve(process.argv[2]);
const story = JSON.parse(fs.readFileSync(storyPath, 'utf8'));
const name = path.basename(storyPath, '.json');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(__dirname, '../engine/render.html'));
  await page.evaluate(() => document.fonts.ready);
  const url = await page.evaluate((st) => {
    window.setup({ scenes: [{ id: 'x', start: 0, end: 99 }], lines: [], cues: {}, duration: 99 });
    const t = 5.2, c = document.getElementById('c').getContext('2d');
    c.setTransform(1, 0, 0, 1, 0, 0);
    const els = new Set((st.thumbnail && st.thumbnail.elements) || []);
    // --- background, identical for every episode
    vgrad([[0, '#02030d'], [0.3, '#0a1233'], [0.55, '#1c2a5a'], [0.72, '#3a3a78'], [0.86, '#1a1440'], [1, '#05040f']]);
    nebula(t, ['rgba(110,60,200,A)', 'rgba(40,120,200,A)', 'rgba(200,80,140,A)'], 0.9);
    stars(t, { alpha: 1 });
    // --- story elements (centre stage, y ~ 560 to 1250)
    if (els.has('moon')) moon(540, 820, 175);
    if (els.has('trees')) {
      giantTree(20, 170, 230, t, 0.5, 62, { lights: 16, lightSpan: 900, lightA: 0.9 });
      giantTree(1060, 180, 210, t, 0.55, 61, { lights: 18, lightSpan: 900, lightA: 0.9 });
    }
    if (els.has('whale')) whale(330, 640, 0.3, t, 0.6, 1);
    if (els.has('fallingStar')) {
      c.save(); c.globalCompositeOperation = 'lighter';
      for (let i = 0; i < 40; i++) { const q = 1 - i / 40; glow(lerp(1000, 640, q), lerp(420, 900, q), 34 * q + 4, 'rgba(200,225,255,A)', 0.55 * q); }
      glow(640, 900, 120, 'rgba(210,230,255,A)', 0.9); glow(640, 900, 20, 'rgba(255,255,255,A)', 1);
      c.restore();
    }
    if (els.has('stoneTrees')) [[70, 1250, 820, 1], [230, 1250, 620, 2], [870, 1250, 700, 3], [1020, 1250, 560, 4]].forEach(([x, b, h, sd]) => stoneTree(x, b, h, sd, '#0c0e1a'));
    if (els.has('whaleBones')) whaleBones(800, 1240, 0.9, '#2a3048');
    if (els.has('heart')) {
      c.save(); c.globalCompositeOperation = 'lighter'; glow(540, 880, 520, 'rgba(120,160,255,A)', 0.55); c.restore();
      heart(540, 880, 46, t, { pulse: 0.6 });
    }
    if (els.has('cloudSea')) cloudSea(t, 1180, 0.9);
    if (els.has('pendant')) pendant(250, 1090, 95, t, { angle: -0.9 });
    if (els.has('ramen')) {
      const bx = 760, by = 1215;
      c.save(); c.globalCompositeOperation = 'lighter'; glow(bx, by - 10, 120, 'rgba(255,190,120,A)', 0.5); c.restore();
      c.fillStyle = '#1b1430';
      c.beginPath(); c.moveTo(bx - 60, by - 40); c.quadraticCurveTo(bx - 55, by + 5, bx, by + 8); c.quadraticCurveTo(bx + 55, by + 5, bx + 60, by - 40); c.fill();
      c.fillRect(bx - 18, by + 5, 36, 8);
      c.strokeStyle = '#c0453a'; c.lineWidth = 6; c.beginPath(); c.moveTo(bx - 56, by - 28); c.quadraticCurveTo(bx, by - 16, bx + 56, by - 28); c.stroke();
      c.fillStyle = '#e8a85a'; c.beginPath(); c.ellipse(bx, by - 40, 60, 13, 0, 0, 7); c.fill();
      c.strokeStyle = '#fbe7b0'; c.lineWidth = 3.5;
      for (let k = 0; k < 6; k++) { c.beginPath(); c.moveTo(bx - 46 + k * 9, by - 42); c.bezierCurveTo(bx - 37 + k * 9, by - 52, bx - 26 + k * 9, by - 32, bx - 14 + k * 9, by - 42); c.stroke(); }
      c.fillStyle = '#fff6e0'; c.beginPath(); c.ellipse(bx + 26, by - 44, 13, 7, -0.2, 0, 7); c.fill();
      c.fillStyle = '#ffb92e'; c.beginPath(); c.ellipse(bx + 27, by - 44, 6, 4, -0.2, 0, 7); c.fill();
      c.strokeStyle = '#d9a86a'; c.lineWidth = 5; c.lineCap = 'round';
      c.beginPath(); c.moveTo(bx - 16, by - 42); c.lineTo(bx + 54, by - 122); c.moveTo(bx - 4, by - 40); c.lineTo(bx + 68, by - 112); c.stroke();
      c.lineWidth = 6;
      for (let k = 0; k < 3; k++) { const x0 = bx - 26 + k * 24; c.strokeStyle = `rgba(240,240,255,${0.55 - k * 0.1})`; c.beginPath(); c.moveTo(x0, by - 58); c.bezierCurveTo(x0 - 16, by - 88, x0 + 16, by - 110, x0, by - 140); c.stroke(); }
    }
    if (els.has('lunara')) moonMouse(620, 1180, 34, t, { dir: 1, mood: 'happy', fly: true, seed: 0.4 });
    particles(t, 40, { y0: 1500, dy: -1100, a: 0.5, color: 'rgba(255,200,140,A)', r: 2, life: 9, glowR: 6 });
    // soft darkening behind the text blocks
    const shade = (y, h) => { const g = c.createLinearGradient(0, y - h, 0, y + h); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(0.5, 'rgba(2,3,12,0.75)'); g.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = g; c.fillRect(0, y - h, 1080, 2 * h); };
    shade(400, 150); shade(1440, 300);
    // --- identical text layout for every episode
    titleText(540, 400, 104, 1, 1);
    c.save(); c.textAlign = 'center';
    c.fillStyle = 'rgba(230,190,120,0.9)'; c.fillRect(300, 470, 480, 2);
    c.font = 'italic 600 40px "Cormorant Garamond"'; c.fillStyle = 'rgba(240,230,215,0.95)';
    c.shadowColor = 'rgba(0,0,0,0.9)'; c.shadowBlur = 12;
    c.fillText(st.tagline || '', 540, 520);
    // gold band with the episode number
    const bw = 820, bh = 210, by0 = 1250;
    const bg = c.createLinearGradient(0, by0, 0, by0 + bh);
    bg.addColorStop(0, '#f7dc9b'); bg.addColorStop(0.5, '#e2a94e'); bg.addColorStop(1, '#a8702c');
    c.shadowColor = 'rgba(255,170,70,0.8)'; c.shadowBlur = 40;
    c.fillStyle = bg; c.beginPath(); c.roundRect(540 - bw / 2, by0, bw, bh, bh / 2); c.fill();
    c.shadowBlur = 0; c.strokeStyle = 'rgba(255,240,200,0.95)'; c.lineWidth = 5; c.stroke();
    if (c.letterSpacing !== undefined) c.letterSpacing = '10px';
    c.font = '700 150px Cinzel'; c.fillStyle = '#2a1606'; c.textBaseline = 'middle';
    c.fillText((st.folge || '').toUpperCase(), 548, by0 + bh / 2 + 10);
    if (c.letterSpacing !== undefined) c.letterSpacing = '0px';
    // episode title
    c.textBaseline = 'alphabetic'; c.font = 'italic 700 86px "Cormorant Garamond"';
    c.shadowColor = 'rgba(0,0,0,0.95)'; c.shadowBlur = 18;
    const tg = c.createLinearGradient(0, 1500, 0, 1660); tg.addColorStop(0, '#fff6e6'); tg.addColorStop(1, '#ffd79a');
    c.fillStyle = tg;
    wrap(st.titel || '', 940).forEach((ln, i) => c.fillText(ln, 540, 1580 + i * 92));
    c.restore();
    return document.getElementById('c').toDataURL('image/png');
  }, story);
  fs.mkdirSync(path.join(__dirname, 'thumbs'), { recursive: true });
  fs.writeFileSync(path.join(__dirname, 'thumbs', name + '.png'), Buffer.from(url.split(',')[1], 'base64'));
  await browser.close();
  console.log('thumbs/' + name + '.png');
})();
