import whisper
from whisper.utils import get_writer
from os.path import isdir
from os import mkdir
from model_constants import OUTPUT_FOLDER

WRAPPER_FOLDER = "whisper-openai/"

# model_type can be "tiny", "base", "small", "medium", or "large"
def transcribe(audio, prompt="", model_type="large", language="en", options={"max_line_width": None, "max_line_count": None, "highlight_words": False}):

    output_dir = OUTPUT_FOLDER + WRAPPER_FOLDER

    if not isdir(OUTPUT_FOLDER):
        mkdir(OUTPUT_FOLDER)
    if not isdir(output_dir):
        mkdir(output_dir)

    print("Creating transcription for " + audio + " using Whisper AI " + model_type + " model.")

    # load model
    model = whisper.load_model(model_type)

    # transcribe video
    result = model.transcribe(audio, initial_prompt=prompt, language=language)

    # create .txt file
    txt_writer = get_writer("txt", output_dir)
    txt_writer(result, audio, options)

    # # create .vtt file
    # vtt_writer = get_writer("vtt", output_dir)
    # vtt_writer(result, audio, options)

    # # create .srt file
    # srt_writer = get_writer("srt", output_dir)
    # srt_writer(result, audio, options)
