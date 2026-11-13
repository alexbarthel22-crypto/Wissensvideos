#!/bin/bash
# Doppelklick startet Muschel-Tal LIVE (Fenster offen lassen, solange du streamst).
# Läuft vollautomatisch: wartet auf den LIVE, verbindet sich, startet sich bei Fehlern selbst neu.
cd "$(dirname "$0")"
if ! command -v node >/dev/null; then
  echo "Node.js fehlt. Bitte einmal installieren: https://nodejs.org (LTS-Version), dann nochmal doppelklicken."
  read -r; exit 1
fi
[ -d node_modules ] || npm install --silent
open "http://localhost:8790"
while true; do
  node server.mjs
  echo "Programm beendet – Neustart in 3 Sekunden (zum Beenden: Fenster schließen)."
  sleep 3
done
