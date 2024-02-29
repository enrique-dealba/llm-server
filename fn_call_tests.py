import logging
import time
from typing import Callable, Dict, List

from dotenv import load_dotenv

from client import Client
from text_processing import TextProcessing as tp
from tools.router_tools import (
    capitalize_first_letter,
    compress_whitespace,
    convert_to_binary,
    convert_to_uppercase,
    count_words,
    divide_by_2,
    extract_domain,
    format_phone_number,
    generate_acronym,
    get_ascii_value,
    get_day_of_week,
    get_last_letter,
    get_lat_long,
    get_time,
    get_vowel_count,
    reverse_string,
)

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
    len_check = abs(len(response) - len(expected)) <= 5  # True if within 5 chars
    return (check or double_check) and len_check


def function_call(
    fn_test: FunctionTest, stats: dict, num_tests: int = 3
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
        t_response = fn_test.function(target)  # TODO: try/except here?
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
            "what's the time in Panama",
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
            "what is the latitude of Moscow",
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
            "what is the last letter of This_is_a_long_word?",
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
            "what is 999 divided by 2?",
            "What's 999999999 divided by 2?",
        ],
        targets=[
            "6",
            "100",
            "76",
            "999",
            "999999999",
        ],
    )

    get_day_of_week_test = FunctionTest(
        function=get_day_of_week,
        prompts=[
            "What day was it on 2018-03-14?",
            "Tell me the day of the week for 2024-01-01",
            "What's the weekday for 2017-09-10?",
            "Find the weekday on 2025-12-31",
            "The day of the week for 2019-04-20?",
        ],
        targets=[
            "2018-03-14",
            "2024-01-01",
            "2017-09-10",
            "2025-12-31",
            "2019-04-20",
        ],
    )

    format_phone_number_test = FunctionTest(
        function=format_phone_number,
        prompts=[
            "Can you format 2468101214?",
            "Make 1357911131 into a phone number",
            "How to write 9080706050 as a phone number?",
            "Format 3213214321 as a phone number",
            "Turn 7539514567 into a readable number",
        ],
        targets=[
            "2468101214",
            "1357911131",
            "9080706050",
            "3213214321",
            "7539514567",
        ],
    )

    compress_whitespace_test = FunctionTest(
        function=compress_whitespace,
        prompts=[
            "Clean up spacing in 'too   many    spaces'",
            "Compress all the spaces in 'spaces   everywhere'",
            "Turn multiple spaces into a single space in 'single    space   please'",
            "How to reduce 'lots    of   spaces' effectively?",
            "Remove extra whitespaces from 'whitespace     reduction'",
        ],
        targets=[
            "too   many    spaces",
            "spaces   everywhere",
            "single    space   please",
            "lots    of   spaces",
            "whitespace     reduction",
        ],
    )

    capitalize_first_letter_test = FunctionTest(
        function=capitalize_first_letter,
        prompts=[
            "Capitalize the first letter of 'capitalize me'",
            "Make the initial letter big in 'small to big'",
            "Start 'sentence with uppercase'",
            "First letter uppercase in 'lower to upper'",
            "Capitalize 'beginning'",
        ],
        targets=[
            "capitalize me",
            "small to big",
            "sentence with uppercase",
            "lower to upper",
            "beginning",
        ],
    )

    reverse_string_test = FunctionTest(
        function=reverse_string,
        prompts=[
            "Reverse the string 'reverse'",
            "Flip 'backwards' to its opposite",
            "How to reverse 'mirror'",
            "Turn '123abc' around",
            "Write 'hello' in reverse",
        ],
        targets=[
            "reverse",
            "backwards",
            "mirror",
            "123abc",
            "hello",
        ],
    )

    generate_acronym_test = FunctionTest(
        function=generate_acronym,
        prompts=[
            "Acronym for 'Graphics Interchange Format'",
            "Short form of 'Portable Network Graphics'",
            "Create an acronym from 'Wireless Fidelity'",
            "What's the acronym for 'Read Only Memory'?",
            "Generate an acronym for 'Global Positioning System'",
        ],
        targets=[
            "Graphics Interchange Format",
            "Portable Network Graphics",
            "Wireless Fidelity",
            "Read Only Memory",
            "Global Positioning System",
        ],
    )

    get_vowel_count_test = FunctionTest(
        function=get_vowel_count,
        prompts=[
            "How many vowels in 'quick brown fox'?",
            "Count the vowels in 'lazy dog'",
            "Number of vowels in 'jumped over'",
            "Vowel count for 'the lazy moon'",
            "Tell me how many vowels are in 'bright sunny day'",
        ],
        targets=[
            "quick brown fox",
            "lazy dog",
            "jumped over",
            "the lazy moon",
            "bright sunny day",
        ],
    )

    convert_to_binary_test = FunctionTest(
        function=convert_to_binary,
        prompts=[
            "Convert '10' to binary",
            "Binary version of 64",
            "What is 100 in binary?",
            "Show 32 as a binary number",
            "How to write '128' in binary?",
        ],
        targets=[
            "10",
            "64",
            "100",
            "32",
            "128",
        ],
    )

    get_ascii_value_test = FunctionTest(
        function=get_ascii_value,
        prompts=[
            "ASCII value of 'b'",
            "What's the ASCII for 'Z'?",
            "Find ASCII number for '@'",
            "ASCII code for '9'",
            "Get me the ASCII of '#'",
        ],
        targets=[
            "b",
            "Z",
            "@",
            "9",
            "#",
        ],
    )

    extract_domain_test = FunctionTest(
        function=extract_domain,
        prompts=[
            "Domain name of 'https://api.example.com/data'",
            "Extract domain from 'http://blog.example.net/read'",
            "What's the domain in 'https://store.example-shop.com/product'",
            "Find the domain of 'www.example-portal.com'",
            "Get the domain from 'https://news.example-news.co/info'",
        ],
        targets=[
            "https://api.example.com/data",
            "http://blog.example.net/read",
            "https://store.example-shop.com/product",
            "www.example-portal.com",
            "https://news.example-news.co/info",
        ],
    )

    count_words_test = FunctionTest(
        function=count_words,
        prompts=[
            "How many words in 'Quick test of words'?",
            "Count words in 'Another, example.'",
            "Word count for 'Word'",
            "Tell me the number of words in 'Three word sentence.'",
            "How many words are there in 'Four words here indeed'?",
        ],
        targets=[
            "Quick test of words",
            "Another, example.",
            "Word",
            "Three word sentence.",
            "Four words here indeed",
        ],
    )

    convert_to_uppercase_test = FunctionTest(
        function=convert_to_uppercase,
        prompts=[
            "Make 'simple text' all uppercase",
            "Uppercase 'Mixed Input Case'",
            "Convert 'varied cases of letters' to all caps",
            "Change 'Another Test' to all uppercase",
            "Transform 'yet another lowercase' into UPPERCASE",
        ],
        targets=[
            "simple text",
            "Mixed Input Case",
            "varied cases of letters",
            "Another Test",
            "yet another lowercase",
        ],
    )

    t_0 = time.perf_counter()

    """
    tools = [
    time_route,
    lat_long_route,
    last_letter_route,
    divide_two_route,
    get_day_of_week_route,
    format_phone_number_route,
    compress_whitespace_route,
    capitalize_first_letter_route,
    reverse_string_route,
    generate_acronym_route,
    get_vowel_count_route,
    convert_to_binary_route,
    get_ascii_value_route,
    extract_domain_route,
    count_words_route,
    convert_to_uppercase_route,
    ]
    """

    stats = function_call(get_time_test, stats=stats)
    stats = function_call(get_lat_long_test, stats=stats)
    stats = function_call(get_last_letter_test, stats=stats)
    stats = function_call(divide_by_two_test, stats=stats)
    stats = function_call(get_day_of_week_test, stats=stats)
    stats = function_call(format_phone_number_test, stats=stats)
    stats = function_call(compress_whitespace_test, stats=stats)
    stats = function_call(capitalize_first_letter_test, stats=stats)
    stats = function_call(reverse_string_test, stats=stats)
    stats = function_call(generate_acronym_test, stats=stats)
    stats = function_call(get_vowel_count_test, stats=stats)
    stats = function_call(convert_to_binary_test, stats=stats)
    stats = function_call(get_ascii_value_test, stats=stats)
    stats = function_call(extract_domain_test, stats=stats)
    stats = function_call(count_words_test, stats=stats)
    stats = function_call(convert_to_uppercase_test, stats=stats)

    t_1 = time.perf_counter()
    total_time = t_1 - t_0

    num_requests = stats["successful_requests"]

    print(f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}")
    print(f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}")
    print(f"Avg Correct Answers: {stats['total_correct']/stats['total_requests']:.2f}")
    print(f"Total Correct Answers: {stats['total_correct']:.2f}")
    print(f"\nTotal Benchmarking Time: {total_time}")
