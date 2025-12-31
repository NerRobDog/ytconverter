FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Create downloads directory
RUN mkdir -p /downloads

# Expose the API port
EXPOSE 8000

# Set environment variable for downloads path
ENV PYTHONUNBUFFERED=1

# Run the API server
CMD ["python", "-m", "ytconverter", "--api", "--host", "0.0.0.0", "--port", "8000"]
