FROM python:3.9-slim AS challenge

RUN mkdir /challenge && \
    chmod 700 /challenge

WORKDIR /app
COPY main.py /app/challenge.py

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cryptography

# Copy flag.txt to /app for your code to use (internal only)
COPY flag.txt /app/flag.txt
# Generate metadata.json without bundling flag.txt in artifacts.tar.gz
RUN echo "{\"flag\":\"$(cat /app/flag.txt)\"}" > /challenge/metadata.json

CMD ["python", "challenge.py"]
