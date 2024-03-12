import json
import os
import random
import subprocess
import time
import logging


logging.basicConfig(filename='experiment.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s'
)

def select_tools_and_tests(num_tools):
    """Randomly selects a subset of tool names and their corresponding test names."""
    tool_names = [
        "time_route",
        #"lat_long_route",
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
        #"get_lat_long_test",
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
    """Writes the used tool names to a JSON file."""
    with open("used_tools.json", "w") as file:
        json.dump(used_tool_names, file)


def run_docker_container(experiment_tests, model_name):
    """Runs the Docker container with the specified experiment tests."""
    try: 
        subprocess.run(["docker", "build", "-t", "my_llm_server", "."])
        subprocess.run(["docker", "rm", "-f", "llm6"])
        huggingface_cache_dir = os.path.expanduser("~/.cache/huggingface")
        current_dir = os.path.abspath(os.path.dirname(__file__))

        experiment_tests_str = ",".join(experiment_tests)

        quantization = "gptq" if "GPTQ" in model_name else "None"

        subprocess.run(
            [
                "docker", "run",
                "-d",
                "-v", f"{huggingface_cache_dir}:/root/.cache/huggingface",
                "-v", f"{current_dir}:/app",
                "-e", f"EXPERIMENT_TESTS={experiment_tests_str}",
                "-e", f"DEFAULT_MODEL={model_name}",
                "-e", f"QUANTIZATION={quantization}",
                "--gpus", "all",
                "--name", "llm6",
                "-p", "8888:8888",
                "my_llm_server",
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run Docker container: {str(e)}")
        raise


def stop_docker_container():
    """Stops the Docker container."""
    try:
        subprocess.run(["docker", "stop", "llm6"], check=True)
    except subprocess.CalledProcessError as e:
        logging.warning(f"Failed to stop Docker container: {str(e)}")
                        
def log_experiment_results(experiment_number, stats, total_time, used_tools):
    """Logs the experiment results to a log file."""
    num_requests = stats["successful_requests"]
    if num_requests <= 0:
        num_requests = 1

    total_requests = stats["total_requests"]
    if total_requests <= 0:
        total_requests = 1

    log_entry = f"Experiment {experiment_number} Results:\n"
    log_entry += f"Selected Tools: {', '.join(used_tools)}\n"
    log_entry += f"Number of Requests: {num_requests}\n"
    log_entry += f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}\n"
    log_entry += (
        f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}\n"
    )
    log_entry += f"Avg Correct Answers: {stats['total_correct']/total_requests:.2f}\n"
    log_entry += f"Total Correct Answers: {stats['total_correct']:.2f}\n"
    log_entry += f"Total Benchmarking Time: {total_time}\n"
    log_entry += "-" * 50 + "\n\n"

    with open("fn_call_tests_output.log", "a") as log_file:
        log_file.write(log_entry)


def run_tests():
    """Runs the tests."""
    stats = {
        "total_tps": 0.0,
        "total_time": 0.0,
        "total_correct": 0.0,
        "successful_requests": 0.0,
        "total_requests": 0.0,
    }

    # subprocess.run(["docker", "exec", "llm6", "python", "fn_call_tests.py"])

    try:
        subprocess.run(["docker", "exec", "llm6", "python", "fn_call_tests.py"],
                       check=True
        )

        with open("fn_call_tests_output.log") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                if last_line:
                    stats = json.loads(last_line)
                else:
                    print("Warning: The last line of log file is empty.")
            else:
                print("Warning: The log file is empty.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run tests: {str(e)}")
    except FileNotFoundError:
        logging.warning("The log file does not exist.")

    return stats


def clear_or_create_log_file():
    """Clears or creates the log file."""
    with open("fn_call_tests_output.log", "w") as _:
        # This clears the file if it exists or creates it if it doesn't
        pass


def main():
    """Main function to run the experiments."""
    num_experiments = 2
    models = [
        #"mistralai/Mistral-7B-Instruct-v0.2",
        #"teknium/OpenHermes-2.5-Mistral-7B",
        #"TheBloke/Mistral-7B-Instruct-v0.2-GPTQ",
        #"TheBloke/OpenHermes-2.5-Mistral-7B-GPTQ",
        "TheBloke/Mixtral-8x7B-v0.1-GPTQ",
    ]

    """
    RUN SINGLETON TOOL TESTS AND 16 TOOLS TEST
    """
    # get all tools

    for model in models:
        print(f"Running experiments for model: {model}")

        # used_tool_names, experiment_test_names = select_tools_and_tests(16)
        # for i in range(len(used_tool_names)):
        #     # test each tool individually
        #     tool = [used_tool_names[i]]
        #     test = [experiment_test_names[i]]
        #     print(f"FUNCS: {tool}")
        #     print(f"TEST: {test}")
        #     print(f"Running experiment {i+1}/16")
        #     clear_or_create_log_file()
        #     print(f"Used tools: {tool}")
        #     write_used_tools_to_file(tool)

        #     run_docker_container(test, model)
        #     time.sleep(25)  # Waits for the container to start

        #     start_time = time.time()
        #     stats = run_tests()
        #     end_time = time.time()
        #     total_time = end_time - start_time

        #     log_experiment_results(i + 1, stats, total_time, tool)
        #     stop_docker_container()
        #     time.sleep(10)  # Waits for the container to stop

        num_funcs = 15

        for i in range(num_experiments):
            print(f"NUM FUNCS: {num_funcs}")
            print(f"Running experiment {i+1}/{num_experiments}")
            clear_or_create_log_file()
            used_tool_names, experiment_test_names = select_tools_and_tests(num_funcs)
            print(f"Used tools: {used_tool_names}")
            write_used_tools_to_file(used_tool_names)

            run_docker_container(experiment_test_names, model)
            time.sleep(25)  # Waits for the container to start

            start_time = time.time()
            stats = run_tests()
            end_time = time.time()
            total_time = end_time - start_time

            log_experiment_results(i + 1, stats, total_time, used_tool_names)
            stop_docker_container()
            time.sleep(10)  # Waits for the container to stop

    # BELOW FOR TESTING SUBSETS OF TOOLS

    # for k in range(1, num_tools):
    #     # Creates an empty log file
    #     open("fn_call_tests_output.log", "w").close()

    #     for i in range(num_experiments):
    #         print(f"NUM FUNCS: {k}")
    #         print(f"Running experiment {i+1}/{num_experiments}")
    #         clear_or_create_log_file()
    #         used_tool_names, experiment_test_names = select_tools_and_tests(k)
    #         print(f"Used tools: {used_tool_names}")
    #         write_used_tools_to_file(used_tool_names)

    #         run_docker_container(experiment_test_names)
    #         time.sleep(20)  # Waits for the container to start

    #         start_time = time.time()
    #         stats = run_tests()
    #         end_time = time.time()
    #         total_time = end_time - start_time

    #         log_experiment_results(i + 1, stats, total_time, used_tool_names)
    #         stop_docker_container()
    #         time.sleep(10)  # Waits for the container to stop


if __name__ == "__main__":
    main()
