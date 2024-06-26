# Model Wrappers
- [WhisperPI](#whisperpi)
- [WhisperOpenAI](#whisperopenai)
- [WhisperCPP](#whispercpp)
- [WhisperCPPQuantized](#whispercppquantized)
- [AzureSpeechToText](#azurespeechtotext-note-this-wrapper-is-not-up-to-date-with-the-modelwrapper-format-and-does-not-work)

## WhisperPI
Wrapper for the WhisperPI transcription model. WhisperPI is an altered version of [OpenAI's Whisper](https://github.com/openai/whisper) speech recognition model, used to transcribe videos on the Perimeter Institute Recorded Seminar Archive (PIRSA).

### Required Packages/Downloads
- pi-whisper &rarr; `$ pip install git+https://github.com/PerimeterInstitute/whisper.git`
- FFmpeg &rarr; `$ sudo apt install ffmpeg`

### Constructor
`WhisperPI(name, options)` : Creates WhisperPI instance
- `String name` : Name of model
- `Dict options` : Model options (includes `model_type`, `language`, `temperature`, and other options offered by [OpenAI's Whisper](https://github.com/openai/whisper))

### Attributes
- `String name` : Name of model
- `String model_type` : Model type ("tiny", "base", "medium", "large", etc.)
- `Dict options` : Model options
- `Dict transcription` : Dictionary containing the text from all transcriptions
- `Dict vtt` : Dictionary containing the VTT file text from all transcriptions
- `Dict load_time` : Dictionary containing all load times
- `Dict transcribe_time` : Dictionary containing all transcribe times
- `Dict result_object` : Dictionary containing all result objects

### Methods
- `load()` : Loads model
- `unload()` : "Unloads" model (i.e. removes select model attributes from memory)
- `transcribe(audio_name, audio_file, prompt=None, output_dir=getcwd())` : Transcribes given audio file, updates result-related attributes
    - `String audio_name` : Name associated with audio
    - `String audio_file` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to `None`
    - `String output_dir` : Directory where temp output will be stored, defaults to current working directory.
- `get_model()` : Returns Whisper model


## WhisperOpenAI
Wrapper for [OpenAI's Whisper](https://github.com/openai/whisper) speech recognition model.

### Required Packages/Downloads
- openai-whisper &rarr; `$ pip install -U openai-whisper`
- FFmpeg &rarr; `$ sudo apt install ffmpeg`

### Constructor
`WhisperOpenAI(name, options)` : Creates WhisperOpenAI instance
- `String name` : Name of model
- `Dict options` : Model options (includes `model_type`, `language`, `temperature`, and other options offered by [OpenAI's Whisper](https://github.com/openai/whisper))

### Attributes
- `String name` : Name of model
- `String model_type` : Model type ("tiny", "base", "medium", "large", etc.)
- `Dict options` : Model options
- `Dict transcription` : Dictionary containing the text from all transcriptions
- `Dict vtt` : Dictionary containing the VTT file text from all transcriptions
- `Dict load_time` : Dictionary containing all load times
- `Dict transcribe_time` : Dictionary containing all transcribe times
- `Dict result_object` : Dictionary containing all result objects

### Methods
- `load()` : Loads model
- `unload()` : "Unloads" model (i.e. removes select model attributes from memory)
- `transcribe(audio_name, audio_file, prompt=None, output_dir=getcwd())` : Transcribes given audio file, updates result-related attributes
    - `String audio_name` : Name associated with audio
    - `String audio_file` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to `None`
    - `String output_dir` : Directory where temp output will be stored, defaults to current working directory.
- `get_model()` : Returns Whisper model


## WhisperCPP
Wrapper for the [Whisper C++](https://github.com/ggerganov/whisper.cpp) speech recognition model.

### Required Packages/Downloads
- whisper.cpp &rarr; `$ git clone https://github.com/ggerganov/whisper.cpp.git`

### Constructor
`WhisperCPP(name, path_to_whispercpp, options)` : Creates WhisperCPP instance
- `String name` : Name of model
- `String path_to_whispercpp` : Path to whisper.cpp git repository
- `Dict options` : Model options (includes `--language`, `--beam-size`, `--entropy-thold`, and other options offered by [Whisper C++](https://github.com/ggerganov/whisper.cpp/blob/master/README.md))

### Attributes
- `String name` : Name of model
- `String model_type` : Model type ("base.en", "medium.en", "large-v2", etc.)
- `Dict options` : Model options
- `Dict transcription` : Dictionary containing the text from all transcriptions
- `Dict vtt` : Dictionary containing the VTT file text from all transcriptions
- `Dict load_time` : Dictionary containing all load times
- `Dict transcribe_time` : Dictionary containing all transcribe times

### Methods
- `load()` : Loads model.
- `unload()` : "Unloads" model (i.e. removes select model attributes from memory)
- `transcribe(audio_name, audio_file, prompt=None, output_dir=getcwd())` : Transcribes given audio file, updates result-related attributes
    - `String audio_name` : Name associated with audio
    - `String audio_file` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to `None`
    - `String output_dir` : Directory where temp output will be stored, defaults to current working directory.
- `makeClean()` : Cleans whisper.cpp repository according to makefile instructions


## WhisperCPPQuantized
Wrapper for the [Whisper C++](https://github.com/ggerganov/whisper.cpp) speech recognition model.

### Required Packages/Downloads
- whisper.cpp &rarr; `$ git clone https://github.com/ggerganov/whisper.cpp.git`

### Constructor
`WhisperCPPQuantized(name, path_to_whispercpp, options)` : Creates WhisperCPPQuantized instance
- `String name` : Name of model
- `String path_to_whispercpp` : Path to whisper.cpp git repository
- `Dict options` : Model options (includes `quantize type` in addition to all options offered by [Whisper C++](https://github.com/ggerganov/whisper.cpp/blob/master/README.md))

### Attributes
- `String name` : Name of model
- `String model_type` : Model type ("base.en", "medium.en", "large-v2", etc.)
- `Dict options` : Model options
- `Dict transcription` : Dictionary containing the text from all transcriptions
- `Dict vtt` : Dictionary containing the VTT file text from all transcriptions
- `Dict load_time` : Dictionary containing all load times
- `Dict transcribe_time` : Dictionary containing all transcribe times

### Methods
- `load()` : Loads model.
- `unload()` : "Unloads" model (i.e. removes select model attributes from memory)
- `transcribe(audio_name, audio_file, prompt=None, output_dir=getcwd())` : Transcribes given audio file, updates result-related attributes
    - `String audio_name` : Name associated with audio
    - `String audio_file` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to `None`
    - `String output_dir` : Directory where temp output will be stored, defaults to current working directory.
- `makeClean()` : Cleans whisper.cpp repository according to makefile instructions


## AzureSpeechToText (NOTE: This wrapper is not up to date with the ModelWrapper format and does not work!)
Wrapper for Azure's speech recognition model.

### Required Packages/Downloads
- Azure Cognitive Services Speech SDK &rarr; `$ pip install azure-cognitiveservices-speech`

### Constructor
`AzureSpeechToText(name, key, region, options)` : Creates AzureSpeechToText instance
- `String name` : Name of model
- `String key` : Azure subscription key
- `String region` : Region name (see [regions](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/regions))
- `Dict options` : Model options (includes `speech_recognition_language`, `endpoint`, `host`, and other options offered by [Azure's Cognitive Services Speech SDK](https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechconfig?view=azure-python#constructor))

### Attributes
- `String name` : Name of model
- `String key` : Azure subscription key
- `String region` : Region name
- `Dict options` : Model options
- `Dict transcription` : Dictionary containing the text from all transcriptions
- `Dict vtt` : Dictionary containing the VTT file text from all transcriptions (NOTE: VTT functionality has not been implemented for this model wrapper yet)
- `Dict load_time` : Dictionary containing all load times
- `Dict transcribe_time` : Dictionary containing all transcribe times

### Methods
- `load()` : Loads model
- `unload()` : "Unloads" model (i.e. removes select model attributes from memory)
- `transcribe(audio_name, audio_file, prompt=None)` : Transcribes given audio file, updates result-related attributes
    - `String audio_name` : Name associated with audio
    - `String audio_file` : File path to audio file
    - `String prompt` : Transcription prompt, defaults to `None` (NOTE: prompts have not been implemented for this model wrapper yet)
- `get_speech_config()` : Returns Azure speech configuration object
