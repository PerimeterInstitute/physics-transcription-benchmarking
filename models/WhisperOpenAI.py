from time import time
from datetime import timedelta
from ModelWrapper import ModelWrapper
import whisper

class WhisperOpenAI(ModelWrapper):

    __model = None

    name = ""
    model_type = ""
    takes_prompt = True
    options = {}

    transcription = {}
    load_time = {}
    transcribe_time = {}
    result_object = {}

    def __init__(self, name, options):
        self.name = name
        self.model_type = options.pop("model_type", "large")
        self.options = options

    def load(self):

        # load model
        load_start = time()
        self.__model = whisper.load_model(self.model_type)
        load_end = time()

        self.__load_time__ = load_end - load_start

    def unload(self):
        del self.__model
        del self.name
        del self.model_type
        del self.options

    def transcribe(self, audio_name, audio_file, prompt=None):

        # transcribe audio
        transcribe_start = time()
        result = self.__model.transcribe(audio_file, initial_prompt=prompt, **self.options)
        transcribe_end = time()
        
        # save load time, transcribe time, and result object
        self.load_time.update({audio_name: str(timedelta(seconds=self.__load_time__))})
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.result_object.update({audio_name: result})

        # save transcription text
        transcription = ""
        for segment in result["segments"]:
            transcription += segment["text"]
        self.transcription.update({audio_name: transcription})

    def get_model(self):
        return self.__model
