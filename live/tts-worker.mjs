// Muschel-Tal LIVE – Annas Stimme mit Piper (offline, unabhängig vom macOS-Sprachdienst).
// Läuft als eigener Prozess: bekommt {id, text, datei}, schreibt eine WAV-Datei und meldet {id, ok, ms}.
// Hängt hier etwas, kann das Hauptprogramm diesen Prozess einfach neu starten – der LIVE läuft weiter.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const MODELL = process.argv[2];
const TEMPO = +(process.argv[3] || 1);                       // > 1 = schneller
const cfg = JSON.parse(fs.readFileSync(MODELL + '.json', 'utf8'));
const RATE = cfg.audio.sample_rate;
const BUILD = path.dirname(require.resolve('@diffusionstudio/piper-wasm/build/piper_phonemize.js'));
const createPiperPhonemize = require(path.join(BUILD, 'piper_phonemize.js'));
const ort = require('onnxruntime-node');

// Laut-IDs immer mit der Liste des Modells bilden (ältere Modelle kennen weniger Laute): ^ Laut _ Laut _ … $
const MAP = cfg.phoneme_id_map || {};
function ids(ausgabe) {
  const ph = ausgabe.phonemes;
  if (!ph || !Object.keys(MAP).length) return ausgabe.phoneme_ids;
  const zeichen = Array.isArray(ph) ? ph.flat().join('') : String(ph), out = [...MAP['^']];
  for (const z of Array.from(zeichen)) { if (MAP[z]) { out.push(...MAP[z], ...MAP['_']); } }
  out.push(...MAP['$']);
  return out;
}
// Lautschrift: espeak-ng (als WebAssembly) wandelt Text in Laute um
const wasm = fs.readFileSync(path.join(BUILD, 'piper_phonemize.wasm'));
function phoneme(text) {
  return new Promise((ok, fehler) => {
    let fertig = false;
    createPiperPhonemize({
      wasmBinary: wasm,
      locateFile: f => path.join(BUILD, f),
      print: d => { if (!fertig) { fertig = true; try { ok(ids(JSON.parse(d))); } catch (e) { fehler(e); } } },
      printErr: () => {},
    }).then(m => {
      m.callMain(['-l', cfg.espeak.voice, '--input', JSON.stringify([{ text }]), '--espeak_data', '/espeak-ng-data']);
      setTimeout(() => { if (!fertig) fehler(new Error('Lautschrift ohne Ergebnis')); }, 5000);
    }, fehler);
  });
}

const sitzung = await ort.InferenceSession.create(MODELL, { intraOpNumThreads: 2, interOpNumThreads: 1, graphOptimizationLevel: 'all' });
async function sprich(text) {
  const ids = await phoneme(text);
  const lang = BigInt64Array.from(ids.map(BigInt));
  const feeds = {
    input: new ort.Tensor('int64', lang, [1, ids.length]),
    input_lengths: new ort.Tensor('int64', BigInt64Array.from([BigInt(ids.length)]), [1]),
    scales: new ort.Tensor('float32', Float32Array.from([cfg.inference.noise_scale, cfg.inference.length_scale / TEMPO, cfg.inference.noise_w]), [3]),
  };
  if (Object.keys(cfg.speaker_id_map || {}).length) feeds.sid = new ort.Tensor('int64', BigInt64Array.from([0n]), [1]);
  return (await sitzung.run(feeds)).output.data;
}
// Aussprache: englische Wörter so schreiben, wie man sie spricht (nur für die Stimme)
const AUSSPRACHE = [
  [/\bLikes\b/gi, 'Leiks'], [/\bLike\b/gi, 'Leik'], [/\bliken\b/gi, 'leiken'], [/\bliked\b/gi, 'leikt'], [/\bgeliked\b/gi, 'geleikt'], [/\blikt\b/gi, 'leikt'],
  [/Like-/g, 'Leik-'], [/\bEvents\b/gi, 'Iwänts'], [/\bEvent\b/gi, 'Iwänt'], [/Event-/g, 'Iwänt-'], [/\bLIVE\b/g, 'Leif'], [/\blive\b/g, 'leif'],
  [/\bHappy Hour\b/gi, 'Häppi Auer'], [/\bMystery\b/gi, 'Misteri'], [/\bTeams?\b/gi, m => m.endsWith('s') ? 'Tiems' : 'Tiem'], [/\bSurf/gi, 'Sörf'],
  [/\bCocktail/gi, 'Kocktäil'], [/\bcool\b/gi, 'kuhl'], [/\bTikTok\b/gi, 'Tick Tock'], [/\bCoins?\b/gi, m => m.endsWith('s') ? 'Keuns' : 'Keun'],
  [/\bCafé\b/g, 'Kaffee'], [/\bFollower\b/gi, 'Folower'], [/\bStream\b/gi, 'Striem'], [/\bShow\b/gi, 'Schou'], [/\bQuiz\b/gi, 'Kwiss'], [/@/g, ''],
];
const sprechbar = t => AUSSPRACHE.reduce((x, [a, b]) => x.replace(a, b), String(t));
// „…“ = kurze Sprechpause: Teile einzeln sprechen, Stille dazwischen
async function satz(text) {
  text = sprechbar(text);
  const teile = String(text).split(/\s*…\s*/).map(t => t.trim()).filter(Boolean);
  const stille = new Float32Array(Math.round(RATE * .25)), stuecke = [];
  for (const [i, t] of teile.entries()) { if (i) stuecke.push(stille); stuecke.push(await sprich(t)); }
  const n = stuecke.reduce((a, s) => a + s.length, 0), pcm = new Int16Array(n);
  let o = 0; for (const s of stuecke) for (let i = 0; i < s.length; i++) pcm[o++] = Math.max(-32768, Math.min(32767, Math.round(s[i] * 32767)));
  const kopf = Buffer.alloc(44);
  kopf.write('RIFF', 0); kopf.writeUInt32LE(36 + pcm.byteLength, 4); kopf.write('WAVE', 8); kopf.write('fmt ', 12);
  kopf.writeUInt32LE(16, 16); kopf.writeUInt16LE(1, 20); kopf.writeUInt16LE(1, 22); kopf.writeUInt32LE(RATE, 24);
  kopf.writeUInt32LE(RATE * 2, 28); kopf.writeUInt16LE(2, 32); kopf.writeUInt16LE(16, 34); kopf.write('data', 36); kopf.writeUInt32LE(pcm.byteLength, 40);
  return Buffer.concat([kopf, Buffer.from(pcm.buffer)]);
}

// Aufträge nacheinander abarbeiten
let kette = Promise.resolve();
process.on('message', ({ id, text, datei }) => {
  kette = kette.then(async () => {
    const t0 = Date.now();
    try { fs.writeFileSync(datei, await satz(text)); process.send({ id, ok: true, ms: Date.now() - t0 }); }
    catch (e) { process.send({ id, ok: false, fehler: String(e?.message || e) }); }
  });
});
process.send({ bereit: true });
