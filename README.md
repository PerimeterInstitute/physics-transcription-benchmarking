# Physics Transcription Benchmarking
Test suite created for benchmarking transcription models.


## How To Run
See [Test.ipynb](examples/Test.ipynb) for an example of the following steps put together.

### 1. Clone Repo
`$ git clone https://github.com/PerimeterInstitute/physics-transcription-benchmarking`

### 2. Use Transcription Model Wrapper

#### Importing Wrapper
- [WhisperPI](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models?tab=readme-ov-file#whisperpi) --> `from models.WhisperPI import WhisperPI`
- [WhisperOpenAI](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models?tab=readme-ov-file#whisperopenai) --> `from models.WhisperOpenAI import WhisperOpenAI`
- [WhisperCPP](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models?tab=readme-ov-file#whispercpp) --> `from models.WhisperCPP import WhisperCPP`
- [AzureSpeechToText](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models?tab=readme-ov-file#azurespeechtotext) --> `from models.AzureSpeechToText import AzureSpeechToText`

#### Instantiating Wrapper
See the wrapper model's associated constructor (defined in [this README](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models/README.md)) to create an instance of it.

#### Creating Your Own Wrapper
See [How to Implement a Model Wrapper](#how-to-implement-a-model-wrapper) to create your own model wrapper.

### 3. Use Test Class for Benchmarking

#### Importing Test Class
`from Test import Test`

#### Instantiating Test
See Test class [constructor](#constructor).

### 4. View Results
- Access TXT and VTT transcription(s) through Model Wrapper object.
- See resulting JSON files (contain load times, transcription times, accuracy data, etc.) in current working directory.


## Test.py 

### Test Class

#### Required Packages/Downloads
- JiWER --> `$ pip install jiwer`

#### Constructor
`Test(model_array, prompt_function_array=[no_prompt], dataset_path="full", run_num=1, save_transcription=False)` : Creates Test instance
- `Model[] model_array` : Array of models to be tested
- `Method[] prompt_function_array` : Array of prompt loading functions to be tested (defaults to contain provided prompt loading function, `no_prompt()`, which returns an empty string)
- `String dataset_path` : Path to dataset to use for testing (use "full" or "dev" to use provided dataset)
- `int run_num` : Number of times to transcribe the same audio file with the same model, prompt, etc.
- `Boolean save_transcription` : Boolean indicating if transcriptions should be saved

#### Results
After running the test, a 'results/' folder in the current working directory will be created. This folder will contain various JSON result files that hold transcription data from each unique model/prompt combination.

Example JSON result file: 
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

### AddToExistingTest Class

#### Required Packages/Downloads
- JiWER --> `$ pip install jiwer`

#### Constructor
`AddToExistingTest(existing_test_json, model, prompt_function=no_prompt, dataset_path="full", run_num=1, output_file_name=None)` : Creates AddToExistingTest instance
- `String existing_test_json` : JSON file created from a previous test
- `Model model` : Model to be further tested (should be same as model used in provided JSON)
- `Method prompt_function` : Prompt function to be further tested (should be same as prompt function used in provided JSON)
- `String dataset_path` : Path to dataset to use for testing (use "full" or "dev" to use provided dataset)
- `int run_num` : Number of times to transcribe the same audio file with the same model, prompt, etc.
- `String output_file_name` : New JSON result file name (optional, will overwrite provided JSON if not used)

#### Results
After running this test, an updated JSON result file will exist containing both the original and desired additional transcription data.


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

Put your model wrapper class file in [models/](models/) folder. Import the Wrapper using `from models.YOUR_WRAPPER_NAME import YOUR_WRAPPER_NAME`



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



## TestSummary.py

### Methods
- `create_test_summary_html(results_folder, filename="test_summary.html")` : Creates HTML file that displays test summary information with a table and bar chart.
    - `String results_folder` : File path to results folder containing result test model JSON files
    - `String filename` : Output name for HTML file, defaults to `test_summary.html`
