# -*- coding: utf-8 -*-
import json


def gen_vectors_from_jsondata(self, fliename):
    """
    """
    with open(filename, "r") as file_ob:
        for line in file_ob:
            node_json = json.loads(line.strip())
            node_vector = node_json['vector']
            node_label = node_json['']
    return


def topic_polarity_stats():
    """
    """
    
def main():
    topic_polarity_stats()

if __name__ == "__main__":
    main()
