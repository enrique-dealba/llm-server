import logging
import time
from typing import Callable, Dict, List

from dotenv import load_dotenv

from client import Client
from text_processing import TextProcessing as tp
from tools.router_tools import get_lat_long, get_time

# Loads environment variables
load_dotenv()


class FunctionTest:
    """Class that encapsulates a function call its prompts."""

    function: Callable
    prompts: List[str]
    targets: List[str]

    def __init__(self, function: Callable, prompts: List[str], targets: List[str]):
        """Initializes the FunctionTest instance."""
        self.function = function
        assert len(prompts) == len(targets)
        self.prompts = prompts
        self.targets = targets


def check_response(response, expected):
    """Boolean logic to check if function call response is coorect."""
    check = bool(str(expected) in str(response) or str(response) in str(expected))
    double_check = bool(
        str(expected) in str(response)[1:-1] or str(response)[1:-1] in str(expected)
    )
    return check or double_check


def function_call(
    fn_test: FunctionTest, stats: dict, num_tests: int = 20
) -> Dict[str, float]:
    """Runs a series of prompts through the LLM router and benchmarks function call."""
    total_tps = 0.0
    total_time = 0.0
    total_correct = 0.0
    successful_requests = 0.0
    total_requests = 0.0

    for i in range(num_tests):
        for idx in range(len(fn_test.prompts)):
            prompt = fn_test.prompts[idx]
            response = None
            try:
                t_0 = time.perf_counter()
                response = Client.generate_text(prompt)
                t_1 = time.perf_counter()
            except Exception as e:
                logging.error(f"LLM failed to generate text: {e}")

            if response and "text" in response:
                # TODO: More elegant way to check str type
                response = str(response["text"])
                elapsed_time = t_1 - t_0
                tps = tp.measure_performance(t_0, t_1, response)
                total_tps += tps
                total_time += elapsed_time
                successful_requests += 1
                total_requests += 1

                response = tp.clean_mistral(response)  # TODO: Maybe remove this

                target = fn_test.targets[idx]
                expected_response = fn_test.function(target)
                correct = check_response(response, expected_response)
                total_correct += int(correct)  # Adds 1 if correct

                if i == 0:  # We only print these out during first iter.
                    print(f"Prompt: {prompt}")
                    print(f"Response: {response}")
                    print(f"Actual: {expected_response}")
                    print(f"Check: {correct}")
                    print(f"TPS: {tps:.2f}\n")
            else:
                total_requests += 1
                print(f"\nFailed to get response for prompt: {prompt}")

    stats["total_tps"] += total_tps
    stats["total_time"] += total_time
    stats["total_correct"] += total_correct
    stats["successful_requests"] += successful_requests
    stats["total_requests"] += total_requests

    return stats


if __name__ == "__main__":
    stats = {
        "total_tps": 0.0,
        "total_time": 0.0,
        "total_correct": 0.0,
        "successful_requests": 0.0,
        "total_requests": 0.0,
    }

    get_time_prompts = [
        "What's the time in rome?",
        "What is the current time in new york?",
    ]

    get_time_targets = [
        "Europe/Rome",
        "America/New_York",
    ]

    get_time_test = FunctionTest(
        function=get_time, prompts=get_time_prompts, targets=get_time_targets
    )

    get_lat_long_prompts = [
        "What's the latitude and longitude of Dallas, TX?",
        "What's the latitude and longitude of Paris?",
    ]

    get_lat_long_targets = [
        "Dallas, Texas",
        "Paris, France",
    ]

    get_lat_long_test = FunctionTest(
        function=get_lat_long,
        prompts=get_lat_long_prompts,
        targets=get_lat_long_targets,
    )

    stats = function_call(get_time_test, stats=stats)
    stats = function_call(get_lat_long_test, stats=stats)

    num_requests = stats["successful_requests"]

    print(f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}")
    print(f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}")
    print(f"Avg Correct Answers: {stats['total_correct']/stats['total_requests']:.2f}")
    print(f"Total Correct Answers: {stats['total_correct']:.2f}")
