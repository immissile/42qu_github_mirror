#coding:utf-8
from collections import defaultdict

CN_CHAR = 1
EN_CHAR = 2
SIGN_CHAR = 3
STOP_CHAR = 4
SPACE_CHAR = 5

SPACE_CHAR_SET = u" 　"
STOP_CHAR_SET = set(u";.。\n")

def _en(char):
    if len(char) >= 2:
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

            if u'\u4e00' <= i and i < u'\u9fa6':
                yield i, CN_CHAR
            elif i in STOP_CHAR_SET:
                yield i, STOP_CHAR
            elif i in SPACE_CHAR_SET:
                yield ' ', SPACE_CHAR
            else:
                yield i, SIGN_CHAR

    r = _en(''.join(pre_char))
    if r:
        yield r

def _iter(line):
    for char, word_type in _cn_en_iter(line):
        yield char.encode('utf-8', 'ignore'), word_type

def line_iter(line):
    for i in _line_iter(line):
        yield ''.join(i)

def _line_iter(line):
    char_buffer = []
    pre_word_type = SPACE_CHAR
    for char, word_type in _iter(line):
        if word_type != STOP_CHAR:
            if (pre_word_type==STOP_CHAR or pre_word_type == SPACE_CHAR) and word_type == SPACE_CHAR:
                continue
            char_buffer.append(char)
        elif char_buffer:
            yield char_buffer
            char_buffer = []
        pre_word_type = word_type
    if char_buffer:
        yield char_buffer

from heapq import nlargest
from hashlib import md5
def feature(txt, limit=64):
    lines = nlargest(limit, [i for i in line_iter(txt) if len(i)>30], key=len)
    return lines

def feature_md5(txt, limit=64):
    result = [md5(i).hexdigest() for i in feature(txt, limit)]
    return result

def title_normal_sign(title):
    title = title\
            .replace('【', '[')\
            .replace('】', ']')\
            .replace('［', '[')\
            .replace('］', ']')\
            .replace('（', '(')\
            .replace('）', ')')\
            .replace('：', ':').strip()

    return title

def sp_txt(txt):
    txt = title_normal_sign(txt)

    if str(txt).replace(" ",'').isalnum():
        yield txt 
    else:
        for i in _line_iter(txt):
           # for n in xrange(len(i)-1):
           #     if not i[n].isspace():
           #         yield ''.join(i[n:n+2])

            for pos,char in enumerate(i):
                if not char.isspace():
                    if pos+2 <= len(i):
                        yield ''.join(i[pos:pos+2])
                

if __name__ == '__main__':
    txt1 = """
Use this command to anonymously check out the latest project source code:
今年央视春晚请走不少老面孔，起初是语言类节目的顶梁柱频频出局，没想到一贯稳定的主持人阵容上也同声共气，飞走了央视当家主持人周涛，迎来了85后小美女李思思。1986年出生的李思思2005年以大学生身份参加《挑战主持人》节目，连任8期擂主后，次年以全国选拔赛季军的身份进入央视。在央视她主持《舞蹈世界》，主持过两届央视舞蹈大赛，并不显山露水，这次登上春晚舞台前，她离春晚最近的一次是主持2011年春晚前的“倒计8小时”直播节目。前天，李思思在春晚彩排的一号演播大厅露面，外界想到了她将登上春晚舞台，却没想到她替下的竟是周涛。

　　另外，记者昨天获悉，影视演员王珞丹(微博)将在开场歌舞中亮相。开场歌舞作为春晚第一炮，不仅要给观众最好的“第一眼”印象，同时也是过去一年里当红艺人的展示舞台。

　　对比近几年的春晚开场，虎年春晚以歌舞大联欢引导主持出场，兔年春晚则主打“山楂树组合”，到龙年春晚由王珞丹等“新鲜”面孔混搭朱军、李咏、老毕组成的“霸气男人帮”阵容，“鲜”字概念逐年突显。
"""
    txt2 = '输入是一个向量，\n'+txt1+"""\n输出是一个f位的签名值。为了陈述方便，假设输入的是一个文档的特征集合，每个特征有一定的权重。比如特征可以是文档中的词，其权重可以是这个词出现的次数。simhash算法如：
"""
    #64 3 肯定有16位是一样的


    #原始 10 . 11 00 01
    #1<>0 11 . 10 00 01
    #2<>0 00 . 10 11 01
    #3<>0 01 . 10 11 00 

    #搜索 为4份 每个到对应的key下面找
    #再分4份
    for i in sp_txt(txt1):
        print i

    #for i in feature(txt1):
    #    print i

    #for i in feature_md5(txt1):
    #    print repr(i)
#key md5 - value array doc_id
#defaultdict doc_id[same_count]
#feature_len
#if same_count> feature_len*.618 
