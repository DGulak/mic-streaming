FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    libopus-dev \
    libvpx-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
