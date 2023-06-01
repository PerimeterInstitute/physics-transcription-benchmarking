from os.path import isfile
import jiwer

class Test():

    def __init__(self, dataset):

        # initializing resultsJSON
        self.resultsJSON = {}

        # load dataset transcription
        filepath = "./datasets/" + dataset + "/" + dataset + ".txt"
        
        if isfile(filepath):
            self.reference = filepath  
        else: 
            raise Exception("ERROR: Dataset '" + dataset + "' does not exist.")

    def createJSON(self, hypothesis):

        # PREPARING INPUT:

        reference = open(self.reference, "r").read()
        hypothesis = open(hypothesis, "r").read()

        # COMPARING INPUT:

        word_output = jiwer.process_words(reference, hypothesis)
        char_output = jiwer.process_characters(reference, hypothesis)

        # CREATING JSON:

        self.resultsJSON.update({"word_error_rate": word_output.wer})
        self.resultsJSON.update({"match_error_rate": word_output.mer})
        self.resultsJSON.update({"word_information_lost": word_output.wil})
        self.resultsJSON.update({"word_information_preserved": word_output.wip})
        self.resultsJSON.update({"character_error_rate": char_output.cer})

        return self.resultsJSON
    