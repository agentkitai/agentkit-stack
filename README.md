# AgentKit Stack — Docker Compose

Run the full AgentKit ecosystem with a single `docker compose up`.

## Services

| Service    | Port | Image | Description |
|------------|------|-------|-------------|
| AgentLens  | 3000 | [`pazgaz/agentlens`](https://hub.docker.com/r/pazgaz/agentlens) | Observability dashboard |
| AgentGate  | 3002 | [`pazgaz/agentgate`](https://hub.docker.com/r/pazgaz/agentgate) | Approval gateway |
| Lore       | 8765 | *(built from source)* | Semantic memory (pgvector) |
| Lore DB    | —    | `pgvector/pgvector:pg16` | PostgreSQL + pgvector |
| Mesh       | 8766 | *(built from source)* | Agent discovery registry |

## Quick Start

```bash
git clone https://github.com/agentkitai/agentkit-stack.git
cd agentkit-stack
docker compose up -d
```

That's it. AgentLens and AgentGate pull from Docker Hub; Lore and Mesh build locally.

## Docker Hub Images

```bash
docker pull pazgaz/agentlens        # ~1GB (dashboard + server)
docker pull pazgaz/agentgate        # ~241MB (approval gateway)
```

## Health Checks

```bash
curl http://localhost:3000/api/health/overview   # AgentLens
curl http://localhost:3002/health                 # AgentGate
curl http://localhost:8765/health                 # Lore
curl http://localhost:8766/health                 # Mesh
```

## Rebuild from Source

To build AgentLens/AgentGate locally instead of pulling from Docker Hub, uncomment the `build:` lines in `docker-compose.yml` and remove the `image:` lines, then:

```bash
docker compose up -d --build
```

## Stop

```bash
docker compose down           # stop containers
docker compose down -v        # stop + remove volumes (data loss!)
```
