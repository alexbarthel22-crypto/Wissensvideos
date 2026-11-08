// Besuche: Wer oben seinen TikTok-Namen sucht, gilt als „online“. Die Seite meldet sich dann jede Minute (Ping).
// Gespeichert wird pro Besuch: Name, Beginn, letztes Lebenszeichen, Anzahl Pings – 14 Tage lang, danach automatisch gelöscht.
// Auslesen nur mit Passwort (Netlify-Umgebungsvariable ADMIN_KEY).
import { getStore } from "@netlify/blobs";

const TAGE = 14, MS_TAG = 864e5;
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const tag = (t) => new Date(t).toLocaleDateString("sv-SE", { timeZone: "Europe/Berlin" }); // JJJJ-MM-TT

export default async (req) => {
  const store = getStore("besuche"), jetzt = Date.now();
  if (req.method === "POST") {
    let b = {};
    try { b = JSON.parse((await req.text()).slice(0, 500)); } catch (e) {}
    const name = String(b.name || "").trim().toLowerCase(), sid = String(b.sid || "");
    if (!/^@[a-z0-9._]{1,40}$/.test(name) || !/^[a-z0-9-]{8,40}$/i.test(sid)) return json({ fehler: "Daten" }, 400);
    const key = `s/${tag(jetzt)}/${sid}_${name.slice(1)}`;
    const v = (await store.get(key, { type: "json" })) || { name, start: jetzt, last: jetzt, n: 0 };
    v.last = jetzt; v.n += 1;
    await store.setJSON(key, v);
    return json({ ok: true });
  }
  if (req.method !== "GET") return json({ fehler: "Methode" }, 405);
  const soll = (globalThis.Netlify && Netlify.env.get("ADMIN_KEY")) || process.env.ADMIN_KEY;
  if (!soll) return json({ fehler: "ADMIN_KEY ist in Netlify nicht gesetzt" }, 503);
  if (new URL(req.url).searchParams.get("key") !== soll) return json({ fehler: "Passwort falsch" }, 401);
  const { blobs } = await store.list({ prefix: "s/" }), grenze = tag(jetzt - TAGE * MS_TAG), out = [];
  for (const { key } of blobs) {
    const d = key.split("/")[1];
    if (d < grenze) { await store.delete(key); continue; }
    const v = await store.get(key, { type: "json" });
    if (v) out.push({ tag: d, ...v });
  }
  out.sort((a, b) => b.start - a.start);
  return json({ besuche: out, jetzt });
};

export const config = { path: "/api/besuch" };
