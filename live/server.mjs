// Muschel-Tal LIVE – verbindet TikTok LIVE (Likes, Kommentare, Geschenke) mit der Live-Insel.
// Start:  node server.mjs          (echter Stream, TikTok-Name aus einstellungen.json)
//         node server.mjs --test   (Simulator mit Test-Zuschauern, ohne TikTok)
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
import { satz, namenListe, festeSaetze } from './saetze.mjs';
import { geschenkFormen } from './geschenke.mjs';
import { anstoessig, satzAnstoessig, ladeSperrliste, gesperrt, normal } from './filter.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const CFG = JSON.parse(fs.readFileSync(path.join(DIR, 'einstellungen.json'), 'utf8'));
const STAND = path.join(DIR, 'stand.json');
const VERSION = '2026-11-14 l';                          // bei jeder Änderung hochzählen – steht beim Start im Terminal
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
S.jobs ||= {};                                             // Gebäude-Nr. (Index in S.fertig) -> { id: Spieler, seit }
if (S.projekt && !CFG.abstimmung.projekte.some(x => x.id === S.projekt.id)) S.projekt = null;
if (S.projekt) S.projekt.ziel = CFG.abstimmung.projekte.find(x => x.id === S.projekt.id).ziel;   // Kosten aus den Einstellungen
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
    sende({ typ: 'neu', id, name: p.name });
    sag(satz('neu', { name: sprechName(p) }), 1);   // erstes Zelt wird immer angesagt
    // Erstes Like/Kommentar: Zelt steht sofort, Kamera zeigt es kurz (startMuscheln optional, Standard 0)
    const start = CFG.startMuscheln ?? 0;
    if (start > 0) setImmediate(() => gibMuscheln(p, start, 'start'));
    if (!hausWunsch.includes(id)) hausWunsch.unshift(id);
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
    if (grund !== 'start') sag(satz('stufe', { name: sprechName(p), stufe: artikel(CFG.stufen[p.stufe].name), stufeDativ: dativ(CFG.stufen[p.stufe].name), stufeName: CFG.stufen[p.stufe].name }), 2);
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
const hausWunsch = [], hausGezeigt = {}, likeSerie = {}, likeDank = [];
let letztesHausZeigen = 0;

// ---------- Ereignisse ----------
function like(u, anzahl) {
  const p = spieler(u); if (!p) { S.likesGesamt += anzahl; inKasse(anzahl * CFG.kasse.proLike); return; }
  S.likesGesamt += anzahl; likeLog.push([Date.now(), anzahl]);
  inKasse(anzahl * CFG.kasse.proLike);
  const ls = likeSerie[p.id] ||= { n: 0, t0: Date.now(), dank: 0 };
  if (Date.now() - ls.t0 > 60000) { ls.n = 0; ls.t0 = Date.now(); }
  ls.n += anzahl;
  if (ls.n >= (CFG.likeDankAb ?? 50) && Date.now() - ls.dank > 180000 && !likeDank.includes(p)) { ls.dank = Date.now(); likeDank.push(p); }
  const faktor = EV.like(p, anzahl);                       // Muschelregen ×2, Bau-Turbo ×3
  gibMuscheln(p, anzahl * CFG.muschelnProLike * faktor, 'like');
}

