from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, ValidationError

time_desciption = """The general structure of the datetime format is:
YYYY-MM-DD HH:MM:SS.ssssss+HH:MM
where:
YYYY is the year
MM is the month
DD is the day
HH is the hour (24-hour format)
MM is the minutes
SS is the seconds
ssssss is the microseconds
+HH:MM is the UTC offset (+ for positive offset, - for negative offset)"""


class ObjectiveModel(BaseModel):
    objective: str


class ObjectiveTime(BaseModel):
    objective_start_time: Union[datetime, str] = Field(
        default=None,
        description="The earliest time when objective should begin execution. In 'YYYY-MM-DD HH:MM:SS.ssssss+HH:MM' format",
    )
    objective_end_time: Union[datetime, str] = Field(
        default=None,
        description="The time when the objective should end execution. In 'YYYY-MM-DD HH:MM:SS.ssssss+HH:MM' format",
    )


class ObjectiveTimeTemplate(BaseModel):
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None


class ObjectiveList(BaseModel):
    rso_id_list: list[str] = Field(
        description="list[str]: List of UUIDs of RSO to keep track of."
    )
    sensor_name_list: list[str] = Field(
        description="list[str]: List of string names of Sensors to perform Objective with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99."
    )
    target_id_list: list[str] = Field(
        description="list[str]: List of belief state UUID's of Targets."
    )


class ObjectiveListTemplate(BaseModel):
    rso_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    target_id_list: Optional[list[str]] = None


class CMO_ObjectiveList(BaseModel):
    target_id_list: list[str] = Field(
        description="list[str]: List of belief state UUID's of Targets."
    )
    sensor_name_list: list[str] = Field(
        description="list[str]: List of string names of Sensors to perform Objective with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99."
    )


class CMO_ObjectiveListTemplate(BaseModel):
    target_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None


class PRO_ObjectiveList(BaseModel):
    target_id_list: list[str] = Field(
        description="list[str]: List of belief state UUID's of Targets."
    )
    sensor_name_list: list[str] = Field(
        description="list[str]: List of string names of Sensors to perform Objective with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99."
    )


class PRO_ObjectiveListTemplate(BaseModel):
    target_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None


class Foo(BaseModel):
    foo_name: str = Field(description="Name of the foo.")
    foo_id: str = Field(description="ID of the foo, usually 3 digits.")


class FooTemplate(BaseModel):
    foo_name: Optional[str] = None
    foo_id: Optional[str] = None


class Marking(str, Enum):
    unclassified = "U"
    classified = "C"
    secret = "S"
    top_secret = "TS"
    fouo = "U//FOUO"


def parse_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as e:
        raise ValidationError([str(e)])


class CatalogMaintenanceObjective(BaseModel):
    classification_marking: str = Field(
        description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'"
    )
    data_mode: str = Field(
        description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'."
    )
    collect_request_type: str = Field(
        description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'."
    )
    orbital_regime: str = Field(
        description="str: String enum of orbital regime for this catalog maintenance objective. One of: 'LEO', 'MEO', 'GEO', 'XGEO'."
    )
    patience_minutes: int = Field(
        description="patience_minutes: default=30. Amount of time to wait until it is assumed that an intent failed."
    )
    end_time_offset_minutes: int = Field(
        description="end_time_offset_minutes: default=20. Amount of minutes into the future to schedule this intent."
    )
    # objective_name: str = None
    # objective_start_time: Union[datetime, str] = None
    # objective_end_time: Union[datetime, str] = None
    priority: int = Field(
        description="int: default=1000. This is the set priority, defaults to 999 (1000th highest priority)."
    )


class CatalogMaintenanceObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    rso_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    orbital_regime: Optional[str] = None
    patience_minutes: Optional[Union[int, str]] = None
    end_time_offset_minutes: Optional[Union[int, str]] = None
    objective_name: Optional[str] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    priority: Optional[Union[int, str]] = None


