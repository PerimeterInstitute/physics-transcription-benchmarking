from os import getcwd
from os.path import join
from shutil import rmtree
from helper_functions.prompt_functions import no_prompt
from helper_functions.test_transcribe_help import load_dataset, make_output_folders
from whisper.normalizers import EnglishTextNormalizer
import gc

# ========================== #
# ==== Transcribe Class ==== #
# ========================== #

class Transcribe():

    def __init__(self, model_array, prompt_function_array=[no_prompt], output_dir=getcwd()):
        self.model_array = model_array
        self.prompt_function_array = prompt_function_array
        self.normalizer = EnglishTextNormalizer()
        self.output_dir = output_dir
        self.most_recent_run = None
        self.transcriptions_folder = None
        self.__temp_folder = None

    def run(self, run_name, dataset_path, normalize=False):
        self.most_recent_run = run_name

        # CREATING OUTPUT FOLDERS:

        _, self.transcriptions_folder, self.__temp_folder = make_output_folders(output_dir=self.output_dir, 
                                                                                run_name=run_name, 
                                                                                dirs_to_make=[False, True, True])

        # LOADING DATASET:

        dataset = load_dataset(dataset_path)
        if dataset == None:
            print("Invalid dataset path provided: '"+dataset_path+"'")
            return

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
                    model.transcribe(audio_name, join(dataset_path, "test_data", audio_file), prompt, self.__temp_folder)

                    # saving transcription as txt
                    if audio_name in model.transcription:   
                        transcription = model.transcription[audio_name]

                        with open(join(self.transcriptions_folder, model.name + "_" + prompt_function.__name__ + "_" + audio_name + ".txt"), "w") as f:     
                            f.write(transcription)

                        if normalize:
                            with open(join(self.transcriptions_folder, model.name + "_" + prompt_function.__name__ + "_" + audio_name + "-normalized.txt"), "w") as f: 
                                f.write(self.normalizer(transcription))
                    
                    # saving transcription as vtt
                    if audio_name in model.vtt:
                        with open(join(self.transcriptions_folder, model.name + "_" + prompt_function.__name__ + "_" + audio_name + ".vtt"), "w") as f:
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
        rmtree(self.__temp_folder)
        del self.__temp_folder
        del dataset
        gc.collect()

    def free(self):
        del self.model_array
        del self.prompt_function_array
        del self.most_recent_run
        del self.normalizer
        del self.transcriptions_folder
        gc.collect()
