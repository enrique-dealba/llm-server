FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Set noninteractive installation
ENV DEBIAN_FRONTEND=noninteractive

# Set timezone
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    build-essential \
    cmake \
    git \
    libopenblas-dev \
    ninja-build \
    pkg-config \
    libopencv-dev \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV VLLM_VERSION=0.5.1
ENV PYTHON_VERSION=310
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA 11.8 support
RUN pip3 install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118

# Install xformers
RUN pip3 install xformers==0.0.23.post1 --index-url https://download.pytorch.org/whl/cu118

# Install VLLM from source with CUDA support
RUN git clone https://github.com/vllm-project/vllm.git && \
    cd vllm && \
    git checkout v${VLLM_VERSION} && \
    CUDA_HOME=/usr/local/cuda pip3 install -e .

# Install llama-cpp-python with CUDA support
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip3 install llama-cpp-python==0.2.81

# Copy application files
COPY . .

# Make sure start.sh is executable
RUN chmod +x start.sh

# Expose port 8888
EXPOSE 8888

# Set start-up script as the entry point
ENTRYPOINT ["./start.sh"]