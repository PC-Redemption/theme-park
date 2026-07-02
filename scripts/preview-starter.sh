#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER="${1:-${STARTER:-operations-shell-jinja}}"
PORT="${PORT:-8000}"
HOST="${HOST:-127.0.0.1}"
RELOAD="${RELOAD:-true}"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

MANIFEST_PATH="${ROOT_DIR}/sites/${STARTER}/starter.manifest.json"
if [[ ! -f "${MANIFEST_PATH}" ]]; then
  echo "Missing starter manifest at ${MANIFEST_PATH}" >&2
  exit 1
fi

RUNTIME="$(python3 - <<'PY' "${MANIFEST_PATH}"
import json
import sys
from pathlib import Path
path = Path(sys.argv[1])
print(json.loads(path.read_text())["runtime"])
PY
)"

if [[ "${RUNTIME}" == "jinja" ]]; then
  APP_DIR="${ROOT_DIR}/sites/${STARTER}"
  if [[ ! -x "${VENV_PYTHON}" ]]; then
    echo "Missing ${VENV_PYTHON}. Run scripts/setup-venv.sh first." >&2
    exit 1
  fi
  cd "${APP_DIR}"
  if [[ "${RELOAD}" == "true" ]]; then
    exec "${VENV_PYTHON}" -m uvicorn app:app --reload --host "${HOST}" --port "${PORT}"
  fi
  exec "${VENV_PYTHON}" -m uvicorn app:app --host "${HOST}" --port "${PORT}"
fi

cd "${ROOT_DIR}"
python3 scripts/theme-park.py build-static --starter "${STARTER}" >/dev/null
echo "Open http://${HOST}:${PORT}/sites/${STARTER}/templates/index.html"
exec python3 -m http.server "${PORT}" --bind "${HOST}"
