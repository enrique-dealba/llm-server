from datetime import datetime
from typing import Callable
from zoneinfo import ZoneInfo

from semantic_router import Route
from semantic_router.utils.function_call import get_schema


class RouteModel:
    """Class that encapsulates a function and its associated Route.

    Useful for Semantic router.
    """

    function: Callable
    route: Route
    name: str

    def __init__(self, function: Callable, route: Route, name: str):
        """Initializes the RouteModel instance."""
        if not callable(function):
            raise ValueError("function must be callable")
        if not isinstance(route, Route):
            raise ValueError("route must be an instance of Route")
        if not isinstance(name, str):
            raise ValueError("name must be a string")

        self.function = function
        self.route = route
        self.name = name


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

general_route = Route(
    name="general",
    utterances=[
        "how's the weather today?",
        "how are things going?",
        "explain the theory of relativity",
        "write a poem about birds",
        "what number is the square root of 16?",
        "write a short sentence",
        "tell me about general knowledge and info",
        "give me a JSON for the solar system",
    ],
)
