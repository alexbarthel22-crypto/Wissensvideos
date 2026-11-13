// Muschel-Konten: Namen beanspruchen, Kontobuch, Login-Serie, Aufgaben, schwebende Muscheln, Spenden.
// Jede Buchung ist ein eigener Eintrag mit festem Schlüssel "b/<name>/<art>/<kennung>/<betrag>" – der Betrag steht im Schlüssel,
// so ergibt sich der Kontostand aus einer einzigen Liste. Feste Schlüssel (z. B. login/2026-11-10) verhindern Doppelbuchungen.
import { getStore } from "@netlify/blobs";
import { JOBS } from "../lib/jobs.mjs";

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
const RESET = [["leamickunnnn", 1], ...["marina.cgnn", "ju1e_smt", "mimposible", "maja.gnw", "eeli_mxo", "luna.gsn02", "toca_lexi00"].map(n => [n, 1, TEST_12_11])];
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
const ZURUECK = [["toca_lexi00", 1, HEUTE_9]];
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
const TEXT = { login: "Login-Serie", quest: "Aufgabe", qbonus: "Alle 3 Aufgaben", shell: "Schwebende Muschel", erf: "Neuer Erfolg", story: "Story geteilt", spende: "Spende Inselkasse" };

export default async (req) => {
  const store = getStore({ name: "muscheln", consistency: "strong" });
  await zuruecksetzen(store);
  await zurueckAuf(store);
  const url = new URL(req.url);
  if (req.method === "GET" && url.searchParams.get("top")) {
    // Muschel-Rangliste: Top 10 der beanspruchten Namen nach Kontostand, Pfeile im Vergleich zu gestern, optional eigener Platz
    const claimed = new Set((await liste(store, "c/")).map(k => k.slice(2)));
    const sum = {};
    for (const k of await liste(store, "b/")) { const [, n, , , a] = k.split("/"); if (claimed.has(n)) sum[n] = (sum[n] || 0) + (Number(a) || 0); }
    const order = Object.entries(sum).filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1));
    const heute = tag(), key = "r/" + heute;
    if (!(await store.get(key))) await store.set(key, JSON.stringify(order.slice(0, 50).map(x => x[0])));
    const vor = JSON.parse((await store.get("r/" + gestern(heute))) || "null");
    const top = order.slice(0, 10).map(([n, v], i) => { const j = vor ? vor.indexOf(n) : -1; return { n: "@" + n, stand: v, d: vor ? (j < 0 ? "neu" : j - i) : null }; });
    const me = (url.searchParams.get("name") || "").trim().toLowerCase().replace(/^@/, "");
    let platz = null, stand = null;
    if (me) { const i = order.findIndex(x => x[0] === me); if (i >= 0) { platz = i + 1; stand = order[i][1]; } }
    const bis10 = platz && platz > 10 && top[9] ? top[9].stand - stand + 1 : null;
    return json({ top, platz, stand, bis10, anzahl: order.length });
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
  if (!NAME.test(name)) return json({ fehler: "Name" }, 400);
  const nm = name.slice(1), heute = tag();

  if (act === "claim") {
    if (await store.get("c/" + nm)) return json({ ok: false, beansprucht: true });
    const token = crypto.randomUUID() + "-" + crypto.randomUUID();
    await store.set("c/" + nm, JSON.stringify({ h: await sha(token), ts: Date.now() }));
    // bei gleichzeitigem Beanspruchen gewinnt, wessen Eintrag gespeichert blieb
    await new Promise(r => setTimeout(r, 300));
    const c = JSON.parse((await store.get("c/" + nm)) || "{}");
    if (c.h !== (await sha(token))) return json({ ok: false, beansprucht: true });
    return json({ ok: true, token });
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
  if (act === "stand") {
    const B = await buch(store, nm), s = await serie(B);
    const posten = B.filter(e => e.a).map(e => ({ art: e.art, id: e.id, a: e.a, t: TEXT[e.art] || e.art }))
      .sort((x, y) => (y.id > x.id ? 1 : -1)).slice(0, 60);
    return json({
      ok: true, stand: B.reduce((s, e) => s + e.a, 0), serie: s,
      shells: B.filter(e => e.art === "shell" && e.id.startsWith(heute)).map(e => Number(e.id.split("-").pop())),
      questsDone: B.filter(e => e.art === "quest" && e.id.startsWith(heute)).map(e => Number(e.id.split("-").pop())),
      gespendet: -B.filter(e => e.art === "spende").reduce((s, e) => s + e.a, 0), posten, heute
    });
  }
  return json({ fehler: "Aktion" }, 400);
};

export const config = { path: "/api/muscheln" };
