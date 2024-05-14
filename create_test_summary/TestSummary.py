from os import listdir
from os.path import join, dirname, realpath
from datetime import datetime, timedelta
from string import Template
import json

def create_test_summary_html(results_folder, filename="test_summary.html"):

    # ensuring proper file extension
    if not filename.lower().endswith(".html"):
        filename = filename + ".html"

    # define table and row templates
    with open(join(dirname(realpath(__file__)), "TestSummaryTemplate.html"), "r") as template_file:
        table_template = Template(template_file.read())

    table_row_template = Template('\
                            <tr class="border-b dark:border-neutral-500"> \n\
                                <td class="whitespace-nowrap px-6 py-4 font-medium">$model_class</td> \n\
                                <td class="whitespace-nowrap px-6 py-4 font-medium">$prompt_function</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$avg_transcribe_time</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$wer</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$mer</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$cer</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$wil</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$wip</td> \n\
                            </tr> \n')
    
    accuracy_graph_template = Template('\
                { \n\
                    label: "$model_title", \n\
                    data: [$wer, $mer, $cer, $wil, $wip] \n\
                },\n')
    
    time_graph_template = Template('\
                { \n\
                    label: "$model_title", \n\
                    data: $transcribe_times \n\
                },\n')

    table_data = ""
    accuracy_graph_data = ""
    time_graph_data = ""
    time_graph_labels = []
    add_to_labels = True
    for file in listdir(results_folder):

        # load all model test info
        json_file = join(results_folder, file)
        model_test_info = json.load(open(json_file))

        # get model info needed for summary table
        model_info = model_test_info["test_details"]["model_info"]
        prompt_info = model_test_info["test_details"]["prompt_info"]
        test_results = model_test_info["test_results"]
        summary_info = model_test_info["test_summary"]

        transcribe_times = []
        for audio_sample in test_results:

            # update labels
            if add_to_labels:
                time_graph_labels.append(audio_sample)

            # update transcribe times
            transcribe_times.append(convertStringToSeconds(test_results[audio_sample]["transcribe_time"]))
            
        add_to_labels = False           # we only need to get the labels from one test result file to know them all, so we stop adding after the first time
        transcribe_times.append(convertStringToSeconds(summary_info["average_transcribe_time"]))        # add average transcribe time

        # add row template to table data
        table_data = table_data + table_row_template.substitute({'model_class': model_info["class_name"],
                                                                 'prompt_function': prompt_info["prompt_function_name"] + "()",
                                                                 'avg_transcribe_time': summary_info["average_transcribe_time"],
                                                                 'wer': summary_info["word_error_rate"],
                                                                 'mer': summary_info["match_error_rate"],
                                                                 'cer': summary_info["character_error_rate"],
                                                                 'wil': summary_info["word_information_lost"],
                                                                 'wip': summary_info["word_information_preserved"]})
        
        accuracy_graph_data = accuracy_graph_data + accuracy_graph_template.substitute({'model_title': model_info["class_name"] + " - " + prompt_info["prompt_function_name"] + "()",
                                                                 'wer': summary_info["word_error_rate"],
                                                                 'mer': summary_info["match_error_rate"],
                                                                 'cer': summary_info["character_error_rate"],
                                                                 'wil': summary_info["word_information_lost"],
                                                                 'wip': summary_info["word_information_preserved"]})

        time_graph_data = time_graph_data + time_graph_template.substitute({'model_title': model_info["class_name"] + " - " + prompt_info["prompt_function_name"] + "()",
                                                                 'transcribe_times': transcribe_times})

    time_graph_labels.append("Average Transcription Time")
    summary_table = table_template.substitute({'table_data': table_data, 'accuracy_graph_data': accuracy_graph_data, 'time_graph_labels': time_graph_labels, 'time_graph_data': time_graph_data, 'date': datetime.now().strftime("%B %d, %Y - %H:%M:%S")})

    try:
        print("Creating " + filename + " ...")
        with open(filename, "w") as html_file:
            html_file.write(summary_table)
        return True
    except Exception as e:
        print("ERROR: " + e)
        return False
    
def convertStringToSeconds(timeStr):
    t = datetime.strptime(timeStr,"%H:%M:%S.%f")
    seconds = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond).total_seconds()
    return seconds
