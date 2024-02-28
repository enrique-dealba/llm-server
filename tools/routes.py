from typing import Callable, List

from semantic_router import Route
from semantic_router.utils.function_call import get_schema

from tools.router_tools import (
    divide_by_2,
    get_last_letter,
    get_lat_long,
    get_time,
    get_time_and_location,
)


class RouteModel:
    """Class that encapsulates a function and its associated Route.

    Useful for Semantic router.
    """

    function: Callable
    route: Route
    name: str

    def __init__(self, function: Callable, name: str, examples: List[str]):
        """Initializes the RouteModel instance."""
        if not callable(function):
            raise ValueError("function must be callable")
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if not isinstance(examples, list):
            raise ValueError("examples must be a list")

        self.function = function
        self.name = name
        self.route = Route(
            name=name,
            utterances=examples,
            function_schema=get_schema(function),
        )


time_route = RouteModel(
    function=get_time,
    name="get_time",
    examples=[
        "what is the time in new york city?",
        "what is the time in london?",
        "I live in Rome, what time is it?",
    ],
)

lat_long_route = RouteModel(
    function=get_lat_long,
    name="get_lat_long",
    examples=[
        "what is the latitude and longitude of france?",
        "what is the latitude of dallas texas",
        "I live in Rome, what's the longitutde?",
        "whats the longitude in allen tx",
    ],
)

time_location_route = RouteModel(
    function=get_time_and_location,
    name="get_time_and_location",
    examples=[
        "what is the time, latitude, and longitude of france?",
        "what is the time, latitude, and longitude of paris?",
        "what is the time and latitude of dallas texas",
        "I live in Rome, what's the time and longitutde?",
        "whats the time and longitude in allen tx",
    ],
)

last_letter_route = RouteModel(
    function=get_last_letter,
    name="get_last_letter",
    examples=[
        "what is the last letter of 'Apple'?",
        "what is the last letter of Banana?",
        "what's the last letter of camel",
        "I live in Rome. What's the last letter in Rome?",
        "whats the last letter in texas",
    ],
)

divide_two_route = RouteModel(
    function=divide_by_2,
    name="divide_by_2",
    examples=[
        "what is half of 7?",
        "what is 19.5 divided by two?",
        "what's 11 divided by 2",
        "I like the number 23. whats 23 divided by 2?",
        "whats half of 100",
    ],
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
