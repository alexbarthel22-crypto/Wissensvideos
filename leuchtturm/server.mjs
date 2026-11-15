// Leuchtturm-Rennen – TikTok LIVE: Jede Stadt bekommt eine eigene kleine Insel mit Leuchtturm.
// Wer seine Stadt in den Chat schreibt, baut mit – jeder Kommentar macht den Leuchtturm höher, ohne Grenze.
// Start:  node server.mjs          (echter Stream, TikTok-Name aus einstellungen.json)
//         node server.mjs --test   (ohne TikTok, mit /test-Zugängen zum Ausprobieren)
//         node server.mjs --still  (ohne Stimme)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn, fork } from 'node:child_process';
import os from 'node:os';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { macheEvents } from './events.mjs';
import { satz, namenListe, festeSaetze, festeSaetzeAus } from './saetze.mjs';
import { klarname } from './vornamen.mjs';
import { stadtAus, landVon, infoVon } from './staedte.mjs';
import { geminiStimme } from './gemini-stimme.mjs';
import { anstoessig, satzAnstoessig, ladeSperrliste, gesperrt, normal } from './filter.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const CFG = JSON.parse(fs.readFileSync(path.join(DIR, 'einstellungen.json'), 'utf8'));
const STAND = path.join(DIR, 'stand.json');
const VERSION = '2026-11-16 b';                          // bei jeder Änderung hochzählen – steht beim Start im Terminal
const TEST = process.argv.includes('--test');
const STILL = process.argv.includes('--still') || !CFG.stimme.an;
// Stimmen und Kerstin-Modell mit Muschel-Tal LIVE teilen (gleicher Speicher = schon erzeugte Leda-Sätze kosten nichts)
const MUSCHELTAL = [path.join(os.homedir(), 'Desktop', 'Muschel-Tal LIVE'), path.join(DIR, '..', 'live'), path.join(DIR, '..', 'Muschel-Tal LIVE')].find(d => fs.existsSync(path.join(d, 'werkzeug')));
const WERKZEUG = [path.join(DIR, 'werkzeug'), ...(MUSCHELTAL ? [path.join(MUSCHELTAL, 'werkzeug')] : [])];
const werkzeugMit = sub => WERKZEUG.find(w => fs.existsSync(path.join(w, sub))) || WERKZEUG[0];

// ---------- Spielstand ----------
const leer = () => ({ staedte: {}, spieler: {}, likesGesamt: 0, sieger: [], woche: { id: '', m: {} }, heute: { id: '', m: {} } });
let S = leer();
try { S = { ...leer(), ...JSON.parse(fs.readFileSync(STAND, 'utf8')) }; } catch {}
if (TEST && process.argv.includes('--neu')) S = leer();
for (const st of Object.values(S.staedte)) if (st.region == null || st.lat === undefined) Object.assign(st, infoVon(st.name));   // ältere Stände ergänzen
// Wochen- und Tageswertung (Meter, die in dieser Woche / heute dazugekommen sind)
const wocheId = () => { const d = new Date(), t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())), w = t.getUTCDay() || 7; t.setUTCDate(t.getUTCDate() + 4 - w); return t.getUTCFullYear() + '-W' + Math.ceil(((t - Date.UTC(t.getUTCFullYear(), 0, 1)) / 864e5 + 1) / 7); };
const tagId = () => new Date().toLocaleDateString('sv-SE');
function zaehle(name, um) {
  if (S.woche?.id !== wocheId()) S.woche = { id: wocheId(), m: {} };
  if (S.heute?.id !== tagId()) S.heute = { id: tagId(), m: {} };
  S.woche.m[name] = (S.woche.m[name] || 0) + um; S.heute.m[name] = (S.heute.m[name] || 0) + um;
}
const top = (m, n = 5) => Object.entries(m || {}).sort((a, b) => b[1] - a[1]).slice(0, n).map(([name, m]) => ({ name, m, land: S.staedte[name]?.land || 'DE' }));
let geaendert = false;
const speichern = () => { if (!geaendert || TEST) return; fs.writeFileSync(STAND, JSON.stringify(S)); geaendert = false; };
setInterval(speichern, 10000);
ladeSperrliste(DIR);
const liveDabei = () => {}, rangMelden = () => {}, inKasse = () => {}, setzeBewohner = () => {};
var bewohnerVonTikTok = false;

// ---------- Zuschauer ----------
function spieler(u) {
  const id = String(u.uniqueId || '').toLowerCase();
  if (!id || gesperrt(id)) return null;
  let p = S.spieler[id];
  if (!p) { p = S.spieler[id] = { id, name: anstoessig(u.uniqueId) || anstoessig(u.nickname) ? 'Gast' : '@' + u.uniqueId, stadt: null, beitrag: 0, zuletzt: Date.now() }; geaendert = true; }
  p.zuletzt = Date.now();
  return p;
}
// Für die Stimme: Klarname („lara91554“ → „Lara“), sonst bereinigter Name. Namen werden bei Leda als eigenes Stück gespeichert.
const GESPROCHENE_NAMEN = new Set();
const sprechName = p => { const n = klarname(p.name) || String(p.name).replace(/^@/, '').replace(/[._]+/g, ' ').replace(/\d{3,}/g, '').trim() || 'Gast'; if (GESPROCHENE_NAMEN.size > 3000) GESPROCHENE_NAMEN.clear(); GESPROCHENE_NAMEN.add(n); return n; };
const namenIn = t => [...GESPROCHENE_NAMEN, ...Object.keys(S.staedte)].filter(n => t.includes(n));
const einmalZeit = new Map();
function einmal(id, art, ms) { const k = id + '|' + art, t = einmalZeit.get(k) || 0; if (Date.now() - t < ms) return false; einmalZeit.set(k, Date.now()); return true; }

// ---------- Leuchttürme ----------
const TURM_UPGRADES = [[10, 'eine Fahne'], [25, 'leuchtende Fenster'], [50, 'eine goldene Galerie'], [100, 'den ersten Farbring'], [150, 'einen Möwenschwarm'],
  [250, 'ein buntes Leuchtfeuer'], [400, 'Funkelsterne'], [500, 'die Wolken'], [750, 'einen Regenbogen'], [1000, 'eine goldene Krone'], [1500, 'einen Hubschrauber'],
  [2000, 'eine Diamant-Spitze'], [3000, 'Mond und Sterne'], [5000, 'eine Rakete'], [7500, 'ein Nordlicht'], [10000, 'Planetenringe']];
const rangListe = () => Object.values(S.staedte).sort((a, b) => b.stock - a.stock);
let fuehrender = null, fuehrungAnsage = 0, upAnsage = 0, neuAnsage = 0;
const plusPuffer = new Map();                                // „+1“-Anzeigen sammeln (nicht jedes Stockwerk einzeln schicken)
function turmWachsen(name, um, p, art) {
  const s = S.staedte[name]; if (!s || um <= 0) return;
  const vorher = s.stock; s.stock += um; geaendert = true; zaehle(name, um);
  if (p) { p.beitrag = (p.beitrag || 0) + um; s.baumeister ||= {}; s.baumeister[p.name] = (s.baumeister[p.name] || 0) + um; }
  const pp = plusPuffer.get(name) || { n: 0, wer: null, art: '' }; pp.n += um; if (p) pp.wer = p.name; if (art) pp.art = art; plusPuffer.set(name, pp);
  const up = TURM_UPGRADES.filter(([n]) => vorher < n && s.stock >= n).pop();
  if (up) { sende({ typ: 'upgrade', stadt: name, stock: up[0], was: up[1] }); if (Date.now() - upAnsage > 20000) { upAnsage = Date.now(); sag(satz('upgrade', { stadt: name, was: up[1] }), 2); } }
  fuehrungPruefen();
}
setInterval(() => { if (!plusPuffer.size) return; sende({ typ: 'plus', l: [...plusPuffer].map(([stadt, v]) => ({ stadt, n: v.n, wer: v.wer, art: v.art })) }); plusPuffer.clear(); zustand(); }, 700);
function fuehrungPruefen() {
  const [a, b] = rangListe(); if (!a) return;
  if (fuehrender && a.name !== fuehrender && Date.now() - fuehrungAnsage > 60000) {
    fuehrungAnsage = Date.now(); sende({ typ: 'fuehrung', stadt: a.name }); sag(satz('fuehrung', { stadt: a.name, zweite: b?.name || '' }), 1);
  }
  fuehrender = a.name;
}
setTimeout(() => { fuehrender = rangListe()[0]?.name || null; }, 0);
// Städte-Fieber: Schreiben viele verschiedene Leute einer Stadt in kurzer Zeit, wächst sie eine Weile doppelt
const aktivität = new Map();                                  // Stadt → Map(Spieler → Zeit)
function fieberPruefen(s, p) {
  const m = aktivität.get(s.name) || new Map(); m.set(p.id, Date.now()); aktivität.set(s.name, m);
  for (const [id, t] of m) if (Date.now() - t > 30000) m.delete(id);
  if (m.size >= (CFG.turm.fieberAb ?? 6) && !(s.fieberBis > Date.now())) {
    s.fieberBis = Date.now() + (CFG.turm.fieberSek ?? 45) * 1000; sende({ typ: 'fieber', stadt: s.name }); sag(satz('fieber', { stadt: s.name }), 1);
  }
}

