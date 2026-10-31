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
