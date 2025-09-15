import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

from dotenv import load_dotenv
import toml


CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "pi-ai-assistant")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.toml")


@dataclass
class PrinterConfig:
	make: str
	model: str
	bed_width_mm: float
	bed_depth_mm: float
	origin_x_mm: float
	origin_y_mm: float
	kinematics: str


@dataclass
class KlipperConfig:
	moonraker_url: str
	api_key: Optional[str]


@dataclass
class AppConfig:
	backend: str
	model: str
	hf_token: Optional[str]
	temperature: float
	max_tokens: int
	printer: Optional[PrinterConfig]
	klipper: KlipperConfig


DEFAULTS = {
	"backend": "huggingface",
	"model_huggingface": "mistralai/Mistral-7B-Instruct-v0.2",
	"temperature": 0.3,
	"max_tokens": 256,
	"moonraker_url": "http://localhost:7125",
}


def _ensure_config_dir() -> None:
	os.makedirs(CONFIG_DIR, exist_ok=True)


def _load_toml_config() -> Dict[str, Any]:
	if not os.path.exists(CONFIG_PATH):
		return {}
	try:
		with open(CONFIG_PATH, "r", encoding="utf-8") as f:
			return toml.load(f)
	except Exception:
		return {}


def save_toml_config(data: Dict[str, Any]) -> None:
	_ensure_config_dir()
	with open(CONFIG_PATH, "w", encoding="utf-8") as f:
		toml.dump(data, f)


def load_config(
	backend_override: Optional[str] = None,
	model_override: Optional[str] = None,
	temperature_override: Optional[float] = None,
	max_tokens_override: Optional[int] = None,
) -> AppConfig:
	load_dotenv()
	file_cfg = _load_toml_config()

	backend = (backend_override or os.getenv("PI_ASSISTANT_BACKEND") or file_cfg.get("backend") or DEFAULTS["backend"]).lower()
	if backend not in {"huggingface"}:
		raise ValueError(f"Unsupported backend: {backend}")

	default_model_key = f"model_{backend}"
	model = model_override or os.getenv("MODEL_NAME") or file_cfg.get("model") or DEFAULTS[default_model_key]

	temperature = float(
		temperature_override or os.getenv("TEMPERATURE") or file_cfg.get("temperature") or DEFAULTS["temperature"]
	)
	max_tokens = int(
		max_tokens_override or os.getenv("MAX_TOKENS") or file_cfg.get("max_tokens") or DEFAULTS["max_tokens"]
	)

	hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN") or file_cfg.get("hf_token")

	moonraker_url = os.getenv("MOONRAKER_URL") or (file_cfg.get("klipper") or {}).get("moonraker_url") or DEFAULTS["moonraker_url"]
	klipper_api_key = os.getenv("KLIPPER_API_KEY") or (file_cfg.get("klipper") or {}).get("api_key")

	printer_section = file_cfg.get("printer") or None
	printer = None
	if isinstance(printer_section, dict):
		try:
			printer = PrinterConfig(
				make=str(printer_section.get("make", "")),
				model=str(printer_section.get("model", "")),
				bed_width_mm=float(printer_section.get("bed_width_mm", 0)),
				bed_depth_mm=float(printer_section.get("bed_depth_mm", 0)),
				origin_x_mm=float(printer_section.get("origin_x_mm", 0)),
				origin_y_mm=float(printer_section.get("origin_y_mm", 0)),
				kinematics=str(printer_section.get("kinematics", "cartesian")),
			)
		except Exception:
			printer = None

	config = AppConfig(
		backend=backend,
		model=model,
		hf_token=hf_token,
		temperature=temperature,
		max_tokens=max_tokens,
		printer=printer,
		klipper=KlipperConfig(moonraker_url=moonraker_url, api_key=klipper_api_key),
	)
	return config


def write_printer_and_klipper_to_config(
	printer: PrinterConfig,
	klipper: KlipperConfig,
	llm_overrides: Optional[Dict[str, Any]] = None,
) -> None:
	data = _load_toml_config()
	data.setdefault("printer", {})
	data["printer"] = {
		"make": printer.make,
		"model": printer.model,
		"bed_width_mm": printer.bed_width_mm,
		"bed_depth_mm": printer.bed_depth_mm,
		"origin_x_mm": printer.origin_x_mm,
		"origin_y_mm": printer.origin_y_mm,
		"kinematics": printer.kinematics,
	}
	data.setdefault("klipper", {})
	data["klipper"] = {
		"moonraker_url": klipper.moonraker_url,
		"api_key": klipper.api_key,
	}
	if llm_overrides:
		data.update(llm_overrides)
	save_toml_config(data)
