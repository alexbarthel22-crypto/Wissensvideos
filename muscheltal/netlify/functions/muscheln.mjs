// Muschel-Konten: Namen beanspruchen, Kontobuch, Login-Serie, Aufgaben, schwebende Muscheln, Spenden.
// Jede Buchung ist ein eigener Eintrag mit festem Schlüssel "b/<name>/<art>/<kennung>/<betrag>" – der Betrag steht im Schlüssel,
// so ergibt sich der Kontostand aus einer einzigen Liste. Feste Schlüssel (z. B. login/2026-11-10) verhindern Doppelbuchungen.
import { getStore } from "@netlify/blobs";
import { JOBS } from "../lib/jobs.mjs";
import { BEWOHNER, NACHBARN, SEIT } from "../lib/bewohner.mjs";
import { liveVergeben } from "./live.mjs";
import { CODES } from "../lib/codes.mjs";
import { SHOP } from "../lib/shop.mjs";

const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const NAME = /^@[a-z0-9._]{1,40}$/;
const SERIE = [3, 5, 8, 12, 17, 23, 32];
const TZ = "Europe/Berlin";
const tag = (t = Date.now()) => new Intl.DateTimeFormat("sv-SE", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date(t));
const gestern = (d) => { const t = new Date(d + "T12:00:00Z"); t.setUTCDate(t.getUTCDate() - 1); return t.toISOString().slice(0, 10); };
const woche = (d) => { const t = new Date(d + "T12:00:00Z"), w = (t.getUTCDay() + 6) % 7; t.setUTCDate(t.getUTCDate() - w); return t.toISOString().slice(0, 10); };
async function sha(s) { const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join(""); }
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
const RESET = [...["marina.cgnn", "ju1e_smt", "mimposible", "maja.gnw", "eeli_mxo", "luna.gsn02", "toca_lexi00"].map(n => [n, 1, TEST_12_11])];
async function zuruecksetzen(store) {
  for (const [n, nr, ab] of RESET) {
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
    for (const k of await liste(kasse, "s/" + n + "/")) await kasse.delete(k);
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
const TEXT = { login: "Login-Serie", quest: "Aufgabe", qbonus: "Alle 3 Aufgaben", shell: "Schwebende Muschel", erf: "Neuer Erfolg", story: "Story geteilt", spende: "Spende Inselkasse", tresor: "Tresor des Schöpfers", code: "Geheimcode aus dem Video", einladung: "Freund eingeladen", kauf: "Muschel-Shop", null: "Neustart: alle Konten auf 0" };

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
  if (VOR.tag !== t) VOR = { tag: t, p: (async () => { await nullen(store); await zuruecksetzen(store); await zurueckAuf(store); await aufraeumen(store); })().catch(() => { VOR.tag = ""; }) };
  return VOR.p;
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
async function rangDaten(store) {
  const jetzt = Date.now();
  if (RANGC.d && jetzt - RANGC.t < 45000) return RANGC.d;
  try { const c = JSON.parse((await store.get("x/rangcache")) || "null"); if (c && jetzt - c.t < 45000) { RANGC = { t: c.t, d: c.d }; return c.d; } } catch (e) {}
  const claimed = new Set((await liste(store, "c/")).map(k => k.slice(2)).filter(n => BEWOHNER.has(n)));// Ausgezogene nicht mehr anzeigen
  const sum = {};
  for (const k of await liste(store, "b/")) { const [, n, , , a] = k.split("/"); if (claimed.has(n)) sum[n] = (sum[n] || 0) + (Number(a) || 0); }
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
async function angebot(store, heute) {
  const k = "x/shop/" + heute, alt = await store.get(k);
  if (alt) return JSON.parse(alt);
  const weg = new Set((await liste(store, "x/einzig/")).map(x => x.slice(9))), r = zufall("muschelshop-" + heute), ids = [];
  for (const kat of SHOP.kat) {
    let pool = Object.entries(SHOP.items).filter(([id, v]) => v[0] === kat && !weg.has(id));
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
  if (!NAME.test(name)) return json({ fehler: "Name" }, 400);
  const nm = name.slice(1), heute = tag();

  if (act === "claim") {
    if (nm === "echter.alex") return json({ ok: false, beansprucht: true });// Schöpfer: nicht beanspruchbar
    if (await store.get("c/" + nm)) return json({ ok: false, beansprucht: true });
    const token = crypto.randomUUID() + "-" + crypto.randomUUID();
    await store.set("c/" + nm, JSON.stringify({ h: await sha(token), ts: Date.now() }));
    // bei gleichzeitigem Beanspruchen gewinnt, wessen Eintrag gespeichert blieb
    await new Promise(r => setTimeout(r, 300));
    const c = JSON.parse((await store.get("c/" + nm)) || "{}");
    if (c.h !== (await sha(token))) return json({ ok: false, beansprucht: true });
    const nachbar = await nachbarErf(store, nm), live = await liveErf(store, nm);
    const von = await einladungPruefen(store, nm, String(d.kt || ""));
    return json({ ok: true, token, von, neu: [...(nachbar ? ["NACHBAR"] : []), ...(live ? ["LIVE"] : [])] });
  }
  // alle weiteren Aktionen nur mit dem Schlüssel des Besitzers
  const c = JSON.parse((await store.get("c/" + nm)) || "null");
  if (!c || c.h !== (await sha(String(d.token || "")))) return json({ fehler: "Nicht beansprucht" }, 403);

  const setze = async (art, id, a) => {
    const pre = "b/" + nm + "/" + art + "/" + id + "/";
    if ((await store.list({ prefix: pre })).blobs.length) return false;
    await store.set(pre + a, String(Date.now()));
    return true;
  };
  const J = job(nm);

  // heutiger Login-Bonus: Serien-Tag aus dem gestrigen Eintrag (sonst Tag 1)
  const serie = async (B) => {
    const L = B.filter(e => e.art === "login");
    const h = L.find(e => e.id.startsWith(heute)), g = L.find(e => e.id.startsWith(gestern(heute)));
    const gTag = g ? Number(g.id.split("_")[1]) || 1 : 0;
    const t = h ? Number(h.id.split("_")[1]) || 1 : (gTag ? gTag % 7 + 1 : 1);
    return { tag: t, abgeholt: !!h, betrag: SERIE[t - 1], job: J };
  };

  if (act === "login") {
    const B = await buch(store, nm), s = await serie(B);
    if (s.abgeholt) return json({ ok: false, schon: true });
    const sum = s.betrag + (J ? J.z : 0);
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
    return json({ ok, tag: s.tag, betrag: s.betrag, job: J, summe: sum, neu });
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
    return json({ ok, bonus });
  }
  if (act === "shell") {
    const i = Number(d.i);
    if (!(i >= 0 && i < 4)) return json({ fehler: "Muschel" }, 400);
    return json({ ok: await setze("shell", heute + "-" + i, 1) });
  }
  if (act === "erf") {
    const k = String(d.key || "").toUpperCase();
    if (!/^[A-Z]{2,12}$/.test(k)) return json({ fehler: "Erfolg" }, 400);
    return json({ ok: await setze("erf", k, 10) });
  }
  // Tresor des Schöpfers (Schlossinsel): einmalige Verlosung je Name – 3, 5, 7 oder 10 Muscheln (je 25 %)
  // Geheimcode aus einem TikTok-Video: gilt nur an den angegebenen Tagen, je Name einmal; höchstens 10 Versuche pro Tag
  if (act === "code") {
    const k = String(d.code || "").toUpperCase().replace(/[^A-Z0-9ÄÖÜ]/g, "").slice(0, 30);
    const vk = "x/codeversuch/" + nm + "/" + heute, vers = Number(await store.get(vk)) || 0;
    if (vers >= 10) return json({ ok: false, grund: "versuche" });
    const c = CODES.find(c => c.code === k && heute >= c.von && heute <= c.bis);
    if (!c) { await store.set(vk, String(vers + 1)); return json({ ok: false, grund: "falsch" }); }
    const betrag = 2 + (crypto.getRandomValues(new Uint32Array(1))[0] % 9);// zufällig 2–10 Muscheln, jede Zahl gleich wahrscheinlich
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
  if (act === "story") return json({ ok: await setze("story", woche(heute), 25) });
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
    if (!(await angebot(store, heute)).includes(id)) return json({ ok: false, grund: "angebot" });
    const B = await buch(store, nm), stand = B.reduce((s, e) => s + e.a, 0);
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
    // neue angerechnete Einladungen einmal melden
    const eingeladen = [];
    for (const k of await liste(store, "b/" + nm + "/einladung/")) { const n = k.split("/")[3], mk = "x/einlmeld/" + nm + "/" + n; if (!(await store.get(mk))) { await store.set(mk, "1"); eingeladen.push(n); } }
    const live = await liveErf(store, nm);
    const nachbar = await nachbarErf(store, nm);// schon beanspruchte Nachbarn bekommen den Erfolg beim nächsten Besuch
    const B = await buch(store, nm), s = await serie(B);
    const posten = B.filter(e => e.a).map(e => ({ art: e.art, id: e.id, a: e.a, t: TEXT[e.art] || e.art }))
      .sort((x, y) => (y.id > x.id ? 1 : -1)).slice(0, 60);
    return json({
      ok: true, nachbar, live, eingeladen, stand: B.reduce((s, e) => s + e.a, 0), serie: s,
      shells: B.filter(e => e.art === "shell" && e.id.startsWith(heute)).map(e => Number(e.id.split("-").pop())),
      questsDone: B.filter(e => e.art === "quest" && e.id.startsWith(heute)).map(e => Number(e.id.split("-").pop())),
      gespendet: -B.filter(e => e.art === "spende").reduce((s, e) => s + e.a, 0), posten, heute, inv: besitz(B), aus: JSON.parse((await store.get("a/" + nm)) || "{}")
    });
  }
  return json({ fehler: "Aktion" }, 400);
};

export const config = { path: "/api/muscheln" };
