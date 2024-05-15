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

    def __init__(self, model_array, prompt_function_array=[get_description], dataset_path="full", run_num=1):

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

        # CREATING NORMALIZER:

        normalizer = EnglishTextNormalizer()

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

                # add test details to current model
                current_model.update({"test_details": test_details})

                for test_case in dataset:

                    local_test_results = {}
                    local_summary = {}
                    audio_name = test_case["audio_name"]
                    audio_file = test_case["audio_file"]
                    transcript_file = test_case["transcript_file"]

                    for i in range(run_num):

                        local_rerun_test_results = {}
                    
                        # creating prompt
                        prompt = prompt_function(test_case["audio_info"])

                        # transcribing model
                        model.transcribe(audio_name, join(dataset_path, "test_data", audio_file), prompt)
        
                        # adding current date and transcribe time to result dict
                        local_rerun_test_results.update({"start_datetime": datetime.now().strftime("%D, %H:%M:%S")})
                        if model.transcribe_time[audio_name]:
                            current_transcribe_time = model.transcribe_time[audio_name]

                            # add to current test dict
                            local_rerun_test_results.update({"transcribe_time": current_transcribe_time})

                            # convert string to timedelta and add to array
                            converted_time = datetime.strptime(current_transcribe_time,"%H:%M:%S.%f")
                            transcribe_time = timedelta(hours=converted_time.hour, minutes=converted_time.minute, seconds=converted_time.second, microseconds=converted_time.microsecond)

                        # evaluating transcription
                        with open(join(dataset_path, "test_data", transcript_file), "r") as f:
                            reference = f.read()
                        accuracy_data = self.__compare(normalizer(reference), normalizer(model.transcription[audio_name]))
                        
                        # updating dictionaries
                        run_data = {"transcribe_time": transcribe_time, **accuracy_data}
                        local_summary = self.__merge_dicts(local_summary, run_data)
                        test_summary = self.__merge_dicts(test_summary, run_data)
                        local_rerun_test_results.update(accuracy_data)
                        local_test_results.update({"run_"+str(i): local_rerun_test_results})

                        # freeing memory
                        del local_rerun_test_results
                        del prompt
                        del reference
                        del accuracy_data

                    # adding local summary to local test results dictionary
                    local_test_results.update({"summary": self.__summarize(local_summary)})

                    # updating test result dictionary
                    test_results.update({test_case["audio_name"]: local_test_results})

                    # freeing memory
                    del local_test_results
                    del local_summary
                    del audio_name
                    del audio_file
                    del transcript_file
                    gc.collect()

                # finalizing test summary dictionary
                test_summary = {"transcriptions_per_audio": run_num, **self.__summarize(test_summary)}

                # adding test_results and test_summary to model dictionary 
                current_model.update({"test_results": test_results, "test_summary": test_summary})

                # creating json file for model
                json_obj = json.dumps(current_model, indent=4)
                with open("./results/" + model.name + "_" + prompt_function.__name__ + "_results.json", "w") as f:
                    f.write(json_obj)

                # freeing memory
                del current_model
                del test_results
                del test_summary
                del mem
                del test_details
                del json_obj
                gc.collect()

            # freeing memory
            model.unload()
            # del model ?
            del model_attributes
            gc.collect()

        # freeing memory
        del dataset
        del uname
        del normalizer
        gc.collect()

    '''
    NAME: __compare()

    FUNCTION: Compares two texts and returns various accuracy data.
    '''

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
    
    '''
    NAME: __merge_dicts()

    FUNCTION: If there are repeated keys in given dictionaries, merge the dictionaries 
              such that all values associated with repeated keys are turned into one 
              key-value pair where the value is a list of all unique values.
              Leaves unique keys the same.

    EXAMPLE:
    Input -->       dict1: {
                                "greeting": "hello", 
                                "fruit": "apple"
                            }
                    dict2: {
                                "greeting": "hi", 
                                "vegetable": "carrot"
                            }

    Output--> merged_dict: {
                                "greeting": ["hello", "hi"],
                                "fruit": "apple",
                                "vegetable": "carrot"
                           }
    '''

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
    
    '''
    NAME: __summarize()

    FUNCTION: If any values are lists, take the average of all values in the list
              and replace the orginal list value with a single average value.
              Otherwise leave the key-value pairs as they are.

    EXAMPLE:
    Input -->            dict: {
                                "value1": 3, 
                                "value2": [1, 2, 8, 9]
                               }

    Output--> summarized_dict: {
                                "value1": 3,
                                "value2": 5
                               }
    '''
    
    def __summarize(self, accuracy_data):
        summarized_data = {}
        for key, value in accuracy_data.items():

            if isinstance(value, list):                     # if list
                if isinstance(value[0], timedelta):         # if timedelta list
                    summarized_data.update({key: str(self.__sum_timedeltas(value)/len(value))})
                else:
                    summarized_data.update({key: sum(value)/len(value)})
            else:                                           # if single value
                if isinstance(value, timedelta):            # if timedelta value
                    summarized_data.update({key: str(value)})
                else:
                    summarized_data.update({key: value})

        return summarized_data
    
    '''
    NAME: __sum_timedeltas()

    FUNCTION: Find the sum of a list of timedelta objects.
    '''

    def __sum_timedeltas(self, timedelta_arr):           # sum() function did not work for timedelta objects, so this function is used instead
        total_time = timedelta(0)
        for time in timedelta_arr:
            total_time += time
        return total_time
