$.fn.extend({
    insert_caret: function(t) {
        var self = this,
        o = self[0];
        if (document.all && o.createTextRange && o.p) {
            var p = o.p;
            p.text = p.text.charAt(p.text.length - 1) == '' ? t + '': t;
        } else if (o.setSelectionRange) {
            var s = o.selectionStart;
            var e = o.selectionEnd;
            var t1 = o.value.substring(0, s);
            var t2 = o.value.substring(e);
            o.value = t1 + t + t2;
            o.focus();
            var len = t.length;
            o.setSelectionRange(s + len, s + len);
            o.blur();
        } else {
            o.value += t;
        }
        self.focus()
    }
})
uphandler = {
    abort: function() {}
};
errdetail = {
    1: '请登录',
    2: '照片太大(每张照片的大小不应超过12M)',
    10: '不支持的图片格式',
    12: '照片格式有误(仅支持JPG,JPEG,GIF,PNG或BMP)',
    14: '添加图片出错',
    16: ' 每篇文章最多配42张图片'
}

function upload(){
    $("#txt").focus();
    $.fancybox({
        content : '<div style="width:260px;padding:8px 16px 16px;font-size:16px"><div class="btns"><p><input style="margin:16px 0;" id="file" type="file" name="img"></p><p><span class="btnw"><button type="submit" class="btn" onclick="start_upload()">上传图片</button></span></p></div></div>',
        hideOnOverlayClick: false
    });
    return false
}

function show_uploading() {
    $('#upload_wait').show();
    $('#upload').hide();
}

function hide_uploading() {
    $('#upload_wait').hide();
    $('#upload').show();
}

function start_upload() {
    uphandler = $.ajaxFileUpload({
        url: UPLOADURL,
        global: true,
        secureuri: false,
        fileElementId: 'file',
        dataType: 'json',
        timeout: 120000,
        allowType: /\.(jpg|png|bmp|gif|jpeg)$/,
        extra: {
            _xsrf : $.cookie.get("_xsrf")
        },
        success: function(data, status) {
            var data_status = data.status, src=data.src;
            if (typeof(data_status) != 'undefined') {
                if (data_status) {
                    alert(errdetail[data_status]);
                } else {
                    src&&add_thumb(src, data.seqid)
                }
            } else {
                alert('无法得到服务器返回');
            }
            hide_uploading()
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
                show_uploading()
            }
        }
    })
    return false
};

function add_thumb(src, id) {
    $('#update_item').tmpl([[id,0,src,""]]).prependTo("#uploaded")
    $('#txt').insert_caret(' 图:' + id + " ");
};

$('.rmpic').live("click", function() {
    var t = $("#txt"),
    id = this.rel;
    if (confirm("确定要删除?")) {
        $.postJSON(
        DELETEURL, 
        {seq: id},
        function(data){
            t.val(t.val().replace(eval('/图:' + id + '/g'), ''));
            $("#pic" + id).fadeOut();
        })
    }
})
function cancel_uploading() {
    uphandler.abort()
    hide_uploading()
}