class PeriodicRevisitObjective(BaseModel):
    classification_marking: str = Field(
        description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'"
    )
    data_mode: str = Field(
        description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'."
    )
    collect_request_type: str = Field(
        description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'."
    )
    patience_minutes: int = Field(
        description="patience_minutes: default=30. Amount of time to wait until it is assumed that an intent failed. If not provided by user, please set to default value of 30."
    )
    revisits_per_hour: float = Field(
        default=1.0,
        description="float: default=1. Desired number of times to revisit and observe each target per hour.",
    )
    hours_to_plan: float = Field(
        default=24.0, description="float: default=24. Maximum hours to plan."
    )
    number_of_frames: int = Field(
        description="int: amount of frames per intent. Defaults to None."
    )
    integration_time: float = Field(
        description="float: Seconds of integration time per frame. Defaults to None."
    )
    binning: int = Field(default=1, description="int: camera binning. Defaults to 1. If not provided by user, please set to default value of 1.")
    # objective_start_time: datetime = None,
    # objective_end_time: datetime = None,
    priority: int = Field(
        default=10,
        description="int: default=10. This is the set priority, defaults to 10 (11th highest priority).",
    )


class PeriodicRevisitObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    patience_minutes: Optional[Union[int, str]] = None
    revisits_per_hour: Optional[Union[float, str]] = None
    hours_to_plan: Optional[Union[float, str]] = None
    number_of_frames: Optional[Union[int, str]] = None
    integration_time: Optional[Union[float, str]] = None
    binning: Optional[Union[int, str]] = None
    objective_name: Optional[str] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    priority: Optional[Union[int, str]] = None


class SearchObjective(BaseModel):
    classification_marking: str = Field(
        description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'"
    )
    target_id: str = Field(description="str: 5 Digit integer RSO satcat id.")
    sensor_name: str = Field(
        description="sensor_name: string name of sensor to perform search with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99."
    )
    data_mode: str = Field(
        description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'."
    )
    collect_request_type: str = Field(
        description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'."
    )
    initial_offset: int = Field(
        description="int: Amount of time before the RSO's current state to start the search at (s). Defaults to 30. Max is 1800."
    )
    final_offset: int = Field(
        description="int: Amount of time after the RSO's current state to start the search at (s). Defaults to 30. Max is 1800."
    )
    frame_overlap_percentage: float = Field(
        description="float: Percentage of frames that will overlap from one to the next. Defaults to 50."
    )
    number_of_frames: int = Field(
        description="int: amount of frames per intent. Defaults to None."
    )
    integration_time: int = Field(
        description="int: Seconds of integration time per frame. Defaults to None."
    )
    binning: int = Field(description="int: camera binning. Defaults to 1.")
    priority: int = Field(
        default=1,
        description="int: default=10. This is the set priority, defaults to 1 (2nd highest priority).",
    )
    end_time_offset_minutes: int = Field(
        description="int: amount of minutes into the future to let astroplan schedule an intent. Defaults to 20 minutes."
    )


class SearchObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id: Optional[str] = None
    sensor_name: Optional[str] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    initial_offset: Optional[int] = None
    final_offset: Optional[Union[int, str]] = None
    objective_name: Optional[str] = None
    frame_overlap_percentage: Optional[Union[float, str]] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    number_of_frames: Optional[Union[int, str]] = None
    integration_time: Optional[Union[int, str]] = None
    binning: Optional[Union[int, str]] = None
    priority: Optional[Union[int, str]] = None
    end_time_offset_minutes: Optional[Union[int, str]] = None


class DataEnrichmentObjective(BaseModel):
    classification_marking: str = Field(
        description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'"
    )
    # target_id_list: list[str] = Field(description="XXX")
    # sensor_name_list: list[str] = Field(description="XXX")
    data_mode: str = Field(
        description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'."
    )
    collect_request_type: str = Field(
        description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'."
    )
    max_rso_to_observe: int = Field(
        description="int: Number of RSO to observe. Defaults to 6."
    )
    revisits_per_hour: float = Field(
        description="float: Desired number of times to observe each target each hour. Defaults to 12.0"
    )
    hours_to_plan: float = Field(
        description="float: Maximum hours to plan. Defaults to 24.0."
    )
    # objective_name: str = Field(description="XXX")
    priority: int = Field(
        default=20,
        description="int: default=20. This is the set priority, defaults to 20 (21th highest priority).",
    )


class DataEnrichmentObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    max_rso_to_observe: Optional[Union[int, str]] = None
    revisits_per_hour: Optional[Union[float, str]] = None
    hours_to_plan: Optional[Union[float, str]] = None
    objective_name: Optional[str] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    priority: Optional[Union[int, str]] = None


