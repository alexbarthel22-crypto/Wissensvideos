# 🗼 Leuchtturm-Rennen (TikTok LIVE)

Ein eigenes LIVE-Spiel: Jede Stadt, jedes Dorf, jede Gemeinde aus Deutschland, Österreich und der Schweiz bekommt eine kleine Insel mit Leuchtturm.

## So spielen die Zuschauer
- **Stadt in den Chat schreiben**: Die Stadt bekommt eine Insel. Tippfehler wie „Hambrug“ oder „Koeln“ werden erkannt.
- **Jeder Kommentar**: +1 Stockwerk für die eigene Stadt (pro Person höchstens alle 30 s).
- **Städte-Fieber**: Schreiben 6 Leute einer Stadt innerhalb von 30 s, zählt 45 s lang alles doppelt.
- **Alle 2 Minuten ein Event** (12 verschiedene) mit Bonus-Stockwerken.
- Der Turm wächst ohne Grenze. Ab bestimmten Höhen gibt es 16 Upgrades, von der Fahne bis zu Planetenringen.
- Bei Stream-Ende wird die **Stadt des Tages** gekürt.

## Starten
1. Ordner auf den Schreibtisch legen.
2. **„Leuchtturm-Rennen starten.command“** doppelklicken. Beim ersten Mal: Rechtsklick → Öffnen.
3. Den https-Link aus dem Terminal in LIVE Studio als Link-Quelle einfügen (1080×1920).
4. Im Ton-Tab (`localhost:8791/?ton`) einmal auf „Ton starten“ klicken. Ton wie bei Muschel-Tal über BlackHole.

Zum Ausprobieren ohne TikTok: **„Leuchtturm-Rennen testen.command“**.

## Stimme, Musik und Regeln
- **Stimme:** Leda (Gemini). Die Schlüssel werden mit Muschel-Tal LIVE geteilt (`~/.muscheltal`). Gespeicherte Sätze und das Tageskontingent werden mitbenutzt, wenn „Muschel-Tal LIVE“ auf dem Schreibtisch liegt.
- **Musik:** eigene, lizenzfreie Lagunen-Musik (`seite/musik/lagune_*.mp3`, erzeugt mit `tools/make_music_lagune.py`).
- **TikTok-Regeln:** Herzen, Folgen, Teilen und Geschenke bringen keine Belohnung und werden nicht angesagt. Es gibt nur ein „Danke, Name!“. Herzen zählen still mit (10 Herzen = 1 Stockwerk).

Alle Zahlen stehen in `einstellungen.json`. Port 8791, damit es nie mit Muschel-Tal LIVE (8790) kollidiert.
