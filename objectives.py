from templates import (
    CatalogMaintenanceObjective,
    CatalogMaintenanceObjectiveTemplate,
    DataEnrichmentObjective,
    DataEnrichmentObjectiveTemplate,
    PeriodicRevisitObjective,
    PeriodicRevisitObjectiveTemplate,
    SearchObjective,
    SearchObjectiveTemplate,
    SpectralClearingObjective,
    SpectralClearingObjectiveTemplate,
)

# CMO_examples = [
#     "RME00",  # sensor_name
#     "TEST",  # data_mode
#     "TS",  # classification_marking
#     30,  # patience_minutes
#     20,  # end_time_offset_minutes
#     # "Catalog Maintenance Objective",  # objective_name
#     10,  # priority
# ]

# PRO_examples = [
#     12345,  # target_id
#     "RME08",  # sensor_name
#     "REAL",  # data_mode
#     "S",  # classification_marking
#     4,  # revisits_per_hour
#     16,  # hours_to_plan
#     2,  # priority
# ]

# cmo_info = {
#     "prompts": [
#         "I need a new catalog maintenance for RME00 with TS markings and use TEST mode with a priority of 10 and set the patience to 30 minutes and end search after 20 minutes.",
#         "Make a new catalog job for sensor ABQ01 in REAL mode, marked as TS, with priority 11, 15 minutes of patience, and a finalization time 25 minutes later.",
#     ],
#     "example": "CMO",
#     "description": """The CMO class represents a scheduling objective for catalog
# maintenance using a specific sensor and algorithm, related to astronomical observations or
# tracking. Catalog Maintenance specifies parameters such as the sensor's name, data mode, scheduling priority,
# timing constraints, and classification marking, providing control over how the maintenance
# task is to be executed. By allowing precise configuration of these parameters, it facilitates
# optimized scheduling in a system where timing and priority are required, such as in an observation
# or tracking environment. CMO is useful for satellite or astronomical observation planning.
# """,
#     "example_fields": CMO_examples,
#     "base_model": CMO,
#     "template": CMOTemplate,
# }

# pro_info = {
#     "prompts": [
#         "Track object 12345 with sensor RME08, revisiting four times per hour for the next 16 hours using REAL mode, 'S' markings, and set priority to 2.",
#         "Monitor object 96284 with sensor UKR44 in REAL mode, plan for two revisits per hour, begin with a 12-hour outline, marked as 'TS', priority set at 3",
#     ],
#     "example": "PRO",
#     "description": """The PRO class is designed to create a specific observation
# objective for a given target, with parameters to configure the observation process
# such as sensor name, data mode, revisit frequency, and duration. Periodic Revisit (PRO) sets an end time
# for the objective, either based on input or a default of 10 minutes from the current time,
# and includes handling for converting input string times to datetime objects. Revisit is
# useful in applications that require scheduled monitoring or tracking of specific targets
# (such as celestial objects or satellites) through designated sensors, allowing for controlled
# and periodic observations.
# """,
#     "example_fields": PRO_examples,
#     "base_model": PRO,
#     "template": PROTemplate,
# }


cmo_examples = [
    "U",  # classification_marking
    # [],  # rso_id_list
    # "['RME02', 'LMNT01']",  # sensor_name_list
    "TEST",  # data_mode
    "RATE_TRACK_SIDEREAL",  # collect_request_type
    "LEO",  # orbital_regime
    10,  # patience_minutes
    25,  # end_time_offset_minutes
    12,  # priority
]

