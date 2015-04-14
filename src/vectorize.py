# -*- coding=utf-8 -*-
import config
import json
from gensim import corpora, models
import word_cutting
import utils

"""
Return Function:
----------------

character_to_vector

get_dictionary


"""
class Vectorize(object):

    def __init__(self):

        self.dictionary = None

    def dict_init(self, words_texts):
        """ change all words in the texts to numeric vector

        Parameters:
        -----------
        words_texts: two dimension list
               type: str list list

        Return:
        -------
        dictionary: the dictionary of corpora
                    type: gensim.corpora.dictionary.Dictionary
        """
        dictionary = corpora.Dictionary(words_texts)
        dictionary.save(config.dictionary_path)
        print dictionary
        return dictionary

    def get_token2id(self):
        return self.dictionary.token2id

    def get_bow_vector(self, text):
        """

        """
        words = word_cutting.cut(text)
        assert(self.dictionary != None)
        bow_vector = self.dictionary.doc2bow(text)
        return bow_vector

def main():
    vectorize = Vectorize()
    texts = utils.get_texts_from_file("../data/Ins_text.txt")
    words_texts = []
    vectorize.dict_init()

    return

if __name__ == "__main__":
    main()
