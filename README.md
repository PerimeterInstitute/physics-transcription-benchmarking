# Physics Transcription Benchmarking
Test suite created for benchmarking transcription models.


## How To Run
See [Test.ipynb](examples/Test.ipynb) for an example of the following steps put together.

### 1. Setup

#### a) Clone Repo
`$ git clone https://github.com/PerimeterInstitute/physics-transcription-benchmarking`

#### b) Run `setup.sh` File
`$ cd physics-transcription-benchmarking/`\
`$ bash setup.sh`

### 2. Use Transcription Model Wrapper

#### Importing Wrapper
- [WhisperPI](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models?tab=readme-ov-file#whisperpi) &rarr; `from models.WhisperPI import WhisperPI`
- [WhisperOpenAI](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models?tab=readme-ov-file#whisperopenai) &rarr; `from models.WhisperOpenAI import WhisperOpenAI`
- [WhisperCPP](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models?tab=readme-ov-file#whispercpp) &rarr; `from models.WhisperCPP import WhisperCPP`
- [AzureSpeechToText](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models?tab=readme-ov-file#azurespeechtotext) &rarr; `from models.AzureSpeechToText import AzureSpeechToText`

#### Instantiating Wrapper
See the wrapper model's associated constructor (defined in [this README](https://github.com/PerimeterInstitute/physics-transcription-benchmarking/tree/main/models/README.md)) to create an instance of it.

#### Creating Your Own Wrapper
See [How to Implement a Model Wrapper](#how-to-implement-a-model-wrapper) to create your own model wrapper.

### 3. Use Test Class for Benchmarking

#### a) Importing Test Class
`from Test import Test`

#### b) Instantiating Test
See Test class [constructor](#constructor).

#### c) Executing Benchmarking Test
See [run()](#methods) method from Test class.

During the test runtime, folders titled 'results/', 'transcriptions/', and 'TEMP_DATA/' will exist in the desired output folder.

<p align=center><b>** DO NOT delete or alter these folders in any way until the benchmarking test has completed! **</b><p>

### 4. View Results
- Access TXT and VTT transcription(s) through Model Wrapper object.
- See resulting JSON files (contain load times, transcription times, accuracy data, etc.) in 'results/' folder in the current working directory.

### 5. Create Test Summary HTML File
- Do this using the [createSummaryHTML()](#methods) method in the Test class
- Do this using the repo's [create_test_summary_html()](#creating-a-summary-html-file) method


## Test.py 

### Test Class
See [Test.ipynb](examples/Test.ipynb) for an example of how to use this class.

<!-- #### Required Packages/Downloads
- JiWER &rarr; `$ pip install jiwer`
- openai-whisper &rarr; `$ pip install -U openai-whisper` -->

#### Constructor
`Test(model_array, prompt_function_array=[no_prompt], output_dir=getcwd())` : Creates Test instance
- `ModelWrapper[] model_array` : Array of models to be tested
- `Method[] prompt_function_array` : Array of prompt loading functions to be tested (defaults to contain provided prompt loading function, `no_prompt()`, which returns an empty string)
- `String output_dir` : Directory where test output will be stored, defaults to current working directory.

#### Methods
- `run(run_name, dataset_path, run_num=1, save_transcription=False)` : Runs tests comparing the transcriptions of each unique model/prompt/audio combination
    - `String run_name` : Name of run
    - `String dataset_path` : Path to dataset to use for testing
    - `int run_num` : Number of times to transcribe the same audio file with the same model/prompt combiation (good for testing consistency!)
    - `Boolean save_transcription` : Boolean indicating if transcriptions should be saved
- `addModel(new_model)` : Adds provided model to model array
    - `ModelWrapper new_model` : New model to be added
- `removeModel(existing_model_name)` : Removes model with provided name from model array
    - `String existing_model_name` : Name of model to be removed
- `addPromptFunction(new_prompt_func)` : Adds provided prompt function to prompt function array
    - `Method new_prompt_func` : New prompt function to be added
- `removePromptFunction(existing_prompt_func_name)` : Removes prompt function with provided name from prompt function array
    - `String existing_prompt_func_name` : Name of prompt function to be removed
- `createSummaryHTML(html_filename=None)` : Creates HTML file that displays intuitive summary of test data from most recent run.
    - `String html_filename` : Output file name (do not include extension, defaults to RUN_NAME)
- `free()` : Removes and frees select attributes from memory

#### Results
After running, a 'results/RUN_NAME/' folder will be created in the current working directory. This folder will contain various JSON result files that hold transcription data from each unique model/prompt combination.

If `save_transcription` is set to `True`, a 'transcriptions/RUN_NAME/' folder will be created in the current working directory. This folder will contain both the original and normalized transcriptions of each unique model/prompt/audio combination.

Example JSON result file: 
```
{
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
            "run_0": {
                "start_datetime": "05/30/24, 15:10:58",
                "transcribe_time": "0:00:03.993462",
                "word_error_rate": 0.012195121951219513,
                "match_error_rate": 0.012048192771084338,
                "character_error_rate": 0.010548523206751054,
                "word_information_lost": 0.012048192771084376,
                "word_information_preserved": 0.9879518072289156,
                "phrase_repeat_diff": 2
            },
            "run_1": {
                "start_datetime": "05/30/24, 15:11:02",
                "transcribe_time": "0:00:03.941539",
                "word_error_rate": 0.012195121951219513,
                "match_error_rate": 0.012048192771084338,
                "character_error_rate": 0.010548523206751054,
                "word_information_lost": 0.012048192771084376,
                "word_information_preserved": 0.9879518072289156,
                "phrase_repeat_diff": 2
            },
            "summary": {
                "transcribe_time": "0:00:03.967500",
                "word_error_rate": 0.012195121951219513,
                "match_error_rate": 0.03951752632280421,
                "character_error_rate": 0.010548523206751054,
                "word_information_lost": 0.012048192771084376,
                "word_information_preserved": 0.9879518072289156,
                "phrase_repeat_diff": 2
            }
        },
        "test_audio_2": {
            "run_0": {
                "start_datetime": "05/30/24, 15:11:25",
                "transcribe_time": "0:00:11.942993",
                "word_error_rate": 0.0546448087431694,
                "match_error_rate": 0.05291005291005291,
                "character_error_rate": 0.03714859437751004,
                "word_information_lost": 0.06370357382893543,
                "word_information_preserved": 0.9362964261710646,
                "phrase_repeat_diff": 0
            },
            "run_1": {
                "start_datetime": "05/30/24, 15:11:37",
                "transcribe_time": "0:00:11.962662",
                "word_error_rate": 0.0546448087431694,
                "match_error_rate": 0.05291005291005291,
                "character_error_rate": 0.03714859437751004,
                "word_information_lost": 0.06370357382893543,
                "word_information_preserved": 0.9362964261710646,
                "phrase_repeat_diff": 0
            },
            "summary": {
                "transcribe_time": "0:00:11.952828",
                "word_error_rate": 0.0546448087431694,
                "match_error_rate": 0.05291005291005291,
                "character_error_rate": 0.03714859437751004,
                "word_information_lost": 0.06370357382893543,
                "word_information_preserved": 0.9362964261710646,
                "phrase_repeat_diff": 0
            }
        }
    },
    "test_summary": {
        "transcriptions_per_audio": 2,
        "transcribe_time": "0:00:07.960164",
        "word_error_rate": 0.03341996534719446,
        "match_error_rate": 0.04621378961642856,
        "character_error_rate": 0.023848558792130548,
        "word_information_lost": 0.037875883300009905,
        "word_information_preserved": 0.9621241166999901,
        "phrase_repeat_diff": 1
    }
}
```

### AddToExistingTest Class

<!-- #### Required Packages/Downloads
- JiWER &rarr; `$ pip install jiwer`
- openai-whisper &rarr; `$ pip install -U openai-whisper` -->

#### Constructor
`AddToExistingTest(existing_test_json, dataset_path, model, prompt_function=no_prompt, output_dir=getcwd())` : Creates AddToExistingTest instance
- `String existing_test_json` : JSON file created from a previous test
- `String dataset_path` : Dataset to be further tested (should be same as dataset used in provided JSON)
- `ModelWrapper model` : Model to be further tested (should be same as model used in provided JSON)
- `Method prompt_function` : Prompt function to be further tested (should be same as prompt function used in provided JSON)
- `String output_dir` : Directory where test output will be stored, defaults to current working directory.

#### Methods
- `run(run_name, run_num=1, output_file_name=None)` : Adds test runs and updates provided test JSON with new run information
    - `String run_name` : Name of run
    - `int run_num` : Number of test runs to add
    - `String output_file_name` : New JSON result file name (optional, defaults to file name of existing json)
- `free()` : Removes and frees select attributes from memory

#### Results
After running, a 'results/RUN_NAME/' folder in the current working directory will be created. This folder will contain an updated JSON result file with both previous and new test information.



## Transcribe.py

### Transcribe Class
See [Transcribe.ipynb](examples/Transcribe.ipynb) for an example of how to use this class.

<!-- #### Required Packages/Downloads
- openai-whisper &rarr; `$ pip install -U openai-whisper` -->

#### Constructor
`Transcribe(model_array, prompt_function_array=[no_prompt], output_dir=getcwd())` : Creates Transcribe instance
- `ModelWrapper[] model_array` : Array of models to use for transcriptions
- `Method[] prompt_function_array` : Array of prompt loading functions to to use for transcriptions (defaults to contain provided prompt loading function, `no_prompt()`, which returns an empty string)
- `String output_dir` : Directory where transcription output will be stored, defaults to current working directory.

#### Methods
- `run(run_name, input_path, normalize=False)` : Creates transcription for audio in provided dataset or folder
    - `String run_name` : Name of run
    - `String input_path` : Path to dataset or folder full of mp4 files to transcribe
    - `Boolean normalize` : Boolean indicating whether or not to include normalized transcriptions alongside untouched transcriptions
- `free()` : Removes and frees select attributes from memory

#### Results
After running, a 'transcriptions/RUN_NAME/' folder in the current working directory (or whichever output_dir is provided) will be created. This folder will contain the transcriptions of each audio sample in the provided dataset. If `normalize` is set to `True`, this folder will also contain the normalized transcriptions of each audio sample in the provided dataset



## How to Implement a Model Wrapper

### ModelWrapper Interface

In order to be compatible with the Test class, a Model Wrapper class must have `name`, `transcription`, `vtt`, `load_time`, and `transcribe_time` attributes, as well as a `transcribe()` method. Using the [ModelWrapper.py](ModelWrapper.py) interface ensures that all required attributes and methods are implemented in a Model Wrapper class. 

```
from ModelWrapper import ModelWrapper

class YOUR_WRAPPER_NAME(ModelWrapper):
    name = ""
    transcription = {}
    vtt = {}
    load_time = {}
    transcribe_time = {}

    def load():
        pass

    def unload():
        pass

    def transcribe(self, audio_name, audio_file, prompt=None, output_dir=getcwd()):
        pass

    ...
```

### Using Your Wrapper

Put your model wrapper class file in the [models/](models/) folder. Import the wrapper using `from models.YOUR_WRAPPER_NAME import YOUR_WRAPPER_NAME`



## Datasets

### Provided Datasets
- [Full Dataset](datasets/full_dataset/)
- [Development Dataset](datasets/dev_dataset/)

### Other Datasets
Datasets must have the following structure in order to be used with the [Test](#test-class) class:
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

Benchmark using this dataset by using the `dataset_path` parameter when instatiating the [Test](#test-class) class.



## Creating a Summary HTML File
See [create_test_summary.ipynb](examples/create_test_summary.ipynb) for an example of the following steps put together.

### Importing 'create_test_summary_html()'
`from create_test_summary.TestSummary import create_test_summary_html`

### Using 'create_test_summary_html()'

`create_test_summary_html(results_folder, filename="test_summary.html")` : Creates HTML file that displays test summary information with a table and bar chart.
- `String results_folder` : File path to results folder containing result test model JSON files
- `String filename` : Output name for HTML file, defaults to `test_summary.html`

## Using 'test-hyperparams.py'

### Login To Weights and Biases Via Command Line

`$ wandb login [ACCOUNT_KEY]`

### Run 'test_hyperparams.py'

`python3 test_hyperparams.py`
