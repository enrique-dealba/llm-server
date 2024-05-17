import logging
import time

import requests
from dotenv import load_dotenv

from config import Settings
from text_processing import TextProcessing as tp
from templates import Foo, get_model_fields_and_descriptions

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


foo_fields_and_descriptions = get_model_fields_and_descriptions(Foo)

field_1_name, field_1_desc = foo_fields_and_descriptions[0]
field_2_name, field_2_desc = foo_fields_and_descriptions[1]

# json_prompt_1 = f"""
# <|im_start|>system
# You are a helpful assistant designed to output single JSON fields.
# Given the following user prompt
# << {user_prompt} >>
# extract the following field:
# << {field_1_name} >> with description: {field_1_desc} from the user prompt.
# Example:
# Input:
# user_prompt: "Make a Foo with name Qwerty and ID 906 please."
# Result: {{
#     "{field_1_name}": "Qwerty",
# }}
# <|im_end|>

# <|im_start|>user
# Input:
# user_prompt: {user_prompt}
# <|im_end|>

# <|im_start|>assistant
# Result:
# """

# json_prompt_2 = f"""
# <|im_start|>system
# You are a helpful assistant designed to output single JSON fields.
# Given the following user prompt
# << {user_prompt} >>
# extract the following field info:
# << {field_1_name} >> with description: {field_1_desc} from the user prompt.
# Example:
# Input:
# user_prompt: "Make a Foo with name Qwerty and ID 906 please."
# field_info: Field name: << {field_1_name} >> with description: {field_1_desc}.
# Result: {{
#     "{field_1_name}": "Qwerty",
# }}
# <|im_end|>

# <|im_start|>user
# Input:
# user_prompt: {user_prompt}
# field_info: Field name: << {field_1_name} >> with description: {field_1_desc}.
# <|im_end|>

# <|im_start|>assistant
# Result:
# """

def main():
    """Conversation loop with LLM server."""
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break

        try:
            json_prompt_1a = f"""
            <|im_start|>system
            You are a helpful assistant designed to output single JSON fields.
            Given the following user prompt
            << {prompt} >>
            extract the following field:
            << {field_1_name} >> with description: {field_1_desc} from the user prompt.
            Example:
            Input:
            user_prompt: "Make a Foo with name Qwerty and ID 906 please."
            Result: {{
                "{field_1_name}": "Qwerty",
            }}
            <|im_end|>

            <|im_start|>user
            Input:
            user_prompt: {prompt}
            <|im_end|>

            <|im_start|>assistant
            Result:
            """

            json_prompt_1b = f"""
            <|im_start|>system
            You are a helpful assistant designed to output single JSON fields.
            Given the following user prompt
            << {prompt} >>
            extract the following field:
            << {field_2_name} >> with description: {field_2_desc} from the user prompt.
            Example:
            Input:
            user_prompt: "Make a Foo with name Qwerty and ID 906 please."
            Result: {{
                "{field_2_name}": "906",
            }}
            <|im_end|>

            <|im_start|>user
            Input:
            user_prompt: {prompt}
            <|im_end|>

            <|im_start|>assistant
            Result:
            """

            t_0 = time.perf_counter()  # better than time.time()
            result_1 = Client.generate_text(json_prompt_1a)
            result_2 = Client.generate_text(json_prompt_1b)
            t_1 = time.perf_counter()

            # print(f"Raw Response: {result}")

            if "text" in result_1:
                response_1 = result_1["text"]
            elif "detail" in result_1:
                response_1 = result_1["detail"]

            if "text" in result_2:
                response_2 = result_2["text"]
            elif "detail" in result_1:
                response_2 = result_2["detail"]

            if not response_1:
                raise ValueError("Empty LLM response content")
            if not isinstance(response_1, str):
                response_1 = str(response_1)  # TODO: add try/catch block

            if not response_2:
                raise ValueError("Empty LLM response content")
            if not isinstance(response_2, str):
                response = str(response_2)  # TODO: add try/catch block

            response = response_1 + "\n" + response_2

            response = tp.clean_mistral(response)  # TODO: check DEFAULT_MODEL to choose
            print(f"\nLLM Response: {response}")

            # queries = result.get("queries")
            # if queries:
            #     print(f"\nPrevious Queries: {queries}")

            tps = tp.measure_performance(t_0, t_1, response)
            print(f"Tokens per second: {tps} t/s")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
