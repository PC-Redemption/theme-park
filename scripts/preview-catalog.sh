#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "${ROOT_DIR}"
python3 scripts/theme-park.py build-static >/dev/null
python3 scripts/theme-park.py build-catalog >/dev/null
echo "Open http://127.0.0.1:8000/catalog/index.html"
exec python3 -m http.server 8000
