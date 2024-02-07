from datetime import datetime
from typing import Callable
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field # , field_validator
from semantic_router import Route
from semantic_router.utils.function_call import get_schema


class RouteModel(BaseModel):
    """Class that encapsulates a function and its associated Route.

    Useful for Semantic router.
    """

    function: Callable
    route: Route
    name: str = Field(description="Name of Route Model")

    # TODO: Fix validation issues with Docker version of pydantic (v1 or v2?)
    # @field_validator("route")
    # def validate_route(cls, v, values):
    #     """Validation to ensure both function and Route are correctly setup."""
    #     if "function" in values:
    #         if get_schema(values["function"]) != v.function_schema:
    #             raise ValueError(
    #                 "Function schema doesn't match Route's function schema"
    #             )
    #     return v


def get_time(timezone: str) -> str:
    """Finds the current time in a specific timezone.

    :param timezone: The timezone to find the current time in, should
        be a valid timezone from the IANA Time Zone Database like
        "America/New_York" or "Europe/London". Do NOT put the place
        name itself like "rome", or "new york", you must provide
        the IANA format.
    :type timezone: str
    :return: The current time in the specified timezone.
    """
    now = datetime.now(ZoneInfo(timezone))
    return now.strftime("%H:%M")


time_schema = get_schema(get_time)

time = Route(
    name="get_time",
    utterances=[
        "what is the time in new york city?",
        "what is the time in london?",
        "I live in Rome, what time is it?",
    ],
    function_schema=time_schema,
)

time_route = RouteModel(function=get_time, route=time, name="get_time")
