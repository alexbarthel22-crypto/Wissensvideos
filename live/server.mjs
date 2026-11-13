// Muschel-Tal LIVE – verbindet TikTok LIVE (Likes, Kommentare, Geschenke) mit der Live-Insel.
// Start:  node server.mjs          (echter Stream, TikTok-Name aus einstellungen.json)
//         node server.mjs --test   (Simulator mit Test-Zuschauern, ohne TikTok)
//         node server.mjs --still  (ohne Stimme)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { macheEvents } from './events.mjs';
import { satz, namenListe } from './saetze.mjs';
import { geschenkFormen } from './geschenke.mjs';
import { anstoessig, satzAnstoessig, ladeSperrliste, gesperrt, normal } from './filter.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const CFG = JSON.parse(fs.readFileSync(path.join(DIR, 'einstellungen.json'), 'utf8'));
const STAND = path.join(DIR, 'stand.json');
const TEST = process.argv.includes('--test');
const STILL = process.argv.includes('--still') || !CFG.stimme.an;
const RUHIG = process.argv.includes('--ruhig');      // Test: wenig Betrieb, kaum Geschenke

// ---------- Spielstand ----------
const leer = () => ({ spieler: {}, reihenfolge: [], projekt: null, fertig: [], likesGesamt: 0, kasse: 0 });
let S = leer();
try { S = { ...leer(), ...JSON.parse(fs.readFileSync(STAND, 'utf8')) }; } catch {}
if (TEST && process.argv.includes('--neu')) S = leer();
let geaendert = false;
const speichern = () => { if (!geaendert || TEST) return; fs.writeFileSync(STAND, JSON.stringify(S)); geaendert = false; };
setInterval(speichern, 10000);

// ---------- Schutz vor anstößigen Namen (filter.mjs, sperrliste.txt) ----------
const anzeigeName = (u, platz) => anstoessig(u.uniqueId) || anstoessig(u.nickname) ? `Bewohner ${platz + 1}` : '@' + u.uniqueId;
function namenPruefen() {                                  // auch für Bewohner aus früheren Streams
  ladeSperrliste(DIR);
  for (const p of Object.values(S.spieler)) {
    p.gesperrt = gesperrt(p.id) || undefined;
    if (p.name.startsWith('@') && anstoessig(p.name)) { p.name = `Bewohner ${p.platz + 1}`; geaendert = true; }
  }
}
S.fertig = (S.fertig || []).filter(id => CFG.abstimmung.projekte.some(x => x.id === id));
if (S.projekt && !CFG.abstimmung.projekte.some(x => x.id === S.projekt.id)) S.projekt = null;
namenPruefen(); setInterval(namenPruefen, 30000);

const stufeVon = m => { let i = 0; CFG.stufen.forEach((s, k) => { if (m >= s.ab) i = k; }); return i; };
for (const p of Object.values(S.spieler)) p.stufe = stufeVon(p.muscheln);   // nach Änderung der Stufen

function spieler(u) {
  const id = String(u.uniqueId || '').toLowerCase();
  if (!id || gesperrt(id)) return null;                   // Sperrliste: komplett ignorieren
  let p = S.spieler[id];
  if (p) p.zuletzt = Date.now();
  if (!p) {
    p = S.spieler[id] = { id, name: anzeigeName(u, S.reihenfolge.length), muscheln: 0, stufe: 0, anbauten: [], farbe: null, platz: S.reihenfolge.length, zuletzt: Date.now() };
    S.reihenfolge.push(id);
    sende({ typ: 'neu', id });
    sag(satz('neu', { name: sprechName(p) }), 3);
  }
  return p;
}

function gibMuscheln(p, n, grund) {
  if (!p || n <= 0) return;
  const vorher = p.stufe;
  p.muscheln += n;
  p.stufe = stufeVon(p.muscheln);
  geaendert = true;
  if (p.stufe > vorher) {
    sende({ typ: 'stufe', id: p.id, stufe: p.stufe });
    sag(satz('stufe', { name: sprechName(p), stufe: artikel(CFG.stufen[p.stufe].name), stufeDativ: dativ(CFG.stufen[p.stufe].name), stufeName: CFG.stufen[p.stufe].name }), 2);
  }
  zustand();
}

const WEIBLICH = /(hütte|villa|Inselvilla mit Hubschrauberlandeplatz)$/i, MAENNLICH = /^(Bungalow|Strandpalast|Korallenpalast)$/;
const dativ = n => (WEIBLICH.test(n) ? 'einer ' : 'einem ') + n;
const artikel = n => (WEIBLICH.test(n) ? 'eine ' : MAENNLICH.test(n) ? 'einen ' : 'ein ') + n;
// Namen für die Stimme lesbar machen: "lena_xx.22" -> "lena xx"
const sprechName = p => p.name.replace(/^@/, '').replace(/[._]+/g, ' ').replace(/\d{3,}/g, '').trim() || 'Neuer Bewohner';

// ---------- „haus“ im Chat = eigenes Haus im Stream zeigen (auch Haus!, hauus, house, huas, mein haus …) ----------
const HAUS_WORTE = ['haus', 'hause', 'haeus', 'hous', 'house', 'huas', 'hasu', 'hus', 'haeuschen', 'zuhause', 'home', 'hutte', 'huete', 'huette'];
const abstand = (a, b) => { const d = Array.from({ length: a.length + 1 }, (_, i) => [i]); for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); return d[a.length][b.length]; };
function istHausWunsch(text) {
  for (const w of String(text || '').split(/\s+/)) {
    const n = normal(w); if (!n) continue;
    if (n.includes('haus') || n.includes('hous') || HAUS_WORTE.includes(n)) return true;
    if (n[0] === 'h' && n.length >= 3 && n.length <= 6 && abstand(n, 'haus') <= 1) return true;
  }
  return false;
}
const hausWunsch = [], hausGezeigt = {};
let letztesHausZeigen = 0;

