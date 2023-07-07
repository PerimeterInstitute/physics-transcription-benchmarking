from os.path import basename
from time import time
from datetime import timedelta
from ModelWrapper import ModelWrapper
import azure.cognitiveservices.speech as speechsdk

class AzureSpeechToText(ModelWrapper):

    __speech_config = None

    name = ""
    options = {}

    transcription = {}
    load_time = {}
    transcribe_time = {}

    def __init__(self, name, key, region, options):
        self.name = name
        self.options = options

        # create speech configuration
        load_start = time()
        self.__speech_config = speechsdk.SpeechConfig(subscription=key, region=region, speech_recognition_language=self.options.pop("language", None))
        load_end = time()

        self.__load_time__ = load_end - load_start

    def transcribe(self, audio, prompt=None):

        audio_name = basename(audio)

        # transcribe audio
        transcribe_start = time()

        audio_config = speechsdk.audio.AudioConfig(filename=audio)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.__speech_config, audio_config=audio_config)
        
        # TODO: this will only transcribe max 15s, do something with start_continuous_recognition_async() func instead
        result = speech_recognizer.recognize_once()     

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized by Azure: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

        transcribe_end = time()
        
        # save load time, and transcribe time, and transcription
        self.load_time.update({audio_name: str(timedelta(seconds=self.__load_time__))})
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.transcription.update({audio_name: result})
