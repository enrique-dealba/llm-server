from typing import Callable

from semantic_router import Route
from semantic_router.utils.function_call import get_schema

from tools.router_tools import (divide_by_2, get_last_letter, get_lat_long,
                                get_time, get_time_and_location)


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

time_location_schema = get_schema(get_time_and_location)

time_location = Route(
    name="get_time_and_location",
    utterances=[
        "what is the time, latitude, and longitude of france?",
        "what is the time, latitude, and longitude of paris?",
        "what is the time and latitude of dallas texas",
        "I live in Rome, what's the time and longitutde?",
        "whats the time and longitude in allen tx",
    ],
    function_schema=time_location_schema,
)

time_location_route = RouteModel(
    function=get_time_and_location, route=time_location, name="get_time_and_location"
)

last_letter_schema = get_schema(get_last_letter)

last_letter = Route(
    name="get_last_letter",
    utterances=[
        "what is the last letter of 'Apple'?",
        "what is the last letter of Banana?",
        "what's the last letter of camel",
        "I live in Rome. What's the last letter in Rome?",
        "whats the last letter in texas",
    ],
    function_schema=last_letter_schema,
)

last_letter_route = RouteModel(
    function=get_last_letter, route=last_letter, name="get_last_letter"
)

divide_two_schema = get_schema(divide_by_2)

divide_two = Route(
    name="divide_by_2",
    utterances=[
        "what is half of 7?",
        "what is 19.5 divided by two?",
        "what's 11 divided by 2",
        "I like the number 23. whats 23 divided by 2?",
        "whats half of 100",
    ],
    function_schema=divide_two_schema,
)

divide_two_route = RouteModel(
    function=divide_by_2, route=divide_two, name="divide_by_2"
)

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
