# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Ensure static/outputs exists
RUN mkdir -p static/outputs

# Expose the port (GCP Cloud Run uses PORT env var, but we'll default to 8080)
EXPOSE 8080

# Command to run the application
# We use 0.0.0.0 to allow external access within the container
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
