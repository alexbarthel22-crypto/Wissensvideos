// Sperre für muscheltal.de: Ohne Zugang sieht man nur „Bald verfügbar“ mit Link zum TikTok-Account.
// Mit dem Passwort (unten nur als SHA-256-Hash gespeichert) bekommt man ein Cookie und sieht die Seite normal.
// Zum Aufheben der Sperre: SPERRE = false setzen (oder den [[edge_functions]]-Eintrag in netlify.toml entfernen).
const SPERRE = true;
const PW_HASH = "e9a96d7241365aba4d836268a2097a9cf904137ee880c889571dbf0c1a4b7956";
const COOKIE = "mt_zugang";
const ACC = "muscheltal";

const sha = async (t) => [...new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)))].map((b) => b.toString(16).padStart(2, "0")).join("");
const gleich = (a, b) => { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; };

function seite(fehler) {
  return `<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Muschel-Tal – bald verfügbar</title><meta name="robots" content="noindex">
<style>
:root{--ink:#2a1b12;--sun:#ffd23f;--pink:#e8467c}
*{box-sizing:border-box}html,body{margin:0;min-height:100%}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:linear-gradient(160deg,#14b3c2,#07547a);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px 16px}
.k{background:#fff8e7;border:4px solid var(--ink);border-radius:28px;box-shadow:0 8px 0 var(--ink);max-width:420px;width:100%;padding:28px 22px 22px;text-align:center}
.logo{font-size:64px;line-height:1}
h1{margin:8px 0 2px;font-size:30px;font-weight:900;letter-spacing:.5px}
.by{font-weight:800;color:#7a5a2b;margin:0 0 18px}
.bald{display:inline-block;background:var(--sun);border:3px solid var(--ink);border-radius:999px;padding:6px 16px;font-weight:900;font-size:20px;margin-bottom:14px}
p{font-size:16px;line-height:1.45;margin:0 0 18px}
.btn{display:inline-block;background:var(--pink);color:#fff;text-decoration:none;font-weight:900;font-size:17px;border:3px solid var(--ink);border-radius:999px;padding:11px 20px;box-shadow:0 4px 0 var(--ink)}
details{margin-top:26px;font-size:13px;color:#8a7a60}summary{cursor:pointer;list-style:none}summary::-webkit-details-marker{display:none}
form{display:flex;gap:8px;margin-top:10px}input{flex:1;min-width:0;font:inherit;font-size:15px;padding:9px 12px;border:2px solid var(--ink);border-radius:12px}
button{font:inherit;font-weight:900;font-size:15px;padding:9px 14px;border:2px solid var(--ink);border-radius:12px;background:var(--sun);cursor:pointer}
.f{color:#c0392b;font-weight:800;margin-top:8px}
</style></head><body><main class="k">
<div class="logo">🐚</div><h1>MUSCHEL-TAL</h1><div class="by">by @${ACC}</div>
<div class="bald">✨ Bald verfügbar</div>
<p>Hier entsteht gerade etwas Neues. Folge <b>@${ACC}</b> auf TikTok, damit du nichts verpasst!</p>
<a class="btn" href="https://www.tiktok.com/@${ACC}" target="_blank" rel="noopener">➕ @${ACC} auf TikTok</a>
<details${fehler ? " open" : ""}><summary>Zugang</summary><form method="post" action="/zugang"><input type="password" name="pw" placeholder="Passwort" autocomplete="current-password" required><button type="submit">→</button></form>${fehler ? '<div class="f">Falsches Passwort</div>' : ""}</details>
</main></body></html>`;
}
const html = (body, status = 200, extra = {}) => new Response(body, { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", ...extra } });

export default async (req, context) => {
  if (!SPERRE) return context.next();
  const token = await sha(PW_HASH + ":zugang");
  const url = new URL(req.url);
  if (url.pathname === "/zugang" && req.method === "POST") {
    let pw = "";
    try { pw = String((await req.formData()).get("pw") || ""); } catch (e) {}
    if (gleich(await sha(pw), PW_HASH))
      return new Response(null, { status: 303, headers: { location: "/", "cache-control": "no-store", "set-cookie": `${COOKIE}=${token}; Path=/; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax` } });
    return html(seite(true), 401);
  }
  const m = (req.headers.get("cookie") || "").match(new RegExp("(?:^|;\\s*)" + COOKIE + "=([0-9a-f]{64})"));
  if (m && gleich(m[1], token)) {
    const r = await context.next();
    const h = new Headers(r.headers);
    h.set("cache-control", "private, no-store");
    return new Response(r.body, { status: r.status, statusText: r.statusText, headers: h });
  }
  if (url.pathname.startsWith("/api/") || url.pathname.startsWith("/.netlify/")) return new Response(JSON.stringify({ fehler: "Gesperrt" }), { status: 403, headers: { "content-type": "application/json", "cache-control": "no-store" } });
  return html(seite(false));
};

export const config = { path: "/*" };
