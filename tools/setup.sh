#!/usr/bin/env bash
# Richtet alles ein, was die TikTok-Pipeline braucht (idempotent).
#   bash tools/setup.sh          # Piper-Stimme (schnell, ~60 MB)
#   bash tools/setup.sh --coqui  # zusätzlich Thorsten VITS (Standard) + CSS10 über Coqui TTS (natürlicher, ~5 GB mit PyTorch, ~40 min)
set -euo pipefail
CACHE="${TIKTOK_CACHE:-$HOME/.cache/tiktok-tts}"
mkdir -p "$CACHE"

pip install -q piper-tts soundfile numpy 2>&1 | grep -v -i warning || true

# Piper-Stimmen (de) als Fallback – GitHub-Release, Hugging Face ist oft gesperrt. kerstin = weiblich
for v in kerstin thorsten; do
  if [ ! -f "$CACHE/voice-de-$v-low/de-$v-low.onnx" ]; then
    mkdir -p "$CACHE/voice-de-$v-low"
    curl -sSL https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-$v-low.tar.gz \
      | tar xz -C "$CACHE/voice-de-$v-low"
  fi
done

if [ "${1:-}" = "--coqui" ]; then
  if [ ! -x "$CACHE/coqui/bin/python" ]; then
    python3 -m venv "$CACHE/coqui"
  fi
  "$CACHE/coqui/bin/pip" install -q coqui-tts torch torchaudio torchcodec "gruut[de]" 2>&1 | tail -2 || true
  # Standardstimme: Thorsten VITS (natürlich, Phonem-basiert)
  if [ ! -f "$CACHE/thorsten-vits/model_file.pth" ]; then
    mkdir -p "$CACHE/thorsten-vits"
    curl -sSL -o "$CACHE/thorsten.zip" \
      https://github.com/coqui-ai/TTS/releases/download/v0.7.0_models/tts_models--de--thorsten--vits.zip
    unzip -o -q -j "$CACHE/thorsten.zip" -d "$CACHE/thorsten-vits" && rm "$CACHE/thorsten.zip"
  fi
  # Weibliche Alternative: CSS10 VITS (klingt abgehackter) (22 kHz). Die Config verweist auf Hugging-Face-Pfade -> lokal umbiegen.
  if [ ! -f "$CACHE/css10-vits/config.json" ]; then
    mkdir -p "$CACHE/css10-vits"
    curl -sSL -o "$CACHE/css10.zip" \
      https://github.com/coqui-ai/TTS/releases/download/v0.8.0_models/tts_models--de--css10--vits.zip
    unzip -o -q -j "$CACHE/css10.zip" -d "$CACHE/css10-vits" && rm "$CACHE/css10.zip" "$CACHE"/css10-vits/._*
    python3 - "$CACHE/css10-vits" <<'PY'
import json, sys
d = sys.argv[1]; p = d + "/config.json"; c = json.load(open(p))
def fix(o):
    for k, v in o.items():
        if isinstance(v, dict): fix(v)
        elif k == "speakers_file": o[k] = d + "/speaker_ids.json"
        elif k == "language_ids_file": o[k] = d + "/language_ids.json"
fix(c); json.dump(c, open(p, "w"), indent=1)
PY
  fi
fi

# HyperFrames-CLI einmal vorladen
"$(dirname "$0")/hf.sh" --version >/dev/null 2>&1 || true
echo "Setup fertig. Cache: $CACHE"
