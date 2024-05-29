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
        quantization = "awq" if "AWQ" in model_name else "None"

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
        "CatalogMaintenanceObjective": [
            "Make a new catalog maintenance for sensor RME02 with U markings and TEST mode, priority 12, patience of 10 mins, ending after 25 mins. Start at 2024-05-21 19:20:00.150000+00:00 and conclude at 2024-05-21 22:30:00.250000+00:00. Include sensor IDs RME02, LMNT01. Set RATE_TRACK_SIDEREAL for the tracking type and operate in LEO orbital regime.",
            "Schedule a new catalog task for sensor ABQ04 with REAL mode, classification marking S, priority 8, patience of 25 minutes, and an end time offset of 35 minutes. Begin on 2024-05-21 19:20:00.150000+00:00 and finish by 2024-05-21 22:30:00.250000+00:00. Use sensors ABQ04, UKR05 and set RATE_TRACK for tracking. Orbital regime is GEO.",
            "Configure catalog maintenance for sensor UKR07 in TEST mode, with classification marking C, priority 12, patience of 15 minutes, concluding 40 minutes later. Starting at 2024-05-21 19:20:00.150000+00:00, ending at 2024-05-21 22:30:00.250000+00:00. Include sensors UKR07, RME04, and use SIDEREAL tracking. Set the orbital regime to MEO.",
            "Set up a catalog entry for sensor RME12, operating in REAL mode, with a U classification, a high priority of 18, 30 minutes of patience, and completion after 45 minutes. Starts at 2024-05-21 19:20:00.150000+00:00 and ends at 2024-05-21 22:30:00.250000+00:00. Include sensors RME12, ABQ09, and set RATE_TRACK_SIDEREAL as the tracking type. Orbital regime is XGEO.",
            "Create a maintenance task for sensor LMNT05 in TEST mode, marked as TS, with a priority of 10, a 30-minute patience window, and an end time offset of 20 minutes. Start at 2024-05-21 19:20:00.150000+00:00, concluding at 2024-05-21 22:30:00.250000+00:00. Include LMNT05, LMNT06 in sensor list and set RATE_TRACK for tracking. Orbital regime is LEO.",
            "Plan a catalog operation for sensor LMNT11 using TEST mode, S classification, with a priority of 13, patience for 20 minutes, and finishing after 30 minutes. Begins at 2024-05-21 19:20:00.150000+00:00 and ends at 2024-05-21 22:30:00.250000+00:00. Include LMNT11, RME16 sensors and use RATE_TRACK_SIDEREAL. Operate in GEO orbital regime.",
            "Create a new catalog maintenance for sensor RME15 with REAL mode, U//FOUO marking, priority 14, patience of 50 minutes, and set to end after 70 minutes. Begins at 2024-05-21 19:20:00.150000+00:00 and concludes at 2024-05-21 22:30:00.250000+00:00. Use sensors RME15, UKR03 and set SIDEREAL for tracking type. Orbital regime should be MEO.",
        ],
        "PeriodicRevisitObjective": [
            "Track object 44248 with sensors RME01 and LMNT45, revisiting twice per hour for the next 36 hours using TEST mode, 'S' markings, and set priority to 2. Begin at 2024-05-21 19:20:00.150000+00:00 and end at 2024-05-21 22:30:00.250000+00:00. Use RATE_TRACK_SIDEREAL as the collect request type and operate in LEO orbital regime.",
            "Track celestial object 21212 with sensors RME33, ABQ42, using REAL mode, revisiting four times per hour, starting execution for a 48-hour plan, marked as 'U//FOUO', with priority set to 1. Begins on 2024-05-21 19:20:00.150000+00:00 and finishes by 2024-05-21 22:30:00.250000+00:00. Employ RATE_TRACK for tracking type and GSO for orbital regime.",
            "Track RSO object 43567 using sensors ABQ42, UKR88 in TEST mode, schedule four revisits per hour, initiate with a 36-hour plan, marked as 'C', with priority set to 3. Start at 2024-05-21 19:20:00.150000+00:00, ending at 2024-05-21 22:30:00.250000+00:00. Use SIDEREAL tracking and MEO orbital regime.",
            "Monitor celestial object 20394 with sensors UKR88, RME02 in REAL mode, configure five revisits per hour, begin with a 42-hour schedule, classified as 'U//FOUO', priority level 3. Starts at 2024-05-21 19:20:00.150000+00:00 and concludes at 2024-05-21 22:30:00.250000+00:00. Apply RATE_TRACK_SIDEREAL and operate in HEO orbital regime.",
            "Observe object 31705 with sensors LMNT33, RME99 in REAL mode, perform three revisits per hour, initiate with a 24-hour strategy, marked as 'S', with priority level 1. Begins on 2024-05-21 19:20:00.150000+00:00 and ends by 2024-05-21 22:30:00.250000+00:00. Set collect request type to RATE_TRACK and orbital regime to GSO.",
            "Follow object 84123 using sensors RME02, ABQ01 in TEST mode, schedule six revisits per hour, start a 12-hour timeline, classified as 'C', with a priority of 2. Starting at 2024-05-21 19:20:00.150000+00:00, ending at 2024-05-21 22:30:00.250000+00:00. Implement SIDEREAL tracking and LEO orbital regime.",
            "Track 43567 using sensors ABQ42, LMNT22 in TEST mode, schedule one revisit per hour, initiate with a 30-hour plan, marked as 'C', with priority set to 5. Begins at 2024-05-21 19:20:00.150000+00:00 and concludes at 2024-05-21 22:30:00.250000+00:00. Choose RATE_TRACK_SIDEREAL for tracking type and operate in MEO orbital regime.",
        ],
        "SearchObjective": [
            "Create a new search objective for target 12345 using sensor UKR12 with S marking and REAL data mode, priority set to 5, and collect request type RATE_TRACK_SIDEREAL. Start the objective at 2024-05-22 09:30:00.000000+00:00 and end at 2024-05-22 11:00:00.000000+00:00. Set initial offset to 60 and final offset to 90, frame overlap percentage to 70%, number of frames to 8, integration time to 2 seconds, binning to 2, and end time offset to 45 minutes.",
            "Generate a search objective for target 98765 using sensor ABQ03 with TS marking and EXERCISE data mode, priority set to 3, and collect request type RATE_TRACK. Start time 2024-05-23 06:15:00.000000+00:00, end time 2024-05-23 08:45:00.000000+00:00. Initial offset 50, final offset 80, frame overlap 55%, 10 number of frames, 3 seconds integration time, binning 1, end time offset 30 minutes.",
            "Make a new search objective for target 54321 using sensor LMNT06 with U//FOUO marking and SIMULATED data mode, priority set to 7, and collect request type SIDEREAL. Start objective at 2024-05-24 00:00:00.000000+00:00 and end at 2024-05-24 02:30:00.000000+00:00. Initial offset 30, final offset 45, frame overlap percentage 65%, 6 number of frames, 2 seconds integration time, binning 3, end time offset 20 minutes.",
            "Create a search objective for target 11111 using sensor RME99 with U marking and TEST data mode, priority set to 10, and collect request type RATE_TRACK_SIDEREAL. Start time 2024-05-25 10:00:00.000000+00:00, end time 2024-05-25 12:15:00.000000+00:00. Initial offset 40, final offset 70, 60 percent frame overlap, 7 number of frames, 1 second integration time, default binning, 25 minutes end time offset.",
            "Generate a search objective for target 22222 using sensor ABQ77 with C marking and REAL data mode, priority set to 4, and collect request type RATE_TRACK. Start time 2024-05-26 15:30:00.000000+00:00, end time 2024-05-26 18:00:00.000000+00:00. 35 initial offset, 55 final offset, frame overlap of 50%, 9 number of frames, 4 seconds integration time, binning 2, 40 minutes end time offset.",
            "Make a new search objective for target 33333 using sensor LMNT22 with S marking and EXERCISE data mode, priority set to 8, and collect request type SIDEREAL. Start objective at 2024-05-27 06:00:00.000000+00:00 and end at 2024-05-27 09:15:00.000000+00:00. Initial offset 45, final offset 75, frame overlap percentage 55%, 8 number of frames, 3 seconds integration time, binning 1, end time offset 35 minutes.",
            "Create a search objective for target 44444 using sensor UKR55 with TS marking and SIMULATED data mode, priority set to 2, and collect request type RATE_TRACK_SIDEREAL. Start time 2024-05-28 12:00:00.000000+00:00, end time 2024-05-28 14:30:00.000000+00:00. 50 initial offset, 90 final offset, frame overlap of 65%, 10 number of frames, 2 seconds integration time, default binning, 30 minutes end time offset.",
            "Generate a search objective for target 55555 using sensor RME11 with U//FOUO marking and TEST data mode, priority set to 6, and collect request type RATE_TRACK. Start time 2024-05-29 18:45:00.000000+00:00, end time 2024-05-30 00:00:00.000000+00:00. 60 initial offset, 80 final offset, frame overlap of 70%, 7 number of frames, 1 second integration time, binning 3, 45 minutes end time offset.",
        ],
        "DataEnrichmentObjective": [
            "Create a data enrichment objective for targets 12345, 67890, and 54321 using sensors RME01, LMNT02, and ABQ03. Set the classification marking to 'U//FOUO', data mode to 'REAL', and collect request type to 'RATE_TRACK'. Observe a maximum of 8 RSOs with 10 revisits per hour, planning for 48 hours. Start the objective at 2024-06-01 08:00:00.000000+00:00 and end at 2024-06-03 08:00:00.000000+00:00. Set the priority to 15.",
            "Generate a data enrichment for targets 98765 and 43210 using sensor UKR01 with 'TS' markings and 'EXERCISE' mode. Set the priority to 25 and use 'SIDEREAL' collect request type. Begin the objective at 2024-07-15 18:30:00.250000+00:00 and conclude at 2024-07-16 06:30:00.250000+00:00. Observe 5 RSOs with 15 revisits per hour, planning for 18 hours.",
            "Prepare a data enrichment objective for targets 13579 and 24680 using sensors RME04 and LMNT05 with 'S' markings and 'TEST' mode. Set the priority to the default value and use 'RATE_TRACK_SIDEREAL' collect request type. Start the objective at 2024-08-10 09:45:00.500000+00:00 and end at 2024-08-11 21:45:00.500000+00:00. Observe the maximum number of RSOs with 8 revisits per hour, planning for 30 hours.",
            "Create a data enrichment for targets 11111, 22222, 33333, and 44444 using sensors ABQ06, UKR07, and RME08 with 'C' markings and 'SIMULATED' mode. Set the priority to 18 and use 'RATE_TRACK' collect request type. Start the objective at 2024-09-05 12:00:00.750000+00:00 and end at 2024-09-06 00:00:00.750000+00:00. Observe 7 RSOs with 20 revisits per hour, planning for 16 hours.",
            "Generate a data enrichment objective for target 55555 using sensor LMNT09 with 'U' markings and 'REAL' mode. Set the priority to 22 and use 'SIDEREAL' collect request type. Begin the objective at 2024-10-20 03:15:00.000000+00:00 and conclude at 2024-10-21 15:15:00.000000+00:00. Observe the default number of RSOs with 10 revisits per hour, planning for 40 hours.",
            "Prepare a data enrichment for targets 66666 and 77777 using sensors RME10 and ABQ11 with 'U//FOUO' markings and 'EXERCISE' mode. Set the priority to 19 and use 'RATE_TRACK_SIDEREAL' collect request type. Start the objective at 2024-11-11 16:30:00.250000+00:00 and end at 2024-11-12 04:30:00.250000+00:00. Observe 4 RSOs with 18 revisits per hour, planning for 20 hours.",
            "Create a data enrichment objective for targets 88888, 99999, and 00000 using sensors UKR12, LMNT13, and RME14 with 'TS' markings and 'TEST' mode. Set the priority to 23 and use 'RATE_TRACK' collect request type. Start the objective at 2024-12-01 06:45:00.500000+00:00 and end at 2024-12-02 18:45:00.500000+00:00. Observe 9 RSOs with 6 revisits per hour, planning for 42 hours.",
            "Generate a data enrichment for target 12121 using sensor ABQ15 with 'S' markings and 'SIMULATED' mode. Set the priority to the default value and use 'SIDEREAL' collect request type. Begin the objective at 2025-01-15 20:00:00.750000+00:00 and conclude at 2025-01-16 08:00:00.750000+00:00. Observe the maximum number of RSOs with 14 revisits per hour, planning for 14 hours.",
        ],
        "SpectralClearingObjective": [
            "Create a spectral clearing objective for targets 78901 and 23456 using sensors LMNT02 and UKR05 with S markings and REAL mode, priority set to 8. Start the objective at 2024-06-01 09:30:00.000000+00:00 and end at 2024-06-02 18:15:00.000000+00:00. Set the patience to 60 minutes, and run integration at 1.5 seconds per frame for 15 total frames per intent, using a binning of 2.",
            "Generate a new spectral clearing objective for target 13579 using sensor RME01 with U//FOUO markings and SIMULATED mode, priority set to 12. Start the objective at 2024-07-15 16:45:00.000000+00:00 and end at 2024-07-16 02:30:00.000000+00:00. Set the patience to 20 minutes, and run integration at 3 seconds per frame for 8 total frames per intent, using the default binning of 1.",
            "Initiate a spectral clearing objective for targets 98765 and 43210 using sensors ABQ02 and RME04 with C markings and TEST mode, priority set to 6. Start the objective at 2024-08-10 11:00:00.000000+00:00 and end at 2024-08-11 09:15:00.000000+00:00. Set the patience to 90 minutes, and run integration at 2.5 seconds per frame for 10 total frames per intent, using a binning of 4.",
            "Create a spectral clearing objective for target 56789 using sensors LMNT01 and UKR03 with U markings and REAL mode, priority set to 14. Start the objective at 2024-09-05 19:30:00.000000+00:00 and end at 2024-09-06 07:45:00.000000+00:00. Set the patience to 30 minutes, and run integration at 1.8 seconds per frame for 20 total frames per intent, using a binning of 3.",
            "Generate a new spectral clearing objective for targets 24680 and 13579 using sensors RME02 and ABQ03 with TS markings and EXERCISE mode, priority set to 9. Start the objective at 2024-10-20 08:15:00.000000+00:00 and end at 2024-10-21 17:30:00.000000+00:00. Set the patience to 75 minutes, and run integration at 2.2 seconds per frame for 18 total frames per intent, using the default binning of 1.",
            "Initiate a spectral clearing objective for target 97531 using sensor LMNT04 with C markings and SIMULATED mode, priority set to 11. Start the objective at 2024-11-12 14:00:00.000000+00:00 and end at 2024-11-13 03:45:00.000000+00:00. Set the patience to 50 minutes, and run integration at 1.2 seconds per frame for 25 total frames per intent, using a binning of 2.",
            "Create a spectral clearing objective for targets 86420 and 75319 using sensors UKR02 and RME05 with S markings and TEST mode, priority set to 7. Start the objective at 2024-12-08 10:45:00.000000+00:00 and end at 2024-12-09 22:30:00.000000+00:00. Set the patience to 40 minutes, and run integration at 2.8 seconds per frame for 14 total frames per intent, using a binning of 4.",
            "Generate a new spectral clearing objective for target 19753 using sensor ABQ04 with U//FOUO markings and REAL mode, priority set to 13. Start the objective at 2025-01-03 18:00:00.000000+00:00 and end at 2025-01-04 06:15:00.000000+00:00. Set the patience to 25 minutes, and run integration at 3.5 seconds per frame for 6 total frames per intent, using the default binning of 1.",
        ],
    }

    num_experiments = 1
    models = [
        # "mistralai/Mistral-7B-Instruct-v0.2",
        # "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ",
        # "TheBloke/Mistral-7B-Instruct-v0.2-AWQ",
        # "teknium/OpenHermes-2.5-Mistral-7B",
        "TheBloke/OpenHermes-2.5-Mistral-7B-GPTQ",
        "TheBloke/OpenHermes-2.5-Mistral-7B-AWQ",
        # "NousResearch/Hermes-2-Pro-Mistral-7B",
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
