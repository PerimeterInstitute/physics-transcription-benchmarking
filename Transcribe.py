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

    def __init__(self, model_array, prompt_function_array=[no_prompt]):
        self.model_array = model_array
        self.prompt_function_array = prompt_function_array
        self.normalizer = EnglishTextNormalizer()

    def run(self, run_name, dataset_path, normalize=False):

        # LOADING DATASET:

        dataset = load_dataset(dataset_path)
        if dataset == None:
            print("Invalid dataset path provided: '"+dataset_path+"'")
            return

        # CREATING OUTPUT FOLDER:

        transcriptions_folder = "./transcriptions-"+run_name+"/"
        if not isdir(transcriptions_folder):         # make 'transcriptions' folder if it doesn't already exist
            mkdir(transcriptions_folder)

        # CREATING TRANSCRIPTIONS:

        for model in self.model_array:

            # load model
            model.load()

            for prompt_function in self.prompt_function_array:

                for audio in dataset:

                    # getting audio variables
                    audio_name = audio["audio_name"]
                    audio_file = audio["audio_file"]
                    audio_info = audio["audio_info"]

                    # creating prompt
                    prompt = prompt_function(audio_info)

                    # transcribing model
                    model.transcribe(audio_name, join(dataset_path, "test_data", audio_file), prompt)

                    # saving transcription as txt
                    if audio_name in model.transcription:   
                        transcription = model.transcription[audio_name]

                        with open(join(transcriptions_folder, model.name + "_" + prompt_function.__name__ + "_" + audio_name + ".txt"), "w") as f:     
                            f.write(transcription)

                        if normalize:
                            with open(join(transcriptions_folder, model.name + "_" + prompt_function.__name__ + "_" + audio_name + "-normalized.txt"), "w") as f: 
                                f.write(self.normalizer(transcription))
                    
                    # saving transcription as vtt
                    if audio_name in model.vtt:
                        with open(join(transcriptions_folder, model.name + "_" + prompt_function.__name__ + "_" + audio_name + ".vtt"), "w") as f:
                            f.write(model.vtt[audio_name])

                    # freeing memory
                    del audio_name
                    del audio_file
                    del audio_info
                    del prompt
                    gc.collect()

                # freeing memory
                del prompt_function
                gc.collect()

            # freeing memory
            model.unload()
            del model
            gc.collect()

        # freeing memory
        del dataset
        gc.collect()

    def free(self):
        del self.model_array
        del self.prompt_function_array
        del self.normalizer
        gc.collect()
