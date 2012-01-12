#coding:utf-8
from collections import defaultdict

CN_CHAR = 1
EN_CHAR = 2
STOP_CHAR = 3


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
            else:
                yield i, STOP_CHAR

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
    pre_word_type = 0
    for char, word_type in _iter(line):
        if word_type != STOP_CHAR or pre_word_type == EN_CHAR:
            char_buffer.append(char)
        elif char_buffer:
            yield char_buffer
            char_buffer = []
        pre_word_type = word_type
    if char_buffer:
        yield char_buffer

from hashes.simhash import simhash as _simhash
def simhash(txt):
    return _simhash(line_iter(txt), 64)

if __name__ == '__main__':
    txt1 = """
1　引言

据统计,互联网上的重复网页约占 30%~45%。这其中有由于镜像转载引起的内容完全相同的网页,也有仅存在微小差别的网页,比如广告,计数器,时间戳等不同,而这些差别是和搜索的内容无关的。根据中国互联网络信息中心2005年7月发布的统计报告显示,用户在回答“检索信息时遇到的最大问题”这一提问时,选择“重复信息太多”选项的占 44.6%,排名第1位[1]。将相似的网页消除,可以节省网络带宽,减少占用的存储空间,提高索引的质量,即提高查询服务的效率和质量,同时减轻网页所在远程服务器的负担。在网页查重算法中shingling和simhash被认为是当前最好的两个算法。

2　Shingling算法 Shingling主要是为

了发现大致相同的文档,即内容相同,除了格式上的变动,微小的修改、签名和logo的不同。同时,也可以发现一个文档“大致包含”在另一个之中。文中首先用数学的概念严格定义了什么叫“大致相同”:两个文档A和B之间的相似度是介于0和1之间的一个数字,这样如果这个数字接近1,那么这两个文档就是“大致相同”的。包含度的定义与此相同。计算两个文档之间的相似度和包含度,只为两个文档保留几百字节的sketch 就可以了。Sketch的计算效率比较高,时间上和文档的大小成线性关系,而给出两个sketch,它们所对应的文档的相似度和包含度的计算在时间上和这两个sketch的大小成线性关系[2]。

该算法把文档看做文字组成的序列,首先把它词法分析为标示(token)序列,忽略一些微小的细节,比如格式,html命令,大小写。然后把文档D和标示的子串所组成的集合S(D,W)联系起来。D中的相邻子串称为shingle。给出一个文档D, 定义它的w-shinglingS(D,W)为D中所有大小为W的不同的shingle。比如,(a,rose,is,a,rose,is, a, rose)的4-shingling就是集合: {(a,rose,is,a),(rose,is,a,rose),(is,a,rose,is)}给定shingle的大小,两个文档A和B的相似度r 定义为:r(A,B)=|S(A)∩S(B)|S(A)∪S(B)因此,相似度是介于0和1之间的一个数值,且r(A,A)=1,即一个文档和它自身 100%相似。给定一个shingle大小W,U是所有大小为W的shingle的集合。不失一般性,我们可以把U看做一个数值的集合。现在设定一个参数 S,对于一个集合W U,定义Mins(w)为:Mins(w)=w中最小的s个元素组成的集合;|w|≥s;w;其他情况;其中“最小”是指U中元素的数值顺序。并且定义 modm(w)=集合W中所有可以被m整除的元素的集合定理:让π:U→U为U统一选定的随机排列,F(A)=MINS(π(S(A))),V(A)=MODM(π(S(A))),F(B)和V(B)同样定义。那么:|MINS(F(A)∪F(B))∩F(A)∩F(B)||MINS(F(A)∪F(B))|是A和B相似度的无偏估计;|V(A)∩V(B)||V(A)∪V(B)|是A和B相似度的无偏估计;由上面的公式可知,我们可以选择一个随机排列,然后为每个文档保留一个 sketch,这个sketch仅仅由F(D)和V(D)组成。仅通过这些sketch我们就可以估计任何一对文档的相似度或者包含度,而不需要原始文件。在文中的系统中,生成sketch方法如下:.移除文档的HTML格式,将所有文字转化为小写;. shingle的大小为10;.用改进后的基于robin fingerprints的40位指纹函数进行随机排列;.用求模取余的方法来选择shingle,m的值选取25。将此算法应用到整个网络的具体步骤为:.取得网络上的文档;.计算每个文档的sketch;.比较每对文档的sketch,看它们是否超过了一定的相似阈值;

.聚类相似文档。

算法很简单,但是简单的实施却不切实际。从网上抓取的大小为30,000,000HTML和文本文档集合做试验,需O(1015)次成对比较,这显然不可行。输入数据的数据量对数据结构的设计和算法都有很大的限制,数据结构中每个文档1位需4M。每个文档一个800字节的sketch需 24G。每个文档微秒级计算总共需8个小时。如果算法有随机的硬盘存取或者有页面活动产生就完全不可行。在文中的算法设计中,通过一个简单的方法来处理数据量大的问题—分割,计算,合并。将数据切割成块,单独计算每一块然后再合并结果。选择块大小为m这样整个计算过程可以在内存中进行。合并结果很简单但是非常消耗时间,因为涉及到I/O操作。单独一次合并是线性级别的,但是全部的操作需要log(n/m),所以整个处理过程是0(nlog(n/m))级别的。
"""
    txt2 = txt1+"""输入是一个向量，输出是一个f位的签名值。为了陈述方便，假设输入的是一个文档的特征集合，每个特征有一定的权重。比如特征可以是文档中的词，其权重可以是这个词出现的次数。simhash算法如：
"""
    _hash1 = simhash(txt1)
    _hash2 = simhash(txt2)


    print _hash1.hamming_distance(_hash2)


