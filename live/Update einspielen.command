#!/bin/bash
# Doppelklick: spielt dieses Update automatisch in deinen bisherigen Muschel-Tal-LIVE-Ordner ein.
# Spielstand, Schlüssel, Musik und Stimmen bleiben dort erhalten.
cd "$(dirname "$0")" || exit 1
NEU="$(pwd)"
echo "🔎 Suche deinen bisherigen Muschel-Tal-LIVE-Ordner …"
ZIEL=""; BEST=0
while IFS= read -r f; do
  d="$(dirname "$f")"
  [ "$d" = "$NEU" ] && continue
  if [ -f "$d/stand.json" ]; then t=$(stat -f %m "$d/stand.json" 2>/dev/null || echo 1)
  elif [ -f "$d/live-schluessel.txt" ] || [ -f "$d/gemini-schluessel.txt" ]; then t=1
  else continue; fi
  if [ "$t" -gt "$BEST" ]; then BEST=$t; ZIEL="$d"; fi
done < <(find "$HOME" -maxdepth 6 -name "Muschel-Tal LIVE starten.command" -not -path "*/Library/*" -not -path "*/.Trash/*" 2>/dev/null)
if [ -z "$ZIEL" ]; then
  echo "❌ Keinen bisherigen Ordner mit Spielstand gefunden."
  echo "   Dann diesen Ordner einfach direkt benutzen: hier „Muschel-Tal LIVE starten.command“ doppelklicken."
  read -r -p "Enter zum Schließen …"; exit 1
fi
echo "📁 Gefunden: $ZIEL"
pkill -f "node server.mjs" 2>/dev/null && echo "⏹  Laufendes Programm beendet." && sleep 1
if ! (cd "$NEU" && tar -cf - --exclude './stand.json' --exclude '*schluessel.txt' --exclude './werkzeug' --exclude './node_modules' --exclude './Update einspielen.command' .) | (cd "$ZIEL" && tar -xf -); then
  echo "❌ Kopieren hat nicht geklappt."; read -r -p "Enter zum Schließen …"; exit 1
fi
# Hängt noch ein alter Unterordner mit gleichem Namen drin (falsch hineingezogen)? Nur melden, nichts löschen.
[ -d "$ZIEL/Muschel-Tal LIVE" ] && echo "ℹ️  Im Ordner liegt noch ein Unterordner „Muschel-Tal LIVE“ – den kannst du in den Papierkorb legen."
V=$(grep -o "const VERSION = '[^']*'" "$ZIEL/server.mjs" | cut -d"'" -f2)
NV=$(grep -o "const VERSION = '[^']*'" "$NEU/server.mjs" | cut -d"'" -f2)
if [ "$V" != "$NV" ]; then echo "❌ Etwas ist schiefgegangen (Version $V statt $NV)."; read -r -p "Enter zum Schließen …"; exit 1; fi
echo ""; echo "✅ Update eingespielt – Version $V"
echo "   Spielstand, Schlüssel, Musik und Stimmen sind erhalten."
read -r -p "Jetzt Muschel-Tal LIVE starten? (Enter = ja, n = nein) " A
[ "$A" != "n" ] && open "$ZIEL/Muschel-Tal LIVE starten.command"
