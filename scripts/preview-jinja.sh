#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"
STARTER="${STARTER:-operations-shell-jinja}"
APP_DIR="${ROOT_DIR}/sites/${STARTER}"
PORT="${PORT:-8000}"
HOST="${HOST:-127.0.0.1}"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "Missing ${VENV_PYTHON}. Run scripts/setup-venv.sh first." >&2
  exit 1
fi

if [[ ! -f "${APP_DIR}/app.py" ]]; then
  echo "Missing starter app at ${APP_DIR}/app.py" >&2
  exit 1
fi

cd "${APP_DIR}"
exec "${VENV_PYTHON}" -m uvicorn app:app --reload --host "${HOST}" --port "${PORT}"
