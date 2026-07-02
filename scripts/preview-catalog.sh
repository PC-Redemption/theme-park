#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "${ROOT_DIR}"
python3 scripts/build-static-sites.py >/dev/null
python3 scripts/build-catalog.py >/dev/null
echo "Open http://127.0.0.1:8000/catalog/index.html"
exec python3 -m http.server 8000
