#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
EMAIL_VALID = re.compile(r'^\w+[-+.\w]*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')

EMAIL_DICT = {
    'msn.com': ('MSN', 'http://login.live.com/'),
    '2008.sina.com': ('新浪', 'http://mail.2008.sina.com.cn/index.html'),
    'sina.com.cn': ('新浪', 'http://mail.sina.com.cn/index.html'),
    'vip.163.com': ('163', 'http://vip.163.com/'),
    'hongkong.com': ('中华邮', 'http://mail.china.com'),
    'sohu.com': ('搜狐', 'http://mail.sohu.com'),
    'live.com': ('Live', 'http://login.live.com/'),
    'eyou.com': ('亿邮', 'http://mail.eyou.com/'),
    'citiz.net': ('Citiz', 'http://citiz.online.sh.cn/citiz_index.htm'),
    'yeah.net': ('Yeah', 'http://mail.yeah.net/'),
    'vip.tom.com': ('Tom', 'http://vip.tom.com/'),
    'vip.qq.com': ('QQ', 'http://mail.qq.com/cgi-bin/loginpage?t=loginpage_vip&f=html'),
    'yahoo.com.hk': ('雅虎', 'http://mail.yahoo.com.hk'),
    'yahoo.cn': ('雅虎', 'http://mail.cn.yahoo.com/'),
    '188.com': ('188', 'http://www.188.com/'),
    '2008.china.com': ('中华邮', 'http://mail.china.com'),
    'vip.sohu.com': ('搜狐', 'http://mail.sohu.com'),
    '163.com': ('163', 'http://mail.163.com'),
    '126.com': ('126', 'http://www.126.com/'),
    'chinaren.com': ('chinaren', 'http://mail.chinaren.com'),
    'tom.com': ('Tom', 'http://mail.tom.com/'),
    'china.com': ('中华邮', 'http://mail.china.com'),
    '139.com': ('139', 'http://mail.139.com/'),
    'hotmail.com': ('Hotmail', 'http://www.hotmail.com'),
    '21cn.com': ('21cn', 'http://mail.21cn.com/'),
    'gmail.com': ('Gmail', 'http://mail.google.com'),
    'my3ia.sina.com': ('新浪', 'http://vip.sina.com.cn/index.html'),
    'yahoo.com.tw': ('雅虎', 'http://mail.yahoo.com.tw'),
    'vip.sina.com': ('新浪', 'http://vip.sina.com.cn/index.html'),
    'mail.china.com': ('中华邮', 'http://mail.china.com'),
    '263.net': ('263', 'http://mail.263.net/'),
    'yahoo.com': ('雅虎', 'https://login.yahoo.com/'),
    'foxmail.com': ('Foxmail', 'http://www.foxmail.com/'),
    'qq.com': ('QQ', 'http://mail.qq.com'),
    'sina.cn': ('新浪', 'http://vip.sina.com.cn/index.html'),
    'yahoo.com.cn': ('雅虎', 'http://mail.cn.yahoo.com/'),
    'sogou.com': ('搜狗', 'http://mail.sogou.com/'),
    'sina.com': ('新浪', 'http://mail.sina.com.cn/index.html'),
    'live.cn': ('Live', 'http://login.live.com/'),
}

import cgi
def mail2link(mail):
    return '<a href="%s" target="_blank">%s</a>' % (mail_link(mail), mail)

def mail_link(mail):
    mail = cgi.escape(mail)
    if mail and mail.find('@') > 0:
        e_domain = mail.split(str('@'))[1]
        link = EMAIL_DICT.get(e_domain)
        if link:
            return link[1]
    return 'http://%s'%mail.rsplit('@', 1)[-1]

def cnenlen(s):
    if type(s) is str:
        s = s.decode('utf-8', 'ignore')
    return len(s.encode('gb18030', 'ignore')) // 2

def cnencut(s, length):
    ts = type(s)
    if ts is str:
        s = s.decode('utf-8', 'ignore')
    s = s.encode('gb18030', 'ignore')[:length*2].decode('gb18030', 'ignore')
    if ts is str:
        s = s.encode('utf-8', 'ignore')
    return  s

def cnenoverflow(s, length):
    txt = cnencut(s , length)
    if txt != s:
        txt = '%s ...' % txt.rstrip()
        has_more = True
    else:
        has_more = False
    return txt, has_more


def format_txt(txt):
    txt = txt.replace('　', ' ').replace('\r\n', '\n').replace('\r', '\n').rstrip().rstrip("\n")
    txt = map(str.strip, txt.split('\n'))
    result = []
    
    has_split = False
    for i in txt:
        if i:
            result.append(i)
            pre = True
        elif result and result[-1]:
            result.append(i)
            has_split = True

    if has_split:
        split = "\n"
    else:
        split = "\n\n"
    txt = split.join(result)
    return txt

