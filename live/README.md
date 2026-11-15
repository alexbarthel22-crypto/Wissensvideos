# 🐚 Muschel-Tal LIVE

Automatischer TikTok-LIVE: Zuschauer bauen mit Likes, Kommentaren und Geschenken ihr eigenes Haus auf der Live-Insel.
Eine Mac-Stimme (unbegrenzt, offline) moderiert.

## Einmal einrichten (Mac)
1. **Node.js** installieren: https://nodejs.org → LTS → „macOS Installer (.pkg)“.
2. **Nur diesen Ordner `live/`** herunterladen (er funktioniert allein – Bewohnerzahl und Bauprojekte holt er sich selbst aus dem Repo). Den Ordner kannst du beliebig umbenennen und ablegen.
3. Im Ordner auf **„Muschel-Tal LIVE testen.command“** doppelklicken.
   Falls der Mac warnt: Rechtsklick → „Öffnen“ → „Öffnen“.
   Es öffnet sich die Insel mit Test-Zuschauern, Kerstin spricht.

**Spielstand:** wird automatisch in `stand.json` gespeichert (alle 10 Sekunden, beim Stream-Ende und beim Schließen des Fensters). Beim nächsten Start geht alles genau dort weiter. Einfach immer denselben Ordner benutzen.
**Update auf eine neue Version:** neuen Ordner holen und deine `stand.json` (Spielstand) und `sperrliste.txt` hineinkopieren.
**Ganz von vorne:** `stand.json` löschen.

## Stream starten
1. **„Muschel-Tal LIVE starten.command“** doppelklicken. Beim ersten Mal lädt es einmalig das Tunnel-Programm „cloudflared“ (Cloudflare) und die TikTok-Anbindung.
2. Im Terminal erscheint ein **🔗 Link** (`https://….trycloudflare.com`) – er ist schon in der Zwischenablage.
3. **LIVE Studio** → Quelle **„Link“** → einfügen (⌘V) → 1080 × 1920. Der Link ist bei jedem Start neu: die vorhandene Link-Quelle bearbeiten und den neuen Link einfügen.
4. **LIVE starten.** Im Terminal muss nach ca. 20 s **„✅ Mit dem LIVE von @muscheltal verbunden“** stehen.
5. Ende: LIVE stoppen, dann das Terminalfenster schließen (Spielstand wird gespeichert, Link wird geschlossen).

**Zum Link:** LIVE Studio nimmt nur echte https-Adressen an. Der Tunnel macht die Insel-Seite nur während das Programm läuft unter dem zufälligen Link erreichbar. Wer den Link kennt, sieht nur die Insel – steuern kann man darüber nichts (Test-Zugänge sind gesperrt, Kerstin spricht nur ihre eigenen Sätze).
**Klappt der Link nicht:** Notlösung Fensteraufnahme – `http://localhost:8790` im Browser öffnen, Fenster möglichst hoch, in LIVE Studio „Fensteraufnahme“ + Systemton.

