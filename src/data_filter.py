# -*- coding=utf-8 -*-
import config
import json
from gensim import corpora, models, similarities

"""
Return Function:
----------------

get_text_from_file

write_to_file

get_stopwords

character_to_vector

"""

def get_text_from_file(path):
    """ get the pure chinese line from file

    Parameters:
    -----------
    path: the data path in the system.

    Return:
    -------
    texts: format: [["aa bb cc"],["a  sd  d"]..  ]
           all the character here is Chinese
           type: str list list
    """
    texts = []
    with open(path) as file_ob:
        for line in file_ob:
            line_json = json.loads(line) # string to json
            # from unicode to str
            word_with_property = line_json.get("text").encode("utf-8")
            words = word_with_property.split(" ")
            # from each line we get a word_list at last
            word_list = [word.split("/")[0] for word in words]
            texts.append(word_list)

    return texts



def write_to_file(data, file_name):
    """ write the data to the file

    Parameters:
    -----------
    data: just the data, always is a LIST
    file_name: contain file_path and file_name exactly,
               for example: "../data/chinese_data.txt"

    Returns:
    --------
    None

    """
    with open(file_name, 'w') as file_ob:
        for data_line in data:
            file_ob.write(data_line + "\n")
    file_ob.close()
    return

def get_stopwords():
    """ get the stopwords list from file

    Parameters:
    -----------
    None

    Return:
    -------
    stopwords: the stopwords list
               type: str list

    """
    stopwords_list = []
    with open(config.stopwords_path) as file_ob:
        for line in file_ob:
            stopwords_list.append(line)
        file_ob.close()

    return stopwords_list



def character_to_vector(texts):
    """ change all word in the texts to numeric vector

    Parameters:
    -----------
    texts: two dimension list
           format: str list list

    Returns:
    --------
    dictionary:

    """

    dictionary = corpora.Dictionary(texts)
    dictionary.save("../data/words.dict")
    token2id = dictionary.token2id

    texts_vec = dictionary.doc2bow(texts[0])
    print texts_vec
    return dictionary

def main():
    """ the main function

    """

    print "prepare text..."
    texts = get_text_from_file(config.frozen_data_path)

    print "prepare stopwords..."
    stopwords = get_stopwords()

    print "filter stopwords from texts..."
    texts = [ [word for word in text if word not in stopwords] for text in texts ]

    print "get directory by corpora..."
    dictionary = character_to_vector(texts)



    return

if __name__ == "__main__":
    main()
