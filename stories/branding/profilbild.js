// Profilbild "Leben in Valdoria" (rund gedacht): Vollmond, Laternen, Lunara und ein Himmelswal im sicheren Kreis.
// Usage: NODE_PATH=$(npm root -g) node branding/profilbild.js  -> branding/profilbild.png (1080x1080)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(__dirname, '../engine/render.html'));
  await page.evaluate(() => document.fonts.ready);
  const [url, round] = await page.evaluate(() => {
    window.setup({ scenes: [{ id: 'x', start: 0, end: 99 }], lines: [], cues: {}, duration: 99 });
    const t = 7.3, cv = document.getElementById('c'), c = cv.getContext('2d');
    c.setTransform(1, 0, 0, 1, 0, 0);
    // night sky over the cloud sea
    vgrad([[0, '#02030d'], [0.25, '#0a1233'], [0.5, '#1c2a5a'], [0.62, '#3a4a7e'], [0.8, '#1a2048'], [1, '#0c1028']]);
    stars(t, { alpha: 1 });
    c.save(); c.globalCompositeOperation = 'lighter';
    glow(540, 850, 560, 'rgba(170,195,255,A)', 0.45);
    glow(770, 660, 100, 'rgba(255,225,180,A)', 0.6); glow(770, 660, 14, 'rgba(255,250,235,A)', 1);
    c.strokeStyle = 'rgba(255,240,215,0.55)'; c.lineWidth = 2.5;
    for (let k = 0; k < 4; k++) { const a = k * Math.PI / 4 + 0.2, r = 52; c.beginPath(); c.moveTo(770 - Math.cos(a) * r, 660 - Math.sin(a) * r); c.lineTo(770 + Math.cos(a) * r, 660 + Math.sin(a) * r); c.stroke(); }
    c.restore();
    moon(540, 850, 205);
    whale(340, 700, 0.27, t, 0.6, 1);
    cloudSea(t, 1300, 0.95);
    c.save(); c.globalCompositeOperation = 'lighter'; glow(540, 1340, 600, 'rgba(170,200,255,A)', 0.25); c.restore();
    // branch from the right, crossing in front of the moon
    const col = '#04050c';
    c.fillStyle = col;
    c.beginPath(); c.moveTo(1200, 1010); c.bezierCurveTo(900, 1040, 520, 1092, 150, 1086); c.quadraticCurveTo(130, 1090, 150, 1100);
    c.bezierCurveTo(520, 1118, 900, 1080, 1200, 1080); c.fill();
    [[300, 1092, 70], [760, 1080, 110], [980, 1056, 60]].forEach(([vx, vy, len], k) => {
      c.strokeStyle = col; c.lineWidth = 2; c.beginPath(); c.moveTo(vx, vy); c.quadraticCurveTo(vx + 3, vy + len / 2, vx + 6, vy + len); c.stroke();
      for (let j = 1; j <= 4; j++) { c.beginPath(); c.ellipse(vx + 6 * j / 4 + (j % 2 ? 5 : -5), vy + len * j / 4.5, 3.5, 8, j % 2 ? 0.7 : -0.7, 0, 7); c.fill(); }
    });
    c.save(); c.strokeStyle = 'rgba(175,200,255,0.5)'; c.lineWidth = 2.5;
    c.beginPath(); c.moveTo(1200, 1011); c.bezierCurveTo(900, 1041, 520, 1093, 150, 1087); c.stroke(); c.restore();
    // lanterns hanging from the branch
    [[300, 1093, 70], [520, 1090, 105], [690, 1082, 60], [930, 1060, 85]].forEach(([lx, by, len]) => {
      c.strokeStyle = col; c.lineWidth = 2; c.beginPath(); c.moveTo(lx, by); c.lineTo(lx, by + len); c.stroke();
      c.fillStyle = col; c.fillRect(lx - 12, by + len, 24, 6); c.fillRect(lx - 10, by + len + 30, 20, 5);
      c.save(); c.globalCompositeOperation = 'lighter'; glow(lx, by + len + 18, 85, 'rgba(255,170,90,A)', 0.6); glow(lx, by + len + 18, 12, 'rgba(255,225,170,A)', 1); c.restore();
    });
    // Lunara on the branch in front of the moon
    moonMouse(815, 1036, 40, t, { dir: -1, mood: 'happy', fly: false, seed: 0.4 });
    particles(t, 40, { y0: 1500, dy: -1100, a: 0.5, color: 'rgba(200,220,255,A)', r: 2, life: 9, glowR: 6 });
    // crop to the square around the subject
    const sq = document.createElement('canvas'); sq.width = 1080; sq.height = 1080;
    sq.getContext('2d').drawImage(cv, 0, 380, 1080, 1080, 0, 0, 1080, 1080);
    const rd = document.createElement('canvas'); rd.width = 1080; rd.height = 1080;
    const r2 = rd.getContext('2d'); r2.beginPath(); r2.arc(540, 540, 540, 0, 7); r2.clip(); r2.drawImage(sq, 0, 0);
    return [sq.toDataURL('image/png'), rd.toDataURL('image/png')];
  });
  fs.writeFileSync(path.join(__dirname, 'profilbild.png'), Buffer.from(url.split(',')[1], 'base64'));
  fs.writeFileSync(path.join(__dirname, 'profilbild_rund_vorschau.png'), Buffer.from(round.split(',')[1], 'base64'));
  await browser.close();
  console.log('profilbild.png');
})();
