from typing import Callable, List

from semantic_router import Route
from semantic_router.utils.function_call import get_schema

from tools.router_tools import (
    divide_by_2,
    get_last_letter,
    get_lat_long,
    get_time,
    get_time_and_location,
    get_day_of_week,
    format_phone_number,
    compress_whitespace,
    capitalize_first_letter,
    reverse_string,
    generate_acronym,
    get_vowel_count,
    convert_to_binary,
    get_ascii_value,
    extract_domain,
    count_words,
    convert_to_uppercase,
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

get_day_of_week_route = RouteModel(
    function=get_day_of_week,
    name="get_day_of_week",
    examples=[
        "what day of the week was it on 2021-07-04?",
        "tell me the day for 2020-01-01",
        "what weekday falls on 2023-12-25?",
        "can you find the day of the week for 2022-08-15?",
        "I need the weekday for 2019-11-11",
    ],
)

format_phone_number_route = RouteModel(
    function=format_phone_number,
    name="format_phone_number",
    examples=[
        "how do you format the number 1234567890?",
        "turn 9876543210 into a readable phone number",
        "format this phone number for me: 1122334455",
        "I have a phone number 5556667777, make it pretty",
        "what's the proper format for 4445556666 as a phone number?",
    ],
)

compress_whitespace_route = RouteModel(
    function=compress_whitespace,
    name="compress_whitespace",
    examples=[
        "clean up the spacing in 'hello    world'",
        "compress spaces in 'I  love   Python'",
        "reduce multiple whitespaces to a single space in 'This    is  a  test'",
        "how to make 'So   many    spaces' neat?",
        "remove extra spaces from 'Too  much    space between  words'",
    ],
)

capitalize_first_letter_route = RouteModel(
    function=capitalize_first_letter,
    name="capitalize_first_letter",
    examples=[
        "make the first letter big in 'hello world'",
        "capitalize the beginning of 'this is an example'",
        "start with a capital letter 'capitalize this'",
        "I want the first character uppercase in 'lowercase to uppercase'",
        "how to capitalize 'first letter'",
    ],
)

reverse_string_route = RouteModel(
    function=reverse_string,
    name="reverse_string",
    examples=[
        "flip 'hello world' backwards",
        "reverse the text 'example'",
        "how to say 'reverse me' in reverse",
        "turn 'backwards' around",
        "write '12345' in reverse order",
    ],
)

generate_acronym_route = RouteModel(
    function=generate_acronym,
    name="generate_acronym",
    examples=[
        "what's the acronym for 'North Atlantic Treaty Organization'?",
        "give me the short form of 'Random Access Memory'",
        "acronym for 'Light Amplification by Stimulated Emission of Radiation'",
        "shorten 'Central Processing Unit' to its acronym",
        "create an acronym from 'Application Programming Interface'",
    ],
)

get_vowel_count_route = RouteModel(
    function=get_vowel_count,
    name="get_vowel_count",
    examples=[
        "how many vowels in 'example text'?",
        "count the vowels in 'Hello World'",
        "number of vowels in 'AEIOU'",
        "vowel count for 'abcdefghijklmnopqrstuvwxyz'",
        "tell me how many vowels are in 'This is a test sentence'",
    ],
)

convert_to_binary_route = RouteModel(
    function=convert_to_binary,
    name="convert_to_binary",
    examples=[
        "convert '15' to binary",
        "binary version of '123'",
        "what is '5' in binary?",
        "show '255' as a binary number",
        "how to write '42' in binary?",
    ],
)

get_ascii_value_route = RouteModel(
    function=get_ascii_value,
    name="get_ascii_value",
    examples=[
        "ASCII value of 'a'",
        "what's the ASCII for 'A'?",
        "find ASCII number for '?'",
        "ASCII code for '0'",
        "get me the ASCII of ' ' (space)",
    ],
)

extract_domain_route = RouteModel(
    function=extract_domain,
    name="extract_domain",
    examples=[
        "domain name of 'https://www.example.com/page'",
        "extract domain from 'http://subdomain.example.org/test'",
        "what's the domain in 'https://another-example.net/path'",
        "find the domain of 'www.test-site.com'",
        "get the domain from 'https://www.this-is-a-test.co.uk/path'",
    ],
)

count_words_route = RouteModel(
    function=count_words,
    name="count_words",
    examples=[
        "how many words are in 'This is an example sentence'?",
        "count words in 'Hello, world!'",
        "word count for 'Single'",
        "tell me the number of words in 'This is another test.'",
        "how many words are there in 'Just a simple sentence'?",
    ],
)

convert_to_uppercase_route = RouteModel(
    function=convert_to_uppercase,
    name="convert_to_uppercase",
    examples=[
        "make 'hello world' all uppercase",
        "uppercase 'This is a test'",
        "convert 'small letters' to big",
        "change 'mixed Case' to all uppercase",
        "transform 'lowercase' into UPPERCASE",
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
