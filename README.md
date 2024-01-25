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

We show GPU performance metrics for two LLMs: Mistral-7B-Instruct-v0.1 and OpenHermes-2.5-Mistral-7B. We compare these models under two different precision formats: 4-bit Activation-aware Weight Quantization (AWQ) and the default 16-bit (`torch.bfloat16`). The metrics are presented in two separate contexts, each using different Python libraries for model handling.

1. Performance Metrics Using vLLM Library

This set of metrics is derived when running the models using pure vLLM:
```python
from vllm import SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
```

| Model | Metrics | 4-bit AWQ | 16-bit |
|-------|--------|-----------|--------|
| *Mistral-7B-Instruct-v0.1* | TPS (tokens/s) | 69.28 | 60.15 |
| | Total Time (s) | 3.18 | 3.38 |
| **OpenHermes-2.5-Mistral-7B** | TPS (tokens/s) | 67.99 | 59.52 |
| | Total Time (s) | 3.72 | 4.81 |

Note: 4-bit AWQ formatted 7B parameter models like `Mistral-7B-Instruct-v0.1-AWQ` and `OpenHermes-2.5-Mistral-7B-AWQ` require at least 6.43 GiB of GPU memory, while the 16-bit 7B models require at least 18.2 GiB of GPU memory.

2. Performance Metrics Using LangChain's vLLM

The following table shows GPU performance metrics for different LLMs using vLLM via LangChain:
```python
from langchain.llms import VLLM
```

| Model | Metrics | 4-bit AWQ | 16-bit |
|-------|--------|-----------|--------|
| *Mistral-7B-Instruct-v0.1* | TPS (tokens/s) | 85.98 | 64.28 |
| | Total Time (s) | 2.61 | 3.30 |
| **OpenHermes-2.5-Mistral-7B** | TPS (tokens/s) | 85.87 | 66.73 |
| | Total Time (s) | 3.02 | 4.05 |

Both sets of metrics were conducted using benchmarks.py.

Note: Have not tested GPTQ quantization.

## Usage

<!-- Use the following `.env` setup for the base LLM implementation.
```.env
SERVER_TYPE=my_server
USING_LLM_SERVER=False
``` -->

Note: Make sure the `config.py` script is using the model you want to test:
```python
DEFAULT_MODEL = "model_name_here"
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
- In our example we're working with 81.92 GiB NVIDIA A100 GPUs, so to get 18.2 GiB for a 7B LLM we need a 0.25 GPU memory utilization. You can change the GPU memory utilization in `config.py`:
```python
DEFAULT_GPU_UTIL = 0.25
```
<!-- or you can change gpu_utilization directly in `my_server.py`:
```python
engine_args = get_engine_args(llm_model=DEFAULT_MODEL, gpu_utilization=DEFAULT_GPU_UTIL)
engine = AsyncLLMEngine.from_engine_args(engine_args)
``` -->

## Troubleshooting
- Make sure Docker has access to your GPU. You may need to install NVIDIA Docker if not already done so.
- If you face issues with the server not starting, check if the port 8888 is already in use.
