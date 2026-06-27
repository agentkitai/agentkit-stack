#!/usr/bin/env python3
"""Generate the AgentKitAI suite overview static site (index + one page per repo)."""
import html, pathlib

# Writes the site next to this script (docs/overview/). Run `python gen_site.py`
# from anywhere to regenerate index.html + one page per product + styles.css.
OUT = pathlib.Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

# ---- data ---------------------------------------------------------------
PRODUCTS = [
  dict(slug="agentlens", emoji="🔍", name="AgentLens", tier="core",
    tagline="Open-source observability for AI agents — with a tamper-evident, hash-chained audit trail.",
    role="Observability + audit", lang="TypeScript + Python SDK", version="0.15.1",
    status="Flagship · most mature",
    purpose="A flight recorder for AI agents: captures every LLM call, tool invocation, approval decision, and error, then exposes them via a queryable API and real-time dashboard. Its differentiator is that every event is SHA-256 hash-chained to the previous one — alter, delete, or reorder a single record after the fact and verification fails, pointing at the exact event that broke. Purpose-built for EU AI Act Article 12 record-keeping and the emerging IETF Agent Audit Trail work.",
    architecture="A Node/Hono server + React dashboard ingest events through five entry points and write them to an append-only, per-session hash-chained store. SQLite by default (zero config); Postgres + Redis for scale. OTel GenAI spans are mapped into the AgentLens model (llm_call/llm_response/tool_call) and hash-chained like any other event; cost is reconstructed from per-model pricing when the source reports only tokens. Auditors export a signed JSON snapshot from GET /api/audit/verify/export; the server verdict can be independently re-walked client-side.",
    features=[
      "Tamper-evident audit: append-only, SHA-256 hash-chained per session; GET /api/audit/verify + signed /verify/export",
      "Five ways to integrate, zero lock-in: OpenTelemetry GenAI (no SDK), 1-line Python auto-instrumentation (9 providers), OpenClaw plugin, TS/Python SDK, MCP server",
      "22 MCP tools spanning observability, analytics, and operations",
      "Real-time dashboard: session timelines, event explorer, LLM analytics, cost tracking, alerting",
      "Cost tracking per session / agent / model with spike alerts; cost reconstructed even for OTel-only agents",
      "Billing-grade per-agent spend tracking (A+B+C)",
      "5-dimension health scores with trend tracking",
      "Session replay — step through any past session with full context",
      "A/B benchmarking with Welch's t-test + chi-squared",
      "Complexity-aware model-recommendation cost optimizer with projected savings",
      "Automated guardrails with dry-run mode",
      "Framework plugins (LangChain, CrewAI, AutoGen, Semantic Kernel) — auto-detect, fail-safe, non-blocking",
      "Multi-tenant isolation with per-tenant data scoping and API-key binding",
    ],
    interfaces=[
      "HTTP API: /api/audit/verify, /api/audit/verify/export, /api/stats, /api/keys, OTLP /v1/traces",
      "22 MCP tools (npx @agentkitai/agentlens-mcp)",
      "Python SDK: agentlensai (AgentLensClient, agentlensai.init())",
      "TypeScript SDK: @agentkitai/agentlens-sdk (AgentLensClient)",
      "Real-time React web dashboard",
      "Docker image: ghcr.io/agentkitai/agentlens (port 3400)",
    ],
    fits="The observability hub of the suite. AgentGate logs its approval decisions here; AgentEval imports production sessions from here as test fixtures and emits eval results back as tamper-evident evidence; agentkit-guardrails watches its metrics to drive reactive policy. Shares the @agentkitai/auth and @agentkitai/pricing libraries with the rest of the suite.",
    notable="The hash-chain is the whole thesis: an agent's behavior becomes not just logged but cryptographically defensible. Cost is reconstructed from model pricing so even SDK-less OTel agents get full cost analytics. Deterministic, fail-safe, non-blocking capture with optional PII redaction.",
    stack="Node.js / Hono · React + Vite dashboard · SQLite (default) → PostgreSQL + Redis · OpenTelemetry ingest · Python SDK (9 provider integrations)",
    links=dict(repo="https://github.com/agentkitai/agentlens", npm="https://www.npmjs.com/package/@agentkitai/agentlens-server", pypi="https://pypi.org/project/agentlensai/")),

  dict(slug="agentgate", emoji="🛂", name="AgentGate", tier="core",
    tagline="Human-in-the-loop approval gateway with policy-based auto-approval, auto-denial, and multi-channel notifications.",
    role="Governance / approval", lang="TypeScript", version="core 0.1.0",
    status="Active · pre-1.0",
    purpose="Keeps humans in control of what AI agents can do by intercepting requests and evaluating them against policies that auto-approve safe actions, auto-deny dangerous ones, and route ambiguous requests to human approvers via web dashboard, Slack, Discord, or email. Provides complete audit trails for compliance and tags every decision with an OWASP LLM Top-10 risk classification.",
    architecture="Agents submit approval requests to an authenticated Hono HTTP API. A policy engine evaluates each request against prioritized, scope-gated rules (per-agent, per-tool, or global) using comparison operators and emits one of four decisions. Real-time HMAC-signed webhooks deliver notifications with exponential-backoff retry. Humans decide via React dashboard, Slack DM, or Discord channel — or a one-click decision link. SQLite (dev) / PostgreSQL (prod) stores requests, policies, keys, audit logs; Redis handles sliding-window rate limiting and queues. Background scanners handle overrides, escalation, and webhook retries with graceful shutdown.",
    features=[
      "Policy engine: rule matching on action/params/context with $lt/$gt/$lte/$gte/$in/$regex operators",
      "Four decision types: auto_approve, auto_deny, route_to_human, route_to_agent — with per-rule approver + channel",
      "Multi-channel approvals: React dashboard, Slack DM bot, Discord channel bot, email (SMTP)",
      "One-click decision links — passwordless approve/deny from the notification itself",
      "OWASP LLM Top-10 risk classification on every decision (compliance evidence)",
      "Full audit trail with actor namespaces (dashboard:/slack:/discord:/mcp:/policy:/api:/system)",
      "Agent identity verification via token signing (SPIFFE support)",
      "Per-agent budget / spend limits with alerts",
      "Override system for per-agent escalation gates (require_approval / deny)",
      "HMAC-SHA256 signed webhooks with event filtering + exponential-backoff retry",
      "API keys with fine-grained scopes + per-key sliding-window rate limiting",
      "Hardened: SSRF protection, ReDoS defense (safe-regex2), CORS, security headers, graceful shutdown",
    ],
    interfaces=[
      "HTTP REST API (POST /api/requests, /api/requests/:id/decide, /api/overrides, …)",
      "10 MCP tools: agentgate_request/get/list/decide, policy CRUD, audit queries",
      "CLI: agentgate config / request / status / list / approve / deny / override",
      "TypeScript SDK: AgentGateClient",
      "React web dashboard (requests, policies, keys, webhooks, audit search)",
      "Slack bot · Discord bot · outbound webhooks",
    ],
    fits="The governance and approval layer of the control plane. Logs every decision to AgentLens; receives reactive policy overrides from agentkit-guardrails when AgentLens metrics breach; consumes the shared @agentkitai/auth library. Drives human approvals through Slack/Discord for teams.",
    notable="Operator-based policy matching with scope gating, passwordless decision-token links, per-agent budget enforcement, and an OWASP-LLM risk tag on every decision — designed so the approval record is itself compliance evidence. Docker secrets via the _FILE env convention.",
    stack="TypeScript 5.7 · Hono · Drizzle ORM · SQLite/PostgreSQL · Redis · React + Tailwind · @slack/bolt · discord.js · jose (JWT) · Vitest",
    links=dict(repo="https://github.com/agentkitai/agentgate", npm="https://www.npmjs.com/package/@agentkitai/agentgate-server")),

  dict(slug="lore", emoji="🧠", name="Lore", tier="core",
    tagline="Cross-agent semantic memory with knowledge graphs, fact extraction, and bi-temporal history.",
    role="Memory / knowledge", lang="Python", version="1.3.0",
    status="Active · beta",
    purpose="Solves the statelessness problem of AI agents by providing a persistent memory layer that stores, connects, and retrieves knowledge across any agent without code changes. Hooks intercept agent activity so agents automatically remember lessons, decisions, and patterns; graph traversal surfaces connected information that vector search alone would miss; auto-snapshots give session continuity.",
    architecture="Local-first by default with an optional remote FastAPI backend. A pluggable MemoryStore protocol backs either SQLite + sqlite-vec (in-process) or PostgreSQL + pgvector (remote). A hook system (UserPromptSubmit / PostToolUse / SessionEnd) drives auto-retrieval and a background auto-capture pipeline — agents never import Lore. A knowledge-graph layer auto-extracts entities, relationships, and facts; retrieval blends semantic (embeddings), full-text (FTS/tsvector), and graph traversal. A session accumulator writes fire-and-forget snapshots that never block the caller.",
    features=[
      "Universal memory ops: remember, recall, forget, list, stats, upvote/downvote",
      "Knowledge graph: auto-extracted entities/relationships — graph_query, entity_map, related, conflicts, list_facts",
      "Interactive D3 force-directed graph UI at /ui/ with entity panels + topic clusters",
      "Session continuity: auto-snapshots + auto-inject via hooks, zero agent cooperation",
      "Bi-temporal facts: supersession chains, facts_at_time queries, timeline drill-down",
      "Scope isolation: project-scoped vs global memories; cross-project search via scope='all'",
      "Multi-agent hooks: Claude Code, Cursor, Codex, OpenClaw — auto-retrieve + auto-capture",
      "Risk-scored graph review: pending connection approval with computed risk scores + audit",
      "Adaptive retrieval profiles (coding, incident-response, research)",
      "Policy-based retention, cron snapshot schedules, restore drills, compliance dashboard",
      "Multi-tenant workspaces with RBAC, scoped keys, SLO dashboard + breach alerts",
      "Plugin SDK (entry_points, 5 lifecycle hooks, hot-reload) + automatic PII redaction",
    ],
    interfaces=[
      "40+ MCP tools (remember/recall/graph_query/extract_facts/timeline/snapshot/…)",
      "25+ REST endpoints under /v1/* (memories, search, retrieve, graph, workspaces, SLO, …)",
      "CLI: lore with 20+ subcommands (remember, recall, graph, facts, serve, mcp, ui, workspace, …)",
      "Web UI at /ui/ (D3 graph, entity panels, topic clusters, search)",
      "Python SDK: Lore (async, local-first or remote)",
      "Published: PyPI/npm lore-sdk · ghcr.io/agentkitai/lore",
    ],
    fits="The persistent memory layer of the suite. Integrates with every major coding agent via hooks (auto-retrieve before prompts, auto-capture after) and via its MCP server for explicit access. Multi-tenant workspaces isolate team memories; global scopes share cross-project learnings.",
    notable="Bi-temporal facts with explicit supersession chains (history without deletion), scope-based isolation preventing cross-project contamination, risk-scored graph connections gating when relationships are exposed, automatic PII redaction, and hook-based invisibility — agents never import Lore.",
    stack="Python 3.10+ · FastAPI / Uvicorn / Pydantic · PostgreSQL + pgvector (remote) or SQLite + sqlite-vec (local) · ONNX MiniLM embeddings · ULID · MCP · optional LiteLLM enrichment",
    links=dict(repo="https://github.com/agentkitai/lore", pypi="https://pypi.org/project/lore-sdk/", npm="https://www.npmjs.com/package/lore-sdk")),

  dict(slug="formbridge", emoji="📝", name="FormBridge", tier="core",
    tagline="Mixed-mode agent↔human form submission — agents fill what they know, humans complete the rest.",
    role="Agent-human handoff", lang="TypeScript", version="0.3.0",
    status="Active",
    purpose="AI agents can gather most of a form's data, but some fields need a human — signatures, file uploads, identity verification, subjective judgment. FormBridge handles the handoff: the agent fills what it knows and hands off a secure resume URL; the human opens a pre-filled form with attribution badges and completes the rest, with full field-level attribution and approval workflows.",
    architecture="Built on Hono. The agent POSTs a submission and fills known fields; FormBridge returns a rotating resume token + handoff URL. A submission state machine (draft → in_progress → submitted → finalized, plus review/approval/upload branches) governs lifecycle; resume tokens rotate on every state change. A triple-write pattern records each event to the submission array, an event emitter (webhook fan-out), and an append-only event store. Each registered intake auto-generates MCP tools. On finalize, an optional signed provenance receipt is issued.",
    features=[
      "Field-level attribution — tracks who filled each field (agent / human / system) and when",
      "Secure handoff: rotating resume tokens, pre-filled forms with 'filled by agent' badges",
      "Submission state machine with validation → optional approval gates → webhook delivery",
      "Auto-generated MCP tools per intake: {intake}__create / set / validate / submit (+ upload)",
      "React form-renderer: JSON Schema → typed field components; resume + multi-step wizard flows",
      "Schema normalizer: Zod / JSON Schema / OpenAPI → one unified IntakeSchema IR",
      "Ready-made templates: vendor onboarding, IT access, customer intake, expense, bug report",
      "HMAC-signed webhook delivery with signing/verification/retry",
      "JWT-VC signed provenance receipts (EdDSA) at finalize — PII attested by hash, not embedded",
      "/.well-known/jwks.json + receipt verify endpoints",
      "Admin dashboard SPA (intakes, submissions, approvals, analytics, webhooks)",
      "~1,427 tests across the monorepo",
    ],
    interfaces=[
      "HTTP API: POST/GET/PATCH /intake/:id/submissions, /submissions/:id/handoff, /resume/:token, /receipts/verify",
      "Per-intake MCP tools (auto-generated), Stdio + SSE transports",
      "React library: @agentkitai/formbridge-form-renderer (FormBridgeForm, ResumeFormPage, WizardForm)",
      "Scaffolding CLI: npx @agentkitai/formbridge-create",
      "Templates + schema-normalizer packages",
      "/.well-known/jwks.json for receipt verification",
    ],
    fits="The human-input arm of the control plane — invoked when an agent hits a field only a person can fill. Its signed provenance receipts mirror the suite's tamper-evident, compliance-first posture; webhook delivery routes finished submissions into downstream systems.",
    notable="The triple-write event pattern, rotating resume tokens, and field-level attribution make every submission an auditable record of exactly who supplied what. JWT-VC receipts (EdDSA, JWKS-published) attest PII by content hash rather than embedding it — provenance without leaking data.",
    stack="TypeScript 5.9 · Hono v4 + @hono/node-server · @modelcontextprotocol/sdk · React (form-renderer + admin) · jose (EdDSA receipts) · Vitest · npm workspaces (6 packages)",
    links=dict(repo="https://github.com/agentkitai/formbridge", npm="https://www.npmjs.com/package/@agentkitai/formbridge-create")),

  dict(slug="agenteval", emoji="✅", name="AgentEval", tier="core",
    tagline="Testing & evaluation for AI agents: YAML suites, pluggable graders, statistical regression detection.",
    role="Testing / evaluation", lang="Python", version="0.7.0",
    status="Active · alpha",
    purpose="Tests the non-deterministic. Enables declarative test-suite definition in YAML, grades agent outputs with 10+ pluggable graders, detects statistical regressions across runs using Welch's t-test, and integrates with AgentLens to import production sessions as test cases and emit eval runs as tamper-evident audit evidence.",
    architecture="YAML suite files define cases (inputs, expected outputs, grading criteria). A loader reads them and a runner executes each case against a sync/async agent callable with timeout + retry. Results are graded by one of 10+ pluggable graders producing GradeResult objects; complete EvalRun objects persist to a SQLite ResultStore. A Coordinator can route cases to Redis-backed workers for distributed execution (with local fallback). Emitters send finished runs to AgentLens as hash-chained federation evidence. 20+ CLI commands orchestrate everything.",
    features=[
      "YAML declarative test suites (inputs, expected outputs, grading criteria)",
      "10 built-in graders: exact, contains, regex, tool-check, llm-judge, custom, json_schema, semantic, latency, cost, trajectory",
      "Statistical regression detection via Welch's t-test; group comparison command",
      "AgentLens integration both ways: import sessions as fixtures; emit runs as tamper-evident evidence",
      "Distributed execution: Redis broker + coordinator, automatic local fallback",
      "Cost + latency tracking per case, aggregated across suites",
      "Framework adapters: LangChain, CrewAI, AutoGen",
      "OpenTelemetry trace import → eval fixtures",
      "GitHub Action for CI gating (min pass-rate, regression thresholds)",
      "Badges, trend analysis, flaky-test detection, EU AI Act compliance checks",
    ],
    interfaces=[
      "CLI: agenteval run / compare / import-agentlens / ci / baseline / worker / evidence / trends / verify / …",
      "GitHub Action: agentkitai/agenteval@v1",
      "Python SDK: EvalCase / EvalSuite / EvalRun / GradeResult, Grader protocol, runner.run_suite()",
      "SQLite persistence (eval_runs, eval_results)",
      "AgentLens HTTP: POST /api/internal/eval/run (service-token gated)",
    ],
    fits="The testing/evaluation arm — closes the loop with AgentLens bidirectionally: production sessions become regression fixtures, and eval results flow back into the tamper-evident audit trail. Complements AgentGate and AgentLens for a build → observe → evaluate cycle.",
    notable="Hash-chained, service-token-gated eval evidence emitted to AgentLens (a full test-case ↔ production-session audit trail); Welch's t-test for statistically sound regression detection rather than naive pass/fail; lazy-loaded grader registry; pure-Python fallback when scipy is unavailable.",
    stack="Python 3.9+ · Click · PyYAML · SQLite · httpx · jsonschema · sentence-transformers · scipy · redis",
    links=dict(repo="https://github.com/agentkitai/agenteval", pypi="https://pypi.org/project/agentevalkit/")),

  dict(slug="agentkit-guardrails", emoji="🚦", name="agentkit-guardrails", tier="support",
    tagline="Reactive policy automation: tightens AgentGate policies when AgentLens metrics breach thresholds.",
    role="Reactive policy loop", lang="TypeScript", version="1.0.0",
    status="Focused · 1.0",
    purpose="Provides automatic guardrails by monitoring AgentLens metrics and reactively creating AgentGate policy overrides when error rates, latency, or other metrics exceed thresholds — then removing them when metrics recover. Delivers reactive, policy-driven incident response with no manual intervention.",
    architecture="A single-process webhook receiver and policy orchestrator. AgentLens POSTs breach/recovery events to /webhook; the service looks up matching YAML rules and calls the AgentGate REST API to create or remove policy overrides. It keeps an in-memory map of active overrides with local TTL timers as a safety net, and reconciles state from AgentGate on startup to avoid orphaned overrides after restarts. Webhook requests require a shared secret; AgentGate calls use optional bearer auth.",
    features=[
      "Webhook receiver (POST /webhook) for metric breach + recovery events",
      "YAML rule config mapping metric names to enforcement actions",
      "Three actions: require_approval (human-in-loop), deny (block tools), allow (whitelist)",
      "Glob tool matching (e.g. external_api.*)",
      "Dual-TTL safety net: in-memory timers + AgentGate-side TTL",
      "Idempotent duplicate-event handling — no duplicate overrides",
      "Startup reconciliation rebuilds override state from AgentGate (source of truth)",
      "Fail-closed shared-secret webhook auth (rejects all if unset)",
      "Health endpoint (GET /health); npx executable",
    ],
    interfaces=[
      "POST /webhook (metric breach/recovery)",
      "GET /health",
      "AgentGate API: POST/DELETE/GET /api/overrides",
      "CLI: agentkit-guardrails config.yaml (npx)",
      "YAML config (rules, port, AgentGate URL + key)",
    ],
    fits="The reactive loop that makes the suite self-tightening: it wires AgentLens (observe) to AgentGate (govern). When metrics degrade, permissions automatically tighten; when they recover, normal access is restored.",
    notable="Three hardening fixes define it: a local-TTL safety net so stale overrides don't block re-creation; startup reconciliation against AgentGate's source of truth so restarts don't orphan/duplicate; and fail-closed shared-secret webhook auth preventing unauthorized policy changes.",
    stack="TypeScript / Node.js · Fastify · Zod · YAML · Pino · Vitest",
    links=dict(repo="https://github.com/agentkitai/agentkit-guardrails", npm="https://www.npmjs.com/package/agentkit-guardrails")),

  dict(slug="agentkit-cli", emoji="🔧", name="agentkit-cli", tier="support",
    tagline="Unified CLI to orchestrate the suite, with Ed25519 agent identity and audit-verified governance.",
    role="Orchestrator + identity", lang="TypeScript", version="0.1.1",
    status="Active",
    purpose="A single command-line interface to initialize, deploy, monitor, and manage the suite of agent microservices running in Docker — plus agent identity management, audit hash-chain verification, compliance evidence export, and governance profiles that enforce secure, auditable operations across the stack.",
    architecture="Three layers: (1) a Commander-based command layer (init/status/up/down/logs/doctor/identity/audit/evidence/demo/mcp/serve) that reads config and orchestrates Docker or service APIs; (2) an MCP layer with a stdio server exposing CLI verbs as tools and an HTTP server bound to a specific agent identity for stack-scoped queries; (3) a support layer with config auto-discovery (walks up 10 dirs for agentkit.config.yaml), a service registry with health checks, project generators, and identity storage. Identity ops are appended to an audit.log for tamper-evidence.",
    features=[
      "init — interactive/non-interactive scaffolding; default or governed-agent (compliance-first) template",
      "up / down / logs — thin Docker Compose wrappers, governance-profile default, fresh secret generation",
      "status — service health monitoring with --watch live mode",
      "doctor — diagnostics (config, Docker daemon, container health, connectivity)",
      "identity mint/inspect/rotate — Ed25519 agent identity lifecycle in ~/.agentkit",
      "audit verify — independent client-side hash-chain re-walk of a running stack",
      "evidence export — signed compliance evidence pack",
      "demo — first-run seed data + guided tour",
      "mcp (stdio) — CLI verbs as MCP tools",
      "serve (HTTP) — identity-scoped MCP server; every result stamped with servedBy {id, fingerprint}",
    ],
    interfaces=[
      "CLI: agentkit init|status|up|down|logs|doctor|identity|audit|evidence|demo|mcp|serve",
      "MCP (stdio): status, doctor, audit_verify, identity_mint/inspect/rotate, init",
      "MCP (HTTP /mcp): identity_whoami, status, audit_verify, evidence_export",
      "Config: agentkit.config.yaml (projectName, language, template, services.*)",
      "Identity store: ~/.agentkit/identities/*.json + *.key (0600) + audit.log (JSONL)",
      "Published: npm @agentkitai/agentkit-cli",
    ],
    fits="The central orchestrator — manages the lifecycle of all five core services and mints the Ed25519 identities used across them. Exposes stack operations to LLM agents via MCP so an agent can operate the control plane itself; governance-by-default cascades audit verification and evidence export through the whole stack.",
    notable="Identity-scoped security: every MCP result is stamped with servedBy {id, fingerprint}. Ed25519 keys stored 0600 outside repos, never printed. audit verify does an independent client-side cross-check of prevHash linkage — integrity beyond the server's own verdict. up/down/logs are deliberately thin Compose wrappers (no re-implementation).",
    stack="TypeScript (CommonJS) · Commander.js · Zod · YAML · @modelcontextprotocol/sdk · Node crypto (ed25519) · Docker Compose",
    links=dict(repo="https://github.com/agentkitai/agentkit-cli", npm="https://www.npmjs.com/package/@agentkitai/agentkit-cli")),

  dict(slug="agentkit-stack", emoji="📦", name="agentkit-stack", tier="support",
    tagline="One docker compose up for the governance trio — AgentLens + AgentGate + Lore.",
    role="Deployment / orchestration", lang="Docker Compose", version="—",
    status="Active · infra",
    purpose="Solves the operational complexity of deploying the control-plane suite. Provides zero-setup deployment via Docker Compose with environment-based config, cloud dev-container support, and composable service profiles, so users can run observability, governance, and semantic memory together with automated health checking and inter-service networking.",
    architecture="A single docker-compose.yml defines four containers on a shared bridge network: AgentLens (Node, 3000), AgentGate (Node, 3002), Lore (Python, 8765), and a pgvector Postgres database (5432). Compose profiles select which services start; .env supplies secrets and URLs; health-check endpoints gate dependent service startup so there are no race conditions.",
    features=[
      "Composable profiles: minimal (observe + memory), governance (+ approval gateway), full",
      "Zero local setup: single docker compose up -d",
      "GitHub Codespaces one-click launch with embedded dev container",
      "Environment-driven secrets (.env, gitignored)",
      "Health-gated startup (e.g. AgentLens waits for Lore)",
      "Pre-configured inter-service networking + DNS",
      "Build from local source or pull from GHCR",
      "CI smoke test validates the governance stack boots healthy",
      "Volume persistence for AgentLens / AgentGate / Lore",
    ],
    interfaces=[
      "docker compose up/down/logs --profile {minimal|governance|full}",
      "Health: :3000/api/stats (Lens), :3002/health (Gate), :8765/health (Lore)",
      ".env configuration",
      "GitHub Codespaces / Dev Containers",
      "Images: ghcr.io/agentkitai/{agentlens,agentgate,lore}",
    ],
    fits="The operational center: run it once, then point the agents in your systems at its endpoints for observability, memory, and governance. Pairs with agentkit-cli (which wraps these same Compose operations behind governance verbs).",
    notable="Composable profiles decouple governance from minimal deployments without config changes; health checks prevent startup races; secrets live in .env (out of git) with safe local-dev defaults; a CI smoke test proves the full governance profile boots healthy within 240s.",
    stack="Docker Compose · pgvector/pgvector:pg16 · shell · GitHub Actions · VS Code Dev Containers",
    links=dict(repo="https://github.com/agentkitai/agentkit-stack")),
]

