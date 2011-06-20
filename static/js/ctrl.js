_gaq=[['_setAccount', 'UA-23361634-1'],['_trackPageview'],['_trackPageLoadTime']];
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
                $("#login").attr('action',"/login?next="+encodeURIComponent(location.href))
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


