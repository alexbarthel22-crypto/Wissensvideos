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
# Notfall-Stimme Chirp-Leda (Google Cloud Text-to-Speech): Schlüssel einmalig eingeben (nur auf diesem Mac gespeichert)
if [ ! -f google-tts-schluessel.txt ]; then
  echo "🆘 Für die Notfall-Stimme (Chirp-Leda, wenn Geminis Tageslimit aufgebraucht ist): Google-Cloud-Schlüssel einfügen und Enter (leer = ohne)."
  read -r -p "Google-TTS-Schlüssel: " TTS_EINGABE
  [ -n "$TTS_EINGABE" ] && printf '%s' "$TTS_EINGABE" > google-tts-schluessel.txt && echo "✅ Gespeichert."
fi
# Moderationsstimme Leda (Google Gemini): Schlüssel einmalig eingeben (wird nur auf diesem Mac gespeichert)
if [ ! -f gemini-schluessel.txt ]; then
  echo "🎙️  Für Ledas Stimme (Gemini): API-Schlüssel aus Google AI Studio einfügen und Enter drücken (leer lassen = Kerstin moderiert)."
  read -r -p "Gemini-Schlüssel: " GEMINI_EINGABE
  [ -n "$GEMINI_EINGABE" ] && printf '%s' "$GEMINI_EINGABE" > gemini-schluessel.txt && echo "✅ Gespeichert."
fi
source ./tunnel.sh
starte_tunnel
trap stoppe_tunnel EXIT
echo "Nur im Browser ansehen (ohne LIVE Studio): http://localhost:8790"
echo ""
caffeinate -dimsu node server.mjs --test --neu
