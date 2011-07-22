/user/po 获取评论
=======================================


输入 ::

    {
        id:
        client_id:
        access_token:
    }


返回 ::

    {
    items:
        [
            {
                user_name: //回复用户名
                txt: //回复内容
                user_id: //回复用户的id
                id: //该条回复的id
                timestamp: //回复的时间
            }
        ]
    }


演示链接 ::

    http://api.yup.xxx/po?client_id=73&id=342&access_token=cec5081ef51fda0099937345ce9b6192e4016e6fa719a70b06215c0aef1fa20d


演示返回 ::

    {
    "items":[
        {   "user_name":"yupbank",
            "txt":"dsfs sdfs",
            "user_id":79,
            "id":343,
            "timestamp":1308891815
        },
        {   "user_name":"yupbank",
            "txt":"sdfsdfsdfsdf",
            "user_id":79,
            "id":344,
            "timestamp":1308891818
        }]
    }
