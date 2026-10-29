#!/usr/bin/env bash
# HyperFrames-CLI mit fester Version (Plugin-Release 0.8.217 ist auf npm noch nicht verfügbar).
HF_VERSION="${HF_VERSION:-0.8.216}"
export HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_SKILL_PKG_VERSION="$HF_VERSION" HYPERFRAMES_PLUGIN_VERSION="$HF_VERSION"
exec npx --yes "hyperframes@${HF_VERSION}" "$@"
