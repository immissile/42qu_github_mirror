/po/audoi 上传音频
=======================================


输入 ::

    {
        access_token:
        audio:  //音频文件
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

演示表单 ::
    {
        <form action="http://api.yup.xxx/po/audio" method="POST" enctype="multipart/form-data">
        <input type="text" value="aw" name="name">
        <input type="text" value="sdsad" name="txt">
        <input type="text" value="asdsaad" name="tag_name">
        <input type="text" value="DQAAAAe_v5FVSsZ_TcnFS8" name="access_token">
        <label for="file">Filename:</label>
        <input type="file" name="audio" id="file" /> 
        <input type="submit" value="ok">
        </form>
    }


演示返回 ::

    {
    "link":"http://zhendi.yup.xxx/10047360"
    "id":10047360
    }
