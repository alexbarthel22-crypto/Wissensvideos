// Muschel-Tal LIVE – was Anna sagt. Für jede Situation mehrere Varianten;
// die zuletzt benutzten werden ausgelassen, damit er sich nicht wiederholt.
// Platzhalter: {name} {namen} {geschenk} {anzahl} {stufe} {anbau} {rest} {projekt} {kasse} {zahl}

const SAETZE = {
  // Geschenke: immer mit Geschenk-Namen, je wertvoller desto größer der Dank
  geschenkKlein: [
    'Danke {name} für {fuer}!',
    'Danke für {fuer}, {name}!',
    'Lieben Dank für {fuer}, {name}!',
  ],
  geschenkMittel: [
    'Wow! Danke {name} für {fuer}! … Dein Haus wächst!',
    'Vielen Dank für {fuer}, {name}! … Das freut die ganze Insel!',
    '{EinNom} von {name}! … Tausend Dank, das ist super lieb!',
  ],
  geschenkGross: [
    'Wahnsinn! … Danke {name} für {fuer}! … Du bist großartig! … Die Krabben bauen schon an deinem Haus!',
    'Riesigen Dank für {fuer}, {name}! … Was für ein tolles Geschenk! … Die ganze Insel feiert!',
    '{name} schickt {einAkk}! … Danke, danke, danke! … Dein Haus macht einen riesigen Sprung!',
  ],
  geschenkMega: [
    'Ich bin sprachlos! … {name}, vielen, vielen Dank für {fuer}! … Das ist unglaublich! … Das ganze Muschel-Tal feiert dich! … Schaut euch dieses Feuerwerk an!',
    'Alle mal herschauen! … {EinNom} von {name}! … Wahnsinn, tausend Dank! … Du bist eine echte Legende! … Die ganze Insel jubelt für dich!',
  ],
  followEins: [
    'Danke fürs Folgen, {name}!',
    'Willkommen als Bewohner, {name}!',
    '{name} zieht ein! Danke!',
    'Neuer Bewohner: {name}! Danke!',
  ],
  followMehrere: [
    'Danke fürs Folgen, {namen}!',
    'Willkommen, {namen}!',
  ],
  followZiel: [
    'Noch {rest} Bewohner bis {projekt}!',
    'Nur noch {rest} Bewohner für {projekt}!',
  ],
  hinweis: [
    'Dein erster Like baut deine Hütte.',
    'Mehr Likes vergrößern deine Hütte.',
    'Sammle Muscheln durch Events!',
    'Mit Muscheln steigst du in der Rangliste auf.',
    'Schreib haus, dann zeige ich dir dein Haus.',
  ],
  likeDank: [
    'Danke für die vielen Likes, {name}!',
    'Wow, {name}! So viele Likes! Danke!',
    'Like-Regen von {name}! Danke!',
  ],
  teilen: [
    'Danke fürs Teilen, {name}!',
    '{name} hat geteilt! Danke!',
    'Geteilt von {name}! Danke!',
  ],
  neu: [
    '{name} baut das erste Zelt!',
    'Neues Zelt auf der Insel! Willkommen, {name}!',
    '{name} ist eingezogen! Das Zelt steht.',
    'Ein Zelt für {name}! Willkommen!',
  ],
  stufe: [
    '{name} hat jetzt {stufe}!',
    'Aufgestiegen! {stufeName} für {name}!',
    'Glückwunsch {name}! {stufeName}!',
  ],
  anbau: [
    '{name} baut {anbau}.',
    '{anbau} für {name}!',
  ],
  zielErreicht: [
    'Geschafft! {zahl} Bewohner! {projekt} ist fertig!',
    'Wahnsinn! {projekt} ist fertig!',
  ],
  projektFertig: [
    'Geschafft! {Projekt} ist fertig!',
    '{Projekt} steht! Danke an alle!',
  ],
  start: [
    'Muschel-Tal live ist gestartet!',
    'Willkommen im Muschel-Tal! Los geht\'s!',
  ],
  // ---------- Dauer-Moderation („…“ = kurze Sprechpause) ----------
  begruessungEins: [
    'Hallo {name}!',
    'Willkommen, {name}!',
    'Hey {name}!',
    'Hi {name}!',
  ],
  begruessungMehrere: [
    'Hallo {namen}!',
  ],
  rundgang: [
    'Hier wohnt {name}. {stufeCap}{anbauText}.',
    'Besuch bei {name}! {stufeCap}{anbauText}.',
    'Das ist das Haus von {name}.',
  ],
  tipp: [
    'Schreib pool oder garten für einen Anbau!',
    'Schreib rot oder blau für eine neue Farbe!',
    'Schreib haus, dann zeige ich dein Haus!',
    'Teilt den Stream mit Freunden!',
  ],
  fakt: [
    'Auf der Haupt-Insel steht der Muschelpalast.',
    'Auf der Kokos-Küste sind die Häuser Kokosnüsse!',
    'Auf der Haupt-Insel gibt es eine Bäckerei.',
    'Jeder Follower bekommt in Muschel-Tal eine Hütte.',
  ],
  frage: [
    'Welche Farbe hat euer Traumhaus?',
    'Pool oder Garten? Schreibt es!',
    'Wie gefällt euch die Insel?',
  ],
  rangliste: [
    'Platz eins: {erster}!',
    'Das beste Haus hat {erster}.',
    'Platz zwei: {zweiter}. Wer holt Platz eins?',
  ],
  kasse: [
    '{kasse} Muscheln in der Kasse!',
    'Die Muschelkasse wächst: {kasse}!',
  ],
  ziel: [
    'Noch {rest} Bewohner bis {projekt}!',
    'Bald ist es geschafft!',
  ],
  projekt: [
    '{projekt}: {prozent} Prozent fertig!',
    'Wir bauen {projekt}. {prozent} Prozent!',
  ],
  teaser: [
    'In {zeit} kommt eine Überraschung!',
    'Bleibt dran! Bald gibt es ein Event.',
  ],
  countdown30: [
    'Noch dreißig Sekunden bis zum Event!',
  ],
  countdown10: [
    'Zehn Sekunden! Macht euch bereit!',
  ],
  stimmung: [
    'Was für eine schöne Insel!',
    'Die Krabben bauen fleißig!',
    '{aktive} Leute bauen mit!',
    'Herrlich hier!',
  ],
  abend: [
    'Die Laternen sind an.',
    'Gemütlicher Abend auf der Insel.',
  ],
  eventAllgemein: [
    'Macht mit!',
    'Noch {rest} Sekunden!',
    'Jetzt mitmachen!',
    'Los, los, los!',
    'Spannend!',
  ],
  hausZeigen: [
    '{name}, hier ist dein Haus!',
    'Da ist dein Haus, {name}!',
    'Hier wohnst du, {name}!',
  ],
  begruessungZurueck: [
    'Willkommen zurück, {name}!',
    'Schön, dass du wieder da bist, {name}!',
    'Da ist ja {name} wieder!',
  ],
  begruessungTreu: [
    '{name}, schon zum {besuche}. Mal da! Danke!',
  ],
  begruessungZurueckMehrere: [
    'Willkommen zurück, {namen}!',
  ],
  baustelleZeigen: [
    'Hier entsteht {ein}!',
    'Die Baustelle! {prozent} Prozent!',
    '{Projekt} wächst!',
  ],
  topEins: [
    'Neuer Platz eins: {name}!',
    'Wechsel an der Spitze: {name}!',
  ],
  topNeu: [
    '{name} ist jetzt auf Platz {platz}!',
    'Neu auf Platz {platz}: {name}!',
  ],
  folgeAufruf: [
    'Wenn dir die Insel gefällt, folg gern muscheltal.',
    'Schön, dass ihr da seid! Wer mag, folgt muscheltal.',
  ],
  eventNoch10: [
    'Noch zehn Sekunden!',
  ],
};

const zuletzt = {};
export function satz(art, werte = {}) {
  const liste = SAETZE[art]; if (!liste) return '';
  const weg = zuletzt[art] || [];
  let frei = liste.map((_, i) => i).filter(i => !weg.includes(i));
  if (!frei.length) frei = liste.map((_, i) => i);                  // Gruppen mit nur einem Satz: einfach wiederholen
  const i = frei[Math.floor(Math.random() * frei.length)];
  zuletzt[art] = [i, ...weg].slice(0, Math.floor(liste.length / 2));
  return liste[i].replace(/\{(\w+)\}/g, (_, k) => werte[k] ?? '');
}
export const namenListe = n => n.length > 1 ? `${n.slice(0, -1).join(', ')} und ${n.at(-1)}` : n[0];
// Alle Sätze ohne Platzhalter (werden beim Start vorab als Sprachdatei erzeugt)
export const festeSaetze = () => Object.values(SAETZE).flat().filter(t => !t.includes('{'));