// ---------- Ereignisse ----------
function like(u, anzahl) {
  const p = spieler(u); if (!p) { S.likesGesamt += anzahl; inKasse(anzahl * CFG.kasse.proLike); return; }
  S.likesGesamt += anzahl; likeLog.push([Date.now(), anzahl]);
  inKasse(anzahl * CFG.kasse.proLike);
  const faktor = EV.like(p, anzahl);                       // Muschelregen ×2, Bau-Turbo ×3
  gibMuscheln(p, anzahl * CFG.muschelnProLike * faktor, 'like');
}

function kommentar(u, text) {
  const neu = !S.spieler[String(u.uniqueId || '').toLowerCase()];
  const p = spieler(u); if (!p) return;
  if (neu) gibMuscheln(p, CFG.muschelnFuerErstenKommentar, 'kommentar');
  const t = String(text || '').toLowerCase().trim();
  if (EV.kommentar(p, t)) { geaendert = true; zustand(); return; }   // Event-Antworten (rot, flasche, A, 42 …)
  if (istHausWunsch(t) && !hausWunsch.includes(p.id) && Date.now() - (hausGezeigt[p.id] || 0) > 120000) {
    hausWunsch.push(p.id); if (hausWunsch.length > 20) hausWunsch.shift();
  }
  for (const wort of t.split(/[^a-zäöüß]+/)) {
    const ab = CFG.anbauten[wort];
    if (ab) {
      if (p.anbauten.includes(wort)) continue;
      if (p.stufe < ab.abStufe) { sende({ typ: 'info', id: p.id, text: `${ab.name} ab ${CFG.stufen[ab.abStufe].name}` }); continue; }
      if (p.muscheln < ab.kosten) { sende({ typ: 'info', id: p.id, text: `${ab.name}: ${ab.kosten} 🐚` }); continue; }
      p.anbauten.push(wort); geaendert = true;
      sende({ typ: 'anbau', id: p.id, was: wort });
      sag(satz('anbau', { name: sprechName(p), anbau: { Boot: 'ein Boot', Palme: 'eine Palme', Laterne: 'eine Laterne', Flagge: 'eine Flagge' }[ab.name] || 'einen ' + ab.name }), 3);
    }
    const f = CFG.farben[wort];
    if (f && p.farbe !== f) { p.farbe = f; geaendert = true; sende({ typ: 'farbe', id: p.id }); }
  }
  zustand();
}

function geschenk(u, name, diamanten, anzahl) {
  const p = spieler(u); if (!p) { inKasse(Math.max(1, diamanten || 1) * Math.max(1, anzahl || 1) * CFG.kasse.proCoin); return; }
  const d = Math.max(1, diamanten || 1) * Math.max(1, anzahl || 1);   // Coins insgesamt: 1 Coin = 1 Muschel (= 0,01 €)
  const g = geschenkFormen(name, anzahl);                  // deutsch, mit Artikel: „für die Rose“, „einen Löwen“
  sende({ typ: 'geschenk', id: p.id, name: g.name, anzahl, diamanten: d });
  EV.geschenkShow(p, g, anzahl, d);
  inKasse(d * CFG.kasse.proCoin);
  sag(satz(d >= 1000 ? 'geschenkGross' : d >= 100 ? 'geschenkMittel' : 'geschenkKlein', { name: sprechName(p), fuer: g.fuer, einAkk: g.einAkk, einNom: g.einNom, EinNom: grossKlein(g.einNom) }), 0);
  gibMuscheln(p, d * CFG.muschelnProCoin, 'geschenk');
}

// ---------- Muschelkasse der Live-Insel (getrennt von der Inselkasse der Haupt-Insel) ----------
if (S.kasse == null) S.kasse = S.likesGesamt || 0;
function inKasse(n) {
  S.kasse += n; geaendert = true;
  if (S.projekt) {
    S.projekt.stand = Math.min(S.projekt.ziel, S.projekt.stand + n);
    if (S.projekt.stand >= S.projekt.ziel) projektFertig();
  }
}

// ---------- Bauprojekte + Bewohnerzahl der Homepage ----------
// Holt muscheltal/daten/insel.json und einwohner.csv direkt aus dem öffentlichen GitHub-Repo (immer aktuell),
// sonst aus dem Nachbarordner ../muscheltal/daten, sonst aus einstellungen.json. Der Ordner live/ reicht also allein.
const ROH = CFG.homepageDaten || 'https://raw.githubusercontent.com/alexbarthel22-crypto/Wissensvideos/claude/sweet-hamilton-2bxep9/muscheltal/daten/';
const LOKAL = path.join(DIR, '..', 'muscheltal', 'daten');
let BAUPROJEKTE = CFG.bewohner.ziele, bewohnerVonTikTok = false;
async function holeDatei(name) {
  try { const r = await fetch(ROH + name, { signal: AbortSignal.timeout(8000) }); if (r.ok) return await r.text(); } catch {}
  try { return fs.readFileSync(path.join(LOKAL, name), 'utf8'); } catch { return null; }
}
async function ladeHomepage() {
  const j = await holeDatei('insel.json');
  try {
    const d = JSON.parse(j);
    if (Array.isArray(d.baustellen) && d.baustellen.length)
      BAUPROJEKTE = d.baustellen.map(b => ({ name: b.name, icon: b.emoji || '🏗️', ziel: b.ziel, ort: 'Haupt-Insel' }));
  } catch {}
  const csv = await holeDatei('einwohner.csv');
  const n = csv ? csv.trim().split('\n').length - 1 : 0;
  if (n > 0 && !bewohnerVonTikTok && n > bewohner) { bewohner = n; S.bewohner = n; }   // still, ohne Ansage
  zustand();
}
setTimeout(ladeHomepage, 0); setInterval(ladeHomepage, 600000);

