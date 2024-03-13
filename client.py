import json
import logging
import time

import requests
from dotenv import load_dotenv
from typing import Union, List, Dict

from config import Settings
from text_processing import TextProcessing as tp

load_dotenv()
settings = Settings()


def deserialize_llm_result(obj: Dict) -> Dict:
    """Custom object hook for deserializing LLMResult objects."""
    if "_type" in obj and obj["_type"] == "LLMResult":
        # Deserialize LLMResult object
        return {
            "text": obj["text"],
        }
    return obj


class Client:
    """Client for interacting with LLM server."""

    # @staticmethod
    # def generate_text(prompt: str):
    #     """Sends text generation request to LLM server."""
    #     prompt = tp.preprocess_prompt(prompt)
    #     payload = {"text": prompt}
    #     try:
    #         response = requests.post(f"{settings.API_URL}/generate", json=payload)
    #         return response.json()
    #     except requests.exceptions.RequestException as e:
    #         logging.error(f"API request failed: {e}")
    #         raise

    @staticmethod
    def generate_text(prompt: str) -> Union[str, List[Dict]]:
        """Sends text generation request to LLM server."""
        prompt = tp.preprocess_prompt(prompt)
        payload = {"text": prompt}

        try:
            response = requests.post(f"{settings.API_URL}/generate", json=payload)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            try:
                # Attempt to parse the response as JSON
                json_response = response.json()

                if isinstance(json_response, list):
                    # Handle case when response is a list of serialized objects
                    deserialized_response = [
                        json.loads(json.dumps(obj), object_hook=deserialize_llm_result)
                        for obj in json_response
                    ]
                    return deserialized_response
                elif isinstance(json_response, dict) and "detail" in json_response:
                    # Handle case when response contains an error message
                    error_message = json_response["detail"]
                    logging.error(f"API request failed: {error_message}")
                    raise ValueError(error_message)
                else:
                    # Handle case when response is a single JSON object
                    return json_response

            except json.JSONDecodeError:
                # Handle case when response is not valid JSON
                logging.error(f"API response is not valid JSON: {response.text}")
                raise

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

            print(f"Raw Response: {result}")

            if "text" in result:
                response = result["text"]
            elif "detail" in result:
                response = result["detail"]

            if not response:
                raise ValueError("Empty LLM response content")
            if not isinstance(response, str):
                response = str(response)  # TODO: add try/catch block

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