// Wer noch kein Haus hat und „haus“ oder eine Farbe schreibt, bekommt den Hinweis: erst liken (höchstens 1× pro Minute)
const likeHinweis = {};
function erstLiken(u, art) {
  const id = String(u.uniqueId || '').toLowerCase();
  if (Date.now() - (likeHinweis[id] || 0) < 60000 || anstoessig(u.uniqueId) || anstoessig(u.nickname)) return;
  likeHinweis[id] = Date.now();
  const name = sprechName({ name: '@' + u.uniqueId });
  sende({ typ: 'erstLiken', name: '@' + u.uniqueId, art });
  sag(art === 'farbe' ? `${name}, like einmal! Dann bekommst du ein Haus zum Streichen.` : `${name}, du hast noch kein Haus. Like einmal, dann wird es gebaut!`, 1);
}
function farbeAus(p, t) {                                 // „blau“ → Haus wird animiert blau gestrichen
  const wort = t.split(/[^a-zäöüß]+/).find(w => CFG.farben[w]); if (!wort) return;
  const f = CFG.farben[wort]; if (p.farbe === f) return;
  const anzeige = { gruen: 'grün', tuerkis: 'türkis', weiss: 'weiß' }[wort] || wort;
  sende({ typ: 'farbe', id: p.id, name: p.name, alt: p.farbe, neu: f, wort: anzeige });
  p.farbe = f; geaendert = true;
  sag(`${sprechName(p)} streicht das Haus ${anzeige}!`, 2);
}
function kommentar(u, text) {
  const id0 = String(u.uniqueId || '').toLowerCase(), t = String(text || '').toLowerCase().trim();
  if (!id0 || gesperrt(id0)) return;
  // Kein Haus: nur bei Event-Antworten wird eins gebaut (Mitmachen zählt). „haus“ und Farben → Hinweis „erst liken“
  if (!S.spieler[id0] && !EV.laeuft()) {
    if (istHausWunsch(t)) return erstLiken(u, 'haus');
    if (t.split(/[^a-zäöüß]+/).some(w => CFG.farben[w])) return erstLiken(u, 'farbe');
    return;
  }
  const p = spieler(u); if (!p) return;
  farbeAus(p, t);                                          // Farbe gilt immer – auch wenn das Wort gleichzeitig eine Event-Antwort ist
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
  sag(satz(d >= 1000 ? 'geschenkMega' : d >= 200 ? 'geschenkGross' : d >= 20 ? 'geschenkMittel' : 'geschenkKlein', { name: sprechName(p), fuer: g.fuer, einAkk: g.einAkk, einNom: g.einNom, EinNom: grossKlein(g.einNom) }), 0);
  gibMuscheln(p, d * CFG.muschelnProCoin, 'geschenk');
}

// ---------- Muschelkasse der Live-Insel (getrennt von der Inselkasse der Haupt-Insel) ----------
if (S.kasse == null) S.kasse = S.likesGesamt || 0;
function inKasse(n) {
  S.kasse += n; geaendert = true;
  finanziere(n * (CFG.kasse.bauAnteil ?? .7));
}
// Gebäude werden aus der Muschelkasse bezahlt: läuft ein Bau, fließen die Muscheln aus der Kasse in die Baustelle
// Damit die Kasse nie leer ist: beim Baustart fließt die Hälfte des Ersparten, danach 70 % jeder neuen Muschel (einstellbar).
function finanziere(anteil) {
  if (!S.projekt || S.kasse <= 0) return 0;
  const roh = anteil * 1 + (S.bauBruch || 0), ganz = Math.floor(roh); S.bauBruch = roh - ganz;
  const t = Math.min(ganz, S.kasse - 1, S.projekt.ziel - S.projekt.stand);   // mindestens 1 Muschel bleibt immer
  if (t <= 0) return 0;
  S.kasse -= t; S.projekt.stand += t; geaendert = true;
  if (S.projekt.stand >= S.projekt.ziel) projektFertig();
  return t;
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
  sag(satz('teilen', { name: sprechName(p) }), 1);
  zustand();
}

// ---------- Gemeinschaftsprojekt (wird per Abstimmungs-Event gewählt) ----------
function projektStarten(pr) {
  S.projekt = { id: pr.id, name: pr.name, ziel: pr.ziel, stand: 0 }; geaendert = true;
  sende({ typ: 'projekt', id: pr.id });
  const aus = finanziere(S.kasse * (CFG.kasse.startAnteil ?? .5));   // die Hälfte des Ersparten fließt sofort in den Bau
  if (aus > 0 && S.projekt) sag(`${aus.toLocaleString('de-DE')} Muscheln aus der Kasse gehen in den Bau!`, 1);
  zustand();
}
function projektFertig() {
  const pr = S.projekt; S.fertig.push(pr.id); S.projekt = null; geaendert = true;
  sende({ typ: 'fertig', id: pr.id });
  const def = CFG.abstimmung.projekte.find(x => x.id === pr.id) || {};
  sag(satz('projektFertig', { Projekt: grossKlein(def.der || pr.name) }), 0);
  const nr = S.fertig.length - 1; setTimeout(() => jobVerlosen(nr), 8000);   // nach der Bau-Animation: Job verlosen
}

