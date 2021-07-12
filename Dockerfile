# Dockerfile for the TAMU Dialogue Act Classifier

from python:latest

COPY requirements.txt .
COPY scripts ./scripts

# Install dependencies
COPY data ./data
RUN ./scripts/install
COPY *.py ./