class SpectralClearingObjective(BaseModel):
    classification_marking: str = Field(
        description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'"
    )
    # target_id_list: list[str] = Field(description="XXX")
    # sensor_name_list: list[str] = Field(description="XXX")
    data_mode: str = Field(
        description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'."
    )
    collect_request_type: str = Field(
        description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'. If not provided by user, please set to default value of RATE_TRACK_SIDEREAL."
    )
    patience_minutes: int = Field(
        description="patience_minutes: default=30. Amount of time to wait until it is assumed that an intent failed."
    )
    target_total_obs: int = Field(
        description="int: total target observations. Defaults to 50."
    )
    # TODO: Fields that default to None and are NOT required -- should make these Optional / check that Optional Nones are OK
    number_of_frames: Optional[int] = Field(
        description="int: amount of frames per intent. Defaults to None."
    )
    integration_time: Optional[float] = Field(
        description="float: Seconds of integration time per frame. Defaults to None."
    )
    binning: int = Field(description="int: camera binning. Defaults to 1.")
    # objective_name: str = Field(description="XXX")
    priority: int = Field(
        default=10,
        description="int: default=10. This is the set priority, defaults to 10 (11th highest priority).",
    )


class SpectralClearingObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    patience_minutes: Optional[Union[int, str]] = None
    target_total_obs: Optional[Union[int, str]] = None
    number_of_frames: Optional[Union[int, str]] = None
    integration_time: Optional[Union[float, str]] = None
    binning: Optional[Union[int, str]] = None
    objective_name: Optional[str] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    priority: Optional[Union[int, str]] = None


# class SingleIntentObjective(BaseModel):
#     classification_marking: str = Field(description="XXX")
#     target_id: str = Field(description="XXX")
#     data_mode: str = Field(description="XXX")
#     collect_request_type: str = Field(description="XXX")
#     sensor_name: str = Field(description="XXX")
#     number_of_frames: int = Field(description="XXX")
#     integration_time: float = Field(description="XXX")
#     binning: int = Field(description="XXX")
#     objective_name: str = Field(description="XXX")
#     priority: int = Field(description="XXX")


# class SingleIntentObjectiveTemplate(BaseModel):
#     classification_marking: Optional[str] = None
#     target_id: Optional[str] = None
#     data_mode: Optional[str] = None
#     collect_request_type: Optional[str] = None
#     sensor_name: Optional[str] = None
#     number_of_frames: Optional[int] = None
#     integration_time: Optional[float] = None
#     binning: Optional[int] = None
#     # intent_start_time: datetime = None,
#     # intent_end_time: datetime = None,
#     objective_name: Optional[str] = None
#     priority: Optional[int] = None


# Prompt 1
maintenance_1 = CatalogMaintenanceObjectiveTemplate(
    classification_marking="U",
    data_mode="TEST",
    collect_request_type="RATE_TRACK_SIDEREAL",
    orbital_regime="LEO",
    patience_minutes=10,
    end_time_offset_minutes=25,
    priority=12,
    sensor_name_list=["RME02", "LMNT01"],
    # TODO: Check if we want to use [] or None?
    rso_id_list=[],
    objective_name="CatalogMaintenanceObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
)

# Prompt 2
maintenance_2 = CatalogMaintenanceObjectiveTemplate(
    classification_marking="S",
    data_mode="REAL",
    collect_request_type="RATE_TRACK",
    orbital_regime="GEO",
    patience_minutes=25,
    end_time_offset_minutes=35,
    priority=8,
    sensor_name_list=["ABQ04", "UKR05"],
    rso_id_list=[],
    objective_name="CatalogMaintenanceObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
)

# Prompt 3
maintenance_3 = CatalogMaintenanceObjectiveTemplate(
    classification_marking="C",
    data_mode="TEST",
    collect_request_type="SIDEREAL",
    orbital_regime="MEO",
    patience_minutes=15,
    end_time_offset_minutes=40,
    priority=12,
    sensor_name_list=["UKR07", "RME04"],
    rso_id_list=[],
    objective_name="CatalogMaintenanceObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
)