// ---------- Bewohner (= Follower) ----------
let bewohner = Math.max(S.bewohner || 0, CFG.bewohner.start || 0);
const zielJetzt = () => BAUPROJEKTE.filter(z => z.ziel > bewohner).sort((a, b) => a.ziel - b.ziel)[0] || null;
function setzeBewohner(n, quelle) {
  if (!n || n < 1) return;
  const vorher = zielJetzt();
  bewohner = n; S.bewohner = n; geaendert = true;
  if (vorher && bewohner >= vorher.ziel) {
    sende({ typ: 'ziel', name: vorher.name });
    sag(satz('zielErreicht', { zahl: bewohner, projekt: vorher.name }), 0);
  }
  zustand();
}
function follow(u) {
  const p = spieler(u); if (!p) { setzeBewohner(bewohner + 1, 'follow'); inKasse(CFG.kasse.proFollow); return; }
  sende({ typ: 'follow', id: p.id });
  setzeBewohner(bewohner + 1, 'follow');
  inKasse(CFG.kasse.proFollow);
  if (!followDank.includes(p)) followDank.push(p);               // Dank kommt, sobald Anna frei ist
  gibMuscheln(p, CFG.muschelnFuerFollow, 'follow');
}

function teilen(u) {
  const p = spieler(u); if (!p) { inKasse(CFG.kasse.proShare); return; }
  inKasse(CFG.kasse.proShare);
  sende({ typ: 'teilen', id: p.id });
  sag(satz('teilen', { name: sprechName(p) }), 3);
  zustand();
}

// ---------- Gemeinschaftsprojekt (wird per Abstimmungs-Event gewählt) ----------
function projektStarten(pr) {
  S.projekt = { id: pr.id, name: pr.name, ziel: pr.ziel, stand: 0 }; geaendert = true;
  sende({ typ: 'projekt', id: pr.id }); zustand();
}
function projektFertig() {
  const pr = S.projekt; S.fertig.push(pr.id); S.projekt = null; geaendert = true;
  sende({ typ: 'fertig', id: pr.id });
  const def = CFG.abstimmung.projekte.find(x => x.id === pr.id) || {};
  sag(satz('projektFertig', { Projekt: grossKlein(def.der || pr.name) }), 0);
}

// ---------- Überraschungs-Events (events.mjs) ----------
const likeLog = [];
function belohne(p, n, extra) {
  if (!p) return;
  if (extra?.farbe) { p.farbe = extra.farbe; sende({ typ: 'farbe', id: p.id }); }
  if (extra?.anbau && !p.anbauten.includes(extra.anbau)) { p.anbauten.push(extra.anbau); sende({ typ: 'anbau', id: p.id, was: extra.anbau }); }
  p.eventMuscheln = (p.eventMuscheln || 0) + n;
  gibMuscheln(p, n, 'event');
}
const EV = macheEvents({
  CFG, test: TEST, sende, zustand: () => zustand(), sag: (t, pr) => sag(t, pr), belohne, name: p => sprechName(p), artikel: n => artikel(n),
  spieler: id => S.spieler[id],
  aktive: min => Object.values(S.spieler).filter(p => !p.gesperrt && Date.now() - (p.zuletzt || 0) < min * 60000),
  likeRate: () => { const t = Date.now() - 300000; while (likeLog.length && likeLog[0][0] < t) likeLog.shift(); return likeLog.reduce((a, [, n]) => a + n, 0) / 5; },
  rekord: v => { if (v != null) { S.likeRekord = v; geaendert = true; } return S.likeRekord || 150; },
  hatProjekt: () => !!S.projekt,
  // kein Limit: noch nicht gebaute zuerst (gemischt), danach schon gebaute (gemischt)
  offeneProjekte: () => { const m = a => a.sort(() => Math.random() - .5); return [...m(CFG.abstimmung.projekte.filter(x => !S.fertig.includes(x.id))), ...m(CFG.abstimmung.projekte.filter(x => S.fertig.includes(x.id)))]; },
  projektStarten,
});
setInterval(zustand, 1000);

