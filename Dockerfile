# Use a lightweight Python base image
FROM python:3.9-slim

# Set system-level dependencies for HDBSCAN and UMAP
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first (leverage Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a directory for Hugging Face cache to avoid re-downloading
RUN mkdir -p /.cache/huggingface && chmod -R 777 /.cache/huggingface
ENV TRANSFORMERS_CACHE=/.cache/huggingface

# Expose Streamlit's default port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]