from templates import CMO, PRO, CMOTemplate, PROTemplate

CMO_examples = [
    "RME00",  # sensor_name
    "TEST",  # data_mode
    "TS",  # classification_marking
    30,  # patience_minutes
    20,  # end_time_offset_minutes
    # "Catalog Maintenance Objective",  # objective_name
    10,  # priority
]

PRO_examples = [
    12345,  # target_id
    "RME08",  # sensor_name
    "REAL",  # data_mode
    "S",  # classification_marking
    4,  # revisits_per_hour
    16,  # hours_to_plan
    2,  # priority
]

cmo_info = {
    "prompts": [
        "I need a new catalog maintenance for RME00 with TS markings and use TEST mode with a priority of 10 and set the patience to 30 minutes and end search after 20 minutes.",
        "Make a new catalog job for sensor ABQ01 in REAL mode, marked as TS, with priority 11, 15 minutes of patience, and a finalization time 25 minutes later.",
    ],
    "example": "CMO",
    "description": """The CMO class represents a scheduling objective for catalog 
maintenance using a specific sensor and algorithm, related to astronomical observations or 
tracking. Catalog Maintenance specifies parameters such as the sensor's name, data mode, scheduling priority, 
timing constraints, and classification marking, providing control over how the maintenance 
task is to be executed. By allowing precise configuration of these parameters, it facilitates 
optimized scheduling in a system where timing and priority are required, such as in an observation 
or tracking environment. CMO is useful for satellite or astronomical observation planning.
""",
    "example_fields": CMO_examples,
    "base_model": CMO,
    "template": CMOTemplate,
}

pro_info = {
    "prompts": [
        "Track object 12345 with sensor RME08, revisiting four times per hour for the next 16 hours using REAL mode, 'S' markings, and set priority to 2.",
        "Monitor object 96284 with sensor UKR44 in REAL mode, plan for two revisits per hour, begin with a 12-hour outline, marked as 'TS', priority set at 3",
    ],
    "example": "PRO",
    "description": """The PRO class is designed to create a specific observation 
objective for a given target, with parameters to configure the observation process 
such as sensor name, data mode, revisit frequency, and duration. Periodic Revisit (PRO) sets an end time 
for the objective, either based on input or a default of 10 minutes from the current time, 
and includes handling for converting input string times to datetime objects. Revisit is 
useful in applications that require scheduled monitoring or tracking of specific targets 
(such as celestial objects or satellites) through designated sensors, allowing for controlled 
and periodic observations.
""",
    "example_fields": PRO_examples,
    "base_model": PRO,
    "template": PROTemplate,
}

objectives = {
    "CMO": cmo_info,
    "PRO": pro_info,
}
