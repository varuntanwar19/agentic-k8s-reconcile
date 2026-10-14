from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from graph import rca_app

app = FastAPI(title="RCA Agent API", version="1.0.0")

class DiagnoseRequest(BaseModel):
    incident_id: str
    incident_payload: Dict[str, Any]

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "rca-agent"}

@app.post("/api/v1/diagnose")
async def diagnose_incident(req: DiagnoseRequest):
    initial_state = {"incident_data": req.incident_payload}
    result = await rca_app.ainvoke(initial_state)
    return {
        "incident_id": req.incident_id,
        "rca_report": result.get("final_rca")
    }     