// ---------- Ereignisse aus dem Chat ----------
const sauber = t => String(t || '').toLowerCase().replace(/[^\p{L}\p{N}\s]/gu, ' ').replace(/\s+/g, ' ').trim();
function eventAntwort(p, t, probe) {
  const versuch = x => probe ? EV.waereAntwort(x) : EV.kommentar(p, x);
  const s = sauber(t); if (!s) return false;
  if (versuch(t) || (s !== t && versuch(s))) return true;
  const w = s.split(' ');
  if (w.length > 1 && w.length <= 6) for (const x of w) if (x && versuch(x)) return true;
  return false;
}
const STADT_EVENTS = new Set(['staedteneu', 'baukolonne', 'nebel']);   // hier ist die Stadt die Antwort
function kommentar(u, text) {
  const t = String(text || '').toLowerCase().trim();
  const p = spieler(u); if (!p) return;
  // 1. Stadt wählen (einmal). Ist der Kommentar gerade eine andere Event-Antwort („licht“, „los“ …), zählen kleine Orte nur mit „aus …“
  if (!p.stadt && EV.id() !== 'turmquiz') {
    const antwort = EV.laeuft() && !STADT_EVENTS.has(EV.id()) && eventAntwort(null, text, true);
    const st = stadtAus(text, antwort);
    if (st) {
      p.stadt = st; p.stadtZeit = Date.now(); geaendert = true;
      const neu = !S.staedte[st];
      const s = S.staedte[st] ||= { name: st, stock: 0, leute: 0, seit: Date.now(), land: landVon(st), ...infoVon(st), gruender: p.name };
      if (neu) S.neueste = st;
      s.leute++;
      turmWachsen(st, 1, p);
      sende({ typ: neu ? 'neueStadt' : 'beitritt', stadt: st, name: p.name });
      if (neu && Date.now() - neuAnsage > 15000) { neuAnsage = Date.now(); sag(klarname(p.name) ? satz('neueStadtName', { name: sprechName(p), stadt: st }) : satz('neueStadt', { stadt: st }), 2); }
      eventAntwort(p, text);
      return;
    }
  }
  // 2. Event-Antwort
  eventAntwort(p, text);
  // 3. Jeder Kommentar: +1 m für die eigene Stadt (pro Person höchstens alle 30 s, im Turbo alle 10 s, im Fieber doppelt)
  //    🎁 im Chat = Mega-Bauschub (+25 m, pro Person alle 60 s), ❤️ im Chat = +1 m (pro Person alle 5 s; im Herz-Regen +2 m alle 2 s)
  if (!p.stadt || !S.staedte[p.stadt]) return;
  const s = S.staedte[p.stadt], turbo = EV.turbo(), regen = EV.herzregen(), T = CFG.turm, fieber = s.fieberBis > Date.now() ? 2 : 1;
  fieberPruefen(s, p);
  const jetzt = Date.now();
  if (GESCHENK_EMOJI.test(text) && jetzt - (p.geschenkZeit || 0) >= (T.geschenkEmojiSek ?? 60) * 1000) {
    p.geschenkZeit = jetzt; p.stadtZeit = jetzt; const n = (T.geschenkEmojiMeter ?? 25) * fieber;
    turmWachsen(s.name, n, p, 'geschenk'); sende({ typ: 'bauschub', stadt: s.name, name: p.name, n }); if (turbo) turbo.n += n;
    if (Date.now() - bauschubAnsage > 20000) { bauschubAnsage = Date.now(); sag(satz('bauschub', { stadt: s.name }), 2); }
    return;
  }
  if (HERZ_EMOJI.test(text) && jetzt - (p.herzZeit || 0) >= (regen ? 2 : (T.herzEmojiSek ?? 5)) * 1000) {
    p.herzZeit = jetzt; p.stadtZeit = jetzt; const n = (regen ? 2 : (T.herzEmojiMeter ?? 1)) * fieber;
    turmWachsen(s.name, n, p, 'herz'); if (regen) regen.n += n; if (turbo) turbo.n += n;
    return;
  }
  const abstand = (turbo ? 10 : (T.proKommentarSek ?? 30)) * 1000;
  if (jetzt - (p.stadtZeit || 0) < abstand) return;
  p.stadtZeit = jetzt;
  turmWachsen(s.name, fieber, p); if (turbo) turbo.n += fieber;
}
const GESCHENK_EMOJI = /🎁/u, HERZ_EMOJI = /(❤|♥|💖|💗|💓|💕|💞|💘|💝|🧡|💛|💚|💙|💜|🤍|🖤|🤎|🩷|🩵|🩶|😍|🥰|<3)/u;
let bauschubAnsage = 0;

// Herzen: still – je X Herzen einer Person 1 Stockwerk für ihre Stadt (wird nie angesagt oder angezeigt)
function like(u, anzahl) {
  S.likesGesamt += anzahl; likeLog.push([Date.now(), anzahl]);
  const pro = CFG.turm.herzenProStockwerk ?? 10, p = S.spieler[String(u?.uniqueId || '').toLowerCase()];
  if (!pro || !p?.stadt || !S.staedte[p.stadt]) return;
  p.herzen = (p.herzen || 0) + anzahl;
  const n = Math.floor(p.herzen / pro); if (n > 0) { p.herzen -= n * pro; turmWachsen(p.stadt, n, p); }
}
const likeLog = [];
// TikTok-Regeln: Folgen/Teilen/Geschenke bringen nichts – nur ein Danke (Geschenk: „Danke, Name!“ mit Herzen, für alle gleich)
const followDank = [];
function follow(u) {
  const id = String(u.uniqueId || '').toLowerCase(); if (!id || gesperrt(id)) return;
  sende({ typ: 'follow', name: S.spieler[id]?.name || '@' + u.uniqueId });
  if (einmal(id, 'follow', 10 * 60000)) followDank.push({ name: sprechName({ name: '@' + u.uniqueId }) });
}
function teilen(u) {
  const id = String(u.uniqueId || '').toLowerCase(); if (!id || gesperrt(id)) return;
  if (einmal(id, 'teilen', 10 * 60000)) sag(satz('teilen', { name: sprechName({ name: '@' + u.uniqueId }) }), 1);
}
function geschenk(u) {
  const id = String(u?.uniqueId || '').toLowerCase(); if (!id || gesperrt(id)) return;
  if (!einmal(id, 'geschenk', 10 * 60000)) return;
  const name = S.spieler[id]?.name || '@' + u.uniqueId;
  sende({ typ: 'danke', name, stadt: S.spieler[id]?.stadt || null });
  sag(satz('danke', { name: sprechName({ name }) }), 1);
}

// ---------- Städte-Events ----------
const EV = macheEvents({
  CFG, test: TEST, sende: e => sende(e), zustand: () => zustand(), sag: (t, pr) => sag(t, pr), name: p => sprechName(p),
  spieler: id => S.spieler[id], stadt: n => S.staedte[n], staedte: () => rangListe(), stadtAus: t => stadtAus(t),
  turmWachsen: (n, um, p) => turmWachsen(n, um, p),
});

// ---------- Stimme (macOS „say“, unbegrenzt, offline) ----------
// Prio 0: Geschenk-Dank, Event-Ansagen · 1: Follow-Dank, Countdown · 2: Haus-Ausbau · 3: Kleinkram · 4: Dauer-Moderation
// Untertitel erscheinen genau dann, wenn Kerstin den Satz spricht. „…“ im Text = Sprechpause.
const warte = []; let spricht = false; const gesprochen = [], kleinkram = [];   // kleinkram: nur Prio-2/3-Ansagen fürs Limit
const TON_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'muscheltal-ton-')); let tonNr = 0;
let stimme = CFG.stimme.mac, stilleSeit = Date.now();
const ECHT = !STILL && process.platform === 'darwin';
const dauerMs = t => t.length * 62 + (t.match(/…/g) || []).length * 450 + 300;   // Schätzung ohne echte Stimme
let ohnePausen = false;                                    // manche Premium-Stimmen hängen an [[slnc]]-Befehlen
const fuerStimme = t => ohnePausen ? t.replace(/\s*…\s*/g, ', ') : t.replace(/\s*…\s*/g, ' [[slnc 250]] ').replace(/([!?])\s+/g, '$1 [[slnc 150]] ');
const ohneLike = t => String(t)
  .replace(/\bgeliked\b/gi, 'Herzen geschickt').replace(/\bliked\b/gi, 'schickt Herzen').replace(/\bliken\b/gi, 'Herzen schicken')
  .replace(/\bLike-/gi, 'Herzen-').replace(/\bLikes\b/gi, 'Herzen').replace(/\bLike\b/gi, 'Herz');
