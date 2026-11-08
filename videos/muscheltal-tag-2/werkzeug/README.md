# Muschel-Tal Tag 2 – Ablauf

1. Stimme: `python3 tools/tts_de.py videos/muscheltal-tag-2 --backend gemini --model gemini-3.1-flash-tts-preview --voice Achird --speed 1.12`
2. Homepage-Stand holen: `git pull`, dann `python3 muscheltal/bau.py --out <tmp>/site` (lokal, nichts veröffentlichen). Die Homepage hat seit 8.11. die echten 575 Einwohner (500 Haupt-Insel + 75 Kokos-Küste).
3. Aufnahme: `node werkzeug/aufnahme.cjs <tmp>/site/index.html assets/voice/timings.json <tmp>/frames <dauer>` → `ffmpeg -framerate 30 -i <tmp>/frames/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 assets/bg.mp4`
4. Szenen: `python3 werkzeug/szenen.py scenes werkzeug/logo_svg.txt`, dann `python3 ../../tools/build_video.py .`, Musik + Atmo, check, render.
