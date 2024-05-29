from string import Template

# ========================== #
# ==== Prompt Templates ==== #
# ========================== #

prompt_keyword_template = Template("$speaker I will be presenting a talk called '$title'. Some of the topics we will cover include $keywords.$speakers")
prompt_description_template = Template("$speaker I will be presenting a talk called '$title'. $description$speakers")
speaker_template = Template(" - Hi my name is $name and I'm representing $institution.")

# ==================================== #
# ==== TEMPLATED Prompt Functions ==== #
# ==================================== #

def get_formatted_description(json_obj):

    # FORMATTING PROMPT:

    speakers = []
    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        speakers.append(speaker_template.substitute({'name': name,
                                                    'institution': institution}))

    # CREATING PROMPT STRING:

    prompt = prompt_description_template.substitute({"title": json_obj["title"].strip(),
                                                "description": json_obj["description"].strip(),
                                                "speaker": speakers[0],
                                                "speakers": " ".join(speakers[1:-1])})
    
    # print("PROMPT:")
    # print (prompt)
    return prompt


def get_formatted_rachaels_keywords(json_obj):

    # FORMATTING PROMPT:

    keywords = ""
    if "rachaels_keywords" in json_obj:
        for keyword in json_obj["rachaels_keywords"]:
            keywords = keywords + keyword.strip() + ", "
        keywords.rstrip(", ")

    speakers = []
    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        speakers.append(speaker_template.substitute({'name': name,
                                                    'institution': institution}))

    # CREATING PROMPT STRING:
    
    return prompt_keyword_template.substitute({"title": json_obj["title"].strip(),
                                       "keywords": keywords,
                                       "speaker": speakers[0],
                                       "speakers": " ".join(speakers[1:-1])})


def get_formatted_azure_keywords(json_obj):

    # FORMATTING PROMPT:

    keywords = ""
    if "azure_keywords" in json_obj:
        for keyword in json_obj["azure_keywords"]:
            keywords = keywords + keyword.strip() + ", "
        keywords.rstrip(", ")

    speakers = []
    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        speakers.append(speaker_template.substitute({'name': name,
                                                    'institution': institution}))

    # CREATING PROMPT STRING:
    
    return prompt_keyword_template.substitute({"title": json_obj["title"].strip(),
                                       "keywords": keywords,
                                       "speaker": speakers[0],
                                       "speakers": " ".join(speakers[1:-1])})


def get_formatted_spacy_keybert_keywords(json_obj):

    # FORMATTING PROMPT:

    keywords = ""
    if "spacy_keybert_keywords" in json_obj:
        for keyword in json_obj["spacy_keybert_keywords"]:
            keywords = keywords + keyword.strip() + ", "
        keywords.rstrip(", ")

    speakers = []
    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        speakers.append(speaker_template.substitute({'name': name,
                                                    'institution': institution}))

    # CREATING PROMPT STRING:
    
    return prompt_keyword_template.substitute({"title": json_obj["title"].strip(),
                                       "keywords": keywords,
                                       "speaker": speakers[0],
                                       "speakers": " ".join(speakers[1:-1])})


def get_formatted_gpt_keywords(json_obj):

    # FORMATTING PROMPT:

    keywords = ""
    if "gpt_keywords" in json_obj:
        for keyword in json_obj["gpt_keywords"]:
            keywords = keywords + keyword.strip() + ", "
        keywords.rstrip(", ")

    speakers = []
    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        speakers.append(speaker_template.substitute({'name': name,
                                                    'institution': institution}))

    # CREATING PROMPT STRING:
    
    return prompt_keyword_template.substitute({"title": json_obj["title"].strip(),
                                       "keywords": keywords,
                                       "speaker": speakers[0],
                                       "speakers": " ".join(speakers[1:-1])})


