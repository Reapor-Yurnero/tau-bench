#!/bin/bash
export CURRENT_TIME=$(TZ="America/New_York" date +"%m-%d_%H-%M-%S")
export CURRENT_DAY=$(TZ="America/New_York" date +"%m-%d")
mkdir -p /checkpoint/memorization/xhfu/jobs/${CURRENT_DAY}
# Generate timestamp in Eastern Time
TIME=$(TZ="America/New_York" date +"%H-%M-%S")

if [ $# -eq 0 ]; then
  echo "Error: No model path provided"
  exit 1
fi
# Get the file path from the first argument
MODEL_PATH="$1" # "meta-llama/Llama-3.1-8B-Instruct"


export AZURE_API_VERSION="2024-06-01"
export AZURE_API_BASE="https://azure-services-fair-openai1-northcentralus.azure-api.net"
export AZURE_API_KEY="YOUR_API_KEY"

export JOB_NAME="single_eval_${MODEL_PATH}"
echo $JOB_NAME
export MODEL_PATH

sbatch --job-name=${JOB_NAME} --output=/checkpoint/memorization/xhfu/jobs/${CURRENT_DAY}/slurm_%j_${JOB_NAME}_${TIME}.out --error=/checkpoint/memorization/xhfu/jobs/${CURRENT_DAY}/slurm_%j_${JOB_NAME}_${TIME}.err --export=ALL evaluate_one.slurm