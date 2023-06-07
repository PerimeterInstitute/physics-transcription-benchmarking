from os.path import basename
from time import time
from datetime import timedelta
from ModelFormat import ModelFormat
import whisper

class WhisperOpenAI(ModelFormat):

    name = ""
    model_type = ""
    options = {}
    full_result = {}
    transcription = {}
    load_time = {}
    transcribe_time = {}

    def __init__(self, name, options):
        self.name = name
        self.model_type = options.pop("model_type", "large")
        self.options = options

    def transcribe(self, audio, prompt=None):

        audio_name = basename(audio)

        # load model
        load_start = time()
        model = whisper.load_model(self.model_type)
        load_end = time()

        # transcribe audio
        transcribe_start = time()
        result = model.transcribe(audio, initial_prompt=prompt, **self.options)
        transcribe_end = time()
        
        # save load time, and transcribe time, and full result
        self.load_time.update({audio_name: str(timedelta(seconds=load_end - load_start))})
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.full_result.update({audio_name: result})

        # save transcription
        transcription = ""
        for segment in result["segments"]:
            transcription += segment["text"]
        self.transcription.update({audio_name: transcription})
