_gaq=[['_setAccount', 'UA-18596900-1'],['_trackPageview'],['_trackPageLoadTime']];
(function(){
        var ga = document.createElement('script');
        ga.type = 'text/javascript';
        ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        /*google 百度 统计*/
})()

function _rm(prefix, url){
    return function(id){ 
        if(confirm('删除 , 确定 ?')){
            var t=$(prefix+id)
            t.fadeOut(function(){t.remove()})
            $.postJSON(url+id)
        }
    }
}
jQuery.fn.extend({  
        elastic_login: function(){
            function _(){
                if(!$.cookie.get('S')){
                    login()
                    return false
                }
            }
            this.find('textarea,input').elastic().focus(_)
            return this.submit(_) 
        }
})


function login(){
    $.fancybox({
            href:'/j/login',
            onComplete:function(){ 
                $("#login").attr('action',"/auth/login?next="+encodeURIComponent(location.href))
                login_autofill("_pop")
            }
    });
}
function login_autofill(suffix){
    suffix = suffix||''
    var mail = $("#login_mail"+suffix).focus(), password = $("#login_password"+suffix), mail_val = $.cookie.get("E");
    if(mail_val&&mail.val()==''){
        mail.val(mail_val).select();
    }
    mail_val = mail.val();
    if(mail_val&&mail_val.length){
        password.focus()
    }
}
/*
 var dnav = $("#dnav").show(), dmore = $("#dmore").addClass('dmore').hide(),body=$('html,body');
 function _(){
     dmore.hide()
     body.unbind('click',_)
 }
 dnav.click(function(e){
         dnav.blur()
         if(dmore.is(":hidden")){
             dmore.show()
             e.stopPropagation()
             body.click(_)
         }else{
             _()
         }
 })
 */
function init_D(){
    var body=$('html,body')
    $("#H .DA").click(function(e){
        var t=this, drop=$(this.parentNode).find('div');
        t.blur();
        function _(){
            drop.hide()
            body.unbind('click',_)
        }
        if(drop.is(":hidden")){
            drop.show()
            e.stopPropagation()
            body.click(_)
        }else{
            _()
        }
    })
}


function po_photo(id){
    var fancybox = $.fancybox;
    fancybox({      
    "content":[

'<form method="POST" enctype="multipart/form-data" id="po_photo_form"><div style="padding:0 10px 5px;">',

id?"编辑文本":"发布图片",

'</div>',

id?'':'<input id="po_photo" style="margin:10px;" type="file" name="photo">',

'<div style="padding:10px;line-height:0;">',

'<input autocomplete="off" id="po_photo_name" name="name" type="text"><textarea name="txt" id="po_photo_txt"></textarea></div><div class="btns">',

id?'<a href="javascript:void(0)" id="po_photo_rm">删除</a>':'<span id="po_photo_error"></span>',

'<span class="btnw"><button type="submit">提交</button></span></div><input type="hidden" name="_xsrf" value=""></form>'

    ].join(''),
    hideOnOverlayClick:false,
    "onComplete":function(){
        var form=$("#po_photo_form"),
            action="/po/photo",
            po_photo=$("#po_photo"),
            po_photo_name=$("#po_photo_name"),
            _xsrf = $.cookie.get("_xsrf");
        form.find("input[name=_xsrf]").val(_xsrf)
        if(id){
            action+="/"+id;
            po_photo_name.val($('#photo_title').text()) 
            //$("#po_photo_txt").html($.trim($('#txt').html()))
            $("#po_photo_rm").attr('href',"/po/rm/"+id+"?_xsrf="+_xsrf).click(function(){
                if(!confirm('删除 , 确定 ?')) return false;
            })
        }else{
            po_photo_name.attr('placeholder',"请输入标题 ..." ).placeholder()
        }
        form.attr('action',action).submit(function(){

            var photo = po_photo.val(),
                name = $.trim(po_photo_name.val()),
                po_photo_error=$("#po_photo_error"),
                self=$(self),
                error;

                if(name==po_photo_name[0].placeholder){
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
                    po_photo_name.focus()
                }
                
                if(error){
                    $("#po_photo_error").text(error).fadeIn()
                    return false;
                }


                fancybox.showActivity();
        })

    }
    })

}



CANNOT_REPLY = '<div class="fancyban"><p>啊 , 出错了 !</p><p>为了假装一本正经的讨论气氛</p><p>未认证用户没有发言权</p><p><a href="/i/verify">点此申请认证吧</a></p></div>'

function follow_a(id){
    var a=$("#follow_a"+id),
        text=a.html(),
        url="/j/follow",
        follow="关注", 
        follow_rm="淡忘";

    if(text==follow){
        text = follow_rm;
        fancybox = $.fancybox;
        fancybox({
            content:'<form id="follow_reply" class="fancyreply"><h3>关注 , 可以有个理由 ...</h3><textarea name="txt"></textarea><div class="btns"><span class="btnw"><button class="btn" type="submit">此致 , 敬礼 !</button></span><span id="follow_secret_span"><input type="checkbox" name="secret" id="follow_reply_secret"><label for="follow_reply_secret">私语</label></span></div></form>',
            onComplete:function(){
                var reply = $("#follow_reply"),
                    textarea = reply.find('textarea');
                reply.submit(function(){
                    var txt = $.trim(textarea.val());
                    if(txt&&txt.length){
                        fancybox.showActivity()
                        $.postJSON(
                            "/j/follow/reply/"+id,
                            {'txt':txt},
                            function(r){
                                if(r.can_not_reply){
                                    fancybox({
                                        content:CANNOT_REPLY  
                                    }) 
                                }else{
                                    fancybox.close()
                                }
                        })
                    }else{
                        fancybox.close()
                    }
                    return false
                })
                textarea.focus()
            }
       })
    }else{
        text = follow;
        url += "/rm"
    }
    $.postJSON(url+"/"+id)
    a.html(text)
}
