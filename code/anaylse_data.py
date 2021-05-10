"""
    Created by ningyuguang.2021-05-10
    用于分析筹文本数据分布情况
"""
import json
from rouge import Rouge


def cal_rouge(a, b):
    """
        a = ["I am a student from xx school"]
        b = ["I am a student from school on china"]
    :param a: 筹转发标题
    :param b: 筹案例描述
    :return: 召回率是以b为基准/每个句子的召回率再求平均
    """
    # a = ["I am a student from xx school", "the cat was found under the bed"]
    # b = ["I am a student from school on china", "the cat was under the bed"]

    if len(a) == 0 or len(b) == 0:
        return 0
    rouge = Rouge()
    rouge_score = rouge.get_scores(a, b, avg=True)

    idx = {"1": rouge_score["rouge-1"]['r'], "2": rouge_score["rouge-2"]['r'], "l": rouge_score["rouge-l"]['r']}

    return idx["1"]


def get_file_rouge():
    with open('../data/record.csv', 'r', encoding='utf-8') as f:
        line = f.readline()
        que = 0
        text = []
        title = []
        number = 0
        result_prob = 0
        result_numb = 0
        while line:
            each_line = line.split('\t')
            if number % 100 == 0 and number != 0:
                recall = cal_rouge(text, title)
                result_prob += recall * len(title)
                result_numb += len(title)
                text = []
                title = []
                print("当前已处理的数据", number)
            if len(each_line) != 2:
                que += 1
                continue
            else:
                title.append(each_line[0])
                text.append(each_line[1])
            line = f.readline()
            number += 1
        print("有问题的样本数量有:", que)

def get_file_basic():
    with open('../data/record.csv', 'r', encoding='utf-8') as f:
        line = f.readline()
        title = []
        text = []
        badcase = 0
        process = 0
        while line:
            each_line = line.split("\t")
            if process % 1000 == 0:
                print("Finish the task:", process)
            if len(each_line) != 2:
                badcase += 1
                continue
            title.append(len(each_line[0]))
            text.append(len(each_line[1]))
            line = f.readline()
            process += 1
    return





if __name__ == '__main__':
    # get_file_rouge()
    get_file_basic()
    # cal_rouge('a', 'b')