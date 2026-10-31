// Render an episode to video.
//   node engine/render.js out/folge01                 full render -> out/folge01/folge.mp4
//   node engine/render.js out/folge01 --stills 3,45   PNG stills for checking
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30, WORKERS = 4;
const outDir = path.resolve(process.argv[2]);
const tl = JSON.parse(fs.readFileSync(path.join(outDir, 'timeline.json'), 'utf8'));
const page_url = 'file://' + path.join(__dirname, 'render.html');

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => { console.error('PAGE ERROR', e); process.exit(1); });
  await page.goto(page_url);
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.fonts].map(f => f.load())); });
  await page.evaluate(t => window.setup(t), tl);
  return page;
}

const grab = (page, t, f, type = 'image/jpeg') =>
  page.evaluate(([t, f, type]) => { window.draw(t, f); return document.getElementById('c').toDataURL(type, 0.93); }, [t, f, type])
    .then(u => Buffer.from(u.split(',')[1], 'base64'));

async function stills(times) {
  const browser = await chromium.launch();
  const page = await openPage(browser);
  fs.mkdirSync(path.join(outDir, 'stills'), { recursive: true });
  for (const t of times) {
    const buf = await grab(page, t, Math.round(t * FPS), 'image/png');
    const p = path.join(outDir, 'stills', `t${String(t).padStart(6, '0')}.png`);
    fs.writeFileSync(p, buf); console.log(p);
  }
  await browser.close();
}

async function chunk(browser, idx, f0, f1) {
  const page = await openPage(browser);
  const file = path.join(outDir, `chunk${idx}.mp4`);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(FPS), file], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = f0; f < f1; f++) {
    const buf = await grab(page, f / FPS, f);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - f0) % 300 === 0) console.log(`worker ${idx}: ${f - f0}/${f1 - f0}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  return file;
}

async function full() {
  const total = Math.ceil(tl.duration * FPS);
  const browser = await chromium.launch({ args: ['--disable-gpu-vsync'] });
  const per = Math.ceil(total / WORKERS);
  const files = await Promise.all([...Array(WORKERS)].map((_, i) => chunk(browser, i, i * per, Math.min(total, (i + 1) * per))));
  await browser.close();
  const list = path.join(outDir, 'chunks.txt');
  fs.writeFileSync(list, files.map(f => `file '${f}'`).join('\n'));
  const out = path.join(outDir, 'folge.mp4');
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-i', path.join(outDir, 'mix.wav'),
    '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], { stdio: 'inherit' });
  files.forEach(f => fs.unlinkSync(f)); fs.unlinkSync(list);
  console.log('fertig:', out);
}

const si = process.argv.indexOf('--stills');
(si > 0 ? stills(process.argv[si + 1].split(',').map(Number)) : full()).catch(e => { console.error(e); process.exit(1); });
