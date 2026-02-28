FROM python:3.11-slim

RUN useradd -m appuser

WORKDIR /app


COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt


COPY src /app/src

WORKDIR /app/src/backend

ENV FLASK_ENV=production
ENV PORT=5000


RUN mkdir -p uploads && chown -R appuser:appuser /app

USER appuser


HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/api/health')" || exit 1

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]