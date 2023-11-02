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
llm_model = os.getenv("MODEL", "mistralai/Mistral-7B-Instruct-v0.1")

NUM_GPUS = 1
llm = VLLM(
    model=llm_model,
    tensor_parallel_size=NUM_GPUS,
    trust_remote_code=True,
)

@app.post("/generate")
async def generate(request: Request):
    request_dict = await request.json()
    query = request_dict.pop("text", None)
    template = """Question: {query}
    Answer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=["query"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    response = llm_chain.run(query)
    ret = {"text": response}

    return JSONResponse(ret)
