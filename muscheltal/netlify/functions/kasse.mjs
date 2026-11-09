// Inselkasse: +50 Muscheln, wenn jemand seinen Muschelpass in der Story teilt (pro TikTok-Name alle 7 Tage).
import { getStore } from "@netlify/blobs";

const WOCHE = 7 * 24 * 60 * 60 * 1000, BONUS = 50;
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export default async (req) => {
  const store = getStore("inselkasse");
  const stand = (await store.get("stand", { type: "json" })) || { bonus: 0, teilungen: 0 };
  if (req.method === "GET") {
    // mit ?name=@… zusätzlich: wann diese Person den nächsten Story-Bonus bekommen kann (geräteübergreifend)
    const n = (new URL(req.url).searchParams.get("name") || "").trim().toLowerCase();
    if (/^@[a-z0-9._]{1,40}$/.test(n)) { const z = Number(await store.get("geteilt/" + n.slice(1))) || 0; return json({ bonus: stand.bonus, naechstes: z ? z + WOCHE : 0 }); }
    return json({ bonus: stand.bonus });
  }
  if (req.method !== "POST") return json({ fehler: "Methode" }, 405);
  let name = "";
  try { name = String((await req.json()).name || "").trim().toLowerCase(); } catch (e) {}
  if (!/^@[a-z0-9._]{1,40}$/.test(name)) return json({ fehler: "Name" }, 400);
  const key = "geteilt/" + name.slice(1), jetzt = Date.now();
  const zuletzt = Number(await store.get(key)) || 0;
  if (jetzt - zuletzt < WOCHE) return json({ ok: false, bonus: stand.bonus, naechstes: zuletzt + WOCHE });
  await store.set(key, String(jetzt));
  stand.bonus += BONUS; stand.teilungen = (stand.teilungen || 0) + 1;
  await store.setJSON("stand", stand);
  return json({ ok: true, bonus: stand.bonus, naechstes: jetzt + WOCHE });
};

export const config = { path: "/api/kasse" };
