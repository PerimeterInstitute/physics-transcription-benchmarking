from abc import ABC, abstractmethod
from os import getcwd

# ================================ #
# ==== ModelWrapper Interface ==== #
# ================================ #

class ModelWrapper(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def transcription(self):
        pass

    @property
    @abstractmethod
    def vtt(self):
        pass

    @property
    @abstractmethod
    def load_time(self):
        pass

    @property
    @abstractmethod
    def transcribe_time(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def unload(self):
        pass

    @abstractmethod
    def transcribe(self, audio_name, audio_file, prompt=None, output_dir=getcwd()):
        pass
