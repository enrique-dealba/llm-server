from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ValidationError


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
    priority: int = Field(description="priority: default=10. Scheduler Priority. If can't find just use the default of 10.")


class CMOTemplate(BaseModel):
    sensor_name: Optional[str] = None
    data_mode: Optional[str] = None
    classification_marking: Optional[str] = None
    patience_minutes: Optional[int] = None
    end_time_offset_minutes: Optional[int] = None
    # objective_name: Optional[str] = None
    # objective_start_time: Annotated[datetime, Field(default_factory=datetime.now)]
    # objective_end_time: Annotated[datetime, Field(default_factory=datetime.now)]
    priority: Optional[int] = None


class CatalogMaintenanceObjective(BaseModel):
    sensor_name: str
    data_mode: str
    classification_marking: Marking
    patience_minutes: int = Field(default=30)
    end_time_offset_minutes: int = Field(default=20)
    objective_name: str = Field(default="Catalog Maintenance Objective")
    objective_start_time: Annotated[datetime, Field(default_factory=datetime.now)]
    objective_end_time: Annotated[datetime, Field(default_factory=datetime.now)]
    priority: int = Field(default=10)

    _parse_objective_start_time = parse_datetime
    _parse_objective_end_time = parse_datetime


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
