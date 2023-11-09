#!/bin/sh

# Load configurations from .env file
export $(grep -v '^#' .env | xargs)

# Determines which FastAPI server to run based on environment variable
SERVER_TYPE=${SERVER_TYPE:-"llm_server"}

if [ "$SERVER_TYPE" = "llm_server" ]; then
  uvicorn llm_server:app --host 0.0.0.0 --port 8888
else
  uvicorn my_server:app --host 0.0.0.0 --port 8888
fi
