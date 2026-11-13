// Muschel-Tal LIVE – was Anna sagt. Für jede Situation mehrere Varianten;
// die zuletzt benutzten werden ausgelassen, damit er sich nicht wiederholt.
// Platzhalter: {name} {namen} {geschenk} {anzahl} {stufe} {anbau} {rest} {projekt} {kasse} {zahl}

const SAETZE = {
  geschenkKlein: [
    'Danke {name} für {fuer}!',
    'Oh, {einNom} von {name}! … Dankeschön!',
    '{name}, danke dir für {fuer}!',
    'Lieben Dank für {fuer}, {name}!',
    'Danke {name}! … Das kommt direkt in die Muschelkasse.',
    'Wie lieb, {name}! … Danke für {fuer}!',
    '{EinNom} von {name}! … Die Krabben freuen sich!',
    'Danke {name}, … dein Haus wächst!',
  ],
  geschenkMittel: [
    'Wow, vielen Dank {name} für {fuer}!',
    '{name}, du bist großartig! … Danke für {fuer}!',
    'Schaut mal, {einNom} von {name}! … Tausend Dank!',
    'Danke {name}! … Auf deinem Grundstück wird jetzt ordentlich gebaut!',
    'Was für ein Geschenk! … Danke {name} für {fuer}!',
    '{name} schickt {einAkk}! … Das ganze Viertel jubelt. … Danke!',
  ],
  geschenkGross: [
    'Wahnsinn! … Riesigen Dank an {name} für {fuer}! … Das ganze Muschel-Tal feiert dich!',
    'Unglaublich! … {name} schickt {einAkk}! … Danke, danke, danke!',
    'Ich bin sprachlos! … {EinNom} von {name}! … Das gibt eine Mega-Show!',
    'Alle mal herschauen! … {name} hat {einAkk} geschickt! … Vielen, vielen Dank!',
    '{name}, du bist eine Legende! … Danke für {fuer}!',
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
  hinweis: [
    'Folgt mir … und eure Hütte wird live gebaut … und euer Platz in Muschel-Tal ist reserviert!',
    'Dein erster Like baut deine Hütte. … Mehr Likes vergrößern deine Hütte.',
    'Sammle Muscheln durch Events … und steige in der Rangliste auf!',
    'Neu hier? … Dein erster Like baut deine Hütte! … Und jedes weitere Like macht sie größer.',
    'Folgen lohnt sich … deine Hütte wird live gebaut … und dein Platz in Muschel-Tal ist dir sicher!',
    'Bei jedem Event gibt es Muscheln zu gewinnen … damit kletterst du in der Rangliste nach oben!',
  ],
  likeDank: [
    'Wow, {name}! … Danke für die vielen Likes! … Dein Haus wächst und wächst.',
    'Danke {name} für so viele Likes! … Da freuen sich die Krabben-Bauarbeiter!',
    '{name} liked wie verrückt! … Danke dir! … Das bringt Muscheln in die Kasse.',
    'Was für ein Like-Regen von {name}! … Danke!',
  ],
  teilen: [
    'Danke {name} fürs Teilen!',
    '{name} hat den Stream geteilt! Danke dir!',
    'Danke fürs Teilen, {name}! Vielleicht ziehen deine Freunde bald nebenan ein!',
    'Geteilt von {name}! Das bringt zwei Muscheln in die Kasse. Danke!',
  ],
  neu: [
    'Willkommen im Muschel-Tal, {name}! … Dein Zelt steht.',
    'Hallo {name}! … Schau mal, dein Zelt ist schon aufgebaut.',
    '{name} ist da! … Das erste Zelt steht sofort.',
    'Ein neues Zelt für {name}! … Jedes Like baut weiter.',
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
    'Geschafft! … {Projekt} ist fertig. … Danke an alle!',
    '{Projekt} steht! … Das habt ihr mit der Muschelkasse gebaut!',
    'Fertig! … {Projekt} ist eröffnet!',
  ],
  start: [
    'Muschel-Tal live ist gestartet. Liked, kommentiert und baut eure Häuser!',
    'Hallo und willkommen im Muschel-Tal! Jedes Like lässt euer Haus wachsen. Los geht\'s!',
    'Die Insel ist wach! Liked und kommentiert, die Krabben warten schon aufs Bauen.',
  ],
  // ---------- Dauer-Moderation („…“ = Sprechpause) ----------
  begruessungEins: [
    'Hallo {name}!',
    'Willkommen, {name}!',
    'Hey {name}, schön, dass du da bist!',
    'Hi {name} … viel Spaß!',
    'Willkommen auf der Insel, {name}!',
  ],
  begruessungMehrere: [
    'Hallo {namen} … schön, dass ihr da seid!',
    'Willkommen im Stream, {namen}! … Macht es euch gemütlich.',
    'Hey {namen}! … Herzlich willkommen auf der Live-Insel!',
    'Da kommen ja gleich mehrere … hallo {namen}!',
    'Willkommen {namen}! … Ein Like, und euer erstes Zelt steht.',
  ],
  rundgang: [
    'Schauen wir mal … bei {name} vorbei. … {stufeCap}{anbauText}. … Sehr schick!',
    'Kleiner Rundgang über die Insel … hier wohnt {name}, … in {stufeDativ}{anbauText}.',
    'Und hier … das Zuhause von {name}. … {stufeCap}{anbauText}. … Gefällt mir!',
    'Wir fliegen mal rüber zu {name} … {stufeCap}{anbauText}. … Da hat jemand fleißig gebaut!',
    'Wer wohnt denn hier? … Ah, {name}! … {stufeCap}{anbauText}.',
  ],
  tipp: [
    'Neu hier? … Jedes Like lässt dein Haus wachsen. … Vom Zelt bis zum Muschelschloss!',
    'Kleiner Tipp … schreibt pool, garten, boot oder palme in die Kommentare … und euer Haus bekommt einen Anbau.',
    'Ihr wollt eine andere Farbe? … Schreibt einfach rot, blau, lila oder gold!',
    'Jeder Coin, … der als Geschenk kommt, … ist eine Muschel für euer Haus und die Muschelkasse.',
    'Teilt den Stream mit Freunden … dann ziehen sie vielleicht bald neben euch ein!',
    'Wer früher kommt, … wohnt näher an der großen Muschel. … Also, ran an die Likes!',
    'Schreib haus … dann zeige ich dir dein Haus hier im Stream!',
  ],
  fakt: [
    'Wusstet ihr? … Auf der Haupt-Insel steht in der Mitte der Muschelpalast … mit zwei Brunnen davor.',
    'Übrigens … auf der Kokos-Küste sind die Häuser Kokosnüsse! … Mit Tür, Fenster und einem Blatt obendrauf.',
    'Auf der Haupt-Insel gibt es eine Dönerbude, … eine Strandbar … und einen Açaí-Stand, der Tag und Nacht geöffnet hat.',
    'Wusstet ihr? … Auf der Kokos-Küste brennt in der Mitte immer ein großes Lagerfeuer.',
    'Auf der Haupt-Insel … duftet es nach frischem Brot. … Da gibt es nämlich eine Bäckerei!',
    'Jeder Follower … bekommt im Muschel-Tal eine eigene Hütte mit seinem Namen.',
    'Auf der Haupt-Insel wird gerade gebaut … das Hotel Sandkorn, … eine Boots-Anlegestelle … und das Tierheim Pfotenkuss.',
  ],
  frage: [
    'Mal eine Frage an euch … welche Farbe hat euer Traumhaus? … Schreibt sie in die Kommentare!',
    'Was meint ihr … wer baut heute das erste Muschelschloss?',
    'Pool oder Garten? … Was ist euch wichtiger? … Schreibt es einfach in den Chat!',
    'Wer von euch war heute schon am Strand? … Also, auf der Insel natürlich!',
    'Wie gefällt euch die Insel? … Ich finde, ihr habt schon richtig viel geschafft!',
  ],
  rangliste: [
    'Ein Blick auf die Rangliste … ganz vorne: {erster}! … Dicht gefolgt von {zweiter}.',
    'Das größte Haus … gehört gerade {erster}. … Wer holt sich Platz eins?',
    'Platz eins … {erster}. … Platz zwei … {zweiter}. … Da ist noch alles drin!',
  ],
  kasse: [
    'In der Muschelkasse … liegen schon {kasse} Muscheln!',
    'Die Muschelkasse wächst und wächst … {kasse} Muscheln! … Jedes Like zählt.',
    '{kasse} Muscheln … in der Kasse der Live-Insel. … Stark!',
  ],
  ziel: [
    'Folgen heißt einziehen! … Noch {rest} Bewohner, … dann wird {projekt} gebaut.',
    'Wir sind schon {bewohner} Bewohner! … Bei {zielzahl} … wird {projekt} fertig.',
    'Noch {rest} neue Bewohner … dann ist {projekt} dran! … Wer zieht als Nächstes ein?',
  ],
  projekt: [
    'Unser Bauprojekt {projekt} … ist schon zu {prozent} Prozent fertig!',
    'Am {projekt} wird fleißig gebaut … {prozent} Prozent haben wir schon!',
  ],
  teaser: [
    'In {zeit} … startet das nächste Überraschungs-Event. … Was es wohl wird?',
    'Bleibt dran … in {zeit} gibt es eine Überraschung!',
    'Ich verrate noch nichts … aber in {zeit} passiert etwas!',
  ],
  countdown30: [
    'Noch dreißig Sekunden … bis zum nächsten Event!',
    'Achtung … in dreißig Sekunden geht es los!',
  ],
  countdown10: [
    'Zehn Sekunden … macht euch bereit!',
    'Gleich ist es so weit … zehn … Sekunden!',
  ],
  stimmung: [
    'Was für eine schöne Insel ihr gebaut habt!',
    'Die Krabben arbeiten auf Hochtouren … überall wird gebaut!',
    'Hört ihr das Meer? … Herrlich hier.',
    '{aktive} Leute bauen gerade mit … der Wahnsinn!',
    'Ich liebe es, wie die Insel jeden Tag wächst.',
  ],
  abend: [
    'Die Laternen sind an … gemütlicher Abend auf der Insel.',
    'Schaut mal, wie die Fenster leuchten … richtig gemütlich heute.',
  ],
  eventAllgemein: [
    'Macht mit … jeder kann gewinnen!',
    'Noch {rest} Sekunden … gebt alles!',
    'Wer noch nicht dabei ist … jetzt ist die Chance!',
    'Das wird spannend …',
    'Ich bin gespannt, wie das ausgeht!',
    'Los, los, los!',
  ],
  hausZeigen: [
    '{name} … hier ist dein Haus! … {stufeCap}{anbauText}.',
    'Bitte schön, {name} … das ist dein Zuhause! … {stufeCap}{anbauText}.',
    'Da ist es, {name}! … {stufeCap}{anbauText}. … Like weiter, dann wird es noch größer!',
    '{name}, … schau mal … hier wohnst du! … {stufeCap}{anbauText}.',
    'Hier ist dein Haus, {name}! … {stufeCap}{anbauText}. … Sieht richtig gut aus!',
  ],
  begruessungZurueck: [
    'Willkommen zurück, {name}!',
    'Schön, dass du wieder da bist, {name}!',
    'Da ist ja {name} wieder!',
    'Hallo {name}, schön, dich wiederzusehen!',
  ],
  begruessungTreu: [
    '{name}, schon zum {besuche}. Mal da … danke!',
    'Willkommen zurück, {name} … zum {besuche}. Mal!',
  ],
  begruessungZurueckMehrere: [
    'Willkommen zurück, {namen}! … Schön, dass ihr wieder da seid.',
    'Bekannte Gesichter! … Hallo {namen}, … eure Häuser stehen noch.',
    'Da sind ja {namen} wieder! … Willkommen zurück auf der Insel.',
  ],
  geschenkInfo: [
    'Übrigens … jedes Geschenk bringt Muscheln für dein Haus. … Ein Coin ist eine Muschel … und dazu gibt es eine Show mit deinem Namen!',
    'Mit Geschenken wächst dein Haus besonders schnell … eine Rose ist eine Muschel, … ein Galaxy schon tausend!',
    'Ab hundert Coins … gibt es ein Feuerwerk mit deinem Namen … und ab tausend sogar eine Mega-Show über der ganzen Insel!',
    'Alle Geschenke gehen auch in die Muschelkasse … für unsere gemeinsamen Bauprojekte. … Danke an alle, die mitbauen!',
    'Wer ein Geschenk schickt, … wird hier groß bedankt … und sein Haus macht einen richtigen Sprung nach oben!',
  ],
  baustelleZeigen: [
    'Schauen wir mal auf die Baustelle … {Projekt} ist schon zu {prozent} Prozent fertig!',
    'Hier entsteht {ein} … noch {rest} Muscheln, dann ist es fertig!',
    'Die Krabben bauen fleißig … {prozent} Prozent geschafft! … Jedes Like hilft mit.',
    'Auf der Baustelle ist ordentlich was los … {Projekt} wächst und wächst!',
  ],
  topEins: [
    '{name} ist jetzt auf Platz eins! … Das beste Haus der ganzen Insel!',
    'Neuer Spitzenreiter: … {name}!',
    'Wechsel an der Spitze! … {name} übernimmt Platz eins!',
  ],
  topNeu: [
    '{name} ist neu in den Top drei … auf Platz {platz}!',
    'Neu auf Platz {platz}: … {name}!',
    '{name} klettert auf Platz {platz} der besten Häuser!',
  ],
  folgeAufruf: [
    'Folge mir … und du bekommst live deine Hütte hier … und in Muschel-Tal für das Spiel!',
    'Noch nicht gefolgt? … Folge mir, dann bekommst du sofort deine Hütte hier im LIVE … und in Muschel-Tal!',
    'Kleiner Aufruf … wer mir folgt, … bekommt live seine eigene Hütte hier … und in Muschel-Tal für das Spiel!',
    'Folgen lohnt sich! … Deine Hütte hier im LIVE … und in Muschel-Tal … wartet schon auf dich.',
  ],
  eventNoch10: [
    'Noch zehn Sekunden!',
    'Zehn Sekunden noch … gebt alles!',
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
