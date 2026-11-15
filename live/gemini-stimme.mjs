// Muschel-Tal LIVE – Moderationsstimme „Leda“ über Google Gemini (menschlich, mit Gefühl).
// Jedes Satzstück wird nach dem ersten Mal in werkzeug/stimme gespeichert und kostet danach nichts mehr.
// Namen werden als eigenes Stück erzeugt, damit „Danke fürs Folgen!“ & Co. nur einmal bezahlt werden.
// Klappt etwas nicht (kein Internet, Limit, Fehler), meldet satz() false – dann spricht Kerstin (Piper) diesen Satz.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export function geminiStimme({ dir, cacheDir, cfg }) {
  const schluessel = (() => { try { return fs.readFileSync(path.join(dir, 'gemini-schluessel.txt'), 'utf8').trim(); } catch { return process.env.GEMINI_API_KEY || ''; } })();
  const stimme = cfg.geminiStimme || 'Leda', modell = cfg.geminiModell || 'gemini-3.8-flash-tts';
  const RATE = 24000;
  let pauseBis = 0, fehlerInFolge = 0;
  const laufend = new Map();                                    // gleiche Stücke nicht doppelt anfragen
  const STIL = {
    normal: 'freundlich, warm und locker, wie eine gut gelaunte Moderatorin am Strand, zügiges Sprechtempo',
    froh: 'fröhlich, herzlich und lächelnd, zügiges Sprechtempo',
    spannend: 'spannend und neugierig machend, etwas aufgeregt, zügiges Sprechtempo',
    jubel: 'begeistert, jubelnd und überglücklich, voller Energie',
    name: 'freundlich und herzlich, nur dieses eine Wort, ohne Pause davor und danach',
  };

  const an = () => !!schluessel && cfg.engine === 'gemini' && Date.now() > pauseBis;

  // Gemini liefert WAV oder rohes PCM (16 Bit, 24 kHz) → immer Int16-Samples
  function pcmAus(buf) {
    if (buf.toString('ascii', 0, 4) !== 'RIFF') return new Int16Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + (buf.length & ~1)));
    let o = 12;
    while (o + 8 <= buf.length) {
      const id = buf.toString('ascii', o, o + 4), gr = buf.readUInt32LE(o + 4);
      if (id === 'data') { const d = buf.subarray(o + 8, o + 8 + Math.min(gr, buf.length - o - 8)); return new Int16Array(d.buffer.slice(d.byteOffset, d.byteOffset + (d.length & ~1))); }
      o += 8 + gr + (gr & 1);
    }
    return new Int16Array(0);
  }
  // Stille am Anfang/Ende abschneiden (sonst entstehen beim Zusammensetzen Lücken)
  function trimmen(p) {
    const s = 450; let a = 0, b = p.length - 1;
    while (a < p.length && Math.abs(p[a]) < s) a++;
    while (b > a && Math.abs(p[b]) < s) b--;
    return p.subarray(Math.max(0, a - RATE * .03), Math.min(p.length, b + RATE * .06));
  }
  const silben = t => (String(t).toLowerCase().match(/[aeiouyäöü]+/g) || []).length || 1;

  async function anfrage(text, gefuehl) {
    const prompt = `### DIRECTOR'S NOTES\nSprich auf Deutsch, ${STIL[gefuehl] || STIL.normal}. Sag genau den Text, nichts dazu.\n\n### TRANSCRIPT\n${text}`;
    const ctrl = new AbortController(), t = setTimeout(() => ctrl.abort(), (cfg.geminiMaxSek || 8) * 1000);
    try {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent`, {
        method: 'POST', signal: ctrl.signal,
        headers: { 'content-type': 'application/json', 'x-goog-api-key': schluessel },
        body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { responseModalities: ['AUDIO'], speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: stimme } } } } }),
      });
      if (!r.ok) { const e = new Error(`Gemini ${r.status}`); e.status = r.status; throw e; }
      const d = (await r.json())?.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
      if (!d) throw new Error('Gemini: keine Tonspur');
      return trimmen(pcmAus(Buffer.from(d, 'base64')));
    } finally { clearTimeout(t); }
  }

  // Ein Stück (Satzteil oder Name) holen: aus dem Speicher oder neu erzeugen
  async function stueck(text, gefuehl) {
    const key = crypto.createHash('md5').update(`gemini1|${modell}|${stimme}|${gefuehl}|${text}`).digest('hex');
    const datei = path.join(cacheDir, 'g_' + key + '.pcm');
    try { const b = fs.readFileSync(datei); return new Int16Array(b.buffer.slice(b.byteOffset, b.byteOffset + b.length)); } catch {}
    if (laufend.has(key)) return laufend.get(key);
    const p = (async () => {
      let pcm = await anfrage(text, gefuehl);
      // Gemini dichtet selten etwas dazu (viel zu lang) → einmal neu versuchen
      if (pcm.length / RATE > silben(text) / 3.2 + 1.2) { try { const n = await anfrage(text, gefuehl); if (n.length < pcm.length) pcm = n; } catch {} }
      try { fs.writeFileSync(datei, Buffer.from(pcm.buffer, pcm.byteOffset, pcm.byteLength)); } catch {}
      return pcm;
    })();
    laufend.set(key, p);
    try { return await p; } finally { laufend.delete(key); }
  }

  // Satz in Stücke teilen: bekannte Namen werden eigene Stücke
  function stuecke(text, namen) {
    const liste = [...new Set(namen.filter(n => n && n.length >= 2))].sort((a, b) => b.length - a.length);
    if (!liste.length) return [{ t: text }];
    const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(`@?(${liste.map(esc).join('|')})`, 'g');       // Treffer = Name (gerade Teile = Text, ungerade = Name)
    return text.split(re).map((s, i) => i % 2 ? { t: s, name: true } : { t: s.trim() }).filter(x => x.t && !/^[\s,.!?…:;–-]*$/.test(x.t));
  }

  function wav(pcm) {
    const k = Buffer.alloc(44);
    k.write('RIFF', 0); k.writeUInt32LE(36 + pcm.byteLength, 4); k.write('WAVE', 8); k.write('fmt ', 12);
    k.writeUInt32LE(16, 16); k.writeUInt16LE(1, 20); k.writeUInt16LE(1, 22); k.writeUInt32LE(RATE, 24);
    k.writeUInt32LE(RATE * 2, 28); k.writeUInt16LE(2, 32); k.writeUInt16LE(16, 34); k.write('data', 36); k.writeUInt32LE(pcm.byteLength, 40);
    return Buffer.concat([k, Buffer.from(pcm.buffer, pcm.byteOffset, pcm.byteLength)]);
  }

  // Ganzen Satz erzeugen → WAV-Datei. true = geklappt, false = bitte Ersatzstimme
  async function satz(text, gefuehl, ziel, namen = []) {
    if (!an()) return false;
    try {
      const teile = await Promise.all(stuecke(text, namen).map(s => stueck(s.t, s.name ? 'name' : gefuehl)));
      const luecke = new Int16Array(Math.round(RATE * .07)), alle = [];
      teile.forEach((p, i) => { if (i) alle.push(luecke); alle.push(p); });
      const n = alle.reduce((a, p) => a + p.length, 0), out = new Int16Array(n);
      let o = 0; for (const p of alle) { out.set(p, o); o += p.length; }
      if (!n) return false;
      if (ziel) fs.writeFileSync(ziel, wav(out));
      fehlerInFolge = 0;
      return true;
    } catch (e) {
      fehlerInFolge++;
      const limit = [400, 401, 403, 404, 429].includes(e.status);
      const warte = limit ? 10 * 60000 : fehlerInFolge >= 3 ? 2 * 60000 : 0;
      if (warte) pauseBis = Date.now() + warte;
      console.log(`⚠️  Leda (Gemini): ${e.name === 'AbortError' ? 'zu langsam' : e.message}${e.status === 429 ? ' – Limit erreicht' : ''} → Kerstin spricht${warte ? ` die nächsten ${Math.round(warte / 60000)} Minuten` : ' diesen Satz'}.`);
      return false;
    }
  }
  // Nächsten Satz schon vorab erzeugen, während der aktuelle läuft (landet im Speicher)
  const vorab = (text, gefuehl, namen) => { if (an()) satz(text, gefuehl, null, namen).catch(() => {}); };

  return { an, satz, vorab, stimme, hatSchluessel: !!schluessel };
}
