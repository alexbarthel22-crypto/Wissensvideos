// Muschel-Pakete mit Echtgeld (Stripe Checkout).
// POST {act:"checkout", name, token, paket} → sichere Stripe-Bezahlseite (Kartendaten berühren muscheltal.de nie).
// POST von Stripe (Webhook, signiert) → Gutschrift erst nach bestätigter Zahlung; Erstattung/Rückbuchung zieht die Muscheln wieder ab.
// Geheime Schlüssel nur in Netlify (Umgebungsvariablen): STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET – nie im Code.
import { getStore } from "@netlify/blobs";
import { BEWOHNER } from "../lib/bewohner.mjs";

export const PAKETE = {
  p150: { cent: 199, muscheln: 180 },
  p250: { cent: 299, muscheln: 300 },
  p450: { cent: 499, muscheln: 540 },
  p800: { cent: 799, muscheln: 960 },
  p1100: { cent: 999, muscheln: 1320 },
  p1750: { cent: 1499, muscheln: 2100 },
  start: { cent: 399, muscheln: 665, einmal: true },// Startangebot: nur einmal je Name
};
const SEITE = "https://muscheltal.de";
const API = () => process.env.STRIPE_API_BASE || "https://api.stripe.com";
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const hex = (b) => [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join("");
async function sha(s) { return hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s))); }
async function hmac(key, msg) { const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]); return hex(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(msg))); }
const gleich = (a, b) => { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; };

// Stripe-Signatur prüfen (Header „Stripe-Signature: t=…,v1=…“, höchstens 5 Minuten alt)
async function signaturOk(roh, kopf, geheim) {
  if (!kopf || !geheim) return false;
  const teile = Object.fromEntries(kopf.split(",").map(x => x.split("=")).map(([k, ...v]) => [k, v.join("=")]));
  const v1 = kopf.split(",").filter(x => x.startsWith("v1=")).map(x => x.slice(3));
  const t = Number(teile.t);
  if (!t || Math.abs(Date.now() / 1000 - t) > 300 || !v1.length) return false;
  const soll = await hmac(geheim, t + "." + roh);
  return v1.some(s => gleich(s, soll));
}
// Buchung genau einmal (fester Schlüssel b/<name>/<art>/<kennung>/<betrag>, wie im Kontobuch der Muschel-Konten)
async function buchen(store, nm, art, id, betrag) {
  const pre = "b/" + nm + "/" + art + "/" + id + "/";
  if ((await store.list({ prefix: pre })).blobs.length) return false;
  await store.set(pre + betrag, String(Date.now()));
  return true;
}

