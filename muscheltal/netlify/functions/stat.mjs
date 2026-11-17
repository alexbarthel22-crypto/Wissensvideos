// Anonyme Besuchs-Statistik + Auswertung für den Betreiber.
// Besucher: Die Seite schickt ohne Cookies/ohne Speicher auf dem Gerät gesammelte Werte einer Sitzung (zufällige Sitzungs-Nummer,
// nur im Arbeitsspeicher) – keine Namen, keine IP-Adressen. Gespeichert als "s/<Tag>/<Sitzung>" (wird bei jeder Meldung überschrieben).
// Betreiber: GET mit Passwort (eigenes Passwort, nur als SHA-256-Hash hier) → Auswertung + Übersicht der
// beanspruchten Spieler aus den Spieldaten (Muscheln, Serie, Aufgaben, Käufe, Erfolge).
import { getStore } from "@netlify/blobs";
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
    ende: W.test(String(d.ende || "")) ? String(d.ende) : "", laden: zahl(d.laden, 6e4), fps: zahl(d.fps, 240), zoom: map(d.zoom, 86400, 10), konto: d.konto ? 1 : 0
  };
}
const add = (a, b) => { for (const [k, v] of Object.entries(b || {})) a[k] = (a[k] || 0) + v; return a; };
function auswerten(S) {
  const A = { sitzungen: S.length, dauer: [], sicht: 0, geraet: {}, quelle: {}, bereiche: {}, ereignisse: {}, orte: {}, heat: {}, ende: {}, stunden: Array(24).fill(0), laden: [], fps: [], zoom: {}, konto: 0, trichter: {} };
  const T = ["besuch", "suche", "pass_auf", "konto_auf", "erkunden", "aufgabe", "kauf"];
  for (const s of S) {
    A.dauer.push(s.sicht || s.dauer); A.sicht += s.sicht; add(A.geraet, { [s.geraet]: 1 }); add(A.quelle, { [s.quelle]: 1 }); add(A.bereiche, s.bereiche); add(A.ereignisse, s.ereignisse);
    add(A.orte, s.orte); add(A.heat, s.heat); if (s.ende) add(A.ende, { [s.ende]: 1 }); A.stunden[stunde(s.t0 || Date.now())]++; if (s.laden) A.laden.push(s.laden); if (s.fps) A.fps.push(s.fps); add(A.zoom, s.zoom); A.konto += s.konto;
    const e = s.ereignisse || {}, hat = { besuch: 1, suche: e.suche, pass_auf: e.pass_auf, konto_auf: e.konto_auf, erkunden: e.erkunden, aufgabe: e.aufgabe, kauf: e.kauf };
    for (const k of T) if (hat[k]) A.trichter[k] = (A.trichter[k] || 0) + 1;
  }
  const med = a => { if (!a.length) return 0; const b = [...a].sort((x, y) => x - y); return b[b.length >> 1]; };
  A.dauerMedian = med(A.dauer); A.dauerSchnitt = A.dauer.length ? Math.round(A.dauer.reduce((s, x) => s + x, 0) / A.dauer.length) : 0;
  A.kurz = A.dauer.filter(x => x < 10).length; A.lang = A.dauer.filter(x => x >= 300).length; A.ladenMedian = med(A.laden); A.fpsMedian = med(A.fps);
  delete A.dauer; delete A.laden; delete A.fps; return A;
}
async function spieler() {
  const st = getStore({ name: "muscheln", consistency: "strong" }), es = getStore("erfolge");
  const claimed = new Map(); for (const k of await liste(st, "c/")) claimed.set(k.slice(2), null);
  const P = {}; for (const n of claimed.keys()) P[n] = { name: "@" + n, stand: 0, logins: 0, letzter: "", serie: 0, aufgaben: 0, kaeufe: 0, ausgegeben: 0, erfolge: 0, tresor: false, code: 0, einladungen: 0 };
  const tage = {};
  for (const k of await liste(st, "b/")) {
    const [, n, art, id, a] = k.split("/"), p = P[n]; if (!p) continue; const v = Number(a) || 0; p.stand += v;
    if (art === "login") { p.logins++; const d = id.slice(0, 10); (tage[n] = tage[n] || new Set()).add(d); if (d > p.letzter) p.letzter = d; }
    else if (art === "quest") p.aufgaben++; else if (art === "kauf") { p.kaeufe++; p.ausgegeben -= v; } else if (art === "tresor") p.tresor = true; else if (art === "code") p.code++; else if (art === "einladung") p.einladungen++;
  }
  for (const k of await liste(es, "e/")) { const n = k.split("/")[1]; if (P[n]) P[n].erfolge++; }
  for (const [n, s] of Object.entries(tage)) { let d = [...s].sort().pop(), z = 0; while (s.has(d)) { z++; const t = new Date(d + "T12:00:00Z"); t.setUTCDate(t.getUTCDate() - 1); d = t.toISOString().slice(0, 10); } P[n].serie = z; }
  return Object.values(P).sort((a, b) => (b.letzter > a.letzter ? 1 : b.letzter < a.letzter ? -1 : b.stand - a.stand));
}
export default async (req) => {
  const store = getStore({ name: "statistik", consistency: "strong" });
  if (req.method === "POST") {
    let d = {}; try { const t = await req.text(); if (t.length > 30000) return json({ ok: false }, 413); d = JSON.parse(t); } catch (e) { return json({ ok: false }, 400); }
    const sid = String(d.sid || ""); if (!/^[a-z0-9]{8,40}$/.test(sid)) return json({ ok: false }, 400);
    const s = sauber(d); await store.set("s/" + tag(s.t0 || Date.now()) + "/" + sid, JSON.stringify(s));
    return json({ ok: true });
  }
  // Auswertung nur mit Passwort
  if ((await sha(req.headers.get("x-pw") || "")) !== PW_HASH) return json({ fehler: "Passwort" }, 403);
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
  const G = { sitzungen: 0, sicht: 0, geraet: {}, quelle: {}, bereiche: {}, ereignisse: {}, orte: {}, heat: {}, ende: {}, stunden: Array(24).fill(0), zoom: {}, konto: 0, trichter: {}, kurz: 0, lang: 0 };
  for (const A of alle) { G.sitzungen += A.sitzungen; G.sicht += A.sicht; G.kurz += A.kurz; G.lang += A.lang; G.konto += A.konto; for (const k of ["geraet", "quelle", "bereiche", "ereignisse", "orte", "heat", "ende", "zoom", "trichter"]) add(G[k], A[k]); A.stunden.forEach((v, i) => G.stunden[i] += v); }
  G.dauerSchnitt = G.sitzungen ? Math.round(G.sicht / G.sitzungen) : 0;
  out.gesamt = G;
  if (u.searchParams.get("spieler")) out.spieler = await spieler();
  // Aufräumen laut Datenschutzerklärung: Einzelwerte älter als 14 Monate löschen (Tagessummen "agg/" bleiben)
  for (let i = 425; i < 455; i++) for (const k of await liste(store, "s/" + tag(Date.now() - i * 864e5) + "/")) await store.delete(k);
  return json(out);
};
export const config = { path: "/api/stat" };
