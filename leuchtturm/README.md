# 🗼 Leuchtturm-Rennen (TikTok LIVE)

Ein eigenes LIVE-Spiel: Jede Stadt, jedes Dorf, jede Gemeinde aus Deutschland, Österreich und der Schweiz bekommt eine kleine Insel mit Leuchtturm.

## So spielen die Zuschauer
- **Stadt in den Chat schreiben**: Die Stadt bekommt eine Insel. Tippfehler wie „Hambrug“ oder „Koeln“ werden erkannt.
- **Jeder Kommentar**: +1 m für die eigene Stadt (pro Person höchstens alle 30 s).
- **❤️ Herz-Emoji im Chat**: +1 m (pro Person alle 5 s). **🎁 im Chat**: Mega-Bauschub +25 m (pro Person einmal pro Minute). Gemeint sind nur Emojis im Chat, echte TikTok-Geschenke bringen nichts.
- **Gründer**: Wer eine Stadt als Erstes schreibt, steht für immer am Leuchtturm.
- **Ranglisten**: Gesamt, Heute, Diese Woche und Bundesländer/Kantone (wechseln oben links). Die Stadt des Tages ist die Stadt, die heute am meisten gebaut hat.
- **Städte-Fieber**: Schreiben 6 Leute einer Stadt innerhalb von 30 s, zählt 45 s lang alles doppelt.
- **Alle 2 Minuten ein Event** (15 verschiedene, u. a. Nachbar-Duell nahe Städte, Bundesland-Duell, Herz-Regen) mit Bonus-Metern.
- Der Turm wächst ohne Grenze, Höhe in Metern mit Höhenzonen (Küste → Wolken → Flughöhe → Weltall → Mondnähe). 16 Upgrades von der Fahne bis zu Planetenringen.
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
- **TikTok-Regeln:** Herzen, Folgen, Teilen und Geschenke bringen keine Belohnung und werden nicht angesagt. Es gibt nur ein „Danke, Name!“. Herzen zählen still mit (10 Herzen = 1 m).

Alle Zahlen stehen in `einstellungen.json`. Port 8791, damit es nie mit Muschel-Tal LIVE (8790) kollidiert.
