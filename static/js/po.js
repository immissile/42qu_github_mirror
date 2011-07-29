function po_(action, name, id, input, oncomplete){
    var fancybox = $.fancybox;
    fancybox({      
        "content":[

        '<form method="POST" enctype="multipart/form-data" id="po_pop_form" class="po_pop_form"><div class="po_pop_tip">',

        id?"编辑文本":"发布"+name,

        '</div>',

        id?'':input,

        '<div><input id="po_pop_name" autocomplete="off" name="name" type="text"><textarea id="po_pop_txt" name="txt" class="po_pop_txt"></textarea></div><div class="btns">',

        id?'<a href="javascript:void(0)" id="po_pop_rm">删除</a>':'<span id="po_pop_error"></span>',

        '<span class="btnw"><button type="submit">提交</button></span></div><input type="hidden" name="_xsrf" value=""></form>'

        ].join(''),
        hideOnOverlayClick:false,
        "onComplete": function(){
            var form=$("#po_pop_form"),
                action="/po/"+action,
                po_pop_name=$("#po_pop_name"),
                _xsrf = $.cookie.get("_xsrf");
                form.find("input[name=_xsrf]").val(_xsrf)
                
                form.find(' [placeholder]').placeholder()
                if(id){
                    form.attr('action',action+"/"+id);
                    po_pop_name.val($('#po_name').text()) 
                    $("#po_pop_txt").val($.trim($('#_txt').val()))
                    $("#po_pop_rm").attr('href',"/po/rm/"+id+"?_xsrf="+_xsrf).click(function(){
                        if(!confirm('删除 , 确定 ?')) return false;
                    })
                }else{
                    fancybox.showActivity();
                    return oncomplete(form, $("#po_pop_error")) 
                }
    })
}

function po_video(id){
    po_(
    'video',
    '视频',
    id,
    '<input id="po_video" autocomplete="off" placeholder="优酷的视频网址 ..." name="video" type="txt">',
    function(form, po_error){
            var po_name=$("#po_pop_name"), input=$('#po_video');
            po_name.attr('placeholder',"请输入视频标题 ..." ).placeholder()
            
            form.attr('action',action).submit(function(){
                var input = input.val(),
                    name = $.trim(po_name.val()),
                    self=$(self),
                    error;

                    if(name==po_video_name[0].placeholder){
                        name='';
                    }
                    
                    if(video&&video.length){
                        if(!(/^(http:\/\/v\.youku\.com\/v_show\/id_)\w{13}(\.html)$/.test(video) || /^(http\:\/\/player\.youku\.com\/player\.php\/sid\/)w{13}(\/v\.swf)$/.test(video))){
                            alert("请输入优酷视频 (分享->视频地址)\n如 : \nhttp://v.youku.com/v_show/id_XMjg5MTA2NzA0.html");
                            return false
                        }
                    }else{
                        error = "请输入视频网址"
                    }
                        

                    if(!(name&&name.length)){
                        error = "请输入标题"
                        po_video_name.focus()
                    }
                    
                    if(error){
                        $("#po_pop_error").text(error).fadeIn()
                        return false;
                    }


            })

    }
    )


}


function po_photo(id){
    po_(
        '视频',
        id,
        '<input id="po_photo" style="margin:10px;" type="file" name="photo">',
        function(){
            var form=$("#po_photo_form"),
                action="/po/photo",
                po_photo=$("#po_photo"),
                po_pop_name=$("#po_pop_name"),
                _xsrf = $.cookie.get("_xsrf");
            form.find("input[name=_xsrf]").val(_xsrf)
            if(id){
                form.attr('action',action+"/"+id);
                po_pop_name.val($('#photo_name').text()) 
                $("#po_photo_txt").val($.trim($('#_txt').val()))
                $("#po_pop_rm").attr('href',"/po/rm/"+id+"?_xsrf="+_xsrf).click(function(){
                    if(!confirm('删除 , 确定 ?')) return false;
                })
            }else{
                po_pop_name.attr('placeholder',"请输入标题 ..." ).placeholder()
                form.attr('action',action).submit(function(){

                    var photo = po_photo.val(),
                        name = $.trim(po_pop_name.val()),
                        po_photo_error=$("#po_photo_error"),
                        self=$(self),
                        error;

                        if(name==po_pop_name[0].placeholder){
                            name='';
                        }
                        
                        if(photo&&photo.length){
                            if(!/\.(jpg|png|bmp|gif|jpeg)$/.test(photo.toLowerCase())){
                                error = "照片格式有误(仅支持JPG,JPEG,GIF,PNG或BMP)"
                            }
                        }else{
                            error = "请选择图片"
                        }

                        if(!(name&&name.length)){
                            error = "请输入标题"
                            po_pop_name.focus()
                        }
                        
                        if(error){
                            $("#po_photo_error").text(error).fadeIn()
                            return false;
                        }


                        fancybox.showActivity();
                })
            }

            }
    )
}
