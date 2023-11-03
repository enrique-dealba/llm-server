import json
import argparse
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from langchain.llms import VLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = FastAPI()

opt_model = "facebook/opt-125m" # For testing
mistral_model = "mistralai/Mistral-7B-Instruct-v0.1"
zephyr_model = "HuggingFaceH4/zephyr-7b-beta" # works with RAG and ReAct

# Setting model directly
llm_model = os.getenv("MODEL", "facebook/opt-125m")

NUM_GPUS = 1
llm = VLLM(
    model=llm_model,
    temperature=0.2,
    use_beam_search=False,
    max_new_tokens=512,
    tensor_parallel_size=NUM_GPUS,
    trust_remote_code=True,
)

class LLMAgent:
    """LLM Agent server that performs user tasks."""
    def __init__(self, prompt, llm):
        self.llm_chain = LLMChain(prompt=prompt, llm=llm)
        self.queries = []

    def add_query(self, query):
        self.queries.append(query)

template = """Question: {query}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["query"])

# Instantiate LLMAgent at the module level
llm_agent = LLMAgent(prompt=prompt, llm=llm)

@app.post("/generate")
async def generate(request: Request):
    request_dict = await request.json()
    query = request_dict.pop("text", None)
    
    llm_agent.add_query(query)
    response = llm_agent.llm_chain.run(query)
    ret = {"text": response, "queries": llm_agent.queries}

    return JSONResponse(ret)
