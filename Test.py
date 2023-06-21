from os import listdir
from os.path import join
import json, jiwer

class Test():

    results = {}

    def __init__(self, model_array, dataset_path="full"):

        # LOADING SCOPE DATASETS:

        if dataset_path == "full":
            dataset_path = "./datasets/full_dataset/"

        elif dataset_path == "dev":
            dataset_path = "./datasets/dev_dataset/"

        # LOADING DATASET'S JSON FILE:

        for file in listdir(dataset_path):
            if file.endswith(".json"):
                json_file = join(dataset_path, file)
                break
        dataset = json.load(open(json_file))

        # RUNNING TESTS:

        for model in model_array:
            current_model = {}

            for test_case in dataset:
                current_test = {}

                # TODO: download these files rather than keeping them in directory
                audio_name = test_case["audio_filename"]
                transcript_name = test_case["transcript_filename"]
                audio_file = join(dataset_path, "test_data/", audio_name)
                transcript_file = join(dataset_path, "test_data/", transcript_name)
                
                # creating prompt
                prompt = self.__load_prompt(test_case["audio_info"])

                # transcribing model
                model.transcribe(audio_file, prompt)

                # adding load time and transcribe time to result dict
                if model.load_time[audio_name]:
                    current_test.update({"load_time": model.load_time[audio_name]})
                if model.transcribe_time[audio_name]:
                    current_test.update({"transcribe_time": model.transcribe_time[audio_name]})

                # evaluating transcription
                reference = open(transcript_file, "r").read()
                current_test.update({"test_results": self.__compare(reference, model.transcription[audio_name])})

                current_model.update({test_case["test_name"]: current_test})

            self.results.update({model.name: current_model})

    def __load_prompt(self, json_obj):

        prompt = []

        # CREATING PROMPT ARRAY:

        for key in json_obj:
            if key == "title" or key == "description":
                prompt.append(json_obj[key])

            elif key == "keywords":
                for keyword in json_obj[key]:
                    prompt.append(keyword)

            elif key == "speakers":
                for speaker in json_obj[key]:
                    name = speaker["name"]
                    institution = speaker["institution"]

                    prompt.append(name)
                    
                    if institution not in prompt:
                        prompt.append(institution)

        # CREATING PROMPT STRING:

        prompt = list(map(str.strip, prompt))
        while "" in prompt:
            prompt.remove("")

        return None if len(prompt) == 0 else " ".join(prompt)

    def __compare(self, reference, hypothesis):

        current_dataset = {}

        # COMPARING INPUT:

        word_output = jiwer.process_words(reference, hypothesis)
        char_output = jiwer.process_characters(reference, hypothesis)

        # CREATING JSON:

        current_dataset.update({"word_error_rate": word_output.wer})
        current_dataset.update({"match_error_rate": word_output.mer})
        current_dataset.update({"word_information_lost": word_output.wil})
        current_dataset.update({"word_information_preserved": word_output.wip})
        current_dataset.update({"character_error_rate": char_output.cer})

        return current_dataset
    