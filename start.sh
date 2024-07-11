#!/bin/bash

set -e

source .env

echo "Checking CUDA availability..."
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'PyTorch version: {torch.__version__}')"

echo "Checking NVIDIA driver..."
nvidia-smi

echo "Checking GPU devices..."
python3 -c "import torch; print(f'GPU count: {torch.cuda.device_count()}'); [print(f'GPU {i}: {torch.cuda.get_device_name(i)}') for i in range(torch.cuda.device_count())]"

echo "Starting FastAPI server..."
exec uvicorn llm_server:app --host 0.0.0.0 --port 8888