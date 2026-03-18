#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "========================================"
echo "Running Pre-push Checks (Universal DX)"
echo "========================================"

# 1. รัน Python Test Suite
echo "[1/2] Running Python Tests (core-api-python)..."
cd services/core-api-python || exit 1

echo "  -> Running Pytest"
python -m pytest -v || {
    echo "ERROR: Python test suite failed. Push aborted."
    exit 1
}

# กลับมาที่ Root directory
cd ../..

# 2. รัน Rust Test Suite
echo "[2/2] Running Rust Tests (data-engine-rust)..."
cd services/data-engine-rust || exit 1

echo "  -> Running Cargo Test"
cargo test || {
    echo "ERROR: Rust test suite failed. Push aborted."
    exit 1
}

# กลับมาที่ Root directory
cd ../..

echo "========================================"
echo "All pre-push tests passed! Pushing..."
echo "========================================"