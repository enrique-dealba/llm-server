# LLM Server

## Introduction

This repository contains code for running a FastAPI server capable of text generation using the Mistral-7B-Instruct or any other compatible language models from vLLM.

## Quick Start
Clone the codebase:
```sh
git clone https://github.com/enrique-dealba/llm-server.git
```

### Build Docker Image
```sh
docker build -t my_llm_server .
```

### Run Docker Container
Run the following command to start the Docker container. Make sure to replace ~/.cache/huggingface with the path to your cached Hugging Face model weights if they are stored in a different location:
```sh
docker run -v ~/.cache/huggingface:/root/.cache/huggingface --gpus all --name llm -p 8888:8888 my_llm_server
```

If you don't want to use the cached model weights, you can also run:
```sh
docker run --gpus all --rm -p 8888:8888 my_llm_server
```

## GPU Performance Metrics

The following table shows GPU performance metrics for different LLMs, focusing on the 4-bit Activation-aware Weight Quantization (AWQ) and default 16-bit (`torch.bfloat16`) precision formats.

| Model | Metrics | 4-bit AWQ | 16-bit |
|-------|--------|-----------|--------|
| *Mistral-7B-Instruct-v0.1* | TPS (tokens/s) | 69.28 | 60.15 |
| | Total Time (s) | 3.18 | 3.38 |
| **OpenHermes-2.5-Mistral-7B** | TPS (tokens/s) | 67.99 | 59.52 |
| | Total Time (s) | 3.72 | 4.81 |

These tests were conducted by running benchmarks.py and running a handful of prompts through the LLM FastAPI server and timing their responses.

## Usage

Use the following `.env` setup for the base LLM implementation.
```.env
SERVER_TYPE=my_server
USING_LLM_SERVER=False
```

Note: Make sure the `my_server.py` script is using the model you want to test (`llm_server.py` is for R&D.):
```python
llm_model = os.getenv("MODEL", model_name_here)
```

### API Endpoint
The server listens on port 8888. You can interact with it using the `/generate` endpoint:
```sh
curl -X POST -d '{"text": "your_prompt_here"}' http://localhost:8888/generate
```

### Using client.py
Alternatively, you can run the `client.py` script to interact with the server:
```sh
python client.py
```

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
