"""FastAPI server for handling Large Language Model (LLM) requests."""

from typing import Optional

import vllm
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from langchain.llms import VLLM
from outlines.serve.vllm import JSONLogitsProcessor
from pydantic import BaseModel

from config import Settings

# from llm_agent.llm_agent import LLMAgent
# from llm_agent.llm_memory import MemoryLLM
from llm_agent.llm_router import LLMRouter
from schemas import schemas

settings = Settings()


class GenerateRequest(BaseModel):
    """Schema for LLM text generation request."""

    text: str


class CustomVLLM(VLLM):
    """Custom VLLM class with additional attributes and methods."""

    def generate(self, prompt, sampling_params):
        return self._generate([prompt], **sampling_params.__dict__)


def create_llm(
    quantization: Optional[str] = None, use_agent: Optional[bool] = False
) -> CustomVLLM:
    """Creates and returns CustomVLLM instance based on current configuration."""
    if quantization is None:
        gpu_utilization = settings.DEFAULT_GPU_UTIL
        dtype_value = "bfloat16"
    else:
        gpu_utilization = getattr(
            settings, f"{quantization.upper()}_GPU_UTIL", settings.DEFAULT_GPU_UTIL
        )
        dtype_value = "half" if quantization in ["awq", "gptq"] else "bfloat16"

    try:
        llm = CustomVLLM(
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
# quantization = os.environ.get("QUANTIZATION", "None")
# quantization = quantization if quantization != "None" else None

quantization = "gptq" if "GPTQ" in settings.DEFAULT_MODEL else None
llm = create_llm(quantization=quantization, use_agent=settings.USE_AGENT)

logits_processor = JSONLogitsProcessor(
    schemas.get(settings.SCHEMA), llm.client.llm_engine
)

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
async def generate(request: Request, llm: CustomVLLM = Depends(get_llm)):
    """Endpoint to generate text using LLM."""
    try:
        request_data = await request.json()
        query = GenerateRequest(**request_data).text
        # response = llm(query)
        response = llm.generate(
            query,
            sampling_params=vllm.SamplingParams(
                max_tokens=settings.MAX_TOKENS,
                logits_processors=[logits_processor],
            ),
        )
        return JSONResponse({"text": response.generations[0][0].text})
        # return JSONResponse({"text": response})
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing user request: {e}"
        )
