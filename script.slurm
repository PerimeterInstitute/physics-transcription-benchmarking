#!/bin/bash
#SBATCH --output=output.txt           # Standard output file
#SBATCH --error=error.txt             # Standard error file
#SBATCH --partition=gpudebugq    # Partition or queue name
#SBATCH --nodes=1                     # Number of nodes
#SBATCH --gpus 2
#SBATCH --time=00:40:00                # Maximum runtime (D-HH:MM:SS)

#Load necessary modules (if needed)
module load python/3.10

source ~/physics-transcription-benchmarking/.venv/bin/activate

#Your job commands go here
#For example:
python run.py