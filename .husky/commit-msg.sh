#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "========================================"
echo "Running Commit Message Guard (Conventional Commits)"
echo "========================================"

# 1. อ่านไฟล์ commit message จาก argument ที่ Husky ส่งเข้ามา
COMMIT_MSG_FILE="$1"
COMMIT_MSG="$(cat "$COMMIT_MSG_FILE")"

# 2. ตรวจสอบรูปแบบ Conventional Commits
# ต้องขึ้นต้นด้วย:
# feat:, fix:, docs:, style:, refactor:, perf:, test:, build:, ci:, chore:, revert:
# และต้องมีช่องว่างตามหลังเครื่องหมาย :
echo "$COMMIT_MSG" | grep -Eq "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert): .+" || {
    echo "ERROR: Invalid commit message format."
    echo "Your commit message must follow Conventional Commits."
    echo "Valid example: feat: add health check endpoint"
    exit 1
}

echo "========================================"
echo "Commit message format is valid."
echo "========================================"