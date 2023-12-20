# Use official Python image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Install PyTorch separately
RUN pip install torch==2.1.0+cu118 torchvision==0.13.1+cu118 torchaudio==0.12.1+cu118 -f https://download.pytorch.org/whl/cu118/torch_stable.html
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
