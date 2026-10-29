---
name: tiktok-video
description: Erstellt deutschsprachige TikTok-Videos (9:16, ca. 60 s) im Stil der Referenzen des Creators – "Was wäre, wenn …?"-Szenarien als 2D-Neon-Erklärvideo mit Zeit-Kapiteln, Zähler-Boxen, Checkliste und Wort-für-Wort-Karaoke-Untertiteln. Komplett im Code mit HyperFrames gebaut, mit deutscher KI-Stimme. Nutzen, wenn der Nutzer ein neues TikTok-Video, ein neues Thema oder Änderungen an einem bestehenden Video in videos/ möchte.
---

# TikTok-Videos „Was wäre, wenn …?“

Alle Videos sind **immer auf Deutsch** (Sprecher, Untertitel, Bildschirmtexte) und werden **komplett im Code mit HyperFrames** gebaut. Ziel: so nah wie möglich an den Referenzvideos des Creators. Stilregeln: `references/stil.md` (vor jedem neuen Video lesen). Fertiges Beispiel: `videos/gta6-19-november/`.

Vorher den HyperFrames-Skill laden (`/hyperframes:hyperframes`); dessen Contract gilt. Die HyperFrames-CLI immer über `tools/hf.sh` aufrufen (fixiert eine auf npm verfügbare Version).

## Ablauf für ein neues Video

1. **Setup** (einmal pro Sitzung): `bash tools/setup.sh --coqui` im Hintergrund starten (PyTorch ~5 GB, ~40 min bei 1 MB/s). Bis dahin mit Piper (`voice-de-kerstin-low`) bauen und prüfen, am Ende mit Coqui neu vertonen.
2. **Projekt anlegen**: `cd videos && ../tools/hf.sh init <slug> --example blank --resolution portrait --non-interactive --skip-skills --skill hyperframes`
3. **Skript** `videos/<slug>/script.json` schreiben (Format unten). ~150–170 Wörter ergeben ~60 s. Aufbau siehe `references/stil.md` → Dramaturgie.
4. **Stimme**: `python3 tools/tts_de.py videos/<slug> --backend coqui --voice thorsten-vits --speed 1.1`. Thorsten VITS (Phonem-basiert, 22 kHz) klingt am natürlichsten; CSS10 (weiblich, buchstabenbasiert) klingt abgehackt und spricht Wörter wie „Mitternacht“ falsch – nicht verwenden. Jede Zeile wird in einem Durchgang erzeugt (`split_sentences=False`), sanfter EQ + De-Esser, Lautheit auf -16 LUFS. Ziel: ~2,7 Wörter/s, Gesamtlänge 60–70 s. Pro Zeile `"speed": 0.92` für dramatische Sätze, `"pause": 0.4` vor einer Pointe. Fallback ohne PyTorch: `--backend piper --voice voice-de-thorsten-low`.
5. **Szenen** `videos/<slug>/scenes/sNN.html` schreiben, eine pro Szene im Skript (Vorlage: jede Szene aus dem Beispielprojekt; `scenes/_common.css` mitkopieren). Animationen hängen an Wörtern: `at("L3", "Start")`, `line("L3")`, `count(...)`.
6. **Bauen**: `python3 tools/build_video.py videos/<slug>` → `index.html`, `compositions/*` (HUD, Untertitel, Szenen, Ton).
7. **Prüfen**: `cd videos/<slug> && ../../tools/hf.sh check --json > /tmp/c.json; python3 ../../tools/check_summary.py /tmp/c.json` – alle Fehler beheben, Warnungen abwägen. Dann `../../tools/hf.sh snapshot --review -o <scratchpad>` und gezielt `--at` auf die Schlüsselmomente; Bilder ansehen und nach `references/stil.md` → QA korrigieren.
8. **Rendern**: `../../tools/hf.sh render --output renders/<slug>.mp4` (1080×1920, 30 fps). Danach `../../tools/hf.sh audio renders/<slug>.mp4 --json` (Lautheit, Ton vorhanden).
9. Ergebnis committen und pushen, MP4 dem Nutzer schicken.

Nach Skriptänderungen immer Schritt 4 → 6 neu ausführen (Timings ändern sich).

## script.json

```json
{
  "title": "…",
  "scenes": [
    { "id": "s01", "tag": "WAS WÄRE WENN", "lines": [
        { "id": "L1", "text": "Was passiert, / wenn am *y:19.|neunzehnten *y:November …" } ],
      "sfx": [ { "name": "pop", "at": "L1:19.", "volume": 0.45 } ] },
    { "id": "s02", "tag": "19. NOV · 00:00", "check": "SERVER", "lines": [ … ] },
    { "id": "s11", "tag": "…", "hold": 2.6, "lines": [ … ] }
  ]
}
```

