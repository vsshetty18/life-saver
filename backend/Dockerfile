# ===============================
# Dockerfile for Render Deployment
# Uses Python 3.11 (slim) to avoid version conflicts with
# ultralytics/opencv on Render's default build environment.
# ===============================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout (cleaner logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required by OpenCV
# (libgl1 and libglib2.0-0 are commonly missing and cause OpenCV import errors)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (better Docker layer caching -
# dependencies only reinstall if requirements.txt changes)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Create uploads folder (in case it's not present)
RUN mkdir -p uploads

# Render provides the PORT environment variable at runtime
ENV PORT=5000
EXPOSE 5000

# Run with gunicorn in production (more robust than Flask's dev server)
# Note: gunicorn must be added to requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