function sag(text, prio = 2) {
  if (!text) return;
  text = ohneLike(text);                                    // Das Wort „Like“ wird nie ausgesprochen
  if (satzAnstoessig(text)) { console.log('🚫 Satz nicht gesprochen (Filter):', text); return; }
  const jetzt = Date.now();
  while (gesprochen.length && jetzt - gesprochen[0] > 60000) gesprochen.shift();
  while (kleinkram.length && jetzt - kleinkram[0] > 60000) kleinkram.shift();
  if (prio >= 2 && prio <= 3) { if (kleinkram.length >= CFG.stimme.maxProMinute) return; kleinkram.push(jetzt); }   // Kleinkram nicht stapeln
  warte.push({ text, prio, t: jetzt });
  warte.sort((a, b) => a.prio - b.prio || a.t - b.t);
  // Geschenk-Dank und Event-Ansagen (Prio 0/1) werden nie verworfen, nur Kleinkram
  while (warte.length > CFG.stimme.maxWarteschlange) { const i = warte.findLastIndex(w => w.prio >= 2); if (i < 0) break; warte.splice(i, 1); }
  // Veraltete Kleinigkeiten (älter als 20 s) fallen weg
  for (let i = warte.length - 1; i >= 0; i--) if (warte[i].prio >= 2 && jetzt - warte[i].t > 20000) warte.splice(i, 1);
  weiter();
}
let sprichtSeit = 0, ansageNr = 0;
// Sicherung: Sprache erzeugen darf max. 10 s dauern, Abspielen max. 20 s. Hängt das Erzeugen öfter, hilft sich das Programm selbst.
let schritt = '', haenger = 0;
setInterval(() => {
  const grenze = schritt === 'piper' ? 8000 : schritt === 'gemini' ? 35000 : schritt === 'erzeugen' ? 25000 : 20000;
  if (schritt === 'piper' && spricht && Date.now() - sprichtSeit >= grenze) { console.log('⚠️  Piper hing – starte die Stimme neu.'); sprichtSeit = Date.now(); PIPER.neustart(); return; }
  if (!spricht || Date.now() - sprichtSeit < grenze) return;
  console.log(`⚠️  Ansage hing beim ${schritt === 'erzeugen' ? 'Erzeugen der Sprache (say, Stimme „' + stimme + '“)' : schritt === 'abspielen' ? 'Abspielen (afplay)' : 'Warten (' + schritt + ')'} – Kerstin macht weiter.`);
  if (schritt === 'erzeugen' && ++haenger >= 2) {
    haenger = 0;
    if (!ohnePausen) { ohnePausen = true; console.log('   → Versuche es ab jetzt ohne Sprechpausen-Befehle.'); }
    else { const e = CFG.stimme.macErsatz.shift(); if (e) { stimme = e; console.log(`   → Wechsle auf die Stimme „${e}“.`); } }
  }
  sprichtSeit = Date.now();
  if (sayProzess && sayProzess.exitCode === null) { try { sayProzess.kill(); } catch { fertig(); } } else fertig();
}, 1000);
function fertig() { ansageNr++; spricht = false; stilleSeit = Date.now(); setTimeout(weiter, 50); }
function weiter() {
  if (spricht || !warte.length) return;
  if (ECHT && !LEDA.aktiv() && !PIPER.bereit && piperErwartet()) { clearTimeout(weiter.t); weiter.t = setTimeout(weiter, 400); return; }   // Stimme startet gerade – kurz warten, nie die Mac-Stimme
  const { text, prio } = warte.shift(); spricht = true; sprichtSeit = Date.now(); gesprochen.push(Date.now()); letzteAnsageZeit = Date.now();
  let untertitelDa = false;
  const untertitel = () => { if (!untertitelDa) { untertitelDa = true; sende({ typ: 'ansage', text, ms: dauerMs(text) }); } };
  if (!(ECHT && LEDA.aktiv())) untertitel();                // bei Leda erst, wenn die Stimme bereit ist (fällt ein Satz weg, kein stummer Untertitel)
  if (!ECHT) { setTimeout(fertig, dauerMs(text)); return; }
  const aufSeite = CFG.stimme.wiedergabe !== 'mac' && seiteHatTon() && Date.now() > stimmeFehlerBis;
  // Sprach-Speicher: schon einmal erzeugte Sätze werden sofort wieder abgespielt (spart die lange Erzeugung)
  const key = crypto.createHash('md5').update(`${LEDA.aktiv() ? 'gemini:' + LEDA.stimme : PIPER.bereit ? 'piper2:' + PIPER.name : stimme}|${CFG.stimme.tempo}|${ohnePausen}|${text}`).digest('hex');
  const fertigDatei = path.join(CACHE_DIR, key + '.wav'), datei = path.join(TON_DIR, `s${++tonNr % 20}.wav`);
  const args = ['-v', stimme, '-r', String(CFG.stimme.tempo)];
  // Immer erst eine Sprachdatei erzeugen (say hängt sonst manchmal an Mehrfach-Ausgabe/BlackHole), dann abspielen
  args.push('-o', datei, '--file-format=WAVE', '--data-format=LEI16@22050');
  schritt = 'erzeugen'; const t0say = Date.now();
  let fehler = '', ersatzGesprochen = false;
  const nachErzeugen = code => {
    if (aufSeite && code === 0) {
      schritt = 'seite';                      // Seite spielt ab; warten, bis die Ansage vorbei ist
      let ms = 2000;
      try {                                            // Dauer aus dem WAV-Kopf (Bytes pro Sekunde), nicht geschätzt
        const b = fs.readFileSync(datei), rate = b.readUInt32LE(28) || 44100;
        let o = 12, daten = b.length - 44;
        while (o + 8 <= b.length) { const id = b.toString('ascii', o, o + 4), gr = b.readUInt32LE(o + 4); if (id === 'data') { daten = Math.min(gr, b.length - o - 8); break; } o += 8 + gr + (gr & 1); }
        ms = Math.min(15000, daten / rate * 1000 + 300);
      } catch {}
      sende({ typ: 'stimme', id: tonSeite, url: '/ton/' + path.basename(datei) + '?' + Date.now() });
      if (++unbestaetigt >= 3) { unbestaetigt = 0; stimmeFehlerBis = Date.now() + 60000; console.log('🔈 Live-Seite bestätigt Kerstins Stimme nicht – spreche 1 Minute über die Mac-Lautsprecher.'); }
      setTimeout(fertig, ms);
      return;
    }
    if (code === 0 && !ausSpeicher && !ersatzGesprochen) {
      haenger = 0; const d = Date.now() - t0say;
      try { fs.copyFileSync(datei, fertigDatei); } catch {}
      if (d > 4000) console.log(`🐢 Sprache erzeugen dauerte ${(d / 1000).toFixed(1)} s`);
      // Zu langsam (Premium-Stimmen brauchen auf manchen Macs ~10 s): automatisch auf die schnellere Stimme wechseln
      langsam = d > (CFG.stimme.maxErzeugenSek ?? 4) * 1000 ? langsam + 1 : 0;
      if (langsam >= 2) { const e = CFG.stimme.macErsatz.shift(); if (e) { console.log(`   → „${stimme}“ ist auf diesem Mac zu langsam – wechsle auf „${e}“.`); stimme = e; } langsam = 0; }
    }
    if (!aufSeite && code === 0) {                     // Mac-Ton: Datei mit afplay abspielen (wie die Musik)
      schritt = 'abspielen';
      const ap = sayProzess = spawn('afplay', ['-v', String(CFG.ton.stimmeAufMac ?? 1), ausSpeicher ? fertigDatei : datei]);
      ap.on('error', e => { console.log('⚠️  afplay-Fehler:', e.message); fertig(); });
      ap.on('close', () => fertig());
      return;
    }
    if (code !== 0 && fehler) console.log('⚠️  say meldet:', fehler.trim().slice(0, 200));
    if (code !== 0 && /voice|stimme/i.test(fehler)) {
      const ersatz = CFG.stimme.macErsatz.shift();
      if (ersatz) { console.log(`Stimme „${stimme}“ nicht gefunden, nehme „${ersatz}“.`); stimme = ersatz; warte.unshift({ text, prio: 0, t: Date.now() }); }
    }
    fertig();
  };
  const ausSpeicher = fs.existsSync(fertigDatei);
  if (ausSpeicher) { untertitel(); if (aufSeite) try { fs.copyFileSync(fertigDatei, datei); } catch {} return nachErzeugen(0); }
  // Nächsten Satz schon vorab bei Leda erzeugen, damit er ohne Wartezeit kommt
  if (warte[0]) LEDA.vorab(warte[0].text, gefuehlVon(warte[0].text), namenIn(warte[0].text), warte[0].prio);
  if (LEDA.aktiv()) {                                      // Leda (Gemini): menschliche Stimme mit Gefühl – nur sie spricht
    schritt = 'gemini';
    const nr = ++ansageNr;
    return LEDA.satz(text, gefuehlVon(text), datei, namenIn(text), { prio }).then(ok => {
      if (nr !== ansageNr || !spricht) return;             // inzwischen abgebrochen (Sicherung hat übernommen)
      if (ok) { untertitel(); return nachErzeugen(0); }
      ersatzGesprochen = true;
      // Ersatzstimme nur, wenn in den Einstellungen gewünscht (Standard: keine – dann fällt der Satz weg)
      if (CFG.stimme.ersatz === 'kerstin' && PIPER.bereit) { if (Date.now() - (weiter.kerstinMeldung || 0) > 60000) { weiter.kerstinMeldung = Date.now(); console.log('ℹ️  Gemini und Chirp liefern gerade nichts – Kerstin springt ein (letzter Ersatz).'); } untertitel(); schritt = 'piper'; return PIPER.sprich(text, datei, ok2 => nachErzeugen(ok2 ? 0 : 1)); }
      fertig();
    });
  }
  if (PIPER.bereit) {                                      // Piper: eigene Offline-Stimme, unabhängig vom macOS-Sprachdienst
    schritt = 'piper';
    return PIPER.sprich(text, datei, ok => { if (!ok) fehler = 'Piper konnte den Satz nicht erzeugen'; nachErzeugen(ok ? 0 : 1); });
  }
  const pr = sayProzess = spawn('say', [...args, fuerStimme(text)], { stdio: ['ignore', 'pipe', 'pipe'] });
  pr.on('error', e => { console.log('⚠️  say-Fehler:', e.message); fertig(); });
  pr.stderr.on('data', d => fehler += d);
  pr.on('close', nachErzeugen);
}

