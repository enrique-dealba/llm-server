# Use the ironbank Python base image
FROM 029514540576.dkr.ecr.us-gov-west-1.amazonaws.com/ironbank/python39-pipenv:2023.3.20 AS builder

ARG NEXUS_TOKEN
ARG NEXUS_USER

# We can just use root in build stage since we will be copying files
# over in next stage and reconfiguring permissions
USER root

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for llama-cpp-python using yum
RUN yum update -y && yum install -y \
    gcc \
    gcc-c++ \
    make \
    cmake \
    && yum clean all

# Copy requirements.txt file
COPY requirements.txt .

# Install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt --extra-index-url https://${NEXUS_USER}:${NEXUS_TOKEN}@nexus.dso-prod.machina.space/repository/pypi-all/simple

# Set environment variables for vLLM version and Python version
# ENV VLLM_VERSION=0.3.0
# ENV PYTHON_VERSION=39

# Install vLLM with CUDA 11.8
# RUN pip install https://github.com/vllm-project/vllm/releases/download/v${VLLM_VERSION}/vllm-${VLLM_VERSION}+cu118-cp${PYTHON_VERSION}-cp${PYTHON_VERSION}-manylinux1_x86_64.whl

# Re-install PyTorch with CUDA 11.8
# RUN pip uninstall torch -y && \
#     pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cu118

# Re-install xFormers with CUDA 11.8
# RUN pip uninstall xformers -y && \
#     pip install xformers==0.0.23.post1 --index-url https://download.pytorch.org/whl/cu118

# Copy all files from the parent directory
# COPY . .

# Make sure start.sh is executable
# RUN chmod +x start.sh

# Expose port 8888
# EXPOSE 8888

# Use the ironbank Python base image (Stage 2)
FROM 029514540576.dkr.ecr.us-gov-west-1.amazonaws.com/ironbank/python39-pipenv:2023.3.20

# Make sure we are root to create user
USER root

# Create a non-root user to run the app
RUN groupadd --gid 5001 appuser
RUN useradd --create-home --system --uid 5001 --gid 5001 appuser

# Change the ownership of the app files to the non-root user
COPY --from=builder --chown=appuser:appuser /app /app

# Switch to the non-root user
USER appuser

# Set the working directory in the container
WORKDIR /app

# Define environment variables
ENV PORT 5000
ENV WORKERS 1

# Set the Python path to recognize our server package since we do not install it
ENV PYTHONPATH .

# Define entrypoint to run the server when the container launches
ENTRYPOINT ["sh", "./start.sh"]