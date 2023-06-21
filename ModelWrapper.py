from abc import ABC, abstractmethod

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
    def load_time(self):
        pass

    @property
    @abstractmethod
    def transcribe_time(self):
        pass

    @abstractmethod
    def transcribe(self, audio, prompt=None):
        pass