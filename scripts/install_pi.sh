#!/usr/bin/env bash
set -euo pipefail

# Basic system deps
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git build-essential curl

# Install Poetry if missing
if ! command -v poetry >/dev/null 2>&1; then
	curl -sSL https://install.python-poetry.org | python3 -
	echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
	echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
	export PATH="$HOME/.local/bin:$PATH"
fi

# Create venv and install
poetry install --no-root

# Suggest Ollama install and a small model
if ! command -v ollama >/dev/null 2>&1; then
	curl -fsSL https://ollama.com/install.sh | sh
fi

# Start Ollama service
sudo systemctl enable ollama || true
sudo systemctl start ollama || true

# Pull a lightweight model
ollama pull llama3.2:3b || true

echo "Installation complete. Try: poetry run pi-assistant --repl"