BY_SLUG = {p["slug"]: p for p in PRODUCTS}
TIER_LABEL = {"core": "Core", "support": "Tooling"}

# ---- shared html bits ---------------------------------------------------
def esc(s): return html.escape(str(s))

def nav(active):
    items = ['<a href="index.html"%s>Overview</a>' % (' class="active"' if active=="index" else "")]
    for p in PRODUCTS:
        cls = ' class="active"' if active==p["slug"] else ""
        items.append('<a href="%s.html"%s>%s %s</a>' % (p["slug"], cls, p["emoji"], esc(p["name"])))
    return '<nav class="topnav">%s</nav>' % "".join(items)

def page(title, active, body):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><link rel="stylesheet" href="styles.css">
</head><body>
<header class="masthead"><a class="brand" href="index.html">⬡ <b>AgentKitAI</b></a>
<span class="brand-sub">open-source control plane for AI agents</span></header>
{nav(active)}
<main>{body}</main>
<footer>AgentKitAI · {esc(len(PRODUCTS))} products · MIT/ISC licensed · github.com/agentkitai</footer>
</body></html>"""

def badge(text, kind=""):
    return f'<span class="badge {kind}">{esc(text)}</span>'

def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"

# ---- the architecture diagram (inline SVG) ------------------------------
DIAGRAM_SVG = """
<svg class="diagram" viewBox="0 0 900 560" role="img" aria-label="How AgentKitAI fits together">
  <defs>
    <marker id="arr" markerWidth="9" markerHeight="9" refX="6.5" refY="3" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L7,3 L0,6 Z" class="dg-ah"/></marker>
    <marker id="arr2" markerWidth="9" markerHeight="9" refX="6.5" refY="3" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L7,3 L0,6 Z" class="dg-ah2"/></marker>
  </defs>

  <!-- agent source bar -->
  <rect class="dg-agent" x="24" y="22" width="856" height="58" rx="12"/>
  <text class="dg-t" x="452" y="47" text-anchor="middle">Your Agent</text>
  <text class="dg-s" x="452" y="67" text-anchor="middle">any framework · OpenTelemetry · SDK · MCP</text>

  <!-- agent → 4 services -->
  <line class="dg-flow" x1="122" y1="80" x2="122" y2="137" marker-end="url(#arr)"/>
  <line class="dg-flow" x1="342" y1="80" x2="342" y2="137" marker-end="url(#arr)"/>
  <line class="dg-flow" x1="562" y1="80" x2="562" y2="137" marker-end="url(#arr)"/>
  <line class="dg-flow" x1="782" y1="80" x2="782" y2="137" marker-end="url(#arr)"/>
  <g><rect class="dg-chip" x="60" y="98" width="124" height="22" rx="11"/><text class="dg-chip-t" x="122" y="113" text-anchor="middle">telemetry</text></g>
  <g><rect class="dg-chip" x="280" y="98" width="124" height="22" rx="11"/><text class="dg-chip-t" x="342" y="113" text-anchor="middle">"may I run X?"</text></g>
  <g><rect class="dg-chip" x="500" y="98" width="124" height="22" rx="11"/><text class="dg-chip-t" x="562" y="113" text-anchor="middle">remember / recall</text></g>
  <g><rect class="dg-chip" x="720" y="98" width="124" height="22" rx="11"/><text class="dg-chip-t" x="782" y="113" text-anchor="middle">human input</text></g>

  <!-- service cards -->
  <g><rect class="dg-box dg-core" x="24" y="138" width="196" height="112" rx="11"/>
    <text class="dg-name" x="122" y="178" text-anchor="middle">🔍 AgentLens</text>
    <text class="dg-s" x="122" y="202" text-anchor="middle">observe · hash-chained audit</text>
    <text class="dg-s" x="122" y="220" text-anchor="middle">cost · session replay</text></g>
  <g><rect class="dg-box dg-core" x="244" y="138" width="196" height="112" rx="11"/>
    <text class="dg-name" x="342" y="178" text-anchor="middle">🛂 AgentGate</text>
    <text class="dg-s" x="342" y="202" text-anchor="middle">approve / deny /</text>
    <text class="dg-s" x="342" y="220" text-anchor="middle">route to human</text></g>
  <g><rect class="dg-box dg-core" x="464" y="138" width="196" height="112" rx="11"/>
    <text class="dg-name" x="562" y="178" text-anchor="middle">🧠 Lore</text>
    <text class="dg-s" x="562" y="202" text-anchor="middle">memory · knowledge graph</text>
    <text class="dg-s" x="562" y="220" text-anchor="middle">bi-temporal facts</text></g>
  <g><rect class="dg-box dg-core" x="684" y="138" width="196" height="112" rx="11"/>
    <text class="dg-name" x="782" y="178" text-anchor="middle">📝 FormBridge</text>
    <text class="dg-s" x="782" y="202" text-anchor="middle">agent fills known fields,</text>
    <text class="dg-s" x="782" y="220" text-anchor="middle">human completes the rest</text></g>

  <!-- reactive loop: Lens → guardrails → Gate -->
  <path class="dg-flow2" d="M122,250 C122,284 165,302 200,304" marker-end="url(#arr2)"/>
  <path class="dg-flow2" d="M300,304 C326,302 342,288 342,254" marker-end="url(#arr2)"/>
  <rect class="dg-box dg-loop" x="150" y="300" width="200" height="48" rx="10"/>
  <text class="dg-name sm" x="250" y="320" text-anchor="middle">🚦 guardrails</text>
  <text class="dg-s" x="250" y="338" text-anchor="middle">Lens metrics → tighten Gate policy</text>

  <!-- AgentEval ↔ AgentLens (bidirectional) -->
  <line class="dg-flow" x1="42" y1="252" x2="42" y2="398" marker-start="url(#arr)" marker-end="url(#arr)"/>
  <text class="dg-dir" x="64" y="292">↓ sessions</text>
  <text class="dg-dir" x="64" y="372">↑ evidence</text>
  <rect class="dg-box" x="24" y="398" width="416" height="66" rx="10"/>
  <text class="dg-name" x="232" y="424" text-anchor="middle">✅ AgentEval</text>
  <text class="dg-s" x="232" y="444" text-anchor="middle">replays AgentLens sessions as regression tests</text>
  <text class="dg-s" x="232" y="460" text-anchor="middle">emits results back as tamper-evident audit evidence</text>

  <!-- shared-base layer -->
  <rect class="dg-box dg-base" x="458" y="398" width="422" height="66" rx="10"/>
  <text class="dg-name sm" x="669" y="421" text-anchor="middle">🧩 Shared base</text>
  <text class="dg-s" x="669" y="441" text-anchor="middle">@agentkitai/auth · @agentkitai/pricing</text>
  <text class="dg-s" x="669" y="457" text-anchor="middle">shared libraries used across the services</text>

  <!-- operate band -->
  <rect class="dg-foot" x="24" y="500" width="856" height="40" rx="9"/>
  <text class="dg-foot-t" x="452" y="525" text-anchor="middle">🔧 agentkit-cli · 📦 agentkit-stack — deploy · run · verify · mint identities for the whole stack</text>
