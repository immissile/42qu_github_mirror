# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
import htmlentitydefs, re

_char = re.compile(r'&(\w+?);')
_dec = re.compile(r'&#(\d{2,4});')
_hex = re.compile(r'&#x(\d{2,4});')

def _char_unescape(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)


import re, htmlentitydefs
def unescape(s):
    # First convert alpha entities (such as &eacute;)
    # (Inspired from http://mail.python.org/pipermail/python-list/2007-June/443813.html)
    def entity2char(m):
        entity = m.group(1)
        if entity in htmlentitydefs.name2codepoint:
            return unichr(htmlentitydefs.name2codepoint[entity])
        return u" "  # Unknown entity: We replace with a space.
    t = re.sub(u'&(%s);' % u'|'.join(htmlentitydefs.name2codepoint), entity2char, s)

    # Then convert numerical entities (such as &#233;)
    t = re.sub(u'&#(\d+);', lambda x: unichr(int(x.group(1))), t)

    # Then convert hexa entities (such as &#x00E9;)
    return re.sub(u'&#x(\w+);', lambda x: unichr(int(x.group(1), 16)), t)


BLOCK_BOLD = set([
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
])

BLOCK = set([
    'form',
    'hr',
    'div',
    'table',
    'tr',
    'li',
    'pre',
    'p',
])

BOLD = set([
    'b',
    'strong',
    'i',
    'em',
])

PASS = set([
    'span',
    'font',
])

def htm2txt(htm):
    htm = htm.replace(u'*', u'﹡')

    soup = BeautifulSoup(htm)

    pic_list = []

    def soup2txt_recursion(soup):
        li = []
        for i in soup:

            if isinstance(i, NavigableString):

                li.append(i.string)

            else:

                name = i.name
                if name == 'img':
                    src = i.get('src')
                    if src:
                        print src
                        if src not in pic_list:
                            pic_seq = len(pic_list) + 1
                            pic_list.append(src)
                        else:
                            pic_seq = pic_list.index(src) + 1
                        li.append(u'\n图:%s\n' % pic_seq)
                else:
                    s = soup2txt_recursion(i)
                    
                    if name in BLOCK_BOLD:
                        li.append(u'\n**%s**\n' % s)
                    elif name in BLOCK:
                        li.append(u'\n%s\n' % s)
                    elif name in BOLD:
                        li.append(u'**%s**' % s)
                    else:
                        li.append(s)

        return u''.join(li)

    s = soup2txt_recursion(soup)
    s = unescape(s)
    return '\n\n'.join(filter(bool, [i.strip() for i in s.splitlines()])), pic_list

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    print htm2txt("""
        <div class="articalContent  " id="sina_keyword_ad_area2">
            <font size="2" face="arial"><span style="line-height: normal;">最近有机会去一个地方城市做教育调研。</span></font><wbr></wbr><font size="2" face="arial"><span style="line-height: normal;">访谈了几个学校的很多老师，教研员，校长，学生，</span></font><wbr></wbr><font size="2" face="arial"><span style="line-height: normal;">包括一些管理者。</span></font><wbr></wbr> <wbr></wbr><font size="2" face="arial"><span style="line-height: normal;">所以我想简单的在这里分享一些我的观感。</span></font>
<div style="font-family: arial; font-size: small; line-height: normal;">
<br></div>
<div>
<div><font size="2"><span style="line-height: 19px;">1.
各位访谈对象对学校的现状都有比较清楚的认识，尤其是校长们。都明白应试教育是根本的问题。如何解决这个问题，或者在这个环境里做的更好，取决于每个人认识的不同，知识的不同，胆略的不同，有不同的看法。</span></font></div>
<div><font size="2"><span style="line-height: 19px;">大家都能认识到应试教育是根本问题所在，但作为既得利益者（或者希望是更大的从现有系统获利），缺乏勇气，也缺乏知识去改变现状。只有极少数人有勇气和知识能力去做些改变。</span></font></div>
</div>
<div>
<div>
<div><span style="background-color: rgb(255, 255, 255);"><font size="2"><span style="line-height: 19px;"><br></span></font></span></div>
<div><font size="2"><span style="line-height: 19px;">a.校长和管理者对问题的实质是很清楚的。这里我们看看校长们的原话是怎么说的。一个校长说他对他的老师们说你们这些老师如果出了学校到社会里都是无法谋生的人。校长也说学校就是监狱。还有一个校长说学校的围墙以后一定会被拆掉的。学校以后不会存在的。这些是校长们讲的。当然不应该排除少数优秀的老师是真的关心孩子的，教学也很认真。这次我们也碰到几个这样的老师。个别的老师凭直觉还是能抓住本学科教学的关键，虽然体制也让他们困惑。</span></font></div>
<div><font size="2"><span style="line-height: 19px;"><br></span></font></div>
<div><font size="2"><span style="line-height: 19px;">b.学生对学校体制的“控诉”（我想这里用这个词应该是恰当的），让我很震惊。</span></font></div>
<br></div>
</div>
<div>
<div><span style="background-color: rgb(255, 255, 255);">2.
我们对人和社会公共事务的冷漠是从小就被培养起来的。这是我参观学校教室后的触动。学生没有任何改变这个系统的机会。只能是被动的接受被教育。造成学生从小就学会了冷漠，虚伪和逢迎。而Sudbury
Valley School最强调的一点就是学生对维护学校环境的责任和对学校建设的参与。</span></div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
<br></div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
3.现在的系统是一个大的庞杂的系统，许多人在其中扮演这不同的角色，每个人学会适应自己的角色。有固定的程序去遵循。大家基本上对这个系统有一个共享的理解。在这个大系统里，也有各种各样的规范的活动来促进教学。并且这些活动在现有的制度框架下应该算已经做得不错的了。</div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
<br></div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
4.
信息技术对学校已经产生很大影响。学校需要信息技术支持。<wbr></wbr>这方面已经没有什么争论。这点我想大家都有共识。<wbr></wbr>老师也已经有经常上网找课件和其他学习资料的习惯。<wbr></wbr>个别学校对信息技术的利用已经很好，覆盖教学的各方面，<wbr></wbr>形式很多样。</div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
<br></div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
5.在现有应试教育的框架下，<wbr></wbr>从老师到教研室到校长等已经动了很多脑筋来以多样的形式来提高教<wbr></wbr>学的质量。所做的确实是大量的工作。<wbr></wbr>不过只有少数的老师和教研员提出让学生自己学，老师少教些，<wbr></wbr>退出些。老师应该退一步海阔天空，不要教的太多了。<wbr></wbr>少数的老师会思考学生到底应该学什么。</div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
<br></div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
6.<wbr></wbr>在老师教研员校长都做了大量工作采用了多种形式的教学活动的情况<wbr></wbr>下，现状仍然是学生不快乐，老师不快乐。这点，<wbr></wbr>大家也都是有共识的。</div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
<br></div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
7.当前的系统内的一些努力，方向是对的，比如强化图书馆，强调阅读，尤其是给学生上课的时间自我阅读，导师制，强调反思等，都是好的方向，抓住了学习的要领。但恐怕还是远远不够。虽然已经是这个系统能做到的最大的改善了。另外特别说一下对语文的教学很多人已经认识到让学生自己多读才是最重要的。而这种认识也慢慢延伸到了其他的学科。特别把这些提出来说一下，肯定目前一些正确的方向。</div>
<div style="font-family: arial, sans-serif; font-size: 13px; line-height: normal;">
<br></div>
<div style="font-family: arial; font-size: small; line-height: normal;">
<br></div>
</div>                          
        </div>
""")[0]
