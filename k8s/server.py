import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class GenerateRequest(BaseModel):
    """Schema for LLM text generation request."""

    text: str


class GenerateResponse(BaseModel):
    """Schema for LLM text generation response."""

    text: str


@app.post("/generate")
async def generate(generate: GenerateRequest) -> GenerateResponse:
    """Endpoint to generate text using LLM."""
    print(os.listdir(os.path.expanduser("~/.cache/huggingface")))
    return GenerateResponse(text=generate.text)
