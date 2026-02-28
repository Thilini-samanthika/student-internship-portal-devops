FROM python:3.11-slim

# Better logging + avoid .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Minimal OS deps (curl used for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user (least privilege)
RUN useradd -m appuser

# Cache-friendly dependency install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source code
COPY src /app/src

# Ensure uploads directory exists and set permissions
RUN mkdir -p /app/src/backend/uploads && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

# Container healthcheck endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:5000/api/health || exit 1

# Start via Gunicorn (expects src/backend/app.py has: app = Flask(...))
WORKDIR /app/src/backend
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]