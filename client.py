import logging
import time

import requests
from dotenv import load_dotenv

from config import Settings
from objectives import objectives
from text_processing import TextProcessing as tp
from utils import (
    calculate_filling_percentage,
    extract_model,
    process_fields,
    process_lists,
    process_objective,
    process_times,
)

load_dotenv()
settings = Settings()


class Client:
    """Client for interacting with LLM server."""

    @staticmethod
    def generate_text(prompt: str):
        """Sends text generation request to LLM server."""
        prompt = tp.preprocess_prompt(prompt)
        payload = {"text": prompt}
        try:
            response = requests.post(f"{settings.API_URL}/generate", json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise


def process_prompt(prompt: str, client: Client):
    """Process the given prompt and return the response."""
    try:
        t_0 = time.perf_counter()

        objective = process_objective(prompt, client)
        json_strs = process_fields(prompt, objective, client)
        list_strs = process_lists(prompt, client)
        time_strs = process_times(prompt, client)

        t_1 = time.perf_counter()

        obj_info = objectives[objective]

        extracted_model = extract_model(obj_info, json_strs, list_strs, time_strs)

        correctness = calculate_filling_percentage(extracted_model)

        response = "\n".join(json_strs)
        cleaned_response = tp.clean_mistral(response)

        # USE BELOW DURING DEBUGGING
        # print(f"\nLLM Response: {cleaned_response}")
        # print("=" * 30)
        # print(f"EXTRACTED OVERALL OBJECTIVE MODEL: {extracted_model}")
        # print(f"Objective Model Correctness: {correctness:.2%}")
        # tps = tp.measure_performance(t_0, t_1, cleaned_response)
        # print(f"Tokens per second: {tps} t/s")

        return cleaned_response, extracted_model, correctness, objective

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def main():
    """Conversation loop with LLM server."""
    client = Client()
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break

        response, _, _, _ = process_prompt(prompt, client)
        # if response:
        #      print("Response confirmed!")


if __name__ == "__main__":
    main()
