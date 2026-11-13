#!/bin/bash
# Probelauf mit simulierten Zuschauern – ohne TikTok, mit Stimme. Speichert nichts.
# Erzeugt auch den https-Link, damit du die Insel in der Vorschau von LIVE Studio prüfen kannst.
cd "$(dirname "$0")"
command -v node >/dev/null || { echo "Node.js fehlt: https://nodejs.org"; read -r; exit 1; }
[ -d node_modules ] || npm install --silent
source ./tunnel.sh
starte_tunnel
trap stoppe_tunnel EXIT
echo "Nur im Browser ansehen (ohne LIVE Studio): http://localhost:8790"
echo ""
caffeinate -dimsu node server.mjs --test --neu
