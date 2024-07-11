#!/bin/bash

# Load configurations from .env file
set -a
source .env
set +a

# Ensures VLLM is properly built
cd /app/vllm
CUDA_HOME=/usr/local/cuda pip3 install -e .
cd /app

# python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
# python3 -c "from vllm import LLMEngine; print('VLLM import successful')"

# Run FastAPI server for llm_server
exec uvicorn llm_server:app --host 0.0.0.0 --port 8888