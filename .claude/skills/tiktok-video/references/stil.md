# Stilregeln aus den Referenzvideos

Drei Referenzen wurden Frame für Frame analysiert (alle 9:16, 75–110 s, durchgehender Ton):

- **A1/A2 – 3D-Simulation** („What if all men / all humans disappeared?“): Low-Poly-3D, Zeitleiter +10 Sek → +1 Mio. Jahre, Serifenschrift, Statistik oben in Hellblau.
- **B – 2D-Story** (Deutsch, „Greta, die letzte Frau“): flache Vektorgrafik auf Dunkelblau, Neon-Akzente, Karaoke-Untertitel. **Das ist der Hauptstil**, weil er deutsch ist und sich mit HyperFrames exakt nachbauen lässt. Von A übernehmen wir die Zeitleiter-Dramaturgie und die großen Statistik-Zahlen.

## Bildsprache (Stil B)

| Element | Vorgabe |
| --- | --- |
| Hintergrund | Dunkles Navy mit radialer Aufhellung in der Mitte (`#1c2250 → #121634 → #0a0c1d`) und feinen Sternen. Einzelne Szenen dürfen eigenen Grund haben (Morgenhimmel, Zimmer), bleiben aber dunkel. |
| Grafik | Flache Formen ohne Konturen, abgerundete Ecken, wenige Farben pro Objekt. Figuren: Kopf-Kreis + abgerundeter Körper, einfache Gesichter. Objekte (Handy, Server, Radio, Tür) zentral, groß, eins pro Moment. |
| Kapitel-Marke | Oben mittig (y ≈ 176), Monospace-Versalien in Goldgelb `#f4d27a`, dünner Goldrahmen, z. B. `19. NOV · 07:00`, `REGEL 2 · UNSICHTBAR`. Wechselt mit jeder Szene. |
| Checkliste | Oben links, kleine Mono-Chips mit rotem Rahmen, wachsen mit der Geschichte (`1. SERVER ✕`). |
| Zähler-Box | Unter der Kapitel-Marke: Rahmen in Akzentfarbe mit Glow, kleines Label in Mono-Versalien, große Zahl in Inter Black. Zahlen zählen sichtbar hoch/runter (deutsches Tausenderformat). |
| Untertitel | Inter Black 80 px, Versalien, zentriert bei y ≈ 1150–1370. Wort für Wort: noch nicht gesprochen = grau `#7d8197`, gesprochen = weiß, Schlüsselwort = Farbe + Glow. 2–4 Wörter pro Gruppe, kurzer Pop beim Erscheinen. Harter Schatten `0 5px 0 rgba(0,0,0,.55)`. |
| Farben | Gelb `#ffd43b`, Rot `#ff3b55`, Pink `#ff4fb0`, Grün `#39e27a`, Blau `#4da3ff`. Pro Bild ein Fokus. |
| Panels | Dunkle Karten `rgba(20,24,56,.9)` mit `#2e3670`-Rahmen, Warn-Panels rot mit Glow. |

Neon, Glow, Mono-Labels und HUD-Elemente sind hier **gewollt** (sie stammen aus der Referenz), obwohl HyperFrames sie sonst als Default verbietet – aber nur so, wie die Referenz sie nutzt: Kapitel-Marke, Checkliste, Zähler-Box, Glow auf Schlüsselwörtern.

## Dramaturgie

1. **Hook (0–7 s)**: Frage als Untertitel + großes Symbolbild (Globus mit Zähler). Frame 0 zeigt schon Globus und Kapitel-Marke.
2. **Auslöser**: der Moment, in dem es losgeht (Knopfdruck, Nachricht, „Sekunde 0“).
3. **Zeitleiter**: 7–9 Stationen mit Uhrzeit/Tag in der Kapitel-Marke. Jede Station = eine sichtbare Folge + eine Zahl. Folgen bauen aufeinander auf (Server → Internet → Strom → Arbeit → Wirtschaft → Alltag).
4. **Kontrast-Moment**: eine Pointe, die zwei Welten gegenüberstellt (z. B. „In Vice City herrscht Chaos. In echten Städten: Stille.“).
5. **Ende**: Rückkehr zum Anfangsbild (Zähler, Uhr) + Cliffhanger oder Frage an die Zuschauer (Kommentar-Köder). Letzte Zeile hält ≥ 2,5 s.

Tempo: alle 2–4 s ein neuer Bildschlag, Sätze kurz (3–8 Wörter), Erzähler in 2. Person oder neutral-dramatisch. Zahlen plausibel halten (überschlagen, im Skript kommentieren) – es ist ein Gedankenexperiment, aber keine erfundenen „Fakten“ als Fakten verkaufen.

## Bewegung

- Ankunft: `expo.out` / `back.out(1.6–2)` in 0,3–0,5 s; Abgang: Blur 8 px + Fade in 0,18 s.
- Ein Hauptobjekt pro Moment; was gesagt wird, passiert im Bild **auf dem Wort** (`at("L4", "Server")`).
- Erschütterung (x ±8 px, 0,04 s, 3–7 Wiederholungen) für Crash/Fehler, Flackern über Overlay-Opacity.
- Keine Dauerschleifen; Blinken nur mit endlicher Wiederholung.

## QA vor dem Rendern

- Frame 0 nicht leer; jede Szene hat zur Mitte ein klar lesbares Bild.
- Nichts überlappt die Checkliste oben links oder die Untertitelzone ab y = 1150.
- Zahlen in Boxen passen in die Box (lange Zahlen 42–44 px).
- Objekte lesen sich als das, was sie sein sollen (ein Kühlturm braucht Dampf, sonst wirkt er wie ein Becher).
- `check` ohne Fehler, Texte ≥ 28 px außer Checkliste.
