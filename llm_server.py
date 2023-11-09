import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from langchain.llms import VLLM
from pydantic import BaseModel, BaseSettings

from llm_agent import LLMAgent


class Config(BaseSettings):
    def __init__(self):
        opt_model: str = "facebook/opt-125m"
        mistral_model: str = "mistralai/Mistral-7B-Instruct-v0.1"
        zephyr_model: str = "HuggingFaceH4/zephyr-7b-beta"
        llm_model: str = os.getenv("MODEL", self.opt_model) # Defaults to opt-125m

        # LLM Configs
        num_gpus: int = 1
        temperature: float = 0.2
        max_new_tokens: int = 512

    def create_llm(self):
        return VLLM(
            model=self.llm_model,
            temperature=self.temperature,
            use_beam_search=False,
            max_new_tokens=self.max_new_tokens,
            tensor_parallel_size=self.num_gpus,
            trust_remote_code=True,
        )


class GenerateRequest(BaseModel):
    text: str


app = FastAPI()

# Initialize configurations and dependencies
config = Config()

llm = config.create_llm()
llm_agent = LLMAgent(llm=llm)

app = FastAPI()

@app.post("/generate")
async def generate(request: Request):
    request_dict = await request.json()
    request_data = GenerateRequest(**request_dict)
    query = request_data.text
    
    llm_agent.add_query(query)

    response = llm_agent.run(query)

    ret = {"text": response, "queries": llm_agent.queries}

    return JSONResponse(ret)
