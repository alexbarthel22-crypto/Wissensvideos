// Anonyme Besuchs-Statistik + Auswertung für den Betreiber.
// Besucher: Die Seite schickt ohne Cookies/ohne Speicher auf dem Gerät gesammelte Werte einer Sitzung (zufällige Sitzungs-Nummer,
// nur im Arbeitsspeicher) – keine Namen, keine IP-Adressen. Gespeichert als "s/<Tag>/<Sitzung>" (wird bei jeder Meldung überschrieben).
// Betreiber: GET mit Passwort (eigenes Passwort, nur als SHA-256-Hash hier) → Auswertung + Übersicht der
// beanspruchten Spieler aus den Spieldaten (Muscheln, Serie, Aufgaben, Käufe, Erfolge).
import { getStore } from "@netlify/blobs";
import { PAKETE } from "./stripe.mjs";
const PW_HASH = "e227d80e4bfb21510b4165198616f10483652d45a3b6c32872dedeab805994a5";
const TZ = "Europe/Berlin";
const tag = (t = Date.now()) => new Intl.DateTimeFormat("sv-SE", { timeZone: TZ }).format(new Date(t));
const stunde = (t) => Number(new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hour: "2-digit", hourCycle: "h23" }).format(new Date(t)));
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const sha = async (t) => [...new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)))].map(b => b.toString(16).padStart(2, "0")).join("");
async function liste(store, prefix) { const out = []; let cursor; do { const r = await store.list({ prefix, cursor }); out.push(...r.blobs.map(b => b.key)); cursor = r.cursor; } while (cursor); return out; }
const W = /^[\p{L}\p{N}_:.\- &()]{1,40}$/u;
// Eingehende Werte streng begrenzen (nur bekannte Felder, Zahlen gedeckelt, Schlüssel kurz)
function sauber(d) {
  const zahl = (x, m) => Math.max(0, Math.min(m, Math.round(Number(x) || 0)));
  const map = (o, m, n = 80) => { const r = {}; let i = 0; for (const [k, v] of Object.entries(o && typeof o === "object" ? o : {})) { if (i++ >= n) break; if (W.test(k)) r[k] = zahl(v, m); } return r; };
  return {
    t0: zahl(d.t0, 4e12), dauer: zahl(d.dauer, 86400), sicht: zahl(d.sicht, 86400), geraet: ["handy", "tablet", "computer"].includes(d.geraet) ? d.geraet : "?",
    quelle: W.test(String(d.quelle || "")) ? String(d.quelle) : "?", seite: W.test(String(d.seite || "")) ? String(d.seite) : "?",
    bereiche: map(d.bereiche, 86400, 20), ereignisse: map(d.ereignisse, 1e4, 60), orte: map(d.orte, 86400, 60), heat: map(d.heat, 86400, 400),
    ende: W.test(String(d.ende || "")) ? String(d.ende) : "", laden: zahl(d.laden, 6e4), fps: zahl(d.fps, 240), zoom: map(d.zoom, 86400, 10), konto: d.konto ? 1 : 0, neu: d.neu === 0 ? 0 : 1
  };
}
const add = (a, b) => { for (const [k, v] of Object.entries(b || {})) a[k] = (a[k] || 0) + v; return a; };
function auswerten(S) {
  const A = { sitzungen: 0, seiten: {}, dauer: [], sicht: 0, geraet: {}, quelle: {}, bereiche: {}, ereignisse: {}, orte: {}, heat: {}, ende: {}, stunden: Array(24).fill(0), laden: [], fps: [], zoom: {}, konto: 0, trichter: {}, premium: {} };
  const T = ["besuch", "suche", "pass_auf", "konto_auf", "erkunden", "aufgabe", "kauf"];
  for (const s of S) {
    // Neu geladen (gleicher Tab, F5/Neuladen) zählt nicht als neuer Besuch: Zeit, Bereiche, Orte usw. zählen mit, Besuch/Gerät/Quelle nicht
    const neu = s.neu !== 0, e0 = { ...(s.ereignisse || {}) }; if (!neu) delete e0.besuch;
    A.sicht += s.sicht; add(A.bereiche, s.bereiche); add(A.ereignisse, e0); add(A.orte, s.orte); add(A.heat, s.heat); add(A.zoom, s.zoom); if (s.fps) A.fps.push(s.fps);
    if (!neu) continue;
    A.sitzungen++; add(A.seiten, { [s.seite || "start"]: 1 });
    A.dauer.push(s.sicht || s.dauer); add(A.geraet, { [s.geraet]: 1 }); add(A.quelle, { [s.quelle]: 1 });
    if (s.ende) add(A.ende, { [s.ende]: 1 }); A.stunden[stunde(s.t0 || Date.now())]++; if (s.laden) A.laden.push(s.laden); A.konto += s.konto;
    if ((s.seite || "start") !== "start") continue;// Weg der Besucher und Premium-Weg nur für die Startseite
    const e = s.ereignisse || {}, hat = { besuch: 1, suche: e.suche, pass_auf: e.pass_auf, konto_auf: e.konto_auf, erkunden: e.erkunden_start || e.erkunden, aufgabe: e.aufgabe, kauf: e.kauf };
    for (const k of T) if (hat[k]) A.trichter[k] = (A.trichter[k] || 0) + 1;
    // Premium-Shop (Echtgeld): Weg pro Sitzung – Shop gesehen → entsperrt → Paket angetippt → Haken gesetzt → zur Bezahlung → bezahlt/abgebrochen
    const pr = { gesehen: e.prem_gesehen || e.prem_gesehen_offen, entsperrt: e.prem_entsperrt, paket: e.pak_auf, haken: e.pak_haken, kasse: e.pak_kasse, bezahlt: e.kauf_ok, abbruch: e.kauf_abbruch, fehler: e.pak_fehler };
    for (const [k, v] of Object.entries(pr)) if (v) A.premium[k] = (A.premium[k] || 0) + 1;
  }
  const med = a => { if (!a.length) return 0; const b = [...a].sort((x, y) => x - y); return b[b.length >> 1]; };
  A.dauerMedian = med(A.dauer); A.dauerSchnitt = A.dauer.length ? Math.round(A.dauer.reduce((s, x) => s + x, 0) / A.dauer.length) : 0;
  A.kurz = A.dauer.filter(x => x < 10).length; A.lang = A.dauer.filter(x => x >= 300).length; A.ladenMedian = med(A.laden); A.fpsMedian = med(A.fps);
  delete A.dauer; delete A.laden; delete A.fps; return A;
}
// Echtgeld-Käufe aus den Buchungen (b/<name>/euro/<Sitzung>/<Muscheln>, Rückbuchungen „euro-zurueck“) und x/euro/<Zahlung>
async function echtgeld(tageN) {
  const st = getStore({ name: "muscheln", consistency: "strong" });
  const proM = {}; for (const [id, p] of Object.entries(PAKETE)) proM[p.muscheln] = { id, cent: p.cent };
  const K = [], zur = {};
  for (const k of await liste(st, "b/")) {
    const [, n, art, id, a] = k.split("/");
    if (art === "euro") K.push({ k, name: "@" + n, sid: id, muscheln: Number(a) || 0 });
    else if (art === "euro-zurueck") zur[n] = (zur[n] || 0) + (Number(a) || 0);
  }
  for (let j = 0; j < K.length; j += 50) { const v = await Promise.all(K.slice(j, j + 50).map(x => st.get(x.k))); v.forEach((t, i) => { K[j + i].zeit = Number(t) || 0; }); }
  const ab = Date.now() - tageN * 864e5, E = { kaeufe: 0, umsatzCent: 0, kaeufer: 0, wiederkaeufer: 0, startangebot: 0, pakete: {}, tage: {}, stunden: Array(24).fill(0), erstattetMuscheln: 0, entsperrt: 0, liste: [] };
  const proKunde = {};
  for (const x of K) {
    const p = proM[x.muscheln] || { id: "?", cent: 0 }; x.paket = p.id; x.cent = p.cent; x.tag = x.zeit ? tag(x.zeit) : "";
    proKunde[x.name] = (proKunde[x.name] || 0) + 1;
    if (x.zeit && x.zeit < ab) continue;
    E.kaeufe++; E.umsatzCent += p.cent; if (p.id === "start") E.startangebot++;
    const P = E.pakete[p.id] = E.pakete[p.id] || { n: 0, cent: 0 }; P.n++; P.cent += p.cent;
    if (x.tag) E.tage[x.tag] = (E.tage[x.tag] || 0) + p.cent; if (x.zeit) E.stunden[stunde(x.zeit)]++;
    E.liste.push({ name: x.name, tag: x.tag, zeit: x.zeit, paket: p.id, cent: p.cent, muscheln: x.muscheln });
  }
  E.kaeufer = Object.keys(proKunde).length; E.wiederkaeufer = Object.values(proKunde).filter(v => v > 1).length;
  E.erstattetMuscheln = -Object.values(zur).reduce((s, v) => s + v, 0);
  E.entsperrt = (await liste(st, "x/premium/")).length;
  E.liste.sort((a, b) => b.zeit - a.zeit); E.liste = E.liste.slice(0, 100);
  return E;
}
async function spieler() {
  const st = getStore({ name: "muscheln", consistency: "strong" }), es = getStore("erfolge");
  const claimed = new Map(); for (const k of await liste(st, "c/")) claimed.set(k.slice(2), null);
  const P = {}; for (const n of claimed.keys()) P[n] = { name: "@" + n, stand: 0, logins: 0, letzter: "", serie: 0, aufgaben: 0, kaeufe: 0, ausgegeben: 0, erfolge: 0, tresor: false, code: 0, einladungen: 0, euro: 0 };
  const tage = {}, EK = {};// Erfolge je Name: Server-Erfolge (e/) und im Browser verdiente (Buchung „erf“), jeder nur einmal
  for (const k of await liste(st, "b/")) {
    const [, n, art, id, a] = k.split("/"), p = P[n]; if (!p) continue; const v = Number(a) || 0; p.stand += v;
    if (art === "login") { p.logins++; const d = id.slice(0, 10); (tage[n] = tage[n] || new Set()).add(d); if (d > p.letzter) p.letzter = d; }
    else if (art === "quest") p.aufgaben++; else if (art === "kauf") { p.kaeufe++; p.ausgegeben -= v; } else if (art === "tresor") p.tresor = true; else if (art === "code") p.code++; else if (art === "einladung") p.einladungen++;
    else if (art === "erf" && v > 0) (EK[n] = EK[n] || new Set()).add(id);
    else if (art === "euro") { const q = Object.values(PAKETE).find(x => x.muscheln === v); p.euro += q ? q.cent : 0; }
  }
  for (const k of await liste(es, "e/")) { const [, n, K] = k.split("/"); if (P[n]) (EK[n] = EK[n] || new Set()).add(K); }
  for (const [n, s] of Object.entries(EK)) if (P[n]) { P[n].erfolge = s.size; P[n].erfolgListe = [...s].sort(); }
  for (const [n, s] of Object.entries(tage)) { let d = [...s].sort().pop(), z = 0; while (s.has(d)) { z++; const t = new Date(d + "T12:00:00Z"); t.setUTCDate(t.getUTCDate() - 1); d = t.toISOString().slice(0, 10); } P[n].serie = z; }
  return Object.values(P).sort((a, b) => (b.letzter > a.letzter ? 1 : b.letzter < a.letzter ? -1 : b.stand - a.stand));
}
// Einmalig (Veröffentlichung nach 18.11., erneut nach 20.11. = voll-3, erneut nach 21.11. = voll-4): Statistik nochmal komplett zurücksetzen – läuft beim ersten Aufruf nach dem Deploy
let LEER2 = null;
async function leeren2(store) {
  if (await store.get("x/bereinigt/voll-4")) return;
  await store.set("x/bereinigt/voll-2", String(Date.now())); await store.set("x/bereinigt/voll-3", String(Date.now())); await store.set("x/bereinigt/voll-4", String(Date.now()));
  for (const k of [...await liste(store, "s/"), ...await liste(store, "agg/")]) await store.delete(k);
}
export default async (req) => {
  const store = getStore({ name: "statistik", consistency: "strong" });
  if (!LEER2) LEER2 = leeren2(store).catch(() => { LEER2 = null; });
  await LEER2;
  if (req.method === "POST") {
    let d = {}; try { const t = await req.text(); if (t.length > 30000) return json({ ok: false }, 413); d = JSON.parse(t); } catch (e) { return json({ ok: false }, 400); }
    const sid = String(d.sid || ""); if (!/^[a-z0-9]{8,40}$/.test(sid)) return json({ ok: false }, 400);
    const s = sauber(d); await store.set("s/" + tag(s.t0 || Date.now()) + "/" + sid, JSON.stringify(s));
    return json({ ok: true });
  }
  // Auswertung nur mit Passwort
  if ((await sha(req.headers.get("x-pw") || "")) !== PW_HASH) return json({ fehler: "Passwort" }, 403);
  // Einmalig (18.11.): Testkäufe aus der Statistik entfernen – Kauf-Schritte (Haken, zur Bezahlung, bezahlt/abgebrochen, Fehler)
  // der Testtage 17./18.11. löschen und die Tagessummen neu berechnen lassen, als hätte es die Testkäufe nie gegeben
  // Einmalig (18.11.): Statistik komplett zurücksetzen – Start mit echten Besuchern (Testphase hinter der Zugangssperre zählt nicht)
  if (!(await store.get("x/bereinigt/voll-1"))) {
    for (const k of [...await liste(store, "s/"), ...await liste(store, "agg/")]) await store.delete(k);
    await store.set("x/bereinigt/voll-1", String(Date.now())); await store.set("x/bereinigt/testkauf-1", String(Date.now()));
  }
  if (!(await store.get("x/bereinigt/testkauf-1"))) {
    const TEST = /^(pak_haken|pak_kasse.*|pak_fehler|kauf_ok|kauf_abbruch)$/;
    for (const d of ["2026-11-17", "2026-11-18"]) {
      for (const k of await liste(store, "s/" + d + "/")) { const v = JSON.parse((await store.get(k)) || "null"); if (!v || !v.ereignisse) continue; let geaendert = false; for (const e of Object.keys(v.ereignisse)) if (TEST.test(e)) { delete v.ereignisse[e]; geaendert = true; } if (geaendert) await store.set(k, JSON.stringify(v)); }
      await store.delete("agg/" + d);
    }
    await store.set("x/bereinigt/testkauf-1", String(Date.now()));
  }
  const u = new URL(req.url), tageN = Math.max(1, Math.min(60, Number(u.searchParams.get("tage")) || 7)), heute = tag();
  const out = { tage: [], gesamt: null };
  const alle = [];
  for (let i = tageN - 1; i >= 0; i--) {
    const d = tag(Date.now() - i * 864e5);
    let S = null;
    if (d !== heute) { const c = await store.get("agg/" + d); if (c) { const A = JSON.parse(c); out.tage.push({ tag: d, ...A }); alle.push(A); continue; } }
    const keys = await liste(store, "s/" + d + "/"); S = [];
    for (let j = 0; j < keys.length; j += 50) S.push(...(await Promise.all(keys.slice(j, j + 50).map(k => store.get(k)))).filter(Boolean).map(x => JSON.parse(x)));
    const A = auswerten(S); if (d !== heute && d < heute) await store.set("agg/" + d, JSON.stringify(A));
    out.tage.push({ tag: d, ...A }); alle.push(A);
  }
  // Summe über den Zeitraum
  const G = { sitzungen: 0, seiten: {}, sicht: 0, geraet: {}, quelle: {}, bereiche: {}, ereignisse: {}, orte: {}, heat: {}, ende: {}, stunden: Array(24).fill(0), zoom: {}, konto: 0, trichter: {}, premium: {}, kurz: 0, lang: 0 };
  for (const A of alle) { G.sitzungen += A.sitzungen; G.sicht += A.sicht; G.kurz += A.kurz; G.lang += A.lang; G.konto += A.konto; for (const k of ["geraet", "quelle", "bereiche", "ereignisse", "orte", "heat", "ende", "zoom", "trichter", "premium", "seiten"]) add(G[k], A[k] || {}); A.stunden.forEach((v, i) => G.stunden[i] += v); }
  G.dauerSchnitt = G.sitzungen ? Math.round(G.sicht / G.sitzungen) : 0;
  out.gesamt = G;
  if (u.searchParams.get("spieler")) { out.spieler = await spieler(); out.echtgeld = await echtgeld(tageN); }
  // Aufräumen laut Datenschutzerklärung: Einzelwerte älter als 14 Monate löschen (Tagessummen "agg/" bleiben)
  for (let i = 425; i < 455; i++) for (const k of await liste(store, "s/" + tag(Date.now() - i * 864e5) + "/")) await store.delete(k);
  return json(out);
};
export const config = { path: "/api/stat" };
