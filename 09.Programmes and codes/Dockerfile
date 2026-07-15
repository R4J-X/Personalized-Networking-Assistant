# Dockerfile — Personalized Networking Assistant (FastAPI backend)
#
# Build:  docker build -t networking-assistant-api .
# Run:    docker run -p 8000:8000 networking-assistant-api
#
# Note: This containerizes the FastAPI backend only. The Streamlit frontend
# can be run locally (pointed at this container via BASE_URL in
# frontend/app.py) or containerized separately using the same base image
# with `CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]`.

FROM python:3.11-slim

WORKDIR /app

# System dependencies required by torch/transformers wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY data/ ./data/

EXPOSE 8000

# Pre-download models at build time is optional; by default they download on
# first request/startup since the pipelines are instantiated at import time.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
