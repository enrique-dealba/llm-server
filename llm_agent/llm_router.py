from semantic_router import RouteLayer
from semantic_router.encoders import HuggingFaceEncoder

from llm_agent.llm_adapter import VLLMAdapter
from tools.routes import general_route, lat_long_route, time_route


class LLMRouter:
    """LLM with semantic routing."""

    def __init__(self, llm):
        """Initializes LLMRouter with a specified LLM."""
        self.llm = llm
        self.vllm = VLLMAdapter(vllm_instance=llm, name="vllm")
        self.tools = [time_route, lat_long_route]
        self.route_layer = None

    def __call__(self, prompt):
        """Allows LLMRouter to be called directly with a prompt."""
        return self.run(prompt)

    def setup_router(self):
        """Sets up the semantic router for the LLM."""
        routes = [tool.route for tool in self.tools]
        routes += [general_route]
        encoder = HuggingFaceEncoder()

        self.route_layer = RouteLayer(encoder=encoder, routes=routes, llm=self.vllm)

    def run(self, prompt: str):
        """Processes prompt via semantic routing and returns LLM response."""
        if not self.route_layer:
            self.setup_router()

        response = self.route_layer(prompt)
        if response.function_call:
            for tool in self.tools:
                if tool.name in response.name:
                    response = tool.function(**response.function_call)
                    break
        else:
            response = self.llm(prompt)
        print(f"LLM Router Response: {response}, dtype={type(response)}")
        return response
