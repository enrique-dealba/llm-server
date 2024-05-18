from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, ValidationError


class Foo(BaseModel):
    foo_name: str
    foo_id: str


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
