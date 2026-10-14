from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI(title="Prometheus MCP Server", version="1.0.0")

PROMETHEUS_ENDPOINT = os.getenv("PROMETHEUS_ENDPOINT", "http://prometheus-k8s.monitoring.svc:9090")

class PromQLQuery(BaseModel):
    query: str

@app.get("/healthz")
def healthz():
    return {"status": "ok", "mcp_server": "prometheus"}

@app.post("/mcp/query")
async def execute_promql(payload: PromQLQuery):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PROMETHEUS_ENDPOINT}/api/v1/query", params={"query": payload.query})
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prometheus MCP Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
