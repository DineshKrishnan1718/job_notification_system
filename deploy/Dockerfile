FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=Asia/Kolkata
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY templates ./templates
COPY deploy/entrypoint.sh ./entrypoint.sh
RUN useradd --create-home --shell /usr/sbin/nologin appuser && chmod +x /app/entrypoint.sh && mkdir -p /app/logs && chown -R appuser:appuser /app
USER appuser
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "app/scheduler/run_scheduler.py"]
