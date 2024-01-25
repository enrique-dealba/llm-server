"""FastAPI server for handling Large Language Model (LLM) requests."""

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from langchain.llms import VLLM
from pydantic import BaseModel

from config import (
    AWQ_GPU_UTIL,
    DEFAULT_GPU_UTIL,
    DEFAULT_MODEL,
    MAX_TOKENS,
    NUM_GPUS,
    TEMPERATURE,
)


class Config:
    """Configuration management for LLM server.
    
    Handles GPU settings and LLM parameters.
    """

    def __init__(self):
        """Initializes the config with default values for LLM server."""
        self.llm_model: str = DEFAULT_MODEL

        # LLM Configs
        self.num_gpus: int = NUM_GPUS
        self.temperature: float = TEMPERATURE
        self.max_new_tokens: int = MAX_TOKENS
        self.gpu_util = {
            "default": DEFAULT_GPU_UTIL,
            "awq": AWQ_GPU_UTIL,
        }

    def create_llm(self, quantization: Optional[str] = None) -> VLLM:
        """Creates and returns VLLM instance based on current configuration."""
        gpu_utilization = self.gpu_util.get(quantization, self.gpu_util["default"])

        try:
            llm = VLLM(
                model=self.llm_model,
                temperature=self.temperature,
                use_beam_search=False,
                max_new_tokens=self.max_new_tokens,
                tensor_parallel_size=self.num_gpus,
                trust_remote_code=False,
                dtype="half" if quantization == "awq" else "bfloat16",
                vllm_kwargs={
                    "quantization": quantization,
                    "gpu_memory_utilization": gpu_utilization,
                },
            )
            return llm
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}")


class GenerateRequest(BaseModel):
    """Schema for LLM text generation request."""
    text: str


# Initialize configurations and dependencies
config = Config()
llm = config.create_llm(quantization=None)
# from llm_agent.llm_agent import LLMAgent
# llm_agent = LLMAgent(llm=llm)

app = FastAPI()


def get_llm():
    """Dependency injector for the LLM.
    
    Useful for testing the /generate endpoint. Easily swap LLM with a mock or stub
    during testing.
    """
    try:
        print("get_llm called, returning llm instance")
        return llm
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
async def generate(request: Request, llm: VLLM = Depends(get_llm)):
    """Endpoint to generate text using LLM."""
    try:
        request_data = await request.json()
        query = GenerateRequest(**request_data).text
        print(f"generate endpoint called with query: {query}")
        response = llm(query)
        print(f"LLM response: {response}")
        return JSONResponse({"text": response})
    except Exception as e:
        print(f"Error in generate endpoint: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error processing user request: {e}"
        )
