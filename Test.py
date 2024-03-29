from os import listdir, mkdir
from os.path import join, isdir
from datetime import datetime
from prompt_functions.prompt_functions import get_description
import gc, inspect, jiwer, json, platform, psutil

# ==================== #
# ==== Test Class ==== #
# ==================== #

class Test():

    def __init__(self, model_array, prompt_function_array=[get_description], dataset_path="full"):

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

        # GETTING SYSTEM INFORMATION:

        uname = platform.uname()

        # RUNNING TESTS:

        if not isdir("./results/"):         # make 'results' folder if it doesn't already exist
            mkdir("./results/")

        for model in model_array:

            # load model
            model.load()

            # get extra model attributes
            model_attributes = {}
            for key, value in model.__dict__.items():
                if key[0] != '_' and key != "name":
                    model_attributes.update({key: value})

            # determine model's prompt func array
            if model.takes_prompt:
                curr_prompt_function_array = prompt_function_array
            else:
                curr_prompt_function_array = [get_description]

            for prompt_function in curr_prompt_function_array:

                current_model = {}
                test_results = {}
                test_summary = {}

                # get memory information
                mem = psutil.virtual_memory()

                # create test_details dictionary, add to current model
                test_details = {"model_info": {"class_name": model.__class__.__name__,
                                            "model_name": model.name,
                                            **model_attributes},
                                "prompt_info": {"prompt_function_name": prompt_function.__name__,
                                                "prompt_function_code": inspect.getsource(prompt_function)},
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

                for test_case in dataset:

                    current_test_results = {}
                    audio_name = test_case["audio_name"]
                    audio_file = test_case["audio_file"]
                    transcript_file = test_case["transcript_file"]
                    
                    # creating prompt
                    prompt = prompt_function(test_case["audio_info"])

                    # transcribing model
                    model.transcribe(audio_name, audio_file, prompt)
    
                    # adding load time and transcribe time to result dict
                    current_test_results.update({"start_datetime": datetime.now().strftime("%D, %H:%M:%S")})
                    if model.load_time[audio_name]:
                        current_test_results.update({"load_time": model.load_time[audio_name]})
                    if model.transcribe_time[audio_name]:
                        current_test_results.update({"transcribe_time": model.transcribe_time[audio_name]})

                    # evaluating transcription
                    with open(transcript_file, "r") as f:
                        reference = f.read()
                    accuracy_data = self.__compare(reference, model.transcription[audio_name])

                    # updating dictionaries
                    test_summary = self.__merge_dicts(test_summary, accuracy_data)
                    current_test_results.update({"accuracy_data": accuracy_data})
                    test_results.update({test_case["audio_name"]: current_test_results})

                    # freeing memory
                    del current_test_results
                    del audio_name
                    del audio_file
                    del transcript_file
                    del prompt
                    del reference
                    del accuracy_data
                    gc.collect()

                # adding test_results and test_summary to current_model dictionary 
                current_model.update({"test_results": test_results, "test_summary": self.__summarize(test_summary)})

                # creating json file for model
                json_obj = json.dumps(current_model, indent=4)
                with open("./results/" + model.name + "_" + prompt_function.__name__ + "_results.json", "w") as f:
                    f.write(json_obj)

                # freeing memory
                del current_model
                del test_results
                del test_summary
                del test_details
                del json_obj
                del mem
                gc.collect()

            # freeing memory
            model.unload()
            del model_attributes
            gc.collect()

        # freeing memory
        del dataset
        del uname
        gc.collect()

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
    