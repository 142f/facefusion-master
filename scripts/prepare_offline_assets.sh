#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
ASSET_ARCHIVE="${ASSET_ARCHIVE:-${PROJECT_ROOT}/facefusion_assets.tar.gz}"

cd "${PROJECT_ROOT}"

python facefusion.py force-download \
  --download-providers github huggingface \
  --log-level info

tar -czf "${ASSET_ARCHIVE}" .assets
sha256sum "${ASSET_ARCHIVE}" > "${ASSET_ARCHIVE}.sha256"

ls -lh "${ASSET_ARCHIVE}"
cat "${ASSET_ARCHIVE}.sha256"
