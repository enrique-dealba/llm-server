"""FastAPI server for handling Large Language Model (LLM) requests."""

import os
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from langchain.llms import VLLM
from pydantic import BaseModel

from config import Settings

# from llm_agent.llm_agent import LLMAgent
# from llm_agent.llm_memory import MemoryLLM
from llm_agent.llm_router import LLMRouter

settings = Settings()


class GenerateRequest(BaseModel):
    """Schema for LLM text generation request."""

    text: str


def create_llm(
    quantization: Optional[str] = None, use_agent: Optional[bool] = False
) -> VLLM:
    """Creates and returns VLLM instance based on current configuration."""
    if quantization is None:
        gpu_utilization = settings.DEFAULT_GPU_UTIL
        dtype_value = "bfloat16"
    else:
        gpu_utilization = getattr(
            settings, f"{quantization.upper()}_GPU_UTIL", settings.DEFAULT_GPU_UTIL
        )
        dtype_value = "half" if quantization in ["awq", "gptq"] else "bfloat16"

    print("quantization:", quantization)
    print("dtype_value:", dtype_value)

    try:
        llm = VLLM(
            model=settings.DEFAULT_MODEL,
            temperature=settings.TEMPERATURE,
            use_beam_search=False,
            max_new_tokens=settings.MAX_TOKENS,
            tensor_parallel_size=settings.NUM_GPUS,
            trust_remote_code=False,
            dtype=dtype_value,
            vllm_kwargs={
                "quantization": quantization,
                "gpu_memory_utilization": gpu_utilization,
                # "max_model_len": settings.MAX_SEQ_LEN,
            },
        )

        if use_agent:
            return LLMRouter(llm=llm)
        return llm
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {e}")


# Initialize configurations and dependencies
quantization = "gptq" if "GPTQ" in settings.DEFAULT_MODEL else "None"
quantization = "awq" if "AWQ" in settings.DEFAULT_MODEL else "None"
print("Model name:", settings.DEFAULT_MODEL)
print(f"AWQ in {settings.DEFAULT_MODEL}: {bool('AWQ' in settings.DEFAULT_MODEL)}")
print(f"GPTQ in {settings.DEFAULT_MODEL}: {bool('GPTQ' in settings.DEFAULT_MODEL)}")
print(f"quantization set to: {quantization}")

llm = create_llm(quantization=quantization, use_agent=settings.USE_AGENT)

app = FastAPI()


def get_llm_instance():
    """Function to retrieve the LLM instance."""
    return llm


def get_llm():
    """Dependency injector for the LLM.

    Useful for testing the /generate endpoint. Easily swap LLM with a mock or stub
    during testing.
    """
    try:
        return get_llm_instance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
async def generate(request: Request, llm: VLLM = Depends(get_llm)):
    """Endpoint to generate text using LLM."""
    try:
        request_data = await request.json()
        query = GenerateRequest(**request_data).text
        response = llm(query)
        return JSONResponse({"text": response})
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing user request: {e}"
        )
