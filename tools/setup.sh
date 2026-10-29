#!/usr/bin/env bash
# Richtet alles ein, was die TikTok-Pipeline braucht (idempotent).
#   bash tools/setup.sh          # Piper-Stimme (schnell, ~60 MB)
#   bash tools/setup.sh --coqui  # zusätzlich Thorsten VITS über Coqui TTS (natürlicher, ~5 GB mit PyTorch)
set -euo pipefail
CACHE="${TIKTOK_CACHE:-$HOME/.cache/tiktok-tts}"
mkdir -p "$CACHE"

pip install -q piper-tts soundfile numpy 2>&1 | grep -v -i warning || true

# Piper-Stimme Thorsten (de) – liegt als GitHub-Release, Hugging Face ist oft gesperrt
if [ ! -f "$CACHE/voice-de-thorsten-low/de-thorsten-low.onnx" ]; then
  mkdir -p "$CACHE/voice-de-thorsten-low"
  curl -sSL https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-thorsten-low.tar.gz \
    | tar xz -C "$CACHE/voice-de-thorsten-low"
fi

if [ "${1:-}" = "--coqui" ]; then
  if [ ! -x "$CACHE/coqui/bin/python" ]; then
    python3 -m venv "$CACHE/coqui"
  fi
  "$CACHE/coqui/bin/pip" install -q coqui-tts torch torchaudio 2>&1 | tail -2 || true
  if [ ! -f "$CACHE/thorsten-vits/model_file.pth" ]; then
    mkdir -p "$CACHE/thorsten-vits"
    curl -sSL -o "$CACHE/thorsten-vits.zip" \
      https://github.com/coqui-ai/TTS/releases/download/v0.7.0_models/tts_models--de--thorsten--vits.zip
    unzip -o -q -j "$CACHE/thorsten-vits.zip" -d "$CACHE/thorsten-vits" && rm "$CACHE/thorsten-vits.zip"
  fi
fi

# HyperFrames-CLI einmal vorladen
"$(dirname "$0")/hf.sh" --version >/dev/null 2>&1 || true
echo "Setup fertig. Cache: $CACHE"