// ---------- Piper: Kerstins Stimme offline im eigenen Prozess (werkzeug/stimme-…/…onnx) ----------
// Wird beim Start geladen. Hängt der Prozess, startet er neu. Fehlt das Modell, spricht wie bisher der Mac (say).
var PIPER = { bereit: false, name: '', w: null, auftraege: new Map(), nr: 0 };
// Mac-Stimme (say) nur, wenn es gar kein Piper-Modell gibt oder in den Einstellungen engine 'mac' steht
var piperDa = null, piperDaZeit = 0;
var piperErwartet = () => { if (CFG.stimme.engine === 'mac') return false; if (Date.now() - piperDaZeit > 10000) { piperDaZeit = Date.now(); try { piperDa = fs.readdirSync(path.join(werkzeugMit(CFG.stimme.piperModell || 'stimme-kerstin'), CFG.stimme.piperModell || 'stimme-kerstin')).some(f => f.endsWith('.onnx')); } catch { piperDa = false; } } return piperDa; };
function piperStarten() {
  if (LEDA.aktiv() && CFG.stimme.ersatz !== 'kerstin') return;   // nur Leda: Kerstin wird gar nicht geladen (spart Rechenleistung)
  const ordner = path.join(werkzeugMit(CFG.stimme.piperModell || 'stimme-kerstin'), CFG.stimme.piperModell || 'stimme-kerstin');
  let modell = null; try { modell = fs.readdirSync(ordner).find(f => f.endsWith('.onnx')); } catch {}
  if (!modell || CFG.stimme.engine === 'mac') { if (!modell && ECHT) console.log('ℹ️  Kerstin-Stimme nicht gefunden – ersatzweise spricht die Mac-Stimme.'); return; }
  PIPER.name = modell.replace('.onnx', '');
  const w = PIPER.w = fork(path.join(DIR, 'tts-worker.mjs'), [path.join(ordner, modell), String(CFG.stimme.piperTempo ?? 1.08), String(CFG.stimme.piperLebhaft ?? 0)], { stdio: ['ignore', 'ignore', 'pipe', 'ipc'] });
  let fehlerText = ''; w.stderr.on('data', d => { fehlerText = (fehlerText + d).slice(-400); });
  w.on('message', m => {
    if (m.bereit) { PIPER.bereit = true; console.log(`🗣️  Kerstin spricht mit der Offline-Stimme „${PIPER.name}“ (Piper) – unabhängig vom macOS-Sprachdienst.`); return; }
    const cb = PIPER.auftraege.get(m.id); PIPER.auftraege.delete(m.id);
    if (!m.ok) console.log('⚠️  Piper:', m.fehler);
    cb?.(m.ok);
  });
  w.on('exit', code => {
    if (PIPER.w !== w) return;
    PIPER.bereit = false; PIPER.w = null;
    for (const cb of PIPER.auftraege.values()) cb(false); PIPER.auftraege.clear();
    console.log(`⚠️  Piper-Prozess beendet (${code ?? 'gestoppt'})${fehlerText ? ': ' + fehlerText.trim().split('\n').pop() : ''} – starte neu …`);
    setTimeout(piperStarten, 2000);
  });
}
PIPER.sprich = (text, datei, cb) => { const id = ++PIPER.nr; PIPER.auftraege.set(id, cb); PIPER.w.send({ id, text, datei, gefuehl: gefuehlVon(text) }); };
// Welches Gefühl passt zum Satz? (Jubel bei großen Momenten, freundlich bei Begrüßung/Dank, spannend bei Events)
function gefuehlVon(t) {
  if (/Wahnsinn|Wow|Unglaublich|sprachlos|Legende|Riesigen Dank|Feuerwerk|Glückwunsch|Platz eins|Aufgestiegen|großen Grundstück|gewinnt|Gewonnen|Geschafft|geschafft|Rekord|Likes!|Party/.test(t)) return 'jubel';
  if (/^(Hallo|Hi|Hey|Willkommen|Danke|Lieben Dank|Vielen Dank|Schön|Neuer Bewohner|Neues Zelt|Ein Zelt|Da ist ja)/.test(t) || /Danke|Willkommen|Hallo/.test(t)) return 'froh';
  if (/Achtung|Sekunden|Event|Abstimmung|Mini-Aufgabe|Schnell|Los, los|Wer |Was |Gleich|!$/.test(t)) return 'spannend';
  return 'normal';
}
PIPER.neustart = () => { const w = PIPER.w; PIPER.bereit = false; PIPER.w = null; for (const cb of PIPER.auftraege.values()) cb(false); PIPER.auftraege.clear(); try { w?.kill(); } catch {} setTimeout(piperStarten, 500); };
setTimeout(piperStarten, 200);
let langsam = 0;
// Beim Start alle festen Sätze leise im Hintergrund vorab erzeugen (niedrige Priorität), damit sie im LIVE sofort kommen
function vorwaermen() {
  if (!ECHT) return;
  if (LEDA.aktiv()) {                                       // Leda: feste Sätze nach und nach im Leerlauf erzeugen (einmalig, danach gespeichert)
    const offen = [...new Set(festeSaetzeAus(['erklaeren', 'countdown30', 'countdown10', 'eventNoch10', 'start']))];   // nur Sätze, die wirklich vorkommen
    let i = 0;
    const naechster = () => {
      if (!LEDA.aktiv() || i >= offen.length) return;
      if (spricht || warte.length) return setTimeout(naechster, 2000);
      if (LEDA.frei() < 4 || LEDA.restGesamt() < 40) return setTimeout(naechster, 15000);   // Kontingent gehört den echten Ansagen
      const t = offen[i++]; LEDA.satz(t, gefuehlVon(t), null, [], { prio: 3, warteMs: 0, nurGemini: true }).finally(() => setTimeout(naechster, 8000));
    };
    return setTimeout(naechster, 8000);
  }
  if (PIPER.bereit || PIPER.w || piperErwartet()) return;  // Piper braucht kein Vorab-Erzeugen (und keine Mac-Stimme)
  const offen = [...festeSaetze(), ...Object.values(require_preis())].filter(Boolean);
  let i = 0, fertigN = 0;
  const naechster = () => {
    if (spricht || warte.length) return setTimeout(naechster, 1500);
    while (i < offen.length) {
      const text = offen[i++], key = crypto.createHash('md5').update(`${PIPER.bereit ? 'piper2:' + PIPER.name : stimme}|${CFG.stimme.tempo}|${ohnePausen}|${text}`).digest('hex'), ziel = path.join(CACHE_DIR, key + '.wav');
      if (fs.existsSync(ziel)) continue;
      const tmp = ziel + '.tmp.wav';
      const pr = spawn('nice', ['-n', '15', 'say', '-v', stimme, '-r', String(CFG.stimme.tempo), '-o', tmp, '--file-format=WAVE', '--data-format=LEI16@22050', fuerStimme(text)]);
      pr.on('error', () => setTimeout(naechster, 1000));
      pr.on('close', c => { if (c === 0) { try { fs.renameSync(tmp, ziel); fertigN++; } catch {} } setTimeout(naechster, 200); });
      return;
    }
    if (fertigN) console.log(`🗣️  ${fertigN} feste Sätze vorab erzeugt – kommen im LIVE sofort.`);
  };
  setTimeout(naechster, 5000);
}
const require_preis = () => EV.preise ? EV.preise() : {};
setTimeout(vorwaermen, 3000);
// Sprach-Speicher in werkzeug/stimme (bleibt zwischen den Streams erhalten, höchstens 2.000 Sätze)
const CACHE_DIR = path.join(werkzeugMit('stimme'), 'stimme');   // mit Muschel-Tal LIVE geteilt (falls vorhanden)
 fs.mkdirSync(CACHE_DIR, { recursive: true });