## Regeln (änderbar in `einstellungen.json`)
| Aktion | Wirkung |
|---|---|
| Erster Like/Kommentar | eigenes Grundstück mit @Namen – wer früher kommt, wohnt näher an der Muschel |
| 1 Like | 1 Muschel in die **Muschelkasse der Live-Insel** (getrennt von der Inselkasse der Haupt-Insel) + 1 Muschel fürs eigene Haus |
| Haus-Stufen (60) | Zelt → Hängematten-Camp → Strohhütte → Fischerhütte → Stelzenhütte → Baumhaus → Bungalow → Surferhütte → Strandhaus → Leuchtturmhaus → Ferienhaus → Poolhaus → Villa → Glasvilla → Luxusvilla → Inselvilla mit Hubschrauberlandeplatz → Strandpalast → Korallenpalast → Muschelschloss → Perlenschloss → danach 40 Prachtschlösser (Goldenes Perlenschloss, Sonnenpalast, … Muschel-Tal-Legende), jedes prächtiger: neue Farbe, Leuchten, Krone, Sterne, Türme, Fahnen, Regenbogen |
| Rangliste „Beste Häuser“ | Name · Haus-Stufe · Muschel-Kontostand; höchste Haus-Stufe zuerst, bei gleicher Stufe die meisten Muscheln (die angezeigte Zahl) |
| Kommentar `palme` `flagge` `garten` `laterne` `pool` `boot` | Anbau (ab bestimmter Stufe) |
| Kommentar `rot` `blau` `lila` … | Hausfarbe |
| Kommentar `haus` (auch Haus!, hauus, house, huas, mein haus …) | ab und zu fliegt die Kamera zum eigenen Haus, Kerstin: „…, hier ist dein Haus!“ |
| Geschenk | **1 Coin = 1 Muschel (= 0,01 €)** – für die Muschelkasse und fürs eigene Haus, große Geschenke = Feuerwerk |
| Folgen | neuer **Bewohner** + 5 Muscheln in die Muschelkasse |
| Stream teilen | 2 Muscheln in die Muschelkasse |
| Abstimmung (eins der Events) | nächstes Stadtgebäude, wird mit Muscheln aus der Muschelkasse gebaut |

Die Insel startet mit 200 Grundstücken und **wächst live**, sobald alle belegt sind (jeweils ca. 60 neue).
Ausbauten werden animiert gebaut (Bambusgerüst, Krabben-Bauarbeiter, Sandstaub), die Kamera fährt dabei an das Haus heran; sonst wechselt sie zwischen Übersicht und kleinen Rundfahrten.
Oben steht immer das **nächste Bauprojekt der Haupt-Insel** – automatisch aus `muscheltal/daten/insel.json` (`baustellen`), Startzahl der Bewohner aus `einwohner.csv`. Straßennamen stehen unter `strassen`.
Die Bewohnerzahl kommt live von TikTok (Follower), `bewohner.start` ist nur der Startwert, falls TikTok sie nicht liefert.

## Überraschungs-Events (alle 2 Minuten, je 1 Minute, 50 verschiedene)
Rechts oben läuft ein Countdown „Nächstes Event“ – welches kommt, bleibt geheim (❓❓❓). Nie dasselbe wie eins der letzten 10.
Beim Start sagt Kerstin, was am Ende passiert (steht auch im Event-Feld unter 🏆). Am Ende nennt sie die Gewinner mit Namen (im Ergebnis-Feld unter 🏆).
Alle Events laufen komplett im Stream und ohne Rauszoomen (die Kamera bleibt bei den Häusern), mitmachen per Like oder Kommentar – niemand muss den Stream verlassen, nichts ist an Geschenke gebunden.
Like-Ziele liegen bei ca. 80 % des normalen Like-Tempos: schaffbar, wenn alle mitmachen. Alle Events sind automatisch geprüft (Test-Zuschauer machen mit, Belohnungen kommen an).