// ---------- Stimme (macOS „say“, unbegrenzt, offline) ----------
// Prio 0: Geschenk-Dank, Event-Ansagen · 1: Follow-Dank, Countdown · 2: Haus-Ausbau · 3: Kleinkram · 4: Dauer-Moderation
// Untertitel erscheinen genau dann, wenn Anna den Satz spricht. „…“ im Text = Sprechpause.
const warte = []; let spricht = false; const gesprochen = [];
const TON_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'muscheltal-ton-')); let tonNr = 0;
let stimme = CFG.stimme.mac, stilleSeit = Date.now();
const ECHT = !STILL && process.platform === 'darwin';
const dauerMs = t => t.length * 62 + (t.match(/…/g) || []).length * 450 + 300;   // Schätzung ohne echte Stimme
const fuerStimme = t => t.replace(/\s*…\s*/g, ' [[slnc 450]] ').replace(/([!?])\s+/g, '$1 [[slnc 250]] ');
function sag(text, prio = 2) {
  if (!text) return;
  if (satzAnstoessig(text)) { console.log('🚫 Satz nicht gesprochen (Filter):', text); return; }
  const jetzt = Date.now();
  while (gesprochen.length && jetzt - gesprochen[0] > 60000) gesprochen.shift();
  if (prio >= 2 && prio <= 3 && gesprochen.length >= CFG.stimme.maxProMinute) return; // Kleinkram nicht stapeln
  warte.push({ text, prio, t: jetzt });
  warte.sort((a, b) => a.prio - b.prio || a.t - b.t);
  // Geschenk-Dank und Event-Ansagen (Prio 0/1) werden nie verworfen, nur Kleinkram
  while (warte.length > CFG.stimme.maxWarteschlange) { const i = warte.findLastIndex(w => w.prio >= 2); if (i < 0) break; warte.splice(i, 1); }
  // Veraltete Kleinigkeiten (älter als 20 s) fallen weg
  for (let i = warte.length - 1; i >= 0; i--) if (warte[i].prio >= 2 && jetzt - warte[i].t > 20000) warte.splice(i, 1);
  weiter();
}
function fertig() { spricht = false; stilleSeit = Date.now(); setTimeout(weiter, 50); }
function weiter() {
  if (spricht || !warte.length) return;
  const { text } = warte.shift(); spricht = true; gesprochen.push(Date.now());
  sende({ typ: 'ansage', text, ms: dauerMs(text) });
  if (!ECHT) { setTimeout(fertig, dauerMs(text)); return; }
  const aufSeite = CFG.stimme.wiedergabe !== 'mac' && seiteHatTon() && Date.now() > stimmeFehlerBis;
  const datei = path.join(TON_DIR, `s${++tonNr % 20}.wav`);
  const args = ['-v', stimme, '-r', String(CFG.stimme.tempo)];
  if (aufSeite) args.push('-o', datei, '--file-format=WAVE', '--data-format=LEI16@22050');
  const pr = spawn('say', [...args, fuerStimme(text)]);
  let fehler = '';
  pr.stderr.on('data', d => fehler += d);
  pr.on('close', code => {
    if (aufSeite && code === 0) {                      // Seite spielt ab; warten, bis die Ansage vorbei ist
      let ms = 2000; try { ms = (fs.statSync(datei).size - 44) / 44.1 + 300; } catch {}
      sende({ typ: 'stimme', id: tonSeite, url: '/ton/' + path.basename(datei) + '?' + Date.now() });
      setTimeout(fertig, ms);
      return;
    }
    if (code !== 0 && /voice|stimme/i.test(fehler)) {
      const ersatz = CFG.stimme.macErsatz.shift();
      if (ersatz) { console.log(`Stimme „${stimme}“ nicht gefunden, nehme „${ersatz}“.`); stimme = ersatz; warte.unshift({ text, prio: 0, t: Date.now() }); }
    }
    fertig();
  });
}

// ---------- Ton-Absicherung ----------
// Läuft auf keiner Live-Seite Ton (Browser blockiert ihn), spielen Stimme und Musik direkt über die Mac-Lautsprecher.
let lokalMusik = null, lokalNr = 0, tonSeite = null, stimmeFehlerBis = 0;
const tonStatus = new Map();                               // Seiten-Nr. -> { an, zeit, vorschau, seit }
const seiteHatTon = () => { const st = tonStatus.get(tonSeite); return !!st && st.an && Date.now() - st.zeit < 10000; };
// Genau EINE Seite spielt Ton: bevorzugt eine, auf der Ton schon läuft, sonst die zuerst geöffnete (keine Vorschau)
function waehleTonSeite() {
  const offen = [...kunden.keys()].filter(id => !tonStatus.get(id)?.vorschau);
  const mitTon = offen.filter(id => tonStatus.get(id)?.an);
  let neu = offen.includes(tonSeite) && (tonStatus.get(tonSeite)?.an || !mitTon.length) ? tonSeite : (mitTon[0] ?? offen[0] ?? null);
  if (neu !== tonSeite) { tonSeite = neu; sende({ typ: 'tonRolle', id: tonSeite }); }
}
const MUSIK_DATEIEN = ['suedsee_3.mp3', 'suedsee_9.mp3', 'suedsee_11.mp3'].map(f => path.join(DIR, 'seite', 'musik', f));
function musikLokal() {
  const brauche = process.platform === 'darwin' && CFG.ton.musikAufMac !== false && !seiteHatTon() && Date.now() - START > 15000;
  if (brauche && !lokalMusik) {
    const f = MUSIK_DATEIEN[lokalNr++ % MUSIK_DATEIEN.length];
    lokalMusik = spawn('afplay', ['-v', String(CFG.ton.musikAufMacLautstaerke ?? .18), f]);
    lokalMusik.on('close', () => { lokalMusik = null; });
    console.log('🎵 Kein Ton auf der Live-Seite – Musik und Stimme laufen über die Mac-Lautsprecher.');
  }
  if (!brauche && lokalMusik) { lokalMusik.kill(); lokalMusik = null; }
}
const START = Date.now();
setInterval(musikLokal, 3000);
process.on('exit', () => lokalMusik?.kill());

