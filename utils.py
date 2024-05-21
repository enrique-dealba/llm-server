import json
import re
from typing import Type

from pydantic import BaseModel
from pydantic_core import from_json

from objectives import cmo_info, objectives, pro_info


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
    user_example = obj_info["prompt"]

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


def calculate_filling_percentage(model_instance: BaseModel) -> float:
    """Calculates the percentage of filled fields in Pydantic model."""
    total_fields = len(model_instance.__fields__)
    filled_fields = sum(
        1 for _, value in model_instance.__dict__.items() if value is not None
    )
    if total_fields == 0:
        return 0.0
    return filled_fields / total_fields
