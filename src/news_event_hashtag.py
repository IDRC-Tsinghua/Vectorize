#-*- coding:utf-8 -*-
import word_cutting


if __name__ == "__main__":
    hashtag_dict = {}
    with open("../data/NewsEvent.tsv", "r") as file_ob:
        next(file_ob)
        for line in file_ob:
            data = line.split("\t")
            node_number = data[1]
            node_text = data[3]
            if node_number != "0":
                continue

            hashtag_list, node_text = word_cutting.filter_syntax_from_text(node_text, "#")
            for tag in hashtag_list:
                if hashtag_dict.get(tag) == None:
                    hashtag_dict[tag] = 1
                else:
                    hashtag_dict[tag] = hashtag_dict[tag] + 1
    file_ob.close()

    for (k,v) in hashtag_dict.items():
        print k,v

    pass
