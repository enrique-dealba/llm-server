import time
from typing import Callable, Dict, List

from dotenv import load_dotenv

from client import Client
from text_processing import TextProcessing as tp
from tools.tools import get_time

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


def function_call(fn_test: FunctionTest) -> Dict[str, float]:
    """Runs a series of prompts through the LLM router and benchmarks function call."""
    total_tps = 0.0
    total_time = 0.0
    successful_requests = 0.0

    for idx in range(len(fn_test.prompts)):
        prompt = fn_test.prompts[idx]
        t_0 = time.perf_counter()
        response = Client.generate_text(prompt)["text"]
        t_1 = time.perf_counter()

        if response:
            elapsed_time = t_1 - t_0
            tps = tp.measure_performance(t_0, t_1, response)
            total_tps += tps
            total_time += elapsed_time
            successful_requests += 1
            print(f"Prompt: {prompt}\nTPS: {tps:.2f}\n")

            response = tp.clean_mistral(response)  # TODO: Maybe remove this

            print(f"\nResponse: {response}\n")
            target = fn_test.targets[idx]
            expected_response = fn_test.function(target)
            print(f"\nActual: {expected_response}\n")
            check = bool(target in response)
            print(f"\nCheck: {check}\n")
        else:
            print(f"Failed to get response for prompt: {prompt}")

    stats = {}
    if successful_requests > 0:
        stats = {
            "avg_tps": total_tps / successful_requests,
            "avg_time": total_time / successful_requests,
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

    stats = function_call(get_time_test)
    print(f"Average Tokens per Second (TPS): {stats['avg_tps']:.2f}")
    print(f"Average Total Time Elapsed Per Response: {stats['avg_time']:.2f}")
