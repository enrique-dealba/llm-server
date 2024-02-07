import logging
import time

import requests
from dotenv import load_dotenv

from config import API_URL
from text_processing import TextProcessing as tp

load_dotenv()


class Client:
    """Client for interacting with LLM server."""

    @staticmethod
    def generate_text(prompt: str):
        """Sends text generation request to LLM server."""
        prompt = tp.preprocess_prompt(prompt)
        payload = {"text": prompt}
        try:
            response = requests.post(f"{API_URL}/generate", json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise


def main():
    """Conversation loop with LLM server."""
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break

        try:
            t_0 = time.perf_counter()  # better than time.time()
            result = Client.generate_text(prompt)
            t_1 = time.perf_counter()

            # if "text" not in result:
            #     raise KeyError("Missing 'text' key in LLM response")
            
            # response = result["text"]
            response = result
            print(response)
            print(type(response))
            
            if 'detail' in response:
                response = response['detail']

            if not response:
                raise ValueError("Empty LLM response content")
            
            response = tp.clean_mistral(response)  # TODO: check DEFAULT_MODEL to choose
            print(f"\nLLM Response: {response}")

            queries = result.get("queries")
            if queries:
                print(f"\nPrevious Queries: {queries}")

            tps = tp.measure_performance(t_0, t_1, response)
            print(f"Tokens per second: {tps} t/s")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
