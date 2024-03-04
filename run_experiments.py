import datetime
import random
import subprocess
import time

from fn_call_tests import (
    capitalize_first_letter_test,
    compress_whitespace_test,
    convert_to_binary_test,
    convert_to_uppercase_test,
    count_words_test,
    divide_by_two_test,
    extract_domain_test,
    format_phone_number_test,
    generate_acronym_test,
    get_ascii_value_test,
    get_day_of_week_test,
    get_last_letter_test,
    get_lat_long_test,
    get_time_test,
    get_vowel_count_test,
    reverse_string_test,
)
from llm_agent.llm_router import update_used_tools
from tools.routes import (
    capitalize_first_letter_route,
    compress_whitespace_route,
    convert_to_binary_route,
    convert_to_uppercase_route,
    count_words_route,
    divide_two_route,
    extract_domain_route,
    format_phone_number_route,
    generate_acronym_route,
    get_ascii_value_route,
    get_day_of_week_route,
    get_vowel_count_route,
    last_letter_route,
    lat_long_route,
    reverse_string_route,
    time_route,
)


def select_tools_and_tests(num_tools):
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

    tests = [
        get_time_test,
        get_lat_long_test,
        get_last_letter_test,
        divide_by_two_test,
        get_day_of_week_test,
        format_phone_number_test,
        compress_whitespace_test,
        capitalize_first_letter_test,
        reverse_string_test,
        generate_acronym_test,
        get_vowel_count_test,
        convert_to_binary_test,
        get_ascii_value_test,
        extract_domain_test,
        count_words_test,
        convert_to_uppercase_test,
    ]

    selected_indices = random.sample(range(len(tools)), num_tools)
    used_tools = [tools[i] for i in selected_indices]
    experiment_tests = [tests[i] for i in selected_indices]

    return used_tools, experiment_tests


def run_docker_container():
    subprocess.run(["docker", "build", "-t", "my_llm_server", "."])
    subprocess.run(["docker", "rm", "-f", "llm6"])
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-v",
            "~/.cache/huggingface:/root/.cache/huggingface",
            "--gpus",
            "all",
            "--name",
            "llm6",
            "-p",
            "8888:8888",
            "my_llm_server",
        ]
    )


def run_tests():
    subprocess.run(["python", "fn_call_tests.py"])


def stop_docker_container():
    subprocess.run(["docker", "stop", "llm6"])


def log_experiment_results(experiment_number, stats, total_time, used_tools):
    num_requests = stats["successful_requests"]
    if num_requests <= 0:
        num_requests = 1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"Experiment {experiment_number} Results:\n"
    log_entry += f"Timestamp: {timestamp}\n"
    log_entry += f"Selected Tools: {', '.join(used_tools)}\n"
    log_entry += f"Number of Requests: {num_requests}\n"
    log_entry += f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}\n"
    log_entry += (
        f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}\n"
    )
    log_entry += (
        f"Avg Correct Answers: {stats['total_correct']/stats['total_requests']:.2f}\n"
    )
    log_entry += f"Total Correct Answers: {stats['total_correct']:.2f}\n"
    log_entry += f"Total Benchmarking Time: {total_time}\n"
    log_entry += "-" * 50 + "\n\n"

    with open("experiment_results.log", "a") as log_file:
        log_file.write(log_entry)


def run_tests(experiment_tests):
    stats = {
        "total_tps": 0.0,
        "total_time": 0.0,
        "total_correct": 0.0,
        "successful_requests": 0.0,
        "total_requests": 0.0,
    }

    subprocess.run(
        ["python", "fn_call_tests.py"],
        env={"STATS": str(stats), "EXPERIMENT_TESTS": str(experiment_tests)},
    )
    with open("fn_call_tests_output.log") as file:
        lines = file.readlines()
        stats = eval(lines[-1])
    return stats


def main():
    num_experiments = 3
    num_tools = 4

    for i in range(num_experiments):
        print(f"Running experiment {i+1}/{num_experiments}")
        used_tools, experiment_tests = select_tools_and_tests(num_tools)
        update_used_tools(used_tools)
        run_docker_container()
        time.sleep(20)  # Wait for the container to start

        start_time = time.time()
        stats = run_tests(experiment_tests)
        end_time = time.time()
        total_time = end_time - start_time

        log_experiment_results(i + 1, stats, total_time, used_tools)
        stop_docker_container()


if __name__ == "__main__":
    main()
