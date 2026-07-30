#!/bin/bash
set -x
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH=scripts
M=mlx-community/Qwen2.5-VL-3B-Instruct-4bit
python scripts/eval_vlm.py --run-id qwen3b-4bit-base_desc --model $M --mode describe > runs/logs/qwen3b-4bit-base_desc.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit-ftfull_desc --model $M --adapter-path runs/ft_full_adapter --mode describe > runs/logs/qwen3b-4bit-ftfull_desc.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit-ftholdout_desc --model $M --adapter-path runs/ft_holdout_adapter --mode describe > runs/logs/qwen3b-4bit-ftholdout_desc.log 2>&1
echo "DESC RUNS DONE"
