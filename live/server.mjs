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

const DIR = path.dirname(fileURLToPath(import.meta.url));
const CFG = JSON.parse(fs.readFileSync(path.join(DIR, 'einstellungen.json'), 'utf8'));
const STAND = path.join(DIR, 'stand.json');
const TEST = process.argv.includes('--test');
const STILL = process.argv.includes('--still') || !CFG.stimme.an;

// ---------- Spielstand ----------
const leer = () => ({ spieler: {}, reihenfolge: [], projekt: null, fertig: [], abstimmung: null, likesGesamt: 0, kasse: 0 });
let S = leer();
try { S = { ...leer(), ...JSON.parse(fs.readFileSync(STAND, 'utf8')) }; } catch {}
if (TEST && process.argv.includes('--neu')) S = leer();
let geaendert = false;
const speichern = () => { if (!geaendert || TEST) return; fs.writeFileSync(STAND, JSON.stringify(S)); geaendert = false; };
setInterval(speichern, 10000);

const stufeVon = m => { let i = 0; CFG.stufen.forEach((s, k) => { if (m >= s.ab) i = k; }); return i; };

function spieler(u) {
  const id = String(u.uniqueId || '').toLowerCase();
  if (!id) return null;
  let p = S.spieler[id];
  if (!p) {
    p = S.spieler[id] = { id, name: '@' + u.uniqueId, muscheln: 0, stufe: 0, anbauten: [], farbe: null, platz: S.reihenfolge.length };
    S.reihenfolge.push(id);
    sende({ typ: 'neu', id });
    sag(`Willkommen im Muschel-Tal, ${sprechName(p)}! Dein Zelt steht.`, 1);
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
    sag(`${sprechName(p)} hat jetzt ${artikel(CFG.stufen[p.stufe].name)}!`, 2);
  }
  zustand();
}

const artikel = n => (/^(Strohhütte|Stelzenhütte|Villa|Luxusvilla)$/.test(n) ? 'eine ' : /^(Bungalow|Strandpalast)$/.test(n) ? 'einen ' : 'ein ') + n;
// Namen für die Stimme lesbar machen: "lena_xx.22" -> "lena xx"
const sprechName = p => p.name.replace(/^@/, '').replace(/[._]+/g, ' ').replace(/\d{3,}/g, '').trim() || 'Neuer Bewohner';

// ---------- Ereignisse ----------
function like(u, anzahl) {
  const p = spieler(u); if (!p) return;
  S.likesGesamt += anzahl;
  inKasse(anzahl * CFG.kasse.proLike);
  gibMuscheln(p, anzahl * CFG.muschelnProLike, 'like');
}

function kommentar(u, text) {
  const neu = !S.spieler[String(u.uniqueId || '').toLowerCase()];
  const p = spieler(u); if (!p) return;
  if (neu) gibMuscheln(p, CFG.muschelnFuerErstenKommentar, 'kommentar');
  const t = String(text || '').toLowerCase().trim();
  // Abstimmung: 1 / 2 / 3
  const a = S.abstimmung;
  if (a && /^[123]$/.test(t)) {
    a.stimmen[p.id] = Number(t) - 1; geaendert = true; zustand(); return;
  }
  for (const wort of t.split(/[^a-zäöüß]+/)) {
    const ab = CFG.anbauten[wort];
    if (ab) {
      if (p.anbauten.includes(wort)) continue;
      if (p.stufe < ab.abStufe) { sende({ typ: 'info', id: p.id, text: `${ab.name} ab ${CFG.stufen[ab.abStufe].name}` }); continue; }
      if (p.muscheln < ab.kosten) { sende({ typ: 'info', id: p.id, text: `${ab.name}: ${ab.kosten} 🐚` }); continue; }
      p.anbauten.push(wort); geaendert = true;
      sende({ typ: 'anbau', id: p.id, was: wort });
      sag(`${sprechName(p)} baut ${ab.name === 'Boot' ? 'ein Boot' : ab.name === 'Palme' ? 'eine Palme' : ab.name === 'Laterne' ? 'eine Laterne' : ab.name === 'Flagge' ? 'eine Flagge' : 'einen ' + ab.name}.`, 3);
    }
    const f = CFG.farben[wort];
    if (f && p.farbe !== f) { p.farbe = f; geaendert = true; sende({ typ: 'farbe', id: p.id }); }
  }
  zustand();
}

