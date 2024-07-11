FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

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

ENV VLLM_VERSION=0.5.1
ENV PYTHON_VERSION=310
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA 11.8 support
RUN pip3 install torch==2.1.2+cu118 torchvision==0.16.2+cu118 torchaudio==2.1.2+cu118 -f https://download.pytorch.org/whl/torch_stable.html

# Install xformers
RUN pip3 install xformers==0.0.23.post1 -f https://download.pytorch.org/whl/cu118/torch_stable.html

# Install VLLM from source with CUDA support
RUN git clone https://github.com/vllm-project/vllm.git && \
    cd vllm && \
    git checkout v${VLLM_VERSION} && \
    CUDA_HOME=/usr/local/cuda pip3 install -e .

# Install llama-cpp-python with CUDA support
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip3 install llama-cpp-python==0.2.81

COPY . .

RUN chmod +x start.sh

EXPOSE 8888

# Add NVIDIA runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

ENTRYPOINT ["./start.sh"]