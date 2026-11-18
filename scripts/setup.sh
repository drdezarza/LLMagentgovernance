#!/bin/bash
# One-time setup: creates a virtual environment, installs dependencies, runs the equivalence tests and,
# if a Nebius key is configured, checks the live model catalogue.
# Usage:  bash scripts/setup.sh
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=""
for c in python3.12 python3.11 python3.10 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)'; then
    PY="$(command -v "$c")"; break
  fi
done
[ -n "$PY" ] || { echo "Python 3.9+ is required."; exit 1; }
echo "Using $PY ($($PY --version))"
[ -d .venv ] || "$PY" -m venv .venv
source .venv/bin/activate
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
echo "✓ environment ready (.venv)"
python tests/test_equivalence.py
python paper/check_numbers.py
if [ ! -f credentials/nebius.env ]; then
  cp credentials/nebius.env.example credentials/nebius.env
fi
if grep -q "PASTE_YOUR_KEY_HERE" credentials/nebius.env && [ -z "$NEBIUS_API_KEY" ]; then
  echo ""
  echo "Offline use is ready (analyze, mock runs). For live runs, paste your key into credentials/nebius.env"
  echo "or export NEBIUS_API_KEY, then run:  python -m agentgov check"
  exit 0
fi
python -m agentgov check
