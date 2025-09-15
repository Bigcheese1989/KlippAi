from ..config import AppConfig
from .base import LLMProvider
from .ollama import OllamaProvider
from .llamacpp import LlamaCppProvider
from .openai_provider import OpenAIProvider


def create_provider(config: AppConfig) -> LLMProvider:
	if config.backend == "ollama":
		return OllamaProvider(config)
	if config.backend == "llamacpp":
		return LlamaCppProvider(config)
	if config.backend == "openai":
		return OpenAIProvider(config)
	raise ValueError(f"Unsupported backend: {config.backend}")
