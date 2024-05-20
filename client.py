import logging
import time

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

from config import Settings
from templates import CMO, CMOTemplate, PRO, PROTemplate
from text_processing import TextProcessing as tp
from utils import combine_jsons, get_model_fields_and_descriptions, is_json_like, extract_json_objective

load_dotenv()
settings = Settings()

foo_fields_and_descriptions = get_model_fields_and_descriptions(PRO)


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


cmo = {
    "prompt": "I need a new catalog maintenance for RME00 with TS markings and use TEST mode with a priority of 10 and set the patience to 30 minutes and end search after 20 minutes.",
    "example": "CMO",
    "description": """The CMO class represents a scheduling objective for catalog 
maintenance using a specific sensor and algorithm, related to astronomical observations or 
tracking. Catalog Maintenance specifies parameters such as the sensor's name, data mode, scheduling priority, 
timing constraints, and classification marking, providing control over how the maintenance 
task is to be executed. By allowing precise configuration of these parameters, it facilitates 
optimized scheduling in a system where timing and priority are required, such as in an observation 
or tracking environment. CMO is useful for satellite or astronomical observation planning.
""",
}

pro = {
    "prompt": "Track object 12345 with sensor RME08, revisiting four times per hour for the next 16 hours using REAL mode, 'S' markings, and set priority to 2.",
    "example": "PRO",
    "description": """The PRO class is designed to create a specific observation 
objective for a given target, with parameters to configure the observation process 
such as sensor name, data mode, revisit frequency, and duration. Periodic Revisit (PRO) sets an end time 
for the objective, either based on input or a default of 10 minutes from the current time, 
and includes handling for converting input string times to datetime objects. Revisit is 
useful in applications that require scheduled monitoring or tracking of specific targets 
(such as celestial objects or satellites) through designated sensors, allowing for controlled 
and periodic observations.
""",
}

def extract_objective(prompt: str) -> str:
    """Extracts objective definition from the user prompt using LLM."""
    json_prompt = f"""
    <|im_start|>system
    You are a helpful assistant designed to output single JSON fields.
    Given the following user prompt
    << {prompt} >>
    extract the objective definition category that the prompt is most associated with.
    The 'objective' should be one of 'CMO', 'PRO', with the following descriptions:
    {cmo['example']}: Description: {cmo['description']}
    {pro['example']}: Description: {pro['description']}
    Examples:
    Input:
    user_prompt: "{cmo['prompt']}"
    Result: {{
        "objective": "{cmo['example']}",
    }}
    Input:
    user_prompt: "{pro['prompt']}"
    Result: {{
        "objective": "{pro['example']}",
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

CMO_examples = [
    "RME00",  # sensor_name
    "TEST",  # data_mode
    "TS",  # classification_marking
    30,  # patience_minutes
    20,  # end_time_offset_minutes
    # "Catalog Maintenance Objective",  # objective_name
    10,  # priority
]

PRO_examples = [
    12345, # target_id
    "RME08", # sensor_name
    "REAL", # data_mode
    "S", # classification_marking
    4, # revisits_per_hour
    16, # hours_to_plan
    2, # priority
]

# user_example = "I need a new catalog maintenance for RME00 with TS markings and use TEST mode with a priority of 10 and set the patience to 30 minutes and end search after 20 minutes."
user_example = "Track object 12345 with sensor RME08, revisiting four times per hour for the next 16 hours using REAL mode, 'S' markings, and set priority to 2."

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
    user_prompt: "{user_example}"
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


def calculate_filling_percentage(model_instance: BaseModel) -> float:
    """Calculates the percentage of filled fields in Pydantic model."""
    total_fields = len(model_instance.__fields__)
    filled_fields = sum(
        1 for _, value in model_instance.__dict__.items() if value is not None
    )
    if total_fields == 0:
        return 0.0
    return filled_fields / total_fields


def process_prompt(prompt: str):
    """Process the given prompt and return the response."""
    try:
        t_0 = time.perf_counter()

        objective_llm = extract_objective(prompt)
        objective = extract_json_objective(objective_llm)
        print(f"EXTRACTED OBJECTIVE: {objective}")

        json_strs = []

        examples = PRO_examples

        max_tries = 3
        if len(examples) != len(foo_fields_and_descriptions):
            raise ValueError("'examples' list must have same length as 'foo_fields'.")

        for (field_name, field_desc), example in zip(
            foo_fields_and_descriptions, examples
        ):
            num_tries = 0
            while num_tries < max_tries:
                response = extract_field_from_prompt(
                    prompt, field_name, field_desc, example=example
                )
                if is_json_like(response):
                    json_strs.append(response)
                    break
                num_tries += 1
            # else:
            #     logging.warning(
            #         f"Failed to extract field '{field_name}' after {max_tries} attempts."
            #     )
        t_1 = time.perf_counter()

        extracted_model = None
        correctness = 0.0
        
        if json_strs:
            extracted_model = combine_jsons(json_strs, PROTemplate)
            correctness = calculate_filling_percentage(extracted_model)
        else:
            json_strs = ["JSON Parsing Failed!"]

        response = "\n".join(json_strs)
        cleaned_response = tp.clean_mistral(response)

        ## USE BELOW DURING DEBUGGING
        print(f"\nLLM Response: {cleaned_response}")
        print("=" * 30)
        print(f"EXTRACTED MODEL: {extracted_model}")
        print(f"Model Correctness: {correctness:.2%}")
        tps = tp.measure_performance(t_0, t_1, cleaned_response)
        print(f"Tokens per second: {tps} t/s")

        return cleaned_response, extracted_model, correctness

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def main():
    """Conversation loop with LLM server."""
    while True:
        prompt = input("Prompt: ")
        if prompt.lower() in ["quit", "exit"]:
            print("Exiting the conversation.")
            break

        response, _, _ = process_prompt(prompt)
        # if response:
        #      print("Response confirmed!")


if __name__ == "__main__":
    main()
