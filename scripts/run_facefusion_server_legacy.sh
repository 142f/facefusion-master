#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"

export FACEFUSION_OFFLINE="${FACEFUSION_OFFLINE:-1}"
export FACEFUSION_ALLOW_CPU_FALLBACK="${FACEFUSION_ALLOW_CPU_FALLBACK:-0}"
export FACEFUSION_CURL_BIN="${FACEFUSION_CURL_BIN:-curl}"
export FACEFUSION_FFMPEG_BIN="${FACEFUSION_FFMPEG_BIN:-ffmpeg}"

python facefusion.py "$@"
