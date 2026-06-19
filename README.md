<p align="center">
  <h1 align="center">🚀 AgentKit Stack</h1>
  <p align="center">
    <strong>Run the full AgentKit ecosystem with a single command</strong><br>
    Docker Compose setup for AgentLens, AgentGate, Lore, and Mesh.
  </p>
  <p align="center">
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
    <a href="https://hub.docker.com/r/pazgaz/agentlens"><img src="https://img.shields.io/docker/v/pazgaz/agentlens?label=agentlens" alt="AgentLens Docker"></a>
    <a href="https://hub.docker.com/r/pazgaz/agentgate"><img src="https://img.shields.io/docker/v/pazgaz/agentgate?label=agentgate" alt="AgentGate Docker"></a>
  </p>
</p>

---

## Quick Start

```bash
git clone https://github.com/agentkitai/agentkit-stack.git
cd agentkit-stack
cp .env.example .env   # then edit .env and set real secrets
docker compose up -d
```

All four services pull pinned images from Docker Hub. Secrets are read from
`.env` (gitignored); `docker compose up` will refuse to start until the
required keys in `.env` are set.

## Services

| Service    | Port | Image | Description |
|------------|------|-------|-------------|
| AgentLens  | 3000 | [`pazgaz/agentlens:0.12.2`](https://hub.docker.com/r/pazgaz/agentlens) | Observability dashboard |
| AgentGate  | 3002 | [`pazgaz/agentgate:0.12.1`](https://hub.docker.com/r/pazgaz/agentgate) | Approval gateway |
| Lore       | 8765 | [`pazgaz/lore:1.1.1`](https://hub.docker.com/r/pazgaz/lore) | Semantic memory (pgvector) |
| Lore DB    | —    | `pgvector/pgvector:pg16` | PostgreSQL + pgvector |
| Mesh       | 8766 | [`pazgaz/agentkit-mesh:1.3.0`](https://hub.docker.com/r/pazgaz/agentkit-mesh) | Agent discovery registry |

## Docker Hub Images

```bash
docker pull pazgaz/agentlens:0.12.2      # dashboard + server
docker pull pazgaz/agentgate:0.12.1      # approval gateway
docker pull pazgaz/lore:1.1.1            # semantic memory
docker pull pazgaz/agentkit-mesh:1.3.0   # agent discovery registry
```

## Health Checks

```bash
curl http://localhost:3000/api/health/overview   # AgentLens
curl http://localhost:3002/health                 # AgentGate
curl http://localhost:8765/health                 # Lore
curl http://localhost:8766/health                 # Mesh
```

## Rebuild from Source

By default every service pulls a pinned image from Docker Hub. To build any of
them from a local checkout instead, uncomment that service's `build:` lines in
`docker-compose.yml` (each expects the sibling repo checked out alongside this
one), then:

```bash
docker compose up -d --build
```

## Stop

```bash
docker compose down           # stop containers
docker compose down -v        # stop + remove volumes (data loss!)
```

## 🤝 Contributing

Contributions are welcome! Fork the repo, make your changes, and open a pull request. For major changes, open an issue first to discuss what you'd like to change.

## 🧰 AgentKit Ecosystem

| Project | Description | |
|---------|-------------|-|
| [AgentLens](https://github.com/agentkitai/agentlens) | Observability & audit trail for AI agents | |
| [Lore](https://github.com/agentkitai/lore) | Cross-agent memory and lesson sharing | |
| [AgentGate](https://github.com/agentkitai/agentgate) | Human-in-the-loop approval gateway | |
| [FormBridge](https://github.com/agentkitai/formbridge) | Agent-human mixed-mode forms | |
| [AgentEval](https://github.com/agentkitai/agenteval) | Testing & evaluation framework | |
| [agentkit-mesh](https://github.com/agentkitai/agentkit-mesh) | Agent discovery & delegation | |
| [agentkit-cli](https://github.com/agentkitai/agentkit-cli) | Unified CLI orchestrator | |
| [agentkit-guardrails](https://github.com/agentkitai/agentkit-guardrails) | Reactive policy guardrails | |
| **agentkit-stack** | Full-stack Docker Compose setup | ⬅️ you are here |

## License

[MIT](LICENSE) © [Amit Paz](https://github.com/amitpaz)
