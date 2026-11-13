#!/bin/bash
# https-Link für TikTok LIVE Studio („Link“-Quelle) über einen Cloudflare Quick Tunnel.
# LIVE Studio nimmt nur echte https-Adressen an – dieser Tunnel macht die Insel auf deinem Mac unter
# https://….trycloudflare.com erreichbar, solange das Programm läuft. Der Link ist bei jedem Start neu.
# Wird von den .command-Dateien eingebunden (source), nicht direkt starten.

starte_tunnel() {
  local CF="" A URL i
  mkdir -p werkzeug
  if command -v cloudflared >/dev/null 2>&1; then CF=cloudflared
  elif [ -x werkzeug/cloudflared ]; then CF=werkzeug/cloudflared
  else
    echo "⬇️  Lade einmalig das Tunnel-Programm „cloudflared“ von Cloudflare …"
    [ "$(uname -m)" = "arm64" ] && A=arm64 || A=amd64
    if curl -fsSL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-$A.tgz" -o werkzeug/cf.tgz \
       && tar -xzf werkzeug/cf.tgz -C werkzeug && chmod +x werkzeug/cloudflared; then
      CF=werkzeug/cloudflared; rm -f werkzeug/cf.tgz
    fi
  fi
  if [ -z "$CF" ]; then
    echo "⚠️  Tunnel-Programm konnte nicht geladen werden (Internet?). Notlösung: in LIVE Studio die Fensteraufnahme nehmen."
    return 1
  fi
  rm -f werkzeug/tunnel.log
  "$CF" tunnel --no-autoupdate --url http://localhost:8790 > werkzeug/tunnel.log 2>&1 &
  TUNNEL_PID=$!
  for i in $(seq 1 45); do
    URL=$(grep -o 'https://[-a-z0-9]*\.trycloudflare\.com' werkzeug/tunnel.log 2>/dev/null | head -1)
    [ -n "$URL" ] && break
    sleep 1
  done
  if [ -z "$URL" ]; then
    echo "⚠️  Kein Link bekommen. Details: werkzeug/tunnel.log – Notlösung: Fensteraufnahme."
    return 1
  fi
  printf '%s' "$URL" | pbcopy
  echo "$URL" > werkzeug/link.txt
  echo ""
  echo "════════════════════════════════════════════════════════════════"
  echo "  🔗 Link für TikTok LIVE Studio (schon in der Zwischenablage):"
  echo ""
  echo "     $URL"
  echo ""
  echo "  LIVE Studio → Quelle „Link“ → einfügen (⌘V) → 1080 × 1920"
  echo "  Der Link ist bei jedem Start neu – vorhandene Quelle bearbeiten."
  echo "════════════════════════════════════════════════════════════════"
  echo ""
}

stoppe_tunnel() { [ -n "$TUNNEL_PID" ] && kill "$TUNNEL_PID" 2>/dev/null; }