| Event | Mitmachen | Belohnung |
|---|---|---|
| 🌊 Sturmflut | gemeinsam liken | Deich hält → 20 🐚 für alle Helfer |
| 🎡 Muschel-Glücksrad | in den letzten 10 Min. aktiv | 150–500 🐚, goldenes Dach oder Pool |
| 🦀 Krabbenrennen | `rot` `blau` `gelb` `grün` oder einfach liken | Siegerteam 25 🐚 |
| ⚔️ Team-Duell | `muschel` / `kokos` oder einfach liken | Siegerteam 30 🐚 |
| 🎉 Hausparty | `party` (Kamera beim Gastgeber) | Gast 10 🐚, Gastgeber 5 🐚 pro Gast |
| 👋 Inselgruß | `moin` / `hallo` | 10 🐚 je Gruß |
| 🏠 Hausbesuch | – (Kamera besucht ein aktives Haus) | 25 🐚 |
| ✨ Muschelregen | liken | Likes zählen doppelt fürs Haus |
| ⚡ Bau-Turbo | liken | Likes zählen dreifach fürs Haus |
| 🧰 Schatzkiste | `1` `2` `3` | richtige Kiste 30 🐚 |
| 🔢 Zahlenraten | Zahl 1–100 (mit Hinweisen) | Treffer 100 🐚 |
| 🎉 Strandparty | Stimmung per Likes | Feuerwerk + 15 🐚 |
| 🐦 Möwenalarm | `fang` (erste 5) | 20 🐚 |
| 🌠 Sternschnuppe | `wunsch` | einer bekommt einen Anbau |
| 🗳️ Abstimmung | `1` `2` `3` | nächstes Stadtgebäude |
| ⌨️ Wortjagd | gezeigtes Wort abtippen (erste 3) | 40 / 25 / 15 🐚 |
| 🍹 Cocktail-Mix | `mango` `kokos` `ananas` | Mehrheit 15 🐚 |
| 🎈 Ballon-Platzen | liken | wer einen Ballon platzen lässt: 10 🐚 |
| 🗼 Leuchtturm anzünden | gemeinsam liken | 20 🐚 für alle Helfer |
| 🌺 Blumenwiese | `blume` | ab 25 Blumen 15 🐚 für alle |
| 🧩 Emoji-Rätsel | Lösung schreiben (z. B. „Sandburg“) | 50 🐚 |
| 🏐 Beachvolleyball | `links` / `rechts` oder einfach liken | Siegerteam 25 🐚 |
| 🤝 Nachbarschaftshilfe | liken = baut beim kleinsten Haus mit | fleißigster Helfer 30 🐚 |
| 🍦 Eiswagen | gemeinsam liken | 15 🐚 für alle |
| 🍀 Glückszahl | Zahl 1–10 | richtige 30 🐚 |
| ❓ Strand-Quiz | `A` `B` `C` | richtige 20 🐚 |
| 🤔 Wahr oder falsch | `wahr` / `falsch` | richtige 20 🐚 |
| 🏄 Surf-Contest | `surf`, dann liken | Bester 60 🐚 |
| 🥥 Kokosnuss-Weitwurf | `wurf` | weitester Wurf 40 🐚 |
| 📸 Inselfoto | `cheese` | 8 🐚 + Name auf dem Foto |
| 🪢 Tauziehen | `muschel` / `seestern` oder einfach liken | Siegerteam 25 🐚 |
| 🔤 Buchstabensalat | Wort aus den Buchstaben schreiben | 50 🐚 |
| 🎲 Muschel-Würfeln | `würfel` | jede Sechs 30 🐚 |
| 🦜 Papagei | gezeigten Satz nachschreiben (erste 5) | 20 🐚 |
| 🌈 Regenbogen malen | `rot` `orange` `gelb` `grün` `blau` `lila` | komplett: 20 🐚 für alle Maler |
| 👑 Inselkönig | 1 Minute am meisten liken | 60 🐚 + Krone |
| 🏆 Like-Rekord | 30 Sekunden liken | Rekord gebrochen: 25 🐚 für alle |
| 🎭 Motto des Tages | `1` `2` `3` | Mehrheit 10 🐚 |
| 🎁 Mystery-Box | `box` | 3–50 🐚 für jeden |
| 🕵️ Wer bin ich? | Tier erraten (3 Hinweise) | 50 🐚 |
| 🎨 Inselfarbe | `rot` / `blau` / `grün` | Mehrheit 10 🐚 |
| 🧴 Sonnencreme | `creme` (erste 10) | 15 🐚 |
| 🍨 Eis-Bestellung | `1` `2` `3` | Mehrheit 15 🐚 |
| 🏴‍☠️ Piratenschatz | gemeinsam liken | 25 🐚 für alle Helfer |
| 🐚 Glücksmuschel | `muschel` | einer gewinnt 80 🐚 |
| 🍹 Happy Hour | liken | Likes zählen doppelt |
| 🎤 Reim-Zeit | Reim schreiben (erste 10) | 10 🐚 |
| ⛵ Bootsrennen | `segel` / `motor`, dann liken | Siegerboot 25 🐚 |
| ✈️ Traumurlaub | `1` `2` `3` | Mehrheit 10 🐚 |
| 💖 Komplimente | `schön` / `toll` | 5 🐚, ab 10 Bonus 10 🐚 |

