#!/bin/bash
# Batch 4: stage 5 (multi-frame 2/4/8) + stage 7 (synthetic-HR fusion) on
#          Qwen2.5-VL-7B-4bit (strongest edge-plausible candidate),
#          plus 3B-4bit multiframe-4 for a size contrast.
set -x
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH=scripts
mkdir -p runs/logs

python scripts/eval_vlm.py --run-id qwen7b-4bit_mf2 --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode multiframe --frames 2 > runs/logs/qwen7b-4bit_mf2.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-4bit_mf4 --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode multiframe --frames 4 > runs/logs/qwen7b-4bit_mf4.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-4bit_mf8 --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode multiframe --frames 8 > runs/logs/qwen7b-4bit_mf8.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit_mf4 --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit --mode multiframe --frames 4 > runs/logs/qwen3b-4bit_mf4.log 2>&1
# SYNTHETIC heart-rate context (not real measurements) — fusion structure test
python scripts/eval_vlm.py --run-id qwen7b-4bit_fusion_normal --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode fusion --fusion-hr normal > runs/logs/qwen7b-4bit_fusion_normal.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-4bit_fusion_low --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode fusion --fusion-hr low > runs/logs/qwen7b-4bit_fusion_low.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-4bit_fusion_high --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit --mode fusion --fusion-hr high > runs/logs/qwen7b-4bit_fusion_high.log 2>&1
echo "BATCH4 DONE"
