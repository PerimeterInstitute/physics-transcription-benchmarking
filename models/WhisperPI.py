from time import time
from os import getcwd, mkdir
from os.path import join, isdir
from shutil import rmtree
from datetime import timedelta
from models.ModelWrapper import ModelWrapper
from pi_whisper.utils import get_writer
import pi_whisper as whisper
import gc

class WhisperPI(ModelWrapper):

    __model = None

    name = ""
    model_type = ""
    options = {}

    transcription = {}
    vtt = {}
    load_time = {}
    transcribe_time = {}
    result_object = {}

    def __init__(self, name, options):
        self.name = name
        self.model_type = options.pop("model_type", "large")
        self.options = options
        self.__outputPath = join(getcwd(), "output")
        self.__vtt_writer = get_writer("vtt", self.__outputPath)

    def load(self):

        # make output folder
        if not isdir(self.__outputPath):        
            mkdir(self.__outputPath)

        # load model
        load_start = time()
        self.__model = whisper.load_model(self.model_type)
        load_end = time()

        self.load_time = str(timedelta(seconds=load_end - load_start))

    def unload(self):
        rmtree(self.__outputPath)       # delete output folder
        del self.__model
        del self.name
        del self.model_type
        del self.options
        del self.__outputPath
        del self.__vtt_writer
        gc.collect()

    def transcribe(self, audio_name, audio_file, prompt=None):

        # transcribe audio
        transcribe_start = time()
        result = self.__model.transcribe(audio_file, initial_prompt=prompt, **self.options)
        transcribe_end = time()
        
        # save transcribe time, result object, transcription text, and transcription vtt
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.result_object.update({audio_name: result})
        self.transcription.update({audio_name: self.__createTranscription(audio_name)})
        self.vtt.update({audio_name: self.__createVTT(audio_name)})

    def __createTranscription(self, audio_name):
        transcription = ""

        for segment in self.result_object[audio_name]["segments"]:
            transcription += (segment["text"] + "\n")

        return transcription
        
    def __createVTT(self, audio_name):
        vtt = ""

        self.__vtt_writer(self.result_object[audio_name], audio_name+".vtt", {"max_line_width": None, "max_line_count": None, "highlight_words": None})
        with open(join(self.__outputPath, audio_name+".vtt"), 'r') as file:
            vtt = file.readlines()

        return "".join(vtt)

    def get_model(self):
        return self.__model
