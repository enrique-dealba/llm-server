import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.sampling_params import SamplingParams
from vllm import LLMEngine, EngineArgs

app = FastAPI()

# Initialize engine with a default model
opt_model = "facebook/opt-125m"
mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
engine_args = EngineArgs(model="facebook/opt-125m")
engine = LLMEngine.from_engine_args(engine_args)

@app.post("/custom_generate")
async def custom_generate(request: Request):
    request_id = 0
    request_dict = await request.json()
    text = request_dict.pop("text", None)
    sampling_params = SamplingParams(**request_dict)
    params_2 = SamplingParams(n=2, # Number of output sequences to return for the given prompt
                              temperature=0.1,
                              top_p=0.95, # Must be in (0, 1] - set to 1 to consider all tokens
                              frequency_penalty=0.1, # > 0 leads to new tokens, < 0 leads to repeat tokens
                              use_beam_search=False, # whether to use beam search instead of sampling
                              # max_tokens=256,
                            )
    
    # prompt, sampling_params = test_prompts.pop(0)
    # engine.add_request(str(request_id), prompt, sampling_params)

    results = await engine.generate([text], sampling_params)
    
    text_outputs = [output.text for output in results.outputs]
    ret = {"text": text_outputs}
    return JSONResponse(ret)
