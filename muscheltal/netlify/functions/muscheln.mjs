// Muschel-Konten: Namen beanspruchen, Kontobuch, Login-Serie, Aufgaben, schwebende Muscheln, Spenden.
// Jede Buchung ist ein eigener Eintrag mit festem Schlüssel "b/<name>/<art>/<kennung>/<betrag>" – der Betrag steht im Schlüssel,
// so ergibt sich der Kontostand aus einer einzigen Liste. Feste Schlüssel (z. B. login/2026-11-10) verhindern Doppelbuchungen.
import { getStore } from "@netlify/blobs";
import { JOBS } from "../lib/jobs.mjs";
import { BEWOHNER, NACHBARN, SEIT } from "../lib/bewohner.mjs";
import { liveVergeben } from "./live.mjs";
import { CODES } from "../lib/codes.mjs";
import { SHOP } from "../lib/shop.mjs";
import { QUIZ } from "../lib/quiz.mjs";

// Schlüssel gilt: der vom Beanspruchen (h) oder einer aus einer Anmeldung mit Name + PIN (hs, höchstens 5 Geräte)
const tokOk = (c, h) => !!c && (c.h === h || (Array.isArray(c.hs) && c.hs.includes(h)));
// Angemeldet bleiben: Name + Schlüssel zusätzlich als HttpOnly-Cookie (nur der Server liest es). Leert der Browser seinen
// Seitenspeicher (z. B. Safari nach 7 Tagen ohne Besuch), stellt die Seite die Anmeldung damit still wieder her – die PIN
// braucht man so nur beim Wechsel in einen anderen Browser oder auf ein anderes Handy.
const mitCookie = (res, nm, token) => { res.headers.append("set-cookie", "mt-k=" + encodeURIComponent(nm + "|" + token) + "; Max-Age=157680000; Path=/api/muscheln; HttpOnly; Secure; SameSite=Lax"); return res; };
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const NAME = /^@[a-z0-9._]{1,40}$/;
const ERF_CLIENT = new Set(["LUPE", "AUF", "UNTER", "SCOOT", "SCHOEPFER", "WAL", "SCHILD", "MOND", "WELT", "NACHT"]);
const STICKER = new Set(["palast", "doener", "bar", "villa", "acai", "werkstatt", "baeckerei", "nagel", "markt", "kiosk", "boba", "pizza", "tierheim", "yacht", "cocobay", "kokosbad", "coast", "kokos", "cococare", "gaming", "feuer", "anleger", "gpearl", "ev_wochenmarkt", "ev_flohmarkt", "ev_konzert", "ev_feuerwerk", "sandburg", "angeln", "ev_kino"]);
const SERIE = [3, 5, 8, 12, 17, 23, 32];
// 🎣 Angelstellen: je Insel 15 eigene Fänge in den Güteklassen 0 Gewöhnlich … 8 Kosmisch (kein Einzigartig). Manche beißen nur zu
// bestimmter Tageszeit (Berlin) oder bei bestimmtem Wetter (Hamburg, vom Server geprüft). Nur selten gibt es zusätzlich 1–3 Muscheln.
const GUETE = [30, 22, 15, 11, 8, 6, 4, 2.4, 1.2, 0.4];
export const FISCHE = {stiefel: [0, 0, ""], sardine: [0, 0, ""], krabbe: [1, 0, ""], seestern: [1, 0, ""], kugel: [2, 0, ""], tinte: [2, 0, "nacht"], hummer: [3, 0, ""], kompass: [3, 0, "regen"], hai: [4, 0, ""], schluessel: [4, 0, "morgen"], ring: [5, 0, ""], amphore: [5, 0, "sturm"], geist: [6, 0, "nacht"], krone: [7, 0, "morgen"], mondfisch: [8, 0, "klarnacht"], treibholz: [0, 1, ""], garnele: [0, 1, ""], schnecke: [1, 1, ""], schwamm: [1, 1, ""], clown: [2, 1, ""], kokosnuss: [2, 1, "sonne"], okto: [3, 1, ""], koralle: [3, 1, "sonne"], anker: [4, 1, ""], auster: [4, 1, "regen"], dreizack: [5, 1, ""], muenze: [5, 1, "abend"], drache: [6, 1, "sturm"], diamant: [7, 1, "nacht"], sternfisch: [8, 1, "klarnacht"]};
const zz = () => crypto.getRandomValues(new Uint32Array(1))[0] / 2 ** 32;
const PRO = {}; for (const [t, i] of Object.values(FISCHE)) PRO[i + "/" + t] = (PRO[i + "/" + t] || 0) + 1;// Fänge je Insel und Güteklasse
let WJ = { t: 0, code: 0, wind: 0 };
async function wetterJetzt() {
  if (Date.now() - WJ.t < 6e5) return WJ;
  try { const r = await fetch("https://api.open-meteo.com/v1/forecast?latitude=" + WLAT + "&longitude=" + WLON + "&current=weather_code,wind_speed_10m&timezone=GMT&forecast_days=1"); const j = await r.json(); WJ = { t: Date.now(), code: j.current.weather_code, wind: j.current.wind_speed_10m }; } catch (e) {}
  return WJ;
}
function bedingungOk(b, w, h) {
  const c = w.code, regen = (c >= 51 && c <= 67) || (c >= 80 && c <= 82) || c >= 95, klar = c <= 2, nacht = h >= 22 || h < 5;
  if (!b) return true;
  if (b === "nacht") return nacht; if (b === "morgen") return h >= 5 && h < 9; if (b === "abend") return h >= 18 && h < 22;
  if (b === "regen") return regen; if (b === "sturm") return c >= 95 || w.wind >= 35; if (b === "sonne") return klar && h >= 8 && h < 18; if (b === "klarnacht") return klar && nacht;
  return false;
}
async function fischZiehen(insel) {
  const w = await wetterJetzt(), h = Number(new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hour: "2-digit", hourCycle: "h23" }).format(new Date()));
  const L = Object.entries(FISCHE).filter(([, [t, i, b]]) => i === insel && bedingungOk(b, w, h));
  const sum = L.reduce((a, [, [t, i]]) => a + GUETE[t] / PRO[i + "/" + t], 0), r = zz() * sum; let s = 0;
  for (const [id, [t, i]] of L) { s += GUETE[t] / PRO[i + "/" + t]; if (r < s) return id; } return L[0][0];
}
// 🏰 Sandburg: Woche Mo–So; Sonntag ab 18 Uhr holt die Flut die Burg (dann kein Bauen)
function flutJetzt() { const p = Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: "Europe/Berlin", weekday: "short", hour: "2-digit", hourCycle: "h23" }).formatToParts(new Date()).map(x => [x.type, x.value])); return p.weekday === "Sun" && +p.hour >= 18; }
const TZ = "Europe/Berlin";
const tag = (t = Date.now()) => new Intl.DateTimeFormat("sv-SE", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date(t));
const gestern = (d) => { const t = new Date(d + "T12:00:00Z"); t.setUTCDate(t.getUTCDate() - 1); return t.toISOString().slice(0, 10); };
const woche = (d) => { const t = new Date(d + "T12:00:00Z"), w = (t.getUTCDay() + 6) % 7; t.setUTCDate(t.getUTCDate() - w); return t.toISOString().slice(0, 10); };
async function sha(s) { const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join(""); }
// Regenbogen: stimmt die Kennung mit der letzten Regenstunde (Hamburg, letzte 3 Std.) überein und ist es jetzt trocken?
const WLAT = 53.592, WLON = 9.949;
async function regenEnde(id) {
  if (process.env.RB_TEST === "1" && id === "test") return true; // nur lokal zum Testen
  if (!/^\d{4}-\d\d-\d\dT\d\d:00$/.test(id)) return false;
  try {
    const r = await fetch("https://api.open-meteo.com/v1/forecast?latitude=" + WLAT + "&longitude=" + WLON + "&hourly=precipitation&past_hours=3&forecast_hours=1&timezone=GMT&forecast_days=1");
    const j = await r.json(), P = j.hourly.precipitation, Z = j.hourly.time;
    let i = P.length - 2; while (i >= 0 && !(P[i] > .1)) i--;
    return i >= 0 && !(P[P.length - 1] > .1) && Z[i] === id;
  } catch (e) { return false; }
}
// Flaschenpost: Frage und Antwort-Reihenfolge hängen von Name und Flasche ab (jeder bekommt eine andere Frage)
function quizH(s) { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }
function quizFrage(nm, fl) {
  const Q = QUIZ[quizH(nm + "|" + fl) % QUIZ.length], o = Q.a.map((t, i) => [t, i]);
  if (o.length > 2) for (let i = o.length - 1; i > 0; i--) { const j = quizH(nm + fl + "#" + i) % (i + 1); [o[i], o[j]] = [o[j], o[i]]; }
  return { q: Q.q, a: o.map(x => x[0]), r: o.findIndex(x => x[1] === Q.r) };
}
async function liste(store, prefix) { const out = []; let cursor; do { const r = await store.list({ prefix, cursor }); out.push(...r.blobs.map(b => b.key)); cursor = r.cursor; } while (cursor); return out; }