## Große Grundstücke
Ab Stufe 12 (Villa, 800 Muscheln) zieht das Haus auf ein **großes Doppel-Grundstück** (so groß wie ein Stadtgebäude-Platz) – mit Rasen, Hecke, Pool, Palmen und größerem Haus. Einstellbar: `grossesGrundstueckAbStufe`.

## Fortschritt
- TikTok schickt bei vielen Likes nicht jedes einzeln mit Namen: die fehlenden Likes werden anteilig auf die Zuschauer verteilt, die gerade liken.
- Kommentare bringen 2 Muscheln (höchstens alle 30 s).
- Stufen-Grenzen: 0, 5, 15, 30, 50, 80, 120, 170, 240, 330, 450, 600, 800, 1.050, 1.400, 1.850, 2.400, 3.100, 4.000, 5.200 Muscheln.

## Immer was los
- **Mini-Aufgaben** zwischen den Events (alle 30–50 s, 25 s lang): Wort schreiben (die ersten 5 bekommen 5 🐚) oder gemeinsam liken (alle Liker 3 🐚). Steht gut sichtbar im Infofeld.
- **Überraschungen im Bild** alle 20–35 s: Heißluftballon, Möwenschwarm, Konfetti, Lichtershow über der Muschel, Hausparty, Delfine, Krabben-Parade, Seifenblasen, Drachen.

## Jobs
Ist ein Stadtgebäude fertig, wird dort ein **Job** unter den Zuschauern der letzten 15 Minuten verlost (Banner, Ansage, gelbes 💼-Schild über dem Gebäude). **Gehalt: alle 5 Minuten 5 Muscheln** fürs eigene Haus (einstellbar unter `jobs` in einstellungen.json). Jobs gelten nur während des Streams: bei jedem Neustart werden alle Jobs neu verlost (nacheinander, alle 30 s einer, sobald Zuschauer aktiv sind).

## Stadtgebäude (ohne Limit)
Per Abstimmung wählt der Chat das nächste Gemeinschafts-Gebäude, bezahlt wird aus der Muschelkasse (beim Baustart fließt die Hälfte des Ersparten in die Baustelle, danach 70 % jeder neuen Muschel – die Kasse ist nie leer). Kosten realistisch: Café/Eisdiele/Friseur 6.000 … Krankenhaus 35.000 Muscheln (einstellbar in einstellungen.json):
Rathaus, Schule, Krankenhaus, Feuerwache, Polizeistation, Supermarkt, Kino, Bibliothek, Post, Café, Eisdiele, Museum, Sporthalle, Markthalle, Hotel, Apotheke, Aquarium, Theater, Schwimmbad, Kindergarten, Restaurant, Friseur, Muschelbank, Inselbahnhof – alle im tropischen Strand-Stil (Palmen, Markisen, Stroh- und Ziegeldächer).
Gebäude dürfen mehrfach gebaut werden (noch nicht gebaute kommen bei der Abstimmung zuerst). Bauplätze: zuerst das Stadtzentrum um den Muschelplatz, dann über die ganze Insel verteilt (fest vorgemerkt, Häuser ziehen nie um). Reichen die Plätze nicht, wächst die Insel – bis ca. 60 Gebäude und 1.800 Grundstücke.
Während des Baus: lebendige Baustelle (Kran mit Last, Krabben-Bauarbeiter, Schubkarre, Betonmischer, Funken, Prozent-Schild); ab und zu fliegt die Kamera hin und Kerstin berichtet. Steigt ein Haus eine Stufe auf: Bau-Animation und Feuerwerk direkt über dem Haus (je höher die Stufe, desto größer). Bei Fertigstellung eines Gebäudes: Bau-Animation (Gerüst, Kran, Krabben, Staub, Gebäude wächst nach oben), dann Feuerwerk.