- `tag`: Kapitel-Marke oben (Datum/Uhrzeit, „REGEL 2 · …“). `check`: fügt der Checkliste oben links einen Punkt hinzu. `hold`: Standzeit nach der letzten Zeile (nur letzte Szene).
- Token: `Anzeige|Aussprache` (Zahlen und Anglizismen ausschreiben bzw. eindeutschen: `GTA_6|Ge-Te-A-sechs`, `Vice_City|Weiss-Sitti`, `800|achthundert`). `_` = Leerzeichen innerhalb eines Tokens.
- Farbe für Schlüsselwörter: `*y:` gelb, `*r:` rot (Gefahr/Verlust), `*p:` pink (Hauptthema), `*g:` grün (positiv/Start), `*b:` blau (Technik/Ruhe). 1–3 Wörter pro Zeile, nicht mehr.
- `/` trennt Untertitel-Gruppen: 2–4 Wörter, höchstens zwei Zeilen.
- `sfx.at`: `L4:Server` (Wortbeginn), `L13:100-0.2` (mit Versatz) oder `s03+0.4`. Verfügbare Effekte: `pop, click, click-soft, whoosh, whoosh-short, glitch-1, impact-bass-1/2, error, notification, ping`, eigene Dateien in `assets/sfx/` per Dateiname. **Keine** langen Rausch-Effekte (`whoosh-cinematic`, `glitch-2/3`, `riser`) – sie rauschen hörbar unter der Stimme. Glitches höchstens 0.25 Lautstärke. Whoosh auf Szenenwechseln setzt der Build automatisch.

## Szenen-Vorlage (Regeln)

- Datei beginnt mit `<template>`, Styles enthalten `/*__COMMON_CSS__*/`, Script ist eine IIFE mit `/*__CUE_HELPERS__*/` am Anfang und registriert `window.__timelines["sNN"]`.
- Eine Bühne `<div id="sNN-stage" class="clip stage" data-start="0" data-duration="__DUR__">`; animiert werden nur Kinder. Alle IDs mit `sNN-` präfixen.
- Bildzone: y = 420–1130 px. Zähler-Box (`.cbox`) bei y = 268, x = 290–790 (oder 300–900). Oben links bleibt frei für die Checkliste (x < 280, y 258–450). Untertitel ab y = 1150 – dort keine wichtigen Grafiken.
- Jede Szene endet mit Blur-Out (0,18 s) ihrer Elemente auf `C.__dur - 0.18`.
- Zufall nur über `rng(seed)`, keine `Math.random()`/`Date.now()`; Zahlen über `count()` (deutsches Format 4.100.000.000).

## Hook und Schluss (Pflicht)

- **Frame 0** muss allein als Thumbnail funktionieren und zum Stoppen bringen: Eilmeldungs-Karte mit roter Leiste („● EILMELDUNG · LIVE“) und einer Schlagzeile mit Zahl + Thema (Inter Black 84 px), darüber Kapitel-Marke und Zähler-Box mit der Endzahl, dahinter das leuchtende Hauptmotiv. Alles ab t = 0 sichtbar, Schlagzeile ≥ 2,5 s stehen lassen.
- **Offene Schleife** im Hook: ein Satz, der eine Auflösung am Ende verspricht („Und um Mitternacht passiert etwas, womit niemand rechnet.“) – die Auflösung kommt in der vorletzten Szene.
- **Aufmerksamkeits-Sound** auf Frame 0: Purge-Sirene (`python3 tools/make_siren.py videos/<slug>/assets/sfx/purge-siren.wav`), im Skript `"lead_in": 0.9` und als sfx `{"name": "purge-siren", "at": "s01+0.0", "volume": 0.85}`. Die Sirene steht 0,85 s allein und wird dann unter die Stimme abgesenkt.
- **Schluss**: direkte Frage an die Zuschauer, ob sie selbst dazugehören („Gehörst du am 19. November zu den vier Milliarden?“) + zwei Antwort-Buttons + „Schreib's in die Kommentare!“. Die letzte Untertitel-Zeile bleibt bis zum Ende stehen.

## Bekannte Grenzen

- Keine Musik verfügbar (HeyGen-Katalog braucht Login). Video kommt mit Stimme + Effekten; der Creator legt in TikTok einen Trend-Sound darunter (Lautstärke dort ~10–20 %).
- Hugging Face ist im Container gesperrt; Stimmen kommen von GitHub-Releases (setup.sh).
- Wortzeiten sind geschätzt (Pausen-Erkennung + Silben) – Karaoke kann um ~0,1 s abweichen. Whisper/Vosk-Modelle sind im Container nicht ladbar.
- CSS10 kennt kein „…“ (wird verworfen) und spricht Anglizismen deutsch aus – Aussprache im Skript lautschriftlich schreiben.
- Das „TikTok @handle“-Wasserzeichen und die TikTok-Endkarte in den Referenzen stammen vom TikTok-Download, **nicht** ins Video einbauen.
