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

  const aktiv = () => !!schluessel && cfg.engine === 'gemini';
  const an = () => aktiv() && Date.now() > pauseBis;
  // Anfragen-Bremse: Gemini erlaubt nur eine bestimmte Zahl Anfragen pro Minute (je nach Konto) – nie darüber
  const proMin = cfg.geminiProMinute || 8, stempel = [];
  const frei = () => { const j = Date.now(); while (stempel.length && j - stempel[0] > 60000) stempel.shift(); return Math.max(0, proMin - stempel.length); };
  async function platz(maxWarteMs) {                           // wartet auf einen freien Platz (oder gibt auf)
    const ende = Date.now() + maxWarteMs;
    while (true) {
      if (Date.now() > pauseBis && frei() > 0) { stempel.push(Date.now()); return true; }
      if (Date.now() > ende) return false;
      await new Promise(r => setTimeout(r, 250));
    }
  }

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
      if (!r.ok) {
        const e = new Error(`Gemini ${r.status}`); e.status = r.status;
        try { const t = await r.text(), m = t.match(/"retryDelay":\s*"(\d+(?:\.\d+)?)s"/); if (m) e.warteSek = +m[1]; e.text = t.slice(0, 300); } catch {}
        throw e;
      }
      const d = (await r.json())?.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
      if (!d) throw new Error('Gemini: keine Tonspur');
      return trimmen(pcmAus(Buffer.from(d, 'base64')));
    } finally { clearTimeout(t); }
  }

  // Ein Stück (Satzteil oder Name) holen: aus dem Speicher oder neu erzeugen
  async function stueck(text, gefuehl, warteMs) {
    const key = crypto.createHash('md5').update(`gemini1|${modell}|${stimme}|${gefuehl}|${text}`).digest('hex');
    const datei = path.join(cacheDir, 'g_' + key + '.pcm');
    try { const b = fs.readFileSync(datei); return new Int16Array(b.buffer.slice(b.byteOffset, b.byteOffset + b.length)); } catch {}
    if (laufend.has(key)) return laufend.get(key);
    if (warteMs < 0) { const e = new Error('nicht im Speicher'); e.speicher = true; throw e; }
    const p = (async () => {
      if (!await platz(warteMs)) { const e = new Error('Anfragen-Limit pro Minute – kurz warten'); e.bremse = true; throw e; }
      let pcm = await anfrage(text, gefuehl);
      // Gemini dichtet selten etwas dazu (viel zu lang) → einmal neu versuchen (nur wenn noch Platz im Limit ist)
      if (pcm.length / RATE > silben(text) / 3.2 + 1.2 && frei() > 2) { stempel.push(Date.now()); try { const n = await anfrage(text, gefuehl); if (n.length < pcm.length) pcm = n; } catch {} }
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
  // warteMs: so lange darf auf einen freien Platz im Anfragen-Limit gewartet werden; -1 = nur aus dem Speicher
  async function satz(text, gefuehl, ziel, namen = [], warteMs = (cfg.geminiMaxWarteSek ?? 12) * 1000) {
    if (!aktiv()) return false;
    if (!an() && warteMs > 0 && pauseBis - Date.now() > warteMs) warteMs = -1;   // lange Pause: nur Gespeichertes
    try {
      const teile = await Promise.all(stuecke(text, namen).map(s => stueck(s.t, s.name ? 'name' : gefuehl, warteMs)));
      const luecke = new Int16Array(Math.round(RATE * .07)), alle = [];
      teile.forEach((p, i) => { if (i) alle.push(luecke); alle.push(p); });
      const n = alle.reduce((a, p) => a + p.length, 0), out = new Int16Array(n);
      let o = 0; for (const p of alle) { out.set(p, o); o += p.length; }
      if (!n) return false;
      if (ziel) fs.writeFileSync(ziel, wav(out));
      fehlerInFolge = 0;
      return true;
    } catch (e) {
      if (e.speicher || e.bremse || !ziel) return false;       // still: Satz fällt weg (oder Vorab-Erzeugung)
      fehlerInFolge++;
      let warte = 0;
      if (e.status === 429) warte = Math.max(15, e.warteSek || 30) * 1000;                // Minuten-/Tageslimit: kurz pausieren
      else if ([400, 401, 403, 404].includes(e.status)) warte = 5 * 60000;               // Schlüssel/Modell falsch
      else if (fehlerInFolge >= 3) warte = 60000;
      if (warte) pauseBis = Math.max(pauseBis, Date.now() + warte);
      const grund = e.name === 'AbortError' ? 'zu langsam' : e.status === 429 ? `Limit erreicht (Google: ${(e.text || '').match(/quota[^"]*|limit[^"]*/i)?.[0]?.slice(0, 90) || 'zu viele Anfragen'})` : e.message;
      const dauer = warte >= 3600000 ? `${Math.round(warte / 3600000)} Std.` : warte >= 120000 ? `${Math.round(warte / 60000)} Min.` : `${Math.round(warte / 1000)} s`;
      console.log(`⚠️  Leda (Gemini): ${grund}${warte ? ` – Pause ${dauer} (Gespeichertes spricht Leda weiter)` : ''}.`);
      if (warte >= 3600000) console.log('   → Das ist das TAGESLIMIT des kostenlosen Zugangs: In AI Studio beim Projekt dieses Schlüssels die Abrechnung (Billing) aktivieren bzw. den Schlüssel aus dem Projekt mit Guthaben nehmen.');
      return false;
    }
  }
  // Nächsten Satz schon vorab erzeugen, während der aktuelle läuft (landet im Speicher)
  // nur wenn genug Platz im Limit bleibt (der aktuelle Satz geht immer vor)
  const vorab = (text, gefuehl, namen) => { if (an() && frei() >= 3) satz(text, gefuehl, null, namen, 0).catch(() => {}); };

  return { an, aktiv, frei, satz, vorab, stimme, hatSchluessel: !!schluessel };
}
