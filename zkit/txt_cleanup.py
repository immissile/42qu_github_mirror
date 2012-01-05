#coding:utf-8
from collections import defaultdict

CN_CHAR = 1
EN_CHAR = 2
STOP_CHAR = 3


def _en(char):
    if len(char) > 3:
        v = []
        for i in char:
            if '.' <= i <= 'z':
                v.append(i)
        if v:
            return ''.join(v) , EN_CHAR


def _cn_en_iter(line):
    line = line.decode('utf-8', 'ignore')
    pre_char = []
    for i in line:
        if i.isdigit() or '.' <= i <= 'z':
            pre_char.append(i)
        else:
            if pre_char:
                r = _en(''.join(pre_char))
                if r:
                    yield r
                pre_char = []
            if u'\u4e00' <= i < u'\u9fa6':
                yield i, CN_CHAR
            else:
                yield i, STOP_CHAR

    r = _en(''.join(pre_char))
    if r:
        yield r

def _iter(line):
    for char, is_word in _cn_en_iter(line):
        yield char.encode('utf-8', 'ignore'), is_word

def line_iter(line):
    for i in _line_iter(line):
        if i and len(i) > 1:
            yield ''.join(i)

def _line_iter(line):
    char_buffer = []
    for char, word_type in _iter(line):
        if word_type is not STOP_CHAR:
            char_buffer.append(char)
        else:
            yield char_buffer
            char_buffer = []
    if char_buffer:
        yield char_buffer

if __name__ == '__main__':
    for i in line_iter("""
第一次听说google的simhash算法[1]时，我感到很神奇。传统的hash算法只负责将原始内容尽量均匀随机地映射为一个签名值，原理上相当于伪随机数产生算法。传统hash算法产生的两个签名，如果相等，说明原始内容在一定概率下是相等的；如果不相等，除了说明原始内容不相等外，不再提供任何信息，因为即使原始内容只相差一个字节，所产生的签名也很可能差别极大。从这个意义上来说，要设计一个hash算法，对相似的内容产生的签名也相近，是更为艰难的任务，因为它的签名值除了提供原始内容是否相等的信息外，还能额外提供不相等的原始内容的差异程度的信息。

    因此当 我知道google[[https://google.com]]的simhash算法产生的签名，可以用来比较原始内容的相似度时，便很想了解这种神奇的算法的原理。出人意料，这个算法并不深奥，其思想是非常清澈美妙的。

simhash算法的输入是一个向量，输出是一个f位的签名值。为了陈述方便，假设输入的是一个文档的特征集合，每个特征有一定的权重。比如特征可以是文档中的词，其权重可以是这个词出现的次数。simhash算法如下：
"""):
        #tf-idf 最大的50词 , 按tf-idf排序
        if len(i) > 20:
            print i


