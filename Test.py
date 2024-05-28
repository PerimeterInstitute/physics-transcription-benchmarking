from os import listdir, mkdir, system
from os.path import join, isdir, normpath, basename
from datetime import datetime, timedelta
from prompt_functions.prompt_functions import no_prompt
import gc, inspect, jiwer, json, platform, psutil, copy
from whisper.normalizers import EnglishTextNormalizer

# ==================== #
# ==== Test Class ==== #
# ==================== #

class Test():

    def __init__(self, model_array, prompt_function_array=[no_prompt], dataset_path="full", run_num=1, save_transcription=False):

        # LOADING DATASET:
        
        dataset = load_dataset(dataset_path)

        # GETTING SYSTEM INFORMATION:

        uname = platform.uname()

        # CREATING NORMALIZER:

        normalizer = EnglishTextNormalizer()

        # RUNNING TESTS:

        for model in model_array:

            # load model
            model.load()

            # get additional model attributes
            model_attributes = {}
            for key, value in model.__dict__.items():
                if key[0] != '_' and key != "name":
                    model_attributes.update({key: value})

            for prompt_function in prompt_function_array:

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

                        if save_transcription:
                            if not isdir("./transcriptions/"):         # make 'transcriptions' folder if it doesn't already exist
                                mkdir("./transcriptions/")
                            transcription = model.transcription[audio_name]
                            with open("./transcriptions/" + model.name + "_" + prompt_function.__name__ + "_" + audio_name + ".txt", "w") as f:
                                f.write(transcription)
                            with open("./transcriptions/" + model.name + "_" + prompt_function.__name__ + "_" + audio_name + "-normalized.txt", "w") as f:
                                f.write(normalizer(transcription))
        
                        # adding current date and transcribe time to result dict
                        local_rerun_test_results.update({"start_datetime": datetime.now().strftime("%D, %H:%M:%S")})
                        if model.transcribe_time[audio_name]:
                            transcribe_time = model.transcribe_time[audio_name]

                            # add to current test dict
                            local_rerun_test_results.update({"transcribe_time": transcribe_time})

                            # convert string to timedelta
                            transcribe_time = string_to_timedelta(transcribe_time)

                        # evaluating transcription
                        with open(join(dataset_path, "test_data", transcript_file), "r") as f:
                            reference = f.read()
                        accuracy_data = compare(normalizer(reference), normalizer(model.transcription[audio_name]))
                        
                        # updating dictionaries
                        run_data = {"transcribe_time": transcribe_time, **accuracy_data}
                        local_summary = merge_dicts(local_summary, run_data)
                        test_summary = merge_dicts(test_summary, run_data)
                        local_rerun_test_results.update(accuracy_data)
                        local_test_results.update({"run_"+str(i): local_rerun_test_results})

                        # freeing memory
                        del local_rerun_test_results
                        del prompt
                        del reference
                        del accuracy_data

                    # adding local summary to local test results dictionary
                    local_test_results.update({"summary": summarize(local_summary)})

                    # updating test result dictionary
                    test_results.update({test_case["audio_name"]: local_test_results})

                    # freeing memory
                    del local_test_results
                    del local_summary
                    del audio_name
                    del audio_file
                    del transcript_file
                    del test_case
                    gc.collect()

                # finalizing test summary dictionary
                test_summary = {"transcriptions_per_audio": run_num, **summarize(test_summary)}

                # adding test_results and test_summary to model dictionary 
                current_model.update({"test_results": test_results, "test_summary": test_summary})

                # creating json file for model
                json_obj = json.dumps(current_model, indent=4)

                if not isdir("./results/"):         # make 'results' folder if it doesn't already exist
                    mkdir("./results/")
                with open("./results/" + model.name + "_" + prompt_function.__name__ + "_results.json", "w") as f:
                    f.write(json_obj)

                # freeing memory
                del current_model
                del test_results
                del test_summary
                del mem
                del test_details
                del json_obj
                del prompt_function
                gc.collect()

            # freeing memory
            model.unload()
            del model_attributes
            del model
            gc.collect()

        # freeing memory
        del dataset
        del uname
        del normalizer
        gc.collect()

# ================================= #
# ==== AddToExistingTest Class ==== #
# ================================= #

'''
Notes: This class will update the given json test output file.
       If no output file name is provided, it will likely 
       overwrite the provided test file.

       The 'test_details' section of the provided test file will 
       be overwritten with data from the provided transcription 
       model (meaning information in the 'test_details' section 
       of the previous run will be lost).
'''
    
