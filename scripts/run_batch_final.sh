#!/bin/bash
# Final chain: smolvlm2 4bit re-convert+run -> CNN x2 -> ceiling models -> multiframe/fusion
set -x
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH=scripts
mkdir -p runs/logs

rm -rf models/smolvlm2-2.2b-4bit
python -m mlx_vlm.convert --hf-path mlx-community/SmolVLM2-2.2B-Instruct-mlx \
  -q --q-bits 4 --dtype bfloat16 --mlx-path models/smolvlm2-2.2b-4bit > runs/logs/convert_smolvlm2_4bit.log 2>&1
python scripts/eval_vlm.py --run-id smolvlm2-4bit_zs_p1 --model models/smolvlm2-2.2b-4bit --mode zeroshot --prompt p1 > runs/logs/smolvlm2-4bit_zs_p1.log 2>&1

python scripts/train_cnn.py --arch mobilenet_v3_small > runs/logs/cnn_mobilenet_v3_small.log 2>&1
python scripts/train_cnn.py --arch resnet18 > runs/logs/cnn_resnet18.log 2>&1

bash scripts/run_batch3.sh > runs/logs/batch3.log 2>&1
bash scripts/run_batch4.sh > runs/logs/batch4.log 2>&1
echo "FINAL CHAIN DONE"
