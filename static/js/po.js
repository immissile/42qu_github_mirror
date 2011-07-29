(function(){
function po_(id, action, name, input, oncomplete){
    var fancybox = $.fancybox;
    fancybox({      
        "content":[
        '<form method="POST" enctype="multipart/form-data" id="po_pop_form" class="po_pop_form"><div class="po_pop_tip">',
        id?"编辑文本":"发布"+name,
        '</div>',
        id?'':input,
        '<div id="po_pop_main"><input id="po_pop_name" autocomplete="off" name="name" type="text"><textarea id="po_pop_txt" name="txt" class="po_pop_txt"></textarea></div><div class="btns">',
        id?'<a href="javascript:void(0)" id="po_pop_rm">删除</a>':'<span id="po_pop_error"></span>',
        '<span class="btnw"><button type="submit">提交</button></span></div><input type="hidden" name="_xsrf" value=""></form>'
        ].join(''),
        hideOnOverlayClick:false,
        "onComplete": function(){
            var form=$("#po_pop_form"),
                po_name=$("#po_pop_name"),
                _xsrf = $.cookie.get("_xsrf"),
                error;
                
                form.find("input[name=_xsrf]").val(_xsrf)
                
                po_name.attr('placeholder',"请输入"+name+"标题 ..." )
                form.attr(
                    'action',
                    "/po/"+action+id?("/"+id):""
                ).find(' [placeholder]').placeholder()

                if(id){
                    $("#po_pop_txt").val($.trim($('#_txt').val()))
                    $("#po_pop_rm").attr('href',"/po/rm/"+id+"?_xsrf="+_xsrf).click(function(){
                        if(!confirm('删除 , 确定 ?')) return false;
                    })
                }

                form.submit(function(){ 
                    name = $.trim(po_name.val())
                    if(name==po_name[0].placeholder){
                        name='';
                    }
                    if(!(name&&name.length)){
                        error = "请输入标题"
                        po_video_name.focus()
                    }

                    fancybox.showActivity();
                    if(!error){
                        if(!id){
                            error = oncomplete() 
                        }
                    }
                    if(error){
                        fancybox.hideActivity();
                        $("#po_pop_error").html(error).fadeIn()
                        return false
                    }
                })
        }
    })
}

po_video = function(id){
    po_(
        id,
        'video',
        '视频',
        '<input id="po_video" autocomplete="off" placeholder="优酷的视频网址 ..." name="video" type="txt">',
        function(){
            var video=$('#po_video'), error;
                if(video&&video.length){
                    if(
                        !(
                            /^(http:\/\/v\.youku\.com\/v_show\/id_)\w{13}(\.html)$/.test(video) 
                            || 
                            /^(http\:\/\/player\.youku\.com\/player\.php\/sid\/)w{13}(\/v\.swf)$/.test(video)
                        )
                    ){
                        error = "请输入优酷视频 (视频下方的分享->视频地址)";
                    }
                }else{
                    error = "请输入视频网址"
                }
                return error 
        }
    )
}

po_photo = function(id){
    po_(
        id,
        'photo',
        '图片',
        '<input id="po_photo" style="margin:10px;" type="file" name="photo">',
        function(){
            var error,
                photo=$("#po_photo").val();
                        
                if(photo&&photo.length){
                    if(!/\.(jpg|png|bmp|gif|jpeg)$/.test(photo.toLowerCase())){
                        error = "照片格式有误(仅支持JPG,JPEG,GIF,PNG或BMP)"
                    }
                }else{
                    error = "请选择图片"
                }
            return error
        }
    )
}


})()

