/po/word 发微博 
=======================================


输入 ::

    {
        client_id:
        access_token:
        txt: //微博内容 不可以重复发送！
    }

返回 ::

    {
        id: //该条微博的id
        link: //该条微博的链接     重复发送返回空
    }

演示链接 ::
    
    http://api.yup.xxx/po/word?client_id=10045260&txt=testxs&access_token=820afba8706f4fd3b281cdd8418b2fa2

演示返回 ::

    {
        "id":"124"
        "link":"http://79.yup.xxx/124"
    }
