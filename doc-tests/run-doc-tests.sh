#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v sphinx-build >/dev/null 2>&1; then
  echo "error: sphinx-build not found. Install docs dependencies first: pip install -r docs/requirements.txt" >&2
  exit 2
fi

echo "[doc-tests] Running strict Sphinx build checks..."
sphinx-build -b html -W -n --keep-going docs/source docs/build/html >/tmp/doc-tests-sphinx.log 2>&1 || {
  cat /tmp/doc-tests-sphinx.log >&2
  exit 1
}

echo "[doc-tests] Validating Mermaid blocks..."
python3 doc-tests/validate_mermaid.py --use-mmdc-if-available

echo "[doc-tests] All documentation checks passed."
