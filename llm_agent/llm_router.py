import json
import random

from semantic_router import RouteLayer
from semantic_router.encoders import HuggingFaceEncoder

from llm_agent.llm_adapter import VLLMAdapter
from tools.routes import routes, objective_route, extraction_route

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
        # self.tools = load_used_tools_from_file()
        self.route_layer = None
        self.objective_found = False

    def __call__(self, prompt):
        """Allows LLMRouter to be called directly with a prompt."""
        return self.run(prompt)

    def setup_router(self):
        """Sets up the semantic router for the LLM."""
        # routes = [tool.route for tool in self.tools]
        # routes += [general_route]
        routes = [objective_route, extraction_route]

        encoder = HuggingFaceEncoder()

        self.route_layer = RouteLayer(encoder=encoder, routes=routes, llm=self.vllm)

    def run(self, prompt: str):
        """Processes prompt via semantic routing and returns LLM response."""
        if not self.route_layer:
            self.setup_router()
        
        response = self.route_layer(prompt)
        print(f"self.route_layer(prompt) = {response}")
        # if response.function_call and response.name:
        #     for tool in self.tools:
        #         if tool.name in response.name:
        #             response = tool.function(**response.function_call)
        #             break
        # TODO: add logic to avoid after doing this once already...
        if (response.name and response.name == 'objective') and not self.objective_found:
            # print("OBJECTIVE FOUND!")
            response = "objective"
            self.objective_found = True
        elif response.name and response.name == 'extraction':
            # print("EXTRACTION FOUND!")
            response = self.llm(prompt)
        else:
            # print("WARNING: NEITHER OBJECTIVE NOR EXTRACTION FOUND")
            response = self.llm(prompt)
        # print(f"LLM Router Response: {response}, dtype={type(response)}")
        return response
