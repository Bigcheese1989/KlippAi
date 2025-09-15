import requests

from ..config import AppConfig
from .base import LLMProvider


class OllamaProvider(LLMProvider):
	def __init__(self, config: AppConfig) -> None:
		super().__init__(config)
		self.base_url = config.ollama_host.rstrip("/")

	def generate(self, prompt: str) -> str:
		url = f"{self.base_url}/api/generate"
		resp = requests.post(
			url,
			json={
				"model": self.config.model,
				"prompt": prompt,
				"stream": False,
				"options": {
					"temperature": self.config.temperature,
					"num_predict": self.config.max_tokens,
				},
			},
			timeout=120,
		)
		resp.raise_for_status()
		data = resp.json()
		return data.get("response", "")
