// Muschel-Tal LIVE – Leuchtturm-Rennen: Städte erkennen, wenn jemand seine Stadt in den Chat schreibt.
// Nur echte Städte aus dieser Liste zählen (keine Fantasie- oder Schimpfwörter auf dem Bildschirm).
// Erkannt wird nur, wenn der Kommentar (fast) nur aus der Stadt besteht: „Köln“, „aus köln“, „Team Hamburg!“, „ich komme aus Wien 😊“.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const norm = t => String(t || '').toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss').replace(/[^a-z]+/g, ' ').trim();

const LISTE = `Berlin|Hamburg|München|Köln|Frankfurt am Main=Frankfurt|Stuttgart|Düsseldorf|Leipzig|Dortmund|Essen|Bremen|Dresden|Hannover|Nürnberg|Duisburg|Bochum|Wuppertal|Bielefeld|Bonn|Münster|Mannheim|Karlsruhe|Augsburg|Wiesbaden|Mönchengladbach|Gelsenkirchen|Aachen|Braunschweig|Kiel|Chemnitz|Halle (Saale)=Halle|Magdeburg|Freiburg im Breisgau=Freiburg|Krefeld|Mainz|Lübeck|Erfurt|Oberhausen|Rostock|Kassel|Hagen|Potsdam|Saarbrücken|Hamm|Ludwigshafen|Mülheim an der Ruhr=Mülheim|Oldenburg|Osnabrück|Leverkusen|Darmstadt|Heidelberg|Solingen|Herne|Neuss|Regensburg|Paderborn|Ingolstadt|Offenbach|Fürth|Würzburg|Ulm|Heilbronn|Pforzheim|Wolfsburg|Göttingen|Bottrop|Reutlingen|Koblenz|Bremerhaven|Recklinghausen|Erlangen|Bergisch Gladbach|Remscheid|Jena|Trier|Moers|Salzgitter|Siegen|Hildesheim|Gütersloh|Kaiserslautern|Cottbus|Witten|Hanau|Schwerin|Gera|Iserlohn|Ludwigsburg|Esslingen|Zwickau|Düren|Ratingen|Flensburg|Tübingen|Villingen-Schwenningen=Villingen|Konstanz|Marl|Worms|Lünen|Velbert|Minden|Dessau-Roßlau=Dessau|Neumünster|Norderstedt|Delmenhorst|Wilhelmshaven|Viersen|Gladbeck|Dorsten|Rheine|Detmold|Troisdorf|Castrop-Rauxel|Arnsberg|Marburg|Lüneburg|Bayreuth|Bamberg|Celle|Landshut|Aschaffenburg|Dinslaken|Brandenburg an der Havel=Brandenburg|Fulda|Aalen|Lippstadt|Plauen|Kempten|Rosenheim|Wesel|Neubrandenburg|Herford|Stralsund|Greifswald|Friedrichshafen|Sindelfingen|Offenburg|Göppingen|Hürth|Stolberg|Langenfeld|Schweinfurt|Wetzlar|Passau|Hameln|Frankfurt (Oder)=Frankfurt Oder|Goslar|Weimar|Freising|Speyer|Peine|Gießen|Neustadt an der Weinstraße=Neustadt|Landau|Bad Homburg|Euskirchen|Emden|Cuxhaven|Wismar|Lingen|Nordhorn|Stade|Kleve|Ahlen|Menden|Bocholt|Unna|Grevenbroich|Herten|Kerpen|Bergheim|Garbsen|Hattingen|Elmshorn|Pinneberg|Sylt|Westerland|Husum|Heide|Itzehoe|Rendsburg|Eckernförde|Schleswig|Kühlungsborn|Warnemünde|Binz|Zingst|Rügen|Usedom|Norderney|Borkum|Juist|Langeoog|Wangerooge|Fehmarn|Timmendorfer Strand=Timmendorf|Travemünde|Büsum|St. Peter-Ording|Wien|Graz|Linz|Salzburg|Innsbruck|Klagenfurt|Villach|Wels|St. Pölten|Dornbirn|Steyr|Feldkirch|Bregenz|Leoben|Kufstein|Zürich|Genf|Basel|Lausanne|Bern|Winterthur|Luzern|St. Gallen|Lugano|Biel|Thun|Schaffhausen|Chur|Zug|Fribourg|Neuenburg|Aarau|Baden|Luxemburg|Südtirol|Bozen|Meran|Mallorca|Kreuzberg|Neukölln|Spandau|Pankow|Altona|Wandsbek|Harburg|Ruhrgebiet|Sauerland|Allgäu|Schwarzwald|Ostfriesland|Eifel|Harz|Hallstatt|Wanne-Eickel|Bodensee|Nordsee|Ostsee|Bayern|Nordrhein-Westfalen=NRW|NRW|Niedersachsen|Hessen|Sachsen|Sachsen-Anhalt|Thüringen|Mecklenburg-Vorpommern=MV|Schleswig-Holstein|Rheinland-Pfalz|Saarland|Baden-Württemberg|Tirol|Kärnten|Steiermark|Vorarlberg|Burgenland|Oberösterreich|Niederösterreich|Österreich|Schweiz|Deutschland|Pott|Spreewald|Erzgebirge|Vogtland|Franken|Schwaben|Oberbayern|Emsland|Münsterland|Westerwald|Odenwald|Taunus|Rhön|Chiemsee|Zillertal|Ötztal`;

