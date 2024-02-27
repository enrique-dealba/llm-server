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
        """Initializes the RouteModel instance."""
        self.function = function
        assert len(prompts) == len(targets)
        self.prompts = prompts
        self.targets = targets


def function_call(fn_test: FunctionTest, num_tests: int = 20) -> Dict[str, float]:
    """Runs a series of prompts through the LLM router and benchmarks function call."""
    total_tps = 0.0
    total_time = 0.0
    total_correct = 0.0
    successful_requests = 0.0
    total_requests = 0.0

    for i in range(num_tests):
        for idx in range(len(fn_test.prompts)):
            prompt = fn_test.prompts[idx]
            t_0 = time.perf_counter()
            response = Client.generate_text(prompt)
            t_1 = time.perf_counter()

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
                check = bool(
                    str(expected_response) in str(response)
                    or str(response) in str(expected_response)
                )
                double_check = bool(
                    str(expected_response) in str(response)[1:-1]
                    or str(response)[1:-1] in str(expected_response)
                )
                total_correct += int(check or double_check)  # Adds 1 if correct

                if i == 0:  # We only print these out during first iter.
                    print(f"Prompt: {prompt}")
                    print(f"Response: {response}")
                    print(f"Actual: {expected_response}")
                    print(f"Check: {check}\n")
                    print(f"TPS: {tps:.2f}")
            else:
                total_requests += 1
                print(f"Failed to get response for prompt: {prompt}")

    stats = {}
    if successful_requests > 0:
        stats = {
            "avg_tps": total_tps / successful_requests,
            "avg_time": total_time / successful_requests,
            "avg_correct": total_correct / total_requests,
            "total_correct": total_correct,
        }

    return stats


if __name__ == "__main__":
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

    stats = function_call(get_lat_long_test)
    print(f"Average Tokens per Second (TPS): {stats['avg_tps']:.2f}")
    print(f"Average Total Time Elapsed Per Response: {stats['avg_time']:.2f}")
    print(f"Average Correct Answers: {stats['avg_correct']:.2f}")
    print(f"Total Correct Answers: {stats['total_correct']:.2f}")
