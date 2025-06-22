# -------- Step 1: Build Dependencies --------
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# -------- Step 2: Run App --------
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy app code
COPY app ./app

# Command to run your app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
