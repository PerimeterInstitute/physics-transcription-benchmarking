import gc
from os import getcwd
from os.path import join
from datetime import timedelta
from time import time

import nemo.collections.asr as nemo_asr
from models.ModelWrapper import ModelWrapper


class Parakeet(ModelWrapper):

    name = "nvidia/parakeet-tdt-0.6b-v2"
    transcription = {}
    vtt = {}
    load_time = {}
    transcribe_time = {}

    def __init__(self, options=None):
        self.options = options or {}
        self.asr_model = None

    def load(self):
        start = time()
        self.asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name=self.name)
        end = time()
        self.load_time = str(timedelta(seconds=end - start))

    def unload(self):
        del self.asr_model
        gc.collect()

    def transcribe(self, audio_name, audio_file, prompt=None, output_dir=getcwd()):
        start = time()

        # Transcribe with timestamps
        output = self.asr_model.transcribe([audio_file], timestamps=True)
        result = output[0]
        end = time()

        self.transcribe_time[audio_name] = str(timedelta(seconds=end - start))
        self.transcription[audio_name] = result.text
        self.vtt[audio_name] = self.__generate_vtt(result.timestamp.get("segment", []))

        # Optionally save output files
        self.__write_output(audio_name, result.text, self.vtt[audio_name], output_dir)

    def __write_output(self, audio_name, text, vtt_text, output_dir):
        txt_path = join(output_dir, f"{audio_name}.txt")
        vtt_path = join(output_dir, f"{audio_name}.vtt")

        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            with open(vtt_path, "w", encoding="utf-8") as f:
                f.write(vtt_text)
        except Exception as e:
            print(f"Failed to write outputs: {e}")

    def __generate_vtt(self, segments):
        lines = ["WEBVTT\n"]
        for idx, seg in enumerate(segments):
            start = self.__format_timestamp(seg["start"])
            end = self.__format_timestamp(seg["end"])
            text = seg["segment"]
            lines.append(f"{idx+1}\n{start} --> {end}\n{text}\n")
        return "\n".join(lines)

    def __format_timestamp(self, seconds):
        millis = int((seconds % 1) * 1000)
        total_seconds = int(seconds)
        mins, secs = divmod(total_seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02}.{millis:03}"
