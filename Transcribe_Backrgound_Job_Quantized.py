# import sys
# sys.path.append('./') 

from Transcribe import Transcribe
# from models.WhisperPI import WhisperPI
from models.WhisperOpenAI_Quantized import WhisperOpenAI
#import WhisperOpenAI
#import whisper
#from prompt_functions.prompt_functions import get_description, get_formatted_description, get_formatted_rachaels_keywords ,get_formatted_azure_keywords, get_formatted_spacy_keybert_keywords ,get_formatted_gpt_keywords, get_formatted_gpt_challenging_keywords, get_speakers_collections_subjects ,get_rachaels_keywords ,get_azure_keywords, get_spacy_keybert_keywords, get_gpt_keywords, get_gpt_challenging_keywords

#my_prompt_function_array=[get_formatted_description,get_formatted_rachaels_keywords,get_formatted_azure_keywords,get_formatted_spacy_keybert_keywords,get_formatted_gpt_keywords,get_formatted_gpt_challenging_keywords,get_speakers_collections_subjects,get_description,get_rachaels_keywords,get_azure_keywords,get_spacy_keybert_keywords,get_gpt_keywords,get_gpt_challenging_keywords]
#my_prompt_function_array=[get_formatted_gpt_challenging_keywords]

model = WhisperOpenAI("whisper_pi_large_v3",
                  {
                    "model_type": "large-v3",
                    "language": "en"
                  }
)

Transcribe(model, dataset_path="./datasets/full_dataset/")