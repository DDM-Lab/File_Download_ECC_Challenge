FROM python:3.9-slim AS challenge

RUN mkdir /challenge && \
    chmod 700 /challenge

WORKDIR /app
# Don't copy flag.txt directly to /app - this causes the reference issue
# COPY flag.txt /app/  <- Remove this line
COPY main.py /app/challenge.py

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cryptography

# Instead, create the flag only inside the container or copy it directly to the artifacts
COPY flag.txt /tmp/flag.txt
RUN tar czvf /challenge/artifacts.tar.gz -C /tmp flag.txt && \
    echo "{\"flag\":\"$(cat /tmp/flag.txt)\"}" > /challenge/metadata.json && \
    # If your code needs access to the flag, create a copy in /app
    cp /tmp/flag.txt /app/flag.txt

CMD ["python", "challenge.py"]
