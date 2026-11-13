# 🐚 Muschel-Tal LIVE

Automatischer TikTok-LIVE: Zuschauer bauen mit Likes, Kommentaren und Geschenken ihr eigenes Haus auf der Live-Insel.
Eine Mac-Stimme (unbegrenzt, offline) moderiert.

## Einmal einrichten (Mac)
1. **Node.js** installieren: https://nodejs.org → LTS-Version.
2. Dieses Repo herunterladen (GitHub → grüner Knopf „Code“ → „Download ZIP“, Branch `claude/serene-dijkstra-z5qm94`) und entpacken.
3. Im Ordner `live/` auf **„Muschel-Tal LIVE testen.command“** doppelklicken.
   Falls der Mac warnt: Rechtsklick → „Öffnen“ → „Öffnen“.
   Es öffnet sich die Insel mit Test-Zuschauern, Markus spricht.

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
| Haus-Stufen | Zelt → Strohhütte → Stelzenhütte → Bungalow → Strandhaus → Ferienhaus → Villa → Luxusvilla → Strandpalast → Muschelschloss |
| Kommentar `palme` `flagge` `garten` `laterne` `pool` `boot` | Anbau (ab bestimmter Stufe) |
| Kommentar `rot` `blau` `lila` … | Hausfarbe |
| Geschenk | **1 Coin = 1 Muschel (= 0,01 €)** – für die Muschelkasse und fürs eigene Haus, große Geschenke = Feuerwerk |
| Folgen | neuer **Bewohner** + 5 Muscheln in die Muschelkasse |
| Stream teilen | 2 Muscheln in die Muschelkasse |
| Abstimmung alle 10 Min. (`1`/`2`/`3`) | Gemeinschaftsprojekt, wird mit Muscheln aus der Muschelkasse gebaut |

Die Insel startet mit 200 Grundstücken und **wächst live**, sobald alle belegt sind (jeweils ca. 60 neue).
Ausbauten werden animiert gebaut (Bambusgerüst, Krabben-Bauarbeiter, Sandstaub), die Kamera fährt dabei an das Haus heran; sonst wechselt sie zwischen Übersicht und kleinen Rundfahrten.
Oben steht immer das **nächste Bauprojekt der Haupt-Insel** – automatisch aus `muscheltal/daten/insel.json` (`baustellen`), Startzahl der Bewohner aus `einwohner.csv`. Straßennamen stehen unter `strassen`.
Die Bewohnerzahl kommt live von TikTok (Follower), `bewohner.start` ist nur der Startwert, falls TikTok sie nicht liefert.

## Ton (Musik + Stimme)
- Im Hintergrund läuft die Südsee-Musik aus den Muschel-Tal-Videos (lizenzfrei, erzeugt mit `tools/make_music_tropical.py`, 3 Stücke à 3 Min. im Wechsel) plus Meeresrauschen (`tools/make_ambience.py`).
- Markus' Ansagen werden über die Live-Seite abgespielt, die Musik wird dabei automatisch leiser. So landet alles im Ton der Link-/Browser-Quelle.
- Falls ein Browser den Ton blockiert, steht unten „Einmal ins Bild klicken für Musik“ – einmal klicken genügt.
- Bei **Fensteraufnahme** statt Link-Quelle: in LIVE Studio zusätzlich den Mac-Ton (Systemaudio) aufnehmen.
- Lautstärken in `einstellungen.json` unter `ton`.

## Tageszeit
Tag, Sonnenaufgang, Sonnenuntergang (je 45 Min.) und Nacht wie auf muscheltal.de nach der echten Uhrzeit (Hamburg). Nachts leuchten Laternen, Fenster, Lagerfeuer und die Muschel.
Zum Ausprobieren: `http://localhost:8790/?zeit=21:30`.

## Stimme
Standard: **Markus (Erweitert)**. Andere Stimme → in `einstellungen.json` bei `"mac"` eintragen (Namen: `say -v '?' | grep de_DE`).
Ohne Stimme starten: `node server.mjs --still`.

## Hinweise
- Die TikTok-Verbindung nutzt die freie Bibliothek „TikTok-Live-Connector“ (inoffiziell). Ändert TikTok etwas, kann sie kurz ausfallen – das Programm versucht es automatisch weiter.
- Wichtige Infos stehen oben, unten bleibt Platz für TikToks Kommentarspalte.
- Die Insel ist noch ein Platzhalter; sobald die Live-Insel auf muscheltal.de existiert, wird sie hier eingesetzt.
