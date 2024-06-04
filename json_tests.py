import argparse
import json
import logging
import time
from typing import Dict, Type

from pydantic import BaseModel

from client import Client, process_prompt
from templates import (
    CatalogMaintenanceObjectiveTemplate,
    DataEnrichmentObjectiveTemplate,
    PeriodicRevisitObjectiveTemplate,
    SearchObjectiveTemplate,
    SpectralClearingObjectiveTemplate,
)
from utils import calculate_matching_percentage


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
    schema_classes: dict[str, Type[BaseModel]], schemas_data: list[dict]
) -> list[BaseModel]:
    """Load schemas from a list of dictionaries."""
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
            print(f"Invalid schema data type: {type(schema_data)}. Expected dict.")
    return loaded_schemas


def function_call(
    stats: Dict,
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

    for _ in range(num_tests):
        for prompt, schema in zip(prompts, schemas):
            try:
                t_0 = time.perf_counter()

                response, extracted_model, _, pred_obj = process_prompt(prompt, client)
                correctness = calculate_matching_percentage(extracted_model, schema)

                t_1 = time.perf_counter()

                if response:
                    elapsed_time = t_1 - t_0
                    total_time += elapsed_time
                    successful_requests += 1
                    total_requests += 1
                    total_correctness += correctness
                    # Checks if predicted objective matches ground truth
                    if pred_obj == objective or objective in pred_obj:
                        obj_correctness += 1

            except Exception as e:
                logging.error(f"Error processing prompt: {e}")
                total_requests += 1

    stats["total_correctness"] += total_correctness
    stats["obj_correctness"] += obj_correctness
    stats["total_time"] += total_time
    stats["successful_requests"] += successful_requests
    stats["total_requests"] += total_requests
    return stats


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
        prompts = json.loads(args.prompts)
        objective = args.objective
        schemas = load_schemas(schema_classes, args.schemas)

        t_0 = time.perf_counter()

        stats = function_call(
            stats=stats,
            prompts=prompts,
            objective=objective,
            schemas=schemas,
            num_tests=2,
        )

        t_1 = time.perf_counter()

        num_requests = stats["successful_requests"]
        if num_requests <= 0:
            num_requests = 1

        print(f"Avg Model Correctness: {stats['total_correctness']/num_requests:.2%}")
        print(f"Avg Objective Correctness: {stats['obj_correctness']/num_requests:.2%}")
        print(f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}")
        print(f"\nTotal Benchmarking Time: {t_1 - t_0}")

    except ValueError as e:
        logging.error(f"Error loading schemas: {e}")
