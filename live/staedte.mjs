// Muschel-Tal LIVE – Leuchtturm-Rennen: Städte erkennen, wenn jemand seine Stadt in den Chat schreibt.
// Nur echte Städte aus dieser Liste zählen (keine Fantasie- oder Schimpfwörter auf dem Bildschirm).
// Erkannt wird nur, wenn der Kommentar (fast) nur aus der Stadt besteht: „Köln“, „aus köln“, „Team Hamburg!“, „ich komme aus Wien 😊“.
const norm = t => String(t || '').toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss').replace(/[^a-z]+/g, ' ').trim();

const LISTE = `Berlin|Hamburg|München|Köln|Frankfurt am Main=Frankfurt|Stuttgart|Düsseldorf|Leipzig|Dortmund|Essen|Bremen|Dresden|Hannover|Nürnberg|Duisburg|Bochum|Wuppertal|Bielefeld|Bonn|Münster|Mannheim|Karlsruhe|Augsburg|Wiesbaden|Mönchengladbach|Gelsenkirchen|Aachen|Braunschweig|Kiel|Chemnitz|Halle (Saale)=Halle|Magdeburg|Freiburg im Breisgau=Freiburg|Krefeld|Mainz|Lübeck|Erfurt|Oberhausen|Rostock|Kassel|Hagen|Potsdam|Saarbrücken|Hamm|Ludwigshafen|Mülheim an der Ruhr=Mülheim|Oldenburg|Osnabrück|Leverkusen|Darmstadt|Heidelberg|Solingen|Herne|Neuss|Regensburg|Paderborn|Ingolstadt|Offenbach|Fürth|Würzburg|Ulm|Heilbronn|Pforzheim|Wolfsburg|Göttingen|Bottrop|Reutlingen|Koblenz|Bremerhaven|Recklinghausen|Erlangen|Bergisch Gladbach|Remscheid|Jena|Trier|Moers|Salzgitter|Siegen|Hildesheim|Gütersloh|Kaiserslautern|Cottbus|Witten|Hanau|Schwerin|Gera|Iserlohn|Ludwigsburg|Esslingen|Zwickau|Düren|Ratingen|Flensburg|Tübingen|Villingen-Schwenningen=Villingen|Konstanz|Marl|Worms|Lünen|Velbert|Minden|Dessau-Roßlau=Dessau|Neumünster|Norderstedt|Delmenhorst|Wilhelmshaven|Viersen|Gladbeck|Dorsten|Rheine|Detmold|Troisdorf|Castrop-Rauxel|Arnsberg|Marburg|Lüneburg|Bayreuth|Bamberg|Celle|Landshut|Aschaffenburg|Dinslaken|Brandenburg an der Havel=Brandenburg|Fulda|Aalen|Lippstadt|Plauen|Kempten|Rosenheim|Wesel|Neubrandenburg|Herford|Stralsund|Greifswald|Friedrichshafen|Sindelfingen|Offenburg|Göppingen|Hürth|Stolberg|Langenfeld|Schweinfurt|Wetzlar|Passau|Hameln|Frankfurt (Oder)=Frankfurt Oder|Goslar|Weimar|Freising|Speyer|Peine|Gießen|Neustadt an der Weinstraße=Neustadt|Landau|Bad Homburg|Euskirchen|Emden|Cuxhaven|Wismar|Lingen|Nordhorn|Stade|Kleve|Ahlen|Menden|Bocholt|Unna|Grevenbroich|Herten|Kerpen|Bergheim|Garbsen|Hattingen|Elmshorn|Pinneberg|Sylt|Westerland|Husum|Heide|Itzehoe|Rendsburg|Eckernförde|Schleswig|Kühlungsborn|Warnemünde|Binz|Zingst|Rügen|Usedom|Norderney|Borkum|Juist|Langeoog|Wangerooge|Fehmarn|Timmendorfer Strand=Timmendorf|Travemünde|Büsum|St. Peter-Ording|Wien|Graz|Linz|Salzburg|Innsbruck|Klagenfurt|Villach|Wels|St. Pölten|Dornbirn|Steyr|Feldkirch|Bregenz|Leoben|Kufstein|Zürich|Genf|Basel|Lausanne|Bern|Winterthur|Luzern|St. Gallen|Lugano|Biel|Thun|Schaffhausen|Chur|Zug|Fribourg|Neuenburg|Aarau|Baden|Luxemburg|Südtirol|Bozen|Meran|Mallorca|Kreuzberg|Neukölln|Spandau|Pankow|Altona|Wandsbek|Harburg|Ruhrgebiet|Sauerland|Allgäu|Schwarzwald|Ostfriesland|Eifel|Harz`;

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
const KEYS = [...STAEDTE.keys()];
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
export function stadtAus(text) {
  const w = norm(text).split(' ').filter(x => x && !FUELL.has(x));
  if (w.length >= 2 && w.every(x => x === w[0])) w.length = 1;   // „berlin berlin“
  if (!w.length || w.length > 4) return null;
  const k = w.join(' ');
  return STAEDTE.get(k) || (w.length > 1 ? STAEDTE.get(w[0]) && w.slice(1).every(x => x.length <= 2) ? STAEDTE.get(w[0]) : null : null)
    || (w.length === 1 ? aehnlich(k) : null) || null;
}
