/user/info/id 获取用户信息 
=======================================

输入 ::

    {
        user_id:
        access_token: //可选
    }


返回 ::

    {
        following_num:   //关注的人数
        self_intro:   //自我介绍
        ico:    //小图标网址
        name:   //昵称
        follower_num:   //被关注的人数
        marry:    // 婚姻状况 1为单身 2为恋爱 3为已婚 0 为没有填写
        place_home:     //家乡地址编码 0为没有填写
        pic:       //大图标
        place_now:    //现住地址编码 0为没有填写
        moto:      // 座右铭
        user_link:   //用户主页地址
        user_id:    //用户id
        sex:    //性别 1为男 2为女
        verify_state: //是否通过验证 9为未验证 10为已经验证 其他代码日后开发完善公布
        place_now_name:    //可能无  现居地址
        place_home_name:   //可能无 家乡地址
    }

