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
| Erster Like/Kommentar | eigenes Grundstück mit @Namen (Zelt) |
| 1 Like | 1 Muschel 🐚 |
| Muscheln | Zelt (0) → Hütte (30) → Haus (150) → Villa (500) → Palast (1500) |
| Kommentar `garten` `pool` `boot` `palme` `laterne` `flagge` | Anbau (ab bestimmter Stufe + Mindest-Muscheln) |
| Kommentar `rot` `blau` `lila` … | Hausfarbe |
| Geschenk | 30 Muscheln pro Diamant (Rose = 30), große Geschenke = Feuerwerk |
| Folgen | 25 Muscheln + Einzug-Banner |
| Abstimmung alle 10 Min. (`1`/`2`/`3`) | Gemeinschaftsprojekt in der Inselmitte, 25 % aller Muscheln fließen hinein |

## Stimme
Standard: **Markus (Erweitert)**. Andere Stimme → in `einstellungen.json` bei `"mac"` eintragen (Namen: `say -v '?' | grep de_DE`).
Ohne Stimme starten: `node server.mjs --still`.

## Hinweise
- Die TikTok-Verbindung nutzt die freie Bibliothek „TikTok-Live-Connector“ (inoffiziell). Ändert TikTok etwas, kann sie kurz ausfallen – das Programm versucht es automatisch weiter.
- Wichtige Infos stehen oben, unten bleibt Platz für TikToks Kommentarspalte.
- Die Insel ist noch ein Platzhalter; sobald die Live-Insel auf muscheltal.de existiert, wird sie hier eingesetzt.
