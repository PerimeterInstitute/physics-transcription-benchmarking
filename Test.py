from os import listdir
from os.path import basename
import json, jiwer

# DATASETS = "./datasets/"
DATASETS = "./dev_datasets/"

class Test():

    def __init__(self, model_arr):

        self.results = {}

        for model in model_arr:
            currentModel = {}

            for dataset in listdir(DATASETS):
                currentTest = {}

                json_file = DATASETS + dataset + "/" + dataset + ".json"
                json_obj = json.load(open(json_file))

                # TODO: download these files rather than keeping them in directory
                audio_name = json_obj["audio_name"]
                audio_file = DATASETS + dataset + "/" + audio_name
                transcript_file = DATASETS + dataset + "/" + json_obj["transcript_name"]
                
                # creating prompt
                prompt = self.loadPrompt(json_obj)

                # transcribing model
                model.transcribe(audio_file, prompt)

                # adding load time and transcribe time to JSON
                if model.load_time[audio_name]:
                    currentTest.update({"load_time": model.load_time[audio_name]})
                if model.transcribe_time[audio_name]:
                    currentTest.update({"transcribe_time": model.transcribe_time[audio_name]})

                # evaluating transcription
                reference = open(transcript_file, "r").read()
                currentTest.update({"test_results": self.compare(reference, model.transcription[audio_name])})

                currentModel.update({dataset: currentTest})

            self.results.update({model.name: currentModel})

    def loadPrompt(self, json_obj):

        prompt = ""

        # CREATING PROMPT:

        for key in json_obj:

            if key == "title":
                prompt += " " + json_obj[key].strip()

            elif key == "description":
                prompt += " " + json_obj[key].strip()

            elif key == "keywords":
                # TODO: decide on way to add keywords to prompt (figure out keyword formatting in JSON first)
                pass

            elif key == "speakers":
                for speaker in json_obj[key].values():                   # TODO: check for duplicate speakers/institutions
                    prompt += " " + speaker["name"].strip()
                    prompt += " " + speaker["institution"].strip()

        return None if prompt == "" else prompt.strip()

    def compare(self, reference, hypothesis):

        currentDataset = {}

        # COMPARING INPUT:

        word_output = jiwer.process_words(reference, hypothesis)
        char_output = jiwer.process_characters(reference, hypothesis)

        # CREATING JSON:

        currentDataset.update({"word_error_rate": word_output.wer})
        currentDataset.update({"match_error_rate": word_output.mer})
        currentDataset.update({"word_information_lost": word_output.wil})
        currentDataset.update({"word_information_preserved": word_output.wip})
        currentDataset.update({"character_error_rate": char_output.cer})

        return currentDataset
    