# Prompt 4
maintenance_4 = CatalogMaintenanceObjectiveTemplate(
    classification_marking="U",
    data_mode="REAL",
    collect_request_type="RATE_TRACK_SIDEREAL",
    orbital_regime="XGEO",
    patience_minutes=30,
    end_time_offset_minutes=45,
    priority=18,
    sensor_name_list=["RME12", "ABQ09"],
    rso_id_list=[],
    objective_name="CatalogMaintenanceObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
)

# Prompt 5
maintenance_5 = CatalogMaintenanceObjectiveTemplate(
    classification_marking="TS",
    data_mode="TEST",
    collect_request_type="RATE_TRACK",
    orbital_regime="LEO",
    patience_minutes=30,
    end_time_offset_minutes=20,
    priority=10,
    sensor_name_list=["LMNT05", "LMNT06"],
    rso_id_list=[],
    objective_name="CatalogMaintenanceObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time=datetime.fromisoformat("2024-05-21T22:30:00.250000+00:00"),
)

# Prompt 6
maintenance_6 = CatalogMaintenanceObjectiveTemplate(
    classification_marking="S",
    data_mode="TEST",
    collect_request_type="RATE_TRACK_SIDEREAL",
    orbital_regime="GEO",
    patience_minutes=20,
    end_time_offset_minutes=30,
    priority=13,
    sensor_name_list=["LMNT11", "RME16"],
    rso_id_list=[],
    objective_name="CatalogMaintenanceObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
)

# Prompt 7
maintenance_7 = CatalogMaintenanceObjectiveTemplate(
    classification_marking="U//FOUO",
    data_mode="REAL",
    collect_request_type="SIDEREAL",
    orbital_regime="MEO",
    patience_minutes=50,
    end_time_offset_minutes=70,
    priority=14,
    sensor_name_list=["RME15", "UKR03"],
    rso_id_list=[],
    objective_name="CatalogMaintenanceObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
)

# Prompt 1 revisit
revisit_1 = PeriodicRevisitObjectiveTemplate(
    classification_marking="S",
    target_id_list=["44248"],
    sensor_name_list=["RME01", "LMNT45"],
    data_mode="TEST",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=30,
    revisits_per_hour=2.0,
    hours_to_plan=36.0,
    number_of_frames=5,
    integration_time=2,
    binning=1,
    objective_name="PeriodicRevisitObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
    priority=2,
)

# Prompt 2
revisit_2 = PeriodicRevisitObjectiveTemplate(
    classification_marking="U//FOUO",
    target_id_list=["21212"],
    sensor_name_list=["RME33", "ABQ42"],
    data_mode="REAL",
    collect_request_type="RATE_TRACK",
    patience_minutes=30,
    revisits_per_hour=4.0,
    hours_to_plan=48.0,
    number_of_frames=10,
    integration_time=1,
    binning=1,
    objective_name="PeriodicRevisitObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
    priority=1,
)

# Prompt 3
revisit_3 = PeriodicRevisitObjectiveTemplate(
    classification_marking="C",
    target_id_list=["43567"],
    sensor_name_list=["ABQ42", "UKR88"],
    data_mode="TEST",
    collect_request_type="SIDEREAL",
    patience_minutes=30,
    revisits_per_hour=4.0,
    hours_to_plan=36.0,
    number_of_frames=12,
    integration_time=4,
    binning=1,
    objective_name="PeriodicRevisitObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
    priority=3,
)

# Prompt 4
revisit_4 = PeriodicRevisitObjectiveTemplate(
    classification_marking="U//FOUO",
    target_id_list=["20394"],
    sensor_name_list=["UKR88", "RME02"],
    data_mode="REAL",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=30,
    revisits_per_hour=5.0,
    hours_to_plan=42.0,
    number_of_frames=3,
    integration_time=10,
    binning=1,
    objective_name="PeriodicRevisitObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
    priority=3,
)

# Prompt 5
revisit_5 = PeriodicRevisitObjectiveTemplate(
    classification_marking="S",
    target_id_list=["31705"],
    sensor_name_list=["LMNT33", "RME99"],
    data_mode="REAL",
    collect_request_type="RATE_TRACK",
    patience_minutes=30,
    revisits_per_hour=3.0,
    hours_to_plan=24.0,
    number_of_frames=16,
    integration_time=20,
    binning=1,
    objective_name="PeriodicRevisitObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
    priority=1,
)