// ---------- Dauer-Moderation: Anna redet immer, mit kurzen Pausen dazwischen ----------
const followDank = [], begruessen = [], begruesst = new Set();
let letzterLive = 0, letzterRundgang = 0, modNr = 0, eventModNr = 0, countdownGesagt = '', eventZehnGesagt = '';
// Rangliste: beste Haus-Stufe zuerst, bei Gleichstand entscheiden die Muscheln aus Events
const rangFolge = (a, b) => b.stufe - a.stufe || (b.eventMuscheln || 0) - (a.eventMuscheln || 0) || b.muscheln - a.muscheln;
const zufallAus = fs => fs[Math.floor(Math.random() * fs.length)]();
const grossKlein = t => t.charAt(0).toUpperCase() + t.slice(1);
const MODERATION = [
  () => satz('tipp'),
  () => { const s = EV.naechstesIn(); return s > 45 ? satz('teaser', { zeit: s >= 100 ? `${Math.round(s / 60)} Minuten` : 'gut einer Minute' }) : null; },
  () => rundgang(),
  () => satz('fakt'),
  () => satz('geschenkInfo'),
  () => { const z = zielJetzt(); return z ? satz('ziel', { rest: z.ziel - bewohner, projekt: z.name, bewohner, zielzahl: z.ziel }) : null; },
  () => satz('frage'),
  () => { const t = Object.values(S.spieler).filter(p => !p.gesperrt).sort(rangFolge); return t.length > 1 ? satz('rangliste', { erster: sprechName(t[0]), zweiter: sprechName(t[1]) }) : null; },
  () => rundgang(),
  () => S.kasse > 0 ? satz('kasse', { kasse: S.kasse.toLocaleString('de-DE') }) : null,
  () => S.projekt ? satz('projekt', { projekt: S.projekt.name, prozent: Math.floor(S.projekt.stand / S.projekt.ziel * 100) }) : null,
  () => baustelleZeigen(),
  () => { const h = new Date().getHours(); return h >= 17 || h < 7 ? satz('abend') : satz('stimmung', { aktive: aktiveAnzahl() }); },
  () => satz('stimmung', { aktive: aktiveAnzahl() }),
];
const aktiveAnzahl = () => Object.values(S.spieler).filter(p => Date.now() - (p.zuletzt || 0) < 600000).length;
function baustelleZeigen() {                                // Kamera fliegt zur Baustelle, Anna berichtet
  if (!S.projekt || Date.now() - letzterRundgang < 30000) return null;
  letzterRundgang = Date.now(); sende({ typ: 'kameraBau', ms: 8000 });
  const def = CFG.abstimmung.projekte.find(x => x.id === S.projekt.id) || {};
  return satz('baustelleZeigen', { Projekt: grossKlein(def.der || S.projekt.name), ein: def.ein || S.projekt.name, prozent: Math.floor(S.projekt.stand / S.projekt.ziel * 100), rest: Math.max(0, Math.ceil(S.projekt.ziel - S.projekt.stand)).toLocaleString('de-DE') });
}
function rundgang() {                                      // Kamera fliegt zu einem Haus, Anna stellt es vor
  if (Date.now() - letzterRundgang < 40000) return null;
  const kand = Object.values(S.spieler).filter(p => !p.gesperrt && Date.now() - (p.zuletzt || 0) < 900000 && p.stufe > 0);
  if (!kand.length) return null;
  const p = kand[Math.floor(Math.random() * kand.length)], st = CFG.stufen[p.stufe].name;
  const an = p.anbauten.map(a => CFG.anbauten[a]?.name).filter(Boolean);
  letzterRundgang = Date.now(); sende({ typ: 'kamera', id: p.id, ms: 9000 });
  return satz('rundgang', { name: sprechName(p), stufeCap: grossKlein(artikel(st)), stufeDativ: dativ(st), anbauText: an.length ? ' mit ' + namenListe(an) : '' });
}
function moderiere() {
  if (spricht || warte.length || Date.now() - stilleSeit < (CFG.stimme.pauseSek ?? 1.6) * 1000) return;
  // 1. Follows bedanken
  if (followDank.length) {
    const n = followDank.splice(0, 4).map(sprechName), z = zielJetzt();
    return sag((n.length > 1 ? satz('followMehrere', { namen: namenListe(n) }) : satz('followEins', { name: n[0] })) + (z && Math.random() < .5 ? satz('followZiel', { rest: z.ziel - bewohner, projekt: z.name }) : ''), 1);
  }
  // 1b. Wer „haus“ geschrieben hat: Kamera fliegt zum Haus (ab und zu, nicht während Events)
  const kameraEvent = ['schatzsuche', 'meeresbesuch', 'flaschenpost', 'moewenalarm', 'hausbesuch'].includes(EV.id());
  if (!kameraEvent && hausWunsch.length && Date.now() - letztesHausZeigen > (EV.laeuft() ? 20000 : 12000)) {
    const p = S.spieler[hausWunsch.shift()];
    if (p && !p.gesperrt) {
      letztesHausZeigen = letzterRundgang = Date.now(); hausGezeigt[p.id] = Date.now();
      sende({ typ: 'kamera', id: p.id, ms: 9000 }); sende({ typ: 'hausGezeigt', id: p.id });
      const st = CFG.stufen[p.stufe].name, an = p.anbauten.map(a => CFG.anbauten[a]?.name).filter(Boolean);
      return sag(satz('hausZeigen', { name: sprechName(p), stufeCap: grossKlein(artikel(st)), anbauText: an.length ? ' mit ' + namenListe(an) : '' }), 1);
    }
  }
  // 2. Laufendes Event: abwechselnd Spielstand, Anfeuern und ab und zu ein normaler Satz
  if (EV.laeuft()) {
    const art = eventModNr++ % 4;
    if (art !== 3 && Date.now() - letzterLive > 6000) { const t = EV.liveSatz(); if (t) { letzterLive = Date.now(); return sag(t, 4); } }
    if (art === 3) return sag(zufallAus([() => satz('tipp'), () => satz('stimmung', { aktive: aktiveAnzahl() })]), 4);
    return sag(satz('eventAllgemein', { rest: EV.restSek() }), 4);   // nie Stille während Events
  }
  // 3. Neue Zuschauer begrüßen (nur wenn kein Event moderiert werden muss)
  if (!EV.laeuft() && begruessen.length) {                  // immer einzeln und kurz
    const b = begruessen.shift();
    if (b.zurueck) return sag(b.besuche >= 3 && Math.random() < .5 ? satz('begruessungTreu', { name: b.name, besuche: b.besuche }) : satz('begruessungZurueck', { name: b.name }), 4);
    return sag(satz('begruessungEins', { name: b.name }), 4);
  }
  if (EV.laeuft()) return;
  // 4. Abwechselnde Moderation
  for (let k = 0; k < MODERATION.length; k++) { const t = MODERATION[modNr++ % MODERATION.length](); if (t) return sag(t, 4); }
  sag(satz('stimmung', { aktive: aktiveAnzahl() }), 4);
}
// Rangliste beobachten: Änderungen in den Top 3 ansagen (höchstens alle 15 s, wichtigste Änderung zuerst)
let topVorher = null, topAnsage = 0;
setInterval(() => {
  const top = Object.values(S.spieler).filter(p => !p.gesperrt).sort(rangFolge).slice(0, 3).map(p => p.id);
  if (!topVorher) { topVorher = top; return; }
  if (Date.now() - topAnsage < 15000) return;
  for (let i = 0; i < top.length; i++) {
    if (top[i] === topVorher[i]) continue;
    const p = S.spieler[top[i]], neuDrin = !topVorher.includes(top[i]);
    if (i > 0 && !neuDrin) continue;                        // nur Platz 1 oder Neueinsteiger ansagen
    topAnsage = Date.now();
    sende({ typ: 'rangliste', id: p.id, platz: i + 1 });
    sag(i === 0 ? satz('topEins', { name: sprechName(p) }) : satz('topNeu', { name: sprechName(p), platz: i === 1 ? 'zwei' : 'drei' }), 1);
    break;
  }
  topVorher = top;
}, 3000);

