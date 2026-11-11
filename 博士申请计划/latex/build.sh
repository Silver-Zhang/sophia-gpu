#!/bin/bash
# V2.1 builds use separate output; --check preserves releases.
set -euo pipefail
cd "$(dirname "$0")"
MODE="${1:-build}"
case "$MODE" in build|--check) ;; *) echo 'Usage: bash build.sh [--check]' >&2; exit 2 ;; esac
BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/proposal-build.XXXXXX")"
trap 'rm -rf "$BUILD_DIR"' EXIT
if [ -x "$HOME/texlive/2026/bin/universal-darwin/xelatex" ]; then
  XELATEX="$HOME/texlive/2026/bin/universal-darwin/xelatex"
else
  XELATEX="$(command -v xelatex)"
fi
python3 check.py
for pass in 1 2 3; do
  if ! "$XELATEX" -halt-on-error -file-line-error -interaction=nonstopmode -output-directory="$BUILD_DIR" main.tex >"$BUILD_DIR/stdout" 2>&1; then
    tail -40 "$BUILD_DIR/stdout" >&2
    exit 1
  fi
done
python3 check.py --log "$BUILD_DIR/main.log"
test -s "$BUILD_DIR/main.pdf"
if [ "$MODE" = '--check' ]; then
  echo 'OK: three XeLaTeX passes; release PDF unchanged.'
else
  mkdir -p ../exports
  cp "$BUILD_DIR/main.pdf" ../exports/.proposal-build.tmp
  mv ../exports/.proposal-build.tmp ../exports/博士科研计划书_V2.1_批注与表达精修_20261111.pdf
  echo 'OK -> ../exports/博士科研计划书_V2.1_批注与表达精修_20261111.pdf'
fi
