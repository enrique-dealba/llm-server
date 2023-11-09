import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from langchain.llms import VLLM

from llm_agent import LLMAgent


class Config:
    def __init__(self):
        self.opt_model = "facebook/opt-125m"
        self.mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
        self.zephyr_model = "HuggingFaceH4/zephyr-7b-beta"
        self.llm_model = os.getenv("MODEL", self.zephyr_model)

        # LLM Configs
        self.num_gpus = 1
        self.temperature = 0.2
        self.max_new_tokens = 512

    def create_llm(self):
        return VLLM(
            model=self.llm_model,
            temperature=self.temperature,
            use_beam_search=False,
            max_new_tokens=self.max_new_tokens,
            tensor_parallel_size=self.num_gpus,
            trust_remote_code=True,
        )

app = FastAPI()

# Initialize configurations and dependencies
config = Config()

llm = config.create_llm()
llm_agent = LLMAgent(llm=llm)

app = FastAPI()

@app.post("/generate")
async def generate(request: Request):
    request_dict = await request.json()
    query = request_dict.pop("text", None)
    
    llm_agent.add_query(query)

    response = llm_agent.run(query)

    ret = {"text": response, "queries": llm_agent.queries}

    return JSONResponse(ret)