export default async (req) => {
  if (req.method !== "POST") return json({ fehler: "Nur POST" }, 405);
  const store = getStore({ name: "muscheln", consistency: "strong" });
  const roh = await req.text();
  const sig = req.headers.get("stripe-signature");

  // --- Webhook von Stripe ---
  if (sig) {
    if (!(await signaturOk(roh, sig, process.env.STRIPE_WEBHOOK_SECRET))) return json({ fehler: "Signatur" }, 400);
    const ev = JSON.parse(roh), o = ev.data && ev.data.object || {};
    if ((ev.type === "checkout.session.completed" || ev.type === "checkout.session.async_payment_succeeded") && o.payment_status === "paid") {
      const nm = String((o.metadata && o.metadata.name) || "").toLowerCase(), p = PAKETE[o.metadata && o.metadata.paket];
      if (!nm || !p || o.amount_total !== p.cent) return json({ ok: false, grund: "daten" });
      await buchen(store, nm, "euro", o.id, p.muscheln);
      if (p.einmal) await store.set("x/start/" + nm, o.id);
      if (o.payment_intent) await store.set("x/euro/" + o.payment_intent, JSON.stringify({ nm, m: p.muscheln, cent: p.cent, sid: o.id }));
      return json({ ok: true });
    }
    // Erstattung oder Rückbuchung: Muscheln (anteilig) wieder abziehen – auch ins Minus
    if (ev.type === "charge.refunded" || ev.type === "charge.dispute.created") {
      const pi = o.payment_intent;
      const k = pi && JSON.parse((await store.get("x/euro/" + pi)) || "null");
      if (!k) return json({ ok: true, grund: "unbekannt" });
      const anteil = ev.type === "charge.refunded" ? Math.min(1, (o.amount_refunded || 0) / k.cent) : 1;
      const m = Math.round(k.m * anteil);
      if (m > 0) await buchen(store, k.nm, "euro-zurueck", pi, -m);
      return json({ ok: true });
    }
    return json({ ok: true, ignoriert: ev.type });
  }

  // --- Bezahlseite für einen Muschel-Paket-Kauf öffnen ---
  let d = {}; try { d = JSON.parse(roh || "{}"); } catch (e) {}
  if (d.act !== "checkout") return json({ fehler: "Aktion" }, 400);
  const name = String(d.name || "").trim().toLowerCase(), nm = name.replace(/^@/, "");
  if (!/^@[a-z0-9._]{1,40}$/.test(name) || !BEWOHNER.has(nm)) return json({ fehler: "Name" }, 400);
  const c = JSON.parse((await store.get("c/" + nm)) || "null");
  if (!c || c.h !== (await sha(String(d.token || "")))) return json({ fehler: "Nicht beansprucht" }, 403);
  const p = PAKETE[d.paket];
  if (!p) return json({ fehler: "Paket" }, 400);
  if (p.einmal && (await store.get("x/start/" + nm))) return json({ fehler: "Startangebot schon genutzt" }, 409);
  // Zustimmung zur sofortigen Ausführung + Kenntnis vom Verlust des Widerrufsrechts (§ 356 Abs. 5 BGB) ist Pflicht
  if (d.zustimmung !== true) return json({ fehler: "Zustimmung fehlt" }, 400);
  const zeit = new Date().toISOString();
  if (!process.env.STRIPE_SECRET_KEY) return json({ fehler: "Bezahlung noch nicht eingerichtet" }, 503);
  const f = new URLSearchParams({
    mode: "payment", locale: "de", submit_type: "pay",
    "line_items[0][quantity]": "1",
    "line_items[0][price_data][currency]": "eur",
    "line_items[0][price_data][unit_amount]": String(p.cent),
    "line_items[0][price_data][product_data][name]": p.muscheln.toLocaleString("de-DE") + " Muscheln – Muschel-Tal",
    "line_items[0][price_data][product_data][description]": "Virtuelle Muscheln für " + name + " (sofort gutgeschrieben, ohne Geldwert, nicht übertragbar)",
    client_reference_id: nm,
    "metadata[name]": nm, "metadata[paket]": d.paket,
    "payment_intent_data[metadata][name]": nm, "payment_intent_data[metadata][paket]": d.paket,
    "metadata[zustimmung]": zeit, "payment_intent_data[metadata][zustimmung]": zeit,
    "custom_text[submit][message]": "Du hast ausdrücklich verlangt, dass wir vor Ablauf der Widerrufsfrist mit der Ausführung beginnen (sofortige Gutschrift), und bestätigt, dass du dadurch dein Widerrufsrecht verlierst. Es gelten unsere AGB: muscheltal.de/agb.html",
    // Bestätigung auf dauerhaftem Datenträger: Rechnung per E-Mail mit Vertragsinhalt und Zustimmung (§ 312f Abs. 3 BGB)
    "invoice_creation[enabled]": "true",
    "invoice_creation[invoice_data][description]": p.muscheln.toLocaleString("de-DE") + " Muscheln (virtuelle Spielwährung) für das Muschel-Konto " + name + " auf muscheltal.de – sofort gutgeschrieben.",
    "invoice_creation[invoice_data][custom_fields][0][name]": "Muschel-Konto",
    "invoice_creation[invoice_data][custom_fields][0][value]": name,
    "invoice_creation[invoice_data][footer]": "Bestätigung: Du hast am " + zeit.slice(0, 10) + " ausdrücklich verlangt, dass wir vor Ablauf der Widerrufsfrist mit der Ausführung des Vertrags beginnen (sofortige Gutschrift der Muscheln), und bestätigt, dass du dadurch mit Beginn der Ausführung dein Widerrufsrecht verlierst. Das Widerrufsrecht ist mit der Gutschrift erloschen (§ 356 Abs. 5 BGB). Muscheln haben keinen Geldwert und sind nicht übertragbar. Es gelten die AGB mit Widerrufsbelehrung: https://muscheltal.de/agb.html – Alcaba UG (haftungsbeschränkt), Grelckstr. 23a, 22529 Hamburg, HRB 180374, USt-IdNr. DE351239794.",
    success_url: SEITE + "/?kauf=ok",
    cancel_url: SEITE + "/?kauf=abbruch",
  });
  const r = await fetch(API() + "/v1/checkout/sessions", { method: "POST", headers: { authorization: "Bearer " + process.env.STRIPE_SECRET_KEY, "content-type": "application/x-www-form-urlencoded" }, body: f });
  const s = await r.json().catch(() => ({}));
  if (!r.ok || !s.url) return json({ fehler: "Stripe", info: s.error && s.error.message }, 502);
  return json({ ok: true, url: s.url });
};
export const config = { path: "/api/stripe" };
