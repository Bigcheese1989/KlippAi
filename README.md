# Pi AI Assistant

Cloud-only CLI AI assistant for Raspberry Pi 4 using Hugging Face Inference API, integrated with Klipper via Moonraker.

## Features
- Hugging Face Inference API backend only (no local models)
- Simple one-shot CLI and interactive REPL
- Setup wizard saves printer info and Moonraker settings to TOML

## Quick Start

### 1) Install system deps (Raspberry Pi OS Lite)
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
```

### 2) Install with Poetry (recommended)
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
poetry install --no-root
```

### 3) Set your Hugging Face token
```bash
export HF_TOKEN=hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
# or add to ~/.config/pi-ai-assistant/config.toml under hf_token
```

### 4) First-time setup (saves to ~/.config/pi-ai-assistant/config.toml)
```bash
poetry run pi-assistant setup
```
Prompts:
- printer make and model
- bed size (width/depth mm)
- origin (defaults 0,0)
- kinematics (cartesian, corexy, delta, bedslinger, scara, other)
- Moonraker: defaults to `http://localhost:7125` and only prompts if unreachable

### 5) Use it
```bash
poetry run pi-assistant "best first layer calibration steps?"
poetry run pi-assistant --repl
```

## Configuration
- File: `~/.config/pi-ai-assistant/config.toml`
- Env vars override TOML values
  - `PI_ASSISTANT_BACKEND` = `huggingface`
  - `MODEL_NAME` (default: `mistralai/Mistral-7B-Instruct-v0.2`)
  - `HF_TOKEN` (or `HUGGING_FACE_HUB_TOKEN`)
  - `TEMPERATURE`, `MAX_TOKENS`
  - `MOONRAKER_URL`, `KLIPPER_API_KEY`

## Klipper Integration
- Uses Moonraker (`http://<pi>:7125`) for connectivity
- Setup tests reachability; you can change the URL if not reachable

## Uninstall
```bash
bash scripts/uninstall_pi.sh
# extras:
bash scripts/uninstall_pi.sh --yes --remove-project
```

## License
MIT
