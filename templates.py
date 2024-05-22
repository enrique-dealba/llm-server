from datetime import datetime
from enum import Enum
from typing import Annotated, Optional, Union

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
    objective_start_time: Union[datetime, str] = Field(default=None, description="The earliest time when objective should begin execution. In 'YYYY-MM-DD HH:MM:SS.ssssss+HH:MM' format")
    objective_end_time: Union[datetime, str] = Field(default=None, description="The time when the objective should end execution. In 'YYYY-MM-DD HH:MM:SS.ssssss+HH:MM' format")


class ObjectiveTimeTemplate(BaseModel):
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None


class Foo(BaseModel):
    foo_name: str =  Field(description="Name of the foo.")
    foo_id: str = Field(description="ID of the foo, usually 3 digits.")


class FooTemplate(BaseModel):
    foo_name: Optional[str] =  None
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
    classification_marking: str = Field(description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'")
    rso_id_list: list[str] = Field(description="list[str]: List of UUIDs of RSO to keep track of.")
    sensor_name_list: list[str] = Field(description="sensor_name: String Name of Sensor to perform Catalog Maintenance with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99.")
    data_mode: str = Field(description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'.")
    collect_request_type: str = Field(description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'.")
    orbital_regime: str = Field(description="str: String enum of orbital regime for this catalog maintenance objective. One of: 'LEO', 'MEO', 'GEO', 'XGEO'.")
    patience_minutes: int = Field(description="patience_minutes: default=30. Amount of time to wait until it is assumed that an intent failed.")
    end_time_offset_minutes: int = Field(description="end_time_offset_minutes: default=20. Amount of minutes into the future to schedule this intent.")
    # objective_name: str = None
    # objective_start_time: Union[datetime, str] = None
    # objective_end_time: Union[datetime, str] = None
    priority: int = Field(description="int: default=1000. This is the set priority, defaults to 999 (1000th highest priority).")

class CMO(BaseModel):
    sensor_name: str = Field(description="sensor_name: String Name of Sensor to perform Catalog Maintenance with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99.")
    data_mode: str = Field(description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'.")
    classification_marking: str = Field(description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'")
    patience_minutes: int = Field(description="patience_minutes: default=30. Amount of time to wait until it is assumed that an intent failed.")
    end_time_offset_minutes: int = Field(description="end_time_offset_minutes: default=20. Amount of minutes into the future to schedule this intent.")
    # objective_name: str = Field(description="objective_name: default='Catalog Maintenance Objective'. The common name for this objective. If can't find just use the default of 'Catalog Maintenance Objective'.")
    # objective_start_time: Annotated[datetime, Field(default_factory=datetime.now)]
    # objective_end_time: Annotated[datetime, Field(default_factory=datetime.now)]
    priority: int = Field(default=999, description="int: default=1000. This is the set priority, defaults to 999 (1000th highest priority).")

class CatalogMaintenanceObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    rso_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    orbital_regime: Optional[str] = None
    patience_minutes: Optional[int] = None
    end_time_offset_minutes: Optional[int] = None
    # objective_name: Optional[str] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    priority: Optional[int] = None


class CMOTemplate(BaseModel):
    sensor_name: Optional[str] = None
    data_mode: Optional[str] = None
    classification_marking: Optional[str] = None
    patience_minutes: Optional[int] = None
    end_time_offset_minutes: Optional[int] = None
    # objective_name: Optional[str] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    priority: Optional[int] = None


class PeriodicRevisitObjective(BaseModel):
    classification_marking: str = Field(description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'")
    target_id_list: list[str] = Field(description="list[str]: List of belief state UUID's of Targets.")
    sensor_name_list: list[str] = Field(description="list[str]: List of sensor(s) name(s) to perform periodic revisit with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99.")
    data_mode: str = Field(description="data_mode: String type for the Machina Common DataModeType being generated. One of: 'TEST', 'REAL', 'SIMULATED', 'EXERCISE'.")
    collect_request_type: str = Field(description="str: Collect request type of tracking type. Defaults to 'RATE_TRACK_SIDEREAL'. One of: 'RATE_TRACK', 'SIDEREAL', 'RATE_TRACK_SIDEREAL'.")
    patience_minutes: int = Field(description="patience_minutes: default=30. Amount of time to wait until it is assumed that an intent failed.")
    revisits_per_hour: float = Field(default=1.0, description="float: default=1. Desired number of times to revisit and observe each target per hour.")
    hours_to_plan: float = Field(default=24.0, description="float: default=24. Maximum hours to plan.")
    number_of_frames: int = Field(description="int: amount of frames per intent. Defaults to None.")
    integration_time: float = Field(description="float: Seconds of integration time per frame. Defaults to None.")
    binning: int = Field(default=1, description="int: camera binning. Defaults to 1.")
    # objective_name: Optional[str] = None
    # objective_start_time: datetime = None,
    # objective_end_time: datetime = None,
    priority: int = Field(default=10, description="int: default=10. This is the set priority, defaults to 10 (11th highest priority).")


class PeriodicRevisitObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    patience_minutes: Optional[int] = None
    revisits_per_hour: Optional[float] = None
    hours_to_plan: Optional[float] = None
    number_of_frames: Optional[int] = None
    integration_time: Optional[float] = None
    binning: Optional[int] = None
    # objective_name: Optional[str] = None
    objective_start_time: datetime = None,
    objective_end_time: datetime = None,
    priority: Optional[int] = None


class PRO(BaseModel):
    # objective_def_name: str = Field(default="PeriodicRevisitObjective", description="Exact name of Objective definition.")
    target_id: int = Field(description="int: 5 Digit RSO satcat id.")
    sensor_name: str = Field(description="sensor_name: String Name of Sensor to perform Revisits with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99.")
    data_mode: str = Field(description="data_mode: String type for the Machina Common DataModeType being generated. Either 'TEST' or 'REAL'.")
    classification_marking: str = Field(description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'")
    revisits_per_hour: int = Field(default=1, description="int: default=1. Desired number of times to revisit and observe each target per hour.")
    hours_to_plan: int = Field(default=24, description="int: default=24. Maximum hours to plan.")
    # objective_name: str = Field(default="Periodic Revisit Objective", description="Name for this objective.")
    # objective_start_time: Optional[Union[datetime, str]] = Field(default=None, description="The earliest time when the objective should begin execution.")
    # objective_end_time: Optional[Union[datetime, str]] = Field(default=None, description="The earliest time when the objective should end execution.")
    priority: int = Field(default=2, description="int: default=2. This is the set priority, defaults to 2 (3rd highest priority).")


class PROTemplate(BaseModel):
    # objective_def_name: Optional[str] = None
    target_id: Optional[int] = None
    sensor_name: Optional[str] = None
    data_mode: Optional[str] = None
    classification_marking: Optional[str] = None
    revisits_per_hour: Optional[int] = None
    hours_to_plan: Optional[int] = None
    # objective_name: Optional[str] = None
    objective_start_time: Optional[Union[datetime, str]] = None
    objective_end_time: Optional[Union[datetime, str]] = None
    priority: Optional[int] = None


class SearchObjective(BaseModel):
    pass


class SearchObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id: Optional[str] = None
    sensor_name: Optional[str] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    initial_offset: Optional[int] = None
    final_offset: Optional[int] = None
    objective_name: Optional[str] = None
    frame_overlap_percentage: Optional[float] = None
    number_of_frames: Optional[int] = None
    integration_time: Optional[int] = None
    binning: Optional[int] = None
    priority: Optional[int] = None
    end_time_offset_minutes: Optional[int] = None


class DataEnrichmentObjective(BaseModel):
    pass


class DataEnrichmentObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    max_rso_to_observe: Optional[int] = None
    revisits_per_hour: Optional[float] = None
    hours_to_plan: Optional[float] = None
    objective_name: Optional[str] = None
    priority: Optional[int] = None


class SpectralClearingObjective(BaseModel):
    pass


class SpectralClearingObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id_list: Optional[list[str]] = None
    sensor_name_list: Optional[list[str]] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    patience_minutes: Optional[int] = None
    target_total_obs: Optional[int] = None
    number_of_frames: Optional[int] = None
    integration_time: Optional[float] = None
    binning: Optional[int] = None
    objective_name: Optional[str] = None
    priority: Optional[int] = None


class SingleIntentObjective(BaseModel):
    pass


class SingleIntentObjectiveTemplate(BaseModel):
    classification_marking: Optional[str] = None
    target_id: Optional[str] = None
    data_mode: Optional[str] = None
    collect_request_type: Optional[str] = None
    sensor_name: Optional[str] = None
    number_of_frames: Optional[int] = None
    integration_time: Optional[float] = None
    binning: Optional[int] = None
    # intent_start_time: datetime = None,
    # intent_end_time: datetime = None,
    objective_name: Optional[str] = None
    priority: Optional[int] = None


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
