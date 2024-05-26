import json
import re
import time
from datetime import datetime, timezone
from typing import Optional, Type, Union

from pydantic import BaseModel
from pydantic_core import from_json

from config import Settings
from objectives import cmo_info, deo_info, objectives, pro_info, sco_info, so_info
from templates import (
    ObjectiveList,
    ObjectiveListTemplate,
    ObjectiveModel,
    ObjectiveTime,
    ObjectiveTimeTemplate,
    time_desciption,
)

settings = Settings()


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


def remove_above_curly(input_string: str) -> str:
    """Removes text from string above left curly '{' character."""
    # Splits string into lines
    lines = input_string.split("\n")

    # Finds index of the line containing the opening brace "{"
    start_index = next((i for i, line in enumerate(lines) if "{" in line), 0)

    # Joins lines starting from the line with the opening brace
    processed_string = "\n".join(lines[start_index:])

    return processed_string


def remove_after_comma(input_string: str) -> str:
    """Removes text from string after the first comma ',' character."""
    # Finds the index of the first comma
    comma_index = input_string.find(",")

    if comma_index != -1:
        # Extracts substring from start until the first comma
        processed_string = input_string[: comma_index + 1]
    else:
        # If no comma is found, returns the original string
        processed_string = input_string

    return processed_string


def remove_after_right_curly(input_string: str) -> str:
    """Removes text from string after the first right-curly '}' character."""
    # Finds the index of the first comma
    curly_index = input_string.find("}")

    if curly_index != -1:
        # Extracts substring from start until the first comma
        processed_string = input_string[: curly_index + 1]
    else:
        # If no comma is found, returns the original string
        processed_string = input_string

    return processed_string


def clean_field_response(input_str: str) -> str:
    """Cleans fields responses from LLM outputs."""
    if is_json_like(input_str):
        return input_str
    clean_str = remove_above_curly(input_str)
    if "}" in clean_str:
        clean_str = remove_after_right_curly(clean_str)
    elif "," in clean_str:
        clean_str = remove_after_comma(clean_str)
    # TODO: Add 'if is_json_like(clean_str):' logic
    return clean_str


def has_json_field(json_str: str, field: str) -> bool:
    """Checks if field str is in JSON-like string."""
    # Checks if the string contains the specified field
    return re.search(rf"\"{field}\"", json_str) is not None


def is_list_string(value: str) -> bool:
    """Check if a string represents a list."""
    return value.startswith("[") and value.endswith("]") or "," in value


def parse_list_string(value: str) -> list:
    """Parse a string representation of a list into an actual list."""
    if value.startswith("[") and value.endswith("]"):
        # Removes the outer square brackets and single quotes
        value = value[1:-1].replace("'", "")
    return [item.strip() for item in value.split(",")]


def preprocess_field(field_value: Union[str, list]) -> Union[str, list]:
    """Preprocess a field value."""
    if isinstance(field_value, str) and is_list_string(field_value):
        return parse_list_string(field_value)
    return field_value


def parse_partial_json(json_str: str, model_class: Type[BaseModel]) -> BaseModel:
    """Parses JSON string and returns in specified Pydantic format."""
    # print(f"FIELD JSON BEFORE: {json_str}")
    preprocessed_json = preprocess_json(json_str)
    # print(f"FIELD JSON AFTER: {preprocessed_json}")
    partial_data = from_json(preprocessed_json, allow_partial=True)

    # Preprocess each field value
    for field_name, field_value in partial_data.items():
        partial_data[field_name] = preprocess_field(field_value)

    # print("\n==============================")
    # print(f"FIELD MODEL VALUE: {partial_data}")
    # print("\n")
    return model_class.model_validate(partial_data)