## Leuchtturm-Rennen
Wer seine Stadt in den Chat schreibt („Köln“, „aus Hamburg“, „Team Wien“), gehört zu dieser Stadt (einmal wählen). Jeder weitere Kommentar macht den Leuchtturm 1 Stockwerk höher – pro Person höchstens alle 30 s (`turmSek`). Erkannt werden nur Städte aus `staedte.mjs`. Die Türme stehen im Meer links, oben und rechts (nie unten) und werden unter der Insel gezeichnet. Neue Spitzenreiter sagt Leda an; alle 3 Min. fliegt die Kamera kurz zum führenden Turm.

## Rangliste
„Beste Häuser“: höchste Haus-Stufe zuerst, bei gleicher Stufe die meisten Muscheln. Neuer Platz 1 oder Neueinsteiger in den Top 3 werden angesagt und als Banner gezeigt.

## Geschenke auf Deutsch
TikTok liefert die Geschenk-Namen auf Englisch – `geschenke.mjs` übersetzt sie mit Artikel und Mehrzahl: „Danke für die Rose“, „für den Löwen“, „für das Parfüm“, „für 3 Rosen“. Unbekannte Geschenke: „für das Geschenk „…““.

## Geschenk-Shows
**Geschenke:** nur ein schlichtes „Danke, Name!“ (Leda) mit Herz-Animation – für jedes Geschenk gleich, ohne Geschenk-Namen, ohne Abstufung nach Wert, ohne Muscheln, pro Person höchstens alle 10 Minuten.
- unter 10 Coins: Herzregen, Muschel-Konfetti oder Seifenblasen am Haus + Danke-Schild
- 10–99 Coins: springender Delfin mit Banner, Heißluftballon mit Namen oder Flugzeug mit Danke-Banner
- 100–999 Coins: Feuerwerk mit Namen, Yacht mit Namen am Rumpf oder Goldregen (Kamera fährt zum Haus)
- ab 1.000 Coins: Mega-Show – Krone, goldenes Leuchten, Dauerfeuerwerk, Name groß über der Insel
Große Geschenke werden vor kleinen gezeigt.

## Moderation
Kerstin redet ununterbrochen – mit kurzen, natürlichen Pausen (`…` in `saetze.mjs` = Sprechpause, Abstand zwischen Sätzen: `stimme.pauseSek`). Untertitel erscheinen genau dann, wenn er spricht.
Reihenfolge, wenn er frei ist:
1. Geschenke bedanken (immer, sofort) · Event-Ansagen · Countdown („noch dreißig Sekunden“, „zehn Sekunden“)
2. Follows bedanken (mehrere zusammengefasst)
3. Während eines Events: Spielstand live kommentieren, anfeuern, ab und zu ein Tipp
4. Sonst: Häuser zeigen (wer „haus“ geschrieben hat), neue Zuschauer begrüßen, Wiederkehrer mit „Willkommen zurück“ (ab dem 3. Besuch mit Danke für die Treue), erklären was Geschenke bringen, Rundgang (Kamera fliegt zu einem Haus, Kerstin stellt es vor), Tipps, Muschel-Tal-Fakten, Fragen an den Chat, Rangliste, Muschelkasse, Bauprojekt, Bewohner-Ziel, Teaser fürs nächste Event (ohne es zu verraten), Abendstimmung
Für jede Situation gibt es mehrere Varianten; der zuletzt benutzte Satz wird ausgelassen.

## Vollautomatisch
`Muschel-Tal LIVE starten.command` wartet, bis dein LIVE läuft, verbindet sich selbst, verbindet sich nach Abbrüchen neu und startet sich nach Fehlern automatisch wieder. Der Spielstand bleibt erhalten.
Der Mac bleibt automatisch wach, solange das Programm läuft (`caffeinate`). Das Einzige, was TikTok nicht erlaubt zu automatisieren: den LIVE in LIVE Studio starten.

