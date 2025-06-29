# -------- Step 1: Build Dependencies --------
FROM python:3.11-slim AS builder

# Avoid writing pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools and headers
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python packages to wheel format
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# -------- Step 2: Create Minimal Runtime Image --------
FROM python:3.11-slim

WORKDIR /app

# Install only what is needed at runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    libffi8 \
    libssl3 \
 && rm -rf /var/lib/apt/lists/*

# Install wheels built in builder stage
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy your full app (main.py, app/, .env etc.)
COPY . .

# Set the command to run FastAPI via uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