// ---------- Jobs: Jedes fertige Gebäude bekommt einen Job, verlost unter den Zuschauern (Gehalt: Muscheln) ----------
const imGebaeude = def => (def.der || '').startsWith('die ') ? 'in der ' + def.name : 'im ' + def.name;
function jobVerlosen(nr) {
  const gid = S.fertig[nr]; if (!gid || S.jobs[nr]) return false;
  const vergeben = new Set(Object.values(S.jobs).map(j => j.id));
  const kand = Object.values(S.spieler).filter(p => !p.gesperrt && !vergeben.has(p.id) && Date.now() - (p.zuletzt || 0) < 15 * 60000);
  if (!kand.length) return false;                          // gerade niemand da – wird später nachgeholt
  const p = kand[Math.floor(Math.random() * kand.length)], def = CFG.abstimmung.projekte.find(x => x.id === gid) || { name: gid };
  S.jobs[nr] = { id: p.id, seit: Date.now() }; geaendert = true;
  const geh = CFG.jobs?.gehalt ?? 5;
  sende({ typ: 'job', nr, id: p.id, name: p.name, wo: imGebaeude(def), gehalt: geh });
  sag(`${sprechName(p)} gewinnt den Job ${imGebaeude(def)}! … ${geh === 1 ? 'Eine Muschel' : geh + ' Muscheln'} Gehalt!`, 1);
  zustand(); return true;
}
setInterval(() => { for (let i = 0; i < S.fertig.length; i++) if (!S.jobs[i] && jobVerlosen(i)) break; }, 60000);   // offene Jobs nachholen
setInterval(() => {                                        // Zahltag: Gehalt für alle mit Job
  const geh = CFG.jobs?.gehalt ?? 5; let n = 0;
  for (const j of Object.values(S.jobs)) { const p = S.spieler[j.id]; if (p && !p.gesperrt) { gibMuscheln(p, geh, 'gehalt'); n++; } }
  if (n) { sende({ typ: 'zahltag', n, gehalt: geh }); sag(`Zahltag! … Alle mit Job bekommen ${geh} Muscheln Gehalt.`, 2); }
}, (CFG.jobs?.gehaltMinuten ?? 5) * 60000);

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
const warte = []; let spricht = false; const gesprochen = [], kleinkram = [];   // kleinkram: nur Prio-2/3-Ansagen fürs Limit
const TON_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'muscheltal-ton-')); let tonNr = 0;
let stimme = CFG.stimme.mac, stilleSeit = Date.now();
const ECHT = !STILL && process.platform === 'darwin';
const dauerMs = t => t.length * 62 + (t.match(/…/g) || []).length * 450 + 300;   // Schätzung ohne echte Stimme
let ohnePausen = false;                                    // manche Premium-Stimmen hängen an [[slnc]]-Befehlen
const fuerStimme = t => ohnePausen ? t.replace(/\s*…\s*/g, ', ') : t.replace(/\s*…\s*/g, ' [[slnc 250]] ').replace(/([!?])\s+/g, '$1 [[slnc 150]] ');
function sag(text, prio = 2) {
  if (!text) return;
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
let sprichtSeit = 0;
// Sicherung: Sprache erzeugen darf max. 10 s dauern, Abspielen max. 20 s. Hängt das Erzeugen öfter, hilft sich das Programm selbst.
let schritt = '', haenger = 0;
setInterval(() => {
  const grenze = schritt === 'piper' ? 8000 : schritt === 'erzeugen' ? 25000 : 20000;
  if (schritt === 'piper' && spricht && Date.now() - sprichtSeit >= grenze) { console.log('⚠️  Piper hing – starte die Stimme neu.'); sprichtSeit = Date.now(); PIPER.neustart(); return; }
  if (!spricht || Date.now() - sprichtSeit < grenze) return;
  console.log(`⚠️  Ansage hing beim ${schritt === 'erzeugen' ? 'Erzeugen der Sprache (say, Stimme „' + stimme + '“)' : schritt === 'abspielen' ? 'Abspielen (afplay)' : 'Warten (' + schritt + ')'} – Anna macht weiter.`);
  if (schritt === 'erzeugen' && ++haenger >= 2) {
    haenger = 0;
    if (!ohnePausen) { ohnePausen = true; console.log('   → Versuche es ab jetzt ohne Sprechpausen-Befehle.'); }
    else { const e = CFG.stimme.macErsatz.shift(); if (e) { stimme = e; console.log(`   → Wechsle auf die Stimme „${e}“.`); } }
  }
  sprichtSeit = Date.now();
  if (sayProzess && sayProzess.exitCode === null) { try { sayProzess.kill(); } catch { fertig(); } } else fertig();
}, 1000);
function fertig() { spricht = false; stilleSeit = Date.now(); setTimeout(weiter, 50); }
function weiter() {
  if (spricht || !warte.length) return;
  if (ECHT && !PIPER.bereit && piperErwartet()) { clearTimeout(weiter.t); weiter.t = setTimeout(weiter, 400); return; }   // Stimme startet gerade – kurz warten, nie die Mac-Stimme
  const { text } = warte.shift(); spricht = true; sprichtSeit = Date.now(); gesprochen.push(Date.now()); letzteAnsageZeit = Date.now();
  sende({ typ: 'ansage', text, ms: dauerMs(text) });
  if (!ECHT) { setTimeout(fertig, dauerMs(text)); return; }
  const aufSeite = CFG.stimme.wiedergabe !== 'mac' && seiteHatTon() && Date.now() > stimmeFehlerBis;
  // Sprach-Speicher: schon einmal erzeugte Sätze werden sofort wieder abgespielt (spart die lange Erzeugung)
  const key = crypto.createHash('md5').update(`${PIPER.bereit ? 'piper:' + PIPER.name : stimme}|${CFG.stimme.tempo}|${ohnePausen}|${text}`).digest('hex');
  const fertigDatei = path.join(CACHE_DIR, key + '.wav'), datei = path.join(TON_DIR, `s${++tonNr % 20}.wav`);
  const args = ['-v', stimme, '-r', String(CFG.stimme.tempo)];
  // Immer erst eine Sprachdatei erzeugen (say hängt sonst manchmal an Mehrfach-Ausgabe/BlackHole), dann abspielen
  args.push('-o', datei, '--file-format=WAVE', '--data-format=LEI16@22050');
  schritt = 'erzeugen'; const t0say = Date.now();
  let fehler = '';
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
      if (++unbestaetigt >= 3) { unbestaetigt = 0; stimmeFehlerBis = Date.now() + 60000; console.log('🔈 Live-Seite bestätigt Annas Stimme nicht – spreche 1 Minute über die Mac-Lautsprecher.'); }
      setTimeout(fertig, ms);
      return;
    }
    if (code === 0 && !ausSpeicher) {
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
  if (ausSpeicher) { if (aufSeite) try { fs.copyFileSync(fertigDatei, datei); } catch {} return nachErzeugen(0); }
  if (PIPER.bereit) {                                      // Piper: eigene Offline-Stimme, unabhängig vom macOS-Sprachdienst
    schritt = 'piper';
    return PIPER.sprich(text, datei, ok => { if (!ok) fehler = 'Piper konnte den Satz nicht erzeugen'; nachErzeugen(ok ? 0 : 1); });
  }
  const pr = sayProzess = spawn('say', [...args, fuerStimme(text)], { stdio: ['ignore', 'pipe', 'pipe'] });
  pr.on('error', e => { console.log('⚠️  say-Fehler:', e.message); fertig(); });
  pr.stderr.on('data', d => fehler += d);
  pr.on('close', nachErzeugen);
}

// ---------- Piper: Annas Stimme offline im eigenen Prozess (werkzeug/stimme-…/…onnx) ----------
// Wird beim Start geladen. Hängt der Prozess, startet er neu. Fehlt das Modell, spricht wie bisher der Mac (say).
var PIPER = { bereit: false, name: '', w: null, auftraege: new Map(), nr: 0 };
// Mac-Stimme (say) nur, wenn es gar kein Piper-Modell gibt oder in den Einstellungen engine 'mac' steht
var piperDa = null, piperDaZeit = 0;
var piperErwartet = () => { if (CFG.stimme.engine === 'mac') return false; if (Date.now() - piperDaZeit > 10000) { piperDaZeit = Date.now(); try { piperDa = fs.readdirSync(path.join(DIR, 'werkzeug', CFG.stimme.piperModell || 'stimme-kerstin')).some(f => f.endsWith('.onnx')); } catch { piperDa = false; } } return piperDa; };
function piperStarten() {
  const ordner = path.join(DIR, 'werkzeug', CFG.stimme.piperModell || 'stimme-kerstin');
  let modell = null; try { modell = fs.readdirSync(ordner).find(f => f.endsWith('.onnx')); } catch {}
  if (!modell || CFG.stimme.engine === 'mac') { if (!modell && ECHT) console.log('ℹ️  Piper-Stimme nicht gefunden – Anna spricht mit der Mac-Stimme.'); return; }
  PIPER.name = modell.replace('.onnx', '');
  const w = PIPER.w = fork(path.join(DIR, 'tts-worker.mjs'), [path.join(ordner, modell), String(CFG.stimme.piperTempo ?? 1.08)], { stdio: ['ignore', 'ignore', 'pipe', 'ipc'] });
  let fehlerText = ''; w.stderr.on('data', d => { fehlerText = (fehlerText + d).slice(-400); });
  w.on('message', m => {
    if (m.bereit) { PIPER.bereit = true; console.log(`🗣️  Anna spricht mit der Offline-Stimme „${PIPER.name}“ (Piper) – unabhängig vom macOS-Sprachdienst.`); return; }
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
PIPER.sprich = (text, datei, cb) => { const id = ++PIPER.nr; PIPER.auftraege.set(id, cb); PIPER.w.send({ id, text, datei }); };
PIPER.neustart = () => { const w = PIPER.w; PIPER.bereit = false; PIPER.w = null; for (const cb of PIPER.auftraege.values()) cb(false); PIPER.auftraege.clear(); try { w?.kill(); } catch {} setTimeout(piperStarten, 500); };
setTimeout(piperStarten, 200);
let langsam = 0;
// Beim Start alle festen Sätze leise im Hintergrund vorab erzeugen (niedrige Priorität), damit sie im LIVE sofort kommen
function vorwaermen() {
  if (!ECHT) return;
  if (PIPER.bereit || PIPER.w || piperErwartet()) return;  // Piper braucht kein Vorab-Erzeugen (und keine Mac-Stimme)
  const offen = [...festeSaetze(), ...Object.values(require_preis())].filter(Boolean);
  let i = 0, fertigN = 0;
  const naechster = () => {
    if (spricht || warte.length) return setTimeout(naechster, 1500);
    while (i < offen.length) {
      const text = offen[i++], key = crypto.createHash('md5').update(`${PIPER.bereit ? 'piper:' + PIPER.name : stimme}|${CFG.stimme.tempo}|${ohnePausen}|${text}`).digest('hex'), ziel = path.join(CACHE_DIR, key + '.wav');
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
const CACHE_DIR = path.join(DIR, 'werkzeug', 'stimme'); fs.mkdirSync(CACHE_DIR, { recursive: true });
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
const MUSIK_DATEIEN = [1, 2, 3, 4, 5].map(i => `insel_${i}.mp3`).map(f => path.join(DIR, 'seite', 'musik', f));
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
// Alle 30 s eine kurze Statuszeile im Terminal – hilft bei der Fehlersuche während des LIVEs
var letzteAnsageZeit = 0;
setInterval(() => {
  const seiten = [...kunden.keys()].map(id => { const t = tonStatus.get(id) || {}; return `#${id}${t.vorschau ? '(Vorschau)' : ''}${id === tonSeite ? '★' : ''} Ton ${t.an ? 'an' : 'aus'}/${t.ac || '?'}`; });
  const weg = ECHT ? (CFG.stimme.wiedergabe !== 'mac' && seiteHatTon() && Date.now() > stimmeFehlerBis ? 'Seite (Stream)' : 'Mac-Lautsprecher') : 'aus (Test)';
  console.log(`ℹ️  ${new Date().toLocaleTimeString('de-DE')} · TikTok: ${tiktokStatus} (${tiktokEreignisse} Ereignisse${tiktokLetztes ? ', letztes vor ' + Math.round((Date.now() - tiktokLetztes) / 1000) + ' s' : ''}) · Seiten: ${seiten.join(', ') || 'keine!'} · Anna über: ${weg} · letzte Ansage vor ${letzteAnsageZeit ? Math.round((Date.now() - letzteAnsageZeit) / 1000) + ' s' : '–'}`);
}, 30000);
setInterval(musikLokal, 3000);
process.on('exit', () => lokalMusik?.kill());

// ---------- Dauer-Moderation: Anna redet immer, mit kurzen Pausen dazwischen ----------
const followDank = [], begruessen = [], begruesst = new Set();
let letzterLive = 0, letzterRundgang = 0, modNr = 0, eventModNr = 0, countdownGesagt = '', eventZehnGesagt = '';
// Rangliste: beste Haus-Stufe zuerst, bei Gleichstand entscheiden die Muscheln aus Events
const rangFolge = (a, b) => b.stufe - a.stufe || (b.eventMuscheln || 0) - (a.eventMuscheln || 0) || b.muscheln - a.muscheln;
const zufallAus = fs => fs[Math.floor(Math.random() * fs.length)]();
const grossKlein = t => t.charAt(0).toUpperCase() + t.slice(1);
const H = () => satz('hinweis');                              // die wichtigsten Hinweise kommen oft
const MODERATION = [
  H,
  () => satz('tipp'),
  () => { const s = EV.naechstesIn(); return s > 45 ? satz('teaser', { zeit: s >= 100 ? `${Math.round(s / 60)} Minuten` : 'gut einer Minute' }) : null; },
  () => rundgang(),
  H,
  () => satz('fakt'),
  () => satz('geschenkInfo'),
  () => { const z = zielJetzt(); return z ? satz('ziel', { rest: z.ziel - bewohner, projekt: z.name, bewohner, zielzahl: z.ziel }) : null; },
  H,
  () => satz('frage'),
  () => { const t = Object.values(S.spieler).filter(p => !p.gesperrt).sort(rangFolge); return t.length > 1 ? satz('rangliste', { erster: sprechName(t[0]), zweiter: sprechName(t[1]) }) : null; },
  () => rundgang(),
  () => S.kasse > 0 ? satz('kasse', { kasse: S.kasse.toLocaleString('de-DE') }) : null,
  () => S.projekt ? satz('projekt', { projekt: S.projekt.name, prozent: Math.floor(S.projekt.stand / S.projekt.ziel * 100) }) : null,
  H,
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
  const dringend = followDank.length || likeDank.length;     // Dank kommt sofort, Moderation erst nach der Pause
  if (spricht || warte.length || Date.now() - stilleSeit < (dringend ? .8 : (CFG.stimme.pauseSek ?? 4)) * 1000) return;
  // 1. Follows bedanken
  if (followDank.length) {
    return sag(satz('followEins', { name: sprechName(followDank.shift()) }), 1);   // einzeln, kurz
  }
  // 1a. Viele Likes von einer Person: bedanken
  if (likeDank.length) { const p = likeDank.shift(); return sag(satz('likeDank', { name: sprechName(p) }), 1); }
  // 1b. Wer „haus“ geschrieben hat: Kamera fliegt zum Haus (ab und zu, nicht während Events)
  const kameraEvent = ['schatzsuche', 'meeresbesuch', 'flaschenpost', 'moewenalarm', 'hausbesuch'].includes(EV.id());
  if (!kameraEvent && hausWunsch.length && Date.now() - letztesHausZeigen > (EV.laeuft() ? 15000 : 8000)) {
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
    if (art === 3) return sag(zufallAus([H, H, () => satz('stimmung', { aktive: aktiveAnzahl() })]), 4);
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
  return {
    ...EV.oeffentlich(),
    spieler: S.reihenfolge.map(id => S.spieler[id]).filter(p => p && !p.gesperrt).map(p => ({ id: p.id, name: p.name, muscheln: p.muscheln, stufe: p.stufe, anbauten: p.anbauten, farbe: p.farbe, platz: p.platz, eventMuscheln: p.eventMuscheln })),
    stufen: CFG.stufen.map(s => s.name), stufenAb: CFG.stufen.map(s => s.ab),
    projekt: S.projekt, fertig: S.fertig, kasse: S.kasse,
    jobs: Object.fromEntries(Object.entries(S.jobs).map(([nr, j]) => [nr, S.spieler[j.id]?.name || ''])),
    bewohner, ziel: zielJetzt(), strassen: CFG.strassen,
    tiktokName: CFG.tiktokName, test: TEST, ton: CFG.ton, ort: CFG.ort,
  };
}

const TYPEN = { '.mp3': 'audio/mpeg', '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/wachsen') {                         // Seite meldet: Insel ist gewachsen (nur Zahl, kein freier Text)
    const n = Math.min(5000, Math.max(0, parseInt(url.searchParams.get('n'), 10) || 0));
    if (n && Date.now() - letzteSeitenAnsage > 15000) { letzteSeitenAnsage = Date.now(); sag(`Die Insel wächst! … ${n} neue Grundstücke sind dazugekommen.`, 0); }
    res.writeHead(204); return res.end();
  }
  // Test-Zugänge nur direkt am Mac – nie über den öffentlichen Link (Cloudflare setzt cf-ray / cf-connecting-ip)
  if (TEST && url.pathname === '/test' && !req.headers['cf-ray'] && !req.headers['cf-connecting-ip']) {                 // nur Test-Modus: Event / Geschenk-Show auslösen
    const id = url.searchParams.get('event'), art = url.searchParams.get('geschenk');
    if (url.searchParams.has('stadt')) { const n = +url.searchParams.get('stadt'), ids = CFG.abstimmung.projekte.map(x => x.id); S.fertig = Array.from({ length: n }, (_, i) => ids[i % ids.length]); const pr = CFG.abstimmung.projekte[n % ids.length]; S.projekt = pr ? { id: pr.id, name: pr.name, ziel: pr.ziel, stand: Math.round(pr.ziel * .45) } : null; zustand(); }
    if (url.searchParams.has('fertigbauen') && S.projekt) { S.projekt.stand = S.projekt.ziel - 1; S.kasse += 10; inKasse(5); }
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
    if (url.searchParams.has('an')) tonStatus.set(id, { ...alt, an: url.searchParams.get('an') === '1', ac: url.searchParams.get('ac'), vorschau: url.searchParams.get('vorschau') === '1', zeit: Date.now() });
    if (url.searchParams.get('stimme') === '1' && alt.stimmeOk !== true) { tonStatus.set(id, { ...tonStatus.get(id), stimmeOk: true }); console.log(`🔊 Anna spricht über die Live-Seite #${id} (Stream-Ton).`); }
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
  const datei = path.join(DIR, 'seite', path.normalize(url.pathname === '/' ? '/index.html' : url.pathname).replace(/^(\.\.[/\\])+/, ''));
  if (!datei.startsWith(path.join(DIR, 'seite'))) { res.writeHead(403); return res.end(); }
  fs.readFile(datei, (e, d) => {
    if (e) { res.writeHead(404); return res.end('nicht gefunden'); }
    res.writeHead(200, { 'Content-Type': TYPEN[path.extname(datei)] || 'application/octet-stream' }); res.end(d);
  });
}).on('error', e => {
  if (e.code === 'EADDRINUSE') {                            // Programm läuft schon in einem anderen Fenster
    console.log(`\n⚠️  Muschel-Tal LIVE läuft schon (in einem anderen Terminalfenster). Dieses Fenster kannst du schließen.\n`);
    process.exit(2);
  }
  throw e;
}).listen(CFG.port, () => {
  console.log(`\n🐚 Muschel-Tal LIVE läuft:  http://localhost:${CFG.port}   (Version ${VERSION})`);
  console.log('   Diese Adresse in TikTok LIVE Studio als Link-/Browser-Quelle (1080×1920) einfügen.\n');
});

// ---------- TikTok-Verbindung ----------
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
  const U = u => u && { ...u, uniqueId: u.uniqueId || u.displayId || u.username || '', nickname: u.nickname || '' };
  const nm = d => '@' + (U(d.user)?.uniqueId || '?');
  const txt = d => d.content ?? d.comment ?? '';
  c.on(WebcastEvent.CHAT, d => { const u = U(d.user); if (!u?.uniqueId) return; tt('💬', `${nm(d)}: ${txt(d)}`); kommentar(u, txt(d)); });
  // TikTok schickt nicht jedes Like einzeln, aber immer die Gesamtzahl (total). Was fehlt, kommt trotzdem in die Kasse.
  let likeTotal = 0;
  c.on(WebcastEvent.LIKE, d => {
    const u = U(d.user), n = +(d.count ?? d.likeCount) || 1, total = +(d.total ?? d.totalLikeCount) || 0;
    if (u?.uniqueId) { tt('❤️', `${nm(d)} +${n} Likes`); like(u, n); } else { S.likesGesamt += n; inKasse(n * CFG.kasse.proLike); }
    if (total) {
      const fehlt = likeTotal ? total - likeTotal - n : 0;
      if (fehlt > 0 && fehlt < 100000) { S.likesGesamt += fehlt; inKasse(fehlt * CFG.kasse.proLike); geaendert = true; zustand(); }
      likeTotal = Math.max(likeTotal, total);
    }
  });
  c.on(WebcastEvent.FOLLOW, d => { const u = U(d.user); if (!u?.uniqueId) return; tt('➕', `${nm(d)} folgt`); follow(u); });
  c.on(WebcastEvent.SHARE, d => { const u = U(d.user); if (!u?.uniqueId) return; tt('🔁', `${nm(d)} teilt`); teilen(u); });
  c.on(WebcastEvent.MEMBER, d => { const u = U(d.user); if (!u?.uniqueId) return; tt('👋', `${nm(d)} ist da`); beitritt(u); });
  c.on(WebcastEvent.GIFT, d => {
    d.user = U(d.user);
    const g = d.giftDetails || {};
    if (g.giftType === 1 && !d.repeatEnd) return; // Serie läuft noch – erst am Ende zählen
    tt('🎁', `${nm(d)}: ${g.giftName || 'Geschenk'} ×${d.repeatCount || 1}`);
    const ex = d.extendedGiftInfo || {};
    geschenk(d.user || {}, g.giftName || ex.name || 'das Geschenk', g.diamondCount || ex.diamond_count || 1, d.repeatCount || 1);
  });
  c.on(WebcastEvent.STREAM_END, () => { console.log('Stream beendet.'); speichern(); });
  c.on('disconnected', () => { tiktokStatus = 'getrennt'; console.log('⚠️  Verbindung zu TikTok weg – neuer Versuch in 15 s'); setTimeout(versuche, 15000); });
  const st = await c.connect();
  tiktokStatus = 'verbunden';
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
// Spielstand sichern beim Beenden – egal wie: ctrl+C, Terminalfenster schließen, Mac fährt herunter
// Sicherheitsnetz: ein unerwarteter Fehler darf nie den LIVE beenden – melden und weiterlaufen
for (const art of ['uncaughtException', 'unhandledRejection']) process.on(art, e => {
  if (e?.code === 'EADDRINUSE') return;
  console.log('⚠️  Interner Fehler (Programm läuft weiter):', e?.stack?.split('\n').slice(0, 3).join(' | ') || e);
  if (spricht && Date.now() - sprichtSeit > 3000) fertig();
});
for (const sig of ['SIGINT', 'SIGHUP', 'SIGTERM']) process.on(sig, () => { geaendert = true; speichern(); process.exit(0); });
