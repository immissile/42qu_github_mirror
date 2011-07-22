/user/follow 关注新用户  
=======================================


输入 ::

    {
        id:
        client_id:
        access_token:
    }


返回 ::

    {
        status: //成功返回true，多次重复为NUll
    }


演示链接 ::

    http://api.yup.xxx/user/follow?client_id=73&id=80&access_token=820afba8706f4fd3b281cdd8418b2fa2


演示返回 ::

    {
        "status":true
    }
