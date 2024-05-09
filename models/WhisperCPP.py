from time import time
from datetime import timedelta
from models.ModelWrapper import ModelWrapper
import os, subprocess

class WhisperCPP(ModelWrapper):

    name = ""
    model_type = ""
    takes_prompt = True
    options = {}

    transcription = {}
    load_time = {}
    transcribe_time = {}
    result_object = {}

    def __init__(self, name, pathToWhisperCPP, options):
        self.name = name
        self.model_type = options.pop("model_type", "base.en")       # other model options listed here: https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#more-audio-samples
        self.options = options
        self.pathToWhisperCPP = pathToWhisperCPP

    def load(self):

        with cd(self.pathToWhisperCPP):
            # load model
            load_start = time()
            subprocess.run(["bash", "models/download-ggml-model.sh", self.model_type]) 
            subprocess.run(["make"]) 
            load_end = time()

        self.__load_time__ = load_end - load_start

    def unload(self):
        del self.name
        del self.model_type
        del self.options

    def transcribe(self, audio_name, audio_file, prompt=None):

        with cd(self.pathToWhisperCPP):
            # transcribe audio
            transcribe_start = time()
            os.system("./main "+audio_file+" > "+audio_name+".txt")
            # subprocess.run(["./main", audio_file]) 
            transcribe_end = time()
        
        # save load time, transcribe time, and result object
        self.load_time.update({audio_name: str(timedelta(seconds=self.__load_time__))})
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})

        # save transcription text
        self.transcription.update({audio_name: self.createTranscription(audio_name)})
        

    def createTranscription(self, audio_name):
        transcription = ""

        file = open(os.path.join(self.pathToWhisperCPP, audio_name+".txt"), "r")
        lines = file.readlines()

        for line in lines:
            split_line = line.split("]", 1)

            if len(split_line) > 1:
                transcription = transcription + split_line[1].strip() + " "

        file.close()

        return transcription
    
class cd:                                                                               # from https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
