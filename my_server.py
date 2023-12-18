import json
import os
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from vllm import SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.utils import random_uuid

from config import DEFAULT_MODEL, MAX_TOKENS, NUM_RESPONSES, TEMPERATURE, TOP_P

app = FastAPI()

GPU_MEMORY_UTILIZATION = 0.30

def create_engine(model_name: str) -> AsyncLLMEngine:
    engine_args = AsyncEngineArgs(model=model_name,
                                  gpu_memory_utilization=GPU_MEMORY_UTILIZATION)
    return AsyncLLMEngine.from_engine_args(engine_args)

model = os.getenv("MODEL", DEFAULT_MODEL)
engine = create_engine(model)

# Request Handlers
async def parse_request(request: Request) -> str:
    request_dict = await request.json()
    return request_dict.pop("text", None)

def create_sampling_params() -> SamplingParams:
    return SamplingParams(n=NUM_RESPONSES,
                          temperature=TEMPERATURE,
                          top_p=TOP_P,
                          max_tokens=MAX_TOKENS,
    )

async def stream_results(generator: AsyncGenerator) -> AsyncGenerator[bytes, None]:
    async for request_output in generator:
        prompt = request_output.prompt
        text_outputs = [prompt + output.text for output in request_output.outputs]
        ret = {"text": text_outputs}
        yield (json.dumps(ret) + "\0").encode("utf-8")

async def get_final_output(generator: AsyncGenerator, request_id: str, request: Request):
    async for request_output in generator:
        if await request.is_disconnected():
            print("Client disconnected. Aborting request.")
            await engine.abort(request_id)
            return None
        return request_output

# FastAPI Routes
@app.post("/generate")
async def generate(request: Request):
    prompt = await parse_request(request)
    sampling_params = create_sampling_params()
    request_id = random_uuid()
    results_generator = engine.generate(prompt, sampling_params, request_id)

    # TODO: Test streaming feature
    stream = False
    if stream:
        return StreamingResponse(stream_results(results_generator))
    
    final_output = await get_final_output(results_generator, request_id, request)
    if final_output is None:
        return Response(status_code=499)
    
    prompt = final_output.prompt
    text_outputs = [output.text for output in final_output.outputs]
    ret = {"text": text_outputs}
    return JSONResponse(ret)
