from os import system, getcwd, chdir, mkdir
from os.path import join, isdir, expanduser
from subprocess import run
from time import time
from shutil import which, rmtree
from datetime import timedelta
from models.ModelWrapper import ModelWrapper

class WhisperCPP(ModelWrapper):

    name = ""
    model_type = ""
    options = {}

    transcription = {}
    vtt = {}
    load_time = {}
    transcribe_time = {}

    def __init__(self, name, pathToWhisperCPP, options):
        self.name = name
        self.model_type = options.pop("model_type", "medium.en")       # other model options listed here: https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#more-audio-samples
        self.options = options
        self.__transcribe_options = self.__getTranscribeOptions()
        self.__pathToWhisperCPP = pathToWhisperCPP
        self.__outputPath = join(pathToWhisperCPP, "output")
        if not isdir(self.__outputPath):         # make output folder if it doesn't already exist
            mkdir(self.__outputPath)
        self.__makeClean()

    def load(self):

        with cd(self.__pathToWhisperCPP):
            
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

    def transcribe(self, audio_name, audio_file, prompt=None):

        with cd(self.__pathToWhisperCPP):

            # remove quotes from prompt
            prompt = prompt.replace('"', '')

            # transcribe audio
            transcribe_start = time()
            system("./main "+self.__transcribe_options+" -m models/ggml-"+self.model_type+".bin -f "+audio_file+" --prompt \""+prompt+"\" --output-file "+join(self.__outputPath, audio_name)+ " --output-txt --output-vtt")
            transcribe_end = time()
        
        # save transcribe time, transcription text, and transcription vtt
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.transcription.update({audio_name: self.__createTranscription(audio_name)})
        self.vtt.update({audio_name: self.__createVTT(audio_name)})

        # delete output folder and contents
        rmtree(self.__outputPath)

    def __createTranscription(self, audio_name):
        transcription = ""

        with open(join(self.__outputPath, audio_name+".txt"), "r") as file:
            transcription = file.readlines()

        return "".join(transcription)
    
    def __createVTT(self, audio_name):
        vtt = ""

        with open(join(self.__outputPath, audio_name+".vtt"), "r") as file:
            vtt = file.readlines()

        return "".join(vtt)
    
    def __makeClean(self):
        with cd(self.__pathToWhisperCPP):
            system("make clean")

    def __getTranscribeOptions(self):
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
