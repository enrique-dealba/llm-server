import json
import re
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


def get_last_letter(word: str) -> str:
    """Finds the last letter of a given word.

    :param word: The word from which to extract the last letter. The
        word should be a non-empty string.
    :type word: str
    :return: The last letter of the given word. If the word is empty,
        the behavior is undefined.
    """
    if word:
        return word[-1]
    return "Invalid string."


def divide_by_2(number: str) -> str:
    """Divides a number, provided as a string, by 2.

    :param number: The number to divide by 2, should be a string that
        can be converted to a float. Do NOT put non-string values or
        strings that cannot be converted to a float, you must provide
        a valid numerical string.
    :type number: str
    :return: The result of the division as a string. If the input cannot
        be converted to a float, returns an error message indicating
        the type of error (conversion or type error).
    """
    try:
        number = float(number)
        return str(number / 2.0)
    except ValueError:
        return "Error: Input could not be converted to a float."
    except TypeError:
        return "Error: Expected a string that can be converted to a float."


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


def get_day_of_week(date: str) -> str:
    """Finds the day of the week for a given date.

    :param date: The date to find the day of the week for, should
        be a string in the format "YYYY-MM-DD". Do NOT put dates in
        other formats or non-date strings, you must provide
        a valid date string in the specified "YYYY-MM-DD" format.
    :type date: str
    :return: The day of the week for the specified date. If the input is empty,
        returns "Invalid date". If the date format is incorrect, returns
        "Invalid date format".
    """
    if not date:
        return "Invalid date"
    try:
        return datetime.strptime(date, "%Y-%m-%d").strftime("%A")
    except ValueError:
        return "Invalid date format"


def format_phone_number(number: str) -> str:
    """Formats a 10-digit phone number into a more readable form.

    :param number: The phone number to format, should be a string of
        10 digits without any separators. Do NOT put numbers with
        less or more than 10 digits or numbers that contain letters
        or special characters, you must provide a valid 10-digit
        numerical string.
    :type number: str
    :return: The formatted phone number in the form "(XXX) XXX-XXXX".
        If the input is not a valid 10-digit numerical string,
        returns "Invalid phone number".
    """
    if len(number) != 10 or not number.isdigit():
        return "Invalid phone number"
    return f"({number[:3]}) {number[3:6]}-{number[6:]}"


def compress_whitespace(text: str) -> str:
    """Compresses all consecutive whitespaces in the text to a single space.

    :param text: The text to compress whitespaces in. Do NOT put non-string
        values, you must provide a string, even if it's empty.
    :type text: str
    :return: The text with all consecutive whitespaces compressed to a single space.
        If the input is only whitespaces or empty, returns an empty string.
    """
    if not text.strip():
        return ""
    return " ".join(text.split())


def capitalize_first_letter(text: str) -> str:
    """Capitalizes the first letter of the text.

    :param text: The text to capitalize the first letter of. Do NOT put non-string
        values, you must provide a string, even if it's empty.
    :type text: str
    :return: The text with the first letter capitalized. If the input is empty,
        it will return an empty string.
    """
    return text.capitalize()


def reverse_string(text: str) -> str:
    """Reverses the given string.

    :param text: The text to be reversed. Do NOT put non-string values,
        you must provide a string, even if it's empty.
    :type text: str
    :return: The reverse of the input text. If the input is empty,
        returns an empty string.
    """
    return text[::-1]


def generate_acronym(text: str) -> str:
    """Generates an acronym from the first letters of each word in the text.

    :param text: The text to generate an acronym from. Do NOT put non-string
        values or strings that do not contain any words, you must provide
        a valid string with at least one word.
    :type text: str
    :return: The acronym generated from the first letters of each word in the text,
        converted to uppercase. If the input is only whitespaces or empty,
        returns an empty string.
    """
    if not text.strip():
        return ""
    return "".join(word[0].upper() for word in text.split())


def get_vowel_count(text: str) -> str:
    """Counts the number of vowels in the given text.

    :param text: The text to count vowels in. Do NOT put non-string values,
        you must provide a string, even if it's empty.
    :type text: str
    :return: The number of vowels in the text as a string. Counts both
        uppercase and lowercase vowels.
    """
    return str(sum(1 for char in text.lower() if char in "aeiou"))


def convert_to_binary(number: str) -> str:
    """Converts a numerical string to its binary representation.

    :param number: The number to convert to binary, should be a string of digits.
        Do NOT put non-digit strings or strings that contain letters or
        special characters, you must provide a valid numerical string.
    :type number: str
    :return: The binary representation of the number as a string. If the input
        is not a valid numerical string, returns "Invalid input".
    """
    if not number.isdigit():
        return "Invalid input"
    return bin(int(number))[2:]


def get_ascii_value(character: str) -> str:
    """Finds the ASCII value of a single character.

    :param character: The character to find the ASCII value for. Do NOT put strings with
        more than one character or empty strings, you must provide a single character.
    :type character: str
    :return: The ASCII value of the character as a string. If the input is not a single
        character, returns "Invalid input".
    """
    if len(character) != 1:
        return "Invalid input"
    return str(ord(character))


def extract_domain(url: str) -> str:
    """Extracts the domain name from a URL.

    :param url: The URL to extract the domain from. Do NOT put non-URL strings or
        strings that do not conform to URL formatting, you must provide a valid URL.
    :type url: str
    :return: The domain name extracted from the URL. If the URL is invalid or the domain
        cannot be extracted, returns "Invalid URL".
    """
    try:
        return re.findall(r"://([^/]+)/?", url)[0]
    except IndexError:
        return "Invalid URL"


def count_words(text: str) -> str:
    """Counts the number of words in the given text.

    :param text: The text to count words in. Do NOT put non-string values,
        you must provide a string, even if it's empty.
    :type text: str
    :return: The number of words in the text as a string. If the input is only
        whitespaces or empty, returns "0".
    """
    if not text.strip():
        return "0"
    return str(len(text.split()))


def convert_to_uppercase(text: str) -> str:
    """Converts all lowercase letters in the text to uppercase.

    :param text: The text to convert to uppercase. Do NOT put non-string values,
        you must provide a string, even if it's empty.
    :type text: str
    :return: The text with all lowercase letters converted to uppercase.
    """
    return text.upper()


"""
Example input format:
    {'json_data': '{"location": "Paris, France", "timezone": "Europe/Paris"}'}
"""


def get_time_and_location(json_data: str) -> str:
    """Parses a JSON string to extract location and timezone information.

    :param json_data: A JSON string containing the keys 'location' and 'timezone'.
        The JSON string must be formatted with these keys and their respective values
        encapsulated in curly braces, like so:
        '{"location": "Location Here", "timezone": "Timezone Here"}'.
        Make sure to input the correctly formatted input string like:
        '{"location": "Paris, France", "timezone": "Europe/Paris"}'. Do NOT just put
        the JSON brackets {} without the string quotes. Please include quotes " like so:
        '{"field": "value"}'.
    :type json_data: str
    :return: A string containing the current time in the specified timezone and
             the latitude and longitude of the specified location.

    Example of a valid input:
        "json_data": '{"location": "Rome, Italy", "timezone": "Europe/Rome"}'
        "json_data": '{"location": "New York, USA", "timezone": "America/New_York"}'
        "json_data": '{"location": "Seoul, South Korea", "timezone": "Asia/Seoul"}'
        "json_data": '{"location": "Kuwait City, Kuwait", "timezone": "Asia/Kuwait"}'
        "json_data": '{"location": "Panama City, Panama", "timezone": "America/Panama"}'
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