class AddToExistingTest():

    def __init__(self, existing_test_json, model, prompt_function=no_prompt, dataset_path="full", run_num=1, output_file_name=None):

        # LOADING PROVIDED MODEL:

        # load model
        model.load()

        # get additional model attributes
        model_attributes = {}
        for key, value in model.__dict__.items():
            if key[0] != '_' and key != "name":
                model_attributes.update({key: value})

        # LOADING EXISTING TEST DATA:

        existing_test_file = open(existing_test_json)
        existing_test_obj = json.load(existing_test_file)
        existing_test_file.close()

        existing_test_details = existing_test_obj["test_details"]
        existing_test_results = existing_test_obj["test_results"]

        # CONFIRMING IF PROPER MODEL AND PROMPT FUNCTION:

        existing_model_info = existing_test_details["model_info"]
        provided_model_info = {"class_name": model.__class__.__name__,
                               "model_name": model.name,
                               **model_attributes,
                               "load_time": model.load_time}
        existing_prompt_info = existing_test_details["prompt_info"]
        provided_prompt_info = {"prompt_function_name": prompt_function.__name__,
                                "prompt_function_code": inspect.getsource(prompt_function)}

        for parameter in existing_model_info:
            if parameter != "model_name" and parameter != "load_time":
                if parameter not in provided_model_info or existing_model_info[parameter] != provided_model_info[parameter]:
                    self.__discrepency_error(parameter, existing_model_info, provided_model_info)
                    
        for parameter in existing_prompt_info:
            if parameter not in provided_prompt_info or existing_prompt_info[parameter] != provided_prompt_info[parameter]:
                self.__discrepency_error(parameter, existing_prompt_info, provided_prompt_info)
                
        # LOADING DATASET:

        dataset = load_dataset(dataset_path)
    
        # GETTING PROVIDED MODEL STATS:

        uname = platform.uname()
        mem = psutil.virtual_memory()
        provided_test_details = {"model_info": provided_model_info,
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

        # CREATING NORMALIZER:

        normalizer = EnglishTextNormalizer()

        # RUNNING TESTS:

        current_model = {"test_details": provided_test_details}
        test_results = {}
        test_summary = {}
        
        for test_case in dataset:

            local_test_results = {}
            local_summary = {}
            num_prev_runs = 0
            audio_name = test_case["audio_name"]
            audio_file = test_case["audio_file"]
            transcript_file = test_case["transcript_file"]

            # updating starting param values if this audio already has existing results
            if audio_name in existing_test_results:

                existing_audio_name = existing_test_results[audio_name]
                num_prev_runs = len(existing_audio_name)-1

                for run in existing_audio_name:

                    if run != "summary":
                        # update local test results
                        local_test_results.update({run: existing_audio_name[run]}) 

                        # deep copy and alter existing test data as needed
                        run_copy = copy.deepcopy(existing_audio_name[run])
                        del run_copy["start_datetime"]
                        run_copy["transcribe_time"] = string_to_timedelta(run_copy["transcribe_time"])

                        # add altered existing test data to summary dicts
                        local_summary = merge_dicts(local_summary, run_copy)
                        test_summary = merge_dicts(test_summary, run_copy)
                          
            for i in range(num_prev_runs, run_num + num_prev_runs):

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
                    transcribe_time = string_to_timedelta(current_transcribe_time)

                # evaluating transcription
                with open(join(dataset_path, "test_data", transcript_file), "r") as f:
                    reference = f.read()
                accuracy_data = compare(normalizer(reference), normalizer(model.transcription[audio_name]))
                
                # updating dictionaries
                run_data = {"transcribe_time": transcribe_time, **accuracy_data}
                local_summary = merge_dicts(local_summary, run_data)
                test_summary = merge_dicts(test_summary, run_data)
                local_rerun_test_results.update(accuracy_data)
                local_test_results.update({"run_"+str(i): local_rerun_test_results})

                # freeing memory
                del local_rerun_test_results
                del prompt
                del reference
                del accuracy_data

            # adding local summary to local test results dictionary
            local_test_results.update({"summary": summarize(local_summary)})

            # updating test result dictionary
            test_results.update({test_case["audio_name"]: local_test_results})
            
            # freeing memory
            del local_test_results
            del local_summary
            del audio_name
            del audio_file
            del transcript_file
            del test_case
            gc.collect()

        # finalizing test summary dictionary
        test_summary = {"transcriptions_per_audio": run_num + num_prev_runs, **summarize(test_summary)}

        # updating json
        current_model.update({"test_results": test_results, "test_summary": test_summary})
        json_obj = json.dumps(current_model, indent=4)

        if not isdir("./results/"):         # make 'results' folder if it doesn't already exist
            mkdir("./results/")
        if output_file_name != None:
            with open(join("./results/", output_file_name), "w") as f:
                f.write(json_obj)
        else:
            with open(join("./results/", existing_model_info["model_name"] + "_" + prompt_function.__name__ + "_results.json"), "w") as f:
                f.write(json_obj)

        # freeing model
        model.unload()
        del model
        gc.collect()

    def __discrepency_error(self, parameter, existing_model_info, provided_model_info, isModel):
        model.unload()
        del model
        gc.collect()
        if isModel:
            raise Exception("Model parameter, '"+parameter+"', between test model (model used to create existing test) and provided model is different.\n\
                            Test model value: "+existing_model_info[parameter]+"\n\
                            Provided model value: "+provided_model_info[parameter])
        else:
            raise Exception("Prompt parameter, '"+parameter+"', between test prompt (prompt used to create existing test) and provided prompt is different.\n\
                            Test prompt value: "+existing_model_info[parameter]+"\n\
                            Provided prompt value: "+provided_model_info[parameter])
            
# ========================== #
# ==== Helper Functions ==== #
# ========================== #

'''
NAME: load_dataset()

FUNCTION: Loads dataset given dataset path.
'''

def load_dataset(dataset_path):

    # loading premade dataset paths
    if dataset_path == "full":
        dataset_path = "./datasets/full_dataset/"       # TODO: use getcwd(), check if the dir exists and raise exception if it doesnt

    elif dataset_path == "dev":
        dataset_path = "./datasets/dev_dataset/"       # TODO: use getcwd(), check if the dir exists and raise exception if it doesnt

    # copy dataset to /local --> for when running on hpc
    system("cp -r " + dataset_path + " /local/")
    dataset_path = join("/local", basename(normpath(dataset_path)))

    # loading dataset json file
    for file in listdir(dataset_path):
        if file.endswith(".json"):
            json_file_path = join(dataset_path, file)
            break
        
    json_file = open(json_file_path)
    dataset = json.load(json_file)
    json_file.close()

    return dataset

'''
NAME: compare()

FUNCTION: Compares two texts and returns various accuracy data.
'''

def compare(reference, hypothesis):

    current_dataset = {}

    # comparing transcriptions
    word_output = jiwer.process_words(reference, hypothesis)
    char_output = jiwer.process_characters(reference, hypothesis)

    # creating results dictionary
    current_dataset.update({"word_error_rate": word_output.wer})
    current_dataset.update({"match_error_rate": word_output.mer})
    current_dataset.update({"character_error_rate": char_output.cer})
    current_dataset.update({"word_information_lost": word_output.wil})
    current_dataset.update({"word_information_preserved": word_output.wip})

    return current_dataset

'''
NAME: merge_dicts()

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

def merge_dicts(dict1, dict2):

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
NAME: summarize()

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

def summarize(accuracy_data):
    summarized_data = {}
    for key, value in accuracy_data.items():

        if isinstance(value, list):                     # if list
            if isinstance(value[0], timedelta):         # if timedelta list
                summarized_data.update({key: str(sum_timedeltas(value)/len(value))})
            else:
                summarized_data.update({key: sum(value)/len(value)})
        else:                                           # if single value
            if isinstance(value, timedelta):            # if timedelta value
                summarized_data.update({key: str(value)})
            else:
                summarized_data.update({key: value})

    return summarized_data

'''
NAME: sum_timedeltas()

FUNCTION: Find the sum of a list of timedelta objects.
'''

def sum_timedeltas(timedelta_arr):           # sum() function did not work for timedelta objects, so this function is used instead
    total_time = timedelta(0)
    for time in timedelta_arr:
        total_time += time
    return total_time

'''
NAME: string_to_timedelta()

FUNCTION: Convert a string value to a timedelta object.
'''

def string_to_timedelta(timeStr):
    t = datetime.strptime(timeStr,"%H:%M:%S.%f")
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