cmo_info = {
    "prompts": [
        "Make a new catalog maintenance for sensor RME02 with U markings and TEST mode, priority 12, patience of 10 mins, ending after 25 mins. Start at 2024-05-21 19:20:00.150000+00:00 and conclude at 2024-05-21 22:30:00.250000+00:00. Include sensor IDs RME02, LMNT01. Set RATE_TRACK_SIDEREAL for the tracking type and operate in LEO orbital regime.",
        "Schedule a new catalog task for sensor ABQ04 with REAL mode, classification marking S, priority 8, patience of 25 minutes, and an end time offset of 35 minutes. Begin on 2024-05-21 19:20:00.150000+00:00 and finish by 2024-05-21 22:30:00.250000+00:00. Use sensors ABQ04, UKR05 and set RATE_TRACK for tracking. Orbital regime is GEO.",
    ],
    "example": "CatalogMaintenanceObjective",
    "description": """The CMO class represents a scheduling objective for catalog 
maintenance using a specific sensor and algorithm, related to astronomical observations or 
tracking. Catalog Maintenance specifies parameters such as the sensor's name, data mode, scheduling priority, 
timing constraints, and classification marking, providing control over how the maintenance 
task is to be executed. By allowing precise configuration of these parameters, it facilitates 
optimized scheduling in a system where timing and priority are required, such as in an observation 
or tracking environment. CMO is useful for satellite or astronomical observation planning.
""",
    "example_fields": cmo_examples,
    "base_model": CatalogMaintenanceObjective,
    "template": CatalogMaintenanceObjectiveTemplate,
}

pro_examples = [
    "S",  # classification_marking
    # ["44248"],  # target_id_list
    # ["RME01", "LMNT45"],  # sensor_name_list
    "TEST",  # data_mode
    "RATE_TRACK_SIDEREAL",  # collect_request_type
    30,  # patience_minutes
    2.0,  # revisits_per_hour
    36.0,  # hours_to_plan
    None,  # number_of_frames
    None,  # integration_time
    1,  # binning
    2,  # priority
]

pro_info = {
    "prompts": [
        "Track object 44248 with sensors RME01 and LMNT45, revisiting twice per hour for the next 36 hours using TEST mode, 'S' markings, and set priority to 2. Begin at 2024-05-21 19:20:00.150000+00:00 and end at 2024-05-21 22:30:00.250000+00:00. Use RATE_TRACK_SIDEREAL as the collect request type and operate in LEO orbital regime.",
        "Track celestial object 21212 with sensors RME33, ABQ42, using REAL mode, revisiting four times per hour, starting execution for a 48-hour plan, marked as 'U//FOUO', with priority set to 1. Begins on 2024-05-21 19:20:00.150000+00:00 and finishes by 2024-05-21 22:30:00.250000+00:00. Employ RATE_TRACK for tracking type and GSO for orbital regime.",
    ],
    "example": "PeriodicRevisitObjective",
    "description": """The PeriodicRevisitObjective class is designed to create a specific observation
objective for a given target, with parameters to configure the observation process
such as sensor name, data mode, revisit frequency, and duration. Periodic Revisit sets an end time
for the objective, either based on input or a default of 10 minutes from the current time,
and includes handling for converting input string times to datetime objects. Revisit is
useful in applications that require scheduled monitoring or tracking of specific targets
(such as celestial objects or satellites) through designated sensors, allowing for controlled
and periodic observations.
""",
    "example_fields": pro_examples,
    "base_model": PeriodicRevisitObjective,
    "template": PeriodicRevisitObjectiveTemplate,
}

so_examples = [
    "S",  # classification_marking
    "12345",  # target_id
    "UKR12",  # sensor_name
    "REAL",  # data_mode
    "RATE_TRACK_SIDEREAL",  # collect_request_type
    60,  # initial_offset
    90,  # final_offset
    70.0,  # frame_overlap_percentage
    8,  # number_of_frames
    2,  # integration_time
    2,  # binning
    5,  # priority
    45,  # end_time_offset_minutes
]

so_info = {
    "prompts": [
        "Create a new search objective for target 12345 using sensor UKR12 with S marking and REAL data mode, priority set to 5, and collect request type RATE_TRACK_SIDEREAL. Start the objective at 2024-05-22 09:30:00.000000+00:00 and end at 2024-05-22 11:00:00.000000+00:00. Set initial offset to 60 and final offset to 90, frame overlap percentage to 70%, number of frames to 8, integration time to 2 seconds, binning to 2, and end time offset to 45 minutes.",
    ],
    "example": "SearchObjective",
    "description": """The SearchObjective class represents a scheduling objective for astronomical search or tracking using a specific sensor and algorithm. It specifies parameters such as the target ID, sensor name, data mode, scheduling priority, timing constraints, and classification marking, providing control over how the search or tracking task is to be executed. By allowing precise configuration of these parameters, it facilitates optimized scheduling in a system where timing and priority are required, such as in an observation or tracking environment. SearchObjective is useful for satellite or astronomical observation planning.
""",
    "example_fields": so_examples,
    "base_model": SearchObjective,
    "template": SearchObjectiveTemplate,
}

