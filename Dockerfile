<<<<<<< HEAD
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
=======
# Use official lightweight Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files & force stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy only source code (ignoring .git, venv, cache, etc.)
COPY . .

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
>>>>>>> fb74ba9e5ea1a37f37db3961a1b8c7e4d5e2f671

# Run the app
CMD ["python", "app.py"]
