#coding:utf-8

LINK = "http://click.union.360buy.com/JdClick/?unionId=2939&t=4&to=http://www.360buy.com/product/%s.html"


ITEM = (
    (   5,
        LINK%10045410,"诚信的背后",
        "帕特诺伊 亲身经历写成，揭开了华尔街金融创新与圈钱游戏的真相。中国证监会前主席刘鸿儒作序推荐。"
    ),
    (   
        4, 
        LINK%10261402, "创业的国度" , 
        """是什么让以色列 — 仅有710万人口、笼罩着战争阴影、没有自然资源的国家 , 产生了如此多的新兴公司 ; 甚至比加拿大、日本、中国、印度、英国等大国都多?  """

    ),
    ( 
        3, LINK%10071236, "设计中的设计" , 
        """设计不是一种技能，而是捕捉事物本质的感觉能力和洞察能力 — 原研哉 """
    ),
)

def rec_item():
    return ITEM

