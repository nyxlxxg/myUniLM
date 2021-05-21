from collections import defaultdict
import json


def longest_common_subsequence(source, target):
    """最长公共子序列（source和target的最长非连续子序列）
    返回：子序列长度, 映射关系（映射对组成的list）
    注意：最长公共子序列可能不止一个，所返回的映射只代表其中一个。
    """
    c = defaultdict(int)
    for i, si in enumerate(source, 1):
        for j, tj in enumerate(target, 1):
            if si == tj:
                c[i, j] = c[i - 1, j - 1] + 1
            elif c[i, j - 1] > c[i - 1, j]:
                c[i, j] = c[i, j - 1]
            else:
                c[i, j] = c[i - 1, j]
    l, mapping = c[len(source), len(target)], []
    i, j = len(source) - 1, len(target) - 1
    while len(mapping) < l:
        if source[i] == target[j]:
            mapping.append((i, j))
            i, j = i - 1, j - 1
        elif c[i + 1, j] > c[i, j + 1]:
            j = j - 1
        else:
            i = i - 1
    return l, mapping[::-1]


def generate_copy_labels(source, target):
    """构建copy机制对应的label
    B:1，表示该token是复制而来
    I:2，表示该token是复制而来而且跟前面Token组成连续片段
    O:0，表示该token不是复制来的
    """
    mapping = longest_common_subsequence(source, target)[1]
    source_labels = [0] * len(source)
    target_labels = [0] * len(target)
    i0, j0 = -2, -2
    for i, j in mapping:
        if i == i0 + 1 and j == j0 + 1:
            source_labels[i] = 2
            target_labels[j] = 2
        else:
            source_labels[i] = 1
            target_labels[j] = 1
        i0, j0 = i, j
    return source_labels, target_labels


if __name__ == '__main__':
    with open('./data/clean_little.csv', "r") as f:
        line = f.readline()
        while line:
            line = json.loads(line)
            src_text = line['src_text']
            tgt_text = line['tgt_text']
            a, b = generate_copy_labels(src_text, tgt_text)
            line = f.readline()