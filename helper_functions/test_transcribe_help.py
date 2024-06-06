from os import listdir, system
from os.path import join, normpath, basename
from datetime import datetime, timedelta
import jiwer, json, re

# ========================================== #
# ==== Test/Transcribe Helper Functions ==== #
# ========================================== #

'''
NAME: load_dataset()

FUNCTION: Loads dataset given dataset path. Returns None if dataset
          cannot be found/loaded.
'''

def load_dataset(dataset_path):

    try:
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

    except:
        return None

'''
NAME: compare()

FUNCTION: Compares two texts and returns various accuracy data.
'''

def compare(reference, hypothesis):

    current_dataset = {}

    # comparing transcriptions
    word_output = jiwer.process_words(reference, hypothesis)
    char_output = jiwer.process_characters(reference, hypothesis)
    phrase_repeat_diff = countRepeatedPhrases(hypothesis) - countRepeatedPhrases(reference)

    # creating results dictionary
    current_dataset.update({"word_error_rate": word_output.wer})
    current_dataset.update({"match_error_rate": word_output.mer})
    current_dataset.update({"character_error_rate": char_output.cer})
    current_dataset.update({"word_information_lost": word_output.wil})
    current_dataset.update({"word_information_preserved": word_output.wip})
    current_dataset.update({"phrase_repeat_diff": phrase_repeat_diff})

    return current_dataset

'''
NAME: countRepeatedPhrases()

FUNCTION: Returns number of repeated phrases. 
          In this function, a repeated phrase is defined as a valid word or
          phrase that has already occured before, seperated only by whitespace.

EXAMPLE:
Input --> "I like pizza I like pizza I like pizza "
          "I like pizza hello I like pizza "
          "hello I like pizza I like pizza hello "
          "hello hello hello I like pizza I like pizza "

Output --> 2
           0
           1
           3
'''

def countRepeatedPhrases(text):
    regex = re.compile(r'\s(.+\s+)\1', flags=re.I)     # slightly altered from https://stackoverflow.com/questions/64529827/find-repeated-sentences-within-text
    return __countRepeatedPhrasesRecursive(regex.split(text), regex.findall(text), regex)

'''
NAME: __countRepeatedPhrasesRecursive()

FUNCTION: Internal recursive function that helps countRepeatedPhrases().
'''

def __countRepeatedPhrasesRecursive(substrings, repeats, regex):
    if len(substrings) == 1:          # i.e. no repeats found
        return 0
    
    num = len(repeats)

    # CASE 1: Repeats are present in already confirmed repeats
    for text in repeats:
        text = " "+text+" "         # ensures deeper repeats are found by regex
        num = num + 2*__countRepeatedPhrasesRecursive(regex.split(text), regex.findall(text), regex)        # '2*' is added since any repeats found in previously confirmed repeat has occurred twice!

    # CASE 2: Repeat is present in a substring following an already confirmed repeat
    for idx in range(0, len(substrings)):
        substring = substrings[idx]
        if substring in repeats:            # if substring has already been confirmed as a repeat, check the start of the next substring for another repeat
            if substrings[idx+1].strip().startswith(substring):
                num += 1

    # CASE 3: Repeats are present in remaining substrings
    new_list = [x for x in substrings if x not in repeats]            # 'substrings' array without any elements that are in 'repeats' array
    for text in new_list:
        text = " "+text+" "         # ensures deeper repeats are found by regex
        num = num + __countRepeatedPhrasesRecursive(regex.split(text), regex.findall(text), regex)

    return num

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
