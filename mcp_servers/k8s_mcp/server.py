
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kubernetes import client, config
import os

app = FastAPI(title="Kubernetes MCP Server", version="1.0.0")

try:
    config.load_incluster_config()
except:
    config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

class LogRequest(BaseModel):
    namespace: str
    service: str

class PatchRequest(BaseModel):
    action: str
    incident_id: str

@app.get("/healthz")
def healthz():
    return {"status": "ok", "mcp_server": "kubernetes"}

@app.post("/mcp/logs")
def fetch_pod_logs(req: LogRequest):
    try:
        pods = v1.list_namespaced_pod(namespace=req.namespace, label_selector=f"app={req.service}")
        logs = []
        for pod in pods.items[:3]:
            pod_log = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace=req.namespace, tail_lines=100)
            logs.append(f"Pod: {pod.metadata.name}\n{pod_log}")
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"K8s MCP Error: {str(e)}")

@app.post("/mcp/patch")
def apply_k8s_patch(req: PatchRequest):
    return {"status": "patched", "action": req.action, "incident_id": req.incident_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
