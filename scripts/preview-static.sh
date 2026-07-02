#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER="${STARTER:-operations-shell-static}"

cd "${ROOT_DIR}"
python3 scripts/build-static-sites.py >/dev/null
if [[ ! -f "${ROOT_DIR}/sites/${STARTER}/starter.manifest.json" ]]; then
  echo "Missing starter manifest for ${STARTER}" >&2
  exit 1
fi
echo "Open http://127.0.0.1:8000/sites/${STARTER}/templates/index.html"
exec python3 sites/operations-shell-static/preview.py
