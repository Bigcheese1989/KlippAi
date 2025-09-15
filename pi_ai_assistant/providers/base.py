from abc import ABC, abstractmethod

from ..config import AppConfig


class LLMProvider(ABC):
	def __init__(self, config: AppConfig) -> None:
		self.config = config

	@abstractmethod
	def generate(self, prompt: str) -> str:
		...
