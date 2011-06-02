function _rm(prefix, url){
    return function(id){ 
        if(confirm('删除 , 是吗?')){
            $("#"+prefix+id).fadeOut()
            $.postJSON(url+id)
        }
    }
}


_gaq=[['_setAccount', 'UA-23361634-1'],['_trackPageview'],['_trackPageLoadTime']];
(function(){
    var ga = document.createElement('script');
    ga.type = 'text/javascript';
    ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    /*google 百度 统计*/
})()

function login(){
    $.fancybox({
        href:'/j/login',
        onComplete:function(){ 
            $("#login_next_pop").val(location.href);
            login_autofill("_pop")
        }
    });
}
function login_autofill(suffix){
    suffix = suffix||''
    var mail = $("#login_mail"+suffix).focus(), password = $("#login_mail"+suffix), mail_val = cookie.get("E");
    if(mail_val){
        mail.val(mail_val).select();
    }
}
