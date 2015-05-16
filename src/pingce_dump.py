# -*- coding:utf-8 -*-
import json
import vec_config

def generate_dataset_pingce():

    # init
    # one topic one file
    lines_of_topic = {} # key: int, value: [[..], [..] ..]
    lines_of_topic_train = {}
    lines_of_topic_test = {}
    line_numbers = 0
    for i in xrange(51):
        lines_of_topic[str(i)] = []
        
    with open ("../data/weibo.tsv") as file_ob:
        next(file_ob)

        header = "topicid" + "\t" \
                 + "docid" + "\t" \
                 + "username" + "\t" \
                 + "text" + "\t" \
                 + "parent" + "\t" \
                 + "children" + "\t" \
                 + "label"
        print header

        threadid_cur = 0
        thread_group = []
        topic_flag = None
        for line in file_ob:
            """
            id,
            threadid,
            number,
            username,
            text,
            parent,
            children,
            depth,
            label1,
            user1,
            label2,
            user2,
            valid,
            ifrelated1,
            ifrelated2,
            topicid

            """
            
            data_of_line = line.split("\t")
            data_of_line = map(lambda x: x.lstrip().rstrip().replace("\"", ""), data_of_line)
            topicid = int(data_of_line[15])
            threadid = data_of_line[1]
            docid = int(data_of_line[2])
            username = data_of_line[3]
            text = data_of_line[4]
            parent = int(data_of_line[5])
            children = data_of_line[6]

            label1 = data_of_line[8]
            label2 = data_of_line[10]
            valid = data_of_line[12]

            # decide the value of label
            label = ""
            if (label1 == "NULL" or label2 == "NULL" or label1 == "2" or label2 == "2"):
                # abadon data
                continue
            if (valid == "NULL"):
                label = int(label1)
            else:
                label = int(valid)

            json_of_line = {}
            json_of_line['TopicID'] = topicid
            json_of_line['ThreadID'] = threadid
            json_of_line['DocID'] = docid
            json_of_line['UserName'] = username
            json_of_line['Text'] = text
            json_of_line['Parent'] = parent
            json_of_line['Children'] = children
            json_of_line['Label'] = label

            line_numbers = line_numbers + 1
            
            # check if in the same thread
            if threadid == threadid_cur:
                thread_group.append(json.dumps(json_of_line))
            else:
                
                # add the group in the topic backet
                # make a new thread_group
                if topic_flag == None:
                    lines_of_topic[str(topicid)].append(thread_group)
                else:
                    lines_of_topic[str(topic_flag)].append(thread_group)
                threadid_cur = threadid
                thread_group = [] # reinit, important!
                topic_flag = topicid
                thread_group.append(json.dumps(json_of_line))

    lines_of_topic[str(topicid)].append(thread_group)
    file_ob.close()

    print "line_numbers: ", line_numbers
    
    # write all the file
    for i in xrange(51):
        print "writing data %s to the dataset" % str(i)
        with open("../dataset/%s.txt" % (str(i)), "w") as file_ob:
            for thread in lines_of_topic[str(i)]:
                for line in thread:
                    file_ob.write(line)
                    file_ob.write("\n")
        file_ob.close()


        for fold in xrange(5):
            print "write fold %s in topic %s" % (str(fold), str(i))
            with open("../dataset/fold_%s/%s.txt" %(str(fold), str(i)), "w") as file_ob:
                thread_cur = 0
                for thread in lines_of_topic[str(i)]:
                    # fold
                    if thread_cur % 5 == fold:
                        for line in thread:
                            file_ob.write(line)
                            file_ob.write("\n")
                    thread_cur = thread_cur + 1
            file_ob.close()
        
        # write train_set
        # even number to write
        """
        print "writing data %s to the trainingset" % str(i)
        cur = 0
        with open("../training_set/%s.txt" % (str(i)), "w") as file_ob:
            for thread in lines_of_topic[str(i)]:
                if cur % 2 == 0:
                    for line in thread:
                        file_ob.write(line)
                        file_ob.write("\n")
                cur = cur + 1
        file_ob.close()
        print "writing data %s to the testingset" % str(i)
        cur = 0
        with open("../testing_set/%s.txt" % (str(i)), "w") as file_ob:
            for thread in lines_of_topic[str(i)]:
                if cur % 2 == 1:
                    for line in thread:
                        file_ob.write(line)
                        file_ob.write("\n")
                cur = cur + 1
        file_ob.close()
        cur = 0
        """                

def main():
    generate_dataset_pingce()
            
if __name__ == "__main__":
    main()