// Alle 3 Minuten: Aufruf zum Folgen (mit Banner)
setInterval(() => { sende({ typ: 'folgeAufruf' }); sag(satz('folgeAufruf'), 1); }, (CFG.folgeAufrufMinuten || 3) * 60000);
setInterval(() => {
  // Countdown-Ansagen (verraten nie, welches Event kommt)
  const s = EV.naechstesIn(), runde = String(Math.floor(Date.now() / 120000));
  if (s <= 31 && s >= 29 && countdownGesagt !== runde + 30) { countdownGesagt = runde + 30; sag(satz('countdown30'), 1); }
  if (s <= 11 && s >= 9 && countdownGesagt !== runde + 10) { countdownGesagt = runde + 10; sag(satz('countdown10'), 1); }
  const r = EV.restSek();
  if (r != null && r <= 11 && r >= 9 && eventZehnGesagt !== runde) { eventZehnGesagt = runde; sag(satz('eventNoch10'), 1); }
  moderiere();
}, 400);
function beitritt(u) {                                     // jemand kommt neu in den Stream
  const id = String(u.uniqueId || '').toLowerCase();
  if (!id || begruesst.has(id) || gesperrt(id) || anstoessig(u.uniqueId) || anstoessig(u.nickname)) return;
  begruesst.add(id);
  const p = S.spieler[id];
  if (p && !p.gesperrt) {                                  // kennt die Insel schon: „Willkommen zurück“
    p.besuche = (p.besuche || 1) + 1; geaendert = true;
    begruessen.push({ name: sprechName(p), zurueck: true, besuche: p.besuche, stufe: CFG.stufen[p.stufe].name });
  } else begruessen.push({ name: sprechName({ name: '@' + u.uniqueId }), zurueck: false });
  if (begruessen.length > 6) begruessen.splice(0, begruessen.length - 6);   // bei vielen Neuen: nur die neuesten
}

// ---------- Seite + Live-Daten (Server-Sent Events) ----------
const kunden = new Map(); let letzteSeitenAnsage = '', seitenNr = 0;
function sende(ev) { const s = `data: ${JSON.stringify(ev)}\n\n`; for (const k of kunden.values()) k.write(s); }
let zLetzt = 0, zOffen = false;
function zustand() {
  if (Date.now() - zLetzt < 250) { if (!zOffen) { zOffen = true; setTimeout(() => { zOffen = false; zustand(); }, 260); } return; }
  zLetzt = Date.now();
  sende({ typ: 'zustand', s: oeffentlich() });
}
function oeffentlich() {
  return {
    ...EV.oeffentlich(),
    spieler: S.reihenfolge.map(id => S.spieler[id]).filter(p => p && !p.gesperrt),
    stufen: CFG.stufen.map(s => s.name), stufenAb: CFG.stufen.map(s => s.ab),
    projekt: S.projekt, fertig: S.fertig, kasse: S.kasse,
    bewohner, ziel: zielJetzt(), strassen: CFG.strassen,
    tiktokName: CFG.tiktokName, test: TEST, ton: CFG.ton, ort: CFG.ort,
  };
}

