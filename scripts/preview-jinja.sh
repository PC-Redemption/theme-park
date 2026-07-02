#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER="${STARTER:-operations-shell-jinja}"
exec "${ROOT_DIR}/scripts/preview-starter.sh" "${STARTER}"
