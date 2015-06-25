# -*- coding: utf-8 -*-
import os
import json
import pdb


def gen_vectors_from_jsondata(filename):
    """
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
            vector = (node_label, [v[0] for v in node_vector ])
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
    pdb.set_trace()
    return vector_list
        

def calculate_info_gain():
    """
    """
    
    return


def main():
    print "foobar"
    gen_all_data("../data/fold_data/")
    return

if __name__ == "__main__":
    main()
