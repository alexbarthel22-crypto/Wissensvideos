// Muschel-Tal LIVE – Schutz vor anstößigen Namen.
// 1. Namen mit anstößigen Wörtern werden anonymisiert („Bewohner 12“): nicht angezeigt, nicht vorgelesen.
// 2. Namen aus sperrliste.txt werden komplett ignoriert (kein Haus, keine Begrüßung, kein Dank).
// Kommentar-Texte werden grundsätzlich nie vorgelesen oder angezeigt.
import fs from 'node:fs';
import path from 'node:path';

const LEET = { '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '8': 'b', '@': 'a', '$': 's', '!': 'i', '|': 'i' };
export function normal(s) {
  return String(s || '').toLowerCase()
    .replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss')
    .replace(/[0134578@$!|]/g, c => LEET[c])
    .replace(/[^a-z]/g, '')
    .replace(/(.)\1+/g, '$1');                         // „fuuuck“ → „fuck“
}

// Wortstämme (werden auch mitten im Namen erkannt). Lieber einmal zu viel anonymisieren als einmal zu wenig.
const WOERTER = [
  // Beleidigungen / Vulgäres (deutsch)
  'fotze', 'hurensohn', 'hure', 'wichser', 'wixer', 'schlampe', 'nute', 'arsch', 'missgeburt', 'spast', 'behindert', 'mongo',
  'schwuchtel', 'kanake', 'kanacke', 'fick', 'titen', 'muschi', 'pimel', 'schwanz', 'scheis', 'kacke', 'pisser', 'drecksau', 'bastard',
  'vergewalt', 'selbstmord', 'umbringen', 'abstechen', 'opfa', 'dumbitch',
  // englisch
  'fuck', 'fuk', 'fack', 'shit', 'bitch', 'cunt', 'dick', 'cock', 'pusy', 'penis', 'vagina', 'boob', 'tits', 'slut', 'whore', 'porn', 'sex', 'anal',
  'blowjob', 'cum', 'rape', 'faggot', 'fag', 'retard', 'killyourself', 'suicide', 'motherf', 'asshole', 'nude', 'naked', 'horny', 'onlyfans',
  // Hass / Extremismus
  'nazi', 'hitler', 'siegheil', 'heilhitler', 'judensau', 'nigger', 'niger', 'niga', 'kkk', 'isis', 'terror', 'holocaust', 'aryan',
  // Drogen
  'cocain', 'kokain', 'heroin', 'meth', 'crack',
].map(normal);

// Harmlose Wörter, die eins der obigen enthalten (werden vor der Prüfung entfernt)
const AUSNAHMEN = ['kanal', 'analys', 'marsch', 'dickens', 'sussex', 'essex', 'documen', 'cucumber', 'cocktail', 'peacock', 'hancock', 'heilig', 'heilbron',
  'scheibe', 'methode', 'something', 'cumulus', 'circum', 'siegfried', 'siegmund', 'siegen', 'sieger', 'nugget', 'nigeria', 'meteor',
  'methan', 'crackers', 'dickie', 'annalena', 'analena', 'minute', 'banal', 'fagot', 'fackel', 'nachbarschaft', 'bikini', 'barsch', 'karsch'].map(normal);

export function anstoessig(text) {
  let n = normal(text);
  for (const a of AUSNAHMEN) n = n.split(a).join('_');
  return WOERTER.some(w => w.length >= 3 && n.includes(w));
}

// ---------- Sperrliste (sperrliste.txt, ein Name pro Zeile, ohne @) ----------
let SPERRE = new Set();
export function ladeSperrliste(dir) {
  const f = path.join(dir, 'sperrliste.txt');
  try {
    SPERRE = new Set(fs.readFileSync(f, 'utf8').split('\n').map(z => z.replace(/#.*/, '').trim().replace(/^@/, '').toLowerCase()).filter(Boolean));
  } catch { SPERRE = new Set(); }
  return SPERRE;
}
export const gesperrt = uniqueId => SPERRE.has(String(uniqueId || '').replace(/^@/, '').toLowerCase());
// Ganze Sätze: jedes Wort einzeln prüfen (sonst Fehlalarme über Wortgrenzen, z. B. „Flasche ist“)
export const satzAnstoessig = text => String(text || '').split(/\s+/).some(w => w.length > 2 && anstoessig(w));
