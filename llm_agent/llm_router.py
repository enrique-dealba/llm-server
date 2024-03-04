import json
import random

from semantic_router import RouteLayer
from semantic_router.encoders import HuggingFaceEncoder

from llm_agent.llm_adapter import VLLMAdapter
from tools.routes import (
    capitalize_first_letter_route,
    compress_whitespace_route,
    convert_to_binary_route,
    convert_to_uppercase_route,
    count_words_route,
    divide_two_route,
    extract_domain_route,
    format_phone_number_route,
    generate_acronym_route,
    get_ascii_value_route,
    get_day_of_week_route,
    get_vowel_count_route,
    last_letter_route,
    lat_long_route,
    reverse_string_route,
    time_route
)

routes = {
        "time_route": time_route,
        "lat_long_route": lat_long_route,
        "last_letter_route": last_letter_route,
        "divide_two_route": divide_two_route,
        "get_day_of_week_route": get_day_of_week_route,
        "format_phone_number_route": format_phone_number_route,
        "compress_whitespace_route": compress_whitespace_route,
        "capitalize_first_letter_route": capitalize_first_letter_route,
        "reverse_string_route": reverse_string_route,
        "generate_acronym_route": generate_acronym_route,
        "get_vowel_count_route": get_vowel_count_route,
        "convert_to_binary_route": convert_to_binary_route,
        "get_ascii_value_route": get_ascii_value_route,
        "extract_domain_route": extract_domain_route,
        "count_words_route": count_words_route,
        "convert_to_uppercase_route": convert_to_uppercase_route,
}


def load_used_tools_from_file():
    try:
        with open("used_tools.json", "r") as file:
            tool_names = json.load(file)
            used_tools = [routes[tool] for tool in tool_names if tool in routes]
            return used_tools
    except FileNotFoundError:
        print("File not found. Loading all tools.")
        return list(routes.values())


class LLMRouter:
    """LLM with semantic routing."""

    def __init__(self, llm):
        """Initializes LLMRouter with a specified LLM."""
        self.llm = llm
        self.vllm = VLLMAdapter(vllm_instance=llm, name="vllm")
        self.tools = load_used_tools_from_file()
        self.route_layer = None

    def __call__(self, prompt):
        """Allows LLMRouter to be called directly with a prompt."""
        return self.run(prompt)

    def setup_router(self):
        """Sets up the semantic router for the LLM."""
        routes = [tool.route for tool in self.tools]
        # routes += [general_route]
        encoder = HuggingFaceEncoder()

        self.route_layer = RouteLayer(encoder=encoder, routes=routes, llm=self.vllm)

    def run(self, prompt: str):
        """Processes prompt via semantic routing and returns LLM response."""
        if not self.route_layer:
            self.setup_router()

        response = self.route_layer(prompt)
        if response.function_call and response.name:
            for tool in self.tools:
                if tool.name in response.name:
                    response = tool.function(**response.function_call)
                    break
        else:
            response = self.llm(prompt)
        print(f"LLM Router Response: {response}, dtype={type(response)}")
        return response
