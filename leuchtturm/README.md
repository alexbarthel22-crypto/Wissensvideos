# 🗼 Leuchtturm-Rennen (TikTok LIVE)

Ein eigenes LIVE-Spiel: Jede Stadt, jedes Dorf, jede Gemeinde aus Deutschland, Österreich und der Schweiz bekommt eine kleine Insel mit Leuchtturm.

## So spielen die Zuschauer
- **Stadt in den Chat schreiben**: Jedes Mal +1 m für diese Stadt (pro Person alle 3 s). Man kann auch andere Städte schreiben und anfeuern. Die erste Stadt ist die eigene Heimatstadt. Tippfehler wie „Hambrug“ oder „Koeln“ werden erkannt.
- **Jeder andere Kommentar**: +1 m für die Heimatstadt (alle 30 s).
- **❤️ Herz-Emoji im Chat**: +1 m (alle 5 s). **🎁 im Chat**: Mega-Bauschub +25 m (einmal pro Minute).
- **Gründer**: Wer eine Stadt als Erstes schreibt, steht für immer am Leuchtturm.
- **Städte-Fieber**: Schreiben 6 Leute einer Stadt innerhalb von 30 s, zählt 45 s lang alles doppelt.
- **Jede Minute ein Event** (60 verschiedene: Schnellste, Gemeinschafts-Ziele, Emoji-Runden, Quiz, Städte-Spiele, Duelle, Glück), jedes 40 s lang.
- **Ranglisten**: Gesamt, Heute, Diese Woche und Bundesländer. Die Stadt des Tages ist die Stadt, die heute am meisten gebaut hat.
- **Turm**: Er wächst ohne Grenze, die Höhe steht in Metern, dazu Höhenzonen. 32 Ausbaustufen, von Fahne und Rettungsring über Lichterkette und Zeppelin bis Astronaut, Galaxie und eigene Sonne. Die Streifenfarbe wechselt mit der Höhe.
- **Dank**:
  - Für Herzregen dankt Leda und lädt zum Mitbauen ein (höchstens einmal pro Minute). Herz-Meilensteine (100, 500, 1.000 …) werden gefeiert.
  - Geschenke: „Tausend Danke, @name, das geht alles in deinen Turm!“ (5 m je Coin).
  - Teilen: Bonus +30 m für den eigenen Turm (pro Person alle 10 Minuten).

## Starten
1. Ordner auf den Schreibtisch legen.
2. **„Leuchtturm-Rennen starten.command“** doppelklicken. Beim ersten Mal: Rechtsklick → Öffnen.
3. Den https-Link aus dem Terminal in LIVE Studio als Link-Quelle einfügen (1080×1920).
4. Im Ton-Tab (`localhost:8791/?ton`) einmal auf „Ton starten“ klicken. Ton wie bei Muschel-Tal über BlackHole.

Zum Ausprobieren ohne TikTok: **„Leuchtturm-Rennen testen.command“**.

## Stimme, Musik und Regeln
- **Stimme:** Leda (Gemini). Die Schlüssel werden mit Muschel-Tal LIVE geteilt (`~/.muscheltal`). Gespeicherte Sätze und das Tageskontingent werden mitbenutzt, wenn „Muschel-Tal LIVE“ auf dem Schreibtisch liegt.
- **Musik:** eigene, lizenzfreie Lagunen-Musik (`seite/musik/lagune_*.mp3`, erzeugt mit `tools/make_music_lagune.py`).
- **TikTok-Regeln:** Boni für Geschenke und Teilen werden nur nachträglich beim Danke erwähnt, nie vorher angekündigt (keine Aufforderung). Das Wort „Like“ fällt nie.

Alle Zahlen stehen in `einstellungen.json`. Port 8791, damit es nie mit Muschel-Tal LIVE (8790) kollidiert.
