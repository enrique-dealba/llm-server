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


class CMO(BaseModel):
    sensor_name: str = Field(description="sensor_name: String Name of Sensor to perform Catalog Maintenance with. Usually in the format 'RME..', 'LMNT..', 'ABQ..', 'UKR...', for example: RME99.")
    data_mode: str = Field(description="data_mode: String type for the Machina Common DataModeType being generated. Either 'TEST' or 'REAL'.")
    classification_marking: str = Field(description="classification_marking: Classification level of objective intents. One of: 'U', 'C', 'S', 'TS', 'U//FOUO'")
    patience_minutes: int = Field(description="patience_minutes: default=30. Amount of time to wait until it is assumed that an intent failed.")
    end_time_offset_minutes: int = Field(description="end_time_offset_minutes: default=20. Amount of minutes into the future to schedule this intent.")
    # objective_name: str = Field(description="objective_name: default='Catalog Maintenance Objective'. The common name for this objective. If can't find just use the default of 'Catalog Maintenance Objective'.")
    # objective_start_time: Annotated[datetime, Field(default_factory=datetime.now)]
    # objective_end_time: Annotated[datetime, Field(default_factory=datetime.now)]
    priority: int = Field(description="int: default=10. This is the set priority, defaults to 10 (11th highest priority).")


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
    pass

class DataEnrichmentObjective(BaseModel):
    pass

class DataEnrichmentObjectiveTemplate(BaseModel):
    pass

class SpectralClearingObjective(BaseModel):
    pass

class SpectralClearingObjectiveTemplate(BaseModel):
    pass

class SingleIntentObjective(BaseModel):
    pass

class SingleIntentObjectiveTemplate(BaseModel):
    pass


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
