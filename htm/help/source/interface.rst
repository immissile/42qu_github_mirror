=======================================
函数接口
=======================================

.. include::  interface/user_info_id.rst
.. include::  interface/po_word.rst






== 3.获取用户粉丝 ==
/user/follower

输入
{{{
{
    user_id:
    limit: //可选 默认为25，最大支持100
    offset: //可选
    client_id: //可选
    access_token: //可选
}
}}}

返回
{{{
{
    follower_list: //粉丝id列表
    total_num: //粉丝数
}
}}}
演示链接
{{{
http://api.yup.xxx/user/follower?user_id=80&offset=1
}}}
返回值
{{{
{
    "follower_list":[3]
    "total_num":2
}
}}}

== 4.获取用户关注 ==

/user/following

输入
{{{
{
    user_id: 
    client_id: //可选
    access_token: //可选
}
}}}

返回
{{{
{
    following_list: //用户关注id列表
    total_num:   //用户关注总数 
}
}}}

演示链接
{{{
http://api.yup.xxx/user/following?user_id=80
}}}

返回值
{{{
{
    "following_list":[3,79]
    "total_num":2
}
}}}

== 5.获取用户关注的微博 ==

/user/live

输入
{{{
{
    user_id:
    client_id: //可选
    access_token: //可选
}
}}}

返回
{{{
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
}}}

演示链接
{{{
http://api.yup.xxx/user/feed?user_id=79
}}}
返回值
{{{
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
}}}

== 6.关注新用户 ==

/user/follow

输入
{{{
{
    id:
    client_id:
    access_token:
}
}}}

返回
{{{
{
    status: //成功返回true，多次重复为NUll
}
}}}

演示链接
{{{
http://api.yup.xxx/user/follow?client_id=73&id=80&access_token=820afba8706f4fd3b281cdd8418b2fa2
}}}

返回值
{{{
{
    "status":true
}
}}}

== 7.取消关注 ==

/user/follow/rm

输入
{{{
{
    id:
    client_id:
    access_token:
}
}}}

返回
{{{
{
    status: //成功返回true，多次重复为NUll
}
}}}

演示链接
{{{
http://api.yup.xxx/user/follow/rm?client_id=73&id=80&access_token=da98ac450ffe18a5278fa620b0ad0f4037b7aa66fc9a169d7a81b936e301ca8d
}}}

返回值
{{{
{
    "status":true
}
}}}

== 8.获取评论 ==

/po

输入
{{{
{
    id:
    client_id:
    access_token:
}
}}}

返回
{{{
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
}}}

演示链接
{{{
http://api.yup.xxx/po?client_id=73&id=342&access_token=cec5081ef51fda0099937345ce9b6192e4016e6fa719a70b06215c0aef1fa20d
}}}

返回值
{{{
{   "items":[
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
}}}

== 9.回复微博 ==

/po/reply

输入
{{{
{
    id:
    txt: 
    client_id:
    access_token:
}
}}}

返回
{{{
{
    id: //新回复的id，若为空则不能回复
}
}}}

演示链接
{{{
http://api.yup.xxx/po/reply?client_id=422&id=427&txt=%E6%82%A8%E5%A5%BD&access_token=4a13b7391a198de774acd78751ca0cfba3a82057ccba7a849a4e851cfc7d2d19
}}}

返回值
{{{
{
    "id":429
}
}}}

== 10.删除回复 ==

/po/reply/rm

输入

{{{
{
    id:
    client_id:
    access_token:
}
}}}

返回
{{{
{
    status: //成功为true，其他为删除失败
}
}}}

演示链接
{{{
http://api.yup.xxx/po/reply/rm?client_id=422&id=429&access_token=40bd69c43a46c4fd376cc7f4623fe250df84475719f55ffcd98132b538fdf943
}}}

返回值
{{{
{
    "status":true
}
}}}


== 11.删除微博 ==

/po/rm

输入

{{{
{
    id:
    client_id:
    access_token:
}
}}}

返回
{{{
{
    status:
}
}}}

演示链接
{{{
http://api.yup.xxx/po/rm?client_id=422&id=427&access_token=40bd69c43a46c4fd376cc7f4623fe250df84475719f55ffcd98132b538fdf943
}}}

返回值
{{{
{
    "status":true
}
}}}
