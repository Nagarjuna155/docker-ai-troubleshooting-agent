# docker-ai-troubleshooting-agent
An MCP-powered AI agent that troubleshoots Docker containers through natural-language conversation


# Docker AI Troubleshooting Agent

An MCP-powered AI agent that troubleshoots Docker containers through
natural-language conversation. Ask about running containers, logs, or
issues in plain English, and get answers backed by real `docker` command
output — not hallucinated guesses.

## How it works

```
You (terminal)
     │
     ▼
LangChain agent (Ollama LLM + tool-calling loop)
     │
     ▼
MCP client  ──stdio──▶  docker_mcp_server.py (FastMCP)
                             │
                             ▼
                     subprocess → docker CLI
                             │
                             ▼
                        Docker daemon
```

The agent doesn't call Docker directly. Instead, `docker_mcp_server.py`
exposes a small set of narrow, well-documented tools over MCP (Model
Context Protocol). The LLM reads each tool's docstring, decides which
tool fits the user's question, calls it, and turns the raw `docker`
output into a plain-English answer — including basic root-cause
reasoning (e.g. spotting a crash from container logs).

## Tools exposed

| Tool | What it does |
|---|---|
| `show_running_containers` | Runs `docker ps` — lists currently running containers |
| `show_all_containers` | Runs `docker ps -a` — lists all containers, including stopped ones |
| `show_container_logs_by_name` | Runs `docker logs --tail 200 <name>` — fetches recent logs for a named container, for debugging and RCA |

## Prerequisites

- Python 3.10+
- Docker installed and running locally
- [Ollama](https://ollama.com) installed, with a model pulled:
  ```bash
  ollama pull gemma4:26b
  ```
  (or any other local model you have — update the `model=` value in
  `docker_agent_mcp.py` to match whatever `ollama list` shows you)

## Setup

```bash
git clone https://github.com/Nagarjuna155/docker-ai-troubleshooting-agent.git
cd docker-ai-troubleshooting-agent
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python docker_agent_mcp.py
```

Example session:
```
Docker MCP Assistant — ask about containers, logs, issues, or RCA.
Type 'exit' or 'quit' to stop.

You: show me running containers
Assistant: You have 2 containers running: nginx-web (Up 3 hours) and
redis-cache (Up 3 hours).

You: any errors in nginx-web logs?
Assistant: I checked the last 200 lines — no errors, just standard
access logs. Everything looks healthy.

You: exit
Goodbye.
```

## Files

| File | Purpose |
|---|---|
| `docker_mcp_server.py` | MCP server exposing Docker-backed tools |
| `docker_agent_mcp.py` | Interactive agent runner (LangChain + Ollama + MCP client), keeps conversation history so follow-up questions have context |
| `requirements.txt` | Python dependencies |

## Notes / current limitations

This is a **learning-grade implementation** — read-only tools, minimal
input validation, no rate limiting or output redaction. It's built for
local experimentation against your own Docker host, not for pointing at
shared or production infrastructure as-is.
