function upload(){
    $.fancybox({
        content : '<div style="width:270px" style="line-height:27px"><h2 style="margin-top:1px" class="Ph2">上传图片</h2><div style="margin-top:27px;margin-bottom:14px"><p style="text-align:center"><input id="file" type="file" name="img" style="height:22px"></p><p class="btns tc mt27"><button class="bbg" onclick="start_upload()">上传</button></p></div></div>'
    });
    return false
}
