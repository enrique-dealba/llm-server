import logging
import time
from typing import Any, Dict, Optional, Tuple

import requests

from client import Client
from config import Settings
from objectives import objectives
from text_processing import TextProcessing as tp
from utils import (
    calculate_filling_percentage,
    extract_model,
    model_to_json,
    process_fields,
    process_lists,
    process_objective,
    process_times,
)


class PromptProcessor:
    """Processes prompts and handles LLM responses."""

    def __init__(self, client: Client):
        """Initializes PromptProcessor."""
        self.client = client

    def process_skill(
        self, prompt: str
    ) -> Tuple[Optional[str], Optional[Dict[str, Any]], Optional[float], Optional[str]]:
        """Processes the given prompt and returns the response."""
        try:
            start_time = time.perf_counter()

            objective = process_objective(prompt, self.client)
            json_strs = process_fields(prompt, objective, self.client)
            list_strs = process_lists(prompt, objective, self.client)
            time_strs = process_times(prompt, self.client)

            end_time = time.perf_counter()

            obj_info = objectives[objective]

            extracted_model = extract_model(obj_info, json_strs, list_strs, time_strs)

            model_json = model_to_json(extracted_model)

            correctness = calculate_filling_percentage(extracted_model)
            response = "\n".join(json_strs)

            cleaned_response = tp.clean_mistral(response)

            # print(f"\nLLM Response: {cleaned_response}")
            # print("=" * 30)
            print(f"\n{objective}: {model_json}")
            # print(f"% Matching Fields: {correctness:.2%}")
            # tps = tp.measure_performance(start_time, end_time, cleaned_response)
            # print(f"Tokens per second: {tps} t/s")
            # print(f"Elapsed Time: {end_time - start_time} seconds")
            # print("=" * 30)

            return cleaned_response, extracted_model, correctness, objective

        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            return None, None, None, None

    def process_prompt(self, prompt: str) -> Optional[str]:
        """Sends prompt to LLM server and returns response."""
        try:
            start_time = time.perf_counter()
            result = self.client.generate_text(prompt)
            end_time = time.perf_counter()

            if "text" in result:
                response = result["text"]
            elif "detail" in result:
                response = result["detail"]
            else:
                raise ValueError("Unexpected LLM response format")

            if not response:
                raise ValueError("Empty LLM response content")

            response = tp.clean_mistral(response)

            tps = tp.measure_performance(start_time, end_time, response)
            print(f"Tokens per second: {tps} t/s")
            return response

        except (requests.exceptions.RequestException, ValueError) as e:
            logging.error(f"An error occurred: {e}")
            return None


def main():
    """Conversation loop with LLM server."""
    settings = Settings()
    client = Client()
    processor = PromptProcessor(client)

    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break

        if settings.USE_AGENT:
            check = processor.process_prompt(prompt)
            print(f"Router: {check}")
            if check == "objective":
                response, _, _, _ = processor.process_skill(prompt)
        else:
            response, _, _, _ = processor.process_skill(prompt)


if __name__ == "__main__":
    main()
