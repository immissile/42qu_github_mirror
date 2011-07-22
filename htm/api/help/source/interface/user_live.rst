/user/live 获取用户关注的微博
=======================================


输入 ::

    {
        user_id: 
        client_id: //可选
        access_token: //可选
    }


返回 ::

    {
        items:  
            [
                {   id: //微博id
                    user_name://用户名
                    user_link: //用户链接
                    rt_list: //转发列表
                    user_id: //用户id
                    cid: //分类id
                    reply_count: //回复数
                    timestamp: //时间戳
                    name: //微博内容 或 文章标题
                    vote_state: //是否支持
                    vote: //支持数
                    txt: //文章内容 微博可能不出现
                }
            ]
    }


演示链接 ::

    http://api.yup.xxx/user/feed?user_id=79


演示返回 ::

    {
         "items":[
                    {   "user_id":79,
                        "name":"\u4e00\u4e2a",
                        "cid":61,
                        "timestamp":1308738857,
                        "vote_state":0,
                        "reply_count":0,
                        "user_link":"http://79.yup.xxx",
                        "vote":0,
                        "user_name":"yupbank",
                        "id":240
                    }
                ]

    }
