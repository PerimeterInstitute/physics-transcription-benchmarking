from os.path import basename, exists
from os import system
from time import time
from datetime import timedelta
from ModelFormat import ModelFormat
from whispercpp import Whisper
from whisper.tokenizer import get_tokenizer

class WhisperCPP(ModelFormat):

    name = ""
    model_type = ""
    options = {}
    model = None

    transcription = {}
    load_time = {}
    transcribe_time = {}
    

    def __init__(self, name, options):
        self.name = name
        self.model_type = options.pop("model_type", "large")
        self.options = options

        # download/load model
        load_start = time()
        self.model = Whisper.from_pretrained(self.model_type)
        load_end = time()

        self.__load_time__ = load_end - load_start

    def transcribe(self, audio, prompt=None):

        audio_name = basename(audio)
        audio_wav = audio.rsplit(".", 1)[0] + ".wav"
        audio_ext = audio.rsplit(".", 1)[1]

        # converting audio file to .wav file (only if .wav file has not already been created AND current audio file is not .wav file)
        if exists(audio_wav):
            audio = audio_wav
        elif not audio_ext == "wav":
            system("ffmpeg -i " + audio + " -ar 16000 -ac 1 -c:a pcm_s16le " + audio_wav)
            audio = audio_wav

        # set prompt
        if not prompt == None:
            # tokenizing prompt
            tokenizer = get_tokenizer(multilingual=False, language=self.options["language"], task="transcribe")
            prompt_tokens = tokenizer.encode(" " + prompt.strip())
            # setting prompt tokens
            self.model.params.set_tokens(prompt_tokens)

        # set options
        for key in self.options:
            exec('self.model.params.with_'+key+'(self.options["'+key+'"])')      # using exec() function so param setter function can change

        # transcribe audio
        transcribe_start = time()
        transcription = self.model.transcribe_from_file(audio)
        transcribe_end = time()
        
        # save load time, transcribe time, and transcription
        self.load_time.update({audio_name: str(timedelta(seconds=self.__load_time__))})
        self.transcribe_time.update({audio_name: str(timedelta(seconds=transcribe_end - transcribe_start))})
        self.transcription.update({audio_name: transcription})
