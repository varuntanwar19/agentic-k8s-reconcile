FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

COPY --from=builder /root/.local /home/mcpuser/.local
COPY . /app/

ENV PATH=/home/mcpuser/.local/bin:$PATH
ENV PROMETHEUS_MCP_PORT=9090

USER mcpuser

EXPOSE 9090

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 9090)); s.close()"

CMD ["python", "server.py"]

