// Muschel-Tal LIVE – Moderationsstimme „Leda“.
// Hauptsächlich Google Gemini (menschlich, mit Gefühl). Nur im Notfall (Tageslimit aufgebraucht, Gemini antwortet nicht)
// spricht „Chirp 3 HD Leda“ (Google Cloud Text-to-Speech, hohe Limits).
// Sparen: Jedes Satzstück wird nach dem ersten Mal in werkzeug/stimme gespeichert und danach kostenlos abgespielt.
// Namen sind eigene Stücke („Danke fürs Folgen,“ + „Lara“) – so wiederholt sich fast alles.
// Gemini-Tageslimit (RPD) wird mitgezählt und mehrere Gemini-Modelle werden nacheinander genutzt (jedes hat ein eigenes Limit).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export function geminiStimme({ dir, cacheDir, cfg }) {
  const lies = (datei, env) => { try { return fs.readFileSync(path.join(dir, datei), 'utf8').trim(); } catch { return process.env[env] || ''; } };
  const schluessel = lies('gemini-schluessel.txt', 'GEMINI_API_KEY');
  // Notfall-Stimme: eigener Schlüssel – sonst wird der Gemini-Schlüssel versucht (klappt, wenn im selben Projekt die Text-to-Speech-API aktiv ist)
  const chirpSchluessel = lies('google-tts-schluessel.txt', 'GOOGLE_TTS_API_KEY') || schluessel;
  let chirpOk = null;
  const stimme = cfg.geminiStimme || 'Leda', chirpStimme = cfg.chirpStimme || 'de-DE-Chirp3-HD-Leda';
  const MODELLE = cfg.geminiModelle || [cfg.geminiModell || 'gemini-3.8-flash-tts', 'gemini-3.1-flash-tts-preview', 'gemini-2.5-flash-preview-tts'];
  const PRO_MIN = cfg.geminiProMinute || 8, PRO_TAG = cfg.geminiProTag || 100;
  const RATE = 24000;
  const laufend = new Map();                                    // gleiche Stücke nicht doppelt anfragen
  const STIL = {
    normal: 'Say warmly and cheerfully in German',
    froh: 'Say happily and warmly in German',
    spannend: 'Say excitedly in German',
    jubel: 'Say with great joy and excitement in German',
    name: 'Say warmly in German',
  };
  const STIL_MODELLE = cfg.geminiStilModelle || [];          // Standard: KEINE Anweisung an Gemini – nur der reine Satz (nichts, was vorgelesen werden könnte)
  // Prüfung: Ist die Aufnahme viel länger als der Text? Dann wurde etwas dazugesprochen (z. B. die Anweisung) → verwerfen
  const silben = t => (String(t).toLowerCase().match(/[aeiouyäöü]+/g) || []).length || 1;
  const zuLang = (pcm, text) => pcm.length / RATE > silben(text) / 3 + (String(text).match(/…/g) || []).length * .7 + 1.1;

  // ---------- Kontingent: pro Modell Anfragen pro Minute und pro Tag (Google zählt den Tag nach Pazifik-Zeit) ----------
  const ZAEHLER = path.join(cacheDir, 'gemini-zaehler.json');
  const heute = () => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Los_Angeles' }).format(new Date());
  let Z = { tag: heute(), n: {} };
  try { const z = JSON.parse(fs.readFileSync(ZAEHLER, 'utf8')); if (z.tag === Z.tag) Z = z; } catch {}
  const minute = Object.fromEntries(MODELLE.map(m => [m, []])), gesperrt = {};
  const tagPruefen = () => { const t = heute(); if (Z.tag !== t) { Z = { tag: t, n: {} }; for (const m of MODELLE) delete gesperrt[m]; } };
  const restTag = m => { tagPruefen(); return Math.max(0, PRO_TAG - 2 - (Z.n[m] || 0)); };   // 2 Reserve
  const restMin = m => { const j = Date.now(), s = minute[m]; while (s.length && j - s[0] > 60000) s.shift(); return Math.max(0, PRO_MIN - s.length); };
  const nutzbar = m => !(gesperrt[m] > Date.now()) && restTag(m) > 0;
  const restGesamt = () => MODELLE.filter(nutzbar).reduce((a, m) => a + restTag(m), 0);
  const zaehlen = m => { minute[m].push(Date.now()); Z.n[m] = (Z.n[m] || 0) + 1; try { fs.writeFileSync(ZAEHLER, JSON.stringify(Z)); } catch {} };
  // Reserve je nach Wichtigkeit: Geschenk-/Follow-Dank und neue Namen dürfen das letzte Kontingent nutzen, Kleinkram nicht
  const reserve = prio => prio <= 1 ? 0 : prio === 2 ? 15 : 30;

  const aktiv = () => (!!schluessel || !!chirpSchluessel) && cfg.engine === 'gemini';
  const an = aktiv;
  const frei = () => MODELLE.filter(nutzbar).reduce((a, m) => a + restMin(m), 0);

  // ---------- Ton-Helfer ----------
  function pcmAus(buf) {                                        // WAV oder rohes PCM (16 Bit, 24 kHz) → Int16-Samples
    if (buf.toString('ascii', 0, 4) !== 'RIFF') return new Int16Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + (buf.length & ~1)));
    let o = 12;
    while (o + 8 <= buf.length) {
      const id = buf.toString('ascii', o, o + 4), gr = buf.readUInt32LE(o + 4);
      if (id === 'data') { const d = buf.subarray(o + 8, o + 8 + Math.min(gr, buf.length - o - 8)); return new Int16Array(d.buffer.slice(d.byteOffset, d.byteOffset + (d.length & ~1))); }
      o += 8 + gr + (gr & 1);
    }
    return new Int16Array(0);
  }
  function trimmen(p) {                                         // Stille am Anfang/Ende weg (sonst Lücken beim Zusammensetzen)
    const s = 450; let a = 0, b = p.length - 1;
    while (a < p.length && Math.abs(p[a]) < s) a++;
    while (b > a && Math.abs(p[b]) < s) b--;
    return p.subarray(Math.max(0, a - RATE * .03), Math.min(p.length, b + RATE * .06));
  }
  function wav(pcm) {
    const k = Buffer.alloc(44);
    k.write('RIFF', 0); k.writeUInt32LE(36 + pcm.byteLength, 4); k.write('WAVE', 8); k.write('fmt ', 12);
    k.writeUInt32LE(16, 16); k.writeUInt16LE(1, 20); k.writeUInt16LE(1, 22); k.writeUInt32LE(RATE, 24);
    k.writeUInt32LE(RATE * 2, 28); k.writeUInt16LE(2, 32); k.writeUInt16LE(16, 34); k.write('data', 36); k.writeUInt32LE(pcm.byteLength, 40);
    return Buffer.concat([k, Buffer.from(pcm.buffer, pcm.byteOffset, pcm.byteLength)]);
  }
  const lesePcm = datei => { try { const b = fs.readFileSync(datei); return new Int16Array(b.buffer.slice(b.byteOffset, b.byteOffset + b.length)); } catch { return null; } };
  const speichere = (datei, pcm) => { try { fs.writeFileSync(datei, Buffer.from(pcm.buffer, pcm.byteOffset, pcm.byteLength)); } catch {} };
  const md5 = s => crypto.createHash('md5').update(s).digest('hex');

  // ---------- Gemini ----------
  // Stil-Anweisung nur kurz und nur beim Hauptmodell; die anderen Modelle bekommen nur den reinen Text
  // (manche Modelle lesen Anweisungen sonst laut vor – das darf im LIVE nie passieren)
  async function geminiAnfrage(m, text, gefuehl, mitStil) {
    const prompt = mitStil ? `${STIL[gefuehl] || STIL.normal}: ${text}` : text;
    const ctrl = new AbortController(), t = setTimeout(() => ctrl.abort(), (cfg.geminiMaxSek || 8) * 1000);
    try {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent`, {
        method: 'POST', signal: ctrl.signal,
        headers: { 'content-type': 'application/json', 'x-goog-api-key': schluessel },
        body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { responseModalities: ['AUDIO'], speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: stimme } } } } }),
      });
      if (!r.ok) {
        const e = new Error(`Gemini ${r.status}`); e.status = r.status;
        try { const x = await r.text(), w = x.match(/"retryDelay":\s*"(\d+(?:\.\d+)?)s"/); if (w) e.warteSek = +w[1]; e.text = x.slice(0, 400); } catch {}
        throw e;
      }
      const d = (await r.json())?.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
      if (!d) throw new Error('keine Tonspur');
      return trimmen(pcmAus(Buffer.from(d, 'base64')));
    } finally { clearTimeout(t); }
  }
  const gDatei = (text, gefuehl) => path.join(cacheDir, 'g_' + md5(`leda3|${stimme}|${STIL_MODELLE.length ? gefuehl : '-'}|${text}`) + '.pcm');
  const gemerkt = (text, gefuehl) => lesePcm(gDatei(text, gefuehl));
  // Alte Aufnahmen (konnten vorgelesene Anweisungen enthalten) einmalig löschen
  try { if (!fs.existsSync(path.join(cacheDir, 'leda3.ok'))) { for (const f of fs.readdirSync(cacheDir)) if (/^g_.*\.pcm$/.test(f)) fs.unlinkSync(path.join(cacheDir, f)); fs.writeFileSync(path.join(cacheDir, 'leda3.ok'), '1'); } } catch {}

  // Ein neues Gemini-Stück: freies Modell suchen (Minute + Tag), bei Limit das nächste Modell
  async function geminiNeu(text, gefuehl, warteMs) {
    const key = 'g|' + gefuehl + '|' + text;
    if (laufend.has(key)) return laufend.get(key);
    const p = (async () => {
      const ende = Date.now() + Math.max(0, warteMs);
      while (true) {
        const m = MODELLE.find(x => nutzbar(x) && restMin(x) > 0);
        if (m) {
          zaehlen(m);
          try {
            let pcm = await geminiAnfrage(m, text, gefuehl, STIL_MODELLE.includes(m));
            if (zuLang(pcm, text)) {                            // etwas dazugesprochen → einmal nur mit reinem Text
              if (!nutzbar(m) || restMin(m) < 1) throw new Error('Aufnahme verworfen (zu lang)');
              zaehlen(m); pcm = await geminiAnfrage(m, text, gefuehl, false);
              if (zuLang(pcm, text)) throw new Error('Aufnahme verworfen (zu lang)');
            }
            speichere(gDatei(text, gefuehl), pcm); return pcm;
          }
          catch (e) {
            if (e.status === 429) {
              const tag = (e.warteSek || 0) > 600 || /per.?day|PerDay|daily/i.test(e.text || '');
              gesperrt[m] = Date.now() + (tag ? 24 * 3600000 : Math.max(15, e.warteSek || 30) * 1000);
              if (tag) { Z.n[m] = PRO_TAG; try { fs.writeFileSync(ZAEHLER, JSON.stringify(Z)); } catch {} }
              console.log(`ℹ️  Leda: ${m} ${tag ? 'Tageslimit erreicht' : 'Minutenlimit erreicht'} – ${MODELLE.some(nutzbar) ? 'weiter mit dem nächsten Gemini-Modell' : chirpSchluessel ? 'Notfall: Chirp-Leda' : 'nur Gespeichertes'}.`);
              continue;
            }
            if ([400, 403, 404].includes(e.status)) { gesperrt[m] = Date.now() + 30 * 60000; console.log(`⚠️  Leda: ${m} antwortet mit Fehler ${e.status}${e.status === 403 ? ' (Schlüssel/Abrechnung prüfen)' : ''}.`); continue; }
            throw e;                                            // Netz/zu langsam → Notfallstimme für diesen Satz
          }
        }
        if (!MODELLE.some(nutzbar) || Date.now() > ende) { const e = new Error('Gemini gerade nicht verfügbar'); e.kein = true; throw e; }
        await new Promise(r => setTimeout(r, 300));             // Minutenlimit: kurz warten
      }
    })();
    laufend.set(key, p);
    try { return await p; } finally { laufend.delete(key); }
  }

  // ---------- Chirp 3 HD (Notfall) ----------
  const cDatei = text => path.join(cacheDir, 'c_' + md5(`chirp1|${chirpStimme}|${text}`) + '.pcm');
  async function chirp(text) {
    const d = cDatei(text), alt = lesePcm(d); if (alt) return alt;
    if (!chirpSchluessel) throw Object.assign(new Error('kein Chirp-Schlüssel'), { kein: true });
    const key = 'c|' + text; if (laufend.has(key)) return laufend.get(key);
    const p = (async () => {
      const ctrl = new AbortController(), t = setTimeout(() => ctrl.abort(), 8000);
      try {
        const r = await fetch('https://texttospeech.googleapis.com/v1/text:synthesize', {
          method: 'POST', signal: ctrl.signal, headers: { 'content-type': 'application/json', 'x-goog-api-key': chirpSchluessel },
          body: JSON.stringify({ input: { text }, voice: { languageCode: 'de-DE', name: chirpStimme }, audioConfig: { audioEncoding: 'LINEAR16', sampleRateHertz: RATE } }),
        });
        if (!r.ok) throw new Error(`Chirp ${r.status}${r.status === 403 ? ' (Text-to-Speech-API im Projekt aktivieren?)' : ''}`);
        const pcm = trimmen(pcmAus(Buffer.from((await r.json()).audioContent, 'base64')));
        speichere(d, pcm); return pcm;
      } finally { clearTimeout(t); }
    })();
    laufend.set(key, p);
    try { return await p; } finally { laufend.delete(key); }
  }

  // Satz in Stücke teilen: bekannte Namen werden eigene Stücke
  function stuecke(text, namen) {
    const liste = [...new Set(namen.filter(n => n && n.length >= 2))].sort((a, b) => b.length - a.length);
    if (!liste.length) return [{ t: text }];
    const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(`@?(${liste.map(esc).join('|')})`, 'g');
    return text.split(re).map((s, i) => i % 2 ? { t: s, name: true } : { t: s.trim() }).filter(x => x.t && !/^[\s,.!?…:;–-]*$/.test(x.t));
  }
  function zusammen(teile) {
    const luecke = new Int16Array(Math.round(RATE * .07)), alle = [];
    teile.forEach((p, i) => { if (i) alle.push(luecke); alle.push(p); });
    const out = new Int16Array(alle.reduce((a, p) => a + p.length, 0));
    let o = 0; for (const p of alle) { out.set(p, o); o += p.length; }
    return out;
  }

  // Ganzen Satz → WAV. Reihenfolge: alles aus dem Gemini-Speicher (gratis) → fehlende Stücke neu bei Gemini (wenn das
  // Kontingent für diese Wichtigkeit reicht) → Notfall: ganzer Satz mit Chirp-Leda (einheitlicher Klang). true = geklappt.
  async function satz(text, gefuehl, ziel, namen = [], { prio = 2, warteMs = (cfg.geminiMaxWarteSek ?? 12) * 1000, nurGemini = false } = {}) {
    if (!aktiv()) return false;
    const st = stuecke(text, namen).map(s => ({ ...s, g: s.name ? 'name' : gefuehl }));
    const haben = st.map(s => gemerkt(s.t, s.g)), fehlen = st.filter((s, i) => !haben[i]);
    let pcm = null, quelle = 'gespeichert';
    if (!fehlen.length) pcm = zusammen(haben);
    else if (schluessel && restGesamt() - fehlen.length >= reserve(prio)) {
      try { const neu = await Promise.all(st.map((s, i) => haben[i] || geminiNeu(s.t, s.g, warteMs))); pcm = zusammen(neu); quelle = 'gemini'; }
      catch (e) { if (!e.kein) console.log(`⚠️  Leda (Gemini): ${e.name === 'AbortError' ? 'zu langsam' : e.message} – Notfall: Chirp-Leda.`); }
    }
    if (!pcm && !nurGemini && chirpSchluessel && chirpOk !== false) {
      try { pcm = zusammen(await Promise.all(st.map(s => chirp(s.t)))); quelle = 'chirp'; }
      catch (e) { if (!e.kein) console.log(`⚠️  Chirp-Leda: ${e.name === 'AbortError' ? 'zu langsam' : e.message}`); }
    }
    if (!pcm || !pcm.length) return false;
    if (ziel) fs.writeFileSync(ziel, wav(pcm));
    satz.letzteQuelle = quelle;
    return true;
  }
  // Nächsten Satz vorab bei Gemini erzeugen – nur wenn Kontingent reichlich da ist
  const vorab = (text, gefuehl, namen, prio = 2) => { if (schluessel && restGesamt() > 40 && frei() >= 3) satz(text, gefuehl, null, namen, { prio, warteMs: 0, nurGemini: true }).catch(() => {}); };
  const info = () => `${schluessel ? 'Gemini heute noch ' + restGesamt() + ' neue Sätze' : 'kein Gemini-Schlüssel'}, Notfall Chirp: ${chirpOk ? 'bereit' : chirpOk === false ? 'nicht verfügbar' : 'wird geprüft'}`;
  // Notfall-Stimme beim Start einmal prüfen (kurzer Satz, wird gespeichert)
  if (chirpSchluessel && cfg.engine === 'gemini') chirp('Hallo!').then(() => { chirpOk = true; }, e => { chirpOk = false; console.log(`ℹ️  Notfall-Stimme Chirp-Leda nicht verfügbar: ${e.message}`); });

  return { an, aktiv, frei, satz, vorab, info, restGesamt, stimme, hatSchluessel: !!schluessel, hatChirp: () => chirpOk === true };
}
