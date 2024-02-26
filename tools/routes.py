from typing import Callable

from semantic_router import Route
from semantic_router.utils.function_call import get_schema

from tools.router_tools import get_lat_long, get_time


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

lat_long_schema = get_schema(get_lat_long)

lat_long = Route(
    name="get_lat_long",
    utterances=[
        "what is the latitude and longitude of france?",
        "what is the latitude of dallas texas",
        "I live in Rome, what's the longitutde?",
        "whats the longitude in allen tx",
    ],
    function_schema=lat_long_schema,
)

lat_long_route = RouteModel(function=get_lat_long, route=lat_long, name="get_lat_long")

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
