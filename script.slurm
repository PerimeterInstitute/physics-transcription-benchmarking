#!/bin/bash
#SBATCH --output=output.txt           # Standard output file
#SBATCH --error=error.txt             # Standard error file
#SBATCH --partition=gpuq    # Partition or queue name
#SBATCH --nodes=1                     # Number of nodes
#SBATCH --gpus 2
#SBATCH --time=02:30:00                # Maximum runtime (D-HH:MM:SS)

source ~/physics-transcription-benchmarking/.venv/bin/activate

#Your job commands go here
#For example:
python run.py