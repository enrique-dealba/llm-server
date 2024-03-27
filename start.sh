#!/bin/sh

# Load configurations from .env file
export $(grep -v '^#' .env | xargs)

# Activate the virtual environment
source /opt/venv/bin/activate

# Run FastAPI server for llm_server
uvicorn llm_server:app --host 0.0.0.0 --port 8888
