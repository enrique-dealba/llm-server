from vllm import AsyncLLMEngine
from fastapi import FastAPI

app = FastAPI()

@app.post("/custom_generate")
async def generate(text: str):
    opt_model = "facebook/opt-125m"
    mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
    engine = AsyncLLMEngine(model=opt_model)
    output = await engine.generate([text])
    # TODO: Additional custom logic goes here
    return output
