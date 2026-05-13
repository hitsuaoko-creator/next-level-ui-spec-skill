#!/usr/bin/env bash

set -euo pipefail

TARGET="${1:-both}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${ROOT_DIR}/src/next-level-ui-spec-skill"

if [[ ! -d "${SRC_DIR}" ]]; then
  echo "Missing source skill directory: ${SRC_DIR}" >&2
  exit 1
fi

install_one() {
  local platform_dir="$1"
  local target_dir="${platform_dir}/next-level-ui-spec-skill"
  mkdir -p "${platform_dir}"
  rm -rf "${target_dir}"
  cp -R "${SRC_DIR}" "${target_dir}"
  echo "Installed to ${target_dir}"
}

case "${TARGET}" in
  codex)
    install_one "${HOME}/.codex/skills"
    ;;
  claude)
    install_one "${HOME}/.claude/skills"
    ;;
  both)
    install_one "${HOME}/.codex/skills"
    install_one "${HOME}/.claude/skills"
    ;;
  *)
    echo "Usage: $0 [codex|claude|both]" >&2
    exit 1
    ;;
esac
