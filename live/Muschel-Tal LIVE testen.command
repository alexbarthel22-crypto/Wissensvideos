#!/bin/bash
# Probelauf mit simulierten Zuschauern – ohne TikTok, mit Stimme. Speichert nichts.
cd "$(dirname "$0")"
command -v node >/dev/null || { echo "Node.js fehlt: https://nodejs.org"; read -r; exit 1; }
[ -d node_modules ] || npm install --silent
open "http://localhost:8790"
node server.mjs --test --neu
