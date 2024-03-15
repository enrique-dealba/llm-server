import json
from typing import Any, Dict, List, Optional

from langchain.llms import VLLM
from semantic_router.llms import BaseLLM
from semantic_router.schema import Message
from semantic_router.utils.logger import logger


class VLLMAdapter(BaseLLM):
    """Adapter class that integrates VLLM instance with semantic router's BaseLLM.

    Allows VLLM instances to be used wherever a BaseLLM is expected.
    """

    name: str
    vllm: VLLM = None

    class Config:
        """Defines config settings for VLLMAdapter Pydantic model.

        Allows model to accommodate VLLM instance field within the VLLMAdapter,
        since VLLM is not be a standard Pydantic type.
        """

        arbitrary_types_allowed = True

    def __init__(self, vllm_instance: VLLM, name: str, **kwargs):
        """Initializes VLLMAdapter."""
        kwargs["vllm"] = vllm_instance
        super().__init__(name=name, **kwargs)

    def __call__(self, messages: List[Message]) -> Optional[str]:
        """Processes list of prompts, generating resposes from wrapped VLLM."""
        if not messages:
            logger.info("No messages provided for generation.")
            return None

        prompts = [message.content for message in messages]
        result = self.vllm._generate(prompts=prompts)
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
        hermes_pro_prompt =  f"""
        <|im_start|>system
        You are a helpful assistant designed to output JSON.
        Given the following function schema
        <tools> {function_schema} </tools>
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

        Result:
        <tool_call>
        {{
            "arguments": {{
                "location": "Hawaii",
                "degree": "International"
                }},
            "name": "get_weather"
        }}
        </tool_call>

        Input:
        query: {query}
        schema:
        <tools>
        {function_schema}
        </tools>
        Result:
        <tool_call>
        {{
            "arguments": {{}},
            "name": ""
        }}
        </tool_call>
        <|im_end|>
        """
        prompt = hermes_pro_prompt
        llm_input = [Message(role="user", content=prompt)]
        output = self(llm_input)  #  call VLLM via __call__
        output = output.replace("'", '"').strip().rstrip(",")
        logger.info(f"LLM output: {output}")
        function_inputs = json.loads(output)
        logger.info(f"Function inputs: {function_inputs}")
        if not self._is_valid_inputs(function_inputs, function_schema):
            raise ValueError("Invalid inputs")
        return function_inputs
