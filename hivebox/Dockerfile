# Use specific Python version with security patches
   FROM python:3.11.6-slim-bookworm
   
   # Set environment variables
   ENV PYTHONDONTWRITEBYTECODE=1 \
       PYTHONUNBUFFERED=1 \
       PYTHONPATH=/app \
       PORT=5000
   
   # Install system dependencies including curl for health check
   RUN apt-get update \
       && apt-get install -y --no-install-recommends \
           gcc \
           libc6-dev \
           curl \
       && rm -rf /var/lib/apt/lists/*
   
   # Create app user for security
   RUN useradd --create-home --shell /bin/bash app
   
   # Set working directory
   WORKDIR /app
   
   # Copy and install requirements as app user
   COPY requirements.txt .
   RUN pip install --no-cache-dir --upgrade pip \
       && pip install --no-cache-dir -r requirements.txt
   
   # Copy application code
   COPY app/ ./app/
   
   # Change ownership to app user
   RUN chown -R app:app /app
   USER app
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
       CMD curl -f http://localhost:$PORT/health || exit 1
   
   # Expose port
   EXPOSE $PORT
   
   # Use gunicorn for production
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.api:create_app()"]

    # EXPOSE 8000
    # CMD ["python", "-m", "app.main", "serve"]