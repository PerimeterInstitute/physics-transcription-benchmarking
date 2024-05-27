from time import time
from datetime import timedelta
from ModelWrapper import ModelWrapper
import azure.cognitiveservices.speech as speechsdk

class AzureSpeechToText(ModelWrapper):

    __speech_config = None

    name = ""
    key = ""
    region = ""
    options = {}

    transcription = {}
    vtt = {}                # TODO: fill this in transcribe() function
    load_time = {}
    transcribe_time = {}

    def __init__(self, name, key, region, options):
        self.name = name
        self.key = key
        self.region = region
        self.options = options

    def load(self):

        # create speech configuration
        load_start = time()
        self.__speech_config = speechsdk.SpeechConfig(subscription=self.key, region=self.region, **self.options)
        load_end = time()

        self.load_time = str(timedelta(seconds=load_end - load_start))

    def unload(self):
        del self.__speech_config
        del self.name
        del self.key
        del self.region
        del self.options

    def transcribe(self, audio_name, audio_file, prompt=None):

        # transcribe audio
        transcribe_start = time()

        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.__speech_config, audio_config=audio_config)
        
        result = ""
        finished = False
        while not finished:

            utterance = speech_recognizer.recognize_once()     

            if utterance.reason == speechsdk.ResultReason.RecognizedSpeech:
                result += utterance.text + "\n"

            elif utterance.reason == speechsdk.ResultReason.NoMatch:
                if utterance.no_match_details.reason == speechsdk.NoMatchReason.InitialSilenceTimeout:      # if the end of the audio file was reached
                    finished = True
                else:
                    print("No speech could be recognized: {}".format(utterance.no_match_details))

            elif utterance.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = utterance.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
                finished = True

        transcribe_end = time()
        
        # save transcribe time and transcription
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.transcription.update({audio_name: result})

    def get_speech_config(self):
        return self.__speech_config
