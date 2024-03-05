import datetime
import json
import os
import random
import subprocess
import time


def select_tools_and_tests(num_tools):
    tool_names = [
        "time_route",
        "lat_long_route",
        "last_letter_route",
        "divide_two_route",
        "get_day_of_week_route",
        "format_phone_number_route",
        "compress_whitespace_route",
        "capitalize_first_letter_route",
        "reverse_string_route",
        "generate_acronym_route",
        "get_vowel_count_route",
        "convert_to_binary_route",
        "get_ascii_value_route",
        "extract_domain_route",
        "count_words_route",
        "convert_to_uppercase_route",
    ]

    tests = [
        "get_time_test",
        "get_lat_long_test",
        "get_last_letter_test",
        "divide_by_two_test",
        "get_day_of_week_test",
        "format_phone_number_test",
        "compress_whitespace_test",
        "capitalize_first_letter_test",
        "reverse_string_test",
        "generate_acronym_test",
        "get_vowel_count_test",
        "convert_to_binary_test",
        "get_ascii_value_test",
        "extract_domain_test",
        "count_words_test",
        "convert_to_uppercase_test",
    ]

    selected_indices = random.sample(range(len(tool_names)), num_tools)
    used_tool_names = [tool_names[i] for i in selected_indices]
    experiment_test_names = [tests[i] for i in selected_indices]

    return used_tool_names, experiment_test_names


def write_used_tools_to_file(used_tool_names):
    with open("used_tools.json", "w") as file:
        json.dump(used_tool_names, file)


def run_docker_container(experiment_tests):
    subprocess.run(["docker", "build", "-t", "my_llm_server", "."])
    subprocess.run(["docker", "rm", "-f", "llm6"])
    huggingface_cache_dir = os.path.expanduser("~/.cache/huggingface")
    current_dir = os.path.abspath(os.path.dirname(__file__))

    experiment_tests_str = ','.join(experiment_tests)

    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-v",
            f"{huggingface_cache_dir}:/root/.cache/huggingface",
            "-v",
            f"{current_dir}:/app",
            "-e",
            f"EXPERIMENT_TESTS={experiment_tests_str}",
            "--gpus",
            "all",
            "--name",
            "llm6",
            "-p",
            "8888:8888",
            "my_llm_server",
        ]
    )


def stop_docker_container():
    subprocess.run(["docker", "stop", "llm6"])


def log_experiment_results(experiment_number, stats, total_time, used_tools):
    num_requests = stats["successful_requests"]
    if num_requests <= 0:
        num_requests = 1

    total_requests = stats['total_requests']
    if total_requests <= 0:
        total_requests = 1

    #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"Experiment {experiment_number} Results:\n"
    #log_entry += f"Timestamp: {timestamp}\n"
    log_entry += f"Selected Tools: {', '.join(used_tools)}\n"
    log_entry += f"Number of Requests: {num_requests}\n"
    log_entry += f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}\n"
    log_entry += (
        f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}\n"
    )
    log_entry += (
        f"Avg Correct Answers: {stats['total_correct']/total_requests:.2f}\n"
    )
    log_entry += f"Total Correct Answers: {stats['total_correct']:.2f}\n"
    log_entry += f"Total Benchmarking Time: {total_time}\n"
    log_entry += "-" * 50 + "\n\n"

    with open("fn_call_tests_output.log", "a") as log_file:
        log_file.write(log_entry)


def run_tests(experiment_number):
    stats = {
        "total_tps": 0.0,
        "total_time": 0.0,
        "total_correct": 0.0,
        "successful_requests": 0.0,
        "total_requests": 0.0,
    }

    subprocess.run(["docker", "exec", "llm6", "python", "fn_call_tests.py"])

    try:
        with open("fn_call_tests_output.log", "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                if last_line:
                    stats = json.loads(last_line)
                else:
                    print("Warning: The last line of the log file 'fn_call_tests_output.log' is empty.")
            else:
                print("Warning: The log file 'fn_call_tests_output.log' is empty.")
    except FileNotFoundError:
        print("Warning: The log file 'fn_call_tests_output.log' does not exist.")

    return stats

def clear_or_create_log_file():
    with open("fn_call_tests_output.log", "w") as file:
        pass  # This clears the file if it exists or creates it if it doesn't


def main():
    num_experiments = 2
    num_tools = 2

    # Create an empty log file
    open("fn_call_tests_output.log", "w").close()

    for i in range(num_experiments):
        print(f"Running experiment {i+1}/{num_experiments}")
        clear_or_create_log_file()
        used_tool_names, experiment_test_names = select_tools_and_tests(num_tools)
        write_used_tools_to_file(used_tool_names)

        run_docker_container(experiment_test_names)
        time.sleep(20)  # Wait for the container to start

        start_time = time.time()
        stats = run_tests(i+1)
        end_time = time.time()
        total_time = end_time - start_time

        log_experiment_results(i+1, stats, total_time, used_tool_names)
        stop_docker_container()


if __name__ == "__main__":
    main()