# Prompt 6
revisit_6 = PeriodicRevisitObjectiveTemplate(
    classification_marking="C",
    target_id_list=["84123"],
    sensor_name_list=["RME02", "ABQ01"],
    data_mode="TEST",
    collect_request_type="SIDEREAL",
    patience_minutes=30,
    revisits_per_hour=6.0,
    hours_to_plan=12.0,
    number_of_frames=32,
    integration_time=5,
    binning=1,
    objective_name="PeriodicRevisitObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
    priority=2,
)

# Prompt 7
revisit_7 = PeriodicRevisitObjectiveTemplate(
    classification_marking="C",
    target_id_list=["43567"],
    sensor_name_list=["ABQ42", "LMNT22"],
    data_mode="TEST",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=30,
    revisits_per_hour=1.0,
    hours_to_plan=30.0,
    number_of_frames=2,
    integration_time=3,
    binning=1,
    objective_name="PeriodicRevisitObjectiveTemplate",
    objective_start_time="2024-05-21T19:20:00.150000+00:00",
    objective_end_time="2024-05-21T22:30:00.250000+00:00",
    priority=5,
)

# search prompts
search_1 = SearchObjectiveTemplate(
    classification_marking="S",
    target_id="12345",
    sensor_name="UKR12",
    data_mode="REAL",
    collect_request_type="RATE_TRACK_SIDEREAL",
    initial_offset=60,
    final_offset=90,
    frame_overlap_percentage=70,
    objective_name="SearchObjectiveTemplate",
    objective_start_time="2024-05-22T09:30:00.000000+00:00",
    objective_end_time="2024-05-22T11:00:00.000000+00:00",
    number_of_frames=8,
    integration_time=2,
    binning=2,
    priority=5,
    end_time_offset_minutes=45,
)

search_2 = SearchObjectiveTemplate(
    classification_marking="TS",
    target_id="98765",
    sensor_name="ABQ03",
    data_mode="EXERCISE",
    collect_request_type="RATE_TRACK",
    initial_offset=50,
    final_offset=80,
    frame_overlap_percentage=55,
    objective_name="SearchObjectiveTemplate",
    objective_start_time="2024-05-23T06:15:00.000000+00:00",
    objective_end_time="2024-05-23T08:45:00.000000+00:00",
    number_of_frames=10,
    integration_time=3,
    binning=1,
    priority=3,
    end_time_offset_minutes=30,
)

search_3 = SearchObjectiveTemplate(
    classification_marking="U//FOUO",
    target_id="54321",
    sensor_name="LMNT06",
    data_mode="SIMULATED",
    collect_request_type="SIDEREAL",
    initial_offset=30,
    final_offset=45,
    frame_overlap_percentage=65,
    objective_name="SearchObjectiveTemplate",
    objective_start_time="2024-05-24T00:00:00.000000+00:00",
    objective_end_time="2024-05-24T02:30:00.000000+00:00",
    number_of_frames=6,
    integration_time=2,
    binning=3,
    priority=7,
    end_time_offset_minutes=20,
)

search_4 = SearchObjectiveTemplate(
    classification_marking="U",
    target_id="11111",
    sensor_name="RME99",
    data_mode="TEST",
    collect_request_type="RATE_TRACK_SIDEREAL",
    initial_offset=40,
    final_offset=70,
    frame_overlap_percentage=60,
    objective_name="SearchObjectiveTemplate",
    objective_start_time="2024-05-25T10:00:00.000000+00:00",
    objective_end_time="2024-05-25T12:15:00.000000+00:00",
    number_of_frames=7,
    integration_time=1,
    binning=None,
    priority=10,
    end_time_offset_minutes=25,
)

search_5 = SearchObjectiveTemplate(
    classification_marking="C",
    target_id="22222",
    sensor_name="ABQ77",
    data_mode="REAL",
    collect_request_type="RATE_TRACK",
    initial_offset=35,
    final_offset=55,
    frame_overlap_percentage=50,
    objective_name="SearchObjectiveTemplate",
    objective_start_time="2024-05-26T15:30:00.000000+00:00",
    objective_end_time="2024-05-26T18:00:00.000000+00:00",
    number_of_frames=9,
    integration_time=4,
    binning=2,
    priority=4,
    end_time_offset_minutes=40,
)

