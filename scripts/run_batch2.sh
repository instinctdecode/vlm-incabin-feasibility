#!/bin/bash
# Batch 2: SmolVLM2-2.2B (bf16 + locally-quantized 4bit) zs/fs/prompt-sensitivity,
#          Qwen 3B/7B bf16 zero-shot p1 (quantization accuracy delta)
set -x
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH=scripts
mkdir -p runs/logs

# local 4-bit quantization of SmolVLM2 (no public 4bit repo on mlx-community).
# --dtype bfloat16 matters: without it, unquantized layers stay float32 and the
# result is ~10 bits/weight (2.6GB) instead of ~1.7GB. The published
# smolvlm2-4bit_zs_p1 run used exactly this conversion.
rm -rf models/smolvlm2-2.2b-4bit
python -m mlx_vlm.convert --hf-path mlx-community/SmolVLM2-2.2B-Instruct-mlx \
  -q --q-bits 4 --dtype bfloat16 --mlx-path models/smolvlm2-2.2b-4bit > runs/logs/convert_smolvlm2_4bit.log 2>&1

python scripts/eval_vlm.py --run-id smolvlm2-bf16_zs_p1 --model mlx-community/SmolVLM2-2.2B-Instruct-mlx --mode zeroshot --prompt p1 > runs/logs/smolvlm2-bf16_zs_p1.log 2>&1
python scripts/eval_vlm.py --run-id smolvlm2-bf16_zs_p2 --model mlx-community/SmolVLM2-2.2B-Instruct-mlx --mode zeroshot --prompt p2 > runs/logs/smolvlm2-bf16_zs_p2.log 2>&1
python scripts/eval_vlm.py --run-id smolvlm2-bf16_zs_p3 --model mlx-community/SmolVLM2-2.2B-Instruct-mlx --mode zeroshot --prompt p3 > runs/logs/smolvlm2-bf16_zs_p3.log 2>&1
python scripts/eval_vlm.py --run-id smolvlm2-bf16_fs1 --model mlx-community/SmolVLM2-2.2B-Instruct-mlx --mode fewshot --fewshot-per-class 1 > runs/logs/smolvlm2-bf16_fs1.log 2>&1
python scripts/eval_vlm.py --run-id smolvlm2-4bit_zs_p1 --model models/smolvlm2-2.2b-4bit --mode zeroshot --prompt p1 > runs/logs/smolvlm2-4bit_zs_p1.log 2>&1
python scripts/eval_vlm.py --run-id qwen3b-bf16_zs_p1 --model mlx-community/Qwen2.5-VL-3B-Instruct-bf16 --mode zeroshot --prompt p1 > runs/logs/qwen3b-bf16_zs_p1.log 2>&1
python scripts/eval_vlm.py --run-id qwen7b-bf16_zs_p1 --model mlx-community/Qwen2.5-VL-7B-Instruct-bf16 --mode zeroshot --prompt p1 > runs/logs/qwen7b-bf16_zs_p1.log 2>&1
echo "BATCH2 DONE"
