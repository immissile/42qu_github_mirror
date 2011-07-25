/user/live 获取用户产生的消息流
=======================================

输入 ::

    {
        user_id:
        access_token: //可选
        begin_id: //可选 (第一页不传)
    }

返回 ::

    {
        items:  
            [
                {
                    id:
                    cid:
                    name:
                    txt: // 日记、问题、回答有
                    question_id: // 回答 与 微波回答有
                    question_name: // 同上
                    question_user: // 同上
                        {
                            name:
                            unit:
                            title:
                            id:
                            ico_url: // 可无
                        }
                }
            ],
        begin_id: // 0 表示没有更多了
    }


演示链接 ::

    http://api.yup.xxx/user/live?user_id=10000000

演示返回 ::

    {
        "items":
            [
                {
                    "cid":65,
                    "id":10046873,
                    "name":"Megan Fox",
                },
                {
                    "cid":65,
                    "id":10046864,
                    "name":"HELLO WORLD",
                }
            ],
        "begin_id":10046864
    }