#<span style="margin-left:4px"><a href="#">显示全部</a></span>
if __name__ == '__main__':
    print mail_link('zsp007@gmail.com')
    print mail_link('zsp007@42qu.com')
    print format_txt("""
1、El que ríe ultimo no ríe mejor, simplemente es por que no entendió el chiste.
笑在最后的并不一定是笑得最好的，他仅仅是最后明白笑话的人而已。

2、Estudiar es desconfiar de la inteligencia de tu compa&ntilde;ero de al lado
学习是对你旁边的同学智慧的不信任。

3、Hay tres tipos de personas: los que saben contar y los que no.
世上有三类人，会数数的和不会数数的。

4、Me emborraché para olvidarte.. y ahora te veo doble.
我喝酒是为了忘记你，但现在我看见两个你。

5、El amor eterno dura aproximadamente tres meses.

永恒的爱大约持续三个月

6、Todas las mujeres tienen algo hermoso.. aunque sea una prima lejana.
所有女人都有某些动人之处，哪怕是你的远房表妹也不例外。

7、Vive de tus padres hasta que puedas vivir de tus hijos.
靠你的父母养，直到你可以被你的子女们养。

8、Lo importante es la plata, la salud va y viene.
重要的是金钱，健康走了还会来。


9、En la vida hay dos palabras que te abrirán muchas puertas...&iexcl;&iexcl;
&iexcl;&iexcl;&iexcl;TIRE y EMPUJE!!!
人生中有两个字可为你开启许多扇门...“拉”和“推”！

10、Nadie es perfecto. Atentamente: Nadie.
没有人是完美的！请注意：我就是没有人。

11、Los dos estamos muy enamorados: yo de él y él de otra.
我们两个都深深坠入爱河，我爱她，她爱另一个。

12、Me revienta que hablen cuando interrumpo.
我最讨厌的事情就是当我打断别人说话的时候别人还在滔滔不绝地说。

13、Dios cura y el médico pasa la factura.
神治病而医生开发票。

14、Ahorra agua. No te duches solo.
要节约用水，所以你别一个人洗澡。

15、He oído hablar tan bien de ti, que creía que estabas muerto.
我听到了太多对你的溢美之词，以至于我一直认为你已经死了。

16、La Psiquiatría/psicología es el único negocio donde el cliente nunca ti
ene la razón.
心理治疗诊所是唯一一个客人永远没道理可讲的地方。

17、Sigue estudiando y serás una calavera sabia.
你继续学吧，不久你就会成为一个聪明的头盖骨。

18、Si un día te levantas con ganas de estudiar, toma una aspirina y vuelvete
a acostar.
如果某天你起床有学习的欲望，吃一颗阿司匹林，回去睡觉。

19、Hay un mundo mejor, pero carísimo.
的确有一个更好的世界，但是昂贵至极。

20、El amor es una cosa esplendorosa...hasta que te sorprende tu esposa.
爱情是一件美妙的事情，直到一天你的妻子惊吓到你。

21、En las próximas elecciones vote a las putas, votar a los hijos no dio res
ultado.
以后的大选我干脆投票给妓女们，因为投票给她们的儿子（狗丅娘养的）也不会有好结果

22、La prueba más clara de que existe vida inteligente en el universo es que
nadie ha intentado contactar con nosotros.
在宇宙中存在智慧生命的最清楚证据就是没人试图与我们联系。

23、Los estudios son la luz del mundo.... deja los estudios y ahorra energía.
学习是世界之光... 别再学了，请节省能源。

24、Dios mío dame paciencia..... &iexcl;&iexcl;&iexcl;pero YA !!!!
神啊，请给我耐心...现在就要！！！

25、Un pesado es alguien que cuando le preguntas cómo está, va y te contesta
一个烦人的人应该是这样的：当你礼节性地问候他“你好吗？”时，他居然真的滔滔不绝
地回答你。

26、El dinero no trae la felicidad, pero cuando se va, se la lleva.
金钱从来都不能带来幸福，但是当它离你而去时，不幸就来了。

27、El mejor amigo del perro es otro perro.
狗是人类最好的朋友，而狗最好的朋友是另一只狗。

28、Hombre de buenas costumbres busca alguien que se las quite.
一个有着好习惯的男人总是在寻找一个能把他所有好习惯拿走的女人。

29、La esclavitud no se abolió, se cambió a 8 hrs diarias.
奴隶制并没有被废除，只是改为每天八小时了。

30、Toda cuestion tiene dos puntos de vista: El equivocado y el nuestro.

我们有两种观点可以看待所有的问题，一种是错误的观点，另一种是我们的观点。

31、Las pirámides son el mejor ejemplo de que en cualquier tiempo y lugar los
obreros tienden a trabajar menos cada vez.
无论何时何地，工人们总是尽可能地偷懒，一天比一天干得少，金字塔就是最好的例子。

32、Se está muriendo gente que antes no se moría.
总有以前没有死掉的人在这一刻正在死掉。

33、No te tomes la vida en serio, al fin y al cabo no saldrás vivo de ella.
别对生活太较真儿，反正无论怎样，你都不能活着逃离它。

34、Arreglar los problemas económicos es fácil, lo único que se necesita es
dinero.
解决经济问题没什么难的，唯一需要的就是钱。

35、Todos te dan un consejo, cuando lo que necesitas es guita.
当你所需要的是金钱的时候，所有人给你的都是建议。

36、La inteligencia me persigue, pero yo soy más rápido.
聪明它追着我跑，但我比它快。

37、&iexcl;&iexcl;&iexcl;Soy la mejor en la cama!!
FIRMA: LA BELLA DURMIENTE
我在床上是最棒的！！
签名：睡美人

38、Dicen que cuando Piscis y Acuario se casan, el matrimonio naufraga.
听说当双鱼和水瓶结婚的时候，婚姻就落难了


西班牙人是一个欢乐的民族
╮(╯▽╰)╭
""")
