import requests

from ..config import AppConfig
from .base import LLMProvider


class LlamaCppProvider(LLMProvider):
	def __init__(self, config: AppConfig) -> None:
		super().__init__(config)
		self.base_url = config.llamacpp_server_url.rstrip("/")

	def generate(self, prompt: str) -> str:
		url = f"{self.base_url}/completion"
		resp = requests.post(
			url,
			json={
				"prompt": prompt,
				"temperature": self.config.temperature,
				"n_predict": self.config.max_tokens,
				"stop": ["</s>", "\n\n"],
			},
			timeout=120,
		)
		resp.raise_for_status()
		data = resp.json()
		# llama.cpp server returns {'content': '...'} or {'choices': [{'text': '...'}]} depending on version
		if isinstance(data, dict):
			if "content" in data:
				return data["content"]
			choices = data.get("choices")
			if choices and isinstance(choices, list) and choices[0].get("text"):
				return choices[0]["text"]
		return ""
