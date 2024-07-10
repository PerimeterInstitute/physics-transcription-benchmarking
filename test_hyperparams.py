from Test import Test
from os.path import join, isfile
from models.WhisperCPP import WhisperCPP
from helper_functions.prompt_functions import get_formatted_description
import wandb, json

sweep_configuration = {
    "method": "random",
    "metric": {"goal": "maximize", "name": "accuracy"},
    "parameters": {
        # beam search params:
        "beam_size": {"values": [1, 5, 8]},
        # "patience": {"values": [-1, 0.5, 1.0, 2.0]},                                # explained in this paper: https://arxiv.org/pdf/2204.05424

        # best of search params:
        "best_of": {"values": [1, 5, 8]},

        # temperature params:
        # "temperature": {"values": [0.0]},                                           # lower temperature is better, so start here!
        # "temperature_inc": {"values": [0.2]},                           

        # threshold params:
        "logprob_threshold": {"values": [-0.1, -0.3, -0.5, -1]},
        "no_speech_threshold": {"values": [0.2, 0.4]},
        "entropy_threshold": {"values": [1.5, 2.0, 2.4]},                         # idk how this works lol. called 'compression threshold' in og whisper --> if "gzip compression ratio" is higher, decoding has failed. Lower values are more strict
        # "word_threshold": {"values": [0.01]},                                     # also dk how this works. no idea what this variable is called in og whisper
    },

    # "parameters": {
    #     # beam search params:
    #     "beam_size": {"values": [5]},
    #     # "patience": {"values": [-1]},                                           # idk how this affects the beam search.

    #     # best of search params:
    #     "best_of": {"values": [5]},

    #     # temperature params:
    #     "temperature": {"values": [0]},                                           # {"values": [0, 0.2, 0.4, 0.6]},
    #     "temperature_inc": {"values": [0.2]},

    #     # threshold params:
    #     "logprob_threshold": {"values": [-0.1, -0.3, -0.5, -1]},
    #     "no_speech_threshold": {"values": [0.2, 0.4, 0.6]},
    #     "entropy_threshold": {"values": [2.4]},                                   # idk how this works lol. called 'compression threshold' in og whisper
    #     "word_threshold": {"values": [0.01]},                                     # also dk how this works. no idea what this variable is called in og whisper
    # },
}
sweep_id = wandb.sweep(sweep=sweep_configuration, project="test-whisper")

def main():

    wandb.init()

    # GET HYPERPARAM VALUES:

    # have to remake whisper cpp to use:
    # temperature = wandb.config.temperature
    # temperature_inc = wandb.config.temperature_inc
    no_speech_threshold = wandb.config.no_speech_threshold
    # patience = wandb.config.patience

    # can control from command line:
    beam_size = wandb.config.beam_size
    best_of = wandb.config.best_of
    logprob_threshold = wandb.config.logprob_threshold
    entropy_threshold = wandb.config.entropy_threshold
    # word_threshold = wandb.config.word_threshold

    # CHECK IF WE NEED TO MAKE CLEAN MODEL:

    filename = "./hyperparams.json"
    remake_model = False
    hyperparams = {}
    prev_temperature = None
    prev_temperature_inc = None
    prev_no_speech_threshold = None

    # get prev hyperparams
    if isfile(filename):
        with open(filename, "r") as file:
            hyperparams = json.load(file)
            # prev_temperature = hyperparams["prev_temperature"]
            # prev_temperature_inc = hyperparams["prev_temperature_inc"]
            prev_no_speech_threshold = hyperparams["prev_no_speech_threshold"]

    # check for changes
    # if temperature != prev_temperature or temperature_inc != prev_temperature_inc or no_speech_threshold != prev_no_speech_threshold:
    #     remake_model = True
    if no_speech_threshold != prev_no_speech_threshold:
        remake_model = True

    # set prev hyperparam values
    # hyperparams.update({"prev_temperature": temperature})
    # hyperparams.update({"prev_temperature_inc": temperature_inc})
    hyperparams.update({"prev_no_speech_threshold": no_speech_threshold})
    with open(filename, "w") as new_file:
        json.dump(hyperparams, new_file)

    # CREATE MODEL:

    new_model = WhisperCPP("cpp" + \
                           "_bs" + str(beam_size) + \
                           "_bo" + str(best_of) + \
                        #    "_temp" + str(temperature) + \
                        #    "_tempinc" + str(temperature_inc) + \
                           "_lpt" + str(logprob_threshold) + \
                           "_nst" + str(no_speech_threshold) + \
                           "_et" + str(entropy_threshold),
                        #    "_wt" + str(word_threshold),

                            "/gpfs/rmohl/whisper.cpp/",
                            {
                                "model_type": "large-v2",
                                "--beam-size": beam_size,
                                "--best-of": best_of,
                                "--logprob-thold": logprob_threshold,
                                "--entropy-thold": entropy_threshold,
                                # "--word-thold": word_threshold,
                            }
    )

    if remake_model:

        # update whisper.cpp file!
        with open(join(new_model.path_to_whispercpp + "whisper.cpp"), "r") as file:
            text = file.readlines()

        with open(join(new_model.path_to_whispercpp + "whisper.cpp"), "w") as new_file:
            for line in text:

                # if "temperature       =" in line:
                #     line = "\t\t/*.temperature       =*/  " + str(temperature) + ",\n"
                # if "temperature_inc   =" in line:
                #     line = "\t\t/*.temperature_inc   =*/  " + str(temperature_inc) + "f,\n"
                if "no_speech_thold   =" in line:
                    line = "\t\t/*.no_speech_thold   =*/  " + str(no_speech_threshold) + "f,\n"
                # if "patience  =" in line:
                #     line = "\t\t\t/*.patience  =*/ " + str(no_speech_threshold) + "f,\n"

                new_file.write(line)

        # make clean
        new_model.makeClean()

    test = Test([new_model],
                prompt_function_array=[get_formatted_description],
                output_dir="/gpfs/rmohl/")
    

    # test.run(run_name="wandb_test",
    #         dataset_path="/gpfs/rmohl/datasets/secrets_full_vid_dataset/", 
    #         run_num=10,
    #         save_transcription=True)
    # test.run(run_name="wandb_test",
    #         dataset_path="/gpfs/rmohl/datasets/poor_audio_full_vid_dataset/", 
    #         run_num=10,
    #         save_transcription=True)
    test.run(run_name="wandb_secrets_full_vid",
            dataset_path="/gpfs/rmohl/datasets/secrets_full_vid_dataset/", 
            run_num=3,
            save_transcription=True)
    
    results = test.most_recent_run_results["test_summary"]

    wandb.log(
        {
            "accuracy": results["word_information_preserved"],
            "time": results["transcribe_time"],
            "phrase_repeat_diff": results["phrase_repeat_diff"],
        }
    )

    test.free()

wandb.agent(sweep_id, function=main)
