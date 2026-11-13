# 🐚 Muschel-Tal LIVE

Automatischer TikTok-LIVE: Zuschauer bauen mit Likes, Kommentaren und Geschenken ihr eigenes Haus auf der Live-Insel.
Eine Mac-Stimme (unbegrenzt, offline) moderiert.

## Einmal einrichten (Mac)
1. **Node.js** installieren: https://nodejs.org → LTS → „macOS Installer (.pkg)“.
2. **Nur diesen Ordner `live/`** herunterladen (er funktioniert allein – Bewohnerzahl und Bauprojekte holt er sich selbst aus dem Repo). Den Ordner kannst du beliebig umbenennen und ablegen.
3. Im Ordner auf **„Muschel-Tal LIVE testen.command“** doppelklicken.
   Falls der Mac warnt: Rechtsklick → „Öffnen“ → „Öffnen“.
   Es öffnet sich die Insel mit Test-Zuschauern, Anna spricht.

**Spielstand:** wird automatisch in `stand.json` gespeichert (alle 10 Sekunden, beim Stream-Ende und beim Schließen des Fensters). Beim nächsten Start geht alles genau dort weiter. Einfach immer denselben Ordner benutzen.
**Update auf eine neue Version:** neuen Ordner holen und deine `stand.json` (Spielstand) und `sperrliste.txt` hineinkopieren.
**Ganz von vorne:** `stand.json` löschen.

## Stream starten
1. In TikTok LIVE Studio den LIVE starten (Hochformat).
2. **„Muschel-Tal LIVE starten.command“** doppelklicken. Das Programm wartet, bis der LIVE von @muscheltal läuft, und verbindet sich dann selbst.
3. In LIVE Studio als Quelle hinzufügen: **Link/Browser** → `http://localhost:8790` (1080 × 1920).
   Gibt es keine Link-Quelle: Browserfenster mit der Seite als **Fensteraufnahme** hinzufügen.
4. Ende: LIVE beenden, dann im Terminalfenster `ctrl + C`. Der Spielstand liegt in `stand.json` und geht beim nächsten Stream weiter.

## Regeln (änderbar in `einstellungen.json`)
| Aktion | Wirkung |
|---|---|
| Erster Like/Kommentar | eigenes Grundstück mit @Namen – wer früher kommt, wohnt näher an der Muschel |
| 1 Like | 1 Muschel in die **Muschelkasse der Live-Insel** (getrennt von der Inselkasse der Haupt-Insel) + 1 Muschel fürs eigene Haus |
| Haus-Stufen (20) | Zelt → Hängematten-Camp → Strohhütte → Fischerhütte → Stelzenhütte → Baumhaus → Bungalow → Surferhütte → Strandhaus → Leuchtturmhaus → Ferienhaus → Poolhaus → Villa → Glasvilla → Luxusvilla → Inselvilla mit Hubschrauberlandeplatz → Strandpalast → Korallenpalast → Muschelschloss → Perlenschloss |
| Rangliste „Beste Häuser“ | höchste Haus-Stufe zuerst, bei Gleichstand entscheiden die Muscheln aus Events |
| Kommentar `palme` `flagge` `garten` `laterne` `pool` `boot` | Anbau (ab bestimmter Stufe) |
| Kommentar `rot` `blau` `lila` … | Hausfarbe |
| Kommentar `haus` (auch Haus!, hauus, house, huas, mein haus …) | ab und zu fliegt die Kamera zum eigenen Haus, Anna: „…, hier ist dein Haus!“ |
| Geschenk | **1 Coin = 1 Muschel (= 0,01 €)** – für die Muschelkasse und fürs eigene Haus, große Geschenke = Feuerwerk |
| Folgen | neuer **Bewohner** + 5 Muscheln in die Muschelkasse |
| Stream teilen | 2 Muscheln in die Muschelkasse |
| Abstimmung (eins der Events) | nächstes Stadtgebäude, wird mit Muscheln aus der Muschelkasse gebaut |

Die Insel startet mit 200 Grundstücken und **wächst live**, sobald alle belegt sind (jeweils ca. 60 neue).
Ausbauten werden animiert gebaut (Bambusgerüst, Krabben-Bauarbeiter, Sandstaub), die Kamera fährt dabei an das Haus heran; sonst wechselt sie zwischen Übersicht und kleinen Rundfahrten.
Oben steht immer das **nächste Bauprojekt der Haupt-Insel** – automatisch aus `muscheltal/daten/insel.json` (`baustellen`), Startzahl der Bewohner aus `einwohner.csv`. Straßennamen stehen unter `strassen`.
Die Bewohnerzahl kommt live von TikTok (Follower), `bewohner.start` ist nur der Startwert, falls TikTok sie nicht liefert.

