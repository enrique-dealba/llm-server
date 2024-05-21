import json
import re
from datetime import datetime, timezone
from typing import Type

from pydantic import BaseModel
from pydantic_core import from_json

from objectives import cmo_info, objectives, pro_info
from templates import time_desciption


def get_current_time() -> str:
    """Gets current time."""
    return str(datetime.now(timezone.utc))


def get_model_fields_and_descriptions(model_class: BaseModel) -> list[tuple[str, str]]:
    """Retrieves the fields and their descriptions from a Pydantic model."""
    schema = model_class.schema()
    fields_and_descriptions = []

    for field_name, field_info in schema["properties"].items():
        description = field_info.get("description", "")
        fields_and_descriptions.append((field_name, description))

    return fields_and_descriptions


def combine_models(model_instances: list[BaseModel]) -> BaseModel:
    """Combines multiple instances of Pydantic model into single unified instance."""
    model_class = type(model_instances[0])
    combined_instance = model_class()

    fields_and_descriptions = get_model_fields_and_descriptions(model_class)

    for field_name, _ in fields_and_descriptions:
        for instance in model_instances:
            field_value = getattr(instance, field_name)
            if field_value is not None:
                setattr(combined_instance, field_name, field_value)
                break

    return combined_instance


def trailing_commas(json_str: str) -> str:
    """Removes trailing commas from JSON string."""
    return re.sub(r",\s*}", "}", json_str)


def preprocess_json(json_str: str) -> str:
    """Preprocess the partial JSON string."""
    new_json = trailing_commas(json_str)
    return new_json


def parse_partial_json(json_str: str, model_class: Type[BaseModel]) -> BaseModel:
    """Parses JSON string and returns in specified Pydantic format."""
    preprocessed_json = preprocess_json(json_str)

    partial_data = from_json(preprocessed_json, allow_partial=True)

    return model_class.model_validate(partial_data)


def combine_jsons(json_str_list: list[str], model_class: Type[BaseModel]) -> BaseModel:
    """Combines JSONs into single Pydantic model."""
    models = []
    for json_str in json_str_list:
        partial_model = parse_partial_json(json_str, model_class)
        models.append(partial_model)

    combined_model = combine_models(models)
    return combined_model


def clean_json_str(json_str: str) -> str:
    """Cleans JSON-like strings to make them more compatible with is_json_like."""
    # Removes leading and trailing whitespace, including newlines and tabs
    json_str = json_str.strip()

    # Removes comments (single-line and multi-line)
    json_str = re.sub(r"//.*", "", json_str)
    json_str = re.sub(r"/\*.*?\*/", "", json_str, flags=re.DOTALL)

    # Removes trailing commas after the last key-value pair
    json_str = re.sub(r",\s*}", "}", json_str)

    # Makes string starts with "{"
    if not json_str.startswith("{"):
        json_str = "{" + json_str

    return json_str


def is_json_like(json_str: str) -> bool:
    """Checks if str is JSON-like."""
    # Checks if the string starts with "{" and ends with "}" or ","
    if re.match(r"^\s*\{.*(\}|,)\s*$", json_str, re.DOTALL):
        # Checks if the string contains valid key-value pairs
        if re.search(
            r'".*?":\s*(".*?"|null|\d+|\{.*?\}|\[.*?\])(,|\s*\})', json_str, re.DOTALL
        ):
            return True
    return False


def extract_json_objective(input_string):
    """Extracts Objective from LLM outputs."""
    normalized_string = re.sub(r"\s+", " ", input_string.replace("\n", " ")).strip()

    # Regex pattern to find the JSON-like substring
    pattern = r'\{\s*"objective"\s*:\s*"(\w+)"\s*,?\s*\}'

    try:
        match = re.search(pattern, normalized_string)
        if match:
            json_str = match.group(0)
            json_str = re.sub(r",\s*\}", " }", json_str)
            json_obj = json.loads(json_str)

            objective_value = json_obj["objective"]
            return objective_value
        else:
            raise ValueError("No matching JSON substring found.")
    except json.JSONDecodeError:
        raise ValueError("Failed to decode JSON.")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")


def extract_objective(prompt: str, client) -> str:
    """Extracts objective definition from the user prompt using LLM."""
    json_prompt = f"""
    <|im_start|>system
    You are a helpful assistant designed to output single JSON fields.
    Given the following user prompt
    << {prompt} >>
    extract the objective definition category that the prompt is most associated with.
    The 'objective' should be one of 'CMO', 'PRO', with the following descriptions:
    {cmo_info['example']}: Description: {cmo_info['description']}
    {pro_info['example']}: Description: {pro_info['description']}
    Examples:
    Input:
    user_prompt: "{cmo_info['prompts'][0]}"
    Result: {{
        "objective": "{cmo_info['example']}",
    }}
    Input:
    user_prompt: "{cmo_info['prompts'][1]}"
    Result: {{
        "objective": "{cmo_info['example']}",
    }}
    Input:
    user_prompt: "{pro_info['prompts'][0]}"
    Result: {{
        "objective": "{pro_info['example']}",
    }}
    user_prompt: "{pro_info['prompts'][1]}"
    Result: {{
        "objective": "{pro_info['example']}",
    }}
    <|im_end|>

    <|im_start|>user
    Input:
    user_prompt: {prompt}
    <|im_end|>

    <|im_start|>assistant
    Result:
    """

    result = client.generate_text(json_prompt)
    if "text" in result:
        return result["text"]
    elif "detail" in result:
        return result["detail"]
    else:
        raise ValueError("Unexpected LLM response format")


def extract_field_from_prompt(
    prompt: str, field_name: str, field_desc: str, example: str, obj: str, client
) -> str:
    """Extracts a single field from the user prompt using the LLM."""
    obj_info = objectives[obj]
    user_example = obj_info["prompts"][0]

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

    result = client.generate_text(json_prompt)
    if "text" in result:
        return result["text"]
    elif "detail" in result:
        return result["detail"]
    else:
        raise ValueError("Unexpected LLM response format")


def extract_time_from_prompt(
    prompt: str, field_name: str, field_desc: str, client
) -> str:
    """Extracts the time fields from the user prompt using the LLM."""
    current_time = get_current_time()

    time_example = "Start the objective at 2024-05-21 19:22:22.650000+00:00"
    example = "2024-05-21 19:22:22.650000+00:00"

    time_prompt = f"""
    <|im_start|>system
    You are a helpful assistant designed to output single JSON fields for times.
    Important note: The current time is {current_time} with the following description:
    {time_desciption}
    Given the following user prompt
    << {prompt} >>
    extract the following time field:
    << {field_name} >> with description: {field_desc} from the user prompt.
    Example:
    Input:
    user_prompt: "{time_example}"
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

    result = client.generate_text(time_prompt)
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
