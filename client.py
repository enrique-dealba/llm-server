import logging
import time

import requests
from dotenv import load_dotenv

from config import Settings
from objectives import objectives
from templates import PeriodicRevisitObjectiveTemplate
from text_processing import TextProcessing as tp
from utils import (
    calculate_filling_percentage,
    calculate_matching_percentage,
    extract_model,
    model_to_json,
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
        # print(f"Prompt: {prompt}")
        try:
            # t_0 = time.perf_counter()
            response = requests.post(f"{settings.API_URL}/generate", json=payload)
            # t_1 = time.perf_counter()
            # print("="*30)
            # print("=" * 30)
            # print(f"PROMPT time: {t_1 - t_0} seconds")
            # print("=" * 30)

            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise


def process_prompt(prompt: str, client: Client):
    """Process the given prompt and return the response."""
    try:
        t_0 = time.perf_counter()

        # t_start = time.perf_counter()
        objective = process_objective(prompt, client)
        # print(f"\nExtracted Objective: {objective}")
        # t_end = time.perf_counter()
        # print(f"process_objective - Elapsed time: {t_end - t_start} seconds")

        # t_start = time.perf_counter()
        json_strs = process_fields(prompt, objective, client)
        # t_end = time.perf_counter()
        # print(f"process_fields - time: {t_end - t_start} seconds")

        # t_start = time.perf_counter()
        list_strs = process_lists(prompt, objective, client)
        # t_end = time.perf_counter()
        # print(f"process_lists - time: {t_end - t_start} seconds")

        # t_start = time.perf_counter()
        time_strs = process_times(prompt, client)
        # t_end = time.perf_counter()
        # print(f"process_times - time: {t_end - t_start} seconds")

        t_1 = time.perf_counter()

        obj_info = objectives[objective]

        # t_start = time.perf_counter()
        extracted_model = extract_model(obj_info, json_strs, list_strs, time_strs)
        # t_end = time.perf_counter()
        # print(f"extract_model - time: {t_end - t_start} seconds")

        model_json = model_to_json(extracted_model)

        pro_check = PeriodicRevisitObjectiveTemplate(
            classification_marking="U",
            target_id_list=["28884"],
            sensor_name_list=["RME01", "RME02"],
            data_mode="TEST",
            collect_request_type="RATE_TRACK_SIDEREAL",
            patience_minutes=30,
            revisits_per_hour=4.0,
            hours_to_plan=36.0,
            number_of_frames=None,
            integration_time=None,
            binning=1,
            objective_name="PeriodicRevisitObjectiveTemplate",
            objective_start_time="2024-05-25 17:30:00.500000+00:00",
            objective_end_time="2024-05-26 22:30:00.250000+00:00",
            priority=3,
        )

        # correctness = calculate_filling_percentage(extracted_model)
        correctness = calculate_matching_percentage(extracted_model, pro_check)
        response = "\n".join(json_strs)

        cleaned_response = tp.clean_mistral(response)

        # USE BELOW DURING DEBUGGING
        # print(f"\nLLM Response: {cleaned_response}")
        # print("=" * 30)
        print(f"\n{objective}: {model_json}")
        print(f"% Matching Fields: {correctness:.2%}")
        # tps = tp.measure_performance(t_0, t_1, cleaned_response)
        # print(f"Tokens per second: {tps} t/s")
        print(f"Elapsed Time: {t_1 - t_0} seconds")
        # print("=" * 30)

        return cleaned_response, extracted_model, correctness, objective

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def send_prompt(prompt: str, client: Client):
    try:
            t_0 = time.perf_counter()  # better than time.time()
            result = client.generate_text(prompt)
            t_1 = time.perf_counter()

            # print(f"Raw Response: {result}")

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

            # queries = result.get("queries")
            # if queries:
            #     print(f"\nPrevious Queries: {queries}")

            tps = tp.measure_performance(t_0, t_1, response)
            print(f"Tokens per second: {tps} t/s")
            return response

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

        # response, _, _, _ = process_prompt(prompt, client)
        check = send_prompt(prompt, client)
        print(f"Router: {check}")
        if check in ['objective']:
            response, _, _, _ = process_prompt(prompt, client)
        # if response:
        #      print("Response confirmed!")


if __name__ == "__main__":
    main()
