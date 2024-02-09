from time import time
from datetime import timedelta
from .ModelWrapper import ModelWrapper
import whisper
#import pi_whisper as whisper
import torch
import os

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

        quantized_model_path = os.path.join("./models/download/", f"{self.name}_quantized_model.pth")
        # If the quantized model directory doesn't exist, create it
        os.makedirs("./models/download/", exist_ok=True)
        
        if os.path.exists(quantized_model_path):
            # Load the quantized model if it exists
            self.__model = torch.load(quantized_model_path)
            return

        # load model
        load_start = time()
        self.__model = whisper.load_model(self.model_type)
        #create a quantized model instance
        self.__model = torch.ao.quantization.quantize_dynamic(
            self.__model,  # the original model
            {torch.nn.Linear},  # a set of layers to dynamically quantize
            dtype=torch.qint8)  # the target dtype for quantized weights

        load_end = time()

        # Save the quantized model to the specified directory
        torch.save(self.__model, quantized_model_path)

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
