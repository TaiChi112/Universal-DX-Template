# Universal DX Template

Production-ready monorepo for a multi-backend architecture with Python FastAPI, Rust Actix-Web, and PostgreSQL.

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
GitHub Actions workflow: `.github/workflows/ci.yml`

It runs on pushes and pull requests to `main` with two jobs:
1. `python-checks`
2. `rust-checks`

Python CI checks:
1. `black --check .`
2. `flake8 .`
3. `pytest -v`

Rust CI checks:
1. `cargo fmt -- --check`
2. `cargo clippy -- -D warnings`
3. `sqlx migrate run`
4. `cargo test`

### Husky hooks
Configured hooks are in `.husky/`:
1. `pre-commit.sh` (active)
2. `pre-push.sh` (currently empty)
3. `commit-msg.sh` (currently empty)

Current active pre-commit checks:
1. Python: `python -m black --check .`, `python -m flake8 .`
2. Rust: `cargo fmt -- --check`, `cargo clippy -- -D warnings`

### Run tests locally
From `services/core-api-python`:

```bash
pytest -v
```

From `services/data-engine-rust`:

```bash
cargo test
```

## Notes

- If `Start Database (PostgreSQL)` fails with Docker CLI not found, ensure Docker Desktop is running and restart VS Code so task shells pick up the Docker PATH.
- Ports used by default: `8000` (FastAPI), `8080` (Actix), `5432` (PostgreSQL).