## Schutz vor anstößigen Namen
- Namen mit anstößigen Wörtern (auch mit Zahlen/Sonderzeichen geschrieben, z. B. „f4ck“) werden zu „Bewohner 12“: nicht angezeigt, nicht vorgelesen. Liste in `filter.mjs`.
- `sperrliste.txt`: ein TikTok-Name pro Zeile – diese Person wird komplett ignoriert (kein Haus, keine Begrüßung, kein Dank). Gilt nach spätestens 30 s, auch während des Streams.
- Kommentar-Texte werden nie vorgelesen oder angezeigt. Jeder Satz von Kerstin wird vor dem Sprechen noch einmal geprüft.
- Zusätzlich empfohlen: in den TikTok-LIVE-Einstellungen den Stichwort-Filter für Kommentare einschalten.

## Leistung (für schwächere Macs)
- Die Seite rechnet intern mit 720×1280 und höchstens 30 Bildern pro Sekunde (so viel kommt bei TikTok an). Volle Größe: `http://localhost:8790/?aufloesung=1080`.
- Insel, Häuser, Kopfzeile und Muschelplatz werden zwischengespeichert und nur bei Änderungen neu gezeichnet.
- **In LIVE Studio** zusätzlich: Video-Einstellungen auf **720p (720×1280), 30 FPS**, Bitrate ca. 2.500–3.000 kbps. Das entlastet den Mac am meisten.
- „Muschel-Tal LIVE starten.command“ öffnet keinen Browser-Tab mehr (spart einen zweiten Durchlauf). Brauchst du doch einen (Fensteraufnahme): `http://localhost:8790` selbst öffnen.

## TikTok-Regeln (LIVE-Monetarisierung)
Kerstin und die Einblendungen werben **nie** für Geschenke: keine Sätze wie „jedes Geschenk bringt …“, keine Coin-Angaben, keine „+X 🐚“ bei Geschenken, keine Versprechen fürs Folgen. Geschenke werden nur bedankt (pro Person einmal). Folgen-Hinweis höchstens alle 15 Minuten, freundlich und ohne Gegenleistung. Verlosungen sind nie an Geschenke gebunden.

## Bildschärfe
- Die Kamera bleibt immer nah bei den Häusern (keine Gesamtansicht mehr) – große Häuser, große weiße Namensschilder in fester Bildschirmgröße.
- Schrift „Lilita One“ (Überschriften, Zahlen, Namen) und „Fredoka“ (Text), liegen in `seite/fonts` (frei, SIL Open Font License). Helle Schrift hat eine dunkle Kontur.
- LIVE Studio: Link-Quelle 1080 × 1920, in den Einstellungen höchste Auflösung (1080p), 30 FPS und die höchste Bitrate wählen.

## Ton (Musik + Stimme)
**Kerstins Stimme = Piper (offline):** Der macOS-Sprachdienst (`say`) blockiert, sobald LIVE Studio live ist. Darum erzeugt das Programm Kerstins Stimme selbst mit der freien Offline-Sprachsoftware **Piper** (deutsche Frauenstimme „Kerstin“, unbegrenzt, kostenlos). Beim ersten Start lädt „Muschel-Tal LIVE starten“ einmalig die Programmteile (npm) und die Stimme (ca. 60 MB). Ein Satz entsteht in ca. 0,2 s; hängt die Stimme, startet sie automatisch neu. Im Terminal steht dann „🗣️ Kerstin spricht mit der Offline-Stimme …“.

