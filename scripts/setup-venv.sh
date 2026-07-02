#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
REQ_FILE="${ROOT_DIR}/sites/operations-shell-jinja/requirements.txt"

python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/python" -m ensurepip --upgrade >/dev/null
"${VENV_DIR}/bin/pip" install -r "${REQ_FILE}"

echo "Virtual environment ready at ${VENV_DIR}"
