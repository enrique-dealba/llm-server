import argparse
import json
import logging
import time
from typing import Dict, Type, Optional, Tuple, Any

from pydantic import BaseModel

from client import Client, process_prompt
from templates import (
    CatalogMaintenanceObjectiveTemplate,
    DataEnrichmentObjectiveTemplate,
    PeriodicRevisitObjectiveTemplate,
    SearchObjectiveTemplate,
    SpectralClearingObjectiveTemplate,
)
from utils import calculate_matching_percentage, calculate_matching_percentage_info, model_to_json


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run JSON tests")
    parser.add_argument(
        "--prompts", type=str, required=True, help="JSON string of prompts"
    )
    parser.add_argument("--objective", type=str, required=True, help="Objective string")
    parser.add_argument(
        "--schemas", type=str, required=True, help="JSON string of schemas"
    )
    return parser.parse_args()


def load_schemas(
    schema_classes: dict[str, Type[BaseModel]], schemas_data: list[dict[str, Any]]
) -> list[BaseModel]:
    """Load schemas from a list of schema data."""
    loaded_schemas = []
    for schema_data in schemas_data:
        if isinstance(schema_data, dict):
            matching_classes = [
                cls
                for cls in schema_classes.values()
                if set(cls.__fields__.keys()) == set(schema_data.keys())
            ]
            if len(matching_classes) == 1:
                model_class = matching_classes[0]
                loaded_schemas.append(model_class(**schema_data))
            else:
                print(f"No matching class found for schema: {schema_data}")
        else:
            print(
                f"Invalid schema data type: {type(schema_data)}. Expected dict."
            )
    return loaded_schemas


def function_call(
    stats: Dict[str, float],
    prompts: list[str],
    objective: str,
    schemas: list[BaseModel],
    num_tests: int = 3,
) -> Dict[str, float]:
    """Runs a series of prompts through the LLM router and benchmarks correctness."""
    client = Client()

    total_correctness = 0.0
    obj_correctness = 0.0
    total_time = 0.0
    successful_requests = 0.0
    total_requests = 0.0

    field_stats = {}

    for _ in range(num_tests):
        for prompt, schema in zip(prompts, schemas):
            try:
                t_0 = time.perf_counter()

                response, extracted_model, _, pred_obj = process_prompt(prompt, client)

                if response is None:
                    print(f"Empty response for prompt: {prompt}")
                    total_requests += 1
                    continue

                # model_json = model_to_json(extracted_model)
                # print("LLM Prediction:")
                # print(f"\n{pred_obj}: {model_json}")
                # print(" ")
                # print("vs.")
                # print(" ")
                # print("Expected Ground Truth:")
                # expected_json = model_to_json(schema)
                # print(f"\n{objective}: {expected_json}")
                # print(" ")


                # correctness = calculate_matching_percentage(extracted_model, schema)
                correctness, stats_dict = calculate_matching_percentage_info(extracted_model, schema)

                # Accumulate field-level stats
                for field_name, value in stats_dict.items():
                    if field_name not in field_stats:
                        field_stats[field_name] = []
                    field_stats[field_name].append(value)

                t_1 = time.perf_counter()

                elapsed_time = t_1 - t_0
                total_time += elapsed_time
                successful_requests += 1
                total_requests += 1
                total_correctness += correctness
                # Checks if predicted objective matches ground truth
                if pred_obj == objective or objective in pred_obj:
                    obj_correctness += 1

                # print(f"% GT Matching Fields: {correctness:.2%}")  # Debug print
                # print(f"Elapsed Time: {elapsed_time} seconds")  # Debug print
                # print("=" * 30)  # Debug print

            except Exception as e:
                logging.error(f"Error processing prompt: {prompt}. {str(e)}")
                total_requests += 1

    # Calculate average field-level stats
    avg_field_stats = {}
    for field_name, values in field_stats.items():
        avg_field_stats[field_name] = sum(values) / len(values)

    stats["total_correctness"] += total_correctness
    stats["obj_correctness"] += obj_correctness
    stats["total_time"] += total_time
    stats["successful_requests"] += successful_requests
    stats["total_requests"] += total_requests
    return stats, avg_field_stats


if __name__ == "__main__":
    args = parse_arguments()

    prompts = json.loads(args.prompts)
    objective = json.loads(args.objective)

    schema_classes = {
        "CatalogMaintenanceObjective": CatalogMaintenanceObjectiveTemplate,
        "PeriodicRevisitObjective": PeriodicRevisitObjectiveTemplate,
        "SearchObjective": SearchObjectiveTemplate,
        "DataEnrichmentObjective": DataEnrichmentObjectiveTemplate,
        "SpectralClearingObjective": SpectralClearingObjectiveTemplate,
    }

    schemas_data = json.loads(args.schemas)
    schemas = load_schemas(schema_classes, schemas_data)

    stats = {
        "total_correctness": 0.0,
        "obj_correctness": 0.0,
        "total_time": 0.0,
        "successful_requests": 0.0,
        "total_requests": 0.0,
    }

    try:
        t_0 = time.perf_counter()

        stats, avg_field_stats = function_call(
            stats=stats,
            prompts=prompts,
            objective=objective,
            schemas=schemas,
            num_tests=3,
        )

        t_1 = time.perf_counter()

        num_requests = stats["successful_requests"]
        if num_requests <= 0:
            num_requests = 1

        print(f"Avg GT Correctness: {stats['total_correctness'] / num_requests:.2%}")
        print(f"Avg Objective Correctness: {stats['obj_correctness'] / num_requests:.2%}")
        # Print the avg_field_stats dictionary
        print("Average Field-Level Stats:")
        for field_name, avg_value in avg_field_stats.items():
            print(f"  {field_name}: {avg_value:.2f}")
        print(f"Avg Time Elapsed Per Response: {stats['total_time'] / num_requests:.2f}")
        print(f"\nTotal Benchmarking Time: {t_1 - t_0}")

    except Exception as e:
        logging.error(f"Error during benchmarking: {str(e)}")
