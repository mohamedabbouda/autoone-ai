FROM python:3.12-slim

WORKDIR /app

# Install system deps (needed for some Python libs)
RUN apt-get update && apt-get install -y build-essential

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose API port (FastAPI default)
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]