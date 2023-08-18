import requests
from bs4 import BeautifulSoup

def create_dataset_json(current_audio_data):

    # Variables:
    speakers = []
    keywords = []
    collections = []
    subjects = []
    speaker_data = requests.get(url=current_audio_data["relationships"]["talk_speaker_profile"]["links"]["related"]["href"]).json()
    collection_data = requests.get(url=current_audio_data["relationships"]["talk_collection"]["links"]["related"]["href"]).json()
    subject_data = requests.get(url=current_audio_data["relationships"]["talk_subject"]["links"]["related"]["href"]).json()
    audio_attributes = current_audio_data["attributes"]
    
    # Getting audio info:
    talk_number = audio_attributes["talk_number"]       # should exist
    title = audio_attributes["title"]                   # should exist
    description = audio_attributes["talk_abstract"]["processed"] if audio_attributes["talk_abstract"] else ""
    talk_date = audio_attributes["talk_date"] if audio_attributes["talk_date"] else "Unknown"
    talk_duration = audio_attributes["talk_duration"] if audio_attributes["talk_duration"] else "Unknown"

    # get keywords (?) --> usually empty

    # Getting speaker info:
    for speaker in speaker_data["data"]:
        name = speaker["attributes"]["display_name"] if speaker["attributes"]["display_name"] else ""
        institution = speaker["attributes"]["institution_name"] if speaker["attributes"]["institution_name"] else ""
        
        if name != "" or institution != "":
            speakers.append({"name": name,
                             "institution": institution})

    # Getting collection info:
    for collection in collection_data["data"]:
        name = collection["attributes"]["title"] if collection["attributes"]["title"] else ""
        description = collection["attributes"]["collection_description"]["processed"] if collection["attributes"]["collection_description"] else ""

        if name != "" or description != "":
            collections.append({"name": name,
                                "description": BeautifulSoup(description, features="html.parser").get_text()})

    # Getting subject info:
    for subject in subject_data["data"]:
        name = subject["attributes"]["name"] if name != "" or description != "" else ""
        description = subject["attributes"]["description"]["processed"] if subject["attributes"]["description"] else ""

        if (name != "" or description != "") and (name != "Other"):
            subjects.append({"name": name,
                            "description": BeautifulSoup(description, features="html.parser").get_text()})
            
    # Creating JSON Object:
    current_audio_json = {"audio_name": str(talk_number),
                          "audio_file": "https://streamer2.perimeterinstitute.ca/mp4-med/"+talk_number+".mp4",
                          "audio_info": {
                                "title": title,
                                "description": BeautifulSoup(description, features="html.parser").get_text(),
                                "keywords": keywords,
                                "speakers": speakers,
                                "date": talk_date,
                                "duration": talk_duration,
                                "collections": collections,
                                "subjects": subjects,
                                "source": {
                                    "link":"https://pirsa.org/"+talk_number,
                                }
                            }
                        }
    
    return current_audio_json