const FUELL = new Set(['ich', 'bin', 'komme', 'komm', 'aus', 'von', 'vom', 'wohne', 'in', 'im', 'team', 'stadt', 'gruesse', 'grusse', 'gruss', 'hallo', 'hi', 'hey', 'moin', 'liebe', 'lg', 'nach', 'fuer', 'go', 'los', 'mit', 'die', 'der', 'das', 'an', 'am', 'aus', 'bei', 'live', 'wir', 'sind']);
const schluessel = t => norm(t).split(' ').filter(x => x && !FUELL.has(x)).join(' ');
const ohneUmlaut = k => k.replace(/ae/g, 'a').replace(/oe/g, 'o').replace(/ue/g, 'u');   // „koln“, „munchen“, „zurich“
const STAEDTE = new Map();          // normalisierter Name/Alias → Anzeigename
for (const e of LISTE.split('|')) {
  const [anzeige, alias] = e.split('=');
  const name = (alias || anzeige).trim();
  for (const k of [schluessel(anzeige), schluessel(name)]) { STAEDTE.set(k, name); if (!STAEDTE.has(ohneUmlaut(k))) STAEDTE.set(ohneUmlaut(k), name); }
}

// Tippfehler: Damerau-Abstand (Vertauschen zählt als 1 Fehler: „hambrug“ → „hamburg“)
function abstand(a, b) {
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i]); for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) {
    d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
  }
  return d[a.length][b.length];
}
const KEYS = [...STAEDTE.keys()];          // Tippfehler-Erkennung nur für diese bekannten Städte

