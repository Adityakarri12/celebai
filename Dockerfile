# Lean production Docker image for CelebraTech AI
FROM python:3.12-slim

WORKDIR /app

# Ensure python logs directly without buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and static assets
COPY app/ ./app/
COPY static/ ./static/
COPY run.py .
COPY README.md .

# Create and switch to non-root user for production security
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:' + str(8000) + '/health')" || exit 1

# Launch the FastAPI Uvicorn server
CMD ["python", "run.py"]
