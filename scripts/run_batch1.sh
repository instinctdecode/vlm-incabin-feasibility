#!/bin/bash
# Batch 1: Qwen2.5-VL 3B/7B 4bit — zero-shot p1/p2/p3 + few-shot (frozen 250)
set -x
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH=scripts
mkdir -p runs/logs
python scripts/eval_vlm.py --run-id qwen3b-4bit_zs_p1 --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit --mode zeroshot --prompt p1 > runs/logs/qwen3b-4bit_zs_p1.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit_zs_p2 --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit --mode zeroshot --prompt p2 > runs/logs/qwen3b-4bit_zs_p2.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit_zs_p3 --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit --mode zeroshot --prompt p3 > runs/logs/qwen3b-4bit_zs_p3.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit_fs1 --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit --mode fewshot --fewshot-per-class 1 > runs/logs/qwen3b-4bit_fs1.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-4bit_zs_p1 --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode zeroshot --prompt p1 > runs/logs/qwen7b-4bit_zs_p1.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-4bit_zs_p2 --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode zeroshot --prompt p2 > runs/logs/qwen7b-4bit_zs_p2.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-4bit_zs_p3 --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode zeroshot --prompt p3 > runs/logs/qwen7b-4bit_zs_p3.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-4bit_fs1 --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode fewshot --fewshot-per-class 1 > runs/logs/qwen7b-4bit_fs1.log 2>&1
echo "BATCH1 DONE"
