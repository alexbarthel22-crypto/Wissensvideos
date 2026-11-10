// Inselkasse: +50 Muscheln, wenn jemand seinen Muschelpass in der Story teilt (pro TikTok-Name alle 7 Tage).
// Sicher gegen Verluste und Doppelbuchungen: Jede Buchung ist ein eigener, unveränderlicher Eintrag im Kontobuch
// ("b/<name>/<zeit>-<zufall>"); es wird kein Zähler überschrieben. Der Kassenstand ist die Summe aller gültigen Einträge.
// Gültig ist pro Name höchstens eine Buchung je 7 Tage (bei gleichzeitigen Anfragen gewinnt die früheste, die andere wird verworfen).
import { getStore } from "@netlify/blobs";

const WOCHE = 7 * 24 * 60 * 60 * 1000, BONUS = 50;
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const NAME = /^@[a-z0-9._]{1,40}$/;

async function liste(store, prefix) {
  const out = [];
  let cursor;
  do { const r = await store.list({ prefix, cursor }); out.push(...r.blobs.map(b => b.key)); cursor = r.cursor; } while (cursor);
  return out;
}
// gültige Buchungen je Name: zeitlich sortiert, jede mindestens 7 Tage nach der vorigen gültigen (inkl. Altbestand aus dem früheren System)
function gueltig(keys, alt) {
  const je = {};
  for (const k of keys) { const [, n, z] = k.split("/"); const ts = Number(String(z).split("-")[0]); if (!(ts > 0)) continue; (je[n] = je[n] || []).push({ k, ts }); }
  const ok = {};
  for (const [n, L] of Object.entries(je)) {
    L.sort((a, b) => a.ts - b.ts || (a.k < b.k ? -1 : 1));
    let last = alt[n] || 0; ok[n] = [];
    for (const e of L) if (!last || e.ts - last >= WOCHE) { ok[n].push(e); last = e.ts; }
  }
  return ok;
}

export default async (req) => {
  const store = getStore({ name: "inselkasse", consistency: "strong" });
  // Altbestand: bisheriger Zähler (bleibt unverändert als Sockel) und die alten "zuletzt geteilt"-Zeiten
  const alt = (await store.get("stand", { type: "json" })) || { bonus: 0 };
  const altZeit = async n => Number(await store.get("geteilt/" + n)) || 0;
  const summe = async () => { const ok = gueltig(await liste(store, "b/"), {}); let c = 0; for (const L of Object.values(ok)) c += L.length; return (alt.bonus || 0) + c * BONUS; };

  if (req.method === "GET") {
    const n = (new URL(req.url).searchParams.get("name") || "").trim().toLowerCase();
    const bonus = await summe();
    if (NAME.test(n)) {
      const nm = n.slice(1), a = await altZeit(nm), ok = gueltig(await liste(store, "b/" + nm + "/"), { [nm]: a })[nm] || [];
      const z = Math.max(a, ok.length ? ok[ok.length - 1].ts : 0);
      return json({ bonus, naechstes: z ? z + WOCHE : 0 });
    }
    return json({ bonus });
  }
  if (req.method !== "POST") return json({ fehler: "Methode" }, 405);
  let name = "";
  try { name = String((await req.json()).name || "").trim().toLowerCase(); } catch (e) {}
  if (!NAME.test(name)) return json({ fehler: "Name" }, 400);
  const nm = name.slice(1), jetzt = Date.now(), a = await altZeit(nm);
  const vorher = gueltig(await liste(store, "b/" + nm + "/"), { [nm]: a })[nm] || [];
  const zuletzt = Math.max(a, vorher.length ? vorher[vorher.length - 1].ts : 0);
  if (zuletzt && jetzt - zuletzt < WOCHE) return json({ ok: false, bonus: await summe(), naechstes: zuletzt + WOCHE });
  // eigener Eintrag (eindeutiger Schlüssel), danach prüfen, ob er gilt – bei gleichzeitigen Anfragen gewinnt die früheste
  const key = "b/" + nm + "/" + jetzt + "-" + Math.random().toString(36).slice(2, 10);
  await store.set(key, "1");
  await new Promise(r => setTimeout(r, 300)); // gleichzeitige Anfragen erst fertig schreiben lassen, dann entscheiden
  const nachher = gueltig(await liste(store, "b/" + nm + "/"), { [nm]: a })[nm] || [];
  const gilt = nachher.some(e => e.k === key);
  if (!gilt) { try { await store.delete(key); } catch (e) {} }
  const letzte = nachher.length ? nachher[nachher.length - 1].ts : zuletzt;
  return json({ ok: gilt, bonus: await summe(), naechstes: letzte + WOCHE });
};

export const config = { path: "/api/kasse" };
