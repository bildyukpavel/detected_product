FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Detected_model.py .
COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
