from time import time
from shutil import which
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
        self.model_type = options.pop("model_type", "medium.en")       # other model options listed here: https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#more-audio-samples
        self.options = options
        self.transcribe_options = self.getTranscribeOptions()
        self.pathToWhisperCPP = pathToWhisperCPP
        self.makeClean()

    def load(self):

        with cd(self.pathToWhisperCPP):
            
            # load model
            load_start = time()

            # download model
            subprocess.run(["bash", "models/download-ggml-model.sh", self.model_type])          # no check, since whispercpp does not download if it already exists!

            # create main executable
            if (which("main") == None):                 # if main does not exist
                os.system("WHISPER_CUDA=1 make -j")

            load_end = time()

        self.load_time = str(timedelta(seconds=load_end - load_start))

    def unload(self):
        del self.name
        del self.model_type
        del self.options

    def transcribe(self, audio_name, audio_file, prompt=None):

        with cd(self.pathToWhisperCPP):

            # transcribe audio
            transcribe_start = time()
            os.system("./main "+self.transcribe_options+" -m models/ggml-"+self.model_type+".bin -f "+audio_file+" > "+audio_name+".txt")
            transcribe_end = time()
        
        # save transcribe time and transcription text
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
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
    
    def makeClean(self):
        with cd(self.pathToWhisperCPP):
            os.system("make clean")

    def getTranscribeOptions(self):
        transcribe_options = []

        for key in self.options:
            key = key.strip()
            if key.startswith("-"):
                transcribe_options.append(key)
                transcribe_options.append(str(self.options[key]))

        return " ".join(transcribe_options)
    

class cd:     # from https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
