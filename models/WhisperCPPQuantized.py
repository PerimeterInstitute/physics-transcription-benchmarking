from os import system, getcwd, chdir, mkdir
from os.path import join, isdir, expanduser
from subprocess import run
from time import time
from shutil import which, rmtree
from datetime import timedelta
from models.ModelWrapper import ModelWrapper
import gc

OUTPUT_FOLDER = "output-cpp-q"

class WhisperCPPQuantized(ModelWrapper):

    name = ""
    model_type = ""
    options = {}

    transcription = {}
    vtt = {}
    load_time = {}
    transcribe_time = {}

    def __init__(self, name, path_to_whispercpp, options):
        self.name = name
        self.model_type = options.pop("model_type", "large-v2")       # other model options listed here: https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#more-audio-samples
        self.quantize_type = options.pop("quantize_type", "q8_0")           # defaults to this quantization method
        self.options = options
        self.__transcribe_options = self.__getTranscribeOptions()
        self.__path_to_whispercpp = path_to_whispercpp
        self.__outputPath = join(path_to_whispercpp, OUTPUT_FOLDER)
        self.__model_file = "models/ggml-"+self.model_type+".bin"
        self.__q_model_file = "models/ggml-"+self.model_type+"-"+self.quantize_type+".bin"
        
    def load(self):

        # make output folder
        if not isdir(self.__outputPath):
            mkdir(self.__outputPath)

        with cd(self.__path_to_whispercpp):
            
            # load model
            load_start = time()

            # download model
            run(["bash", "models/download-ggml-model.sh", self.model_type])          # no check, since whispercpp does not download if it already exists!

            # create main executable
            if (which("main") == None):                 # if main does not exist
                system("WHISPER_CUDA=1 make -j")

            # quantize model
            run(["./quantize", self.__model_file, self.__q_model_file, self.quantize_type]) 

            load_end = time()

        self.load_time = str(timedelta(seconds=load_end - load_start))

    def unload(self):
        rmtree(self.__outputPath)       # delete output folder
        del self.name
        del self.model_type
        del self.quantize_type
        del self.options
        del self.__transcribe_options
        del self.__path_to_whispercpp
        del self.__outputPath
        del self.__model_file
        del self.__q_model_file
        gc.collect()

    def transcribe(self, audio_name, audio_file, prompt=None):

        with cd(self.__path_to_whispercpp):

            # transcribe audio
            transcribe_start = time()
            system("./main "+self.__transcribe_options+" -m "+self.__q_model_file+" -f "+audio_file+" --prompt \""+prompt+"\" --output-file "+join(self.__outputPath, audio_name)+ " --output-txt --output-vtt")
            transcribe_end = time()
        
        # save transcribe time, transcription text, and transcription vtt
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.transcription.update({audio_name: self.__createTranscription(audio_name)})
        self.vtt.update({audio_name: self.__createVTT(audio_name)})

    def makeClean(self):
        with cd(self.__path_to_whispercpp):
            system("make clean")

    def __createTranscription(self, audio_name):
        transcription = ""
        file = None

        # opening file
        try:
            file = open(join(self.__outputPath, audio_name+".txt"), "r")
        except:
            try:
                file = open(join(self.__outputPath, audio_name+".txt"), "r", encoding="latin-1")
            except:
                print("Could not transcribe file!")

        # reading file
        if file != None:
            transcription = file.readlines()
            file.close()

        return "\n".join(transcription)
    
    def __createVTT(self, audio_name):
        vtt = ""

        try:
            with open(join(self.__outputPath, audio_name+".vtt"), "r") as file:
                vtt = file.readlines()
        except:
            print("Could not transcribe file!")

        return "".join(vtt)

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
