from semantic_router import Route, RouteLayer
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.utils.function_call import get_schema

from tools.routes import get_time


class LLMRouter:
    """LLM with semantic routing."""

    def __init__(self, llm):
        """Initializes LLMRouter with a specified LLM."""
        self.llm = llm
        self.route_layer = None

    def setup_router(self):
        """Sets up the semantic router for the LLM."""
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

        routes = [time]
        encoder = HuggingFaceEncoder()

        self.route_layer = RouteLayer(encoder=encoder, routes=routes, llm=self.llm)

    def run(self, prompt: str):
        """Processes prompt via semantic routing and returns LLM response."""
        if not self.route_layer:
            self.setup_router()

        response = self.route_layer(prompt)
        if "get_time" in response.name:
            response = get_time(**response)
        print(f"LLM Router Response: {response}, dtype={type(response)}")
        return response

    def __call__(self, prompt):
        """Allows LLMRouter to be called directly with a prompt."""
        return self.run(prompt)
