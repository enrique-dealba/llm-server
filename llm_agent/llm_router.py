import json
from typing import Any, Dict, List, Optional

from langchain.llms import VLLM
from semantic_router import Route, RouteLayer
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.llms import BaseLLM
from semantic_router.schema import Message
from semantic_router.utils.function_call import get_schema
from semantic_router.utils.logger import logger

from tools.routes import get_time


class VLLMAdapter(BaseLLM):
    name: str
    vllm: VLLM

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, vllm_instance: VLLM, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.vllm = vllm_instance

    def __call__(self, messages: List[Message]) -> Optional[str]:
        prompts = [message.content for message in messages]
        result = self.vllm._generate(prompts=prompts)
        # result = self.vllm(prompts)
        if result.generations:
            return result.generations[0][0].text
        return None

    def _is_valid_inputs(
        self, inputs: Dict[str, Any], function_schema: Dict[str, Any]
    ) -> bool:
        """Reuses the validation logic from BaseLLM's implementation."""
        try:
            signature = function_schema["signature"]
            param_info = [param.strip() for param in signature[1:-1].split(",")]
            param_names = [info.split(":")[0].strip() for info in param_info]
            param_types = [
                info.split(":")[1].strip().split("=")[0].strip() for info in param_info
            ]

            for name, _ in zip(param_names, param_types):
                if name not in inputs:
                    logger.error(f"Input {name} missing from query")
                    return False
            return True
        except Exception as e:
            logger.error(f"VLLMAdapter Input validation error: {str(e)}")
            return False

    def extract_function_inputs(
        self, query: str, function_schema: dict[str, Any]
    ) -> dict:
        """Adapted from semantic router BaseLLM."""
        logger.info("Extracting function input using VLLM...")

        prompt = f"""
        You are a helpful assistant designed to output JSON.
        Given the following function schema
        << {function_schema} >>
        and query
        << {query} >>
        extract the parameters values from the query, in a valid JSON format.
        Example:
        Input:
        query: "How is the weather in Hawaii right now in International units?"
        schema:
        {{
            "name": "get_weather",
            "description": "Useful to get the weather in a specific location",
            "signature": "(location: str, degree: str) -> str",
            "output": "<class 'str'>",
        }}

        Result: {{
            "location": "London",
            "degree": "Celsius",
        }}

        Input:
        query: {query}
        schema: {function_schema}
        Result:
        """
        llm_input = [Message(role="user", content=prompt)]
        output = self(llm_input)  #  call VLLM via __call__
        output = output.replace("'", '"').strip().rstrip(",")
        logger.info(f"LLM output: {output}")
        function_inputs = json.loads(output)
        logger.info(f"Function inputs: {function_inputs}")
        if not self._is_valid_inputs(function_inputs, function_schema):
            raise ValueError("Invalid inputs")
        return function_inputs


class LLMRouter:
    """LLM with semantic routing."""

    def __init__(self, llm):
        """Initializes LLMRouter with a specified LLM."""
        self.llm = VLLMAdapter(vllm_instance=llm)
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
