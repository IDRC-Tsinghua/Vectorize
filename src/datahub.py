#-*- coding:utf-8 -*-
import utils
import word_cutting
from vectorize import Vectorize
import json
import operator
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

def get_node_from_origin_line(line, vectorize):
    """ Form a NODE structure from origin line
    Parameters:
    -----------
    line: just one line from txt
          type: str

    vectorize: the vectorize object
    Return:
    -------
    node: an node-structure dict
              type: str
              format: {"id": "xx",
                       "threadid",
                       "number": "xx",
                       "username": "xx",
                       "text": "xx",
                       "parent": "xx",
                       "children": "{xx, xx, xx}"
                       "depth": "xx",
                       "label": "xx",
                       "vector": "{ k1:v1, k2:v2, k3:v3  }",
                       "emoji": "{xx, xx, xx, xx}",
                       "mention": "{xx, xx, xx, xx}",
                       "hashtag": "{xx, xx, xx, xx}"
                      }
    """

    data = line.split("\t")
    nodestr = ""
    node_id = data[1]
    node_number = data[2]
    node_name = data[3].replace("\"", "")
    node_text = data[4]
    node_parent = data[5]
    # skip the children!!!!!
    # Update: do not skip the children
    child_str = data[6].replace("\"", "")
    node_children = child_str.split(",")
    node_depth = data[7]
    node_valid = data[12]
    if node_valid != "NULL":
        node_label = node_valid
    else:
        node_label = data[8]

    # text pre-process
    emoji_list, node_text = word_cutting.filter_emoji_from_text(node_text)
    mention_list, node_text = word_cutting.filter_syntax_from_text(node_text, '@')
    hashtag_list, node_text = word_cutting.filter_syntax_from_text(node_text, '#')

    # dictionary init
    node_words = word_cutting.cut(node_text)
    bow_vector = vectorize.get_bow_vector(node_words)
       
    nodejson = {}
    nodejson['id'] = node_id
    nodejson['number'] = node_number
    nodejson['name'] = node_name
    nodejson['parent'] = node_parent
    # update children
    nodejson['children'] = node_children
    nodejson['depth'] =node_depth
    nodejson['label'] = node_label

    nodejson['vector'] = bow_vector

    nodejson['emoji'] = emoji_list
    nodejson['mention'] = mention_list
    nodejson['hashtag'] = hashtag_list


    return nodejson, bow_vector



def main():
    """
    """
    print "==========vectorize dict init...============"
    vectorize = Vectorize()
    # prepare str list list words
    vectorize.dict_init_from_file("../data/weiboV2.tsv")

    
    print "==========load sample data==========="
    sample_lines = utils.get_lines_from_file_useful("../data/weiboV2.tsv")
    print len(sample_lines)

    # begin to write files
    print "============begin to write files============"
    temp_id = ""
    temp_strs = []
    cur = 0

    print "=========== word appear count stat"
    word_count_stat = {}

    for line in sample_lines:
        node, bow_vector = get_node_from_origin_line(line, vectorize) # json dict
        for [index, cnt] in bow_vector:
            index = str(index)
            if word_count_stat.get(index) != None:
                word_count_stat[index] = word_count_stat[index] + cnt
            else:
                word_count_stat[index] = 1

        nodestr = json.dumps(node)
        """
        if temp_id != node.get('id'):
            with open("../res/res_%d.txt" % cur, "w") as file_ob:
                # print "----write to %d file now ----" % cur
                for line in temp_strs:
                    file_ob.write(line + "\n")
            file_ob.close()
            # re init
            cur = cur + 1
            temp_id = node.get('id')
            temp_strs = []
            temp_strs.append(nodestr)
        else:
            temp_strs.append(nodestr)
        """
    sorted_cnt = sorted(word_count_stat.items(), key=operator.itemgetter(1),
                        reverse=True)
    dictionary_dict = vectorize.get_token2id()
    print "dict len", len(dictionary_dict)
    print "sorted len", len(sorted_cnt)
    print "word_count_dict stat: ", len(word_count_stat)
    with open("word_dict.txt", "w") as file_ob:
        
        for (k, cnt) in sorted_cnt:
            for (name, index) in dictionary_dict.items():
                if index == int(k):
                    # print index, name.encode("utf-8"), cnt, vectorize.word_pesg_tbl[name]
                    line = str(index) + "\t" \
                           + str(name.encode("utf-8")) + "\t" \
                           + str(cnt) + "\t" \
                           + str(vectorize.word_pesg_tbl[name])
                    file_ob.write(line)
                    file_ob.write("\n")
                    break
    file_ob.close()

    with open("token_dict.txt", "w") as file_ob:
        for (k,v) in dictionary_dict.items():
            line = str(k.encode("utf-8")) + "\t" + str(v)
            file_ob.write(line)
            file_ob.write("\n")
    file_ob.close()
    
    """
    if temp_strs != []:
        with open("../res/res_%d.txt" % cur, "w") as file_ob:
            # print "----write to %d file now ----" % cur
            for line in temp_strs:
                file_ob.write(line + "\n")
        file_ob.close()
    """

    """
    sorted_cnt = sorted(word_count_stat.items(), key=operator.itemgetter(1),
                        reverse=True)
    # sorted_cnt = sorted_cnt.reverse()

    print_count = 0
    dictionary_dict = vectorize.get_token2id()

    pseg_list = "v vd vn vshi vyou vf vx vi vl vg a ad an ag al".split(" ")
    for (k,cnt) in sorted_cnt:
        for (name, index) in dictionary_dict.items():
            if index == int(k) and vectorize.word_pesg_tbl[name] in pseg_list:
                print index, name.encode("utf-8"), cnt, vectorize.word_pesg_tbl[name]
                break
        print_count = print_count + 1
    """


    return

if __name__ == "__main__":
    main()