</svg>
"""

# ---- index --------------------------------------------------------------
def card(p):
    return f"""<a class="card tier-{p['tier']}" href="{p['slug']}.html">
  <div class="card-top"><span class="emoji">{p['emoji']}</span>
    <span class="card-name">{esc(p['name'])}</span></div>
  <div class="card-tag">{esc(p['tagline'])}</div>
  <div class="card-meta">{badge(p['role'])}{badge(p['lang'],'lang')}{badge('v'+p['version'] if p['version']!='—' else 'infra','ver')}</div>
</a>"""

def index_body():
    cores = "".join(card(p) for p in PRODUCTS if p["tier"]=="core")
    supp = "".join(card(p) for p in PRODUCTS if p["tier"]=="support")
    return f"""
<section class="hero">
  <h1>The control plane for AI agents</h1>
  <p class="lede">Frameworks help you <em>build</em> an agent. <b>AgentKitAI</b> is the layer around it in production —
  <b>observe</b> what it did, <b>govern</b> what it's allowed to do, <b>remember</b> across sessions,
  <b>collect human input</b> when it's stuck, and <b>evaluate</b> that it still works. The through-line across every
  product is <b>provenance &amp; compliance</b>: tamper-evident audit, signed evidence, and EU&nbsp;AI&nbsp;Act / OWASP-LLM framing —
  so an agent's behavior isn't just logged, it's cryptographically <em>defensible</em>.</p>
  <p class="lede">Everything is MIT/ISC-licensed, self-hostable, and <b>MCP-native</b> — each service is also a Model Context
  Protocol server, so Claude Desktop / Cursor / any MCP client can drive it. Distribution is unified under the
  <code>@agentkitai/*</code> npm scope (PyPI for the Python services, <code>ghcr.io/agentkitai/*</code> for Docker,
  <code>io.github.agentkitai/*</code> in the MCP Registry).</p>
</section>

<section><h2>How the pieces fit</h2>{DIAGRAM_SVG}</section>

<section><h2>Core products</h2><div class="grid">{cores}</div></section>
<section><h2>Supporting tooling</h2><div class="grid">{supp}</div></section>

<section><h2>What ties it together</h2>
  <ol class="ties">
    <li><b>Provenance is the product.</b> Hash-chained audit (Lens), OWASP-tagged decisions (Gate), signed evidence packs (CLI), JWT-VC receipts (FormBridge), tamper-evident eval evidence (Eval) — defensible records, not just logs.</li>
    <li><b>Real integrations.</b> Eval↔Lens (sessions→tests, results→audit), Guardrails (Lens metrics→Gate policy), shared <code>@agentkitai/auth</code> + <code>@agentkitai/pricing</code> libraries, CLI-minted identities used across services.</li>
    <li><b>MCP-native throughout.</b> Every core service is also an MCP server (~22 Lens + 40 Lore + 10 Gate + per-intake FormBridge tools) — an LLM agent can operate the control plane itself.</li>
    <li><b>Tokenless, reproducible distribution.</b> Unified <code>@agentkitai/*</code> scope, 20 OIDC Trusted Publishers, MCP Registry entries current — supply-chain hygiene matching the compliance story.</li>
  </ol>
</section>

<section class="oneliner"><b>In one line:</b> AgentKitAI is the governance, observability, memory, and evaluation plane you wrap around any agent so it's auditable, controllable, stateful, and testable — independent MIT-licensed services that each stand alone but compose into one self-hostable control plane.</section>
"""

# ---- product page -------------------------------------------------------
def links_row(p):
    out=[]; L=p["links"]
    if L.get("repo"): out.append(f'<a class="lnk" href="{L["repo"]}">GitHub ↗</a>')
    if L.get("npm"):  out.append(f'<a class="lnk" href="{L["npm"]}">npm ↗</a>')
    if L.get("pypi"): out.append(f'<a class="lnk" href="{L["pypi"]}">PyPI ↗</a>')
    return '<div class="links">'+"".join(out)+'</div>'

def prevnext(p):
    idx=[q["slug"] for q in PRODUCTS].index(p["slug"]); out=[]
    if idx>0:
        q=PRODUCTS[idx-1]; out.append(f'<a href="{q["slug"]}.html">← {q["emoji"]} {esc(q["name"])}</a>')
    else: out.append('<span></span>')
    if idx<len(PRODUCTS)-1:
        q=PRODUCTS[idx+1]; out.append(f'<a href="{q["slug"]}.html">{q["emoji"]} {esc(q["name"])} →</a>')
    else: out.append('<span></span>')
    return "".join(out)

def product_body(p):
    return f"""
<a class="back" href="index.html">← All products</a>
<header class="phead tier-{p['tier']}">
  <h1><span class="emoji-lg">{p['emoji']}</span> {esc(p['name'])}</h1>
  <p class="tag">{esc(p['tagline'])}</p>
  <div class="card-meta">{badge(TIER_LABEL[p['tier']])}{badge(p['role'])}{badge(p['lang'],'lang')}{badge('v'+p['version'] if p['version']!='—' else 'infra','ver')}{badge(p['status'],'status')}</div>
  {links_row(p)}
</header>
<section><h2>Purpose</h2><p>{esc(p['purpose'])}</p></section>
<section><h2>Architecture</h2><p>{esc(p['architecture'])}</p></section>
<section><h2>Key features</h2>{ul(p['features'],'features')}</section>
<section><h2>Interfaces</h2>{ul(p['interfaces'],'ifaces')}</section>
<section><h2>How it fits the suite</h2><p>{esc(p['fits'])}</p></section>
<section><h2>Notable engineering</h2><p>{esc(p['notable'])}</p></section>
<section><h2>Stack</h2><p class="stack">{esc(p['stack'])}</p></section>
<nav class="prevnext">{prevnext(p)}</nav>
"""

# ---- css ----------------------------------------------------------------
CSS = """
:root{--bg:#0d1117;--panel:#161b22;--panel2:#1c2430;--ink:#e6edf3;--mut:#9aa7b4;--line:#2a3340;
--acc:#6e7bff;--acc2:#3fb6a8;--core:#6e7bff;--support:#3fb6a8;--code:#1a2230;}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
code{background:var(--code);padding:.1em .4em;border-radius:5px;font-size:.88em;
font-family:"SF Mono",SFMono-Regular,Consolas,"Liberation Mono",Menlo,monospace;color:#b8c4ff}
.masthead{display:flex;align-items:baseline;gap:.75rem;padding:1rem 1.5rem .9rem;border-bottom:1px solid var(--line);
background:linear-gradient(180deg,#11161d,#0d1117)}
.brand{font-size:1.15rem;color:var(--ink)}.brand b{color:#fff}.brand-sub{color:var(--mut);font-size:.85rem}
.topnav{display:flex;flex-wrap:wrap;gap:.15rem;padding:.5rem 1rem;border-bottom:1px solid var(--line);
background:var(--panel);position:sticky;top:0;z-index:5;overflow-x:auto}
.topnav a{color:var(--mut);padding:.3rem .6rem;border-radius:7px;font-size:.85rem;white-space:nowrap}
.topnav a:hover{background:var(--panel2);color:var(--ink);text-decoration:none}
.topnav a.active{background:var(--acc);color:#fff}
main{max-width:980px;margin:0 auto;padding:2rem 1.25rem 3rem}
h1{font-size:2rem;margin:.2em 0 .3em;line-height:1.15}
h2{font-size:1.15rem;margin:2rem 0 .6rem;padding-bottom:.35rem;border-bottom:1px solid var(--line);color:#fff}
section{margin-bottom:.4rem}
.hero h1{font-size:2.4rem;background:linear-gradient(90deg,#fff,#9aa7ff);-webkit-background-clip:text;background-clip:text;color:transparent}
.lede{color:#c9d4df;font-size:1.05rem;max-width:75ch}
/* svg diagram */
svg.diagram{width:100%;height:auto;display:block;background:linear-gradient(180deg,#121826,#0f1420);
border:1px solid var(--line);border-radius:12px;padding:8px;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.dg-agent{fill:#1a2138;stroke:var(--acc);stroke-width:1.6}
.dg-box{fill:var(--panel);stroke:var(--line);stroke-width:1.2}
.dg-core{stroke:#454f8c}
.dg-loop{fill:#15211f;stroke:#2c5b54}
.dg-foot{fill:#141b27;stroke:var(--line)}
.dg-t{fill:#fff;font-size:16px;font-weight:600}
.dg-name{fill:#fff;font-size:15px;font-weight:600}.dg-name.sm{font-size:13px}
.dg-s{fill:#9aa7b4;font-size:12px}
.dg-foot-t{fill:#c4d0dc;font-size:12.5px}
.dg-chip{fill:var(--panel2);stroke:var(--line)}
.dg-chip-t{fill:#c9d4df;font-size:11px}
.dg-flow{stroke:var(--acc);stroke-width:1.7;fill:none}
.dg-flow2{stroke:var(--acc2);stroke-width:1.7;fill:none}
.dg-ah{fill:var(--acc)}.dg-ah2{fill:var(--acc2)}
.dg-dir{fill:#8fb9ff;font-size:11.5px;font-weight:500}
.dg-base{fill:#141d22;stroke:#3a6e66;stroke-dasharray:5 4}
/* cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--core);
border-radius:11px;padding:1rem 1.1rem;transition:.12s;color:var(--ink)}
.card:hover{background:var(--panel2);transform:translateY(-2px);text-decoration:none;border-color:var(--acc)}
.card.tier-support{border-left-color:var(--support)}
.card-top{display:flex;align-items:center;gap:.5rem;margin-bottom:.35rem}
.emoji{font-size:1.3rem}.card-name{font-weight:700;font-size:1.05rem;color:#fff}
.card-tag{color:var(--mut);font-size:.9rem;margin-bottom:.6rem}
.card-meta{display:flex;flex-wrap:wrap;gap:.35rem}
.badge{display:inline-block;background:var(--panel2);border:1px solid var(--line);color:var(--mut);
font-size:.72rem;padding:.12rem .5rem;border-radius:20px;white-space:nowrap}
.badge.lang{color:#a7b6ff;border-color:#39427a}.badge.ver{color:#7fe0d4;border-color:#2c5b54}
.badge.status{color:#ffce8a;border-color:#5e4a26}
.ties li{margin:.5rem 0}.ties{max-width:80ch}
.oneliner{background:linear-gradient(90deg,#161d2e,#13201d);border:1px solid var(--line);border-radius:11px;
padding:1.1rem 1.25rem;margin-top:1.5rem;font-size:1.05rem}
.back{display:inline-block;color:var(--mut);font-size:.9rem;margin-bottom:.5rem}
.phead{border-left:3px solid var(--core);padding:.2rem 0 1rem 1rem;margin-bottom:.5rem}
.phead.tier-support{border-left-color:var(--support)}
.emoji-lg{font-size:2rem}.tag{color:var(--mut);font-size:1.08rem;margin:.1rem 0 .8rem;max-width:75ch}
.links{display:flex;gap:.5rem;margin-top:.7rem}
.lnk{background:var(--panel2);border:1px solid var(--line);padding:.3rem .7rem;border-radius:8px;font-size:.85rem}
.lnk:hover{border-color:var(--acc);text-decoration:none}
ul.features,ul.ifaces{margin:.3rem 0;padding-left:0;list-style:none}
ul.features li,ul.ifaces li{position:relative;padding:.28rem 0 .28rem 1.4rem;border-bottom:1px solid #1d2530}
ul.features li:before{content:"▸";position:absolute;left:.2rem;color:var(--acc)}
ul.ifaces li{font-family:"SF Mono",Consolas,Menlo,monospace;font-size:.86rem;color:#c4d0dc}
ul.ifaces li:before{content:"›";position:absolute;left:.3rem;color:var(--acc2)}
.stack{color:#c4d0dc}
.prevnext{display:flex;justify-content:space-between;margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line)}
.prevnext a{background:var(--panel);border:1px solid var(--line);padding:.5rem .9rem;border-radius:9px;font-size:.9rem}
.prevnext a:hover{border-color:var(--acc);text-decoration:none}
footer{max-width:980px;margin:0 auto;padding:1.5rem 1.25rem 3rem;color:var(--mut);font-size:.85rem;
border-top:1px solid var(--line);text-align:center}
@media(max-width:600px){.hero h1{font-size:1.8rem}main{padding:1.25rem 1rem 2rem}}
"""

# ---- write --------------------------------------------------------------
(OUT/"styles.css").write_text(CSS, encoding="utf-8")
(OUT/"index.html").write_text(page("AgentKitAI — Suite Overview","index",index_body()), encoding="utf-8")
for p in PRODUCTS:
    (OUT/f"{p['slug']}.html").write_text(page(f"{p['name']} — AgentKitAI", p["slug"], product_body(p)), encoding="utf-8")

# remove the now-deleted mesh page if it lingers from a prior run
stale = OUT/"agentkit-mesh.html"
if stale.exists(): stale.unlink()

print("wrote", len(PRODUCTS)+2, "files;", "removed stale mesh page" if not stale.exists() else "")
import os
for f in sorted(OUT.iterdir()): print("  ", f.name)
