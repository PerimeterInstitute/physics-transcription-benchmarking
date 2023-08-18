from Test import Test
from prompt_functions import get_description, get_rachaels_keywords, get_azure_keywords, get_spacy_keybert_keywords, get_gpt_keywords, get_gpt_challenging_keywords, get_formatted_description, get_formatted_rachaels_keywords, get_formatted_azure_keywords, get_formatted_spacy_keybert_keywords, get_formatted_gpt_keywords, get_formatted_gpt_challenging_keywords
from models.AzureSpeechToText import AzureSpeechToText
from models.WhisperOpenAI import WhisperOpenAI
from models.WhisperPI import WhisperPI

AZURE_KEY = ""
AZURE_REGION = ""

azure_model = AzureSpeechToText("azure_large", AZURE_KEY, AZURE_REGION,
                            {
                              "speech_recognition_language": "en-US"
                            }
)

whisper_model = WhisperOpenAI("whisper_openai_large",
                  {
                    "model_type": "large",
                    "language": "en" 
                  }
)

whisperPI_model = WhisperPI("whisper_pi_large",
                  {
                    "model_type": "large",
                    "language": "en"
                  }
)

test = Test([azure_model, whisper_model, whisperPI_model], prompt_function_array=[get_description, get_rachaels_keywords, get_azure_keywords, get_spacy_keybert_keywords, get_gpt_keywords, get_gpt_challenging_keywords, get_formatted_description, get_formatted_rachaels_keywords, get_formatted_azure_keywords, get_formatted_spacy_keybert_keywords, get_formatted_gpt_keywords, get_formatted_gpt_challenging_keywords], dataset_path="./datasets/full_dataset/")