## Überraschungs-Events (alle 3 Minuten, 40 verschiedene)
Rechts oben läuft ein Countdown „Nächstes Event“ – welches kommt, bleibt geheim (❓❓❓). Nie dasselbe wie eins der letzten 10.
Beim Start sagt Anna, was am Ende passiert (steht auch im Event-Feld unter 🏆). Am Ende nennt sie die Gewinner mit Namen (im Ergebnis-Feld unter 🏆).
Alle Events laufen komplett im Stream, mitmachen per Like oder Kommentar – niemand muss den Stream verlassen, nichts ist an Geschenke gebunden.
Like-Ziele liegen bei ca. 80 % des normalen Like-Tempos: schaffbar, wenn alle mitmachen. Alle 40 Events sind automatisch geprüft (Test-Zuschauer machen mit, Belohnungen kommen an).

| Event | Mitmachen | Belohnung |
|---|---|---|
| 🌊 Sturmflut | gemeinsam liken | Deich hält → 20 🐚 für alle Helfer |
| 🎡 Muschel-Glücksrad | in den letzten 10 Min. aktiv | 150–500 🐚, goldenes Dach oder Pool |
| 🦀 Krabbenrennen | `rot` `blau` `gelb` `grün` oder einfach liken | Siegerteam 25 🐚 |
| ⚔️ Team-Duell | `muschel` / `kokos` oder einfach liken | Siegerteam 30 🐚 |
| 🍾 Flaschenpost | zuerst `flasche` | 40–150 🐚 / Anbau |
| 🐋 Besuch vom Meer | `hallo` | 10 🐚 je Gruß |
| 🏠 Hausbesuch | – (Kamera besucht ein aktives Haus) | 25 🐚 |
| ✨ Muschelregen | liken | Likes zählen doppelt fürs Haus |
| ⚡ Bau-Turbo | liken | Likes zählen dreifach fürs Haus |
| 🗺️ Schatzsuche | `A` `B` `C` `D` | richtige 30 🐚 |
| 🔢 Zahlenraten | Zahl 1–100 (mit Hinweisen) | Treffer 100 🐚 |
| 🎉 Strandparty | Stimmung per Likes | Feuerwerk + 15 🐚 |
| 🐦 Möwenalarm | `fang` (erste 5) | 20 🐚 |
| 🌠 Sternschnuppe | `wunsch` | einer bekommt einen Anbau |
| 🗳️ Abstimmung | `1` `2` `3` | nächstes Stadtgebäude |
| ⌨️ Wortjagd | gezeigtes Wort abtippen (erste 3) | 40 / 25 / 15 🐚 |
| 🍹 Cocktail-Mix | `mango` `kokos` `ananas` | Mehrheit 15 🐚 |
| 🎈 Ballon-Platzen | liken | wer einen Ballon platzen lässt: 10 🐚 |
| 🐢 Schildkröten-Rettung | gemeinsam liken | 20 🐚 für alle Helfer |
| 🌺 Blumenwiese | `blume` | ab 25 Blumen 15 🐚 für alle |
| 🧩 Emoji-Rätsel | Lösung schreiben (z. B. „Sandburg“) | 50 🐚 |
| 🏐 Beachvolleyball | `links` / `rechts` oder einfach liken | Siegerteam 25 🐚 |
| 🦈 Hai-Alarm | `ufer` (erste 10) | 15 🐚 |
| 🍦 Eiswagen | gemeinsam liken | 15 🐚 für alle |
| 🍀 Glückszahl | Zahl 1–10 | richtige 30 🐚 |
| ❓ Strand-Quiz | `A` `B` `C` | richtige 20 🐚 |
| 🐚 Muscheln sammeln | `sammeln` (erste 20) | 12 🐚 |
| 🏄 Surf-Contest | `surf`, dann liken | Bester 60 🐚 |
| 🥥 Kokosnuss-Weitwurf | `wurf` | weitester Wurf 40 🐚 |
| 📸 Inselfoto | `cheese` | 8 🐚 + Name auf dem Foto |
| 🪢 Tauziehen | `muschel` / `seestern` oder einfach liken | Siegerteam 25 🐚 |
| 🔤 Buchstabensalat | Wort aus den Buchstaben schreiben | 50 🐚 |
| 🎲 Muschel-Würfeln | `würfel` | jede Sechs 30 🐚 |
| 🦜 Papagei | gezeigten Satz nachschreiben (erste 5) | 20 🐚 |
| 🌈 Regenbogen malen | `rot` `orange` `gelb` `grün` `blau` `lila` | komplett: 20 🐚 für alle Maler |
| 🐠 Fische zählen | Anzahl der Fische schreiben | genau 30 🐚, ±1 10 🐚 |
| 🏆 Like-Rekord | 30 Sekunden liken | Rekord gebrochen: 25 🐚 für alle |
| 🎭 Motto des Tages | `1` `2` `3` | Mehrheit 10 🐚 |
| 🎁 Mystery-Box | `box` | 3–50 🐚 für jeden |
| 🕵️ Wer bin ich? | Tier erraten (3 Hinweise) | 50 🐚 |