def get_partial_json(
    json_str: str, model_class: Type[BaseModel]
) -> Optional[BaseModel]:
    """Gets JSON string and returns in specified Pydantic format.

    (Tested on ObjectiveModel)
    """
    try:
        # Removes trailing commas and add closing curly brace if missing
        json_str = re.sub(r",\s*\}", "}", json_str)
        json_str = re.sub(r",\s*$", "}", json_str, flags=re.DOTALL)
        partial_data = json.loads(json_str)
        return model_class(**partial_data)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def remove_slashes(text: str) -> str:
    """Removes /'s (slashes) from strings."""
    return text.replace("\\", "").replace("/", "")


def combine_jsons(json_str_list: list[str], model_class: Type[BaseModel]) -> BaseModel:
    """Combines JSONs into single Pydantic model."""
    models = []
    for json_str in json_str_list:
        if settings.USE_MISTRAL:
            json_str = remove_slashes(json_str)
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

    # Removes any remaining dots (.) outside of quotes
    json_str = re.sub(r'\.(?=(?:[^"]*"[^"]*")*[^"]*$)', "", json_str)

    # Removes any remaining whitespace
    json_str = json_str.strip()
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


def extract_json_objective(input_string: str) -> Optional[str]:
    """Extracts Objective from LLM outputs."""
    input_string = remove_above_curly(input_string)
    input_string = remove_after_comma(input_string)
    normalized_string = re.sub(r"\s+", " ", input_string.replace("\n", " ")).strip()
    cleaned_string = clean_json_str(normalized_string)
    if has_json_field(cleaned_string, field="objective"):
        json_obj = get_partial_json(cleaned_string, ObjectiveModel)
        if json_obj:
            return json_obj.objective
    return None


def format_prompt_mistral(user_prompt: str, system_prompt: str = ""):
    """Formats prompts for Mistral models."""
    if system_prompt.strip():
        return f"[INST] {system_prompt} {user_prompt} [/INST]"
    return f"[INST] {user_prompt} [/INST]"


def extract_objective(prompt: str, client) -> str:
    """Extracts objective definition from the user prompt using LLM."""
    json_prompt = f"""
    <|im_start|>system
    You are a helpful assistant designed to output single JSON fields.
    Given the following user prompt
    << {prompt} >>
    extract the objective definition category that the prompt is most associated with.
    The 'objective' should be one of:
    'CatalogMaintenanceObjective', 'PeriodicRevisitObjective', 'SearchObjective', 'DataEnrichmentObjective', 'SpectralClearingObjective',
    with the following descriptions:
    {cmo_info['example']}: Description: {cmo_info['description']}
    {pro_info['example']}: Description: {pro_info['description']}
    {so_info['example']}: Description: {so_info['description']}
    {deo_info['example']}: Description: {deo_info['description']}
    {sco_info['example']}: Description: {sco_info['description']}
    Examples:
    Input:
    user_prompt: "{cmo_info['prompts'][0]}"
    Result: {{
        "objective": "{cmo_info['example']}",
    }}
    Input:
    user_prompt: "{pro_info['prompts'][0]}"
    Result: {{
        "objective": "{pro_info['example']}",
    }}
    Input:
    user_prompt: "{so_info['prompts'][0]}"
    Result: {{
        "objective": "{so_info['example']}",
    }}
    Input:
    user_prompt: "{deo_info['prompts'][0]}"
    Result: {{
        "objective": "{deo_info['example']}",
    }}
    Input:
    user_prompt: "{sco_info['prompts'][0]}"
    Result: {{
        "objective": "{sco_info['example']}",
    }}
    <|im_end|>

    <|im_start|>user
    Input:
    user_prompt: {prompt}
    <|im_end|>

    <|im_start|>assistant
    Result:
    """
    if settings.USE_MISTRAL:
        system_prompt = f"""You are a helpful assistant designed to output single JSON fields.
    Given the following user prompt
    << {prompt} >>
    extract the objective definition category that the prompt is most associated with.
    The 'objective' should be one of:
    'CatalogMaintenanceObjective', 'PeriodicRevisitObjective', 'SearchObjective', 'DataEnrichmentObjective', 'SpectralClearingObjective',
    with the following descriptions:
    {cmo_info['example']}: Description: {cmo_info['description']}
    {pro_info['example']}: Description: {pro_info['description']}
    {so_info['example']}: Description: {so_info['description']}
    {deo_info['example']}: Description: {deo_info['description']}
    {sco_info['example']}: Description: {sco_info['description']}
    Examples:
    Input:
    user_prompt: "{cmo_info['prompts'][0]}"
    Result: {{
        "objective": "{cmo_info['example']}",
    }}
    Input:
    user_prompt: "{pro_info['prompts'][0]}"
    Result: {{
        "objective": "{pro_info['example']}",
    }}
    Input:
    user_prompt: "{so_info['prompts'][0]}"
    Result: {{
        "objective": "{so_info['example']}",
    }}
    Input:
    user_prompt: "{deo_info['prompts'][0]}"
    Result: {{
        "objective": "{deo_info['example']}",
    }}
    Input:
    user_prompt: "{sco_info['prompts'][0]}"
    Result: {{
        "objective": "{sco_info['example']}",
    }}
    """
        user_prompt = f"""Input:
    user_prompt: {prompt}
    Result:
    """
        json_prompt = format_prompt_mistral(user_prompt, system_prompt)

    t_start = time.perf_counter()
    result = client.generate_text(json_prompt)
    t_end = time.perf_counter()
    print(
        f"extract_objective: client.generate_text took: {t_end - t_start:.4f} seconds"
    )

    if "text" in result:
        return result["text"]
    elif "detail" in result:
        return result["detail"]
    else:
        raise ValueError("Unexpected LLM response format")


