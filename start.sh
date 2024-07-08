#!/bin/bash

# Load configurations from .env file
set -a
source .env
set +a

# Activate the virtual environment
source /opt/venv/bin/activate

# Run FastAPI server for llm_server
exec uvicorn llm_server:app --host 0.0.0.0 --port 8888