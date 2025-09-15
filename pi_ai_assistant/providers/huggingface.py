import os
from typing import Any, Dict

import requests

from ..config import AppConfig
from .base import LLMProvider


class HuggingFaceProvider(LLMProvider):
	def __init__(self, config: AppConfig) -> None:
		super().__init__(config)
		self.api_url = f"https://api-inference.huggingface.co/models/{self.config.model}"
		self.api_token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN") or self.config.hf_token
		if not self.api_token:
			raise ValueError("HF_TOKEN is required for huggingface backend")

	def _headers(self) -> Dict[str, str]:
		return {
			"Authorization": f"Bearer {self.api_token}",
			"Content-Type": "application/json",
		}

	def generate(self, prompt: str) -> str:
		payload: Dict[str, Any] = {
			"inputs": prompt,
			"parameters": {
				"max_new_tokens": self.config.max_tokens,
				"temperature": self.config.temperature,
			},
		}
		resp = requests.post(self.api_url, headers=self._headers(), json=payload, timeout=120)
		resp.raise_for_status()
		data = resp.json()
		# Responses are typically a list with {'generated_text': '...'}
		if isinstance(data, list) and data:
			item = data[0]
			text = item.get("generated_text") or ""
			if text:
				# Some models echo the prompt; try to strip it
				if text.startswith(prompt):
					return text[len(prompt):].lstrip()
				return text
		return ""
