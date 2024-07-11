#!/bin/bash

# Load configurations from .env file
set -a
source .env
set +a

# Print CUDA and PyTorch information
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'PyTorch version: {torch.__version__}')"

# Run FastAPI server for llm_server
exec uvicorn llm_server:app --host 0.0.0.0 --port 8888