# AgentKit Stack — Docker Compose

Run the AgentKit ecosystem via Docker Desktop on Windows.

## Services

| Service    | Port | Description                        | Health Check          |
|------------|------|------------------------------------|-----------------------|
| AgentLens  | 3000 | Observability server + dashboard   | `GET /api/health/overview` |
| AgentGate  | 3002 | Approval gateway server            | `GET /health`         |

> **Note:** FormBridge and agentkit-mesh are libraries/CLI tools, not long-running servers — they are not included.

## Quick Start

```bash
cd /path/to/agentkit-stack
docker compose up -d --build
```

## Check Status

```bash
docker compose ps
docker compose logs -f          # all services
docker compose logs -f agentlens  # single service
```

## Health Checks

```bash
curl http://localhost:3000/api/health/overview   # AgentLens
curl http://localhost:3002/health                 # AgentGate
```

## Stop

```bash
docker compose down           # stop containers
docker compose down -v        # stop + remove volumes (data loss!)
```

## Rebuild After Code Changes

```bash
docker compose up -d --build
```
