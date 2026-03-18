# This root Dockerfile allows GCP to find a default build target
# It builds the Backend by default as it is the core of the application

FROM python:3.10-slim

WORKDIR /app

# Copy requirements from the backend folder
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY backend/ .

# Ensure the output directory exists
RUN mkdir -p static/outputs

# GCP Cloud Run uses the PORT environment variable
EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
