/user/follower 获取粉丝
=======================================


输入 ::

    {
        user_id:
        limit: //可选 默认为25，最大支持100
        offset: //可选
        client_id: //可选
        access_token: //可选
    }


返回 ::

    {
        follower_list: //粉丝id列表
        total_num: //粉丝数
    }


演示链接 ::

    http://api.yup.xxx/user/follower?user_id=80&offset=1


演示返回 ::

    {
        "follower_list":[3]
        "total_num":2
    }
