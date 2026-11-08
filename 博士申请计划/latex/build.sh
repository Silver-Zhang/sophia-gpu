#!/bin/bash
# XeLaTeX：隔离中间文件，失败时不留下可误认为新结果的 main.pdf。
set -euo pipefail
cd "$(dirname "$0")"
BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/rp-v5-build.XXXXXX")"
mkdir -p qa/build
if [ -f main.pdf ]; then
  mv main.pdf "$BUILD_DIR/previous-main.pdf"
fi
if [ -f ../exports/博士科研计划书_V5.pdf ]; then
  mv ../exports/博士科研计划书_V5.pdf "$BUILD_DIR/previous-export.pdf"
fi
trap 'code=$?; if [ "$code" -ne 0 ]; then echo "FAILED (exit $code): 隔离构建目录 ${BUILD_DIR}；旧 PDF（如有）为 previous-main.pdf" >&2; fi' EXIT
if [ -x "$HOME/texlive/2026/bin/universal-darwin/xelatex" ]; then
  XELATEX="$HOME/texlive/2026/bin/universal-darwin/xelatex"
elif command -v xelatex >/dev/null 2>&1; then
  XELATEX="$(command -v xelatex)"
else
  echo '找不到 xelatex，请安装 TeX Live 并加入 PATH' >&2
  exit 1
fi
python3 qa/check_integrity.py
for pass in 1 2 3; do
  if "$XELATEX" -halt-on-error -file-line-error -interaction=nonstopmode -output-directory="$BUILD_DIR" main.tex >"$BUILD_DIR/pass-$pass.stdout" 2>&1; then
    cp "$BUILD_DIR/main.log" "qa/build/pass-$pass.log"
  else
    code=$?
    cp "$BUILD_DIR/pass-$pass.stdout" "qa/build/failed-pass-$pass.txt"
    [ ! -f "$BUILD_DIR/main.log" ] || cp "$BUILD_DIR/main.log" qa/build/failed-main.log
    tail -35 "$BUILD_DIR/pass-$pass.stdout" >&2
    exit "$code"
  fi
done
python3 qa/check_integrity.py --log "$BUILD_DIR/main.log"
test -s "$BUILD_DIR/main.pdf"
cp "$BUILD_DIR/main.pdf" main.pdf
mkdir -p ../exports
cp main.pdf ../exports/博士科研计划书_V5.pdf
python3 - "$BUILD_DIR" <<'PY'
from pathlib import Path
import hashlib,json,sys
root=Path.cwd();out={'source_sha256':hashlib.sha256((root/'main.tex').read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256((root/'main.pdf').read_bytes()).hexdigest(),'build_directory':sys.argv[1],'passes':3,'xelatex_return_codes':[0,0,0],'final_log_sha256':hashlib.sha256((root/'qa/build/pass-3.log').read_bytes()).hexdigest()}
(root/'qa/build/build_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
PY
printf 'OK -> %s/main.pdf\n' "$PWD"
