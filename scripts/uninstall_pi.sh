#!/usr/bin/env bash
set -euo pipefail

CONFIRM=0
if [[ "${1-}" == "--yes" || "${1-}" == "-y" ]]; then
	CONFIRM=1
fi

if [[ $CONFIRM -eq 0 ]]; then
	read -r -p "This will remove Pi AI Assistant config and stop Ollama. Continue? [y/N] " ans
	case "$ans" in
		[yY][eE][sS]|[yY]) ;;
		*) echo "Aborted."; exit 1;;
	esac
fi

# Remove config
CONFIG_DIR="$HOME/.config/pi-ai-assistant"
CONFIG_FILE="$CONFIG_DIR/config.toml"
if [[ -f "$CONFIG_FILE" ]]; then
	echo "Removing config: $CONFIG_FILE"
	rm -f "$CONFIG_FILE"
fi
if [[ -d "$CONFIG_DIR" ]]; then
	rmdir "$CONFIG_DIR" 2>/dev/null || true
fi

echo "Attempting to stop/disable Ollama service (if present)"
sudo systemctl stop ollama 2>/dev/null || true
sudo systemctl disable ollama 2>/dev/null || true

if command -v ollama >/dev/null 2>&1; then
	echo "Removing example model (if present): llama3.2:3b"
	ollama rm llama3.2:3b 2>/dev/null || true
fi

# Remove Poetry virtualenv for this project if present
if command -v poetry >/dev/null 2>&1; then
	echo "Removing Poetry virtualenv (if any)"
	poetry env remove --all 2>/dev/null || true
fi

echo "Uninstall complete. You can delete the project folder if desired."
