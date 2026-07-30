#!/bin/bash
# Download the State Farm Distracted Driver dataset.
# Preferred: official Kaggle competition route (requires ~/.kaggle/kaggle.json
# and accepting the competition rules on the Kaggle website).
# Fallback: HuggingFace mirror (no auth). Images are NEVER redistributed by
# this repo; you download them yourself under the original terms.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data

if [ -f "$HOME/.kaggle/kaggle.json" ] && command -v kaggle >/dev/null 2>&1; then
  echo "[official] Kaggle competition download"
  kaggle competitions download -c state-farm-distracted-driver-detection -p data/raw_kaggle
  unzip -q data/raw_kaggle/state-farm-distracted-driver-detection.zip -d data/raw_hf/extracted
else
  echo "[fallback] HuggingFace mirror (gymprathap/Driver-Distracted-Dataset)"
  echo "  For the official route: create a Kaggle API token (~/.kaggle/kaggle.json),"
  echo "  'pip install kaggle', and accept the competition rules at"
  echo "  https://www.kaggle.com/c/state-farm-distracted-driver-detection"
  hf download gymprathap/Driver-Distracted-Dataset --repo-type dataset --local-dir data/raw_hf
  unzip -q data/raw_hf/Distracted-Driver-Detection-Dataset.zip -d data/raw_hf/extracted
fi
echo "done: data/raw_hf/extracted"
find data/raw_hf/extracted -maxdepth 2 | head
