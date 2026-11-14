
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY *.py ./
COPY payment.ini ./

EXPOSE 8080

CMD ["uwsgi", "--ini", "payment.ini"]
