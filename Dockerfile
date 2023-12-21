# Start from an NVIDIA CUDA base image with Python
# FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04
# Attempt 2:
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# Install tzdata without interactive prompts and then Python 3.9
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y tzdata && \
    apt-get install -y python3.9 python3-pip python3.9-dev && \
    ln -s /usr/bin/python3.9 /usr/bin/python && \
    pip3 install --upgrade pip

# Verify CUDA installation
RUN nvcc --version

ENV VLLM_VERSION=0.2.4
ENV PYTHON_VERSION=39

RUN pip install https://github.com/vllm-project/vllm/releases/download/v${VLLM_VERSION}/vllm-${VLLM_VERSION}+cu118-cp${PYTHON_VERSION}-cp${PYTHON_VERSION}-manylinux1_x86_64.whl

# Re-installs PyTorch with CUDA 11.8
RUN pip uninstall torch -y && \
    pip install torch --upgrade --index-url https://download.pytorch.org/whl/cu118

# Set working directory
WORKDIR /app

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
