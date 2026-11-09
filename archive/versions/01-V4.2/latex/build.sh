#!/bin/bash
# 编译博士科研计划书 LaTeX 源码（需要 XeLaTeX + ctex + 系统中文宋体/黑体）
# 用法：bash build.sh
set -euo pipefail

cd "$(dirname "$0")"

# 优先级：本机用户级 TeX Live（含 ctex） > PATH 中的 xelatex
if [ -x "$HOME/texlive/2026/bin/universal-darwin/xelatex" ]; then
  XELATEX="$HOME/texlive/2026/bin/universal-darwin/xelatex"
elif command -v xelatex >/dev/null 2>&1; then
  XELATEX=xelatex
else
  echo "找不到 xelatex，请先安装 TeX Live 并加入 PATH" >&2
  exit 1
fi

"$XELATEX" -interaction=nonstopmode main.tex >/dev/null || true   # 第 1 遍：写 .aux
"$XELATEX" -interaction=nonstopmode main.tex >/dev/null || true   # 第 2 遍：解析目录与引用

if [ -f main.pdf ]; then
  echo "OK  -> $(pwd)/main.pdf"
else
  echo "FAILED：请看 main.log 中的 ! 开头行" >&2
  grep -n '^!' main.log | head -20 >&2
  exit 1
fi
