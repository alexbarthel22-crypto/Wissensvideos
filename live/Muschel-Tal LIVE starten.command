#!/bin/bash
# Doppelklick startet Muschel-Tal LIVE (Fenster offen lassen, solange du streamst).
# Läuft vollautomatisch: erzeugt den https-Link für LIVE Studio, wartet auf den LIVE, verbindet sich,
# startet sich bei Fehlern selbst neu.
cd "$(dirname "$0")"
if ! command -v node >/dev/null; then
  echo "Node.js fehlt. Bitte einmal installieren: https://nodejs.org (LTS-Version), dann nochmal doppelklicken."
  read -r; exit 1
fi
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
# Läuft noch ein Probelauf (Test-Fenster)? Den beenden – sonst sähen die Zuschauer simulierte Daten.
if pgrep -f "server.mjs --test" >/dev/null; then
  echo "🧪 Ein Probelauf lief noch – wird beendet."; pkill -f "server.mjs --test"; pkill -f "cloudflared tunnel"; sleep 2
fi
source ./tunnel.sh
starte_tunnel
trap stoppe_tunnel EXIT
# Ton-Tab im Browser öffnen: Anna + Musik laufen dort (einmal „Ton starten“ klicken, Tab offen lassen)
( sleep 4; open "http://localhost:8790/?ton" ) &
while true; do
  caffeinate -dimsu node server.mjs      # Mac bleibt wach, solange das Programm läuft
  [ $? -eq 2 ] && { read -r -p "Enter drücken zum Schließen"; exit 0; }   # läuft schon in einem anderen Fenster
  echo "Programm beendet – Neustart in 3 Sekunden (zum Beenden: Fenster schließen)."
  sleep 3
done
