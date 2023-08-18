from os import mkdir
from os.path import isdir, join
from datetime import datetime
import requests, json
from create_dataset_json import create_dataset_json

# GETTING AUDIO DATA:

DATE = datetime.today().strftime('%Y-%m-%d')        # gets current date
URL = "https://pirsa.org/api/node/talk"
PARAMS = {"filter[status][value]": "1",
          "filter[talk_date-filter][condition][path]": "field_talk_date",
          "filter[talk_date-filter][condition][operator]": "%3E=",
          "filter[talk_date-filter][condition][value][1]": DATE,
          "sort": "field_talk_date"}

param_string = "&".join("%s=%s" % (k,v) for k,v in PARAMS.items())
audio_data = requests.get(url=URL, params=param_string).json()

# CREATING DATASET:

OUTPUT_DIR = "./datasets/"
DATASET_NAME = DATE

dataset = []

for current_audio_data in audio_data["data"]:
    dataset.append(create_dataset_json(current_audio_data))

# SAVING DATASET:

dataset_folder = join(OUTPUT_DIR, DATASET_NAME)

# Making folders:
if not isdir(OUTPUT_DIR):                   # make 'OUTPUT_DIR' folder if it doesn't already exist
    mkdir(OUTPUT_DIR)
if not isdir(dataset_folder):               # make 'dataset_folder' folder if it doesn't already exist
    mkdir(dataset_folder)       

# Making JSON file:
with open(join(dataset_folder, DATASET_NAME+".json"), "w") as f:
    f.write(json.dumps(dataset, indent=4))
