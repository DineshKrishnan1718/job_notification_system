# 1. Base Image: Lightweight Python 3.11
FROM python:3.11-slim

# 2. Environment Variables
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr (so logs appear immediately)
ENV PYTHONUNBUFFERED=1
# Ensure our scheduler runs in the correct timezone!
ENV TZ="Asia/Kolkata"

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies required for PostgreSQL (psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements and install them
# (Remember, because we set `context: ../` in docker-compose, this looks at the root folder!)
COPY requirements.txt .
# --no-cache-dir keeps the image size small
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY . .

# 7. Start the Scheduler when the container boots
CMD ["python", "app/scheduler/run_scheduler.py"]