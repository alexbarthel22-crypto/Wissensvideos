#!/bin/bash
# Doppelklick: spielt dieses Update in ALLE Muschel-Tal-LIVE-Ordner auf diesem Mac ein (egal welchen du startest).
# Spielstand, Schlüssel, Musik und Stimmen bleiben jeweils erhalten.
cd "$(dirname "$0")" || exit 1
NEU="$(pwd)"
NV=$(grep -o "const VERSION = '[^']*'" "$NEU/server.mjs" | cut -d"'" -f2)
echo "🔎 Suche alle Muschel-Tal-LIVE-Ordner auf diesem Mac …"
ORDNER=(); HAUPT=""; BEST=0
while IFS= read -r f; do
  d="$(dirname "$f")"
  [ "$d" = "$NEU" ] && continue
  case "$d" in "$NEU"/*) continue;; esac
  ORDNER+=("$d")
  t=1; [ -f "$d/stand.json" ] && t=$(stat -f %m "$d/stand.json" 2>/dev/null || echo 1)
  if [ "$t" -gt "$BEST" ]; then BEST=$t; HAUPT="$d"; fi
done < <(find "$HOME" -maxdepth 6 -name "Muschel-Tal LIVE starten.command" -not -path "*/Library/*" -not -path "*/.Trash/*" 2>/dev/null)
if [ ${#ORDNER[@]} -eq 0 ]; then
  echo "❌ Kein bisheriger Ordner gefunden. Dann diesen Ordner direkt benutzen: hier „Muschel-Tal LIVE starten.command“ doppelklicken."
  read -r -p "Enter zum Schließen …"; exit 1
fi
pkill -f "node server.mjs" 2>/dev/null && echo "⏹  Laufendes Programm beendet." && sleep 1
FEHLER=0
for d in "${ORDNER[@]}"; do
  ALT=$(grep -o "const VERSION = '[^']*'" "$d/server.mjs" 2>/dev/null | cut -d"'" -f2)
  if (cd "$NEU" && tar -cf - --exclude './stand.json' --exclude '*schluessel.txt' --exclude './werkzeug' --exclude './node_modules' --exclude './Update einspielen.command' .) | (cd "$d" && tar -xf -); then
    V=$(grep -o "const VERSION = '[^']*'" "$d/server.mjs" | cut -d"'" -f2)
    [ "$V" = "$NV" ] && echo "✅ $d  (${ALT:-?} → $V)" || { echo "❌ $d  (Version $V statt $NV)"; FEHLER=1; }
  else echo "❌ $d  – Kopieren hat nicht geklappt"; FEHLER=1; fi
done
[ ${#ORDNER[@]} -gt 1 ] && echo "" && echo "ℹ️  Du hast ${#ORDNER[@]} Muschel-Tal-Ordner. Alle sind jetzt aktuell. Tipp: alte Kopien in den Papierkorb legen, dein Spielstand liegt in: $HAUPT"
echo ""; [ $FEHLER = 0 ] && echo "✅ Update eingespielt – Version $NV. Spielstand, Schlüssel, Musik und Stimmen sind erhalten."
read -r -p "Jetzt Muschel-Tal LIVE starten (Ordner mit deinem Spielstand)? (Enter = ja, n = nein) " A
[ "$A" != "n" ] && open "$HAUPT/Muschel-Tal LIVE starten.command"
