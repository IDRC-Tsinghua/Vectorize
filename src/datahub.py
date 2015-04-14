#-*- coding:utf-8 -*-
import utils
import word_cutting
from vectorize import Vectorize

"""
description:

the origin data format:

id  number  "username"  "text"  parent  "children"  depth  label1  "user1"  label2  "user2"  valid

"""

def get_text_from_line(line):
    """ get the weibo text from one line

    Parameters:
    -----------
    line: one line
          type: str

    Return:
    -------
    text: type: str

    """
    row_data = line.split("\t")
    text = row_data[3]
    return text




def get_nodestr_from_origin_line(line, vectorize):
    """ Form a NODE structure from origin line
    Parameters:
    -----------
    line: just one line from txt
          type: str

    vectorize: the vectorize object
    Return:
    -------
    node-str: an node-structure string
              type: str
              format: {"id": "xx",
                       "number": "xx",
                       "name": "xx",
                       "text": "xx",
                       "parent": "xx",
                       "depth": "xx",
                       "label": "xx",
                       "vector": "{ k1:v1, k2:v2, k3:v3  }",
                       "emoji": "{xx, xx, xx, xx}",
                       "mention": "{xx, xx, xx, xx}",
                       "hashtag": "{xx, xx, xx, xx}"
                      }
    """

    nodestr = ""
    node_id = line[0]
    node_number = line[1]
    node_name = line[2]
    node_text = line[3]
    node_parant = line[4]
    # skip the children!!!!!
    node_depth = line[6]
    node_label = line[7]

    # text pre-process
    emoji_list, node_text = word_cutting.filter_emoji_from_text(node_text)
    mention_list, node_text = word_cutting.filter_syntax_from_text(node_text, '@')
    hashtag_list, node_text = word_cutting.filter_syntax_from_text(node_text, '#')

    # dictionary init
    node_words = word_cutting.cut(node_text)
    print node_words
    bow_vector = vectorize.get_bow_vector(node_words)

    nodestr = ""
    nodejson = {}
    nodejson['id'] = node_id
    nodejson['number'] = node_number
    nodejson['name'] = node_name
    nodejson['parent'] = node_parent
    nodejson['depth'] =node_depth
    nodejson['label'] = node_label

    nodejson['vector'] = bow_vector

    nodejson['emoji'] = emoji_list
    nodejson['mention'] = mention_list
    nodejson['hashtag_list'] = hashtag_list

    nodestr = json.dump(nodejson)
    print nodestr
    return nodestr



def main():
    """
    """
    vectorize = Vectorize()
    # prepare str list list words
    lines =utils.get_lines_from_file_useful("../data/Interstellar.tsv")
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

    vectorize.dict_init(words_doc)
    print vectorize.get_token2id

    return

if __name__ == "__main__":
    main()
