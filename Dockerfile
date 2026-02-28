FROM python:3.11-slim

# Better logging + no .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# (Optional but useful) minimal OS deps for healthchecks / some wheels
# If you use psycopg2-binary you may NOT need build deps.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user early
RUN useradd -m appuser

# Cache-friendly dependency install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source
COPY src /app/src

# Ensure uploads dir exists and permissions are correct
RUN mkdir -p /app/src/backend/uploads && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

# Healthcheck (simple + readable)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:5000/api/health || exit 1

# Run Flask via Gunicorn (ensure app.py contains: app = Flask(...))
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]