# Physics Transcription Benchmarking

Test suite created for benchmarking transcription models.



## How To Run

See [Test.ipynb](examples/Test.ipynb) for an example of the following steps put together.

### 1. Import Test Class
`from Test import Test`

### 2. Import Transcription Model(s)

#### Provided Model Wrappers
- [WhisperPI](#whisperpi) --> `from models.WhisperPI import WhisperPI`
- [WhisperOpenAI](#whisperopenai) --> `from models.WhisperOpenAI import WhisperOpenAI`
- [AzureSpeechToText](#azurespeechtotext) --> `from models.AzureSpeechToText import AzureSpeechToText`

#### Other Model Wrappers
See [How to Implement a Model Wrapper](#how-to-implement-a-model-wrapper).

### 3. Create Model Instance(s)

#### Provided Model Wrappers
- [WhisperPI](#whisperpi) --> See WhisperPI [constructor](#constructor-1)
- [WhisperOpenAI](#whisperopenai) --> See WhisperOpenAI [constructor](#constructor-2)
- [AzureSpeechToText](#azurespeechtotext) --> See AzureSpeechToText [constructor](#constructor-3)

#### Other Model Wrappers
See [How to Implement a Model Wrapper](#how-to-implement-a-model-wrapper).

### 4. Create Test Instance
See Test class [constructor](#constructor).

### 5. Access Resulting Data
Access test data (load time, transcription time, accuracy data, etc.) through Test class [attributes](#attributes).

Access transcription data through Model Wrapper class [attributes](#attributes-1).



## Test.py 

### Prompt Loading Function

`load_prompt_default(json_obj)` : Loads prompt string given audio information.
- `Dict json_obj` : JSON object containing audio information (it's suggested that this is loaded from a [dataset](#datasets) JSON file).

### Test Class

#### Required Packages
- JiWER --> `$ pip install jiwer`

#### Constructor
`Test(model_array, prompt_function_array=[load_prompt_default], dataset_path="full")` : Creates Test instance.
- `Model[] model_array` : Array of models to be tested
- `Method[] prompt_function_array` : Array of prompt loading functions to be tested (defaults to contain provided prompt loading function, [load_prompt_default()](#prompt-loading-function))
- `String dataset_path` : Path to dataset to use for testing (use "full" or "dev" to use provided dataset)

#### Attributes
- `Dict results` : Dictionary containing load time, transcription time, and accuracy data (word error rate, character error rate, etc.) for each model that was provided in the constructor

Example `results` dictionary: 
```
"results": {
    "model_1": {
        "test_details": {
            "model_info": {
                "class_name": "WhisperOpenAI",
                "model_name": "model_1",
                "model_type": "medium",
                "options": {
                    "language": "en"
                }
            },
        "prompt_info": {
            "prompt_function_name": "load_prompt_default",
            "prompt_function_code": "def load_prompt_default(json_obj): ..."
        },
            "system_info": {
                "system": "Linux",
                "release": "5.15.0-1040-azure",
                "version": "#47-Ubuntu SMP Thu Jun 1 19:38:24 UTC 2023",
                "machine": "x86_64",
                "processor": "x86_64"
            },
            "cpu_info": {
                "physical_cores": 2,
                "total_cores": 4
            },
            "memory_info": {
                "total_memory": 16767574016,
                "available_memory": 7527411712,
                "used_memory": 8884101120
            }
        },
        "test_results": {
            "test_audio_1": {
                "start_datetime": "06/30/2023 15:01:37",
                "load_time": "0:00:16.374215",
                "transcribe_time": "0:00:55.688600",
                "accuracy_data": {
                    "word_error_rate": 0.1917808219178082,
                    "match_error_rate": 0.17721518987341772,
                    "word_information_lost": 0.25799086757990863,
                    "word_information_preserved": 0.7420091324200914,
                    "character_error_rate": 0.023305084745762712
                }
            },
            "test_audio_2": {
                "start_datetime": "06/30/2023 15:02:26",
                "load_time": "0:00:16.374215",
                "transcribe_time": "0:00:48.690690",
                "accuracy_data": {
                    "word_error_rate": 0.19047619047619047,
                    "match_error_rate": 0.17647058823529413,
                    "word_information_lost": 0.2679738562091504,
                    "word_information_preserved": 0.7320261437908496,
                    "character_error_rate": 0.019178082191780823
                }
            },
            "test_audio_3": {
                "start_datetime": "06/30/2023 15:05:03",
                "load_time": "0:00:16.374215",
                "transcribe_time": "0:02:37.643353",
                "accuracy_data": {
                    "word_error_rate": 0.3380952380952381,
                    "match_error_rate": 0.3141592920353982,
                    "word_information_lost": 0.4846632346632347,
                    "word_information_preserved": 0.5153367653367653,
                    "character_error_rate": 0.12126696832579185
                }
            }
        },
        "test_summary": {
            "word_error_rate": 0.2401174168297456,
            "match_error_rate": 0.22261502338137004,
            "word_information_lost": 0.3368759861507646,
            "word_information_preserved": 0.6631240138492355,
            "character_error_rate": 0.05458337842111179
        }
    }
}
```



## Model Wrappers

### WhisperPI
Wrapper for the WhisperPI transcription model. WhisperPI is an altered version of [OpenAI's Whisper](https://github.com/openai/whisper) speech recognition model, used to transcribe videos on the Perimeter Institute Recorded Seminar Archive (PIRSA).

#### Required Packages
- pi-whisper --> `$ pip install git+https://github.com/rmohl/whisper.git`

#### Constructor
`WhisperPI(name, options)` : Creates WhisperPI instance.
- `String name` : Name of model
- `Dict options` : Model options (includes `model_type`, `language`, `temperature`, and other options offered by [OpenAI's Whisper](https://github.com/openai/whisper))


#### Attributes
- `String name` : Name of model
- `String model_type` : Model type ("tiny", "base", "medium", "large", etc.)
- `Bool takes_prompt` : Indicates whether the model takes a prompt or not
- `Dict options` : Model options
- `Dict full_result` : Dictionary containing all result objects.
- `Dict transcription` : Dictionary containing the text from all resulting transcriptions.
- `Dict load_time` : Dictionary containing all load times.
- `Dict transcribe_time` : Dictionary containing all transcribe times.

#### Methods
- `load()` : Loads model.
- `unload()` : "Unloads" model (i.e. removes select model attributes from memory).
- `transcribe(audio, prompt=None)` : Transcribes given audio file, updates result-related attributes.
    - `String audio` : File path to audio file
    - `String prompt` : Transcription prompt


### WhisperOpenAI
Wrapper for [OpenAI's Whisper](https://github.com/openai/whisper) speech recognition model.

#### Required Packages
- openai-whisper --> `$ pip install -U openai-whisper`

#### Constructor
`WhisperOpenAI(name, options)` : Creates WhisperOpenAI instance.
- `String name` : Name of model
- `Dict options` : Model options (includes `model_type`, `language`, `temperature`, and other options offered by [OpenAI's Whisper](https://github.com/openai/whisper))

#### Attributes
- `String name` : Name of model
- `String model_type` : Model type ("tiny", "base", "medium", "large", etc.)
- `Bool takes_prompt` : Indicates whether the model takes a prompt or not
- `Dict options` : Model options
- `Dict full_result` : Dictionary containing all result objects.
- `Dict transcription` : Dictionary containing the text from all resulting transcriptions.
- `Dict load_time` : Dictionary containing all load times.
- `Dict transcribe_time` : Dictionary containing all transcribe times.

#### Methods
- `load()` : Loads model.
- `unload()` : "Unloads" model (i.e. removes select model attributes from memory).
- `transcribe(audio, prompt=None)` : Transcribes given audio file, updates result-related attributes.
    - `String audio` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to `None`


### AzureSpeechToText
Wrapper for Azure's speech recognition model.

#### Required Packages
- Azure Cognitive Services Speech SDK --> `$ pip install azure-cognitiveservices-speech`

#### Constructor
`AzureSpeechToText(name, key, region, options)` : Creates AzureSpeechToText instance.
- `String name` : Name of model
- `String key` : Azure subscription key
- `String region` : Region name (see [regions](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/regions))
- `Dict options` : Model options (includes `speech_recognition_language`, `endpoint`, `host`, and other options offered by [Azure's Cognitive Services Speech SDK](https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechconfig?view=azure-python#constructor))

#### Attributes
- `String name` : Name of model
- `String key` : Azure subscription key
- `String region` : Region name
- `Bool takes_prompt` : Indicates whether the model takes a prompt or not
- `Dict options` : Model options
- `Dict transcription` : Dictionary containing the text from all resulting transcriptions.
- `Dict load_time` : Dictionary containing all load times.
- `Dict transcribe_time` : Dictionary containing all transcribe times.

#### Methods
- `load()` : Loads model.
- `unload()` : "Unloads" model (i.e. removes select model attributes from memory).
- `transcribe(audio, prompt=None)` : Transcribes given audio file, updates result-related attributes.
    - `String audio` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to `None`



## How to Implement a Model Wrapper

### ModelWrapper Interface

In order to be compatible with the Test class, a Model Wrapper class must have `name`, `transcription`, `load_time`, and `transcribe_time` attributes, as well as a `transcribe()` method. Using the [ModelWrapper.py](ModelWrapper.py) interface ensures that all required attributes and methods are implemented in a Model Wrapper class. 

```
from ModelWrapper import ModelWrapper

class NewModelWrapper(ModelWrapper):
    name = ""
    takes_prompt = True
    transcription = {}
    load_time = {}
    transcribe_time = {}

    def load():
        pass

    def unload():
        pass

    def transcribe():
        pass

    ...
```

### Using Model Wrapper

Put the Model Wrapper class file in [models/](models/) folder. Import the Wrapper using `from models.YOUR_WRAPPER_NAME import YOUR_WRAPPER_NAME`



## Datasets

### Provided Datasets
- [Full Dataset](datasets/full_dataset/) --> use dataset path "full" in Test [constructor](#constructor)
- [Development Dataset](datasets/dev_dataset/) --> use dataset path "dev" in Test [constructor](#constructor)

### Other Datasets
Datasets must have the following structure in order to be used with the Test class:
```
dataset_name/
    --> dataset_name.json
    --> test_data/
        --> data_1.mp4
        --> data_1.txt
        --> data_2.wav
        --> data_2.txt
               ...
```
Please reference [full_dataset.json](datasets/full_dataset/full_dataset.json) for formatting of the dataset JSON file. 

For each audio/transcript pair that will be tested, there should be an audio or video file (.mp4, .mp3, .wav, etc.) and a text file of the same name that contains a reference transcription. All of these files should go in the 'test_data' folder.

Test using this dataset by passing it's local path into the Test class [constructor](#constructor).



## Creating Test Summary HTML

### TestSummary.py

#### Methods
- `create_test_summary_html(results_folder, filename="test_summary.html")` : Creates HTML file that displays test summary information with a table and bar chart.
    - `String results_folder` : File path to results folder containing result test model JSON files
    - `String filename` : Output name for HTML file, defaults to `test_summary.html`