var LEDA = geminiStimme({ dir: DIR, cacheDir: CACHE_DIR, cfg: CFG.stimme });
if (ECHT) console.log(LEDA.an() ? `🎙️  Moderation: Leda (Gemini, mit Gefühl) – ${LEDA.info()}.` : CFG.stimme.engine === 'gemini' ? 'ℹ️  Kein Gemini-Schlüssel (gemini-schluessel.txt) – Kerstin moderiert.' : '');
try { const f = fs.readdirSync(CACHE_DIR).map(n => ({ n, t: fs.statSync(path.join(CACHE_DIR, n)).mtimeMs })).sort((a, b) => b.t - a.t); f.slice(2000).forEach(x => fs.unlinkSync(path.join(CACHE_DIR, x.n))); } catch {}

// ---------- Ton-Absicherung ----------
// Läuft auf keiner Live-Seite Ton (Browser blockiert ihn), spielen Stimme und Musik direkt über die Mac-Lautsprecher.
var sayProzess = null, lokalMusik = null, lokalNr = 0, tonSeite = null, stimmeFehlerBis = 0, unbestaetigt = 0;
const tonStatus = new Map();                               // Seiten-Nr. -> { an, zeit, vorschau, seit }
const seiteHatTon = () => { const st = tonStatus.get(tonSeite); return !!st && st.an && Date.now() - st.zeit < 15000; };
// Genau EINE Seite spielt Ton: bevorzugt eine, auf der Ton schon läuft, sonst die zuerst geöffnete (keine Vorschau)
// Spielt die gewählte Seite nach 8 s noch keinen Ton, kommt die nächste dran (LIVE Studio lädt die Seite manchmal doppelt).
let rolleSeit = 0; const tonFehl = new Map();             // Seiten-Nr. -> wann zuletzt ohne Ton
function waehleTonSeite() {
  if (CFG.stimme.wiedergabe === 'mac') { if (tonSeite !== null) { tonSeite = null; sende({ typ: 'tonRolle', id: null }); } return; }
  if (CFG.stimme.wiedergabe === 'browser') {               // nur der Ton-Tab (?ton) spielt Ton – nie die Seite in LIVE Studio
    const tabs = [...kunden.keys()].filter(id => tonStatus.get(id)?.tonseite);
    const neu = tabs.includes(tonSeite) ? tonSeite : (tabs.find(id => tonStatus.get(id)?.an) ?? tabs[0] ?? null);
    if (neu !== tonSeite) { tonSeite = neu; sende({ typ: 'tonRolle', id: tonSeite }); if (tonSeite != null) console.log(`🔊 Ton-Tab verbunden (#${tonSeite}).`); }
    return;
  }
  const offen = [...kunden.keys()].filter(id => !tonStatus.get(id)?.vorschau);
  const mitTon = offen.filter(id => tonStatus.get(id)?.an);
  let neu = tonSeite;
  if (!offen.includes(tonSeite)) neu = null;
  else if (!tonStatus.get(tonSeite)?.an && Date.now() - rolleSeit > 8000) {   // hängt – weiterreichen
    tonFehl.set(tonSeite, Date.now());
    const andere = offen.filter(id => id !== tonSeite).sort((a, b) => (tonFehl.get(a) || 0) - (tonFehl.get(b) || 0));
    if (andere.length) neu = mitTon[0] ?? andere[0];
  }
  if (neu == null) neu = mitTon[0] ?? [...offen].sort((a, b) => (tonFehl.get(a) || 0) - (tonFehl.get(b) || 0))[0] ?? null;
  if (neu !== tonSeite) { tonSeite = neu; rolleSeit = Date.now(); sende({ typ: 'tonRolle', id: tonSeite }); if (tonSeite != null) console.log(`🔊 Ton-Aufgabe → Live-Seite #${tonSeite}`); }
}
// Musik: eigene Lagunen-Musik (seite/musik/lagune_*.mp3, lizenzfrei, tools/make_music_lagune.py). Weitere MP3s dort werden mitgespielt.
const MUSIK_ORDNER = path.join(DIR, 'seite', 'musik');
const musikListe = () => { try { return fs.readdirSync(MUSIK_ORDNER).filter(f => f.toLowerCase().endsWith('.mp3') && !/^(atmo|meer)/.test(f)).sort(); } catch { return []; } };
const MUSIK_LISTE = musikListe(), MUSIK_DATEIEN = MUSIK_LISTE.map(f => path.join(MUSIK_ORDNER, f));
if (!MUSIK_DATEIEN.length) console.log('⚠️  Keine Musik gefunden – bitte die MP3-Dateien in den Ordner „werkzeug/musik“ legen (im Programmordner).');
else console.log(`🎵 ${MUSIK_DATEIEN.length} ${MUSIK_DATEIEN.length === 1 ? "Musikstück" : "Musikstücke"} gefunden.`);
function musikLokal() {
  const macModus = CFG.stimme.wiedergabe === 'mac';
  const brauche = process.platform === 'darwin' && CFG.ton.musikAufMac !== false && (macModus || (!seiteHatTon() && Date.now() - START > 15000));
  if (brauche && !lokalMusik) {
    const f = MUSIK_DATEIEN[lokalNr++ % MUSIK_DATEIEN.length];
    lokalMusik = spawn('afplay', ['-v', String(CFG.ton.musikAufMacLautstaerke ?? .18), f]);
    lokalMusik.on('close', () => { lokalMusik = null; });
    if (!macModus) console.log('🎵 Kein Ton auf der Live-Seite – Musik und Stimme laufen über die Mac-Lautsprecher.');
  }
  if (!brauche && lokalMusik) { lokalMusik.kill(); lokalMusik = null; }
}
const START = Date.now();
// Ton-Ausgabe des Macs prüfen: Damit die Zuschauer Kerstin hören, muss sie auf „Gerät mit mehreren Ausgängen“ (mit BlackHole) stehen
var tonAusgabe = '', tonAusgabeOk = null;
function tonAusgabePruefen() {
  if (process.platform !== 'darwin') return;
  const pr = spawn('system_profiler', ['SPAudioDataType', '-json']); let out = '';
  pr.stdout.on('data', d => out += d); pr.on('error', () => {});
  pr.on('close', () => {
    try {
      const geraete = JSON.parse(out).SPAudioDataType.flatMap(x => x._items || []);
      const aus = geraete.find(g => g.coreaudio_default_audio_output_device === 'spaudio_yes');
      if (!aus) return;
      const name = aus._name || '', ok = /mehrere|multi|blackhole|aggregat/i.test(name);
      if (ok !== tonAusgabeOk || name !== tonAusgabe) {
        if (ok) console.log(`✅ Ton-Ausgabe des Macs: „${name}“ – Kerstin und Musik gehen in den Stream.`);
        else console.log(`ℹ️  Ton-Ausgabe des Macs: „${name}“ (wenn du BlackHole nutzt, gehört hier „Gerät mit mehreren Ausgängen“ hin).`);
      }
      tonAusgabe = name; tonAusgabeOk = ok;
    } catch {}
  });
}
setTimeout(tonAusgabePruefen, 2000); setInterval(tonAusgabePruefen, 30000);
// Alle 30 s eine kurze Statuszeile im Terminal – hilft bei der Fehlersuche während des LIVEs
var letzteAnsageZeit = 0;
setInterval(() => {
  const seiten = [...kunden.keys()].map(id => { const t = tonStatus.get(id) || {}; return `#${id}${t.vorschau ? '(Vorschau)' : ''}${id === tonSeite ? '★' : ''} Ton ${t.an ? 'an' : 'aus'}/${t.ac || '?'}`; });
  const weg = ECHT ? (CFG.stimme.wiedergabe !== 'mac' && seiteHatTon() && Date.now() > stimmeFehlerBis ? 'Seite (Stream)' : 'Mac-Lautsprecher') : 'aus (Test)';
  console.log(`ℹ️  ${new Date().toLocaleTimeString('de-DE')} · TikTok: ${tiktokStatus} (${tiktokEreignisse} Ereignisse${tiktokLetztes ? ', letztes vor ' + Math.round((Date.now() - tiktokLetztes) / 1000) + ' s' : ''}) · Seiten: ${seiten.join(', ') || 'keine!'} · Stimme: ${LEDA.aktiv() ? 'Leda (' + LEDA.info() + ')' : 'Kerstin'} über ${weg}${tonAusgabe ? ` (Mac-Ausgabe: ${tonAusgabe})` : ''} · letzte Ansage vor ${letzteAnsageZeit ? Math.round((Date.now() - letzteAnsageZeit) / 1000) + ' s' : '–'}`);
}, 30000);
setInterval(musikLokal, 3000);
process.on('exit', () => lokalMusik?.kill());

