FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Git install mandatory for GitPython operations
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

COPY --from=builder /root/.local /home/mcpuser/.local
COPY . /app/

ENV PATH=/home/mcpuser/.local/bin:$PATH
ENV GITHUB_MCP_PORT=8080

USER mcpuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 8080)); s.close()"

CMD ["python", "server.py"]
