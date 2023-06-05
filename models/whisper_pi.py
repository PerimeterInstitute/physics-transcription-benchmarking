from time import time
from datetime import timedelta
import whisper

class WhisperPI:

    def __init__(self, options):
        self.model_type = options.pop("model_type", "large")
        self.options = options
        self.resultObj = None
        self.transcription = None
        self.load_time = None
        self.transcribe_time = None

    def transcribe(self, audio, prompt=None):

        # load model
        load_start = time()
        model = whisper.load_model(self.model_type)
        load_end = time()

        # transcribe audio
        transcribe_start = time()
        result = model.transcribe(audio, initial_prompt=prompt, **self.options)
        transcribe_end = time()
        
        self.load_time = timedelta(seconds=load_end - load_start)
        self.transcribe_time = timedelta(seconds=transcribe_end - transcribe_start)
        self.resultObj = result

        self.transcription = ""
        for segment in self.resultObj["segments"]:
            self.transcription += segment["text"]
