#! /bin/bash

#SBATCH --partition=gpuq
#SBATCH --job-name=transcription_test
#SBATCH --nodelist=cn078
#SBATCH --nodes=1
#SBATCH --mem-per-gpu=4G
#SBATCH --gres=gpu:4
#SBATCH --output=%x-%j.out

python3 example.py

