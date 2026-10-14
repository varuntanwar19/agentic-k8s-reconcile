from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
import operator

# 1. State Definition
class TrapperState(TypedDict):
    raw_alert: Dict[str, Any]
    parsed_labels: Dict[str, str]
    prometheus_metrics: Dict[str, Any]
    incident_payload: Dict[str, Any]
    next_node: str

# 2. Node Implementations
def parse_alert_node(state: TrapperState) -> Dict[str, Any]:
    alert = state.get("raw_alert", {})
    labels = alert.get("labels", {})
    return {"parsed_labels": labels}

def fetch_prom_context_node(state: TrapperState) -> Dict[str, Any]:
    # Interacts with Prometheus MCP Server
    labels = state.get("parsed_labels", {})
    alert_name = labels.get("alertname", "Unknown")
    return {"prometheus_metrics": {"alert": alert_name, "rate_5m": "45.2 req/s", "error_ratio": "12.4%"}}

def synthesize_incident_node(state: TrapperState) -> Dict[str, Any]:
    return {
        "incident_payload": {
            "title": f"CRITICAL: {state['parsed_labels'].get('alertname')}",
            "service": state['parsed_labels'].get('service', 'unknown'),
            "context": state['prometheus_metrics']
        }
    }

# 3. Graph Assembly
workflow = StateGraph(TrapperState)
workflow.add_node("parse_alert", parse_alert_node)
workflow.add_node("fetch_prom_context", fetch_prom_context_node)
workflow.add_node("synthesize_incident", synthesize_incident_node)

workflow.set_entry_point("parse_alert")
workflow.add_edge("parse_alert", "fetch_prom_context")
workflow.add_edge("fetch_prom_context", "synthesize_incident")
workflow.add_edge("synthesize_incident", END)

event_trapper_app = workflow.compile()