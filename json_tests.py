import argparse
import json
import logging
import time
from typing import Dict

from client import Client, process_prompt


def function_call(
    stats: Dict, prompts: list, objective: str, num_tests: int = 3
) -> Dict[str, float]:
    """Runs a series of prompts through the LLM router and benchmarks correctness."""
    client = Client()

    total_correctness = 0.0
    obj_correctness = 0.0
    total_time = 0.0
    successful_requests = 0.0
    total_requests = 0.0

    for _ in range(num_tests):
        for prompt in prompts:
            try:
                t_0 = time.perf_counter()
                response, _, correctness, pred_obj = process_prompt(prompt, client)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=str, required=True)
    parser.add_argument("--objective", type=str, required=True)
    args = parser.parse_args()

    prompts = json.loads(args.prompts)
    objective = json.loads(args.objective)

    stats = {
        "total_correctness": 0.0,
        "obj_correctness": 0.0,
        "total_time": 0.0,
        "successful_requests": 0.0,
        "total_requests": 0.0,
    }

    t_0 = time.perf_counter()

    stats = function_call(
        stats=stats, prompts=prompts, objective=objective, num_tests=10
    )

    t_1 = time.perf_counter()
    total_time = t_1 - t_0

    num_requests = stats["successful_requests"]
    if num_requests <= 0:
        num_requests = 1

    print(f"Avg Model Correctness: {stats['total_correctness']/num_requests:.2%}")
    print(f"Avg Objective Correctness: {stats['obj_correctness']/num_requests:.2%}")
    print(f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}")
    print(f"\nTotal Benchmarking Time: {total_time}")