def get_formatted_gpt_challenging_keywords(json_obj):

    # FORMATTING PROMPT:

    keywords = ""
    if "gpt_challenging_keywords" in json_obj:
        for keyword in json_obj["gpt_challenging_keywords"]:
            keywords = keywords + keyword.strip() + ", "
        keywords.rstrip(", ")

    speakers = []
    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        speakers.append(speaker_template.substitute({'name': name,
                                                    'institution': institution}))

    # CREATING PROMPT STRING:
    
    return prompt_keyword_template.substitute({"title": json_obj["title"].strip(),
                                       "keywords": keywords,
                                       "speaker": speakers[0],
                                       "speakers": " ".join(speakers[1:-1])})

# ================================== #
# ==== KEYWORD Prompt Functions ==== #
# ================================== #

def no_prompt(json_obj):
    return ""

def get_speakers_collections_subjects(json_obj):

    # FORMATTING PROMPT:

    prompt = json_obj["title"].strip() + ", " 

    # Speakers
    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        prompt = prompt + name + ", "
        if institution not in prompt:
            prompt = prompt + institution + ", "

    # Collections
    for collection in json_obj["collections"]:
        prompt = prompt + collection["name"].strip() + ", "

    # Subjects
    for subject in json_obj["subjects"]:
        prompt = prompt + subject["name"].strip() + ", "

    prompt.rstrip(", ")

    return prompt

def get_description(json_obj):

    # FORMATTING PROMPT:

    prompt = json_obj["title"].strip() + ", " 

    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        prompt = prompt + name + ", "
        if institution not in prompt:
            prompt = prompt + institution + ", "

    prompt = prompt + json_obj["description"].strip()

    return prompt


def get_rachaels_keywords(json_obj):

    # FORMATTING PROMPT:

    prompt = json_obj["title"].strip() + ", " 

    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        prompt = prompt + name + ", "
        if institution not in prompt:
            prompt = prompt + institution + ", "

    if "rachaels_keywords" in json_obj:
        for keyword in json_obj["rachaels_keywords"]:
            prompt = prompt + keyword.strip() + ", "

    prompt.rstrip(", ")

    return prompt


def get_azure_keywords(json_obj):

    # FORMATTING PROMPT:

    prompt = json_obj["title"].strip() + ", " 

    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        prompt = prompt + name + ", "
        if institution not in prompt:
            prompt = prompt + institution + ", "

    if "azure_keywords" in json_obj:
        for keyword in json_obj["azure_keywords"]:
            prompt = prompt + keyword.strip() + ", "

    prompt.rstrip(", ")

    return prompt


def get_spacy_keybert_keywords(json_obj):

    # FORMATTING PROMPT:

    prompt = json_obj["title"].strip() + ", " 

    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        prompt = prompt + name + ", "
        if institution not in prompt:
            prompt = prompt + institution + ", "

    if "spacy_keybert_keywords" in json_obj:
        for keyword in json_obj["spacy_keybert_keywords"]:
            prompt = prompt + keyword.strip() + ", "

    prompt.rstrip(", ")

    return prompt


def get_gpt_keywords(json_obj):

    # FORMATTING PROMPT:

    prompt = json_obj["title"].strip() + ", " 

    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        prompt = prompt + name + ", "
        if institution not in prompt:
            prompt = prompt + institution + ", "

    if "gpt_keywords" in json_obj:
        for keyword in json_obj["gpt_keywords"]:
            prompt = prompt + keyword.strip() + ", "

    prompt.rstrip(", ")

    return prompt


def get_gpt_challenging_keywords(json_obj):

    # FORMATTING PROMPT:

    prompt = json_obj["title"].strip() + ", " 

    for speaker in json_obj["speakers"]:
        name = speaker["name"].strip()
        institution = speaker["institution"].strip()

        prompt = prompt + name + ", "
        if institution not in prompt:
            prompt = prompt + institution + ", "

    if "gpt_challenging_keywords" in json_obj:
        for keyword in json_obj["gpt_challenging_keywords"]:
            prompt = prompt + keyword.strip() + ", "

    prompt.rstrip(", ")

    return prompt