def extract_field_from_prompt(
    prompt: str,
    field_name: str,
    field_desc: str,
    example: str,
    obj: str,
    client,
) -> str:
    """Extracts a single field from the user prompt using the LLM."""
    """
    t_start = time.perf_counter()
    json_strs = process_fields(prompt, objective, client)
    t_end = time.perf_counter()
    print(f"process_fields took: {t_end - t_start:.4f} seconds")
    """
    t_start = time.perf_counter()
    obj_info = objectives[obj]
    user_example = obj_info["prompts"][0]
    t_end = time.perf_counter()
    print(f"extract_field_from_prompt (part 1) took: {t_end - t_start:.4f} seconds")

    t_start = time.perf_counter()
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
    t_end = time.perf_counter()
    print(f"extract_field_from_prompt (part 2) took: {t_end - t_start:.4f} seconds")

    t_start = time.perf_counter()

    if settings.USE_MISTRAL:
        system_prompt = f"""You are a helpful assistant designed to output single JSON fields.
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
    """
        user_prompt = f"""Input:
    user_prompt: {prompt}
    Result:
    """
        json_prompt = format_prompt_mistral(user_prompt, system_prompt)
    t_end = time.perf_counter()
    print(f"extract_field_from_prompt (part 3) took: {t_end - t_start:.4f} seconds")

    t_start = time.perf_counter()

    result = client.generate_text(json_prompt)
    t_end = time.perf_counter()
    print(
        f"extract_field_from_prompt - client.generate_text (part 4) took: {t_end - t_start:.4f} seconds"
    )

    if "text" in result:
        return result["text"]
    elif "detail" in result:
        return result["detail"]
    else:
        raise ValueError("Unexpected LLM response format")


