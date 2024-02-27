import time
from typing import Dict, List

from dotenv import load_dotenv

from client import Client
from config import DEFAULT_MODEL
from text_processing import TextProcessing as tp

# Loads environment variables
load_dotenv()


def benchmark_prompts(prompts: List[str]) -> Dict[str, float]:
    """Runs a series of prompts through the LLM and benchmarks response speed."""
    total_tps = 0.0
    total_time = 0.0
    successful_requests = 0.0

    for prompt in prompts:
        t_0 = time.perf_counter()
        response = Client.generate_text(prompt)
        t_1 = time.perf_counter()

        if response and "text" in response:
            response = response["text"]
            elapsed_time = t_1 - t_0
            tps = tp.measure_performance(t_0, t_1, response)
            total_tps += tps
            total_time += elapsed_time
            successful_requests += 1
            print(f"Prompt: {prompt}\nTPS: {tps:.2f}\n")

            response = tp.clean_mistral(response)

            print(f"\nResponse: {response}\n")
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
    prompts = [
        "What is the square root of 1024?",
        "Explain the theory of relativity in the style of a pirate",
        "Write python code for radix sort with comments",
        "Write two Haikus about kubernetes: one arguing for and one against",
        "Write python Skyfield code to find the distance between Earth and Mars. Code:",
        "What is the number that rhymes with the word tree?",
        "Who killed George Washington?",
        (
            "If I hang 5 shirts outside and it takes them 5 hours to dry, "
            "how long would it take to dry 30 shirts?"
        ),
        "Write a sentence where every word starts with the letter a",
        "Explain how to break into a car",
        (
            "Bob is 30 years old, lives in California, and works as an engineer. "
            "Write a JSON for Bob"
        ),
    ]

    stats = benchmark_prompts(prompts)
    print(f"Average Tokens per Second (TPS): {stats['avg_tps']:.2f}")
    print(f"Average Total Time Elapsed Per Response: {stats['avg_time']:.2f}")
