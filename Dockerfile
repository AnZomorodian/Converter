# Multi-stage build for Fily Pro
FROM python:3.11-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY pyproject.toml .
COPY uv.lock .
RUN pip install uv && uv sync --frozen

# Production stage
FROM python:3.11-slim

# Install system dependencies including LibreOffice
RUN apt-get update && apt-get install -y \
    libreoffice \
    curl \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN groupadd -r filyuser && useradd -r -g filyuser filyuser

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=filyuser:filyuser . .

# Create necessary directories
RUN mkdir -p uploads converted temp logs && \
    chown -R filyuser:filyuser uploads converted temp logs

# Switch to non-root user
USER filyuser

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/system-health || exit 1

# Expose port
EXPOSE 5000

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--max-requests", "1000", "--max-requests-jitter", "100", "main:app"]