deo_examples = [
    "U//FOUO",  # classification_marking
    "REAL",  # data_mode
    "RATE_TRACK",  # collect_request_type
    8,  # max_rso_to_observe
    10.0,  # revisits_per_hour
    48.0,  # hours_to_plan
    15,  # priority
]

deo_info = {
    "prompts": [
        "Create a data enrichment objective for targets 12345, 67890, and 54321 using sensors ABC01, DEF02, and GHI03. Set the classification marking to 'U//FOUO', data mode to 'REAL', and collect request type to 'RATE_TRACK'. Observe a maximum of 8 RSOs with 10 revisits per hour, planning for 48 hours. Start the objective at 2024-06-01 08:00:00.000000+00:00 and end at 2024-06-03 08:00:00.000000+00:00. Set the priority to 15.",
    ],
    "example": "DataEnrichmentObjective",
    "description": """The Data Enrichment Objective (DataEnrichmentObjective) class represents a scheduling objective for data enrichment tasks related to observing and tracking resident space objects (RSOs). It allows the specification of parameters such as classification marking, data mode, collect request type, maximum RSOs to observe, revisits per hour, hours to plan, and priority. The DataEnrichmentObjective class optimizes scheduling and prioritizes objectives within time constraints. The deo_examples list provides an example of field values for a specific objective. The DataEnrichmentObjectiveTemplate class is a template version with optional fields for flexibility. DEO is relevant in scenarios involving satellite tracking, space situational awareness, and astronomical observations.
""",
    "example_fields": deo_examples,
    "base_model": DataEnrichmentObjective,
    "template": DataEnrichmentObjectiveTemplate,
}

sco_examples = [
    "S",  # classification_marking
    "REAL",  # data_mode
    "RATE_TRACK_SIDEREAL",  # collect_request_type (defaults to 'RATE_TRACK_SIDEREAL')
    60,  # patience_minutes
    15,  # target_total_obs (total frames per intent)
    15,  # number_of_frames
    1.5,  # integration_time
    2,  # binning
    8,  # priority
]

sco_info = {
    "prompts": [
        "Create a spectral clearing objective for targets 78901 and 23456 using sensors LMNT02 and UKR05 with S markings and REAL mode, priority set to 8. Start the objective at 2024-06-01 09:30:00.000000+00:00 and end at 2024-06-02 18:15:00.000000+00:00. Set the patience to 60 minutes, and run integration at 1.5 seconds per frame for 15 total frames per intent, using a binning of 2."
    ],
    "example": "SpectralClearingObjective",
    "description": """The SpectralClearingObjective class defines a scheduling objective for spectral clearing observations. It allows configuring parameters such as classification marking, data mode, collection request type, patience time, number of observations, integration time, binning, and priority. This facilitates optimized scheduling for spectral analysis tasks in astronomical or satellite observation systems. The class includes fields for specifying target objects, sensors, and observation time windows. The SpectralClearingObjectiveTemplate class serves as a template for creating instances with optional field values, enabling flexibility in defining objectives. Overall, the class provides a structured way to manage and execute spectral clearing tasks efficiently.
""",
    "example_fields": sco_examples,
    "base_model": SpectralClearingObjective,
    "template": SpectralClearingObjectiveTemplate,
}

objectives = {
    "CatalogMaintenanceObjective": cmo_info,
    "PeriodicRevisitObjective": pro_info,
    "SearchObjective": so_info,
    "DataEnrichmentObjective": deo_info,
    "SpectralClearingObjective": sco_info,
}
