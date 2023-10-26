import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.sampling_params import SamplingParams

app = FastAPI()

# Initialize engine with a default model
opt_model = "facebook/opt-125m"
mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
engine = AsyncLLMEngine(model=opt_model, worker_use_ray=False, engine_use_ray=False)

@app.post("/custom_generate")
async def custom_generate(request: Request):
    request_dict = await request.json()
    text = request_dict.pop("text", None)
    sampling_params = SamplingParams(**request_dict)

    results = await engine.generate([text], sampling_params)
    
    text_outputs = [output.text for output in results.outputs]
    ret = {"text": text_outputs}
    return JSONResponse(ret)
