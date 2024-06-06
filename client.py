import logging
from typing import Any, Dict

import requests

from config import Settings
from text_processing import TextProcessing as tp


class Client:
    """Client for interacting with LLM server."""

    def __init__(self):
        """Initializes Client."""
        self.settings = Settings()

    def generate_text(self, prompt: str) -> Dict[str, Any]:
        """Sends a text generation request to the LLM server."""
        processed_prompt = tp.preprocess_prompt(prompt)
        payload = {"text": processed_prompt}
        try:
            response = requests.post(f"{self.settings.API_URL}/generate", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise
