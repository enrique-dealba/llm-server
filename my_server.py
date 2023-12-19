from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from vllm import SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.utils import random_uuid

from config import (DEFAULT_GPU, DEFAULT_MODEL, MAX_TOKENS, NUM_RESPONSES,
                    TEMPERATURE, TOP_P)

app = FastAPI()

def get_engine_args(llm_model: str, gpu_utilization: float) -> AsyncEngineArgs:
    """Generates AsyncEngineArgs based on the given llm_model."""
    AWQ_GPU = 0.31 # for quantized models like AWQ
    QUANTIZATION = "awq"
    DTYPE = "half"

    if 'awq' in llm_model.lower():
        return AsyncEngineArgs(model=llm_model,
                               gpu_memory_utilization=AWQ_GPU,
                               quantization=QUANTIZATION,
                               dtype=DTYPE)
    else:
        return AsyncEngineArgs(model=llm_model,
                               gpu_memory_utilization=gpu_utilization)

engine_args = get_engine_args(llm_model=DEFAULT_MODEL,
                              gpu_utilization=DEFAULT_GPU)
engine = AsyncLLMEngine.from_engine_args(engine_args)

@app.post("/generate")
async def generate(request: Request):
    request_dict = await request.json()
    prompt = request_dict.pop("text", None)

    sampling_params = SamplingParams(n=NUM_RESPONSES,
                              temperature=TEMPERATURE,
                              top_p=TOP_P,
                              max_tokens=MAX_TOKENS,
    )

    request_id = random_uuid()
    results_generator = engine.generate(prompt, sampling_params, request_id)

    # Non-streaming case
    final_output = None
    async for request_output in results_generator:
        if await request.is_disconnected():
            print("Client disconnected. Aborting request.")
            await engine.abort(request_id)
            return Response(status_code=499)
        final_output = request_output
    # TODO: Test streaming

    assert final_output is not None
    prompt = final_output.prompt
    text_outputs = [output.text for output in final_output.outputs]
    ret = {"text": text_outputs}

    return JSONResponse(ret)