**Wichtig (LIVE Studio auf dem Mac):** Der Ton der Link-Quelle kommt bei LIVE Studio nicht im Stream an. Darum laufen Kerstin und die Musik über den Mac-Ton (`"wiedergabe": "mac"` in einstellungen.json) und gelangen über das kostenlose Programm **BlackHole** als „Mikrofon“ in LIVE Studio:
1. BlackHole 2ch installieren (kostenlos): existential.audio/blackhole – oder im Terminal `brew install blackhole-2ch`. Danach Mac neu starten.
2. Programm **Audio-MIDI-Setup** öffnen → unten links **+** → **Gerät mit mehreren Ausgängen erstellen** → Haken bei **MacBook-Lautsprecher** (bzw. deinen Lautsprechern) und **BlackHole 2ch**.
3. **Systemeinstellungen → Ton → Ausgabe:** „Gerät mit mehreren Ausgängen“ wählen. (Die Lautstärketasten gehen dann nicht – Lautstärke im Audio-MIDI-Setup.)
4. **LIVE Studio → Mikrofon: „BlackHole 2ch“.** Bei der Link-Quelle den Ton aus.
5. Beim Start öffnet sich automatisch ein **Ton-Tab** im Browser (http://localhost:8790/?ton): einmal **„Ton starten“** klicken und den Tab offen lassen (darf im Hintergrund sein). Kerstin und die Musik laufen dort – ohne für jeden Satz ein neues Programm zu starten (das hing an der Mehrfach-Ausgabe). Ist der Tab zu, übernimmt automatisch der Mac (say/afplay).
6. Test: wenn Kerstin spricht, schlägt in LIVE Studio der Mikrofon-Pegel aus.
Nach dem Stream kannst du in den Systemeinstellungen wieder die normalen Lautsprecher wählen.

- **Es spielt immer nur eine Seite Ton**, auch wenn Browser und LIVE Studio gleichzeitig offen sind (die zuerst geöffnete). Vor dem LIVE deshalb alte Browser-Tabs mit der Insel schließen – oder sie mit `?vorschau` öffnen (Bild ohne Ton).
- Im Hintergrund läuft ruhige, lizenzfreie Strand-/Urlaubsmusik („strand“, erzeugt mit `tools/make_music_strand.py`): 4 Stücke à 6 Min., langsam (65–68 bpm), Lounge-Stimmung – weicher Akkord-Teppich, warmer Bass, leise gedämpfte Gitarre, weicher Kick + Besen, sparsame tiefe Flöte, leise Wellen. Kein Klingklang, alles über ca. 1,8 kHz abgesenkt. Dazu sanftes, dumpfes Meeresrauschen. Musik liegt in `werkzeug/musik` (Updates überschreiben sie nie; neue Stücke aus „Downloads“ werden beim Start übernommen). Die „strand“-Stücke haben Vorrang vor älteren.
- Kerstin spricht kurze Sätze, etwa alle 2–4 Sekunden einer, je Satz nur eine Sache. Geschenke werden immer mit Namen bedankt („Danke für die Rose“) – je wertvoller, desto größer der Dank (4 Stufen: unter 20, ab 20, ab 200, ab 1.000 Coins).
- Kerstins Ansagen werden über die Live-Seite abgespielt, die Musik wird dabei automatisch leiser. So landet alles im Ton der Link-/Browser-Quelle.
- Falls ein Browser den Ton blockiert, steht unten „Einmal ins Bild klicken für Musik“ – einmal klicken genügt.
- Bei **Fensteraufnahme** statt Link-Quelle: in LIVE Studio zusätzlich den Mac-Ton (Systemaudio) aufnehmen.
- Lautstärken in `einstellungen.json` unter `ton`.

## Tageszeit
Tag, Sonnenaufgang, Sonnenuntergang (je 45 Min.) und Nacht wie auf muscheltal.de nach der echten Uhrzeit (Hamburg). Nachts leuchten Laternen, Fenster, Lagerfeuer und die Muschel.
Zum Ausprobieren: `http://localhost:8790/?zeit=21:30`.

## Stimme
Moderationsstimme: **Leda** über Google Gemini (menschlich, mit Gefühl je nach Satz). Gemini-Schlüssel wird beim ersten Start abgefragt (`gemini-schluessel.txt`, nur lokal).
- **Sparen:** Jedes Satzstück wird in `werkzeug/stimme` gespeichert und danach kostenlos abgespielt; Namen sind eigene Stücke („Danke fürs Folgen,“ + „Lara“).
- **Kontingent:** Das Programm zählt die Gemini-Anfragen pro Tag mit (`geminiProTag`, Tag nach Pazifik-Zeit wie bei Google) und nutzt nacheinander 3.8 Flash TTS, 3.1 Flash TTS und 2.5 Flash TTS (jedes Modell hat ein eigenes Tageslimit). Höchstens `geminiProMinute` pro Minute und Modell. Wird es knapp, gehen Geschenk-/Follow-Dank und neue Namen vor.
- **Notfall:** Ist Geminis Kontingent aufgebraucht oder antwortet Gemini nicht, spricht **Chirp-Leda** (Google Cloud Text-to-Speech, `de-DE-Chirp3-HD-Leda`) den ganzen Satz. Schlüssel: `google-tts-schluessel.txt` (Abfrage beim Start) – leer gelassen wird der Gemini-Schlüssel versucht (dafür im selben Google-Projekt die „Cloud Text-to-Speech API“ aktivieren). Die Statuszeile zeigt „Gemini heute noch … neue Sätze, Notfall Chirp: bereit“. Liefern Gemini und Chirp beide nichts (Internet, Störung), spricht als letzter Ersatz Kerstin (offline, `"ersatz": "kerstin"`) – es ist nie ganz still.
Ohne Stimme starten: `node server.mjs --still`.

## Hinweise
- Die TikTok-Verbindung nutzt die freie Bibliothek „TikTok-Live-Connector“ (inoffiziell). Ändert TikTok etwas, kann sie kurz ausfallen – das Programm versucht es automatisch weiter.
- Wichtige Infos stehen oben, unten bleibt Platz für TikToks Kommentarspalte.
- Die Insel ist noch ein Platzhalter; sobald die Live-Insel auf muscheltal.de existiert, wird sie hier eingesetzt.

## Wenn im LIVE nichts reagiert oder Kerstin stumm ist
- Im Terminal muss nach dem Live-Gehen **„✅✅✅ Mit deinem TikTok-LIVE verbunden“** stehen. Danach erscheint jedes Like, jeder Kommentar und jedes Geschenk als Zeile (❤️ 💬 🎁 👋).
- Alle 30 s zeigt eine **ℹ️-Zeile**: TikTok-Verbindung, Anzahl Ereignisse, Live-Seiten, über welchen Weg Kerstin spricht.
- Steht dort dauerhaft „TikTok: nicht verbunden“: kostenlosen Schlüssel auf eulerstream.com holen und in `einstellungen.json` bei `eulerApiKey` eintragen.
- Bestätigt die Live-Seite Kerstins Stimme nicht, spricht sie automatisch über die Mac-Lautsprecher.

## Erfolg „Live dabei“ auf muscheltal.de
Alle Zuschauer, die im echten LIVE etwas tun (beitreten, kommentieren, liken, folgen, teilen, schenken), werden alle 15 s an `https://muscheltal.de/api/live` gemeldet und bekommen dort den Erfolg „📺 Live dabei“. Dafür beim ersten Start den Schlüssel einfügen (wird nur lokal in `live-schluessel.txt` gespeichert, nicht im Repo). Im Test-Modus wird nichts gemeldet.

## LIVE-Rangliste auf muscheltal.de
Mit demselben Schlüssel schickt die App alle 2 Minuten (nur bei Änderungen) und am Stream-Ende die **Top 10 insgesamt** und die **Top 10 des aktuellen/letzten Streams** (gesammelte Muscheln in diesem Stream) an `https://muscheltal.de/api/live`. Die Homepage zeigt sie unter „🔴 LIVE-Rangliste“ (Startseite + Knopf „🏆 Rangliste“ auf der LIVE-Insel). Ein neuer Stream beginnt beim Verbinden, wenn der letzte vor über 30 Min. endete.

**Orte-Liste:** `orte-dach.txt` enthält ca. 11.000 Städte, Gemeinden und Dörfer aus Deutschland, Österreich, der Schweiz, Liechtenstein und Luxemburg (Daten: GeoNames, CC BY 4.0, über das npm-Paket cities.json). `orte-mehrdeutig.txt` listet Ortsnamen, die auch normale Wörter sind („Sand“, „Wald“, „Regen“) – die zählen nur mit „aus …“, „Team …“ oder „von …“. Bundesländer, Kantone und Regionen (Bayern, NRW, Tirol, Ostsee …) stehen zusätzlich in `staedte.mjs`.
