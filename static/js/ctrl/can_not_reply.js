(function(){var reply_txt=$("#reply_txt"),form=reply_txt.parents('form');
function _(){
    $.fancybox({
        content:'<div class="tc f16 pd16" style="width:225px"><p>为了维护一本正经的讨论气氛</p><p>未认证用户不能回复哦 , 亲<p><p><a href="/i/verify">点此申请认证吧</a></p></div>'
    })
    return false;
}
reply_txt.focus(_)
form.submit(_)
})()
