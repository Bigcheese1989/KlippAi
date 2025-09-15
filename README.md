# Pi AI Assistant

Local-first CLI AI assistant designed to run efficiently on Raspberry Pi 4 (Raspberry Pi OS Lite).

## Features
- Local or remote LLM backends (llama.cpp/Ollama, optional OpenAI fallback)
- Simple one-shot CLI and interactive REPL
- Setup wizard saves printer info and Klipper (Moonraker) settings to TOML
- Config via env vars or TOML file

## Quick Start

### 1) Install system deps (Raspberry Pi OS Lite)
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git build-essential
```

### 2) Install with Poetry (recommended)
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
poetry install --no-root
```

### 3) First-time setup (saves to ~/.config/pi-ai-assistant/config.toml)
```bash
poetry run pi-assistant setup
```
Prompts:
- printer make and model
- bed size (width/depth mm)
- origin (defaults 0,0)
- kinematics (cartesian, corexy, delta, bedslinger, scara, other)
- Moonraker: defaults to `http://localhost:7125` and only prompts if unreachable

### 4) Use it
```bash
poetry run pi-assistant "how to level my 3D printer bed?"
poetry run pi-assistant --repl
```

## Configuration
- File: `~/.config/pi-ai-assistant/config.toml`
- Env vars override TOML values
  - `PI_ASSISTANT_BACKEND` = `ollama` | `llamacpp` | `openai`
  - `OLLAMA_HOST`, `LLAMACPP_SERVER_URL`, `OPENAI_API_KEY`
  - `MODEL_NAME`, `TEMPERATURE`, `MAX_TOKENS`
  - `MOONRAKER_URL`, `KLIPPER_API_KEY`

## Klipper Integration
- Uses Moonraker (`http://<pi>:7125`) to communicate
- Setup tests reachability; you can change the URL if not reachable
- Future: command execution, status queries, and job control

## Backends
- Ollama: small footprint server on Pi (q4_K_M models recommended)
- llama.cpp server: use compiled binary with server mode
- OpenAI: optional cloud fallback

## Raspberry Pi Notes
- Prefer 64-bit Raspberry Pi OS. Enable zram or swap for larger models.
- Good starting models: `llama3.2:3b`, `phi3:mini`, `mistral:7b` (quantized).
- Thermal management helps sustain performance.

## License
MIT
