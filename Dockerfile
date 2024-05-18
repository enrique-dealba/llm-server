# Use official Python image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Install system dependencies for llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for vLLM version and Python version
# Prev: ENV VLLM_VERSION=0.2.4
ENV VLLM_VERSION=0.3.0
ENV PYTHON_VERSION=39

# Install vLLM with CUDA 11.8
RUN pip install https://github.com/vllm-project/vllm/releases/download/v${VLLM_VERSION}/vllm-${VLLM_VERSION}+cu118-cp${PYTHON_VERSION}-cp${PYTHON_VERSION}-manylinux1_x86_64.whl

# Re-install PyTorch with CUDA 11.8
RUN pip uninstall torch -y && \
    pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cu118
    # pip install torch --upgrade --index-url https://download.pytorch.org/whl/cu118

# Re-install xFormers with CUDA 11.8
RUN pip uninstall xformers -y && \
    pip install xformers==0.0.23.post1 --index-url https://download.pytorch.org/whl/cu118
    # pip install --upgrade xformers --index-url https://download.pytorch.org/whl/cu118

# TODO: Delete this later
RUN pip install pydantic==2.7.1 pydantic-core==2.18.2

# Copy .env file and other files
COPY .env .env
COPY . .

# Make sure start.sh is executable
RUN chmod +x start.sh

# Expose port 8888
EXPOSE 8888

# Set start-up script as the entry point
ENTRYPOINT ["sh", "./start.sh"]