// Alle Orte in Deutschland, Österreich, Schweiz, Liechtenstein, Luxemburg (GeoNames, ca. 11.000 Städte, Gemeinden, Dörfer)
// Name wird gekürzt angezeigt: „Neustadt an der Weinstraße“ → „Neustadt“, „Halle (Saale)“ → „Halle“
const ORTE = new Map(), LAND = new Map(), INFO = new Map(), PRIO = new Map(), DIR = path.dirname(fileURLToPath(import.meta.url));
const kurz = n => n.split(/ (?:am|an|im|in|vor|ob|bei|auf)(?= )| \(|, | - |\//)[0].trim();
const ohneAkzent = t => t.normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
try {
  for (const z of fs.readFileSync(path.join(DIR, 'orte-dach.txt'), 'utf8').split('\n')) {
    const [n0, land, region, lat, lng] = z.split('\t'), n = (n0 || '').trim(); if (!n) continue; const k = kurz(n);
    const prio = (n === k ? 0 : 10) + ({ DE: 0, AT: 1, CH: 2, LU: 3, LI: 4 }[(land || '').trim()] ?? 5), alt = PRIO.get(k);
    if (alt == null || prio < alt) { PRIO.set(k, prio); if (land) LAND.set(k, land.trim()); if (lat) INFO.set(k, { region: region || '', lat: +lat, lng: +lng }); }
    for (const key of [schluessel(ohneAkzent(n)), schluessel(ohneAkzent(k))]) if (key && !STAEDTE.has(key) && !ORTE.has(key)) ORTE.set(key, k);
  }
} catch {}
// Ortsnamen, die auch normale Wörter sind („Sand“, „Wald“, „Berg“, „Laufen“): zählen nur mit „aus …“, „Team …“, „von …“
let MEHRDEUTIG = new Set();
try { MEHRDEUTIG = new Set(fs.readFileSync(path.join(DIR, 'orte-mehrdeutig.txt'), 'utf8').split('\n').map(x => x.trim()).filter(Boolean)); } catch {}
const ABSICHT = new Set(['aus', 'von', 'vom', 'team', 'stadt', 'wohne', 'komme', 'komm', 'gruesse', 'grusse', 'gruss']);
// Ähnliche Schreibweise: ab 6 Buchstaben 1 Fehler, ab 9 Buchstaben 2 Fehler – nur wenn genau EINE Stadt passt
function aehnlich(k) {
  if (k.length < 6 || ALLTAG.has(k)) return null;
  const max = k.length >= 9 ? 2 : 1, treffer = new Set();
  for (const s of KEYS) if (Math.abs(s.length - k.length) <= max && s[0] === k[0] && abstand(k, s) <= max) treffer.add(STAEDTE.get(s));
  return treffer.size === 1 ? [...treffer][0] : null;
}
// Alltagswörter, die wie Städte aussehen, nie umdeuten
const ALLTAG = new Set(['hallo', 'halloo', 'danke', 'schoen', 'schon', 'bitte', 'lieben', 'liebe', 'gruesse', 'haeuser', 'hause', 'zuhause', 'muschel', 'muscheln', 'strand', 'sommer', 'sonne', 'bremse', 'wiener', 'berliner', 'hamburger', 'kieler', 'koelner', 'essens', 'essen']);

// Gibt den Anzeigenamen der Stadt zurück – oder null
// streng = der Kommentar ist gerade auch eine Event-Antwort → kleine Orte nur mit „aus …“/„Team …“ zählen
const KEIN_ORT = new Set(['Deutschland', 'Österreich', 'Schweiz', 'Liechtenstein', 'Europa', 'Bayern', 'NRW', 'Niedersachsen', 'Hessen', 'Sachsen', 'Sachsen-Anhalt', 'MV', 'Mecklenburg-Vorpommern',
  'Schleswig-Holstein', 'Rheinland-Pfalz', 'Saarland', 'Baden-Württemberg', 'Thüringen', 'Tirol', 'Kärnten', 'Steiermark', 'Vorarlberg', 'Burgenland', 'Oberösterreich', 'Niederösterreich',
  'Südtirol', 'Mallorca', 'Aargau', 'Thurgau', 'Graubünden', 'Wallis', 'Tessin', 'Waadt', 'Nordsee', 'Ostsee',
  // Landschaften und Regionen sind keine Orte
  'Ruhrgebiet', 'Pott', 'Sauerland', 'Allgäu', 'Schwarzwald', 'Ostfriesland', 'Eifel', 'Harz', 'Bodensee', 'Spreewald', 'Erzgebirge', 'Vogtland', 'Franken', 'Schwaben',
  'Oberbayern', 'Emsland', 'Münsterland', 'Westerwald', 'Odenwald', 'Taunus', 'Rhön', 'Chiemsee', 'Zillertal', 'Ötztal', 'Rügen', 'Allgaeu']);
export const keinOrt = n => KEIN_ORT.has(n);
export function stadtAus(text, streng = false) { const r = stadtAus0(text, streng); return r && !KEIN_ORT.has(r) ? r : null; }
function stadtAus0(text, streng = false) {
  const alle = norm(ohneAkzent(String(text || ''))).split(' ').filter(Boolean), absicht = alle.some(x => ABSICHT.has(x));
  const w = alle.filter(x => !FUELL.has(x));
  if (w.length >= 2 && w.every(x => x === w[0])) w.length = 1;   // „berlin berlin“
  if (!w.length || w.length > 4) return null;
  const k = w.join(' ');
  const gross = STAEDTE.get(k) || (w.length > 1 ? STAEDTE.get(w[0]) && w.slice(1).every(x => x.length <= 2) ? STAEDTE.get(w[0]) : null : null);
  if (gross) return gross;
  // alle anderen Orte: exakt (Tippfehler nur bei den bekannten Städten), bei Allerweltswörtern nur mit Absicht
  const ort = ORTE.get(k);
  if (ort && ((!MEHRDEUTIG.has(k) && k.length >= 3 && !streng) || absicht)) return ort;
  const r = (w.length === 1 && !streng ? aehnlich(k) : null) || null;
  if (!r && /ae|oe|ue/.test(k)) return stadtAus0((absicht ? 'aus ' : '') + k.replace(/ae/g, 'a').replace(/oe/g, 'o').replace(/ue/g, 'u'), streng);   // „Toelz“ = „Tölz“
  return r;
}

// Land eines Ortes (DE, AT, CH, LI, LU) – für das Länder-Duell. Bekannte Regionen/Länder ohne Eintrag: geschätzt.
const LAND_EXTRA = { Wien: 'AT', 'St. Pölten': 'AT', Tirol: 'AT', Kärnten: 'AT', Steiermark: 'AT', Vorarlberg: 'AT', Burgenland: 'AT', Oberösterreich: 'AT', Niederösterreich: 'AT', Österreich: 'AT', Zillertal: 'AT', Ötztal: 'AT', Hallstatt: 'AT',
  Schweiz: 'CH', 'St. Gallen': 'CH', Genf: 'CH', Neuenburg: 'CH', Luxemburg: 'LU', Südtirol: 'IT', Bozen: 'IT', Meran: 'IT', Mallorca: 'ES' };
// Bundesland/Kanton und Lage (für Nachbar-Duell und Bundesland-Wertung)
const I = (region, lat, lng, land = 'DE') => ({ region, lat, lng, land });
const INFO_EXTRA = { Münster: I('NRW', 51.962, 7.626), Essen: I('NRW', 51.457, 7.012), Halle: I('Sachsen-Anhalt', 51.482, 11.97), Freiburg: I('Baden-Württemberg', 47.999, 7.842), Oberhausen: I('NRW', 51.47, 6.852),
  Hagen: I('NRW', 51.36, 7.474), Hamm: I('NRW', 51.681, 7.816), Mülheim: I('NRW', 51.432, 6.882), Oldenburg: I('Niedersachsen', 53.144, 8.214), Offenbach: I('Hessen', 50.1, 8.766), Fürth: I('Bayern', 49.477, 10.989),
  Koblenz: I('Rheinland-Pfalz', 50.357, 7.589), Esslingen: I('Baden-Württemberg', 48.74, 9.31), Stolberg: I('NRW', 50.771, 6.229), Langenfeld: I('NRW', 51.108, 6.948), Neustadt: I('Rheinland-Pfalz', 49.35, 8.138),
  Landau: I('Rheinland-Pfalz', 49.198, 8.116), Bergheim: I('NRW', 50.955, 6.639), Husum: I('Schleswig-Holstein', 54.477, 9.052), Harburg: I('Hamburg', 53.46, 9.98),
  Linz: I('Oberösterreich', 48.306, 14.286, 'AT'), Baden: I('Niederösterreich', 48.005, 16.233, 'AT'), Zürich: I('Zürich', 47.377, 8.54, 'CH'), Graz: I('Steiermark', 47.071, 15.439, 'AT'), Salzburg: I('Salzburg', 47.8, 13.044, 'AT'), Innsbruck: I('Tirol', 47.263, 11.394, 'AT'), Bern: I('Bern', 46.948, 7.447, 'CH'), Basel: I('Basel-Stadt', 47.558, 7.587, 'CH'), Luzern: I('Luzern', 47.05, 8.309, 'CH'),
  München: I('Bayern', 48.137, 11.575), Nürnberg: I('Bayern', 49.452, 11.077), Frankfurt: I('Hessen', 50.11, 8.682), 'Frankfurt Oder': I('Brandenburg', 52.347, 14.551), Villingen: I('Baden-Württemberg', 48.06, 8.459),
  Greifswald: I('Mecklenburg-Vorpommern', 54.093, 13.387), Stade: I('Niedersachsen', 53.6, 9.476), Sylt: I('Schleswig-Holstein', 54.9, 8.33), Kühlungsborn: I('Mecklenburg-Vorpommern', 54.15, 11.76), Rügen: I('Mecklenburg-Vorpommern', 54.42, 13.4),
  Wangerooge: I('Niedersachsen', 53.79, 7.9), Timmendorf: I('Schleswig-Holstein', 53.99, 10.78), 'St. Peter-Ording': I('Schleswig-Holstein', 54.3, 8.64), Wien: I('Wien', 48.208, 16.373), 'St. Pölten': I('Niederösterreich', 48.204, 15.626),
  Genf: I('Genf', 46.204, 6.143), 'St. Gallen': I('St. Gallen', 47.424, 9.377), Hallstatt: I('Oberösterreich', 47.562, 13.649), 'Wanne-Eickel': I('NRW', 51.53, 7.16), Bozen: I('Südtirol', 46.498, 11.354), Meran: I('Südtirol', 46.67, 11.16), Südtirol: I('Südtirol', 46.6, 11.3),
  Ruhrgebiet: I('NRW', 51.47, 7.2), Pott: I('NRW', 51.47, 7.2), Sauerland: I('NRW', 51.2, 8.1), Münsterland: I('NRW', 51.9, 7.5), Eifel: I('Rheinland-Pfalz', 50.3, 6.7), Westerwald: I('Rheinland-Pfalz', 50.6, 7.9), Allgäu: I('Bayern', 47.7, 10.3), Franken: I('Bayern', 49.6, 10.8), Oberbayern: I('Bayern', 47.9, 11.6), Chiemsee: I('Bayern', 47.87, 12.43), Schwaben: I('Baden-Württemberg', 48.5, 9.6),
  Schwarzwald: I('Baden-Württemberg', 48.1, 8.2), Bodensee: I('Baden-Württemberg', 47.6, 9.4), Odenwald: I('Hessen', 49.65, 8.95), Taunus: I('Hessen', 50.25, 8.4), Rhön: I('Hessen', 50.45, 9.95), Ostfriesland: I('Niedersachsen', 53.4, 7.5), Emsland: I('Niedersachsen', 52.8, 7.4), Harz: I('Sachsen-Anhalt', 51.75, 10.7),
  Spreewald: I('Brandenburg', 51.85, 14.0), Erzgebirge: I('Sachsen', 50.6, 13.0), Vogtland: I('Sachsen', 50.45, 12.2), Zillertal: I('Tirol', 47.2, 11.87), Ötztal: I('Tirol', 47.1, 10.95),
  Bayern: I('Bayern', 48.8, 11.5), NRW: I('NRW', 51.5, 7.5), Niedersachsen: I('Niedersachsen', 52.6, 9.5), Hessen: I('Hessen', 50.6, 9.0), 'Sachsen-Anhalt': I('Sachsen-Anhalt', 51.9, 11.7), MV: I('Mecklenburg-Vorpommern', 53.8, 12.5),
  'Schleswig-Holstein': I('Schleswig-Holstein', 54.2, 9.8), 'Rheinland-Pfalz': I('Rheinland-Pfalz', 49.9, 7.4), Saarland: I('Saarland', 49.4, 6.95), 'Baden-Württemberg': I('Baden-Württemberg', 48.6, 9.0),
  Tirol: I('Tirol', 47.25, 11.4), Kärnten: I('Kärnten', 46.7, 13.9), Steiermark: I('Steiermark', 47.2, 15.0), Vorarlberg: I('Vorarlberg', 47.25, 9.9), Burgenland: I('Burgenland', 47.5, 16.5), Oberösterreich: I('Oberösterreich', 48.1, 14.0), Niederösterreich: I('Niederösterreich', 48.3, 15.8),
  Luxemburg: I('Luxemburg', 49.61, 6.13) };
const REGION_EXTRA = { Tirol: 'Tirol', Kärnten: 'Kärnten', Steiermark: 'Steiermark', Vorarlberg: 'Vorarlberg', Burgenland: 'Burgenland', Oberösterreich: 'Oberösterreich', Niederösterreich: 'Niederösterreich', Bayern: 'Bayern', Sachsen: 'Sachsen', Hessen: 'Hessen', Thüringen: 'Thüringen', NRW: 'NRW' };
export function infoVon(name) { if (INFO_EXTRA[name]) { const { land, ...r } = INFO_EXTRA[name]; return r; } return INFO.get(name) || (REGION_EXTRA[name] ? { region: REGION_EXTRA[name], lat: null, lng: null } : { region: '', lat: null, lng: null }); }
export function landVon(name) { return LAND_EXTRA[name] || INFO_EXTRA[name]?.land || LAND.get(name) || 'DE'; }
