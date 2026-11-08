# Muschel-Tal Tag 2 – Ablauf

1. Stimme: `python3 tools/tts_de.py videos/muscheltal-tag-2 --backend gemini --model gemini-3.1-flash-tts-preview --voice Achird --speed 1.12`
2. Homepage für die Aufnahme bauen (nur lokal, nicht veröffentlichen): `muscheltal/` nach `<tmp>/mt2` kopieren, in `daten/insel.json` Insel 2 = „Kokos-Küste“, `daten/einwohner.csv` = alle 557 Follower (älteste zuerst), `python3 bau.py --out <tmp>/mt2/site`; in `site/index.html` die Einwohnerzahl der Insel 2 auf 75 setzen (`fmt(v.i===1?75:v.people.length)`).
3. Aufnahme: `node werkzeug/aufnahme.js <tmp>/mt2/site/index.html assets/voice/timings.json <tmp>/frames <dauer>` → `ffmpeg -framerate 30 -i <tmp>/frames/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 assets/bg.mp4`
4. Szenen: `python3 werkzeug/szenen.py scenes werkzeug/logo_svg.txt`, dann `python3 ../../tools/build_video.py .`, Musik + Atmo, check, render.
