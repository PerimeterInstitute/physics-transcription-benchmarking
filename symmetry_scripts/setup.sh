#! /bin/bash

# Load slurm
module load slurm

# Load modules to use CUDA in Python:
module load cuda
module load python/3.8

# Install required Python modules
pip3 install ffmpeg-python
pip3 install jiwer
pip3 install git+https://github.com/rmohl/whisper.git
pip3 install -U openai-whisper
pip3 install azure-cognitiveservices-speech
