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
    # objective_name: Optional[str] = None
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
        description="patience_minutes: default=30. Amount of time to wait until it is assumed that an intent failed."
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
    binning: int = Field(default=1, description="int: camera binning. Defaults to 1.")
    # objective_name: Optional[str] = None
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
    # objective_name: Optional[str] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    priority: Optional[Union[int, str]] = None


class SearchObjective(BaseModel):
    classification_marking: str = Field(description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'")
    target_id: str = Field(description="str: 5 Digit integer RSO satcat id.")
    sensor_name: str = Field(description="sensor_name: string name of sensor to perform search with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99.")
    data_mode: str = Field(description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'.")
    collect_request_type: str = Field(description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'.")
    initial_offset: int = Field(description="int: Amount of time before the RSO's current state to start the search at (s). Defaults to 30. Max is 1800.")
    final_offset: int = Field(description="int: Amount of time after the RSO's current state to start the search at (s). Defaults to 30. Max is 1800.")
    frame_overlap_percentage: float = Field(description="float: Percentage of frames that will overlap from one to the next. Defaults to 50.")
    number_of_frames: int = Field(description="int: amount of frames per intent. Defaults to None.")
    integration_time: int = Field(description="int: Seconds of integration time per frame. Defaults to None.")
    binning: int = Field(description="int: camera binning. Defaults to 1.")
    priority: int = Field(default=1,description="int: default=10. This is the set priority, defaults to 1 (2nd highest priority).")
    end_time_offset_minutes: int = Field(description="int: amount of minutes into the future to let astroplan schedule an intent. Defaults to 20 minutes.")


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
    # objective_name: Optional[str] = None
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
        description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'."
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
    # objective_name: Optional[str] = None
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


# json_prompt_1 = f"""
# <|im_start|>system
# You are a helpful assistant designed to output single JSON fields.
# Given the following user prompt
# << {user_prompt} >>
# extract the following field:
# << {field_1_name} >> with description: {field_1_desc} from the user prompt.
# Example:
# Input:
# user_prompt: "Make a Foo with name Qwerty and ID 906 please."
# Result: {{
#     "{field_1_name}": "Qwerty",
# }}
# <|im_end|>

# <|im_start|>user
# Input:
# user_prompt: {user_prompt}
# <|im_end|>

# <|im_start|>assistant
# Result:
# """

# json_prompt_2 = f"""
# <|im_start|>system
# You are a helpful assistant designed to output single JSON fields.
# Given the following user prompt
# << {user_prompt} >>
# extract the following field info:
# << {field_1_name} >> with description: {field_1_desc} from the user prompt.
# Example:
# Input:
# user_prompt: "Make a Foo with name Qwerty and ID 906 please."
# field_info: Field name: << {field_1_name} >> with description: {field_1_desc}.
# Result: {{
#     "{field_1_name}": "Qwerty",
# }}
# <|im_end|>

# <|im_start|>user
# Input:
# user_prompt: {user_prompt}
# field_info: Field name: << {field_1_name} >> with description: {field_1_desc}.
# <|im_end|>

# <|im_start|>assistant
# Result:
# """
