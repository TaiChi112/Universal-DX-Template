#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "========================================"
echo "Running Pre-commit Checks (Universal DX)"
echo "========================================"

# 1. ตรวจสอบ Python (FastAPI)
echo "[1/2] Checking Python Service (core-api-python)..."
cd services/core-api-python || exit 1

echo "  -> Running Black (Code Formatter)"
python -m black --check . || {
    echo "ERROR: Python code formatting failed. Please run 'black .' to fix."
    exit 1
}

echo "  -> Running Flake8 (Linter)"
python -m flake8 . || {
    echo "ERROR: Python linting failed. Please fix the Flake8 warnings."
    exit 1
}

# กลับมาที่ Root directory
cd ../..

# 2. ตรวจสอบ Rust (Actix)
echo "[2/2] Checking Rust Service (data-engine-rust)..."
cd services/data-engine-rust || exit 1

echo "  -> Running Cargo Fmt (Code Formatter)"
cargo fmt -- --check || {
    echo "ERROR: Rust code formatting failed. Please run 'cargo fmt' to fix."
    exit 1
}

echo "  -> Running Cargo Clippy (Linter)"
cargo clippy -- -D warnings || {
    echo "ERROR: Rust linting failed. Please fix the Clippy warnings."
    exit 1
}

# กลับมาที่ Root directory
cd ../..

echo "========================================"
echo "All pre-commit checks passed! Committing..."
echo "========================================"