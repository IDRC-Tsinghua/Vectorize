#-*- coding:utf-8 -*-
import json
import jieba
import data_filter
import re
from parse import *
import vec_config

def cut(text):
    """ cut words to list from jieba

    Parameters:
    -----------
    texts: the single sentence.
           type: str

    Returns:
    --------
    list(seg_list):
                    type: str list
    """
    seg_list = jieba.cut(text, cut_all=False)
    # print " /".join(seg_list)

    # filter the stopwords
    stop_words = get_stopwords()
    seg_list = [word for word in seg_list if word not in stop_words]
    return list(seg_list)

""" ================== emoji mention and hashtag process
"""



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
    with open(vec_config.stopwords_path) as file_ob:
        for line in file_ob:
            stopwords_list.append(line)
        file_ob.close()

    return stopwords_list


def get_emoji():
    """
    Parameters:
    -----------
    None

    Returns:
    --------
    emoji_list:
                type: str list



    """
    emoji_list = []
    with open(vec_config.emoji_path, "r") as file_ob:
        for emoji in file_ob:
            # delete \n
            emoji = emoji.strip("\n")
            emoji_list.append(emoji)
    file_ob.close()
    return emoji_list

def filter_emoji_from_text(text):
    """
    """
    emoji_list = get_emoji()
    emoji_res = []
    # get all emoji that appeared
    # not delete the emoji in this turn, for store the repeate emoji
    for emoji in emoji_list:
        if emoji in text:
            emoji_res.append(emoji)

    # delete all emoji from origin text
    text_filter = text
    for emoji in emoji_res:
        text_filter = text_filter.replace(emoji, "")


    return emoji_res, text_filter

def filter_syntax_from_text(text, syntax='@'):
    """
    Parameters:
    -----------
    text: one line string
          type: str

    syntax: the mark parse character
            type: char
    """
    mention_list = []

    c_flag = False
    mention = ""
    for c in text:
        if c == syntax:
            c_flag = True
        if c_flag == True:
            if c != ' ':
                mention = mention + str(c)
            else:
                # end mention
                # delete the syntax char
                mention_list.append(mention.decode("utf-8")[1:-1])
                # delete mention from origin text
                text = text.replace(mention, "")
                # re_init
                mention = ""
                c_flag = False
    return mention_list, text

def get_weibos():
    regex = re.compile(r"\b(\w+)\s*:\s*([^:]*)(?=\s+\w+\s*:|$)")
    weibo_list = []
    with open("../data/mahang_dat.txt") as file_ob:
        next(file_ob)
        for line in file_ob:
            items = dict(regex.findall(line))
            word = items.get("text")
            if word:
                weibo_list.append(word.decode("utf-8"))
    return weibo_list



if __name__ == "__main__":


    """
    emoji_list, text = filter_emoji_from_text("今天天气不错[笑哈哈][草泥马]")
    print emoji_list, text

    mention_list, text = filter_syntax_from_text("今天天气不错@火神 #天气预报  ", '@')
    print mention_list, text
    hashtag_list, text = filter_syntax_from_text(text, '#')
    print hashtag_list, text
    """
