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
import { anstoessig, satzAnstoessig, ladeSperrliste, gesperrt } from './filter.mjs';

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
namenPruefen(); setInterval(namenPruefen, 30000);

const stufeVon = m => { let i = 0; CFG.stufen.forEach((s, k) => { if (m >= s.ab) i = k; }); return i; };

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

const dativ = n => (/^(Strohhütte|Stelzenhütte|Villa|Luxusvilla)$/.test(n) ? 'einer ' : 'einem ') + n;
const artikel = n => (/^(Strohhütte|Stelzenhütte|Villa|Luxusvilla)$/.test(n) ? 'eine ' : /^(Bungalow|Strandpalast)$/.test(n) ? 'einen ' : 'ein ') + n;
// Namen für die Stimme lesbar machen: "lena_xx.22" -> "lena xx"
const sprechName = p => p.name.replace(/^@/, '').replace(/[._]+/g, ' ').replace(/\d{3,}/g, '').trim() || 'Neuer Bewohner';

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
  sende({ typ: 'geschenk', id: p.id, name, anzahl, diamanten: d });
  EV.geschenkShow(p, name, anzahl, d);
  inKasse(d * CFG.kasse.proCoin);
  const wie = anzahl > 1 ? `${anzahl} mal ${name}` : name;
  sag(satz(d >= 1000 ? 'geschenkGross' : d >= 100 ? 'geschenkMittel' : 'geschenkKlein', { name: sprechName(p), geschenk: wie }), 0);
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

// ---------- Bauprojekte der Homepage (muscheltal/daten/insel.json) ----------
const INSEL_JSON = path.join(DIR, '..', 'muscheltal', 'daten', 'insel.json');
const EINW_CSV = path.join(DIR, '..', 'muscheltal', 'daten', 'einwohner.csv');
let BAUPROJEKTE = CFG.bewohner.ziele;
function ladeHomepage() {
  try {
    const d = JSON.parse(fs.readFileSync(INSEL_JSON, 'utf8'));
    if (Array.isArray(d.baustellen) && d.baustellen.length)
      BAUPROJEKTE = d.baustellen.map(b => ({ name: b.name, icon: b.emoji || '🏗️', ziel: b.ziel, ort: 'Haupt-Insel' }));
  } catch {}
}
ladeHomepage(); setInterval(ladeHomepage, 600000);
function startBewohner() {
  try { return fs.readFileSync(EINW_CSV, 'utf8').trim().split('\n').length - 1; } catch { return CFG.bewohner.start; }
}

// ---------- Bewohner (= Follower) ----------
let bewohner = Math.max(S.bewohner || 0, startBewohner());
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
  if (!followDank.includes(p)) followDank.push(p);               // Dank kommt, sobald Markus frei ist
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
  sag(satz('projektFertig', { projekt: pr.name }), 0);
}

// ---------- Überraschungs-Events (events.mjs) ----------
const likeLog = [];
function belohne(p, n, extra) {
  if (!p) return;
  if (extra?.farbe) { p.farbe = extra.farbe; sende({ typ: 'farbe', id: p.id }); }
  if (extra?.anbau && !p.anbauten.includes(extra.anbau)) { p.anbauten.push(extra.anbau); sende({ typ: 'anbau', id: p.id, was: extra.anbau }); }
  gibMuscheln(p, n, 'event');
}
const EV = macheEvents({
  CFG, test: TEST, sende, zustand: () => zustand(), sag: (t, pr) => sag(t, pr), belohne, name: p => sprechName(p), artikel: n => artikel(n),
  spieler: id => S.spieler[id],
  aktive: min => Object.values(S.spieler).filter(p => !p.gesperrt && Date.now() - (p.zuletzt || 0) < min * 60000),
  likeRate: () => { const t = Date.now() - 300000; while (likeLog.length && likeLog[0][0] < t) likeLog.shift(); return likeLog.reduce((a, [, n]) => a + n, 0) / 5; },
  hatProjekt: () => !!S.projekt,
  offeneProjekte: () => CFG.abstimmung.projekte.filter(x => !S.fertig.includes(x.id)),
  projektStarten,
});
setInterval(zustand, 1000);