def extract_list_from_prompt(
    prompt: str, field_name: str, field_desc: str, client
) -> str:
    """Extracts the time fields from the user prompt using the LLM."""
    list_prompt = "Make an objective with RME01 and LMNT01."
    example = "['RME01', 'LMNT01']"
    field_example = "sensor_name_list"

    list_prompt = f"""
    <|im_start|>system
    You are a helpful assistant designed to output single JSON fields for lists of strings (list[str]).
    Given the following user prompt
    << {prompt} >>
    extract the following time field:
    << {field_name} >> with description: {field_desc} from the user prompt.
    Example:
    Input:
    user_prompt: "{list_prompt}"
    Result: {{
        "{field_example}": "{example}",
    }}
    Note: ONLY respond in JSON.
    <|im_end|>

    <|im_start|>user
    Input:
    user_prompt: {prompt}
    <|im_end|>

    <|im_start|>assistant
    Result:
    """
    if settings.USE_MISTRAL:
        system_prompt = f"""You are a helpful assistant designed to output single JSON fields for lists of strings (list[str]).
    Given the following user prompt
    << {prompt} >>
    extract the following time field:
    << {field_name} >> with description: {field_desc} from the user prompt.
    Example:
    Input:
    user_prompt: "{list_prompt}"
    Result: {{
        "{field_example}": "{example}",
    }}
    Note: ONLY respond in JSON.
    """
        user_prompt = f"""Input:
    user_prompt: {prompt}
    Result:
    """
        list_prompt = format_prompt_mistral(user_prompt, system_prompt)

    result = client.generate_text(list_prompt)
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
    Note: ONLY respond in JSON.
    <|im_end|>

    <|im_start|>user
    Input:
    user_prompt: {prompt}
    <|im_end|>

    <|im_start|>assistant
    Result:
    """
    if settings.USE_MISTRAL:
        system_prompt = f"""You are a helpful assistant designed to output single JSON fields for times.
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
    Note: ONLY respond in JSON.
    """
        user_prompt = f"""Input:
    user_prompt: {prompt}
    Result:
    """
        time_prompt = format_prompt_mistral(user_prompt, system_prompt)

    result = client.generate_text(time_prompt)
    if "text" in result:
        return result["text"]
    elif "detail" in result:
        return result["detail"]
    else:
        raise ValueError("Unexpected LLM response format")


def calculate_filling_percentage(model_instance: BaseModel) -> float:
    """Calculates the percentage of filled fields in Pydantic model."""
    if model_instance is None:
        return 0.0
    
    total_fields = len(model_instance.__fields__)
    filled_fields = sum(
        1 for _, value in model_instance.__dict__.items() if value is not None
    )
    if total_fields == 0:
        return 0.0
    return filled_fields / total_fields


def process_fields(prompt: str, objective: str, client):
    """Extracts all basic str, int , float fields from prompt."""
    """
    t_start = time.perf_counter()
    json_strs = process_fields(prompt, objective, client)
    t_end = time.perf_counter()
    print(f"process_fields took: {t_end - t_start:.4f} seconds")
    """
    t_start = time.perf_counter()
    json_strs = []
    obj_info = objectives[objective]

    fields_and_descriptions = get_model_fields_and_descriptions(obj_info["base_model"])
    t_end = time.perf_counter()
    print(f"process_fields part 1 (setup) took: {t_end - t_start:.4f} seconds")

    max_tries = 3
    if len(obj_info["example_fields"]) != len(fields_and_descriptions):
        raise ValueError("'examples' list must have same length as objective fields.")

    for (field_name, field_desc), example in zip(
        fields_and_descriptions, obj_info["example_fields"]
    ):
        if field_name in ["objective_start_time", "objective_end_time"]:
            continue

        num_tries = 0
        while num_tries < max_tries:
            t_start = time.perf_counter()
            response = extract_field_from_prompt(
                prompt,
                field_name,
                field_desc,
                example=example,
                obj=objective,
                client=client,
            )
            t_end = time.perf_counter()
            print(
                f"process_fields part 2 (extract_field_from_prompt TOTAL) took: {t_end - t_start:.4f} seconds"
            )

            t_start = time.perf_counter()
            cleaned_response = clean_field_response(response)
            if is_json_like(response):
                json_strs.append(response)
                break
            elif is_json_like(cleaned_response):
                json_strs.append(cleaned_response)
                break
            # else:
            #     print("WARNING: MODEL FIELD NOT JSON-LIKE")
            #     print(f"Raw LLM response at attempt={num_tries}: {response}")
            num_tries += 1
            t_end = time.perf_counter()
            print(
                f"process_fields part 3 (end of loop) took: {t_end - t_start:.4f} seconds"
            )
        # else:
        #     logging.warning(
        #         f"Failed to extract field '{field_name}' after {max_tries} attempts."
        #     )

    return json_strs


def process_lists(prompt: str, client):
    """Extracts list[str] fields (rso_id_list, sensor_name_list, etc) from prompt."""
    list_strs = []

    list_model = get_model_fields_and_descriptions(ObjectiveList)
    max_tries = 3
    for field_name, field_desc in list_model:
        num_tries = 0
        while num_tries < max_tries:
            response = extract_list_from_prompt(
                prompt,
                field_name,
                field_desc,
                client=client,
            )

            cleaned_response = clean_field_response(response)
            if is_json_like(response):
                list_strs.append(response)
                break
            elif is_json_like(cleaned_response):
                list_strs.append(cleaned_response)
                break
            # else:
            #     print("WARNING: LIST FIELD NOT JSON-LIKE")
            #     print(f"Raw LLM response at attempt={num_tries}: {response}")
            num_tries += 1
        # else:
        #     logging.warning(
        #         f"Failed to extract time field '{field_name}' after {max_tries} attempts."
        #     )

    return list_strs


def process_times(prompt: str, client):
    """Extracts time fields (objective_start_time, objective_end_time) from prompt."""
    time_strs = []

    time_model = get_model_fields_and_descriptions(ObjectiveTime)

    max_tries = 3
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
            # else:
            #     print("WARNING: TIME FIELD NOT JSON-LIKE")
            #     print(f"Raw LLM response at attempt={num_tries}: {response}")
            num_tries += 1
        # else:
        #     logging.warning(
        #         f"Failed to extract time field '{field_name}' after {max_tries} attempts."
        #     )

    return time_strs


def process_objective(prompt: str, client):
    """Extracts Objective name from a user prompt."""
    # TODO: Use 3 max tries to extract Objective
    t_start = time.perf_counter()
    objective_llm = extract_objective(prompt, client)
    objective = extract_json_objective(objective_llm)
    t_end = time.perf_counter()
    print(f"process_objective (part 1 total): {t_end - t_start:.4f} seconds")
    print(f"EXTRACTED OBJECTIVE: {objective}")

    if objective:
        for objective_name in objectives.keys():
            if objective_name in objective:
                objective = objective_name
    else:
        print("Objective not found. Defaulting to CatalogMaintenanceObjective.")
        objective = "CatalogMaintenanceObjective"  # default

    return objective


def extract_model(
    obj_info: dict, json_strs: list, list_strs: list, time_strs: list
) -> Optional[ObjectiveModel]:
    """Extracts Objective model based on previous field extractions."""
    extracted_model = None
    extracted_list = None
    extracted_time = None

    if json_strs:
        extracted_model = combine_jsons(json_strs, obj_info["template"])
    else:
        json_strs = ["JSON Parsing Failed!"]

    if list_strs:
        extracted_list = combine_jsons(list_strs, ObjectiveListTemplate)
    else:
        list_strs = ["LIST Parsing Failed!"]

    if time_strs:
        extracted_time = combine_jsons(time_strs, ObjectiveTimeTemplate)
    else:
        time_strs = ["TIME Parsing Failed!"]

    if extracted_model is None:
        return None

    model_fields = get_model_fields_and_descriptions(obj_info["template"])
    for field_name, _ in model_fields:
        if field_name == "rso_id_list":
            extracted_model.rso_id_list = getattr(extracted_list, "rso_id_list", [])
        elif field_name == "sensor_name_list":
            extracted_model.sensor_name_list = getattr(
                extracted_list, "sensor_name_list", []
            )
        elif field_name == "target_id_list":
            extracted_model.target_id_list = getattr(
                extracted_list, "target_id_list", []
            )
        elif field_name == "objective_start_time":
            extracted_model.objective_start_time = getattr(
                extracted_time, "objective_start_time", "None"
            )
        elif field_name == "objective_end_time":
            extracted_model.objective_end_time = getattr(
                extracted_time, "objective_end_time", "None"
            )

    return extracted_model
