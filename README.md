# LLM Server

## Introduction

This repository contains code for running a FastAPI server capable of text generation using the Mistral-7B-Instruct or any other compatible language models from vLLM.

## Quick Start
- Clone the codebase
### Build Docker Image
`docker build -t my_llm_server .`
### Run Docker Container
Run the following command to start the Docker container. Make sure to replace ~/.cache/huggingface with the path to your cached Hugging Face model weights if they are stored in a different location:
`docker run -v ~/.cache/huggingface:/root/.cache/huggingface --gpus all --name llm -p 8888:8888 my_llm_server`

If you don't want to use the cached model weights, you can also run:
`docker run --gpus all --rm -p 8888:8888 my_llm_server`

## Usage

### API Endpoint
The server listens on port 8888. You can interact with it using the `/generate` endpoint:
`curl -X POST -d '{"text": "your_prompt_here"}' http://localhost:8888/generate`

### Using client.py
Alternatively, you can use `client.py` to interact with the server:
`python client.py`
Follow the prompt to input your text.

## Important Notes
- If you're using the Mistral-7B-Instruct model, make sure you have around 75.713 GiB of GPU memory. This has been tested on A100 GPUs.

## Troubleshooting
- Make sure Docker has access to your GPU. You may need to install NVIDIA Docker if not already done so.
- If you face issues with the server not starting, check if the port 8888 is already in use.
