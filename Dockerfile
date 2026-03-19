# STAGE 1: Build the React Frontend
FROM node:18-slim AS frontend-build
WORKDIR /app/frontend

# Install dependencies (use legacy-peer-deps for Three.js compatibility)
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps

# Copy frontend source and build
COPY frontend/ ./
# We don't need VITE_API_URL, as the monolith uses relative paths
RUN npm run build

# STAGE 2: Build the Python Backend
FROM python:3.10-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Copy the built frontend from Stage 1 to backend's static/dist folder
# In the monolith, the backend serves the frontend from static/dist
RUN mkdir -p static/dist
COPY --from=frontend-build /app/frontend/dist ./static/dist

# Ensure the output directory for 3D models exists
RUN mkdir -p static/outputs

# GCP Cloud Run uses the PORT environment variable (default to 8080)
EXPOSE 8080

# Run uvicorn on 0.0.0.0 and port $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
