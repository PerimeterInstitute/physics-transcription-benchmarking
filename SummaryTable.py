from os import listdir
from os.path import join
import json

def create_summary_table(results_folder):

    # define title row in summery table
    summary_table = [["Model Name", "Average Word Error Rate", "Average Match Error Rate", "Average Word Information Lost", "Average Word Information Preseved", "Average Character Error Rate"]]
    
    for file in listdir(results_folder):
        model_summary = []

        # load model json
        json_file = join(results_folder, file)
        model_test = json.load(open(json_file))

        # create model row
        model_summary.append(model_test["test_details"]["model_info"]["model_name"])
        for data in model_test["test_summary"].values():
            model_summary.append(data)

        # add model row to summary table
        summary_table.append(model_summary)

    return summary_table
