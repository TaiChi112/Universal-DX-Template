# Contributing to Universal DX Template

Thank you for contributing to this production-ready monorepo. This guide covers development workflows, code standards, and instructions for scaling the project by adding new services or features.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Standards](#development-standards)
3. [Git Workflow](#git-workflow)
4. [Scaling the Project](#scaling-the-project)
5. [Adding New Services](#adding-new-services)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites
1. Docker Desktop (running)
2. Visual Studio Code
3. VS Code extension: Dev Containers (`ms-vscode-remote.remote-containers`)
4. Node.js (for Husky pre-commit hooks)

### Local Setup
1. Clone the repository
2. Open in VS Code and run Command Palette: `Dev Containers: Reopen in Container`
3. Wait for container initialization

### Start developing
```bash
# Run the full environment
Tasks: Run Task → [RUN] Start Full Environment

# Or manually start services:
docker compose up -d postgres-db
cd services/core-api-python && python -m uvicorn src.main:app --reload --port 8000
cd services/data-engine-rust && cargo run
```

---

## Development Standards

### Code Style & Formatting

**Python (FastAPI):**
- Formatter: `black`
- Linter: `flake8`
- Auto-format before commit: `black services/core-api-python/`
- Check formatting: `black --check services/core-api-python/`

**Rust (Actix-Web):**
- Formatter: `cargo fmt`
- Linter: `cargo clippy`
- Auto-format before commit: `cargo fmt` (in `services/data-engine-rust/`)
- Check formatting: `cargo fmt -- --check`

### Testing

**Python Tests:**
```bash
cd services/core-api-python
pytest -v
```

**Rust Tests:**
```bash
cd services/data-engine-rust
cargo test
```

### Git Hooks (Husky)

Commit hooks are automatically enforced:

| Hook            | Purpose              | What it checks                                                                |
| :-------------- | :------------------- | :---------------------------------------------------------------------------- |
| `pre-commit.sh` | Format & lint check  | Python: `black --check`, `flake8` / Rust: `cargo fmt --check`, `cargo clippy` |
| `commit-msg.sh` | Conventional Commits | Commit message must start with `feat:`, `fix:`, `docs:`, `refactor:`, etc.    |
| `pre-push.sh`   | Test validation      | Runs `pytest -v` and `cargo test` before pushing                              |

**Valid commit message formats:**
```
feat: add new feature
fix: resolve bug in authentication
docs: update README
refactor: improve code structure
test: add unit tests for serialization
```

---

## Git Workflow

### 1. Create a feature branch
```bash
git checkout -b feat/your-feature-name
```

### 2. Make changes and commit
```bash
# Auto-format code (recommended)
black services/core-api-python/
cargo fmt -p data-engine-rust

# Commit with conventional message
git commit -m "feat: add new endpoint for document upload"
```

If formatting fails, fix the issues and commit again.

### 3. Push and create a pull request
```bash
git push origin feat/your-feature-name
```

The following will run automatically:
1. **Pre-push hook:** Tests validate (`pytest`, `cargo test`)
2. **GitHub Actions CI:** Full pipeline runs (formatting, linting, testing)
3. **Code owners review:** Appropriate teams are notified

### 4. Code review and merge
Once approved, merge into `main` via GitHub UI.

---

## Scaling the Project

### Adding a New Python Endpoint

**File locations:**
```
services/core-api-python/
├── src/
│   ├── main.py                 # FastAPI app definition
│   ├── api/
│   │   ├── routes/
│   │   │   └── {new_router}.py # Add your new router here
│   │   └── dependencies.py      # Dependency injection
│   ├── services/
│   │   └── {new_service}.py    # Business logic
│   └── schema/
│       └── {new_schema}.py     # Pydantic models
└── tests/
    └── test_{new_feature}.py
```

**Steps:**
1. Create a new router in `src/api/routes/{feature_name}.py`
2. Define Pydantic models in `src/schema/{feature_name}.py`
3. Add business logic in `src/services/{feature_name}.py`
4. Register router in `src/main.py`: `app.include_router(router, prefix="/api/v1")`
5. Write tests in `tests/test_{feature_name}.py`
6. Run `pytest -v` to validate

**Example:**
```python
# src/api/routes/user_router.py
from fastapi import APIRouter, Depends
from src.schema.user_schema import User
from src.services.user_service import UserService
from src.api.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(user: User, service: UserService = Depends(get_user_service)):
    return await service.create(user)
```

### Adding a New Rust Endpoint

**File locations:**
```
services/data-engine-rust/
├── src/
│   ├── main.rs                  # HTTP server setup
│   ├── handlers/
│   │   └── {new_handler}.rs    # Request handlers
│   ├── models/
│   │   └── {new_dto}.rs        # Data transfer objects
│   ├── repositories/
│   │   └── {new_repo}.rs       # Database operations
│   └── infrastructure/
│       └── db.rs                # Database connection management
├── migrations/
│   └── {timestamp}_{description}.sql # SQLx migrations
└── Cargo.toml                    # Dependencies
```

**Steps:**
1. Create migration in `migrations/` if needed: `CREATE TABLE ...`
2. Create DTO model in `src/models/{feature_name}.rs`
3. Create repository in `src/repositories/{feature_name}.rs` (handles DB)
4. Create handler in `src/handlers/{feature_name}.rs` (handles HTTP)
5. Register handler in `src/main.rs`: `.route("/api/v1/{path}", web::post().to(handler))`
6. Export modules: Update `src/handlers/mod.rs`, `src/models/mod.rs`, etc.
7. Run `cargo test` to validate

**Example:**
```rust
// src/handlers/user_handler.rs
use actix_web::{web, HttpResponse, Responder};
use crate::models::user_dto::UserDto;

pub async fn create_user(user: web::Json<UserDto>) -> impl Responder {
    // Insert logic here
    HttpResponse::Created().json(user.into_inner())
}
```

### Adding a New Service (Full Stack)

**Directory structure:**
```
services/my-new-service/
├── src/
├── Cargo.toml                   # (for Rust) or pyproject.toml (for Python)
├── Dockerfile.{python|rust}
├── migrations/                  # (if database access needed)
└── tests/
```

**Steps:**
1. Create new service directory in `services/`
2. Set up service-specific dependencies (`pyproject.toml` or `Cargo.toml`)
3. Create `Dockerfile.{python|rust}` for containerization
4. Add Docker Compose service in root `docker-compose.yml`:
   ```yaml
   my-new-service:
     build:
       context: ./services/my-new-service
       dockerfile: Dockerfile.python
     ports:
       - "8001:8000"  # Adjust port
     environment:
       - DATABASE_URL=postgres://...
     depends_on:
       - postgres-db
     restart: unless-stopped
   ```
5. Update `.github/CODEOWNERS` to assign ownership
6. Update `.github/dependabot.yml` for dependency updates
7. Add CI checks in `.github/workflows/ci.yml`:
   ```yaml
   - name: Check New Service
     working-directory: ./services/my-new-service
     run: your-service-tests-here
   ```
8. Create VS Code task in `.vscode/tasks.json` to run the service
9. Update `README.md` with service documentation

### Extending the Database Schema

**For Rust (using SQLx):**
1. Create migration file: `services/data-engine-rust/migrations/{timestamp}_{description}.sql`
2. Write SQL: `CREATE TABLE ...` or `ALTER TABLE ...`
3. Update models in `src/models/` to reflect schema changes
4. Update repository queries in `src/repositories/`
5. Run tests: `cargo test`

**Example migration:**
```sql
-- migrations/20260411120000_add_user_table.sql
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## Monorepo Best Practices

1. **Service Independence:** Services should be deployable independently
2. **Explicit Dependencies:** Document inter-service communication in `README.md`
3. **Shared Contracts:** Use JSON Schemas in `lib/api-contracts/` for API contracts
4. **Configuration:** Use environment variables and `.env.example` (never commit secrets)
5. **Testing:** Write tests alongside features; aim for >70% coverage
6. **Documentation:** Update `README.md` and relevant service docs when changing behavior

---

## Troubleshooting

### Pre-commit hook fails
**Problem:** `pre-commit.sh` failed with formatting errors
**Solution:**
```bash
# Auto-format Python
black services/core-api-python/

# Auto-format Rust
cargo fmt -p data-engine-rust

# Retry commit
git commit -m "your message"
```

### Pre-push hook fails (tests failing)
**Problem:** `pre-push.sh` failed; tests are failing
**Solution:**
1. Run local tests to reproduce:
   ```bash
   cd services/core-api-python && pytest -v
   cd services/data-engine-rust && cargo test
   ```
2. Fix failing tests
3. Commit and push again

### Commit message doesn't follow Conventional Commits
**Problem:** `commit-msg.sh` rejected your message
**Solution:**
```bash
# Use git commit --amend to fix the message
git commit --amend -m "feat: correct message format"
```

### Docker container issues
**Problem:** Container fails to start
**Solution:**
```bash
# Rebuild the Dev Container
Dev Containers: Rebuild Container

# Or restart Docker Compose
docker compose down
docker compose up -d postgres-db
```

---

## Questions?

- Open an issue on GitHub
- Check existing issues for solutions
- Review project architecture in `README.md`
- Contact the team: see `.github/CODEOWNERS`
