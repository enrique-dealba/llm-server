import logging
import time

import requests
from dotenv import load_dotenv

from config import API_URL, DEFAULT_MODEL
from text_processing import TextProcessing as tp

load_dotenv()


class Client:
    """Client for interacting with LLM server."""
    @staticmethod
    def generate_text(prompt: str):
        """Sends text generation request to LLM server."""
        payload = {"text": prompt}
        try:
            response = requests.post(f"{API_URL}/generate", json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise


if __name__ == "__main__":
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break

        try:
            t_0 = time.perf_counter() # better than time.time()
            result = Client.generate_text(prompt)
            t_1 = time.perf_counter()

            response = result["text"]
            response = tp.clean_mistral(response) # TODO: check DEFAULT_MODEL to choose
            # response1 = tp.parse_llm_server(response) # for list/str responses
            # response2 = tp.parse_response(response1) # for /user [user] etc
            # response3 = tp.clean_text(response2) # for whitespaces

            print(f"\nLLM Response: {response}")

            queries = result.get("queries")
            if queries:
                print(f"\nPrevious Queries: {queries}")

            tps = tp.measure_performance(t_0, t_1, response)
            print(f"Tokens per second: {tps} t/s")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
