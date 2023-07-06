from os import listdir
from os.path import join
from datetime import datetime
from string import Template
import json

def create_test_summary_html(results_folder, filename="test_summary.html"):

    # ensuring proper file extension
    if not filename.lower().endswith(".html"):
        filename = filename + ".html"

    # define table and row templates
    with open("TestSummaryTemplate.html", "r") as template_file:
        table_template = Template(template_file.read())

    table_row_template = Template('\
                            <tr class="border-b dark:border-neutral-500"> \n\
                                <td class="whitespace-nowrap px-6 py-4 font-medium">$model_class</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$model_type</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$wer</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$mer</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$wil</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$wip</td> \n\
                                <td class="whitespace-nowrap px-6 py-4">$cer</td> \n\
                            </tr> \n')
    
    graph_data_template = Template('\
                { \n\
                    label: "$model_class", \n\
                    data: [$wer, $mer, $wil, $wip, $cer] \n\
                },\n')

    table_data = ""
    graph_data = ""
    for file in listdir(results_folder):

        # load all model test info
        json_file = join(results_folder, file)
        model_test_info = json.load(open(json_file))

        # get model info needed for summary table
        model_info = model_test_info["test_details"]["model_info"]
        summary_info = model_test_info["test_summary"]

        # add row template to table data
        table_data = table_data + table_row_template.substitute({'model_class': model_info["class_name"],
                                                                 'model_type': model_info["model_type"],
                                                                 'wer': summary_info["word_error_rate"],
                                                                 'mer': summary_info["match_error_rate"],
                                                                 'wil': summary_info["word_information_lost"],
                                                                 'wip': summary_info["word_information_preserved"],
                                                                 'cer': summary_info["character_error_rate"]})
        
        graph_data = graph_data + graph_data_template.substitute({'model_class': model_info["class_name"],
                                                                 'wer': summary_info["word_error_rate"],
                                                                 'mer': summary_info["match_error_rate"],
                                                                 'wil': summary_info["word_information_lost"],
                                                                 'wip': summary_info["word_information_preserved"],
                                                                 'cer': summary_info["character_error_rate"]})

    summary_table = table_template.substitute({'table_data': table_data, 'graph_data': graph_data, 'date': datetime.now().strftime("%B %d, %Y - %H:%M:%S")})

    try:
        print("Creating " + filename + " ...")
        with open(filename, "w") as html_file:
            html_file.write(summary_table)
        return True
    except Exception as e:
        print("ERROR: " + e)
        return False
