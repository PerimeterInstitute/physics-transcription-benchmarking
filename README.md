# transcription-benchmarking

Test suite created for benchmarking transcription models.



## How To Run

See [example.ipynb](example.ipynb) for an example of these steps put together.

### 1. Import Test Class
`from Test import Test`

### 2. Import Transcription Model(s)

#### Provided Model Wrappers
- [WhisperPI](#whisperpi) --> `from models.WhisperPI import WhisperPI`
- [WhisperOpenAI](#whisperopenai) --> `from models.WhisperOpenAI import WhisperOpenAI`

#### Other Model Wrappers
See [How to Implement a Model Wrapper](#how-to-implement-a-model-wrapper)

### 3. Create Model Instance(s)

#### Provided Model Wrappers
- [WhisperPI](#whisperpi) --> See WhisperPI [constructor](#constructor-1)
- [WhisperOpenAI](#whisperopenai) --> See WhisperOpenAI [constructor](#constructor-2)

#### Other Model Wrappers
See [How to Implement a Model Wrapper](#how-to-implement-a-model-wrapper)

### 4. Create Test Instance
See Test class [constructor](#constructor).

### 5. Access Resulting Data
Access test data (load time, transcription time, accuracy data, etc.) through Test class [attributes](#attributes).

Access transcription data through Model Wrapper class [attributes](#attributes-1).



## Test Class

#### Constructor
`Test(model_array, dataset_path="full")` : Creates Test instance.
- `Model[] model_array` : Array of models to be tested
- `String dataset_path` : Path to dataset to use for testing (use "full" or "dev" to use provided dataset)

#### Attributes
- `Dict results` : Dictionary containing load time, transcription time, and accuracy data (word error rate, character error rate, etc.) for each model that was provided in the constructor

Example `results` dictionary: 
```
"results": {
    "model_1": {
        "test_audio_1": {
            "load_time": "0:05:43.108026",
            "transcribe_time": "0:00:54.956891",
            "test_results": {
                "word_error_rate": 0.2191780821917808,
                "match_error_rate": 0.1951219512195122,
                "word_information_lost": 0.272302038088874,
                "word_information_preserved": 0.727697961911126,
                "character_error_rate": 0.05084745762711865
            }
        },
        "test_audio_2": {
            "load_time": "0:05:43.108026",
            "transcribe_time": "0:00:49.013099",
            "test_results": {
                "word_error_rate": 0.19047619047619047,
                "match_error_rate": 0.17647058823529413,
                "word_information_lost": 0.2679738562091504,
                "word_information_preserved": 0.7320261437908496,
                "character_error_rate": 0.019178082191780823
            }
        }
    },
    "model_2": {
        "test_audio_1": {
            "load_time": "0:00:32.582526",
            "transcribe_time": "0:01:35.986448",
            "test_results": {
                "word_error_rate": 0.2191780821917808,
                "match_error_rate": 0.1951219512195122,
                "word_information_lost": 0.272302038088874,
                "word_information_preserved": 0.727697961911126,
                "character_error_rate": 0.05084745762711865
            }
        },
        "test_audio_2": {
            "load_time": "0:00:32.582526",
            "transcribe_time": "0:01:27.272061",
            "test_results": {
                "word_error_rate": 0.12698412698412698,
                "match_error_rate": 0.11940298507462686,
                "word_information_lost": 0.17531390665719027,
                "word_information_preserved": 0.8246860933428097,
                "character_error_rate": 0.010958904109589041
            }
        },
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
- `Dict options` : Model options (see og Whisper options)
- `Dict full_result` : Dictionary containing all result objects.
- `Dict transcription` : Dictionary containing the text from all resulting transcriptions.
- `Dict load_time` : Dictionary containing all load times.
- `Dict transcribe_time` : Dictionary containing all transcribe times.

#### Methods
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
- `Dict options` : Model options (see og Whisper options)
- `Dict full_result` : Dictionary containing all result objects.
- `Dict transcription` : Dictionary containing the text from all resulting transcriptions.
- `Dict load_time` : Dictionary containing all load times.
- `Dict transcribe_time` : Dictionary containing all transcribe times.

#### Methods
- `transcribe(audio, prompt=None)` : Transcribes given audio file, updates result-related attributes.
    - `String audio` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to None



## How to Implement a Model Wrapper

### ModelWrapper Interface
`from ModelWrapper import ModelWrapper`

In order to be compatible with the Test class, a Model Wrapper class must have `name`, `transcription`, `load_time`, and `transcribe_time` attributes, as well as a `transcribe()` method. Using the [ModelWrapper.py](ModelWrapper.py) interface ensures that all required attributes and methods are implemented in a Model Wrapper class. 

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
