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
# Annas Offline-Stimme (Piper, „Kerstin“, ca. 60 MB) einmalig laden
if [ ! -f werkzeug/stimme-kerstin/de-kerstin-low.onnx ]; then
  echo "⬇️  Lade einmalig Annas Offline-Stimme (ca. 60 MB) …"
  mkdir -p werkzeug/stimme-kerstin
  curl -fsSL https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-kerstin-low.tar.gz | tar xz -C werkzeug/stimme-kerstin \
    || echo "⚠️  Stimme konnte nicht geladen werden – Anna spricht dann mit der Mac-Stimme."
fi
# Nicht aus Versehen starten (z. B. wenn das Terminal alte Fenster wiederherstellt) und nie neben dem echten LIVE
if pgrep -f "node server.mjs" >/dev/null; then
  echo "⚠️  Muschel-Tal LIVE läuft gerade (echter Stream). Probelauf wird NICHT gestartet."; read -r -p "Enter zum Schließen"; exit 0
fi
read -r -p "🧪 Probelauf mit Test-Zuschauern starten? (j = ja, Enter = abbrechen) " ok
[ "$ok" = "j" ] || [ "$ok" = "J" ] || exit 0
source ./tunnel.sh
starte_tunnel
trap stoppe_tunnel EXIT
echo "Nur im Browser ansehen (ohne LIVE Studio): http://localhost:8790"
echo ""
caffeinate -dimsu node server.mjs --test --neu
