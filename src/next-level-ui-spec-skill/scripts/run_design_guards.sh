#!/usr/bin/env bash

set -euo pipefail

TARGET="${1:-both}"
MODE="${2:-changed}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${TARGET}" != "mobile" && "${TARGET}" != "web" && "${TARGET}" != "both" ]]; then
  echo "Usage: $0 [mobile|web|both] [changed|staged|all]" >&2
  exit 1
fi

if [[ "${MODE}" != "changed" && "${MODE}" != "staged" && "${MODE}" != "all" ]]; then
  echo "Usage: $0 [mobile|web|both] [changed|staged|all]" >&2
  exit 1
fi

run_mobile() {
  echo "Running mobile design guard (${MODE})"
  python3 "${SCRIPT_DIR}/mobile_design_spec_guard.py" "--${MODE}"
}

run_web() {
  echo "Running web design guard (${MODE})"
  python3 "${SCRIPT_DIR}/web_design_spec_guard.py" "--${MODE}"
}

case "${TARGET}" in
  mobile)
    run_mobile
    ;;
  web)
    run_web
    ;;
  both)
    run_mobile
    run_web
    ;;
esac
