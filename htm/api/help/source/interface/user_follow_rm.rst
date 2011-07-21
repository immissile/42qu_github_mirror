/user/follow/rm 取消关注
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

    http://api.yup.xxx/user/follow/rm?client_id=73&id=80&access_token=da98ac450ffe18a5278fa620b0ad0f4037b7aa66fc9a169d7a81b936e301ca8d


演示返回 ::

    {
        "status":true
    }
