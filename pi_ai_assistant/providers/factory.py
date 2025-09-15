from ..config import AppConfig
from .base import LLMProvider
from .huggingface import HuggingFaceProvider


def create_provider(config: AppConfig) -> LLMProvider:
	if config.backend == "huggingface":
		return HuggingFaceProvider(config)
	raise ValueError(f"Unsupported backend: {config.backend}")
