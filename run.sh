#!/usr/bin/env bash
# One-shot launcher: builds the AI engine if needed, creates a venv, installs deps, runs the game.
set -euo pipefail
cd "$(dirname "$0")"

if command -v pyenv >/dev/null 2>&1; then
  eval "$(pyenv init -)"
  pyenv install -s "$(cat .python-version)"
fi

if [ ! -d .venv ]; then
  python -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -q -r requirements.txt

make -s ai
python main.py "$@"