function geschenk(u, name, diamanten, anzahl) {
  const p = spieler(u); if (!p) return;
  const d = Math.max(1, diamanten || 1) * Math.max(1, anzahl || 1);   // Coins insgesamt: 1 Coin = 1 Muschel (= 0,01 €)
  sende({ typ: 'geschenk', id: p.id, name, anzahl, diamanten: d });
  inKasse(d * CFG.kasse.proCoin);
  sag(anzahl > 1 ? `Danke ${sprechName(p)} für ${anzahl} mal ${name}!` : `Danke ${sprechName(p)} für ${name}!`, 0);
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
    sag(`Wahnsinn! ${bewohner} Bewohner! ${vorher.name} auf der ${vorher.ort} ist fertig!`, 0);
  }
  zustand();
}
function follow(u) {
  const p = spieler(u); if (!p) return;
  sende({ typ: 'follow', id: p.id });
  setzeBewohner(bewohner + 1, 'follow');
  inKasse(CFG.kasse.proFollow);
  const z = zielJetzt();
  sag(`${sprechName(p)} zieht ins Muschel-Tal ein!${z ? ` Noch ${z.ziel - bewohner} Bewohner bis zum ${z.name}.` : ''}`, 1);
  gibMuscheln(p, CFG.muschelnFuerFollow, 'follow');
}

function teilen(u) {
  const p = spieler(u); if (!p) return;
  inKasse(CFG.kasse.proShare);
  sende({ typ: 'teilen', id: p.id });
  sag(`Danke ${sprechName(p)} fürs Teilen!`, 3);
  zustand();
}

// ---------- Gemeinschaftsprojekt + Abstimmung ----------
function starteAbstimmung() {
  if (S.abstimmung || S.projekt) return;
  const offen = CFG.abstimmung.projekte.filter(x => !S.fertig.includes(x.id));
  if (!offen.length) return;
  const wahl = offen.sort(() => Math.random() - .5).slice(0, 3);
  S.abstimmung = { optionen: wahl.map(x => x.id), stimmen: {}, endet: Date.now() + CFG.abstimmung.dauerSekunden * 1000 };
  sag(`Abstimmung! Was bauen wir als Nächstes? Schreibt 1 für ${wahl[0].name}, 2 für ${wahl[1]?.name}${wahl[2] ? ', oder 3 für ' + wahl[2].name : ''}.`, 0);
  zustand();
}
function beendeAbstimmung() {
  const a = S.abstimmung; if (!a) return;
  const z = a.optionen.map(() => 0); Object.values(a.stimmen).forEach(i => z[i]++);
  const sieger = z.indexOf(Math.max(...z));
  const pr = CFG.abstimmung.projekte.find(x => x.id === a.optionen[sieger]);
  S.abstimmung = null;
  S.projekt = { id: pr.id, name: pr.name, ziel: pr.ziel, stand: 0 };
  geaendert = true;
  sende({ typ: 'projekt', id: pr.id });
  sag(`Entschieden: Wir bauen ${pr.name === 'Brücke' || pr.name === 'Eisdiele' ? 'eine ' + pr.name : pr.name === 'Riesenrad' ? 'ein Riesenrad' : 'einen ' + pr.name}! Jedes Like hilft mit.`, 0);
  zustand();
}
function projektFertig() {
  const pr = S.projekt; S.fertig.push(pr.id); S.projekt = null; geaendert = true;
  sende({ typ: 'fertig', id: pr.id });
  sag(`Geschafft! ${pr.name} ist fertig. Danke an alle!`, 0);
  naechsteAbstimmung = Date.now() + 20000;
}
let naechsteAbstimmung = Date.now() + (TEST ? 15000 : 60000);
setInterval(() => {
  const a = S.abstimmung;
  if (a && Date.now() >= a.endet) beendeAbstimmung();
  if (!a && !S.projekt && Date.now() >= naechsteAbstimmung) {
    starteAbstimmung(); naechsteAbstimmung = Date.now() + CFG.abstimmung.alleMinuten * 60000;
  }
  zustand();
}, 1000);

