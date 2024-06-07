"""FastAPI server for handling Large Language Model (LLM) requests."""

import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from langchain.llms import VLLM
from pydantic import BaseModel

from config import Settings
# from llm_agent.llm_agent import LLMAgent
from llm_agent.llm_memory import MemoryLLM
from llm_agent.llm_router import LLMRouter

settings = Settings()


class GenerateRequest(BaseModel):
    """Schema for LLM text generation request."""

    text: str


def get_llm_agent(llm):
    """Returns LLM Agent based on config settings."""
    if settings.LLM_AGENT == "LLMRouter":
        return LLMRouter(llm=llm)
    elif settings.LLM_AGENT == "MemoryLLM":
        return MemoryLLM(llm=llm)
    # elif settings.LLM_AGENT == "LLMAgent":
    #     return LLMAgent(llm=llm)
    else:
        raise ValueError(
            f"Invalid LLM_AGENT value: {settings.LLM_AGENT}. "
            "Must be one of: 'LLMRouter', 'MemoryLLM', 'LLMAgent'."
        )


def get_quantization():
    """Returns quantization method based on config settings."""
    quantization = os.environ.get("QUANTIZATION", "None")
    if "GPTQ" in settings.DEFAULT_MODEL:
        quantization = "gptq"
    elif "AWQ" in settings.DEFAULT_MODEL:
        quantization = "awq"
    else:
        quantization = None
    return quantization


def create_llm() -> VLLM:
    """Creates and returns VLLM instance based on current configuration."""
    quantization = get_quantization()
    if quantization is None:
        gpu_utilization = settings.DEFAULT_GPU_UTIL
        dtype_value = "bfloat16"
    else:
        gpu_utilization = getattr(
            settings, f"{quantization.upper()}_GPU_UTIL", settings.DEFAULT_GPU_UTIL
        )
        dtype_value = "half" if quantization in ["awq", "gptq"] else "bfloat16"

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

        if settings.USE_AGENT:
            return get_llm_agent(llm)
        return llm
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {e}")


llm = create_llm()

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
