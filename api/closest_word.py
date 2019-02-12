import numpy as np
import logging


class Closest_Word:

    def __init__(self, filename = "glove.6B.50d.txt"):
        self.filename    = filename
        self.num_words   = None
        self.vector_dim  = None
        self.words       = {}
        self.words_vec   = []
        self.data_loaded = False

    def get_number_of_words(self, reload = False):
        if(not self.num_words or reload):
            self.num_words = sum(1 for line in open(self.filename))
        return(self.num_words)

    def get_vector_dim(self, reload = False):
        if(not self.vector_dim or reload):
            f = open(self.filename, "r")
            first_line = f.readline().split()
            vector = first_line[1:len(first_line)]
            self.vector_dim = len(first_line)-1
            f.close()
            return(self.vector_dim)

    def load(self, reload = False):
        if not self.data_loaded or reload:
            logging.info("Loading data set ...")
            self.num_words  = self.get_number_of_words(reload)
            self.vector_dim = self.get_vector_dim(reload)
            self.words_vec  = [0] * self.num_words
            self.vectors    = np.zeros((self.num_words, self.vector_dim))

            index = 0
            f  = open(self.filename, "r")
            for line in f:
                line = line.split()
                word = line[0]
                self.words_vec[index]      = word
                self.words[word]           = {}
                self.words[word]["vector"] = line[1:len(line)]
                self.words[word]["index"]  = index
                self.vectors[index]        = line[1:len(line)]
                index = index + 1

            self.data_loaded = True
            f.close()
            logging.info("Data set loaded.")

    def find_closest_words(self, word, N):
        word          = word.lower()
        N             = int(N)
        closest_words = []
        result        = {}

        if(N < 1):
            message = "N has to be larger than 0."

        elif(word in self.words and N > 0):
            message = ""
            if(N >= self.num_words):
                N = self.num_words-1
                message = "N larger than available words. "
            index       = self.words[word]["index"]
            word_vector = self.vectors[index]
            matrix      = self.vectors - word_vector
            norms       = np.linalg.norm(matrix, axis=1)
            indices     = np.argpartition(norms, range(N+1))[1:(N+1):]

            for index in indices:
                logging.debug(repr(self.words_vec[index]) + " " + repr(norms[index]))
                closest_words.append(self.words_vec[index])

            message = message + "Success."

        else:
            message = word + " could not be found in the dictionary."

        result["words"]   = closest_words
        result["message"] = message
        return(result)
