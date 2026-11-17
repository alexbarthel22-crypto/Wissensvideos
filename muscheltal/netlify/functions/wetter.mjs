// Wetter für die Karte über den eigenen Server (statt direkt aus dem Browser): Die IP-Adresse der Besucher geht so nicht an den Wetterdienst.
// Ergebnis wird 15 Minuten zwischengespeichert (im Speicher und im Netlify-CDN).
let CACHE = { t: 0, k: "", d: null };
export default async (req) => {
  const u = new URL(req.url), lat = Number(u.searchParams.get("lat")) || 51.16, lon = Number(u.searchParams.get("lon")) || 10.45;
  const k = lat.toFixed(2) + "," + lon.toFixed(2);
  if (!(CACHE.d && CACHE.k === k && Date.now() - CACHE.t < 9e5)) {
    try {
      const r = await fetch("https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon + "&current=weather_code,wind_speed_10m&daily=sunrise,sunset&hourly=precipitation&past_hours=3&forecast_hours=1&timezone=GMT&forecast_days=1");
      if (r.ok) CACHE = { t: Date.now(), k, d: await r.text() };
    } catch (e) {}
  }
  return new Response(CACHE.d || "{}", { status: CACHE.d ? 200 : 502, headers: { "content-type": "application/json", "cache-control": "public, max-age=600", "netlify-cdn-cache-control": "public, max-age=900" } });
};
export const config = { path: "/api/wetter" };
