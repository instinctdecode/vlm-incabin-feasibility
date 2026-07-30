#!/bin/bash
# Batch 2b: rerun 3B few-shot (fixed interleaved 224px format), then batch2
set -x
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH=scripts
mkdir -p runs/logs
python scripts/eval_vlm.py --run-id qwen3b-4bit_fs1 --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit --mode fewshot --fewshot-per-class 1 > runs/logs/qwen3b-4bit_fs1.log 2>&1
bash scripts/run_batch2.sh
