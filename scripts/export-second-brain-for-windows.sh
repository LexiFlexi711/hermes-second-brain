#!/usr/bin/env bash
set -euo pipefail

SRC="/home/sjoe/system/hermes-second-brain/second-brain"
OUT="/tmp/second-brain-clean.tar.gz"

tar \
  --exclude='.git' \
  --exclude='graphify-out' \
  --exclude='brain-cron.log' \
  --exclude='*/second-brain' \
  --exclude='*UTC*' \
  -czf "$OUT" \
  -C "$SRC" .

echo "Export created: $OUT"
ls -lh "$OUT"
