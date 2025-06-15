# Use PyTorch base image with CUDA
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/.cache/huggingface
ENV LANGCHAIN_API_KEY=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
ENV LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
ENV LANGCHAIN_PROJECT=govassist-dev
ENV LANGCHAIN_TRACING_V2=true

# Install system packages
RUN apt-get update && apt-get install -y \
    git curl build-essential \
    libgl1-mesa-glx \
    poppler-utils \
    libglib2.0-0 \
    tesseract-ocr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy files
COPY . .

# Install pip packages in stages
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu118 \
        torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 && \
    pip install --no-cache-dir "numpy<2.0.0" && \
    pip install --no-cache-dir -r requirements.txt

# Expose the Gradio app port
EXPOSE 7860

# Start the Gradio app
CMD ["python", "frontend/frontend_app.py"]