search_6 = SearchObjectiveTemplate(
    classification_marking="S",
    target_id="33333",
    sensor_name="LMNT22",
    data_mode="EXERCISE",
    collect_request_type="SIDEREAL",
    initial_offset=45,
    final_offset=75,
    frame_overlap_percentage=55,
    objective_name="SearchObjectiveTemplate",
    objective_start_time="2024-05-27T06:00:00.000000+00:00",
    objective_end_time="2024-05-27T09:15:00.000000+00:00",
    number_of_frames=8,
    integration_time=3,
    binning=1,
    priority=8,
    end_time_offset_minutes=35,
)

search_7 = SearchObjectiveTemplate(
    classification_marking="TS",
    target_id="44444",
    sensor_name="UKR55",
    data_mode="SIMULATED",
    collect_request_type="RATE_TRACK_SIDEREAL",
    initial_offset=50,
    final_offset=90,
    frame_overlap_percentage=65,
    objective_name="SearchObjectiveTemplate",
    objective_start_time="2024-05-28T12:00:00.000000+00:00",
    objective_end_time="2024-05-28T14:30:00.000000+00:00",
    number_of_frames=10,
    integration_time=2,
    binning=None,
    priority=2,
    end_time_offset_minutes=30,
)

search_8 = SearchObjectiveTemplate(
    classification_marking="U//FOUO",
    target_id="55555",
    sensor_name="RME11",
    data_mode="TEST",
    collect_request_type="RATE_TRACK",
    initial_offset=60,
    final_offset=80,
    frame_overlap_percentage=70,
    objective_name="SearchObjectiveTemplate",
    objective_start_time="2024-05-29T18:45:00.000000+00:00",
    objective_end_time="2024-05-30T00:00:00.000000+00:00",
    number_of_frames=7,
    integration_time=1,
    binning=3,
    priority=6,
    end_time_offset_minutes=45,
)

# enrichment prompts
enrichment_1 = DataEnrichmentObjectiveTemplate(
    classification_marking="U//FOUO",
    target_id_list=["12345", "67890", "54321"],
    sensor_name_list=["RME01", "LMNT02", "ABQ03"],
    data_mode="REAL",
    collect_request_type="RATE_TRACK",
    max_rso_to_observe=8,
    revisits_per_hour=10,
    hours_to_plan=48,
    objective_name="DataEnrichmentObjectiveTemplate",
    objective_start_time="2024-06-01T08:00:00.000000+00:00",
    objective_end_time="2024-06-03T08:00:00.000000+00:00",
    priority=15,
)

enrichment_2 = DataEnrichmentObjectiveTemplate(
    classification_marking="TS",
    target_id_list=["98765", "43210"],
    sensor_name_list=["UKR01"],
    data_mode="EXERCISE",
    collect_request_type="SIDEREAL",
    max_rso_to_observe=5,
    revisits_per_hour=15,
    hours_to_plan=18,
    objective_name="DataEnrichmentObjectiveTemplate",
    objective_start_time="2024-07-15T18:30:00.250000+00:00",
    objective_end_time="2024-07-16T06:30:00.250000+00:00",
    priority=25,
)

enrichment_3 = DataEnrichmentObjectiveTemplate(
    classification_marking="S",
    target_id_list=["13579", "24680"],
    sensor_name_list=["RME04", "LMNT05"],
    data_mode="TEST",
    collect_request_type="RATE_TRACK_SIDEREAL",
    max_rso_to_observe=None,
    revisits_per_hour=8,
    hours_to_plan=30,
    objective_name="DataEnrichmentObjectiveTemplate",
    objective_start_time="2024-08-10T09:45:00.500000+00:00",
    objective_end_time="2024-08-11T21:45:00.500000+00:00",
    priority=None,
)

enrichment_4 = DataEnrichmentObjectiveTemplate(
    classification_marking="C",
    target_id_list=["11111", "22222", "33333", "44444"],
    sensor_name_list=["ABQ06", "UKR07", "RME08"],
    data_mode="SIMULATED",
    collect_request_type="RATE_TRACK",
    max_rso_to_observe=7,
    revisits_per_hour=20,
    hours_to_plan=16,
    objective_name="DataEnrichmentObjectiveTemplate",
    objective_start_time="2024-09-05T12:00:00.750000+00:00",
    objective_end_time="2024-09-06T00:00:00.750000+00:00",
    priority=18,
)