// Job-Zuschlag pro Login-Tag: Team +2, Leitung +3, Ämter (Bürgermeister/in, Palast-Leitung …) +4
function job(nm) {
  const j = JOBS[nm]; if (!j) return null;
  if (j[2] && Date.parse(j[2] + ":00+01:00") <= Date.now()) return null;
  const b = (j[0] || "").toLowerCase(), o = j[1] || "";
  const z = /bürgermeister|palast/.test(b) || /palast/i.test(o) && b !== "team" ? 4 : b === "leitung" ? 3 : 2;
  return { beruf: j[0] || "", ort: o, z };
}
// Kontobuch lesen: Einträge mit Art, Kennung, Betrag
async function buch(store, nm) {
  return (await liste(store, "b/" + nm + "/")).map(k => { const [, , art, id, a] = k.split("/"); return { art, id, a: Number(a) || 0 }; });
}
// Einmaliges Zurücksetzen (z. B. zum Testen): Beanspruchung, Kontobuch, Aufgaben und Spenden des Namens werden gelöscht.
// Läuft je Eintrag genau einmal (Merker x/reset/<name>/<nr>); danach kann der Name neu beansprucht werden.
// [Name, Lauf-Nr., optional: ab Zeitpunkt (ms) – dann werden auch Erfolge und Story-Buchungen ab diesem Zeitpunkt gelöscht]
const TEST_12_11 = 1794438000000; // 12.11.2026 0:00 Uhr (Berlin): Testlauf mit mehreren Testern
const RESET = [...["marina.cgnn", "ju1e_smt", "mimposible", "maja.gnw", "eeli_mxo", "luna.gsn02", "toca_lexi00"].map(n => [n, 1, TEST_12_11]), ["haltsmaulimmeroderso", 1, 0, { kasse: false }], ["marie_nwd0", 1, 0, { voll: true }]];// 18.11.: Test-Konto (Zahlung + Events) komplett zurück auf 0// 17.11.: Beanspruchung entfernt, Konto auf 0 (Spenden in der Inselkasse bleiben)
// Vollständiges Zurücksetzen eines Test-Kontos: alles, was der Name getan hat, wird gelöscht (Konto, Aufgaben, Ausrüstung,
// Sticker, Fische, Sandburg-Beiträge, Likes, Anklopfen, Flaschenpost, Premium/Startangebot, Echtgeld-Testkäufe, Einladungs-Bonus
// des Einladenden, einzigartige Items, alle Erfolge, Spenden). Danach startet der Name wieder bei 0 und kann neu beansprucht werden.
async function vollReset(store, n) {
  for (const k of await liste(store, "")) {
    const t = k.split("/");
    if (k.startsWith("x/reset/") || k.startsWith("x/zurueck/") || k.startsWith("x/nullung/")) continue;
    let weg = (["c", "a", "s", "b", "q"].includes(t[0]) && t[1] === n) || (t[0] === "x" && t.slice(2).includes(n)) || (t[0] === "b" && t[2] === "einladung" && t[3] === n);
    if (!weg && t[0] === "x" && (t[1] === "einzig" || t[1] === "euro")) { const v = String((await store.get(k)) || ""); weg = v === n || v.includes('"nm":"' + n + '"'); }
    if (weg) await store.delete(k);
  }
  const es = getStore("erfolge");
  for (const k of await liste(es, "e/" + n + "/")) await es.delete(k);
}
// PIN vergessen: Name wieder freigeben (nur die Beanspruchung wird gelöscht – Muscheln, Erfolge, Käufe bleiben).
// Danach kann der Spieler seinen Namen neu beanspruchen und eine neue PIN wählen. [Name, Lauf-Nr.] – läuft je Eintrag einmal.
const FREIGEBEN = [["l_i09", 1]];// 20.11.: Verknüpfung von @l_i09 entfernt (Nutzerwunsch)
async function freigeben(store) {
  for (const [n, nr] of FREIGEBEN) {
    const mk = "x/frei/" + n + "/" + nr;
    if (await store.get(mk)) continue;
    await store.set(mk, String(Date.now()));
    await store.delete("c/" + n); await store.delete("x/pinfail/" + n);
  }
}
async function zuruecksetzen(store) {
  for (const [n, nr, ab, opt] of RESET) {
    const mk = "x/reset/" + n + "/" + nr;
    if (await store.get(mk)) continue;
    await store.set(mk, String(Date.now()));
    for (const pre of ["c/" + n, "b/" + n + "/", "q/" + n + "/"])
      for (const k of await liste(store, pre)) if (k === "c/" + n || pre.endsWith("/")) await store.delete(k);
    for (const k of await liste(store, "r/")) {
      const L = JSON.parse((await store.get(k)) || "[]");
      if (Array.isArray(L) && L.includes(n)) await store.set(k, JSON.stringify(L.filter(x => x !== n)));
    }
    const kasse = getStore({ name: "inselkasse", consistency: "strong" });
    if (!(opt && opt.kasse === false)) for (const k of await liste(kasse, "s/" + n + "/")) await kasse.delete(k);
    if (opt && opt.voll) await vollReset(store, n);
    if (ab) {
      // im Test verdiente Erfolge und Story-Buchungen (Zeitstempel im Schlüssel) ebenfalls entfernen
      const es = getStore("erfolge");
      for (const k of await liste(es, "e/" + n + "/")) if (Number(k.split("/").pop()) >= ab) await es.delete(k);
      for (const k of await liste(kasse, "b/" + n + "/")) if (Number(String(k.split("/").pop()).split("-")[0]) >= ab) await kasse.delete(k);
    }
  }
}
// Teil-Zurücksetzen auf einen Zeitpunkt: alles, was ab „ab“ (ms) passiert ist, wird gelöscht (Buchungen, Spenden,
// Erfolge, Story, Aufgabenliste von heute; Beanspruchung nur, wenn sie erst danach erfolgte). Läuft je Eintrag genau einmal.
const HEUTE_9 = 1794556800000; // 13.11.2026 9:00 Uhr (Berlin)
const TEST_14_11_13 = 1794657600000; // 14.11.2026 13:00 Uhr (Berlin): @charlieeee5108 ist Testkonto
const ZURUECK = [["toca_lexi00", 1, HEUTE_9], ["charlieeee5108", 1, TEST_14_11_13]];
async function zurueckAuf(store) {
  for (const [n, nr, ab] of ZURUECK) {
    const mk = "x/zurueck/" + n + "/" + nr;
    if (await store.get(mk)) continue;
    await store.set(mk, String(Date.now()));
    const c = JSON.parse((await store.get("c/" + n)) || "null");
    if (c && Number(c.ts) >= ab) await store.delete("c/" + n);
    for (const k of await liste(store, "b/" + n + "/")) if (Number(await store.get(k)) >= ab) await store.delete(k);
    for (const k of await liste(store, "q/" + n + "/")) if (k.endsWith("/" + tag(ab))) await store.delete(k);
    const kasse = getStore({ name: "inselkasse", consistency: "strong" });
    for (const k of await liste(kasse, "s/" + n + "/")) if (Number(String(k.split("/")[2]).split("-")[0]) >= ab) await kasse.delete(k);
    for (const k of await liste(kasse, "b/" + n + "/")) if (Number(String(k.split("/").pop()).split("-")[0]) >= ab) await kasse.delete(k);
    const es = getStore("erfolge");
    for (const k of await liste(es, "e/" + n + "/")) if (Number(k.split("/").pop()) >= ab) await es.delete(k);
  }
}
// Einmalig (18./19.11.): ALLE Bewohner zurück auf den Stand 18.11.2026 18:00 Uhr (Berlin) – alles, was danach passiert ist
// (Beanspruchungen, Buchungen, Aufgaben, Erfolge, Sticker, Fische, Sandburg, Likes, Anklopfen, Flaschenpost, Einladungen,
// Shop-Käufe samt Ausrüstung, Spenden, Story) wird gelöscht. Echtgeld-Käufe (Stripe) bleiben erhalten.
// 20.11.: nochmal (Lauf 2) – wieder alles nach 18.11. 18:00 bis zur nächsten Veröffentlichung
const ALLE_AB = 1795021200000, ALLE_NR = 2;
let ALLE_OK = false;
// parallel (schneller), höchstens 40 gleichzeitig
async function jeParallel(L, f) { for (let i = 0; i < L.length; i += 40) await Promise.all(L.slice(i, i + 40).map(f)); }
async function allesZurueck(store) {
  if (ALLE_OK) return;
  const mk = "x/zurueck-alle/" + ALLE_NR;
  if (await store.get(mk)) { ALLE_OK = true; return; }
  // Sperre gegen gleichzeitige Läufe; bricht ein Lauf ab (Zeitlimit), macht der nächste Aufruf nach 60 s weiter
  const lk = mk + "-lauf", lv = Number(await store.get(lk)) || 0;
  if (Date.now() - lv < 60000) return;
  await store.set(lk, String(Date.now()));
  // Obergrenze = Zeitpunkt des ersten Laufs (Deploy): was danach passiert, bleibt immer erhalten
  const bk = mk + "-bis"; let BIS = Number(await store.get(bk)) || 0;
  if (!BIS) { BIS = Date.now(); await store.set(bk, String(BIS)); }
  const AB = ALLE_AB, T = tag(AB), TB = tag(BIS), num = v => Number(v) || 0, js = v => { try { return JSON.parse(v); } catch (e) { return null; } };
  const drin = ts => ts >= AB && ts < BIS, datum = k => (k.match(/\d{4}-\d{2}-\d{2}/g) || []).pop() || "";// letztes Datum im Schlüssel (Sandburg: Woche/Name/Tag)
  const klopfWeg = new Set(), weg = [];
  const L = (await liste(store, "")).filter(k => !k.startsWith("x/zurueck-alle/"));
  await jeParallel(L, async k => {
    const t = k.split("/"), d = datum(k);
    if (t[0] === "x" && ["reset", "zurueck", "nullung", "aufraeumen", "start", "euro", "shop", "tierheim", "bereinigt", "einzig", "ausruestung", "gesehen", "strecke", "fstreak", "einlmeld"].includes(t[1])) return;
    if (d && d < T) return;// alles vor dem 18.11. bleibt sicher
    let w = false;
    if (t[0] === "c") { const c = js(await store.get(k)); w = !!c && drin(num(c.ts)); }
    else if (t[0] === "b") w = !["euro", "euro-zurueck", "null"].includes(t[2]) && drin(num(await store.get(k)));
    else if (t[0] === "q" || t[0] === "r") w = d > T && d <= TB;
    else if (t[0] === "live") w = drin(num(await store.get(k)));
    else if (t[0] === "x") {
      const a = t[1];
      if (["klick", "eingeladen", "geschenkt"].includes(a)) { const v = js(await store.get(k)); w = !!v && drin(num(v.ts || v.t)); }
      else if (["fisch", "like", "premium", "sticker", "sand"].includes(a)) w = drin(num(await store.get(k)));
      else if (a === "klopfan") { w = drin(num(t[3].split("-")[0])); if (w) klopfWeg.add(t[3].split("-").slice(1).join("-") + "|" + t[2]); }
      else if (a === "flasche") { const h0 = Date.UTC(2026, 0, 1) + Math.floor(num(t[4]) / 10) * 3.6e6; w = h0 + 3.6e6 > AB && h0 < BIS; }
      else if (a === "codeversuch" || a === "klopft") w = d > T && d <= TB;
      else if (a === "rangcache") w = true;
    }
    if (w) weg.push(k);
  });
  await jeParallel(weg, k => store.delete(k));
  // Anklopfen am 18.11. nach 18 Uhr: Tagesmerker des Klopfenden löschen
  await jeParallel(await liste(store, "x/klopft/"), async k => { const t = k.split("/"); if (t[3] === T && klopfWeg.has(t[2] + "|" + (await store.get(k)))) await store.delete(k); });
  // Einzigartige Items und Ausrüstung: nur was nach dem Zurücksetzen noch im Besitz ist
  const B = {}; for (const k of await liste(store, "b/")) { const [, n, art, id] = k.split("/"); if (art === "kauf") (B[n] = B[n] || new Set()).add(id.slice(11)); }
  await jeParallel(await liste(store, "x/einzig/"), async k => { const n = await store.get(k); if (!(B[n] && B[n].has(k.slice(9)))) await store.delete(k); });
  const alle = {};
  await jeParallel(await liste(store, "a/"), async k => {
    const n = k.slice(2), a = js(await store.get(k)) || {}, neu = {};
    for (const [slot, id] of Object.entries(a)) if (B[n] && B[n].has(id)) neu[slot] = id;
    if (Object.keys(neu).length) { alle[n] = neu; if (Object.keys(neu).length !== Object.keys(a).length) await store.set(k, JSON.stringify(neu)); } else await store.delete(k);
  });
  await store.set("x/ausruestung", JSON.stringify(alle));
  const kasse = getStore({ name: "inselkasse", consistency: "strong" });
  await jeParallel(await liste(kasse, "s/"), async k => { if (drin(num(String(k.split("/")[2]).split("-")[0]))) await kasse.delete(k); });
  await jeParallel(await liste(kasse, "b/"), async k => { if (drin(num(String(k.split("/").pop()).split("-")[0]))) await kasse.delete(k); });
  const es = getStore("erfolge");
  await jeParallel(await liste(es, "e/"), async k => { if (drin(num(k.split("/").pop()))) await es.delete(k); });
  RANGC = { t: 0, d: null };
  await store.set(mk, String(Date.now())); ALLE_OK = true;
}
// Ausgezogene (nicht mehr in der Bewohnerliste): einmal täglich wird ihr Name überall entfernt.
// Persönliches (Beanspruchung, Kontobuch, Aufgaben, Erfolge) wird gelöscht; Spenden und Story-Boni der
// Inselkasse bleiben mit gleichem Betrag erhalten, laufen aber unter einer zufälligen Kennung statt dem Namen.
async function aufraeumen(store) {
  const mk = "x/aufraeumen/" + tag();
  if (await store.get(mk)) return;
  await store.set(mk, String(Date.now()));
  if (!BEWOHNER || BEWOHNER.size < 100) return; // Sicherheitsnetz: nie bei leerer/kaputter Liste
  const weg = n => !!n && !n.startsWith("~") && !BEWOHNER.has(n);
  for (const pre of ["c/", "b/", "q/"])
    for (const k of await liste(store, pre)) { const n = pre === "c/" ? k.slice(2) : k.split("/")[1]; if (weg(n)) await store.delete(k); }
  for (const k of await liste(store, "r/")) {
    const L = JSON.parse((await store.get(k)) || "[]");
    if (Array.isArray(L) && L.some(weg)) await store.set(k, JSON.stringify(L.filter(n => !weg(n))));
  }
  const es = getStore("erfolge");
  for (const k of await liste(es, "e/")) if (weg(k.split("/")[1])) await es.delete(k);
  const kasse = getStore({ name: "inselkasse", consistency: "strong" }), anon = {};
  for (const pre of ["s/", "b/"]) for (const k of await liste(kasse, pre)) {
    const t = k.split("/"), n = t[1];
    if (!weg(n)) continue;
    const id = anon[n] || (anon[n] = "~" + crypto.randomUUID().slice(0, 8));
    t[1] = id; await kasse.set(t.join("/"), (await kasse.get(k)) || "1"); await kasse.delete(k);
  }
}
const TEXT = { login: "Login-Serie", quest: "Aufgabe", qbonus: "Alle 3 Aufgaben", shell: "Schwebende Muschel", erf: "Neuer Erfolg", story: "Story geteilt", spende: "Spende Inselkasse", tresor: "Tresor des Schöpfers", code: "Geheimcode aus dem Video", einladung: "Freund eingeladen", kauf: "Muschel-Shop", null: "Neustart: alle Konten auf 0", stern: "Sternschnuppe 🌠", angeln: "Fang am Angelsteg 🎣", euro: "Muschel-Paket gekauft/geschenkt 💎", "euro-zurueck": "Muschel-Paket erstattet", regenbogen: "Schatz am Regenbogen 🌈", flasche: "Flaschenpost-Quiz 🍾", geschenk: "Tagesgeschenk 🎁" };

