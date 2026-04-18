#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
HOST="127.0.0.1"
PORT="8001"

cd "$PROJECT_DIR"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Virtual environment not found at: $VENV_DIR"
  echo "Create it first with:"
  echo "  python3 -m venv .venv"
  echo "  source .venv/bin/activate"
  echo "  pip install -r requirements.txt"
  exit 1
fi

source "$VENV_DIR/bin/activate"

if [[ ! -f "$PROJECT_DIR/app/main.py" ]]; then
  echo "FastAPI entrypoint not found: $PROJECT_DIR/app/main.py"
  exit 1
fi

echo "Starting Serinity AI API on http://$HOST:$PORT"
exec uvicorn app.main:app --reload --host "$HOST" --port "$PORT"