// ---------- Moderation: nur bei Anlass, dazu regelmäßig die Spielerklärung ----------
const begruessen = [], begruesst = new Set();
let letzteBegruessung = 0, letzteErklaerung = Date.now() - 60000, letzterSpot = Date.now(), countdownGesagt = '', eventZehnGesagt = '';
function moderiere() {
  if (spricht || warte.length || Date.now() - stilleSeit < (followDank.length ? .8 : (CFG.stimme.pauseSek ?? 3)) * 1000) return;
  if (followDank.length) return sag(satz('followEins', { name: followDank.shift().name }), 1);
  // Begrüßung nur mit Klarnamen (lara91554 → „Lara“), höchstens alle 30 s
  while (begruessen.length && !begruessen[0].klar) begruessen.shift();
  if (!EV.laeuft() && begruessen.length && Date.now() - letzteBegruessung > 30000) {
    const b = begruessen.shift(); letzteBegruessung = Date.now();
    return sag(b.stadt ? satz('begruessungStadt', { name: b.name, stadt: b.stadt }) : b.zurueck ? satz('begruessungZurueck', { name: b.name }) : satz('begruessungEins', { name: b.name }), 3);
  }
  // Spielerklärung alle paar Minuten (feste Sätze → einmal erzeugt, danach kostenlos)
  if (!EV.laeuft() && Date.now() - letzteErklaerung > (CFG.turm.erklaerenMinuten ?? 3) * 60000) {
    letzteErklaerung = Date.now(); sende({ typ: 'erklaeren' }); return sag(satz('erklaeren'), 3);
  }
}
setInterval(() => {
  const s = EV.naechstesIn(), runde = String(Math.floor(Date.now() / 60000));
  if (s <= 31 && s >= 29 && countdownGesagt !== runde + 30) { countdownGesagt = runde + 30; sag(satz('countdown30'), 1); }
  if (s <= 11 && s >= 9 && countdownGesagt !== runde + 10) { countdownGesagt = runde + 10; sag(satz('countdown10'), 1); }
  const r = EV.restSek();
  if (r != null && r <= 11 && r >= 9 && eventZehnGesagt !== runde) { eventZehnGesagt = runde; sag(satz('eventNoch10'), 1); }
  // Kamera steht sonst still (spart Rechenleistung) – nur ab und zu ein kurzer Blick auf die führende Stadt
  if (!EV.laeuft() && Date.now() - letzterSpot > (CFG.turm.spotlightMinuten ?? 2) * 60000 && rangListe().length) { letzterSpot = Date.now(); sende({ typ: 'spotlight', stadt: rangListe()[0].name }); }
  moderiere();
}, 400);
function beitritt(u) {
  const id = String(u.uniqueId || '').toLowerCase();
  if (!id || begruesst.has(id) || gesperrt(id) || anstoessig(u.uniqueId) || anstoessig(u.nickname)) return;
  begruesst.add(id);
  const p = S.spieler[id], name = sprechName({ name: '@' + u.uniqueId });
  begruessen.push({ name, klar: !!klarname(u.uniqueId), zurueck: !!p, stadt: p?.stadt || null });
  if (begruessen.length > 6) begruessen.splice(0, begruessen.length - 6);
}
// Stream-Ende: Stadt des Tages
function streamEnde() {
  const heute = top(S.heute?.id === tagId() ? S.heute.m : {}, 1)[0] || (rangListe()[0] && { name: rangListe()[0].name, m: 0 }); if (!heute) return;
  S.sieger = [{ stadt: heute.name, datum: tagId(), m: heute.m }, ...(S.sieger || [])].slice(0, 30); geaendert = true;
  sende({ typ: 'tagessieger', stadt: heute.name, m: heute.m }); sag(satz('tagessieger', { stadt: heute.name }), 0); speichern();
}

// ---------- Seite + Live-Daten (Server-Sent Events) ----------
// ---------- Live-Daten an die Seite: einfache Abfragen (/poll), funktionieren auch durch den Cloudflare-Tunnel ----------
// Jede Seite fragt ca. 3× pro Sekunde nach. Ereignisse liegen nummeriert in einer Liste; die große Bewohnerliste
// wird nur mitgeschickt, wenn sie sich geändert hat, und die Antwort wird gepackt (gzip).
const kunden = new Map(); let letzteSeitenAnsage = 0, seitenNr = 0;      // Seiten-Nr. -> zuletzt gesehen
const LOG = [], listeZeit = new Map(); let seq = 0, letzterZustand = null, spielerJSON = '[]', spielerVer = 0;
const wartende = new Set();                                  // offene Abfragen der Live-Seiten (Long-Poll)
function sende(ev) {
  LOG.push({ n: ++seq, ev }); if (LOG.length > 400) LOG.splice(0, LOG.length - 400);
  if (wartende.size) setImmediate(() => { for (const f of wartende) f(); wartende.clear(); });
}
let zLetzt = 0, zOffen = false;
function zustand() {
  if (Date.now() - zLetzt < 250) { if (!zOffen) { zOffen = true; setTimeout(() => { zOffen = false; zustand(); }, 260); } return; }
  zLetzt = Date.now();
  const o = oeffentlich(), sj = JSON.stringify(o.spieler); delete o.spieler;
  if (sj !== spielerJSON) { spielerJSON = sj; spielerVer++; }
  letzterZustand = { typ: 'zustand', s: o }; sende(letzterZustand);
}
setInterval(() => {                                         // Seiten, die nicht mehr fragen, gelten als geschlossen
  let weg = false; for (const [id, z] of kunden) if (Date.now() - z > 8000) { kunden.delete(id); tonStatus.delete(id); weg = true; }
  if (weg) waehleTonSeite();
}, 3000);
function oeffentlich() {
  const l = rangListe();
  return {
    ...EV.oeffentlich(), spieler: [],
    staedte: l.slice(0, 40).map(s => ({ name: s.name, stock: s.stock, leute: s.leute, land: s.land, region: s.region || '', gruender: s.gruender || '', fieber: s.fieberBis > Date.now(), baumeister: Object.entries(s.baumeister || {}).sort((a, b) => b[1] - a[1])[0]?.[0] || '' })),
    anzahlStaedte: l.length, woche: top(S.woche?.id === wocheId() ? S.woche.m : {}), heute: top(S.heute?.id === tagId() ? S.heute.m : {}),
    regionen: Object.entries(l.reduce((m, s) => { if (s.region) { const r = m[s.region] ||= { m: 0, land: s.land }; r.m += s.stock; } return m; }, {})).sort((a, b) => b[1].m - a[1].m).slice(0, 5).map(([name, r]) => ({ name, m: r.m, land: r.land })), neueste: S.neueste || null, stockGesamt: l.reduce((a, s) => a + s.stock, 0), laender: l.reduce((m, s) => (m[s.land || '?'] = (m[s.land || '?'] || 0) + 1, m), {}), ort: CFG.ort, sieger: S.sieger?.[0]?.stadt || null, tiktokName: CFG.tiktokName, test: TEST, ton: CFG.ton, musik: MUSIK_LISTE, bildrate: CFG.bildrate || 30,
  };
}

