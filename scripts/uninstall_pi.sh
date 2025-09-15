#!/usr/bin/env bash
set -euo pipefail

# Usage:
#  bash scripts/uninstall_pi.sh [--yes|-y] [--remove-ollama] [--remove-project]
#
# --yes|-y           non-interactive
# --remove-ollama    also remove Ollama binary, service, and data directories
# --remove-project   delete this project folder after uninstall

CONFIRM=0
REMOVE_OLLAMA=0
REMOVE_PROJECT=0

for arg in "$@"; do
	case "$arg" in
		--yes|-y) CONFIRM=1 ;;
		--remove-ollama) REMOVE_OLLAMA=1 ;;
		--remove-project) REMOVE_PROJECT=1 ;;
		*) echo "Unknown option: $arg"; exit 2 ;;
	esac
done

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

echo "Stopping/disabling Ollama service (if present)"
sudo systemctl stop ollama 2>/dev/null || true
sudo systemctl disable ollama 2>/dev/null || true

# Remove default pulled model, ignore errors
if command -v ollama >/dev/null 2>&1; then
	echo "Removing example model (if present): llama3.2:3b"
	ollama rm llama3.2:3b 2>/dev/null || true
fi

# Optionally remove Ollama binary, service unit, and data
if [[ $REMOVE_OLLAMA -eq 1 ]]; then
	echo "Removing Ollama binary, service unit, and data (if present)"
	# Binary
	sudo rm -f /usr/local/bin/ollama 2>/dev/null || true
	# Systemd unit
	sudo rm -f /etc/systemd/system/ollama.service 2>/dev/null || true
	sudo systemctl daemon-reload 2>/dev/null || true
	# Data directories used by various installs
	rm -rf "$HOME/.ollama" 2>/dev/null || true
	sudo rm -rf /var/lib/ollama 2>/dev/null || true
	sudo rm -rf /usr/share/ollama 2>/dev/null || true
fi

# Remove Poetry virtualenv for this project if present
if command -v poetry >/dev/null 2>&1; then
	echo "Removing Poetry virtualenv (if any)"
	poetry env remove --all 2>/dev/null || true
fi

echo "Uninstall complete."

# Optionally remove project directory
if [[ $REMOVE_PROJECT -eq 1 ]]; then
	PROJECT_DIR=$(cd "$(dirname "$0")/.." && pwd)
	if [[ $CONFIRM -eq 0 ]]; then
		read -r -p "Delete project directory $PROJECT_DIR ? [y/N] " ans2
		case "$ans2" in
			[yY][eE][sS]|[yY]) ;;
			*) echo "Skipped project deletion."; exit 0;;
		esac
	fi
	echo "Deleting $PROJECT_DIR"
	rm -rf "$PROJECT_DIR"
fi
