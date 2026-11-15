// Leuchtturm-Rennen – was Leda sagt. Kurze Sätze, mehrere Varianten. Platzhalter: {name} {stadt} {zweite} {zahl} {was}
// Wichtig (TikTok-Regeln): nie zu Herzen/Folgen/Teilen/Geschenken auffordern, nie Belohnungen dafür versprechen.
const SAETZE = {
  start: [
    'Willkommen beim Leuchtturm-Rennen! … Schreibt eure Stadt in den Chat!',
    'Das Leuchtturm-Rennen geht los! … Welche Stadt baut den höchsten Leuchtturm?',
  ],
  erklaeren: [
    'Schreibt eure Stadt in den Chat, dann bekommt sie eine eigene Insel mit Leuchtturm!',
    'Jeder Kommentar macht den Leuchtturm eurer Stadt einen Meter höher!',
    'Welche Stadt baut den höchsten Leuchtturm? … Schreibt eure Stadt in den Chat!',
    'Dorf, Stadt oder Gemeinde, alles zählt! … Schreibt einfach euren Ort in den Chat.',
    'Holt eure Freunde aus eurer Stadt dazu, zusammen wächst der Leuchtturm schneller!',
    'Schreibt ein Herz-Emoji in den Chat, jedes Herz bringt eurer Stadt einen Meter!',
    'Schreibt das Päckchen-Emoji in den Chat, das ist ein Mega-Bauschub für eure Stadt!',
    'Wer seine Stadt als Erstes schreibt, wird Gründer und steht für immer am Leuchtturm!',
  ],
  bauschub: [
    'Mega-Bauschub für {stadt}!',
    'Bauschub! … {stadt} schießt in die Höhe!',
    '{stadt} wächst und wächst!',
  ],
  neueStadt: [
    'Eine neue Insel für {stadt}!',
    '{stadt} ist dabei! … Der erste Stein liegt.',
    'Willkommen im Rennen, {stadt}!',
  ],
  neueStadtName: [
    '{name} holt {stadt} ins Rennen!',
    '{name} baut die erste Insel für {stadt}!',
  ],
  fuehrung: [
    '{stadt} übernimmt die Führung!',
    'Wechsel an der Spitze! … {stadt} führt jetzt!',
    '{stadt} überholt {zweite}!',
  ],
  upgrade: [
    '{stadt} hat jetzt {was} am Leuchtturm!',
    'Neu bei {stadt}: {was}!',
  ],
  fieber: [
    '{stadt} hat das Städte-Fieber! … Jetzt zählt alles doppelt!',
    'Städte-Fieber in {stadt}! … Doppelte Meter!',
  ],
  meilenstein: [
    '{stadt} knackt {zahl} Meter!',
    '{zahl} Meter für {stadt}! … Wahnsinn!',
  ],
  danke: [
    'Danke, {name}!',
    'Danke dir, {name}!',
  ],
  followEins: [
    'Danke fürs Folgen, {name}!',
    'Schön, dass du da bist, {name}!',
  ],
  teilen: [
    'Danke fürs Teilen, {name}!',
  ],
  begruessungEins: [
    'Hallo {name}!',
    'Willkommen, {name}!',
    'Hey {name}! … Aus welcher Stadt kommst du?',
  ],
  begruessungZurueck: [
    'Schön, dass du wieder da bist, {name}!',
    'Willkommen zurück, {name}!',
  ],
  begruessungStadt: [
    'Willkommen zurück, {name} aus {stadt}!',
    'Hallo {name}! … {stadt} braucht dich!',
  ],
  countdown30: [
    'In dreißig Sekunden kommt das nächste Event!',
    'Gleich geht es los … noch dreißig Sekunden!',
  ],
  countdown10: [
    'Noch zehn Sekunden!',
  ],
  eventNoch10: [
    'Noch zehn Sekunden!',
  ],
  tagessieger: [
    '{stadt} ist die Stadt des Tages!',
    'Heute hat {stadt} am meisten gebaut! … Stadt des Tages!',
  ],
};

const zuletzt = {};
export function satz(art, werte = {}) {
  const liste = SAETZE[art]; if (!liste) return '';
  const weg = zuletzt[art] || [];
  let frei = liste.map((_, i) => i).filter(i => !weg.includes(i));
  if (!frei.length) frei = liste.map((_, i) => i);
  const i = frei[Math.floor(Math.random() * frei.length)];
  zuletzt[art] = [i, ...weg].slice(0, Math.floor(liste.length / 2));
  return liste[i].replace(/\{(\w+)\}/g, (_, k) => werte[k] ?? '');
}
export const namenListe = n => n.length > 1 ? `${n.slice(0, -1).join(', ')} und ${n.at(-1)}` : n[0];
export const festeSaetzeAus = gruppen => gruppen.flatMap(g => SAETZE[g] || []).filter(t => !t.includes('{'));
export const festeSaetze = () => Object.values(SAETZE).flat().filter(t => !t.includes('{'));