## Stadtgebäude (ohne Limit)
Per Abstimmung wählt der Chat das nächste Gemeinschafts-Gebäude, bezahlt wird aus der Muschelkasse:
Rathaus, Schule, Krankenhaus, Feuerwache, Polizeistation, Supermarkt, Kino, Bibliothek, Post, Café, Eisdiele, Museum, Sporthalle, Markthalle, Hotel, Apotheke, Aquarium, Theater, Schwimmbad, Kindergarten, Restaurant, Friseur, Muschelbank, Inselbahnhof – alle im tropischen Strand-Stil (Palmen, Markisen, Stroh- und Ziegeldächer).
Gebäude dürfen mehrfach gebaut werden (noch nicht gebaute kommen bei der Abstimmung zuerst). Bauplätze: zuerst das Stadtzentrum um den Muschelplatz, dann über die ganze Insel verteilt (fest vorgemerkt, Häuser ziehen nie um). Reichen die Plätze nicht, wächst die Insel – bis ca. 60 Gebäude und 1.800 Grundstücke.
Während des Baus: lebendige Baustelle (Kran mit Last, Krabben-Bauarbeiter, Schubkarre, Betonmischer, Funken, Prozent-Schild); ab und zu fliegt die Kamera hin und Anna berichtet. Bei Fertigstellung: Bau-Animation (Gerüst, Kran, Krabben, Staub, Gebäude wächst nach oben), dann Feuerwerk.

## Rangliste
„Beste Häuser“: höchste Haus-Stufe zuerst, bei Gleichstand die Muscheln aus Events. Neuer Platz 1 oder Neueinsteiger in den Top 3 werden angesagt und als Banner gezeigt.

## Geschenke auf Deutsch
TikTok liefert die Geschenk-Namen auf Englisch – `geschenke.mjs` übersetzt sie mit Artikel und Mehrzahl: „Danke für die Rose“, „für den Löwen“, „für das Parfüm“, „für 3 Rosen“. Unbekannte Geschenke: „für das Geschenk „…““.

## Geschenk-Shows
Jedes Geschenk wird bedankt (Anna) und bekommt eine Show mit dem Namen des Spenders – je wertvoller, desto größer:
- unter 10 Coins: Herzregen, Muschel-Konfetti oder Seifenblasen am Haus + Danke-Schild
- 10–99 Coins: springender Delfin mit Banner, Heißluftballon mit Namen oder Flugzeug mit Danke-Banner
- 100–999 Coins: Feuerwerk mit Namen, Yacht mit Namen am Rumpf oder Goldregen (Kamera fährt zum Haus)
- ab 1.000 Coins: Mega-Show – Krone, goldenes Leuchten, Dauerfeuerwerk, Name groß über der Insel
Große Geschenke werden vor kleinen gezeigt.

## Moderation
Anna redet ununterbrochen – mit kurzen, natürlichen Pausen (`…` in `saetze.mjs` = Sprechpause, Abstand zwischen Sätzen: `stimme.pauseSek`). Untertitel erscheinen genau dann, wenn er spricht.
Reihenfolge, wenn er frei ist:
1. Geschenke bedanken (immer, sofort) · Event-Ansagen · Countdown („noch dreißig Sekunden“, „zehn Sekunden“)
2. Follows bedanken (mehrere zusammengefasst)
3. Während eines Events: Spielstand live kommentieren, anfeuern, ab und zu ein Tipp
4. Sonst: Häuser zeigen (wer „haus“ geschrieben hat), neue Zuschauer begrüßen, Wiederkehrer mit „Willkommen zurück“ (ab dem 3. Besuch mit Danke für die Treue), erklären was Geschenke bringen, Rundgang (Kamera fliegt zu einem Haus, Anna stellt es vor), Tipps, Muschel-Tal-Fakten, Fragen an den Chat, Rangliste, Muschelkasse, Bauprojekt, Bewohner-Ziel, Teaser fürs nächste Event (ohne es zu verraten), Abendstimmung
Für jede Situation gibt es mehrere Varianten; der zuletzt benutzte Satz wird ausgelassen.

