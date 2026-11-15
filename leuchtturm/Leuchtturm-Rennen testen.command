#!/bin/bash
# Probelauf mit simulierten Zuschauern – ohne TikTok, mit Stimme. Speichert nichts.
cd "$(dirname "$0")"
if ! command -v node >/dev/null; then
  echo "Node.js fehlt. Bitte einmal installieren: https://nodejs.org (LTS-Version), dann nochmal doppelklicken."
  read -r; exit 1
fi
if [ ! -d node_modules/onnxruntime-node ] || [ ! -d node_modules/@diffusionstudio/piper-wasm ] || [ ! -d node_modules/tiktok-live-connector ]; then
  echo "📦 Installiere Programmteile (einmalig, kann ein paar Minuten dauern) …"
  ONNXRUNTIME_NODE_INSTALL=skip npm install --silent
fi
# Notfall-Stimme Kerstin: wird von Muschel-Tal LIVE mitbenutzt, sonst einmalig laden (ca. 60 MB)
MT="$HOME/Desktop/Muschel-Tal LIVE"
if [ ! -f werkzeug/stimme-kerstin/de-kerstin-low.onnx ] && [ ! -f "$MT/werkzeug/stimme-kerstin/de-kerstin-low.onnx" ]; then
  echo "⬇️  Lade einmalig die Notfall-Stimme (ca. 60 MB) …"
  mkdir -p werkzeug/stimme-kerstin
  curl -fsSL https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-kerstin-low.tar.gz | tar xz -C werkzeug/stimme-kerstin \
    || { H=https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/kerstin/low/de_DE-kerstin-low; curl -fsSL -o werkzeug/stimme-kerstin/de-kerstin-low.onnx.json "$H.onnx.json" && curl -fsSL -o werkzeug/stimme-kerstin/de-kerstin-low.onnx "$H.onnx"; } \
    || echo "⚠️  Notfall-Stimme konnte nicht geladen werden."
fi
if pgrep -f "node server.mjs" >/dev/null; then
  echo "⚠️  Ein LIVE-Programm läuft gerade. Probelauf wird NICHT gestartet."; read -r -p "Enter zum Schließen"; exit 0
fi
read -r -p "🧪 Probelauf mit Test-Zuschauern starten? (j = ja, Enter = abbrechen) " ok
[ "$ok" = "j" ] || [ "$ok" = "J" ] || exit 0
# Schlüssel: dieselben wie bei Muschel-Tal LIVE (einmal gespeichert in ~/.muscheltal, werden nicht erneut abgefragt)
mkdir -p "$HOME/.muscheltal"
schluessel() {   # $1 Datei, $2 Frage, $3 Erklärung
  if [ ! -f "$1" ] && [ -f "$HOME/.muscheltal/$1" ]; then cp "$HOME/.muscheltal/$1" "$1"; fi
  if [ ! -f "$1" ]; then
    echo "$3"; read -r -p "$2 " EINGABE
    printf '%s' "$EINGABE" > "$1"; cp "$1" "$HOME/.muscheltal/$1"
    [ -n "$EINGABE" ] && echo "✅ Gespeichert – wird nie wieder abgefragt." || echo "ℹ️  Ohne Schlüssel gemerkt."
  elif [ ! -f "$HOME/.muscheltal/$1" ]; then cp "$1" "$HOME/.muscheltal/$1"; fi
}
schluessel gemini-schluessel.txt "Gemini-Schlüssel:" "🎙️  Für Ledas Stimme: „Gemini API Key“ aus Google einfügen und Enter."
schluessel google-tts-schluessel.txt "Google-TTS-Schlüssel:" "🆘 Für die Notfall-Stimme Chirp-Leda: „TikTok Stimme API“-Schlüssel einfügen und Enter (leer = ohne)."
source ./tunnel.sh
starte_tunnel
trap stoppe_tunnel EXIT
echo "Im Browser ansehen: http://localhost:8791   (Ton: http://localhost:8791/?ton)"
( sleep 4; open "http://localhost:8791/?ton" ) &
caffeinate -dimsu node server.mjs --test --neu
