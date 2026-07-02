#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export STARTER="review-studio-jinja"
exec "${ROOT_DIR}/scripts/preview-jinja.sh"
