# Use official Python image
# FROM python:3.9-slim-buster

# Attempt 5
# Start from an NVIDIA CUDA base image with Python
FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

# Install Python 3.9 (if not already included in the base image)
RUN apt-get update && apt-get install -y python3.9 python3-pip python3.9-dev && \
    ln -s /usr/bin/python3.9 /usr/bin/python && \
    pip3 install --upgrade pip

ENV VLLM_VERSION=0.2.4
ENV PYTHON_VERSION=39

# RUN apt-get update && apt-get install -y python3-pip python3-dev && \
#     ln -s /usr/bin/python3 /usr/bin/python && \
#     pip3 install --upgrade pip

RUN pip install https://github.com/vllm-project/vllm/releases/download/v${VLLM_VERSION}/vllm-${VLLM_VERSION}+cu118-cp${PYTHON_VERSION}-cp${PYTHON_VERSION}-manylinux1_x86_64.whl

# Re-installs PyTorch with CUDA 11.8
RUN pip uninstall torch -y && \
    pip install torch --upgrade --index-url https://download.pytorch.org/whl/cu118

# Set working directory
WORKDIR /app

# Install PyTorch separately for CUDA 11.8
# RUN pip install torch==2.0.0+cu118 torchvision==0.15.0+cu118 torchaudio==0.16.0+cu118 -f https://download.pytorch.org/whl/cu118/torch_stable.html
# Attempt 2:
# RUN pip install light-the-torch
# RUN ltt install torch torchvision
# Attempt 3:
# RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# Attempt 4:
# RUN pip install --upgrade fschat accelerate autoawq vllm



# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy .env file and other files
COPY .env .env
COPY . .

# Make sure start.sh is executable
RUN chmod +x start.sh

# Expose port 8888
EXPOSE 8888

# Set start-up script as the entry point
ENTRYPOINT ["sh", "./start.sh"]
