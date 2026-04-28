#!/usr/bin/env bash
set -euo pipefail

export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}
PORT=${PORT:-9100}
echo "Starting Sanctra Avatar GPU on port ${PORT}"
uvicorn server.main:app --host 0.0.0.0 --port "${PORT}"
