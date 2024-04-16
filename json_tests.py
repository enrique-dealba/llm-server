import argparse
import json
import logging
import os
import time
from typing import Dict

from client import Client
from text_processing import TextProcessing as tp


def check_response(response: str) -> bool:
    """Boolean logic to check if string text can be json parsed."""
    try:
        json.loads(response)
        return True
    except json.JSONDecodeError:
        return False


parser = argparse.ArgumentParser()
parser.add_argument("--prompts", type=str, required=True)
args = parser.parse_args()

prompts = json.loads(args.prompts)


def function_call(stats: dict, num_tests: int = 10) -> Dict[str, float]:
    """Runs a series of prompts through the LLM router and benchmarks json parsing."""
    total_tps = 0.0
    total_time = 0.0
    total_correct = 0.0
    successful_requests = 0.0
    total_requests = 0.0

    for _ in range(num_tests):
        for idx in range(len(prompts)):
            prompt = prompts[idx]
            response = None

            try:
                t_0 = time.perf_counter()
                response = Client.generate_text(prompt)
                t_1 = time.perf_counter()
            except Exception as e:
                logging.error(f"LLM failed to generate text: {e}")

            print(f"Raw Response: {response}")

            if response and "text" in response:
                # TODO: More elegant way to check str type
                response = str(response["text"])
                elapsed_time = t_1 - t_0
                tps = tp.measure_performance(t_0, t_1, response)
                total_tps += tps
                total_time += elapsed_time
                successful_requests += 1
                total_requests += 1

                # response = tp.clean_mistral(response)  # TODO: Maybe remove this

                correct = check_response(response)
                total_correct += int(correct)  # Adds 1 if correct

                # if i == 0:  # We only print these out during first iter.
                # print(f"Prompt: {prompt}")
                # print(f"Response: {response}")
                # print(f"Actual: {expected_response}")
                # print(f"Check: {correct}")
                # print(f"TPS: {tps:.2f}\n")
            else:
                total_requests += 1
                print(f"\nFailed to get response for prompt: {prompt}")

    stats["total_tps"] += total_tps
    stats["total_time"] += total_time
    stats["total_correct"] += total_correct
    stats["successful_requests"] += successful_requests
    stats["total_requests"] += total_requests

    return stats


# def run_experiment_tests(stats, experiment_tests):
#     """Runs experiment tests for a given list of route tests."""
#     t_0 = time.perf_counter()

#     for test_name in experiment_tests:
#         test_function = test_functions_mapping.get(test_name)
#         if test_function:
#             stats = function_call(test_function, stats=stats)
#         else:
#             print(f"Test function {test_name} not found.")

#     t_1 = time.perf_counter()
#     total_time = t_1 - t_0

#     num_requests = stats["successful_requests"]
#     if num_requests <= 0:
#         num_requests = 1

#     print(f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}")
#     print(f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}")
#     print(f"Avg Correct Answers: {stats['total_correct']/stats['total_requests']:.2f}")
#     print(f"Total Correct Answers: {stats['total_correct']:.2f}")
#     print(f"\nTotal Benchmarking Time: {total_time}")

#     with open("fn_call_tests_output.log", "a") as log_file:
#         json.dump(stats, log_file)
#         log_file.write("\n")  # Add a newline to separate entries


# if __name__ == "__main__":
#     experiment_tests_str = os.getenv("EXPERIMENT_TESTS")
#     if experiment_tests_str:
#         experiment_tests = experiment_tests_str.split(",")

#         stats = {
#             "total_tps": 0.0,
#             "total_time": 0.0,
#             "total_correct": 0.0,
#             "successful_requests": 0.0,
#             "total_requests": 0.0,
#         }
#         run_experiment_tests(stats, experiment_tests)
#     else:
#         print("EXPERIMENT_TESTS environment variable not found.")

if __name__ == "__main__":
    stats = {
            "total_tps": 0.0,
            "total_time": 0.0,
            "total_correct": 0.0,
            "successful_requests": 0.0,
            "total_requests": 0.0,
    }

    t_0 = time.perf_counter()

    stats = function_call(stats=stats, num_tests=3)

    t_1 = time.perf_counter()
    total_time = t_1 - t_0

    num_requests = stats["successful_requests"]
    if num_requests <= 0:
        num_requests = 1

    print(f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}")
    print(f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}")
    print(
        f"Avg Correct Answers: {stats['total_correct']/stats['total_requests']:.2f}"
    )
    print(f"Total Correct Answers: {stats['total_correct']:.2f}")
    print(f"\nTotal Benchmarking Time: {total_time}")
