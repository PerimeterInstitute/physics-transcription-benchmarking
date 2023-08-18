from os import mkdir
from os.path import isdir, join
import requests, json
from create_dataset_json import create_dataset_json

# GETTING AUDIO DATA:

START_DATE = "2021-02-10"
END_DATE = "2021-02-12"
URL = "https://pirsa.org/api/node/talk"
# URL = "https://staging-5em2ouy-3mliee2m4wdei.ca-1.platformsh.site/api/node/talk"      # talk 21020004 has a transcript file with this url
PARAMS = {"filter[status][value]": "1",
          "include": "talk_attachments",
          "filter[talk_date-filter][condition][path]": "field_talk_date",
          "filter[talk_date-filter][condition][operator]": "BETWEEN",
          "filter[talk_date-filter][condition][value][1]": START_DATE,
          "filter[talk_date-filter][condition][value][2]": END_DATE,
          "sort": "field_talk_date"}

param_string = "&".join("%s=%s" % (k,v) for k,v in PARAMS.items())
audio_data = requests.get(url=URL, params=param_string).json()

# CREATING DATASET:

OUTPUT_DIR = "./datasets/"
DATASET_NAME = START_DATE+"--"+END_DATE

dataset = []

for current_audio_data in audio_data["data"]:

    # Check if PIRSA video has transcript file
    has_transcript = False
    attachment_data = requests.get(url=current_audio_data["relationships"]["talk_attachments"]["links"]["related"]["href"]).json()
    for attachment in attachment_data["data"]:
        if attachment["attributes"]["name"] == "transcript_" + current_audio_data["attributes"]["talk_number"] + ".txt":
            has_transcript = True
            break

    # Add to JSON if video does not have transcript file
    if not has_transcript:
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
