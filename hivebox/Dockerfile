# Use official Python runtime as base image
FROM python:3.11-slim
   
# Set working directory in container
WORKDIR /app
   
# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
   
# Copy application code
COPY app/ ./app/
   
# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app
   
# Set environment variables
ENV PYTHONPATH=/app
   
# Run the application
CMD ["python", "-m", "app.main"]