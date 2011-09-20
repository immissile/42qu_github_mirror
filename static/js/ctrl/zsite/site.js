
function init_say(){
    document.write('<div class="say"><div class="say_txt">今天 ,  想说什么?</div></div> <div class="pop_say"> <textarea class="pop_txt"></textarea> <div class="pop_banner"><a class="pop_submit" href="javascript:post_say();void(0)">发表</a><div class="pop_tip"></div><a class="pop_close" href="javascript:close_pop();void(0)"></a></div></div>')
}

$(function(){
    var say = $('.say')
    var pop_say = $(".pop_say")
    var txt = $('.say_txt')
    var pop_txt = $('.pop_txt')
    var txt_tip = txt.text()
    var  pop_tip = $('.pop_tip') 
    
    can_say = txt_maxlen(pop_txt,pop_tip,142)

    txt.click(function(){
        if(pop_say.is(":hidden")){
            pop_say.show();
            pop_txt.focus()
        }  
    })
    
    close_pop = function (){
        var cont = $('.pop_txt').val()
        pop_say.hide()
        if($.trim(cont)=='') txt.text(txt_tip)
        else txt.text(cont)
    }

    post_say = function (){
        if(!can_say()){
            pop_tip.fadeOut(function(){pop_tip.fadeIn()})
            return false
        }
        var val=pop_txt.val()
        pop_txt.replaceWith($('<pre class="pop_txt" id="pop_txt"/>').html(val))
        pop_tip.replaceWith('<div class="say_loading pop_tip"></div>')
        $('.pop_close,.pop_submit').hide()
        $.postJSON(
            '/j/po/word',
            {
                "txt":val
            },
            function(){
                $('.pop_tip').replaceWith('<div class="pop_ok pop_tip">发表成功</div>')
                var pop_ok = $('.pop_ok')  
                pop_ok.fadeIn(function(){
                    location="/word"
                })
            }
        )
    }
})




function fav(){
    if(!islogin())return;
    fancybox_word(
        '备注 :',
        '/j/fav',
        function(){
            $("#fav_a").text('设置').attr('href','/mark')
        },
        function(){return 1} 
    )
}
