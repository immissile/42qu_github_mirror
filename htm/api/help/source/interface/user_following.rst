/user/following 获取用户关注
=======================================


输入 ::

    {
        user_id: 
        client_id: //可选
        access_token: //可选
    }


返回 ::

    {
        following_list: //用户关注id列表
        total_num:   //用户关注总数 
    }


演示链接 ::

    http://api.yup.xxx/user/following?user_id=80


演示返回 ::

    {
        "following_list":[3,79]
        "total_num":2
    }
