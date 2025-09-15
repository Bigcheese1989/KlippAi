import os
from typing import Any, Dict

import requests

from ..config import AppConfig
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
	def __init__(self, config: AppConfig) -> None:
		super().__init__(config)
		if not config.openai_api_key:
			raise ValueError("OPENAI_API_KEY is required for openai backend")
		self.api_key = config.openai_api_key
		self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

	def _headers(self) -> Dict[str, str]:
		return {
			"Authorization": f"Bearer {self.api_key}",
			"Content-Type": "application/json",
		}

	def generate(self, prompt: str) -> str:
		# Use Chat Completions for widest compatibility
		url = f"{self.base_url}/chat/completions"
		payload: Dict[str, Any] = {
			"model": self.config.model,
			"messages": [
				{"role": "system", "content": "You are a concise, helpful CLI assistant."},
				{"role": "user", "content": prompt},
			],
			"temperature": self.config.temperature,
			"max_tokens": self.config.max_tokens,
		}
		resp = requests.post(url, headers=self._headers(), json=payload, timeout=120)
		resp.raise_for_status()
		data = resp.json()
		choices = data.get("choices") or []
		if choices:
			message = choices[0].get("message") or {}
			return message.get("content", "")
		return ""
