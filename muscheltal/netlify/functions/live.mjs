// Erfolg „Live dabei“: Die Live-Seite (TikTok-LIVE-Overlay) meldet während des Streams die Usernamen der Zuschauer
// (Beitreten, Kommentar, Like, Folgen, Geschenk). Geschützt mit geheimem Schlüssel (Netlify-Umgebungsvariable LIVE_SCHLUESSEL).
// Merker je Name: "live/<name>" im Store "muscheln". Wer schon beansprucht ist, bekommt den Erfolg sofort (+10 Muscheln),
// alle anderen beim Beanspruchen / nächsten Besuch (siehe muscheln.mjs → liveErf).
import { getStore } from "@netlify/blobs";

const CORS = { "access-control-allow-origin": "*", "access-control-allow-methods": "GET, POST, OPTIONS", "access-control-allow-headers": "content-type, x-live-schluessel" };
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store", ...CORS } });
const NAME = /^[a-z0-9._]{1,40}$/;
const gleich = (a, b) => { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; };

export async function liveVergeben(store, nm) {
  const es = getStore("erfolge"), pre = "e/" + nm + "/LIVE/";
  if ((await es.list({ prefix: pre })).blobs.length) return false;
  await es.set(pre + Date.now(), "1");
  const bp = "b/" + nm + "/erf/LIVE/";
  if (!(await store.list({ prefix: bp })).blobs.length) await store.set(bp + "10", String(Date.now()));
  return true;
}

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  const store = getStore({ name: "muscheln", consistency: "strong" });
  // öffentlich: LIVE-Rangliste (insgesamt + letzter Stream), von der Live-App gemeldet
  if (req.method === "GET") return json(JSON.parse((await store.get("liverang")) || "null") || { gesamt: [], stream: null, ts: 0 });
  if (req.method !== "POST") return json({ fehler: "Methode" }, 405);
  const soll = (typeof Netlify !== "undefined" && Netlify.env.get("LIVE_SCHLUESSEL")) || process.env.LIVE_SCHLUESSEL || "";
  const ist = req.headers.get("x-live-schluessel") || "";
  if (!soll || soll.length < 16 || !gleich(ist, soll)) return json({ fehler: "Schlüssel" }, 403);
  let d = {};
  try { d = await req.json(); } catch (e) {}
  // Rangliste aus dem LIVE speichern (nur Name, Muscheln, Haus-Stufe – je höchstens 10)
  if (d.rang && typeof d.rang === "object") {
    const L = a => (Array.isArray(a) ? a : []).slice(0, 10).map(r => ({ n: String(r.n || "").slice(0, 42), id: NAME.test(String(r.id || "")) ? String(r.id) : null, m: Math.max(0, Math.round(Number(r.m) || 0)), s: String(r.s || "").slice(0, 30) }));
    const st = d.rang.stream && typeof d.rang.stream === "object" ? { start: Number(d.rang.stream.start) || 0, ende: Number(d.rang.stream.ende) || 0, top: L(d.rang.stream.top) } : null;
    await store.set("liverang", JSON.stringify({ gesamt: L(d.rang.gesamt), stream: st, live: !!d.rang.live, ts: Date.now() }));
    if (!Array.isArray(d.namen)) return json({ ok: true, rang: true });
  }
  const namen = [...new Set((Array.isArray(d.namen) ? d.namen : []).map(n => String(n || "").trim().toLowerCase().replace(/^@/, "")).filter(n => NAME.test(n)))].slice(0, 300);
  let neu = 0, sofort = 0;
  for (const nm of namen) {
    if (nm === "echter.alex") continue;
    if (!(await store.get("live/" + nm))) { await store.set("live/" + nm, String(Date.now())); neu++; }
    if (await store.get("c/" + nm)) { if (await liveVergeben(store, nm)) sofort++; }
  }
  return json({ ok: true, gemeldet: namen.length, neu, sofort });
};

export const config = { path: "/api/live" };
