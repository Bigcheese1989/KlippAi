#!/usr/bin/env bash
set -euo pipefail

# Basic system deps
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl

# Install Poetry if missing
if ! command -v poetry >/dev/null 2>&1; then
	curl -sSL https://install.python-poetry.org | python3 -
	echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
	echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
	export PATH="$HOME/.local/bin:$PATH"
fi

# Create venv and install
poetry install --no-root

echo "Install complete. Set HF_TOKEN and run: poetry run pi-assistant setup"
