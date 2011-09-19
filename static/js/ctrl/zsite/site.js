
$(function(){
    var say = $('.say')
    var pop_say = $(".pop_say")
    var txt = $('.say_txt')
    var pop_txt = $('.pop_txt')
    var txt_tip = txt.text()
    var  pop_tip = $('.pop_tip') 
    can_say = txt_maxlen(pop_txt,pop_tip,142)

    txt.click(function(){
        if(pop_say.css("display")=='none'){
            pop_say.css("display","block")
        }  
    })
    
    close_pop = function (){
        var cont = $('.pop_txt').val()
        pop_say.css('display','none')
        if($.trim(cont)=='') txt.text(txt_tip)
        else txt.text(cont)
    }

    post_say = function (){
        if(!can_say()){
            pop_tip.fadeOut(function(){pop_tip.fadeIn()})
            return false
        }
        pop_txt.replaceWith($('<pre class="pop_txt" id="pop_txt"/>').html(pop_txt.val()))
        pop_tip.replaceWith('<div class="say_loading pop_tip"></div>')
        $('.pop_close,.pop_submit').hide()
        $.postJSON(
            '/j/po/word',
            {
                "txt":pop_txt.val()
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
