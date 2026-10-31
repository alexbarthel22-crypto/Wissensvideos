# Stories

Episoden-Generator für stilisierte, vertonte Kurzfilme im Hochformat (1080×1920, 30 fps).
Die Bilder werden im Browser als Canvas-Animation gerendert (Silhouetten, Licht, Partikel, Magie),
die Stimmen kommen von Google Cloud Text-to-Speech, Musik und Soundeffekte werden per Code synthetisiert.

## Serie: STERNENFALL
- `story/folge01.json`: Folge 1 „Das Herz, das vom Himmel fiel“ (Drehbuch, Stimmen, Timing-Cues)

## Bauen
Voraussetzungen: `GOOGLE_TTS_API_KEY`, Python 3 mit `numpy` und `scipy`, Node mit `playwright`, `ffmpeg`.

```sh
python3 engine/tts.py story/folge01.json out/folge01   # Stimmen + Zeitachse
python3 engine/audio.py out/folge01                    # Musik, Effekte, Mix
node engine/render.js out/folge01                      # Video -> out/folge01/folge.mp4
node engine/render.js out/folge01 --stills 10,40.5     # einzelne Standbilder prüfen
```

Die Stimmen werden in `out/<folge>/voice/` zwischengespeichert; nur geänderte Zeilen werden neu synthetisiert.
