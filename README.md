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

#### Other Models Wrappers
See [How to Implement a Model Wrapper](#how-to-implement-a-model-wrapper)

### 4. Create Test Instance
See Test class [constructor](#constructor).

### 5. Access Resulting Data
Access test data (load time, transcription time, accuracy data, etc.) through Test class [attributes](#attributes).
Access transcription data through Model Wrapper class [attributes](#attributes-1).



## Test Class

#### Constructor
`Test(Model[] model_array, String dataset_path)="full"` : Creates Test instance.
- `Model[] model_array` : Array of models to be tested
- `String dataset_path` : Path to dataset to use for testing (use "full" or "dev" to use provided dataset)

#### Attributes
- `Dict results`: Dictionary containing load time, transcription time, and accuracy data (word error rate, character error rate, etc.) for each model that was provided in the constructor

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
Wrapper for Whisper transcription model altered for the purpose of effectively transcribing PIRSA lectures.

#### Required Packages
- pi-whisper: `$ pip install git+https://github.com/rmohl/whisper.git`

#### Constructor
`WhisperPI(name, options)` : Creates WhisperPI instance.
- `String name` : Name of model
- `Dict options` : Model options (`model_type`, `language`, see other og Whisper options)

#### Attributes
- `String name` : Name of model
- `String model_type` : Model type ("tiny", "base", "medium", "large", etc.)
- `Dict options` : Model options (see og Whisper options)
- `Dict full_result` : Dictionary containing all result objects.
- `Dict transcription` : Dictionary containing the text from all resulting transcriptions.
- `Dict load_time` : Dictionary containing all load times.
- `Dict transcribe_time` : Dictionary containing all transcribe times.

#### Methods
- `transcribe(String audio, String prompt=None):` : Transcribes given audio file, updates result-related attributes.
    - `String audio` : File path to audio file
    - `String prompt` : Transcription prompt


### WhisperOpenAI
Wrapper for original Whisper transcription model (from --link to git--).

#### Required Packages
- openai-whisper: `$ pip install -U openai-whisper`

#### Constructor
`WhisperOpenAI(name, options)` : Creates WhisperOpenAI instance.
- `String name` : Name of model
- `Dict options` : Model options (`model_type`, `language`, see other og Whisper options)

#### Attributes
- `String name` : Name of model
- `String model_type` : Model type ("tiny", "base", "medium", "large", etc.)
- `Dict options` : Model options (see og Whisper options)
- `Dict full_result` : Dictionary containing all result objects.
- `Dict transcription` : Dictionary containing the text from all resulting transcriptions.
- `Dict load_time` : Dictionary containing all load times.
- `Dict transcribe_time` : Dictionary containing all transcribe times.

#### Methods
- `transcribe(String audio_file, String prompt=None)` : Transcribes given audio file, updates result-related attributes.
    - `String audio` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to None



## How to Implement a Model Wrapper
Use ModelFormat.py



## Datasets

### Provided Datasets

### Folder Structure
If you would like to use your own dataset, please use this file structure.
