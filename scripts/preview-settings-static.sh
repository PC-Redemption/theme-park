#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export STARTER="settings-portal-static"
exec "${ROOT_DIR}/scripts/preview-static.sh"
