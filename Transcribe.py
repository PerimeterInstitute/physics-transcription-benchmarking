from os import mkdir
from os.path import join, isdir
from helper_functions.prompt_functions import no_prompt
from helper_functions.test_transcribe_help import load_dataset
from whisper.normalizers import EnglishTextNormalizer
import gc

# ========================== #
# ==== Transcribe Class ==== #
# ========================== #

class Transcribe():

    def __init__(self, model, prompt_function=no_prompt):
        self.model = model
        self.prompt_function = prompt_function
        self.normalizer = EnglishTextNormalizer()

    def run(self, dataset_path="full", normalize=False):

        # LOADING DATASET:

        dataset = load_dataset(dataset_path)

        # CREATING OUTPUT FOLDER:

        if not isdir("./transcriptions/"):         # make 'transcriptions' folder if it doesn't already exist
            mkdir("./transcriptions/")

        # LOADING MODEL:

        self.model.load()

        # CREATING TRANSCRIPTIONS:

        for audio in dataset:

            # getting audio variables
            audio_name = audio["audio_name"]
            audio_file = audio["audio_file"]
            audio_info = audio["audio_info"]

            # creating prompt
            prompt = self.prompt_function(audio_info)

            # transcribing model
            self.model.transcribe(audio_name, join(dataset_path, "test_data", audio_file), prompt)

            # saving transcription as txt
            if audio_name in self.model.transcription:                               
                with open("./transcriptions/"+audio_name+".txt", "w") as f:     # TODO: use getcwd() instead of ./
                    text = self.model.transcription[audio_name]
                    if normalize:
                        text = self.normalizer(text)
                    f.write(text)
            
            # saving transcription as vtt
            if audio_name in self.model.vtt:
                with open("./transcriptions/"+audio_name+".vtt", "w") as f:     # TODO: use getcwd() instead of ./
                    f.write(self.model.vtt[audio_name])

            # freeing memory
            del audio_name
            del audio_file
            del audio_info
            del prompt
            gc.collect()

        # freeing memory
        self.model.unload()
        del dataset
        gc.collect()

    def free(self):
        del self.model
        del self.prompt_function
        del self.normalizer
        gc.collect()

