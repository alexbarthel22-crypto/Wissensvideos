// Leuchtturm-Rennen – was Leda sagt. Kurze Sätze, mehrere Varianten. Platzhalter: {name} {stadt} {zweite} {zahl} {was}
// Wichtig (TikTok-Regeln): nie zu Herzen/Folgen/Teilen/Geschenken auffordern, nie Belohnungen dafür versprechen.
const SAETZE = {
  start: [
    'Willkommen beim Leuchtturm-Rennen! … Schreibt eure Stadt in den Chat!',
    'Das Leuchtturm-Rennen geht los! … Welche Stadt baut den höchsten Leuchtturm?',
  ],
  erklaeren: [
    'Schreibt eure Stadt in den Chat, dann bekommt sie eine eigene Insel mit Leuchtturm!',
    'Jedes Mal, wenn ihr eure Stadt in den Chat schreibt, wächst ihr Leuchtturm um einen Meter!',
    'Ihr könnt auch andere Städte schreiben! … Jede Stadt, die ihr schreibt, wächst einen Meter!',
    'Schreibt eure Stadt, immer wieder! … Jedes Mal ein Meter mehr!',
    'Welche Stadt baut den höchsten Leuchtturm? … Schreibt eure Stadt in den Chat!',
    'Dorf, Stadt oder Gemeinde, alles zählt! … Schreibt einfach euren Ort in den Chat.',
    'Holt eure Freunde aus eurer Stadt dazu, zusammen wächst der Leuchtturm schneller!',
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
  platzZwei: [
    '{stadt} überholt {zweite}! … Jetzt auf Platz zwei!',
    '{stadt} springt auf Platz zwei!',
  ],
  platzDrei: [
    '{stadt} überholt {zweite} und ist jetzt Dritter!',
    '{stadt} klettert auf Platz drei!',
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
    'Danke fürs Teilen, {name}! … Schreib deine Stadt, dann bekommt ihr Turm einen Bonus!',
  ],
  teilenStadt: [
    'Danke fürs Teilen, {name}! … Ein Bonus für den Turm von {stadt}!',
    'Wow, danke fürs Teilen, {name}! … {stadt} bekommt einen Extra-Schub!',
  ],
  geschenkDank: [
    'Tausend Danke, {name}, das geht alles in deinen Turm!',
  ],
  geschenkDankOhne: [
    'Tausend Danke, {name}! … Schreib deine Stadt, dann geht alles in deinen Turm!',
  ],
  herzDank: [
    'Danke für den Herzregen, {name}! … Schreib deine Stadt und bau mit!',
    'Was für ein Herzregen, {name}! … Aus welcher Stadt kommst du? Schreib sie in den Chat!',
  ],
  herzDankStadt: [
    'Danke für den Herzregen, {name}! … Schreib {stadt} weiter in den Chat!',
    'Herzregen von {name}! … Los, {stadt}, baut weiter!',
  ],
  herzMeilenstein: [
    'Wahnsinn! … Schon {zahl} Herzen! … Ihr seid unglaublich!',
    'Wow! … {zahl} Herzen! … Danke, ihr seid die Besten!',
    'Unglaublich, {zahl} Herzen! … Was für eine Stimmung!',
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
  folgeAufruf: [
    'Folgt dem Leuchtturm-Rennen, damit eure Stadt beim nächsten Rennen nicht ohne euch baut!',
    'Wer folgt, verpasst kein Rennen mehr! … Eure Stadt zählt auf euch!',
    'Jeder Leuchtturm braucht treue Wächter! … Folgt uns für das nächste Rennen!',
    'Folgt uns! … Dann seid ihr beim nächsten Städte-Rennen wieder vorne mit dabei!',
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
