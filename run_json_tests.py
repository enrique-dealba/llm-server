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
                # "-e", f"SCHEMA={schema}",
                "--gpus", "all",
                "--name", "llm6",
                "-p", "8889:8889",
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
    log_entry += f"Avg Correctness: {stats['total_correctness']/num_requests:.2%}\n"
    log_entry += (
        f"Avg Time Elapsed Per Response: {stats['total_time']/num_requests:.2f}\n"
    )
    log_entry += f"Total Benchmarking Time: {total_time}\n"
    log_entry += "-" * 50 + "\n\n"

    with open("json_tests_output.log", "a") as log_file:
        log_file.write(log_entry)


def run_tests(prompts, objective):
    """Runs the tests."""
    stats = {
        "total_correctness": 0.0,
        "obj_correctness": 0.0,
        "total_time": 0.0,
        "successful_requests": 0.0,
        "total_requests": 0.0,
    }

    try:
        subprocess.run(
            ["docker", "exec", "llm6",
             "python", "json_tests.py",
             f"--prompts={json.dumps(prompts)}",
             f"--objective={json.dumps(objective)}"],
            check=True
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
    # schema_prompts = {
    #     "CMO": [
    #         "Make a new catalog maintenance for sensor RME02 with U markings and TEST mode, with priority 12, and patience of 10 mins ending after 25 mins",
    #         "Schedule a new catalog task for sensor ABQ04 with REAL mode, classification marking S, priority 8, patience of 25 minutes, and an end time offset of 35 minutes.",
    #         "Configure catalog maintenance for sensor UKR07 in TEST mode, with classification marking C, priority 12, patience of 15 minutes, and concluding 40 minutes later.",
    #         "Set up a catalog entry for sensor RME12, operating in REAL mode, with a U classification, a high priority of 18, 30 minutes of patience, and completion after 45 minutes",
    #         "Create a maintenance task for sensor LMNT05 in TEST mode, marked as TS, with a priority of 10, a 30-minute patience window, and an end time offset of 20 minutes.",
    #         "Plan a catalog operation for sensor LMNT11 using TEST mode, S classification, with a priority of 13, patience for 20 minutes, and finishing after 30 minutes",
    #         # "Make a new catalog job for sensor ABQ01 in REAL mode, marked as TS, with priority 11, 15 minutes of patience, and a finalization time 25 minutes later.",
    #         "Create a new catalog maintenance for sensor RME15 with REAL mode, U//FOUO marking, priority 14, patience of 50 minutes, and set to end after 70 minutes.",
    #     ],
    #     "PRO": [
    #         "Track object 44248 with sensor RME01, revisiting twice per hour for the next 36 hours using TEST mode, 'S' markings, and set priority to 2.",
    #         "Track celestial object 21212 with sensor RME33 with REAL mode, revisiting four times per hour, starting execution with REAL mode for a 48-hour plan, marked as “U//FOUO, with priority set to 1.",
    #         "Track RSO object 43567 using sensor ABQ42 in TEST mode, schedule four revisits per hour, initiate with a 36-hour plan, marked as 'C', with priority set to 3",
    #         "Monitor celestial object 20394 with sensor UKR88 in REAL mode, configure five revisits per hour, begin with a 42-hour schedule, classified as 'U//FOUO', priority level 3",
    #         "Observe object 31705 with sensor LMNT33 in REAL mode, perform three revisits per hour, initiate with a 24-hour strategy, marked as 'S', with priority level 1",
    #         "Follow object 84123 using sensor RME02 in TEST mode, schedule six revisits per hour, start a 12-hour timeline, classified as 'C', with a priority of 2",
    #         # "Monitor object 96284 with sensor UKR44 in REAL mode, plan for two revisits per hour, begin with a 12-hour outline, marked as 'TS', priority set at 3",
    #         "Track 43567 using sensor ABQ42 in TEST mode, schedule one revisit per hour, initiate with a 30-hour plan, marked as 'C', with priority set to 5",
    #     ],
    # }
    schema_prompts = {
        "CMO": [
            "Make a new catalog maintenance for sensor RME02 with U markings and TEST mode, with priority 12, and patience of 10 mins ending after 25 mins. Start at 2024-05-21 19:20:00.150000+00:00 and conclude at 2024-05-21 22:30:00.250000+00:00.",
            "Schedule a new catalog task for sensor ABQ04 with REAL mode, classification marking S, priority 8, patience of 25 minutes, and an end time offset of 35 minutes. Begin on 2024-05-21 19:20:00.150000+00:00 and finish by 2024-05-21 22:30:00.250000+00:00.",
            "Configure catalog maintenance for sensor UKR07 in TEST mode, with classification marking C, priority 12, patience of 15 minutes, and concluding 40 minutes later. Starting at 2024-05-21 19:20:00.150000+00:00, ending at 2024-05-21 22:30:00.250000+00:00.",
            "Set up a catalog entry for sensor RME12, operating in REAL mode, with a U classification, a high priority of 18, 30 minutes of patience, and completion after 45 minutes. Starts at 2024-05-21 19:20:00.150000+00:00 and ends at 2024-05-21 22:30:00.250000+00:00.",
            "Create a maintenance task for sensor LMNT05 in TEST mode, marked as TS, with a priority of 10, a 30-minute patience window, and an end time offset of 20 minutes. Start at 2024-05-21 19:20:00.150000+00:00, concluding at 2024-05-21 22:30:00.250000+00:00.",
            "Plan a catalog operation for sensor LMNT11 using TEST mode, S classification, with a priority of 13, patience for 20 minutes, and finishing after 30 minutes. Begins at 2024-05-21 19:20:00.150000+00:00 and ends at 2024-05-21 22:30:00.250000+00:00.",
            "Create a new catalog maintenance for sensor RME15 with REAL mode, U//FOUO marking, priority 14, patience of 50 minutes, and set to end after 70 minutes. Begins at 2024-05-21 19:20:00.150000+00:00 and concludes at 2024-05-21 22:30:00.250000+00:00.",
        ],
        "PRO": [
            "Track object 44248 with sensor RME01, revisiting twice per hour for the next 36 hours using TEST mode, 'S' markings, and set priority to 2. Begin at 2024-05-21 19:20:00.150000+00:00 and end at 2024-05-21 22:30:00.250000+00:00.",
            "Track celestial object 21212 with sensor RME33 with REAL mode, revisiting four times per hour, starting execution with REAL mode for a 48-hour plan, marked as “U//FOUO, with priority set to 1. Starts on 2024-05-21 19:20:00.150000+00:00 and finishes by 2024-05-21 22:30:00.250000+00:00.",
            "Track RSO object 43567 using sensor ABQ42 in TEST mode, schedule four revisits per hour, initiate with a 36-hour plan, marked as 'C', with priority set to 3. Start at 2024-05-21 19:20:00.150000+00:00, ending at 2024-05-21 22:30:00.250000+00:00.",
            "Monitor celestial object 20394 with sensor UKR88 in REAL mode, configure five revisits per hour, begin with a 42-hour schedule, classified as 'U//FOUO', priority level 3. Starts at 2024-05-21 19:20:00.150000+00:00 and concludes at 2024-05-21 22:30:00.250000+00:00.",
            "Observe object 31705 with sensor LMNT33 in REAL mode, perform three revisits per hour, initiate with a 24-hour strategy, marked as 'S', with priority level 1. Begins on 2024-05-21 19:20:00.150000+00:00 and ends by 2024-05-21 22:30:00.250000+00:00.",
            "Follow object 84123 using sensor RME02 in TEST mode, schedule six revisits per hour, start a 12-hour timeline, classified as 'C', with a priority of 2. Starting at 2024-05-21 19:20:00.150000+00:00, ending at 2024-05-21 22:30:00.250000+00:00.",
            "Track 43567 using sensor ABQ42 in TEST mode, schedule one revisit per hour, initiate with a 30-hour plan, marked as 'C', with priority set to 5. Begins at 2024-05-21 19:20:00.150000+00:00 and concludes at 2024-05-21 22:30:00.250000+00:00.",
        ],
    }

    num_experiments = 1
    models = [
        # "mistralai/Mistral-7B-Instruct-v0.2",
        # "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ",
        "teknium/OpenHermes-2.5-Mistral-7B",
        "TheBloke/OpenHermes-2.5-Mistral-7B-GPTQ",
        "NousResearch/Hermes-2-Pro-Mistral-7B",
    ]

    for model in models:
        print(f"Running experiments for model: {model}")

        for obj, prompts in schema_prompts.items():
            print(f"Running experiments for objective: {obj}")

            for i in range(num_experiments):
                print(f"Running experiment {i+1}/{num_experiments}")
                clear_or_create_log_file()

                run_docker_container(model)
                waiting_time = 40
                print(f"Waiting {waiting_time} seconds for the server to start...")
                time.sleep(waiting_time)  # Waits for the container to start

                start_time = time.time()
                stats = run_tests(prompts, obj)
                end_time = time.time()
                total_time = end_time - start_time

                log_experiment_results(i + 1, stats, total_time)
                stop_docker_container()
                time.sleep(12)  # Waits for the container to stop


if __name__ == "__main__":
    main()