// ---------- Stimme (macOS „say“, unbegrenzt, offline) ----------
const warte = []; let spricht = false; const gesprochen = [];
const TON_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'muscheltal-ton-')); let tonNr = 0;
let stimme = CFG.stimme.mac;
function sag(text, prio = 2) {
  sende({ typ: 'ansage', text });
  if (STILL) return;
  const jetzt = Date.now();
  while (gesprochen.length && jetzt - gesprochen[0] > 60000) gesprochen.shift();
  if (prio >= 2 && gesprochen.length >= CFG.stimme.maxProMinute) return; // nicht zuquatschen
  warte.push({ text, prio });
  warte.sort((a, b) => a.prio - b.prio);
  if (warte.length > CFG.stimme.maxWarteschlange) warte.pop();
  weiter();
}
function weiter() {
  if (spricht || !warte.length) return;
  if (process.platform !== 'darwin') { warte.length = 0; return; }
  const { text } = warte.shift(); spricht = true; gesprochen.push(Date.now());
  const aufSeite = CFG.stimme.wiedergabe !== 'mac' && kunden.size > 0;
  const datei = path.join(TON_DIR, `s${++tonNr % 20}.wav`);
  const args = ['-v', stimme, '-r', String(CFG.stimme.tempo)];
  if (aufSeite) args.push('-o', datei, '--file-format=WAVE', '--data-format=LEI16@22050');
  const pr = spawn('say', [...args, text]);
  let fehler = '';
  pr.stderr.on('data', d => fehler += d);
  pr.on('close', code => {
    if (aufSeite && code === 0) {                      // Seite spielt ab; warten, bis die Ansage vorbei ist
      let ms = 2000; try { ms = (fs.statSync(datei).size - 44) / 44.1 + 400; } catch {}
      sende({ typ: 'stimme', url: '/ton/' + path.basename(datei) + '?' + Date.now() });
      setTimeout(() => { spricht = false; weiter(); }, ms);
      return;
    }
    spricht = false;
    if (code !== 0 && /voice|stimme/i.test(fehler)) {
      const ersatz = CFG.stimme.macErsatz.shift();
      if (ersatz) { console.log(`Stimme „${stimme}“ nicht gefunden, nehme „${ersatz}“.`); stimme = ersatz; warte.unshift({ text, prio: 0 }); }
    }
    weiter();
  });
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
  const a = S.abstimmung;
  let abst = null;
  if (a) {
    const z = a.optionen.map(() => 0); Object.values(a.stimmen).forEach(i => z[i]++);
    abst = { optionen: a.optionen.map(id => CFG.abstimmung.projekte.find(x => x.id === id).name), stimmen: z, rest: Math.max(0, Math.round((a.endet - Date.now()) / 1000)) };
  }
  return {
    spieler: S.reihenfolge.map(id => S.spieler[id]),
    stufen: CFG.stufen.map(s => s.name), stufenAb: CFG.stufen.map(s => s.ab),
    projekt: S.projekt, fertig: S.fertig, abstimmung: abst, kasse: S.kasse,
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
  sag('Muschel-Tal live ist gestartet. Liked, kommentiert und baut eure Häuser!', 0);
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
    const p = spieler({ uniqueId: nm }); const st = CFG.stufen[(i * 7) % CFG.stufen.length];
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
    if (S.abstimmung && r < .3) kommentar(u, String(1 + Math.floor(Math.random() * 3)));
    else if (r < .7) like(u, 1 + Math.floor(Math.random() * 15));
    else if (r < .9) kommentar(u, worte[Math.floor(Math.random() * worte.length)]);
    else if (r < .97) { const g = gifts[Math.floor(Math.random() * (Math.random() < .9 ? 4 : gifts.length))]; geschenk(u, g[0], g[1], 1 + Math.floor(Math.random() * 3)); }
    else if (Math.random() < .5) teilen(u); else follow(u);
  }, 700);
}

if (TEST) simulator(); else versuche();
process.on('SIGINT', () => { geaendert = true; speichern(); process.exit(0); });
