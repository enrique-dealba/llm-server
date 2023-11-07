#!/bin/sh

# Load configurations from .env file
export $(grep -v '^#' .env | xargs)

# Start FastAPI server
uvicorn my_server:app --host 0.0.0.0 --port 8888
# uvicorn llm_server:app --host 0.0.0.0 --port 8888
