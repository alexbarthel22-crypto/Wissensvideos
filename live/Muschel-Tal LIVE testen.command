#!/bin/bash
# Probelauf mit simulierten Zuschauern – ohne TikTok, mit Stimme. Speichert nichts.
# Erzeugt auch den https-Link, damit du die Insel in der Vorschau von LIVE Studio prüfen kannst.
cd "$(dirname "$0")"
command -v node >/dev/null || { echo "Node.js fehlt: https://nodejs.org"; read -r; exit 1; }
[ -d node_modules ] || npm install --silent
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
