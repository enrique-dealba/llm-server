from datetime import datetime
from typing import Callable
from zoneinfo import ZoneInfo

from geopy.geocoders import Nominatim
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


def get_lat_long(location: str) -> str:
    """Finds the latitude and longitude of a specific location.

    :param location: The name of the location to find the latitude and
        longitude for. This should be a string representing a place
        that can be recognized by the Nominatim geocoder, such as
        "Paris, France" or "Tokyo, Japan".
    :type location: str
    :return: A tuple containing the latitude and longitude of the
        specified location.
    :rtype: tuple(float, float).
    """
    geolocator = Nominatim(user_agent="YourAppNameHere")
    location = geolocator.geocode(str(location))
    latitude, longitude = location.latitude, location.longitude
    return latitude, longitude


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