const TYPEN = { '.mp3': 'audio/mpeg', '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  // Test-Zugänge nur direkt am Mac – nie über den öffentlichen Link (Cloudflare setzt cf-ray / cf-connecting-ip)
  if (TEST && url.pathname === '/test' && !req.headers['cf-ray'] && !req.headers['cf-connecting-ip']) {   // nur Test-Modus, nur am Mac
    const q = url.searchParams, id = q.get('event'); if (id) EV.starte(id);
    const nutzer = q.get('user');
    if (nutzer) {
      const u = { uniqueId: nutzer };
      if (q.has('kommentar')) kommentar(u, q.get('kommentar'));
      if (q.has('like')) like(u, +q.get('like'));
      if (q.has('follow')) follow(u);
      if (q.has('teilen')) teilen(u);
      if (q.has('gift')) geschenk(u);
      if (q.has('beitritt')) beitritt(u);
    }
    if (q.has('ende')) EV.beendeJetzt();
    if (q.has('streamende')) streamEnde();
    if (q.has('spot') && rangListe().length) sende({ typ: 'spotlight', stadt: rangListe()[0].name });
    if (q.has('erklaeren')) sende({ typ: 'erklaeren' });
    if (q.has('zustand')) { res.writeHead(200, { 'Content-Type': 'application/json' }); return res.end(JSON.stringify({ ...oeffentlich(), alle: rangListe(), spieler: S.spieler })); }
    res.writeHead(204); return res.end();
  }
  if (url.pathname === '/tonstatus') {                       // Live-Seite meldet, ob ihr Ton läuft
    const id = +url.searchParams.get('id'), alt = tonStatus.get(id) || {};
    if (url.searchParams.has('an')) tonStatus.set(id, { ...alt, an: url.searchParams.get('an') === '1', ac: url.searchParams.get('ac'), vorschau: url.searchParams.get('vorschau') === '1', zeit: Date.now() });
    if (url.searchParams.get('stimme') === '1' && alt.stimmeOk !== true) { tonStatus.set(id, { ...tonStatus.get(id), stimmeOk: true }); console.log(`🔊 Kerstin spricht über die Live-Seite #${id} (Stream-Ton).`); }
    if (url.searchParams.get('stimme') === '0') console.log(`   Grund (Seite #${id}): ${url.searchParams.get('grund') || '?'}`);
    if (url.searchParams.get('stimme') === '0') { stimmeFehlerBis = Date.now() + 60000; console.log('🔈 Stimme auf der Seite blockiert – spreche über die Mac-Lautsprecher.'); }
    if (url.searchParams.get('stimme') === '1') { stimmeFehlerBis = 0; unbestaetigt = 0; }
    waehleTonSeite();
    res.writeHead(204); return res.end();
  }
  if (url.pathname === '/poll') {
    // Nichts Neues? Kurz offen halten und sofort antworten, wenn etwas passiert (max. 8 s)
    const nAlt = +url.searchParams.get('n') || 0;
    if (url.searchParams.get('w') === '1' && nAlt && nAlt >= seq && !req._gewartet) {
      req._gewartet = true; const id0 = +url.searchParams.get('id') || 0; if (id0) kunden.set(id0, Date.now());
      let fertigF; const t = setTimeout(() => { wartende.delete(fertigF); fertigF(); }, 8000);
      fertigF = () => { clearTimeout(t); server.emit('request', req, res); };
      wartende.add(fertigF); req.on('close', () => { clearTimeout(t); wartende.delete(fertigF); });
      return;
    }
    let id = +url.searchParams.get('id') || 0;
    const neu = !id || !kunden.has(id);
    if (neu && !id) id = ++seitenNr;
    kunden.set(id, Date.now());
    if (url.searchParams.has('an')) { const alt = tonStatus.get(id) || {}; tonStatus.set(id, { ...alt, an: url.searchParams.get('an') === '1', ac: url.searchParams.get('ac'), vorschau: url.searchParams.get('vorschau') === '1', tonseite: url.searchParams.get('tonseite') === '1', zeit: Date.now() }); }
    waehleTonSeite();
    const n = +url.searchParams.get('n') || 0, sv = +url.searchParams.get('sv');
    if (!letzterZustand) zustand();
    // Erste Abfrage oder zu weit zurück: nur den aktuellen Zustand (keine alten Shows/Banner nachspielen)
    let ev = (!n || (LOG[0] && n < LOG[0].n - 1)) ? [letzterZustand] : LOG.filter(x => x.n > n).map(x => x.ev);
    const z = ev.filter(e => e.typ === 'zustand').pop(); ev = ev.filter(e => e.typ !== 'zustand'); if (z) ev.push(z);   // nur der neueste Zustand
    const mitListe = sv !== spielerVer && (Date.now() - (listeZeit.get(id) || 0) > 900);      // Bewohnerliste höchstens 1×/s
    if (mitListe) listeZeit.set(id, Date.now());
    const antwort = { id, n: seq, ev, tonSeite, sv: mitListe ? spielerVer : sv, spieler: mitListe ? JSON.parse(spielerJSON) : undefined };
    let body = Buffer.from(JSON.stringify(antwort)); const kopf = { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' };
    if (/gzip/.test(req.headers['accept-encoding'] || '') && body.length > 1024) { body = zlib.gzipSync(body); kopf['Content-Encoding'] = 'gzip'; }
    res.writeHead(200, kopf); return res.end(body);
  }
  if (url.pathname.startsWith('/ton/')) {
    const f = path.join(TON_DIR, path.basename(url.pathname));
    return fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': 'audio/wav' }); res.end(d); });
  }
  if (url.pathname.startsWith('/musik/')) { const m = path.join(MUSIK_ORDNER, path.basename(decodeURIComponent(url.pathname))); if (fs.existsSync(m)) return fs.readFile(m, (e, d) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': 'audio/mpeg' }); res.end(d); }); }
  const datei = path.join(DIR, 'seite', path.normalize(url.pathname === '/' ? '/index.html' : url.pathname).replace(/^(\.\.[/\\])+/, ''));
  if (!datei.startsWith(path.join(DIR, 'seite'))) { res.writeHead(403); return res.end(); }
  fs.readFile(datei, (e, d) => {
    if (e) { res.writeHead(404); return res.end('nicht gefunden'); }
    res.writeHead(200, { 'Content-Type': TYPEN[path.extname(datei)] || 'application/octet-stream' }); res.end(d);
  });
}).on('error', e => {
  if (e.code === 'EADDRINUSE') {                            // Programm läuft schon in einem anderen Fenster
    console.log(`\n⚠️  Leuchtturm-Rennen läuft schon (in einem anderen Terminalfenster). Dieses Fenster kannst du schließen.\n`);
    process.exit(2);
  }
  throw e;
}).listen(CFG.port, () => {
  console.log(`\n🗼 Leuchtturm-Rennen läuft:  http://localhost:${CFG.port}   (Version ${VERSION})`);
  console.log('   Diese Adresse in TikTok LIVE Studio als Link-/Browser-Quelle (1080×1920) einfügen.\n');
});

// ---------- TikTok-Verbindung ----------
var geschenkGesehen = new Map();
var tiktokStatus = TEST ? 'Test-Modus' : 'noch nicht verbunden', tiktokEreignisse = 0, tiktokLetztes = 0, likeLogZeit = 0;
function tt(art, text) {                                     // jedes echte TikTok-Ereignis kurz im Terminal zeigen
  tiktokEreignisse++; tiktokLetztes = Date.now();
  if (art === '❤️' && Date.now() - likeLogZeit < 5000) return; if (art === '❤️') likeLogZeit = Date.now();
  console.log(`${art} ${text}`);
}
async function verbinde() {
  const { TikTokLiveConnection, WebcastEvent } = await import('tiktok-live-connector');
  // Keine Geschenkliste abfragen: die braucht bei Eulerstream einen Bezahl-Plan. Name + Coins kommen mit jedem Geschenk.
  const opt = { enableExtendedGiftInfo: false, processInitialData: false };
  if (CFG.eulerApiKey) opt.signApiKey = CFG.eulerApiKey;   // optional: eigener Schlüssel von eulerstream.com (stabiler)
  const c = new TikTokLiveConnection(CFG.tiktokName, opt);
  // Neue TikTok-Schnittstelle: Benutzername steht in displayId (früher uniqueId), Kommentar in content, Likes in count
  const U = u => { const r = u && { ...u, uniqueId: u.uniqueId || u.displayId || u.username || '', nickname: u.nickname || '' }; if (r?.uniqueId) liveDabei(r.uniqueId); return r; };
  const nm = d => '@' + (U(d.user)?.uniqueId || '?');
  const txt = d => d.content ?? d.comment ?? '';
  c.on(WebcastEvent.CHAT, d => { const u = U(d.user); if (!u?.uniqueId) return; tt('💬', `${nm(d)}: ${txt(d)}`); kommentar(u, txt(d)); });
  // TikTok schickt nicht jedes Like einzeln, aber immer die Gesamtzahl (total). Was fehlt, kommt trotzdem in die Kasse.
  let likeTotal = 0; const aktiveLiker = new Map();
  c.on(WebcastEvent.LIKE, d => {
    const u = U(d.user), n = +(d.count ?? d.likeCount) || 1, total = +(d.total ?? d.totalLikeCount) || 0;
    if (u?.uniqueId) { tt('❤️', `${nm(d)} +${n} Likes`); like(u, n); const id = String(u.uniqueId).toLowerCase(), alt = aktiveLiker.get(id); aktiveLiker.set(id, { n: (alt && Date.now() - alt.t < 30000 ? alt.n : 0) + n, t: Date.now() }); } else { S.likesGesamt += n; inKasse(n * CFG.kasse.proLike); }
    if (total) {
      const fehlt = likeTotal ? total - likeTotal - n : 0;   // TikTok meldet nicht jedes Like einzeln – die fehlenden zählen trotzdem
      if (fehlt > 0 && fehlt < 100000) { S.likesGesamt += fehlt; geaendert = true; }
      likeTotal = Math.max(likeTotal, total);
    }
  });
  c.on(WebcastEvent.FOLLOW, d => { const u = U(d.user); if (!u?.uniqueId) return; tt('➕', `${nm(d)} folgt`); follow(u); });
  c.on(WebcastEvent.SHARE, d => { const u = U(d.user); if (!u?.uniqueId) return; tt('🔁', `${nm(d)} teilt`); teilen(u); });
  c.on(WebcastEvent.MEMBER, d => { const u = U(d.user); if (!u?.uniqueId) return; tt('👋', `${nm(d)} ist da`); beitritt(u); });
  c.on(WebcastEvent.GIFT, d => {
    d.user = U(d.user);
    // Neue Schnittstelle: Geschenk steht in d.gift (name, diamondCount, type), früher in d.giftDetails (giftName, giftType)
    const g = d.gift || d.giftDetails || {}, ex = d.extendedGiftInfo || {};
    const serie = g.type === 1 || g.giftType === 1 || g.combo;
    if (serie && !d.repeatEnd) return;                     // Serie (z. B. 5 Rosen) läuft noch – nur einmal am Ende danken
    const schluessel = `${nm(d)}|${d.giftId || g.id}|${d.groupId || ''}|${d.repeatCount || 1}`;
    if (geschenkGesehen.has(schluessel)) return;            // dieselbe Meldung kommt manchmal doppelt
    geschenkGesehen.set(schluessel, Date.now()); for (const [k, t] of geschenkGesehen) if (Date.now() - t > 30000) geschenkGesehen.delete(k);
    const name = g.name || g.giftName || ex.name || '', coins = g.diamondCount || ex.diamond_count || 1, anzahl = d.repeatCount || d.comboCount || 1;
    tt('🎁', `${nm(d)}: ${name || 'Geschenk'} ×${anzahl} (${coins * anzahl} Coins)`);
    geschenk(d.user || {}, name, coins, anzahl);
  });
  c.on(WebcastEvent.STREAM_END, () => { console.log('Stream beendet.'); streamEnde(); });
  c.on('disconnected', () => { if (c.absichtlich) return; tiktokStatus = 'getrennt'; console.log('⚠️  Verbindung zu TikTok weg – neuer Versuch in 15 s'); setTimeout(versuche, 15000); });
  const st = await c.connect();
  tiktokStatus = 'verbunden'; const seit = Date.now(), raum = st?.roomId || c.roomId || '?';
  // Programm läuft schon, bevor in Studio „LIVE gehen“ gedrückt wurde: alter/vorbereiteter Raum ist noch nicht live → warten
  const status = st?.roomInfo?.data?.status ?? st?.roomInfo?.status;
  if (Number(status) === 4) {                                // 4 = Raum beendet (alter LIVE)
    c.absichtlich = true; try { Promise.resolve(c.disconnect()).catch(() => {}); } catch {}
    tiktokStatus = 'wartet auf LIVE';
    if (Date.now() - (verbinde.warteMeldung || 0) > 60000) { verbinde.warteMeldung = Date.now(); console.log('⏳ Dein LIVE läuft noch nicht – sobald du in Studio „LIVE gehen“ drückst, verbindet sich das Programm automatisch.'); }
    return setTimeout(versuche, 10000);
  }
  console.log(`🔗 TikTok-Raum ${raum}`);
  // Wächter: Kommen 90 s lang keine Ereignisse an, hängt die Verbindung oft an einem alten Raum (z. B. Programm vor „LIVE gehen“
  // gestartet oder LIVE neu gestartet) → neu verbinden, dann wird der aktuelle Raum genommen.
  clearInterval(verbinde.w);
  verbinde.w = setInterval(() => {
    if (tiktokStatus !== 'verbunden' || Date.now() - Math.max(tiktokLetztes, seit) < (CFG.tiktokStilleSek ?? 60) * 1000) return;
    clearInterval(verbinde.w); c.absichtlich = true;
    console.log(`🔄 Seit ${CFG.tiktokStilleSek ?? 60} s kommt nichts von TikTok an – verbinde neu (aktueller LIVE-Raum) …`);
    tiktokStatus = 'verbinde neu'; try { Promise.resolve(c.disconnect()).catch(() => {}); } catch {}
    setTimeout(versuche, 3000);
  }, 15000);
  // neuer Stream (für die Stream-Rangliste): wenn noch keiner läuft oder der letzte vor über 30 Min. endete
  console.log(`\n✅✅✅ Mit deinem TikTok-LIVE (@${CFG.tiktokName}) verbunden – Likes, Kommentare und Geschenke kommen jetzt an.\n`);
  // Echte Follower-Zahl = Bewohner (beim Start und alle 5 Minuten)
  const fol = info => { const f = suche(info, 'follower_count'); if (f) { bewohnerVonTikTok = true; setzeBewohner(Number(f), 'tiktok'); } };
  fol(st.roomInfo || c.roomInfo);
  clearInterval(verbinde.t); verbinde.t = setInterval(() => c.fetchRoomInfo().then(fol).catch(() => {}), 300000);
  sag(satz('start'), 0);
}
function suche(o, key, tiefe = 0) {
  if (!o || typeof o !== 'object' || tiefe > 6) return null;
  if (o[key] != null) return o[key];
  for (const v of Object.values(o)) { const r = suche(v, key, tiefe + 1); if (r != null) return r; }
  return null;
}
async function versuche() {
  try { await verbinde(); }
  catch (e) {
    tiktokStatus = 'nicht verbunden';
    console.log(`⏳ TikTok: noch nicht verbunden (${e.constructor?.name || ''}: ${e.message || e}${e.errors ? ' – ' + e.errors.map(x => x.message).join(' | ') : ''}). Neuer Versuch in 15 s …`);
    setTimeout(versuche, 15000);
  }
}

// ---------- Test ohne TikTok ----------
function simulator() {
  console.log('🧪 Test-Modus: simulierte Zuschauer aus verschiedenen Städten.');
  const orte = ['Köln', 'Hamburg', 'aus Berlin', 'München', 'Wien', 'Zürich', 'Buxtehude', 'Oberstdorf', 'Sylt', 'Graz', 'Leipzig', 'Bremen', 'Hambrug', 'Team Dresden', 'Kitzbühel', 'Davos'];
  const leute = Array.from({ length: 40 }, (_, i) => 'tester' + i);
  setInterval(() => {
    const u = { uniqueId: leute[Math.floor(Math.random() * leute.length)] }, r = Math.random(), p = S.spieler[u.uniqueId];
    if (!p?.stadt && r < .5) kommentar(u, orte[Math.floor(Math.random() * orte.length)]);
    else if (EV.laeuft() && r < .5) kommentar(u, ['licht', 'los', 'halten', 'köln', 'berlin', String(Math.floor(Math.random() * 300)), p?.stadt || 'hallo'][Math.floor(Math.random() * 7)]);
    else if (r < .8) kommentar(u, ['hallo', 'cool', 'los geht\'s', 'super'][Math.floor(Math.random() * 4)]);
    else like(u, 5 + Math.floor(Math.random() * 20));
  }, 800);
}

if (TEST && !process.argv.includes('--leer')) simulator(); else if (!TEST) versuche();
for (const art of ['uncaughtException', 'unhandledRejection']) process.on(art, e => {
  if (e?.code === 'EADDRINUSE') return;
  console.log('⚠️  Interner Fehler (Programm läuft weiter):', e?.stack?.split('\n').slice(0, 3).join(' | ') || e);
  if (spricht && Date.now() - sprichtSeit > 3000) fertig();
});
for (const sig of ['SIGINT', 'SIGHUP', 'SIGTERM']) process.on(sig, () => { geaendert = true; speichern(); process.exit(0); });
