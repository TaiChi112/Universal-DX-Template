# Universal DX Template

Production-ready monorepo for a multi-backend architecture with Python FastAPI, Rust Actix-Web, and PostgreSQL.

## Why This Project Exists

Modern teams often struggle when they need both rapid product iteration and high-performance data processing in the same system.

Common real-world pain points:
1. A single backend stack becomes a bottleneck because all workloads are forced into one runtime.
2. Teams cannot experiment quickly because architecture changes are expensive and risky.
3. Service boundaries are unclear, so ownership and scaling decisions become difficult.
4. Local development differs from production behavior, causing integration surprises late in delivery.

This project was created as a practical reference implementation to solve those issues with a clear, reproducible foundation.

## Problem Statement

The target use case is document ingestion and processing, where an API must:
1. Receive files from clients reliably.
2. Extract or enrich document data with application-level logic.
3. Persist structured results efficiently.

In many teams, these concerns are mixed into one service, creating tight coupling between HTTP handling, business logic, and persistence. That coupling slows down releases and makes independent scaling difficult.

Universal DX Template demonstrates how to split those concerns into focused services while preserving a smooth developer experience.

## Design Goals

1. Fast iteration for API-facing features in Python FastAPI.
2. High-throughput persistence path in Rust Actix-Web.
3. Explicit service contracts and clear network boundaries.
4. Repeatable local setup using Docker Compose and VS Code tasks.
5. Clean Architecture principles in the Python service to keep domain logic testable.
6. Production-minded defaults such as health checks, dependency injection, and CI-friendly structure.

## Intended Audience

This template is for:
1. Teams exploring polyglot backends (Python + Rust) in one monorepo.
2. Engineers who want a clean baseline for document-centric backend systems.
3. Technical leads who need a teaching/reference project for architecture discussions.

## Current Scope and Non-Goals

Current scope:
1. End-to-end service flow from upload request to database write.
2. Separation of API orchestration (Python) and data persistence engine (Rust).
3. Foundational testing and development workflow.

Intentional non-goals in this template stage:
1. Full OCR/AI production pipeline (OCR adapter is scaffolded and currently mocked).
2. Complete authn/authz and tenant isolation.
3. Full observability stack (distributed tracing, metrics dashboards, alerting).
4. Advanced deployment manifests for Kubernetes or cloud-specific infrastructure.

## What Success Looks Like

If this template is used correctly, you should be able to:
1. Start all services locally in minutes.
2. Make changes in one service without breaking ownership boundaries.
3. Extend endpoints and data models predictably with minimal cross-service friction.
4. Use this repository as a base for a production project, not only a demo.

## 1. System Architecture

The repository is organized into independent services with clear responsibilities and explicit network boundaries.

| Component        | Stack                          | Repository Path               | Exposed Port | Role                                                |
| :--------------- | :----------------------------- | :---------------------------- | :----------: | :-------------------------------------------------- |
| Core API         | Python 3.11+, FastAPI, Uvicorn | `services/core-api-python`    |    `8000`    | Public API layer, document processing orchestration |
| Data Engine      | Rust, Actix-Web, SQLx          | `services/data-engine-rust`   |    `8080`    | High-performance ingestion and persistence handler  |
| Persistence      | PostgreSQL 15 (Alpine)         | Docker service: `postgres-db` |    `5432`    | Primary relational data store                       |
| Shared Contracts | JSON Schema                    | `lib/api-contracts`           |      -       | Shared schema definitions                           |

Runtime topology from `docker-compose.yml`:
- `core-api-python` calls `data-engine-rust` via `RUST_SERVICE_URL=http://data-engine-rust:8080`
- `data-engine-rust` connects to PostgreSQL via `DATABASE_URL=postgres://admin:secretpassword@postgres-db:5432/universal_dx`
- Persistent PostgreSQL storage is backed by volume `pgdata`

## 2. Prerequisites

Required tools for local development:
1. Docker Desktop (running)
2. Visual Studio Code
3. VS Code extension: Dev Containers (`ms-vscode-remote.remote-containers`)

Recommended for non-container local execution:
1. Python 3.11+
2. Rust toolchain (`cargo`)

## 3. Local Development Setup

This section follows the current `docker-compose.yml` and `.vscode/tasks.json` exactly.

### A. Open In Dev Container (recommended)
1. Open the repository in VS Code.
2. Run Command Palette: `Dev Containers: Reopen in Container`.
3. Wait for container initialization to complete.

### B. Start the full environment with VS Code Tasks
1. Open Command Palette: `Tasks: Run Task`.
2. Run task: `[RUN] Start Full Environment`.

Current task chain:
1. `Start Database (PostgreSQL)`
2. `Start Backend APIs` (parallel)
3. `Run FastAPI (Python)` and `Run Actix (Rust)`

### C. Equivalent manual commands
From repository root:

```bash
docker compose up -d postgres-db
```

From `services/core-api-python`:

```bash
python -m uvicorn src.main:app --reload --port 8000
```

From `services/data-engine-rust`:

```bash
cargo run
```

### D. Verify service health
Core API:

```bash
curl http://127.0.0.1:8000/health
```

Expected: JSON payload containing `status: healthy`.

## 4. Development Workflow

### Hot-reload workflow
Use VS Code task execution to run both APIs during development:
1. Run task: `Start Backend APIs`
2. FastAPI runs with `--reload`
3. Rust service runs via `cargo run`

### Multi-target debugging
The workspace includes launch configurations in `.vscode/launch.json`:
1. Open **Run and Debug** in VS Code.
2. Select `Debug All Services (Multi-Target)`.
3. Press `F5`.

This starts:
1. `Debug FastAPI (Python)` using `uvicorn src.main:app --reload --port 8000`
2. `Debug Actix (Rust)` using Cargo build target `data-engine-rust`

## 5. Testing & Code Quality

### CI/CD pipeline
GitHub Actions workflow: `.github/workflows/ci.yml` runs on all pushes and pull requests to `main`. It validates code formatting, linting, and test suites for both Python and Rust services.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed command references.

### Husky hooks
Git hooks enforce code quality automatically. Configured hooks are in `.husky/`:
1. `pre-commit.sh` - Runs formatters (`black`, `cargo fmt`) and linters (`flake8`, `clippy`)
2. `commit-msg.sh` - Enforces Conventional Commits standard
3. `pre-push.sh` - Runs test suites (`pytest`, `cargo test`)

No manual intervention needed; hooks run automatically on `git commit` and `git push`.

### Run tests locally
Refer to [CONTRIBUTING.md](CONTRIBUTING.md#testing-and-code-quality) for testing commands.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development standards and code style
- Git workflow and commit message conventions
- Instructions for scaling the project
- Adding new services or endpoints
- Troubleshooting common issues

## Notes

- If `Start Database (PostgreSQL)` fails with Docker CLI not found, ensure Docker Desktop is running and restart VS Code so task shells pick up the Docker PATH.
- Ports used by default: `8000` (FastAPI), `8080` (Actix), `5432` (PostgreSQL).