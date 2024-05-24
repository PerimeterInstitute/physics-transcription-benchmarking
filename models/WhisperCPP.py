from os import system, getcwd, chdir, mkdir
from os.path import join, isdir, expanduser
from subprocess import run
from time import time
from shutil import which
from datetime import timedelta
from models.ModelWrapper import ModelWrapper

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
        self.outputPath = join(pathToWhisperCPP, "transcriptions")
        if not isdir(self.outputPath):         # make output folder if it doesn't already exist
            mkdir(self.outputPath)
        self.makeClean()

    def load(self):

        with cd(self.pathToWhisperCPP):
            
            # load model
            load_start = time()

            # download model
            run(["bash", "models/download-ggml-model.sh", self.model_type])          # no check, since whispercpp does not download if it already exists!

            # create main executable
            if (which("main") == None):                 # if main does not exist
                system("WHISPER_CUDA=1 make -j")

            load_end = time()

        self.load_time = str(timedelta(seconds=load_end - load_start))

    def unload(self):
        del self.name
        del self.model_type
        del self.options

    def transcribe(self, audio_name, audio_file, prompt=None, create_vtt=False):

        with cd(self.pathToWhisperCPP):

            # remove quotes from prompt
            prompt = prompt.replace('"', '')

            # create transcribe command string
            cmd = "./main "+self.transcribe_options+" -m models/ggml-"+self.model_type+".bin -f "+audio_file+" --prompt \""+prompt+"\" --output-file "+join(self.outputPath, audio_name)+ " --output-txt"
            
            if create_vtt:
                cmd = cmd + " --output-vtt"

            # transcribe audio
            transcribe_start = time()
            system(cmd)
            transcribe_end = time()
        
        # save transcribe time and transcription text
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.transcription.update({audio_name: self.createTranscription(audio_name)})

    def createTranscription(self, audio_name):
        transcription = ""

        with open(join(self.outputPath, audio_name+".txt"), "r") as file:
            transcription = file.readlines()

        return " ".join(transcription)
    
    def makeClean(self):
        with cd(self.pathToWhisperCPP):
            system("make clean")

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
        self.newPath = expanduser(newPath)

    def __enter__(self):
        self.savedPath = getcwd()
        chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        chdir(self.savedPath)
