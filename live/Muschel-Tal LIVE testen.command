#!/bin/bash
# Probelauf mit simulierten Zuschauern – ohne TikTok, mit Stimme. Speichert nichts.
# Erzeugt auch den https-Link, damit du die Insel in der Vorschau von LIVE Studio prüfen kannst.
cd "$(dirname "$0")"
command -v node >/dev/null || { echo "Node.js fehlt: https://nodejs.org"; read -r; exit 1; }
# Pakete installieren bzw. ergänzen (z. B. nach einem Update)
if [ ! -d node_modules/onnxruntime-node ] || [ ! -d node_modules/@diffusionstudio/piper-wasm ] || [ ! -d node_modules/tiktok-live-connector ]; then
  echo "📦 Installiere Programmteile (einmalig, kann ein paar Minuten dauern) …"
  ONNXRUNTIME_NODE_INSTALL=skip npm install --silent
fi
# Musik: liegt in werkzeug/musik (Updates überschreiben das nie). Neue Stücke aus „Downloads“ automatisch übernehmen.
mkdir -p werkzeug/musik
for f in "$HOME"/Downloads/strand_*.mp3 "$HOME"/Downloads/cozy_*.mp3 "$HOME"/Downloads/insel_*.mp3; do [ -f "$f" ] && [ ! -f "werkzeug/musik/$(basename "$f")" ] && cp "$f" werkzeug/musik/ && echo "🎵 Musik übernommen: $(basename "$f")"; done
# Kerstins Offline-Stimme (Piper, „Kerstin“, ca. 60 MB) einmalig laden
if [ ! -f werkzeug/stimme-kerstin/de-kerstin-low.onnx ]; then
  echo "⬇️  Lade einmalig Kerstins Offline-Stimme (ca. 60 MB) …"
  mkdir -p werkzeug/stimme-kerstin
  curl -fsSL https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-kerstin-low.tar.gz | tar xz -C werkzeug/stimme-kerstin \
    || { H=https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/kerstin/low/de_DE-kerstin-low; curl -fsSL -o werkzeug/stimme-kerstin/de-kerstin-low.onnx.json "$H.onnx.json" && curl -fsSL -o werkzeug/stimme-kerstin/de-kerstin-low.onnx "$H.onnx"; } \
    || echo "⚠️  Stimme konnte nicht geladen werden – dann spricht ersatzweise die Mac-Stimme."
fi
# Nicht aus Versehen starten (z. B. wenn das Terminal alte Fenster wiederherstellt) und nie neben dem echten LIVE
if pgrep -f "node server.mjs" >/dev/null; then
  echo "⚠️  Muschel-Tal LIVE läuft gerade (echter Stream). Probelauf wird NICHT gestartet."; read -r -p "Enter zum Schließen"; exit 0
fi
read -r -p "🧪 Probelauf mit Test-Zuschauern starten? (j = ja, Enter = abbrechen) " ok
[ "$ok" = "j" ] || [ "$ok" = "J" ] || exit 0
# Schlüssel: werden einmal abgefragt und dauerhaft in ~/.muscheltal gespeichert (gelten für alle Ordner und Updates).
# Leer lassen = ohne (wird auch gemerkt). Neu eingeben: Datei in ~/.muscheltal und hier im Ordner löschen.
mkdir -p "$HOME/.muscheltal"
schluessel() {   # $1 Datei, $2 Frage, $3 Erklärung
  if [ ! -f "$1" ] && [ -f "$HOME/.muscheltal/$1" ]; then cp "$HOME/.muscheltal/$1" "$1"; fi
  if [ ! -f "$1" ]; then
    echo "$3"; read -r -p "$2 " EINGABE
    printf '%s' "$EINGABE" > "$1"; cp "$1" "$HOME/.muscheltal/$1"
    [ -n "$EINGABE" ] && echo "✅ Gespeichert – wird nie wieder abgefragt." || echo "ℹ️  Ohne Schlüssel gemerkt."
  elif [ ! -f "$HOME/.muscheltal/$1" ]; then cp "$1" "$HOME/.muscheltal/$1"; fi
}
schluessel live-schluessel.txt "Schlüssel:" "📺 Für die Rangliste auf muscheltal.de: Netlify-Schlüssel (LIVE_SCHLUESSEL) einfügen und Enter (leer = ohne)."
schluessel gemini-schluessel.txt "Gemini-Schlüssel:" "🎙️  Für Ledas Stimme: „Gemini API Key“ aus Google einfügen und Enter (leer = Kerstin moderiert)."
schluessel google-tts-schluessel.txt "Google-TTS-Schlüssel:" "🆘 Für die Notfall-Stimme Chirp-Leda: „TikTok Stimme API“-Schlüssel einfügen und Enter (leer = ohne)."
source ./tunnel.sh
starte_tunnel
trap stoppe_tunnel EXIT
echo "Nur im Browser ansehen (ohne LIVE Studio): http://localhost:8790"
echo ""
caffeinate -dimsu node server.mjs --test --neu
