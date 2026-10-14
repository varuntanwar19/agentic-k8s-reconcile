from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="GitHub MCP Server", version="1.0.0")

class PRRequest(BaseModel):
    title: str
    body: str

class CommitRequest(BaseModel):
    repo: str
    branch: str

@app.get("/healthz")
def healthz():
    return {"status": "ok", "mcp_server": "github"}

@app.post("/mcp/commits")
def get_recent_commits(req: CommitRequest):
    # Mocking GitHub API for MCP payload
    return {
        "commits": [
            {"sha": "a1b2c3d4", "author": "sre-dev", "message": "feat: update memory settings"},
            {"sha": "e5f6g7h8", "author": "ci-bot", "message": "chore: trigger deployment"}
        ]
    }

@app.post("/mcp/create-pr")
def create_pull_request(req: PRRequest):
    return {
        "status": "created",
        "pr_url": "https://github.com/enterprise/gitops-repo/pull/142",
        "title": req.title
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)