const TYPEN = { '.mp3': 'audio/mpeg', '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };
http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/sag') {
    const t = String(url.searchParams.get('t') || '').slice(0, 200);
    if (t && t !== letzteSeitenAnsage) { letzteSeitenAnsage = t; sag(t, 0); setTimeout(() => letzteSeitenAnsage = '', 15000); }
    res.writeHead(204); return res.end();
  }
  if (TEST && url.pathname === '/test') {                 // nur Test-Modus: Event / Geschenk-Show auslösen
    const id = url.searchParams.get('event'), art = url.searchParams.get('geschenk');
    if (url.searchParams.has('stadt')) { const n = +url.searchParams.get('stadt'), ids = CFG.abstimmung.projekte.map(x => x.id); S.fertig = Array.from({ length: n }, (_, i) => ids[i % ids.length]); const pr = CFG.abstimmung.projekte[n % ids.length]; S.projekt = pr ? { id: pr.id, name: pr.name, ziel: pr.ziel, stand: Math.round(pr.ziel * .45) } : null; zustand(); }
    if (url.searchParams.has('fertigbauen') && S.projekt) { S.projekt.stand = S.projekt.ziel - 1; inKasse(1); }
    if (id) EV.starte(id);
    const nutzer = url.searchParams.get('user');               // gezielt als Test-Zuschauer handeln
    if (nutzer) {
      const u = { uniqueId: nutzer }, q = url.searchParams;
      if (q.has('kommentar')) kommentar(u, q.get('kommentar'));
      if (q.has('like')) like(u, +q.get('like'));
      if (q.has('follow')) follow(u);
      if (q.has('teilen')) teilen(u);
      if (q.has('gift')) geschenk(u, q.get('gift'), +q.get('coins') || 1, +q.get('anzahl') || 1);
      if (q.has('beitritt')) beitritt(u);
    }
    if (url.searchParams.has('ende')) EV.beendeJetzt();
    if (url.searchParams.has('zustand')) { res.writeHead(200, { 'Content-Type': 'application/json' }); return res.end(JSON.stringify({ ...oeffentlich(), bewohner, hausWunsch, begruessen, followDank: followDank.map(p => p.id) })); }
    if (art) { const p = Object.values(S.spieler)[3]; geschenk({ uniqueId: p.name.slice(1) }, url.searchParams.get('name') || 'Rose', +url.searchParams.get('coins') || 1, 1); }
    res.writeHead(204); return res.end();
  }
  if (url.pathname === '/tonstatus') {                       // Live-Seite meldet, ob ihr Ton läuft
    const id = +url.searchParams.get('id'), alt = tonStatus.get(id) || {};
    if (url.searchParams.has('an')) tonStatus.set(id, { ...alt, an: url.searchParams.get('an') === '1', vorschau: url.searchParams.get('vorschau') === '1', zeit: Date.now() });
    if (url.searchParams.get('stimme') === '0') { stimmeFehlerBis = Date.now() + 60000; console.log('🔈 Stimme auf der Seite blockiert – spreche über die Mac-Lautsprecher.'); }
    if (url.searchParams.get('stimme') === '1') stimmeFehlerBis = 0;
    waehleTonSeite();
    res.writeHead(204); return res.end();
  }
  if (url.pathname === '/events') {
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
    res.write(`data: ${JSON.stringify({ typ: 'zustand', s: oeffentlich() })}\n\n`);
    const id = ++seitenNr; kunden.set(id, res);
    res.write(`data: ${JSON.stringify({ typ: 'hallo', id })}\n\n`);
    res.write(`data: ${JSON.stringify({ typ: 'tonRolle', id: tonSeite })}\n\n`);
    waehleTonSeite();
    req.on('close', () => { kunden.delete(id); tonStatus.delete(id); waehleTonSeite(); });
    return;
  }
  if (url.pathname.startsWith('/ton/')) {
    const f = path.join(TON_DIR, path.basename(url.pathname));
    return fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': 'audio/wav' }); res.end(d); });
  }
  const datei = path.join(DIR, 'seite', path.normalize(url.pathname === '/' ? '/index.html' : url.pathname).replace(/^(\.\.[/\\])+/, ''));
  if (!datei.startsWith(path.join(DIR, 'seite'))) { res.writeHead(403); return res.end(); }
  fs.readFile(datei, (e, d) => {
    if (e) { res.writeHead(404); return res.end('nicht gefunden'); }
    res.writeHead(200, { 'Content-Type': TYPEN[path.extname(datei)] || 'application/octet-stream' }); res.end(d);
  });
}).listen(CFG.port, () => {
  console.log(`\n🐚 Muschel-Tal LIVE läuft:  http://localhost:${CFG.port}`);
  console.log('   Diese Adresse in TikTok LIVE Studio als Link-/Browser-Quelle (1080×1920) einfügen.\n');
});

