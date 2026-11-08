# Muschel-Tal Story 4 – Ich betrete die Kokos-Küste (14 s)

Ich-Perspektive ohne Hände: vom Wasser auf die Kokos-Küste, an den ersten Kokosnuss-Hütten mit Follower-Namen vorbei, dann Blick über die ganze Insel: „Hier ist jetzt Platz für die nächsten 1.500 Follower“.

1. Stimme: `python3 tools/tts_de.py videos/muscheltal-story-4 --backend gemini --model gemini-3.1-flash-tts-preview --voice Achird --speed 1.12`
2. Homepage lokal bauen: `python3 muscheltal/bau.py --out <tmp>/site` (nichts veröffentlichen)
3. Aufnahme: `node werkzeug/aufnahme.cjs <tmp>/site/index.html assets/voice/timings.json <tmp>/frames 14.4` → `ffmpeg -framerate 30 -i <tmp>/frames/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 assets/bg.mp4`
4. `python3 ../../tools/build_video.py .`, check, `HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell ../../tools/hf.sh render --output renders/muscheltal-story-4.mp4`
