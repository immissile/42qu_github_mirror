/po/video 发视频
=======================================


输入 ::

    {
        access_token:
        video:  //视频链接
        name:  //展示的名称
        txt: //内容

        id: //可以为空，如果存在，则为修改视频
        tag: //tag_id 可以为空，默认为1
        tag_name: //tag名称 为空则没有标签
    }

返回 ::
    
    {
        link: //
        id: //po的id
    }

演示链接 ::

    http://api.yup.xxx/po/word?video=http://v.youku.com/v_show/id_XMjkzOTM4Njcy.html&name=让梦想飞&txt=还不错&tag_name=手机上传&access_token=820afba8706f4fd3b281cdd8418b2fa2


演示返回 ::

    {
        "id":"124"
        "link":"http://79.yup.xxx/124"
    }
