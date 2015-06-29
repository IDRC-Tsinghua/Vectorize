# -*- coding: utf-8 -*-
import os
import json
import pdb
import math
import operator
from vectorize import Vectorize 

def gen_vectors_from_jsondata(filename):
    """

    Return:
    -------
    vector_list: the vector that contain the label and word index

    """
    # the vector list's format: [ [1, [1,2,3,4]], [2,[4,5,62]]
    vector_list = []

    with open(filename, "r") as file_ob:
        for line in file_ob:
            node_json = json.loads(line.strip())
            node_vector = node_json.get("vector")
            node_label = node_json.get("label")
            if node_vector == None:
                continue
            vector = [node_label, [v[0] for v in node_vector ]]
            vector_list.append(vector)

    file_ob.close()
    return vector_list

def gen_all_data(rootpath):
    """
    the root folder's structure:
    data/ fold_0/1/2/3 / 0/1/2/3/4...txt

    Parameters:
    -----------
    rootpah: the root folder's path
             type: string
    """
    vector_list = []
    for (cur, dirs, files) in os.walk(rootpath):
        # get each fold_data folder
        for folder in dirs:
            for (_cur, _dirs, _files) in os.walk(cur+folder):
                for filename in _files:
                    vector_list += gen_vectors_from_jsondata(_cur+"/"+filename)
    # pdb.set_trace()
    return vector_list

def gen_tfidf():
    """
    """
    vectorize = Vectorize()
    vectorize.gen_words_doc("../data/weibo.tsv")
    vectorize.tfidf_init()
    return vectorize


def gen_prob_table(vector_list, len_of_idx, len_of_doc):
    """
    generate the probability of each token(germ)
    about the p(t) which denote the prob that the term t accure in the all docs.
    and the p(c|t) which denote the prob that the term t accure in the doc which
    label is c.

    params:
    -----------
    vector_list: a structured list that contain the label and corresponding word
                 vector.
                 type: list. example: [(1, [45,7,1231,3]), (0, [545,12,5,1])]

    len_of_idx: the length of word index.
                type: int

    len_of_doc: the length of document.
    returns:
    --------
    prob_tbl: the dict that store all the p(t) and p(c|t) given t.
              type: dict,
              format: {"idx": ( sum(t), sum(c_{-1}|t),      )}

    """
    prob_tbl = dict( (k, [0.0]*4) for k in xrange(1, len_of_idx))

    for item in vector_list:
        y = item[0]
        vec = item[1]
        for v in vec:
            # sum(t) acc
            prob_tbl[v][0] += 1
            # sum(c|t) acc
            prob_tbl[v][y+2] += 1

    # calculate the result
    for idx in xrange(1,len_of_idx):
        if prob_tbl[idx][0] == 0:
            continue
        print idx
        prob_tbl[idx][1] /= prob_tbl[idx][0]
        prob_tbl[idx][2] /= prob_tbl[idx][0]
        prob_tbl[idx][3] /= prob_tbl[idx][0]
        prob_tbl[idx][0] /= len_of_doc

    prob_non_tbl = dict( (k, [0.0]*4) for k in xrange(1, len_of_idx))

    print "=== narrow bottle ==="
    for item in vector_list:
        y = item[0]
        vec = item[1]
        for idx in xrange(1, len_of_idx):
            if idx not in vec:
                prob_non_tbl[idx][0] += 1
                prob_non_tbl[idx][y+2] += 1
        # print "next..", cur

    for idx in xrange(1, len_of_idx):
        if prob_non_tbl[idx][0] == 0:
            continue
        prob_non_tbl[idx][1] /= prob_non_tbl[idx][0]
        prob_non_tbl[idx][2] /= prob_non_tbl[idx][0]
        prob_non_tbl[idx][3] /= prob_non_tbl[idx][0]
        prob_non_tbl[idx][0] /= len_of_doc
    return prob_tbl, prob_non_tbl

def save_prob_tbl(filepath, prob_tbl):
    """
    """
    with open(filepath, "w") as file_ob:
        for k, v in prob_tbl.items():
            line = str(k)
            line += str(v)
            file_ob.write(line)
	file_ob.close()
    return

def gen_prob_y(vector_list):
    """
    """
    prob_y = dict( (c, 0.0) for c in xrange(-1, 2))
    for item in vector_list:
        y = item[0]
        prob_y[y] += 1

    y_all = sum([v for k,v in prob_y.items()])
    for c in xrange(-1,2):
        prob_y[c] /= y_all
    return prob_y

def calculate_info_gain(vector_list, len_of_idx, len_of_doc):
    """
    calculate the information gain by the probability table.

    """
    info_gain = dict( (k, 0.0) for k in xrange(1, len_of_idx))

    prob_y = gen_prob_y(vector_list)
    prob_tbl, prob_non_tbl = gen_prob_table(vector_list, len_of_idx, len_of_doc)

    H_C = sum([p_y * math.log(p_y,2) for k, p_y in prob_y.items() ])

    for idx in xrange(1, len_of_idx):
        p_t = prob_tbl[idx][0] or 1
        p_c_neg_given_t = prob_tbl[idx][1] or 1
        p_c_neu_given_t = prob_tbl[idx][2] or 1
        p_c_pos_given_t = prob_tbl[idx][3] or 1

        p_non_t = prob_non_tbl[idx][0] or 1
        p_non_c_neg_given_t = prob_non_tbl[idx][1] or 1
        p_non_c_neu_given_t = prob_non_tbl[idx][2] or 1
        p_non_c_pos_given_t = prob_non_tbl[idx][3] or 1

        # Trick debug
        print "p_t", p_t
        print "p_c_neg_given_t", p_c_neg_given_t
        print "p_c_neu_given_t", p_c_neu_given_t
        print "p_c_pos_given_t", p_c_pos_given_t
        print "p_non_t", p_non_t
        print "p_non_c_neg_given_t", p_non_c_neg_given_t
        print "p_non_c_neu_given_t", p_non_c_neu_given_t
        print "p_non_c_pos_given_t", p_non_c_pos_given_t

        info_gain[idx] = H_C + \
                         p_t * p_c_neg_given_t * math.log(p_c_neg_given_t, 2) + \
                         p_non_t * p_non_c_neg_given_t * math.log(p_non_c_neg_given_t, 2) + \
                         p_t * p_c_neu_given_t * math.log(p_c_neu_given_t, 2) + \
                         p_non_t * p_non_c_neu_given_t * math.log(p_non_c_neu_given_t, 2) + \
                         p_t * p_c_pos_given_t * math.log(p_c_pos_given_t, 2) + \
                         p_non_t * p_non_c_pos_given_t * math.log(p_non_c_pos_given_t, 2)
        print idx
        print info_gain[idx]
    return info_gain


def main():
    print "foobar"
    vector_list = gen_all_data("../data/fold_data/")
    #prob_tbl = gen_prob_table(vector_list,19902 ,14733)
    #prob_y = gen_prob_y(vector_list)
    info_gain = calculate_info_gain(vector_list, 19902, 14733)
    sorted_ig = sorted(info_gian.items(), key=operator.itemgetter(0))
    sorted_ig = sorted_ig.reverse()
    verbose = 100
    cur = 0
    for k, v in sorted_ig.items():
        if cur < verbose:
            print k
            cur += 1
        else:
            break
    pdb.set_trace()
    return

if __name__ == "__main__":
    main()