// ---------- Stimme (macOS „say“, unbegrenzt, offline) ----------
// Prio 0: Geschenk-Dank, Event-Ansagen · 1: Follow-Dank, Countdown · 2: Haus-Ausbau · 3: Kleinkram · 4: Dauer-Moderation
// Untertitel erscheinen genau dann, wenn Markus den Satz spricht. „…“ im Text = Sprechpause.
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
  const aufSeite = CFG.stimme.wiedergabe !== 'mac' && kunden.size > 0;
  const datei = path.join(TON_DIR, `s${++tonNr % 20}.wav`);
  const args = ['-v', stimme, '-r', String(CFG.stimme.tempo)];
  if (aufSeite) args.push('-o', datei, '--file-format=WAVE', '--data-format=LEI16@22050');
  const pr = spawn('say', [...args, fuerStimme(text)]);
  let fehler = '';
  pr.stderr.on('data', d => fehler += d);
  pr.on('close', code => {
    if (aufSeite && code === 0) {                      // Seite spielt ab; warten, bis die Ansage vorbei ist
      let ms = 2000; try { ms = (fs.statSync(datei).size - 44) / 44.1 + 300; } catch {}
      sende({ typ: 'stimme', url: '/ton/' + path.basename(datei) + '?' + Date.now() });
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

// ---------- Dauer-Moderation: Markus redet immer, mit kurzen Pausen dazwischen ----------
const followDank = [], begruessen = [], begruesst = new Set();
let letzterLive = 0, letzterRundgang = 0, modNr = 0, eventModNr = 0, countdownGesagt = '', eventZehnGesagt = '';
const zufallAus = fs => fs[Math.floor(Math.random() * fs.length)]();
const grossKlein = t => t.charAt(0).toUpperCase() + t.slice(1);
const MODERATION = [
  () => satz('tipp'),
  () => { const s = EV.naechstesIn(); return s > 45 ? satz('teaser', { zeit: s >= 100 ? `${Math.round(s / 60)} Minuten` : 'gut einer Minute' }) : null; },
  () => rundgang(),
  () => satz('fakt'),
  () => { const z = zielJetzt(); return z ? satz('ziel', { rest: z.ziel - bewohner, projekt: z.name, bewohner, zielzahl: z.ziel }) : null; },
  () => satz('frage'),
  () => { const t = Object.values(S.spieler).sort((a, b) => b.muscheln - a.muscheln); return t.length > 1 ? satz('rangliste', { erster: sprechName(t[0]), zweiter: sprechName(t[1]) }) : null; },
  () => rundgang(),
  () => S.kasse > 0 ? satz('kasse', { kasse: S.kasse.toLocaleString('de-DE') }) : null,
  () => S.projekt ? satz('projekt', { projekt: S.projekt.name, prozent: Math.floor(S.projekt.stand / S.projekt.ziel * 100) }) : null,
  () => { const h = new Date().getHours(); return h >= 17 || h < 7 ? satz('abend') : satz('stimmung', { aktive: aktiveAnzahl() }); },
  () => satz('stimmung', { aktive: aktiveAnzahl() }),
];
const aktiveAnzahl = () => Object.values(S.spieler).filter(p => Date.now() - (p.zuletzt || 0) < 600000).length;
function rundgang() {                                      // Kamera fliegt zu einem Haus, Markus stellt es vor
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
  // 2. Laufendes Event: abwechselnd Spielstand, Anfeuern und ab und zu ein normaler Satz
  if (EV.laeuft()) {
    const art = eventModNr++ % 4;
    if (art !== 3 && Date.now() - letzterLive > 6000) { const t = EV.liveSatz(); if (t) { letzterLive = Date.now(); return sag(t, 4); } }
    if (art === 1) return sag(satz('eventAllgemein', { rest: EV.restSek() }), 4);
    if (art === 3) return sag(zufallAus([() => satz('tipp'), () => satz('stimmung', { aktive: aktiveAnzahl() })]), 4);
    return;
  }
  // 3. Neue Zuschauer begrüßen (nur wenn kein Event moderiert werden muss)
  if (!EV.laeuft() && begruessen.length) {
    const n = begruessen.splice(0, 3);
    return sag(n.length > 1 ? satz('begruessungMehrere', { namen: namenListe(n) }) : satz('begruessungEins', { name: n[0] }), 4);
  }
  if (EV.laeuft()) return;
  // 4. Abwechselnde Moderation
  for (let k = 0; k < MODERATION.length; k++) { const t = MODERATION[modNr++ % MODERATION.length](); if (t) return sag(t, 4); }
}
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
  begruesst.add(id); begruessen.push(sprechName({ name: '@' + u.uniqueId }));
  if (begruessen.length > 12) begruessen.splice(0, begruessen.length - 12);   // nur die neuesten
}

// ---------- Seite + Live-Daten (Server-Sent Events) ----------
const kunden = new Set(); let letzteSeitenAnsage = '';
function sende(ev) { const s = `data: ${JSON.stringify(ev)}\n\n`; for (const k of kunden) k.write(s); }
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
    if (id) EV.starte(id);
    if (art) { const p = Object.values(S.spieler)[3]; geschenk({ uniqueId: p.name.slice(1) }, url.searchParams.get('name') || 'Rose', +url.searchParams.get('coins') || 1, 1); }
    res.writeHead(204); return res.end();
  }
  if (url.pathname === '/events') {
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
    res.write(`data: ${JSON.stringify({ typ: 'zustand', s: oeffentlich() })}\n\n`);
    kunden.add(res); req.on('close', () => kunden.delete(res));
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
  const fol = info => { const f = suche(info, 'follower_count'); if (f) setzeBewohner(Number(f), 'tiktok'); };
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
  const worte = ['pool', 'garten', 'boot', 'palme', 'rot', 'blau', 'lila', 'gelb', 'laterne', 'flagge', 'hallo!', 'wie geht das?', 'türkis'];
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
    if (Math.random() < .15) beitritt({ uniqueId: 'zuschauer.' + Math.random().toString(36).slice(2, 6) });
  }, RUHIG ? 2500 : 700);
}

if (TEST) simulator(); else versuche();
process.on('SIGINT', () => { geaendert = true; speichern(); process.exit(0); });
