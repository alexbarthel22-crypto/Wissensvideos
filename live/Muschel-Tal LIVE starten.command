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
# Läuft noch ein Probelauf (Test-Fenster)? Den beenden – sonst sähen die Zuschauer simulierte Daten.
if pgrep -f "server.mjs --test" >/dev/null; then
  echo "🧪 Ein Probelauf lief noch – wird beendet."; pkill -f "server.mjs --test"; pkill -f "cloudflared tunnel"; sleep 2
fi
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
# Ton-Tab im Browser öffnen: Kerstin + Musik laufen dort (einmal „Ton starten“ klicken, Tab offen lassen)
( sleep 4; open "http://localhost:8790/?ton" ) &
while true; do
  caffeinate -dimsu node server.mjs      # Mac bleibt wach, solange das Programm läuft
  [ $? -eq 2 ] && { read -r -p "Enter drücken zum Schließen"; exit 0; }   # läuft schon in einem anderen Fenster
  echo "Programm beendet – Neustart in 3 Sekunden (zum Beenden: Fenster schließen)."
  sleep 3
done
