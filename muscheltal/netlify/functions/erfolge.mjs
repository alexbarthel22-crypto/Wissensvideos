// Erfolge dauerhaft speichern: Wer einen Erfolg erzielt, hat ihn für immer auf seinem Muschelpass – auf jedem Gerät.
// Ein Eintrag je Erfolg: Schlüssel "e/<name>/<ERFOLG>/<zeitstempel>" (kein Überschreiben, keine Wettläufe).
import { getStore } from "@netlify/blobs";

const ERLAUBT = new Set(["LUPE", "AUF", "UNTER", "SCOOT"]);
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export default async (req) => {
  const store = getStore("erfolge");
  if (req.method === "GET") {
    const alle = {};
    let cursor;
    do {
      const r = await store.list({ prefix: "e/", cursor });
      for (const b of r.blobs) {
        const [, n, k, ts] = b.key.split("/");
        const m = (alle["@" + n] = alle["@" + n] || {});
        if (!m[k] || Number(ts) < m[k]) m[k] = Number(ts);
      }
      cursor = r.cursor;
    } while (cursor);
    return json({ erfolge: alle });
  }
  if (req.method !== "POST") return json({ fehler: "Methode" }, 405);
  let name = "", key = "", ts = 0;
  try { const d = await req.json(); name = String(d.name || "").trim().toLowerCase(); key = String(d.key || ""); ts = Number(d.ts) || 0; } catch (e) {}
  if (!/^@[a-z0-9._]{1,40}$/.test(name) || !ERLAUBT.has(key)) return json({ fehler: "Daten" }, 400);
  const jetzt = Date.now();
  if (!(ts >= 1 && ts <= jetzt)) ts = jetzt;
  const pre = "e/" + name.slice(1) + "/" + key + "/";
  const da = await store.list({ prefix: pre });
  if (da.blobs.length) return json({ ok: true, neu: false });
  await store.set(pre + ts, "1");
  return json({ ok: true, neu: true });
};

export const config = { path: "/api/erfolge" };