// ---------- TikTok-Verbindung ----------
async function verbinde() {
  const { TikTokLiveConnection, WebcastEvent } = await import('tiktok-live-connector');
  const c = new TikTokLiveConnection(CFG.tiktokName, { enableExtendedGiftInfo: true, processInitialData: false });
  c.on(WebcastEvent.CHAT, d => d.user && kommentar(d.user, d.comment));
  c.on(WebcastEvent.LIKE, d => d.user && like(d.user, d.likeCount || 1));
  c.on(WebcastEvent.FOLLOW, d => d.user && follow(d.user));
  c.on(WebcastEvent.SHARE, d => d.user && teilen(d.user));
  c.on(WebcastEvent.MEMBER, d => d.user && beitritt(d.user));
  c.on(WebcastEvent.GIFT, d => {
    const g = d.giftDetails || {};
    if (g.giftType === 1 && !d.repeatEnd) return; // Serie läuft noch – erst am Ende zählen
    const ex = d.extendedGiftInfo || {};
    geschenk(d.user || {}, g.giftName || ex.name || 'das Geschenk', g.diamondCount || ex.diamond_count || 1, d.repeatCount || 1);
  });
  c.on(WebcastEvent.STREAM_END, () => { console.log('Stream beendet.'); speichern(); });
  c.on('disconnected', () => { console.log('Verbindung weg – neuer Versuch in 15 s'); setTimeout(versuche, 15000); });
  const st = await c.connect();
  console.log(`✅ Mit dem LIVE von @${CFG.tiktokName} verbunden (Raum ${st.roomId}).`);
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
    console.log(`⏳ Noch nicht live oder keine Verbindung (${e.message || e}). Neuer Versuch in 20 s …`);
    setTimeout(versuche, 20000);
  }
}

// ---------- Simulator ----------
function simulator() {
  const namen = ['lena.sun', 'muschel_max', 'koko.nuss22', 'sandy_beach', 'tim.wave', 'perle.88', 'jonas_insel', 'mia.meer', 'surfer.ben', 'krabbe.kalle',
    'lotta.fsthff', 'paulepfpgfn', 'vidafilipa', 'nina_palme', 'ole.anker', 'emma.sonne', 'leo.leuchtturm', 'hanna.hai', 'finn.flut', 'ella.ebbe'];
  const worte = ['haus', 'Haus!', 'hauus', 'mein haus', 'house', 'pool', 'garten', 'boot', 'palme', 'rot', 'blau', 'lila', 'gelb', 'laterne', 'flagge', 'hallo!', 'wie geht das?', 'türkis'];
  const gifts = [['Rose', 1], ['Rose', 1], ['TikTok', 1], ['Finger Heart', 5], ['Donut', 30], ['Perfume', 20], ['Galaxy', 1000]];
  // Volle Insel zum Ansehen: viele Bewohner mit allen Haus-Stufen
  const silben = ['sun', 'meer', 'koko', 'palm', 'surf', 'wave', 'sand', 'perl', 'hai', 'lagu', 'mango', 'ebbe', 'flut', 'riff', 'kiki', 'lia', 'max', 'ben'];
  for (let i = 0; i < 230; i++) namen.push(silben[i % 18] + (i % 3 ? '.' : '_') + silben[(i * 7) % 18] + (10 + i));
  namen.slice(0, 195).forEach((nm, i) => {
    const p = spieler({ uniqueId: nm }); if (!p) return; const st = CFG.stufen[(i * 7) % CFG.stufen.length];
    p.muscheln = st.ab + 5; p.stufe = stufeVon(p.muscheln);
    p.anbauten = Object.keys(CFG.anbauten).filter((k, j) => (i + j) % 4 === 0 && CFG.anbauten[k].abStufe <= p.stufe);
  });
  warte.length = 0;
  let n = namen.length;
  console.log('🧪 Test-Modus: simulierte Zuschauer.');
  setInterval(() => {
    
    if (Math.random() < .04) { namen.push('gast.' + Math.random().toString(36).slice(2, 7)); n = namen.length; }
    const u = { uniqueId: namen[Math.floor(Math.random() * n)] };
    const r = Math.random();
    const evAntwort = ['1', '2', '3', 'rot', 'blau', 'gelb', 'grün', 'muschel', 'kokos', 'flasche', 'hallo', 'a', 'b', 'c', 'd', String(1 + Math.floor(Math.random() * 100)), 'fang', 'wunsch'];
    if (EV.laeuft() && r < .3) kommentar(u, evAntwort[Math.floor(Math.random() * evAntwort.length)]);
    else if (r < .7) like(u, 1 + Math.floor(Math.random() * 15));
    else if (r < .9) kommentar(u, worte[Math.floor(Math.random() * worte.length)]);
    else if (r < .97) { if (RUHIG && Math.random() < .9) return; const g = gifts[Math.floor(Math.random() * (Math.random() < .9 ? 4 : gifts.length))]; geschenk(u, g[0], g[1], 1 + Math.floor(Math.random() * 3)); }
    else if (Math.random() < .5) teilen(u); else follow(u);
    if (Math.random() < .15) beitritt(Math.random() < .5 ? { uniqueId: 'zuschauer.' + Math.random().toString(36).slice(2, 6) } : { uniqueId: namen[Math.floor(Math.random() * n)] });
  }, RUHIG ? 2500 : 700);
}

if (TEST && !process.argv.includes('--leer')) simulator(); else if (!TEST) versuche();
process.on('SIGINT', () => { geaendert = true; speichern(); process.exit(0); });
