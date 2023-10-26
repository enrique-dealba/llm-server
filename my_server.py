import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from vllm import LLMEngine, EngineArgs, SamplingParams

app = FastAPI()

opt_model = "facebook/opt-125m"
mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
engine_args = EngineArgs(model=opt_model)
engine = LLMEngine.from_engine_args(engine_args)

@app.post("/custom_generate")
async def custom_generate(request: Request):
    request_dict = await request.json()
    prompt = request_dict.pop("text", None)
    print(f"Received request: {request_dict}")
    print(f"Prompt: {prompt}")
    
    # Set your sampling params, customize as needed
    sampling_params = SamplingParams(**request_dict)
    params_2 = SamplingParams(n=2, # Number of output sequences to return for the given prompt
                              temperature=0.1,
                              top_p=0.95, # Must be in (0, 1] - set to 1 to consider all tokens
                              frequency_penalty=0.1, # > 0 leads to new tokens, < 0 leads to repeat tokens
                              use_beam_search=False, # whether to use beam search instead of sampling
                              # max_tokens=256,
                            )
    
    request_id = 123
    engine.add_request(str(request_id), prompt, params_2)
    
    request_outputs = None
    while not request_outputs:
        request_outputs = engine.step()
        print(f"Engine step output: {request_outputs}")
    
    for request_output in request_outputs:
        print(f"Processing request_output: {request_output}")
        if request_output.request_id == request_id and request_output.finished:
            text_outputs = [output.text for output in request_output.outputs]
            print(f"Generated outputs: {text_outputs}")
            return JSONResponse({"text": text_outputs})
