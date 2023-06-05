from os import listdir
import jiwer

class Test():

    def __init__(self, model):

        # initializing resultsJSON
        self.results = {}

        for dataset in listdir("./datasets/"):
           reference = open("./datasets/" + dataset + "/" + dataset + ".txt", "r").read()
           self.results.update({dataset: self.compare(reference, model.transcription)})

    def compare(self, reference, hypothesis):

        currentTest = {}

        # COMPARING INPUT:

        word_output = jiwer.process_words(reference, hypothesis)
        char_output = jiwer.process_characters(reference, hypothesis)

        # CREATING JSON:

        currentTest.update({"word_error_rate": word_output.wer})
        currentTest.update({"match_error_rate": word_output.mer})
        currentTest.update({"word_information_lost": word_output.wil})
        currentTest.update({"word_information_preserved": word_output.wip})
        currentTest.update({"character_error_rate": char_output.cer})

        return currentTest
    
    