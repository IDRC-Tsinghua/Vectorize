# -*- coding=utf-8 -*-
import vec_config
import json
from gensim import corpora, models
import word_cutting
import utils
import pdb
"""
Return Function:
----------------

character_to_vectorion

get_dictionary


"""
class Vectorize(object):

    def __init__(self):

        word_cutting.load_thirdparty_words("../dict/favourate.txt")
        self.dictionary = None
        self.word_pesg_tbl = {} # the word-pesg hashtable
	self.words_doc = None
	self.tfidf = None

    def gen_words_doc(self, filepath):
	"""
	"""
	lines = utils.get_line_from_file(filepath)
        texts = utils.get_text_only_from_lines(lines)
        text_filters = []
        for text in texts:
            emoji_list, text_filter = word_cutting.filter_emoji_from_text(text)
            mention_list, text_filter = word_cutting.filter_syntax_from_text(text, '@')
            hashtag_list, text_filter = word_cutting.filter_syntax_from_text(text, '#')
            text_filters.append(text_filter)
        words_doc = []

        for text in text_filters:
            words = word_cutting.cut(text)
            words_doc.append(words)
        """
        for text in text_filters:
            text_pesg = word_cutting.cut_with_pseg(text)
            
            # set the pesg to the hashtable
            for word_pesg in text_pesg:
                self.word_pesg_tbl[word_pesg.word] = word_pesg.flag

            doc = []
            doc = [w.word for w in text_pesg]
            words_doc.append(doc)
        """
        # filter stop words
        stop_words = word_cutting.get_stopwords()
        ## test
        words_doc = [[word for word in doc if word.encode("utf-8") not in stop_words] for doc in words_doc]
	self.words_doc = words_doc
	return

    def dict_init_from_file(self, filepath):
        """
        """
        # words_doc = [[] for doc in words_doc]
        self.dict_init_from_texts(self.words_doc)
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
        # print self.dictionary
        return self.dictionary

    def get_token2id(self):
        return self.dictionary.token2id

    def print_token2id(self):
        for (k, v) in self.dictionary.token2id.items():
            #print type(k), type(v)
            print k.encode("utf-8"), v
        return

    def get_bow_vector(self, words):
        """

        """
        assert(self.dictionary != None)
        bow_vector = self.dictionary.doc2bow(words)
        return bow_vector
	
    def tfidf_init(self):
	"""
	"""
        print "=== tf-idf init ==="
        index_doc = [self.get_bow_vector(words) for words in self.words_doc]
	self.tfidf = models.TfidfModel(index_doc) 
	return

    def get_tfidf(self, doc):
	"""
	transfor the doc to the tfidf space
	"""
	assert(self.tfidf) != None
	return self.tfidf[doc]

