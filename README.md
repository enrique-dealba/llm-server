# LLM Server

## Introduction

This repository contains code for running a FastAPI server capable of text generation using the Mistral-7B-Instruct or any other compatible language models from vLLM.

## Quick Start
Clone the codebase: `git clone https://github.com/enrique-dealba/llm-server.git`
### Build Docker Image
`docker build -t my_llm_server .`
### Run Docker Container
Run the following command to start the Docker container. Make sure to replace ~/.cache/huggingface with the path to your cached Hugging Face model weights if they are stored in a different location:

`docker run -v ~/.cache/huggingface:/root/.cache/huggingface --gpus all --name llm -p 8888:8888 my_llm_server`

If you don't want to use the cached model weights, you can also run:

`docker run --gpus all --rm -p 8888:8888 my_llm_server`

## Usage

Use the following `.env` setup for the base LLM implementation.
```.env
SERVER_TYPE=my_server
USING_LLM_SERVER=False
```
Note: `llm_server.py` is for R&D.

Also, make sure the `my_server.py` script is using the model you want to test:
```python
llm_model = os.getenv("MODEL", model_name_here)
```

### API Endpoint
The server listens on port 8888. You can interact with it using the `/generate` endpoint:

`curl -X POST -d '{"text": "your_prompt_here"}' http://localhost:8888/generate`

### Using client.py
Alternatively, you can use `client.py` to interact with the server by running `python client.py`
Follow the prompt to input your text.

Note: For our usage of `client.py` we use a conda env with Python 3.11.5:
1. `conda create -n llm python=3.11.5`
2. `conda activate llm`
3. `pip -r requirements.txt`

## Important Notes
- If you're using the Mistral-7B-Instruct model, make sure to have at least 18.2 GiB of GPU memory. This has been tested on A100 GPUs.
- In our example we're working with 81.92 GiB NVIDIA A100 GPUs, so to get 18.2 GiB for a 7B LLM we need a 0.25 GPU memory utilization. In `my_server.py` you can change the GPU memory utilization like so:
```python
engine_args = AsyncEngineArgs(model=llm_model, gpu_memory_utilization=0.25)
engine = AsyncLLMEngine.from_engine_args(engine_args)
```

## Troubleshooting
- Make sure Docker has access to your GPU. You may need to install NVIDIA Docker if not already done so.
- If you face issues with the server not starting, check if the port 8888 is already in use.
