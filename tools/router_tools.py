import json
from datetime import datetime
from zoneinfo import ZoneInfo

from geopy.geocoders import Nominatim


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
        "Paris, France" or "Tokyo, Japan". Please make sure to include
        a comma for the location string like "Dallas, Texas". Do NOT
        just put the name "Dallas" please make sure to include the
        full localised name of the place like "Dallas, Texas" or for
        Socorro / socorro we would use "Socorro, New Mexico" etc.
    :type location: str
    :return: A tuple containing the latitude and longitude of the
        specified location.
    :rtype: The latitude, longitude for the specified location.
    """
    geolocator = Nominatim(user_agent="YourAppNameHere")
    location = geolocator.geocode(str(location))
    latitude, longitude = location.latitude, location.longitude
    return latitude, longitude


"""
Example input format:
    {'json_data': '{"location": "Paris, France", "timezone": "Europe/Paris"}'}
"""


def get_time_and_location(json_data: str) -> str:
    """Parses a JSON string to extract location and timezone information.

    :param json_data: A JSON string containing the keys 'location' and 'timezone'.
    The JSON string must be formatted with these keys and their respective values
    encapsulated in curly braces, like so:
    "{'location': 'Your Location Here', 'timezone': 'Your Timezone Here'}".
    Make sure to input the correctly formatted input string like:
    "{'location': 'Paris, France', 'timezone': 'Europe/Paris'}". Do NOT just put
    the json brackets {} without the str quotes. Please include quotes " like so:
    "{'field': 'value'}".
    :type json_data: str
    :return: A string containing the current time in the specified timezone and
             the latitude and longitude of the specified location.
    """
    try:
        data = json.loads(json_data)
        location = data.get("location")
        timezone = data.get("timezone")

        if not location or not timezone:
            return "JSON must include 'location' and 'timezone' fields."
            # raise ValueError("JSON must include 'location' and 'timezone' fields.")

        time = get_time(timezone)
        latitude, longitude = get_lat_long(location)

        return (
            f"Current time in {timezone} is {time}. "
            f"Latitude and longitude of {location} are {latitude}, {longitude}."
        )
    except json.JSONDecodeError:
        return "Invalid JSON data provided."
        # raise ValueError("Invalid JSON data provided.")
