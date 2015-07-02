# -*- coding: utf-8 -*-
import numpy as np
from sklearn.svm import SVC
import json
import pdb
from weibo_dump import get_info_gain_list
from vectorize import Vectorize

def feature_encoding():
    """
    encoding the origin sparse features
    to the new 1000-length feature dict

    matching regulation:
    
    """
    info_gain_list = get_info_gain_list()
    feature_dict = {}
    # pdb.set_trace()
    for i in xrange(999):
        feature_dict[info_gain_list[i]] = i
    return feature_dict

def get_all_emoji_dict():
    emoji_dict = {}
    emoji_htb = {}
    for fold in xrange(5):
        for topicid in xrange(51):
            with open("../data/fold_data/fold_%i/%i.txt" %(fold, topicid)) as file_ob:
                for line in file_ob:
                    json_of_data = json.loads(line)
                    node_emoji = json_of_data["emoji"]
                    for emoji in node_emoji:
                        emoji_htb[emoji] = 1
            file_ob.close()
    start_index = 4000
    for emoji, val in emoji_htb.items():
        emoji_dict[emoji] = start_index
        start_index += 1
    print start_index
    # pdb.set_trace()
    return emoji_dict

def gen_data(feature_dict, emoji_dict, feature_len, vectorize, if_train="train"):
    """
    """
    data_X = []
    data_y = []

    if if_train == "train":
        fold_list = [0,1,3,4]
    else:
        fold_list = [2]
        
    for fold in fold_list:
        for topicid in xrange(51):
            with open("../data/fold_data/fold_%s/%s.txt" \
                      %( str(fold), str(topicid)), "r") as file_ob:
                for line in file_ob:

                    x = [0.]* feature_len
                    y = 0
                    
                    node_json = json.loads(line)
                    node_vector = node_json['vector']
                    node_label = node_json['label']
                    node_emoji  =node_json['emoji']
                    for v in node_vector:
                        f = feature_dict.get(str(v[0]))
                        # pdb.set_trace()
                        if f != None:
                            x[f] = v[1]
                    for e in node_emoji:
                        e_index = emoji_dict.get(e)
                        print e_index
                        if e_index != None:
                            x[e_index] = 1

                    y = int(node_label) + 2
                    # pdb.set_trace()
                    data_X.append(x)
                    data_y.append(y)
    data_X = np.asarray(data_X, dtype=np.float32)
    data_y = np.asarray(data_y, dtype=np.int32)
    
    return data_X, data_y


if __name__ == "__main__":

    # vecoterize init
    vectorize = Vectorize()
    vectorize.gen_words_doc("../data/weiboV2.tsv")
    vectorize.dict_init_from_file("../data/weiboV2.tsv")
    vectorize.tfidf_init()
    
    feature_dict = feature_encoding()
    emoji_dict = get_all_emoji_dict()
    train_X, train_y = gen_data(feature_dict, emoji_dict, 1244, vectorize, "train")
    test_X, test_y = gen_data(feature_dict, emoji_dict, 1244, vectorize, "test")

    clf = SVC(degree=3,
              kernel="rbf",
              class_weight={1:0.2, 2:0.4, 3:0.4})
    print "=== train SVM model... === "
    clf.fit(train_X, train_y)
    pred_y_res = clf.predict(test_X)

    accuracy_cnt = 0
    for pred_y, label_y in zip(pred_y_res, test_y):
        if pred_y == label_y:
            accuracy_cnt += 1
    print accuracy_cnt
    print accuracy_cnt * 1.0 / len(test_y)
    

    
