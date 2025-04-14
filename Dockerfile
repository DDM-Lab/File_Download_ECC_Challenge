FROM python:3.9-slim AS challenge

RUN mkdir /challenge && \
    chmod 700 /challenge

WORKDIR /app
COPY challenge.py flag.txt start.sh ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x start.sh

RUN pip install --no-cache-dir cryptography
RUN echo "{\"flag\":\"$(cat flag.txt)\"}" > /challenge/metadata.json

# The start.sh script starts a socat listener on port 5555, that connects to the
# python script.
EXPOSE 5555
# PUBLISH 5555 AS socat
CMD ["./start.sh"]
