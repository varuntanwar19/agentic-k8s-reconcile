# agentic-k8s-reconcile
Multi Agent self healing framework using LangGraph, MCP, Helm Charts and ArgoCD

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Kubernetes](https://img.shields.io/badge/kubernetes-v1.28%2B-blue?logo=kubernetes)
![Helm](https://img.shields.io/badge/helm-v3.12%2B-white?logo=helm)
![ArgoCD](https://img.shields.io/badge/argocd-v2.9%2B-orange?logo=argo)
![LangGraph](https://img.shields.io/badge/framework-LangGraph%20v0.1-green)
![Model Context Protocol](https://img.shields.io/badge/protocol-MCP%20v1.0-purple)

> **Enterprise-Grade Event-Driven Autonomous Incident Detection, Root Cause Analysis (RCA), and Automated Remediation Engine for Mission-Critical Kubernetes Clusters.**

---

## 🏛️ Executive Architecture Overview

The **Autonomous AI-SRE Platform** is a Next-Generation Cognitive Infrastructure Engine designed for zero-touch Kubernetes reliability engineering. It combines state-of-the-art **LangGraph State Machine Orchestration**, standardized **Model Context Protocol (MCP)** tool execution servers, Prometheus metrics ingestion, and cloud-native **GitOps Continuous Deployment via ArgoCD**.

```
                          +-------------------------------------------------------+
                          |            KUBERNETES CLUSTER OBSERVABILITY          |
                          +-------------------------------------------------------+
                                                     |
                                          Prometheus Alertmanager
                                                     | Webhook
                                                     v
                                       +---------------------------+
                                       | Event Trapper Agent       |
                                       | (LangGraph Event Router)  |
                                       +---------------------------+
                                                     |
                                       +-------------+-------------+
                                       |                           |
                                       v                           v
                          +------------------------+   +------------------------+
                          |  RCA Agent             |   | Remediation Agent      |
                          |  (LangGraph Reasoning) |   | (LangGraph Execution)  |
                          +------------------------+   +------------------------+
                                      |                            |
         +----------------------------+----------------------------+----------------------------+
         |                            |                                                         |
         v                            v                                                         v
+-------------------+        +-------------------+                                     +-------------------+
|  Prometheus MCP   |        |  Kubernetes MCP   |                                     |    GitHub MCP     |
|     Server        |        |     Server        |                                     |      Server       |
+-------------------+        +-------------------+                                     +-------------------+
         |                            |                                                         |
         v                            v                                                         v
  Prometheus API               Kubernetes API Server                                    GitHub REST / GraphQL
(Metrics & Alerts Query)     (Pods, Logs, Events, Patch)                              (PRs, Commits, GitOps)
```

---

## 🏗️ Technical Stack & Architectural Layers

### 1. LangGraph Orchestrated Autonomous Agents
- **Event Trapper Agent (`agents/event-trapper`)**: High-throughput async ingestion engine listening to Prometheus Alertmanager, CloudWatch, and Event Hubs. Filters noise, deduplicates alerts, enriches context, and triggers the RCA workflow state machine.
- **Root Cause Analysis (RCA) Agent (`agents/rca-agent`)**: Deep diagnostic agent leveraging LangGraph stateful multi-step reasoning. Queries metrics via Prometheus MCP, reads live pod logs/events via K8s MCP, and correlates recent deployment changes via GitHub MCP.
- **Remediation Agent (`agents/remediation-agent`)**: Autonomous execution engine. Formulates patch plans, validates blast-radius policy via Kyverno/OPA, applies live hotfixes via K8s MCP, or opens GitOps Pull Requests via GitHub MCP for permanent infrastructure updates.

### 2. Model Context Protocol (MCP) Servers
- **Prometheus MCP Server (`mcp-servers/prometheus-mcp`)**: Standardized tool interface providing high-level abstraction for PromQL query evaluation, time-series anomaly detection, and metric threshold inspection.
- **Kubernetes MCP Server (`mcp-servers/k8s-mcp`)**: RBAC-isolated MCP bridge allowing granular read/write inspection of Cluster CRDs, Pod logs, deployment rollouts, service topologies, and patch operations.
- **GitHub MCP Server (`mcp-servers/github-mcp`)**: Secure GitHub API protocol server managing enterprise repositories, GitOps repository syncing, automated PR creation, and CI/CD status inspection.

### 3. GitOps & Helm Infrastructure (`charts/` & `argocd/`)
- **Helm 3 Microservice Architecture**: Fully parameterized, unified chart supporting decoupled deployments of Agents, MCP Servers, ConfigMaps, Secrets, HPAs, and Service Accounts.
- **ArgoCD GitOps App-of-Apps**: Declarative GitOps control loop featuring Custom Lua Health Checks for Agent CRDs, automated out-of-sync auto-healing, and canary deployment pipelines.

---

## 📁 Complete Repository Layout

```text
ai-sre-platform/
├── README.md                                  # Enterprise Architectural Documentation
├── charts/                                    # Unified Helm 3 Helm Chart
│   └── ai-sre-platform/
│       ├── Chart.yaml
│       ├── values.yaml                        # Multi-Environment Parameterization
│       └── templates/
│           ├── _helpers.tpl                   # Template Engine Helpers
│           ├── agents-deployment.yaml         # LangGraph Agents (Trapper, RCA, Remediation)
│           ├── mcp-servers-deployment.yaml    # MCP Protocol Servers (Prometheus, K8s, GitHub)
│           ├── crd-definition.yaml            # AutonomousAgentPolicy CRD Definition
│           ├── configmaps.yaml                # Prompt Templates & MCP Configs
│           ├── secrets.yaml                   # Vault-Integrated Secret Placeholders
│           ├── services.yaml                  # ClusterIP Services for Inter-Agent MCP
│           ├── hpa.yaml                       # Autoscaling Rules (CPU/Memory/Queue Depth)
│           └── rbac-serviceaccount.yaml       # ClusterRole & ServiceAccount Bindings
├── argocd/                                    # ArgoCD GitOps Engine
│   ├── root-app-of-apps.yaml                  # ArgoCD App-of-Apps Root Manifest
│   ├── dev-application.yaml                   # Development Environment Sync Rule
│   ├── prod-application.yaml                  # Production Environment Sync Rule (Auto-Heal)
│   ├── argocd-project.yaml                    # RBAC Security Boundaries & Whitelists
│   └── lua-health-checks.yaml                 # Custom Lua Health Check Scripts for ArgoCD
├── agents/                                    # Python LangGraph Microservices
│   ├── event_trapper/
│   │   ├── main.py                            # Async FastAPI Event Listener & Router
│   │   └── graph.py                           # LangGraph Trapper State Workflow
│   ├── rca_agent/
│   │   ├── main.py                            # Multi-Step Reasoning Engine
│   │   └── graph.py                           # LangGraph Deep-Diagnostic Graph
│   └── remediation_agent/
│       ├── main.py                            # Hotfix & GitOps PR Action Engine
│       └── graph.py                           # Safety-Gated Execution Workflow
└── mcp_servers/                               # MCP Tool Adapters
    ├── prometheus_mcp/
    │   └── server.py                          # PromQL & Alerting MCP Protocol Implementation
    ├── k8s_mcp/
    │   └── server.py                          # Kubernetes Client MCP Protocol Implementation
    └── github_mcp/
        └── server.py                          # GitOps & Repository Management MCP Adapter
```

---

## ⚡ Deployment & Quickstart Guide

### Prerequisites
- Kubernetes cluster (v1.28+)
- Helm 3.12+
- ArgoCD Controller deployed in `argocd` namespace
- `kubectl` configured with cluster-admin access

### Option 1: GitOps Deployment via ArgoCD (Recommended)

1. **Register ArgoCD App-of-Apps**:
   ```bash
   kubectl apply -f argocd/argocd-project.yaml
   kubectl apply -f argocd/lua-health-checks.yaml
   kubectl apply -f argocd/root-app-of-apps.yaml
   ```

2. **Verify Sync & Health Status**:
   ```bash
   argocd app get ai-sre-platform-prod
   ```

### Option 2: Direct Helm Chart Installation

```bash
# Dry-run render templates
helm template ai-sre-platform ./charts/ai-sre-platform --values ./charts/ai-sre-platform/values.yaml

# Install/Upgrade
helm upgrade --install ai-sre-platform ./charts/ai-sre-platform \
  --namespace ai-sre-system \
  --create-namespace \
  --values ./charts/ai-sre-platform/values.yaml
```

---

## 📊 Observability & Metrics

The platform exposes Prometheus metrics at `:9090/metrics`:
- `agent_event_trapper_ingested_total`: Count of raw alerts received.
- `agent_rca_diagnostics_duration_seconds`: Histogram of root cause determination latency.
- `agent_remediation_actions_executed_total`: Actions triggered segmented by `type="k8s_patch"` vs `type="github_pr"`.
- `mcp_server_request_latency_seconds`: Tool execution latency across Prometheus, K8s, and GitHub MCP servers.

---

## 🛡️ Security & Enterprise Governance
- **Zero Trust Service Mesh**: Inter-agent communication encrypted via mTLS.
- **Least-Privilege RBAC**: Kubernetes MCP server operates under restrictive ClusterRole bindings.
- **GitOps Audit Trail**: All production cluster modifications require human approval via GitHub PRs created by the Remediation Agent.

---
