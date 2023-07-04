from os import listdir
from os.path import join
from datetime import datetime
from string import Template
import json
from SummaryTableTemplate import table_template

def create_summary_table(results_folder):

    # define row template
    table_row_template = Template('\
    <tr> \n\
        <td>$model_class</td> \n\
        <td>$model_type</td> \n\
        <td>$wer</td> \n\
        <td>$mer</td> \n\
        <td>$wil</td> \n\
        <td>$wip</td> \n\
        <td>$cer</td> \n\
    </tr> \n')

    table_data = ""
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

    return table_template.substitute({'table_data': table_data, 'date': datetime.now().strftime("%B %d, %Y - %H:%M:%S")})
