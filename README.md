<p align="center">
  <h1 align="center">🚀 AgentKit Stack</h1>
  <p align="center">
    <strong>Run the full AgentKit ecosystem with a single command</strong><br>
    Docker Compose setup for AgentLens, AgentGate, and Lore.
  </p>
  <p align="center">
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
    <a href="https://github.com/orgs/agentkitai/packages/container/package/agentlens"><img src="https://img.shields.io/badge/ghcr-agentlens-blue?logo=docker" alt="AgentLens Docker"></a>
    <a href="https://github.com/orgs/agentkitai/packages/container/package/agentgate"><img src="https://img.shields.io/badge/ghcr-agentgate-blue?logo=docker" alt="AgentGate Docker"></a>
  </p>
</p>

---

## Quick Start

Zero local setup — open the whole stack in a cloud dev environment (a thin
[devcontainer](.devcontainer/devcontainer.json) with Docker-in-Docker; it seeds
`.env` for you, then just `docker compose up -d`):

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/agentkitai/agentkit-stack)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode%3A%2F%2Fms-vscode-remote.remote-containers%2FcloneInVolume%3Furl%3Dhttps%3A%2F%2Fgithub.com%2Fagentkitai%2Fagentkit-stack)

Or locally:

```bash
git clone https://github.com/agentkitai/agentkit-stack.git
cd agentkit-stack
cp .env.example .env   # then edit .env and set real secrets
docker compose up -d
```

All four services pull pinned images from GHCR (ghcr.io/agentkitai). Secrets are read from
`.env` (gitignored); `docker compose up` will refuse to start until the
required keys in `.env` are set.

## Profiles

Run only the slice you need with [Compose profiles](https://docs.docker.com/compose/profiles/):

| Profile      | Services                                   | For |
|--------------|--------------------------------------------|-----|
| `minimal`    | AgentLens, Lore (+ Lore DB)                | Observability + memory |
| `governance` | `minimal` + AgentGate                      | Compliance: approval gateway / guardrails |
| `full`       | alias of `governance`                      | Everything (the default) |

```bash
docker compose --profile minimal up -d      # leanest
docker compose --profile governance up -d   # + approval gateway
docker compose up -d                         # full (COMPOSE_PROFILES=full in .env)
```

The default `docker compose up` activates `full` via `COMPOSE_PROFILES` in
`.env` — set it to `minimal` or `governance` there to change the default.

## Services

| Service    | Port | Image | Description |
|------------|------|-------|-------------|
| AgentLens  | 3000 | [`ghcr.io/agentkitai/agentlens:latest`](https://github.com/orgs/agentkitai/packages/container/package/agentlens) | Observability dashboard |
| AgentGate  | 3002 | [`ghcr.io/agentkitai/agentgate:latest`](https://github.com/orgs/agentkitai/packages/container/package/agentgate) | Approval gateway |
| Lore       | 8765 | [`ghcr.io/agentkitai/lore:latest`](https://github.com/orgs/agentkitai/packages/container/package/lore) | Semantic memory (pgvector) |
| Lore DB    | —    | `pgvector/pgvector:pg16` | PostgreSQL + pgvector |

## Images (GHCR)

```bash
docker pull ghcr.io/agentkitai/agentlens:latest      # dashboard + server
docker pull ghcr.io/agentkitai/agentgate:latest      # approval gateway
docker pull ghcr.io/agentkitai/lore:latest            # semantic memory
```

## Health Checks

```bash
curl http://localhost:3000/api/health/overview   # AgentLens
curl http://localhost:3002/health                 # AgentGate
curl http://localhost:8765/health                 # Lore
```

## Rebuild from Source

By default every service pulls a pinned image from GHCR. To build any of
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
| [agentkit-cli](https://github.com/agentkitai/agentkit-cli) | Unified CLI orchestrator | |
| **agentkit-stack** | Full-stack Docker Compose setup | ⬅️ you are here |

## License

[MIT](LICENSE) © [Amit Paz](https://github.com/amitpaz)
