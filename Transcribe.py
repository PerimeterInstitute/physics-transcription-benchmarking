from os import listdir, mkdir, system
from os.path import join, isdir, basename, normpath
from prompt_functions.prompt_functions import get_description
from whisper.utils import get_writer
from whisper.normalizers import EnglishTextNormalizer
import gc, os, json

# ========================== #
# ==== Transcribe Class ==== #
# ========================== #

class Transcribe():

    def __init__(self, model, prompt_function=get_description, dataset_path="full", normalize=False):

        # LOADING SCOPE DATASETS:

        if dataset_path == "full":
            dataset_path = "./datasets/full_dataset/"

        elif dataset_path == "dev":
            dataset_path = "./datasets/dev_dataset/"

        # copy dataset to /local
        system("cp -r " + dataset_path + " /local/")
        dataset_path = join("/local", basename(normpath(dataset_path)))

        # LOADING DATASET'S ASSOCIATED JSON FILE:

        for file in listdir(dataset_path):
            if file.endswith(".json"):
                json_file = join(dataset_path, file)
                break
        dataset = json.load(open(json_file))

        # CREATING OUTPUT FOLDER:

        if not isdir("./transcriptions/"):         # make 'transcriptions' folder if it doesn't already exist
            mkdir("./transcriptions/")

        # CREATING NORMALIZER:

        normalizer = None
        if normalize:
            normalizer = EnglishTextNormalizer()

        # CREATING TRANSCRIPTIONS:

        # load model
        model.load()

        for audio in dataset:

            # getting audio variables
            audio_name = audio["audio_name"]
            audio_file = audio["audio_file"]
            audio_info = audio["audio_info"]

            # creating prompt
            prompt = prompt_function(audio_info)

            # transcribing model
            model.transcribe(audio_name, os.path.join(dataset_path, "test_data", audio_file), prompt)

            # saving transcription
            if audio_name in model.transcription:
                with open("./transcriptions/"+audio_name+".txt", "w") as f:     # as txt file
                    text = model.transcription[audio_name]
                    
                    if normalize:
                        text = normalizer(text)
                    f.write(text)
                    

            if audio_name in model.result_object:
                writer = get_writer("vtt", "./transcriptions/")                 # as vtt file
                writer(model.result_object[audio_name], audio_name+".vtt", {"max_line_width": None, "max_line_count": None, "highlight_words": None})

            # freeing memory
            del audio_name
            del audio_file
            del audio_info
            del prompt
            gc.collect()

        # freeing memory
        model.unload()
        del dataset
        gc.collect()
