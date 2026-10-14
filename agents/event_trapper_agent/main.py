from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from graph import event_trapper_app

app = FastAPI(title="Event Trapper Agent API", version="1.0.0")

class AlertPayload(BaseModel):
    status: str
    labels: Dict[str, str]
    annotations: Dict[str, str]

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "event-trapper"}

@app.post("/webhook/alertmanager")
async def handle_alertmanager_webhook(payload: Dict[str, Any], background_tasks: BackgroundTasks):
    initial_state = {"raw_alert": payload}
    result = await event_trapper_app.ainvoke(initial_state)
    return {
        "status": "processed",
        "incident": result.get("incident_payload")
    } 