/live 获取当前登录用户的消息流
=======================================

输入 ::

    {
        access_token:
        client_id: //可选
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
                    user:
                        {
                            name:
                            unit:
                            title:
                            id:
                            ico_url: // 可无
                        }
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

    http://api.yup.xxx/live?access_token=xxxxxxxxxxxxxxx

演示返回 ::

    {
        "items":
            [
                {
                    "cid":65,
                    "id":10046873,
                    "name":"Megan Fox",
                    "user":
                        {
                            "name":"真谛~",
                            "ico_url":"http://p.zjd.xxx/96/664/26264.jpg",
                            "id":10001299,
                            "unit":"42区",
                            "title":"运营&死coder"
                        }
                },
                {
                    "cid":65,
                    "id":10046864,
                    "name":"HELLO WORLD",
                    "user":
                        {
                            "name":"真谛~",
                            "ico_url":"http://p.zjd.xxx/96/664/26264.jpg",
                            "id":10001299,
                            "unit":"42区",
                            "title":"运营&死coder"
                        }
                }
            ],
        "begin_id":10046864
    }
