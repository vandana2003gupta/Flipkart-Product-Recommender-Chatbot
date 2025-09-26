# Parent image
FROM python:3.10-slim

# Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Work directory inside the docker container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy all contents from local to /app
COPY . .

# Install package via setup.py
RUN pip install --no-cache-dir -e .

# Expose port (Cloud Run uses 8080)
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
