import logging
import time

import requests
from dotenv import load_dotenv

from config import Settings
from objectives import objectives
from text_processing import TextProcessing as tp
from utils import (
    calculate_filling_percentage,
    combine_jsons,
    clean_json_str,
    extract_field_from_prompt,
    extract_time_from_prompt,
    extract_json_objective,
    extract_objective,
    get_model_fields_and_descriptions,
    is_json_like,
)

from templates import ObjectiveTime, ObjectiveTimeTemplate

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

        objective_llm = extract_objective(prompt, client)
        objective = extract_json_objective(objective_llm)
        print(f"EXTRACTED OBJECTIVE: {objective}")

        json_strs = []
        time_strs = []

        if objective:
            for objective_name in objectives.keys():
                if objective_name in objective:
                    objective = objective_name
        else:
            print("Objective not found. Defaulting to CMO.")
            objective = "CMO"  # default

        obj_info = objectives[objective]
        fields_and_descriptions = get_model_fields_and_descriptions(
            obj_info["base_model"]
        )

        max_tries = 3
        if len(obj_info["example_fields"]) != len(fields_and_descriptions):
            raise ValueError("'examples' list must have same length as objective fields.")

        for (field_name, field_desc), example in zip(
            fields_and_descriptions, obj_info["example_fields"]
        ):
            num_tries = 0
            while num_tries < max_tries:
                response = extract_field_from_prompt(
                    prompt,
                    field_name,
                    field_desc,
                    example=example,
                    obj=objective,
                    client=client,
                )
                if is_json_like(response):
                    json_strs.append(response)
                    break
                num_tries += 1
            else:
                logging.warning(
                    f"Failed to extract field '{field_name}' after {max_tries} attempts."
                )

        time_model = get_model_fields_and_descriptions(ObjectiveTime)
        for field_name, field_desc in time_model:
            num_tries = 0
            while num_tries < max_tries:
                response = extract_time_from_prompt(
                    prompt,
                    field_name,
                    field_desc,
                    client=client,
                )

                cleaned_response = clean_json_str(response)
                if is_json_like(cleaned_response):
                    time_strs.append(cleaned_response)
                    break
                elif is_json_like(response):
                    time_strs.append(response)
                    break
                else:
                    print("WARNING: NOT JSON-LIKE")
                    print(f"Raw LLM response at attempt={num_tries}: {response}")
                num_tries += 1
            else:
                logging.warning(
                    f"Failed to extract time field '{field_name}' after {max_tries} attempts."
                )

        t_1 = time.perf_counter()

        extracted_model = None
        extracted_time = None
        correctness = 0.0
        time_correctness = 0.0

        if json_strs:
            extracted_model = combine_jsons(json_strs, obj_info["template"])
            correctness = calculate_filling_percentage(extracted_model)
        else:
            json_strs = ["JSON Parsing Failed!"]

        if time_strs:
            extracted_time = combine_jsons(time_strs, ObjectiveTimeTemplate)
            time_correctness = calculate_filling_percentage(extracted_time)
        else:
            time_strs = ["TIME Parsing Failed!"]


        response = "\n".join(json_strs)
        cleaned_response = tp.clean_mistral(response)

        # USE BELOW DURING DEBUGGING
        print(f"\nLLM Response: {cleaned_response}")
        print("=" * 30)
        print(f"EXTRACTED OBJECTIVE MODEL: {extracted_model}")
        print(f"EXTRACTED TIME MODEL: {extracted_time}")
        print(f"Objective Model Correctness: {correctness:.2%}")
        print(f"Time Correctness: {time_correctness:.2%}")

        tps = tp.measure_performance(t_0, t_1, cleaned_response)
        print(f"Tokens per second: {tps} t/s")

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
