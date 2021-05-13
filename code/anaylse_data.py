"""
    Created by ningyuguang.2021-05-10
    用于分析筹文本数据分布情况
"""
import json
from rouge import Rouge
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import re
import sys
import json
sys.setrecursionlimit(2000)

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
    rouge_score = rouge.get_scores(a, b)

    idx = {"1": rouge_score[0]["rouge-1"]['r'], "2": rouge_score[0]["rouge-2"]['r'], "l": rouge_score[0]["rouge-l"]['r']}

    return idx["2"]

def get_file_rouge():
    """
        目标：判断是否使用长文本编码方式还是用短文本编码方式。
        方案：1.建议使用长文本编码方式，因为后面推理的时候，不需要使用滑动窗口。
        2.通过数据说明，案例详情和转发标题关联性比较强的句子通常会出现在哪里？
        3.如果分布相对比较分散，那需要使用长文本编码；如果相对分布比较集中，那可以使用短文本+滑动窗口。
    :param :
    :return:
    """
    with open('../data/chou_single.csv', 'r', encoding='utf-8') as f:
        line = f.readline()
        result = []       # 记录每一个case和标题关联位置
        number = 0
        # 对res中每个list 切四分，头部/中部上/中部下/尾部
        result_dict = {'top':0, 'mid+':0,'mid-':0,'down':0}
        while line:
            each_line = line.strip('\n').split('\t')
            if len(each_line) != 2:
                line = f.readline()
                continue
            if len(each_line[0]) <= 5:
                line = f.readline()
                continue
            if len(each_line[1]) < 512:
                line = f.readline()
                continue
            if number % 100 == 0:
                print("finish number", number)
            title = each_line[0]
            title = re.sub(u"\\(.*?\\)|\\【.*?】", "", title)
            title_space = ''.join([t+" " for t in title]).strip()
            text = each_line[1]
            text_lst = text.split("。")
            line_result = []
            for line in text_lst:
                line_str = ''.join([word+" " for word in line]).strip()
                if len(line_str)==0:
                    continue
                line_result.append(cal_rouge([line_str], [title_space]))
            result.append(line_result)
            number += 1
            line = f.readline()
            if number % 1000 == 0:
                for case in result:
                    step = round(len(case)/4)
                    result_dict['top'] += sum(case[0:step])
                    result_dict['mid+'] += sum(case[step:step*2])
                    result_dict['mid-'] += sum(case[step*2: step*3])
                    result_dict['down'] += sum(case[step*3:])
                result = []
                print(result_dict)


def draw_figure(text, d):
    """
        输入文本数量和转发标题数量
    :param title: title数量列表
    :param text: 文本数量列表
    :return:
    """
    num_bins = (max(text)-min(text))//d + 1
    print(max(text), min(text), max(text)-min(text))
    print(num_bins)

    plt.hist(text, num_bins, range=(min(text), max(text)))
    plt.xticks(range(min(text), max(text)+d, d), rotation=30)

    plt.grid()
    plt.show()


def get_file_basic():
    title = []
    text = []
    badcase = 0
    process = 0
    with open('../data/record.csv', 'r') as f:
        line = f.readline()
        while line:
            each_line = line.split("\t")
            if process % 1000 == 0:
                print("Finish the task:", process)
                print("Bad case num:", badcase)
            if len(each_line) != 2:
                badcase += 1
            else:
                title.append(len(each_line[0]))
                text.append(len(each_line[1]))
            process += 1
            line = f.readline()
    print("标题均值：", np.mean(title), "标题中位数：", np.median(title))
    print("文章均值：", np.mean(text), "文章中位数：", np.median(text))
    return title, text


def words_percent(text, title):
    result_text = {"<128":0, "<256":0, "<512":0, "other":0}
    result_title = {"<3":0, "<10":0, "<25":0, "other":0}
    for t in text:
        if t < 128:
            result_text["<128"] += 1
        elif t >= 128 and t <256:
            result_text["<256"] += 1
        elif t>=256 and t<512:
            result_text["<512"] += 1
        else:
            result_text["other"] += 1
    for t in title:
        if t < 3:
            result_title["<3"] += 1
        elif t >=3 and t < 10:
            result_title["<10"] += 1
        elif t>=10 and t< 25:
            result_title["<25"] += 1
        else:
            result_title["other"] += 1
    total_text = 0
    total_title = 0
    for key, value in result_text.items():
       total_text += value
    for key, value in result_title.items():
        total_title += value
    for key, value in result_text.items():
        result_text[key] = value / total_text
    for key, value in result_title.items():
        result_title[key] = value / total_title
    print(result_text)
    print(result_title)

def check_data():
    """
        查验具体的数据，输出指标较为奇怪的数据
    :param data_path:
    :return:
    """
    with open('../data/chou_single.csv', 'r') as f:
        line = f.readline()
        number = 0
        text = []
        while line:
            each_line = line.strip("\n").split("\t")
            if len(each_line) == 2:
                if len(each_line[1]) > 512:
                    number += 1
                    # text.append(line)
                    print(number)
            line = f.readline()
        print("OK")


def clean_data_title():
    """
        数据清洗
        1.过滤掉转发标题中文[]的内容
    :return:
    """
    with open('../data/chou_single.csv', 'r') as f:
        with open('../data/clean.csv', 'w') as fw:
            line = f.readline()
            while line:
                each_line = line.strip("\n").split("\t")
                if len(each_line) != 2:
                    line = f.readline()
                    continue
                # 筹转发标题处理
                # 去掉中文括号
                title = re.sub(u"\\(.*?\\)|\\【.*?】", "", each_line[0])
                # 去掉emoji符号，去掉非中文内容
                title = re.sub("[^\u4e00-\u9fa5^a-z^A-Z^0-9^！|？|｡|＂|＃|＄|％|＆|＇|（|）|＊|＋|，|－|／|：|；|＜|＝|＞|＠|［|＼|］|＾|＿|｀|｛|｜|｝|～|｟|｠|｢|｣|､|、|〃|》|「|」|『|』|【|】|〔|〕|〖|〗|〘|〙|〚|〛|〜|〝|〞|〟|〰|〾|〿|–|—|‘|’|‛|“|”|„|‟|…|‧|﹏|.]", "", title)
                # 字数限制在10个字以上
                if len(title) <= 10:
                    line = f.readline()
                    continue
                # 筹文本处理
                text = re.sub("[^\u4e00-\u9fa5^a-z^A-Z^0-9^！|？|｡|＂|＃|＄|％|＆|＇|（|）|＊|＋|，|－|／|：|；|＜|＝|＞|＠|［|＼|］|＾|＿|｀|｛|｜|｝|～|｟|｠|｢|｣|､|、|〃|》|「|」|『|』|【|】|〔|〕|〖|〗|〘|〙|〚|〛|〜|〝|〞|〟|〰|〾|〿|–|—|‘|’|‛|“|”|„|‟|…|‧|﹏|.｜]", "", each_line[1])
                if len(text) <= 500 or len(text) >1000:
                    line = f.readline()
                    continue
                # 如果能通过过滤条件则陷入文件
                json_dict = {'src_text': text, 'tgt_text': title}
                d1 = json.dumps(json_dict, ensure_ascii=False)
                fw.write(d1)
                fw.write("\n")

                line = f.readline()




if __name__ == '__main__':
    # 字数统计分析
    # title, text = get_file_basic()
    # words_percent(text, title)
    # draw_figure(title, 3)
    # draw_figure(text, 150)

    # 数据校验
    # check_data()

    # 数据清洗
    clean_data_title()

    # 内容分布分析
    # get_file_rouge()