## Vollautomatisch
`Muschel-Tal LIVE starten.command` wartet, bis dein LIVE läuft, verbindet sich selbst, verbindet sich nach Abbrüchen neu und startet sich nach Fehlern automatisch wieder. Der Spielstand bleibt erhalten.
Der Mac bleibt automatisch wach, solange das Programm läuft (`caffeinate`). Das Einzige, was TikTok nicht erlaubt zu automatisieren: den LIVE in LIVE Studio starten.

## Schutz vor anstößigen Namen
- Namen mit anstößigen Wörtern (auch mit Zahlen/Sonderzeichen geschrieben, z. B. „f4ck“) werden zu „Bewohner 12“: nicht angezeigt, nicht vorgelesen. Liste in `filter.mjs`.
- `sperrliste.txt`: ein TikTok-Name pro Zeile – diese Person wird komplett ignoriert (kein Haus, keine Begrüßung, kein Dank). Gilt nach spätestens 30 s, auch während des Streams.
- Kommentar-Texte werden nie vorgelesen oder angezeigt. Jeder Satz von Anna wird vor dem Sprechen noch einmal geprüft.
- Zusätzlich empfohlen: in den TikTok-LIVE-Einstellungen den Stichwort-Filter für Kommentare einschalten.

## Leistung (für schwächere Macs)
- Die Seite rechnet intern mit 720×1280 und höchstens 30 Bildern pro Sekunde (so viel kommt bei TikTok an). Volle Größe: `http://localhost:8790/?aufloesung=1080`.
- Insel, Häuser, Kopfzeile und Muschelplatz werden zwischengespeichert und nur bei Änderungen neu gezeichnet.
- **In LIVE Studio** zusätzlich: Video-Einstellungen auf **720p (720×1280), 30 FPS**, Bitrate ca. 2.500–3.000 kbps. Das entlastet den Mac am meisten.
- „Muschel-Tal LIVE starten.command“ öffnet keinen Browser-Tab mehr (spart einen zweiten Durchlauf). Brauchst du doch einen (Fensteraufnahme): `http://localhost:8790` selbst öffnen.

## Ton (Musik + Stimme)
- **Es spielt immer nur eine Seite Ton**, auch wenn Browser und LIVE Studio gleichzeitig offen sind (die zuerst geöffnete). Vor dem LIVE deshalb alte Browser-Tabs mit der Insel schließen – oder sie mit `?vorschau` öffnen (Bild ohne Ton).
- Im Hintergrund läuft die Südsee-Musik aus den Muschel-Tal-Videos (lizenzfrei, erzeugt mit `tools/make_music_tropical.py`, 3 Stücke à 3 Min. im Wechsel) plus Meeresrauschen (`tools/make_ambience.py`).
- Annas Ansagen werden über die Live-Seite abgespielt, die Musik wird dabei automatisch leiser. So landet alles im Ton der Link-/Browser-Quelle.
- Falls ein Browser den Ton blockiert, steht unten „Einmal ins Bild klicken für Musik“ – einmal klicken genügt.
- Bei **Fensteraufnahme** statt Link-Quelle: in LIVE Studio zusätzlich den Mac-Ton (Systemaudio) aufnehmen.
- Lautstärken in `einstellungen.json` unter `ton`.

## Tageszeit
Tag, Sonnenaufgang, Sonnenuntergang (je 45 Min.) und Nacht wie auf muscheltal.de nach der echten Uhrzeit (Hamburg). Nachts leuchten Laternen, Fenster, Lagerfeuer und die Muschel.
Zum Ausprobieren: `http://localhost:8790/?zeit=21:30`.

## Stimme
Standard: **Anna (Premium)**. Andere Stimme → in `einstellungen.json` bei `"mac"` eintragen (Namen: `say -v '?' | grep de_DE`).
Ohne Stimme starten: `node server.mjs --still`.

## Hinweise
- Die TikTok-Verbindung nutzt die freie Bibliothek „TikTok-Live-Connector“ (inoffiziell). Ändert TikTok etwas, kann sie kurz ausfallen – das Programm versucht es automatisch weiter.
- Wichtige Infos stehen oben, unten bleibt Platz für TikToks Kommentarspalte.
- Die Insel ist noch ein Platzhalter; sobald die Live-Insel auf muscheltal.de existiert, wird sie hier eingesetzt.
