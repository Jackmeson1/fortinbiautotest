#!/usr/bin/env bash
# Set up a Python virtual environment and install project dependencies.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

if [ ! -f config/config.yaml ] && [ -f config/config.yaml.example ]; then
    cp config/config.yaml.example config/config.yaml
fi

echo "Environment setup complete."
