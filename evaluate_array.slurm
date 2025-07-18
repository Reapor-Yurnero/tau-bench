#!/bin/bash
#SBATCH -A memorization

#SBATCH --qos=alignment_shared
#SBATCH --partition=learn
#SBATCH --nodes=1
#SBATCH --gpus-per-node=4
#SBATCH --mem 512GB
#SBATCH --cpus-per-task 64
#SBATCH --array=0-9%3  # This will be replaced by the actual count of checkpoints

# Environment variable for checkpoint directory
# Example: CHECKPOINT_DIR=/checkpoint/memorization/xhfu/sft_models/meta-llama/Llama-3.1-8B-Instruct_IL
if [ -z "$CHECKPOINT_DIR" ]; then
    echo "Error: CHECKPOINT_DIR environment variable not set"
    exit 1
fi

# Use the checkpoint list file that was created by the wrapper script
CHECKPOINT_LIST="${CHECKPOINT_DIR}/checkpoint_list.txt"

# Verify the checkpoint list exists
if [ ! -f "$CHECKPOINT_LIST" ]; then
    echo "Error: Checkpoint list file not found at $CHECKPOINT_LIST"
    echo "Make sure to run this job through the submit_checkpoint_eval.sh wrapper"
    exit 1
fi

# Get the total number of checkpoints
TOTAL_CHECKPOINTS=$(wc -l < "$CHECKPOINT_LIST")
if [ "$TOTAL_CHECKPOINTS" -eq 0 ]; then
    echo "Error: No checkpoints found in $CHECKPOINT_DIR"
    exit 1
fi

# Skip if this task ID is beyond the available checkpoints
if [ "$SLURM_ARRAY_TASK_ID" -ge "$TOTAL_CHECKPOINTS" ]; then
    echo "Task ID $SLURM_ARRAY_TASK_ID exceeds number of available checkpoints ($TOTAL_CHECKPOINTS). Nothing to do."
    exit 0
fi

# Get the checkpoint for this array task
# Add 1 to SLURM_ARRAY_TASK_ID because sed line numbers start from 1, not 0
CHECKPOINT_PATH=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" "$CHECKPOINT_LIST")

# Create a more descriptive checkpoint name with both model name and checkpoint step
MODEL_NAME=$(basename "$(dirname "$CHECKPOINT_PATH")")
CHECKPOINT_STEP=$(basename "$CHECKPOINT_PATH")
CHECKPOINT_NAME="${MODEL_NAME}_${CHECKPOINT_STEP}"

echo "Processing checkpoint $SLURM_ARRAY_TASK_ID/$TOTAL_CHECKPOINTS: $CHECKPOINT_PATH"

# Start vLLM server
vllm serve "$CHECKPOINT_PATH" \
    --dtype auto \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --host 0.0.0.0 \
    --enable-auto-tool-choice \
    --tool-call-parser llama3_json &

# Wait for vLLM server to start
echo "Waiting for vLLM server to start... (initial 60s delay)"
sleep 60

# After initial delay, start checking server availability
echo "Checking vLLM server status..."
max_attempts=60
attempt=1
while [ $attempt -le $max_attempts ]; do
    if curl -s "http://localhost:8000/v1/models" | grep -q "id"; then
        echo "vLLM server is up and running"
        break
    fi
    echo "Attempt $attempt/$max_attempts: Server not ready yet, waiting..."
    sleep 10
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Error: vLLM server failed to start after $(( 60 + 10*max_attempts ))s"
    exit 1
fi

# Run the evaluation
VLLM_HOST=localhost python run.py \
    --agent-strategy tool-calling \
    --env retail \
    --num-trial 3 \
    --model "hosted_vllm/$CHECKPOINT_PATH" \
    --model-provider openai \
    --user-model azure/gpt-4o \
    --user-model-provider azure \
    --user-strategy llm \
    --max-concurrency 10 \
    --log-dir "results/$CHECKPOINT_NAME"

VLLM_HOST=localhost python run.py \
    --agent-strategy tool-calling \
    --env airline \
    --num-trial 3 \
    --model "hosted_vllm/$CHECKPOINT_PATH" \
    --model-provider openai \
    --user-model azure/gpt-4o \
    --user-model-provider azure \
    --user-strategy llm \
    --max-concurrency 10 \
    --log-dir "results/$CHECKPOINT_NAME"

# Kill the vLLM server
pkill -f "vllm serve"

# We'll leave the checkpoint list file for now
# It will be overwritten next time or can be manually removed if needed
# Not deleting it here avoids race conditions between concurrent tasks
echo "Task completed for checkpoint $SLURM_ARRAY_TASK_ID: $CHECKPOINT_PATH"