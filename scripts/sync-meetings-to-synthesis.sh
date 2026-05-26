#!/usr/bin/env bash
set -euo pipefail

SRC="/home/sjoe/Noa-Hermes/autonomous/meetings"
DST="/home/sjoe/system/hermes-second-brain/second-brain/wiki/synthesis"

echo "Source: $SRC"
echo "Target: $DST"

mkdir -p "$DST"

echo "Clearing generated synthesis files..."
find "$DST" -maxdepth 1 -type f -delete

echo "Copying meeting records..."
cp "$SRC"/*.md "$DST"/
cp "$SRC"/*.json "$DST"/

echo "Done."
echo "Files in synthesis:"
find "$DST" -maxdepth 1 -type f | sort | wc -l
find "$DST" -maxdepth 1 -type f | sort
