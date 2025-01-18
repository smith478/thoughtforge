FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Set environment variable for CUDA
ENV CUDA_VISIBLE_DEVICES=0

# Download model during build (optional, could also be mounted)
RUN python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-7B-Instruct', device_map='auto', trust_remote_code=True); AutoTokenizer.from_pretrained('Qwen/Qwen2.5-7B-Instruct')"

EXPOSE 8000

CMD ["python", "app.py"]