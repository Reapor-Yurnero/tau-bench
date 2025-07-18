#!/bin/bash
#SBATCH -A memorization

#SBATCH --qos=alignment_shared
#SBATCH --partition=learn
#SBATCH --nodes=1
#SBATCH --gpus-per-node=8
#SBATCH --mem 512GB
#SBATCH --cpus-per-task 64

MODEL_NAME=$(basename "$MODEL_PATH")

vllm serve $MODEL_PATH \
    --dtype auto \
    --tensor-parallel-size 8 \
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

VLLM_HOST=localhost python run.py --agent-strategy tool-calling --env retail --model hosted_vllm/$MODEL_PATH --model-provider openai --user-model azure/gpt-4o --user-model-provider azure --user-strategy llm --max-concurrency 10 --num-trial 3 --log-dir "results/$MODEL_NAME"

VLLM_HOST=localhost python run.py --agent-strategy tool-calling --env airline --model hosted_vllm/$MODEL_PATH --model-provider openai --user-model azure/gpt-4o --user-model-provider azure --user-strategy llm --max-concurrency 10 --num-trial 3 --log-dir "results/$MODEL_NAME"

pkill -f "vllm serve"
#    --tool-call-parser llama3_json, hermes