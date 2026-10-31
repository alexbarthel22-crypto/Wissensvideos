// Profilbild "Leben in Valdoria": nur der Vollmond als rundes Bild, davor ein Himmelswal und Lunara.
// Usage: NODE_PATH=$(npm root -g) node branding/profilbild_mond.js -> branding/profilbild.png + profilbild_rund_vorschau.png
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(__dirname, '../engine/render.html'));
  await page.evaluate(() => document.fonts.ready);
  const [sqUrl, rdUrl] = await page.evaluate(() => {
    window.setup({ scenes: [{ id: 'x', start: 0, end: 99 }], lines: [], cues: {}, duration: 99 });
    const t = 7.3, cv = document.getElementById('c'), c = cv.getContext('2d');
    c.setTransform(1, 0, 0, 1, 0, 0);
    // deep night around the moon (only visible as a thin rim in the circle)
    vgrad([[0, '#05081c'], [1, '#0b1030']]);
    stars(t, { alpha: 1 });
    c.save(); c.globalCompositeOperation = 'lighter'; glow(540, 960, 760, 'rgba(170,195,255,A)', 0.55); c.restore();
    // the full moon filling the frame
    moon(540, 960, 505);
    // lunar surface: dark maria, many craters with lit rims, fine grain (all clipped to the disc)
    c.save(); c.beginPath(); c.arc(540, 960, 505, 0, 7); c.clip();
    const R = (i, k) => rnd(i, 1300 + k);
    // maria: soft irregular grey-blue seas made of overlapping blobs
    [[400, 800, 170], [600, 760, 120], [690, 900, 150], [450, 1050, 130], [700, 1120, 110], [330, 960, 90]].forEach(([mx, my, mr], m) => {
      for (let j = 0; j < 9; j++) {
        const x = mx + (R(m * 20 + j, 1) - 0.5) * mr, y = my + (R(m * 20 + j, 2) - 0.5) * mr * 0.8, r = mr * (0.35 + 0.45 * R(m * 20 + j, 3));
        const g = c.createRadialGradient(x, y, 0, x, y, r);
        g.addColorStop(0, 'rgba(120,128,160,0.20)'); g.addColorStop(1, 'rgba(120,128,160,0)');
        c.fillStyle = g; c.beginPath(); c.arc(x, y, r, 0, 7); c.fill();
      }
    });
    // craters: dark floor, shadowed upper-left wall, bright lower-right rim
    for (let i = 0; i < 70; i++) {
      const a = R(i, 4) * 6.283, d = Math.sqrt(R(i, 5)) * 470, x = 540 + Math.cos(a) * d, y = 960 + Math.sin(a) * d;
      const r = i < 6 ? 34 + 30 * R(i, 6) : 5 + 16 * R(i, 6) ** 2;
      c.fillStyle = 'rgba(110,116,150,0.22)'; c.beginPath(); c.arc(x, y, r, 0, 7); c.fill();
      c.strokeStyle = 'rgba(80,86,125,0.35)'; c.lineWidth = Math.max(1.2, r * 0.18);
      c.beginPath(); c.arc(x, y, r * 0.9, Math.PI * 0.9, Math.PI * 1.75); c.stroke();
      c.strokeStyle = 'rgba(255,255,255,0.45)'; c.lineWidth = Math.max(1, r * 0.12);
      c.beginPath(); c.arc(x, y, r * 1.02, Math.PI * -0.15, Math.PI * 0.7); c.stroke();
      if (i < 3) { // ray craters
        c.strokeStyle = 'rgba(255,255,255,0.10)'; c.lineWidth = 3;
        for (let k = 0; k < 12; k++) { const b = k / 12 * 6.283 + R(i, 7); c.beginPath(); c.moveTo(x + Math.cos(b) * r, y + Math.sin(b) * r); c.lineTo(x + Math.cos(b) * r * (4 + 3 * R(i * 12 + k, 8)), y + Math.sin(b) * r * (4 + 3 * R(i * 12 + k, 8))); c.stroke(); }
      }
    }
    // fine grain
    for (let i = 0; i < 2600; i++) {
      const a = R(i, 9) * 6.283, d = Math.sqrt(R(i, 10)) * 505;
      c.fillStyle = R(i, 11) > 0.5 ? 'rgba(90,96,130,0.10)' : 'rgba(255,255,255,0.10)';
      c.fillRect(540 + Math.cos(a) * d, 960 + Math.sin(a) * d, 2, 2);
    }
    c.restore();
    // gentle blue shading so the white mouse stands out
    const sh = c.createRadialGradient(470, 860, 120, 540, 960, 520);
    sh.addColorStop(0, 'rgba(255,255,255,0)'); sh.addColorStop(1, 'rgba(60,80,150,0.38)');
    c.fillStyle = sh; c.beginPath(); c.arc(540, 960, 505, 0, 7); c.fill();
    // sky whale gliding across the moon
    whale(560, 820, 1.05, t, 0.85, 1);
    // Lunara in front of the moon, with a soft dark halo for contrast
    const g = c.createRadialGradient(560, 1210, 30, 560, 1210, 200);
    g.addColorStop(0, 'rgba(20,24,64,0.85)'); g.addColorStop(0.55, 'rgba(20,24,64,0.55)'); g.addColorStop(1, 'rgba(20,24,64,0)');
    c.fillStyle = g; c.beginPath(); c.arc(560, 1210, 200, 0, 7); c.fill();
    moonMouse(560, 1210, 78, t, { dir: -1, mood: 'happy', fly: true, seed: 0.4 });
    particles(t, 30, { y0: 1500, dy: -900, a: 0.5, color: 'rgba(220,230,255,A)', r: 2, life: 9, glowR: 6 });
    const sq = document.createElement('canvas'); sq.width = 1080; sq.height = 1080;
    sq.getContext('2d').drawImage(cv, 0, 420, 1080, 1080, 0, 0, 1080, 1080);
    const rd = document.createElement('canvas'); rd.width = 1080; rd.height = 1080;
    const r2 = rd.getContext('2d'); r2.beginPath(); r2.arc(540, 540, 540, 0, 7); r2.clip(); r2.drawImage(sq, 0, 0);
    return [sq.toDataURL('image/png'), rd.toDataURL('image/png')];
  });
  fs.writeFileSync(path.join(__dirname, 'profilbild.png'), Buffer.from(sqUrl.split(',')[1], 'base64'));
  fs.writeFileSync(path.join(__dirname, 'profilbild_rund_vorschau.png'), Buffer.from(rdUrl.split(',')[1], 'base64'));
  await browser.close();
  console.log('profilbild.png');
})();
