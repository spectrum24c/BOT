# Orchestration & Bridge Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY sample_data/ ./sample_data/
CMD ["pytest", "src/inference_server/tests"]
