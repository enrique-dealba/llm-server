import json
import argparse
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from vllm import LLMEngine, EngineArgs, SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.utils import random_uuid

app = FastAPI()

opt_model = "facebook/opt-125m" # For testing
mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"

# Setting model directly
opt_model = os.getenv("MODEL", "mistralai/Mistral-7B-Instruct-v0.1")

engine_args = AsyncEngineArgs(model=opt_model, gpu_memory_utilization=0.96)
engine = AsyncLLMEngine.from_engine_args(engine_args)

@app.post("/generate")
async def generate(request: Request):
    request_dict = await request.json()
    prompt = request_dict.pop("text", None)
    
    sampling_params = SamplingParams(n=2, # Number of output sequences to return for the given prompt
                              temperature=0.2,
                              top_p=0.95, # Must be in (0, 1] - set to 1 to consider all tokens
                              #frequency_penalty=0.1, # > 0 leads to new tokens, < 0 leads to repeat tokens
                              #use_beam_search=False, # whether to use beam search instead of sampling
                              max_tokens=250,
                            )
    
    request_id = random_uuid()
    results_generator = engine.generate(prompt, sampling_params, request_id)
    print("engine.generate called")
    
    # Non-streaming case
    final_output = None
    async for request_output in results_generator:
        if await request.is_disconnected():
            print("Client disconnected. Aborting request.")
            # Abort the request if the client disconnects.
            await engine.abort(request_id)
            return Response(status_code=499)
        final_output = request_output

    assert final_output is not None
    prompt = final_output.prompt
    text_outputs = [prompt + output.text for output in final_output.outputs]
    ret = {"text": text_outputs}

    return JSONResponse(ret)
