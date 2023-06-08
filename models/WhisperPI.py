from os.path import basename
from time import time
from datetime import timedelta
from ModelFormat import ModelFormat
import whisper

class WhisperPI(ModelFormat):

    name = ""
    model_type = ""
    options = {}
    model = None

    full_result = {}
    transcription = {}
    load_time = {}
    transcribe_time = {}

    def __init__(self, name, options):
        self.name = name
        self.model_type = options.pop("model_type", "large")
        self.options = options

        # load model
        load_start = time()
        self.model = whisper.load_model(self.model_type)
        load_end = time()

        self.__load_time__ = load_end - load_start

    def transcribe(self, audio, prompt=None):

        audio_name = basename(audio)

        # transcribe audio
        transcribe_start = time()
        result = self.model.transcribe(audio, initial_prompt=prompt, **self.options)
        transcribe_end = time()
        
        # save load time, and transcribe time, and full result
        self.load_time.update({audio_name: str(timedelta(seconds=self.__load_time__))})
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.full_result.update({audio_name: result})

        # save transcription
        transcription = ""
        for segment in result["segments"]:
            transcription += segment["text"]
        self.transcription.update({audio_name: transcription})
