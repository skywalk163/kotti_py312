# Dockerfile for kotti2_g4f
FROM python:3.12-slim

LABEL maintainer="Kotti Developers <kotti@googlegroups.com>"
LABEL description="kotti2_g4f - GPT4Free integration for Kotti2 CMS"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -e ".[testing]"

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Default command
CMD ["pserve", "development.ini", "--reload"]
