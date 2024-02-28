import logging
import time
from typing import Callable, Dict, List

from dotenv import load_dotenv

from client import Client
from text_processing import TextProcessing as tp
from tools.router_tools import divide_by_2, get_last_letter, get_lat_long, get_time

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
    if len(str(response)) >= 2:
        double_check = bool(
            str(expected) in str(response)[1:-1] or str(response)[1:-1] in str(expected)
        )
    else:
        double_check = False
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

    expected_responses = []
    for idx in range(len(fn_test.targets)):
        target = fn_test.targets[idx]
        t_response = fn_test.function(target) # TODO: try/except here?
        expected_responses.append(t_response)

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

                expected_response = expected_responses[idx]
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

    get_time_test = FunctionTest(
        function=get_time,
        prompts=[
            "What's the time in rome?",
            "What is the current time in new york?",
            "What's the time in Seoul?",
            "what is the current time in kuwait?",
            "what's the time in Panama"
        ],
        targets=[
            "Europe/Rome",
            "America/New_York",
            "Asia/Seoul",
            "Asia/Kuwait",
            "America/Panama",
        ],
    )

    get_lat_long_test = FunctionTest(
        function=get_lat_long,
        prompts=[
            "What's the latitude and longitude of Dallas, TX?",
            "What's the latitude and longitude of Paris?",
            "What is the latitude and longitude of Socorro NM?",
            "What is the longitude of London?",
            "what is the latitude of Moscow"
        ],
        targets=[
            "Dallas, Texas",
            "Paris, France",
            "Socorro, New Mexico",
            "London",
            "Moscow, Russia",
        ],
    )

    get_last_letter_test = FunctionTest(
        function=get_last_letter,
        prompts=[
            "What's the last letter in Texas?",
            "What is the last letter of Diamond?",
            "what's the last letter of ABABAB",
            "what is the last letter of 'This_is_a_long_word'?",
            "what is the last letter of This_is_a_long_word?"
        ],
        targets=[
            "Texas",
            "Diamond",
            "ABABAB",
            "This_is_a_long_word",
            "This_is_a_long_word",
        ],
    )

    divide_by_two_test = FunctionTest(
        function=divide_by_2,
        prompts=[
            "What's 6 divided by 2?",
            "What is 100 divided by 2?",
            "what's half of 76?",
            "what is 999 divided by 2?"
            "What's 999999999 divided by 2?"
        ],
        targets=[
            "6",
            "100",
            "76",
            "999",
            "999999999",
        ],
    )

    t_0 = time.perf_counter()
    stats = function_call(get_time_test, stats=stats)
    stats = function_call(get_lat_long_test, stats=stats)
    stats = function_call(get_last_letter_test, stats=stats)
    stats = function_call(divide_by_two_test, stats=stats)
    t_1 = time.perf_counter()
    total_time = t_1 - t_0

    num_requests = stats["successful_requests"]

    print(f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}")
    print(f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}")
    print(f"Avg Correct Answers: {stats['total_correct']/stats['total_requests']:.2f}")
    print(f"Total Correct Answers: {stats['total_correct']:.2f}")
    print(f"\nTotal Benchmarking Time: {total_time}")
