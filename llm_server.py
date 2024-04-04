"""FastAPI server for handling Large Language Model (LLM) requests."""

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from langchain.llms import VLLM
from outlines.serve.vllm import JSONLogitsProcessor
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
# quantization = os.environ.get("QUANTIZATION", "None")
# quantization = quantization if quantization != "None" else None

llm = create_llm(quantization="gptq", use_agent=settings.USE_AGENT)

# Print all attributes and methods of the VLLM instance
for attr in dir(llm):
    if not attr.startswith('__'):
        # This filters out the magic methods/attributes
        print(attr)

# If you also want to see the values of these attributes, you can modify the loop to:
for attr in dir(llm):
    if not attr.startswith('__'):  # Skip magic methods and attributes
        try:
            # Attempt to get the value of the attribute
            value = getattr(llm, attr)
            print(f"{attr} = {value}")
        except Exception as e:
            print(f"{attr}: Could not retrieve value - {e}")

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


# sampler._apply_logits_processors = _patched_apply_logits_processors


class ConceptsList(BaseModel):
    concepts: List[str]


logits_processor = JSONLogitsProcessor(ConceptsList, llm.llm_engine)


@app.post("/generate")
async def generate(request: Request, llm: VLLM = Depends(get_llm)):
    """Endpoint to generate text using LLM."""
    try:
        request_data = await request.json()
        query = GenerateRequest(**request_data).text
        # response = llm(query)
        response = llm.generate(
            query,
            sampling_params=VLLM.SamplingParams(
                max_tokens=100, logits_processors=[logits_processor]
            ),
        )
        return JSONResponse({"text": response})
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing user request: {e}"
        )
