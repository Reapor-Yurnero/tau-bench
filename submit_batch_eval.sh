#!/bin/bash

# Generate timestamp in Eastern Time
export CURRENT_TIME=$(TZ="America/New_York" date +"%m-%d_%H-%M-%S")
export CURRENT_DAY=$(TZ="America/New_York" date +"%m-%d")
mkdir -p /checkpoint/memorization/xhfu/jobs/${CURRENT_DAY}
TIME=$(TZ="America/New_York" date +"%H-%M-%S")

# Parse command line arguments
if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/checkpoint/directory [max_concurrent_jobs]"
  echo "Example: $0 /checkpoint/memorization/xhfu/sft_models/meta-llama/Llama-3.1-8B-Instruct_IL 3"
  exit 1
fi

# Get checkpoint directory from command line or use default
if [ $# -ge 1 ]; then
  CHECKPOINT_DIR="$1"
else
  echo "Error: No checkpoint directory provided"
  exit 1
fi

# Get max concurrent jobs from command line or use default
if [ $# -ge 2 ]; then
  MAX_CONCURRENT="$2"
else
  MAX_CONCURRENT=3  # Default: run 3 jobs concurrently
fi

# Verify the checkpoint directory exists
if [ ! -d "$CHECKPOINT_DIR" ]; then
  echo "Error: Checkpoint directory not found: $CHECKPOINT_DIR"
  exit 1
fi

echo "Scanning for checkpoints in: $CHECKPOINT_DIR"

# Create checkpoint list file directly in the checkpoint directory
CHECKPOINT_LIST_FILE="${CHECKPOINT_DIR}/checkpoint_list.txt"
find "$CHECKPOINT_DIR" -type d -name "checkpoint-*" | sort > "$CHECKPOINT_LIST_FILE"

# Count checkpoint folders
CHECKPOINT_COUNT=$(wc -l < "$CHECKPOINT_LIST_FILE")

if [ "$CHECKPOINT_COUNT" -eq 0 ]; then
  echo "Error: No checkpoint folders found in $CHECKPOINT_DIR"
  rm "$CHECKPOINT_LIST_FILE"
  exit 1
fi

echo "Found $CHECKPOINT_COUNT checkpoint folders, list saved to $CHECKPOINT_LIST_FILE"

# Set job name
JOB_NAME="ckpt-eval-$(basename "$CHECKPOINT_DIR")"

# Build the array parameter
ARRAY_PARAM="0-$((CHECKPOINT_COUNT-1))%$MAX_CONCURRENT"

export AZURE_API_VERSION="2024-06-01"
export AZURE_API_BASE="https://azure-services-fair-openai1-northcentralus.azure-api.net"
export AZURE_API_KEY="YOUR_API_KEY"

# Submit the job with the array parameter
echo "Submitting job with array=$ARRAY_PARAM"
JOB_ID=$(sbatch --job-name=${JOB_NAME} \
  --output=/checkpoint/memorization/xhfu/jobs/${CURRENT_DAY}/slurm_%j_${JOB_NAME}_${TIME}.out \
  --error=/checkpoint/memorization/xhfu/jobs/${CURRENT_DAY}/slurm_%j_${JOB_NAME}_${TIME}.err \
  --array=$ARRAY_PARAM \
  --export=ALL,CHECKPOINT_DIR="$CHECKPOINT_DIR" \
  /home/xhfu/tau-bench/evaluate_array.slurm | awk '{print $NF}')

echo "Submitted job with ID: $JOB_ID"
echo "Job will process $CHECKPOINT_COUNT checkpoints with max $MAX_CONCURRENT concurrent jobs"
echo "Job output will be written to: /checkpoint/memorization/xhfu/jobs/${CURRENT_DAY}/slurm_${JOB_ID}_${JOB_NAME}_${TIME}.out"
echo "Monitor with: squeue -j $JOB_ID"