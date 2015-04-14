#-*- coding:utf-8 -*-
import vec_config


""" =================== file and text process
"""


def get_lines_from_file_useful(filepath):
    """ get lines from file which label1 = label2 and label1 != 2 or NULL

    Parameters:
    -----------
    filepath: the data path in the system
              type: str

    Return:
    -------
    lines : all data in the file
            type: str list list
    """
    lines = []
    with open(filepath) as file_ob:
        for line in file_ob:
            data = line.split("\t")
            label1 = data[7]
            label2 = data[9]
            if (label1 == label2) and (label1 != "NULL") and (label1 != "2"):
                lines.append(line)
    file_ob.close()
    return lines


def get_texts_from_file(filename):
    """

    """
    texts = []
    with open(filename, "r") as file_ob:
        for line in file_ob:
            texts.append(line)
    file_ob.close()
    return texts


def get_text_only_from_lines(lines):

    texts = []
    for line in lines:
        data = line.split("\t")
        texts.append(data[3])
    return texts

def write_to_file(data, file_name):
    """ write the data to the file

    Parameters:
    -----------
    data: just the data, always is a LIST
    file_name: contain file_path and file_name exactly,
               for example: "../data/chinese_data.txt"
               type: str
    Returns:
    --------
    None

    """
    with open(file_name, 'w') as file_ob:
        for data_line in data:
            file_ob.write(data_line + "\n")
    file_ob.close()
    return

def main():

    from_filepath = "../data/Interstellar.tsv"
    lines = get_lines_from_file_useful(from_filepath)
    texts = get_text_only_from_lines(lines)
    to_file_path = "../data/Ins_text.txt"
    write_to_file(texts, to_file_path)

if __name__ == "__main__":
    main()
