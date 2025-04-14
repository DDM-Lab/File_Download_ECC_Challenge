FROM python:3.9-slim AS challenge

RUN mkdir /challenge && \
    chmod 700 /challenge

WORKDIR /app
COPY flag.txt /app/
COPY main.py /app/challenge.py

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cryptography

CMD ["python", "challenge.py"]
