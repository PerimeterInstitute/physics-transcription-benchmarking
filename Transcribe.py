from os import listdir, mkdir, system, getcwd
from os.path import join, isdir, basename, normpath
from json import load
from gc import collect
from prompt_functions.prompt_functions import no_prompt
from whisper.normalizers import EnglishTextNormalizer

# ========================== #
# ==== Transcribe Class ==== #
# ========================== #

class Transcribe():

    def __init__(self, model, prompt_function=no_prompt, dataset_path="full", normalize=False):

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
        dataset = load(open(json_file))

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
            model.transcribe(audio_name, join(dataset_path, "test_data", audio_file), prompt)

            # saving transcription as txt
            if audio_name in model.transcription:                               
                with open("./transcriptions/"+audio_name+".txt", "w") as f:     # TODO: use getcwd() instead of ./
                    text = model.transcription[audio_name]
                    if normalize:
                        text = normalizer(text)
                    f.write(text)
            
            # saving transcription as vtt
            if audio_name in model.vtt:
                with open("./transcriptions/"+audio_name+".vtt", "w") as f:     # TODO: use getcwd() instead of ./
                    f.write(model.vtt[audio_name])

            # freeing memory
            del audio_name
            del audio_file
            del audio_info
            del prompt
            collect()

        # freeing memory
        model.unload()
        del dataset
        collect()
