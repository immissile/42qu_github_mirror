(function(){var reply_txt=$("#reply_txt"),form=reply_txt.parents('form');
function _(){
    $.fancybox({
        content:'<div class="tc f16 pd16" style="width:250px"><p>为了一本正经的讨论气氛</p><p>未认证用户没有发言权哦<p><p><a href="/i/verify">点此申请认证吧 , 亲</a></p></div>'
    })
    return false;
}
reply_txt.focus(_)
form.submit(_)
})()
