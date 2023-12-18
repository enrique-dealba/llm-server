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

Below is a comparison of performance metrics across different LLMs at different quantizations.

<!-- | | **Bits** | **4 (AWQ)** | **32** | **64** | **128** | **192** | **MAX** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| *Mistral-7B-Instruct-v0.1* | TPS (tokens/s) | 0.46 | 1.32 | 3.35 | 7.46 | 7.31 | 7.36 |
| | Total time (s) | 559.3 | 178.9 | 73.72 | 37.13 | 34.76 | 35.07 |
| **OpenHermes-2.5-Mistral-7B** | TPS (tokens/s) | 0.51 | 1.28 | 3.57 | 7.56 | 7.29 | 7.59 |
| | Total time (s) | 484.68 | 208.17 | 67.52 | 33.22 | 36.50 | 28.35 | -->

## Usage

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
- If you're using the Mistral-7B-Instruct model, make sure you have around 75.713 GiB of GPU memory. This has been tested on A100 GPUs.

## Troubleshooting
- Make sure Docker has access to your GPU. You may need to install NVIDIA Docker if not already done so.
- If you face issues with the server not starting, check if the port 8888 is already in use.
