
from fastapi import FastAPI
from pydantic import BaseModel
from graph import remediation_app

app = FastAPI(title="Remediation Agent API", version="1.0.0")

class ActionRequest(BaseModel):
    incident_id: str
    rca_report: str

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "remediation-agent"}

@app.post("/api/v1/remediate")
async def remediate_incident(req: ActionRequest):
    initial_state = {"rca_report": req.rca_report}
    result = await remediation_app.ainvoke(initial_state)
    return {
        "incident_id": req.incident_id,
        "action_taken": result.get("remediation_action"),
        "pull_request": result.get("github_pr_url"),
        "success": result.get("applied_status")
    }