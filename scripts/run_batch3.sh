#!/bin/bash
# Batch 3: upper-reference models (NOT edge candidates — accuracy ceiling)
#          Qwen2.5-VL-32B-4bit zs+fs, 72B-4bit zs (if downloaded)
set -x
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH=scripts
mkdir -p runs/logs

python scripts/eval_vlm.py --run-id qwen32b-4bit_zs_p1 --model mlx-community/Qwen2.5-VL-32B-Instruct-4bit --mode zeroshot --prompt p1 > runs/logs/qwen32b-4bit_zs_p1.log 2>&1
python scripts/eval_vlm.py --run-id qwen32b-4bit_fs1 --model mlx-community/Qwen2.5-VL-32B-Instruct-4bit --mode fewshot --fewshot-per-class 1 > runs/logs/qwen32b-4bit_fs1.log 2>&1
python scripts/eval_vlm.py --run-id qwen72b-4bit_zs_p1 --model mlx-community/Qwen2.5-VL-72B-Instruct-4bit --mode zeroshot --prompt p1 > runs/logs/qwen72b-4bit_zs_p1.log 2>&1
echo "BATCH3 DONE"
