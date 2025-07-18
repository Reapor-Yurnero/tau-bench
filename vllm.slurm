#!/bin/bash
#SBATCH -A memorization

#SBATCH --qos=alignment_shared
#SBATCH --partition=learn
#SBATCH --nodes=1
#SBATCH --gpus-per-node=8
#SBATCH --mem 512GB
#SBATCH --cpus-per-task 64


vllm serve /checkpoint/memorization/xhfu/sft_models/meta-llama/Llama-3.1-8B-Instruct_WM_IL/ \
    --dtype auto \
    --tensor-parallel-size 8 \
    --max-model-len 32768 \
    --host 0.0.0.0 \
    --enable-auto-tool-choice \
    --tool-call-parser llama3_json &

#    --tool-call-parser hermes # for qwen