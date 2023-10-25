#!/bin/sh

# Load configurations
. ./config.yaml

# Start FastAPI server
uvicorn my_server:app --host 0.0.0.0 --port 8888
