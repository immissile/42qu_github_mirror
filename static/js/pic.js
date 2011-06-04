uphandler = {
    abort: function() {}
};
errdetail = {
    1: '请登录',
    2: '照片太大(每张照片的大小不应超过3M)',
    10: '不支持的图片格式',
    12: '照片格式有误(仅支持JPG,JPEG,GIF,PNG或BMP)',
    14: '添加图片出错',
    16: ' 每篇文章最多配42张图片'
}

function upload(){
    $.fancybox({
        content : '<h2>上传图片</h2><div><p><input id="file" type="file" name="img"></p><p><button onclick="start_upload()">上传</button></p></div>',
        onClosed : show_uploading,
        onStart : hide_uploading 
    });
    return false
}

function show_uploading() {
    $('#upload_wait').hide();
    $('#upload').show();
}

function hide_uploading() {
    $('#upload_wait').show();
    $('#upload').hide();
}

function start_upload() {
    uphandler = $.ajaxFileUpload({
        url: UPLOADURL,
        global: true,
        secureuri: false,
        fileElementId: 'file',
        dataType: 'json',
        timeout: 120000,
        allowType: 'jpg|png|bmp|gif|jpeg',
        extra: {
            _xsrf : cookie.get("_xsrf")
        },
        success: function(data, status) {
            if (typeof(data.status) != 'undefined') {
                if (data.status) {
                    alert(errdetail[parseInt(data.status)]);
                } else {
                    add_thumb(data.src, data.seqid);
                }
            } else {
                alert('无法得到服务器返回');
            }
        },
        error: function(data, status, e) {
            hide_uploading();
            alert(e);
        },
        begin: function(e) {
            if (e != '') {
                alert(errdetail[e]);
            } else {
                $.fancybox.close();
                location.href = '#loading';
            }
        }
    })
    return false
};

function add_thumb(src, id) {
    $("#addpic_wait").after('<div class="cl imgblock"><img class="picsrc"><div><p>&lt;图片<span class="seqid"></span>&gt; 标题:<input class="titpic itx" value=""></p><p class="tc mt21"><input type="radio" value="1" class="radio"><label>居左</label><input type="radio" value="0" checked="checked" class="radio"><label>居中</label><input type="radio" value="2" class="radio"><label>居右</label></p><p style="margin-top:10px;"><a href="javascript:void(0)" class="rmpic">删除</a></p></div></div>')
    var imgblock = $(".imgblock:first").attr("id", "pic" + id),
    p = "pos" + id;
    imgblock.find('.picsrc').attr("src", src);
    imgblock.find('.seqid').text(id)
    var r = imgblock.find('.radio').attr('name', p)
    imgblock.find('.rmpic').attr('rel', id)

    imgblock.find(".titpic").attr('name', "tit" + id)
    $('#txt').insert_caret('<图片' + id + '>');
    var l = imgblock.find("label")
    p += "_"
    $(l[0]).attr("for", p + 1)
    $(l[1]).attr("for", p + 0)
    $(l[2]).attr("for", p + 2)
    $(r[0]).attr("id", p + 1)
    $(r[1]).attr("id", p + 0)
    $(r[2]).attr("id", p + 2)
};