enrichment_5 = DataEnrichmentObjectiveTemplate(
    classification_marking="U",
    target_id_list=["55555"],
    sensor_name_list=["LMNT09"],
    data_mode="REAL",
    collect_request_type="SIDEREAL",
    max_rso_to_observe=None,
    revisits_per_hour=10,
    hours_to_plan=40,
    objective_name="DataEnrichmentObjectiveTemplate",
    objective_start_time="2024-10-20T03:15:00.000000+00:00",
    objective_end_time="2024-10-21T15:15:00.000000+00:00",
    priority=22,
)

enrichment_6 = DataEnrichmentObjectiveTemplate(
    classification_marking="U//FOUO",
    target_id_list=["66666", "77777"],
    sensor_name_list=["RME10", "ABQ11"],
    data_mode="EXERCISE",
    collect_request_type="RATE_TRACK_SIDEREAL",
    max_rso_to_observe=4,
    revisits_per_hour=18,
    hours_to_plan=20,
    objective_name="DataEnrichmentObjectiveTemplate",
    objective_start_time="2024-11-11T16:30:00.250000+00:00",
    objective_end_time="2024-11-12T04:30:00.250000+00:00",
    priority=19,
)

enrichment_7 = DataEnrichmentObjectiveTemplate(
    classification_marking="TS",
    target_id_list=["88888", "99999", "00000"],
    sensor_name_list=["UKR12", "LMNT13", "RME14"],
    data_mode="TEST",
    collect_request_type="RATE_TRACK",
    max_rso_to_observe=9,
    revisits_per_hour=6,
    hours_to_plan=42,
    objective_name="DataEnrichmentObjectiveTemplate",
    objective_start_time="2024-12-01T06:45:00.500000+00:00",
    objective_end_time="2024-12-02T18:45:00.500000+00:00",
    priority=23,
)

enrichment_8 = DataEnrichmentObjectiveTemplate(
    classification_marking="S",
    target_id_list=["12121"],
    sensor_name_list=["ABQ15"],
    data_mode="SIMULATED",
    collect_request_type="SIDEREAL",
    max_rso_to_observe=None,
    revisits_per_hour=14,
    hours_to_plan=14,
    objective_name="DataEnrichmentObjectiveTemplate",
    objective_start_time="2025-01-15T20:00:00.750000+00:00",
    objective_end_time="2025-01-16T08:00:00.750000+00:00",
    priority=None,
)


# Spectral prompts, spectral
spectral_1 = SpectralClearingObjectiveTemplate(
    classification_marking="S",
    target_id_list=["78901", "23456"],
    sensor_name_list=["LMNT02", "UKR05"],
    data_mode="REAL",
    patience_minutes=60,
    target_total_obs=None,
    number_of_frames=15,
    integration_time=1.5,
    binning=2,
    objective_name="SpectralClearingObjectiveTemplate",
    objective_start_time="2024-06-01T09:30:00.000000+00:00",
    objective_end_time="2024-06-02T18:15:00.000000+00:00",
    priority=8,
)


spectral_2 = SpectralClearingObjectiveTemplate(
    classification_marking="U//FOUO",
    target_id_list=["13579"],
    sensor_name_list=["RME01"],
    data_mode="SIMULATED",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=20,
    target_total_obs=None,
    number_of_frames=8,
    integration_time=3,
    binning=1,
    objective_name="SpectralClearingObjectiveTemplate",
    objective_start_time="2024-07-15T16:45:00.000000+00:00",
    objective_end_time="2024-07-16T02:30:00.000000+00:00",
    priority=12,
)


spectral_3 = SpectralClearingObjectiveTemplate(
    classification_marking="C",
    target_id_list=["98765", "43210"],
    sensor_name_list=["ABQ02", "RME04"],
    data_mode="TEST",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=90,
    target_total_obs=None,
    number_of_frames=10,
    integration_time=2.5,
    binning=4,
    objective_name="SpectralClearingObjectiveTemplate",
    objective_start_time="2024-08-10T11:00:00.000000+00:00",
    objective_end_time="2024-08-11T09:15:00.000000+00:00",
    priority=6,
)


