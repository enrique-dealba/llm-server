import json
import logging
import os
import subprocess
import time

logging.basicConfig(
    filename="experiment_json.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_docker_container(model_name):
    """Runs the Docker container with the specified model."""
    try:
        subprocess.run(["docker", "build", "-t", "my_llm_server", "."])
        subprocess.run(["docker", "rm", "-f", "llm6"])
        huggingface_cache_dir = os.path.expanduser("~/.cache/huggingface")
        current_dir = os.path.abspath(os.path.dirname(__file__))

        quantization = "gptq" if "GPTQ" in model_name else "None"

        subprocess.run(
            [
                "docker", "run", "-d",
                "-v", f"{huggingface_cache_dir}:/root/.cache/huggingface",
                "-v", f"{current_dir}:/app",
                "-e", f"DEFAULT_MODEL={model_name}",
                "-e", f"QUANTIZATION={quantization}",
                "--gpus", "all",
                "--name", "llm6",
                "-p", "8888:8888",
                "my_llm_server",
            ],
            check=True,
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


def log_experiment_results(experiment_number, stats, total_time):
    """Logs the experiment results to a log file."""
    num_requests = stats["successful_requests"]
    if num_requests <= 0:
        num_requests = 1

    total_requests = stats["total_requests"]
    if total_requests <= 0:
        total_requests = 1

    log_entry = f"Experiment {experiment_number} Results:\n"
    log_entry += f"Number of Requests: {num_requests}\n"
    log_entry += f"Avg Tokens per Second (TPS): {stats['total_tps']/num_requests:.2f}\n"
    log_entry += (
        f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}\n"
    )
    log_entry += f"Avg Correct Answers: {stats['total_correct']/total_requests:.2f}\n"
    log_entry += f"Total Correct Answers: {stats['total_correct']:.2f}\n"
    log_entry += f"Total Benchmarking Time: {total_time}\n"
    log_entry += "-" * 50 + "\n\n"

    with open("json_tests_output.log", "a") as log_file:
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

    try:
        subprocess.run(
            ["docker", "exec", "llm6", "python", "json_tests.py"], check=True
        )

        with open("json_tests_output.log") as file:
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
    with open("json_tests_output.log", "w") as _:
        # This clears the file if it exists or creates it if it doesn't
        pass


def main():
    """Main function to run the experiments."""
    num_experiments = 2
    models = [
        # "mistralai/Mistral-7B-Instruct-v0.2",
        # "teknium/OpenHermes-2.5-Mistral-7B",
        # "microsoft/phi-2",
        "NousResearch/Hermes-2-Pro-Mistral-7B",
        # "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ",
        # "TheBloke/OpenHermes-2.5-Mistral-7B-GPTQ",
    ]

    for model in models:
        print(f"Running experiments for model: {model}")

        for i in range(num_experiments):
            print(f"Running experiment {i+1}/{num_experiments}")
            clear_or_create_log_file()

            run_docker_container(model)
            waiting_time = 50
            print(f"Waiting {waiting_time} seconds for the server to start...")
            time.sleep(waiting_time)  # Waits for the container to start

            start_time = time.time()
            stats = run_tests()
            end_time = time.time()
            total_time = end_time - start_time

            log_experiment_results(i + 1, stats, total_time)
            stop_docker_container()
            time.sleep(10)  # Waits for the container to stop


if __name__ == "__main__":
    main()
