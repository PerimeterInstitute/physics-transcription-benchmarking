from os import listdir, mkdir
from os.path import join, isdir
from datetime import datetime, timedelta
from prompt_functions.prompt_functions import get_description
import gc, inspect, jiwer, json, platform, psutil
from whisper.normalizers import EnglishTextNormalizer

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

        # CREATING NORMALIZER CLASS:

        normalizer = EnglishTextNormalizer()

        # RUNNING TESTS:

        if not isdir("./results/"):         # make 'results' folder if it doesn't already exist
            mkdir("./results/")

        for model in model_array:

            all_transcribe_times = []

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
                                            **model_attributes,
                                            "load_time": model.load_time},
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
                # TODO: add GPU details?

                current_model.update({"test_details": test_details})

                for test_case in dataset:

                    current_test_results = {}
                    audio_name = test_case["audio_name"]
                    audio_file = test_case["audio_file"]
                    transcript_file = test_case["transcript_file"]
                    
                    # creating prompt
                    prompt = prompt_function(test_case["audio_info"])

                    # transcribing model
                    model.transcribe(audio_name, join(dataset_path, "test_data", audio_file), prompt)
    
                    # adding current date and transcribe time to result dict
                    current_test_results.update({"start_datetime": datetime.now().strftime("%D, %H:%M:%S")})
                    if model.transcribe_time[audio_name]:
                        current_transcribe_time = model.transcribe_time[audio_name]

                        # add to current test dict
                        current_test_results.update({"transcribe_time": current_transcribe_time})

                        # convert string to timedelta and add to array
                        converted_time = datetime.strptime(current_transcribe_time,"%H:%M:%S.%f")
                        all_transcribe_times.append(timedelta(hours=converted_time.hour, minutes=converted_time.minute, seconds=converted_time.second, microseconds=converted_time.microsecond))

                    # evaluating transcription
                    with open(join(dataset_path, "test_data", transcript_file), "r") as f:
                        reference = f.read()
                    accuracy_data = self.__compare(normalizer(reference), normalizer(model.transcription[audio_name]))

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

                # determine average transcribe time and convert to a string
                average_transcribe_time = str(self.__add_times(all_transcribe_times) / len(all_transcribe_times))

                # finalizing test summary dict
                test_summary = self.__summarize(test_summary)
                test_summary["average_transcribe_time"] = average_transcribe_time

                # adding test_results and test_summary to current_model dictionary 
                current_model.update({"test_results": test_results, "test_summary": test_summary})

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
                del average_transcribe_time
                gc.collect()

            # freeing memory
            model.unload()
            del all_transcribe_times
            del model_attributes
            gc.collect()

        # freeing memory
        del dataset
        del uname
        del normalizer
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
    
    def __add_times(self, timedelta_arr):           # sum() function did not work for timedelta objects, so this function is used instead
        total_time = timedelta(0)
        for time in timedelta_arr:
            total_time += time
        return total_time