spectral_4 = SpectralClearingObjectiveTemplate(
    classification_marking="U",
    target_id_list=["56789"],
    sensor_name_list=["LMNT01", "UKR03"],
    data_mode="REAL",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=30,
    target_total_obs=None,
    number_of_frames=20,
    integration_time=1.8,
    binning=3,
    objective_name="SpectralClearingObjectiveTemplate",
    objective_start_time="2024-09-05T19:30:00.000000+00:00",
    objective_end_time="2024-09-06T07:45:00.000000+00:00",
    priority=14,
)


spectral_5 = SpectralClearingObjectiveTemplate(
    classification_marking="TS",
    target_id_list=["24680", "13579"],
    sensor_name_list=["RME02", "ABQ03"],
    data_mode="EXERCISE",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=75,
    target_total_obs=None,
    number_of_frames=18,
    integration_time=2.2,
    binning=1,
    objective_name="SpectralClearingObjectiveTemplate",
    objective_start_time="2024-10-20T08:15:00.000000+00:00",
    objective_end_time="2024-10-21T17:30:00.000000+00:00",
    priority=9,
)


spectral_6 = SpectralClearingObjectiveTemplate(
    classification_marking="C",
    target_id_list=["97531"],
    sensor_name_list=["LMNT04"],
    data_mode="SIMULATED",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=50,
    target_total_obs=None,
    number_of_frames=25,
    integration_time=1.2,
    binning=2,
    objective_name="SpectralClearingObjectiveTemplate",
    objective_start_time="2024-11-12T14:00:00.000000+00:00",
    objective_end_time="2024-11-13T03:45:00.000000+00:00",
    priority=11,
)

spectral_7 = SpectralClearingObjectiveTemplate(
    classification_marking="S",
    target_id_list=["86420", "75319"],
    sensor_name_list=["UKR02", "RME05"],
    data_mode="TEST",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=40,
    target_total_obs=None,
    number_of_frames=14,
    integration_time=2.8,
    binning=4,
    objective_name="SpectralClearingObjectiveTemplate",
    objective_start_time="2024-12-08T10:45:00.000000+00:00",
    objective_end_time="2024-12-09T22:30:00.000000+00:00",
    priority=7,
)

spectral_8 = SpectralClearingObjectiveTemplate(
    classification_marking="U//FOUO",
    target_id_list=["19753"],
    sensor_name_list=["ABQ04"],
    data_mode="REAL",
    collect_request_type="RATE_TRACK_SIDEREAL",
    patience_minutes=25,
    target_total_obs=None,
    number_of_frames=6,
    integration_time=3.5,
    binning=1,
    objective_name="SpectralClearingObjectiveTemplate",
    objective_start_time="2025-01-03T18:00:00.000000+00:00",
    objective_end_time="2025-01-04T06:15:00.000000+00:00",
    priority=13,
)


gt_catalog_maintenace = [
    maintenance_1,
    maintenance_2,
    maintenance_3,
    maintenance_4,
    maintenance_5,
    maintenance_6,
    maintenance_7,
]

gt_periodic_revisit = [
    revisit_1,
    revisit_2,
    revisit_3,
    revisit_4,
    revisit_5,
    revisit_6,
    revisit_7,
]

gt_search = [
    search_1,
    search_2,
    search_3,
    search_4,
    search_5,
    search_6,
    search_7,
    search_8,
]

gt_enrichment = [
    enrichment_1,
    enrichment_2,
    enrichment_3,
    enrichment_4,
    enrichment_5,
    enrichment_6,
    enrichment_7,
    enrichment_8,
]

gt_spectral = [
    spectral_1,
    spectral_2,
    spectral_3,
    spectral_4,
    spectral_5,
    spectral_6,
    spectral_7,
    spectral_8,
]

objective_to_schema = {
    "CatalogMaintenanceObjective": gt_catalog_maintenace,
    "PeriodicRevisitObjective": gt_periodic_revisit,
    "SearchObjective": gt_search,
    "DataEnrichmentObjective": gt_enrichment,
    "SpectralClearingObjective": gt_spectral,
}
