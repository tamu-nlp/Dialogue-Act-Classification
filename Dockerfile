# Dockerfile for the TAMU Dialogue Act Classifier

from python:latest

EXPOSE 1883

COPY requirements.txt .
COPY scripts ./scripts
COPY message_bus ./message_bus

# Install dependencies
COPY data ./data
RUN ./scripts/install
COPY *.py ./
