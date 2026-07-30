#!/bin/bash
# Batch 5 (task B): QLoRA fine-tune Qwen2.5-VL-3B-4bit (full + c9-holdout),
# then re-evaluate on the frozen 250 set + open-vocab describe probes.
set -x
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH=scripts
mkdir -p runs/logs

T0=$SECONDS
python -m mlx_vlm.lora --model-path mlx-community/Qwen2.5-VL-3B-Instruct-4bit \
  --dataset data/ft_full --split train --learning-rate 1e-4 --batch-size 2 \
  --epochs 2 --steps-per-report 50 --steps-per-save 500 \
  --lora-rank 16 --lora-alpha 32 --lora-dropout 0.05 --train-on-completions \
  --output-path runs/ft_full_adapter > runs/logs/train_ft_full.log 2>&1
echo "FT_FULL_TRAIN_SECONDS=$((SECONDS-T0))" >> runs/logs/train_ft_full.log

T1=$SECONDS
python -m mlx_vlm.lora --model-path mlx-community/Qwen2.5-VL-3B-Instruct-4bit \
  --dataset data/ft_holdout --split train --learning-rate 1e-4 --batch-size 2 \
  --epochs 2 --steps-per-report 50 --steps-per-save 500 \
  --lora-rank 16 --lora-alpha 32 --lora-dropout 0.05 --train-on-completions \
  --output-path runs/ft_holdout_adapter > runs/logs/train_ft_holdout.log 2>&1
echo "FT_HOLDOUT_TRAIN_SECONDS=$((SECONDS-T1))" >> runs/logs/train_ft_holdout.log

M=mlx-community/Qwen2.5-VL-3B-Instruct-4bit
python scripts/eval_vlm.py --run-id qwen3b-4bit-ftfull_zs_p1 --model $M --adapter-path runs/ft_full_adapter --mode zeroshot --prompt p1 > runs/logs/qwen3b-4bit-ftfull_zs_p1.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit-ftfull_zs_p2 --model $M --adapter-path runs/ft_full_adapter --mode zeroshot --prompt p2 > runs/logs/qwen3b-4bit-ftfull_zs_p2.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit-ftfull_zs_p3 --model $M --adapter-path runs/ft_full_adapter --mode zeroshot --prompt p3 > runs/logs/qwen3b-4bit-ftfull_zs_p3.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit-ftholdout_zs_p1 --model $M --adapter-path runs/ft_holdout_adapter --mode zeroshot --prompt p1 > runs/logs/qwen3b-4bit-ftholdout_zs_p1.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit-base_desc --model $M --mode describe > runs/logs/qwen3b-4bit-base_desc.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit-ftfull_desc --model $M --adapter-path runs/ft_full_adapter --mode describe > runs/logs/qwen3b-4bit-ftfull_desc.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-4bit-ftholdout_desc --model $M --adapter-path runs/ft_holdout_adapter --mode describe > runs/logs/qwen3b-4bit-ftholdout_desc.log 2>&1
echo "BATCH5 DONE"
