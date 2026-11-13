// Muschel-Tal LIVE – was Markus sagt. Für jede Situation mehrere Varianten;
// die zuletzt benutzten werden ausgelassen, damit er sich nicht wiederholt.
// Platzhalter: {name} {namen} {geschenk} {anzahl} {stufe} {anbau} {rest} {projekt} {kasse} {zahl}

const SAETZE = {
  geschenkKlein: [
    'Danke {name} für {geschenk}!',
    'Oh, {geschenk} von {name}! Dankeschön!',
    '{name}, danke dir für {geschenk}!',
    'Lieben Dank für {geschenk}, {name}!',
    'Danke {name}! {geschenk} kommt direkt in die Muschelkasse.',
    'Wie lieb, {name}! Danke für {geschenk}!',
    '{geschenk} von {name}! Die Krabben freuen sich!',
    'Danke {name}, dein Haus wächst!',
  ],
  geschenkMittel: [
    'Wow, vielen Dank {name} für {geschenk}!',
    '{name}, du bist großartig! Danke für {geschenk}!',
    'Schaut mal, {geschenk} von {name}! Tausend Dank!',
    'Danke {name}! Mit {geschenk} wird auf deinem Grundstück ordentlich gebaut!',
    'Was für ein Geschenk! Danke {name} für {geschenk}!',
    '{name} schickt {geschenk}! Das ganze Viertel jubelt. Danke!',
  ],
  geschenkGross: [
    'Wahnsinn! Riesigen Dank an {name} für {geschenk}! Das ganze Muschel-Tal feiert dich!',
    'Unglaublich! {name} schickt {geschenk}! Danke, danke, danke!',
    'Ich bin sprachlos! {geschenk} von {name}! Das gibt eine Mega-Show!',
    'Alle mal herschauen! {name} hat {geschenk} geschickt! Vielen, vielen Dank!',
    '{name}, du bist eine Legende! Danke für {geschenk}!',
  ],
  followEins: [
    'Danke {name} fürs Folgen!',
    'Willkommen als Bewohner, {name}! Danke fürs Folgen!',
    '{name} zieht ins Muschel-Tal ein! Danke fürs Folgen!',
    'Schön, dass du da bist, {name}! Danke fürs Folgen!',
    'Ein neuer Bewohner! Danke {name}!',
    'Danke {name}, du wohnst jetzt offiziell im Muschel-Tal!',
  ],
  followMehrere: [
    'Danke {namen} fürs Folgen!',
    'Willkommen, neue Bewohner! Danke {namen}!',
    '{namen} ziehen ins Muschel-Tal ein! Danke fürs Folgen!',
    'Da kommen gleich mehrere! Danke {namen} fürs Folgen!',
    'Herzlich willkommen {namen}! Schön, dass ihr hier wohnt!',
  ],
  followZiel: [
    ' Noch {rest} Bewohner, dann ist {projekt} dran.',
    ' Nur noch {rest} Bewohner, dann wird {projekt} gebaut!',
    ' Wir brauchen noch {rest} Bewohner für {projekt}.',
  ],
  teilen: [
    'Danke {name} fürs Teilen!',
    '{name} hat den Stream geteilt! Danke dir!',
    'Danke fürs Teilen, {name}! Vielleicht ziehen deine Freunde bald nebenan ein!',
    'Geteilt von {name}! Das bringt zwei Muscheln in die Kasse. Danke!',
  ],
  neu: [
    'Willkommen im Muschel-Tal, {name}! Dein Zelt steht.',
    'Hallo {name}! Dein Grundstück ist bereit.',
    '{name} ist da! Das erste Zelt steht schon.',
    'Ein neues Zelt für {name}! Viel Spaß beim Bauen!',
  ],
  stufe: [
    '{name} hat jetzt {stufe}!',
    'Aufgestiegen! {name} wohnt jetzt in {stufeDativ}.',
    'Die Krabben haben fertig gebaut: {stufe} für {name}!',
    'Neues Zuhause für {name}: {stufe}!',
    'Glückwunsch {name}! Das neue Zuhause ist fertig: {stufeName}!',
  ],
  anbau: [
    '{name} baut {anbau}.',
    '{anbau} für {name}! Sieht schick aus.',
    'Bei {name} gibt es jetzt {anbau}.',
  ],
  zielErreicht: [
    'Wahnsinn! {zahl} Bewohner! {projekt} auf der Haupt-Insel ist fertig!',
    'Geschafft! Mit {zahl} Bewohnern wird {projekt} fertig gebaut! Danke an alle!',
  ],
  projektFertig: [
    'Geschafft! {projekt} ist fertig. Danke an alle!',
    '{projekt} steht! Das habt ihr mit der Muschelkasse gebaut!',
    'Fertig! Unser {projekt} ist eröffnet!',
  ],
  start: [
    'Muschel-Tal live ist gestartet. Liked, kommentiert und baut eure Häuser!',
    'Hallo und willkommen im Muschel-Tal! Jedes Like lässt euer Haus wachsen. Los geht\'s!',
    'Die Insel ist wach! Liked und kommentiert, die Krabben warten schon aufs Bauen.',
  ],
};

const zuletzt = {};
export function satz(art, werte = {}) {
  const liste = SAETZE[art]; if (!liste) return '';
  const weg = zuletzt[art] || [];
  const frei = liste.map((_, i) => i).filter(i => !weg.includes(i));
  const i = frei[Math.floor(Math.random() * frei.length)];
  zuletzt[art] = [i, ...weg].slice(0, Math.max(1, Math.floor(liste.length / 2)));
  return liste[i].replace(/\{(\w+)\}/g, (_, k) => werte[k] ?? '');
}
export const namenListe = n => n.length > 1 ? `${n.slice(0, -1).join(', ')} und ${n.at(-1)}` : n[0];
