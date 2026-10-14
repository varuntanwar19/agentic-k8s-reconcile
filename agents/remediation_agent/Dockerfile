FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r agentuser && useradd -r -g agentuser agentuser

COPY --from=builder /root/.local /home/agentuser/.local
COPY . /app/

ENV PATH=/home/agentuser/.local/bin:$PATH
ENV PORT=8082

USER agentuser

EXPOSE 8082

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8082/healthz')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]