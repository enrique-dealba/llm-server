import logging
import time

import requests
from dotenv import load_dotenv

from config import Settings
from templates import Foo, FooTemplate
from text_processing import TextProcessing as tp
from utils import combine_jsons, get_model_fields_and_descriptions, is_json_like

load_dotenv()
settings = Settings()

foo_fields_and_descriptions = get_model_fields_and_descriptions(Foo)


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


def extract_field_from_prompt(
    prompt: str, field_name: str, field_desc: str, example: str
) -> str:
    """Extracts a single field from the user prompt using the LLM."""
    json_prompt = f"""
    <|im_start|>system
    You are a helpful assistant designed to output single JSON fields.
    Given the following user prompt
    << {prompt} >>
    extract the following field:
    << {field_name} >> with description: {field_desc} from the user prompt.
    Example:
    Input:
    user_prompt: "Make a Foo with name Qwerty and ID 906 please."
    Result: {{
        "{field_name}": "{example}",
    }}
    <|im_end|>

    <|im_start|>user
    Input:
    user_prompt: {prompt}
    <|im_end|>

    <|im_start|>assistant
    Result:
    """

    result = Client.generate_text(json_prompt)
    if "text" in result:
        return result["text"]
    elif "detail" in result:
        return result["detail"]
    else:
        raise ValueError("Unexpected LLM response format")


def main():
    """Conversation loop with LLM server."""
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break

        try:
            t_0 = time.perf_counter()
            json_strs = []
            examples = ["Qwerty", "987"]
            i = 0
            for field_name, field_desc in foo_fields_and_descriptions:
                response = extract_field_from_prompt(
                    prompt, field_name, field_desc, example=examples[i]
                )
                i += 1
                if is_json_like(response):
                    json_strs.append(response)
            t_1 = time.perf_counter()

            if json_strs:
                extracted_model = combine_jsons(json_strs, FooTemplate)
            else:
                json_strs = ["JSON Parsing Failed!"]

            response = "\n".join(json_strs)
            cleaned_response = tp.clean_mistral(response)
            print(f"\nLLM Response: {cleaned_response}")
            print("=" * 30)
            print(f"EXTRACTED MODEL: {extracted_model}")

            tps = tp.measure_performance(t_0, t_1, cleaned_response)
            print(f"Tokens per second: {tps} t/s")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