// Einmal-Aufgaben (Zurücksetzen, Aufräumen) nur einmal pro Tag und Server-Instanz prüfen – spart bei jeder Muschel-Aktion
// rund 10 Speicherabfragen (schnellere Gutschriften)
let VOR = { tag: "", p: null };
// Alle Konten einmalig auf 0 setzen (16.11.): je Name eine Gegenbuchung „Neustart“ über den aktuellen Kontostand.
// Buchungen bleiben erhalten (Login-Serie, Tresor, Codes, Einladungen, Shop-Inventar zählen weiter nur einmal).
const NULLUNG = "x/nullung/2026-11-16";
async function nullen(store) {
  if (await store.get(NULLUNG)) return;
  await store.set(NULLUNG, String(Date.now()));
  const sum = {};
  for (const k of await liste(store, "b/")) { const [, n, , , a] = k.split("/"); sum[n] = (sum[n] || 0) + (Number(a) || 0); }
  const id = tag() + "-" + Date.now();
  for (const [n, v] of Object.entries(sum)) if (v !== 0) await store.set("b/" + n + "/null/" + id + "/" + (-v), "1");
  RANGC = { t: 0, d: null };
  for (const k of ["x/rangcache", "r/" + tag()]) await store.delete(k);
}
function vorarbeit(store) {
  const t = tag();
  if (VOR.tag !== t) VOR = { tag: t, p: (async () => { await nullen(store); await zuruecksetzen(store); await zurueckAuf(store); await freigeben(store); await aufraeumen(store); })().catch(() => { VOR.tag = ""; }) };
  return VOR.p.then(() => ALLE_OK || allesZurueck(store)).catch(() => {});
}
// Erfolg „Nachbarn“: nur für beanspruchte Namen, die in der Nachbarn-Liste stehen (+10 Muscheln, einmalig)
async function nachbarErf(store, nm) {
  if (!NACHBARN || !NACHBARN.has(nm)) return false;
  const es = getStore("erfolge"), pre = "e/" + nm + "/NACHBAR/";
  if ((await es.list({ prefix: pre })).blobs.length) return false;
  await es.set(pre + Date.now(), "1");
  const bp = "b/" + nm + "/erf/NACHBAR/";
  if (!(await store.list({ prefix: bp })).blobs.length) await store.set(bp + "10", String(Date.now()));
  return true;
}
// Erfolg „Live dabei“: wer im TikTok-LIVE war (Merker live/<name>) und beansprucht ist
async function liveErf(store, nm) { return (await store.get("live/" + nm)) ? await liveVergeben(store, nm) : false; }
// Muschel-Rangliste zwischenspeichern (Server-Speicher + Blob, 45 s): das Durchzählen aller Buchungen dauert,
// die Rangliste soll aber sofort da sein
let RANGC = { t: 0, d: null };
// 🏅 Erfolge-Rangliste: verschiedene Erfolge je beanspruchtem Namen (Server- und Browser-Erfolge, jeder einmal), 60 s zwischengespeichert
let ERFC = { t: 0, d: null };
async function erfDaten(store) {
  if (ERFC.d && Date.now() - ERFC.t < 60000) return ERFC.d;
  const claimed = new Set((await liste(store, "c/")).map(k => k.slice(2))), E = {};
  for (const k of await liste(store, "b/")) { const [, n, art, id] = k.split("/"); if (art === "erf" && claimed.has(n)) (E[n] = E[n] || new Set()).add(id); }
  for (const k of await liste(getStore("erfolge"), "e/")) { const [, n, K] = k.split("/"); if (claimed.has(n)) (E[n] = E[n] || new Set()).add(K); }
  const order = Object.entries(E).map(([n, s]) => [n, s.size]).filter(x => x[1] > 0).sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1));
  ERFC = { t: Date.now(), d: order }; return order;
}
async function rangDaten(store) {
  const jetzt = Date.now();
  if (RANGC.d && jetzt - RANGC.t < 45000) return RANGC.d;
  try { const c = JSON.parse((await store.get("x/rangcache")) || "null"); if (c && jetzt - c.t < 45000) { RANGC = { t: c.t, d: c.d }; return c.d; } } catch (e) {}
  const claimed = new Set((await liste(store, "c/")).map(k => k.slice(2)).filter(n => BEWOHNER.has(n)));// Ausgezogene nicht mehr anzeigen
  // Rangliste zählt nur erspielte Muscheln: Kontostand minus die noch nicht ausgegebenen gekauften Muscheln
  // (gekaufte gelten als zuerst ausgegeben – wer gekaufte Muscheln im Shop ausgibt, verliert keine erspielten)
  const sum = {}, kauf = {}, aus = {};
  for (const k of await liste(store, "b/")) { const [, n, art, , a0] = k.split("/"); if (!claimed.has(n)) continue; const a = Number(a0) || 0;
    sum[n] = (sum[n] || 0) + a;
    if (art === "euro" || art === "euro-zurueck") kauf[n] = (kauf[n] || 0) + a; else if (a < 0 && (art === "kauf" || art === "spende")) aus[n] = (aus[n] || 0) - a; }
  for (const n in kauf) sum[n] -= Math.max(0, kauf[n] - (aus[n] || 0));
  const order = Object.entries(sum).filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1));
  const heute = tag(), key = "r/" + heute;
  const [hat, vorRoh] = await Promise.all([store.get(key), store.get("r/" + gestern(heute))]);
  if (!hat) await store.set(key, JSON.stringify(order.slice(0, 50).map(x => x[0])));
  const d = { order, vor: JSON.parse(vorRoh || "null"), beansprucht: claimed.size };
  RANGC = { t: jetzt, d };
  await store.set("x/rangcache", JSON.stringify({ t: jetzt, d }));
  return d;
}
// Freunde einladen: Klick auf den Einladungslink wird mit Zeitpunkt beim Server vermerkt (Token). Beim Beanspruchen zählt
// die Einladung nur, wenn der Neue erst NACH dem Klick eingezogen ist, nicht sich selbst einlädt und noch nie gezählt wurde.
// Belohnung: +10 Muscheln für den Einladenden, ab 3 Einladungen Erfolg „Inselbotschafter“ (+10).
const berlinTag = ms => new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Berlin" }).format(new Date(ms));
async function einladungPruefen(store, nm, kt) {
  if (!kt || !/^[0-9a-f-]{36}$/.test(kt)) return null;
  const k = JSON.parse((await store.get("x/klick/" + kt)) || "null");
  if (!k || !k.von || k.von === nm || !BEWOHNER.has(k.von)) return null;
  if (!SEIT || !SEIT[nm] || SEIT[nm] < berlinTag(k.ts)) return null;// war schon vor dem Klick Bewohner
  if (await store.get("x/eingeladen/" + nm)) return null;
  await store.set("x/eingeladen/" + nm, JSON.stringify({ von: k.von, ts: Date.now() }));
  await store.set("b/" + k.von + "/einladung/" + nm + "/10", String(Date.now()));
  const anzahl = (await store.list({ prefix: "b/" + k.von + "/einladung/" })).blobs.length;
  if (anzahl >= 3) {
    const es = getStore("erfolge"), pre = "e/" + k.von + "/BOTSCHAFTER/";
    if (!(await es.list({ prefix: pre })).blobs.length) { await es.set(pre + Date.now(), "1"); await store.set("b/" + k.von + "/erf/BOTSCHAFTER/10", String(Date.now())); }
  }
  return k.von;
}
// ---------- Muschel-Shop ----------
// Tagesangebot: je Kategorie 2 Items, Seltenheit nach Gewicht (Stufe zuerst, dann Item), für alle gleich, neu um 0:00 Uhr (Berlin).
// Einmal am Tag erzeugt und gespeichert (x/shop/<tag>); „Einzigartig“-Items gibt es nur ein einziges Mal (x/einzig/<id>).
function zufall(seed) { let h = 2166136261; for (const ch of seed) h = Math.imul(h ^ ch.charCodeAt(0), 16777619); return () => { h += 0x6D2B79F5; let t = h; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
// 🐾 Tierheim-Shop (Tierheim eröffnet 17.11.); täglich um 0:00 neu, je Tierart 2 Tiere (Stufe nach Gewicht, „Einzigartig“ nie)
const TIERHEIM_AB = 800;
const tierheimOffen = () => true;// eröffnet am 17.11.2026
async function tierAngebot(store, heute) {
  const k = "x/tierheim/" + heute, alt = await store.get(k); if (alt) return JSON.parse(alt);
  const r = zufall("tierheim-" + heute), ids = [], arten = [...new Set(Object.keys(SHOP.items).filter(id => SHOP.items[id][0] === "tier").map(id => id.split("_")[1]))];
  for (const art of arten) {
    let pool = Object.entries(SHOP.items).filter(([id, v]) => v[0] === "tier" && id.split("_")[1] === art && v[2] < 10);
    for (let n = 0; n < 2 && pool.length; n++) {
      const st = [...new Set(pool.map(([, v]) => v[2]))], sum = st.reduce((s, x) => s + SHOP.stufen[x - 1], 0);
      let z = r() * sum, w = st[st.length - 1]; for (const x of st) { z -= SHOP.stufen[x - 1]; if (z < 0) { w = x; break; } }
      const kand = pool.filter(([, v]) => v[2] === w), pick = kand[Math.floor(r() * kand.length)][0];
      ids.push(pick); pool = pool.filter(([id]) => id !== pick);
    }
  }
  await store.set(k, JSON.stringify(ids)); return ids;
}
async function angebot(store, heute) {
  const k = "x/shop/" + heute, alt = await store.get(k);
  if (alt) { const L = JSON.parse(alt); if (!L.some(id => SHOP.items[id] && SHOP.items[id][2] === 10)) return L; }// „Einzigartig“ nie im Shop (17.11.)
  const weg = new Set((await liste(store, "x/einzig/")).map(x => x.slice(9))), r = zufall("muschelshop-" + heute), ids = [];
  for (const kat of SHOP.kat) {
    let pool = Object.entries(SHOP.items).filter(([id, v]) => v[0] === kat && v[2] < 10 && !weg.has(id));
    for (let n = 0; n < 2 && pool.length; n++) {
      const st = [...new Set(pool.map(([, v]) => v[2]))], sum = st.reduce((s, x) => s + SHOP.stufen[x - 1], 0);
      let z = r() * sum, w = st[st.length - 1]; for (const x of st) { z -= SHOP.stufen[x - 1]; if (z < 0) { w = x; break; } }
      const kand = pool.filter(([, v]) => v[2] === w), pick = kand[Math.floor(r() * kand.length)][0];
      ids.push(pick); const rest = pool.filter(([id, v]) => v[1] !== SHOP.items[pick][1]);// zweites Item möglichst aus einem anderen Bereich
      pool = rest.length ? rest : pool.filter(([id]) => id !== pick);
    }
  }
  await store.set(k, JSON.stringify(ids));
  return ids;
}
const besitz = (B) => [...new Set(B.filter(e => e.art === "kauf").map(e => e.id.slice(11)))];
async function ausruestungAlle(store) { return JSON.parse((await store.get("x/ausruestung")) || "{}"); }
const bisMitternacht = () => { const n = Date.now(), h = new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23" }).format(new Date(n)).split(":").map(Number); return 86400000 - ((h[0] * 60 + h[1]) * 60 + h[2]) * 1000; };

export default async (req) => {
  const store = getStore({ name: "muscheln", consistency: "strong" });
  await vorarbeit(store);
  const url = new URL(req.url);
  if (req.method === "GET" && url.searchParams.get("erftop")) {
    const order = await erfDaten(store), me = (url.searchParams.get("name") || "").trim().toLowerCase().replace(/^@/, "");
    const top = order.slice(0, 10).map(([n, v]) => ({ n: "@" + n, stand: v }));
    let platz = null, stand = null; if (me) { const i = order.findIndex(x => x[0] === me); if (i >= 0) { platz = i + 1; stand = order[i][1]; } }
    return json({ top, platz, stand, bis10: platz && platz > 10 && top[9] ? top[9].stand - stand + 1 : null, anzahl: order.length });
  }
  if (req.method === "GET" && url.searchParams.get("top")) {
    // Muschel-Rangliste: Top 10 der beanspruchten Namen nach Kontostand, Pfeile im Vergleich zu gestern, optional eigener Platz
    const { order, vor, beansprucht } = await rangDaten(store);
    const top = order.slice(0, 10).map(([n, v], i) => { const j = vor ? vor.indexOf(n) : -1; return { n: "@" + n, stand: v, d: vor ? (j < 0 ? "neu" : j - i) : null }; });
    const me = (url.searchParams.get("name") || "").trim().toLowerCase().replace(/^@/, "");
    let platz = null, stand = null;
    if (me) { const i = order.findIndex(x => x[0] === me); if (i >= 0) { platz = i + 1; stand = order[i][1]; } }
    const bis10 = platz && platz > 10 && top[9] ? top[9].stand - stand + 1 : null;
    return json({ top, platz, stand, bis10, anzahl: order.length, beansprucht: beansprucht ?? null, einwohner: BEWOHNER.size });
  }
  if (req.method === "GET" && url.searchParams.get("shop")) {
    const ids = await angebot(store, tag());
    const weg = []; for (const id of ids) if (SHOP.items[id][2] === 10 && await store.get("x/einzig/" + id)) weg.push(id);
    return json({ tag: tag(), ids, weg, bis: bisMitternacht() });
  }
  // öffentlich: nur die Anzahl der Likes eines Passes (für Besucher ohne beanspruchten Namen)
  if (req.method === "GET" && url.searchParams.get("likes")) {
    const an = String(url.searchParams.get("likes")).toLowerCase().replace(/^@/, "");
    if (!BEWOHNER.has(an) && an !== "echter.alex") return json({ n: 0 });
    return json({ n: (await liste(store, "x/like/" + an + "/")).length });
  }
  if (req.method === "GET" && url.searchParams.get("sand")) {
    const wo = woche(tag());
    return json({ woche: wo, n: (await liste(store, "x/sand/" + wo + "/")).length, flut: flutJetzt() });
  }
  if (req.method === "GET" && url.searchParams.get("tierheim")) {
    const offen = tierheimOffen();
    return json({ tag: tag(), offen, ids: offen ? await tierAngebot(store, tag()) : [], weg: [], bis: bisMitternacht(), ab: TIERHEIM_AB });
  }
  if (req.method === "GET" && url.searchParams.get("aus")) return new Response(JSON.stringify(await ausruestungAlle(store)), { headers: { "content-type": "application/json", "cache-control": "public, max-age=30" } });
  if (req.method === "GET" && url.searchParams.get("einladungen")) {
    // Liste der angerechneten Einladungen (für die Nachbarschaft beim nächsten Listen-Update)
    const L = [];
    for (const k of await liste(store, "x/eingeladen/")) { const v = JSON.parse((await store.get(k)) || "{}"); L.push([v.von, k.slice(13), v.ts]); }
    return json({ einladungen: L });
  }
  if (req.method === "GET") {
    // öffentlich: nur, ob ein Name beansprucht ist (für den Hinweis im Muschelpass)
    const n = (url.searchParams.get("name") || "").trim().toLowerCase();
    if (!NAME.test(n)) return json({ fehler: "Name" }, 400);
    return json({ beansprucht: !!(await store.get("c/" + n.slice(1))) });
  }
  if (req.method !== "POST") return json({ fehler: "Methode" }, 405);
  let d = {};
  try { d = await req.json(); } catch (e) {}
  const name = String(d.name || "").trim().toLowerCase(), act = String(d.act || "");
  if (act === "klick") {
    // Einladungslink geöffnet: Werber + Zeitpunkt merken (ohne Anmeldung)
    const von = String(d.von || "").trim().toLowerCase().replace(/^@/, "");
    if (!/^[a-z0-9._]{1,40}$/.test(von) || !BEWOHNER.has(von)) return json({ ok: false });
    const kt = crypto.randomUUID();
    await store.set("x/klick/" + kt, JSON.stringify({ von, ts: Date.now() }));
    return json({ ok: true, kt });
  }
  if (act === "wer") {
    const m = (req.headers.get("cookie") || "").match(/(?:^|;\s*)mt-k=([^;]+)/);
    const [n, t] = m ? decodeURIComponent(m[1]).split("|") : [];
    if (!n || !t) return json({ ok: false });
    const c = JSON.parse((await store.get("c/" + n)) || "null");
    if (!tokOk(c, await sha(t))) return json({ ok: false });
    return mitCookie(json({ ok: true, n: "@" + n, t }), n, t);
  }
  if (act === "pinLogin") {
    // 🔑 Anmelden mit Name + Muschel-PIN (in jedem Browser); nach 5 falschen Versuchen 1 Stunde gesperrt
    const n = String(d.name || "").trim().toLowerCase().replace(/^@/, ""), pin = String(d.pin || "");
    if (!/^[a-z0-9._]{1,40}$/.test(n) || !/^\d{4}$/.test(pin)) return json({ ok: false, grund: "eingabe" });
    const c = JSON.parse((await store.get("c/" + n)) || "null");
    if (!c) return json({ ok: false, grund: "frei" });
    if (!c.pin) return json({ ok: false, grund: "keinepin" });
    const fk = "x/pinfail/" + n, F = JSON.parse((await store.get(fk)) || '{"n":0,"t":0}'), jetzt = Date.now();
    if (F.n >= 5 && jetzt - F.t < 3600e3) return json({ ok: false, grund: "gesperrt", min: Math.ceil((3600e3 - (jetzt - F.t)) / 60000) });
    if (c.pin !== (await sha(n + "|" + pin))) { const nn = (jetzt - F.t < 3600e3 ? F.n : 0) + 1; await store.set(fk, JSON.stringify({ n: nn, t: jetzt })); return json({ ok: false, grund: nn >= 5 ? "gesperrt" : "falsch", rest: Math.max(0, 5 - nn), min: 60 }); }
    if (F.n) await store.delete(fk);
    const t = crypto.randomUUID() + "-" + crypto.randomUUID();
    c.hs = [...(Array.isArray(c.hs) ? c.hs : []), await sha(t)].slice(-5);
    await store.set("c/" + n, JSON.stringify(c));
    return mitCookie(json({ ok: true, n: "@" + n, t }), n, t);
  }
  if (!NAME.test(name)) return json({ fehler: "Name" }, 400);
  const nm = name.slice(1), heute = tag();

  if (act === "claim") {
    if (nm === "echter.alex") return json({ ok: false, beansprucht: true });// Schöpfer: nicht beanspruchbar
    if (await store.get("c/" + nm)) return json({ ok: false, beansprucht: true });
    const pin = String(d.pin || "");
    if (!/^\d{4}$/.test(pin)) return json({ ok: false, grund: "pin" });// Muschel-PIN (4 Ziffern) ist Pflicht
    const token = crypto.randomUUID() + "-" + crypto.randomUUID();
    await store.set("c/" + nm, JSON.stringify({ h: await sha(token), ts: Date.now(), pin: await sha(nm + "|" + pin) }));
    // bei gleichzeitigem Beanspruchen gewinnt, wessen Eintrag gespeichert blieb
    await new Promise(r => setTimeout(r, 300));
    const c = JSON.parse((await store.get("c/" + nm)) || "{}");
    if (c.h !== (await sha(token))) return json({ ok: false, beansprucht: true });
    const nachbar = await nachbarErf(store, nm), live = await liveErf(store, nm);
    const von = await einladungPruefen(store, nm, String(d.kt || ""));
    return mitCookie(json({ ok: true, token, von, neu: [...(nachbar ? ["NACHBAR"] : []), ...(live ? ["LIVE"] : [])] }), nm, token);
  }
  // alle weiteren Aktionen nur mit dem Schlüssel des Besitzers
  const c = JSON.parse((await store.get("c/" + nm)) || "null");
  if (!tokOk(c, await sha(String(d.token || "")))) return json({ fehler: "Nicht beansprucht" }, 403);
  if (act === "pinSetzen") {
    // Muschel-PIN nachträglich festlegen (für alle, die vor der PIN beansprucht haben) oder ändern
    const pin = String(d.pin || ""); if (!/^\d{4}$/.test(pin)) return json({ ok: false, grund: "pin" });
    c.pin = await sha(nm + "|" + pin); await store.set("c/" + nm, JSON.stringify(c)); return json({ ok: true });
  }

  const setze = async (art, id, a) => {
    const pre = "b/" + nm + "/" + art + "/" + id + "/";
    if ((await store.list({ prefix: pre })).blobs.length) return false;
    await store.set(pre + a, String(Date.now()));
    return true;
  };
  // vom Server vergebener Erfolg (nur einmal; +10 Muscheln; auch in der Erfolgsliste für alle sichtbar)
  const erfGib = async (k) => {
    const es = getStore("erfolge"), pre = "e/" + nm + "/" + k + "/";
    if ((await es.list({ prefix: pre })).blobs.length) return false;
    await es.set(pre + Date.now(), "1"); await setze("erf", k, 10); return true;
  };
  const berlinStunde = () => Number(new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hour: "2-digit", hourCycle: "h23" }).format(new Date()));
  const J = job(nm);

  // heutiger Login-Bonus: Serien-Tag aus dem gestrigen Eintrag (sonst Tag 1)
  const serie = async (B) => {
    const L = B.filter(e => e.art === "login");
    const h = L.find(e => e.id.startsWith(heute)), g = L.find(e => e.id.startsWith(gestern(heute)));
    const gTag = g ? Number(g.id.split("_")[1]) || 1 : 0;
    const t = h ? Number(h.id.split("_")[1]) || 1 : (gTag ? gTag % 7 + 1 : 1);
    // Treue-Bonus: +1 Muschel je volle Woche ohne Unterbrechung (bis gestern), höchstens +5 – damit nach Tag 7 nicht alles von vorn beginnt
    const tage = new Set(L.map(e => e.id.slice(0, 10)));
    let lauf = 0, d0 = gestern(heute); while (tage.has(d0) && lauf < 60) { lauf++; d0 = gestern(d0); }
    const treue = Math.min(5, Math.floor(lauf / 7));
    return { tag: t, abgeholt: !!h, betrag: SERIE[t - 1], treue, job: J };
  };

  if (act === "login") {
    const B = await buch(store, nm), s = await serie(B);
    if (s.abgeholt) return json({ ok: false, schon: true });
    const sum = s.betrag + s.treue + (J ? J.z : 0);
    const ok = await setze("login", heute + "_" + s.tag, sum);
    // Geheime Erfolge beim Login: 7/30/100 Tage am Stück, Heiligabend, Silvester (je +10 Muscheln, nur einmal)
    const neu = [];
    if (ok) {
      const tage = new Set((await buch(store, nm)).filter(e => e.art === "login").map(e => e.id.slice(0, 10)));
      let lauf = 0, d0 = heute;
      while (tage.has(d0) && lauf < 400) { lauf++; d0 = gestern(d0); }
      const md = heute.slice(5), K = [];
      if (lauf >= 7) K.push("TAG7");
      if (lauf >= 30) K.push("TAG30");
      if (lauf >= 100) K.push("TAG100");
      if (md === "12-24") K.push("HEILIG");
      if (md === "12-31") K.push("SILVESTER");
      const es = getStore("erfolge");
      for (const k of K) {
        const pre = "e/" + nm + "/" + k + "/";
        if ((await es.list({ prefix: pre })).blobs.length) continue;
        await es.set(pre + Date.now(), "1");
        await setze("erf", k, 10);
        neu.push(k);
      }
    }
    if (await nachbarErf(store, nm)) neu.push("NACHBAR");
    if (await liveErf(store, nm)) neu.push("LIVE");
    return json({ ok, tag: s.tag, betrag: s.betrag, treue: s.treue, job: J, summe: sum, neu });
  }
  if (act === "quests") {
    // Aufgaben des Tages: Wer gestern keine erledigt hat, behält die alten; sonst gelten die neu vorgeschlagenen
    let q = JSON.parse((await store.get("q/" + nm + "/" + heute)) || "null");
    if (!q) {
      const alt = JSON.parse((await store.get("q/" + nm + "/" + gestern(heute))) || "null");
      const B = await buch(store, nm), gDone = B.some(e => e.art === "quest" && e.id.startsWith(gestern(heute)));
      q = alt && !gDone ? alt : (Array.isArray(d.vorschlag) ? d.vorschlag.slice(0, 3).map(x => String(x).slice(0, 80)) : []);
      if (q.length) await store.set("q/" + nm + "/" + heute, JSON.stringify(q));
    }
    return json({ ok: true, quests: q });
  }
  if (act === "quest") {
    const i = Number(d.i);
    const q = JSON.parse((await store.get("q/" + nm + "/" + heute)) || "[]");
    if (!(i >= 0 && i < q.length)) return json({ fehler: "Aufgabe" }, 400);
    const ok = await setze("quest", heute + "-" + i, 5);
    let bonus = false;
    const B = await buch(store, nm);
    if (B.filter(e => e.art === "quest" && e.id.startsWith(heute)).length >= q.length && q.length === 3) bonus = await setze("qbonus", heute, 5);
    // Erfolge für erledigte Aufgaben insgesamt: 10, 100, 500 (je +10 Muscheln, nur einmal)
    const neu = [], anz = B.filter(e => e.art === "quest").length, es = getStore("erfolge");
    for (const [n, k] of [[10, "AUFG10"], [100, "AUFG100"], [500, "AUFG500"]]) {
      if (anz < n) continue;
      const pre = "e/" + nm + "/" + k + "/";
      if ((await es.list({ prefix: pre })).blobs.length) continue;
      await es.set(pre + Date.now(), "1"); await setze("erf", k, 10); neu.push(k);
    }
    return json({ ok, bonus, neu, anz });
  }
  if (act === "shell") {
    // 20.11.: 10 schwebende Muscheln pro Stunde und Insel (je 1 🐚), pro Spieler höchstens 10 pro Stunde über alle Inseln.
    // Kennung „Stunde-Insel-Nr.“, gilt nur in der aktuellen (oder gerade vergangenen) Stunde
    const m = /^(\d{1,2})-(\d)-(\d)$/.exec(String(d.i || "")), h = berlinStunde();
    if (!m || !(Number(m[1]) === h || Number(m[1]) === h - 1)) return json({ fehler: "Muschel" }, 400);
    const hh = String(m[1]).padStart(2, "0");
    if ((await liste(store, "b/" + nm + "/shell/" + heute + "-" + hh + "-")).length >= 10) return json({ ok: false, grund: "limit" });
    return json({ ok: await setze("shell", heute + "-" + hh + "-" + m[2] + "-" + m[3], 1) });
  }
  if (act === "erf") {
    const k = String(d.key || "").toUpperCase();
    // nur Erfolge, die im Browser vergeben werden (alle anderen bucht der Server selbst) – sonst ließen sich mit erfundenen Namen Muscheln erzeugen
    if (!ERF_CLIENT.has(k)) return json({ fehler: "Erfolg" }, 400);
    if (k === "NACHT" && berlinStunde() !== 3) return json({ ok: false, grund: "zeit" });// Nachteule nur zwischen 3 und 4 Uhr
    return json({ ok: await setze("erf", k, k === "WELT" ? 30 : 10) });// Weltenbummler (alle Sticker) = 30
  }
  // Tresor des Schöpfers (Schlossinsel): einmalige Verlosung je Name – 3, 5, 7 oder 10 Muscheln (je 25 %)
  // Geheimcode aus einem TikTok-Video: gilt nur an den angegebenen Tagen, je Name einmal; höchstens 10 Versuche pro Tag
  if (act === "code") {
    const k = String(d.code || "").toUpperCase().replace(/[^A-Z0-9ÄÖÜ]/g, "").slice(0, 30);
    const vk = "x/codeversuch/" + nm + "/" + heute, vers = Number(await store.get(vk)) || 0;
    if (vers >= 10) return json({ ok: false, grund: "versuche" });
    const c = CODES.find(c => c.code === k && heute >= c.von && heute <= c.bis);
    if (!c) { await store.set(vk, String(vers + 1)); return json({ ok: false, grund: "falsch" }); }
    const betrag = 10;// Geheimcode aus dem Video: immer 10 Muscheln
    const ok = await setze("code", k, betrag);
    return json({ ok, grund: ok ? null : "schon", betrag });
  }
  if (act === "tresor") {
    const pre = "b/" + nm + "/tresor/einmal/";
    const L = (await store.list({ prefix: pre })).blobs;
    if (L.length) return json({ ok: false, betrag: Number(L[0].key.slice(pre.length)) || 0 });
    const betrag = [3, 5, 7, 10][crypto.getRandomValues(new Uint32Array(1))[0] % 4];
    await store.set(pre + betrag, String(Date.now()));
    return json({ ok: true, betrag });
  }
  // Sternschnuppe (nur nachts, 19–6 Uhr Berlin): Rubbellos mit 1–3 Muscheln, höchstens 2× pro Nacht
  if (act === "stern") {
    const h = Number(new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hour: "2-digit", hourCycle: "h23" }).format(new Date()));
    if (!(h >= 19 || h < 6)) return json({ ok: false, grund: "tag" });
    const nacht = h < 6 ? gestern(heute) : heute, pre = "b/" + nm + "/stern/" + nacht + "-";
    const schon = (await liste(store, pre)).length;
    if (schon >= 2) return json({ ok: false, grund: "genug" });
    const id = String(Number(d.id) || 0).slice(0, 12), betrag = 1 + (crypto.getRandomValues(new Uint32Array(1))[0] % 3);
    if (!(await setze("stern", nacht + "-" + id, betrag))) return json({ ok: false, grund: "genug" });
    return json({ ok: true, betrag, rest: 1 - schon });
  }
  // Regenbogen: Schatztruhe mit 5 Muscheln, einmalig pro Regen-Ende. Kennung = letzte Regenstunde; der Server prüft sie selbst beim Wetterdienst.
  if (act === "regenbogen") {
    const id = String(d.id || "");
    if (!(await regenEnde(id))) return json({ ok: false, grund: "kein" });
    const ok = await setze("regenbogen", id.replace(/[^0-9T]/g, ""), 5), B = await buch(store, nm);
    return json({ ok, grund: ok ? null : "schon", stand: B.reduce((s, e) => s + e.a, 0) });
  }
  // 🍾 Flaschenpost: Quizfrage zu Muschel-Tal. Flasche = Stunde*10+Nr (nur aktuelle/letzte Stunde), höchstens 3 pro Tag, je Flasche 1 Versuch, richtig = +2
  if (act === "flasche" || act === "flascheAntwort") {
    const fl = Math.floor(Number(d.fl)), hJetzt = Math.floor((Date.now() - Date.UTC(2026, 0, 1)) / 3.6e6);
    if (!(fl >= 0) || !(fl % 10 < 2) || Math.floor(fl / 10) < hJetzt - 1 || Math.floor(fl / 10) > hJetzt) return json({ ok: false, grund: "weg" });
    const f = quizFrage(nm, fl), xk = "x/flasche/" + nm + "/" + heute + "/" + fl;
    if (await store.get(xk)) return json({ ok: false, grund: "schon" });
    if ((await liste(store, "x/flasche/" + nm + "/" + heute + "/")).length >= 3) return json({ ok: false, grund: "genug" });
    if (act === "flasche") return json({ ok: true, q: f.q, a: f.a });
    const w = Math.floor(Number(d.wahl)); await store.set(xk, String(w));
    const richtig = w === f.r; if (richtig) await setze("flasche", heute + "-" + fl, 2);
    const sk = "x/fstreak/" + nm, serie = richtig ? (Number(await store.get(sk)) || 0) + 1 : 0; await store.set(sk, String(serie));
    const neuF = serie >= 10 && (await erfGib("KLUG")) ? ["KLUG"] : [];
    const B = await buch(store, nm);
    return json({ ok: true, richtig, loesung: f.a[f.r], neu: neuF, stand: B.reduce((s, e) => s + e.a, 0) });
  }
  // 🎁 Tagesgeschenk vor der eigenen Hütte: 1–3 Muscheln, 1× pro Tag
  // 🏰 Sandburg: 1× pro Tag mitbauen (gemeinsamer Fortschritt der Woche)
  if (act === "sandburg") {
    if (flutJetzt()) return json({ ok: false, grund: "flut" });
    const wo = woche(heute), k = "x/sand/" + wo + "/" + nm + "/" + heute;
    if (await store.get(k)) return json({ ok: false, grund: "schon", n: (await liste(store, "x/sand/" + wo + "/")).length });
    await store.set(k, String(Date.now()));// keine Muscheln – nur gemeinsamer Fortschritt
    return json({ ok: true, n: (await liste(store, "x/sand/" + wo + "/")).length });
  }
  // 🎣 Angeln: 1 Fang pro Tag (der Server bestimmt den Fisch); jeder Fisch kommt ins Fisch-Album
  if (act === "angeln") {
    const insel = Number(d.insel) === 1 ? 1 : 0, tagId = heute + "-" + insel + "_";
    const B0 = await buch(store, nm);
    if (B0.some(e => e.art === "angeln" && e.id.startsWith(tagId))) return json({ ok: false, grund: "schon" });
    const f = await fischZiehen(insel), betrag = zz() < 0.15 ? 1 + Math.floor(zz() * 3) : 0, ok = await setze("angeln", tagId + f, betrag);
    if (ok) await store.set("x/fisch/" + nm + "/" + f, String(Date.now()));
    const B = await buch(store, nm);
    return json({ ok, grund: ok ? null : "schon", fisch: ok ? f : null, betrag: ok ? betrag : 0, stand: B.reduce((s, e) => s + e.a, 0), fische: (await liste(store, "x/fisch/" + nm + "/")).map(k => k.split("/")[3]) });
  }
  if (act === "geschenk") {
    const betrag = 1 + (crypto.getRandomValues(new Uint32Array(1))[0] % 3), ok = await setze("geschenk", heute, betrag), B = await buch(store, nm);
    return json({ ok, grund: ok ? null : "schon", betrag: ok ? betrag : 0, stand: B.reduce((s, e) => s + e.a, 0) });
  }
  // 👋 Anklopfen: 1× pro Tag bei einer fremden Hütte; der Bewohner sieht es beim nächsten Besuch
  // ❤️ Muschelpass liken: einmal je Pass (nochmal tippen = Like zurücknehmen); nie den eigenen
  if (act === "like" || act === "likeinfo") {
    const an = String(d.an || "").toLowerCase().replace(/^@/, "");
    if ((!BEWOHNER.has(an) && an !== "echter.alex") || an === nm) return json({ ok: false, grund: "wer" });// auch der Pass des Schöpfers kann geliked werden
    const k = "x/like/" + an + "/" + nm; let hab = !!(await store.get(k));
    if (act === "like") { if (hab) await store.delete(k); else await store.set(k, String(Date.now())); hab = !hab; }
    return json({ ok: true, hab, n: (await liste(store, "x/like/" + an + "/")).length });
  }
  if (act === "klopf") {
    const an = String(d.an || "").toLowerCase().replace(/^@/, "");
    if (!BEWOHNER.has(an) || an === nm) return json({ ok: false, grund: "wer" });
    const k = "x/klopft/" + nm + "/" + heute;
    if (await store.get(k)) return json({ ok: false, grund: "heute" });
    await store.set(k, an); await store.set("x/klopfan/" + an + "/" + Date.now() + "-" + nm, "1");
    const verschieden = new Set(); for (const kk of await liste(store, "x/klopft/" + nm + "/")) verschieden.add(await store.get(kk));
    return json({ ok: true, neu: verschieden.size >= 20 && (await erfGib("KLOPF")) ? ["KLOPF"] : [] });
  }
  // 💎 Premium-Shop einmal entsperrt → für immer offen
  if (act === "premium") { await store.set("x/premium/" + nm, String(Date.now())); return json({ ok: true }); }
  // 🔍 Detektiv: Muschelpässe von 50 verschiedenen Bewohnern angesehen
  if (act === "gesehen") {
    const an = String(d.an || "").toLowerCase().replace(/^@/, "");
    if (!BEWOHNER.has(an) || an === nm) return json({ ok: false });
    await store.set("x/gesehen/" + nm + "/" + an, "1");
    const n = (await liste(store, "x/gesehen/" + nm + "/")).length;
    return json({ ok: true, n, neu: n >= 50 && (await erfGib("DETEKTIV")) ? ["DETEKTIV"] : [] });
  }
  // 🏃 Marathon: Strecke beim Erkunden (Meter); höchstens so viel, wie man seit der letzten Meldung schaffen kann (8 m/s)
  if (act === "strecke") {
    const sk = "x/strecke/" + nm, alt = JSON.parse((await store.get(sk)) || '{"m":0,"t":0}'), jetzt = Date.now();
    const dtS = Math.min(120, (jetzt - (alt.t || 0)) / 1000), m = Math.max(0, Math.min(Number(d.m) || 0, dtS * 8));
    if (dtS < 15) return json({ ok: false, m: alt.m });
    const neuM = alt.m + m; await store.set(sk, JSON.stringify({ m: neuM, t: jetzt }));
    return json({ ok: true, m: Math.round(neuM), neu: neuM >= 42195 && (await erfGib("MARATHON")) ? ["MARATHON"] : [] });
  }
  // 🧩 Sticker-Album: Ort besucht → Sticker (je Ort einmal)
  if (act === "sticker") {
    const id = String(d.id || ""); if (!STICKER.has(id)) return json({ ok: false });
    if (id.startsWith("ev_")) {// Event-Sticker nur während des Events (Berliner Zeit)
      const p = Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: TZ, weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date()).map(x => [x.type, x.value]));
      const h = +p.hour + p.minute / 60, wd = p.weekday;
      const aktiv = { wochenmarkt: wd === "Wed" && h >= 6 && h < 12, flohmarkt: wd === "Sat" && h >= 10 && h < 18, konzert: wd === "Sun" && h >= 16 && h < 19, feuerwerk: wd === "Fri" && h >= 20 && h < 20.25, kino: (wd === "Fri" || wd === "Sat") && h >= 20 && h < 22 };
      if (process.env.EV_TEST !== "1" && !aktiv[id.slice(3)]) return json({ ok: false, grund: "zeit" });
    }
    await store.set("x/sticker/" + nm + "/" + id, String(Date.now()));
    return json({ ok: true, sticker: (await liste(store, "x/sticker/" + nm + "/")).map(k => k.split("/")[3]) });
  }
  if (act === "story") { // 20.11.: Muschelpass teilen = 1× pro Woche +10 🐚 aufs Konto und +10 🐚 in die Inselkasse
    const w = woche(heute), ok = await setze("story", w, 10);
    if (ok) await getStore({ name: "inselkasse", consistency: "strong" }).set("s/" + nm + "/" + Date.now() + "-story/10", "1");
    return json({ ok, kasse: ok ? 10 : 0 });
  }
  if (act === "spende") {
    const a = Math.floor(Number(d.betrag));
    const B = await buch(store, nm), stand = B.reduce((s, e) => s + e.a, 0);
    if (!(a >= 1) || a > stand) return json({ ok: false, fehler: "Betrag", stand });
    const id = Date.now() + "-" + Math.random().toString(36).slice(2, 8);
    await store.set("b/" + nm + "/spende/" + id + "/" + (-a), String(Date.now()));
    await getStore({ name: "inselkasse", consistency: "strong" }).set("s/" + nm + "/" + id + "/" + a, "1");
    // Erfolg „Inselfreund“ ab insgesamt 100 gespendeten Muscheln
    const gesp = -B.filter(e => e.art === "spende").reduce((s, e) => s + e.a, 0) + a;
    let freund = false;
    if (gesp >= 100) {
      const es = getStore("erfolge"), pre = "e/" + nm + "/FREUND/";
      if (!(await es.list({ prefix: pre })).blobs.length) { await es.set(pre + Date.now(), "1"); freund = true; await setze("erf", "FREUND", 10); }
    }
    return json({ ok: true, stand: stand - a + (freund ? 10 : 0), gespendet: gesp, freund });
  }
  if (act === "kauf") {
    const id = String(d.id || ""), it = SHOP.items[id];
    if (!it) return json({ ok: false, grund: "item" });
    if (it[0] === "tier" && !tierheimOffen()) return json({ ok: false, grund: "angebot" });// Tiere nur im Tierheim
    const [L, B] = await Promise.all([it[0] === "tier" ? tierAngebot(store, heute) : angebot(store, heute), buch(store, nm)]);// gleichzeitig laden (schneller)
    if (!L.includes(id)) return json({ ok: false, grund: "angebot" });
    const stand = B.reduce((s, e) => s + e.a, 0);
    if (besitz(B).includes(id)) return json({ ok: false, grund: "schon", stand });
    if (stand < it[3]) return json({ ok: false, grund: "geld", stand });
    if (it[2] === 10) {// Einzigartig: nur der erste Käufer bekommt es
      const ek = "x/einzig/" + id; if (await store.get(ek)) return json({ ok: false, grund: "weg", stand });
      await store.set(ek, nm); await new Promise(r => setTimeout(r, 300));
      if ((await store.get(ek)) !== nm) return json({ ok: false, grund: "weg", stand });
    }
    await store.set("b/" + nm + "/kauf/" + heute + "-" + id + "/" + (-it[3]), String(Date.now()));
    return json({ ok: true, stand: stand - it[3], inv: [...besitz(B), id] });
  }
  if (act === "anlegen") {
    // Slot belegen (id) oder leeren (id = null); nur eigene Items
    const slot = String(d.slot || ""), id = d.id ? String(d.id) : null;
    if (!Object.values(SHOP.items).some(v => v[1] === slot)) return json({ ok: false });
    if (id && (!SHOP.items[id] || SHOP.items[id][1] !== slot || !besitz(await buch(store, nm)).includes(id))) return json({ ok: false });
    const a = JSON.parse((await store.get("a/" + nm)) || "{}");
    if (id) a[slot] = id; else delete a[slot];
    await store.set("a/" + nm, JSON.stringify(a));
    const alle = await ausruestungAlle(store);
    if (Object.keys(a).length) alle[nm] = a; else delete alle[nm];
    await store.set("x/ausruestung", JSON.stringify(alle));
    return json({ ok: true, aus: a });
  }
  if (act === "stand") {
    // Alles Unabhängige gleichzeitig laden (deutlich schneller als nacheinander)
    const [einlL, live, likeL, klopfL, geschL, nachbar, premRoh, startRoh, stkL, fisL, sandRoh, ausRoh] = await Promise.all([
      liste(store, "b/" + nm + "/einladung/"), liveErf(store, nm), liste(store, "x/like/" + nm + "/"), liste(store, "x/klopfan/" + nm + "/"),
      liste(store, "x/geschenkt/" + nm + "/"), nachbarErf(store, nm), store.get("x/premium/" + nm), store.get("x/start/" + nm),
      liste(store, "x/sticker/" + nm + "/"), liste(store, "x/fisch/" + nm + "/"), store.get("x/sand/" + woche(heute) + "/" + nm + "/" + heute), store.get("a/" + nm)]);
    // neue angerechnete Einladungen einmal melden
    const eingeladen = [];
    await Promise.all(einlL.map(async k => { const n = k.split("/")[3], mk = "x/einlmeld/" + nm + "/" + n; if (!(await store.get(mk))) { await store.set(mk, "1"); eingeladen.push(n); } }));
    const likeN = likeL.length;
    const klopfer = [];// wer hat seit dem letzten Besuch geklopft? (einmal melden, dann löschen)
    for (const k of klopfL) { const n = k.split("/")[3].split("-").slice(1).join("-"); if (n && !klopfer.includes(n)) klopfer.push(n); }
    const geschenke = [];// 🎁 Muschel-Geschenke (Echtgeld) seit dem letzten Besuch: einmal melden, dann löschen
    await Promise.all([...klopfL.map(k => store.delete(k)), ...geschL.map(async k => { try { const g = JSON.parse((await store.get(k)) || "{}"); if (g.von) geschenke.push({ von: "@" + g.von, m: g.m }); } catch (e) {} await store.delete(k); })]);
    const B = await buch(store, nm), s = await serie(B);// nach Nachbar-/LIVE-Erfolg, damit deren Buchungen schon drin sind
    const posten = B.filter(e => e.a).map(e => ({ art: e.art, id: e.id, a: e.a, t: TEXT[e.art] || e.art }))
      .sort((x, y) => (y.id > x.id ? 1 : -1)).slice(0, 60);
    return mitCookie(json({
      ok: true, pinFehlt: !c.pin, nachbar, live, eingeladen, klopfer, geschenke, premium: !!premRoh, startDa: !startRoh, likes: { n: likeN }, neu: likeN >= 25 && (await erfGib("HERZ")) ? ["HERZ"] : [], sticker: stkL.map(k => k.split("/")[3]), fische: fisL.map(k => k.split("/")[3]), angelnHeute: Object.fromEntries([0, 1].map(i => [i, (B.find(e => e.art === "angeln" && e.id.startsWith(heute + "-" + i + "_")) || {}).id?.split("_")[1] || null])), sandHeute: !!sandRoh, geschenk: B.some(e => e.art === "geschenk" && e.id === heute), stand: B.reduce((s, e) => s + e.a, 0), serie: s,
      shells: B.filter(e => e.art === "shell" && e.id.startsWith(heute) && e.id.split("-").length === 6).map(e => e.id.split("-").slice(3).map(Number).join("-")),
      questsDone: B.filter(e => e.art === "quest" && e.id.startsWith(heute)).map(e => Number(e.id.split("-").pop())),
      gespendet: -B.filter(e => e.art === "spende").reduce((s, e) => s + e.a, 0), posten, heute, inv: besitz(B), aus: JSON.parse(ausRoh || "{}")
    }), nm, String(d.token || ""));
  }
  return json({ fehler: "Aktion" }, 400);
};

export const config = { path: "/api/muscheln" };
