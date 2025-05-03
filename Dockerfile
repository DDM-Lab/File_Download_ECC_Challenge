FROM python:3.9-slim AS challenge

RUN mkdir /challenge && \
    chmod 700 /challenge

WORKDIR /app
COPY main.py setup_challenge.py ./
COPY start.sh /opt/
RUN chmod +x /opt/start.sh

ARG SEED
ENV SEED=${SEED}
ARG FLAG
ENV FLAG=${FLAG}

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cryptography

RUN python setup_challenge.py

# The start.sh script starts a socat listener on port 5555, that connects to the
# python script.
EXPOSE 5555
# PUBLISH 5555 AS socat
CMD ["/opt/start.sh"]
