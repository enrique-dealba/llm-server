# Use the ironbank Python base image
FROM 029514540576.dkr.ecr.us-gov-west-1.amazonaws.com/ironbank/python39-pipenv:2023.3.20 AS builder

ARG NEXUS_TOKEN
ARG NEXUS_USER

# We can just use root in build stage since we will be copying files
# over in next stage and reconfiguring permissions
USER root

# Set the working directory in the container
WORKDIR /app

# TODO: Add LLM server Dockerfile
# Copy the necessary directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install requirements
ENV VIRTUAL_ENV /usr/local/
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && source ${HOME}/.cargo/env \
    && uv pip install --no-cache -r requirements.txt \
    --extra-index-url https://${NEXUS_USER}:${NEXUS_TOKEN}@nexus.dso-prod.machina.space/repository/pypi-all/simple

COPY server.py /app/server.py

# Use the ironbank Python base image (Stage 2)
FROM 029514540576.dkr.ecr.us-gov-west-1.amazonaws.com/ironbank/python39-pipenv:2023.3.20

# Make sure we are root to create user
USER root

# Create a non-root user to run the app
RUN groupadd --gid 5001 appuser
RUN useradd --create-home --system --uid 5001 --gid 5001 appuser

# Change the ownership of the app files to the non-root user
COPY --from=builder --chown=appuser:appuser /app /app
COPY --from=builder --chown=appuser:appuser /usr/local/bin /usr/local/bin
COPY --from=builder --chown=appuser:appuser /usr/local/lib /usr/local/lib

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
ENTRYPOINT uvicorn server:app --host 0.0.0.0 --port ${PORT} --workers=${WORKERS}