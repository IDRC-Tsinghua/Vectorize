# -*- coding=utf-8 -*-
import vec_config
import json
from gensim import corpora, models
import word_cutting
import utils

"""
Return Function:
----------------

character_to_vectorion

get_dictionary


"""
class Vectorize(object):

    def __init__(self):

        self.dictionary = None

    def dict_init_from_file(self, filepath):
        """
        """
        lines = utils.get_lines_from_file_useful(filepath)
        texts = utils.get_text_only_from_lines(lines)
        text_filters = []
        for text in texts:
            emoji_list, text_filter = word_cutting.filter_emoji_from_text(text)
            mention_list, text_filter = word_cutting.filter_syntax_from_text(text, '@')
            hashtag_list, text_filter = word_cutting.filter_syntax_from_text(text, '#')
            text_filters.append(text_filter)
        words_doc = []
        for text in text_filters:
            words_doc.append(word_cutting.cut(text))
        self.dict_init_from_texts(words_doc)

        return

    def dict_init_from_texts(self, words_texts):
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
        self.dictionary = corpora.Dictionary(words_texts)
        self.dictionary.save(vec_config.dictionary_path)
        print self.dictionary
        return self.dictionary

    def get_token2id(self):
        return self.dictionary.token2id

    def get_bow_vector(self, words):
        """

        """
        assert(self.dictionary != None)
        bow_vector = self.dictionary.doc2bow(words)
        return bow_vector

def main():
    vectorize = Vectorize()
    texts = utils.get_texts_from_file("../data/Ins_text.txt")
    words_texts = []
    vectorize.dict_init()

    return

if __name__ == "__main__":
    main()
