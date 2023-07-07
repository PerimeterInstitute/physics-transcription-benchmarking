from os import listdir, mkdir
from os.path import join, isdir
from datetime import datetime
import platform, psutil
import json, jiwer

class Test():

    results = {}

    def __init__(self, model_array, dataset_path="full"):

        # LOADING SCOPE DATASETS:

        if dataset_path == "full":
            dataset_path = "./datasets/full_dataset/"

        elif dataset_path == "dev":
            dataset_path = "./datasets/dev_dataset/"

        # LOADING DATASET'S ASSOCIATED JSON FILE:

        for file in listdir(dataset_path):
            if file.endswith(".json"):
                json_file = join(dataset_path, file)
                break
        dataset = json.load(open(json_file))

        # RUNNING TESTS:

        if not isdir("./results/"):         # make 'results' folder if it doesn't already exist
            mkdir("./results/")

        # for get_prompt in prompt_funcs:
        for model in model_array:

            current_model = {}

            # load model
            model.load()

            # set variables needed to create test_details dictionary
            uname = platform.uname()
            mem = psutil.virtual_memory()
            model_attributes = {}
            for key, value in model.__dict__.items():
                if key[0] != '_' and key != "name":
                    model_attributes.update({key: value})

            # create test_details dictionary, add to current model
            test_details = {"model_info": {"class_name": model.__class__.__name__,
                                           "model_name": model.name,
                                           **model_attributes},
                            "system_info": {"system": uname.system,
                                            "release": uname.release,
                                            "version": uname.version,
                                            "machine": uname.machine,
                                            "processor": uname.processor},
                            "cpu_info": {"physical_cores": psutil.cpu_count(logical=False),
                                         "total_cores": psutil.cpu_count(logical=True)},
                            "memory_info": {"total_memory": mem.total,
                                            "available_memory": mem.available,
                                            "used_memory": mem.used}}
            current_model.update({"test_details": test_details})

            test_results = {}
            test_summary = {}
            for test_case in dataset:

                current_test_results = {}
                audio_name = test_case["audio_filename"]
                transcript_name = test_case["transcript_filename"]
                audio_file = join(dataset_path, "test_data/", audio_name)
                transcript_file = join(dataset_path, "test_data/", transcript_name)
                
                # creating prompt
                prompt = self.__load_prompt(test_case["audio_info"])

                # transcribing model
                model.transcribe(audio_file, prompt)
   
                # adding load time and transcribe time to result dict
                current_test_results.update({"start_datetime": datetime.now().strftime("%D, %H:%M:%S")})
                if model.load_time[audio_name]:
                    current_test_results.update({"load_time": model.load_time[audio_name]})
                if model.transcribe_time[audio_name]:
                    current_test_results.update({"transcribe_time": model.transcribe_time[audio_name]})

                # evaluating transcription
                reference = open(transcript_file, "r").read()
                accuracy_data = self.__compare(reference, model.transcription[audio_name])

                # update dictionaries
                test_summary = self.__merge_dicts(test_summary, accuracy_data)
                current_test_results.update({"accuracy_data": accuracy_data})
                test_results.update({test_case["test_name"]: current_test_results})

            # add test_results and test_summary to current_model dictionary 
            current_model.update({"test_results": test_results, "test_summary": self.__summarize(test_summary)})

            # create json file for model
            json_obj = json.dumps(current_model, indent=4)
            with open("./results/" + model.name + "_results.json", "w") as f:
                f.write(json_obj)
            f.close()

            # add model results to 'results' dictionary
            self.results.update({model.name: current_model})

            # unload model
            model.unload()

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
        current_dataset.update({"character_error_rate": char_output.cer})
        current_dataset.update({"word_information_lost": word_output.wil})
        current_dataset.update({"word_information_preserved": word_output.wip})

        return current_dataset
    
    def __merge_dicts(self, dict1, dict2):

        merged_dict = {**dict2, **dict1}        # this order ensures values in dict1 take priority
        for key, value in merged_dict.items():
            if key in dict1 and key in dict2:
                if isinstance(value, list):
                    value.append(dict2[key])
                    merged_dict[key] = value
                else:
                    merged_dict[key] = [value, dict2[key]]

        return merged_dict
    
    def __summarize(self, accuracy_data):
        summarized_data = {}
        for key, value in accuracy_data.items():
            if isinstance(value, list):
                summarized_data.update({key: sum(value)/len(value)})
            else:
                summarized_data.update({key: value})
        return summarized_data
    